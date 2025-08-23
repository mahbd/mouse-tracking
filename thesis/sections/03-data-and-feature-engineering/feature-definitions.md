## Feature Definitions

- segment_duration_ms: sum of time deltas within the window.
- total_distance_pixels: cumulative Euclidean distance along cursor positions.
- path_straightness: ratio of end-to-end distance to path length (0,1].
- mean_speed, std_dev_speed, median_speed: first-order kinematics from distance/time.
- skewness_speed, kurtosis_speed: higher-moment descriptors of speed distribution.
- max_speed, min_speed: extremes of estimated speed.
- mean_acceleration, std_dev_acceleration, max_acceleration: changes in speed per unit time.
- ratio_DM/VM/HM: fraction of movement events with diagonal/vertical/horizontal components.

Counts and identity-related features (e.g., window title hash) are often excluded in modeling to focus on behavior.
