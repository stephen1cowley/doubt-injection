#!/bin/bash
# Update the repo
git stash
git pull
# Move all .out files to outputs directory
find . -not -path "./outputs/*" -name "*.out" -exec mv {} outputs/ \;
# Move all machine.file.* files to outputs directory
find . -not -path "./outputs/*" -name "machine.file.*" -exec mv {} outputs/ \;
# Make all scripts executable
chmod +x *.sh *.wilkes3 sbatch/*.sh sbatch/*.wilkes3
