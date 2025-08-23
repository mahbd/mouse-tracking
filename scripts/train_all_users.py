#!/usr/bin/env python3

import pandas as pd
import sys
import os
sys.path.append('.')

from abnormal.one_class_svm import train_anomaly_model_for_user
from abnormal.isolation_forest import train_isolation_forest_model

def train_models_for_all_users():
    users = ['atiq', 'masum', 'rakib', 'zia']
    
    for user in users:
        print(f"\n=== Training models for user: {user} ===")
        
        # Train One-Class SVM
        print(f"Training One-Class SVM for {user}...")
        try:
            train_anomaly_model_for_user(
                feature_file='data/processed/train.csv',
                user_model_output_path=f'{user}_anomaly_model.joblib',
                scaler_output_path=f'{user}_svm_scaler.joblib',
            )
            print(f"One-Class SVM model saved for {user}")
        except Exception as e:
            print(f"Error training One-Class SVM for {user}: {e}")
        
        # Train Isolation Forest
        print(f"Training Isolation Forest for {user}...")
        try:
            train_isolation_forest_model(
                feature_file='processed/train.csv',
                user_model_output_path=f'{user}_isoforest_model.joblib',
                scaler_output_path=f'{user}_isoforest_scaler.joblib',
            )
            print(f"Isolation Forest model saved for {user}")
        except Exception as e:
            print(f"Error training Isolation Forest for {user}: {e}")

if __name__ == "__main__":
    train_models_for_all_users()
