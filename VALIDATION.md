# Validation record

Local checks completed on 5 November 2026 using Python 3.12.14 and the versions pinned in `requirements.txt`.

| Check | Outcome |
| --- | --- |
| `python -m unittest discover -s tests -v` | 10 tests passed |
| `python run_all.py` | All four existing examples completed; tracked outputs remained unchanged |
| `python -m compileall -q code papers tests` | Passed |
| Paper thermal verification program | Six mesh/time-step runs completed; finest surface peak 378.007203 K, relative energy residual approximately 4.62e-14 |
| Three supplied `main.tex` files | Each compiled successfully with two pdfLaTeX passes in a temporary output directory |
| Local Markdown links | No missing file targets |
| Supplied source archives | Extracted files preserved byte-for-byte |
| `git diff --check` | Passed |

The tests exercise energy balance, no-heating equilibrium, particle-shape limits, area-weighted flow, UCI feature parsing, calendar gaps, chronological partitions, metric calculations, invalid/duplicate sensor rows and undefined AUC.

This record validates implementation behavior and document buildability. It does not reproduce the original rainfall/gas metrics, validate the original COMSOL model, or establish the packed-bed report's 190% pressure-drop comparison. COMSOL compilation and execution were not performed. The GitHub Actions workflow repeats Python checks; its status is visible on GitHub after publication.
