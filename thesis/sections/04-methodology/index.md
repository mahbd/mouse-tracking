
\newpage
	hispagestyle{plain}

\begin{center}
\vspace*{2cm}
	extbf{\Large CHAPTER 4}\\[0.5cm]
	extbf{\Large METHODOLOGY}
\end{center}

\newpage

## 4.1 Overview (condensed)

This chapter outlines a reproducible experimental framework for (a) multi‑user classification and (b) per‑user anomaly detection using the engineered features. Emphasis is on fair evaluation, statistical rigor, and practical deployment concerns [@brodley2003; @ahmed2004].

## 4.2 Problem Definitions (condensed)

- Classification: Given a segment X, predict user y among known users. Evaluation uses stratified cross‑validation and per‑class metrics.
- Anomaly detection: Train a per‑user model M_u (OC‑SVM / Isolation Forest / Autoencoder) on user data and flag out‑of‑baseline segments; evaluate self and cross‑user anomaly rates.

## 4.3 Algorithms and Evaluation (condensed)

Selected algorithms: Random Forest, SVM, KNN, MLP for classification; One‑Class SVM and Isolation Forest for anomaly detection [@brodley2003; @rahman2021]. Metrics: accuracy, precision, recall, F1, confusion matrices, ROC/AUC and anomaly rates. Validation: 5‑fold stratified cross‑validation with hyperparameter tuning inside folds to avoid leakage [@varma2006].

## 4.4 Feature and Model Analysis (condensed)

We use feature importance (Random Forest impurity and permutation), mutual information, correlation analysis, and ablation studies to identify compact, stable feature sets. Ablations quantify the contribution of temporal, spatial, kinematic and contextual features.

## 4.5 Reproducibility and Controls (condensed)

All preprocessing is deterministic and applied identically across algorithms; scalers and model artifacts are versioned and saved. Experiments use fixed random seeds, documented parameter grids, and statistical tests (paired tests, confidence intervals) for comparisons.

## 4.6 Threats to Validity and Ethics (condensed)

Key threats: small participant pool, temporal and environmental biases, and feature/model validity. Mitigations include transparent reporting, temporal analysis where possible, multi‑algorithm comparison, and strict privacy controls (anonymization, consent, limited retention).

## 4.7 Implementation Notes (condensed)

Experimental code is modular and tested; pipelines support batch and streaming modes. Resource settings (parallelism, memory) are documented to aid reproducibility.

\newpage
**Practical Relevance**: Experimental conditions and evaluation metrics are designed to reflect realistic deployment scenarios rather than artificial laboratory conditions.

**Reproducibility Standards**: Complete documentation and standardized procedures enable independent validation and extension of results.

**Ethical Integration**: Comprehensive integration of ethical considerations ensures responsible research practices and participant protection.

The following chapters present the results of applying this methodology to our mouse dynamics dataset, providing detailed analysis of both user identification and anomaly detection performance along with insights into the behavioral patterns that enable effective mouse-based authentication.

ewpage
