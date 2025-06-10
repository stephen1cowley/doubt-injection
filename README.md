# Doubt Injection

arXiv paper: (link coming soon)

## Evaluation Code
First install PyTorch from the official website. Then:
```
pip install numpy pandas transformers protobuf sentencepiece
```
To run an evaluation on the AIME 2024 dataset:
```
python3 aime_eval.py --doubt_injection $1 --llm_name "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B" --temperature_set "0.6" --injection_string "But"
```
To run a specific question evaluation on the SimpleBench dataset:
```
python simplebench_eval.py --q_id 2 --llm_name deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B --temperature_set "0.6" --injection_string "But"
```
