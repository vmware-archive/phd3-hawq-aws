__author__ = 'dbaskette'

# Read json file with info....  or just have everything as a  parameter
import argparse

from boto.cloudformation import CloudFormationConnection


def cliParse():
    VALID_ACTION = ["create", "delete"]
    parser = argparse.ArgumentParser(description='Pivotal HD Cloud Creator')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_create = subparsers.add_parser("create", help="Create a PHD Cloud")
    parser_delete = subparsers.add_parser("delete", help="Delete a PHD Cloud")
    parser_create.add_argument("--name", dest='clustername', action="store", help="Name of Cluster to be Created",
                               required=True)
    parser_create.add_argument("--nodes", dest='nodeCnt', default=1, action="store",
                               help="Number of Nodes to be Created", required=True)
    parser_create.add_argument("--key", dest='accessKey', action="store", help="AWS Access Key",
                               required=True)
    parser_create.add_argument("--secret", dest='secretKey', action="store", help="AWS Secret Key",
                               required=True)
    parser_create.add_argument("--region", dest='region', action="store", help="AWS Region",
                               required=True)
    parser_delete.add_argument("--name", dest='clustername', action="store", help="Name of Cluster to be Deleted",
                               required=True)
    args = parser.parse_args()
    clusterDictionary = {}
    if (args.subparser_name == "create"):
        print  args.clustername
    elif (args.subparser_name == "delete"):
        print  args.clustername

    cloudFormation(args.clustername, args.nodeCnt, args.accessKey, args.secretKey, args.region)


def cloudFormation(clusterName, nodeCnt, accessKey, secretKey, regionName):
    conn = CloudFormationConnection(aws_access_key_id=accessKey, aws_secret_access_key=secretKey)
    conn.create_stack(clusterName, template_body=None,
                      template_url='https://s3.amazonaws.com/phd-3.0/cloudformation_update.json', notification_arns=[],
                      disable_rollback=False, timeout_in_minutes=None, capabilities=None)


if __name__ == '__main__':
    cliParse()