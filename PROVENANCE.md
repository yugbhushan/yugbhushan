# Evidence, authorship and reproducibility

Updated 5 November 2026. This inventory records what is actually available in this repository.

## Source materials

| Material | Available files | What they establish |
| --- | --- | --- |
| Yug Bhushan's supplied CV | [Public academic summary](CV.md) | Education, skills, achievements, project descriptions and self-reported metrics |
| Rainfall term paper and LaTeX archive | [Paper package](papers/rainfall-prediction) | Methodology and a runnable one-day-ahead reconstruction protocol |
| Gas-sensor term paper and LaTeX archive | [Paper package](papers/gas-sensor-monitoring) | PCA/forest methodology and a runnable temporal evaluation protocol |
| Brake term paper and LaTeX archive | [Paper package](papers/brake-thermal-analysis) | Heat-transfer formulation and a one-dimensional verification example |
| Original packed-bed term paper | [PDF and appendix](papers/packed-bed-transport) | Collaborative report; partial source listing transcribed into Python |
| Previously published portfolio examples | [Code](code), [notebooks](sources), [outputs](results) | Separate illustrative reconstructions, preserved with their assumptions |

The packed-bed report is authored by **Parikshit, Shrish Kumar and Yug Bhushan**. The three other reports name Yug Bhushan. Paper text, plots and code retain their source attribution. No repository-wide license has been applied to jointly authored material.

## Claims and limits

| Project | Historical claim | Available validation and missing evidence |
| --- | --- | --- |
| Rainfall | R = 0.95–0.99 for three cities | Reported in the CV. Original data, date ranges, fitted coefficients and test predictions are missing. Correlation is not an accuracy percentage. Synthetic demo scores are separate. |
| Gas sensing | 97.8% accuracy, 97.6% F1, 0.99 AUC | Reported in the CV. Original split, fitted model and probability predictions are missing. A random holdout score does not demonstrate temporal drift robustness. |
| Brake heating | Favorable thermal stability for the ceramic rotor | Original COMSOL MPH file, material property tables and results are missing. Python results are illustrative slab calculations; the existing Java builder is unvalidated in COMSOL. Carbon-ceramic composites and monolithic SiC must not be treated as interchangeable. |
| Packed bed | Approximately 190% higher pressure drop at sphericity 0.65 | The paper reports this comparison, but the partial appendix does not reproduce it. For fixed voidage, volume-equivalent diameter and fluid conditions, the implemented Ergun pressure ratio lies between 1/φ and 1/φ²: about 1.538–2.367 at φ=0.65, or 53.8–136.7% higher. Additional differing inputs or a corrected comparison are required to establish 190%. |

The Ergun coefficients 150 and 1.75 are empirical. A momentum balance motivates the structure of the model, but does not independently derive these empirical constants.

The packed-bed appendix's damped cosine porosity expression reaches 1 at the wall and becomes negative at some interior points for the printed constants. It is retained as a transcription, not used as a physical input to the runnable annular-flow solver. The latter uses its own explicitly illustrative positive voidage profile.

## Code origin

- `code/` and `sources/`: existing portfolio reconstructions, with seeded synthetic gas/rainfall examples and illustrative physical models.
- `papers/*/*.py` for rainfall, gas and brake: unmodified files recovered from the supplied LaTeX archives. These are AI-assisted reconstruction/verification materials, not authenticated original project code.
- `papers/packed-bed-transport/appendix.py`: transcription of Appendix A, with whitespace normalized and line wraps repaired. The paper omits plotting code.
- `native/comsol/`: existing illustrative Java model builder, requiring a licensed COMSOL installation and separate validation. No original MPH file is included.
- `tests/`: physical consistency checks, input-format checks and execution checks. Synthetic fixtures validate code behavior; they do not validate historical project performance.

## Completing original-result reproduction

Add the original datasets with provenance and redistribution permission, train/test definitions, original scripts, model files and parameter tables. Record versions, run the relevant programs, and retain predictions and metrics. For COMSOL, supply the MPH file, material model, boundary selections and mesh/time convergence evidence. For the collaborative report, preserve authorship when adding source files.
