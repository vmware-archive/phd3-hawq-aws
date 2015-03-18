__author__ = 'dbaskette'


# Download  Software
# Setup Repos
# Make changes for Repo Distribution
# Install Ambari-Server


import json
import argparse
import tarfile
import os

import boto
import boto.s3.connection
from simplethreads.ThreadPool import ThreadPool
import yum
import requests
from requests.auth import HTTPBasicAuth


S3Location = "http://s3.amazonaws.com/"
baseDir = "/opt/phd3/software/"


def getBucketName(fileType):
    with open("./phd3.json", "r") as phd3Files:
        fileNames = json.load(phd3Files)
        for file in fileNames:
            if file == fileType:
                return fileNames[file]
        return 0


def downloadSoftware(key, fileName):

    try:
        key.get_contents_to_filename(baseDir + fileName)
        return 0
    except Exception as e:
        # key.get_contents_to_filename("/tmp/"+fileName)
        return -1


def getSoftware(awsKey, secretKey, fileType):
    bucketName = getBucketName("bucket")
    fileNames = []
    # conn = boto.connect_s3(aws_access_key_id=awsKey, aws_secret_access_key=secretKey)
    conn = boto.connect_s3(aws_access_key_id=awsKey, aws_secret_access_key=secretKey)

    pool = ThreadPool(10)
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)
    if conn.get_bucket(bucketName) is None:
        print "BUCKET DOES NOT EXIST!"
        exit(0)
    else:
        bucket = conn.get_bucket(bucketName)
        for key in bucket.get_all_keys():
            fileName = str(key).split(",")[1][:-1]
            pool.process(downloadSoftware, key, fileName)
            fileNames.append(fileName)
    pool.shutdown()
    conn.close()
    return fileNames


def createRepo(fileNames):
    yb = yum.YumBase()
    inst = yb.rpmdb.returnPackages()
    installed = [x.name for x in inst]
    packages = ['httpd', 'createrepo']

    for package in packages:
        if package in installed:
            print('{0} is already installed'.format(package))
        else:
            print('Installing {0}'.format(package))
            kwarg = {
                'name': package
            }
            yb.install(**kwarg)
            yb.resolveDeps()
            yb.buildTransaction()
            yb.processTransaction()

    os.system("service httpd restart")

    for fileName in fileNames:
        print "Create Repo for " + fileName
        tar = tarfile.open(baseDir + fileName, "r:gz")
        tar.extractall(baseDir)
        tar.close()
        repoPath = baseDir + fileName[:-7]
        print repoPath
        os.system(repoPath + "/setup_repo.sh")


def cliParse():
    VALID_ACTION = ["get"]
    parser = argparse.ArgumentParser(description='Amazon S3 Download')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_get = subparsers.add_parser("get", help="Get a file from S3")
    parser_get.add_argument("--key", dest='accessKey', action="store", help="Your access key", required=False)
    parser_get.add_argument("--secret", dest='secretKey', action="store", help="Your Secret key", required=False)
    parser_get.add_argument("--file", dest='fileType', action="store", help="File to Download", required=False)

    args = parser.parse_args()
    return args


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



def prepareEnv(args):
    fileNames = getSoftware(args.accessKey, args.secretKey, args.fileType)
    createRepo(fileNames)


def install():
    print "Attempting Install of Ambari"
    hostNames = parseAmbariHosts()
    blueprintName = str(len(hostNames) - 1) + "-node-blueprint"
    groups = parseBlueprint(blueprintName)
    buildHostMappingTemplate(hostNames, groups, blueprintName)
    url = "http://localhost:8080/api/v1"
    applyBlueprint(url, blueprintName)

if __name__ == '__main__':
    print "PHD3 Installer"
    prepareEnv(cliParse())
    install()



