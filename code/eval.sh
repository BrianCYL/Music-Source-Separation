python evaluate.py \
    --root dataset \
    --model ./checkpoints_best/ \
    --target vocals \
    --residual True \
    --is-wav \
    --outdir ./output/ \
    --evaldir ./eval/ \

echo "Calculating SDR matrix ..."
python metric_calculation.py \
    --folder_dir ./eval_best/test

