cd initrd

########## GENERATE INIT FILE ##########
echo '#!/bin/sh' > init
echo 'mount -t sysfs sysfs /sys' >> init
echo 'mount -t proc proc /proc' >> init
echo 'mount -t devtmpfs udev /dev' >> init
echo 'sysctl -w kernel.printk="2 4 1 7"' >> init
echo 'clear' >> init
echo 'echo -e "Welcome to \\e[34mWave \\e[32mLinux \\e[31mLive\\e[0m (/init)"' >> init
echo '/bin/sh' >> init
echo 'poweroff -f' >> init
########## GENERATE INIT FILE ##########

chmod -R 777 .
find . | cpio -o -H newc > ../initrd.img

cd ..