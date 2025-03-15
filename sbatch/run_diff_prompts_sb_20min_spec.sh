# q_id, doubt_injection, temperature csv, injection_string
injection_strings=(
    "But wait, I shouldn't assume a question is easy just because it seems so at first."
    "But wait, I should think about the real world."
    "But wait, the question may be a trick question."
    "I'm confused."
)

for i in 40 50; do
    for _ in {1..50}; do
        for j in 1 2 3 8 9 10; do
            sbatch simplebench_eval_20mins.wilkes3 $j $i 1.0 "But"
        done
    done
done
