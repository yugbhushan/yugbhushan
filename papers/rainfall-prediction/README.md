# Rainfall prediction: paper and pipeline

[Project overview](../../projects/rainfall-prediction.md) · [Read the paper](report.pdf) · [LaTeX](main.tex)

The supplied manuscript's Python appendix specifies a **reconstruction protocol**, not the original experiment. It fits an OLS next-day model for Delhi, Chennai and Agra, with training-only standardization, a chronological 70/30 split, a boundary purge, and persistence/training-mean baselines.

## Run

Install the root requirements first, then run from the repository root:

```sh
python papers/rainfall-prediction/rainfall_analysis.py weather.csv --out runs/rainfall-paper
```

CSV columns:

| Column | Meaning / unit |
| --- | --- |
| date | Daily date, YYYY-MM-DD; one record per city/date |
| city | Delhi, Chennai or Agra; all three must occur |
| temperature | Degrees Celsius |
| humidity | Relative humidity, percent from 0 to 100 |
| wind_speed | Metres per second, nonnegative |
| pressure | Surface pressure in hPa, positive |
| rainfall | Daily rainfall in mm, nonnegative |

The script needs at least 40 complete next-day pairs per city, variable training predictors, and a full-rank design. Missing calendar days remain gaps before target shifting. Predictions remain raw OLS values, which can be negative; any nonnegative postprocessing requires separate evaluation.

Outputs include per-city coefficients, predictions, diagnostic figures and combined metrics (R, R², MSE, RMSE, MAE and bias). The historical R = 0.95–0.99 is not hard-coded into the pipeline. Original measurements were not supplied.

`worked_example.pdf` contains an illustrative figure used by `main.tex`. Compile the paper in this directory with `pdflatex main.tex` twice.
