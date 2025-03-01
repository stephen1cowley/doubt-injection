A=$1
B=$2
for i in $(seq $A $B); do
    scancel --user=$USER $i
done