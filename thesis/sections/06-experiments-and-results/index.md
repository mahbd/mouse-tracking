\newpage
\thispagestyle{plain}

\begin{center}
\vspace*{2cm}
\textbf{\Large CHAPTER 6}\\[0.5cm]
\textbf{\Large EXPERIMENTS AND RESULTS}
\end{center}

\newpage

This section consolidates findings from `results/results.md` and `results/training_results.txt`.

## 6.1 Dataset Summary

- 76,693 segments across 4 users: atiq, masum, rakib, zia.
- 36 engineered features; 16 core features used for modeling.
- Segmentation: 50 events per segment.

### Dataset table

| User  | Segments | Notes |
|------:|---------:|-------|
| atiq  | 20585    | multiple sessions, varied tasks |
| masum | 13447    | shorter sessions, distinctive patterns |
| rakib | 21269    | longer sessions, mixed tasks |
| zia   | 21392    | consistent sampling across sessions |


## 6.2 Classification Performance

- Random Forest (best): 85.36% accuracy overall.
- Decision Tree: 77.24%
- PCA + XGBoost: 70.20%
- KNN: 60.30%
- MLP: 44.43%
- Naive Bayes: 38.37%

Per-user (Random Forest): masum highest precision/recall (≈98%); rakib/zia show more confusion.

### Classification summary table

| Algorithm     | Accuracy |
|--------------:|---------:|
| Random Forest | 85.36%   |
| Decision Tree | 77.24%   |
| PCA + XGBoost | 70.20%   |
| KNN           | 60.30%   |
| MLP           | 44.43%   |
| Naive Bayes   | 38.37%   |

### Random Forest per-user table

| User  | Precision | Recall | F1-Score |
|:-----:|----------:|-------:|---------:|
| atiq  | 0.89      | 0.86   | 0.87     |
| masum | 0.98      | 0.98   | 0.98     |
| rakib | 0.79      | 0.82   | 0.81     |
| zia   | 0.81      | 0.80   | 0.80     |

## 6.3 Anomaly Detection

- Self-tests: ~5% anomalies for both One-Class SVM and Isolation Forest on their training users (nu/contamination=0.05).

Cross-user anomaly rates (selected):

- Masum’s models: up to 31.6% anomalies on other users (most distinctive).
- Atiq’s models: ~1–5% anomalies on others (least distinctive).
- Rakib/Zia: intermediate distinctiveness.

### Figures: Cross-user anomaly rates

![One-Class SVM cross-user anomaly heatmap](figures/svm_cross_user_heatmap.png){width=90%}

Caption: One-Class SVM anomaly rates (%) where rows = model user and columns = test user. Diagonal entries are self-test rates (~5%).

![Isolation Forest cross-user anomaly heatmap](figures/iso_cross_user_heatmap.png){width=90%}

Caption: Isolation Forest anomaly rates (%) where rows = model user and columns = test user. Isolation Forest shows higher cross-user sensitivity for some models.

Isolation Forest generally yields higher cross-user anomaly rates than One-Class SVM, indicating greater sensitivity.

### Cross-user matrices (numeric)

#### One-Class SVM cross-user matrix

<!-- include: tables-and-figures.md -->

<!-- include: svm_cross_user_matrix.md -->

#### Isolation Forest cross-user matrix

<!-- include: iso_cross_user_matrix.md -->

### Additional Figures

![Random Forest confusion matrix (test set)](figures/rf_confusion_matrix.png){width=80%}

Caption: Confusion matrix for Random Forest on held-out test data. The matrix shows most confusion between rakib and zia.

![Top 12 Random Forest feature importances](figures/rf_top12_feature_importances.png){width=80%}

Caption: Feature importances (gini importance) from Random Forest. Mean speed and path straightness are among the most important features.

![Top 6 features distribution by user](figures/top6_feature_violin_by_user.png){width=90%}

Caption: Violin plots of the top 6 features split by user to show distributional separability.

## 6.4 Key Findings

- Mouse dynamics enable feasible user identification (85.36% accuracy).
- Behavioral distinctiveness varies by user; useful for continuous authentication.
- Ensemble methods outperform simple baselines; deep models need more data/tuning.

## 6.5 Reproducibility

- See `appendices/B-reproducibility.md` for environment and script details.

## 6.6 Additional Analyses (Placeholders)

### Feature Distributions

Figure: Histogram/violin plots for key features (e.g., mean_speed, path_straightness) per user to visualize separability.

### Confusion Matrix (Random Forest)

Figure: 4x4 confusion matrix highlighting misclassifications between rakib and zia.

### Cross-User Anomaly ROC-style View

Figure: For each user’s model, plot anomaly rate vs. threshold to illustrate sensitivity (proxy ROC since labels are cross-user).

### Ablation Study (Planned)

Table: Impact of removing feature groups (speed stats, ratios, acceleration) on RF accuracy and ISO cross-user anomaly rates.
