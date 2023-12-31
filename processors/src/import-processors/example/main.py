from time import sleep
from ...helper.main import Helper
from stix2 import Indicator, Malware, Relationship, Bundle

indicator = Indicator(
    id="indicator--a932fcc6-e032-476c-826f-cb970a5a1ade",
    created="2014-02-20T09:16:08.989Z",
    modified="2014-02-20T09:16:08.989Z",
    name="File hash for Poison Ivy variant",
    description="This file hash indicates that a sample of Poison Ivy is present.",
    indicator_types=["malicious-activity"],
    pattern="[file:hashes.'SHA-256' = 'ef537f25c895bfa782526529a9b63d97aa631564d5d789c2b765448c8635fb6c']",
    pattern_type="stix",
    valid_from="2014-02-20T09:00:00.000000Z",
)

malware = Malware(
    id="malware--fdd60b30-b67c-41e3-b0b9-f01faf20d111",
    created="2014-02-20T09:16:08.989Z",
    modified="2014-02-20T09:16:08.989Z",
    name="Poison Ivy",
    malware_types=["remote-access-trojan"],
    is_family="false",
)

relationship = Relationship(indicator, "indicates", malware)

bundle = Bundle(objects=[indicator, malware, relationship])


class ExampleProcessor:
    def start():
        sleep(1)
        print("Pushing data...")
        Helper.send_stix_bundle(bundle)


if __name__ == "__main__":
    ExampleProcessor.start()
