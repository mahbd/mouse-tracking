## Anomaly Detection Details

For each user, we trained One-Class SVM and Isolation Forest on that user’s segments with 5% contamination (nu=0.05). Self-tests confirmed calibration (~5% anomalies). Cross-user tests quantified distinctiveness, with Masum’s models flagging 11–31.6% anomalies for other users, while Atiq’s models flagged ~1–5%.

These results indicate varying uniqueness in behavioral patterns and justify personalized thresholds in deployment.
