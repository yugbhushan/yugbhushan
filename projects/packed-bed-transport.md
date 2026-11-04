# Momentum Transport in Packed Beds

**Transport phenomena / Pressure-drop modelling / Python**  
April 2026

[Profile](../README.md) · [All projects](README.md)

## Engineering question

How do particle shape and wall channeling affect pressure drop and flow distribution in a packed bed?

## Modelling approach

| Component | Approach |
| :--- | :--- |
| Governing model | Ergun equation, derived from a shell momentum balance |
| Particle shape | Sphericity-based extension for non-spherical particles |
| Implementation | Python pressure-drop model |
| Wall effects | Benenati–Brosilow correlation |

## My contribution

1. Derived the pressure-drop relation from a shell momentum balance.
2. Extended the model to account for particle sphericity.
3. Compared crushed catalyst particles with spherical beads.
4. Modelled wall channeling and proposed packed-bed design guidelines.

## Reported comparison

Crushed catalyst at a sphericity of **0.65** produced approximately **190% higher pressure drop per unit length** than spherical beads under the studied conditions.

This percentage describes the specific model comparison; it is not a general result for every bed geometry or flow regime.

## Engineering relevance

The analysis brings particle geometry and near-wall flow into the assessment of packed-bed resistance and design.

## Reproducibility

This repository currently contains the project summary. The original Python model, derivation, bed and fluid properties, operating conditions, correlation implementation, and plots are needed to reproduce the comparison.

*Project scope and results are drawn from my CV; the analysis has not been independently rerun in this repository.*
