# Momentum transport in packed beds

**Authors:** Parikshit, Shrish Kumar and Yug Bhushan.  
**Report date:** 27 April 2026.

[Read the original report](report.pdf) · [Project overview](../../projects/packed-bed-transport.md) · [Extended Python model](../../code/packed_bed.py)

## Available source

`appendix.py` transcribes the partial Python listing in Appendix A (printed page 25). Formatting and line wraps have been normalized. It defines the Ergun calculation, evaluates three voidages and computes the printed radial porosity expression. The report explicitly omits the plotting commands, so the transcription does not create plots.

```sh
python papers/packed-bed-transport/appendix.py
python code/packed_bed.py --out runs/packed-bed
```

The second command runs the existing, separately constructed portfolio model with plots and CSV outputs. Its assumptions differ from those of the appendix.

## Interpretation

- The original LaTeX, complete plotting script and experimental observations were not supplied.
- The paper's approximately 190% pressure-drop increase cannot be reproduced solely by changing sphericity from 1 to 0.65 with other Ergun inputs fixed. See the [derivation and comparison](../../projects/packed-bed-transport.md).
- The printed damped cosine expression produces negative porosity for some distances with its listed constants. It is retained for source transparency and is not used as a physical porosity input in the extended flow solver.
- The empirical Ergun constants are not derived from first principles by the shell balance.

Retain all three authors when citing or sharing the report.
