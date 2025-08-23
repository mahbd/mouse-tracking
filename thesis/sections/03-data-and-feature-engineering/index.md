\newpage
\thispagestyle{plain}

\begin{center}
\vspace*{2cm}
\textbf{\Large CHAPTER 3}\\[0.5cm]
\textbf{\Large DATA AND FEATURE ENGINEERING}
\end{center}

\newpage

## 3.1 Data Collection and Processing

Raw mouse events are transformed into behavioral signatures through systematic feature engineering. Our approach emphasizes behavioral relevance, statistical robustness, privacy preservation, computational efficiency, and interpretability.

## 3.2 Event Structure

**Event Types**: Movement (cursor changes), clicks (button press/release), scrolling (wheel events), hover/dwell (stability periods).

**Attributes**: Temporal (timestamps, intervals), spatial (X/Y coordinates), behavioral (event classifications), contextual (anonymized application data).

**Quality Assurance**: Temporal consistency, spatial validity, sequence validation, completeness monitoring.

## 3.3 Feature Engineering

**Segmentation**: 50-event windows providing consistent behavioral data.

**Feature Categories**:

- **Temporal**: Segment duration, inter-event intervals, rhythm patterns
- **Spatial**: Total distance, path straightness, movement range
- **Kinematic**: Velocity statistics (mean, median, max, std dev, skewness, kurtosis)
- **Statistical**: Distribution characteristics and higher-order patterns

**Core Features**: From 36 engineered features, 16 selected based on discrimination power: segment_duration_ms, total_distance_pixels, path_straightness, mean_speed, median_speed, max_speed, std_dev_speed, skewness_speed, kurtosis_speed, plus temporal and spatial statistics.

**Fixed-Time Windows**: Consistent temporal scope but variable behavioral data amounts.

**Fixed-Event Windows**: Consistent behavioral data but variable temporal scope.

**Activity-Based Segmentation**: Natural behavioral units requiring sophisticated detection.

**Adaptive Segmentation**: Optimal behavioral units with implementation complexity.

### 3.3.2 Fixed-Event Window Approach

For this research, we adopt a fixed-event window approach with 50 consecutive mouse events per behavioral segment. This choice is motivated by several important considerations:

**Behavioral Consistency**: Fixed-event windows ensure that each behavioral segment contains the same amount of interaction data, facilitating direct comparison between segments and consistent feature computation.

**Temporal Adaptivity**: By focusing on event count rather than time duration, the segmentation naturally adapts to individual interaction speeds and activity levels, capturing behavioral patterns at the natural temporal scale of each user.

**Computational Efficiency**: Fixed-event windows simplify real-time processing by providing predictable computational loads and memory requirements for feature extraction and classification.

**Literature Compatibility**: The 50-event window size is consistent with previous research in mouse dynamics, enabling comparison with published results and leveraging established best practices.

### 3.3.3 Segmentation Implementation

The implementation of fixed-event segmentation requires careful consideration of several technical details:

**Window Boundaries**: Segments are constructed using strict event ordering without overlap, ensuring that each event contributes to exactly one behavioral segment. This approach prevents information leakage between segments while maximizing data utilization.

**Session Handling**: Segment boundaries are not permitted to cross user session boundaries, ensuring that behavioral segments represent coherent interaction periods rather than artifacts of data collection scheduling.

**Quality Filtering**: Segments containing anomalous events (invalid coordinates, timing errors, etc.) are excluded from analysis to prevent data quality issues from affecting behavioral modeling.

**Buffer Management**: Real-time implementation requires efficient buffer management to maintain sliding windows of events for continuous segmentation and feature extraction.

### 3.3.4 Segment Characteristics Analysis

Understanding the characteristics of the resulting behavioral segments is important for interpreting feature extraction results and assessing the appropriateness of the segmentation strategy:

**Temporal Duration Distribution**: Analysis of segment duration distributions reveals the natural temporal scope of behavioral segments across different users and contexts. Our 50-event segments typically span 10-60 seconds depending on user interaction patterns.

