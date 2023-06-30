# Enhancing Cybersecurity Situational Awareness through Human-Centric Visualization

## Project Aim

The goal of this project is to improve cybersecurity situational awareness by developing a prototype software tool that utilizes human-centric visualization. Situational awareness is crucial for identifying and mitigating security risks in various domains. By employing visualizations, the tool aims to provide effective insights into large volumes of data, allowing non-experts in cybersecurity to explore the cybersecurity landscape and make informed decisions. The prototype software tool consists of two main functions: (1) collecting, storing, and preprocessing heterogeneous cybersecurity data such as logs, machine-readable data, and text, and (2) presenting the processed cybersecurity data in a human-centric format supported by visualizations. The target users of this tool are individuals without expertise in cybersecurity, who will be able to analyze vast amounts of data, detect trends and unexpected events, and take proactive actions.

## Related Literature

To explore further research in this area, you can refer to the following literature:

- [Literature review](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9782400)

### Technical papers

- [Conceptual Model of Visual Analytics for Hands-on Cybersecurity Training](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9018081)
- [Enhancing Cyber Situation Awareness for Non-Expert Users using Visual Analytics](https://uwe-repository.worktribe.com/preview/920729/cybersa_final.pdf)

## Technical Information

The application is broken down into 3 major components, prepare, store, visualise.

<img width="500px" src="./docs/Cyber%20Situational%20Awarenesss%20Visualisation.png" alt="Cyber Situational Awareness Visualisation"/>

Each component feeds into the next, transforming the data, storing the data, and then visualising the data. An event-based pipeline architecture works well for this type of system as the data is taken into the pipeline and each component transforms the data until it is stored in the database. Once it is stored, the user interface can visualise the data however it requires.

<img width="500px" alt="Architecture diagram" src="./docs/Cyber%20Situational%20Awareness%20Architecture.png"/>

The preparation stage consists of ingesting heterogeneous data and standardising it for use by the rest of the application. This is the only part of the system that can modify the data; once it is past this stage the data is immutable.

For this application the standard I chose to use is the [STIX 2.1 standard](https://oasis-open.github.io/cti-documentation/stix/intro.html). Structured Threat Information Expression (STIX) is a language and serialization format used to exchange cyber threat intelligence (CTI) information. It is completely open source, developed and supported by leading members of the cybersecurity industry. STIX is broken up into different types of objects, each having standard relationships with other types of STIXs objects. For example, `malwares` can `exploit` certain `vulnerabilities`.

The below diagram visualises the relationships between a few of the central STIX objects.

<img width="500px" alt="STIX 2.1 flow diagram" src="./docs/STIX%202.1%20Flow.png"/>

The preparation stage uses processor plugins to ingest data from a source (a network, an external API, a [TAXII](https://oasis-open.github.io/cti-documentation/taxii/intro.html) server, etc.) and converts them into STIX compatible objects. These processors can be run on any cadence that they set for themselves, i.e. pulling daily vulnerabilities might run as a daily cron job however pulling in network data might happen continously. Once these processors have converted the raw data, it pushes it onto a queue for further handling. Each of the processors can use whatever language best fits the processor (most of the OOtB plugins use python), as the plugins are decoupled from each other and the rest of the system.

The storing stage has workers that continously pull data from the queue of STIX objects, validating them, and adding them to the database. This uses the [competing consumer pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/competing-consumers), allowing for scalability, availability, and higher throughput. The ordering of the messages is not guaranteed, but it does not affect the system given the context.

The final stage is visualisation. This stage reads the data from the database and displays it on the dashboard in different components. The OOtB components are a network (node-edge) graph, time graph, geolocation graph, and malicious sighting calendar. These could be extended based on the available data. A component that I want to add is a course of action recommendation component for vulnerabilities that exist in the infrastructure. This would require additional information about the infrastructure and its vulnerabilities, but given the extensability of the plugins, it is entirely possible to add.
