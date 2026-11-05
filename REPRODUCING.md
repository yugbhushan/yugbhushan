# Run the engineering portfolio

These are newly written Python reconstructions of four projects described in Yug Bhushan's CV. The checked-in figures and tables come from the programs in this repository. The project pages preserve the original academic findings separately.

## Install and run

Clone this repository and run these commands from its root using Python 3.12. The dependencies are pinned to the versions used for the checked-in outputs.

```sh
python -m venv .venv
# Linux or macOS
source .venv/bin/activate
# On Windows PowerShell use .venv\Scripts\Activate.ps1 instead.
python -m pip install -r requirements.txt
python run_all.py
python -m unittest discover -s tests -v
```

After installation the default examples run offline. Each command writes only to its output directory. Repeated runs overwrite files with the same name. To keep a separate run, use the individual program's `--out DIRECTORY` option.

| Project | Run from the repository root | Data or model | Outputs |
| --- | --- | --- | --- |
| [Gas classification](projects/gas-sensor-monitoring.md) | `python code/gas.py` | Seeded 16-channel signals across ten batches | Confusion matrix, predictions, metrics |
| [Packed bed](projects/packed-bed-transport.md) | `python code/packed_bed.py` | Uniform Ergun model and radial sensitivity study | Pressure curves, wall velocity, flow balance |
| [Brake heating](projects/brake-thermal-analysis.md) | `python code/brake.py` | Through-thickness transient finite elements | Temperature histories, energy balance, refinement check |
| [Rainfall](projects/rainfall-prediction.md) | `python code/rainfall.py` | Seeded daily weather for three city labels | Forecasts, coefficients, skill against persistence |

The gas model also accepts extracted UCI batch files. The rainfall model accepts a daily-observations CSV. Instructions and input units are on their respective project pages. The original notebooks, weather measurements and native COMSOL model were unavailable when these examples were built.

## Uploaded term-paper implementations

The [papers directory](papers/README.md) adds the four supplied PDFs, three complete LaTeX packages and the available Python appendices. These are separate from the older examples above. Follow each paper directory's README for its exact CSV schema and commands. In particular, the gas paper trains on batches 1–6; the older gas example uses 1–7.

The test suite checks both code families, including missing calendar dates, invalid sensor rows, undefined AUC, and thermal energy conservation. Synthetic execution fixtures test program behavior without claiming to reproduce historical scores.

The GitHub Actions workflow repeats the Python checks on pushes and pull requests. COMSOL execution and LaTeX compilation require separate installations and are not part of Python CI.
