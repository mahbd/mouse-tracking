#!/usr/bin/env python3

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
import joblib
import os

def train_user_specific_models():
    """Train anomaly detection models for each user using only their own data"""
    
    # Load the full dataset with all users
    df = pd.read_csv('../data/features.csv')
    users = df['user'].unique()
    
    # Features to use for training (excluding count features and metadata)
    training_features = [
        'segment_duration_ms', 'total_distance_pixels', 'mean_speed', 'std_dev_speed',
        'median_speed', 'skewness_speed', 'kurtosis_speed', 'max_speed', 'min_speed',
        'mean_acceleration', 'std_dev_acceleration', 'max_acceleration', 'path_straightness',
        'ratio_DM', 'ratio_VM', 'ratio_HM'
    ]
    
    results = {}
    
    for user in users:
        print(f"\n=== Training models for user: {user} ===")
        
        # Filter data for this user only
        user_data = df[df['user'] == user].copy()
        print(f"Training samples for {user}: {len(user_data)}")
        
        # Prepare features
        X = user_data[training_features].copy()
        X.dropna(inplace=True)
        
        if X.empty:
            print(f"No valid data for user {user}")
            continue
            
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train One-Class SVM
        print(f"Training One-Class SVM for {user}...")
        svm_model = OneClassSVM(gamma='scale', nu=0.05)
        svm_model.fit(X_scaled)
        
        # Save SVM model and scaler
        joblib.dump(svm_model, f'../models/svm/{user}_svm_model.joblib')
        joblib.dump(scaler, f'../models/scalers/{user}_svm_scaler.joblib')
        
        # Train Isolation Forest
        print(f"Training Isolation Forest for {user}...")
        iso_model = IsolationForest(contamination=0.05, random_state=42)
        iso_model.fit(X_scaled)
        
        # Save Isolation Forest model and scaler
        joblib.dump(iso_model, f'../models/isolation_forest/{user}_iso_model.joblib')
        joblib.dump(scaler, f'../models/scalers/{user}_iso_scaler.joblib')
        
        # Test on user's own data for baseline
        svm_predictions = svm_model.predict(X_scaled)
        iso_predictions = iso_model.predict(X_scaled)
        
        svm_anomalies = np.sum(svm_predictions == -1)
        iso_anomalies = np.sum(iso_predictions == -1)
        
        results[user] = {
            'samples': len(X),
            'svm_anomalies': svm_anomalies,
            'svm_anomaly_rate': svm_anomalies / len(X) * 100,
            'iso_anomalies': iso_anomalies,
            'iso_anomaly_rate': iso_anomalies / len(X) * 100
        }
        
        print(f"SVM detected {svm_anomalies}/{len(X)} anomalies ({svm_anomalies/len(X)*100:.2f}%)")
        print(f"Isolation Forest detected {iso_anomalies}/{len(X)} anomalies ({iso_anomalies/len(X)*100:.2f}%)")
    
    return results

def cross_user_anomaly_test():
    """Test each user's model on other users' data to see cross-user anomaly detection"""
    
    df = pd.read_csv('../data/features.csv')
    users = df['user'].unique()
    
    training_features = [
        'segment_duration_ms', 'total_distance_pixels', 'mean_speed', 'std_dev_speed',
        'median_speed', 'skewness_speed', 'kurtosis_speed', 'max_speed', 'min_speed',
        'mean_acceleration', 'std_dev_acceleration', 'max_acceleration', 'path_straightness',
        'ratio_DM', 'ratio_VM', 'ratio_HM'
    ]
    
    print("\n=== CROSS-USER ANOMALY DETECTION TEST ===")
    
    cross_results = {}
    
    for model_user in users:
        print(f"\nTesting {model_user}'s models on other users:")
        
        # Load the user's models
        try:
            svm_model = joblib.load(f'../models/svm/{model_user}_svm_model.joblib')
            svm_scaler = joblib.load(f'../models/scalers/{model_user}_svm_scaler.joblib')
            iso_model = joblib.load(f'../models/isolation_forest/{model_user}_iso_model.joblib')
            iso_scaler = joblib.load(f'../models/scalers/{model_user}_iso_scaler.joblib')
        except FileNotFoundError:
            print(f"Models for {model_user} not found, skipping...")
            continue
        
        cross_results[model_user] = {}
        
        for test_user in users:
            if test_user == model_user:
                continue  # Skip self-testing
                
            # Get test user's data
            test_data = df[df['user'] == test_user].copy()
            X_test = test_data[training_features].copy()
            X_test.dropna(inplace=True)
            
            if X_test.empty:
                continue
            
            # Scale using the model user's scaler
            X_test_scaled_svm = svm_scaler.transform(X_test)
            X_test_scaled_iso = iso_scaler.transform(X_test)
            
            # Predict anomalies
            svm_pred = svm_model.predict(X_test_scaled_svm)
            iso_pred = iso_model.predict(X_test_scaled_iso)
            
            svm_anomalies = np.sum(svm_pred == -1)
            iso_anomalies = np.sum(iso_pred == -1)
            
            svm_rate = svm_anomalies / len(X_test) * 100
            iso_rate = iso_anomalies / len(X_test) * 100
            
            cross_results[model_user][test_user] = {
                'svm_anomaly_rate': svm_rate,
                'iso_anomaly_rate': iso_rate,
                'samples': len(X_test)
            }
            
            print(f"  {test_user}: SVM {svm_rate:.1f}% anomalies, ISO {iso_rate:.1f}% anomalies ({len(X_test)} samples)")
    
    return cross_results

if __name__ == "__main__":
    # Train user-specific models
    results = train_user_specific_models()
    
    print("\n=== TRAINING SUMMARY ===")
    for user, stats in results.items():
        print(f"{user}: {stats['samples']} samples, SVM: {stats['svm_anomaly_rate']:.2f}% anomalies, ISO: {stats['iso_anomaly_rate']:.2f}% anomalies")
    
    # Test cross-user anomaly detection
    cross_results = cross_user_anomaly_test()
    
    print("\n=== CROSS-USER ANOMALY DETECTION SUMMARY ===")
    for model_user, test_results in cross_results.items():
        print(f"\n{model_user}'s models detecting anomalies in other users:")
        for test_user, rates in test_results.items():
            print(f"  {test_user}: SVM {rates['svm_anomaly_rate']:.1f}%, ISO {rates['iso_anomaly_rate']:.1f}%")
