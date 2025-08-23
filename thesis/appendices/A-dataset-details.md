# Appendix A: Dataset Details

## A.1 Dataset Overview

76,693 behavioral segments from 4 participants during natural computer usage. Cross-platform collection (Windows/Linux) with standard hardware configurations over multi-week periods.

## A.2 Participant Information

- **atiq**: 18,957 segments, software development usage, moderate movement speed
- **masum**: 19,384 segments, academic research usage, highly distinctive patterns
- **rakib**: 19,156 segments, mixed development/browsing usage, variable patterns
- **zia**: 19,196 segments, general office usage, distinctive acceleration patterns

## A.3 Event Structure

**Event Types**: DM (Drag Move), VM (Vertical Move), HM (Horizontal Move), LD/LU (Left Down/Up), RD/RU (Right Down/Up), MW (Mouse Wheel)

**Attributes**: Timestamps, coordinates, event state, time differences, anonymized application context

## A.4 Data Processing

50-event segmentation windows, feature extraction yielding 36 features reduced to 16 core features for modeling.

- **VM (Vertical Move)**: Predominantly vertical mouse movements with minimal horizontal component
- **HM (Horizontal Move)**: Predominantly horizontal mouse movements with minimal vertical component

**Button Events**:

- **LD (Left Down)**: Left mouse button press events
- **LU (Left Up)**: Left mouse button release events
- **RD (Right Down)**: Right mouse button press events
- **RU (Right Up)**: Right mouse button release events

**Scroll Events**:

- **MW (Mouse Wheel)**: Mouse wheel scroll events in either direction

### A.3.2 Temporal Encoding

**Timestamp Precision**: All events are captured with millisecond precision using system-level timing mechanisms to ensure accurate temporal analysis.

**Time Difference Calculation**: Inter-event intervals are computed as the difference between consecutive event timestamps, providing direct measurement of interaction timing patterns.

**Day Time Discretization**: Time-of-day information is encoded in 5-minute bins (0-287) to provide temporal context while preserving privacy through coarse granularity.

### A.3.3 Spatial Encoding

**Coordinate System**: Screen coordinates are captured in pixel units relative to the primary display, with normalization procedures to accommodate different screen resolutions.

**Position Accuracy**: Cursor positions are captured at the native resolution of the input system, providing sub-pixel accuracy where supported by the operating system.

**Screen Boundaries**: All coordinates are validated to ensure they fall within expected screen boundaries, with outliers flagged for potential data quality issues.

### A.3.4 Contextual Information

**Window Title Hashing**: Application context is captured through cryptographic hashing of window titles to provide contextual information while preserving privacy.

**Session Management**: Data collection sessions are tracked to enable temporal segmentation and analysis of behavioral patterns across different usage periods.

## A.4 Segmentation and Processing Details

### A.4.1 Fixed-Event Window Implementation

**Window Size Rationale**: The 50-event window size was selected based on preliminary analysis showing this provides sufficient behavioral information while maintaining computational efficiency and real-time processing capability.

**Boundary Conditions**: Segment boundaries are strictly enforced at event counts with no overlapping windows, ensuring independent behavioral samples for statistical analysis.

**Session Handling**: Segments cannot span session boundaries, ensuring that each behavioral segment represents a coherent interaction period rather than artifacts of data collection timing.

### A.4.2 Quality Assurance Procedures

**Data Validation**: Comprehensive validation procedures check for temporal consistency, spatial validity, and event sequence correctness to ensure data quality.

**Outlier Detection**: Statistical outlier detection identifies unusual events that may result from data collection errors or anomalous system behavior.

**Completeness Assessment**: Analysis of data completeness across users and time periods ensures representative coverage of behavioral patterns.

## A.5 Statistical Characteristics

### A.5.1 Temporal Statistics

**Segment Duration Distribution**:

- Mean: 34.2 seconds
- Median: 28.7 seconds
- Standard Deviation: 18.4 seconds
- Range: 5.2 - 142.8 seconds

**Inter-Event Timing**:

- Mean: 127.3 milliseconds
- Median: 89.2 milliseconds
- 95th Percentile: 412.7 milliseconds

### A.5.2 Spatial Statistics

**Movement Distance Distribution**:

- Mean: 2,847.6 pixels per segment
- Median: 2,234.1 pixels per segment
- Standard Deviation: 1,923.4 pixels

**Screen Coverage**:

- Average screen utilization: 23.4% of total screen area
- Spatial clustering coefficient: 0.67
- Movement range variability: 0.43

### A.5.3 Event Type Distribution

**Overall Event Frequencies**:

