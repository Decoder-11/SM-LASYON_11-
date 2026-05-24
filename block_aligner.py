
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith(('elif ', 'else:', 'except:', 'except ', 'finally:')):
        # We need to find the parent.
        # Parent keywords for each:
        # elif/else -> if
        # except/finally/else -> try
        
        target_parents = []
        if stripped.startswith(('elif ', 'else:')):
            target_parents = ['if', 'elif', 'for', 'while', 'try'] 
        if stripped.startswith(('except', 'finally:')):
            target_parents = ['try']
            
        found_indent = None
        for j in range(i-1, -1, -1):
            prev_line = lines[j]
            ps = prev_line.strip()
            if not ps: continue
            
            # If we find a line starting with a parent keyword
            if any(ps.startswith(p) for p in target_parents):
                # This is a likely candidate. Match its indent.
                found_indent = len(prev_line) - len(prev_line.lstrip())
                # However, if it's an 'if' inside another block, we want the "matching" one.
                # This is hard without full parsing, but usually it's the closest one
                # that doesn't have a sibling yet? 
                # Let's just take the closest one for now, it's better than nothing.
                break
        
        if found_indent is not None:
            line = (" " * found_indent) + stripped + "\n"
            
    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Block aligner complete.")
