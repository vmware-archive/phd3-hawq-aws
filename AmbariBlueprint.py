__author__ = 'dbaskette'

import json
import socket

import requests
from requests.auth import HTTPBasicAuth


def parseAmbariHosts():
    # Parse ambari-hosts.txt and pull out agent hostnames

    jsonString = ""
    jsonFound = False
    hostNames = []
    with open("./ambari-hosts.txt", "r") as hostsFile:
        for line in hostsFile:
            if "{" in line:
                jsonFound = True
            if jsonFound:
                jsonString = jsonString + line
                # jsonString = jsonString[:-1]
    for items in json.loads(jsonString)["items"]:
        hostNames.append(items["Hosts"]["host_name"])
    print hostNames
    return hostNames

def parseBlueprint(blueprintName):
    # Parse Blueprint to pull out Groups and # hosts per

    groupsArray = []
    with open(blueprintName + ".json", "r") as blueprintFile:
        bluePrint = json.load(blueprintFile)
        for groups in bluePrint["host_groups"]:
            groupsArray.append(groups["cardinality"] + ":" + groups["name"])
        return groupsArray


def buildHostMappingTemplate(hostNames, groups, blueprintName):
    # Assign Hosts to groups
    template = "{\n\"blueprint\": \"" + str(
        blueprintName) + "\",\n\"default_password\": \"super-secret-password\",\n\"host_groups\": [\n"
    i = 0
    hostGroup = []
    for group in groups:
        for hostCount in range(int(group.split(":")[0])):
            hostInfo = {}
            hostInfo["hostname"] = hostNames[i]
            hostInfo["group"] = group.split(":")[1]
            hostGroup.append(hostInfo)
            i += 1
    groupInfo = {}
    for host in hostGroup:
        try:
            currentVal = groupInfo[host["group"]]
            groupInfo[host["group"]] = currentVal + ":" + host["hostname"]
        except:
            currentVal = ""
            groupInfo[host["group"]] = host["hostname"]

    hostsString = ""
    with open("./hostmapping-template.json", "w") as templateFile:
        templateFile.write(template)
        for group in groupInfo:
            hostsString = hostsString + "{\n\"hosts\": [\n "
            hosts = str(groupInfo[group]).split(":")
            for host in hosts:
                hostsString = hostsString + "{\"fqdn\": \"" + host + "\"},"
            hostsString = hostsString[:-1] + "\n"
            hostsString = hostsString + "],"

            hostsString = hostsString + "\"name\": " + "\"" + group + "\"}\n ,"
        hostsString = hostsString[:-1] + "\n]\n}"
        templateFile.write(hostsString)

def applyBlueprint(url, blueprintName):
    print "ApplyBlueprint"
    fileName = str(blueprintName) + ".json"
    postURL = str(url) + "/blueprints/" + str(blueprintName) + "?validate_topology=false"
    auth = HTTPBasicAuth('admin', 'admin')
    headers = {'X-Requested-By': 'Heffalump'}
    fileHandle = open(fileName, "rb")
    response = requests.post(postURL, auth=auth, data=fileHandle, headers=headers)
    fileHandle2 = open("hostmapping-template.json")
    postURL2 = str(url) + "/clusters/PHDCluster"
    response2 = requests.post(postURL2, auth=auth, data=fileHandle2, headers=headers)

    print response.text
    print response2.text


def setRepo():
    print "setRepo"
    # READ REPO FILES AND BUILD THEM
    hostName = socket.getfqdn()
    payload = {"Repositories": {"base_url": hostName + "/PHD/"}}
    headers = {'X-Requested-By': 'Heffalump'}
    auth = HTTPBasicAuth('admin', 'admin')
    url = "http://" + hostName + ":8080/api/v1/stacks/PHD/versions/3.0/operating_systems/redhat6/repositories/PHD-3.0"
    requests.put(url, auth=auth, headers=headers, data=payload)





if __name__ == '__main__':
    hostNames = parseAmbariHosts()
    blueprintName = str(len(hostNames) - 1) + "-node-blueprint"
    groups = parseBlueprint(blueprintName)
    # buildHostMappingTemplate(hostNames, groups, len(hostNames) - 1)
    buildHostMappingTemplate(hostNames, groups, blueprintName)
    url = "http://localhost:8080/api/v1"
    applyBlueprint(url, blueprintName)
    print "blueprint"
