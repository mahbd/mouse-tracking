import os
import pandas as pd
import joblib
import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA_CSV = os.path.join(ROOT, 'data', 'features.csv')
MODELS_DIR = os.path.join(ROOT, 'models')
OUT_DIR = os.path.join(ROOT, 'thesis', 'sections', '06-experiments-and-results')
FIG_DIR = os.path.join(ROOT, 'thesis', 'figures')

os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(DATA_CSV)
users = df['user'].unique()
training_features = [
    'segment_duration_ms', 'total_distance_pixels', 'mean_speed', 'std_dev_speed',
    'median_speed', 'skewness_speed', 'kurtosis_speed', 'max_speed', 'min_speed',
    'mean_acceleration', 'std_dev_acceleration', 'max_acceleration', 'path_straightness',
    'ratio_DM', 'ratio_VM', 'ratio_HM'
]

svm_rates = pd.DataFrame(index=users, columns=users, dtype=float)
iso_rates = pd.DataFrame(index=users, columns=users, dtype=float)

for model_user in users:
    try:
        svm_model = joblib.load(os.path.join(MODELS_DIR, 'svm', f'{model_user}_svm_model.joblib'))
        svm_scaler = joblib.load(os.path.join(MODELS_DIR, 'scalers', f'{model_user}_svm_scaler.joblib'))
        iso_model = joblib.load(os.path.join(MODELS_DIR, 'isolation_forest', f'{model_user}_iso_model.joblib'))
        iso_scaler = joblib.load(os.path.join(MODELS_DIR, 'scalers', f'{model_user}_iso_scaler.joblib'))
    except FileNotFoundError:
        continue
    for test_user in users:
        test_df = df[df['user']==test_user]
        X_test = test_df[training_features].dropna()
        if X_test.empty:
            continue
        Xs_svm = svm_scaler.transform(X_test)
        Xs_iso = iso_scaler.transform(X_test)
        svm_pred = svm_model.predict(Xs_svm)
        iso_pred = iso_model.predict(Xs_iso)
        svm_rate = np.sum(svm_pred==-1)/len(X_test)*100
        iso_rate = np.sum(iso_pred==-1)/len(X_test)*100
        svm_rates.loc[model_user, test_user] = round(svm_rate,2)
        iso_rates.loc[model_user, test_user] = round(iso_rate,2)

# save CSVs
svm_rates.to_csv(os.path.join(OUT_DIR, 'svm_cross_user_matrix.csv'))
iso_rates.to_csv(os.path.join(OUT_DIR, 'iso_cross_user_matrix.csv'))

# also dump markdown tables
with open(os.path.join(OUT_DIR, 'svm_cross_user_matrix.md'), 'w') as f:
    f.write(svm_rates.to_markdown())
with open(os.path.join(OUT_DIR, 'iso_cross_user_matrix.md'), 'w') as f:
    f.write(iso_rates.to_markdown())

print('Exported anomaly matrices to', OUT_DIR)
