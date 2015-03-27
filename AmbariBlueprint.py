__author__ = 'dbaskette'

import json
import socket
import argparse

import boto
import boto.s3.connection
from boto.s3.key import Key
import requests
from requests.auth import HTTPBasicAuth


def parseAmbariHosts():
    # Parse ambari-hosts.txt and pull out agent hostnames

    # jsonString = ""
    # jsonFound = False
    # hostNames = []
    # with open("./ambari-hosts.txt", "r") as hostsFile:
    # for line in hostsFile:
    #         if "{" in line:
    #             jsonFound = True
    #         if jsonFound:
    #             jsonString = jsonString + line
    #             # jsonString = jsonString[:-1]
    # for items in json.loads(jsonString)["items"]:
    #     hostNames.append(items["Hosts"]["host_name"])
    hostNames = []
    with open("ambariAgents.txt", "r") as agentFile:
        for host in agentFile:
            hostNames.append(str(host).strip())


    return hostNames

def parseBlueprint(blueprintName):
    # Parse Blueprint to pull out Groups and # hosts per

    groupsArray = []
    with open(blueprintName + ".json", "r") as blueprintFile:
        bluePrint = json.load(blueprintFile)
        for groups in bluePrint["host_groups"]:
            groupsArray.append(groups["cardinality"] + ":" + groups["name"])
        return groupsArray



        # ,
        #       {
        #          "hosts": [
        #             {
        #                "fqdn": "${machines[0]}"
        #           }
        #      ],
        #     "name": "gateway"
        #}

def buildHostMappingTemplate(hostNames, groups, blueprintName):
    # Assign Hosts to groups

    hostNames.remove(socket.getfqdn())
    template = "{\n\"blueprint\": \"" + str(
        blueprintName) + "\",\n\"default_password\": \"super-secret-password\",\n\"host_groups\": [\n"
    i = 0
    hostGroup = []
    gateway = socket.getfqdn()
    gatewayString = "{\"hosts\": [ {\"fqdn\": \"" + socket.getfqdn() + "\"} ],\"name\": \"gateway\"}"
    print gatewayString
    for group in groups:
        if "gateway" not in group:
            for hostCount in range(int(group.split(":")[0])):
                hostInfo = {}
                hostInfo["hostname"] = hostNames[i]
                hostInfo["group"] = group.split(":")[1]
                hostGroup.append(hostInfo)
                i += 1
    print hostGroup

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
        hostsString = hostsString + gatewayString
        hostsString = hostsString + "\n]\n}"
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


def buildHostsFile(hostNames, awsKey, secretKey, stacks):
    print "Build /etc/hosts"
    print hostNames
    with open("/etc/hosts", "a") as hostsFile:
        for host in hostNames:
            hostIP = ""
            hostIP = str(host.split(".")[0])[3:].replace("-", ".")
            hostsFile.write(hostIP + "     " + host + "\n")

    bucketName = str(stacks) + "-ambari-repo"
    try:
        conn = boto.connect_s3(aws_access_key_id=awsKey, aws_secret_access_key=secretKey)
        bucket = conn.get_bucket(bucketName)
        print bucket
        k = Key(bucket)
        k.key = 'hosts'
        k.set_contents_from_filename("/etc/hosts")
        k.set_canned_acl('private')
    except Exception as e:
        pass


def cliParse():
    VALID_ACTION = ["install", "hosts"]
    parser = argparse.ArgumentParser(description='Amazon S3 Upload')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_hosts = subparsers.add_parser("hosts", help="Upload hostsfile from S3")
    parser_hosts.add_argument("--key", dest='accessKey', action="store", help="Your access key", required=False)
    parser_hosts.add_argument("--secret", dest='secretKey', action="store", help="Your Secret key", required=False)
    parser_hosts.add_argument("--stack", dest='stack', action="store", help="StackName", required=False)

    parser_install = subparsers.add_parser("install", help="Install with Blueprint")

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = cliParse()
    print args.subparser_name
    if (args.subparser_name == "install"):

        hostNames = parseAmbariHosts()

        blueprintName = str(len(hostNames) - 1) + "-node-blueprint"
        groups = parseBlueprint(blueprintName)
        # buildHostMappingTemplate(hostNames, groups, len(hostNames) - 1)
        buildHostMappingTemplate(hostNames, groups, blueprintName)
        url = "http://localhost:8080/api/v1"
        applyBlueprint(url, blueprintName)
    elif (args.subparser_name == "hosts"):
        print "hosts"
        hostNames = parseAmbariHosts()
        buildHostsFile(hostNames, args.accessKey, args.secretKey, args.stack)
