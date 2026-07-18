import machine
import dht
import time

# --- PINS ---
# DHT22 is on Pin 15
sensor = dht.DHT22(machine.Pin(15))

# Geiger Counter (Simulated by a button on Pin 16)
geiger_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

# Valve/LED on Pin 14
valve = machine.Pin(14, machine.Pin.OUT)

# State Variables
radiation_count = 0
in_radiation_anomaly = False

def geiger_triggered(pin):
    global radiation_count, in_radiation_anomaly
    radiation_count += 150  # Simulate a massive spike in flux hits
    in_radiation_anomaly = not in_radiation_anomaly # Toggle anomaly state
    
    print(f"\n[ALERT] Geiger Counter Triggered! Rad Count Spike: {radiation_count}")
    
    # Update Valve based on radiation anomaly state
    if in_radiation_anomaly:
        valve.value(1)
        print(">> SAA Anomaly Detected: Radiation HIGH. Valve OPENED (LED ON) <<")
    else:
        valve.value(0)
        print(">> Left SAA Anomaly: Radiation Normal. Valve CLOSED (LED OFF) <<")
    print("--------------------------------------------------")

# Attach an interrupt to trigger instantly when the button is pressed
geiger_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=geiger_triggered)

print("CubeSat Payload Boot Sequence Complete.")
print("Starting telemetry loop...\n")

while True:
    try:
        # 1. Read temperature and humidity
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        # 2. Print telemetry to the ground station
        valve_status = "OPEN" if in_radiation_anomaly else "CLOSED"
        print(f"TELEMETRY | Temp: {temp:.1f}°C | Hum: {hum:.1f}% | Rad Count: {radiation_count} | Valve: {valve_status}")
            
    except OSError as e:
        print("Sensor read error.")
        
    # Wait 2 seconds before the next reading
    time.sleep(2)
