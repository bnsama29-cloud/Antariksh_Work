"""
hysteresis.py
Owner: EC member
Purpose: Hysteresis controller — reads flux_profile.csv,
         outputs valve_state.csv (1 = OPEN, 0 = CLOSED)

Control Logic (pure hysteresis, NO PID):
  - If flux > UPPER_THRESH  → valve = OPEN  (1)
  - If flux < LOWER_THRESH  → valve = CLOSED (0)
  - Otherwise               → HOLD current state (deadband)

Thresholds (from CubeSat.html):
  UPPER_THRESH = 500 μGy/hr
  LOWER_THRESH = 350 μGy/hr
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ── Thresholds ────────────────────────────────────────────────────────────────
UPPER_THRESH = 500.0    # μGy/hr — valve opens  (high radiation → protect cells)
LOWER_THRESH = 350.0    # μGy/hr — valve closes (radiation safe → resume nutrients)
INITIAL_VALVE = 0       # start CLOSED

# ── Load flux ─────────────────────────────────────────────────────────────────
df_flux = pd.read_csv("data/flux_profile.csv")
time_hr = df_flux["time_hr"].values
flux    = df_flux["flux_uGy_hr"].values

# ── Hysteresis loop ───────────────────────────────────────────────────────────
valve_state = np.zeros(len(time_hr), dtype=int)
current_valve = INITIAL_VALVE

for i, f in enumerate(flux):
    if f > UPPER_THRESH:
        current_valve = 1       # OPEN  — high radiation event
    elif f < LOWER_THRESH:
        current_valve = 0       # CLOSE — safe to re-expose
    # else: HOLD — deadband, no change
    valve_state[i] = current_valve

# ── Save CSV ──────────────────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
df_out = pd.DataFrame({"time_hr": time_hr, "valve_state": valve_state})
df_out.to_csv("data/valve_state.csv", index=False)

# ── Standalone validation plot ────────────────────────────────────────────────
os.makedirs("figures", exist_ok=True)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

ax1.plot(time_hr, flux, color="#4f7fff", lw=1.5, label="Flux (μGy/hr)")
ax1.axhline(UPPER_THRESH, color="#e05c5c", ls="--", lw=1, label=f"Upper = {UPPER_THRESH}")
ax1.axhline(LOWER_THRESH, color="#00d4a0", ls="--", lw=1, label=f"Lower = {LOWER_THRESH}")
ax1.set_ylabel("Flux (μGy/hr)")
ax1.legend(fontsize=8)
ax1.set_title("Hysteresis Controller — Flux & Valve State")
ax1.grid(True, alpha=0.3)

ax2.step(time_hr, valve_state, where="post", color="#f0a500", lw=1.5)
ax2.set_yticks([0, 1])
ax2.set_yticklabels(["CLOSED", "OPEN"])
ax2.set_xlabel("Time (hr)")
ax2.set_ylabel("Valve State")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figures/hysteresis_validation.png", dpi=300)
plt.close()

print(f"[hysteresis] Saved data/valve_state.csv  ({len(df_out)} rows)")
print(f"  OPEN events  : {valve_state.sum()} hrs")
print(f"  CLOSED events: {(1 - valve_state).sum()} hrs")
print("  Validation plot saved to figures/hysteresis_validation.png")
