# Disc-brake heating: paper and verification code

[Project overview](../../projects/brake-thermal-analysis.md) · [Read the paper](report.pdf) · [LaTeX](main.tex)

The supplied Python program solves an **illustrative one-dimensional half-slab finite-element problem**. It uses a consistent mass matrix, backward Euler integration, convection, nonlinear radiation and Newton iteration. The braking input is obtained from explicitly assumed vehicle and rotor parameters.

## Run

After installing the root requirements:

```sh
cd papers/brake-thermal-analysis
python thermal_verification.py
```

The script writes `verification_outputs/` in the current directory: temperature/energy history, mesh/time refinement summary and a figure. Assumptions are in the `PARAMS` dictionary. The supplied `verification_results/` and `verification.pdf` are illustrative report outputs, not results from the original COMSOL project.

The finest report calculation has a surface peak of approximately 378.01 K. Its purpose is checking a numerical method and energy balance. It does not establish a three-dimensional rotor temperature or compare the original material cases.

The original COMSOL MPH file, geometry, material curves and numerical results were not supplied. The separate [existing Java builder](../../native/comsol) constructs an illustrative study and has not been compiled or solved in COMSOL here. Carbon-ceramic composite properties require their own specification.

Compile `main.tex` twice with pdfLaTeX from this directory; the supplied report uses the included `verification.pdf` figure.
