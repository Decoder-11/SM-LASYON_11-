
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # If the line starts an f-string or normal string but doesn't end it
    # Simplified check: line starts with f" or " and doesn't have a closing one on the same line
    # (And we ignore valid multi-line comments)
    if (stripped.startswith('f"') or stripped.startswith('"')) and stripped.count('"') % 2 != 0:
        # Try to join with next lines until closed
        j = i + 1
        while j < len(lines) and (line.strip().count('"') % 2 != 0):
            next_line = lines[j].strip()
            line = line.rstrip() + " " + next_line + "\n"
            j += 1
        new_lines.append(line)
        i = j
    else:
        new_lines.append(line)
        i += 1

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("F-string fixer complete.")
