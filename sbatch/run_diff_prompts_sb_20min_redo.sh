# q_id, doubt_injection, temperature csv, injection_string
injection_strings=(
    "But wait, I shouldn't assume a question is easy just because it seems so at first."
    "But wait, I should think about the real world."
    "But wait, the question may be a trick question."
    "I'm confused."
)

# sbatch simplebench_eval_20mins.wilkes3 2 25 1.0 "\"I'm confused.\""
# sbatch simplebench_eval_20mins.wilkes3 2 25 1.0 "\"I'm confused.\""
# sbatch simplebench_eval_20mins.wilkes3 1 25 1.0 "\"I'm confused.\""

# sbatch simplebench_eval_20mins.wilkes3 2 25 1.0 "\"But wait, the question may be a trick question.\""
# sbatch simplebench_eval_20mins.wilkes3 3 25 1.0 "\"But wait, the question may be a trick question.\""
# sbatch simplebench_eval_20mins.wilkes3 8 25 1.0 "\"But wait, the question may be a trick question.\""
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, the question may be a trick question.\""
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, the question may be a trick question.\""
# sbatch simplebench_eval_20mins.wilkes3 10 25 1.0 "\"But wait, the question may be a trick question.\""
# sbatch simplebench_eval_20mins.wilkes3 10 25 1.0 "\"But wait, the question may be a trick question.\""

# sbatch simplebench_eval_20mins.wilkes3 3 25 1.0 "\"But wait, I shouldn't assume a question is easy just because it seems so at first.\""
# sbatch simplebench_eval_20mins.wilkes3 8 25 1.0 "\"But wait, I shouldn't assume a question is easy just because it seems so at first.\""

# sbatch simplebench_eval_20mins.wilkes3 2 25 1.0 "\"But wait, I should think about the real world.\""
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, I should think about the real world.\""
# sbatch simplebench_eval_20mins.wilkes3 10 25 1.0 "\"But wait, I should think about the real world.\""

# for i in 1 2 3 8 9 10; do
#     for _ in {1..20}; do
#         sbatch simplebench_eval_20mins.wilkes3 $i 25 1.0 "But"
#     done
# done

# for i in 1 2 3 8 9 10; do
#     for _ in {1..30}; do
#         sbatch simplebench_eval_20mins.wilkes3 $i 25 1.0 "\"But wait, let me think again.\""
#     done
# done

# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, let me think again.\""
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, let me think again.\""
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, let me think again.\""
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, let me think again.\""
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, let me think again.\""
# sbatch simplebench_eval_20mins.wilkes3 10 25 1.0 "\"But wait, let me think again.\""

# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "But"
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "But"
# sbatch simplebench_eval_20mins.wilkes3 1 25 1.0 "\"But wait, let me think again.\""
# sbatch simplebench_eval_20mins.wilkes3 8 25 1.0 "\"But wait, let me think again.\""
# sbatch simplebench_eval_20mins.wilkes3 9 25 1.0 "\"But wait, let me think again.\""
# sbatch simplebench_eval_20mins.wilkes3 10 25 1.0 "\"But wait, let me think again.\""

##
sbatch simplebench_eval_20mins.wilkes3 1 10 1.0 "But"
# sbatch simplebench_eval_20mins.wilkes3 1 40 1.0 "But"
# sbatch simplebench_eval_20mins.wilkes3 8 50 1.0 "But"
