"""
power_sim.py
Owner: Systems Engineering
Purpose: Simulates the 48-hour power budget and battery state of charge (SoC)
         for the LOC CubeSat, accounting for base loads, solar generation, and battery capacity.

Outputs: data/power_log.csv
"""

import numpy as np
import pandas as pd

# Constants for Power Budget
BATTERY_CAPACITY_MWH = 6660      # 1800 mAh * 3.7 V
BASE_DRAW_MW = 387               # Duty-cycled average draw (mW) from Table 9
SOLAR_GEN_MW = 750               # 0.5U Solar Panel Average Generation in sunlight (mW)
ORBIT_PERIOD_HR = 1.5            # 90 minute ISS orbit
SUNLIT_FRACTION = 0.6            # Rough estimate of sunlit portion of LEO orbit (approx 54 mins)

def generate_power_log():
    # Load master log for time steps
    df = pd.read_csv("data/master_log.csv")
    time_hr = df["time_hr"].values
    
    battery_charge = np.zeros(len(time_hr))
    battery_charge[0] = BATTERY_CAPACITY_MWH
    
    net_power_mw = np.zeros(len(time_hr))
    solar_generation = np.zeros(len(time_hr))
    
    for i in range(1, len(time_hr)):
        dt = time_hr[i] - time_hr[i-1]
        
        # Calculate solar generation (binary sunlit/eclipse based on orbit)
        orbit_phase = (time_hr[i] % ORBIT_PERIOD_HR) / ORBIT_PERIOD_HR
        if orbit_phase < SUNLIT_FRACTION:
            solar_power = SOLAR_GEN_MW
        else:
            solar_power = 0
            
        solar_generation[i] = solar_power
        
        # Net power draw/generation
        net_power = solar_power - BASE_DRAW_MW
        net_power_mw[i] = net_power
        
        # Update battery charge (Energy = Power * time)
        energy_change = net_power * dt
        new_charge = battery_charge[i-1] + energy_change
        
        # Cap battery at 100% capacity and floor at 0
        battery_charge[i] = max(0, min(BATTERY_CAPACITY_MWH, new_charge))
        
    df_out = pd.DataFrame({
        "time_hr": time_hr,
        "solar_gen_mw": solar_generation,
        "net_power_mw": net_power_mw,
        "battery_charge_mwh": battery_charge,
        "battery_pct": (battery_charge / BATTERY_CAPACITY_MWH) * 100.0
    })
    
    df_out.to_csv("data/power_log.csv", index=False)
    print(f"[power_sim] Simulated {len(time_hr)} hours. Final battery: {battery_charge[-1]:.1f} mWh ({battery_charge[-1]/BATTERY_CAPACITY_MWH*100:.1f}%)")

if __name__ == "__main__":
    generate_power_log()
