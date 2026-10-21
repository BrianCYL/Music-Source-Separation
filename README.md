# Music Source Separation

This repository implements music source separation with
[Open-Unmix](https://github.com/sigsep/open-unmix-pytorch). The model separates a
mixture into vocals and the remaining accompaniment. The provided checkpoints
are trained with the MUSDB18-HQ dataset.

## Setup

Download the model checkpoints from the
[Google Drive](https://drive.google.com/drive/folders/1bBZqflie5vj9ULSPvPUGdCZG9samhHEa?usp=sharing).

Install the dependencies listed by running:

```bash
pip install -r requirements.txt
```

Run all commands from the `Music-Source-Separation/` directory. For GPU inference, install a
PyTorch and TorchAudio build compatible with the available CUDA version.

Place the MUSDB18-HQ dataset, which can be downloaded on [this website](https://zenodo.org/records/3338373) and the model checkpoint under the same parent
directory as this repository. The expected structure is:

```text
Music-Source-Separation/
├── dataset/
│   └── train/
│       ├── ...
│   └── valid/
│       ├── ...
│   └── test/
│       ├── A1 James - Schoolboy Facination/
│       │   └── ...
│       ├── AM Contra - Heart Peripheral/
│       │   └── ...
│       └── ...
├── openunmix/
├── code/
└── checkpoints_best/
│   ├── separator.json
│   ├── vocals.json
│   └── vocals.pth
└── ...
```

The `checkpoints_best/` directory is a custom checkpoint directory. It must
contain `separator.json` and the target model files. The repository also
contains checkpoints from other training epochs, such as
`checkpoints_25/`, `checkpoints_50/`, and `checkpoints_150/`.

## Training

Train the vocals separator from the project root with the MUSDB18-HQ dataset.
The trainer reads the dataset from `./dataset`, saves checkpoints under the
selected output folder, and writes a `separator.json` file plus the model
snapshot(s) for the target source.

```bash
python code/train.py \
  --root ./dataset \
  --target vocals \
  --output ./checkpoints_hidden256 \
  --batch-size 128 \
  --hidden-size 256 \
  --epochs 200 \
  --patience 50 \
  --nb-workers 8
```

To train the larger variant, change the hidden size and output directory:

```bash
python code/train.py \
  --root ./dataset \
  --target vocals \
  --output ./checkpoints_hidden1024 \
  --batch-size 128 \
  --hidden-size 1024 \
  --epochs 200 \
  --patience 50 \
  --nb-workers 8
```

Optional training flags supported by the project code include:

- `--unidirectional` to use a unidirectional LSTM;
- `--checkpoint <path>` to resume training from a saved checkpoint; and
- `--model <path>` to fine-tune a pretrained model.

The best model is saved as `vocals_best.pth` (or the corresponding target name),
with validation and training histories stored in the output directory as JSON
metadata.

## Inference and evaluation

Inference is implemented in `code/evaluate.py`. It loads the custom
checkpoint, iterates over the selected MUSDB18 subset, separates each track
into the requested targets, and evaluates the estimates with `museval`.
The code also maps the residual source to `accompaniment` when
`--residual` is enabled.

Run inference and evaluation on the MUSDB18 test subset:

```bash
python code/evaluate.py \
  --root ./dataset \
  --subset test \
  --model ./checkpoints_best \
  --targets vocals \
  --residual residual \
  --outdir ./result \
  --evaldir ./data/eval
```

The command:

- loads `./checkpoints_best/` as the separator model;
- uses the `vocals` checkpoint target;
- creates `accompaniment` from the residual mixture;
- saves separated WAV files under `./result/`;
- saves per-track `museval` JSON files under `./data/eval/`; and
- saves the aggregated evaluation store as `./checkpoints_best.pandas`.

To force CPU inference or evaluate multiple tracks in parallel:

```bash
python code/evaluate.py \
  --root ./dataset \
  --subset test \
  --model ./checkpoints_best \
  --targets vocals \
  --residual accompaniment \
  --outdir ./result \
  --evaldir ./data/eval \
  --no-cuda \
  --cores 4
```

The `--niter` option controls the number of post-processing refinement
iterations. Use `--niter 0` for faster inference. The `--phase-estimation`
option can be set to `griffinlim` to use the Griffin-Lim reconstruction path.
The default value, `None`, uses the direct waveform estimates.

## Calculate median SDR metrics

After evaluation, summarize the test-set metrics with:

```bash
python code/metric_calculation.py --folder_dir ./data/eval
```

The script prints the median SDR, SIR, SAR, and ISR:

```text
SDR: ...
SIR: ...
SAR: ...
ISR: ...
```

If `--folder_dir` points directly to a directory containing evaluation JSON
files, the script uses it directly; otherwise it appends `/test`.
