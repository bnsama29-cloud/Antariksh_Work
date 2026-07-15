import os

with open('src/dashboard.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Modify Figure 2
fig2_old = """ax.plot(t, df["N_ch2"], color=ACCENT2, lw=2, label="CH-2: C. sphaerospermum")
ax.plot(t, df["N_ch3"], color=CH3_COLOR, lw=2, ls="--", label="CH-3: W. dermatitidis")"""

fig2_new = """ax.plot(t, df["N_ch2"], color=ACCENT2, lw=2, label="CH-2: C. sphaerospermum")
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
"""

if fig2_old in content:
    content = content.replace(fig2_old, fig2_new)
    # Fix the legend handles
    content = content.replace('ax.legend(fontsize=9, facecolor="#131727", edgecolor="#1e2540")', 'ax.legend(handles=handles, fontsize=9, facecolor="#131727", edgecolor="#1e2540")')

# 2. Append new Figures
new_figs = """
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

print("\\n[dashboard] All 7 figures exported to figures/ at 300 DPI")
"""

content = content.replace('print("\\n[dashboard] All 4 figures exported to figures/ at 300 DPI")', new_figs)
content = content.replace('print("  Insert into TA report as Fig 1-4 per the format checklist.")', 'print("  Insert into TA report as Fig 1-7 per the format checklist.")')

with open('src/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
