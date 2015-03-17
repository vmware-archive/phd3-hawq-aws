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


S3Location = "http://s3.amazonaws.com/"


def getBucketName(fileType):
    with open("./phd3.json", "r") as phd3Files:
        fileNames = json.load(phd3Files)
        for file in fileNames:
            if file == fileType:
                return fileNames[file]
        return 0


def downloadSoftware(key, fileName):
    try:
        key.get_contents_to_filename("/tmp/" + fileName)
        return 0
    except Exception as e:
        # key.get_contents_to_filename("/tmp/"+fileName)
        return -1


def getSoftware(awsKey, secretKey, fileType):
    bucketName = getBucketName("bucket")
    fileNames = []
    conn = boto.connect_s3(aws_access_key_id=awsKey, aws_secret_access_key=secretKey)
    pool = ThreadPool(10)

    if conn.get_bucket(bucketName) is None:
        print "BUCKET DOES NOT EXIST!"
        exit(0)
    else:
        bucket = conn.get_bucket(bucketName)
        for key in bucket.get_all_keys():
            fileName = str(key).split(",")[1][:-1]
            print "Filename:" + fileName
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
        tar = tarfile.open("/tmp/" + fileName, "r:gz")
        tar.extractall("/tmp")
        tar.close()
        repoPath = "/tmp/" + fileName[:-7]
        print repoPath
        os.system(repoPath + "/setup_repo.sh")


def cliParse():
    VALID_ACTION = ["get"]
    parser = argparse.ArgumentParser(description='Amazon S3 Download')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_get = subparsers.add_parser("get", help="Get a file from S3")
    parser_get.add_argument("--key", dest='accessKey', action="store", help="Your access key", required=True)
    parser_get.add_argument("--secret", dest='secretKey', action="store", help="Your Secret key", required=True)
    parser_get.add_argument("--file", dest='fileType', action="store", help="File to Download", required=True)

    args = parser.parse_args()
    return args


def prepareEnv(args):
    fileNames = getSoftware(args.accessKey, args.secretKey, args.fileType)
    createRepo(fileNames)


if __name__ == '__main__':
    print "PHD3 Installer"
    prepareEnv(cliParse())



