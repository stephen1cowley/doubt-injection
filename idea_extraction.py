from typing import List
import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


IDEAS_LIST = [
    "the farmer returning alone",
    "the setup in the classic version being different",
    "the farmer's presence prevents adverse interactions",
    "the puzzle being unsolvable",
    "'I'm confused'",
    "the wolf and cabbage starting on the left",
    "the solution seems too simple"
    "7 numbered steps to solve the puzzle"
]


def make_coherent(
    chunk: str,
    remove_end: bool = True,
    remove_start: bool = True
) -> str:
    "Trim the text chunk to start at a new sentence and finish at the end of a sentence"
    end_chars = [".", "\n"]
    # End at a logical end
    if remove_end:
        i: int = len(chunk) - 1
        while chunk[i] not in end_chars and i > 0:
            i -= 1
        chunk = chunk[:i+1]
    # Start at a logical start
    if remove_start:
        i: int = 0
        while chunk[i] not in end_chars and i < len(chunk)-1:
            i += 1
    return chunk[i+1:]


# Query LLM
llm_name = "Qwen/Qwen2.5-1.5B"
tokenizer = AutoTokenizer.from_pretrained(llm_name)
model = AutoModelForCausalLM.from_pretrained(llm_name, torch_dtype=torch.bfloat16)
model = model.to("cuda" if torch.cuda.is_available() else "cpu")  # Move model to GPU if available
# Check model's dtype
print(f"Model dtype: {model.dtype}")
print(f"First layer dtype: {next(model.parameters()).dtype}")


response_files: List[str] = os.listdir("responses")


# Read last response
with open("responses/" + response_files[-1], 'r') as f:
    response: str = json.load(f)[0]

# Split up into N characters with overlap
chunk_size = 500
chunks = [response[i:i + chunk_size] for i in range(0, len(response), chunk_size//2)]
chunks[0] = make_coherent(chunks[0], remove_start=False)
chunks[-1] = make_coherent(chunks[-1], remove_end=False)
for i in range(1, len(chunks)-1):
    chunks[i] = make_coherent(chunks[i])


for idea in IDEAS_LIST:
    for i in range(len(chunks)):
        print("\n\n--------------------------------------")

        prompt = f"""
Given the following passage, give an answer which is either 'true' or 'false'.
Passage:

{chunks[i]}

(end of passage)
Did the passage contain mention of {idea}?
Answer (true/false): """

        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
        output = model.generate(
            input_ids,
            max_new_tokens=1
        )

        print(tokenizer.decode(output[0], skip_special_tokens=True))
