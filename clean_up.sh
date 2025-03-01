#!/bin/bash
# Move all .out files to outputs directory
find . -name "*.out" -exec mv {} outputs/ \;
# Move all machine.file.* files to outputs directory
find . -name "machine.file.*" -exec mv {} outputs/ \;

git stash
git pull
chmod +x *.sh *.wilkes3 /sbatch/*.sh /sbatch/*.wilkes3
