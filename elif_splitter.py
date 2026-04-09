
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    m = re.match(r'^(\s*)', line)
    indent = m.group(1) if m else ""
    
    # If elif is floating on a line after other code
    # Regex: match non-space non-colon, then space, then elif
    if ' elif ' in line:
        line = line.replace(' elif ', f'\n{indent}elif ')
    
    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Elif splitter complete.")
