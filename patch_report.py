import re

# 1. Patch HTML
with open('LOC_CubeSat_Report.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Add to list of figures in HTML
html = html.replace(
    '<div class="dots"></div><span>8</span>',
    '<div class="dots"></div><span>8</span>\n    </div>\n    <div class="toc-entry"><span>Fig 5: Power Budget Feasibility (48h)</span>\n      <div class="dots"></div><span>9</span>\n    </div>\n    <div class="toc-entry"><span>Fig 6: Hysteresis Valve State Timeline</span>\n      <div class="dots"></div><span>9</span>\n    </div>\n    <div class="toc-entry"><span>Fig 7: OD600 vs Biomass Linear Calibration</span>\n      <div class="dots"></div><span>9</span>'
, 1)

# Add Fig 6 to HTML
fig1_str = '''        <td>
          <img src="src/figures/fig1_flux_valve.png" alt="Fig 1: LEO Radiation Flux and Valve State">
          <div class="fig-caption">Fig 1: LEO Radiation Flux Profile over 48 hours with Hysteresis Valve State Overlay.
            GCR baseline = 200 μGy/hr; SAA peaks reach ~672 μGy/hr. Red shaded regions indicate valve OPEN events (11
            total). Upper threshold (500 μGy/hr) and lower threshold (350 μGy/hr) shown as dashed lines.</div>
        </td>'''
fig6_str = fig1_str + '''
      </tr>
      <tr>
        <td>
          <img src="src/figures/fig6_valve_timeline.png" alt="Fig 6: Valve Timeline">
          <div class="fig-caption">Fig 6: Hysteresis Valve State Timeline. A discrete step-plot showing the precise timing and duration of valve actuations.</div>
        </td>'''
html = html.replace(fig1_str, fig6_str)

# Add Fig 7 to HTML
fig4_str = '''        <td style="width:50%">
          <img src="src/figures/fig4_od600_proxy.png" alt="Fig 4: OD600 proxy">
          <div class="fig-caption">Fig 4: OD600 Optical Density Proxy - simulating auxiliary computer camera output.
            OD600 is proportional to biomass: OD = k·N, where k = 3.0 OD·L/g (empirical calibration).</div>
        </td>
      </tr>
    </table>'''
fig7_str = fig4_str.replace('    </table>', '''      <tr>
        <td colspan="2">
          <img src="src/figures/fig7_od600_correlation.png" alt="Fig 7: OD600 Correlation" style="width:50%; margin: 0 auto; display: block;">
          <div class="fig-caption">Fig 7: OD600 vs Biomass Linear Calibration. Demonstrates the strict proportional relationship used by the camera sensor proxy.</div>
        </td>
      </tr>
    </table>''')
html = html.replace(fig4_str, fig7_str)

# Add 7.4 Power Budget to HTML
html = html.replace('<h2>7.4. 3D Structural Model - Autodesk Fusion 360</h2>', '''<h2>7.4. Power Budget Simulation</h2>
    <p>
      Mission power feasibility was simulated by tracking battery charge over the 48-hour mission. The CubeSat runs continuously with an average draw of 387 mW. A 0.5U body-mounted solar panel provides ~750 mW during the sunlit portion of the orbit. As shown in Fig 5, this yields a net positive power generation, keeping the 6.66 Wh battery fully charged.
    </p>
    <table class="fig-table">
      <tr>
        <td>
          <img src="src/figures/fig5_power_budget.png" alt="Fig 5: Power Budget">
          <div class="fig-caption">Fig 5: Power Budget Feasibility (48h). The battery remains at maximum capacity due to the duty-cycled loads and supplementary solar panel.</div>
        </td>
      </tr>
    </table>

    <h2>7.5. 3D Structural Model - Autodesk Fusion 360</h2>''')

html = html.replace('<h2>7.5. Reliability and Failure Modes Analysis</h2>', '<h2>7.6. Reliability and Failure Modes Analysis</h2>')

with open('LOC_CubeSat_Report.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Patch docx script
with open('html_to_docx.py', 'r', encoding='utf-8', errors='ignore') as f:
    py = f.read()

py = py.replace('("   7.4. 3D Model - Fusion 360", "9"),', '("   7.4. Power Budget Simulation", "9"),\n    ("   7.5. 3D Model - Fusion 360", "10"),')
py = py.replace('("   7.5. Reliability and Failure Modes Analysis", "9"),', '("   7.6. Reliability and Failure Modes Analysis", "10"),')

py = py.replace('("Fig 4", "OD600 Proxy - Auxiliary Computer Camera Simulation", "8"),', '("Fig 4", "OD600 Proxy - Auxiliary Computer Camera Simulation", "8"),\n    ("Fig 5", "Power Budget Feasibility (48h)", "9"),\n    ("Fig 6", "Hysteresis Valve State Timeline", "7"),\n    ("Fig 7", "OD600 vs Biomass Linear Calibration", "8"),')

fig1_docx = 'add_figure(doc, BASE_DIR / "src/figures/fig1_flux_valve.png",\n           "Fig 1: LEO Radiation Flux Profile over 48 hours with Hysteresis Valve State Overlay. "\n           "GCR baseline = 200 uGy/hr; SAA peaks reach ~672 uGy/hr. Red shaded regions indicate valve "\n           "OPEN events. Upper threshold (500 uGy/hr) and lower threshold (350 uGy/hr) shown as dashed lines.")'
fig6_docx = fig1_docx + '\n\nadd_figure(doc, BASE_DIR / "src/figures/fig6_valve_timeline.png",\n           "Fig 6: Hysteresis Valve State Timeline. A discrete step-plot showing the precise timing and duration of valve actuations.")'
py = py.replace(fig1_docx, fig6_docx)

fig4_docx = 'add_figure(doc, BASE_DIR / "src/figures/fig4_od600_proxy.png",\n           "Fig 4: OD600 Optical Density Proxy - simulating auxiliary computer camera output. "\n           "OD600 is proportional to biomass: OD = k·N, where k = 3.0 OD·L/g (empirical calibration).")'
fig7_docx = fig4_docx + '\n\nadd_figure(doc, BASE_DIR / "src/figures/fig7_od600_correlation.png",\n           "Fig 7: OD600 vs Biomass Linear Calibration. Demonstrates the strict proportional relationship used by the camera sensor proxy.")'
py = py.replace(fig4_docx, fig7_docx)

s74_docx = '''add_h2(doc, "7.4. 3D Structural Model - Autodesk Fusion 360")'''
s74_new = '''add_h2(doc, "7.4. Power Budget Simulation")
add_para(doc, "Mission power feasibility was simulated by tracking battery charge over the 48-hour mission. The CubeSat runs continuously with an average draw of 387 mW. A 0.5U body-mounted solar panel provides ~750 mW during the sunlit portion of the orbit. As shown in Fig 5, this yields a net positive power generation, keeping the 6.66 Wh battery fully charged.")
add_figure(doc, BASE_DIR / "src/figures/fig5_power_budget.png", "Fig 5: Power Budget Feasibility (48h). The battery remains at maximum capacity due to the duty-cycled loads and supplementary solar panel.")

add_h2(doc, "7.5. 3D Structural Model - Autodesk Fusion 360")'''
py = py.replace(s74_docx, s74_new)

py = py.replace('add_h2(doc, "7.5. Reliability and Failure Modes Analysis")', 'add_h2(doc, "7.6. Reliability and Failure Modes Analysis")')

with open('html_to_docx.py', 'w', encoding='utf-8') as f:
    f.write(py)
