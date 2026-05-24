
import os
import re
import sys

# Set explicit encoding for stdout to avoid charmap errors
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []

for line in lines:
    stripped = line.strip()
    if not stripped:
        new_lines.append(line)
        continue
        
    indent = line[:len(line) - len(line.lstrip())]
    
    # Aggressive split: detect multiple statements on one line
    # Match ') ' but check if it's likely a split point
    if ') ' in line and ('=' in line or 'print(' in line or 'self.' in line):
        # Look behind for ') ' that is outside of a string is hard, 
        # but in this file, we can split by ') ' and filter.
        tokens = re.split(r'(?<=\)) ', line)
        if len(tokens) > 1:
            # We only split if the second token starts with something 'official'
            current_indent = indent
            for i, t in enumerate(tokens):
                t_stripped = t.strip()
                if not t_stripped: continue
                
                # Check if this token should be on its own line
                # If it's the first token, keep its original relative indent if any
                if i == 0:
                    new_lines.append(indent + t_stripped)
                else:
                    # New line with same indent
                    new_lines.append(indent + t_stripped)
            continue
            
    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Aggressive splitter V2.1 complete.")
