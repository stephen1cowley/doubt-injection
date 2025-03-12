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
- Initially done 10 reponses for each one of 10 simplebench questions, for each 6 probabilities of injection, for each of 7 temperatures. Therefore $10\times10\times6\times7=4,200$ reponses. 100 GPU hrs approx. (0.25hrs per 10 responses)
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
- Tokens for the start of a word like to first start with a space!!


- The dream: 100 reponses for each, not 10.
- Finer-grained temperature measurements (every 0.1)
- $100\times10\times6\times14=84,000$ responses (2000 GPU hrs approx).
- Hmm, I could maybe do 50 reponses, and don't bother with fine-grained (hence 500 GPU hrs approx)

### EXPERIMENT 1
- Doing currently: $20\times10\times5\times7=7000$ responses (175 GPU hrs)

### EXPERIMENT 2
Explore the range of $T\in[0.6, 1.1]$. Only for $p\in\{0.0, 0.5\}$ as 0.5 showed the most promise. Only on subset of 7 questions (not 4, 6, 7; edit this in the shell script). Question is granularity of temperatures (tempted to not go too granular), as well as @X (tempted to go higher to reduce those pesky error bars...).

Roughly want to use on the order of the same amount of compute as the last experiment.

Do @100. Error bars will decrease size by ~2.5X. May be enough to not have overlapping error bars. Do T=0.6, 0.75, 0.9, 1.0, 1.1. (To try an exploit some existing results to minimise error bars).

Num responses: $100\times7\times2\times5=7000$ responses.

### Clean-up
Because of time out from long responses, this means there are currently *slightly* uneven weightings of the questionset per quesion.

To repair this, I have a small list of missing results.

Alternatively, just write a module that will take existing results and, for each datapoint in the json, make sure each question is weighted properly. Either by removing random results until they equalise, or 


### Finale
Want to get nice, polished results, that tell a story.

- Give a rest to SimpleBench
- Get proper, high quality NQ dataset
- Set up deepseek on NQ.
- Test effect of add-CAD in the CoT.
- Create error bar graphs for CAD stuff...


## TODO
- Same graph but response length <----- (easy nice graph)

- 5 or so different injection strings, try at T=1.0 only. (Aim is to find anything that improves!)
- Create a holiday list of things I need to run (GSM8K will be required to show how performance degrades across a different task.)
- Need *some* sort of literature review on CoT? Would be nice on background motivating that sort of stuff.
- Also *some* mini lit review on effect of temperature across different tasks!

## DONE
- Cleaner that removes all machine files etc to a different folder, including chmod +x
- Get working Doubt Injector -- ensure works locally
- Results evaluator for simplebench json files, by scanning the `os.listdir` of `/responses`
- Analyse it on a per-question basis (different lines same graph)
- SOlve why We get a weird double space. Use injection ids found in actual repsponses?
- TEST whether new injection solves problem!!
- Create plots, do a write up plus plan for final 2 weeks
- 50 responses at each temperature for DeepSeek on 10 simplebench questions
- Equal weighting of the 6 questions, for fair comparisons!