**Event Type Distribution**: Analysis of event type distributions within segments provides insights into the behavioral richness captured by each segment and the consistency of interaction patterns.
We selected 50-event windows providing consistent behavioral data for analysis. This approach balances temporal consistency with sufficient behavioral information capture.

## 3.4 Comprehensive Feature Engineering Framework

Our framework transforms raw mouse events into meaningful behavioral features across multiple dimensions:

### 3.4.1 Feature Categories

**Temporal Features**: Timing patterns, interaction rhythm, temporal dynamics
**Spatial Features**: Movement patterns, spatial preferences, geometric properties  
**Kinematic Features**: Velocity, acceleration, movement dynamics
**Contextual Features**: Application usage, environmental factors
**Statistical Features**: Distribution characteristics and higher-order patterns

### 3.4.2 Key Features

**Temporal**: Segment duration (segment_duration_ms), average inter-event intervals, temporal variance and stability

**Spatial**: Total distance traveled (total_distance_pixels), path straightness (ratio of straight-line to actual distance), movement range and distribution

**Kinematic**: Mean/median/max/min speed, velocity standard deviation, acceleration patterns, movement smoothness indicators

**Statistical**: Velocity skewness/kurtosis indicating movement distribution characteristics

### 3.4.3 Feature Selection

From 36 engineered features, we selected 16 core features based on discrimination power and stability:

- Temporal: segment_duration_ms, time-based statistics
- Spatial: total_distance_pixels, path_straightness
- Kinematic: mean_speed, median_speed, max_speed, std_dev_speed, skewness_speed, kurtosis_speed
- Additional: movement smoothness, pause characteristics, directional preferences

#### Acceleration Analysis

Acceleration features provide information about movement smoothness and control characteristics:

**Acceleration Computation**: For each velocity measurement:

```
acceleration_i = (velocity_i+1 - velocity_i) / time_interval_i
```

**Statistical Acceleration Features**:

- **Mean Acceleration (mean_acceleration)**: Average acceleration indicating typical acceleration patterns
- **Standard Deviation (std_dev_acceleration)**: Acceleration variability indicating smoothness of movement control
- **Maximum Acceleration (max_acceleration)**: Peak acceleration indicating maximum control capability

#### Advanced Kinematic Analysis

**Jerk Analysis**: Computation of jerk (rate of change of acceleration) to capture movement smoothness and neuromotor control characteristics.

**Movement Phase Analysis**: Segmentation of movements into acceleration, constant velocity, and deceleration phases with analysis of phase characteristics and transitions.

**Ballistic vs. Corrective Movement Analysis**: Classification of movements into ballistic (rapid, ballistic movements) and corrective (slower, guided movements) categories with separate analysis of each category.

### 3.4.5 Contextual Feature Engineering

Contextual features capture information about the interaction environment and usage patterns while maintaining privacy through statistical abstraction.

#### Application Context Features

**Window Title Analysis**: Statistical analysis of application usage patterns through hashed window titles:

**Most Common Window Title Hash (most_common_window_title_hash)**: The most frequently occurring application context within each segment, providing information about primary application usage.

**Application Diversity**: Measures of application switching frequency and diversity within segments, indicating multitasking patterns and interface navigation behavior.

#### Temporal Context Features

**Time-of-Day Analysis**: Analysis of interaction patterns relative to time-of-day:

**Most Common Day Time Bin (most_common_daytime_bin)**: The most frequent time-of-day category (5-minute bins) within each segment.

**Day Time Standard Deviation (std_dev_daytime_bin)**: Variability in time-of-day within segments, indicating session temporal consistency.

**Circadian Pattern Analysis**: Analysis of behavioral variations across different times of day to capture individual circadian behavioral patterns.

### 3.4.6 Event Pattern Features

Event pattern features analyze the distribution and sequencing of different types of mouse events to capture individual interaction style preferences.

#### Event Type Distribution

**Movement Event Ratios**: Proportions of different movement types within each segment:

