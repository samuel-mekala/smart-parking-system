"""
Smart Parking Management System - Interactive Web Application & Admin Dashboard
---------------------------------------------------------------------------------
Based on IEEE Paper: "New Parking System: Revolutionizing Parking Management
Through IoT-Enabled Smart Parking Solutions"
Authors: Mekala Samuel (21BCB7145), M. Bhanu Prakash, Shaik Mohammad Mujahiddin, N. Sandeep
VIT-AP University
"""

import os
import time
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import joblib

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Parking System | IoT + ML Dashboard",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS Styling ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #2563EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .slot-box-free {
        background-color: #D1FAE5;
        border: 2px solid #10B981;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .slot-box-occupied {
        background-color: #FEE2E2;
        border: 2px solid #EF4444;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .lcd-display {
        background-color: #1E293B;
        color: #38BDF8;
        font-family: 'Courier New', monospace;
        padding: 15px;
        border-radius: 8px;
        border: 3px solid #0EA5E9;
        font-size: 1.2rem;
        box-shadow: inset 0 0 10px #000000;
    }
    .stButton>button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State Initialization ──────────────────────────────────────────────
if "slots" not in st.session_state:
    st.session_state.slots = {
        1: {"distance_cm": 45, "occupied": False},
        2: {"distance_cm": 10, "occupied": True},
        3: {"distance_cm": 50, "occupied": False},
        4: {"distance_cm": 8,  "occupied": True}
    }

if "gate_state" not in st.session_state:
    st.session_state.gate_state = "CLOSED"  # CLOSED, OPEN

if "pin_input" not in st.session_state:
    st.session_state.pin_input = ""

if "lcd_line1" not in st.session_state:
    st.session_state.lcd_line1 = "Smart Parking"

if "lcd_line2" not in st.session_state:
    st.session_state.lcd_line2 = "System v1.0"

if "pir_motion" not in st.session_state:
    st.session_state.pir_motion = False

if "light_relay" not in st.session_state:
    st.session_state.light_relay = False

if "last_motion_time" not in st.session_state:
    st.session_state.last_motion_time = 0

if "reservations" not in st.session_state:
    st.session_state.reservations = []

# ─── Helper Functions ──────────────────────────────────────────────────────────
CORRECT_PIN = "1234"
OCCUPIED_THRESHOLD_CM = 15.0

def load_ml_model():
    model_path = os.path.join("ml_model", "parking_demand_model.pkl")
    if os.path.exists(model_path):
        try:
            saved_data = joblib.load(model_path)
            return saved_data["model"], saved_data.get("metrics", {})
        except Exception:
            return None, {}
    return None, {}

def get_dynamic_price(occupancy_rate):
    base_rate = 2.00  # $2/hour
    if occupancy_rate >= 75.0:
        multiplier = 1.75  # High demand peak rate
        tier = "Peak Demand (1.75x)"
    elif occupancy_rate >= 50.0:
        multiplier = 1.25  # Moderate demand rate
        tier = "Moderate Demand (1.25x)"
    else:
        multiplier = 1.00  # Normal base rate
        tier = "Standard Rate (1.00x)"
    
    current_price = round(base_rate * multiplier, 2)
    return current_price, tier

# ─── Sidebar Navigation ────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/000000/parking.png", width=70)
st.sidebar.title("Smart Parking System")
st.sidebar.caption("IoT & ML Parking Solution · VIT-AP")

