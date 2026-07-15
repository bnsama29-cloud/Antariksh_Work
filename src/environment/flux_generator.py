"""
flux_generator.py
"""

import numpy as np
import pandas as pd
import yaml
import os
import logging

def load_config(config_path="config.yaml"):
    with open(config_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def generate_environment():
    logging.info("Generating environmental data...")
    config = load_config()
    
    DURATION_HRS = config["experiment"]["duration_hrs"]
    TIME_STEP_HRS = config["experiment"]["time_step_hrs"]
    
    env_config = config["environment"]
    RAD = env_config["radiation"]
    TEMP = env_config["temperature"]
    HUM = env_config["humidity"]
    
    np.random.seed(42)

    time_hr = np.arange(0, DURATION_HRS + TIME_STEP_HRS, TIME_STEP_HRS)
    
    flux = np.full_like(time_hr, RAD["gcr_baseline"])
    
    for saa_center in np.arange(RAD["saa_interval"], DURATION_HRS, RAD["saa_interval"]):
        for i, t in enumerate(time_hr):
            if abs(t - saa_center) < RAD["saa_duration"]:
                flux[i] += (RAD["saa_peak"] - RAD["gcr_baseline"]) * np.exp(
                    -0.5 * ((t - saa_center) / (RAD["saa_duration"] / 2)) ** 2
                )
    
    flux += np.random.normal(0, RAD["noise_sigma"], size=len(time_hr))
    flux = np.clip(flux, 0, None)
    
    orbit_period = 1.5
    temp = TEMP["nominal"] + TEMP["fluctuation"] * np.sin(2 * np.pi * time_hr / orbit_period)
    temp += np.random.normal(0, TEMP["std_noise"], size=len(time_hr))
    
    humidity = HUM["nominal"] + HUM["fluctuation"] * np.cos(2 * np.pi * time_hr / orbit_period)
    humidity += np.random.normal(0, HUM["std_noise"], size=len(time_hr))
    
    os.makedirs(config["experiment"]["save_dir"], exist_ok=True)
    
    df = pd.DataFrame({
        "time_hr": time_hr, 
        "flux_uGy_hr": np.round(flux, 3),
        "temperature_c": np.round(temp, 2),
        "humidity_rh": np.round(humidity, 2)
    })
    
    out_path = os.path.join(config["experiment"]["save_dir"], "environment.csv")
    df.to_csv(out_path, index=False)
    logging.info(f"Saved {out_path} ({len(df)} rows)")

if __name__ == "__main__":
    generate_environment()
