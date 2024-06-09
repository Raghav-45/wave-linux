import os
import requests
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

os.makedirs(kernel_dir, exist_ok=True)
os.makedirs(busybox_dir, exist_ok=True)

# Function to download a file from a URL with a progress bar
def download_file(url, path):
    local_filename = os.path.join(path, url.split('/')[-1])
    if os.path.exists(local_filename):
        print(f"{local_filename} already exists. Skipping download.")
        return local_filename
    
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
        raise Exception("ERROR: Something went wrong with the download")
    
    return local_filename

# Download the Linux kernel and BusyBox tarballs
kernel_tarball = download_file(kernel_url, kernel_dir)
busybox_tarball = download_file(busybox_url, busybox_dir)

print(f"Linux Kernel downloaded to: {kernel_tarball}")
print(f"BusyBox downloaded to: {busybox_tarball}")