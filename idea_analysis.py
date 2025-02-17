from typing import List
import json
import os

idea_files: List[str] = sorted(os.listdir("ideas"))
print(len(idea_files))
results: List[List[int]] = [[0 for _ in range(10)] for _ in range(5)]

for i in range(5):
    for j in range(50):
        # Read last response
        with open("ideas/" + idea_files[i*50+j], 'r') as f:
            ideas: List[bool] = json.load(f)

        for k in range(len(ideas)):
            results[i][k] += int(ideas[k])

print(results)
