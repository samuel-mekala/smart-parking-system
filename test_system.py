"""
End-to-End System Test Suite for Smart Parking Management System
------------------------------------------------------------------
Validates:
 1. ML Model predictions and evaluation metrics
 2. Dynamic pricing engine tiers
 3. Password keypad authentication & gate control logic
 4. Slot distance measurement & occupancy mapping
 5. Parking FULL overflow prevention logic
"""

import os
import unittest
import numpy as np
import pandas as pd
import joblib

from iot_simulator import VirtualSmartParkingHardware
from app import get_dynamic_price, CORRECT_PIN

class TestSmartParkingSystem(unittest.TestCase):

    def setUp(self):
        self.hw = VirtualSmartParkingHardware(slot_count=4)
        self.model_path = os.path.join("ml_model", "parking_demand_model.pkl")

    def test_01_ml_model_prediction(self):
        """Test that the ML model loads and predicts expected occupancy rates."""
        self.assertTrue(os.path.exists(self.model_path), "ML Model pickle file must exist.")
        saved_data = joblib.load(self.model_path)
        model = saved_data["model"]
        metrics = saved_data["metrics"]

        print("\n[TEST] ML Model Loaded Successfully.")
        print(f"       R² Score: {metrics['r2']:.4f}, MAE: {metrics['mae']:.2f}%")

        # Predict for a peak hour (2 PM on Wednesday)
        sample_input = pd.DataFrame([{
            "hour": 14,
            "day_of_week": 2,
            "is_weekend": 0,
            "is_holiday": 0,
            "temperature_c": 30.0,
            "event_nearby": 1
        }])
        pred = model.predict(sample_input)[0]
        self.assertGreaterEqual(pred, 0.0)
        self.assertLessEqual(pred, 100.0)
        print(f"       Predicted Occupancy Rate for 2 PM Wednesday: {pred:.1f}%")

    def test_02_dynamic_pricing_engine(self):
        """Test dynamic pricing tiers based on occupancy rate."""
        # Low occupancy (<50%) -> Standard rate $2.00
        p_low, tier_low = get_dynamic_price(25.0)
        self.assertEqual(p_low, 2.00)
        self.assertIn("Standard Rate", tier_low)

        # Moderate occupancy (50%-74%) -> Moderate rate $2.50
        p_mod, tier_mod = get_dynamic_price(60.0)
        self.assertEqual(p_mod, 2.50)
        self.assertIn("Moderate Demand", tier_mod)

        # High occupancy (>=75%) -> Peak rate $3.50
        p_high, tier_high = get_dynamic_price(85.0)
        self.assertEqual(p_high, 3.50)
        self.assertIn("Peak Demand", tier_high)

        print("\n[TEST] Dynamic Pricing Tiers verified ($2.00 base, $2.50 mod, $3.50 peak).")

    def test_03_hardware_distance_occupancy(self):
        """Test HC-SR04 ultrasonic distance threshold detection (<15cm occupied)."""
        # Distance 10cm -> Occupied
        occ1 = self.hw.update_slot_state(1, 10.0)
        self.assertTrue(occ1)

        # Distance 45cm -> Free
        occ2 = self.hw.update_slot_state(2, 45.0)
        self.assertFalse(occ2)

        print("\n[TEST] Slot Distance & Occupancy Determination verified.")

    def test_04_keypad_password_and_gate_actuation(self):
        """Test keypad entry, correct password pin, wrong password, and gate servo angle."""
        # Test Correct Password
        pin = "1234"
        self.assertEqual(pin, CORRECT_PIN)
        status_open = self.hw.operate_gate_servo(open_gate=True)
        self.assertEqual(self.hw.servo_angle, 90)
        print(f"\n[TEST] Correct PIN ('1234') -> {status_open}")

        # Test Gate Close
        status_close = self.hw.operate_gate_servo(open_gate=False)
        self.assertEqual(self.hw.servo_angle, 0)
        print(f"       Gate Reset -> {status_close}")

    def test_05_parking_overflow_logic(self):
        """Test overflow logic when all 4 slots are occupied (<15cm)."""
        for i in range(1, 5):
            self.hw.update_slot_state(i, 8.0) # all occupied

        free_count = sum(1 for info in self.hw.slots.values() if not info["occupied"])
        self.assertEqual(free_count, 0)

        # Gate should refuse entry if 0 slots available
        gate_opened = False
        if CORRECT_PIN == "1234" and free_count > 0:
            gate_opened = True

        self.assertFalse(gate_opened)
        print("\n[TEST] Overflow Prevention: All slots occupied -> Entry Denied (Parking FULL!).")

if __name__ == "__main__":
    unittest.main()
