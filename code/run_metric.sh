for i in 25 50 150 best griffinlim nonlstm noaug unidir hidden256 hidden1024
do
    echo "Evaluating epoch" $i
    python ./hw2_code/metric_calculation.py \
        --folder_dir ./eval_$i/
done