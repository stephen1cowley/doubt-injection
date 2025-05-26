# sbatch aime_eval_2hrs.wilkes3 0 "But"

for _ in {1..4}; do
    sbatch aime_eval_2hrs.wilkes3 0 "But"
    sbatch aime_eval_2hrs.wilkes3 5 "But"
    sbatch aime_eval_2hrs.wilkes3 10 "But"
    sbatch aime_eval_2hrs.wilkes3 25 "But"
done
