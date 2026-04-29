/*
 * New Smart Parking System
 * IoT-Enabled Parking Management with Password Protection,
 * Ultrasonic Slot Detection & Motion-Activated Lighting
 *
 * Paper: "New Parking System: Revolutionizing Parking Management
 * Through IoT-Enabled Smart Parking Solutions"
 * Authors: Mekala Samuel (21BCB7145), M. Bhanu Prakash (21BCB7050),
 *          Shaik Mohammad Mujahiddin (21BCB7101), N. Sandeep (21BCB7166)
 * VIT-AP University
 *
 * Hardware:
 *   Arduino UNO, Ultrasonic Sensors (HC-SR04), Servo Motor,
 *   Keypad (4x4), LCD (16x2), PIR Motion Sensor, LEDs, Buzzer
 */

#include <LiquidCrystal.h>
#include <Servo.h>
#include <Keypad.h>

// ─── LCD Pins: RS, E, D4, D5, D6, D7 ────────────────────────────────────────
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

// ─── Servo Motor (Gate) ───────────────────────────────────────────────────────
Servo gateServo;
#define SERVO_PIN    3
#define GATE_OPEN   90
#define GATE_CLOSED  0

// ─── Ultrasonic Sensors ───────────────────────────────────────────────────────
// Slot 1
#define TRIG1  A0
#define ECHO1  A1
// Slot 2
#define TRIG2  A2
#define ECHO2  A3
// Slot 3
#define TRIG3  10
#define ECHO3  11
// Slot 4
#define TRIG4  12
#define ECHO4  13

#define OCCUPIED_DIST_CM 10   // Distance threshold: < 10 cm = slot occupied

// ─── Slot LEDs ────────────────────────────────────────────────────────────────
#define LED_SLOT1  22
#define LED_SLOT2  23
#define LED_SLOT3  24
#define LED_SLOT4  25

// ─── Motion Sensor (PIR) for lighting ─────────────────────────────────────────
#define PIR_PIN       30
#define LIGHT_PIN     31
#define LIGHT_TIMEOUT 30000UL   // Auto-off after 30 s

// ─── Keypad ───────────────────────────────────────────────────────────────────
const byte ROWS = 4;
const byte COLS = 4;
char hexaKeys[ROWS][COLS] = {
    {'1','2','3','A'},
    {'4','5','6','B'},
    {'7','8','9','C'},
    {'*','0','#','D'}
};
byte rowPins[ROWS] = {32, 33, 34, 35};
byte colPins[COLS] = {36, 37, 38, 39};
Keypad keypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

// ─── Password ─────────────────────────────────────────────────────────────────
const String PASSWORD = "1234";   // Change to your desired 4-digit PIN
String inputPassword  = "";

// ─── Helpers ──────────────────────────────────────────────────────────────────

long measure_distance(int trigPin, int echoPin) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH, 30000);  // 30 ms timeout
    if (duration == 0) return 999;   // No echo = slot empty / out of range
    return duration * 0.034 / 2;    // Convert to cm
}

bool is_slot_occupied(int trigPin, int echoPin) {
    long dist = measure_distance(trigPin, echoPin);
    return (dist > 0 && dist < OCCUPIED_DIST_CM);
}

void open_gate() {
    gateServo.write(GATE_OPEN);
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Gate: OPEN");
    delay(5000);   // Keep open for 5 s
    gateServo.write(GATE_CLOSED);
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Gate: CLOSED");
}

// ─── Setup ────────────────────────────────────────────────────────────────────

void setup() {
    Serial.begin(9600);

    lcd.begin(16, 2);
    lcd.print("Smart Parking");
    lcd.setCursor(0, 1);
    lcd.print("System v1.0");
    delay(2000);
    lcd.clear();

    gateServo.attach(SERVO_PIN);
    gateServo.write(GATE_CLOSED);

    // Ultrasonic trigger pins
    pinMode(TRIG1, OUTPUT); pinMode(ECHO1, INPUT);
    pinMode(TRIG2, OUTPUT); pinMode(ECHO2, INPUT);
    pinMode(TRIG3, OUTPUT); pinMode(ECHO3, INPUT);
    pinMode(TRIG4, OUTPUT); pinMode(ECHO4, INPUT);

    // Slot indicator LEDs
    pinMode(LED_SLOT1, OUTPUT);
    pinMode(LED_SLOT2, OUTPUT);
    pinMode(LED_SLOT3, OUTPUT);
    pinMode(LED_SLOT4, OUTPUT);

    // Motion sensor & light
    pinMode(PIR_PIN,   INPUT);
    pinMode(LIGHT_PIN, OUTPUT);
    digitalWrite(LIGHT_PIN, LOW);
}

// ─── Main Loop ────────────────────────────────────────────────────────────────

unsigned long lastMotion = 0;

void loop() {
    // ── 1. Slot availability check ──
    bool s1 = is_slot_occupied(TRIG1, ECHO1);
    bool s2 = is_slot_occupied(TRIG2, ECHO2);
    bool s3 = is_slot_occupied(TRIG3, ECHO3);
    bool s4 = is_slot_occupied(TRIG4, ECHO4);

    // Update slot LEDs: ON = occupied, OFF = free
    digitalWrite(LED_SLOT1, s1 ? HIGH : LOW);
    digitalWrite(LED_SLOT2, s2 ? HIGH : LOW);
    digitalWrite(LED_SLOT3, s3 ? HIGH : LOW);
    digitalWrite(LED_SLOT4, s4 ? HIGH : LOW);

    int freeSlots = (!s1) + (!s2) + (!s3) + (!s4);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Free slots: ");
    lcd.print(freeSlots);
    lcd.setCursor(0, 1);
    lcd.print(s1?"O":"F");
    lcd.print(s2?"O":"F");
    lcd.print(s3?"O":"F");
    lcd.print(s4?"O":"F");
    lcd.print(" (O=occ F=free)");

    // ── 2. Motion-activated lighting ──
    if (digitalRead(PIR_PIN) == HIGH) {
        lastMotion = millis();
        digitalWrite(LIGHT_PIN, HIGH);
    } else if ((millis() - lastMotion) >= LIGHT_TIMEOUT) {
        digitalWrite(LIGHT_PIN, LOW);
    }

    // ── 3. Password-protected gate entry ──
    char key = keypad.getKey();
    if (key) {
        if (key == '#') {
            // Confirm entry
            if (inputPassword == PASSWORD) {
                if (freeSlots > 0) {
                    lcd.clear();
                    lcd.print("Access Granted!");
                    open_gate();
                } else {
                    lcd.clear();
                    lcd.print("No Free Slots!");
                    delay(2000);
                }
            } else {
                lcd.clear();
                lcd.print("Wrong Password!");
                delay(2000);
            }
            inputPassword = "";
        } else if (key == '*') {
            // Clear entry
            inputPassword = "";
            lcd.clear();
            lcd.print("Enter Password:");
        } else {
            inputPassword += key;
            lcd.clear();
            lcd.setCursor(0, 0); lcd.print("Enter Password:");
            lcd.setCursor(0, 1);
            for (unsigned int i = 0; i < inputPassword.length(); i++) {
                lcd.print('*');
            }
        }
    }

    delay(300);
}
