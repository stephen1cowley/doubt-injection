# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

llm_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
# llm_name = "Qwen/Qwen2.5-1.5B"

tokenizer = AutoTokenizer.from_pretrained(llm_name)
model = AutoModelForCausalLM.from_pretrained(llm_name, torch_dtype=torch.bfloat16)
model = model.to("cuda" if torch.cuda.is_available() else "cpu")  # Move model to GPU if available

# Check model's dtype
print(f"Model dtype: {model.dtype}")
print(f"First layer dtype: {next(model.parameters()).dtype}")

# Prepare initial input
input_ids = tokenizer.encode("User: Solve the equation 5x^2 + 8x + 1 = 0. Assistant:", return_tensors="pt").to(model.device)
past_key_values = None

# Generate one token at a time
while True:
    # Generate next token using forward pass
    with torch.no_grad():
        outputs = model(
            input_ids=input_ids if past_key_values is None else input_ids[:, -1:],
            past_key_values=past_key_values,
            use_cache=True,
        )

    # Get logits and updated past key values
    next_token_logits = outputs.logits[:, -1, :]
    past_key_values = outputs.past_key_values

    # Sample next token
    probs = torch.nn.functional.softmax(next_token_logits / 0.7, dim=-1)
    next_token = torch.multinomial(probs, num_samples=1)

    # Print the new token
    print(tokenizer.decode(next_token[0], skip_special_tokens=True), end='', flush=True)

    # Break if we hit the end token or max length
    if next_token[0] == tokenizer.eos_token_id or input_ids.shape[1] >= 500:
        break

    # Update input_ids for next iteration
    input_ids = torch.cat([input_ids, next_token], dim=-1)

print()  # New line after generation is complete
