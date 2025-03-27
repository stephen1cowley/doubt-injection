import json

with open("aime/aime_2024.json", "r") as f:
    data = json.load(f)


for i in range(len(data)):
    print(data[i]["problem"])
    print(int(data[i]["answer"]))
    print("-" * 100)
