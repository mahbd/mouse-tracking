import customtkinter as ctk
import pandas as pd
import numpy as np
import joblib
from scipy.stats import skew, kurtosis
from collections import Counter
import subprocess
import sys
import os
import threading
import queue

# --- Configuration ---
USERNAME = "zia"
BATCH_SIZE = 2000
SEGMENT_LENGTH_EVENTS = 50
CPP_EXECUTABLE_NAME = "mouse_logger.exe"

# ====================================================================================
# SCRIPT 1: DATA SEGMENTATION AND FEATURE EXTRACTION (Corrected)
# ====================================================================================


def _process_chunk_by_events(chunk_rows, segment_length, all_segments_list):
    if not chunk_rows:
        return
    chunk_df = pd.DataFrame(list(chunk_rows))
    if chunk_df.empty:
        return
    for i in range(0, len(chunk_df), segment_length):
        sub_segment_df = chunk_df.iloc[i : i + segment_length]
        all_segments_list.append(sub_segment_df)


def segment_data(
    df,
    segment_length_events=50,
    large_time_diff_threshold=10000,
    user_col="Name",
    time_col="TimeDiff",
):
    all_segments = []
    if df.empty:
        return all_segments
    for _, group in df.groupby(user_col):
        current_chunk_rows = []
        if group.empty:
            continue
        for _, row_series in group.iterrows():
            if current_chunk_rows and row_series[time_col] > large_time_diff_threshold:
                _process_chunk_by_events(
                    current_chunk_rows, segment_length_events, all_segments
                )
                current_chunk_rows = []
            current_chunk_rows.append(row_series.to_dict())
        if current_chunk_rows:
            _process_chunk_by_events(
                current_chunk_rows, segment_length_events, all_segments
            )
    return all_segments


def calculate_segment_features(segment_df):
    features = {}
    if segment_df.empty:
        return features
    segment_df["Name"] = USERNAME
    required_cols = ["XPos", "YPos", "TimeDiff", "State", "WindowTitle", "DayTime"]
    if any(col not in segment_df.columns for col in required_cols):
        return features

    features["user"] = USERNAME
    features["segment_duration_ms"] = segment_df["TimeDiff"].sum()
    features["num_events"] = len(segment_df)
    dx = segment_df["XPos"].diff().fillna(0)
    dy = segment_df["YPos"].diff().fillna(0)
    step_distances = np.sqrt(dx**2 + dy**2)
    features["total_distance_pixels"] = step_distances.sum()
    actual_movement_times = segment_df["TimeDiff"].iloc[1:]
    valid_time_mask = actual_movement_times > 0
    speeds = (
        step_distances.iloc[1:][valid_time_mask]
        / actual_movement_times[valid_time_mask]
    )

    if not speeds.empty:
        features.update(
            {
                "mean_speed": speeds.mean(),
                "std_dev_speed": speeds.std(ddof=0),
                "median_speed": speeds.median(),
                "skewness_speed": skew(speeds),
                "kurtosis_speed": kurtosis(speeds),
                "max_speed": speeds.max(),
                "min_speed": speeds.min(),
            }
        )
    else:
        features.update(
            {
                k: 0
                for k in [
                    "mean_speed",
                    "std_dev_speed",
                    "median_speed",
                    "skewness_speed",
                    "kurtosis_speed",
                    "max_speed",
                    "min_speed",
                ]
            }
        )

    features.update(
        {
            k: 0
            for k in ["mean_acceleration", "std_dev_acceleration", "max_acceleration"]
        }
    )

    if features["total_distance_pixels"] > 0:
        start_pos = segment_df[["XPos", "YPos"]].iloc[0]
        end_pos = segment_df[["XPos", "YPos"]].iloc[-1]
        # *** THIS IS THE CORRECTED LINE ***
        features["path_straightness"] = (
            np.linalg.norm(end_pos.values - start_pos.values)
            / features["total_distance_pixels"]
        )
    else:
        features["path_straightness"] = 1.0

    state_counts = Counter(segment_df["State"])
    tracked_states = ["DM", "VM", "HM", "LD", "LU", "RD", "RU", "MW"]
    for state in tracked_states:
        features[f"count_{state}"] = state_counts.get(state, 0)
        features[f"ratio_{state}"] = features[f"count_{state}"] / features["num_events"]

    features.update(
        {
            "num_clicks": features["count_LD"] + features["count_RD"],
            "num_unique_window_titles": segment_df["WindowTitle"].nunique(),
            "most_common_window_title_hash": segment_df["WindowTitle"].mode().iloc[0],
            "most_common_daytime_bin": segment_df["DayTime"].mode().iloc[0],
            "std_dev_daytime_bin": segment_df["DayTime"].std(ddof=0),
        }
    )
    return {k: 0.0 if pd.isna(v) else v for k, v in features.items()}


# ====================================================================================
# SCRIPT 2: PREDICTION LOGIC
# ====================================================================================

TRAINING_FEATURES = [
    "segment_duration_ms",
    "total_distance_pixels",
    "mean_speed",
    "std_dev_speed",
    "median_speed",
    "skewness_speed",
    "kurtosis_speed",
    "max_speed",
    "min_speed",
    "mean_acceleration",
    "std_dev_acceleration",
    "max_acceleration",
    "path_straightness",
    "ratio_DM",
    "ratio_VM",
    "ratio_HM",
]

