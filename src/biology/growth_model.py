"""
growth_model.py
Fungal growth simulation using Monod kinetics with environmental modifiers.
"""

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import yaml
import os
import logging
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List

@dataclass
class StrainConfig:
    name: str
    r: float
    mu: float
    rho: float
    alpha: float

@dataclass
class BiologyConfig:
    ch2: StrainConfig
    ch3: StrainConfig
    K: float
    N0: float
    initial_nutrients: float
    nutrient_consumption: float
    k_od600: float
    valve_restricted_mod: float
    T_opt: float
    H_opt: float
    save_dir: str

def load_config(config_path: str = "config.yaml") -> BiologyConfig:
    with open(config_path, 'r', encoding="utf-8") as f:
        raw: Dict[str, Any] = yaml.safe_load(f)
        
    return BiologyConfig(
        ch2=StrainConfig(**raw["biology"]["ch2_strain"]),
        ch3=StrainConfig(**raw["biology"]["ch3_strain"]),
        K=float(raw["biology"]["global"]["K"]),
        N0=float(raw["biology"]["global"]["N0"]),
        initial_nutrients=float(raw["biology"]["global"]["initial_nutrients"]),
        nutrient_consumption=float(raw["biology"]["global"]["nutrient_consumption"]),
        k_od600=float(raw["biology"]["global"]["k_od600"]),
        valve_restricted_mod=float(raw["biology"]["global"]["valve_restricted_mod"]),
        T_opt=float(raw["environment"]["temperature"]["optimal_growth"]),
        H_opt=float(raw["environment"]["humidity"]["optimal_growth"]),
        save_dir=str(raw["experiment"]["save_dir"])
    )

def run_biology() -> None:
    logging.info("Running biological growth models...")
    cfg: BiologyConfig = load_config()
    
    env_path = os.path.join(cfg.save_dir, "environment.csv")
    valve_path = os.path.join(cfg.save_dir, "valve_state.csv")
    
    df_env = pd.read_csv(env_path)
    df_valve = pd.read_csv(valve_path)
    
    time_points: np.ndarray = df_env["time_hr"].values
    temp_arr: np.ndarray    = df_env["temperature_c"].values
    hum_arr: np.ndarray     = df_env["humidity_rh"].values
    valve_arr: np.ndarray   = df_valve["valve_state"].values
    
    Y: float = 1.0 / cfg.nutrient_consumption
    K_c: float = 5.0
    
    def get_env(t: float) -> float:
        idx = int(np.searchsorted(time_points, t, side="right") - 1)
        idx = max(0, min(idx, len(time_points) - 1))
        
        T = temp_arr[idx]
        H = hum_arr[idx]
        mod_T = np.exp(-((T - cfg.T_opt)**2) / (2 * 5.0**2))
        mod_H = np.exp(-((H - cfg.H_opt)**2) / (2 * 10.0**2))
        
        valve = valve_arr[idx]
        mod_valve = cfg.valve_restricted_mod if valve == 1 else 1.0
        
        return mod_T * mod_H * mod_valve

    def monod_ode(t: float, y: List[float], r_base: float) -> List[float]:
        N, C = y
        if N < 0: N = 0
        if C < 0: C = 0
        
        mod = get_env(t)
        r_eff = r_base * mod
        
        growth_rate = r_eff * N * (1.0 - N / cfg.K) * (C / (C + K_c))
        
        if C <= 0.1:
            growth_rate = -0.05 * N
            
        dNdt = growth_rate
        dCdt = -(1.0 / Y) * growth_rate if growth_rate > 0 else 0
        
        return [dNdt, dCdt]

    t_span: Tuple[float, float] = (time_points[0], time_points[-1])
    
    sol_ch2 = solve_ivp(monod_ode, t_span, [cfg.N0, cfg.initial_nutrients], t_eval=time_points, args=(cfg.ch2.r,), method="RK45")
    sol_ch3 = solve_ivp(monod_ode, t_span, [cfg.N0, cfg.initial_nutrients], t_eval=time_points, args=(cfg.ch3.r,), method="RK45")
    
    N_ch2, C_ch2 = sol_ch2.y
    N_ch3, C_ch3 = sol_ch3.y
    
    OD_ch2 = cfg.k_od600 * N_ch2 + np.random.normal(0, 0.02, size=len(N_ch2))
    OD_ch3 = cfg.k_od600 * N_ch3 + np.random.normal(0, 0.02, size=len(N_ch3))
    
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
    out_path = os.path.join(cfg.save_dir, "growth_output.csv")
    df_out.to_csv(out_path, index=False)
    
    logging.info(f"Saved {out_path} ({len(df_out)} rows)")

if __name__ == "__main__":
    run_biology()
