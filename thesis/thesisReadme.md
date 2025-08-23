# Mouse Tracking — Behavioral Biometrics and Anomaly Detection

This repository contains tools to collect mouse activity, transform it into engineered features, and train models for:

- User classification (identify which user generated the mouse behavior)
- Unsupervised anomaly detection for a single user (flag unusual behavior)
- A small Windows GUI app for real-time anomaly detection from a native mouse logger

The project spans C++ collectors (Windows and Linux), Python preprocessing/feature extraction, several classic ML baselines, and two anomaly detection approaches (One-Class SVM and Isolation Forest).

## Repository structure

- `collection/`
  - `collector.cpp` — Windows console collector that writes CSV batches to `C:\\mouse-data`.
  - `collector_linux.cpp` — Linux/Wayland collector using libinput/udev; writes CSV to `~/mouse-data`.
  - `preprocess.py` — Segments raw CSV into fixed-length event windows and computes features; writes `processed/<username>.csv`.
  - `merge_files.ipynb` — Helper to merge/prepare raw CSV files (optional).
- `classification/`
  - `decission_tree.py`, `knn.py`, `naive_bayes.py`, `random_forest.py`, `pca.py` — Baselines for multi-user classification using the engineered features.
  - `mlp.py` — Simple PyTorch MLP classifier (optional dependency).
- `abnormal/`
  - `one_class_svm.py` — Train One-Class SVM on a single user’s feature set.
  - `isolation_forest.py` — Train an Isolation Forest on a single user’s feature set.
  - `predict_svm.py`, `predict_isolation.py` — Evaluate anomaly detectors on test features.
- `AnomalyDetectorApp/`
  - `mouse_logger.cpp` — Windows low-level mouse hook that prints events to stdout for the GUI.
  - `main_app.py` — CustomTkinter GUI that reads the logger output, batches events, extracts features, and runs an anomaly model.
- `models/` — **Organized model storage**
  - `svm/` — One-Class SVM models (`*_anomaly_model.joblib`, `*_svm_model.joblib`)
  - `isolation_forest/` — Isolation Forest models (`*_isoforest_model.joblib`, `*_iso_model.joblib`)
  - `scalers/` — All scaler files (`*_scaler.joblib`, `*_svm_scaler.joblib`, `*_iso_scaler.joblib`)
- `scripts/` — **Training and utility scripts**
  - `train_user_specific.py` — Train models for all users and perform cross-user testing
  - `train_all_users.py` — Additional training utilities
- `results/` — **Training results and logs**
  - `training_results.txt` — Model performance summaries
- `data/` — Raw and processed data files
- `processed/` — Individual user feature files

## Data model

Raw CSV (produced by collectors) has the columns:

- `WindowTitle` — 64-bit hash of the active window title (Windows); `0` on Linux/Wayland (title not available via libinput).
- `State` — Mouse event type:
  - `DM` diagonal move, `VM` vertical move, `HM` horizontal move,
  - `LD`/`LU` left button down/up, `RD`/`RU` right button down/up,
  - `MW` mouse wheel
- `Time Diff` — Milliseconds since the previous event.
- `Day Time` — 5‑minute bucket index: `(hour*60 + minute)/5` (0–287).
- `X Pos`, `Y Pos` — Cursor coordinates (Windows) or accumulated relative deltas (Linux collector).

Feature CSV (produced by `collection/preprocess.py`) aggregates fixed-length segments (default 50 events) with columns including:

- Identity/context: `user`, `num_events`, `num_unique_window_titles`, `most_common_window_title_hash`, `most_common_daytime_bin`, `std_dev_daytime_bin`
- Motion: `segment_duration_ms`, `total_distance_pixels`, `path_straightness`
- Speed stats: `mean_speed`, `std_dev_speed`, `median_speed`, `skewness_speed`, `kurtosis_speed`, `max_speed`, `min_speed`
- Acceleration stats: `mean_acceleration`, `std_dev_acceleration`, `max_acceleration`
- Event counts/ratios per state: `count_DM`, `ratio_DM`, `count_VM`, `ratio_VM`, `count_HM`, `ratio_HM`, `count_LD`, `ratio_LD`, `count_LU`, `ratio_LU`, `count_RD`, `ratio_RD`, `count_RU`, `ratio_RU`, `count_MW`, `ratio_MW`
- `num_clicks` (derived)

Note: The GUI and anomaly scripts often exclude the count features during training; see each script’s exclusions/list of `TRAINING_FEATURES`.

## Quick start

### 1) Python environment

- Python 3.10+ recommended
- Create a virtual environment and install core dependencies

