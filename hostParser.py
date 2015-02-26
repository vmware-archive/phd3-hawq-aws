__author__ = 'dbaskette'
import json

def parseAmbariHosts():
    # Parse ambari-hosts.txt and pull out agent hostnames

    jsonString=""
    jsonFound = False
    hostNames=[]
    with open("./ambari-hosts.txt","r") as hostsFile:
        for line in hostsFile:
            if "{" in line:
                jsonFound = True
            if jsonFound:
                jsonString = jsonString + line
        jsonString = jsonString[:-1]
    for items in json.loads(jsonString)["items"]:
        hostNames.append(items["Hosts"]["host_name"])
    return hostNames

def parseBlueprint(numHosts):
    # Parse Blueprint to pull out Groups and # hosts per

    groupsArray=[]
    with open(str(numHosts)+"-node-blueprint.json","r") as blueprintFile:
        bluePrint = json.load(blueprintFile)
        for groups in bluePrint["host_groups"]:
            groupsArray.append(groups["cardinality"]+":"+groups["name"])
        return groupsArray

def buildHostMappingTemplate(hostNames,groups):
    # Assign Hosts to groups

    template = "{\n\"blueprint\": \"blueprint-phd-multinode-basic\",\n\"default_password\": \"super-secret-password\",\n\"host_groups\": [\n"
    i=0
    hostGroup = []
    for group in groups:
        for hostCount in range(int(group.split(":")[0])):
            hostInfo = {}
            hostInfo["hostname"] = hostNames[i]
            hostInfo["group"] = group.split(":")[1]
            hostGroup.append(hostInfo)
            i += 1
    groupInfo={}
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

if __name__ == '__main__':
    hostNames =parseAmbariHosts()
    groups = parseBlueprint(len(hostNames)-1)
    buildHostMappingTemplate(hostNames,groups)