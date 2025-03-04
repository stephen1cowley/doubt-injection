for _ in {1..100}; do
    for i in 1 2 3 5 8 9 10; do
        for j in 0 50; do
            sbatch simplebench_eval_50mins.wilkes3 $i $j
        done
    done
done