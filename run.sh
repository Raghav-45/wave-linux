#!/bin/bash

# Boolean variable to control the use of -nographic and -append 'console=ttyS0'
USE_CONSOLE=false

# Basic qemu command
CMD="qemu-system-x86_64 -kernel bzImage -initrd initrd.img"

# Check the boolean variable and modify the command accordingly
if [ "$USE_CONSOLE" = true ]; then
    CMD="$CMD -nographic -append 'console=ttyS0'"
fi

# Execute the command
eval $CMD
