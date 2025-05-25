"""
This script analyzes the results of the experiments and saves the summary to a json file.
The results should be in json lists in `responses/` of ExperimentResults schema.
"""

from typing import List, Dict, Tuple
import re
import os
import json

files: List[str] = []
injection_strings = [
    "But wait, I shouldn't assume a question is easy just because it seems so at first.",
    "But wait, I should think about the real world.",
    "But wait, the question may be a trick question.",
    "I'm confused."
]
# Note that for this experiment, all temperatures are 1.0, all doubt injection probs are 0.25.

for file in os.listdir("responses"):
    if file.endswith(".json") and file.startswith("results_q"):
        files.append(file)


# question -> (temperature -> (doubt_injection_prob -> (correct, total)))
results_per_doubtprob: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = {}

for file in files:
    if int(re.sub('[a-zA-Z]', '', file.split("_")[-1].split(".")[0])) < 1741852800:
        # Not interested if it was one of the old results (before 8:00am 13th March)
        continue
    print(file)
    with open(os.path.join(f"responses/{file}"), "r") as f:
        results: List[dict] = json.load(f)

        for result in results:
            # Handle case where injection_string key doesn't exist  
            if "injection_string" not in result:
                continue
            injection_string = str(result["injection_string"])
            if injection_string != "But":
                continue
            question_id = str(result["question_id"])
            temperature = str(result["temperature"])
            doubt_injection_prob = str(result["doubt_injection_prob"])

            # Initialize nested dictionaries for results_per_question
            if question_id not in results_per_doubtprob:
                results_per_doubtprob[question_id] = {}
            if temperature not in results_per_doubtprob[question_id]:
                results_per_doubtprob[question_id][temperature] = {}
            if doubt_injection_prob not in results_per_doubtprob[question_id][temperature]:
                results_per_doubtprob[question_id][temperature][doubt_injection_prob] = (0, 0)

            # HARD CODED:
            # cap at 50 (experiment is AVG@50)
            if results_per_doubtprob[question_id][temperature][doubt_injection_prob][1] >= 50:
                continue

            # Update counts
            # if result["llm_answer"] == result["correct_answer"]:
            #     results_per_doubtprob[question_id][temperature][doubt_injection_prob] = (
            #         results_per_doubtprob[question_id][temperature][doubt_injection_prob][0] + 1,
            #         results_per_doubtprob[question_id][temperature][doubt_injection_prob][1] + 1
            #     )
            # else:
            #     results_per_doubtprob[question_id][temperature][doubt_injection_prob] = (
            #         results_per_doubtprob[question_id][temperature][doubt_injection_prob][0],
            #         results_per_doubtprob[question_id][temperature][doubt_injection_prob][1] + 1
            #     )
            
            # Determine if length of response is greater than 10000
            if result["response_length"] > 10000:
                results_per_doubtprob[question_id][temperature][doubt_injection_prob] = (
                    results_per_doubtprob[question_id][temperature][doubt_injection_prob][0] + 1,
                    results_per_doubtprob[question_id][temperature][doubt_injection_prob][1] + 1
                )
            else:
                results_per_doubtprob[question_id][temperature][doubt_injection_prob] = (
                    results_per_doubtprob[question_id][temperature][doubt_injection_prob][0],
                    results_per_doubtprob[question_id][temperature][doubt_injection_prob][1] + 1
                )

# Save results_summary to json
print(results_per_doubtprob)
with open("results_per_doubtprob_length_10000.json", "w") as f:
    json.dump(results_per_doubtprob, f, indent=4)
