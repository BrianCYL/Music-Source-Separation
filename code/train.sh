# python train.py \
#     --root dataset \
#     --target vocals \
#     --output checkpoints_nonlstm \
#     --batch-size 128 \
#     --epochs 200 \
#     --patience 50 \
#     --nb-workers 8 \
#     --n_layers 1 \
#     --is-wav \

# python train.py \
#     --root dataset \
#     --target vocals \
#     --output checkpoints_unidir \
#     --batch-size 128 \
#     --epochs 200 \
#     --patience 50 \
#     --nb-workers 8 \
#     --unidirectional \
#     --is-wav \

# python train.py \
#     --root dataset \
#     --target vocals \
#     --output checkpoints_noaug \
#     --batch-size 128 \
#     --epochs 200 \
#     --patience 50 \
#     --nb-workers 8 \
#     --is-wav \
#     --source-augmentations "" \

python train.py \
    --root dataset \
    --target vocals \
    --output checkpoints_hidden256 \
    --batch-size 128 \
    --hidden-size 256 \
    --epochs 200 \
    --patience 50 \
    --nb-workers 8 \
    --is-wav \

python train.py \
    --root dataset \
    --target vocals \
    --output checkpoints_hidden1024 \
    --batch-size 128 \
    --hidden-size 1024 \
    --epochs 200 \
    --patience 50 \
    --nb-workers 8 \
    --is-wav \


