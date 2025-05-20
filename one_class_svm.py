import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
import joblib # For saving and loading models

def train_anomaly_model_for_user(feature_file="features.csv", user_model_output_path="user_anomaly_model.joblib", scaler_output_path="user_scaler.joblib"):
    try:
        features_df = pd.read_csv(feature_file)
    except FileNotFoundError:
        print(f"Error: Feature file '{feature_file}' not found. Please run the preprocessing script first.")
        return
    except Exception as e:
        print(f"Error loading feature file '{feature_file}': {e}")
        return

    if features_df.empty:
        print("Feature DataFrame is empty. Cannot train model.")
        return

    if 'user' not in features_df.columns:
        raise ValueError("The 'user' column is missing in the features DataFrame. Please ensure it is included in the preprocessing step.")
    else:
        user_names = features_df['user'].unique()
        if len(user_names) > 1:
            raise ValueError(f"Multiple users found in the dataset: {user_names}. Please filter the dataset to a single user before training.")
        elif len(user_names) == 0:
            raise ValueError("No user found in the dataset. Please check your features.csv file.")
    user_name = user_names[0] # Not strictly needed if features_df is now filtered

    print(f"Training anomaly detection model for user: {user_name}")
    # excluded_cols = ['user', 'most_common_window_title_hash', 'most_common_daytime_bin']
    excluded_cols = [
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
    "count_HM"
]
    numeric_features_df = features_df.select_dtypes(include=np.number)
    training_features = [col for col in numeric_features_df.columns if col not in excluded_cols]

    if not training_features:
        raise ValueError("No suitable numerical features found for training after exclusions.")
        
    X_train = numeric_features_df[training_features].copy()

    X_train.dropna(inplace=True)

    if X_train.empty:
        raise ValueError("No data available for training after processing.")
    
    print(f"Using {len(training_features)} features for training: {training_features}")
    print(f"Number of training samples (segments): {len(X_train)}")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    print("Training One-Class SVM model...")
    model = OneClassSVM(nu=0.05, kernel="rbf", gamma='auto')
    model.fit(X_train_scaled)
    print("Model training complete.")

    try:
        joblib.dump(model, user_model_output_path)
        print(f"Trained anomaly model saved to '{user_model_output_path}'")
        joblib.dump(scaler, scaler_output_path)
        print(f"Scaler saved to '{scaler_output_path}'")
    except Exception as e:
        print(f"Error saving model or scaler: {e}")

if __name__ == "__main__":
    username = "atiq"
    model_file = f"{username}_anomaly_model.joblib"
    scaler_file = f"{username}_scaler.joblib"

    train_anomaly_model_for_user(feature_file=f"{username}_features_train.csv", 
                                 user_model_output_path=model_file, 
                                 scaler_output_path=scaler_file)
