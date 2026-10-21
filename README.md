# Music Source Separation

This repository implements music source separation with
[Open-Unmix](https://github.com/sigsep/open-unmix). The model separates a
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
