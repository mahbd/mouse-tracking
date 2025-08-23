# Experiments and Results

This section consolidates findings from `results/results.md` and `results/training_results.txt`.

## Dataset Summary

- 76,693 segments across 4 users: atiq, masum, rakib, zia.
- 36 engineered features; 16 core features used for modeling.
- Segmentation: 50 events per segment.

## Classification Performance

- Random Forest (best): 85.36% accuracy overall.
- Decision Tree: 77.24%
- PCA + XGBoost: 70.20%
- KNN: 60.30%
- MLP: 44.43%
- Naive Bayes: 38.37%

Per-user (Random Forest): masum highest precision/recall (≈98%); rakib/zia show more confusion.

## Anomaly Detection

- Self-tests: ~5% anomalies for both One-Class SVM and Isolation Forest on their training users (nu/contamination=0.05).

Cross-user anomaly rates (selected):

- Masum’s models: up to 31.6% anomalies on other users (most distinctive).
- Atiq’s models: ~1–5% anomalies on others (least distinctive).
- Rakib/Zia: intermediate distinctiveness.

Isolation Forest generally yields higher cross-user anomaly rates than One-Class SVM, indicating greater sensitivity.

## Key Findings

- Mouse dynamics enable feasible user identification (85.36% accuracy).
- Behavioral distinctiveness varies by user; useful for continuous authentication.
- Ensemble methods outperform simple baselines; deep models need more data/tuning.

## Reproducibility

- See `appendices/B-reproducibility.md` for environment and script details.

## Additional Analyses (Placeholders)

### Feature Distributions

Figure: Histogram/violin plots for key features (e.g., mean_speed, path_straightness) per user to visualize separability.

### Confusion Matrix (Random Forest)

Figure: 4x4 confusion matrix highlighting misclassifications between rakib and zia.

### Cross-User Anomaly ROC-style View

Figure: For each user’s model, plot anomaly rate vs. threshold to illustrate sensitivity (proxy ROC since labels are cross-user).

### Ablation Study (Planned)

Table: Impact of removing feature groups (speed stats, ratios, acceleration) on RF accuracy and ISO cross-user anomaly rates.
