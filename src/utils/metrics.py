"""
metrics.py
"""

import pandas as pd
import numpy as np
import yaml
import os
import json
import logging

def load_config(config_path="config.yaml"):
    with open(config_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_metrics():
    logging.info("Running metrics integration...")
    config = load_config()
    save_dir = config["experiment"]["save_dir"]
    
    env    = pd.read_csv(os.path.join(save_dir, "environment.csv"))
    valve  = pd.read_csv(os.path.join(save_dir, "valve_state.csv"))
    growth = pd.read_csv(os.path.join(save_dir, "growth_output.csv"))
    attn   = pd.read_csv(os.path.join(save_dir, "attenuation_output.csv"))
        
    master = env.merge(valve, on="time_hr") \
                .merge(growth, on="time_hr") \
                .merge(attn, on="time_hr")
                
    out_path = os.path.join(save_dir, "master_log.csv")
    master.to_csv(out_path, index=False)
    logging.info(f"Saved {out_path} ({len(master)} rows)")
    
    faults = []
    if master.isnull().sum().sum() > 0:
        faults.append("NaN values found in master_log.csv")
        
    peak_ch2 = master["attn_ch2_pct"].max()
    if peak_ch2 > 10.0:
        faults.append(f"CH-2 attenuation {peak_ch2:.2f}% exceeds 10%")
    elif peak_ch2 < 0.5:
        faults.append(f"CH-2 attenuation {peak_ch2:.3f}% is very low")
        
    if master["C_ch2"].iloc[-1] <= 0 or master["C_ch3"].iloc[-1] <= 0:
        faults.append("Nutrients completely depleted")
        
    for f in faults:
        logging.warning(f"FAULT: {f}")
        
    summary = {
        "experiment_duration_hrs": config["experiment"]["duration_hrs"],
        "mean_flux_uGy_hr": float(master['flux_uGy_hr'].mean()),
        "restricted_hrs": int(master['valve_state'].sum()),
        "ch2": {
            "final_biomass_gL": float(master['N_ch2'].iloc[-1]),
            "peak_attenuation_pct": float(master['attn_ch2_pct'].max())
        },
        "ch3": {
            "final_biomass_gL": float(master['N_ch3'].iloc[-1]),
            "peak_attenuation_pct": float(master['attn_ch3_pct'].max())
        },
        "faults": faults
    }
    
    sum_path = os.path.join(save_dir, "summary.json")
    with open(sum_path, 'w', encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
        
    logging.info(f"Saved {sum_path}")

if __name__ == "__main__":
    run_metrics()
