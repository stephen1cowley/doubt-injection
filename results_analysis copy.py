"""
This script analyzes the results of the experiments and saves the summary to a json file.
The results should be in json lists in `responses/aime/` of ExperimentResults schema.
"""

from typing import List, Dict, Tuple
import os
import json

files: List[str] = []

for file in os.listdir("responses/aime"):
    if file.endswith(".json") and file.startswith("results_q"):
        files.append(file)


# question -> (doubt_injection_prob -> temperature -> (correct, total))
results_per_question: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = {}

# question -> (doubt_injection_prob -> temperature -> (#exceeding 10k tokens, total))
exceeding_10k_tokens: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = {}

# question -> (doubt_injection_prob -> temperature -> (#no answer, total))
no_answer: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = {}


for file in files:
    # if int(re.sub('[a-zA-Z]', '', file.split("_")[-1].split(".")[0])) < 1740940200:
    #     # Not interested if it was one of the old results (before 6:30pm 2nd March)
    #     continue
    print(file)
    with open(os.path.join(f"responses/aime/{file}"), "r") as f:
        results: List[dict] = json.load(f)

        for result in results:
            temperature = str(result["temperature"])
            doubt_injection_prob = str(result["doubt_injection_prob"])
            question_id = str(result["question_id"])

            # Initialize nested dictionaries for results_per_question
            if question_id not in results_per_question:
                results_per_question[question_id] = {}
            if doubt_injection_prob not in results_per_question[question_id]:
                results_per_question[question_id][doubt_injection_prob] = {}
            if temperature not in results_per_question[question_id][doubt_injection_prob]:
                results_per_question[question_id][doubt_injection_prob][temperature] = (0, 0)

            if results_per_question[question_id][doubt_injection_prob][temperature][1] >= 4:
                continue
            # Update counts
            if result["llm_answer"] == result["correct_answer"]:
                results_per_question[question_id][doubt_injection_prob][temperature] = (
                    results_per_question[question_id][doubt_injection_prob][temperature][0] + 1,
                    results_per_question[question_id][doubt_injection_prob][temperature][1] + 1
                )
            else:
                results_per_question[question_id][doubt_injection_prob][temperature] = (
                    results_per_question[question_id][doubt_injection_prob][temperature][0],
                    results_per_question[question_id][doubt_injection_prob][temperature][1] + 1
                )

# Save results_summary to json
print(results_per_question)
with open("results_per_question_aime.json", "w") as f:
    json.dump(results_per_question, f, indent=4)
