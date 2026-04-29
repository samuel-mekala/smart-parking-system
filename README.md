# 🅿️ New Parking System — IoT-Enabled Smart Parking Solution

> **Academic Paper / IoT Project** · VIT-AP University  
> **Authors:** Mekala Samuel · M. Bhanu Prakash · Shaik Mohammad Mujahiddin · N. Sandeep  
> **Student ID:** 21BCB7145

---

## 📌 Overview

Urbanization and rising car ownership have made parking one of the biggest pain points in modern cities — causing traffic congestion, energy waste, and security vulnerabilities. This project introduces the **"New Parking System"**, a smart IoT-based parking management solution that uses:

- 🔐 **Password-protected access control** (keypad entry)
- 📡 **Ultrasonic distance sensing** (real-time slot detection)
- ⚙️ **Servo motor actuation** (automated gate control)
- 💡 **Motion-activated lighting** (energy conservation)

The result: a more **secure, space-efficient, and energy-responsible** urban parking experience.

---

## 🏗️ System Architecture

```
Power Supply
     ↓
  Arduino UNO  ──────────→  Servo Motor (Gate Control)
     ↑    ↓
  Keypad    Ultrasonic Sensor (Slot Detection)
             ↓
        Motion Sensor → LED Lighting (Auto ON/OFF)
```

**Block Diagram Flow:**
```
Power Supply → Arduino → Servo Motor (open/close gate)
                ↑
             Keypad (password entry)
                ↑
          Ultrasonic Sensor (detect car presence)
```

---

## ⚙️ How It Works

### 1. Access Control
- Driver enters **password via keypad**
- Arduino validates the password
- If correct → **servo motor opens the gate**
- If incorrect → gate stays closed (security maintained)

### 2. Slot Detection
- **Ultrasonic sensors** continuously measure distance to detect if a slot is occupied or vacant
- Real-time occupancy data is processed by the Arduino

### 3. Motion-Activated Lighting
- **Motion sensors** trigger LED lights only when a vehicle or person is present
- Lights auto-OFF when area is empty → significant energy savings

### 4. Gate Automation
- **Servo motor** controls the physical barrier
- Opens on valid entry, closes after vehicle passes
- Prevents unauthorized access at all times

---

## 🔧 Hardware Components

| Component | Purpose |
|---|---|
| **Arduino UNO** | Main microcontroller — processes all inputs/outputs |
| **Ultrasonic Sensor** | Measures distance to detect vehicle presence in slots |
| **Servo Motor** | Actuates the parking gate (open/close) |
| **Keypad** | Password input for access control |
| **Motion Sensor** | Triggers lighting when movement detected |
| **LED Lights** | Energy-efficient motion-activated lighting |
| **Power Supply** | Powers the entire system |

---

## 💻 Software

| Component | Details |
|---|---|
| **IDE** | Arduino IDE |
| **Language** | C (Arduino/ATmega328) |
| **Key Libraries** | `Servo.h` · `Keypad.h` · `NewPing.h` (ultrasonic) |

---

## 🎯 Key Features

| Feature | Benefit |
|---|---|
| Password-protected entry | Prevents unauthorized parking |
| Real-time slot detection | Drivers know instantly if space is available |
| Automated gate control | No manual intervention needed |
| Motion-activated lights | Reduces energy consumption significantly |
| Scalable architecture | Can be expanded to multi-floor parking systems |

---

## 📊 Problem → Solution Mapping

| Problem | Our Solution |
|---|---|
| Traffic congestion from parking search | Real-time slot availability detection |
| Unauthorized parking | Password-protected servo gate |
| Energy waste from always-on lights | Motion-activated LED system |
| Manual gate operation | Automated servo motor actuation |
| Poor space utilization | Ultrasonic sensors for precise slot monitoring |

---

## 🌆 Smart Parking Strategies Explored

This project also reviewed and analyzed 6 key strategies for urban parking efficiency:

1. **Smart Parking Systems** — Sensors + cameras + real-time data
2. **Shared Parking Concepts** — Off-peak space sharing between buildings
3. **Dynamic Pricing** — Variable rates based on demand
4. **Multipurpose Parking Structures** — Adaptable architecture for events/markets
5. **Alternative Transportation Promotion** — Bike racks, EV charging stations
6. **Mixed-Use Buildings** — Pooled parking for commercial + residential

---

## 📁 Project Structure

```
smart-parking-system/
├── firmware/
│   └── parking_system.ino     # Main Arduino sketch
├── schematics/
│   └── circuit_diagram.png    # Full wiring diagram
├── docs/
│   └── research_paper.pdf     # Published paper
├── images/
│   └── prototype.jpg          # Working prototype photo
├── requirements.txt
└── README.md
```

---

## 🚀 How to Deploy

```
1. Wire all components as per the circuit diagram
2. Open firmware/parking_system.ino in Arduino IDE
3. Set your password in the code:
   char password[] = "1234";  // Change this
4. Upload to Arduino UNO
5. Power the system
6. Test: Enter password on keypad → gate opens → ultrasonic detects car
```

---

## 🔮 Future Scope

- [ ] Mobile app integration for remote slot booking and payment
- [ ] Integration with Google Maps / Waze for navigation to open slots
- [ ] Cloud dashboard for facility managers (occupancy, revenue, reports)
- [ ] Dynamic pricing based on real-time demand
- [ ] Multi-floor support with floor-wise slot tracking
- [ ] RFID / QR code based access (replacing keypad)
- [ ] Camera-based license plate recognition for security

---

## 📚 References

1. Widyasari et al. — IoT-based Smart Parking System, ICODSE 2019
2. Vinay Raj Tripathi — Smart Vehicle Parking System Using IoT, ICE3 2020
3. S. Gunanandhini et al. — Smart Parking with Surveillance Using IoT, ICACCS 2022
4. Namgiri Suresh et al. — IoT-powered Smart Car Parking Solutions, ICAAIC 2023
5. Yuchang Wu — Optimizing Urban Public Parking Resources, ITAIC 2022
6. Shanmugapriya P et al. — IoT-based Control and Management for Parking, ICPECTS 2022

---

## 🖼️ Prototype

![Working Prototype](images/prototype.jpg)

---

*VIT-AP University · IoT & Embedded Systems · Samuel Mekala (21BCB7145)*
