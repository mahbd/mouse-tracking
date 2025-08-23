## Algorithms and Hyperparameters

- Random Forest: n_estimators, max_depth, max_features tuned by CV.
- Decision Tree: depth/pruning parameters to manage overfitting.
- KNN: k and distance metric; sensitive to scaling.
- Naive Bayes: Gaussian assumption on standardized features.
- PCA+XGBoost: reduce to ~50% variance dimensions; gradient-boosted trees thereafter.
- MLP: modest hidden layers; requires larger datasets for optimal results.
- One-Class SVM: RBF kernel, nu=0.05, gamma=scale.
- Isolation Forest: n_estimators=100, contamination=0.05, random_state=42.
