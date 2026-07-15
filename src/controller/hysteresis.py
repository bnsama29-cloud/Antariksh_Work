"""
hysteresis.py
"""

import numpy as np
import pandas as pd
import yaml
import os
import logging

def load_config(config_path="config.yaml"):
    with open(config_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_controller():
    logging.info("Running hysteresis controller...")
    config = load_config()
    
    UPPER_THRESH = 500.0
    LOWER_THRESH = 350.0
    INITIAL_VALVE = 0
    
    save_dir = config["experiment"]["save_dir"]
    env_path = os.path.join(save_dir, "environment.csv")
    
    df_env = pd.read_csv(env_path)
    time_hr = df_env["time_hr"].values
    flux    = df_env["flux_uGy_hr"].values
    
    valve_state = np.zeros(len(time_hr), dtype=int)
    current_valve = INITIAL_VALVE
    
    for i, f in enumerate(flux):
        if f > UPPER_THRESH:
            current_valve = 1
        elif f < LOWER_THRESH:
            current_valve = 0
        valve_state[i] = current_valve
        
    df_out = pd.DataFrame({"time_hr": time_hr, "valve_state": valve_state})
    out_path = os.path.join(save_dir, "valve_state.csv")
    df_out.to_csv(out_path, index=False)
    
    logging.info(f"Saved {out_path} ({len(df_out)} rows)")

if __name__ == "__main__":
    run_controller()
