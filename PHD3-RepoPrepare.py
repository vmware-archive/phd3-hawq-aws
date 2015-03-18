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
from boto.s3.connection import Location
from boto.s3.key import Key
from simplethreads.ThreadPool import ThreadPool
import yum


baseDir = "/opt/phd3/software/"
ambariBucket = "ambari-repo"


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
    except Exception as e:
        pass


def getSoftware(awsKey, secretKey):
    bucketName = getBucketName("bucket")
    fileNames = []
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


def createRepo(fileNames, logFile):
    yb = yum.YumBase()
    inst = yb.rpmdb.returnPackages()
    installed = [x.name for x in inst]
    packages = ['httpd']

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
        try:
            tar = tarfile.open(baseDir + fileName, "r:gz")
            tar.extractall(baseDir)
            tar.close()
            repoPath = baseDir + fileName[:-7]
            os.system(repoPath + "/setup_repo.sh")
        except Exception as e:
            logFile.write(e)


def uploadRepo(awsKey, secretKey, stack, logFile):
    bucketName = stack + "-" + ambariBucket
    try:
        conn = boto.connect_s3(aws_access_key_id=awsKey, aws_secret_access_key=secretKey)
        conn.create_bucket(bucketName, location=Location.DEFAULT)
        bucket = conn.get_bucket(bucketName)
        k = Key(bucket)
        k.key = 'ambari.repo'
        k.set_contents_from_filename("/etc/yum.repos.d/ambari.repo")
        k.set_canned_acl('public-read')
    except Exception as e:
        logFile.write(e)





def cliParse():
    VALID_ACTION = ["get"]
    parser = argparse.ArgumentParser(description='Amazon S3 Download')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_get = subparsers.add_parser("get", help="Get a file from S3")
    parser_get.add_argument("--key", dest='accessKey', action="store", help="Your access key", required=False)
    parser_get.add_argument("--secret", dest='secretKey', action="store", help="Your Secret key", required=False)
    parser_get.add_argument("--stack", dest='stack', action="store", help="StackName", required=False)
    args = parser.parse_args()
    return args


def prepareEnv(args):
    logFile = open("repo-prepare.log", "w+")
    fileNames = getSoftware(args.accessKey, args.secretKey)
    createRepo(fileNames, logFile)
    uploadRepo(args.accessKey, args.secretKey, args.stack, logFile)


if __name__ == '__main__':
    print "PHD3 Installer"
    prepareEnv(cliParse())



