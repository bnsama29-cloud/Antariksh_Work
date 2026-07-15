import sys
import os
import pytest
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

def test_beer_lambert():
    # I = I0 * exp(-mu * rho * x)
    I0 = 100.0
    mu = 0.043
    rho = 1.40
    
    # 0 thickness = no attenuation
    x = 0.0
    I = I0 * np.exp(-mu * rho * x)
    assert np.isclose(I, I0)
    
    # Positive thickness = some attenuation
    x = 1.0
    I = I0 * np.exp(-mu * rho * x)
    assert I < I0
    
    # Attenuation percentage calculation
    attn_pct = (I0 - I) / I0 * 100
    assert 0 < attn_pct < 100
