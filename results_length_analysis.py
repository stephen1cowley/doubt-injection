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


# doubt_injection_prob -> temperature -> (mean #tokens, 97.5% value, 2.5% value)
mean_tokens: Dict[str, Dict[str, Tuple[float, float, float]]] = {}

tokens_temp: Dict[str, Dict[str, List[int]]] = {}

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
            if question_id not in ["1", "2", "3", "8", "9", "10"]:
                continue
            if doubt_injection_prob not in ["0.0", "0.5"]:
                continue

            # Initialize nested dictionaries for mean_tokens
            if doubt_injection_prob not in tokens_temp:
                tokens_temp[doubt_injection_prob] = {}
            if temperature not in tokens_temp[doubt_injection_prob]:
                tokens_temp[doubt_injection_prob][temperature] = []

            # HARD CODED:
            # cap T=0.75,1.0 at 120
            # cap T=0.6, 0.9, 1.1 at 100
            # cap T=0.0, 0.25, 0.5, 1.25, 1.5 at 20
            if temperature in ["0.75", "1.0"] and len(tokens_temp[doubt_injection_prob][temperature]) >= 120:
                continue
            if temperature in ["0.6", "0.9", "1.1"] and len(tokens_temp[doubt_injection_prob][temperature]) >= 100:
                continue
            if temperature in ["0.0", "0.25", "0.5", "1.25", "1.5"] and len(tokens_temp[doubt_injection_prob][temperature]) >= 20:
                continue

            # Update tokens_temp
            tokens_temp[doubt_injection_prob][temperature].append(result["response_length"])


# Now calculate the mean, upper 95%, lower 95%
for doubt_injection_prob in tokens_temp:
    for temperature in tokens_temp[doubt_injection_prob]:
        tokens = tokens_temp[doubt_injection_prob][temperature]
        mean = sum(tokens) / len(tokens)
        upper_95 = sorted(tokens)[int(len(tokens) * 0.75)]
        lower_95 = sorted(tokens)[int(len(tokens) * 0.25)]
        if doubt_injection_prob not in mean_tokens:
            mean_tokens[doubt_injection_prob] = {}
        mean_tokens[doubt_injection_prob][temperature] = (mean, upper_95, lower_95)

# Save results_summary to json
print(mean_tokens)
with open("mean_tokens.json", "w") as f:
    json.dump(mean_tokens, f, indent=4)
