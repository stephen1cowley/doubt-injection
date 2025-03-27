import pandas as pd

df = pd.read_parquet("hf://datasets/Maxwell-Jia/AIME_2024/aime_2024_problems.parquet")

# Convert to JSON
df.to_json("aime_2024_2.json", orient="records", indent=4)
