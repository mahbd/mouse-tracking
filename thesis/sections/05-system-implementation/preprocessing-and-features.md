## Preprocessing and Features

The Python pipeline reads raw CSVs, segments windows, and computes features. It ensures numeric coercion, handles missing values via row drops, and persists per-user feature files. Consistency between training and inference is enforced via shared TRAINING_FEATURES definitions and saved scalers.
