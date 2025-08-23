ewpage
hispagestyle{plain}

\begin{center}
\vspace\*{2cm}
extbf{\Large CHAPTER 4}\[0.5cm]
extbf{\Large METHODOLOGY}
\end{center}

ewpage

## 4.1 Introduction to Experimental Methodology

The experimental methodology employed in this research is designed to provide rigorous, reproducible, and comprehensive evaluation of mouse-based behavioral biometrics for both user identification and anomaly detection applications. Our methodological approach emphasizes statistical rigor, practical applicability, and transparent reporting to ensure that findings can inform both academic research and practical deployment decisions.

The design of our experimental methodology is guided by several key principles:

**Scientific Rigor**: All experimental procedures are designed to meet high standards of scientific methodology including appropriate controls, statistical validation, and reproducible procedures.

**Practical Relevance**: Experimental conditions are designed to reflect realistic deployment scenarios rather than artificial laboratory conditions, ensuring that findings are applicable to real-world implementations.

**Comprehensive Coverage**: The methodology encompasses both user identification and anomaly detection tasks, multiple machine learning algorithms, and various evaluation metrics to provide comprehensive assessment of system capabilities.

**Reproducibility**: All experimental procedures, parameter settings, and evaluation protocols are fully documented to enable independent reproduction and validation of results.

**Statistical Validity**: Appropriate statistical techniques are employed throughout the evaluation process to ensure reliable conclusions and appropriate interpretation of results.

## 4.2 Problem Formulation and Research Questions

Our experimental methodology addresses two fundamental problems in behavioral biometrics, each requiring distinct approaches and evaluation strategies.

### 4.2.1 Multi-User Classification Problem

The user identification problem seeks to determine which of several known users is currently interacting with the system based on observed behavioral patterns. This represents a supervised learning problem where behavioral features serve as input variables and user identity serves as the target variable.

**Formal Problem Definition**: Given a behavioral segment $X = \{x_1, x_2, ..., x_n\}$ where each $x_i$ represents a behavioral feature, predict the user identity $y \in \{u_1, u_2, ..., u_k\}$ where $k$ is the number of known users.

**Research Questions**:

1. What level of classification accuracy can be achieved using mouse behavioral features for user identification?
2. Which machine learning algorithms are most effective for this task?
3. Which behavioral features contribute most significantly to classification performance?
4. How consistent is classification performance across different users?
5. What are the primary sources of classification errors and confusion between users?

### 4.2.2 Single-User Anomaly Detection Problem

The anomaly detection problem focuses on identifying when observed behavior deviates significantly from an established baseline for a known user, enabling detection of unauthorized access or behavioral changes.

**Formal Problem Definition**: Given a trained model $M_u$ representing normal behavioral patterns for user $u$, and a new behavioral segment $X$, determine whether $X$ represents normal behavior for user $u$ or anomalous behavior that may indicate unauthorized access.

**Research Questions**:

