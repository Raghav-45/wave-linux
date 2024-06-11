import os, subprocess

def get_coreutils_commands():
    result = subprocess.run(["./workspace/bin/coreutils", "--list"], capture_output=True, text=True)
    commands = result.stdout.strip().replace("[", "").replace("]", "").split()
    return commands

def create_symlinks(commands):
    binary_dir = "workspace/bin"
    for cmd in commands:
        symlink_path = os.path.join(binary_dir, cmd)
        os.system(f"ln -s ./{binary_dir}/coreutils ./{symlink_path}")
        # os.system(f"rm -rf ./{symlink_path}")
        print(f"Created symlink for {cmd}")

commands = get_coreutils_commands()
# print(commands)

formatted_commands = ["-p uu_" + command for command in commands]
result = ' '.join(formatted_commands)
print(result)

# create_symlinks(commands)