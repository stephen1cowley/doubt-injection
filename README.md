## Running
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

## NOTES
- Initially done 10 reponses for each one of 10 simplebench questions, for each 6 probabilities of injection, for each of 7 temperatures. Therefore $10*10*6*7=4,200$ reponses. 100 GPU hrs approx. (0.25hrs per 10 responses)
- I then realised because of weird output witht he injection, e.g.
```
But wait, let me think again.  maybe I missed something.

But wait, let me think again.  because 15 isn't an option, so I must have made a mistake.
```
- No capitalisation, weird extra space
- So I have changed the injection to *not* include a space after the full-stop. I think this is essentially in a weird, unexpected format for the particular tokenization of this particular LLM?
- Hopefully this is more in line with what the LLM is expecting.
- Unfortunately means initial results were a bit of a waste...?
- Reading the responses was critical to spotting this issue...
- YES, problem now solved.


- The dream: 100 reponses for each, not 10.
- Finer-grained temperature measurements (every 0.1)
- $100*10*6*14=84,000$ responses (2000 GPU hrs approx).
- Hmm, I could maybe do 50 reponses, and don't bother with fine-grained (hence 500 GPU hrs approx)

### CURRENT EXPERIMENT
- Doing currently: $20*10*5*7=7000$ responses (175 GPU hrs)

## TODO
- 50 responses at each temperature for DeepSeek on 10 simplebench questions
- Same graph but response length
- Create plots, do a write up plus plan for final 2 weeks

## DONE
- Cleaner that removes all machine files etc to a different folder, including chmod +x
- Get working Doubt Injector -- ensure works locally
- Results evaluator for simplebench json files, by scanning the `os.listdir` of `/responses`
- Analyse it on a per-question basis (different lines same graph)
- SOlve why We get a weird double space. Use injection ids found in actual repsponses?
- TEST whether new injection solves problem!!
