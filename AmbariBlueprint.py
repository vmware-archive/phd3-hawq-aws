__author__ = 'dbaskette'

import json

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
    print str(url) + "/blueprints/" + str(blueprintName) + "?validate_topology=false -d " + str(blueprintName) + ".json"

    req = requests.post(url + "/blueprints/" + blueprintName + "?validate_topology=false -d " + blueprintName + ".json",
                        auth=HTTPBasicAuth('admin', 'admin'))
    preq = requests.post(url + "clusters/PHDCluster -d @hostmapping-template.json",
                         auth=HTTPBasicAuth('admin', 'admin'))
    # Testing just the blueprint post

    # "curl -u admin:admin -H 'X-Requested-By:dbaskette' -X POST http://$MY_IP:8080/api/v1/clusters/PivCluster -d @hostmapping-template.json >>phd.log\n"
    # "curl -u admin:admin -H 'X-Requested-By:dbaskette' -X POST http://$MY_IP:8080/api/v1/blueprints/blueprint-phd-multinode-basic?validate_topology=false -d @blueprint.json >> phd.log\n",


if __name__ == '__main__':
    hostNames = parseAmbariHosts()
    blueprintName = str(len(hostNames) - 1) + "-node-blueprint"
    groups = parseBlueprint(blueprintName)
    # buildHostMappingTemplate(hostNames, groups, len(hostNames) - 1)
    buildHostMappingTemplate(hostNames, groups, blueprintName)

    url = "http://localhost:8080/api/v1"
    applyBlueprint(url, blueprintName)
    print "blueprint"