- **Ratio DM (ratio_DM)**: Proportion of drag movement events
- **Ratio VM (ratio_VM)**: Proportion of vertical movement events
- **Ratio HM (ratio_HM)**: Proportion of horizontal movement events

These ratios capture individual preferences for different types of movement patterns and interaction styles.

**Click Event Analysis**: Analysis of clicking patterns including click frequency, timing, and coordination with movement events.

**Scroll Event Analysis**: Analysis of scrolling behavior including scroll frequency, direction preferences, and rhythm patterns.

#### Event Sequence Analysis

**Transition Pattern Analysis**: Analysis of event type transitions using techniques such as Markov chain analysis to capture sequential dependencies in interaction patterns.

**Event Clustering**: Temporal clustering of similar events to identify burst patterns and interaction rhythms that may be characteristic of individual users.

### 3.4.7 Statistical Summary Features

Statistical summary features provide higher-order characterizations of behavioral distributions that capture subtle individual differences in interaction patterns.

#### Distribution Shape Analysis

**Skewness Analysis**: Computation of skewness for various behavioral measures to capture distribution asymmetry patterns that may be characteristic of individual users.

**Kurtosis Analysis**: Computation of kurtosis for behavioral measures to capture distribution peakedness and tail characteristics.

**Percentile Analysis**: Computation of various percentiles (10th, 25th, 75th, 90th) for behavioral measures to capture distribution shape characteristics.

#### Correlation and Dependency Analysis

**Feature Correlation Analysis**: Analysis of correlations between different behavioral measures within each segment to capture coordination patterns and dependencies.

**Temporal Autocorrelation**: Analysis of temporal dependencies within behavioral sequences to capture rhythm and pattern characteristics.

## 3.5 Feature Selection and Optimization

The comprehensive feature engineering framework produces a total of 36 distinct features across all categories. However, practical machine learning applications often benefit from feature selection that focuses on the most discriminative and stable features while reducing computational complexity.

### 3.5.1 Feature Selection Criteria

Our feature selection process is guided by several important criteria:

**Discriminative Power**: Features should demonstrate strong ability to distinguish between different users in preliminary analysis and have high information content for classification tasks.

**Stability**: Features should exhibit reasonable consistency within users over time while maintaining distinctiveness between users.

**Independence**: Selected features should provide complementary information rather than redundant characterizations of the same behavioral aspects.

**Interpretability**: Where possible, selected features should have clear behavioral interpretations that enable system understanding and debugging.

**Computational Efficiency**: Selected features should be computable with reasonable computational overhead for real-time applications.

### 3.5.2 Core Feature Set Selection

Based on extensive preliminary analysis and literature review, we identify a core set of 16 features that provide optimal balance between discrimination capability and practical implementation requirements:

#### Temporal Features (1)

- **segment_duration_ms**: Basic temporal scope normalization

#### Spatial Features (2)

- **total_distance_pixels**: Movement extent characterization
- **path_straightness**: Navigation efficiency analysis

#### Kinematic Features (10)

- **mean_speed**: Central tendency of velocity distribution
- **std_dev_speed**: Velocity consistency characterization
- **median_speed**: Robust central tendency estimate
- **skewness_speed**: Velocity distribution asymmetry
- **kurtosis_speed**: Velocity distribution peakedness
- **max_speed**: Peak movement capability
- **min_speed**: Baseline movement speed
- **mean_acceleration**: Acceleration tendency characterization
- **std_dev_acceleration**: Acceleration consistency analysis
- **max_acceleration**: Peak acceleration capability

#### Event Pattern Features (3)

- **ratio_DM**: Drag movement preference
- **ratio_VM**: Vertical movement preference
- **ratio_HM**: Horizontal movement preference

This core feature set provides comprehensive coverage of the most important behavioral dimensions while maintaining computational efficiency and interpretability.

### 3.5.3 Feature Exclusion Strategy

Certain features are systematically excluded from the core set for specific reasons:

