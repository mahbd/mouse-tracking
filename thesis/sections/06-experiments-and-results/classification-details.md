## Classification Details

We trained classic classifiers on `processed/features.csv` using stratified 5-fold CV. Random Forest provided the best accuracy (85.36%), consistent with non-linear interactions among kinematic and pattern features. KNN showed sensitivity to scaling and feature correlation. The MLP underperformed likely due to limited data and minimal tuning.
