# Appendix B: Reproducibility

## Environment

- Python 3.13
- Key libraries: scikit-learn, pandas, numpy, joblib, xgboost, (optional) PyTorch.
- Install with `pip install -r requirements.txt` in a virtual environment.

## Steps

1. Collect raw CSVs with the OS-specific collectors.
2. Run `collection/preprocess.py` to generate `processed/<username>.csv`.
3. For classification: prepare `processed/features.csv` with multiple users.
4. Run scripts in `classification/` to train and evaluate classifiers.
5. For anomaly detection: run `abnormal/one_class_svm.py` and `abnormal/isolation_forest.py` per user, then `predict_*` scripts for evaluation.
6. Real-time: run `AnomalyDetectorApp/main_app.py` on Windows with a trained SVM model and scaler.

## Models and Artifacts

- Models saved in `models/svm/` and `models/isolation_forest/`.
- Scalers saved in `models/scalers/`.
- Results summarized in `results/`.

## Notes

- Keep feature lists and scaler alignment consistent between training and inference.
- Random seeds are set where applicable for repeatability.
