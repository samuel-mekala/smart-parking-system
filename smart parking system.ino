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
 *   Arduino UNO, HC-SR04 Ultrasonic Sensors (×4), Servo Motor (SG90),
 *   4×4 Keypad, 16×2 LCD (without I2C), PIR Sensor, LEDs (×4), Buzzer
 *
 * Features:
 *   1. Real-time slot detection via ultrasonic sensors
 *   2. Password-protected servo gate (keypad entry)
 *   3. Motion-activated lighting (PIR + relay)
 *   4. LCD status display (free slots + slot map)
 *   5. Per-slot LED indicators (ON = occupied, OFF = free)
 */

#include <LiquidCrystal.h>
#include <Servo.h>
#include <Keypad.h>

// ─── LCD: RS, E, D4, D5, D6, D7 ─────────────────────────────────────────────
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// ─── Servo Motor (Gate) ───────────────────────────────────────────────────────
Servo gateServo;
#define SERVO_PIN    9
#define GATE_OPEN   90    // degrees — gate open position
#define GATE_CLOSED  0    // degrees — gate closed position

// ─── Ultrasonic Sensors (HC-SR04) ────────────────────────────────────────────
//              TRIG     ECHO
#define TRIG1    A0
#define ECHO1    A1
#define TRIG2    A2
#define ECHO2    A3
#define TRIG3    A4
#define ECHO3    A5
#define TRIG4    6
#define ECHO4    7

#define OCCUPIED_CM  15   // < 15 cm = slot occupied by a vehicle

// ─── Per-Slot Indicator LEDs ─────────────────────────────────────────────────
#define LED1  A0   // reused as output when sensor not scanning — or use shift register
// NOTE: On Uno, use separate digital pins if possible. Assign based on availability.
// Simplest approach: single bi-colour LED or one LED per slot on pins below
// Adjust to your actual wiring:
int slotLEDs[4] = {13, 8, -1, -1};  // pins for slot 1 & 2 LEDs; -1 = not wired

// ─── PIR Motion Sensor + Light Relay ─────────────────────────────────────────
#define PIR_PIN       10
#define LIGHT_RELAY   -1    // set to actual pin if wired, e.g. pin 13; -1 = skip
#define LIGHT_TIMEOUT 30000UL   // lights auto-off after 30 seconds

// ─── Keypad (4×4) ────────────────────────────────────────────────────────────
// NOTE: On Arduino Uno, rows/cols must use remaining free digital pins.
// Adjust rowPins/colPins to match your wiring.
const byte ROWS = 4;
const byte COLS = 3;   // using 3-col subset (1-9, *, 0, #) to save pins on Uno

char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};
byte rowPins[ROWS] = {A0, A1, A2, A3};  // ← adjust to free analog pins used as digital
byte colPins[COLS] = {6, 7, 8};         // ← adjust to free digital pins

// IMPORTANT: The pin assignments above are a reference layout.
// Because Uno has limited pins, you may need to multiplex or use a PCF8574
// I2C expander for the keypad + LCD together. Adjust all pin defines to
// match your actual hardware wiring before uploading.

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// ─── Password ─────────────────────────────────────────────────────────────────
const String PASSWORD = "1234";   // ← change to your desired PIN
String inputPassword  = "";

// ─── Global State ─────────────────────────────────────────────────────────────
unsigned long lastMotionTime = 0;

// ─── Distance Measurement ─────────────────────────────────────────────────────
long measure_cm(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 25000); // 25ms timeout ~4m max
  if (duration == 0) return 999;
  return duration * 0.034 / 2;
}

bool is_occupied(int trigPin, int echoPin) {
  return measure_cm(trigPin, echoPin) < OCCUPIED_CM;
}

// ─── Gate Control ─────────────────────────────────────────────────────────────
void open_gate() {
  gateServo.write(GATE_OPEN);
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print("Access Granted!");
  lcd.setCursor(0, 1); lcd.print("Gate: OPEN");
  delay(5000);
  gateServo.write(GATE_CLOSED);
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print("Gate: CLOSED");
  delay(1000);
}

