\newpage
\thispagestyle{plain}

\begin{center}
\vspace*{2cm}
\textbf{\Large ABSTRACT}
\end{center}

\vspace*{2cm}

Traditional authentication mechanisms are vulnerable to security threats, necessitating continuous authentication systems. This thesis investigates mouse tracking as a behavioral biometric for user identification and anomaly detection.

We address multi-user classification and single-user anomaly detection using comprehensive mouse interaction data from four participants, resulting in 76,693 behavioral segments. From 50-event windows, we engineered 36 behavioral features encompassing temporal, spatial, kinematic, and contextual characteristics.

For classification, Random Forest achieved optimal performance (85.36% accuracy), significantly outperforming Decision Trees (77.24%), PCA+XGBoost (70.20%), KNN (60.30%), MLP (44.43%), and Naive Bayes (38.37%). For anomaly detection, One-Class SVM and Isolation Forest achieved expected ~5% self-test rates while demonstrating significant cross-user distinctiveness (up to 31.6% anomaly rates).

The complete implementation includes cross-platform data collection, preprocessing pipelines, model training frameworks, and real-time GUI components. Results demonstrate mouse dynamics viability for continuous authentication, with implications for cybersecurity and human-computer interaction. The 85.36% classification accuracy and meaningful anomaly discrimination support practical deployment potential.

\newpage
