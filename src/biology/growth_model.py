"""
growth_model.py
"""

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import yaml
import os
import logging

def load_config(config_path="config.yaml"):
    with open(config_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_biology():
    logging.info("Running biological growth models...")
    config = load_config()
    bio = config["biology"]
    
    save_dir = config["experiment"]["save_dir"]
    env_path = os.path.join(save_dir, "environment.csv")
    valve_path = os.path.join(save_dir, "valve_state.csv")
    
    df_env = pd.read_csv(env_path)
    df_valve = pd.read_csv(valve_path)
    
    time_points = df_env["time_hr"].values
    temp_arr    = df_env["temperature_c"].values
    hum_arr     = df_env["humidity_rh"].values
    valve_arr   = df_valve["valve_state"].values
    
    T_opt = config["environment"]["temperature"]["optimal_growth"]
    H_opt = config["environment"]["humidity"]["optimal_growth"]
    
    r_ch2 = bio["ch2_strain"]["r"]
    r_ch3 = bio["ch3_strain"]["r"]
    K     = bio["global"]["K"]
    N0    = bio["global"]["N0"]
    C0    = bio["global"]["initial_nutrients"]
    Y     = 1.0 / bio["global"]["nutrient_consumption"]
    K_c   = 5.0
    
    def get_env(t):
        idx = int(np.searchsorted(time_points, t, side="right") - 1)
        idx = max(0, min(idx, len(time_points) - 1))
        
        T = temp_arr[idx]
        H = hum_arr[idx]
        mod_T = np.exp(-((T - T_opt)**2) / (2 * 5.0**2))
        mod_H = np.exp(-((H - H_opt)**2) / (2 * 10.0**2))
        
        valve = valve_arr[idx]
        mod_valve = bio["global"]["valve_restricted_mod"] if valve == 1 else 1.0
        
        return mod_T * mod_H * mod_valve

    def monod_ode(t, y, r_base):
        N, C = y
        if N < 0: N = 0
        if C < 0: C = 0
        
        mod = get_env(t)
        r_eff = r_base * mod
        
        growth_rate = r_eff * N * (1.0 - N / K) * (C / (C + K_c))
        
        if C <= 0.1:
            growth_rate = -0.05 * N
            
        dNdt = growth_rate
        dCdt = -(1.0 / Y) * growth_rate if growth_rate > 0 else 0
        
        return [dNdt, dCdt]

    t_span = (time_points[0], time_points[-1])
    
    sol_ch2 = solve_ivp(monod_ode, t_span, [N0, C0], t_eval=time_points, args=(r_ch2,), method="RK45")
    sol_ch3 = solve_ivp(monod_ode, t_span, [N0, C0], t_eval=time_points, args=(r_ch3,), method="RK45")
    
    N_ch2, C_ch2 = sol_ch2.y
    N_ch3, C_ch3 = sol_ch3.y
    
    k_od = bio["global"]["k_od600"]
    OD_ch2 = k_od * N_ch2 + np.random.normal(0, 0.02, size=len(N_ch2))
    OD_ch3 = k_od * N_ch3 + np.random.normal(0, 0.02, size=len(N_ch3))
    
    OD_ch2 = np.clip(OD_ch2, 0, None)
    OD_ch3 = np.clip(OD_ch3, 0, None)
    
    df_out = pd.DataFrame({
        "time_hr": time_points,
        "N_ch2":   np.round(N_ch2, 4),
        "N_ch3":   np.round(N_ch3, 4),
        "C_ch2":   np.round(C_ch2, 2),
        "C_ch3":   np.round(C_ch3, 2),
        "OD_ch2":  np.round(OD_ch2, 4),
        "OD_ch3":  np.round(OD_ch3, 4),
    })
    out_path = os.path.join(save_dir, "growth_output.csv")
    df_out.to_csv(out_path, index=False)
    
    logging.info(f"Saved {out_path} ({len(df_out)} rows)")

if __name__ == "__main__":
    run_biology()
