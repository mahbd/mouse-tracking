# Data and Feature Engineering

## Raw Mouse Event Data

Raw CSV events include: WindowTitle (hash or 0), State (DM/VM/HM/LD/LU/RD/RU/MW), Time Diff (ms), Day Time (5-min bin), X Pos, Y Pos.

## Segmentation Strategy

- Fixed-length windows of 50 consecutive events per behavioral segment.
- Benefits: controls for window size variability; simplifies model input.
- Alternatives: time-based windows, overlapping windows (future work).

## Engineered Features

We compute 36 features and typically select a 16-feature subset for modeling:

- Temporal: segment_duration_ms
- Spatial: total_distance_pixels, path_straightness
- Speed: mean_speed, std_dev_speed, median_speed, skewness_speed, kurtosis_speed, max_speed, min_speed
- Acceleration: mean_acceleration, std_dev_acceleration, max_acceleration
- Movement ratios: ratio_DM, ratio_VM, ratio_HM
- Context/identity: user, most_common_window_title_hash, most_common_daytime_bin, std_dev_daytime_bin, event counts (often excluded)

## Preprocessing

- Numeric coercion for timing fields; drop invalid rows.
- Feature exclusions: remove counts and metadata for behavior-only models.
- Standardization: StandardScaler fit per training split; scalers saved to `models/scalers/`.

## Datasets

- Users: atiq, masum, rakib, zia
- Total segments: 76,693
- Distribution per user given in `results/results.md`.

## Storage Layout

- Processed per-user features: `processed/<username>.csv`
- Unified features for classification: `processed/features.csv`

## Reproducibility Notes

- Preprocess with `collection/preprocess.py`.
- Keep segmentation length and feature list consistent between training and inference (GUI).
