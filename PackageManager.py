__author__ = 'root'

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


def install(pkg):
    print "Install Package(s): " + str(pkg)
    yb = yum.YumBase()

    if not installed(pkg):
        matches = yb.searchGenerator(["name"], [pkg])
        for (po, matched_value) in matches:
            if po.name == pkg:
                yb.install(po)
        try:
            yb.buildTransaction()
            yb.processTransaction()
        except Exception as e:
            pass


def remove(pkg):
    yb = yum.YumBase()

    if installed(pkg):
        matches = yb.searchGenerator(["name"], [pkg])
        for (po, matched_value) in matches:
            if po.name == pkg:
                yb.remove(po)
        try:
            yb.buildTransaction()
            yb.processTransaction()
        except Exception as e:
            pass


# def cliParse():
# VALID_ACTION = ["install", "remove"]
#     parser = argparse.ArgumentParser(description='YUM Package Manager')
#     subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
#     parser_install = subparsers.add_parser("install", help="Install a YUM Package")
#     parser_install.add_argument("--pkgs", dest='pkgs', action="store", help="Package Names", required=True)
#     parser_remove = subparsers.add_parser("remove", help="Remove a YUM Packager")
#     parser_remove.add_argument("--pkgs", dest='pkgs', action="store", help="Package Names", required=True)
#
#     args = parser.parse_args()
#     pkgs = []
#
#     if (args.subparser_name == "install"):
#         for pkg in args.pkgs.split(","):
#             print pkg
#             pkgs.append(pkg)
#         install(pkgs)
#     elif (args.subparser_name == "remove"):
#         for pkg in args.pkgs.split(","):
#             print pkg
#             pkgs.append(pkg)
#         remove(pkgs)
#
#
# if __name__ == '__main__':
#     print "PHD3 Client Prepare"
#     cliParse()
