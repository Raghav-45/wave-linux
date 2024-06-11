import os, subprocess

def get_coreutils_commands():
    result = subprocess.run(["./initrd/bin/busybox", "--list"], capture_output=True, text=True)
    commands = result.stdout.strip().replace("[", "").replace("]", "").split()
    return commands

def create_symlinks(commands):
    binary_dir = "initrd/bin"
    for cmd in commands:
        symlink_path = os.path.join(binary_dir, cmd)
        os.system(f"rm -rf ./{symlink_path}")
        # os.system(f"ln -s ./busybox ./{symlink_path}") # relative path for that link (./busybox)
        print(f"Created symlink for {cmd}")

    os.system(f"for cmd in $(./busybox --list); do ln -s /bin/busybox ./{binary_dir}/$cmd; done")  # IDK why but this works but run this inside initrd/bin directory manually

commands = get_coreutils_commands()
# print(commands)

create_symlinks(commands)