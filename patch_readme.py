import re

with open('README.md', 'r', encoding='utf-8') as f:
    md = f.read()

tree_old = '''│       ├── fig3_attenuation.png
│       ├── fig4_od600_proxy.png
│       ├── hysteresis_validation.png'''
tree_new = '''│       ├── fig3_attenuation.png
│       ├── fig4_od600_proxy.png
│       ├── fig5_power_budget.png
│       ├── fig6_valve_timeline.png
│       ├── fig7_od600_correlation.png
│       ├── hysteresis_validation.png'''

md = md.replace(tree_old, tree_new)

fig4_old = '''### Fig 4 - OD600 Camera Proxy (What the Camera Sees)
> OD600 (Optical Density at 600 nm wavelength) is a standard measure of how cloudy a culture is - cloudier = more biomass. The auxiliary Raspberry Pi camera tracks this as a proxy for growth.

![Fig 4: OD600 Proxy](src/figures/fig4_od600_proxy.png)'''

fig_new = fig4_old + '''

---

### Fig 5 - Power Budget Feasibility
> A critical engineering requirement. This simulation models the continuous duty-cycled average draw (387 mW) against the 0.5U solar panel generation (~750 mW during sunlit phases). The net positive generation keeps the 6.66 Wh battery at maximum capacity for the full 48-hour mission.

![Fig 5: Power Budget](src/figures/fig5_power_budget.png)'''

md = md.replace(fig4_old, fig_new)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(md)
