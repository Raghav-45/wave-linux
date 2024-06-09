import os
import requests

# Define variables for the Linux kernel version and BusyBox version
linux_kernel_version = "5.14.6"
busybox_version = "1.34.1"

# Extract the major kernel version (e.g., "5" from "5.14.6")
kernel_major = linux_kernel_version.split('.')[0]

# Construct the URLs
kernel_url = f"https://mirrors.edge.kernel.org/pub/linux/kernel/v{kernel_major}.x/linux-{linux_kernel_version}.tar.gz"
busybox_url = f"https://www.busybox.net/downloads/busybox-{busybox_version}.tar.bz2"

# Create the src directory and the subdirectories for kernel and busybox
src_dir = "src"
kernel_dir = os.path.join(src_dir, f"linux-{linux_kernel_version}")
busybox_dir = os.path.join(src_dir, f"busybox-{busybox_version}")

os.makedirs(kernel_dir, exist_ok=True)
os.makedirs(busybox_dir, exist_ok=True)

# Function to download a file from a URL
def download_file(url, path):
    local_filename = os.path.join(path, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# Download the Linux kernel and BusyBox tarballs
kernel_tarball = download_file(kernel_url, kernel_dir)
busybox_tarball = download_file(busybox_url, busybox_dir)

print(f"Linux Kernel downloaded to: {kernel_tarball}")
print(f"BusyBox downloaded to: {busybox_tarball}")