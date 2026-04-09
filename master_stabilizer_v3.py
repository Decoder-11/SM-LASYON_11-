
import os

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until = -1
within_class = False

# Things that definitively mean a class has ended if found at col 0
CLASS_STOPPERS = ['try:', 'import ', 'from ', '# =', '# -', 'if __name__', 'GEN_LANG', 'ROCHE_', 'def ai_status_report', '_GENERAVITY']

for i in range(len(lines)):
    if i <= skip_until:
        continue
        
    line = lines[i]
    stripped = line.strip()
    
    # 1. Detect Class Start
    if line.startswith('class '):
        within_class = True
        new_lines.append(line)
        continue
        
    # 2. Detect Class End (Col 0 check)
    if within_class:
        # If it starts with a stopper at col 0, or it's a known global
        for stopper in CLASS_STOPPERS:
            if line.startswith(stopper):
                print(f"Class ended at line {i+1} by '{stopper}'")
                within_class = False
                break

    # 3. Join strings (re-run as it's the most common failure)
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

    # 4. Correct Indentation
    if within_class and line.strip() and not line.startswith('    ') and not line.startswith('class '):
        # Indent it
        new_lines.append("    " + line)
    elif not within_class and line.startswith('    ') and (line.strip().startswith('def ') or line.strip().startswith('try:') or line.strip().startswith('import ')):
        # Potentially over-indented due to previous bad runs
        # Only unindent if it's a known global pattern or top-level thing
        # For now, let's just unindent if it starts with '    try:' or '    def' and we are NOT in a class
        print(f"Fixing over-indent at line {i+1}")
        new_lines.append(line[4:])
    else:
        new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Master stabilization V3 complete.")
