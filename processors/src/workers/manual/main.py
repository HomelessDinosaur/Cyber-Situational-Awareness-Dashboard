#!/usr/bin/env python3
from dataclasses import replace
import datetime
import json
import os
import csv
from random import randint
import pymongo

from stix2validator import validate_string
from stix2 import (
    Bundle,
    NetworkTraffic,
    IPv4Address,
    Sighting,
    Relationship,
    Location,
    Indicator,
    Infrastructure,
    parse,
)

conn_str = f"mongodb://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@db:27017/?retryWrites=true&w=majority"


class ManualWorker:
    def __init__(self):
        self.client = pymongo.MongoClient(
            conn_str, serverSelectionTimeoutMS=60000
        )
        self.db = self.client["highrisk"]

    def already_initialised(self) -> bool:
        initialised = self.db["network-traffic"].count_documents({}) > 200
        print("Already Initialised? ", initialised)
        return initialised

    def listen(self):
        print("Procesing High Risk Data...")
        bundles = self.process_data()
        print("Pushing bundles...")
        for b in bundles:
            self.process_message(b)

    def process_data(self):
        bundles = []
        with open("high_risk.csv", newline="") as f:
            high_risk_data = csv.reader(f, delimiter=",")
            for row in high_risk_data:
                try:
                    # information about the source ip address
                    src_internet_protocolV4 = IPv4Address(value=row[0])
                    # information about the destination ip address
                    des_internet_protocolV4 = IPv4Address(value=row[2])
                    # creating a network packet in the Stix 2.1
                    network_traffic = NetworkTraffic(
                        start=datetime.datetime.now().replace(
                            hour=randint(0, 23)
                        ),
                        is_active=False,
                        src_ref=src_internet_protocolV4,
                        dst_ref=des_internet_protocolV4,
                        src_port=row[1],
                        dst_port=row[3],
                        protocols="ipv4, " + row[4],
                    )

                    location = Location(
                        country=["CHI", "RUS"][randint(0, 1)]
                        if row[8] == "attack"
                        else ["AUS", "USA"][randint(0, 1)]
                    )

                    if row[8] == "attack":
                        relationship = Relationship(
                            relationship_type="originates-from",
                            source_ref=src_internet_protocolV4["id"],
                            target_ref=location["id"],
                        )

                        indicator = Indicator(
                            pattern=f"[ipv4-addr:value = '{row[0]}']",
                            pattern_type="stix",
                            valid_from=datetime.datetime.now(
                                datetime.timezone.utc
                            ),
                        )
                        sighting = Sighting(sighting_of_ref=indicator["id"])

                        bundles.append(
                            Bundle(
                                objects=[
                                    src_internet_protocolV4,
                                    des_internet_protocolV4,
                                    network_traffic,
                                    sighting,
                                    indicator,
                                    location,
                                    relationship,
                                ]
                            )
                        )
                    else:
                        bundles.append(
                            Bundle(
                                objects=[
                                    src_internet_protocolV4,
                                    des_internet_protocolV4,
                                    network_traffic,
                                ]
                            )
                        )
                except Exception as e:
                    print(row)
                    print(e)
        return bundles

    def process_message(self, bundle: Bundle):
        if ManualWorker.validate(bundle):
            new_bundle = []
            ips = []
            # Get all ips out of the bundle
            for obj in bundle.objects:
                document = json.loads(obj.serialize())
                if document["type"] == "ipv4-addr":
                    ips.append(document)

            # Find all the ips that already exist in the database
            replace_ips = {}
            for ip in ips:
                db_ip = self.db["ipv4-addr"].find_one({"value": ip["value"]})
                if db_ip is not None:
                    replace_ips[ip["id"]] = db_ip["id"]
                else:
                    new_bundle.append(ip)

            # Replace any existing IPs in the bundle with the IPs that need to be replaced
            for obj in bundle.objects:
                document = json.loads(obj.serialize())
                for key in document:
                    try:
                        if type(document[key]) == list:
                            continue
                        if document[key] in replace_ips.keys():
                            document[key] = replace_ips[document[key]]
                    except KeyError:
                        continue
                if document["type"] != "ipv4-addr":
                    new_bundle.append(document)

            print(new_bundle)
            # Add bundle to the database
            for obj in new_bundle:
                if obj["type"] == "ipv4-addr" and obj["value"].startswith(
                    "192.168"
                ):
                    infrastructure = Infrastructure(name="Device")
                    self.db["infrastructure"].insert_one(
                        json.loads(infrastructure.serialize())
                    )

                    # Relationship describing the infrastructure to the ipv4address
                    relationship = Relationship(
                        infrastructure, "has", parse(obj)
                    )
                    self.db["relationship"].insert_one(
                        json.loads(relationship.serialize())
                    )
                self.db[obj["type"]].insert_one(obj)

    @staticmethod
    def validate(bundle: Bundle) -> bool:
        result = validate_string(bundle.serialize())
        return result.is_valid


if __name__ == "__main__":
    worker = ManualWorker()
    if not worker.already_initialised():
        worker.listen()
