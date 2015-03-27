CloudFormation script for Auto-Deploying [Pivotal HD 3.0](http://pivotal.io/big-data/pivotal-hd) and HAWQ on AWS with [Ambari Blueprints.](https://cwiki.apache.org/confluence/display/AMBARI/Blueprints)    These scripts will
build out a cluster of a specific size, and then deploy Pivotal HD 3.0 on the cluster according to the specifications
in the Ambari Blueprint.  The sizes available have been pre-determined and blueprints have been designed for that specific
cluster size.   Today the options are:
*  6 Nodes plus a Gateway/Management Node
* 10 Nodes plus a Gateway/Management Node

![alt tag](https://raw.githubusercontent.com/dbbaskette/heffalump/master/docs/HeffalumpWorkflow.jpg)


