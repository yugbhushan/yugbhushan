Gas Sensor Monitoring Term Paper - LaTeX Project

Upload the ZIP to Overleaf as a new project.
Main document: main.tex
Compiler: pdfLaTeX

Keep main.tex, pca_example.pdf and gas_sensor_analysis.py together.
Compile locally with pdflatex main.tex three times for stable contents.
The Python file is included as a code listing; it does not run during
LaTeX compilation. Original project data are not included.

For analysis, install numpy pandas matplotlib scikit-learn.
CSV input: batch,class,x1,...,x128 (preserve original sensor order).
Temporal evaluation:
python gas_sensor_analysis.py sensor_data.csv --out temporal_results
Random diagnostic:
python gas_sensor_analysis.py sensor_data.csv --protocol random --out random_results
Optional sensor-group importance: append --importance.

The reported project metrics are attributed to the supplied summary;
worked examples are illustrative. The documented reconstruction settings
are not asserted to be the original experiment settings.
