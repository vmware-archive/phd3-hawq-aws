__author__ = 'root'

import argparse

import yum


def installed(pkg):
    yb = yum.YumBase()
    inst = yb.rpmdb.returnPackages()
    installed = [x.name for x in inst]
    if pkg in [x.name for x in inst]:
        print installed
        return True
    else:
        return False


def install(pkgs):
    print "Install Package(s): " + str(pkgs)
    yb = yum.YumBase()
    print pkgs
    for pkg in pkgs:
        if installed(pkg):
            print str(pkg) + " is already installed"
        else:
            print "Installing " + str(pkg)
            yb.install(pkg)
            yb.buildTransaction()
            yb.processTransaction()


def remove(pkgs):
    print "Remove Package(s): " + str(pkgs)
    yb = yum.YumBase()

    print pkgs
    for pkg in pkgs:
        if installed(pkg):
            print "Removing " + str(pkg)
            yb.remove({'name': pkg})
            yb.buildTransaction()
            yb.processTransaction()
        else:
            print str(pkg) + " is not installed"


def cliParse():
    VALID_ACTION = ["install", "remove"]
    parser = argparse.ArgumentParser(description='YUM Package Manager')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_install = subparsers.add_parser("install", help="Install a YUM Packager")
    parser_install.add_argument("--pkgs", dest='pkgs', action="store", help="Package Names", required=True)
    parser_remove = subparsers.add_parser("remove", help="Remove a YUM Packager")
    parser_remove.add_argument("--pkgs", dest='pkgs', action="store", help="Package Names", required=True)

    args = parser.parse_args()
    pkgs = []

    if (args.subparser_name == "install"):
        for pkg in args.pkgs.split(","):
            print pkg
            pkgs.append(pkg)
        install(pkgs)
    elif (args.subparser_name == "remove"):
        for pkg in args.pkgs.split(","):
            print pkg
            pkgs.append(pkg)
        remove(pkgs)


if __name__ == '__main__':
    print "PHD3 Client Prepare"
    cliParse()
