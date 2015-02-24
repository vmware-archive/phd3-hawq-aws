yum install wget
wget http://s3tools.org/repo/RHEL_6/s3tools.repo
cp s3tools.repo /etc/yum.repos.d/
yum install s3cmd
s3cmd --configure

s3cmd get s3://amey-data/pivotal --recursive
