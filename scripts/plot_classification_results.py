import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, accuracy_score

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA_CSV = os.path.join(ROOT, 'data', 'features.csv')
FIG_DIR = os.path.join(ROOT, 'thesis', 'figures')

os.makedirs(FIG_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_CSV)

# Prepare X, y
X = df.drop(columns=['user'])
X = X.select_dtypes(include=np.number)
# Remove columns that are counts / irrelevant (keep core features if present)
# If those core features are present, prioritize them
core_features = [
    'segment_duration_ms', 'total_distance_pixels', 'mean_speed', 'std_dev_speed',
    'median_speed', 'skewness_speed', 'kurtosis_speed', 'max_speed', 'min_speed',
    'mean_acceleration', 'std_dev_acceleration', 'max_acceleration', 'path_straightness',
    'ratio_DM', 'ratio_VM', 'ratio_HM'
]
available_core = [c for c in core_features if c in X.columns]
if available_core:
    X = X[available_core]

le = LabelEncoder()
y = le.fit_transform(df['user'])

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Train RF
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train_s, y_train)

# Evaluate
y_pred = rf.predict(X_test_s)
acc = accuracy_score(y_test, y_pred)
print('RF test accuracy:', acc)
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
fig, ax = plt.subplots(figsize=(6,5))
disp.plot(ax=ax, cmap='Blues')
# rotate tick labels safely
for lbl in ax.get_xticklabels():
    lbl.set_rotation(45)
plt.title('Random Forest confusion matrix')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'rf_confusion_matrix.png'))
plt.close()

# Feature importances
importances = rf.feature_importances_
feat_imp = pd.Series(importances, index=X.columns).sort_values(ascending=False)
feat_imp.head(12).to_csv(os.path.join(FIG_DIR, 'rf_feature_importances.csv'))

plt.figure(figsize=(8,4))
sns.barplot(x=feat_imp.head(12).values, y=feat_imp.head(12).index, palette='viridis')
plt.title('Top 12 Random Forest feature importances')
plt.xlabel('Importance')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'rf_top12_feature_importances.png'))
plt.close()

# Violin plots for top 6 features
top6 = list(feat_imp.head(6).index)
plot_df = df[[*top6, 'user']].melt(id_vars='user', var_name='feature', value_name='value')
plt.figure(figsize=(12,6))
# Use dodge (no split) because split=True requires exactly two levels of hue
sns.violinplot(x='feature', y='value', hue='user', data=plot_df, dodge=True, inner='quartile', palette='Set2')
plt.title('Distribution of top 6 features by user')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'top6_feature_violin_by_user.png'))
plt.close()

print('Classification plots saved to', FIG_DIR)
