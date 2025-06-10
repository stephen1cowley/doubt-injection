from typing import Dict, Tuple
import json

with open("results_per_doubtprob_aime_length_10000_1p5B.json", "r") as f:
    results_1: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = json.load(f)

with open("results_per_doubtprob_aime_length_10000_32B.json", "r") as f:
    results_2: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = json.load(f)

# question -> (llm_name -> doubt_injection_prob -> (correct, total))
combined_results: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = {}

for question_id in results_1:
    combined_results[question_id] = {}
    question_results_1 = results_1[question_id]
    question_results_2 = results_2[question_id]

    for temp in question_results_1:
        combined_results[question_id]["1.5B"] = question_results_1[temp]
        combined_results[question_id]["32B"] = question_results_2[temp]

# Save results_summary to json
print(combined_results)
with open("combined_results_aime_exceeding_10000.json", "w") as f:
    json.dump(combined_results, f, indent=4)
