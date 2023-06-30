import nvdlib
import os
from stix2 import Vulnerability, Relationship, CourseOfAction, Bundle
from zeit3101helpers import Helper


class CVEProcessor:
    def __init__(self):
        self.helper = Helper(hostname="localhost")

    def start(self) -> None:
        print("Pushing data...")
        self.send_stix_bundles()
        print("Collected all data")

    def send_stix_bundles(self) -> None:
        # Used to search for muliple types of CVE's https://nvdlib.com/en/latest/CVE.html#searching-cves for doco
        response = nvdlib.searchCVE(
            pubStartDate="2022-04-1 00:00",
            keyword="windows",
            pubEndDate="2022-07-10 00:00",
            cvssV3Severity="HIGH",
            key=os.getenv("CVE_API_KEY"),
            limit=5,
        )

        for cve in response:
            bundle = CVEProcessor.process_cve(cve)

            self.helper.send_stix_bundle(bundle)

    @staticmethod
    def process_cve(cve) -> Bundle:
        vulnerability = Vulnerability(
            name=str(cve.id),
            description=str(cve.cve.description.description_data[0].value)
            + "More information can be found here:"
            + str(cve.url)
            + "The CVS SCORE: "
            + str(cve.v3score),
        )
        course_of_action = CourseOfAction(
            name="Update software",
            description="It is recommended you update the software of the that contains the identified vulnerability. More information can be found here:"
            + str(cve.url),
        )
        relationship = Relationship(
            course_of_action, "mitigates", vulnerability
        )
        return Bundle(objects=[vulnerability, course_of_action, relationship])


if __name__ == "__main__":
    CVEProcessor.start()
