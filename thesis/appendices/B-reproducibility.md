# Appendix B: Reproducibility

## Environment

Python 3.13, key libraries: scikit-learn, pandas, numpy, xgboost. Install with `pip install -r requirements.txt`.

## Execution Steps

1. Collect data with OS-specific collectors
2. Run `collection/preprocess.py` for feature extraction
3. Execute `classification/` scripts for user identification
4. Run `abnormal/` scripts for anomaly detection
5. Use `AnomalyDetectorApp/main_app.py` for real-time analysis

## Artifacts

Models saved in `models/`, results in `results/`. Random seeds set for repeatability.
