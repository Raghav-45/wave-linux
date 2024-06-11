cd initrd

echo '#!/bin/sh' > init
echo 'mount -t sysfs sysfs /sys' >> init
echo 'mount -t proc proc /proc' >> init
echo 'mount -t devtmpfs udev /dev' >> init
echo 'sysctl -w kernel.printk="2 4 1 7"' >> init
echo 'clear' >> init
echo '/bin/sh' >> init
echo 'poweroff -f' >> init

chmod -R 777 .
find . | cpio -o -H newc > ../initrd.img

cd ..