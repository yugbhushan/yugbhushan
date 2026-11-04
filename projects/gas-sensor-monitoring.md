# Gas-Sensor Process Monitoring

**Machine learning / Chemical process monitoring**  
July–October 2025

[Profile](../README.md) · [All projects](README.md)

## Research question

How can multivariate gas-sensor readings be used to distinguish gas classes while accounting for changes in sensor response over time?

## Project scope

| Component | Scope |
| :--- | :--- |
| Observations | More than 13,900 multivariate readings |
| Sensor array | 16 sensors |
| Classification task | Six gas classes |
| Dimensionality reduction | Principal component analysis (PCA) |
| Classifier | Random Forest |

## My contribution

1. Processed the multivariate sensor readings for classification.
2. Applied PCA to reduce the dimensionality of the sensor data.
3. Trained a Random Forest classifier in the context of sensor drift.
4. Evaluated classification performance on held-out test data and identified key sensor features.

## Reported results

| Test metric | Value |
| :--- | ---: |
| Accuracy | 97.8% |
| F1-score | 97.6% |
| ROC-AUC | 0.99 |

## Engineering relevance

The project connects chemical process monitoring with statistical feature extraction and machine learning. Its central theme is using high-dimensional sensor signals to support class identification.

## Reproducibility

This repository currently contains the project summary. Original code, data provenance, preprocessing, train/test split, metric averaging conventions, and drift-specific evaluation are needed to independently reproduce the reported results. A held-out score alone does not establish performance on future sensor drift.

*Project scope and results are drawn from my CV; the analysis has not been independently rerun in this repository.*
