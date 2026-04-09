
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
expected_indent = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if not stripped:
        new_lines.append(line)
        continue
    
    current_indent = len(line) - len(line.lstrip())
    
    prev_real_line = None
    for k in range(i-1, -1, -1):
        ps = lines[k].strip()
        if ps:
            if ps.endswith(':') and not ps.startswith('#'):
                prev_real_line = lines[k]
            break
    
    if prev_real_line:
        prev_indent = len(prev_real_line) - len(prev_real_line.lstrip())
        if current_indent <= prev_indent:
            # Indent it!
            print(f"Indenting line {i+1} as it follows a colon.")
            line = (" " * (prev_indent + 4)) + stripped + "\n"
            current_indent = prev_indent + 4
    
    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Mini parser fixer complete.")
