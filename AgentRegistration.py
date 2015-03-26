__author__ = 'dbaskette'
import argparse


def cliParse():
    VALID_ACTION = ["monitor"]
    parser = argparse.ArgumentParser(description='Agent Registration')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_monitor = subparsers.add_parser("monitor", help="Monitor Agent Registration")
    parser_monitor.add_argument("--ambari", dest='ambariServer', action="store", help="Ambari Server", required=True)
    parser_monitor.add_argument("--agents", dest='anumAgents', action="store", help="Number of Agents to Register",
                                required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print "Agent Registration"
    args = cliParse()
