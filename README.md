# Wave Linux

This project provides a minimal Linux implementation using `Rust Coreutils` and the `Linux Kernel`. The setup script downloads the specified Linux Kernel and BusyBox, extracts them into designated directories, and prepares them for further development or usage.

- **Linux Kernel:** [torvalds/linux](https://github.com/torvalds/linux)
- **Rust Coreutils:** [uutils/coreutils](https://github.com/uutils/coreutils)

## Description 📝

By leveraging the power and efficiency of Rust, along with Linux kernel, I've created a lightweight linux.

## Features ( Currently ) ✨

- Downloads and extracts the Linux Kernel and BusyBox.
- Utilizes Rust Coreutils for enhanced performance.
- Using a script for automated setup and extraction.

## Usage 🚀

1. Clone the repository:

    ```sh
    git clone https://github.com/raghav-45/wave-linux.git
    cd wave-linux
    ```

2. Install Required tools ( Ubuntu's [Build Your Own Kernel](https://wiki.ubuntu.com/Kernel/BuildYourOwnKernel) guide ):

    ```sh
    sudo apt-get install libncurses-dev flex bison openssl libssl-dev dkms libelf-dev libudev-dev libpci-dev libiberty-dev autoconf bc
    ```

3. Run the setup script:

    ```sh
    python build-minimal.py
    ```


## Building Rust Coreutils 🛠️

1. Clone the Rust Coreutils

2. Install [Rust](https://www.rust-lang.org/tools/install) 🦀:

3. Build Rust Coreutils ( You can specify which utilities you want ):

    ```sh
   cargo build --target x86_64-unknown-linux-musl --release -p uu_arch -p uu_base32 -p uu_base64 -p uu_basename -p uu_basenc -p uu_cat -p uu_chgrp -p uu_chmod -p uu_chown -p uu_chroot -p uu_cksum -p uu_comm -p uu_cp -p uu_csplit -p uu_cut -p uu_date -p uu_dd -p uu_df -p uu_dir -p uu_dircolors -p uu_dirname -p uu_du -p uu_echo -p uu_env -p uu_expand -p uu_expr -p uu_factor -p uu_false -p uu_fmt -p uu_fold -p uu_groups -p uu_hashsum -p uu_head -p uu_hostid -p uu_hostname -p uu_id -p uu_install -p uu_join -p uu_kill -p uu_link -p uu_ln -p uu_logname -p uu_ls -p uu_mkdir -p uu_mkfifo -p uu_mknod -p uu_mktemp -p uu_more -p uu_mv -p uu_nice -p uu_nl -p uu_nohup -p uu_nproc -p uu_numfmt -p uu_od -p uu_paste -p uu_pathchk -p uu_pinky -p uu_pr -p uu_printenv -p uu_printf -p uu_ptx -p uu_pwd -p uu_readlink -p uu_realpath -p uu_rm -p uu_rmdir -p uu_seq -p uu_shred -p uu_shuf -p uu_sleep -p uu_sort -p uu_split -p uu_stat -p uu_stdbuf -p uu_sum -p uu_sync -p uu_tac -p uu_tail -p uu_tee -p uu_test -p uu_timeout -p uu_touch -p uu_tr -p uu_true -p uu_truncate -p uu_tsort -p uu_tty -p uu_uname -p uu_unexpand -p uu_uniq -p uu_unlink -p uu_uptime -p uu_users -p uu_vdir -p uu_wc -p uu_who -p uu_whoami -p uu_yes
   ```