1. How effectively can anomaly detection algorithms distinguish between normal and anomalous behavior for individual users?
2. What level of cross-user behavioral distinctiveness can be achieved (how often do other users' behaviors appear anomalous)?
3. How do different anomaly detection algorithms compare in terms of sensitivity and specificity?
4. What are appropriate threshold settings for practical deployment scenarios?
5. How stable are anomaly detection models over time and across different usage contexts?

## 4.3 Experimental Design Framework

Our experimental design employs a comprehensive framework that addresses both classification and anomaly detection tasks while ensuring statistical validity and practical relevance.

### 4.3.1 Dataset Organization and Partitioning

**User-Stratified Approach**: All experimental procedures maintain user stratification to ensure balanced representation and prevent bias toward users with larger amounts of training data.

**Cross-Validation Strategy**: We employ 5-fold stratified cross-validation for all classification experiments to provide robust performance estimates and assess variability in algorithmic performance.

**Temporal Considerations**: While our current dataset does not span sufficient time periods for comprehensive temporal analysis, our experimental design accounts for temporal factors and provides frameworks for future longitudinal evaluation.

**Data Integrity**: Strict data partitioning procedures ensure that no information leakage occurs between training and testing phases, maintaining the validity of performance estimates.

### 4.3.2 Feature Engineering Integration

**Consistent Feature Pipeline**: All experiments use identical feature engineering procedures to ensure comparable results across different algorithms and experimental conditions.

**Feature Selection Validation**: Feature selection procedures are applied within each cross-validation fold to prevent information leakage and provide unbiased performance estimates.

**Scaling and Normalization**: Feature scaling procedures are consistently applied across all experiments with scalers fit only on training data and applied to validation data.

### 4.3.3 Algorithm Selection and Configuration

**Comprehensive Algorithm Coverage**: We evaluate multiple algorithm categories including tree-based methods, ensemble approaches, distance-based methods, probabilistic models, and neural networks to provide comprehensive performance comparison.

**Hyperparameter Optimization**: Systematic hyperparameter optimization is employed for algorithms where performance is sensitive to parameter settings, using grid search or random search as appropriate.

**Baseline Comparisons**: Performance comparisons include both sophisticated algorithms and simple baselines to establish performance context and assess the value of complex approaches.

## 4.4 User Classification Methodology

The user classification methodology encompasses algorithm selection, training procedures, evaluation metrics, and analysis approaches specifically designed for multi-user identification tasks.

### 4.4.1 Algorithm Selection and Rationale

We evaluate six distinct machine learning algorithms that represent different approaches to classification and have proven effective in behavioral biometric applications:

#### Random Forest

**Algorithm Overview**: Random Forest constructs multiple decision trees using random subsets of features and training samples, then combines their predictions through majority voting.

**Rationale for Inclusion**: Random Forest has demonstrated excellent performance in behavioral biometric applications due to its ability to handle complex feature interactions, resistance to overfitting, and inherent feature importance analysis capabilities.

**Configuration**: We optimize the number of estimators (50-200), maximum depth (5-20), and maximum features (auto, sqrt, log2) using grid search cross-validation.

#### Decision Trees

**Algorithm Overview**: Single decision trees create hierarchical rules based on feature values to classify samples into user categories.

**Rationale for Inclusion**: Decision trees provide highly interpretable models that can reveal the most important behavioral discriminators and decision patterns.

**Configuration**: We optimize maximum depth (5-20), minimum samples split (2-10), and minimum samples leaf (1-5) parameters.

#### k-Nearest Neighbors (KNN)

**Algorithm Overview**: KNN classifies samples based on the majority class among the k nearest neighbors in the feature space.

**Rationale for Inclusion**: KNN provides a non-parametric approach that can capture complex decision boundaries without making strong distributional assumptions.

**Configuration**: We optimize k (3-15), distance metrics (Euclidean, Manhattan), and weighting schemes (uniform, distance-based).

#### Naive Bayes

**Algorithm Overview**: Naive Bayes applies Bayes' theorem with independence assumptions between features to compute class probabilities.

**Rationale for Inclusion**: Naive Bayes provides a probabilistic baseline and performs surprisingly well despite strong independence assumptions.

**Configuration**: We evaluate Gaussian Naive Bayes with default parameters and assess performance sensitivity to feature scaling.

#### Principal Component Analysis + XGBoost

**Algorithm Overview**: Dimensionality reduction through PCA followed by gradient boosting classification using XGBoost.

**Rationale for Inclusion**: This combination addresses potential curse of dimensionality issues while leveraging the strong performance of gradient boosting methods.

**Configuration**: We optimize the number of PCA components (5-15) and XGBoost parameters including learning rate, max depth, and regularization terms.

#### Multi-Layer Perceptron (MLP)

**Algorithm Overview**: Neural network with multiple hidden layers trained using backpropagation to learn complex non-linear mappings.

**Rationale for Inclusion**: Neural networks provide automatic feature learning capabilities and can potentially capture complex behavioral patterns.

**Configuration**: We optimize network architecture (hidden layer sizes), learning rate, regularization parameters, and activation functions.

### 4.4.2 Training and Validation Procedures

**Cross-Validation Protocol**: 5-fold stratified cross-validation ensures that each fold maintains the original user distribution while providing robust performance estimates across different data partitions.

**Stratification Procedure**: Stratification is performed at the user level to ensure balanced representation of all users in each training and validation fold.

**Hyperparameter Optimization**: Grid search cross-validation is employed within each training fold to select optimal hyperparameters without introducing bias from validation data.

**Model Persistence**: Trained models and associated preprocessing components (scalers, feature selectors) are saved for each fold to enable reproducible evaluation and error analysis.

### 4.4.3 Performance Evaluation Metrics

**Overall Accuracy**: The proportion of correctly classified samples provides a general measure of system performance:
$$ ext{Accuracy} = \frac{ ext{Correct Predictions}}{ ext{Total Predictions}}$$

**Per-Class Precision**: The proportion of correct predictions for each user class:
$$ ext{Precision}\_u = \frac{ ext{True Positives}\_u}{ ext{True Positives}\_u + ext{False Positives}\_u}$$

**Per-Class Recall**: The proportion of actual instances correctly identified for each user:
$$ ext{Recall}\_u = \frac{ ext{True Positives}\_u}{ ext{True Positives}\_u + ext{False Negatives}\_u}$$

**F1-Score**: The harmonic mean of precision and recall for each user:
$$ ext{F1-Score}\_u = 2 imes \frac{ ext{Precision}\_u imes ext{Recall}\_u}{ ext{Precision}\_u + ext{Recall}\_u}$$

**Confusion Matrix Analysis**: Detailed analysis of classification errors to identify patterns in misclassification and user pairs that are difficult to distinguish.

### 4.4.4 Statistical Significance Testing

**Performance Comparison**: Statistical significance testing using paired t-tests or non-parametric alternatives to assess whether performance differences between algorithms are statistically significant.

**Confidence Intervals**: Computation of confidence intervals for performance metrics to quantify uncertainty in performance estimates.

**Effect Size Analysis**: Assessment of practical significance alongside statistical significance to determine whether performance differences are meaningful for practical applications.

## 4.5 Anomaly Detection Methodology

The anomaly detection methodology addresses the unique challenges of single-class learning and threshold setting for continuous authentication applications.

### 4.5.1 Anomaly Detection Algorithm Selection

#### One-Class Support Vector Machine (OC-SVM)

**Algorithm Overview**: OC-SVM learns a decision boundary that encapsulates normal behavioral patterns using an RBF kernel, with the nu parameter controlling the expected fraction of anomalies.

**Rationale for Inclusion**: OC-SVM provides a solid theoretical foundation based on statistical learning theory and has demonstrated effectiveness in behavioral anomaly detection applications.

**Configuration**: We use RBF kernel with nu=0.05 (expecting 5% anomalies) and optimize gamma parameter through cross-validation.

#### Isolation Forest

**Algorithm Overview**: Isolation Forest isolates anomalies by constructing random decision trees that partition the feature space, with anomalies requiring fewer partitions to isolate.

**Rationale for Inclusion**: Isolation Forest provides computational efficiency and reduced sensitivity to feature scaling compared to distance-based methods.

**Configuration**: We use 100 estimators, contamination=0.05 (expecting 5% anomalies), and random_state=42 for reproducibility.

### 4.5.2 Training and Validation Procedures

**Individual User Models**: Separate anomaly detection models are trained for each user using only their behavioral data to establish personalized behavioral baselines.

**Self-Validation**: Each user's model is validated on a held-out portion of their own data to assess calibration and confirm expected anomaly rates.

**Cross-User Validation**: Each user's model is tested on other users' data to assess cross-user behavioral distinctiveness and threshold sensitivity.

**Threshold Analysis**: Systematic analysis of decision thresholds to understand the trade-off between false positive and false negative rates.

### 4.5.3 Evaluation Metrics for Anomaly Detection

**Self-Test Anomaly Rate**: The proportion of a user's own data flagged as anomalous by their trained model:
$$ ext{Self-Anomaly Rate}\_u = \frac{ ext{Anomalous Predictions on User}\_u}{ ext{Total Predictions for User}\_u}$$

**Cross-User Anomaly Rate**: The proportion of other users' data flagged as anomalous by a user's model:

$$
	ext{Cross-Anomaly Rate}_{u
ightarrow v} = \frac{	ext{Anomalous Predictions on User}_v}{	ext{Total Predictions for User}_v}
$$

**Calibration Assessment**: Comparison of observed anomaly rates with expected rates based on algorithm configuration to assess model calibration.

**Distinctiveness Analysis**: Analysis of the distribution of cross-user anomaly rates to quantify behavioral distinctiveness and identify users with highly distinctive patterns.

## 4.6 Feature Analysis Methodology

Understanding the contribution and importance of different behavioral features is crucial for system optimization and behavioral interpretation.

### 4.6.1 Feature Importance Analysis

**Random Forest Feature Importance**: Utilization of Random Forest's built-in feature importance measures based on impurity reduction to identify the most discriminative behavioral features.

**Permutation Importance**: Assessment of feature importance through permutation testing, measuring the decrease in model performance when each feature is randomly shuffled.

**Correlation Analysis**: Analysis of feature correlations to identify redundant features and understand relationships between different behavioral characteristics.

### 4.6.2 Ablation Studies

**Feature Category Ablation**: Systematic removal of different feature categories (temporal, spatial, kinematic, contextual) to assess their individual contributions to classification and anomaly detection performance.

**Individual Feature Analysis**: Analysis of individual feature contributions through systematic inclusion and exclusion studies.

**Minimal Feature Set Identification**: Identification of the smallest feature set that maintains acceptable performance for practical applications with computational constraints.

### 4.6.3 Behavioral Interpretation

**Feature Distribution Analysis**: Analysis of feature distributions across different users to understand the behavioral basis for discrimination.

**Pattern Recognition**: Identification of behavioral patterns that distinguish between users and contribute to classification performance.

**Contextual Analysis**: Investigation of how behavioral features vary across different contexts and usage scenarios.

## 4.7 Validation and Reproducibility Framework

Ensuring the validity and reproducibility of experimental results is fundamental to scientific methodology and practical applicability.

### 4.7.1 Experimental Controls

**Consistent Preprocessing**: All algorithms receive identically preprocessed data to ensure fair comparison and eliminate preprocessing-related performance differences.

**Standardized Evaluation**: All algorithms are evaluated using identical metrics, cross-validation procedures, and statistical tests to enable direct performance comparison.

**Parameter Documentation**: Complete documentation of all algorithmic parameters, random seeds, and configuration settings to enable exact reproduction of results.

### 4.7.2 Bias Prevention and Mitigation

**Data Leakage Prevention**: Strict procedures to prevent information leakage between training and validation data, including proper scaling, feature selection, and cross-validation procedures.

**Selection Bias Mitigation**: Systematic evaluation of multiple algorithms and parameter settings to prevent cherry-picking of favorable results.

**Reporting Bias Prevention**: Comprehensive reporting of all experimental results, including negative results and performance limitations.

### 4.7.3 Statistical Rigor

**Multiple Comparison Correction**: Application of appropriate statistical corrections when conducting multiple comparisons to prevent inflated Type I error rates.

**Effect Size Reporting**: Reporting of effect sizes alongside statistical significance to assess practical importance of observed differences.

**Confidence Interval Estimation**: Provision of confidence intervals for all performance estimates to quantify uncertainty and enable risk assessment.

## 4.8 Threats to Validity and Mitigation Strategies

Acknowledging and addressing potential threats to validity is essential for reliable experimental conclusions and appropriate interpretation of results.

### 4.8.1 Internal Validity Threats

**Selection Bias**: The limited number of participants (four users) may not be representative of broader user populations.
_Mitigation_: Transparent reporting of participant characteristics and limitations; detailed analysis of individual user patterns to understand variability.

**Temporal Bias**: Data collection over relatively short time periods may not capture longer-term behavioral evolution.
_Mitigation_: Analysis of available temporal patterns; framework design for future longitudinal evaluation.

**Environmental Bias**: Data collection in controlled environments may not reflect real-world usage variability.
_Mitigation_: Collection during natural computer usage; documentation of environmental factors; discussion of generalizability limitations.

### 4.8.2 External Validity Threats

**Population Generalizability**: Findings may not generalize to users with different demographic characteristics, technical expertise, or usage patterns.
_Mitigation_: Detailed documentation of participant characteristics; discussion of generalizability limitations; framework for future diverse population studies.

**Technology Generalizability**: Results may not generalize to different hardware configurations, operating systems, or software environments.
_Mitigation_: Multi-platform data collection; documentation of technical environments; analysis of cross-platform consistency.

**Task Generalizability**: Behavioral patterns may vary significantly across different computing tasks and applications.
_Mitigation_: Collection during diverse usage scenarios; analysis of contextual factors; discussion of task-dependent limitations.

### 4.8.3 Construct Validity Threats

**Feature Validity**: Engineered features may not accurately capture the intended behavioral characteristics.
_Mitigation_: Comprehensive feature validation; comparison with literature benchmarks; behavioral interpretation analysis.

**Model Validity**: Machine learning models may not accurately represent the underlying behavioral patterns.
_Mitigation_: Multiple algorithm evaluation; model interpretation analysis; performance validation across different conditions.

## 4.9 Ethical Considerations in Experimental Design

The experimental methodology incorporates important ethical considerations that are essential for responsible research in behavioral biometrics.

### 4.9.1 Informed Consent

**Comprehensive Disclosure**: Participants receive complete information about data collection procedures, intended uses, and potential risks.

**Voluntary Participation**: All participation is voluntary with the right to withdraw at any time without penalty.

**Ongoing Consent**: Participants are informed of any changes to data usage or research procedures.

### 4.9.2 Privacy Protection

**Data Minimization**: Collection is limited to the minimum behavioral information necessary for research objectives.

**Anonymization**: Personal identifiers are separated from behavioral data and protected through secure procedures.

**Secure Storage**: All data is stored using appropriate security measures and access controls.

### 4.9.3 Risk Mitigation

**Minimal Risk Design**: Experimental procedures are designed to minimize potential risks to participants.

**Confidentiality Protection**: Strong confidentiality measures protect participant privacy and prevent unauthorized disclosure.

**Responsible Reporting**: Research results are reported in ways that protect participant privacy and prevent potential misuse.

## 4.10 Implementation and Computational Considerations

The practical implementation of our experimental methodology requires careful attention to computational efficiency, reproducibility, and maintainability.

### 4.10.1 Computational Architecture

**Modular Implementation**: Experimental code is organized into modular components that enable independent testing and validation of different algorithmic approaches.

**Parallel Processing**: Where appropriate, parallel processing techniques are employed to accelerate experimental evaluation while maintaining reproducibility.

**Resource Management**: Efficient memory and storage management enables handling of large datasets and complex experimental configurations.

### 4.10.2 Reproducibility Infrastructure

**Version Control**: All experimental code, configuration files, and documentation are maintained under version control to enable exact reproduction of results.

**Environment Management**: Computational environments are carefully documented and managed to ensure consistent execution across different systems.

**Automated Testing**: Automated testing procedures validate the correctness of experimental implementations and detect potential regression errors.

### 4.10.3 Performance Optimization

**Algorithm Efficiency**: Implementation optimizations ensure acceptable computational performance for both training and inference phases.

**Scalability Considerations**: Experimental frameworks are designed to accommodate larger datasets and more complex experimental configurations.

**Real-Time Capability**: Where relevant, experimental implementations support real-time analysis suitable for practical deployment scenarios.

## 4.11 Summary and Methodological Contributions

This comprehensive experimental methodology provides a rigorous framework for evaluating mouse-based behavioral biometrics while addressing important considerations of validity, reproducibility, and ethical responsibility. The methodology makes several important contributions:

**Comprehensive Evaluation Framework**: The dual focus on both classification and anomaly detection provides complete assessment of system capabilities for different application scenarios.

**Statistical Rigor**: Careful attention to cross-validation, significance testing, and bias prevention ensures reliable and interpretable results.

**Practical Relevance**: Experimental conditions and evaluation metrics are designed to reflect realistic deployment scenarios rather than artificial laboratory conditions.

**Reproducibility Standards**: Complete documentation and standardized procedures enable independent validation and extension of results.

**Ethical Integration**: Comprehensive integration of ethical considerations ensures responsible research practices and participant protection.

The following chapters present the results of applying this methodology to our mouse dynamics dataset, providing detailed analysis of both user identification and anomaly detection performance along with insights into the behavioral patterns that enable effective mouse-based authentication.

ewpage
