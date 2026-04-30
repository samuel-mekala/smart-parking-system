# 🅿️ Smart Parking System

> **IoT Project** · VIT-AP University  
> **Team:** **Mekala Samuel (21BCB7145)** · M. Bhanu Prakash (21BCB7050) · Shaik Mohammad Mujahiddin (21BCB7101) · N. Sandeep (21BCB7166)

-----

## 📌 Overview

Finding a parking spot wastes time, fuel, and increases urban congestion. This project builds an **IoT-enabled smart parking management system** that monitors real-time slot availability, controls gate access with password protection, and reduces energy consumption with motion-activated lighting.

-----

## ✨ Features

- 🔍 **Real-time slot detection** — HC-SR04 ultrasonic sensors monitor 4 parking slots continuously
- 🔐 **Password-protected gate** — 4×4 keypad entry controls a servo motor barrier
- 💡 **Motion-activated lighting** — PIR sensor auto-turns lights on/off with 30s timeout
- 📟 **LCD status display** — shows free slot count and per-slot occupancy map live
- 🚫 **Overflow prevention** — gate stays closed and shows “Parking FULL!” when all slots are taken
- 🔴 **Per-slot LEDs** — LED ON = occupied, OFF = free

-----

## 🔧 Hardware Components

|Component                          |Purpose                                     |
|-----------------------------------|--------------------------------------------|
|**Arduino Uno**                    |Main microcontroller                        |
|**HC-SR04 Ultrasonic Sensors (×4)**|Detect whether each parking slot is occupied|
|**Servo Motor (SG90)**             |Controls the entry gate                     |
|**4×4 Keypad**                     |Password input for gate access              |
|**16×2 LCD Display**               |Shows real-time slot availability           |
|**PIR Motion Sensor**              |Triggers automatic parking area lighting    |
|**LEDs (×4)**                      |Per-slot occupancy indicators               |
|**Light Relay Module**             |Switches parking lights via PIR             |
|**Power Supply**                   |5V regulated supply                         |

-----

## 💻 Software

|Component    |Details                                   |
|-------------|------------------------------------------|
|**IDE**      |Arduino IDE                               |
|**Language** |C (Arduino / ATmega328)                   |
|**Libraries**|`LiquidCrystal.h` · `Servo.h` · `Keypad.h`|

-----

## ⚙️ How It Works

```
System Boot → LCD shows "Smart Parking System v1.0"
        ↓
Continuous Loop:
  → Ultrasonic sensors measure distance to each slot
  → Slot LED: ON (occupied) / OFF (free)
  → LCD: "Free: X/4" + slot map (1:O=open, 1:X=taken)
  → PIR detects motion → lights ON (auto-off after 30s)
        ↓
User approaches keypad:
  → Type password digits → press # to confirm
  → Correct + free slot available → Gate opens (5s) → closes
  → Wrong password          → LCD: "Wrong Password!"
  → All slots full           → LCD: "Parking FULL!"
  → Press * to clear input
```

-----

## 🛠️ Tech Stack

![C](https://img.shields.io/badge/C-00599C?style=flat-square&logo=c&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white)
![IoT](https://img.shields.io/badge/IoT-Embedded-green?style=flat-square)

-----

## 📁 Project Structure

```
smart-parking-system/
├── smart_parking_system.ino   # Main Arduino sketch
└── README.md
```

-----

## 🚀 How to Deploy

```
1. Install required libraries in Arduino IDE
   (Sketch → Include Library → Manage Libraries):
   - Keypad by Mark Stanley
   (LiquidCrystal and Servo are built-in — no install needed)

2. Wire components to Arduino Uno:
   - LCD (16×2)              : RS=12, E=11, D4=5, D5=4, D6=3, D7=2
   - Servo motor (SG90)      : Signal=Pin 9
   - Ultrasonic sensor Slot1 : TRIG=A0, ECHO=A1
   - Ultrasonic sensor Slot2 : TRIG=A2, ECHO=A3
   - Ultrasonic sensor Slot3 : TRIG=A4, ECHO=A5
   - Ultrasonic sensor Slot4 : TRIG=6,  ECHO=7
   - PIR sensor              : OUT=Pin 10
   - Slot LEDs               : Pin 13 (Slot 1), Pin 8 (Slot 2)
   Note: adjust slotLEDs[] array in sketch if wiring differently

3. Update the password in smart_parking_system.ino:
   const String PASSWORD = "1234";  ← change to your PIN

4. Open smart_parking_system.ino in Arduino IDE
5. Select Board: Arduino Uno → select correct COM Port → Upload

6. Power on — LCD shows "Smart Parking System v1.0" then live slot status
   - Enter password on keypad → press # to open gate
   - Press * to clear entry at any time
```

-----

## 🔮 Future Scope

- [ ] **Mobile app** — view slot availability remotely via Wi-Fi (ESP8266)
- [ ] **RFID/NFC access** — contactless entry instead of keypad
- [ ] **Cloud dashboard** — track occupancy history and peak hours
- [ ] **Automated billing** — time-based parking fee calculation
- [ ] **Multi-level support** — scale to multiple floors with a central display

-----

*VIT-AP University · IoT & Embedded Systems Project*