```
pip install numpy pandas transformers protobuf sentencepiece
```

Install torch.


On local Windows machine
```
#!/bin/bash
..\memotrap-testing\myenv\Scripts\activate
export TRANSFORMERS_CACHE=C:\Users\steph\.cache\huggingface\hub

python3 simplebench_eval.py --q_id 2 --llm_name deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```

## To Update Remote Machine
To update code and clean up in one command, on remote machine, run:
```
./clean_up.sh
```

## To Run Long Experiment
On remote machine, run:
```
cd sbatch
./run_long_doubt_simple_bench_50min.sh
```



## TODO
- 50 responses at each temperature for DeepSeek on 10 simplebench questions
- Analyse it on a per-question basis (different lines same graph)

## DONE
- Cleaner that removes all machine files etc to a different folder, including chmod +x
- Get working Doubt Injector -- ensure works locally
- Results evaluator for simplebench json files, by scanning the `os.listdir` of `/responses`
