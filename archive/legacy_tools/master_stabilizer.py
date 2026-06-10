
import os
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

if not os.path.exists(target_file):
    print(f"File not found: {target_file}")
    exit(1)

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until = -1

for i in range(len(lines)):
    if i <= skip_until:
        continue
    
    line = lines[i]
    stripped = line.strip()
    
    # Check for unclosed print(f" or print(" or print(f' or print('
    # Pattern: starts with print(f" or print(" and DOES NOT end with ") or ')
    # Also ignore triple quoted strings which are handles differently
    is_print = (stripped.startswith('print(f"') or stripped.startswith('print("') or 
                stripped.startswith("print(f'") or stripped.startswith("print('"))
    
    is_closed = stripped.endswith('")') or stripped.endswith("')") or stripped.endswith('") #') or stripped.endswith("') #")
    
    # Special case: print(f"..." + ...) or similar might not end with ")
    # But for this codebase, most broken ones are simple splits.
    
    if is_print and not is_closed and '"""' not in line and "'''" not in line:
        # Potential split string. Try to join next lines.
        current_block = line.rstrip()
        merged_count = 0
        for j in range(i + 1, min(i + 5, len(lines))): # Look ahead up to 5 lines
            next_line = lines[j].strip()
            current_block += " " + next_line
            if next_line.endswith('")') or next_line.endswith("')"):
                merged_count = j - i
                break
        
        if merged_count > 0:
            print(f"Joining lines {i+1} to {i+1+merged_count}")
            new_lines.append(current_block + "\n")
            skip_until = i + merged_count
            continue

    # Fallback: fix indentation for methods if they are at col 0
    if stripped.startswith('def ') and not line.startswith('    '):
        # Check if we are inside a class block (heuristic)
        # In this file, almost all defs belong to a class and should be indented 4 spaces
        print(f"Indenting method at line {i+1}")
        new_lines.append("    " + line)
        continue

    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Master stabilization complete.")
