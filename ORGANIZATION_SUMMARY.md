# Project Organization Summary

## Changes Made

### 1. Created Organized Folder Structure
- `models/` - Centralized model storage
  - `svm/` - One-Class SVM models
  - `isolation_forest/` - Isolation Forest models  
  - `scalers/` - All scaler files
- `scripts/` - Training and utility scripts
- `results/` - Training results and logs

### 2. Moved Files to Appropriate Locations
- **SVM Models**: `*_anomaly_model.joblib`, `*_svm_model.joblib` → `models/svm/`
- **Isolation Forest Models**: `*_isoforest_model.joblib`, `*_iso_model.joblib` → `models/isolation_forest/`
- **Scalers**: All `*_scaler.joblib` files → `models/scalers/`
- **Training Scripts**: `train_*.py` → `scripts/`
- **Results**: `training_results.txt` → `results/`

### 3. Updated Code References
Updated all scripts to use the new organized paths:

#### Anomaly Detection Scripts (`abnormal/`)
- `one_class_svm.py` - Updated model/scaler save paths
- `isolation_forest.py` - Updated model/scaler save paths  
- `predict_svm.py` - Updated model/scaler load paths
- `predict_isolation.py` - Updated model/scaler load paths

#### Training Scripts (`scripts/`)
- `train_user_specific.py` - Updated all model save/load paths

#### Classification Scripts (`classification/`)
- All scripts updated to use `../features.csv` path

#### GUI Application (`AnomalyDetectorApp/`)
- `main_app.py` - Updated model/scaler load paths

### 4. Updated Documentation
- `README.md` - Updated repository structure section to reflect new organization

## Benefits
- **Clean base directory** - No more scattered model files
- **Logical organization** - Models grouped by type
- **Easier maintenance** - Clear separation of concerns
- **Better scalability** - Easy to add new model types
- **Consistent paths** - All scripts use organized structure

## Usage Notes
- Run training scripts from the `scripts/` directory
- Run classification scripts from the `classification/` directory  
- Run anomaly detection scripts from the `abnormal/` directory
- All paths are relative to the script's location
