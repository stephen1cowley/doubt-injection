#!/bin/bash
source /rds/user/ssc42/hpc-work/pytorch-env/bin/activate
export TRANSFORMERS_CACHE=/rds/user/ssc42/hpc-work

python3 test_3.py
