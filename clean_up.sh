#!/bin/bash
# Copy all .out files to outputs directory
find . -name "*.out" -exec cp {} outputs/ \;
# Copy all machine.file.* files to outputs directory
find . -name "machine.file.*" -exec cp {} outputs/ \;

chmod +x *.sh *.wilkes3 /sbatch/*.sh /sbatch/*.wilkes3