**Direct Identity Features**: Features such as explicit user identifiers are excluded to focus on pure behavioral characteristics rather than direct identity cues.

**Event Count Features**: Raw event counts are excluded because they are inherently constant due to our fixed-event segmentation strategy and provide no discriminative information.

**Highly Contextual Features**: Features that are strongly dependent on specific applications or environmental factors are excluded to improve generalizability across different usage scenarios.

**Redundant Features**: Features that provide essentially the same information as other selected features are excluded to reduce dimensionality and prevent multicollinearity issues.

## 3.6 Preprocessing and Normalization

Effective preprocessing and normalization of features is crucial for ensuring optimal performance of machine learning algorithms and maintaining consistency across different experimental conditions.

### 3.6.1 Data Cleaning and Validation

The preprocessing pipeline begins with comprehensive data cleaning and validation procedures:

**Missing Value Handling**: Detection and appropriate handling of missing values that may result from data collection issues or computation errors. Our approach uses domain-specific imputation strategies rather than generic missing value techniques.

**Outlier Detection**: Identification and handling of extreme outliers that may result from data collection errors or unusual behavioral circumstances. We employ statistical outlier detection based on inter-quartile range analysis combined with domain knowledge constraints.

**Data Type Validation**: Ensuring appropriate data types for all features and correcting type conversion issues that may arise during data collection or processing.

**Range Validation**: Validation that all feature values fall within expected ranges based on domain knowledge and detection of impossible values that indicate computation errors.

### 3.6.2 Feature Scaling and Normalization

Different features in our framework exhibit vastly different scales and distributions, making normalization essential for many machine learning algorithms:

**StandardScaler Application**: We employ scikit-learn's StandardScaler to transform features to have zero mean and unit variance:

```
scaled_feature = (feature - mean) / standard_deviation
```

This transformation ensures that all features contribute equally to distance-based algorithms and prevents features with larger scales from dominating the analysis.

**Scaling Procedure**: The scaling transformation is fit on training data only and then applied to both training and validation data to prevent information leakage that could bias performance estimates.

**Scaler Persistence**: Trained scalers are saved alongside trained models to ensure consistent preprocessing during inference and deployment.

### 3.6.3 Feature Distribution Analysis

Understanding the statistical properties of engineered features is important for algorithm selection and performance interpretation:

**Distribution Shape Analysis**: Analysis of feature distributions to identify skewness, kurtosis, and other characteristics that may affect algorithm performance or require specialized handling.

**Correlation Analysis**: Computation of feature correlation matrices to identify highly correlated features that may cause multicollinearity issues in some algorithms.

**Class Separability Analysis**: Analysis of feature distributions across different user classes to identify the most discriminative features and understand the behavioral basis for classification performance.

## 3.7 Privacy and Ethical Considerations

The design of our feature engineering framework incorporates important privacy and ethical considerations that are essential for responsible deployment of behavioral biometric systems.

### 3.7.1 Data Minimization Principles

**Content Abstraction**: Our features focus on movement dynamics and statistical patterns rather than specific content or detailed activity information, minimizing privacy exposure while preserving behavioral discrimination capability.

**Temporal Abstraction**: Time-of-day information is discretized into coarse bins rather than precise timestamps, providing contextual information while reducing temporal tracking capabilities.

**Spatial Abstraction**: Spatial features focus on movement patterns rather than specific screen locations or content positions, preserving behavioral information while minimizing location tracking.

**Application Abstraction**: Application context is captured through statistical usage patterns rather than detailed application monitoring, providing contextual information while preserving activity privacy.

### 3.7.2 Anonymization Strategies

**Hash-Based Anonymization**: Window titles and other potentially identifying information are processed through cryptographic hashing to prevent direct identification while preserving statistical analysis capabilities.

**Statistical Aggregation**: Individual events are aggregated into statistical summaries that preserve behavioral patterns while preventing reconstruction of specific interaction sequences.

**Identifier Removal**: Direct user identifiers are separated from behavioral features and handled through secure key management procedures to prevent accidental linkage.

