"""
flux_generator.py
Generates the simulated Low Earth Orbit environment (Radiation, Temperature, Humidity).
"""

import numpy as np
import pandas as pd
import yaml
import os
import logging
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EnvironmentConfig:
    duration_hrs: float
    time_step_hrs: float
    save_dir: str
    gcr_baseline: float
    saa_peak: float
    saa_duration: float
    saa_interval: float
    noise_sigma: float
    temp_nominal: float
    temp_fluctuation: float
    temp_std_noise: float
    hum_nominal: float
    hum_fluctuation: float
    hum_std_noise: float
    fault_sensor_failure: bool
    fault_start_hr: float

def load_config(config_path: str = "config.yaml") -> EnvironmentConfig:
    with open(config_path, 'r', encoding="utf-8") as f:
        raw: Dict[str, Any] = yaml.safe_load(f)
    
    return EnvironmentConfig(
        duration_hrs=float(raw["experiment"]["duration_hrs"]),
        time_step_hrs=float(raw["experiment"]["time_step_hrs"]),
        save_dir=str(raw["experiment"]["save_dir"]),
        gcr_baseline=float(raw["environment"]["radiation"]["gcr_baseline"]),
        saa_peak=float(raw["environment"]["radiation"]["saa_peak"]),
        saa_duration=float(raw["environment"]["radiation"]["saa_duration"]),
        saa_interval=float(raw["environment"]["radiation"]["saa_interval"]),
        noise_sigma=float(raw["environment"]["radiation"]["noise_sigma"]),
        temp_nominal=float(raw["environment"]["temperature"]["nominal"]),
        temp_fluctuation=float(raw["environment"]["temperature"]["fluctuation"]),
        temp_std_noise=float(raw["environment"]["temperature"]["std_noise"]),
        hum_nominal=float(raw["environment"]["humidity"]["nominal"]),
        hum_fluctuation=float(raw["environment"]["humidity"]["fluctuation"]),
        hum_std_noise=float(raw["environment"]["humidity"]["std_noise"]),
        fault_sensor_failure=bool(raw.get("fault_injection", {}).get("sensor_failure", False)),
        fault_start_hr=float(raw.get("fault_injection", {}).get("sensor_failure_start_hr", 24.0))
    )

def generate_environment() -> None:
    logging.info("Generating environmental data...")
    cfg: EnvironmentConfig = load_config()
    
    np.random.seed(42)

    time_hr = np.arange(0, cfg.duration_hrs + cfg.time_step_hrs, cfg.time_step_hrs)
    
    # Radiation Flux
    flux = np.full_like(time_hr, cfg.gcr_baseline)
    for saa_center in np.arange(cfg.saa_interval, cfg.duration_hrs, cfg.saa_interval):
        for i, t in enumerate(time_hr):
            if abs(t - saa_center) < cfg.saa_duration:
                flux[i] += (cfg.saa_peak - cfg.gcr_baseline) * np.exp(
                    -0.5 * ((t - saa_center) / (cfg.saa_duration / 2)) ** 2
                )
    
    flux += np.random.normal(0, cfg.noise_sigma, size=len(time_hr))
    flux = np.clip(flux, 0, None)
    
    # Fault Injection: Sensor failure
    if cfg.fault_sensor_failure:
        fault_idx = time_hr >= cfg.fault_start_hr
        flux[fault_idx] = 0.0
        logging.warning(f"FAULT INJECTED: Radiation sensor failed at T={cfg.fault_start_hr}h")
    
    # Temperature
    orbit_period = 1.5
    temp = cfg.temp_nominal + cfg.temp_fluctuation * np.sin(2 * np.pi * time_hr / orbit_period)
    temp += np.random.normal(0, cfg.temp_std_noise, size=len(time_hr))
    
    # Humidity
    humidity = cfg.hum_nominal + cfg.hum_fluctuation * np.cos(2 * np.pi * time_hr / orbit_period)
    humidity += np.random.normal(0, cfg.hum_std_noise, size=len(time_hr))
    
    os.makedirs(cfg.save_dir, exist_ok=True)
    
    df = pd.DataFrame({
        "time_hr": time_hr, 
        "flux_uGy_hr": np.round(flux, 3),
        "temperature_c": np.round(temp, 2),
        "humidity_rh": np.round(humidity, 2)
    })
    
    out_path = os.path.join(cfg.save_dir, "environment.csv")
    df.to_csv(out_path, index=False)
    logging.info(f"Saved {out_path} ({len(df)} rows)")

if __name__ == "__main__":
    generate_environment()