// ─── Setup ────────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(9600);

  lcd.begin(16, 2);
  lcd.print("Smart  Parking");
  lcd.setCursor(0, 1);
  lcd.print("System  v1.0");
  delay(2000);
  lcd.clear();

  gateServo.attach(SERVO_PIN);
  gateServo.write(GATE_CLOSED);

  // Ultrasonic pins
  int trigs[] = {TRIG1, TRIG2, TRIG3, TRIG4};
  int echos[] = {ECHO1, ECHO2, ECHO3, ECHO4};
  for (int i = 0; i < 4; i++) {
    pinMode(trigs[i], OUTPUT);
    pinMode(echos[i], INPUT);
  }

  // Slot LEDs
  for (int i = 0; i < 4; i++) {
    if (slotLEDs[i] != -1) {
      pinMode(slotLEDs[i], OUTPUT);
      digitalWrite(slotLEDs[i], LOW);
    }
  }

  // PIR + light relay
  pinMode(PIR_PIN, INPUT);
  if (LIGHT_RELAY != -1) {
    pinMode(LIGHT_RELAY, OUTPUT);
    digitalWrite(LIGHT_RELAY, LOW);
  }
}

// ─── Main Loop ────────────────────────────────────────────────────────────────
void loop() {

  // ── 1. Check all 4 slots ──────────────────────────────────────────────────
  bool occupied[4];
  int  trigs[] = {TRIG1, TRIG2, TRIG3, TRIG4};
  int  echos[] = {ECHO1, ECHO2, ECHO3, ECHO4};

  int freeCount = 0;
  for (int i = 0; i < 4; i++) {
    occupied[i] = is_occupied(trigs[i], echos[i]);
    if (!occupied[i]) freeCount++;
    if (slotLEDs[i] != -1)
      digitalWrite(slotLEDs[i], occupied[i] ? HIGH : LOW);
  }

  // ── 2. Update LCD ─────────────────────────────────────────────────────────
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Free: ");
  lcd.print(freeCount);
  lcd.print("/4");

  lcd.setCursor(0, 1);
  for (int i = 0; i < 4; i++) {
    lcd.print(i + 1);
    lcd.print(":");
    lcd.print(occupied[i] ? "X" : "O");
    lcd.print(" ");
  }
  // Display: "1:X 2:O 3:O 4:X"  (X=taken, O=open)

  // ── 3. PIR motion-activated lighting ─────────────────────────────────────
  if (digitalRead(PIR_PIN) == HIGH) {
    lastMotionTime = millis();
    if (LIGHT_RELAY != -1) digitalWrite(LIGHT_RELAY, HIGH);
  } else {
    if ((millis() - lastMotionTime) >= LIGHT_TIMEOUT) {
      if (LIGHT_RELAY != -1) digitalWrite(LIGHT_RELAY, LOW);
    }
  }

  // ── 4. Keypad password entry ──────────────────────────────────────────────
  char key = keypad.getKey();
  if (key) {
    if (key == '#') {
      // Confirm password
      if (inputPassword == PASSWORD) {
        if (freeCount > 0) {
          open_gate();
        } else {
          lcd.clear();
          lcd.setCursor(0, 0); lcd.print("Parking FULL!");
          lcd.setCursor(0, 1); lcd.print("No slots free.");
          delay(2000);
        }
      } else {
        lcd.clear();
        lcd.setCursor(0, 0); lcd.print("Wrong Password!");
        lcd.setCursor(0, 1); lcd.print("Try again.");
        delay(2000);
      }
      inputPassword = "";

    } else if (key == '*') {
      // Clear / reset input
      inputPassword = "";
      lcd.clear();
      lcd.setCursor(0, 0); lcd.print("Enter Password:");
      lcd.setCursor(0, 1); lcd.print("                ");

    } else {
      // Add digit to password
      inputPassword += key;
      lcd.clear();
      lcd.setCursor(0, 0); lcd.print("Enter Password:");
      lcd.setCursor(0, 1);
      for (unsigned int i = 0; i < inputPassword.length(); i++) {
        lcd.print('*');
      }
    }

    Serial.print("Key pressed: "); Serial.println(key);
  }

  delay(200);
}
