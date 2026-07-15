/*
 * cubesat_electronics.ino
 * Owner: EC member
 * Simulation: Arduino / Wokwi electronics sim for LOC CubeSat payload
 *
 * What this simulates (virtual twin of the CubeSat):
 *   - DHT22: Temperature & Humidity sensor (Auxiliary Computer)
 *   - SIM radiation sensor via potentiometer (Geiger counter proxy)
 *   - LED status lights (valve state indicator)
 *   - I2C LCD for live readings
 *   - Serial output → can be read by Python via pyserial for integration
 *
 * How to run:
 *   Option A (Wokwi online): Go to https://wokwi.com → New Project →
 *             Arduino Uno → paste this code. Add DHT22, potentiometer, LCD.
 *   Option B (TinkerCad): circuits.tinkercad.com → Create Circuit → paste.
 *
 * Wiring summary:
 *   DHT22 DATA → Pin 2
 *   Radiation POT (analog) → A0
 *   Valve OPEN LED (red)   → Pin 8
 *   Valve CLOSED LED (grn) → Pin 9
 *   LCD (I2C) → SDA=A4, SCL=A5
 */

#include <DHT.h>
#include <LiquidCrystal_I2C.h>

// ── Pin Definitions ────────────────────────────────────────────────────────
#define DHT_PIN        2
#define DHT_TYPE       DHT22
#define RAD_SENSOR_PIN A0    // Potentiometer simulating Geiger counter output
#define VALVE_OPEN_LED 8     // Red LED — valve OPEN (high radiation)
#define VALVE_CLOSED_LED 9   // Green LED — valve CLOSED (safe)

// ── Hysteresis Thresholds ──────────────────────────────────────────────────
const float UPPER_THRESH = 500.0;   // μGy/hr — opens nutrient valve
const float LOWER_THRESH = 350.0;   // μGy/hr — closes nutrient valve

// ── Sensor / State ─────────────────────────────────────────────────────────
DHT dht(DHT_PIN, DHT_TYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);   // I2C address 0x27, 16 cols, 2 rows

bool valveOpen = false;         // hysteresis state
unsigned long lastLog = 0;
const unsigned long LOG_INTERVAL_MS = 2000;   // log every 2 sec

// ── Helper: map ADC reading (0–1023) to flux range ────────────────────────
// Pot at 0   → 150 μGy/hr (GCR background)
// Pot at 512 → 425 μGy/hr (deadband)
// Pot at 1023→ 700 μGy/hr (SAA peak)
float mapRadiation(int adcVal) {
    return (float)adcVal / 1023.0 * (700.0 - 150.0) + 150.0;
}

void setup() {
    Serial.begin(9600);
    dht.begin();
    lcd.init();
    lcd.backlight();

    pinMode(VALVE_OPEN_LED, OUTPUT);
    pinMode(VALVE_CLOSED_LED, OUTPUT);

    lcd.setCursor(0, 0);
    lcd.print("LOC CubeSat Sim");
    lcd.setCursor(0, 1);
    lcd.print("Initializing...");
    delay(1500);
    lcd.clear();

    Serial.println("time_s,flux_uGy_hr,valve_state,temp_C,humidity_pct");
}

void loop() {
    unsigned long now = millis();

    // ── Read sensors ──────────────────────────────────────────────────────
    int   rawRad  = analogRead(RAD_SENSOR_PIN);
    float flux    = mapRadiation(rawRad);

    float temp    = dht.readTemperature();    // °C
    float humidity = dht.readHumidity();      // %

    if (isnan(temp) || isnan(humidity)) {
        temp = 25.0;        // fallback if DHT not connected in sim
        humidity = 60.0;
    }

    // ── Hysteresis controller ─────────────────────────────────────────────
    if (flux > UPPER_THRESH) {
        valveOpen = true;    // OPEN — high radiation, restrict nutrients
    } else if (flux < LOWER_THRESH) {
        valveOpen = false;   // CLOSE — safe, resume nutrients
    }
    // else: HOLD (deadband — no state change)

    // ── LED indicators ────────────────────────────────────────────────────
    digitalWrite(VALVE_OPEN_LED,   valveOpen ? HIGH : LOW);
    digitalWrite(VALVE_CLOSED_LED, valveOpen ? LOW : HIGH);

    // ── LCD Display ───────────────────────────────────────────────────────
    lcd.setCursor(0, 0);
    lcd.print("F:");
    lcd.print((int)flux);
    lcd.print("uG V:");
    lcd.print(valveOpen ? "OPN" : "CLS");

    lcd.setCursor(0, 1);
    lcd.print("T:");
    lcd.print(temp, 1);
    lcd.print("C H:");
    lcd.print((int)humidity);
    lcd.print("%  ");

    // ── Serial log (CSV format — readable by Python pyserial) ─────────────
    if (now - lastLog >= LOG_INTERVAL_MS) {
        lastLog = now;
        Serial.print(now / 1000);   Serial.print(",");
        Serial.print(flux, 1);      Serial.print(",");
        Serial.print(valveOpen ? 1 : 0); Serial.print(",");
        Serial.print(temp, 1);      Serial.print(",");
        Serial.println(humidity, 1);
    }

    delay(200);
}
