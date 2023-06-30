# Malpedia API by Gilly Inbus supported by Saksit Wilamat
import requests
import json
from stix2 import (ThreatActor, Relationship, Identity, Bundle)

"""
#This will get us our requested API Information, a single request

req = requests.get('https://malpedia.caad.fkie.fraunhofer.de/api/get/actor/allanite')

#Req is now storing our API information in JSON Format
#We need to convert our the stored information in Req into text because we want to first see the JSON request format for the API
#This is because we can then extract specific information about it and used only that in our stix2 format scenario
data = json.loads(req.text)

#print(json.dumps(data, indent=2))

#Once we have seen the JSON request format, we can then structure our queries to gather specific information
#print(json.dumps(data["meta"]["since"], indent=2))

#The code above retrieves the since value in the request API data in a nested JSON format

#print(data["meta"]["synonyms"][0])
#The code above retrieves data from a Neested JSON request with multiple values, you can select [0] or have not index selected and it will get you all the values

#The code below retrieves data that is the description
#description = str(data["description"])
#print(description)

threatActor = ThreatActor(
    name = str(data["families"]),
    description = str(data["description"]) + "More information can be found here:" + str(data["meta"]["refs"]),
)
identity = Identity(
    name="Threat Ref.",
    description="Represent identified vulnerability sources. More information can be found here:" + str(data["meta"]["refs"]),
)
relationship = Relationship(
    identity,'indentify', threatActor
)

bundle = Bundle(objects=[threatActor,identity,relationship])
#print(bundle)
"""

# Used to search for muliple types of Malpedia
#List of Actor
MultiReq = requests.get('https://malpedia.caad.fkie.fraunhofer.de/api/list/actors')
print(MultiReq.text)
MultiReqList = json.loads(MultiReq.text)
print(MultiReqList)
#print(json.dumps(MultiReqList, indent=2))
#print(str(MultiReqList))
i = 0

#Get meta data actor from the list
for each in MultiReqList:
    #print(str(MultiReqList[i]))
    ActorID = requests.get('https://malpedia.caad.fkie.fraunhofer.de/api/get/actor/' + MultiReqList[i])
    #print(ActorID.text)
    textload = json.loads(ActorID.text)
    textprint = json.dumps(textload, indent=2)
    #print(textprint)

    #make the ThreatActor object
    try:
        threatActor = ThreatActor(
            name=str(textload["families"]),
            description=str(textload["description"]) + "More information can be found here:" + str(
                textload["meta"]["refs"]) + "The Malpedia Value: " + str(textload["value"]),
        )
    #no description found
    except:
        print("No description found in ActorID = " + str(textload))
    #print(threatActor)

    # make the Identity object
    try:
        identity = Identity(
            name="Threat Ref.",
            description="Threat's UUID: " + str(
                textload["uuid"])
        )
    except:
        print("No UUID found in ActorID = " + str(textload))

    # make the Relationship object
    relationship = Relationship(
        identity, 'Indentify', threatActor
    )

    bundleMulti = Bundle(objects=[threatActor, identity, relationship])
    print(bundleMulti)
    i = i+1

