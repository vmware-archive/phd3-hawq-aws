__author__ = 'root'

import argparse
import os

import boto
import boto.s3.connection

import PackageManager


def getRepo(awsKey, secretKey, stack, ambariServer):
    ambariBucket = "ambari-repo"
    ambariRepo = "ambari.repo"
    bucketName = stack + "-" + ambariBucket
    conn = boto.connect_s3(aws_access_key_id=awsKey, aws_secret_access_key=secretKey)
    bucketExists = False

    while not bucketExists:
        try:
            bucket = conn.get_bucket(bucketName)
            bucketExists = True
        except Exception as e:
            pass
    fileExists = False
    while not fileExists:
        try:
            key = bucket.get_key(ambariRepo)
            key.get_contents_to_filename("/etc/yum.repos.d/" + ambariRepo)
            fileExists = True
        except Exception as e:
            pass
    fileExists = False
    installAmbariAgent(ambariServer)
    while not fileExists:
        try:
            key = bucket.get_key("hosts")
            key.get_contents_to_filename("/etc/hosts")
            fileExists = True
        except Exception as e:
            pass
    conn.close()


def allowSSH():
    lines = []
    with open("/etc/ssh/sshd_config", "r")as origFile:
        contents = origFile.read()
        contents = contents.replace("PasswordAuthentication no", "PasswordAuthentication yes")
        # contents = contents.replace("#PubkeyAuthentication", "PubkeyAuthentication")

    with (open("/etc/ssh/sshd_config", "w")) as newFile:
        newFile.write(contents)
        os.system("service sshd restart")


def installAmbariAgent(ambariServer):
    ambariAgentConfigFile = "/etc/ambari-agent/conf/ambari-agent.ini"
    PackageManager.install("ambari-agent")
    lines = []
    with open(ambariAgentConfigFile, "r")as origFile:
        contents = origFile.read()
        contents = contents.replace("localhost", ambariServer)
    with (open(ambariAgentConfigFile, "w")) as newFile:
        newFile.write(contents)
    os.system("service ambari-agent start")


def cliParse():
    VALID_ACTION = ["prep"]
    parser = argparse.ArgumentParser(description='Client Prepare')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_prep = subparsers.add_parser("prep", help="Get a file from S3")
    parser_prep.add_argument("--key", dest='accessKey', action="store", help="Your access key", required=True)
    parser_prep.add_argument("--secret", dest='secretKey', action="store", help="Your Secret key", required=True)
    parser_prep.add_argument("--stack", dest='stack', action="store", help="StackName", required=True)
    parser_prep.add_argument("--ambari", dest='ambariServer', action="store", help="Hostname of Ambari Server",
                             required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print "PHD3 Client Prepare"
    args = cliParse()
    allowSSH()
    getRepo(args.accessKey, args.secretKey, args.stack, args.ambariServer)