- Movement events (DM/VM/HM): 78.3% of all events
- Click events (LD/LU/RD/RU): 18.9% of all events
- Scroll events (MW): 2.8% of all events

**User-Specific Variations**:

- Significant individual differences in event type preferences
- Consistent patterns within users across sessions
- Application-dependent variations in event distributions

## A.6 Data Quality Assessment

### A.6.1 Completeness Analysis

**Temporal Coverage**: Data collection achieved comprehensive temporal coverage across different times of day, days of week, and usage contexts for all participants.

**Behavioral Diversity**: The dataset encompasses diverse interaction patterns including different applications, tasks, and interface usage scenarios.

**Technical Quality**: Minimal data collection artifacts or technical issues, with error rates below 0.1% of collected events.

### A.6.2 Consistency Validation

**Within-User Consistency**: High consistency in behavioral patterns within individual users across different sessions and time periods.

**Cross-Platform Consistency**: Consistent behavioral pattern capture across different operating systems and hardware configurations.

**Temporal Stability**: Behavioral patterns show appropriate stability over the collection period with natural variations reflecting different usage contexts.

## A.7 Privacy and Anonymization

### A.7.1 Data Protection Measures

**Personal Information Removal**: All directly identifying information has been removed from the dataset with only behavioral characteristics retained.

**Application Context Anonymization**: Window titles are processed through cryptographic hashing to provide contextual information while preventing identification of specific applications or content.

**Temporal Discretization**: Precise timestamps are discretized to prevent detailed temporal tracking while preserving behavioral timing patterns.

### A.7.2 Anonymization Validation

**Re-identification Risk Assessment**: Comprehensive analysis confirms that the processed dataset does not enable re-identification of participants through behavioral patterns alone.

**Information Content Validation**: Verification that anonymization procedures preserve behavioral discrimination capability while protecting privacy.

**Compliance Verification**: Confirmation that data processing procedures comply with applicable privacy regulations and institutional guidelines.

## A.8 Dataset Distribution and Availability

### A.8.1 File Organization

**Processed Individual Files**:

- `processed/atiq.csv`: Individual behavioral features for user atiq
- `processed/masum.csv`: Individual behavioral features for user masum
- `processed/rakib.csv`: Individual behavioral features for user rakib
- `processed/zia.csv`: Individual behavioral features for user zia

**Unified Classification Dataset**:

- `processed/features.csv`: Combined dataset for multi-user classification experiments
- `processed/train.csv`: Training subset for validation experiments

**Raw Data Archive**:

- Individual user folders containing original event sequences
- Metadata files documenting collection parameters and procedures

### A.8.2 Data Format Specifications

**CSV Structure**: All processed data files use standard CSV format with headers describing feature names and data types.

**Feature Encoding**: Numerical features use standard floating-point representation while categorical features use string encoding.

**Missing Value Handling**: Missing values are explicitly encoded as null values with documentation of imputation procedures where applicable.

## A.9 Comparative Analysis

### A.9.1 Literature Comparison

**Dataset Size**: Our dataset of 76,693 segments represents one of the larger mouse dynamics datasets in the literature, enabling robust statistical analysis.

**User Population**: While the four-user population is modest compared to some studies, the depth of data per user provides detailed behavioral characterization.

**Temporal Scope**: The extended collection period provides better temporal coverage than many previous studies that focus on single-session data collection.

### A.9.2 Methodological Advantages

**Natural Usage Data**: Collection during natural computer usage provides higher ecological validity compared to controlled experimental tasks.

**Cross-Platform Coverage**: Multi-platform data collection demonstrates robustness across different technical environments.

**Quality Assurance**: Comprehensive quality assurance procedures ensure higher data reliability compared to studies with limited validation.

## A.10 Usage Guidelines and Recommendations

### A.10.1 Research Applications

**Replication Studies**: The comprehensive documentation enables exact replication of experimental procedures and validation of results.

**Extension Research**: The modular data organization supports extension to additional research questions and algorithmic approaches.

**Comparative Evaluation**: The standardized format facilitates comparison with other behavioral biometric datasets and approaches.

### A.10.2 Practical Applications

**Prototype Development**: The dataset provides a solid foundation for developing and testing practical behavioral authentication systems.

**Algorithm Validation**: The comprehensive coverage enables validation of new algorithmic approaches under realistic conditions.

**Performance Benchmarking**: The established performance baselines provide reference points for evaluating new methods and improvements.

This comprehensive dataset documentation provides the foundation for reproducible research and practical applications in mouse-based behavioral biometrics while ensuring appropriate privacy protection and data quality standards.
