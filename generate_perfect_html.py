import re
import os
from datetime import datetime

def generate_html():
    with open('raw_doc.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    html = []
    
    html.append('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>TEAM 4 - LOC CubeSat Payload</title>
  <style>
    @page { margin: 25mm 25mm 25mm 30mm; size: A4; }
    body {
      font-family: "Times New Roman", Times, serif;
      line-height: 1.5;
      text-align: justify;
      background: #ffffff;
      color: #000000;
      margin: 0 auto;
      max-width: 800px;
      padding: 40px;
    }
    h1 {
      font-size: 16pt;
      font-weight: bold;
      margin-top: 30px;
      margin-bottom: 15px;
      page-break-after: avoid;
    }
    h2 {
      font-size: 14pt;
      font-weight: bold;
      margin-top: 25px;
      margin-bottom: 10px;
      page-break-after: avoid;
    }
    h3 {
      font-size: 14pt;
      text-transform: uppercase;
      margin-top: 20px;
      margin-bottom: 10px;
      page-break-after: avoid;
    }
    .title {
      font-size: 16pt;
      font-weight: bold;
      text-align: center;
      text-transform: uppercase;
      margin-top: 40px;
      margin-bottom: 20px;
    }
    .subtitle {
      font-size: 14pt;
      font-weight: bold;
      text-align: center;
      margin-bottom: 40px;
    }
    .cover-team {
      text-align: center;
      font-size: 14pt;
      margin-top: 60px;
    }
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 12pt;
    }
    table.data-table th, table.data-table td {
      border: 1px solid #000000;
      padding: 8px;
      text-align: center;
    }
    table.data-table th {
      font-weight: bold;
    }
    .table-caption {
      text-align: center;
      font-size: 12pt;
      font-weight: bold;
      margin-bottom: 5px;
    }
    .fig-table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    .fig-table td {
      border: 1px solid #000000;
      padding: 10px;
      text-align: center;
    }
    .fig-caption {
      font-size: 10pt;
      text-align: center;
      margin-top: 8px;
    }
    .toc-entry {
      display: flex;
      justify-content: space-between;
      margin-bottom: 5px;
    }
    .toc-h1 { font-weight: bold; margin-top: 10px; }
    .toc-h2 { margin-left: 20px; }
    .toc-h3 { margin-left: 40px; }
    .page-break { page-break-before: always; }
    
    .console-output {
      background-color: #1e1e1e;
      color: #00ff00;
      font-family: 'Courier New', Courier, monospace;
      font-size: 10pt;
      padding: 15px;
      border-radius: 5px;
      overflow-x: auto;
      margin: 20px 0;
      text-align: left;
    }
    .console-output div {
      white-space: pre-wrap;
      line-height: 1.3;
    }
  </style>
</head>
<body>
''')

    # Cover Page
    html.append('''  <div class="page-break">
    <img src="src/figures/rvce_header.png" style="width: 100%; margin-bottom: 30px;">
    <div style="display: flex; justify-content: flex-end; width: 100%; margin-bottom: 20px;">
      <img src="src/figures/antariksh_logo.png" style="width: 120px; margin-bottom: 5px;">
    </div>
    
    <div class="title">TEAM ANTARIKSH<br><br>
    TITLE: LAB-ON-A-CHIP CUBESAT PAYLOAD SIMULATION:<br>
    FUNGAL RADIATION SHIELDING STUDY IN LOW EARTH ORBIT</div>
    <div class="subtitle">3-Chamber Comparative Analysis of Melanin-Rich Fungal Strains</div>
    
    <div class="cover-team">
      <strong>TEAM 4</strong><br><br>
      Aditi Ambashtha<br>
      Sarthak Kapadia<br>
      Samarth BN<br>
      Shubhajit Nair<br>
      Preetham S<br>
      Yash Joshi
    </div>
  </div>''')

    # Parse Body to get sequential Figures and Tables
    body_start_idx = 0
    for i, line in enumerate(lines):
        if "LAB-ON-A-CHIP CUBESAT PAYLOAD SIMULATION" in line and i > 50:
            body_start_idx = i + 1
            break

    fig_map = {}
    table_map = {}
    fig_counter = 1
    table_counter = 1
    
    # Pre-pass for mapping original numbers to sequential numbers
    for line in lines[body_start_idx:]:
        line = line.strip()
        m_fig = re.match(r'^Fig\s+(.*?):', line)
        if m_fig:
            old_val = m_fig.group(1).strip()
            if old_val not in fig_map and "CAD-" not in old_val:
                fig_map[old_val] = str(fig_counter)
                fig_counter += 1
                
        m_table = re.match(r'^Table\s+(\d+):', line)
        if m_table:
            old_val = m_table.group(1).strip()
            if old_val not in table_map:
                table_map[old_val] = str(table_counter)
                table_counter += 1

    # Now, parse TOC
    html.append('<div class="page-break">')
    html.append('<div class="title">TABLE OF CONTENTS</div>')
    
    toc_idx = 0
    for i, line in enumerate(lines):
        if "TABLE OF CONTENTS" in line:
            toc_idx = i + 1
            break
            
    for i in range(toc_idx, len(lines)):
        line = lines[i].strip()
        if "LIST OF FIGURES" in line:
            break
        if not line or "_____" in line:
            continue
            
        # It's a TOC line. usually format: "1. Executive Summary        1"
        m = re.match(r'^(.*?)(\s+\d+)$', line)
        if m:
            text_part = m.group(1).strip()
            page_part = m.group(2).strip()
            
            cls = "toc-entry"
            if re.match(r'^\d+\.\s', text_part):
                cls += " toc-h1"
            elif re.match(r'^\d+\.\d+\.\s', text_part):
                cls += " toc-h2"
            elif re.match(r'^\d+\.\d+\.\d+\.\s', text_part):
                cls += " toc-h3"
                
            html.append(f'<div class="{cls}"><span>{text_part}</span><span>{page_part}</span></div>')
            
    html.append('</div>')
    
    # Parse List of Figures
    html.append('<div class="page-break">')
    html.append('<div class="title">LIST OF FIGURES</div>')
    list_of_figures_idx = 0
    for i, line in enumerate(lines):
        if "LIST OF FIGURES" in line:
            list_of_figures_idx = i + 1
            break
            
    toc_figures = []
    for i in range(list_of_figures_idx, body_start_idx):
        line = lines[i].strip()
        if "LAB-ON-A-CHIP" in line:
            break
        if not line or "_____" in line:
            continue
            
        m = re.match(r'^Fig\s+(.*?):\s+(.*?)\s+(\d+)$', line)
        if m:
            old_val = m.group(1).strip()
            if "CAD-" in old_val:
                continue
            desc = m.group(2).strip()
            page = m.group(3).strip()
            
            if old_val in fig_map:
                new_val = fig_map[old_val]
                toc_figures.append((int(new_val), desc, page))
                
    toc_figures.sort(key=lambda x: x[0])
    for num, desc, page in toc_figures:
        html.append(f'<div class="toc-entry"><span>Fig {num}: {desc}</span><span>{page}</span></div>')
    
    html.append('</div>')

    # Process Body
    html.append('<div class="page-break">')
    
    i = body_start_idx
    in_table = False
    in_log = False
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for Console Log
        if "2026-07-15 23:22:52" in line or "INFO -" in line or "Starting LOC CubeSat" in line:
            if not in_log:
                html.append('<div class="console-output">')
                in_log = True
            html.append(f'<div>{line}</div>')
            i += 1
            continue
        elif in_log:
            html.append('</div>')
            in_log = False
            
        if not line or "_____" in line:
            i += 1
            continue
            
        # Ignore CAD placeholders
        if "[PLACEHOLDER" in line:
            i += 1
            continue
            
        # Heading 1
        m_h1 = re.match(r'^(\d+\.\s+[A-Z].*)', line)
        if m_h1 and line.split()[0].endswith('.'):
            # It's an H1 but the text might be capitalized or not. Format requires H1 to be bold.
            # We'll just put it in <h1>
            text = m_h1.group(1).replace('.', '', 1).strip()  # Remove first dot for "1 Executive Summary" -> "1. Executive Summary"
            # Actually just keep the original text
            html.append(f'<h1>{line}</h1>')
            i += 1
            continue
            
        # Heading 2
        m_h2 = re.match(r'^\d+\.\d+\.\s+.*', line)
        if m_h2:
            html.append(f'<h2>{line}</h2>')
            i += 1
            continue
            
        # Heading 3
        m_h3 = re.match(r'^\d+\.\d+\.\d+\.\s+.*', line)
        if m_h3:
            html.append(f'<h3>{line.upper()}</h3>')
            i += 1
            continue
            
        # Table
        m_table = re.match(r'^Table\s+(\d+):\s+(.*)', line)
        if m_table:
            old_num = m_table.group(1)
            new_num = table_map.get(old_num, old_num)
            html.append(f'<div class="table-caption">Table {new_num}: {m_table.group(2)}</div>')
            
            # Start gathering table rows
            i += 1
            table_rows = []
            while i < len(lines):
                tl = lines[i].strip()
                if not tl or tl.startswith("Table") or re.match(r'^\d+\s', tl) or re.match(r'^\d+\.', tl) or tl.startswith("Fig ") or tl.startswith("[PLACEHOLDER") or tl.startswith("____") or "---" in tl:
                    break
                table_rows.append(tl)
                i += 1
                
            if table_rows:
                html.append('<table class="data-table">')
                for r_idx, r_text in enumerate(table_rows):
                    cols = r_text.split('\\t')
                    html.append('  <tr>')
                    for col in cols:
                        if r_idx == 0:
                            html.append(f'    <th>{col.strip()}</th>')
                        else:
                            html.append(f'    <td>{col.strip()}</td>')
                    html.append('  </tr>')
                html.append('</table>')
            continue

        # Figure Caption (Standalone or with image)
        m_fig = re.match(r'^Fig\s+(.*?):\s+(.*)', line)
        if m_fig:
            old_val = m_fig.group(1)
            new_val = fig_map.get(old_val, old_val)
            desc = m_fig.group(2)
            caption_text = f"Fig {new_val}: {desc}"
            
            # Map image path
            img_path = None
            if "Valve CLOSED" in line and "GCR" in line: img_path = 'src/figures/electronics_sim/wokwi_pico_normal.png'
            elif "Valve OPEN triggered" in line: img_path = 'src/figures/electronics_sim/wokwi_pico_triggered.png'
            elif "Valve OPEN hold" in line or "Deadband Holding" in line: img_path = 'src/figures/electronics_sim/wokwi_pico_high_rad.png'
            elif "Flux vs Valve State" in line or "Hysteresis Controller Validation" in line: img_path = 'src/figures/hysteresis_validation.png'
            elif "Flux Profile" in line: img_path = 'src/figures/fig1_flux_valve.png'
            elif "Biomass Growth" in line: img_path = 'src/figures/fig2_growth_curves.png'
            elif "OD600 Optical Density Proxy" in line or "OD600 Proxy" in line: img_path = 'src/figures/fig4_od600_proxy.png'
            elif "Radiation Attenuation" in line: img_path = 'src/figures/fig3_attenuation.png'
            elif "3D model" in line or "Internal Layout" in line: img_path = 'src/figures/fig_cad_master.png'
            
            if img_path and os.path.exists(img_path):
                html.append('<table class="fig-table">')
                html.append('  <tr>')
                html.append('    <td>')
                html.append(f'      <img src="{img_path}" style="width:100%; max-width:600px; display:block; margin: 10px auto;">')
                html.append(f'      <div class="fig-caption">{caption_text}</div>')
                html.append('    </td>')
                html.append('  </tr>')
                html.append('</table>')
            else:
                html.append(f'<div class="fig-caption">{caption_text}</div>')
            i += 1
            continue

        # Replace in-text figure/table references
        for old_num, new_num in sorted(fig_map.items(), key=lambda x: len(x[0]), reverse=True):
            line = re.sub(r'\\bFig ' + re.escape(old_num) + r'\\b', f'Fig {new_num}', line)
        for old_num, new_num in sorted(table_map.items(), key=lambda x: len(x[0]), reverse=True):
            line = re.sub(r'\\bTable ' + re.escape(old_num) + r'\\b', f'Table {new_num}', line)
            
        # Synthetic Camera block (hardcoded logic)
        if "Synthetic images generated by the pipeline simulating" in line:
            html.append(f'<p>{line}</p>')
            html.append('<div style="text-align:center; margin: 30px 0;">')
            html.append('  <strong>T = 0 hours (Inoculation)</strong><br>')
            html.append('  <img src="figures/camera/img_00h.png" style="width:100%; max-width:500px; display:block; margin: 5px auto 20px;">')
            html.append('  <strong>T = 24 hours (Mid-orbit)</strong><br>')
            html.append('  <img src="figures/camera/img_24h.png" style="width:100%; max-width:500px; display:block; margin: 5px auto 20px;">')
            html.append('  <strong>T = 48 hours (Completion)</strong><br>')
            html.append('  <img src="figures/camera/img_48h.png" style="width:100%; max-width:500px; display:block; margin: 5px auto 20px;">')
            html.append('</div>')
            # Skip the next few lines that belonged to the old table
            i += 1
            while i < len(lines) and ("T = " in lines[i] or ".png" in lines[i]):
                i += 1
            continue
            
        if line:
            html.append(f'<p>{line}</p>')
        i += 1

    if in_log:
        html.append('</div>')

    html.append('  </div>')
    html.append('</body>')
    html.append('</html>')

    with open('LOC_CubeSat_Report.html', 'w', encoding='utf-8') as f:
        f.write('\\n'.join(html))

if __name__ == '__main__':
    generate_html()
    print("Perfect HTML generated!")