### 3.7.3 Consent and Transparency

**Informed Consent**: Data collection procedures incorporate comprehensive informed consent processes that clearly explain what behavioral information is collected and how it is used.

**Data Usage Transparency**: Clear documentation of data usage, retention periods, and sharing policies ensures that users understand how their behavioral information is handled.

**Control Mechanisms**: Provision of user controls for data collection preferences, retention periods, and deletion requests supports user autonomy and privacy management.

## 3.8 Implementation Architecture

The technical implementation of our feature engineering framework emphasizes efficiency, maintainability, and extensibility to support both research and practical deployment scenarios.

### 3.8.1 Software Architecture

**Modular Design**: The feature engineering pipeline is implemented using a modular architecture that separates data loading, preprocessing, feature extraction, and output formatting into distinct components.

**Configuration Management**: Comprehensive configuration management enables easy adjustment of feature selection, processing parameters, and output formats without code modifications.

**Error Handling**: Robust error handling and logging capabilities ensure reliable operation and facilitate debugging in both development and production environments.

**Performance Optimization**: Implementation optimizations including vectorized computation, efficient data structures, and memory management ensure acceptable performance for real-time applications.

### 3.8.2 Data Flow Architecture

**Stream Processing**: The architecture supports both batch processing for training data and stream processing for real-time applications, ensuring consistency between training and inference pipelines.

**Quality Assurance**: Integrated quality assurance checks at each stage of the pipeline ensure data integrity and feature quality throughout the processing workflow.

**Monitoring and Logging**: Comprehensive monitoring and logging capabilities enable performance tracking, error detection, and system optimization in operational deployments.

### 3.8.3 Extensibility and Maintenance

**Feature Framework**: The modular feature framework enables easy addition of new features and modification of existing features without affecting other system components.

**Version Management**: Versioning of feature definitions and processing procedures ensures reproducibility and enables controlled evolution of the feature engineering approach.

**Documentation**: Comprehensive documentation of feature definitions, computation procedures, and implementation details facilitates maintenance and knowledge transfer.

## 3.9 Validation and Quality Assurance

Ensuring the quality and correctness of engineered features is crucial for reliable behavioral analysis and system performance.

### 3.9.1 Feature Validation Procedures

**Mathematical Validation**: Verification that feature computations produce mathematically correct results through unit testing, boundary condition analysis, and comparison with manual calculations.

**Behavioral Validation**: Verification that features capture intended behavioral characteristics through analysis of feature values for known behavioral patterns and correlation with expected behavioral differences.

**Consistency Validation**: Verification that features produce consistent results across different processing runs, data orderings, and computational environments.

### 3.9.2 Cross-Validation and Reproducibility

**Reproducible Processing**: Implementation of deterministic processing procedures that produce identical results given identical inputs, supporting reproducible research and reliable deployment.

**Cross-Platform Validation**: Validation of feature computation across different operating systems and hardware configurations to ensure consistent behavioral analysis capabilities.

**Version Control Integration**: Integration with version control systems to track changes in feature definitions and ensure reproducibility of experimental results.

## 3.10 Dataset Characteristics and Statistics

Understanding the characteristics of our processed dataset provides important context for interpreting experimental results and assessing the generalizability of our findings.

### 3.10.1 Dataset Scale and Scope

**Total Segments**: Our processed dataset comprises 76,693 behavioral segments across all users, representing a substantial corpus for behavioral analysis.

**User Distribution**: The dataset includes contributions from four users (atiq, masum, rakib, zia) with varying levels of data contribution reflecting natural differences in computer usage patterns.

**Temporal Scope**: Data collection spans multiple sessions and time periods for each user, providing insights into both short-term behavioral consistency and longer-term patterns.

**Behavioral Diversity**: The dataset encompasses diverse interaction patterns including different applications, tasks, and usage scenarios, enhancing the ecological validity of our analysis.

### 3.10.2 Feature Distribution Analysis

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
