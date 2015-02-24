#!/bin/bash
master_node_internal_dns=$1
number_of_slaves=$2
# Adds the master node
number_of_slaves=`echo $(($number_of_slaves + 1))`

`curl -i -u admin:admin http://$master_node_internal_dns:8080/api/v1/hosts > ambari-hosts.txt`

number_of_registered_slaves=`grep -c "host_name" ambari-hosts.txt`
echo "Number of slaves requested : " $number_of_slaves
echo "Number of registred slaves found : " $number_of_registered_slaves
while [ "$number_of_registered_slaves" != "$number_of_slaves" ]
        do
        sleep 30
        echo "Trying again after sleep"
        `curl -i -u admin:admin http://$master_node_internal_dns:8080/api/v1/hosts > ambari-hosts.txt`
        number_of_registered_slaves=`grep -c "host_name" ambari-hosts.txt`
        echo "Number of slaves requested : " $number_of_slaves
        echo "Number of registred slaves found : " $number_of_registered_slaves
done
echo "Registered slave nodes match Requested slave nodes"
exit 0