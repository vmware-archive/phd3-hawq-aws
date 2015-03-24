__author__ = 'root'

import argparse

import yum


def setupJDK():
    # "yum -y remove *openjdk \n",
    #     "wget --no-check-certificate --no-cookies --header 'Cookie: oraclelicense=accept-securebackup-cookie' http://download.oracle.com/otn-pub/java/jdk/7u67-b01/jdk-7u67-linux-x64.rpm \n",
    # 	  "wget --no-check-certificate --no-cookies --header 'Cookie: oraclelicense=accept-securebackup-cookie' http://download.oracle.com/otn-pub/java/jdk/7u67-b01/jdk-7u67-linux-x64.tar.gz \n",
    #  "wget --no-check-certificate http://public-repo-1.hortonworks.com/ARTIFACTS/UnlimitedJCEPolicyJDK7.zip \n",

    #	  "yum -y install jdk-7u67-linux-x64.rpm \n",
    print "Setup JDK"
    yb = yum.YumBase()
    inst = yb.rpmdb.returnPackages()
    installed = [x.name for x in inst]
    package = '*openjdk'
    if package in installed:
        kwarg = {
            'name': package
        }
        yb.remove(**kwarg)
        yb.resolveDeps()
        yb.buildTransaction()
        yb.processTransaction()
    else:
        print "Package Not Found"

        # for package in packages:
        #     if package in installed:
        #         print('{0} is already installed'.format(package))
        #         yb.remove(package)
        #     else:
        #         print('Installing {0}'.format(package))
        #         kwarg = {
        #             'name': package
        #         }
        #         yb.install(**kwarg)
        #         yb.resolveDeps()
        #         yb.buildTransaction()
        #         yb.processTransaction()


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


def prepareEnv():
    setupJDK()


if __name__ == '__main__':
    print "PHD3 Gateawy Prepare"
    prepareEnv()
