## Motivation and Scope

Security systems increasingly rely on continuous authentication to supplement one-time logins. Mouse dynamics provide an unobtrusive, evergreen signal that can be collected without specialized hardware. This work focuses on everyday, free-form computer use rather than constrained gestures. The scope includes feature engineering from raw events, classical ML baselines for user identification, and single-user anomaly detection for continuous authentication.

We center our analysis on a four-user dataset (76,693 segments) with fixed 50-event windows, representative of a modest but realistic behavioral corpus. The methodology is designed to scale to more users and to integrate with additional modalities.
