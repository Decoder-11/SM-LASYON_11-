
import os

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
OPERATORS = ['+', '-', '*', '/', '%', '<', '>', '=', '.', '[', '{']

for line in lines:
    stripped = line.strip()
    if not stripped:
        new_lines.append(line)
        continue
        
    # If the current line starts with an operator and the previous line ends with something that could have it continue
    # actually, ANY line starting with an operator (except maybe unary -) should probably be joined back
    # Also handle the cases where we over-split ') print('
    
    if new_lines and (stripped.startswith(tuple(OPERATORS)) or stripped.startswith('**')):
        # Join to the previous line
        prev = new_lines.pop().rstrip()
        new_lines.append(prev + " " + stripped + "\n")
        continue

    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Re-joining complete.")
