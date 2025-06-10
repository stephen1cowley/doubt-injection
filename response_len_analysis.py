import os
import json
from typing import Dict, List

with open(os.path.join(f"response_len_per_doubtprob_aime_newlim.json"), "r") as f:
    results: Dict[str, List[int]] = json.load(f)

for doubt_injection_prob in results:
    print(f"Doubt injection prob: {doubt_injection_prob}")
    print(sum(results[doubt_injection_prob]) / len(results[doubt_injection_prob]))
