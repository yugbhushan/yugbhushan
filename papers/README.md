# Term papers and accompanying source

[Profile](../README.md) · [Projects](../projects/README.md) · [Evidence inventory](../PROVENANCE.md)

| Project | Report | Editable source | Executable code |
| --- | --- | --- | --- |
| Rainfall prediction | [PDF](rainfall-prediction/report.pdf) | [LaTeX](rainfall-prediction/main.tex) | [Python](rainfall-prediction/rainfall_analysis.py) |
| Gas-sensor monitoring | [PDF](gas-sensor-monitoring/report.pdf) | [LaTeX](gas-sensor-monitoring/main.tex) | [Python](gas-sensor-monitoring/gas_sensor_analysis.py) |
| Disc-brake heat transfer | [PDF](brake-thermal-analysis/report.pdf) | [LaTeX](brake-thermal-analysis/main.tex) | [Python](brake-thermal-analysis/thermal_verification.py) |
| Packed-bed momentum transport | [PDF](packed-bed-transport/report.pdf) | Original LaTeX was not supplied | [Transcribed appendix](packed-bed-transport/appendix.py), [extended example](../code/packed_bed.py) |

The first three reports and their accompanying files were supplied as PDF/LaTeX packages. Their Python programs are **reconstruction or verification implementations**, as stated in the manuscripts, rather than the unavailable original research scripts. The packed-bed report is a collaborative paper by **Parikshit, Shrish Kumar and Yug Bhushan**; its printed appendix is partial and omits plotting code.

Each directory has its own README with commands, inputs and limitations. The original source packages are retained without changing their analysis code. Installation uses the root [requirements.txt](../requirements.txt).

## Compile the three LaTeX papers

From the corresponding paper directory, run `pdflatex main.tex` twice, or use `latexmk -pdf main.tex`. Keep the included Python file and PDF figure alongside `main.tex`. A TeX installation is required. The supplied rendered PDFs are included; compilation is separate from the Python tests.