navigation = st.sidebar.radio(
    "Select Mode",
    ["🚗 Driver Portal & Gate Simulator", "📊 Admin Dashboard", "🧠 ML Demand Prediction", "⚡ IoT Hardware Control"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Authors & Paper")
st.sidebar.markdown("""
- **Mekala Samuel** (21BCB7145)
- Shaik Mohammad Mujahiddin
- M. Bhanu Prakash
- N. Sandeep

*Published Research Project*
""")

# ─── Header Section ────────────────────────────────────────────────────────────
st.markdown("<div class='main-header'>🅿️ Smart Parking Management System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>IoT-Enabled Real-Time Slot Detection, Password Gate, Motion Lighting & ML Dynamic Pricing</div>", unsafe_allow_html=True)

# Update slot occupancy based on distance threshold
for slot_id, info in st.session_state.slots.items():
    info["occupied"] = info["distance_cm"] < OCCUPIED_THRESHOLD_CM

free_slots = sum(1 for info in st.session_state.slots.values() if not info["occupied"])
total_slots = len(st.session_state.slots)
occupancy_rate = ((total_slots - free_slots) / total_slots) * 100.0
current_price, price_tier = get_dynamic_price(occupancy_rate)

# Update default LCD lines if in normal state
if st.session_state.lcd_line1 == "Smart Parking" and st.session_state.lcd_line2 == "System v1.0":
    st.session_state.lcd_line1 = f"Free: {free_slots}/{total_slots} Slots"
    slot_map_str = " ".join([f"{s}:{'X' if st.session_state.slots[s]['occupied'] else 'O'}" for s in range(1, 5)])
    st.session_state.lcd_line2 = slot_map_str

# ─── MODE 1: DRIVER PORTAL & GATE SIMULATOR ────────────────────────────────────
if navigation == "🚗 Driver Portal & Gate Simulator":
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("🅿️ Live Parking Slot Status")
        slot_cols = st.columns(4)
        for idx, (slot_id, info) in enumerate(st.session_state.slots.items()):
            with slot_cols[idx]:
                if info["occupied"]:
                    st.markdown(f"""
                    <div class='slot-box-occupied'>
                        <h3>Slot {slot_id}</h3>
                        <p>🔴 <b>OCCUPIED</b></p>
                        <p><small>Distance: {info['distance_cm']} cm</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='slot-box-free'>
                        <h3>Slot {slot_id}</h3>
                        <p>🟢 <b>FREE</b></p>
                        <p><small>Distance: {info['distance_cm']} cm</small></p>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Available Slots", f"{free_slots} / {total_slots}")
        m_col2.metric("Occupancy Rate", f"{occupancy_rate:.0f}%")
        m_col3.metric("Current Rate", f"${current_price:.2f}/hr", delta=price_tier)

        st.markdown("---")
        st.subheader("📝 Reserve a Parking Slot & Pay")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            driver_name = st.text_input("Driver Name", "Samuel Mekala")
            vehicle_no = st.text_input("Vehicle Registration No.", "AP-39-CB-7145")
            selected_slot = st.selectbox("Select Available Slot", [s for s, info in st.session_state.slots.items() if not info["occupied"]] or ["No Free Slots Available"])
        with res_col2:
            duration_hrs = st.slider("Parking Duration (Hours)", 1, 12, 2)
            total_fee = duration_hrs * current_price
            st.markdown(f"### Total Parking Fee: **${total_fee:.2f}**")
            payment_method = st.selectbox("Payment Channel", ["Credit/Debit Card", "UPI / Mobile Wallet", "RFID / Fastag"])

        if st.button("💳 Confirm Reservation & Pay Now", use_container_width=True):
            if selected_slot == "No Free Slots Available":
                st.error("Cannot reserve: Parking lot is full!")
            else:
                new_res = {
                    "res_id": f"RES-{int(time.time())}",
                    "driver": driver_name,
                    "vehicle": vehicle_no,
                    "slot": selected_slot,
                    "duration": f"{duration_hrs} hrs",
                    "fee": f"${total_fee:.2f}",
                    "payment": payment_method,
                    "status": "Confirmed",
                    "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.reservations.append(new_res)
                st.success(f"✅ Reservation Confirmed! Slot {selected_slot} assigned to {vehicle_no}. Entry Code: {CORRECT_PIN}")

    with col2:
        st.subheader("🔐 Password-Protected Gate Entry (Hardware Keypad Simulator)")
        
        # LCD Display Box
        st.markdown(f"""
        <div class='lcd-display'>
            <div>📟 <b>16x2 LCD MONITOR</b></div>
            <div style="color: #FACC15; font-size: 1.4rem;">{st.session_state.lcd_line1}</div>
            <div style="color: #38BDF8; font-size: 1.2rem;">{st.session_state.lcd_line2}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"**Gate Barrier Status:** `{st.session_state.gate_state}` " + ("🚪 OPEN" if st.session_state.gate_state == "OPEN" else "🚧 CLOSED"))
        st.markdown(f"**PIN Entered:** `{'*' * len(st.session_state.pin_input)}`")

        # 4x4 Keypad Buttons Grid
        keypad_grid = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["*", "0", "#"]
        ]

        for row in keypad_grid:
            btn_cols = st.columns(3)
            for i, key in enumerate(row):
                with btn_cols[i]:
                    if st.button(key, key=f"btn_{key}", use_container_width=True):
                        if key == '#':
                            # Verify Password
                            if st.session_state.pin_input == CORRECT_PIN:
                                if free_slots > 0:
                                    st.session_state.gate_state = "OPEN"
                                    st.session_state.lcd_line1 = "Access Granted!"
                                    st.session_state.lcd_line2 = "Gate: OPEN (5s)"
                                    st.balloons()
                                else:
                                    st.session_state.gate_state = "CLOSED"
                                    st.session_state.lcd_line1 = "Parking FULL!"
                                    st.session_state.lcd_line2 = "No slots free."
                            else:
                                st.session_state.gate_state = "CLOSED"
                                st.session_state.lcd_line1 = "Wrong Password!"
                                st.session_state.lcd_line2 = "Try again."
                            st.session_state.pin_input = ""

                        elif key == '*':
                            # Clear PIN
                            st.session_state.pin_input = ""
                            st.session_state.lcd_line1 = "Enter Password:"
                            st.session_state.lcd_line2 = "                "
                        else:
                            st.session_state.pin_input += key
                            st.session_state.lcd_line1 = "Enter Password:"
                            st.session_state.lcd_line2 = "*" * len(st.session_state.pin_input)
                        st.rerun()

        st.caption("Press `#` to Submit PIN (`1234`), press `*` to Clear.")

# ─── MODE 2: ADMIN DASHBOARD ──────────────────────────────────────────────────
elif navigation == "📊 Admin Dashboard":
    st.subheader("📊 Centralized Facility Management & Analytics")

    # Overview Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Capacity", f"{total_slots} Slots")
    c2.metric("Occupied Slots", f"{total_slots - free_slots}")
    c3.metric("Free Slots", f"{free_slots}")
    c4.metric("Estimated Daily Revenue", f"${len(st.session_state.reservations) * 5.00 + 42.00:.2f}")

    st.markdown("---")
    ad_col1, ad_col2 = st.columns([1.3, 1])

    with ad_col1:
        st.markdown("### 📈 Live Occupancy Gauges & Distribution")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=occupancy_rate,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Parking Occupancy (%)", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#2563EB"},
                'steps': [
                    {'range': [0, 50], 'color': "#D1FAE5"},
                    {'range': [50, 75], 'color': "#FEF3C7"},
                    {'range': [75, 100], 'color': "#FEE2E2"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with ad_col2:
        st.markdown("### 🏷️ Dynamic Pricing Configuration")
        st.info(f"**Current Dynamic Tier:** {price_tier}")
        st.write(f"- Base Rate: **$2.00/hr**")
        st.write(f"- Low Demand (<50%): **$2.00/hr**")
        st.write(f"- Moderate Demand (50-75%): **$2.50/hr**")
        st.write(f"- High Demand (>75%): **$3.50/hr**")
        st.markdown("---")
        st.markdown("### 💡 Motion-Activated Energy System")
        st.write(f"- PIR Motion Sensor: `{ 'DETECTED' if st.session_state.pir_motion else 'IDLE' }`")
        st.write(f"- Area Light Relay: `{ 'ON (30s Timer Active)' if st.session_state.light_relay else 'OFF (Energy Saving)' }`")

    st.markdown("---")
    st.markdown("### 📋 Recent Reservations & Access Logs")
    if st.session_state.reservations:
        df_res = pd.DataFrame(st.session_state.reservations)
        st.dataframe(df_res, use_container_width=True)
    else:
        st.write("No active driver reservations yet.")

# ─── MODE 3: ML DEMAND PREDICTION ─────────────────────────────────────────────
elif navigation == "🧠 ML Demand Prediction":
    st.subheader("🧠 Machine Learning Parking Demand Forecasting & Analytics")
    model, metrics = load_ml_model()

    if metrics:
        m1, m2, m3 = st.columns(3)
        m1.metric("Model Algorithm", "Random Forest Regressor")
        m2.metric("Mean Absolute Error (MAE)", f"{metrics.get('mae', 0):.2f}%")
        m3.metric("R² Score Accuracy", f"{metrics.get('r2', 0):.4f}")
        st.markdown("---")

    p_col1, p_col2 = st.columns([1, 1.2])

    with p_col1:
        st.markdown("### 🔮 Predict Occupancy Rate")
        pred_hour = st.slider("Hour of Day (0-23)", 0, 23, 14)
        pred_day = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=2)
        pred_temp = st.slider("Temperature (°C)", 15.0, 42.0, 28.0)
        pred_event = st.checkbox("Special Event Nearby?", value=False)
        pred_holiday = st.checkbox("Public Holiday?", value=False)

        day_idx = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(pred_day)
        is_weekend = 1 if day_idx in [5, 6] else 0

        # Run Prediction
        input_data = pd.DataFrame([{
            "hour": pred_hour,
            "day_of_week": day_idx,
            "is_weekend": is_weekend,
            "is_holiday": 1 if pred_holiday else 0,
            "temperature_c": pred_temp,
            "event_nearby": 1 if pred_event else 0
        }])

        if model is not None:
            predicted_occupancy = model.predict(input_data)[0]
        else:
            # Fallback heuristic calculation if model pickle not loaded yet
            predicted_occupancy = 45.0 + (pred_hour - 12) ** 2 * (-0.3) + (20 if pred_event else 0)
        
        predicted_occupancy = float(np.clip(predicted_occupancy, 0.0, 100.0))
        predicted_slots = int(np.round((predicted_occupancy / 100.0) * total_slots))
        rec_price, rec_tier = get_dynamic_price(predicted_occupancy)

        st.markdown(f"### Expected Occupancy: **{predicted_occupancy:.1f}%** (~{predicted_slots}/{total_slots} Slots)")
        st.markdown(f"### Recommended Dynamic Price: **${rec_price:.2f}/hr**")

    with p_col2:
        st.markdown("### 📊 24-Hour Predicted Demand Curve")
        hours_range = list(range(24))
        forecast_rates = []

        for h in hours_range:
            row = pd.DataFrame([{
                "hour": h,
                "day_of_week": day_idx,
                "is_weekend": is_weekend,
                "is_holiday": 1 if pred_holiday else 0,
                "temperature_c": pred_temp,
                "event_nearby": 1 if pred_event else 0
            }])
            if model is not None:
                val = model.predict(row)[0]
            else:
                val = 30 + 50 * np.exp(-((h - 14)**2)/18.0) if is_weekend else 20 + 60 * np.exp(-((h - 9)**2)/4.0) + 55 * np.exp(-((h - 18)**2)/6.0)
            forecast_rates.append(np.clip(val, 0.0, 100.0))

        df_forecast = pd.DataFrame({"Hour": hours_range, "Predicted Occupancy (%)": forecast_rates})
        fig_curve = px.line(df_forecast, x="Hour", y="Predicted Occupancy (%)", markers=True,
                            title=f"24-Hour Demand Forecast ({pred_day})")
        fig_curve.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="Peak Threshold (75%)")
        fig_curve.update_layout(height=350)
        st.plotly_chart(fig_curve, use_container_width=True)

