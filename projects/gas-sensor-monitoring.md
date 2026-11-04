# ML-Based Chemical Process Monitoring

**PCA · Random Forest · Multivariate sensor data**  
July–October 2025

[← Back to profile](../README.md)

## The engineering problem

Gas-sensor arrays produce multivariate signals whose response can drift over time. This project explored classification across six gas classes as a route toward chemical process monitoring.

## Work completed

- Processed more than 13,900 multivariate readings from a 16-sensor array.
- Applied principal component analysis for dimensionality reduction.
- Trained a Random Forest classifier to address classification in the presence of sensor drift.
- Identified key sensor features.

## Reported results

| Metric | Result |
| :--- | ---: |
| Accuracy | 97.8% |
| F1-score | 97.6% |
| ROC-AUC | 0.99 |

These are the held-out test results stated in my CV. The split strategy, averaging convention, preprocessing details, and drift-specific validation need to accompany the implementation for independent evaluation.

## Implementation status

This page is a project summary. Source code, dataset provenance, trained artefacts, and evaluation plots are not included in this profile package. In particular, the reported metrics should not be interpreted as a verified temporal generalisation result without the original validation protocol.
