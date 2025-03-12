"""
This script analyzes the results of the experiments and saves the summary to a json file.
The results should be in json lists in `responses/` of ExperimentResults schema.
"""

from typing import List, Dict, Tuple
import re
import os
import json

files: List[str] = []

for file in os.listdir("responses"):
    if file.endswith(".json") and file.startswith("results_q"):
        files.append(file)


# question_id -> (doubt_injection_prob -> temperature -> (total # tokens, total #tokens^2, # responses))
mean_tokens: Dict[str, Dict[str, Dict[str, Tuple[int, int, int]]]] = {}


for file in files:
    if int(re.sub('[a-zA-Z]', '', file.split("_")[-1].split(".")[0])) < 1740940200:
        # Not interested if it was one of the old results (before 6:30pm 2nd March)
        continue
    print(file)
    with open(os.path.join(f"responses/{file}"), "r") as f:
        results: List[dict] = json.load(f)

        for result in results:
            # Handle case where doubt_injection_prob key doesn't exist
            if "doubt_injection_prob" not in result:
                continue
            # Handle case where temperature key doesn't exist
            if "temperature" not in result:
                continue  # Skip this result if temperature is missing
            temperature = str(result["temperature"])
            doubt_injection_prob = str(result["doubt_injection_prob"])
            question_id = str(result["question_id"])

            # Initialize nested dictionaries for mean_tokens
            if question_id not in mean_tokens:
                mean_tokens[question_id] = {}
            if doubt_injection_prob not in mean_tokens[question_id]:
                mean_tokens[question_id][doubt_injection_prob] = {}
            if temperature not in mean_tokens[question_id][doubt_injection_prob]:
                mean_tokens[question_id][doubt_injection_prob][temperature] = (0, 0, 0)

            # HARD CODED:
            # cap T=0.75,1.0 at 120
            # cap T=0.6, 0.9, 1.1 at 100
            # cap T=0.0, 0.25, 0.5, 1.25, 1.5 at 20
            if temperature in ["0.75", "1.0"] and mean_tokens[question_id][doubt_injection_prob][temperature][1] >= 120:
                continue
            if temperature in ["0.6", "0.9", "1.1"] and mean_tokens[question_id][doubt_injection_prob][temperature][1] >= 100:
                continue
            if temperature in ["0.0", "0.25", "0.5", "1.25", "1.5"] and mean_tokens[question_id][doubt_injection_prob][temperature][1] >= 20:
                continue
            # Update counts
            mean_tokens[question_id][doubt_injection_prob][temperature] = (
                mean_tokens[question_id][doubt_injection_prob][temperature][0] + result["response_length"],
                mean_tokens[question_id][doubt_injection_prob][temperature][1] + result["response_length"]**2,
                mean_tokens[question_id][doubt_injection_prob][temperature][2] + 1,
            )


# Save results_summary to json
print(mean_tokens)
with open("mean_tokens.json", "w") as f:
    json.dump(mean_tokens, f, indent=4)
