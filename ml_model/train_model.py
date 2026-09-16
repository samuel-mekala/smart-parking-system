"""
Smart Parking Management System - Fast Machine Learning Model Trainer
-----------------------------------------------------------------------
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

def main():
    print("Generating dataset...", flush=True)
    np.random.seed(42)
    start_date = pd.Timestamp("2026-01-01")
    days = 90
    total_hours = days * 24
    timestamps = [start_date + pd.Timedelta(hours=i) for i in range(total_hours)]

    data = []
    total_capacity = 4

    for ts in timestamps:
        hour = ts.hour
        day_of_week = ts.dayofweek
        is_weekend = 1 if day_of_week in [5, 6] else 0
        is_holiday = 1 if (ts.month == 1 and ts.day in [1, 26]) else 0

        base_temp = 24.0 + 5.0 * np.sin((hour - 8) / 12.0 * np.pi)
        temperature_c = round(base_temp + np.random.normal(0, 1.5), 1)
        event_nearby = 1 if np.random.rand() < 0.10 else 0

        if is_weekend:
            peak_factor = np.exp(-((hour - 14) ** 2) / 18.0)
            base_occupancy = 0.30 + 0.55 * peak_factor
        else:
            morning_peak = np.exp(-((hour - 9) ** 2) / 4.0)
            evening_peak = np.exp(-((hour - 18) ** 2) / 6.0)
            midday = np.exp(-((hour - 13) ** 2) / 12.0) * 0.40
            base_occupancy = 0.15 + 0.65 * morning_peak + 0.60 * evening_peak + midday

        if event_nearby:
            base_occupancy += 0.25
        if is_holiday:
            base_occupancy *= 0.60

        base_occupancy += np.random.normal(0, 0.08)
        base_occupancy = float(np.clip(base_occupancy, 0.0, 1.0))

        occupied_slots = int(np.round(base_occupancy * total_capacity))
        occupancy_rate = round((occupied_slots / total_capacity) * 100.0, 1)

        data.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": hour,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
            "temperature_c": temperature_c,
            "event_nearby": event_nearby,
            "total_capacity": total_capacity,
            "occupied_slots": occupied_slots,
            "occupancy_rate": occupancy_rate
        })

    df = pd.DataFrame(data)
    os.makedirs("ml_model", exist_ok=True)
    csv_path = os.path.join("ml_model", "dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"Dataset generated ({len(df)} rows) and saved to {csv_path}", flush=True)

    feature_cols = ["hour", "day_of_week", "is_weekend", "is_holiday", "temperature_c", "event_nearby"]
    X = df[feature_cols]
    y = df["occupancy_rate"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForestRegressor model...", flush=True)
    model = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))

    print(f"MAE: {mae:.2f}%, RMSE: {rmse:.2f}%, R²: {r2:.4f}", flush=True)

    model_path = os.path.join("ml_model", "parking_demand_model.pkl")
    joblib.dump({"model": model, "feature_cols": feature_cols, "metrics": {"mae": mae, "rmse": rmse, "r2": r2}}, model_path)
    print(f"Model successfully saved to {model_path}", flush=True)

if __name__ == "__main__":
    main()
