
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    if not line:
        new_lines.append("\n")
        i += 1
        continue
    
    # Check if this line should be joined to the NEXT line (e.g. ends with 'or', 'and', '=')
    # Actually, it's easier to check if the NEXT line starts with an operator and join it to the CURRENT.
    
    while i + 1 < len(lines):
        next_line = lines[i+1].strip()
        if not next_line:
            # Skip empty lines to look for the next real content
            # Wait, if we have an empty line between fragments, should we delete it?
            # Usually yes if it's a split statement.
            temp_next_i = i + 1
            while temp_next_i < len(lines) and not lines[temp_next_i].strip():
                temp_next_i += 1
            if temp_next_i < len(lines):
                next_content = lines[temp_next_i].strip()
                # If next real content starts with 'or', 'and', etc.
                if re.match(r'^(or |and |else |elif |==|!=|<=|>=|<|>|\+|\*|/|%|&|\||\^)', next_content):
                    line = line + " " + next_content
                    i = temp_next_i
                    continue
        
        if re.match(r'^(or |and |else |elif |==|!=|<=|>=|<|>|\+|\*|/|%|&|\||\^)', next_line):
            line = line + " " + next_line
            i += 1
        else:
            break
            
    new_lines.append(line + "\n")
    i += 1

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Super joiner complete.")
