# Methodology

## Problem Formulations

- Multi-user classification: Predict `user` label from behavioral segment features.
- Single-user anomaly detection: Learn "normal" behavior for a user and flag deviations.

## Algorithms

- Classification: Random Forest, Decision Tree, KNN, Naive Bayes, PCA+XGBoost, MLP.
- Anomaly Detection: One-Class SVM (RBF, nu=0.05), Isolation Forest (n_estimators=100, contamination=0.05, random_state=42).

## Training Protocols

- Classification: 5-fold stratified cross-validation; report mean accuracy and per-user precision/recall/F1 on held-out folds.
- Anomaly: Train on each user’s feature file; validate expected anomaly fraction on training set; perform cross-user tests using other users’ data.

## Feature Selection

- Use 16 core behavioral features; exclude counts and direct identity cues.
- Scale numerical features with StandardScaler; persist scaler alongside model.

## Evaluation Metrics

- Classification: Accuracy, precision, recall, F1-score.
- Anomaly: Anomaly rate (% flagged) on self and cross-user data.

## Validation and Significance

- Consistent preprocessing across models.
- Repeatability ensured by fixed random seeds where applicable.

## Implementation Details

- Hyperparameter search: GridSearchCV for RF (trees, depth, features). Fixed params for SVM/ISO for comparability.
- Data splitting: Stratified folds preserve per-user class balance.
- Scaling: Fit scaler on training folds only; apply to validation folds to avoid leakage.

## Threats to Validity and Mitigation

- Small sample of users: address through cross-user tests and transparent reporting.
- Potential device variance: note collector environment; future work includes device-normalized features.
- Temporal drift: limited in current dataset; propose longitudinal validation.
