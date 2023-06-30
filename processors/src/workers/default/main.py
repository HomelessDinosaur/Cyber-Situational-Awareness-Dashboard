#!/usr/bin/env python3
from dataclasses import replace
import json
import os

import pymongo
from stix2validator import validate_string
from stix2 import Bundle
from zeit3101helpers import Helper

conn_str = f"mongodb://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@db:27017/?retryWrites=true&w=majority"


class Worker:
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
        if Worker.validate(bundle):
            new_bundle = []
            ips = []
            for obj in bundle.objects:
                document = json.loads(obj.serialize())
                if document["type"] == "ipv4-addr":
                    ips.append(document)

            replace_ips = {}
            for ip in ips:
                db_ip = self.db["ipv4-addr"].find_one({"value": ip["value"]})
                if db_ip is not None:
                    replace_ips[ip["id"]] = db_ip["id"]
                else:
                    new_bundle.append(ip)

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
            for obj in new_bundle:
                self.db[obj["type"]].insert_one(obj)

    @staticmethod
    def validate(bundle: Bundle) -> bool:
        result = validate_string(bundle.serialize())
        return result.is_valid


if __name__ == "__main__":
    worker = Worker()
    worker.listen()
