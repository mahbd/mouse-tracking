# Tables and Figures

## Classification Summary Table

| Algorithm     | Accuracy |
| ------------- | -------- |
| Random Forest | 85.36%   |
| Decision Tree | 77.24%   |
| PCA + XGBoost | 70.20%   |
| KNN           | 60.30%   |
| MLP           | 44.43%   |
| Naive Bayes   | 38.37%   |

## Random Forest Per-User Metrics

| User  | Precision | Recall | F1-Score |
| ----- | --------- | ------ | -------- |
| atiq  | 0.89      | 0.86   | 0.87     |
| masum | 0.98      | 0.98   | 0.98     |
| rakib | 0.79      | 0.82   | 0.81     |
| zia   | 0.81      | 0.80   | 0.80     |

## Anomaly Detection Cross-User Summary

Isolation Forest generally shows higher anomaly rates than One-Class SVM. The numeric cross-user matrices follow.

#### One-Class SVM cross-user matrix

<!-- include: svm_cross_user_matrix.md -->

#### Isolation Forest cross-user matrix

<!-- include: iso_cross_user_matrix.md -->

### Figures

- `thesis/figures/svm_cross_user_heatmap.png` — One-Class SVM cross-user anomaly heatmap.
- `thesis/figures/iso_cross_user_heatmap.png` — Isolation Forest cross-user anomaly heatmap.
- `thesis/figures/svm_self_vs_cross.png` — SVM self vs mean cross bar chart.
- `thesis/figures/iso_self_vs_cross.png` — ISO self vs mean cross bar chart.
- `thesis/figures/rf_confusion_matrix.png` — Random Forest confusion matrix (test set).
- `thesis/figures/rf_top12_feature_importances.png` — Top-12 RF feature importances.
- `thesis/figures/top6_feature_violin_by_user.png` — Distributions of top 6 features by user.

> Source: results/training_results.txt
