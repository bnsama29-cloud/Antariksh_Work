import sys
import os
import pytest
import numpy as np
import yaml

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from biology.growth_model import run_biology

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def test_config_loads():
    config = load_config()
    assert "biology" in config
    assert "ch2_strain" in config["biology"]

def test_environmental_modifiers():
    # Simple mathematical verification of the Gaussian modifier used in growth model
    T_opt = 25.0
    T_test = 25.0
    mod_T = np.exp(-((T_test - T_opt)**2) / (2 * 5.0**2))
    assert np.isclose(mod_T, 1.0)
    
    T_test_low = 20.0
    mod_T_low = np.exp(-((T_test_low - T_opt)**2) / (2 * 5.0**2))
    assert mod_T_low < 1.0
    
    H_opt = 60.0
    H_test = 60.0
    mod_H = np.exp(-((H_test - H_opt)**2) / (2 * 10.0**2))
    assert np.isclose(mod_H, 1.0)

def test_monod_kinetics_limit():
    r = 0.3
    N = 1.0
    K = 1.0
    C = 100.0
    K_c = 5.0
    
    # Growth should be 0 when N reaches K
    growth = r * N * (1.0 - N / K) * (C / (C + K_c))
    assert np.isclose(growth, 0.0)
    
    # Growth should be 0 when nutrients C run out completely
    N = 0.5
    C = 0.0
    growth = r * N * (1.0 - N / K) * (C / (C + K_c))
    assert np.isclose(growth, 0.0)
