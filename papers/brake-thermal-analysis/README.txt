Disc Brake Thermal Term Paper - Complete LaTeX Project

Overleaf: upload this ZIP as a new project, choose main.tex,
and compile with pdfLaTeX. Recompile until contents numbers settle.

Files required for compilation:
  main.tex
  verification.pdf
  thermal_verification.py

The Python file is included as a listing and need not run during
LaTeX compilation. It is an independent illustrative 1-D finite
element verification problem, not the original COMSOL model.

To reproduce the reference calculation, install numpy, pandas,
and matplotlib, then run:
  python thermal_verification.py

The verification_results folder contains calculated CSV data for
this independent problem only. No original COMSOL .mph file or
material-comparison outputs are included. Original project claims
are attributed to the supplied project summary in the paper.
