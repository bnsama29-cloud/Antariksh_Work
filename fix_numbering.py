import os
import re

# 1. Update Dashboard
with open('src/dashboard.py', 'r', encoding='utf-8') as f:
    dash = f.read()

# Swap the dashboard figure title numbers
dash = dash.replace('Fig 2: Fungal Biomass Growth', 'Fig 3: Fungal Biomass Growth')
dash = dash.replace('Fig 3: Radiation Attenuation', 'Fig 6: Radiation Attenuation')
dash = dash.replace('Fig 4: OD600 Proxy', 'Fig 5: OD600 Proxy')
dash = dash.replace('Fig 5: Power Budget', 'Fig 7: Power Budget')
dash = dash.replace('Fig 6: Hysteresis Valve State', 'Fig 2: Hysteresis Valve State')
dash = dash.replace('Fig 7: OD600 vs Biomass', 'Fig 4: OD600 vs Biomass')

with open('src/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(dash)

# 2. Re-run Dashboard to regenerate images
print("Running dashboard.py...")
os.chdir('src')
os.system('python dashboard.py')
os.chdir('..')

# 3. Update HTML Report
with open('LOC_CubeSat_Report.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix List of Figures in HTML
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

# Replace all old figure numbering in HTML text
html = html.replace('Fig 10: Isometric', 'Fig 13: Isometric')
html = html.replace('Fig 11: Section', 'Fig 14: Section')
html = html.replace('Fig 12: Exploded', 'Fig 15: Exploded')
html = html.replace('Fig 9: Software Pipeline', 'Fig 12: Software Pipeline')
html = html.replace('Fig 8: Valve OPEN holding', 'Fig 11: Valve OPEN holding')
html = html.replace('Fig 7: Valve OPEN triggered', 'Fig 10: Valve OPEN triggered')
html = html.replace('Fig 6: Valve CLOSED', 'Fig 9: Valve CLOSED')
html = html.replace('Fig 5: Hysteresis Controller', 'Fig 8: Hysteresis Controller')

html = html.replace('Fig 5: Power Budget', 'Fig 7: Power Budget')
html = html.replace('Fig 3: Radiation Attenuation', 'Fig 6: Radiation Attenuation')
html = html.replace('Fig 3. Both', 'Fig 6. Both')
html = html.replace('Fig 4: OD600 Optical', 'Fig 5: OD600 Optical')
html = html.replace('alt="Fig 4: OD600 proxy"', 'alt="Fig 5: OD600 proxy"')
html = html.replace('Fig 7: OD600 vs Biomass', 'Fig 4: OD600 vs Biomass')
html = html.replace('alt="Fig 7: OD600 Correlation"', 'alt="Fig 4: OD600 Correlation"')
html = html.replace('Fig 2: Fungal', 'Fig 3: Fungal')
html = html.replace('alt="Fig 2: Growth curves"', 'alt="Fig 3: Growth curves"')
html = html.replace('Fig 6: Hysteresis Valve State', 'Fig 2: Hysteresis Valve State')
html = html.replace('alt="Fig 6: Valve Timeline"', 'alt="Fig 2: Valve Timeline"')

# I need to do a manual replace of TOC using regex because of possible formatting
import re
toc_pattern = re.compile(r'<div class="toc-entry"><span>Fig 1.*?<span>Fig 12: Exploded View - LOC and Electronics</span>\s*</div>', re.DOTALL)
if toc_pattern.search(html):
    html = toc_pattern.sub(new_toc, html)
else:
    print("WARNING: HTML TOC replacement failed, fallback.")
    # Fallback to simple replace
    html = html.replace(old_toc, new_toc)

with open('LOC_CubeSat_Report.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 4. Update html_to_docx.py
with open('html_to_docx.py', 'r', encoding='utf-8') as f:
    py = f.read()

py = py.replace('("Fig 1", "LEO Radiation Flux Profile with Hysteresis Valve State Overlay", "7"),', '("Fig 1", "LEO Radiation Flux Profile with Hysteresis Valve State Overlay", "7"),\n    ("Fig 2", "Hysteresis Valve State Timeline", "7"),')
py = py.replace('("Fig 2", "Fungal Biomass Growth - Logistic ODE (CH-2 vs CH-3)", "8"),', '("Fig 3", "Fungal Biomass Growth - Logistic ODE (CH-2 vs CH-3)", "8"),\n    ("Fig 4", "OD600 vs Biomass Linear Calibration", "8"),')
py = py.replace('("Fig 4", "OD600 Proxy - Auxiliary Computer Camera Simulation", "8"),\n    ("Fig 5", "Power Budget Feasibility (48h)", "9"),\n    ("Fig 6", "Hysteresis Valve State Timeline", "7"),\n    ("Fig 7", "OD600 vs Biomass Linear Calibration", "8"),', '("Fig 5", "OD600 Proxy - Auxiliary Computer Camera Simulation", "8"),\n    ("Fig 6", "Radiation Attenuation (%) - CH-2 vs CH-3 with ISS Reference", "8"),\n    ("Fig 7", "Power Budget Feasibility (48h)", "9"),')
py = py.replace('("Fig 3", "Radiation Attenuation (%) - CH-2 vs CH-3 with ISS Reference", "8"),\n', '')

py = py.replace('("Fig 5", "Hysteresis Controller Validation - Flux vs Valve State", "6"),', '("Fig 8", "Hysteresis Controller Validation - Flux vs Valve State", "6"),')
py = py.replace('("Fig 6", "Wokwi Electronics Simulation - Valve CLOSED (GCR Background)", "4"),', '("Fig 9", "Wokwi Electronics Simulation - Valve CLOSED (GCR Background)", "4"),')
py = py.replace('("Fig 7", "Wokwi Electronics Simulation - Valve OPEN (SAA Trigger >500 uGy/hr)", "4"),', '("Fig 10", "Wokwi Electronics Simulation - Valve OPEN (SAA Trigger >500 uGy/hr)", "4"),')
py = py.replace('("Fig 8", "Wokwi Electronics Simulation - Valve OPEN (Deadband Holding)", "4"),', '("Fig 11", "Wokwi Electronics Simulation - Valve OPEN (Deadband Holding)", "4"),')
py = py.replace('("Fig 9", "System Architecture Block Diagram", "6"),', '("Fig 12", "System Architecture Block Diagram", "6"),')
py = py.replace('("Fig 10", "Reference 3D Model', '("Fig 13", "Reference 3D Model')

py = py.replace('add_figure(doc, BASE_DIR / "src/figures/fig6_valve_timeline.png",\n           "Fig 6: Hysteresis Valve State Timeline.', 'add_figure(doc, BASE_DIR / "src/figures/fig6_valve_timeline.png",\n           "Fig 2: Hysteresis Valve State Timeline.')
py = py.replace('add_figure(doc, BASE_DIR / "src/figures/fig4_od600_proxy.png",\n           "Fig 4: OD600', 'add_figure(doc, BASE_DIR / "src/figures/fig4_od600_proxy.png",\n           "Fig 5: OD600')
py = py.replace('add_figure(doc, BASE_DIR / "src/figures/fig7_od600_correlation.png",\n           "Fig 7: OD600', 'add_figure(doc, BASE_DIR / "src/figures/fig7_od600_correlation.png",\n           "Fig 4: OD600')
py = py.replace('add_figure(doc, BASE_DIR / "src/figures/fig5_power_budget.png", "Fig 5: Power', 'add_figure(doc, BASE_DIR / "src/figures/fig5_power_budget.png", "Fig 7: Power')
py = py.replace('add_figure(doc, BASE_DIR / "src/figures/fig3_attenuation.png",\n           "Fig 3: Radiation', 'add_figure(doc, BASE_DIR / "src/figures/fig3_attenuation.png",\n           "Fig 6: Radiation')

py = py.replace('Fig 10: Isometric Exterior View', 'Fig 13: Isometric Exterior View')
py = py.replace('Fig 11: Section View', 'Fig 14: Section View')
py = py.replace('Fig 12: Exploded View', 'Fig 15: Exploded View')

with open('html_to_docx.py', 'w', encoding='utf-8') as f:
    f.write(py)

# 5. Re-run html_to_docx
print("Running html_to_docx.py...")
os.system('python html_to_docx.py')
