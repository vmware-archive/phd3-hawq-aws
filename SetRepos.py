__author__ = 'root'

import os
import socket

from requests.auth import HTTPBasicAuth
import requests


def getRepos():
    print "getRepo"
    # look through repo files and then submit via REST
    repos = os.listdir("/etc/yum.repos.d")
    hostName = socket.getfqdn()
    headers = {'X-Requested-By': 'Heffalump'}
    auth = HTTPBasicAuth('admin', 'admin')
    # url = "http://" + hostName + ":8080/api/v1/stacks/PHD/versions/3.0/operating_systems/redhat6/repositories/PHD-3.0"

    for repoFile in repos:
        repo = repoFile[:-5]

        if "PHD-3.0" in repo:
            url = "http://" + hostName + ":8080/api/v1/stacks/PHD/versions/3.0/operating_systems/redhat6/repositories/PHD-3.0"
            payload = {"Repositories": {"base_url": hostName + "/" + repo + "/"}}
            print payload
            print url
            print requests.put(url, auth=auth, headers=headers, data=payload)
        elif "PHD-UTILS" in repo:
            url = "http://" + hostName + ":8080/api/v1/stacks/PHD/versions/3.0/operating_systems/redhat6/repositories/PHD-UTILS"
            payload = {"Repositories": {"base_url": hostName + "/" + repo + "/"}}
            print payload
            print url
            print requests.put(url, auth=auth, headers=headers, data=payload)
        elif "PADS" in repo:
            url = "http://" + hostName + ":8080/api/v1/stacks/PHD/versions/3.0/operating_systems/redhat6/repositories/PHD-UTILS"
            payload = {"Repositories": {"base_url": hostName + "/" + repo + "/"}}
            print payload
            print url
            print requests.put(url, auth=auth, headers=headers, data=payload)


if __name__ == '__main__':
    print "PHD3 Repo Setup"
    getRepos()
