#!/bin/bash
source /rds/user/ssc42/hpc-work/pytorch-env/bin/activate
export TRANSFORMERS_CACHE=/rds/user/ssc42/hpc-work

python3 aime_eval.py --doubt_injection $1 --llm_name "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B" --temperature_set "0.6" --injection_string "$2" --spec_question $3