```zsh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional packages:

- PyTorch for `classification/mlp.py` (install according to your platform/CUDA)

### 2) Collect raw data

Choose your OS and collector. The collectors buffer events and periodically write CSV files.

- Windows console collector (`collection/collector.cpp`)

  - Builds a background logger writing to `C:\\mouse-data\\<date>_<hour>_<5min>.csv`.
  - Build (MSVC or MinGW), then run the executable.

- Linux/Wayland collector (`collection/collector_linux.cpp`)

  - Requires root privileges; writes to `~/mouse-data/<date>_<hour>_<5min>.csv`.
  - Build:

    ```zsh
    g++ collection/collector_linux.cpp -o wayland_mouse_logger -linput -ludev -std=c++17
    sudo ./wayland_mouse_logger
    ```

If you already have many CSVs, you can merge them with `collection/merge_files.ipynb` into a single file per user (e.g., `raw/<username>.csv`).

### 3) Preprocess and feature extraction

Use `collection/preprocess.py` to segment events and compute features:

- Edit the `username`, `data_files`, and `output_feature_file` at the bottom of the script as needed.
- Default segmentation is 50 events per segment (`segment_length_events=50`).
- Run:

```zsh
python collection/preprocess.py
```

This will write a feature CSV to `processed/<username>.csv`.

### 4) Train a classifier (multi-user)

If you have multiple users’ feature rows in a single CSV, you can train a classifier to predict `user`.

- The scripts in `classification/` expect either `features.csv` or `processed/features.csv` (there’s some inconsistency).
  - Easiest: create a unified features file `processed/features.csv` with a `user` column (concatenate multiple users’ processed CSVs).

Examples:

```zsh
# Random Forest with CV (expects processed/features.csv)
python classification/random_forest.py

# KNN / Decision Tree / Naive Bayes / PCA+XGBoost (default expects features.csv)
python classification/knn.py
python classification/decission_tree.py
python classification/naive_bayes.py
python classification/pca.py
```

For `mlp.py`, install PyTorch and run:

```zsh
python classification/mlp.py
```

### 5) Train an anomaly detector (single user)

You need a feature file for one user only.

- One-Class SVM (`abnormal/one_class_svm.py`)

  - Edit the `__main__` block to point `feature_file` to your single-user CSV (e.g., `processed/<user>.csv`).
  - Optionally change `username` used to name output files.
  - Outputs: `<username>_anomaly_model.joblib` and `<username>_scaler.joblib`.

  ```zsh
  python abnormal/one_class_svm.py
  ```

- Isolation Forest (`abnormal/isolation_forest.py`)

  - Edit the constants near the bottom: `username` and the `feature_file` path (defaults to `processed/train.csv`).
  - Outputs: `<username>_isoforest_model.joblib` and `<username>_scaler.joblib`.

  ```zsh
  python abnormal/isolation_forest.py
  ```

- Evaluate/predict:

  ```zsh
  # One-Class SVM predictor (set feature_file inside to your test user’s CSV)
  python abnormal/predict_svm.py

  # Isolation Forest predictor (set test_file/model/scaler inside the script)
  python abnormal/predict_isolation.py
  ```

Interpretation notes (per scripts): depending on model and thresholding:

- One-Class SVM uses `decision_function`; higher may indicate more anomalous depending on sign. Scripts currently count `anomaly_score >= 0` as anomaly.
- Isolation Forest uses `.predict()` where `-1` is anomaly and `1` is normal.

### 6) Run the Windows GUI app (real-time anomaly detection)

The GUI streams events from a native logger, extracts features in batches, scales them, and applies the trained One‑Class SVM.

- Build the Windows logger that prints events to stdout: `AnomalyDetectorApp/mouse_logger.cpp` → `mouse_logger.exe`.
- Place `mouse_logger.exe` next to `AnomalyDetectorApp/main_app.py` (or adjust path in the script).
- Ensure the trained model and scaler (`<USERNAME>_anomaly_model.joblib`, `<USERNAME>_scaler.joblib`) exist for the same `USERNAME` set at the top of `main_app.py`.
- Run the GUI:

```zsh
python AnomalyDetectorApp/main_app.py
```

Notes:

- The GUI is Windows‑focused. Linux collector doesn’t integrate with this GUI (it writes CSV files instead).
- `BATCH_SIZE` (default 2000 events) and `SEGMENT_LENGTH_EVENTS` (default 50) control processing cadence.
- `TRAINING_FEATURES` in the GUI is a subset of all engineered features; ensure your trained model used compatible features and scaling.

## Important paths and naming consistency

- The code sometimes references `features.csv`, `processed/features.csv`, or `processed/train.csv`. For reliability:
  - Keep your consolidated multi-user file at `processed/features.csv` for classification.
  - Keep per-user files as `processed/<username>.csv` for anomaly detection.
  - Edit path variables in scripts before running.

## Development tips and troubleshooting

- If you change feature engineering, retrain models and keep the scaler consistent. Save both model and scaler with `joblib`.
- On Linux/Wayland, window titles aren’t available via libinput; `WindowTitle` is `0`.
- Ensure `Time Diff` is numeric before segmentation; the preprocess script coerces and drops non-numeric rows.
- If `No suitable numerical features found` appears, verify your column names and that exclusions don’t remove everything.
- CustomTkinter requires a working Tk installation; on Linux you may need `tk`/`tk-dev` packages.

## Requirements

Core Python dependencies are listed in `requirements.txt`. Optional:

- PyTorch if you want to run `classification/mlp.py`.

## License

No explicit license is provided in this repository. If you intend to use or distribute this code, consider adding a license file.
