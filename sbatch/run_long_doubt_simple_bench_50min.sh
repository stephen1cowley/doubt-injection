for i in {1..10}; do
    for j in 0 2 4 6 8 10; do
        sbatch simplebench_eval_50mins.wilkes3 $i $j
    done
done