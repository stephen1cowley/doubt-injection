for i in {1..10}; do
    sbatch simplebench_eval_50mins.wilkes3 $i 75
done