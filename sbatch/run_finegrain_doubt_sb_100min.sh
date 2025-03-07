# This script corrects for some missing runs (worked out manually)
# Q1
# sbatch simplebench_eval_100mins.wilkes3 1 50

# Q2
# sbatch simplebench_eval_100mins.wilkes3 2 50
sbatch simplebench_eval_100mins.wilkes3 2 50 0.0,0.25,0.5,0.75,1.0,1.25,1.5

# Q3
# sbatch simplebench_eval_100mins.wilkes3 3 0

# Q8
# All good

# Q9
# sbatch simplebench_eval_100mins.wilkes3 9 0
for _ in {1..12}; do
    sbatch simplebench_eval_100mins.wilkes3 9 0 0.0,0.25,0.5,0.75,1.0,1.25,1.5
done
for _ in {1..5}; do
    sbatch simplebench_eval_100mins.wilkes3 9 50 0.0,0.25,0.5,0.75,1.0,1.25,1.5
done

# Q10
sbatch simplebench_eval_100mins.wilkes3 10 0 0.0,0.25,0.5,0.75,1.0,1.25,1.5
