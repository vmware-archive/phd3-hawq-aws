chkconfig iptables off
chkconfig ip6tables off
service iptables stop
service ip6tables stop
sed -i 's/SELINUX=[a-z]*/SELINUX=disabled/' /etc/selinux/config
echo 0 > /selinux/enforce

mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdb
mkdir /data1
mount -t ext4 /dev/xvdb /data1
echo "/dev/xvdb /data1 auto noatime 0 0" | sudo tee -a /etc/fstab

mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdc
mkdir /data2
mount -t ext4 /dev/xvdc /data2
echo "/dev/xvdc /data2 auto noatime 0 0" | sudo tee -a /etc/fstab

mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdd
mkdir /data3
mount -t ext4 /dev/xvdd /data3
echo "/dev/xvdd /data3 auto noatime 0 0" | sudo tee -a /etc/fstab

mkfs -t ext4 -E lazy_itable_init=1 /dev/xvde
mkdir /data4
mount -t ext4 /dev/xvde /data4
echo "/dev/xvde /data4 auto noatime 0 0" | sudo tee -a /etc/fstab
