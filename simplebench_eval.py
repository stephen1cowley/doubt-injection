from typing import List, Dict
import json
import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, DynamicCache
from dataclasses import dataclass, asdict


@dataclass
class ExperimentResult:
    temperature: float
    response_length: int
    llm_answer: str
    correct_answer: str
    llm_name: str
    question_id: int
    top_p: float
    prompt_name: str


llm_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
temperatures: List[float] = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
temperatures: List[float] = [0.0]
max_length: int = 20000
top_p: float = 0.95
prompt_name: str = "simplebench_deepseek.txt"

# Load questions
with open("simplebench/simplebench.json", "r") as f:
    questions: List[Dict[str, str]] = json.load(f)["eval_data"]
    num_questions = len(questions)
    print(f"Number of simplebench questions: {num_questions}")

# Load prompt
with open(f"prompts/{prompt_name}", "r") as f:
    prompt: str = f.read()

# Load model
tokenizer = AutoTokenizer.from_pretrained(llm_name)
model = AutoModelForCausalLM.from_pretrained(llm_name, torch_dtype=torch.bfloat16)
model = model.to("cuda" if torch.cuda.is_available() else "cpu")  # Move model to GPU if available

# Check model
print(f"Model: {llm_name}")
print(f"Model dtype: {model.dtype}")

# Initialize results list
results: List[ExperimentResult] = []

# Evaluate
for question_id in range(num_questions):
    question: str = questions[question_id]["prompt"]
    answer: str = questions[question_id]["answer"]

    llm_prompt: str = prompt.format(question=question)
    print(llm_prompt)

    for temperature in temperatures:
        input_ids: torch.Tensor = tokenizer.encode(llm_prompt, return_tensors="pt").to(model.device)
        cache = None

        # Generate one token at a time
        while True:
            # Generate next token using forward pass
            with torch.no_grad():
                outputs = model(
                    input_ids=input_ids if cache is None else input_ids[:, -1:],
                    past_key_values=cache,
                    use_cache=True,
                )

            # Get logits and updated past key values
            if cache is None:
                print("\n--------------------------------\n")
            next_token_logits = outputs.logits[:, -1, :]
            cache = DynamicCache.from_legacy_cache(outputs.past_key_values)

            # Sample next token
            if temperature == 0.0:
                # For temperature 0, just take the argmax (greedy decoding)
                next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
            else:
                # Regular temperature sampling
                probs = torch.nn.functional.softmax(next_token_logits / temperature, dim=-1)

                # Sort probabilities in descending order
                sorted_probs, sorted_indices = torch.sort(probs, descending=True)
                cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

                # Create nucleus mask
                nucleus_mask = cumulative_probs <= top_p
                nucleus_mask[..., 1:] = nucleus_mask[..., :-1].clone()
                nucleus_mask[..., 0] = True

                # Apply mask and renormalize
                sorted_probs[~nucleus_mask] = 0
                sorted_probs = sorted_probs / sorted_probs.sum()

                # Sample from filtered distribution
                next_token_idx = torch.multinomial(sorted_probs, num_samples=1)
                next_token = sorted_indices[0, next_token_idx]

            # Print the new token
            print(tokenizer.decode(next_token[0], skip_special_tokens=False), end='', flush=True)

            # Break if we hit the end token or max length
            if next_token[0] == tokenizer.eos_token_id or input_ids.shape[1] >= max_length:
                break

            # Update input_ids for next iteration
            input_ids = torch.cat([input_ids, next_token], dim=-1)

        llm_response: str = tokenizer.decode(
            input_ids[0],
            skip_special_tokens=True
        )[len(llm_prompt):]

        llm_answer: str = llm_response.split('<answer>')[-1].split('</answer>')[0].strip()

        print("\n")
        if len(llm_answer) != 1:
            print(f"LLM failed to generate a single answer for question {question_id + 1}")
            llm_answer = "X"

        result = ExperimentResult(
            temperature=temperature,
            response_length=len(input_ids[0]),
            llm_answer=llm_answer,
            correct_answer=answer,
            llm_name=llm_name,
            question_id=question_id+1,
            top_p=top_p,
            prompt_name=prompt_name
        )
        results.append(result)

        print(f"LLM answer at temperature {result.temperature}: {result.llm_answer}")
        print(f"Correct answer: {result.correct_answer}")
        print("\n--------------------------------\n")

# Save results to JSON file with timestamp
timestamp = int(time.time())
output_filename = f"responses/results_{timestamp}.json"
with open(output_filename, "w") as f:
    # Convert dataclass objects to dictionaries
    json_results = [asdict(result) for result in results]
    json.dump(json_results, f, indent=2)

print(f"Results saved to {output_filename}")
