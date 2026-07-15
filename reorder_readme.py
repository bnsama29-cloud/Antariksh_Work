import re

with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
in_figures = False

fig_blocks = {}
current_fig = None
current_block = []

while i < len(lines):
    line = lines[i]
    
    if line.startswith('### Fig 1 - LEO Radiation Flux Profile'):
        in_figures = True
        current_fig = 1
        current_block.append(line)
    elif line.startswith('### Fig '):
        if in_figures:
            fig_blocks[current_fig] = current_block
            match = re.search(r'### Fig (\d+)', line)
            current_fig = int(match.group(1))
            current_block = [line]
        else:
            new_lines.append(line)
    elif line.startswith('## 💻 Academic Report'):
        if in_figures:
            fig_blocks[current_fig] = current_block
            in_figures = False
            
            # Now output them in sorted order
            for fnum in sorted(fig_blocks.keys()):
                new_lines.extend(fig_blocks[fnum])
                
        new_lines.append(line)
    else:
        if in_figures:
            current_block.append(line)
        else:
            new_lines.append(line)
    
    i += 1

if in_figures:
    fig_blocks[current_fig] = current_block
    for fnum in sorted(fig_blocks.keys()):
        new_lines.extend(fig_blocks[fnum])

with open('README.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

