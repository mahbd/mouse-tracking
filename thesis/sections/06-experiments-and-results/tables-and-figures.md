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

Isolation Forest generally shows higher anomaly rates than One-Class SVM.

- Masum’s models: 11–31.6% anomalies on others.
- Rakib’s models: 2–21.2%.
- Zia’s models: 2–19%.
- Atiq’s models: 1–5.3%.

> Source: results/training_results.txt
