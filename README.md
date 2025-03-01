```
pip install numpy pandas transformers protobuf sentencepiece
```

Install torch.


```
#!/bin/bash
..\memotrap-testing\myenv\Scripts\activate
export TRANSFORMERS_CACHE=C:\Users\steph\.cache\huggingface\hub

python3 simplebench_eval.py --q_id 2 --llm_name deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```


## TODO
- Results evaluator for simplebench json files, by scanning the `os.listdir` of `/responses`
- 50 responses at each temperature for DeepSeek on 10 simplebench questions
- Get working Doubt Injector -- ensure works locally
