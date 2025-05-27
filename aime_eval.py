"""
This script is used to evaluate the performance of a given LLM on the AIME dataset.

A major difference between this script and simplebench_eval is that this script uses a chat template
to generate the input ids. This ensures the correct formatting of the input is used.

Also we prompt it to put the answer into \\boxed{} tags.

Usage:
python aime_eval.py --doubt_injection 0 --llm_name "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    --prompt_name "aime_deepseek.txt" --temperature_set "0.6" --injection_string "But"
"""

from typing import List, Dict
import json
import torch
import time
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM, DynamicCache
from dataclasses import asdict
from experiment_types import ExperimentResult


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate AIME questions')
    parser.add_argument('--doubt_injection', type=int, default=0,
                        help='0-100 probability to inject doubt into the response')
    parser.add_argument('--llm_name', type=str,
                        default="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
                        help='LLM name or path')
    parser.add_argument('--prompt_name', type=str,
                        default="aime_deepseek.txt",
                        help='Prompt name')
    parser.add_argument('--temperature_set', type=str,
                        default="0.6",
                        help='Temperature set (string)')
    parser.add_argument('--injection_string', type=str,
                        default="But",
                        help='Injection string')
    parser.add_argument('--spec_question', type=int,
                        default=None,
                        help='Specific question to evaluate')
    return parser.parse_args()


