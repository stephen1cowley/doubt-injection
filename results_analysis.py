"""
This script analyzes the results of the experiments and saves the summary to a json file.
The results should be in json lists in `responses/` of ExperimentResults schema.
"""

from typing import List, Dict, Tuple
import os
import json

files: List[str] = []

for file in os.listdir("responses"):
    if file.endswith(".json") and file.startswith("results_q"):
        files.append(file)


# doubt_injection_prob -> temperature -> (correct, total)
results_summary: Dict[str, Dict[str, Tuple[int, int]]] = {}
# question -> (doubt_injection_prob -> temperature -> (correct, total))
results_per_question: Dict[str, Dict[str, Dict[str, Tuple[int, int]]]] = {}
for file in files:
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

            # Initialize nested dictionaries if they don't exist
            if doubt_injection_prob not in results_summary:
                results_summary[doubt_injection_prob] = {}
            if temperature not in results_summary[doubt_injection_prob]:
                results_summary[doubt_injection_prob][temperature] = (0, 0)

            # Initialize nested dictionaries for results_per_question
            if question_id not in results_per_question:
                results_per_question[question_id] = {}
            if doubt_injection_prob not in results_per_question[question_id]:
                results_per_question[question_id][doubt_injection_prob] = {}
            if temperature not in results_per_question[question_id][doubt_injection_prob]:
                results_per_question[question_id][doubt_injection_prob][temperature] = (0, 0)

            # Update counts
            if result["llm_answer"] == result["correct_answer"]:
                results_summary[doubt_injection_prob][temperature] = (
                    results_summary[doubt_injection_prob][temperature][0] + 1,
                    results_summary[doubt_injection_prob][temperature][1] + 1
                )
                results_per_question[question_id][doubt_injection_prob][temperature] = (
                    results_per_question[question_id][doubt_injection_prob][temperature][0] + 1,
                    results_per_question[question_id][doubt_injection_prob][temperature][1] + 1
                )
            else:
                results_summary[doubt_injection_prob][temperature] = (
                    results_summary[doubt_injection_prob][temperature][0],
                    results_summary[doubt_injection_prob][temperature][1] + 1
                )
                results_per_question[question_id][doubt_injection_prob][temperature] = (
                    results_per_question[question_id][doubt_injection_prob][temperature][0],
                    results_per_question[question_id][doubt_injection_prob][temperature][1] + 1
                )


# Save results_summary to json
print(results_summary)
with open("results_summary.json", "w") as f:
    json.dump(results_summary, f, indent=4)

# Save results_summary to json
print(results_summary)
with open("results_per_question.json", "w") as f:
    json.dump(results_per_question, f, indent=4)
