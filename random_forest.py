# python
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.model_selection import train_test_split


features_df = pd.read_csv("features.csv")

X = features_df.drop(columns=['user'])
X = X.select_dtypes(include=np.number)
y = features_df['user']


label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# Build a pipeline combining scaling and the classifier 
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier(random_state=42))
])

# Define a hyperparameter search space
param_dist = {
    'rf__n_estimators': [100, 200, 500],
    'rf__max_depth': [None, 10, 20, 30],
    'rf__min_samples_split': [2, 5, 10],
    'rf__min_samples_leaf': [1, 2, 4],
    'rf__bootstrap': [True, False]
}

# Stratified k-fold for more reliable CV
cv = StratifiedKFold(n_splits=5, shuffle=False)

# Randomized search over the grid
search = RandomizedSearchCV(
    pipeline,
    param_distributions=param_dist,
    n_iter=10,
    cv=cv,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)

# Fit on training data
search.fit(X_train, y_train)

# Evaluate on test set
y_pred = search.best_estimator_.predict(X_test)
print("Test Accuracy:", accuracy_score(y_test, y_pred) * 100)
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))