# ====================================================================================
# Main Application GUI
# ====================================================================================


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.monitoring_process = None
        self.data_queue = queue.Queue()
        self.data_buffer = []
        self.total_batches_processed = 0
        self.total_anomalies_found = 0
        self.is_processing = False
        self.model, self.scaler = None, None
        self.load_ml_assets()
        self.title("Batch Anomaly Detection")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.start_button = ctk.CTkButton(
            control_frame, text="Start Monitoring", command=self.start_monitoring
        )
        self.start_button.pack(side="left", padx=10, pady=5)
        self.stop_button = ctk.CTkButton(
            control_frame,
            text="Stop Monitoring",
            state="disabled",
            command=self.stop_monitoring,
        )
        self.stop_button.pack(side="left", padx=10, pady=5)
        self.buffer_label = ctk.CTkLabel(
            control_frame, text=f"Buffer: 0 / {BATCH_SIZE}"
        )
        self.buffer_label.pack(side="right", padx=10)
        status_frame = ctk.CTkFrame(self)
        status_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.status_label = ctk.CTkLabel(
            status_frame, text="Status: Stopped. Model loaded."
        )
        if self.model is None:
            self.status_label.configure(
                text="Status: Stopped. ERROR: Model/Scaler not found!", text_color="red"
            )
        self.status_label.pack(side="left", padx=10)
        self.batch_summary_label = ctk.CTkLabel(
            status_frame, text="Total Batches: 0 | Total Anomalies: 0"
        )
        self.batch_summary_label.pack(side="right", padx=10)
        self.results_box = ctk.CTkTextbox(self, wrap="none")
        self.results_box.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.results_box.insert("0.0", "Batch processing results will appear here.")
        self.results_box.configure(state="disabled")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_ml_assets(self):
        try:
            self.model = joblib.load(f"{USERNAME}_anomaly_model.joblib")
            self.scaler = joblib.load(f"{USERNAME}_scaler.joblib")
            print("Successfully loaded model and scaler.")
        except Exception as e:
            print(f"ERROR loading model assets: {e}")

    def start_monitoring(self):
        if self.model is None or self.monitoring_process:
            return
        try:
            self.monitoring_process = subprocess.Popen(
                [os.path.join(os.path.abspath("."), CPP_EXECUTABLE_NAME)],
                stdout=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            threading.Thread(target=self.read_output, daemon=True).start()
            self.process_queue()
            self.status_label.configure(
                text="Status: Monitoring...", text_color="green"
            )
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color="red")

    def read_output(self):
        for line in iter(self.monitoring_process.stdout.readline, ""):
            self.data_queue.put(line)

    def process_queue(self):
        if self.is_processing:
            self.after(100, self.process_queue)
            return
        try:
            while not self.data_queue.empty():
                line = self.data_queue.get_nowait().strip()
                if not line:
                    continue
                try:
                    parts = line.split(",")
                    if len(parts) == 6:
                        # Robustly convert parts to correct data types
                        event = {
                            "WindowTitle": int(parts[0]),
                            "State": parts[1],
                            "TimeDiff": int(parts[2]),
                            "DayTime": int(parts[3]),
                            "XPos": int(parts[4]),
                            "YPos": int(parts[5]),
                        }
                        self.data_buffer.append(event)
                except (ValueError, IndexError):
                    print(f"Skipping malformed data line: {line}")
                    continue
            self.buffer_label.configure(
                text=f"Buffer: {len(self.data_buffer)} / {BATCH_SIZE}"
            )
            if len(self.data_buffer) >= BATCH_SIZE:
                self.is_processing = True
                self.status_label.configure(
                    text="Status: Processing batch...", text_color="orange"
                )
                threading.Thread(target=self.process_batch, daemon=True).start()
        finally:
            self.after(100, self.process_queue)

    def process_batch(self):
        batch_data = self.data_buffer[:BATCH_SIZE]
        self.data_buffer = self.data_buffer[BATCH_SIZE:]
        batch_df = pd.DataFrame(batch_data)
        batch_df["Name"] = USERNAME
        segments = segment_data(batch_df, segment_length_events=SEGMENT_LENGTH_EVENTS)
        batch_anomalies = 0
        for segment_df in segments:
            features = calculate_segment_features(segment_df)
            if not features:
                continue
            feature_vector_df = pd.DataFrame([features])
            X = feature_vector_df[TRAINING_FEATURES]
            X_scaled = self.scaler.transform(X)
            anomaly_score = self.model.decision_function(X_scaled)[0]
            if anomaly_score >= 0:
                batch_anomalies += 1
        self.update_gui_with_batch_results(len(segments), batch_anomalies)
        self.is_processing = False

    def update_gui_with_batch_results(self, num_segments, num_anomalies):
        self.total_batches_processed += 1
        self.total_anomalies_found += num_anomalies
        log_message = f"Batch {self.total_batches_processed} Processed:\n  - Segments created: {num_segments}\n  - Anomalies detected: {num_anomalies}\n\n"
        self.results_box.configure(state="normal")
        self.results_box.insert("0.0", log_message)
        self.results_box.configure(state="disabled")
        self.batch_summary_label.configure(
            text=f"Total Batches: {self.total_batches_processed} | Total Anomalies: {self.total_anomalies_found}"
        )
        self.status_label.configure(text="Status: Monitoring...", text_color="green")

    def stop_monitoring(self):
        if self.monitoring_process:
            self.monitoring_process.terminate()
        self.monitoring_process = None
        self.status_label.configure(text="Status: Stopped", text_color="white")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def on_closing(self):
        self.stop_monitoring()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
