\newpage
	hispagestyle{plain}

\begin{center}
\vspace*{2cm}
	extbf{\Large CHAPTER 2}\\[0.5cm]
	extbf{\Large BACKGROUND AND RELATED WORK}
\end{center}

\newpage

## 2.1 Behavioral Biometrics (condensed)

Behavioral biometrics use measurable interaction patterns (e.g., keystrokes, mouse movement, touch) to identify or re‑authenticate users [@traore2012; @bailey2014]. Their advantages are unobtrusive collection and continuous monitoring; primary challenges are intra‑user variability, class imbalance, and privacy. Key properties are distinctiveness, stability, collectability, and measurability.

## 2.2 Mouse Dynamics (condensed)

Mouse dynamics capture cursor trajectories, clicks and scrolls at millisecond resolution. Common feature families are temporal (timing, pauses), spatial (path length, straightness), kinematic (velocity, acceleration, jerk), and statistical summaries (moments, percentiles) [@gamboa2004; @gamboa2004]. Early work established feasibility [@pusara2004; @brodley2003], while later studies refined feature sets and demonstrated robust verification systems [@zheng2011; @shen2013; @mondal2015].

## 2.3 Anomaly Detection & User Classification (condensed)

Anomaly detection learns per‑user baselines (OC‑SVM, Isolation Forest, autoencoders) to flag deviations [@ahmed2004; @pusara2004]. User classification treats the problem as multi‑class supervised learning (Random Forest, SVM, MLP, KNN) and requires careful cross‑validation, class‑balanced metrics (precision/recall/F1), and temporal testing to assess stability [@eberz2017].

## 2.4 Privacy and Security (condensed)

Behavioral data is sensitive: minimize raw logging, anonymize context (hash window titles), store aggregated summaries, and obtain informed consent. Threats include replay, spoofing, and model inversion; mitigations are freshness checks, model hardening, and strict access controls. Compliance with GDPR and industry standards is required for deployments.

## 2.5 Selected Related Work (highlights)

- Pusara & Brodley (2004): early re‑authentication via statistical outlier detection.
- Ahmed & Traore (2007): comprehensive feature-based identification study.
- Zheng et al. (2011), Shen et al. (2013), Mondal & Bours (2015): advanced feature engineering and continuous authentication approaches.

## 2.6 Gaps and Opportunities (condensed)

Existing gaps include limited cross‑user analysis at scale, inconsistent evaluation protocols, practical deployment details (real‑time capture, cross‑platform collection), and limited treatment of privacy-preserving operational practices—areas this thesis targets.

\newpage
