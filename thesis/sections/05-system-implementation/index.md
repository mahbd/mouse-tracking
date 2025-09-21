\newpage
\thispagestyle{plain}

\begin{center}
\vspace*{2cm}
\textbf{\Large CHAPTER 5}\\[0.5cm]
\textbf{\Large SYSTEM IMPLEMENTATION}
\end{center}

\newpage

## 5.1 Overview

The system integrates data collection, preprocessing/feature engineering, model training, and an optional real-time GUI app.

## 5.2 Collectors (C++)

- Windows: `collection/collector.cpp` and `AnomalyDetectorApp/mouse_logger.cpp` (low-level hook).
- Linux/Wayland: `collection/collector_linux.cpp` using libinput/udev; root privileges required.

## 5.3 Preprocessing (Python)

- Script: `collection/preprocess.py` segments events (50 per window) and computes features.
- Outputs: `processed/<username>.csv` per user; merged `processed/features.csv` for classification.

## 5.4 Modeling (Python)

- Classification: `classification/*.py` scripts implement baselines and an MLP.
- Anomaly: `abnormal/one_class_svm.py`, `abnormal/isolation_forest.py` with predictors.
- Models and scalers saved to `models/` subfolders.

## 5.5 Real-Time GUI

- `AnomalyDetectorApp/main_app.py` reads events from the Windows logger, batches to segments, scales, and applies a trained One-Class SVM.
- Configuration: BATCH_SIZE, SEGMENT_LENGTH_EVENTS, and TRAINING_FEATURES must match training setup.

## 5.6 Project Structure

See repository `README.md` for a detailed overview of folders and scripts.
