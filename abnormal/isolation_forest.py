import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib


def train_isolation_forest_model(
    feature_file="features.csv",
    user_model_output_path="user_isoforest_model.joblib",
    scaler_output_path="user_scaler.joblib",
    contamination=0.05,
):
    try:
        features_df = pd.read_csv(feature_file)
    except FileNotFoundError:
        print(f"Error: Feature file '{feature_file}' not found.")
        return
    except Exception as e:
        print(f"Error loading feature file '{feature_file}': {e}")
        return

    if features_df.empty:
        print("Feature DataFrame is empty. Cannot train model.")
        return

    if "user" not in features_df.columns:
        raise ValueError("The 'user' column is missing in the DataFrame.")

    user_names = features_df["user"].unique()
    if len(user_names) > 1:
        raise ValueError(
            f"Multiple users found: {user_names}. Please filter to one user."
        )
    elif len(user_names) == 0:
        raise ValueError("No user found in dataset.")

    user_name = user_names[0]
    print(f"Training Isolation Forest model for user: {user_name}")

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
    if not training_features:
        raise ValueError("No suitable numerical features found for training.")

    X_train = numeric_features_df[training_features].copy()
    X_train.dropna(inplace=True)

    if X_train.empty:
        raise ValueError("No data available for training after cleaning.")

    print(f"Features used: {training_features}")
    print(f"Training samples: {len(X_train)}")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = IsolationForest(
        n_estimators=100, contamination=contamination, random_state=42
    )
    model.fit(X_train_scaled)

    joblib.dump(model, user_model_output_path)
    joblib.dump(scaler, scaler_output_path)
    print(f"Model saved to: {user_model_output_path}")
    print(f"Scaler saved to: {scaler_output_path}")


username = "atiq"
train_isolation_forest_model(
    feature_file="processed/train.csv",
    user_model_output_path=f"{username}_isoforest_model.joblib",
    scaler_output_path=f"{username}_scaler.joblib",
)
