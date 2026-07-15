import re
import os

print("--- Fixing README.md ---")
with open('README.md', 'r', encoding='utf-8') as f:
    md = f.read()

# I will just replace the entire block of figures in README
new_fig_blocks = """### Fig 1 - LEO Radiation Flux Profile & Hysteresis Valve State
> Simulates a typical 48-hour LEO orbit crossing the South Atlantic Anomaly (SAA) ~6 times per day. The red shaded regions show exactly when our controller forces the nutrient valve OPEN based on radiation levels.

![Fig 1: Radiation flux with SAA spikes and valve state](src/figures/fig1_flux_valve.png)

---

### Fig 2 - Valve State Timeline
> A discrete step-plot showing the precise timing and duration of the 11 hysteresis valve actuations during South Atlantic Anomaly passes.

![Fig 2: Valve Timeline](src/figures/fig6_valve_timeline.png)

---

### Fig 3 - Fungal Biomass Growth (Logistic S-Curve)
> Microgravity stimulates a 23% increase in *C. sphaerospermum* intrinsic growth rate. Both fungi successfully reach the 1.0 g/L carrying capacity. The slight slope variations align perfectly with the nutrient restrictions applied when the valve is OPEN.

![Fig 3: Logistic growth curves for both strains](src/figures/fig2_growth_curves.png)

---

### Fig 4 - OD600 Correlation
> Demonstrates the linear calibration relationship (K_OD600 = 3.0) between the simulated fungal biomass and the optical density proxy measurement.

![Fig 4: OD600 Correlation](src/figures/fig7_od600_correlation.png)

---

### Fig 5 - OD600 Camera Proxy (What the Camera Sees)
> OD600 (Optical Density at 600 nm wavelength) is a standard measure of how cloudy a culture is - cloudier = more biomass. The auxiliary Raspberry Pi camera tracks this as a proxy for growth.

![Fig 5: OD600 optical density proxy over time](src/figures/fig4_od600_proxy.png)

---

### Fig 6 - Radiation Attenuation Comparison — The Main Result
> CH-3 (*W. dermatitidis*) consistently attenuates more radiation than CH-2. The ISS reference line (2.17%) confirms our model is correctly calibrated. The shaded area shows CH-3's advantage.

![Fig 6: Attenuation comparison with ISS reference line](src/figures/fig3_attenuation.png)

---

### Fig 7 - Power Budget Feasibility
> A critical engineering requirement. This simulation models the continuous duty-cycled average draw (387 mW) against the 0.5U solar panel generation (~750 mW during sunlit phases). The net positive generation keeps the 6.66 Wh battery at maximum capacity for the full 48-hour mission.

![Fig 7: Power Budget](src/figures/fig5_power_budget.png)

---

### Fig 8 - Hysteresis Controller Validation
> Validates the control logic: valve switches OPEN when flux crosses 500 μGy/hr (upper line), and only closes when flux drops below 350 μGy/hr (lower line). The gap between thresholds = deadband (prevents rapid switching).

![Fig 8: Hysteresis validation plot](src/figures/hysteresis_validation.png)"""

# Find the start of Fig 1 and end of Fig 5 in the old readme
start_idx = md.find('### Fig 1 - LEO Radiation Flux Profile')
end_idx = md.find('## 💻 Electronics Simulation', start_idx)

md = md[:start_idx] + new_fig_blocks + '\n\n' + md[end_idx:]

# Fix wokwi figs
md = md.replace('Fig 6: Wokwi valve CLOSED', 'Fig 9: Wokwi valve CLOSED')
md = md.replace('Fig 7: Wokwi valve OPEN', 'Fig 10: Wokwi valve OPEN')
md = md.replace('Fig 8: Wokwi valve OPEN holding', 'Fig 11: Wokwi valve OPEN holding')

# Fix CAD figs
md = md.replace('Fig 10: Isometric', 'Fig 13: Isometric')
md = md.replace('Fig 11: Section', 'Fig 14: Section')
md = md.replace('Fig 12: Exploded', 'Fig 15: Exploded')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(md)


