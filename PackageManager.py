__author__ = 'root'

import yum


def installed(pkg):
    yb = yum.YumBase()
    inst = yb.rpmdb.returnPackages()
    yb.close()
    if pkg in [x.name for x in inst]:
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
            print e
    yb.close()



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
            print e
    yb.close()

