\newpage
	hispagestyle{plain}

\begin{center}
\vspace*{2cm}
	extbf{\Large CHAPTER 3}\\[0.5cm]
	extbf{\Large DATA AND FEATURE ENGINEERING}
\end{center}

\newpage

## 3.1 Data and Event Overview (condensed)

Raw mouse events (movements, clicks, scrolls) are captured with timestamps and X/Y coordinates and converted into fixed-length segments (50 events) for analysis. Segments balance temporal context and computational tractability while enabling consistent feature computation.

## 3.2 Feature Families (condensed)

We extract compact, interpretable features grouped as:
- Temporal: segment duration, inter-event intervals, pause rates.
- Spatial: total distance, path straightness, movement range.
- Kinematic: mean/median/max speed, acceleration statistics, jerk.
- Statistical: skewness, kurtosis, percentiles, and event‑type ratios.

From an initial set of ~36 engineered features, a core subset (~16) was selected by mutual information, stability, and cross‑validation performance to reduce redundancy and computational cost. These selection and aggregation practices follow common procedures in mouse dynamics research and continuous authentication literature [@zheng2011; @shen2013].

## 3.3 Preprocessing and Scaling (condensed)

Pipeline steps: data cleaning, missing value handling, outlier filtering (IQR‑based), and StandardScaler normalization fit on training data only. Scalers and feature definitions are persisted with models to ensure consistent inference. These preprocessing steps mirror established pipelines for behavioral biometric datasets and help reduce session-level variability and measurement noise [@gamboa2004; @pusara2004].

## 3.4 Privacy and Contextual Features (condensed)

To reduce identifiability we aggregate events into summaries, hash window titles for coarse application context, discretize time‑of‑day into bins, and avoid raw location storage. Consent and secure storage policies are enforced.

## 3.5 Dataset Snapshot (condensed)

Dataset includes contributions from four users with thousands of segments (example: atiq ≈5k, masum ≈4k). Segments average ~50 events and cover diverse tasks and sessions, enabling both within‑user and cross‑user evaluation.

## 3.6 Implementation Notes (condensed)

The feature pipeline is modular for batch and streaming modes, implemented with vectorized operations for speed, and versioned to ensure reproducibility. Unit tests validate key computations (e.g., distance, velocity, acceleration).

\newpage

**Statistical Summaries**: Comprehensive statistical summaries of all engineered features including means, standard deviations, ranges, and distribution characteristics provide insights into the behavioral space covered by our dataset.

**Inter-User Variability**: Analysis of feature distributions across different users reveals the degree of behavioral distinctiveness captured by our feature engineering approach.

**Temporal Stability**: Analysis of feature consistency within users over time provides insights into the stability of behavioral patterns and the appropriateness of our feature definitions.

### 3.10.3 Quality Metrics

**Completeness**: Assessment of data completeness across users, time periods, and interaction types ensures representative coverage of behavioral patterns.

**Consistency**: Analysis of feature consistency and reliability across different data collection sessions and computational runs validates the robustness of our feature engineering approach.

**Validity**: Comparison of computed features with expected behavioral characteristics and literature benchmarks validates the correctness and appropriateness of our feature definitions.

## 3.11 Summary and Implications

This comprehensive treatment of data and feature engineering establishes the foundation for effective behavioral biometric analysis based on mouse interaction patterns. Our approach successfully transforms raw mouse event streams into meaningful behavioral signatures while addressing important practical considerations including computational efficiency, privacy preservation, and system maintainability.

The resulting feature engineering framework provides several important capabilities:

**Comprehensive Behavioral Characterization**: The multi-dimensional feature approach captures temporal, spatial, kinematic, and contextual aspects of mouse interaction patterns, providing rich behavioral signatures suitable for both classification and anomaly detection applications.

**Privacy-Preserving Analysis**: The statistical abstraction approach preserves essential behavioral characteristics while minimizing privacy exposure through content abstraction, temporal discretization, and anonymization techniques.

**Practical Implementation**: The modular, efficient implementation supports both research applications and practical deployment scenarios with appropriate attention to performance, maintainability, and extensibility requirements.

**Quality Assurance**: Comprehensive validation and quality assurance procedures ensure reliable and reproducible feature extraction suitable for rigorous experimental evaluation and operational deployment.

The insights gained from this feature engineering process inform the subsequent methodological approach and experimental evaluation presented in the following chapters. The balance achieved between behavioral discrimination capability, privacy preservation, and computational efficiency demonstrates the feasibility of practical mouse-based behavioral biometric systems while establishing a solid foundation for future research and development in this area.

\newpage
