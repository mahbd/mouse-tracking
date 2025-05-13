import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from collections import Counter

def load_data(file_paths):
    all_data = []
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            all_data.append(df)
        except FileNotFoundError:
            print(f"Warning: File not found {file_path}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    if not all_data:
        return pd.DataFrame()
        
    return pd.concat(all_data, ignore_index=True)

def _process_chunk_by_events(chunk_rows, segment_length_events, all_segments_list):
    if not chunk_rows:
        return
    chunk_df = pd.DataFrame(list(chunk_rows))
    if chunk_df.empty:
        return
    for i in range(0, len(chunk_df), segment_length_events):
        sub_segment_df = chunk_df.iloc[i:i + segment_length_events]
        all_segments_list.append(sub_segment_df)

def segment_data(df, segment_length_events=50, large_time_diff_threshold=10000, user_col='Name', time_col='TimeDiff'):
    all_segments = []
    if df.empty:
        print("Warning: Input DataFrame to segment_data is empty.")
        return all_segments

    if not pd.api.types.is_numeric_dtype(df[time_col]):
        print(f"Warning: Time column '{time_col}' is not numeric. Attempting conversion.")
        df[time_col] = pd.to_numeric(df[time_col], errors='coerce')
        df.dropna(subset=[time_col], inplace=True)

    for _, group in df.groupby(user_col):
        current_chunk_rows = []
        if group.empty:
            continue

        for _, row_series in group.iterrows():
            time_diff_for_current_event = row_series[time_col]
            if current_chunk_rows and time_diff_for_current_event > large_time_diff_threshold:
                _process_chunk_by_events(current_chunk_rows, segment_length_events, all_segments)
                current_chunk_rows = []
            current_chunk_rows.append(row_series)

        if current_chunk_rows:
            _process_chunk_by_events(current_chunk_rows, segment_length_events, all_segments)
            
    return all_segments

def calculate_segment_features(segment_df):
    """
    Calculates various features for a single segment of mouse data.
    Assumes segment_df column names are: 'XPos', 'YPos', 'TimeDiff', 'State', 'WindowTitle', 'DayTime', 'Name'.
    """
    features = {}

    if segment_df.empty:
        return features

    # Define required columns based on typical usage in this function
    # Note: 'Name' is used for 'user', but not strictly required for all calcs if handled upstream
    required_cols = ['XPos', 'YPos', 'TimeDiff', 'State', 'WindowTitle', 'DayTime']
    missing_cols = [col for col in required_cols if col not in segment_df.columns]
    if missing_cols:
        print(f"Warning: Segment missing required columns: {missing_cols}. Skipping feature extraction for this segment.")
        return features

    # Basic Info
    features['user'] = segment_df['Name'].iloc[0] if 'Name' in segment_df.columns else 'Unknown'
    features['segment_duration_ms'] = segment_df['TimeDiff'].sum() # Includes time from prev event to first event in segment
    features['num_events'] = len(segment_df)

    # Kinematic Features
    # Calculate displacements (dx, dy) for each step within the segment
    # .diff() computes the difference from the PREVIOUS row.
    # dx[i] = XPos[i] - XPos[i-1]. dx[0] will be NaN, filled with 0.
    dx = segment_df['XPos'].diff().fillna(0)
    dy = segment_df['YPos'].diff().fillna(0)

    # step_distances[i] is the distance of the move from point i-1 to point i.
    # step_distances[0] will be 0 because dx[0] and dy[0] are 0.
    step_distances_full = np.sqrt(dx**2 + dy**2)
    features['total_distance_pixels'] = step_distances_full.sum()

    # Speed Calculation:
    # Speed is calculated for actual movements within the segment.
    # A movement occurs from point i-1 to point i, taking segment_df['TimeDiff'].iloc[i] time.
    # So, we consider step_distances_full.iloc[1:] and segment_df['TimeDiff'].iloc[1:].
    
    actual_movement_distances = step_distances_full.iloc[1:].reset_index(drop=True)
    actual_movement_times = segment_df['TimeDiff'].iloc[1:].reset_index(drop=True)

    speeds = pd.Series(dtype=float) # Initialize empty series for speeds
    if not actual_movement_times.empty:
        valid_time_mask = actual_movement_times > 0
        if valid_time_mask.any():
            # Calculate speeds only for movements with positive time duration
            speeds = actual_movement_distances[valid_time_mask] / actual_movement_times[valid_time_mask]
            # speeds index will be from the valid_time_mask

    if not speeds.empty:
        features['mean_speed'] = speeds.mean()
        features['std_dev_speed'] = speeds.std() if len(speeds) >= 2 else 0
        features['median_speed'] = speeds.median()
        # Skewness and Kurtosis are meaningful with more data points
        features['skewness_speed'] = skew(speeds) if len(speeds) >= 3 else 0
        features['kurtosis_speed'] = kurtosis(speeds) if len(speeds) >= 4 else 0 # Fisher kurtosis (normal=0)
        features['max_speed'] = speeds.max()
        features['min_speed'] = speeds.min()
    else:
        features['mean_speed'] = 0
        features['std_dev_speed'] = 0
        features['median_speed'] = 0
        features['skewness_speed'] = 0
        features['kurtosis_speed'] = 0
        features['max_speed'] = 0
        features['min_speed'] = 0

    # Acceleration Calculation:
    # Acceleration is the change in speed over time.
    # speed_changes[i] = speeds[i] - speeds[i-1]
    # The time interval for this change is the time taken for the movement that resulted in speeds[i].
    # These times are from actual_movement_times that corresponded to the speeds.
    
    accelerations = pd.Series(dtype=float) # Initialize empty series
    if len(speeds) > 1:
        speed_changes = speeds.diff() # First element will be NaN
        
        # Get the time durations that correspond to each speed value in the 'speeds' Series
        # 'speeds' was created from 'actual_movement_distances[valid_time_mask]' and 'actual_movement_times[valid_time_mask]'
        # So, the times corresponding to 'speeds' are 'actual_movement_times[valid_time_mask]'
        times_corresponding_to_speeds = actual_movement_times[valid_time_mask].reset_index(drop=True)

        # We need the time intervals for the *second* speed onwards for acceleration calculation
        # (i.e., times_corresponding_to_speeds.iloc[1:], aligning with speed_changes.iloc[1:])
        if len(times_corresponding_to_speeds) > 1:
            accel_numerators = speed_changes.iloc[1:].reset_index(drop=True)
            accel_denominators = times_corresponding_to_speeds.iloc[1:].reset_index(drop=True)
            
            # Ensure lengths match for division (they should if logic is correct)
            min_len = min(len(accel_numerators), len(accel_denominators))
            accel_numerators = accel_numerators.iloc[:min_len]
            accel_denominators = accel_denominators.iloc[:min_len]

            valid_accel_denom_mask = accel_denominators > 0
            if valid_accel_denom_mask.any():
                accelerations = accel_numerators[valid_accel_denom_mask] / accel_denominators[valid_accel_denom_mask]
                accelerations.replace([np.inf, -np.inf], np.nan, inplace=True) # Handle potential division by very small numbers

    if not accelerations.empty and accelerations.notna().any():
        features['mean_acceleration'] = accelerations.mean()
        features['std_dev_acceleration'] = accelerations.std() if len(accelerations) >= 2 else 0
        features['max_acceleration'] = accelerations.max() # Max of absolute values might be more informative
                                                          # features['max_abs_acceleration'] = accelerations.abs().max()
    else:
        features['mean_acceleration'] = 0
        features['std_dev_acceleration'] = 0
        features['max_acceleration'] = 0

    # Path Straightness
    if features['total_distance_pixels'] > 0 and len(segment_df) > 0:
        start_x, start_y = segment_df['XPos'].iloc[0], segment_df['YPos'].iloc[0]
        end_x, end_y = segment_df['XPos'].iloc[-1], segment_df['YPos'].iloc[-1]
        straight_line_distance = np.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        features['path_straightness'] = straight_line_distance / features['total_distance_pixels']
    elif features['total_distance_pixels'] == 0 and len(segment_df) > 0 : # No movement
        features['path_straightness'] = 1.0 # A single point or no movement is perfectly "straight"
    else: # Should not happen if segment_df is not empty
        features['path_straightness'] = 0.0


    # State-based Features
    state_counts = Counter(segment_df['State'])
    # Define the states you are tracking from your C++ collector
    tracked_states = ['DM', 'VM', 'HM', 'LD', 'LU', 'RD', 'RU', 'MW']
    for state_val in tracked_states:
        features[f'count_{state_val}'] = state_counts.get(state_val, 0)
        features[f'ratio_{state_val}'] = (state_counts.get(state_val, 0) / features['num_events']) if features['num_events'] > 0 else 0
    
    features['num_clicks'] = features.get('count_LD', 0) + features.get('count_RD', 0) # Total down-clicks

    # Window Title Features
    features['num_unique_window_titles'] = segment_df['WindowTitle'].nunique()
    if not segment_df['WindowTitle'].empty: # Add most common if needed, but it's categorical
         features['most_common_window_title_hash'] = segment_df['WindowTitle'].mode().iloc[0]
    else:
         features['most_common_window_title_hash'] = -1 # Or some other placeholder

    # DayTime Features (example, if you want to use it more directly)
    if not segment_df['DayTime'].empty:
        features['most_common_daytime_bin'] = segment_df['DayTime'].mode().iloc[0]
        features['std_dev_daytime_bin'] = segment_df['DayTime'].std() if len(segment_df['DayTime']) > 1 else 0
    else:
        features['most_common_daytime_bin'] = -1
        features['std_dev_daytime_bin'] = 0


    # Removed avg_left_click_duration and avg_right_click_duration
    # The original calculation was incorrect as segment_df['TimeDiff'] for an 'LD' or 'RD' event
    # is the time *since the previous mouse event*, not the duration of the click itself.
    # Calculating actual click duration requires pairing 'LD' with 'LU' (and 'RD' with 'RU')
    # and summing TimeDiffs between them, which is more complex sequence analysis.

    # Final check for NaNs that might have slipped through (e.g. from .std() on single element after filtering)
    for key, value in features.items():
        if pd.isna(value):
            features[key] = 0.0 # Ensure numeric type for NaNs from numeric calculations
    return features

def main():
    output_feature_file = "features.csv"
    data_files = ["merged_data.csv"]
    segment_length_events = 50
    raw_df = load_data(data_files)

    if raw_df.empty:
        print("No data loaded. Exiting.")
        return

    print(f"Loaded {len(raw_df)} total mouse events.")
    raw_df['TimeDiff'] = pd.to_numeric(raw_df['TimeDiff'], errors='coerce')
    raw_df.dropna(subset=['TimeDiff'], inplace=True)
    segments = segment_data(raw_df, segment_length_events=segment_length_events)
    
    if not segments:
        print("No segments created. Check data or segmentation parameters.")
        return
        
    print(f"Created {len(segments)} segments of (up to) {segment_length_events} events each.")
    all_features_list = []
    for i, segment in enumerate(segments):
        if not segment.empty:
            print(f"Processing segment {i+1} for user {segment['Name'].iloc[0]}:")
            segment_features = calculate_segment_features(segment)
            if segment_features:
                 all_features_list.append(segment_features)
        else:
            print(f"Warning: Segment {i+1} is empty.")


    if not all_features_list:
        print("No features extracted. Exiting.")
        return


    features_df = pd.DataFrame(all_features_list)

    try:
        features_df.to_csv(output_feature_file, index=False)
        print(f"Features successfully saved to '{output_feature_file}'")
    except Exception as e:
        print(f"Error saving features to CSV: {e}")
    
    print("\n--- Features DataFrame ---")
    print(features_df.head())
    print(f"\nShape of features DataFrame: {features_df.shape}")

    # --- Preparing for Machine Learning ---
    if 'user' not in features_df.columns:
        print("Error: 'user' column not found in features_df. Cannot proceed with ML preparation.")
        return

    X = features_df.drop(columns=['user'])
    X = X.select_dtypes(include=np.number)
    y = features_df['user']

    print("\n--- ML Data Preparation ---")
    print("X (features) head:")
    print(X.head(n=10))
    print("\ny (target) head:")
    print(y.head(n=10))

    # Next steps would be:
    # 1. Encode categorical features (e.g., if you keep them)
    from sklearn.preprocessing import LabelEncoder, OneHotEncoder
    # 2. Encode the target variable 'y' (user names) into numerical labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)  # Encode the target variable
    # 3. Split data into training and testing sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    # 4. Scale numerical features
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    # 5. Train a classifier (e.g., RandomForest, SVM, LSTM)
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    main()
