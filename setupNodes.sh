chkconfig iptables off
chkconfig ip6tables off
service iptables stop
service ip6tables stop
sed -i 's/SELINUX=[a-z]*/SELINUX=disabled/' /etc/selinux/config
echo 0 > /selinux/enforce

mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdb
mkdir /mnt/data1
mount -t ext4 /dev/xvdb /mnt
echo "/dev/xvdb /mnt auto noatime 0 0" | sudo tee -a /etc/fstab

mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdc
mkdir /mnt/data2
mount -t ext4 /dev/xvdc /mnt/data2
echo "/dev/xvdc /mnt/data2 auto noatime 0 0" | sudo tee -a /etc/fstab

mkfs -t ext4 -E lazy_itable_init=1 /dev/xvdd
mkdir /mnt/data3
mount -t ext4 /dev/xvdd /mnt/data3
echo "/dev/xvdd /mnt/data3 auto noatime 0 0" | sudo tee -a /etc/fstab

mkfs -t ext4 -E lazy_itable_init=1 /dev/xvde
mkdir /mnt/data4
mount -t ext4 /dev/xvde /mnt/data4
echo "/dev/xvde /mnt/data4 auto noatime 0 0" | sudo tee -a /etc/fstab
