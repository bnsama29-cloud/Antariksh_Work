"""
dashboard.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import yaml

def load_config(config_path="config.yaml"):
    with open(config_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_dashboard():
    logging.info("Generating dashboard figures...")
    config = load_config()
    save_dir = config["experiment"]["save_dir"]
    master_csv = os.path.join(save_dir, "master_log.csv")
    
    df = pd.read_csv(master_csv)
    t  = df["time_hr"].values
    
    os.makedirs("figures", exist_ok=True)
    
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
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig.patch.set_facecolor("#0c0f1a")
    
    ax1.plot(t, df["flux_uGy_hr"], color=ACCENT, lw=1.5)
    ax1.axhline(500, color=VALVE_COLOR, ls="--", lw=1, alpha=0.7)
    ax1.set_ylabel("Flux (μGy/hr)")
    ax1.set_title("Environment: Radiation Flux", color=BRIGHT)
    
    ax2.plot(t, df["temperature_c"], color=WARN, lw=1.5)
    ax2.set_ylabel("Temp (C)")
    ax2.set_title("Environment: Temperature", color=BRIGHT)
    
    ax3.plot(t, df["humidity_rh"], color=ACCENT2, lw=1.5)
    ax3.set_ylabel("Humidity (%)")
    ax3.set_xlabel("Time (hr)")
    ax3.set_title("Environment: Humidity", color=BRIGHT)
    
    plt.tight_layout()
    plt.savefig("figures/fig1_environment.png", dpi=300, facecolor=fig.get_facecolor())
    plt.close()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.patch.set_facecolor("#0c0f1a")
    
    ax1.plot(t, df["N_ch2"], color=ACCENT2, lw=2, label="CH-2 (C. sphaerospermum)")
    ax1.plot(t, df["N_ch3"], color=CH3_COLOR, lw=2, ls="--", label="CH-3 (W. dermatitidis)")
    ax1.set_ylabel("Biomass [g/L]")
    ax1.set_title("Fungal Biomass Growth", color=BRIGHT)
    ax1.legend(facecolor="#131727", edgecolor="#1e2540")
    
    ax2.plot(t, df["C_ch2"], color=ACCENT2, lw=2, label="CH-2 Nutrients")
    ax2.plot(t, df["C_ch3"], color=CH3_COLOR, lw=2, ls="--", label="CH-3 Nutrients")
    ax2.set_ylabel("Nutrients [mg]")
    ax2.set_xlabel("Time (hr)")
    ax2.set_title("Nutrient Depletion", color=BRIGHT)
    ax2.legend(facecolor="#131727", edgecolor="#1e2540")
    
    plt.tight_layout()
    plt.savefig("figures/fig2_biology.png", dpi=300, facecolor=fig.get_facecolor())
    plt.close()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0c0f1a")
    
    ax.plot(t, df["attn_ch2_pct"], color=ACCENT2, lw=2, label="CH-2: C. sphaerospermum")
    ax.plot(t, df["attn_ch3_pct"], color=CH3_COLOR, lw=2, ls="--", label="CH-3: W. dermatitidis")
    ax.set_ylabel("Attenuation (%)")
    ax.set_xlabel("Time (hr)")
    ax.set_title("Radiation Attenuation vs Baseline", color=BRIGHT)
    ax.legend(facecolor="#131727", edgecolor="#1e2540")
    
    plt.tight_layout()
    plt.savefig("figures/fig3_attenuation.png", dpi=300, facecolor=fig.get_facecolor())
    plt.close()
    
    logging.info("Saved figures/fig1_environment.png, fig2_biology.png, fig3_attenuation.png")

if __name__ == "__main__":
    run_dashboard()
