# Malpedia API by Gilly Inbus supported by Saksit Wilamat
import requests
import json
import datetime
from stix2 import (Indicator, Relationship, ThreatActor, Bundle)

'''
#This will get us our requested API Information, a single request
Input = "file/6c5360d41bd2b14b1565f5b18e5c203cf512e493/analysis"
cveInput = "cve/CVE-2014-0160/general"
nidInput = "nids/2820184/general"
urlInput = "url/http://www.fotoidea.com/sport/4x4_san_ponso/slides/IMG_0068.html/url_list"
Req = requests.get('https://otx.alienvault.com/api/v1/indicators/' + urlInput)

#connection response check
#print(Req)
#print out detail
#print(Req.text)
#convert into json formatting
data = json.loads(Req.text)
#print(json.dumps(data, indent=2))

#Once we have seen the JSON request format, we can then structure our queries to gather specific information
#print(json.dumps(data["base_indicator"]["id"], indent=2))

#The code above retrieves the since value in the request API data in a nested JSON format
#print(json.dumps(data["pulse_info"]["pulses"][0], indent=2))

#description = str(data["base_indicator"]["description"])
#print(description)

indicator = Indicator(
    pattern = str(data["url_list"][0]["result"]["urlworker"]["http_response"]["CONTENT-TYPE"]),
    pattern_type = str(data["url_list"][0]["result"]["urlworker"]["http_response"]["VARY"]),
#    valid_from = datetime(data["url_list"][0]["result"]["urlworker"]["http_response"]["DATE"]),
    description = str(data["url_list"][0]["result"]["urlworker"]["filemagic"]) + "More information can be found here:" + str(data["url_list"][0]["url"]),
)
print(indicator)

threatActor = ThreatActor(
    name = str(data["net_loc"]),
)
#print(threatActor)

relationship = Relationship(
    indicator,'indicates', threatActor
)

bundle = Bundle(objects=[indicator,threatActor,relationship])
#print(bundle)
'''

#Multi request
#'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt' for ip actor list
MultiReq = requests.get('https://www.binarydefense.com/banlist.txt')
#print(MultiReq.text)

#make a list out of MultiReq data
def stringToList(string):
    listMultiReq = list(string.split("\n"))
    return listMultiReq

MultiReqList = stringToList(MultiReq.text)
#print(MultiReqList[14])

i = 15

for each in MultiReqList:
    #print(i)
    print(str(MultiReqList[i]))
    indicatorURL = requests.get('https://otx.alienvault.com/api/v1/indicators/IPv4/' + MultiReqList[i])
    #print(indicatorURL.text)
    textload = json.loads(indicatorURL.text)
    textprint = json.dumps(textload, indent=2)
    #print(textprint)
    #print(textload["pulse_info"]["count"])
    #each data within each ip address
    a = range(0, (textload["pulse_info"]["count"]))
    #print(a)
    for x in a:
        #print(x)
        #make the Indicator object
        try:
            indicator = Indicator(
                name = str(textload["indicator"]) + " - " + str(textload["pulse_info"]["pulses"][x]["name"]),
                pattern = str(textload["pulse_info"]["pulses"][x]["id"]),
                pattern_type = str(textload["pulse_info"]["pulses"][x]["related_indicator_type"]),
                #valid_from = datetime(textload["pulse_info"]["pulses"][0]["created"]),
                description = str(textload["pulse_info"]["pulses"][x]["description"]) + "More information can be found here:" + str(textload["pulse_info"]["pulses"][x]["references"])
            )
        #no description found
        except:
            print("No description found in indicatorURL = " + str(textload))
        print(indicator)
        x = x +1

    # make the ThreatActor object
    try:
        threatActor = ThreatActor(
            name = str(textload["indicator"]),
        )
    # no description found
    except:
        print("No description found in ActorID = " + str(textload))
    # print(threatActor)

    # make the Relationship object
    relationship = Relationship(
        indicator,'indicates', threatActor
    )

    bundleMulti = Bundle(objects=[indicator,threatActor,relationship])
    print(bundleMulti)
    i = i+1
