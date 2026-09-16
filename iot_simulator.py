"""
Smart Parking System - Virtual IoT Hardware Simulator
------------------------------------------------------
Simulates hardware sensor readings (HC-SR04 ultrasonic distance sensors,
PIR motion detection, SG90 Servo motor, and Keypad PIN entries) for testing
the system without needing physical microcontrollers connected.
"""

import time
import random

class VirtualSmartParkingHardware:
    def __init__(self, slot_count=4):
        self.slot_count = slot_count
        self.servo_angle = 0  # 0 = closed, 90 = open
        self.pir_motion = False
        self.light_relay = False
        self.last_motion_timestamp = 0
        self.slots = {i: {"distance_cm": 50, "occupied": False} for i in range(1, slot_count + 1)}

    def read_ultrasonic_distance(self, slot_id):
        """Simulates distance measurement in cm from HC-SR04 sensor."""
        if slot_id in self.slots:
            return self.slots[slot_id]["distance_cm"]
        return 999

    def update_slot_state(self, slot_id, distance_cm):
        """Updates slot distance and occupancy determination."""
        occupied = distance_cm < 15.0
        self.slots[slot_id] = {
            "distance_cm": distance_cm,
            "occupied": occupied
        }
        return occupied

    def trigger_pir_motion(self, detected=True):
        """Simulates PIR motion sensor triggering light relay."""
        self.pir_motion = detected
        if detected:
            self.light_relay = True
            self.last_motion_timestamp = time.time()
        return self.light_relay

    def check_light_timeout(self, timeout_seconds=30):
        """Auto-turns off lighting relay if motion timeout exceeded."""
        if self.light_relay and (time.time() - self.last_motion_timestamp) >= timeout_seconds:
            self.light_relay = False
            self.pir_motion = False
        return self.light_relay

    def operate_gate_servo(self, open_gate=True):
        """Simulates SG90 Servo gate movement."""
        if open_gate:
            self.servo_angle = 90
            status = "Gate Opened (90 degrees)"
        else:
            self.servo_angle = 0
            status = "Gate Closed (0 degrees)"
        return status

if __name__ == "__main__":
    hw = VirtualSmartParkingHardware()
    print("Virtual Smart Parking Hardware Initialized.")
    print("Slot 1 distance:", hw.read_ultrasonic_distance(1), "cm")
    hw.update_slot_state(1, 10)  # Park car in slot 1
    print("Slot 1 occupied after car parked:", hw.slots[1]["occupied"])
    print(hw.operate_gate_servo(True))
