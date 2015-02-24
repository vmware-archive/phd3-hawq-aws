wget http://public-repo-1.hortonworks.com/ambari/centos6/1.x/updates/1.6.0/ambari.repo

cp ambari.repo /etc/yum.repos.d

yum -y install ambari-server

ambari-server -s -v setup

ambari-server start



