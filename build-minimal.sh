#!/bin/bash

# Define variables for the Linux kernel version and BusyBox version
LINUX_KERNEL_VERSION="5.14.6"
BUSYBOX_VERSION="1.34.1"

# Extract the major kernel version (e.g., "5" from "5.14.6")
KERNEL_MAJOR=$(echo $LINUX_KERNEL_VERSION | cut -d '.' -f 1)

# Create the src directory and the subdirectories for kernel and busybox
SRC_DIR="src"
KERNEL_DIR="${SRC_DIR}/linux-${LINUX_KERNEL_VERSION}"
BUSYBOX_DIR="${SRC_DIR}/busybox-${BUSYBOX_VERSION}"

# Construct the URLs
KERNEL_URL="https://mirrors.edge.kernel.org/pub/linux/kernel/v${KERNEL_MAJOR}.x/linux-${LINUX_KERNEL_VERSION}.tar.xz"
BUSYBOX_URL="https://www.busybox.net/downloads/busybox-${BUSYBOX_VERSION}.tar.bz2"

WORKSPACE_DIRS=("initrd" "initrd/bin" "initrd/sbin" "initrd/dev" "initrd/proc" "initrd/sys")

mkdir -p $SRC_DIR
cd $SRC_DIR
    wget $KERNEL_URL
    tar -xf linux-$LINUX_KERNEL_VERSION.tar.xz
    cd linux-$LINUX_KERNEL_VERSION
        make defconfig
        make -j$(nproc) || exit
    cd ..

    wget $BUSYBOX_URL
    tar -xf busybox-$BUSYBOX_VERSION.tar.bz2
    cd busybox-$BUSYBOX_VERSION
        make defconfig
        sed 's/^.*CONFIG_STATIC[^_].*$/CONFIG_STATIC=y/g' -i .config
        # sed -i "s|.*CONFIG_STATIC.*|CONFIG_STATIC=y|" .config  # this also works
        make CC=musl-gcc -j$(nproc) busybox
    cd ..
cd ..

cp $KERNEL_DIR/arch/x86/boot/bzImage ./

# for DIR in "${WORKSPACE_DIRS[@]}"; do
#     mkdir -p $DIR
# done

mkdir initrd
cd initrd
    mkdir -p bin sbin dev proc sys
    cd bin
        cd ../../$BUSYBOX_DIR/busybox ./

        for cmd in $(./busybox --list); do
            ln -s /bin/busybox ./$cmd;
        done
    cd ..

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