"""
growth_model.py
Owner: AIML-1 member
Purpose: Solves logistic ODE dN/dt = r*N*(1 - N/K) for two fungal strains
         in CH-2 and CH-3, modulated by valve_state (nutrient valve).
         Also computes OD600 proxy for camera-based biomass monitoring.

Outputs: data/growth_output.csv
Columns: time_hr, N_ch2, N_ch3, OD_ch2, OD_ch3

Biology parameters (BT member to validate):
  C. sphaerospermum (CH-2): r = 0.299 h⁻¹ (ISS study value)
  W. dermatitidis   (CH-3): r = 0.270 h⁻¹ (estimated from Chernobyl lit.)
  K (carrying capacity): ~1.0 g/L (normalized)
  N0 (inoculation):       0.01 g/L
"""

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import os

# ── Biological Parameters ─────────────────────────────────────────────────────
# CH-2: Cladosporium sphaerospermum (ISS baseline strain)
R_CH2 = 0.299          # h⁻¹ — validated from Shunk et al. 2020 (ISS study)
K_CH2 = 1.0            # g/L — normalized carrying capacity

# CH-3: Wangiella dermatitidis (challenger strain)
R_CH3 = 0.270          # h⁻¹ — BT member to verify from literature
K_CH3 = 1.0            # g/L

N0    = 0.01           # g/L — inoculation density (same for both)

# Valve modifier: nutrient restriction under high radiation (valve = OPEN means shielding open)
# When valve OPEN → cell exposure is higher → we REDUCE nutrient → r_eff = 0.5 * r
VALVE_OPEN_MODIFIER   = 0.5   # nutrient-limited growth during high-radiation event
VALVE_CLOSED_MODIFIER = 1.0   # full nutrient supply

# OD600 calibration constant (empirical): OD600 ≈ kOD * N
# Beer-Lambert: OD = log10(I0 / I_transmitted)
K_OD600 = 3.0          # OD600 per g/L  (typical for fungal cultures)

# ── Load valve state ──────────────────────────────────────────────────────────
df_valve = pd.read_csv("data/valve_state.csv")
time_points = df_valve["time_hr"].values
valve_arr   = df_valve["valve_state"].values

# Build interpolated valve state function
def get_modifier(t, strain="ch2"):
    idx = int(np.searchsorted(time_points, t, side="right") - 1)
    idx = max(0, min(idx, len(valve_arr) - 1))
    valve = valve_arr[idx]
    if valve == 1:      # OPEN — high radiation event, nutrient valve restricted
        return VALVE_OPEN_MODIFIER
    else:
        return VALVE_CLOSED_MODIFIER

# ── ODE definition ────────────────────────────────────────────────────────────
def logistic_ode(t, y, r, K, strain):
    N = y[0]
    mod = get_modifier(t, strain)
    r_eff = r * mod
    dNdt = r_eff * N * (1.0 - N / K)
    return [dNdt]

# ── Solve ODE for each chamber ────────────────────────────────────────────────
t_span = (time_points[0], time_points[-1])
t_eval = time_points

sol_ch2 = solve_ivp(
    logistic_ode,
    t_span, [N0],
    t_eval=t_eval,
    args=(R_CH2, K_CH2, "ch2"),
    method="RK45",
    dense_output=True
)

sol_ch3 = solve_ivp(
    logistic_ode,
    t_span, [N0],
    t_eval=t_eval,
    args=(R_CH3, K_CH3, "ch3"),
    method="RK45",
    dense_output=True
)

N_ch2 = sol_ch2.y[0]
N_ch3 = sol_ch3.y[0]

# ── OD600 proxy ───────────────────────────────────────────────────────────────
# OD600 = k * N  (linear proxy; camera reads light attenuation through culture)
OD_ch2 = K_OD600 * N_ch2
OD_ch3 = K_OD600 * N_ch3

# ── Save ──────────────────────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
df_out = pd.DataFrame({
    "time_hr": time_points,
    "N_ch2":   np.round(N_ch2, 6),
    "N_ch3":   np.round(N_ch3, 6),
    "OD_ch2":  np.round(OD_ch2, 6),
    "OD_ch3":  np.round(OD_ch3, 6),
})
df_out.to_csv("data/growth_output.csv", index=False)

print(f"[growth_model] Saved data/growth_output.csv  ({len(df_out)} rows)")
print(f"  CH-2 final N : {N_ch2[-1]:.4f} g/L  (r={R_CH2} h-1)")
print(f"  CH-3 final N : {N_ch3[-1]:.4f} g/L  (r={R_CH3} h-1)")
print(f"  CH-2 peak OD : {OD_ch2.max():.4f}")
print(f"  CH-3 peak OD : {OD_ch3.max():.4f}")
