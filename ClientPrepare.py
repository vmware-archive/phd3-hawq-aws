__author__ = 'root'

import argparse

import boto
import boto.s3.connection


def getRepo(awsKey, secretKey, stack):
    ambariBucket = "ambari-repo"
    ambariRepo = "ambari.repo"
    bucketName = stack + "-" + ambariBucket
    conn = boto.connect_s3(aws_access_key_id=awsKey, aws_secret_access_key=secretKey)
    bucketExists = False

    while not bucketExists:
        try:
            bucket = conn.get_bucket(bucketName)
            bucketExists = False
        except Exception as e:
            pass
    fileExists = False
    while not fileExists:
        try:
            key = bucket.get_key(ambariRepo)
            key.get_contents_to_filename("/etc/yum.repos.d/" + ambariRepo)
            fileExists = False
        except Exception as e:
            pass
    conn.close()


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
    getRepo(args.accessKey, args.secretKey, args.stack)


if __name__ == '__main__':
    print "PHD3 Client Prepare"
    prepareEnv(cliParse())
