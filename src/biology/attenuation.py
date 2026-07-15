"""
attenuation.py
"""

import numpy as np
import pandas as pd
import yaml
import os
import logging

def load_config(config_path="config.yaml"):
    with open(config_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_attenuation():
    logging.info("Running radiation attenuation model...")
    config = load_config()
    bio = config["biology"]
    
    save_dir = config["experiment"]["save_dir"]
    growth_path = os.path.join(save_dir, "growth_output.csv")
    env_path = os.path.join(save_dir, "environment.csv")
    
    df_growth = pd.read_csv(growth_path)
    df_env    = pd.read_csv(env_path)
    
    time_hr = df_growth["time_hr"].values
    N_ch2   = df_growth["N_ch2"].values
    N_ch3   = df_growth["N_ch3"].values
    I0      = df_env["flux_uGy_hr"].values
    
    MU_CH2 = bio["ch2_strain"]["mu"]
    RHO_CH2 = bio["ch2_strain"]["rho"]
    ALPHA_CH2 = bio["ch2_strain"]["alpha"]
    
    MU_CH3 = bio["ch3_strain"]["mu"]
    RHO_CH3 = bio["ch3_strain"]["rho"]
    ALPHA_CH3 = bio["ch3_strain"]["alpha"]
    
    delta_ch2 = ALPHA_CH2 * N_ch2
    delta_ch3 = ALPHA_CH3 * N_ch3
    
    I_ch2 = I0 * np.exp(-MU_CH2 * RHO_CH2 * delta_ch2)
    I_ch3 = I0 * np.exp(-MU_CH3 * RHO_CH3 * delta_ch3)
    
    attn_ch2_pct = (I0 - I_ch2) / I0 * 100
    attn_ch3_pct = (I0 - I_ch3) / I0 * 100
    
    attn_ch2_pct = np.nan_to_num(attn_ch2_pct, 0.0)
    attn_ch3_pct = np.nan_to_num(attn_ch3_pct, 0.0)
    
    df_out = pd.DataFrame({
        "time_hr":      time_hr,
        "delta_ch2":    np.round(delta_ch2,    6),
        "delta_ch3":    np.round(delta_ch3,    6),
        "I_ch2":        np.round(I_ch2,        3),
        "I_ch3":        np.round(I_ch3,        3),
        "attn_ch2_pct": np.round(attn_ch2_pct, 4),
        "attn_ch3_pct": np.round(attn_ch3_pct, 4),
    })
    out_path = os.path.join(save_dir, "attenuation_output.csv")
    df_out.to_csv(out_path, index=False)
    
    logging.info(f"Saved {out_path} ({len(df_out)} rows)")

if __name__ == "__main__":
    run_attenuation()
