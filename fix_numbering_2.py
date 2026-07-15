import re

# 1. Update README
with open('README.md', 'r', encoding='utf-8') as f:
    md = f.read()

md = md.replace('Fig 10: Isometric', 'Fig 13: Isometric')
md = md.replace('Fig 11: Section', 'Fig 14: Section')
md = md.replace('Fig 12: Exploded', 'Fig 15: Exploded')

md = md.replace('Fig 5: Wokwi', 'Fig 9: Wokwi')
md = md.replace('Fig 6: Wokwi', 'Fig 9: Wokwi')
md = md.replace('Fig 7: Wokwi', 'Fig 10: Wokwi')
md = md.replace('Fig 8: Wokwi', 'Fig 11: Wokwi')
md = md.replace('Fig 5 - Hysteresis Controller', 'Fig 8 - Hysteresis Controller')
md = md.replace('Fig 5: Hysteresis validation', 'Fig 8: Hysteresis validation')
md = md.replace('Fig 5 - Power Budget', 'Fig 7 - Power Budget')
md = md.replace('Fig 5: Power Budget', 'Fig 7: Power Budget')

md = md.replace('Fig 4 - OD600 Camera', 'Fig 5 - OD600 Camera')
md = md.replace('Fig 4: OD600 optical', 'Fig 5: OD600 optical')
md = md.replace('Fig 7 - OD600 Correlation', 'Fig 4 - OD600 Correlation')
md = md.replace('Fig 7: OD600 Correlation', 'Fig 4: OD600 Correlation')

md = md.replace('Fig 3 - Radiation', 'Fig 6 - Radiation')
md = md.replace('Fig 3: Attenuation comparison', 'Fig 6: Attenuation comparison')

md = md.replace('Fig 2 - Fungal', 'Fig 3 - Fungal')
md = md.replace('Fig 2: Logistic', 'Fig 3: Logistic')

md = md.replace('Fig 6 - Valve State', 'Fig 2 - Valve State')
md = md.replace('Fig 6: Valve Timeline', 'Fig 2: Valve Timeline')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(md)


# 2. Fix HTML TOC
with open('LOC_CubeSat_Report.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the TOC wokwi elements
html = html.replace('<span>Fig 6: Wokwi', '<span>Fig 9: Wokwi')
html = html.replace('<span>Fig 7: Wokwi', '<span>Fig 10: Wokwi')
html = html.replace('<span>Fig 8: Wokwi', '<span>Fig 11: Wokwi')
html = html.replace('<span>Fig 9: System Architecture', '<span>Fig 12: System Architecture')
html = html.replace('alt="Fig 3: Attenuation comparison"', 'alt="Fig 6: Attenuation comparison"')
html = html.replace('alt="Fig 7: OD600 Correlation"', 'alt="Fig 4: OD600 Correlation"')


with open('LOC_CubeSat_Report.html', 'w', encoding='utf-8') as f:
    f.write(html)
