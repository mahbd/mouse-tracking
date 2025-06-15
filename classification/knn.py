import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Load data
features_df = pd.read_csv("features.csv")
if 'user' not in features_df.columns:
    print("Error: 'user' column not found in features_df. Cannot proceed with ML preparation.")

# Prepare features and labels
X = features_df.drop(columns=['user'])
X = X.select_dtypes(include=np.number)
y = features_df['user']

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train KNN model
model = KNeighborsClassifier(n_neighbors=5)  # You can tune n_neighbors
model.fit(X_train_scaled, y_train)

# Evaluate model
accuracy = model.score(X_test_scaled, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
