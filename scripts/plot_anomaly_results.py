import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
DATA_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'features.csv')
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
FIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'thesis', 'figures')

os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(DATA_CSV)
users = df['user'].unique()

training_features = [
    'segment_duration_ms', 'total_distance_pixels', 'mean_speed', 'std_dev_speed',
    'median_speed', 'skewness_speed', 'kurtosis_speed', 'max_speed', 'min_speed',
    'mean_acceleration', 'std_dev_acceleration', 'max_acceleration', 'path_straightness',
    'ratio_DM', 'ratio_VM', 'ratio_HM'
]

# Prepare matrices
svm_rates = pd.DataFrame(index=users, columns=users, dtype=float)
iso_rates = pd.DataFrame(index=users, columns=users, dtype=float)

for model_user in users:
    # load models
    try:
        svm_model = joblib.load(os.path.join(MODELS_DIR, 'svm', f'{model_user}_svm_model.joblib'))
        svm_scaler = joblib.load(os.path.join(MODELS_DIR, 'scalers', f'{model_user}_svm_scaler.joblib'))
        iso_model = joblib.load(os.path.join(MODELS_DIR, 'isolation_forest', f'{model_user}_iso_model.joblib'))
        iso_scaler = joblib.load(os.path.join(MODELS_DIR, 'scalers', f'{model_user}_iso_scaler.joblib'))
    except FileNotFoundError:
        print(f"Models for {model_user} not found, skipping")
        continue

    for test_user in users:
        test_df = df[df['user'] == test_user].copy()
        X_test = test_df[training_features].dropna()
        if X_test.empty:
            continue
        X_test_svm = svm_scaler.transform(X_test)
        X_test_iso = iso_scaler.transform(X_test)

        svm_pred = svm_model.predict(X_test_svm)
        iso_pred = iso_model.predict(X_test_iso)

        svm_rate = np.sum(svm_pred == -1) / len(X_test) * 100
        iso_rate = np.sum(iso_pred == -1) / len(X_test) * 100

        svm_rates.loc[model_user, test_user] = svm_rate
        iso_rates.loc[model_user, test_user] = iso_rate

# Plot heatmaps
plt.figure(figsize=(8,6))
sns.heatmap(svm_rates.astype(float), annot=True, fmt='.1f', cmap='viridis')
plt.title('One-Class SVM anomaly rates (%) — model user (rows) vs test user (cols)')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'svm_cross_user_heatmap.png'))
plt.close()

plt.figure(figsize=(8,6))
sns.heatmap(iso_rates.astype(float), annot=True, fmt='.1f', cmap='magma')
plt.title('Isolation Forest anomaly rates (%) — model user (rows) vs test user (cols)')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'iso_cross_user_heatmap.png'))
plt.close()

# Bar plots of self vs mean cross
svm_self = np.diag(svm_rates.astype(float))
iso_self = np.diag(iso_rates.astype(float))
svm_cross_mean = svm_rates.astype(float).mean(axis=1)
iso_cross_mean = iso_rates.astype(float).mean(axis=1)

x = np.arange(len(users))
plt.figure(figsize=(8,4))
plt.bar(x-0.2, svm_self, width=0.4, label='SVM self')
plt.bar(x+0.2, svm_cross_mean, width=0.4, label='SVM mean cross')
plt.xticks(x, users)
plt.ylabel('Anomaly rate (%)')
plt.title('SVM: self vs mean cross anomaly rates')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'svm_self_vs_cross.png'))
plt.close()

plt.figure(figsize=(8,4))
plt.bar(x-0.2, iso_self, width=0.4, label='ISO self')
plt.bar(x+0.2, iso_cross_mean, width=0.4, label='ISO mean cross')
plt.xticks(x, users)
plt.ylabel('Anomaly rate (%)')
plt.title('ISO: self vs mean cross anomaly rates')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'iso_self_vs_cross.png'))
plt.close()

print('Plots saved to', FIG_DIR)
