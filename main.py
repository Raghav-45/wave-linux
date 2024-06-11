import os, shutil
import requests
import tarfile
from tqdm import tqdm

# Define variables for the Linux kernel version and BusyBox version
linux_kernel_version = "5.14.6"
busybox_version = "1.34.1"

# Extract the major kernel version (e.g., "5" from "5.14.6")
kernel_major = linux_kernel_version.split('.')[0]

# Construct the URLs
kernel_url = f"https://mirrors.edge.kernel.org/pub/linux/kernel/v{kernel_major}.x/linux-{linux_kernel_version}.tar.xz"
busybox_url = f"https://www.busybox.net/downloads/busybox-{busybox_version}.tar.bz2"

# Create the src directory and the subdirectories for kernel and busybox
src_dir = "src"
kernel_dir = os.path.join(src_dir, f"linux-{linux_kernel_version}")
busybox_dir = os.path.join(src_dir, f"busybox-{busybox_version}")

workspace_dir = ["initrd", "initrd/bin", "initrd/sbin", "initrd/dev", "initrd/proc", "initrd/sys"]

os.makedirs(kernel_dir, exist_ok=True)
os.makedirs(busybox_dir, exist_ok=True)

for dir in workspace_dir: os.makedirs(dir, exist_ok=True)

def download_file(url, path):
    local_filename = os.path.join(path, os.path.basename(url))
    if os.path.exists(local_filename):
        print(f"{local_filename} already exists. Skipping download.\n")
        return local_filename
    
    print(f"Downloading {local_filename}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192  # 8KB
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=block_size):
            t.update(len(chunk))
            f.write(chunk)
    t.close()
    
    if total_size != 0 and t.n != total_size:
        raise Exception("ERROR: Something went wrong with the download\n")
    
    extract_tarball(local_filename)
    return local_filename


def extract_tarball(tarball_path):
    extract_path = os.path.dirname(tarball_path)
    if tarfile.is_tarfile(tarball_path):
        with tarfile.open(tarball_path, 'r:*') as tar:
            file_count = len(tar.getmembers())
            with tqdm(total=file_count) as pbar:
                for member in tar:
                    tar.extract(member, path=extract_path)
                    pbar.update(1)
        print(f"Extracted {tarball_path}")
    else:
        raise Exception(f"ERROR: {tarball_path} is not a valid tar file")


def build_kernel():
    # execute build commands only if the bzImage does not exist
    if not os.path.exists(f"{kernel_dir}/arch/x86/boot/bzImage"):
        os.system(f"make -C {kernel_dir} defconfig")
        os.system(f"make -C {kernel_dir} -j8")


def build_busybox():
    # execute build commands
    if not os.path.exists(f"{busybox_dir}/busybox"):
        os.system(f"make -C {busybox_dir} defconfig")
        os.system(f"sed 's/^.*CONFIG_STATIC[^_].*$/CONFIG_STATIC=y/g' -i {busybox_dir}/.config")
        os.system(f"make CC=musl-gcc -C {busybox_dir} -j8 busybox")


kernel_tarball = download_file(kernel_url, src_dir)
print(f"Linux Kernel downloaded and extracted to: {kernel_dir}")

busybox_tarball = download_file(busybox_url, src_dir)
print(f"BusyBox downloaded and extracted to: {busybox_dir}")

# build_kernel()
# build_busybox()
# print(f"{busybox_dir}/.config")

def directory_structure():
    # shutil.copyfile(f"{busybox_dir}/busybox", f"{workspace_dir[0]}/bin/busybox")
    # shutil.copyfile(f"{kernel_dir}/arch/x86/boot/bzImage", f"./bzImage")
    
    os.system(f"./{workspace_dir[0]}/bin/busybox echo '#!/bin/sh' > init")
    os.system(f"./{workspace_dir[0]}/bin/busybox echo 'mount -t sysfs sysfs /sys' >> init")
    os.system(f"./{workspace_dir[0]}/bin/busybox echo 'mount -t proc proc /proc' >> init")
    os.system(f"./{workspace_dir[0]}/bin/busybox echo 'mount -t devtmpfs udev /dev' >> init")
    os.system(f"./{workspace_dir[0]}/bin/busybox echo 'sysctl -w kernel.printk=\"2 4 1 7\"' >> init")
    # os.system(f"./{workspace_dir[0]}/bin/busybox echo 'clear' >> init")
    os.system(f"./{workspace_dir[0]}/bin/busybox echo '/bin/sh' >> init")
    os.system(f"./{workspace_dir[0]}/bin/busybox echo 'poweroff -f' >> init")

    # os.system(f"./{workspace_dir[0]}/bin/busybox chmod -R 777 ./{workspace_dir[0]}")
    os.system(f"./{workspace_dir[0]}/bin/busybox find ./{workspace_dir[0]}/ | cpio -o -H newc > ./initrd.img")


directory_structure()