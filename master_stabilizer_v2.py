
import os
import sys

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until = -1
within_class = False

# Known global functions that should be at col 0
GLOBAL_FUNCTIONS = ['ai_status_report', 'loading_bar', 'main_logic', 'run_simulation']

for i in range(len(lines)):
    if i <= skip_until:
        continue
        
    line = lines[i]
    stripped = line.strip()
    col0 = line.startswith(tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")) or line.startswith('_')
    
    # 1. Handle Class boundaries
    if line.startswith('class '):
        within_class = True
        new_lines.append(line)
        continue
        
    # 2. Handle specific global indicators that end class scope
    if line.startswith('if __name__ == "__main__":'):
        within_class = False
        new_lines.append(line)
        continue

    # 3. Handle redundant Simule3_Constants at 6491
    # Line 6491 in original was 'class Simule3_Constants:' (now shifted)
    if 'class Simule3_Constants:' in line and i > 100: # 43 is the good one
        print(f"Skipping redundant Simule3_Constants at line {i+1}")
        # Skip until the next class or significant block
        skip_count = 0
        for j in range(i + 1, len(lines)):
            if lines[j].startswith('class ') or lines[j].startswith('# ---'):
                skip_count = j - i - 1
                break
        skip_until = i + skip_count
        continue

    # 4. Handle Indentation
    if within_class and col0 and not line.startswith('class '):
        # Is it a global function we shouldn't indent?
        is_global = False
        for gf in GLOBAL_FUNCTIONS:
            if stripped.startswith(f'def {gf}('):
                is_global = True
                break
        
        if not is_global:
            # It's a method or property inside a class that lost its indent
            print(f"Fixing indent for {stripped[:20]}... at line {i+1}")
            new_lines.append("    " + line)
            continue

    # 5. Handle unclosed prints (re-run logic to be safe)
    is_print = (stripped.startswith('print(f"') or stripped.startswith('print("') or 
                stripped.startswith("print(f'") or stripped.startswith("print('"))
    is_closed = stripped.endswith('")') or stripped.endswith("')") or stripped.endswith('") #') or stripped.endswith("') #")
    
    if is_print and not is_closed and '"""' not in line:
        current_block = line.rstrip()
        merged_count = 0
        for j in range(i + 1, min(i + 10, len(lines))):
            next_line = lines[j].strip()
            current_block += " " + next_line
            if next_line.endswith('")') or next_line.endswith("')"):
                merged_count = j - i
                break
        if merged_count > 0:
            new_lines.append(current_block + "\n")
            skip_until = i + merged_count
            continue

    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Final stabilization and deduplication complete.")
