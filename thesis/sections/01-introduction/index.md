# Introduction

Behavioral biometrics leverage the unique ways individuals interact with computing systems. Mouse tracking—capturing sequences of cursor movements, clicks, and scroll events—offers a continuous, unobtrusive signal for identifying users and detecting anomalous behavior. Prior studies have explored mouse-based authentication and region usage patterns in human-computer interaction contexts \cite{rahman2021}. This thesis investigates mouse tracking as a behavioral biometric for two goals: multi-user classification (who is at the computer) and single-user anomaly detection (is the current behavior unusual for this user?).

## Motivation

- Security: Continuous authentication complements point-in-time logins.
- Usability: Passive and privacy-conscious when engineered from motion dynamics rather than content.
- Practicality: Mouse signals are ubiquitous across desktop environments and inexpensive to collect.

## Objectives

1. Design and implement a cross-platform data collection and feature extraction pipeline for mouse events.
2. Engineer robust behavioral features from fixed-length event segments.
3. Train and compare classification models for user identification.
4. Train One-Class SVM and Isolation Forest for single-user anomaly detection.
5. Evaluate cross-user anomaly rates to quantify behavioral distinctiveness.

## Contributions

- An end-to-end open codebase with C++ collectors (Windows, Linux), Python preprocessing, classic ML baselines, and a minimal GUI for real-time anomaly detection.
- A curated feature set centered on motion, speed/acceleration statistics, and event pattern ratios.
- A comprehensive experimental study on 76,693 behavioral segments across four users, achieving 85.36% best classification accuracy (Random Forest) and notable cross-user anomaly separation.

## Thesis Outline

- Background and Related Work: Behavioral biometrics, mouse dynamics, anomaly detection.
- Data and Feature Engineering: Raw signal, segmentation, features, scaling, exclusions.
- Methodology: Modeling tasks, algorithms, training protocols, validation.
- System Implementation: Collectors, preprocessing, models, GUI app, storage layout.
- Experiments and Results: Dataset, metrics, classifier performance, anomaly detection analyses.
- Discussion and Future Work: Limitations, threats to validity, ethical considerations, next steps.
- Conclusion: Findings, implications, and closing remarks.

Note: Results summarized here are derived from `results/results.md` and `results/training_results.txt` within this repository; reproducibility details are provided in the appendices.
