"""
attenuation.py
Owner: AIML-2 member
Purpose: Computes Beer-Lambert radiation attenuation for CH-2 and CH-3
         using biomass N(t) from growth_output.csv.

Physics (Beer-Lambert Law):
  x(t)   = alpha * N(t)              [effective melanin layer thickness, cm]
  I(t)   = I0(t) * exp(-mu * rho * x(t))   [attenuated flux, uGy/hr]
  Attn%  = (I0 - I(t)) / I0 * 100          [% attenuation vs CH-1 baseline]

Where:
  mu   = mass attenuation coefficient of melanin (cm^2/g)
  rho  = melanin density (g/cm^3)
  alpha = calibrated thickness per unit biomass (cm per g/L)
  I0   = CH-1 flux (pure agar, no shielding)

Calibration: alpha_ch2 set so that at peak N=1.0 g/L,
  Attn% = 2.17% (matches Shunk et al. 2020, ISS study)
  => mu * rho * alpha = -ln(1 - 0.0217) = 0.02194
  => alpha = 0.02194 / (0.043 * 1.4) = 0.364 cm per (g/L)

BT member validates: mu, rho values from melanin literature.
Expected CH-2 peak attenuation ~2.17%, CH-3 should be slightly higher.
"""

import numpy as np
import pandas as pd
import os

# ── Physical Parameters (BT member to validate) ───────────────────────────────
# C. sphaerospermum (CH-2) — DHN-melanin
MU_CH2    = 0.043       # cm^2/g — mass attenuation coefficient (DHN-melanin, gamma)
RHO_CH2   = 1.40        # g/cm^3 — melanin density
# Calibrated alpha: at N=1.0 g/L => Attn% = 2.17% (validated against ISS study)
# alpha = -ln(1 - 0.0217) / (MU * RHO) = 0.02194 / 0.0602 = 0.3645
ALPHA_CH2 = 0.3645      # cm per (g/L) — melanin layer thickness per unit biomass

# W. dermatitidis (CH-3) — DHN-melanin, higher density (Dadachova et al. 2008)
MU_CH3    = 0.043       # cm^2/g — same melanin type
RHO_CH3   = 1.45        # g/cm^3 — denser melanin (higher melanin content per cell)
# CH-3 has ~15% more melanin per biomass than C. sphaerospermum
ALPHA_CH3 = 0.4192      # cm per (g/L) — 15% higher than CH-2 alpha

# ── Load data ─────────────────────────────────────────────────────────────────
df_growth = pd.read_csv("data/growth_output.csv")
df_flux   = pd.read_csv("data/flux_profile.csv")

time_hr = df_growth["time_hr"].values
N_ch2   = df_growth["N_ch2"].values
N_ch3   = df_growth["N_ch3"].values
I0      = df_flux["flux_uGy_hr"].values      # CH-1 baseline flux (no attenuation)

# ── Effective melanin layer thickness x(t) ────────────────────────────────────
# x [cm] = alpha [cm/(g/L)] * N(t) [g/L]
delta_ch2 = ALPHA_CH2 * N_ch2    # cm
delta_ch3 = ALPHA_CH3 * N_ch3    # cm

# ── Beer-Lambert: I(t) = I0 * exp(-mu * rho * x(t)) ─────────────────────────
I_ch2 = I0 * np.exp(-MU_CH2 * RHO_CH2 * delta_ch2)
I_ch3 = I0 * np.exp(-MU_CH3 * RHO_CH3 * delta_ch3)

# ── Attenuation percentage ────────────────────────────────────────────────────
# Formula from CubeSat.html: Attn% = (CH1 - CHn) / CH1 * 100
attn_ch2_pct = (I0 - I_ch2) / I0 * 100
attn_ch3_pct = (I0 - I_ch3) / I0 * 100

# ── Save ──────────────────────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
df_out = pd.DataFrame({
    "time_hr":      time_hr,
    "delta_ch2":    np.round(delta_ch2,    6),
    "delta_ch3":    np.round(delta_ch3,    6),
    "I_ch2":        np.round(I_ch2,        3),
    "I_ch3":        np.round(I_ch3,        3),
    "attn_ch2_pct": np.round(attn_ch2_pct, 4),
    "attn_ch3_pct": np.round(attn_ch3_pct, 4),
})
df_out.to_csv("data/attenuation_output.csv", index=False)

print(f"[attenuation] Saved data/attenuation_output.csv  ({len(df_out)} rows)")
print(f"  CH-2 peak attenuation : {attn_ch2_pct.max():.3f}%  (expect ~2.17%)")
print(f"  CH-3 peak attenuation : {attn_ch3_pct.max():.3f}%  (challenger strain)")
if attn_ch2_pct.max() > attn_ch3_pct.max():
    print("  RESULT: C. sphaerospermum (CH-2) is the better bioshield")
else:
    print("  RESULT: W. dermatitidis (CH-3) is the better bioshield")
