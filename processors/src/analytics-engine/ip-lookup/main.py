#!/usr/bin/env python3
import datetime
import json
from time import sleep
import requests
import pymongo
import os
from stix2validator import validate_string
from stix2 import Bundle, Sighting, Location, Relationship, Indicator
from zeit3101helpers import Helper

conn_str = f"mongodb://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@db:27017/?retryWrites=true&w=majority"


class IpLookup:
    def __init__(self):
        self.helper = Helper(hostname="queue")
        self.client = pymongo.MongoClient(
            conn_str, serverSelectionTimeoutMS=5000
        )
        self.db = self.client["realtime"]

    def listen(self):
        print("Pushing data...")
        self.helper.consume_stix(self.process_message)

    def process_message(self, bundle: Bundle):
        print(bundle)
        if IpLookup.validate(bundle):
            for obj in bundle.objects:
                document = json.loads(obj.serialize())

                if document["type"] == "ipv4-addr":
                    if not document["value"].startswith("192.168"):
                        exists = self.db["ip-lookup"].find_one(
                            {"id": document["value"]}
                        )
                        if exists is None:
                            while True:
                                url = f"https://www.virustotal.com/api/v3/ip_addresses/{document['value']}"

                                headers = {
                                    "accept": "application/json",
                                    "x-apikey": os.environ.get(
                                        "VIRUSTOTAL_API_KEY"
                                    ),
                                }

                                response = requests.get(url, headers=headers)

                                if response.status_code == 200:
                                    break

                                sleep(10000)

                            response = response.json()

                            print(response)

                            country = response["data"]["attributes"].get(
                                "country"
                            )
                            location = Location(
                                country=country
                                if country is not None
                                else "UNKNOWN"
                            )
                            self.db["location"].insert_one(
                                json.loads(location.serialize())
                            )

                            relationship = Relationship(
                                relationship_type="originates-from",
                                source_ref=document["id"],
                                target_ref=location["id"],
                            )
                            self.db["relationship"].insert_one(
                                json.loads(relationship.serialize())
                            )

                            malicious = IpLookup.is_malicious(
                                response["data"]["attributes"][
                                    "last_analysis_stats"
                                ]
                            )
                            indicator = Indicator(
                                pattern=f"[ipv4-addr:value = '{document['value']}']",
                                pattern_type="stix",
                                valid_from=datetime.datetime.now(
                                    datetime.timezone.utc
                                ),
                            )

                            self.db["ip-lookup"].insert_one(
                                {
                                    "id": document["value"],
                                    "malicious": malicious,
                                    "indicator-ref": indicator["id"]
                                    if malicious
                                    else "",
                                }
                            )

                            if malicious:
                                self.db["indicator"].insert_one(
                                    json.loads(indicator.serialize())
                                )
                                sighting = Sighting(
                                    sighting_of_ref=indicator["id"]
                                )
                                self.db["sighting"].insert_one(
                                    json.loads(sighting.serialize())
                                )
                        else:
                            if exists["malicious"]:
                                sighting = Sighting(
                                    sighting_of_ref=exists["indicator-ref"]
                                )
                                self.db["sighting"].insert_one(
                                    json.loads(sighting.serialize())
                                )

    @staticmethod
    def is_malicious(analysis_stats: dict):
        if analysis_stats["malicious"] > 5:
            return True

        if (
            analysis_stats["malicious"] != 0
            and analysis_stats["suspicious"] != 0
        ):
            total = (
                analysis_stats["malicious"]
                + analysis_stats["suspicious"]
                + analysis_stats["harmless"]
            )

            if (
                analysis_stats["malicious"] + analysis_stats["suspicious"]
            ) / total > 0.05:
                return True

        return False

    @staticmethod
    def validate(bundle: Bundle) -> bool:
        result = validate_string(bundle.serialize())
        return result.is_valid


if __name__ == "__main__":
    lookup = IpLookup()
    lookup.listen()
