#phd3-hawq-aws
previously known as Heffalump

CloudFormation script for Auto-Deploying [Pivotal HD 3.0](http://pivotal.io/big-data/pivotal-hd) and HAWQ on AWS with [Ambari Blueprints.](https://cwiki.apache.org/confluence/display/AMBARI/Blueprints)    These scripts will
build out a cluster of a specific size, and then deploy Pivotal HD 3.0 on the cluster according to the specifications
in the Ambari Blueprint.  The sizes available have been pre-determined and blueprints have been designed for that specific
cluster size.  The current options are:
*  6 Nodes plus a Gateway/Management Node
* 10 Nodes plus a Gateway/Management Node

The CloudFormation cluster design in this revision is a simplistic design that was created to simplify the
development process.   A new, more robust design is under development and will be added to the project soon.

Upcoming features:
* New cluster design
* Enhanced error detection and logging
* Ability to install projects that are not installable via Ambari
* Kerberos Authenticated cluster


![alt tag](https://raw.githubusercontent.com/dbbaskette/phd3-hawq-aws/master/docs/Workflow.jpg)


