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
    features = {}

    if segment_df.empty:
        return features

    required_cols = ['XPos', 'YPos', 'TimeDiff', 'State', 'WindowTitle', 'DayTime']
    missing_cols = [col for col in required_cols if col not in segment_df.columns]
    if missing_cols:
        print(f"Warning: Segment missing required columns: {missing_cols}. Skipping feature extraction for this segment.")
        return features

    features['user'] = segment_df['Name'].iloc[0] if 'Name' in segment_df.columns else 'Unknown'
    features['segment_duration_ms'] = segment_df['TimeDiff'].sum()
    features['num_events'] = len(segment_df)
    dx = segment_df['XPos'].diff().fillna(0)
    dy = segment_df['YPos'].diff().fillna(0)
    step_distances_full = np.sqrt(dx**2 + dy**2)
    features['total_distance_pixels'] = step_distances_full.sum()
    
    actual_movement_distances = step_distances_full.iloc[1:].reset_index(drop=True)
    actual_movement_times = segment_df['TimeDiff'].iloc[1:].reset_index(drop=True)

    speeds = pd.Series(dtype=float)
    if not actual_movement_times.empty:
        valid_time_mask = actual_movement_times > 0
        if valid_time_mask.any():
            speeds = actual_movement_distances[valid_time_mask] / actual_movement_times[valid_time_mask]

    if not speeds.empty:
        features['mean_speed'] = speeds.mean()
        features['std_dev_speed'] = speeds.std() if len(speeds) >= 2 else 0
        features['median_speed'] = speeds.median()
        features['skewness_speed'] = skew(speeds) if len(speeds) >= 3 else 0
        features['kurtosis_speed'] = kurtosis(speeds) if len(speeds) >= 4 else 0
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
    
    accelerations = pd.Series(dtype=float)
    if len(speeds) > 1:
        speed_changes = speeds.diff()
        times_corresponding_to_speeds = actual_movement_times[valid_time_mask].reset_index(drop=True)

        if len(times_corresponding_to_speeds) > 1:
            accel_numerators = speed_changes.iloc[1:].reset_index(drop=True)
            accel_denominators = times_corresponding_to_speeds.iloc[1:].reset_index(drop=True)
            min_len = min(len(accel_numerators), len(accel_denominators))
            accel_numerators = accel_numerators.iloc[:min_len]
            accel_denominators = accel_denominators.iloc[:min_len]

            valid_accel_denom_mask = accel_denominators > 0
            if valid_accel_denom_mask.any():
                accelerations = accel_numerators[valid_accel_denom_mask] / accel_denominators[valid_accel_denom_mask]
                accelerations.replace([np.inf, -np.inf], np.nan, inplace=True)

    if not accelerations.empty and accelerations.notna().any():
        features['mean_acceleration'] = accelerations.mean()
        features['std_dev_acceleration'] = accelerations.std() if len(accelerations) >= 2 else 0
        features['max_acceleration'] = accelerations.max()
    else:
        features['mean_acceleration'] = 0
        features['std_dev_acceleration'] = 0
        features['max_acceleration'] = 0

    if features['total_distance_pixels'] > 0 and len(segment_df) > 0:
        start_x, start_y = segment_df['XPos'].iloc[0], segment_df['YPos'].iloc[0]
        end_x, end_y = segment_df['XPos'].iloc[-1], segment_df['YPos'].iloc[-1]
        straight_line_distance = np.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        features['path_straightness'] = straight_line_distance / features['total_distance_pixels']
    elif features['total_distance_pixels'] == 0 and len(segment_df) > 0 :
        features['path_straightness'] = 1.0
    else:
        features['path_straightness'] = 0.0


    state_counts = Counter(segment_df['State'])
    tracked_states = ['DM', 'VM', 'HM', 'LD', 'LU', 'RD', 'RU', 'MW']
    for state_val in tracked_states:
        features[f'count_{state_val}'] = state_counts.get(state_val, 0)
        features[f'ratio_{state_val}'] = (state_counts.get(state_val, 0) / features['num_events']) if features['num_events'] > 0 else 0
    
    features['num_clicks'] = features.get('count_LD', 0) + features.get('count_RD', 0)
    features['num_unique_window_titles'] = segment_df['WindowTitle'].nunique()
    if not segment_df['WindowTitle'].empty:
         features['most_common_window_title_hash'] = segment_df['WindowTitle'].mode().iloc[0]
    else:
         features['most_common_window_title_hash'] = -1

    if not segment_df['DayTime'].empty:
        features['most_common_daytime_bin'] = segment_df['DayTime'].mode().iloc[0]
        features['std_dev_daytime_bin'] = segment_df['DayTime'].std() if len(segment_df['DayTime']) > 1 else 0
    else:
        features['most_common_daytime_bin'] = -1
        features['std_dev_daytime_bin'] = 0

    for key, value in features.items():
        if pd.isna(value):
            features[key] = 0.0
    return features

def main():
    username = "zia"
    output_feature_file = f"processed/{username}.csv"
    data_files = [f"raw/{username}.csv"]
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

if __name__ == "__main__":
    main()
