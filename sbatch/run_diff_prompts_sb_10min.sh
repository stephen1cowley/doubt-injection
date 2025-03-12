# q_id, doubt_injection, temperature csv, injection_string
injection_strings=(
    "But wait, I shouldn't assume a question is easy just because it seems so at first."
    "But wait, I should think about the real world."
    "But wait, the question may be a trick question."
    "I'm confused."
)

for injection_string in "${injection_strings[@]}"; do
    for _ in 1; do
        for i in 1; do
            sbatch simplebench_eval_20mins.wilkes3 $i 25 1.0 "\"$injection_string\""
        done
    done
done