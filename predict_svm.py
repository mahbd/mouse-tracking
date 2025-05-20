import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from collections import Counter
from sklearn.preprocessing import StandardScaler
import joblib

username = "atiq"
model_file = f"{username}_anomaly_model.joblib"
scaler_file = f"{username}_scaler.joblib"
feature_file = f"zia_features.csv"
loaded_model = joblib.load(model_file)
loaded_scaler = joblib.load(scaler_file)



try:
    features_df = pd.read_csv(feature_file)
except FileNotFoundError:
    raise FileNotFoundError(f"Error: Feature file '{feature_file}' not found. Please run the preprocessing script first.")
except Exception as e:
    raise Exception(f"Error loading feature file '{feature_file}': {e}")

if features_df.empty:
    raise ValueError("Feature DataFrame is empty. Cannot train model.")

if 'user' not in features_df.columns:
    raise ValueError("The 'user' column is missing in the features DataFrame. Please ensure it is included in the preprocessing step.")
else:
    user_names = features_df['user'].unique()
    if len(user_names) > 1:
        raise ValueError(f"Multiple users found in the dataset: {user_names}. Please filter the dataset to a single user before training.")
    elif len(user_names) == 0:
        raise ValueError("No user found in the dataset. Please check your features.csv file.")

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


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
    # 3. When new mouse data for "atiq" comes in:
    #    a. Process it using your `segment_data` and `calculate_segment_features` to get `new_features_df`.
    #    b. Select the *same* training features (order matters): `new_X = new_features_df[training_features_list_from_training]`
    #    c. Scale it: `new_X_scaled = loaded_scaler.transform(new_X)`
prediction = loaded_model.predict(X_train_scaled)
    #       (prediction will be +1 for normal/inlier, -1 for suspicious/outlier)
counts = Counter(prediction)
num_normal = counts[1]
num_suspicious = counts[-1]

print(f"Number of Normal segments (1): {num_normal}")
print(f"Number of Suspicious segments (-1): {num_suspicious}")