# ─── MODE 4: IOT HARDWARE CONTROL & SIMULATOR ─────────────────────────────────
elif navigation == "⚡ IoT Hardware Control":
    st.subheader("⚡ Hardware Sensor & Actuator Simulator")
    st.write("Adjust sensor inputs to test physical hardware logic in real-time.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📡 HC-SR04 Ultrasonic Distance Sensors")
        for slot_id in range(1, 5):
            curr_dist = st.session_state.slots[slot_id]["distance_cm"]
            new_dist = st.slider(f"Slot {slot_id} Distance (cm)", 2, 80, curr_dist, key=f"dist_slider_{slot_id}")
            st.session_state.slots[slot_id]["distance_cm"] = new_dist
            st.session_state.slots[slot_id]["occupied"] = new_dist < OCCUPIED_THRESHOLD_CM

    with col2:
        st.markdown("### 🚶 PIR Motion & Lighting Relay Control")
        motion_toggle = st.checkbox("Trigger PIR Motion Sensor", value=st.session_state.pir_motion)
        if motion_toggle != st.session_state.pir_motion:
            st.session_state.pir_motion = motion_toggle
            if motion_toggle:
                st.session_state.light_relay = True
                st.session_state.last_motion_time = time.time()
                st.success(" Motion detected! Area lights switched ON.")
            else:
                st.session_state.light_relay = False
                st.info("Motion stopped. Area lights will turn OFF after 30s timeout.")

        st.markdown("---")
        st.markdown("### 🚪 SG90 Servo Gate Actuator")
        st.write(f"Current Servo Angle: **{90 if st.session_state.gate_state == 'OPEN' else 0}°** ({st.session_state.gate_state})")
        c1, c2 = st.columns(2)
        if c1.button("Open Gate (90°)", use_container_width=True):
            st.session_state.gate_state = "OPEN"
            st.rerun()
        if c2.button("Close Gate (0°)", use_container_width=True):
            st.session_state.gate_state = "CLOSED"
            st.rerun()