def main():
    args = parse_args()
    llm_name: str = args.llm_name
    temperature: float = float(args.temperature_set)
    max_length: int = 32768
    top_p: float = 0.95
    prompt_name: str = args.prompt_name
    doubt_injection_prob: float = args.doubt_injection / 100
    injection_string: str = args.injection_string
    spec_question: int = args.spec_question
    print(f"Injection string: {injection_string}")

    # Load questions
    with open("aime/aime_2024.json", "r") as f:
        questions: List[Dict[str, str]] = json.load(f)
        num_questions = len(questions)
        print(f"Number of aime questions: {num_questions}")

    # Load prompt
    with open(f"prompts/{prompt_name}", "r") as f:
        prompt: str = f.read()

    # Load model
    tokenizer = AutoTokenizer.from_pretrained(llm_name)

    # Solving the issue when multiple processes try to download the model at the same time
    max_retries = 6
    base_wait_time = 2  # seconds
    for attempt in range(max_retries):
        try:
            model = AutoModelForCausalLM.from_pretrained(llm_name, torch_dtype=torch.bfloat16)
            break
        except FileExistsError:
            if attempt == max_retries - 1:
                raise  # Re-raise the error if we've exhausted all retries
            # Exponential backoff: 2s, 4s, 8s, 16s...
            wait_time = base_wait_time * (2 ** attempt)
            print(f"Symlink already exists, waiting {wait_time}s before retry {attempt + 1}/"
                  f"{max_retries}")
            time.sleep(wait_time)

    model = model.to("cuda" if torch.cuda.is_available() else "cpu")

    # Check model
    print(f"Model: {llm_name}")
    print(f"Model dtype: {model.dtype}")

    # Initialize results list
    results: List[ExperimentResult] = []

    # Set doubtful statement
    if args.doubt_injection:
        doubtful_statement_ids: torch.Tensor = tokenizer.encode(
            injection_string, return_tensors="pt", add_special_tokens=False).to(model.device)

    doubtful_prefix: List[str] = [".\n\n", " \n\n", "\n\n",  ". \n\n"]

    for q_id in range(num_questions):
        if spec_question:
            q_id = spec_question - 1
        # Evaluate
        question: str = questions[q_id]["problem"]
        answer: str = questions[q_id]["answer"]
        chat = [
            {"role": "user", "content": prompt + question}
        ]
        time_0 = time.time()
        tokenized_input = tokenizer.apply_chat_template(chat, add_generation_prompt=True)
        input_ids = torch.tensor([tokenized_input]).to(model.device)
        print(tokenizer.decode(input_ids[0]))
        input_length: int = len(input_ids[0])
        print(f"Input length: {input_length}")
        # Initialize cache to be empty each response -- save memory
        past_key_values = DynamicCache()

        # Generate one token at a time
        first_token: bool = True
        in_cot: bool = True
        num_tokens: int = 0
        while True:
            # Generate next token using forward pass
            with torch.no_grad():
                outputs = model(
                    input_ids=input_ids if first_token else input_ids[:, -1:],
                    past_key_values=past_key_values,
                    use_cache=True,
                )

            # Get logits and updated past key values
            if first_token:
                print("\n--------------------------------\n")
            next_token_logits = outputs.logits[:, -1, :]

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
            curr_token: str = tokenizer.decode(next_token[0], skip_special_tokens=False)

            if args.doubt_injection:
                if "</think>" in curr_token:
                    in_cot = False

            # Break if we hit the end token or max length
            if next_token[0] == tokenizer.eos_token_id or input_ids.shape[1] >= max_length:
                print(f"###Reached max length: {input_ids.shape[1]}###")
                break

            if args.doubt_injection and curr_token in doubtful_prefix and in_cot:
                # if input_ids.shape[1] >= 9000:
                #     # Inject the end of thought token
                #     end_think_token = tokenizer.encode("</think>\n\n", return_tensors="pt",
                #                                        add_special_tokens=False).to(model.device)
                #     input_ids = torch.cat(
                #         [input_ids, next_token, end_think_token], dim=-1)
                #     print(curr_token + "</think>" + "###forced_stop###", end='', flush=True)
                #     in_cot = False
                # elif args.doubt_injection:
                # Inject doubt into the response on '.\n\n'
                if torch.bernoulli(torch.tensor([doubt_injection_prob])).item() == 1:
                    input_ids = torch.cat(
                        [input_ids, next_token, doubtful_statement_ids], dim=-1)
                    print(curr_token + injection_string + "###injection###", end='', flush=True)
                else:
                    input_ids = torch.cat([input_ids, next_token], dim=-1)
                    print(curr_token, end='', flush=True)
            else:
                # Update input_ids for next iteration
                input_ids = torch.cat([input_ids, next_token], dim=-1)
                print(curr_token, end='', flush=True)

            if first_token:
                first_token = False
            
            num_tokens += 1

        llm_response: str = tokenizer.decode(
            input_ids[0],
            skip_special_tokens=True
        )

        llm_answer: str = llm_response.split('\\boxed{')[-1].split('}')[0].strip()

        print("\n")
        # if len(llm_answer) != 1:
        #     print(f"LLM failed to generate a single answer for question {q_id + 1}")
        #     llm_answer = "X"

        result = ExperimentResult(
            temperature=temperature,
            response_length=len(input_ids[0])-input_length,
            llm_answer=llm_answer,
            correct_answer=answer,
            llm_name=llm_name,
            question_id=q_id+1,
            top_p=top_p,
            prompt_name=prompt_name,
            doubt_injection_prob=doubt_injection_prob,
            injection_string=injection_string
        )
        results.append(result)

        print(f"Question {q_id+1}:")
        print(f"LLM answer at temperature {result.temperature}: {result.llm_answer}")
        print(f"Probability of doubt injection: {doubt_injection_prob}")
        print(f"Correct answer: {result.correct_answer}")
        print(f"Time taken: {time.time() - time_0:.2f} seconds")
        print("\n--------------------------------\n")

        # Calculate results every question
        # Save results to JSON file with timestamp
        timestamp = int(time.time())
        output_filename = (f"responses/aime/results_q{str(q_id+1)}_"
                           f"d{str(args.doubt_injection)}_p{str(int(timestamp))}.json")
        with open(output_filename, "w") as f:
            # Convert dataclass objects to dictionaries
            json_results = [asdict(result) for result in results]
            json.dump(json_results, f, indent=2)

        print(f"Results saved to {output_filename}")
        results = []

        if spec_question:
            break


if __name__ == "__main__":
    main()
