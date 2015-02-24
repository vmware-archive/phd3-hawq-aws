yum -y localinstall jdk-7u*-linux-x64.rpm

alternatives --install /usr/bin/java java /usr/java/default/bin/java 1 \
--slave /usr/bin/jar jar /usr/java/default/bin/jar \
--slave /usr/bin/javac javac /usr/java/default/bin/javac \
--slave /usr/bin/javadoc javadoc /usr/java/default/bin/javadoc \
--slave /usr/bin/javaws javaws /usr/java/default/bin/javaws \
--slave /usr/bin/jcontrol jcontrol /usr/java/default/bin/jcontrol

sudo /usr/sbin/alternatives --install "/usr/bin/java" "java" "/usr/java/jdk1.7.0_55/bin/java" 3
sudo /usr/sbin/alternatives --install "/usr/bin/javac" "javac" "/usr/java/jdk1.7.0_55/bin/javac" 3
sudo /usr/sbin/alternatives --config java

chkconfig iptables off
chkconfig ip6tables off
service iptables stop
service ip6tables stop

#Password Change for PCC Node, is root password required for Ambari?
password=pivotal123
sed -i "s/#PermitRootLogin yes/PermitRootLogin yes/g" /etc/ssh/sshd_config
sed -i "s/#PasswordAuthentication yes/PasswordAuthentication yes/g" /etc/ssh/sshd_config
service sshd restart
passwd <<EOF
$password
$password
EOF

sed -i 's/SELINUX=[a-z]*/SELINUX=disabled/' /etc/selinux/config
 echo 0 > /selinux/enforce
