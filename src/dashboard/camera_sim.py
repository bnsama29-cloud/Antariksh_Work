"""
camera_sim.py
Generates synthetic Raspberry Pi camera images simulating fungal growth inside the Lab-on-Chip chambers.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
import os
import logging
from typing import Dict, Any

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    with open(config_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def generate_chamber_image(N_ch2: float, N_ch3: float, time_hr: float, output_path: str):
    """
    Generates a synthetic grayscale image of the 3 LOC chambers.
    CH1: Control (Empty)
    CH2: C. sphaerospermum
    CH3: W. dermatitidis
    """
    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor('#1a1a24')
    ax.set_facecolor('#1a1a24')
    
    # 3 Chambers
    centers = [1, 4, 7]
    names = ["CH-1 (Control)", "CH-2 (C. sphaero)", "CH-3 (W. derma)"]
    biomass_vals = [0.0, N_ch2, N_ch3]
    
    for i, cx in enumerate(centers):
        # Draw agar base (lighter gray)
        agar = plt.Circle((cx, 1.5), 1.2, color='#2c2c38', zorder=1)
        ax.add_patch(agar)
        
        # Add random noise to simulate agar texture
        noise_x = cx + (np.random.rand(100) - 0.5) * 2.2
        noise_y = 1.5 + (np.random.rand(100) - 0.5) * 2.2
        
        # Keep noise inside circle
        dist = np.sqrt((noise_x - cx)**2 + (noise_y - 1.5)**2)
        valid = dist < 1.1
        ax.scatter(noise_x[valid], noise_y[valid], s=2, color='#3a3a48', alpha=0.5, zorder=2)
        
        # Draw fungal colony (dark spots, density based on biomass)
        biomass = biomass_vals[i]
        if biomass > 0.05:
            # Number of spots scales with biomass (up to ~500)
            n_spots = int(biomass * 500)
            
            # Scatter spots clustered towards center
            r = np.random.normal(0, 0.4 + (biomass * 0.3), n_spots)
            theta = np.random.uniform(0, 2 * np.pi, n_spots)
            fx = cx + r * np.cos(theta)
            fy = 1.5 + r * np.sin(theta)
            
            # Clip to chamber
            f_dist = np.sqrt((fx - cx)**2 + (fy - 1.5)**2)
            f_valid = f_dist < 1.1
            
            ax.scatter(fx[f_valid], fy[f_valid], s=8, color='#0d0d12', alpha=0.7, zorder=3)
            
            # Add a central dense mass
            dense_r = np.random.uniform(0, 0.2 + (biomass * 0.2), int(n_spots/2))
            dense_theta = np.random.uniform(0, 2 * np.pi, int(n_spots/2))
            dx = cx + dense_r * np.cos(dense_theta)
            dy = 1.5 + dense_r * np.sin(dense_theta)
            ax.scatter(dx, dy, s=15, color='#050508', alpha=0.9, zorder=4)
        
        # Label
        ax.text(cx, -0.3, names[i], color='white', ha='center', fontsize=10, family='monospace')
        
    ax.set_xlim(0, 8)
    ax.set_ylim(-0.5, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add timestamp
    ax.text(0.2, 2.7, f"T = {time_hr:04.1f} hrs", color='red', family='monospace', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

def run_camera_sim() -> None:
    logging.info("Generating synthetic camera images...")
    config = load_config()
    save_dir = config["experiment"]["save_dir"]
    
    growth_path = os.path.join(save_dir, "growth_output.csv")
    if not os.path.exists(growth_path):
        logging.error(f"Cannot run camera_sim: {growth_path} not found.")
        return
        
    df = pd.read_csv(growth_path)
    
    cam_dir = "figures/camera"
    os.makedirs(cam_dir, exist_ok=True)
    
    # We will generate images every 4 hours to avoid clutter
    sample_intervals = np.arange(0, config["experiment"]["duration_hrs"] + 1, 4.0)
    
    count = 0
    for t in sample_intervals:
        # Find closest row
        idx = (np.abs(df['time_hr'] - t)).argmin()
        row = df.iloc[idx]
        
        out_path = os.path.join(cam_dir, f"img_{int(t):02d}h.png")
        generate_chamber_image(row['N_ch2'], row['N_ch3'], row['time_hr'], out_path)
        count += 1
        
    logging.info(f"Generated {count} synthetic images in {cam_dir}/")

if __name__ == "__main__":
    run_camera_sim()
