# 🅿️ Smart Parking Management System (IoT + ML + Web App)

> **IoT & Machine Learning Project** · VIT-AP University  
> **Authors:** **Mekala Samuel (21BCB7145)** · M. Bhanu Prakash (21BCB7050) · Shaik Mohammad Mujahiddin (21BCB7101) · N. Sandeep (21BCB7166)  
> **Paper:** *"New Parking System: Revolutionizing Parking Management Through IoT-Enabled Smart Parking Solutions"*

🌐 **Live Online Web Application:** **[https://smart-parking-system-sps.streamlit.app/](https://smart-parking-system-sps.streamlit.app/)**  
📂 **GitHub Repository:** **[https://github.com/samuel-mekala/smart-parking-system](https://github.com/samuel-mekala/smart-parking-system)**

---

## 📌 Overview

Urban traffic congestion and inefficient parking management result in wasted time, excess fuel consumption, and higher carbon emissions. This repository presents an **IoT-enabled and Machine Learning-powered Smart Parking System**.

### 🌟 Key Capabilities & Requirements Implemented:
1. 🔍 **Real-Time Slot Detection & Occupancy Map**: HC-SR04 ultrasonic distance sensors continuously monitor parking slots (<15cm = occupied).
2. 🔐 **Password-Protected Gate Access**: 4×4 keypad PIN entry (`1234`) actuates the SG90 servo motor barrier.
3. 🚫 **Overflow Prevention**: When capacity is reached, gate entry is blocked with a `"Parking FULL!"` LCD alert.
4. 💡 **Motion-Activated Lighting**: PIR sensor triggers parking area relay with 30-second energy-saving timeout.
5. 🏷️ **Dynamic Pricing Engine**: Automated pricing tiers ($2.00 base, $2.50 moderate, $3.50 peak) based on live occupancy rate.
6. 🧠 **ML Demand Forecasting**: `RandomForestRegressor` trained on historical occupancy, temporal, and weather data to forecast 24-hour peak demand.
7. 🚗 **Driver Web Portal & Admin Dashboard**: Interactive web app built in Streamlit & Plotly featuring slot reservations, simulated cashless payment, keypad simulator, live occupancy gauges, and demand charts.

---

## 🌐 Live Online Deployment

The project is deployed online and accessible globally:
👉 **[https://smart-parking-system-sps.streamlit.app/](https://smart-parking-system-sps.streamlit.app/)**

---

## 🏗️ System Architecture

```
smart-parking-system/
├── app.py                      # Full-stack Streamlit Web Application & Admin Dashboard
├── ml_model/
│   ├── train_model.py          # Synthetic dataset generator & ML model trainer
│   ├── dataset.csv             # 90-day hourly parking occupancy dataset
│   └── parking_demand_model.pkl# Saved RandomForest ML model artifact
├── iot_simulator.py            # Virtual hardware sensor simulator
├── test_system.py              # Unit & integration test suite
├── run_full_e2e_test.py        # Comprehensive end-to-end test runner
├── smart parking system.ino    # Arduino C sketch for hardware deployment
├── requirements.txt            # Python dependencies
├── Procfile                    # Web deployment startup configuration
├── render.yaml                 # Render cloud hosting deployment configuration
├── .streamlit/config.toml      # Web app theme settings
└── README.md
```

---

## 🚀 Quick Start & Local Execution

### 1. Clone the Repository
```bash
git clone https://github.com/samuel-mekala/smart-parking-system.git
cd smart-parking-system
```

### 2. Set Up Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Train the Machine Learning Model
```bash
python ml_model/train_model.py
```
*Output: Generates `ml_model/dataset.csv` and saves `ml_model/parking_demand_model.pkl` ($R^2 \approx 0.78$, MAE $\approx 10.0\%$).*

### 4. Run Automated End-to-End Test Suite
```bash
python run_full_e2e_test.py
```

### 5. Launch Local Web Application
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`** (or **`http://localhost:8505`**).

---

## 📊 Web Application Features

### 1. 🚗 Driver Portal & Gate Simulator
- **Live Slot Grid**: Real-time status of Slots 1 to 4 with distance readouts.
- **Hardware Keypad Simulator**: Enter PIN `1234` on 4×4 keypad to trigger servo gate opening (`Access Granted!`). Test wrong PIN (`Wrong Password!`) and overflow (`Parking FULL!`).
- **Slot Reservation & Cashless Payment**: Select free slot, set duration, view total dynamic fee, and confirm simulated payment.

### 2. 📊 Admin Dashboard
- **Live Occupancy Gauge**: Visual dial displaying parking utilization %.
- **Dynamic Pricing Controls**: Real-time rate calculation based on demand intensity.
- **PIR Lighting Status**: Motion state and 30s auto-off relay status.

### 3. 🧠 ML Demand Prediction
- **Interactive Predictor**: Set Hour of Day, Day of Week, Temperature, and Special Event flags to predict occupancy rate.
- **24-Hour Forecast Curve**: Plotly interactive graph displaying predicted demand for the next 24 hours.

---

## 🛠️ Arduino Hardware Setup (`smart parking system.ino`)

| Component | Pin Connection (Arduino Uno) |
|---|---|
| 16×2 LCD | RS=12, E=11, D4=5, D5=4, D6=3, D7=2 |
| SG90 Servo Gate | Signal Pin 9 |
| Ultrasonic Slot 1 | TRIG = A0, ECHO = A1 |
| Ultrasonic Slot 2 | TRIG = A2, ECHO = A3 |
| Ultrasonic Slot 3 | TRIG = A4, ECHO = A5 |
| Ultrasonic Slot 4 | TRIG = Pin 6, ECHO = Pin 7 |
| PIR Motion Sensor | Pin 10 |
| Slot LEDs | Pin 13, Pin 8 |

---

*VIT-AP University · Department of Computer Science & Engineering*
