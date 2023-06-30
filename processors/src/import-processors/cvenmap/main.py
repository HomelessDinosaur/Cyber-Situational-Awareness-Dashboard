import os
import nmap3
import json
import socket
import nvdlib
from stix2 import (
    Infrastructure,
    Relationship,
    IPv4Address,
    Bundle,
    Software,
    Vulnerability,
    CourseOfAction,
)
from zeit3101helpers import Helper
import netifaces as ni


class NmapProcessor:
    def __init__(self):
        self.active_hosts = []
        network_address = NmapProcessor.get_ip_address(
            os.environ.get("MAIN_INTERFACE", "eth0")
        )
        self.network_address = ".".join(network_address.split(".")[:-1] + [""])
        self.__discover_hosts()
        self.helper = Helper(hostname="localhost")

    @staticmethod
    def get_ip_address(ifname: str):
        return ni.ifaddresses(ifname)[ni.AF_INET][0]["addr"]

    def start(self):
        print("Pushing data...")
        self.send_stix_bundles()
        print("Collected all data")

    def send_stix_bundles(self):
        self.__os_detection()

    # Host Discovery Scan, used to discover only active hosts on the network.
    def __discover_hosts(self):
        for increment in range(1, 256):
            hosts = self.network_address + str(increment)
            nmap_port = nmap3.NmapHostDiscovery()
            host_result = nmap_port.nmap_no_portscan(hosts)
            # Prepares the dictionary result from the NMAP query
            textformat_host = json.dumps(host_result, indent=2)
            # Converts the dictionary type format result into a JSON type format
            textformat_load_host = json.loads(textformat_host)

            try:
                # if the host has the active key value in the JSON format, then add it to the active host list
                if textformat_load_host[hosts]["state"]["state"] == "up":
                    print("Active Host Found: " + hosts)
                    self.active_hosts.append(hosts)
                    # STIX Object indicating a device on a network
                    infrastructure = Infrastructure(
                        name=hosts,
                        description="Active device found on the network",
                    )
                    ipv4address = IPv4Address(value=hosts)
                    relationship = Relationship(
                        infrastructure, "has", ipv4address
                    )
                    bundle = Bundle(
                        objects=[infrastructure, ipv4address, relationship]
                    )
                    print(bundle)
            except KeyError:
                # If the host is down print it
                print("Host not active: " + hosts)

    # OS detection, useful for network awareness
    def __os_detection(self):
        for host in self.active_hosts:
            print("Starting Hosts OS Scan\n")
            nmap_os = nmap3.Nmap()
            # Command to scan for target OS in nmap
            os_results = nmap_os.nmap_os_detection(
                host, args="-p 22-1024 --host-timeout 2M"
            )
            # Prepares the dictionary result from the NMAP query
            textformat_os = json.dumps(os_results, indent=2)
            # Converts the dictionary type format result into a JSON type format
            textformat_load_os = json.loads(textformat_os)
            # Temp hold OS
            os_exists = ""
            try:
                if "osmatch" in textformat_load_os[host]:
                    print("HAS OS")
                    if "name" in textformat_load_os[host]["osmatch"]:
                        os_exists = textformat_load_os.get("name")
                else:
                    print("NO OS")
                    os_exists = "No OS found"
                    continue
            except KeyError:
                print("NO OS")
                continue
            infrastructure = Infrastructure(
                # Queries the specified name
                # name=textformat_load_os[each_hosts]["osmatch"][0]["name"],
                name=os_exists,
                description=textformat_load_os[host]["osmatch"],
            )
            # IPv4 address of the host
            ipv4address = IPv4Address(value=host)

            relationship = Relationship(
                infrastructure,
                "consists-of",
                ipv4address,
            )
            bundle = Bundle(
                objects=[infrastructure, ipv4address, relationship]
            )

            print(bundle)

            self.helper.send_stix_bundle(bundle)

    # Port scanning of hosts
    def __host_port_scanning(self):
        for host in self.active_hosts:
            print("Starting Hosts Port Scan\n")
            nmap_port = nmap3.NmapHostDiscovery()
            # Command to scan for target ports in nmap, args -sV scans for service version, -P targets ports in a range
            port_results = nmap_port.nmap_portscan_only(
                host, args="-p 22-1024 -sV --host-timeout 2M"
            )
            # Prepares the dictionary result from the NMAP query
            textformat_ports = json.dumps(port_results, indent=2)
            # Converts the dictionary type format result into a JSON type format
            textformat_load_ports = json.loads(textformat_ports)
            infrastructure = Infrastructure(
                name="Online Device", description="OPEN PORT FOUND"
            )
            # IPv4 address of the host
            ipv4address = IPv4Address(value=host)
            # Describes the infrastructure relationship
            relationship = Relationship(
                infrastructure,
                "consists-of",
                ipv4address,
            )
            # For loop to iterate through the JSON output and check for the specified keys
            try:
                for each_ports in textformat_load_ports[host]["ports"]:
                    located_port = Infrastructure(
                        name="Port:" + each_ports["portid"],
                        description="Active Port: " + str(each_ports),
                    )
                    # Describes the relationship of the infrastructure to the port
                    port_relationship = Relationship(
                        infrastructure, "has", located_port
                    )
                    # Creates the bundle
                    bundle = Bundle(
                        objects=[
                            infrastructure,
                            ipv4address,
                            relationship,
                            located_port,
                            port_relationship,
                        ]
                    )
                    # Print the bundle
                    print(bundle)
            except KeyError:
                print("NO PORTS ACTIVE")
                continue

    # Nmap CPE(Common Platform Enumeration) version scanning of hosts
    def __cpe_scanning(self):
        for host in self.active_hosts:
            # Network Mapping
            nmap_cpe = nmap3.Nmap()
            # Detects open ports and their versions from a home host range of 192.168.*.*, can be changed
            cpe_results = nmap_cpe.nmap_version_detection(
                host, args="-p 22-1024 --host-timeout 2M"
            )
            # Used for debugging and readability
            textformat_cpe = json.dumps(cpe_results, indent=2)
            textformat_load_cpe = json.loads(textformat_cpe)
            # Scan for CPE
            print("Starting Hosts CPE Scan\n")
            try:
                for each_hostcpes in textformat_load_cpe[host]["ports"]:
                    # Debug statements used to analyse the JSON output
                    # print(each_hostcpes["service"]["name"])
                    # print(each_hostcpes["cpe"][0]["cpe"])
                    # print(each_hostcpes["service"]["version"])

                    # Temp variables used to check if the specified JSON key exists. Done so the prevent errors
                    PRODUCT_HOLD = ""
                    CPE_HOLD = ""
                    VERSION_HOLD = ""

                    # Checks if the product key exists in the JSON output from each CPE
                    if "product" in each_hostcpes["service"]:
                        PRODUCT_HOLD = each_hostcpes["service"]["product"]
                        # print(PRODUCT_HOLD)
                    else:
                        PRODUCT_HOLD = ""

                    # Checks if the cpe key exists in the JSON output from each CPE
                    if "cpe" in each_hostcpes:
                        CPE_HOLD = each_hostcpes.get("cpe")
                    else:
                        CPE_HOLD = "CPE NOT FOUND"

                    # Checks if the version key exists in the JSON output from each CPE
                    if "version" in each_hostcpes["service"]:
                        VERSION_HOLD = each_hostcpes["service"]["version"]
                    else:
                        VERSION_HOLD = ""

                    # Print statement to improve readability
                    # print("Starting Hosts CPE Scan\n")
                    # STIX 2.1 describing the CPE software
                    software = Software(
                        name=each_hostcpes["service"]["name"]
                        + ":"
                        + PRODUCT_HOLD,
                        cpe=CPE_HOLD,
                        version=VERSION_HOLD,
                    )
                    # STIX 2.1 infrastructure object
                    infrastructure = Infrastructure(
                        name="Device", description="CPE Discovered: "
                    )
                    # Ipv4 address of the device with the CPE
                    ipv4address = IPv4Address(value=host)
                    # Relationship describing the infrastructure to the software
                    relationship = Relationship(
                        infrastructure, "has", software
                    )
                    # Relationship describing the infrastructure to the ipv4address
                    second_relationship = Relationship(
                        infrastructure, "has", ipv4address
                    )
                    # Temp statements use to hold values
                    main_course_of_action = []
                    main_vulnerability = []
                    main_relationship_course = []

                    # Used to search for muliple types of CVE's https://nvdlib.com/en/latest/CVE.html#searching-cves for doco
                    multipleResponse = nvdlib.searchCVE(
                        keyword=each_hostcpes["service"]["name"],
                        cvssV3Severity="HIGH",
                        key=os.environ.get("CVE_API_KEY"),
                        limit=5,
                    )
                    for eachCVE in multipleResponse:
                        # Gets the vulnerability and its ID
                        vulnerability = Vulnerability(
                            name=str(eachCVE.id),
                            description=str(
                                eachCVE.cve.description.description_data[
                                    0
                                ].value
                            )
                            + "More information can be found here:"
                            + str(eachCVE.url)
                            + "The CVS SCORE: "
                            + str(eachCVE.v3score),
                        )
                        # Talks about the course of action required
                        course_of_action = CourseOfAction(
                            name="Update software",
                            description="It is recommended you update the software of the that contains the identified vulnerability. More information can be found here:"
                            + str(eachCVE.url),
                        )
                        # Relationship describing the course of action to the vulnerability
                        relationship_course = Relationship(
                            course_of_action, "mitigates", vulnerability
                        )
                        # Relationship describing the software to the vulnerability
                        # link_relationship = Relationship(
                        #     software, "May have", vulnerability
                        # )
                        # Temp statements taking in values
                        main_vulnerability = vulnerability
                        main_course_of_action = course_of_action
                        main_relationship_course = relationship_course

                        # Bundle for the STIX 2.1 Objects
                        bundle = Bundle(
                            objects=[
                                software,
                                ipv4address,
                                infrastructure,
                                relationship,
                                second_relationship,
                                main_vulnerability,
                                main_course_of_action,
                                main_relationship_course,
                            ]
                        )
                        # Print statement for debugging
                        print(bundle)
                        self.helper.send_stix_bundle(bundle)

            except KeyError:
                print("NO SERVICES ACTIVE")
                continue

        print(bundle)


if __name__ == "__main__":
    processor = NmapProcessor()
    processor.start()
