from typing import Dict, Tuple
import json


with open("results_per_doubtprob.json", "r") as f:
    results_per_doubtprob: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = json.load(f)
    # question -> (temperature -> (doubt_injection_prob -> (correct, total)))

with open("results_per_question_even_weights.json", "r") as f:
    results_per_question_even_weights: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = json.load(f)
    # question -> (doubt_injection_prob -> temperature -> (correct, total))

# From results_per_question_even_weights, only keep T=1.0, doubt_injection_prob=0.25
for question_id in results_per_doubtprob:
    for doubt_injection_prob in results_per_question_even_weights[question_id]:
        for temperature in results_per_question_even_weights[question_id][doubt_injection_prob]:
            if temperature != "1.0":
                continue
            if doubt_injection_prob == "0.0":
                results_per_doubtprob[question_id][temperature][doubt_injection_prob] = results_per_question_even_weights[question_id][doubt_injection_prob][temperature]


with open("results_per_doubtprob_updated.json", "w") as f:
    json.dump(results_per_doubtprob, f)
