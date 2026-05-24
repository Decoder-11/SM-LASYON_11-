
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []

for line in lines:
    # Handle the specific case at 2405: ] space identifier =
    # Regex: replace '] ' with ']\n[indent]' if followed by an assignment
    
    # We find the indent
    m = re.match(r'^(\s*)', line)
    indent = m.group(1) if m else ""
    
    # Heuristic: split if we see ] or ) followed by a space and an identifier then an equal sign
    # e.g. ] dist_real =
    line = re.sub(r'([\)\]])\s+([a-zA-Z_][a-zA-Z0-9_]*\s*=)', rf'\1\n{indent}\2', line)
    
    # Also handle multiple assignments like x = 1 y = 2
    # Regex: matches space, identifier, space, equal, not preceded by comma
    # line = re.sub(r'(?<!,)\s+([a-zA-Z_][a-zA-Z0-9_]*\s*=[^=])', rf'\n{indent}\1', line)
    # This is dangerous. Let's stick to the brackets first.

    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Triple splitter complete.")
