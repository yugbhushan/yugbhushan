Rainfall Prediction Term Paper - LaTeX Source

Files:
  main.tex                 Complete paper source
  worked_example.pdf       Figure used in the paper
  rainfall_analysis.py     Code included in Appendix A

Overleaf:
  Upload this ZIP as a new project.
  Set the main document to main.tex and compiler to pdfLaTeX.
  Recompile as needed until contents-page numbers settle.

Local compilation (from this directory):
  pdflatex main.tex
  pdflatex main.tex
  pdflatex main.tex

Keep all three source files in the same folder.
The Python program is embedded as a listing; it need not be executed
in order to compile the paper. Running it separately requires NumPy,
pandas, Matplotlib, and a real input dataset as described in the paper.
