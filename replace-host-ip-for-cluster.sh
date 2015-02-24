#!/bin/bash
master_node_ip="$1"
COUNTER=0
slave_node_ip_list=""
for slave_node_ip in `grep "host_name" ambari-hosts.txt | awk -F':' '{print $(NF)}'`; do
  if [ \"$master_node_ip\" != "$slave_node_ip" ] 
  	then
  	   	let COUNTER=COUNTER+1
  	   	if [ $COUNTER -gt 1 ]; then
  	    	slave_node_ip_list="$slave_node_ip_list , \n"
       	fi
  	  echo "Replacing slave$COUNTER with $slave_node_ip"
  	  slave_node_ip_list="$slave_node_ip_list \n\{\n\"fqdn\" : $slave_node_ip\n\}\n"
  fi
done
`sed -i "s/slave_nodes/$slave_node_ip_list/;s/master_node/\"$master_node_ip\"/" blueprint-cluster-definition.json`