print("--- Fixing LOC_CubeSat_Report.html ---")
with open('LOC_CubeSat_Report.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix TOC exactly
old_toc = """    <div class="toc-entry"><span>Fig 1: LEO Radiation Flux Profile with Hysteresis Valve State Overlay</span>
      <div class="dots"></div><span>11</span>
    </div>
    <div class="toc-entry"><span>Fig 2: Fungal Biomass Growth - Logistic ODE (CH-2 vs CH-3)</span>
      <div class="dots"></div><span>12</span>
    </div>
    <div class="toc-entry"><span>Fig 3: Radiation Attenuation (%) - CH-2 vs CH-3 with ISS Reference</span>
      <div class="dots"></div><span>12</span>
    </div>
    <div class="toc-entry"><span>Fig 4: OD600 Proxy - Auxiliary Computer Camera Simulation</span>
      <div class="dots"></div><span>12</span>
    </div>
    <div class="toc-entry"><span>Fig 5: Hysteresis Controller Validation - Flux vs Valve State</span>
      <div class="dots"></div><span>6</span>
    </div>
    <div class="toc-entry"><span>Fig 6: Wokwi Electronics Simulation - Valve CLOSED (GCR Background)</span>
      <div class="dots"></div><span>7</span>
    </div>
    <div class="toc-entry"><span>Fig 7: Wokwi Electronics Simulation - Valve OPEN (SAA Trigger &gt;500 μGy/hr)</span>
      <div class="dots"></div><span>7</span>
    </div>
    <div class="toc-entry"><span>Fig 8: Wokwi Electronics Simulation - Valve OPEN (Deadband Holding)</span>
      <div class="dots"></div><span>7</span>
    </div>
    <div class="toc-entry"><span>Fig 9: System Architecture Block Diagram</span>
      <div class="dots"></div><span>8</span>
    </div>
    <div class="toc-entry"><span>Fig 5: Power Budget Feasibility (48h)</span>
      <div class="dots"></div><span>9</span>
    </div>
    <div class="toc-entry"><span>Fig 6: Hysteresis Valve State Timeline</span>
      <div class="dots"></div><span>9</span>
    </div>
    <div class="toc-entry"><span>Fig 7: OD600 vs Biomass Linear Calibration</span>
      <div class="dots"></div><span>9</span>
    </div>
    <div class="toc-entry"><span>Fig 10: Isometric Exterior View - 3U CubeSat shell</span>
      <div class="dots"></div><span>9</span>
    </div>
    <div class="toc-entry"><span>Fig 11: Section View (Interior Layout)</span>
      <div class="dots"></div><span>9</span>
    </div>
    <div class="toc-entry"><span>Fig 12: Exploded View - LOC and Electronics</span>
      <div class="dots"></div><span>9</span>
    </div>"""

new_toc = """    <div class="toc-entry"><span>Fig 1: LEO Radiation Flux Profile with Hysteresis Valve State Overlay</span>
      <div class="dots"></div><span>11</span>
    </div>
    <div class="toc-entry"><span>Fig 2: Hysteresis Valve State Timeline</span>
      <div class="dots"></div><span>11</span>
    </div>
    <div class="toc-entry"><span>Fig 3: Fungal Biomass Growth - Logistic ODE (CH-2 vs CH-3)</span>
      <div class="dots"></div><span>12</span>
    </div>
    <div class="toc-entry"><span>Fig 4: OD600 vs Biomass Linear Calibration</span>
      <div class="dots"></div><span>12</span>
    </div>
    <div class="toc-entry"><span>Fig 5: OD600 Proxy - Auxiliary Computer Camera Simulation</span>
      <div class="dots"></div><span>12</span>
    </div>
    <div class="toc-entry"><span>Fig 6: Radiation Attenuation (%) - CH-2 vs CH-3 with ISS Reference</span>
      <div class="dots"></div><span>12</span>
    </div>
    <div class="toc-entry"><span>Fig 7: Power Budget Feasibility (48h)</span>
      <div class="dots"></div><span>13</span>
    </div>
    <div class="toc-entry"><span>Fig 8: Hysteresis Controller Validation - Flux vs Valve State</span>
      <div class="dots"></div><span>6</span>
    </div>
    <div class="toc-entry"><span>Fig 9: Wokwi Electronics Simulation - Valve CLOSED (GCR Background)</span>
      <div class="dots"></div><span>7</span>
    </div>
    <div class="toc-entry"><span>Fig 10: Wokwi Electronics Simulation - Valve OPEN (SAA Trigger &gt;500 μGy/hr)</span>
      <div class="dots"></div><span>7</span>
    </div>
    <div class="toc-entry"><span>Fig 11: Wokwi Electronics Simulation - Valve OPEN (Deadband Holding)</span>
      <div class="dots"></div><span>7</span>
    </div>
    <div class="toc-entry"><span>Fig 12: System Architecture Block Diagram</span>
      <div class="dots"></div><span>8</span>
    </div>
    <div class="toc-entry"><span>Fig 13: Isometric Exterior View - 3U CubeSat shell</span>
      <div class="dots"></div><span>9</span>
    </div>
    <div class="toc-entry"><span>Fig 14: Section View (Interior Layout)</span>
      <div class="dots"></div><span>9</span>
    </div>
    <div class="toc-entry"><span>Fig 15: Exploded View - LOC and Electronics</span>
      <div class="dots"></div><span>9</span>
    </div>"""

# Replace in chunks to avoid unicode/spacing issues
start_idx = html.find('<div class="toc-entry"><span>Fig 1:')
end_idx = html.find('</div>\n  </div>', start_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_toc + '\n  ' + html[end_idx:]

# Replace fig captions in body
html = html.replace('alt="Fig 6: Valve Timeline"', 'alt="Fig 2: Valve Timeline"')
html = html.replace('Fig 6: Hysteresis Valve State Timeline', 'Fig 2: Hysteresis Valve State Timeline')
html = html.replace('alt="Fig 2: Growth curves"', 'alt="Fig 3: Growth curves"')
html = html.replace('Fig 2: Fungal Biomass Growth', 'Fig 3: Fungal Biomass Growth')
html = html.replace('alt="Fig 7: OD600 Correlation"', 'alt="Fig 4: OD600 Correlation"')
html = html.replace('Fig 7: OD600 vs Biomass', 'Fig 4: OD600 vs Biomass')
html = html.replace('alt="Fig 4: OD600 proxy"', 'alt="Fig 5: OD600 proxy"')
html = html.replace('Fig 4: OD600 Optical', 'Fig 5: OD600 Optical')
html = html.replace('alt="Fig 3: Attenuation comparison"', 'alt="Fig 6: Attenuation comparison"')
html = html.replace('Fig 3: Radiation Attenuation', 'Fig 6: Radiation Attenuation')
html = html.replace('Fig 3. Both fungal chambers', 'Fig 6. Both fungal chambers')
html = html.replace('alt="Fig 5: Power Budget"', 'alt="Fig 7: Power Budget"')
html = html.replace('Fig 5: Power Budget Feasibility', 'Fig 7: Power Budget Feasibility')

html = html.replace('Fig 5: Hysteresis Controller Validation - radiation flux (top)', 'Fig 8: Hysteresis Controller Validation - radiation flux (top)')
html = html.replace('Fig 6: Valve CLOSED', 'Fig 9: Valve CLOSED')
html = html.replace('Fig 7: Valve OPEN triggered', 'Fig 10: Valve OPEN triggered')
html = html.replace('Fig 8: Valve OPEN holding', 'Fig 11: Valve OPEN holding')
html = html.replace('Fig 9: Software Pipeline', 'Fig 12: Software Pipeline')
html = html.replace('alt="Fig 10: Isometric', 'alt="Fig 13: Isometric')
html = html.replace('Fig 10: Isometric', 'Fig 13: Isometric')
html = html.replace('alt="Fig 11: Section', 'alt="Fig 14: Section')
html = html.replace('Fig 11: Section', 'Fig 14: Section')
html = html.replace('alt="Fig 12: Exploded', 'alt="Fig 15: Exploded')
html = html.replace('Fig 12: Exploded', 'Fig 15: Exploded')

with open('LOC_CubeSat_Report.html', 'w', encoding='utf-8') as f:
    f.write(html)


print("--- Fixing html_to_docx.py ---")
with open('html_to_docx.py', 'r', encoding='utf-8') as f:
    py = f.read()

# Replace docx python script figures list
old_figs = """figures = [
    ("Fig 1", "LEO Radiation Flux Profile with Hysteresis Valve State Overlay", "7"),
    ("Fig 2", "Fungal Biomass Growth - Logistic ODE (CH-2 vs CH-3)", "8"),
    ("Fig 3", "Radiation Attenuation (%) - CH-2 vs CH-3 with ISS Reference", "8"),
    ("Fig 4", "OD600 Proxy - Auxiliary Computer Camera Simulation", "8"),
    ("Fig 5", "Power Budget Feasibility (48h)", "9"),
    ("Fig 6", "Hysteresis Valve State Timeline", "7"),
    ("Fig 7", "OD600 vs Biomass Linear Calibration", "8"),
    ("Fig 5", "Hysteresis Controller Validation - Flux vs Valve State", "6"),
    ("Fig 6", "Wokwi Electronics Simulation - Valve CLOSED (GCR Background)", "4"),
    ("Fig 7", "Wokwi Electronics Simulation - Valve OPEN (SAA Trigger >500 uGy/hr)", "4"),
    ("Fig 8", "Wokwi Electronics Simulation - Valve OPEN (Deadband Holding)", "4"),
    ("Fig 9", "System Architecture Block Diagram", "6"),
    ("Fig 10", "Reference 3D Model - LOC CubeSat Internal Layout", "9"),
    ("Fig CAD-1", "[PLACEHOLDER] Fusion 360 - Isometric Exterior View", "9"),
    ("Fig CAD-2", "[PLACEHOLDER] Fusion 360 - Section View (Interior Layout)", "9"),
    ("Fig CAD-3", "[PLACEHOLDER] Fusion 360 - Exploded View", "9"),
]"""

new_figs = """figures = [
    ("Fig 1", "LEO Radiation Flux Profile with Hysteresis Valve State Overlay", "7"),
    ("Fig 2", "Hysteresis Valve State Timeline", "7"),
    ("Fig 3", "Fungal Biomass Growth - Logistic ODE (CH-2 vs CH-3)", "8"),
    ("Fig 4", "OD600 vs Biomass Linear Calibration", "8"),
    ("Fig 5", "OD600 Proxy - Auxiliary Computer Camera Simulation", "8"),
    ("Fig 6", "Radiation Attenuation (%) - CH-2 vs CH-3 with ISS Reference", "8"),
    ("Fig 7", "Power Budget Feasibility (48h)", "9"),
    ("Fig 8", "Hysteresis Controller Validation - Flux vs Valve State", "6"),
    ("Fig 9", "Wokwi Electronics Simulation - Valve CLOSED (GCR Background)", "4"),
    ("Fig 10", "Wokwi Electronics Simulation - Valve OPEN (SAA Trigger >500 uGy/hr)", "4"),
    ("Fig 11", "Wokwi Electronics Simulation - Valve OPEN (Deadband Holding)", "4"),
    ("Fig 12", "System Architecture Block Diagram", "6"),
    ("Fig 13", "Reference 3D Model - LOC CubeSat Internal Layout", "9"),
    ("Fig CAD-1", "[PLACEHOLDER] Fusion 360 - Isometric Exterior View", "9"),
    ("Fig CAD-2", "[PLACEHOLDER] Fusion 360 - Section View (Interior Layout)", "9"),
    ("Fig CAD-3", "[PLACEHOLDER] Fusion 360 - Exploded View", "9"),
]"""
py = py.replace(old_figs, new_figs)

py = py.replace('Fig 6: Hysteresis Valve State', 'Fig 2: Hysteresis Valve State')
py = py.replace('Fig 4: OD600 Optical', 'Fig 5: OD600 Optical')
py = py.replace('Fig 7: OD600 vs Biomass', 'Fig 4: OD600 vs Biomass')
py = py.replace('Fig 5: Power Budget', 'Fig 7: Power Budget')

py = py.replace('presented in Fig 3.', 'presented in Fig 6.')
py = py.replace('Fig 3: Radiation Attenuation', 'Fig 6: Radiation Attenuation')

py = py.replace('Fig 10: Isometric Exterior', 'Fig 13: Isometric Exterior')
py = py.replace('Fig 11: Section View', 'Fig 14: Section View')
py = py.replace('Fig 12: Exploded View', 'Fig 15: Exploded View')

with open('html_to_docx.py', 'w', encoding='utf-8') as f:
    f.write(py)


# 4. Final step: dashboard.py (Update the Matplotlib titles too!)
with open('src/dashboard.py', 'r', encoding='utf-8') as f:
    dash = f.read()

dash = dash.replace('Fig 2: Fungal Biomass Growth', 'Fig 3: Fungal Biomass Growth')
dash = dash.replace('Fig 3: Radiation Attenuation', 'Fig 6: Radiation Attenuation')
dash = dash.replace('Fig 4: OD600 Proxy', 'Fig 5: OD600 Proxy')
dash = dash.replace('Fig 5: Power Budget', 'Fig 7: Power Budget')
dash = dash.replace('Fig 6: Hysteresis Valve State', 'Fig 2: Hysteresis Valve State')
dash = dash.replace('Fig 7: OD600 vs Biomass', 'Fig 4: OD600 vs Biomass')

with open('src/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(dash)

print("Done with script logic. Now re-running dashboard.py and html_to_docx.py...")
os.chdir('src')
os.system('python dashboard.py')
os.chdir('..')
os.system('python html_to_docx.py')
