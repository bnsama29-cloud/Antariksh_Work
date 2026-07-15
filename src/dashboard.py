"""
dashboard.py
Owner: CS member
Purpose: Generates 4 required figures from master_log.csv and saves
         as 300 DPI PNGs for the TA report.

Figures produced:
  Fig 1: Radiation flux vs. time with valve state overlay
  Fig 2: Biomass growth curves — CH-2 vs. CH-3
  Fig 3: Attenuation % vs. time — CH-2 vs. CH-3 comparison
  Fig 4: OD600 proxy vs. time (auxiliary computer camera output)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── Style ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0c0f1a",
    "axes.facecolor":    "#131727",
    "axes.edgecolor":    "#1e2540",
    "axes.labelcolor":   "#d8dff0",
    "xtick.color":       "#6b7699",
    "ytick.color":       "#6b7699",
    "text.color":        "#d8dff0",
    "grid.color":        "#1e2540",
    "grid.linestyle":    "--",
    "axes.grid":         True,
    "font.family":       "monospace",
    "axes.titlesize":    12,
    "axes.labelsize":    10,
})

ACCENT      = "#4f7fff"
ACCENT2     = "#00d4a0"
WARN        = "#f0a500"
BRIGHT      = "#ffffff"
VALVE_COLOR = "#e05c5c"
CH3_COLOR   = "#b06fff"

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("data/master_log.csv")
t  = df["time_hr"].values

os.makedirs("figures", exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1: Radiation Flux + Valve State
# ══════════════════════════════════════════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor("#0c0f1a")

ax1.plot(t, df["flux_uGy_hr"], color=ACCENT, lw=1.5, label="Radiation Flux (μGy/hr)")
ax1.axhline(500, color=VALVE_COLOR, ls="--", lw=1, alpha=0.7, label="Upper threshold (500 μGy/hr)")
ax1.axhline(350, color=ACCENT2,    ls="--", lw=1, alpha=0.7, label="Lower threshold (350 μGy/hr)")
ax1.set_ylabel("Flux (μGy/hr)")
ax1.set_xlabel("Time (hr)")
ax1.set_title("Fig 1: LEO Radiation Flux & Hysteresis Valve State", color=BRIGHT, fontweight="bold")

# Shade OPEN valve regions
valve = df["valve_state"].values
in_open = False
for i in range(len(t)):
    if valve[i] == 1 and not in_open:
        open_start = t[i]
        in_open = True
    elif valve[i] == 0 and in_open:
        ax1.axvspan(open_start, t[i], alpha=0.15, color=VALVE_COLOR, label="_nolegend_")
        in_open = False
if in_open:
    ax1.axvspan(open_start, t[-1], alpha=0.15, color=VALVE_COLOR)

valve_patch = mpatches.Patch(color=VALVE_COLOR, alpha=0.3, label="Valve OPEN (SAA event)")
handles, labels = ax1.get_legend_handles_labels()
handles.append(valve_patch)
ax1.legend(handles=handles, fontsize=8, facecolor="#131727", edgecolor="#1e2540")

plt.tight_layout()
plt.savefig("figures/fig1_flux_valve.png", dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("  Saved figures/fig1_flux_valve.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2: Biomass Growth Curves — CH-2 vs CH-3
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#0c0f1a")

ax.plot(t, df["N_ch2"], color=ACCENT2, lw=2, label="CH-2: C. sphaerospermum")
ax.plot(t, df["N_ch3"], color=CH3_COLOR, lw=2, ls="--", label="CH-3: W. dermatitidis")

# Shade OPEN valve regions in Fig 2
in_open = False
for i in range(len(t)):
    if valve[i] == 1 and not in_open:
        open_start = t[i]
        in_open = True
    elif valve[i] == 0 and in_open:
        ax.axvspan(open_start, t[i], alpha=0.1, color=VALVE_COLOR, label="_nolegend_")
        in_open = False
if in_open:
    ax.axvspan(open_start, t[-1], alpha=0.1, color=VALVE_COLOR)

valve_patch_2 = mpatches.Patch(color=VALVE_COLOR, alpha=0.1, label="Valve OPEN (Growth Suppressed)")
handles, labels = ax.get_legend_handles_labels()
handles.append(valve_patch_2)

ax.axhline(1.0, color=WARN, ls=":", lw=1, alpha=0.5, label="Carrying capacity K = 1.0 g/L")
ax.set_ylabel("Biomass N(t) [g/L]")
ax.set_xlabel("Time (hr)")
ax.set_title("Fig 2: Fungal Biomass Growth — Logistic ODE Model", color=BRIGHT, fontweight="bold")
ax.legend(handles=handles, fontsize=9, facecolor="#131727", edgecolor="#1e2540")

plt.tight_layout()
plt.savefig("figures/fig2_growth_curves.png", dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("  Saved figures/fig2_growth_curves.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3: Attenuation % Comparison — CH-2 vs CH-3
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#0c0f1a")

ax.plot(t, df["attn_ch2_pct"], color=ACCENT2, lw=2,
        label="CH-2: C. sphaerospermum")
ax.plot(t, df["attn_ch3_pct"], color=CH3_COLOR, lw=2, ls="--",
        label="CH-3: W. dermatitidis")
ax.axhline(2.17, color=WARN, ls=":", lw=1, alpha=0.7,
           label="ISS reference: 2.17% (Shunk 2020)")
ax.fill_between(t, df["attn_ch2_pct"], df["attn_ch3_pct"],
                alpha=0.08, color=ACCENT, label="Differential shielding")
ax.set_ylabel("Attenuation (%)")
ax.set_xlabel("Time (hr)")
ax.set_title("Fig 3: Radiation Attenuation — CH-2 vs CH-3 (vs CH-1 baseline)", color=BRIGHT, fontweight="bold")
ax.legend(handles=handles, fontsize=9, facecolor="#131727", edgecolor="#1e2540")

# Annotate peak
peak_idx = df["attn_ch2_pct"].idxmax()
ax.annotate(f"CH-2 peak: {df['attn_ch2_pct'].max():.2f}%",
            xy=(t[peak_idx], df["attn_ch2_pct"].max()),
            xytext=(t[peak_idx] - 6, df["attn_ch2_pct"].max() + 0.05),
            arrowprops=dict(arrowstyle="->", color=ACCENT2),
            color=ACCENT2, fontsize=8)

plt.tight_layout()
plt.savefig("figures/fig3_attenuation.png", dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("  Saved figures/fig3_attenuation.png")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4: OD600 Proxy (Auxiliary Computer Camera Sim)
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#0c0f1a")

ax.plot(t, df["OD_ch2"], color=ACCENT2, lw=2, label="CH-2 OD600 (C. sphaerospermum)")
ax.plot(t, df["OD_ch3"], color=CH3_COLOR, lw=2, ls="--", label="CH-3 OD600 (W. dermatitidis)")
ax.set_ylabel("OD600 (Optical Density)")
ax.set_xlabel("Time (hr)")
ax.set_title("Fig 4: OD600 Proxy — Auxiliary Computer Camera Simulation", color=BRIGHT, fontweight="bold")
ax.legend(handles=handles, fontsize=9, facecolor="#131727", edgecolor="#1e2540")

plt.tight_layout()
plt.savefig("figures/fig4_od600_proxy.png", dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("  Saved figures/fig4_od600_proxy.png")


# =================================================================================================================
# FIGURE 5: Power Budget (Battery Charge)
# =================================================================================================================
try:
    df_pwr = pd.read_csv("data/power_log.csv")
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0c0f1a")
    ax.plot(df_pwr["time_hr"], df_pwr["battery_charge_mwh"], color="#4caf50", lw=2, label="Battery Charge (mWh)")
    ax.axhline(6660, color=BRIGHT, ls=":", lw=1, alpha=0.5, label="Max Capacity (6660 mWh)")
    ax.set_ylabel("Charge (mWh)")
    ax.set_xlabel("Time (hr)")
    ax.set_ylim(0, 7000)
    ax.set_title("Fig 5: Power Budget Feasibility (48h)", color=BRIGHT, fontweight="bold")
    ax.legend(fontsize=9, facecolor="#131727", edgecolor="#1e2540")
    plt.tight_layout()
    plt.savefig("figures/fig5_power_budget.png", dpi=300, facecolor=fig.get_facecolor())
    plt.close()
    print("  Saved figures/fig5_power_budget.png")
except Exception as e:
    print("  Warning: Could not plot Fig 5 (Power Budget):", e)

# =================================================================================================================
# FIGURE 6: Valve Timeline
# =================================================================================================================
fig, ax = plt.subplots(figsize=(10, 3))
fig.patch.set_facecolor("#0c0f1a")
ax.step(t, df["valve_state"], color=VALVE_COLOR, lw=2, where="post")
ax.set_yticks([0, 1])
ax.set_yticklabels(["CLOSED (Normal)", "OPEN (SAA Spike)"], color=BRIGHT)
ax.set_xlabel("Time (hr)")
ax.set_title("Fig 6: Hysteresis Valve State Timeline", color=BRIGHT, fontweight="bold")
plt.tight_layout()
plt.savefig("figures/fig6_valve_timeline.png", dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("  Saved figures/fig6_valve_timeline.png")

# =================================================================================================================
# FIGURE 7: OD600 vs Biomass Correlation
# =================================================================================================================
fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("#0c0f1a")
ax.plot(df["N_ch2"], df["OD_ch2"], color=ACCENT2, lw=2, label="CH-2 Calibration")
ax.plot(df["N_ch3"], df["OD_ch3"], color=CH3_COLOR, lw=2, ls="--", label="CH-3 Calibration")
ax.set_xlabel("Biomass N(t) [g/L]")
ax.set_ylabel("OD600 (Optical Density)")
ax.set_title("Fig 7: OD600 vs Biomass Linear Calibration", color=BRIGHT, fontweight="bold")
ax.legend(fontsize=9, facecolor="#131727", edgecolor="#1e2540")
plt.tight_layout()
plt.savefig("figures/fig7_od600_correlation.png", dpi=300, facecolor=fig.get_facecolor())
plt.close()
print("  Saved figures/fig7_od600_correlation.png")

print("\n[dashboard] All 7 figures exported to figures/ at 300 DPI")

print("  Insert into TA report as Fig 1-7 per the format checklist.")
