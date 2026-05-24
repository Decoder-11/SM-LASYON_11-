
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith(('elif ', 'else:', 'except:', 'except ', 'finally:')):
        # Find if it's currently over-indented
        current_indent = len(line) - len(line.lstrip())
        
        # Look back for the matching start at a shallow level
        # This is a bit complex, but we can try to find the logic 'if' or 'try'
        # that is just before this one and has a smaller or equal indent.
        
        found = False
        for j in range(i-1, -1, -1):
            prev_line = lines[j]
            prev_stripped = prev_line.strip()
            if not prev_stripped: continue
            
            prev_indent = len(prev_line) - len(prev_line.lstrip())
            
            # If we find an 'if' or 'try' that seems to be the parent
            # Usually it's the first line upwards with a smaller indent
            if prev_indent < current_indent:
                if prev_stripped.startswith(('if ', 'try:', 'for ', 'while ')):
                    # Match this indent
                    indent_str = prev_line[:prev_indent]
                    line = indent_str + stripped + "\n"
                    found = True
                    break
        
    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Smart indenter complete.")
