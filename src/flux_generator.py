"""
flux_generator.py
Owner: EC / Aerospace member
Purpose: Generates a synthetic 48-hour LEO radiation flux profile
         (GCR baseline + SAA passage spikes) and saves to data/flux_profile.csv

ISS Orbit: 400 km altitude, 51.6 deg inclination
SAA passages: ~6 times per day for ISS-like orbit
"""

import numpy as np
import pandas as pd
import os

# ── Parameters ────────────────────────────────────────────────────────────────
DURATION_HRS   = 48          # total simulation time (hours)
TIME_STEP_HRS  = 1.0         # 1-hour resolution
GCR_BASELINE   = 200.0       # μGy/hr  — galactic cosmic ray background in LEO
SAA_PEAK       = 650.0       # μGy/hr  — South Atlantic Anomaly peak dose rate
SAA_DURATION   = 0.25        # hours   — SAA passage duration (~15 min)
SAA_PERIOD     = 90.0 / 60   # hours   — ISS orbital period (~1.5 hr)
NOISE_SIGMA    = 15.0        # μGy/hr  — sensor noise standard deviation

np.random.seed(42)           # reproducible

# ── Time array ────────────────────────────────────────────────────────────────
time_hr = np.arange(0, DURATION_HRS + TIME_STEP_HRS, TIME_STEP_HRS)

# ── Build flux profile ────────────────────────────────────────────────────────
flux = np.full_like(time_hr, GCR_BASELINE)

# Add SAA spikes: 6 per day → every ~4 hrs (simplified; real SAA ~6 passes/day)
SAA_INTERVAL_HRS = 4.0
for saa_center in np.arange(SAA_INTERVAL_HRS, DURATION_HRS, SAA_INTERVAL_HRS):
    for i, t in enumerate(time_hr):
        if abs(t - saa_center) < SAA_DURATION:
            # Gaussian spike profile
            flux[i] += (SAA_PEAK - GCR_BASELINE) * np.exp(
                -0.5 * ((t - saa_center) / (SAA_DURATION / 2)) ** 2
            )

# Add noise
flux += np.random.normal(0, NOISE_SIGMA, size=len(time_hr))
flux = np.clip(flux, 0, None)   # no negative flux

# ── Save ──────────────────────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
df = pd.DataFrame({"time_hr": time_hr, "flux_uGy_hr": np.round(flux, 3)})
df.to_csv("data/flux_profile.csv", index=False)

print(f"[flux_generator] Saved data/flux_profile.csv  ({len(df)} rows)")
print(f"  GCR baseline : {GCR_BASELINE} uGy/hr")
print(f"  SAA peak     : {flux.max():.1f} uGy/hr")
print(f"  Mean flux    : {flux.mean():.1f} uGy/hr")
