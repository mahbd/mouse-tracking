# Background and Related Work

This section surveys behavioral biometrics with emphasis on mouse dynamics, anomaly detection, and user classification.

## Behavioral Biometrics

Behavioral biometrics analyze how people perform actions (typing, moving a mouse, swiping, gait). Unlike physiological traits (fingerprint, face), behavioral traits can be monitored continuously and updated over time, enabling continuous authentication and intrusion detection.

## Mouse Dynamics

Prior work shows that cursor trajectories, speed/acceleration profiles, and click timing can uniquely characterize users \cite{rahman2021}. Common paradigms include:

- Fixed-task gestures (e.g., target acquisition, drag-and-drop)
- Free-form activity logs during normal computer use

Feature classes often include trajectory geometry, kinematics, frequency of event types, and context (application window, time-of-day). Our pipeline focuses on free-form events aggregated into fixed-length segments.

## Anomaly Detection Techniques

- One-Class SVM: Learns a decision boundary around normal data using an RBF kernel. Key parameter: nu (anomaly fraction). Pros: solid theoretical foundation; Cons: scaling-sensitive.
- Isolation Forest: Isolates anomalies via random partitions. Key parameter: contamination. Pros: efficient, less sensitive to scaling; Cons: may over-flag in heterogeneous data.

## User Classification

Classical ML (Random Forest, Decision Trees, KNN, Naive Bayes) remains competitive on tabular behavioral features. Ensembles capture non-linear interactions and often outperform linear baselines. Neural networks can underperform without abundant data and tuning.

## Threats and Considerations

- Data drift over time (fatigue, device change) threatens stability.
- Privacy: mouse dynamics are less sensitive than content, but still identifying. Aggregation and differential privacy can mitigate risks.
- Adversarial concerns: spoofing trajectories may be possible; continuous monitoring and multi-modal fusion improve robustness.

## References

- \cite{rahman2021}: Mouse movement-driven authentication and region usage (IEEE CCWC 2021)
- \cite{paper_document}: Additional PDF resource provided with limited metadata; update when full details are known
