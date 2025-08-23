import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib


def predict_anomalies(
    test_file="test.csv",
    model_path="user_isoforest_model.joblib",
    scaler_path="user_scaler.joblib",
):
    try:
        features_df = pd.read_csv(test_file)
    except Exception as e:
        print(f"Error loading test file: {e}")
        return

    excluded_cols = [
        "num_events",
        "user",
        "std_dev_daytime_bin",
        "num_unique_window_titles",
        "most_common_window_title_hash",
        "most_common_daytime_bin",
        "count_LD",
        "ratio_LD",
        "count_LU",
        "ratio_LU",
        "count_RD",
        "ratio_RD",
        "count_RU",
        "ratio_RU",
        "count_MW",
        "ratio_MW",
        "num_clicks",
        "count_DM",
        "count_VM",
        "count_HM",
    ]

    numeric_features_df = features_df.select_dtypes(include=np.number)
    training_features = [
        col for col in numeric_features_df.columns if col not in excluded_cols
    ]

    X_test = numeric_features_df[training_features].copy()
    X_test.dropna(inplace=True)

    scaler = joblib.load(scaler_path)
    model = joblib.load(model_path)

    X_test_scaled = scaler.transform(X_test)
    predictions = model.predict(X_test_scaled)  # -1 = anomaly, 1 = normal

    # count anomalies
    num_anomalies = np.sum(predictions == -1)
    num_normal = np.sum(predictions == 1)
    print(
        f"Value: {num_anomalies} anomalies detected, {num_normal} normal data points."
    )
    print(f"Accuracy: {num_normal / (num_anomalies + num_normal) * 100:.2f}%")


predict_anomalies(
    test_file="../processed/rakib.csv",
    model_path=f"../models/isolation_forest/atiq_isoforest_model.joblib",
    scaler_path=f"../models/scalers/atiq_isoforest_scaler.joblib",
)
