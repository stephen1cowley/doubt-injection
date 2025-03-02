for _ in {1..5}; do
    for i in {1..10}; do
        for j in 0 25 50 75 100; do
            sbatch simplebench_eval_50mins.wilkes3 $i $j
        done
    done
done