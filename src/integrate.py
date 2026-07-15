"""
integrate.py
Owner: CS member
Purpose: Merges all module CSV outputs into a single master_log.csv.
         Runs sanity checks. Prints key metrics.

Expected columns in master_log.csv:
  time_hr, flux_uGy_hr, valve_state,
  N_ch2, N_ch3, OD_ch2, OD_ch3,
  delta_ch2, delta_ch3, I_ch2, I_ch3,
  attn_ch2_pct, attn_ch3_pct
"""

import pandas as pd
import os

# ── Load all module outputs ───────────────────────────────────────────────────
print("[integrate] Loading module outputs...")
flux   = pd.read_csv("data/flux_profile.csv")
valve  = pd.read_csv("data/valve_state.csv")
growth = pd.read_csv("data/growth_output.csv")
attn   = pd.read_csv("data/attenuation_output.csv")

# ── Merge on time_hr (inner join — all modules must align) ────────────────────
master = flux.merge(valve,  on="time_hr") \
             .merge(growth, on="time_hr") \
             .merge(attn,   on="time_hr")

# ── Sanity checks ─────────────────────────────────────────────────────────────
nan_count = master.isnull().sum().sum()
if nan_count > 0:
    print(f"  WARNING: {nan_count} NaN values found -- check time alignment across CSVs")
else:
    print("  NaN check PASSED (0 NaNs)")

peak_ch2 = master["attn_ch2_pct"].max()
if peak_ch2 > 10.0:
    print(f"  WARNING: CH-2 attenuation {peak_ch2:.2f}% exceeds 10% -- check alpha, mu with BT")
elif peak_ch2 < 0.5:
    print(f"  WARNING: CH-2 attenuation {peak_ch2:.3f}% is very low -- verify biological parameters")
else:
    print(f"  Attenuation range check PASSED ({peak_ch2:.3f}%)")

# ── Save master log ───────────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
master.to_csv("data/master_log.csv", index=False)

# ── Print summary ─────────────────────────────────────────────────────────────
print(f"\n[integrate] Saved data/master_log.csv  ({len(master)} rows x {len(master.columns)} cols)")
print(f"\n  === KEY RESULTS ===")
print(f"  Peak CH-2 attenuation (C. sphaerospermum) : {master['attn_ch2_pct'].max():.3f}%")
print(f"  Peak CH-3 attenuation (W. dermatitidis)   : {master['attn_ch3_pct'].max():.3f}%")
print(f"  Mean flux      : {master['flux_uGy_hr'].mean():.1f} uGy/hr")
print(f"  Total OPEN hrs : {master['valve_state'].sum()} / {len(master)} hrs")
print(f"  CH-2 final N   : {master['N_ch2'].iloc[-1]:.4f} g/L")
print(f"  CH-3 final N   : {master['N_ch3'].iloc[-1]:.4f} g/L")

if master["attn_ch3_pct"].max() > master["attn_ch2_pct"].max():
    winner = "W. dermatitidis (CH-3) -- CHALLENGER WINS"
else:
    winner = "C. sphaerospermum (CH-2) -- BASELINE HOLDS"
print(f"\n  CONCLUSION: Better bioshield --> {winner}")
print("\n  Running Power Simulation...")
import power_sim
power_sim.generate_power_log()

print("\n  All checks complete.")
