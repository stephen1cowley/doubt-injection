from typing import List
import os
import time
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


question = """
A conversation between User and Assistant. The user asks a question, and the Assistant solves it. The assistant first thinks about the reasoning process in the mind and then provides the user with the answer. The reasoning process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively, i.e., <think> reasoning process here </think> <answer> answer here </answer>. User:
Solve the following puzzle: A man and a goat are on the left side of a river.
There is a wolf and a cabbage on the right side of the river.
The man has a boat.
The boat can carry only the farmer and a single item.
How can the farmer get the goat to the right side of the river?
Assistant: """


IDEAS_LIST = [
    "'the farmer returning alone'",
    "'the setup in the classic version being different'",
    "'the farmer's presence prevents adverse interactions'",
    "'the puzzle is unsolvable'",
    "'I'm confused'",
    "'the wolf and cabbage start on the left'",
    "'the solution seems too simple'",
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
llm_name = "Qwen/Qwen2.5-32B"
tokenizer = AutoTokenizer.from_pretrained(llm_name)
model = AutoModelForCausalLM.from_pretrained(llm_name, torch_dtype=torch.bfloat16)
model = model.to("cuda" if torch.cuda.is_available() else "cpu")  # Move model to GPU if available
# Check model's dtype
print(f"Model dtype: {model.dtype}")
print(f"First layer dtype: {next(model.parameters()).dtype}")


response_files: List[str] = sorted(os.listdir("responses"))[-250:]

n = 0
for response_file in response_files:
    time_0 = time.time()
    ideas: List[bool] = [False] * len(IDEAS_LIST)

    # Read last response
    with open("responses/" + response_file, 'r') as f:
        response: str = json.load(f)[0]
        response = response[len(question):]

    # Split up into N characters with overlap
    chunk_size = 500
    chunks = [response[i:i + chunk_size] for i in range(0, len(response), chunk_size//2)]
    chunks[0] = make_coherent(chunks[0], remove_start=False)
    chunks[-1] = make_coherent(chunks[-1], remove_end=False)
    for i in range(1, len(chunks)-1):
        chunks[i] = make_coherent(chunks[i])

    for idea_id in range(len(IDEAS_LIST)):
        for i in range(len(chunks)):
            if chunks[i] == "":
                continue

            print("\n\n--------------------------------------")

            prompt = f"""
You must read and answer a question about the passage that follows. The answer given must either be 'yes' or 'no'.
Passage:

{chunks[i]}

(end of passage)
Question: Does the passage contain explicit mention of {IDEAS_LIST[idea_id]}?
Answer (yes/no): """

            input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
            output = model.generate(
                input_ids,
                max_new_tokens=1
            )

            print(tokenizer.decode(output[0], skip_special_tokens=True))
            ans = tokenizer.decode(output[0], skip_special_tokens=True)[len(prompt):]
            print("\n ANS:", ans)

            if "yes" in ans:
                ideas[idea_id] = True
                break

    with open(f"ideas/ideas_{response_file}", "w") as f:
        json.dump(ideas, f)

    print(response_file)
    print(f"{n} ###### Reponse took {time.time() - time_0}")
    n += 1
