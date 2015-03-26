__author__ = 'dbaskette'
import argparse
import socket
import time
import json

import requests
from requests.auth import HTTPBasicAuth




# Add this as a method
# chkconfig iptables off
# chkconfig ip6tables off
# service iptables stop
# service ip6tables stop
# sed -i 's/SELINUX=[a-z]*/SELINUX=disabled/' /etc/selinux/config
# echo 0 > /selinux/enforce
#
# mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdb
# mkdir /mnt/data1
# mount -t ext4 /dev/xvdb /mnt
# echo "/dev/xvdb /mnt auto noatime 0 0" | sudo tee -a /etc/fstab
#
# mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdc
# mkdir /mnt/data2
# mount -t ext4 /dev/xvdc /mnt/data2
# echo "/dev/xvdc /mnt/data2 auto noatime 0 0" | sudo tee -a /etc/fstab
#
# mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdd
# mkdir /mnt/data3
# mount -t ext4 /dev/xvdd /mnt/data3
# echo "/dev/xvdd /mnt/data3 auto noatime 0 0" | sudo tee -a /etc/fstab
#
# mkfs -t ext4 -E lazy_itable_init=1 /dev/xvde
# mkdir /mnt/data4
# mount -t ext4 /dev/xvde /mnt/data4
# echo "/dev/xvde /mnt/data4 auto noatime 0 0" | sudo tee -a /etc/fstab




def registrationMonitor(numAgents):
    hostName = socket.getfqdn()
    auth = HTTPBasicAuth('admin', 'admin')
    url = "http://" + hostName + ":8080/api/v1/hosts"
    complete = False
    while not complete:
        registeredCount = 0
        agentInfo = requests.get(url, auth=auth)
        ambariHosts = open("ambariAgents.txt", "w")
        agentJSON = json.loads(agentInfo.text)
        registeredCount = len(agentJSON["items"])
        if registeredCount == numAgents:
            for line in agentJSON["items"]:
                ambariHosts.write(line["Hosts"]["host_name"] + "\n")
            complete = True
        else:
            time.sleep(15)


def cliParse():
    VALID_ACTION = ["monitor"]
    parser = argparse.ArgumentParser(description='Agent Registration')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_monitor = subparsers.add_parser("monitor", help="Monitor Agent Registration")
    parser_monitor.add_argument("--agents", dest='numAgents', action="store", help="Number of Agents to Register",
                                required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print "Agent Registration"
    args = cliParse()
    numAgents = int(args.numAgents) + 1  # Account for Agent on Ambari Server itself
    registrationMonitor(numAgents)
