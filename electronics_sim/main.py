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

radiation_count = 0

def radiation_detected(pin):
    global radiation_count
    radiation_count += 1
    print(f"[ALERT] Radiation particle detected! Total count: {radiation_count}")

# Attach an interrupt to trigger instantly when the "Geiger" button is pressed
geiger_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=radiation_detected)

print("CubeSat Payload Boot Sequence Complete.")
print("Starting telemetry loop...\n")

while True:
    try:
        # 1. Read temperature and humidity
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        # 2. Print telemetry to the ground station (serial monitor)
        print(f"TELEMETRY | Temp: {temp:.1f}°C | Hum: {hum:.1f}% | Rad Count: {radiation_count}")
        
        # 3. Basic Logic: If it gets too hot, open the valve (turn on LED)
        if temp > 30.0:
            valve.value(1)
            print(">> WARNING: High Temp! Valve OPEN.")
        else:
            valve.value(0)
            
    except OSError as e:
        print("Sensor read error.")
        
    # Wait 2 seconds before the next reading (DHT22 limit)
    time.sleep(2)
