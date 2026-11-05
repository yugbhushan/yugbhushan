# Gas-sensor monitoring: paper and pipeline

[Project overview](../../projects/gas-sensor-monitoring.md) · [Read the paper](report.pdf) · [LaTeX](main.tex)

This supplied reconstruction protocol compares PCA + Random Forest with a forest without PCA and a majority-class baseline. It uses 128 features (eight per sensor for 16 sensors), six labels and ten batches. Its default split trains on batches 1–6 and evaluates batches 7–10. The older example in `code/gas.py` uses batches 1–7 for training; these are different declared experiments.

## Run

Install the root requirements first, then run from the repository root:

```sh
python papers/gas-sensor-monitoring/gas_sensor_analysis.py sensor_data.csv --out runs/gas-paper
python papers/gas-sensor-monitoring/gas_sensor_analysis.py sensor_data.csv --protocol random --out runs/gas-random
```

CSV columns must include `batch`, `class`, and `x1` through `x128`. Batches are integers 1–10, classes integers 1–6. Preserve the benchmark feature order. Values must be finite, and duplicate feature rows are rejected for investigation. All six classes must occur in training.

The default forest has 300 trees. `--trees N` changes the declared model; `--importance` enables grouped permutation analysis assuming eight adjacent features per sensor. Verify that ordering before interpreting physical sensor importance.

Outputs include pooled and per-batch metrics, saved split indices, class probabilities, predictions, confusion matrices, PCA variance/loadings and optional sensor-group importance. Undefined six-class AUC is stored as a blank value.

The CV's 97.8% accuracy, 97.6% F1 and 0.99 AUC remain historical reported figures. The original dataset, trained model and split were not supplied. Public UCI compatibility does not establish identity with the original experiment.

Compile the paper in this directory with `pdflatex main.tex` twice, keeping `pca_example.pdf` and the Python file alongside it.
