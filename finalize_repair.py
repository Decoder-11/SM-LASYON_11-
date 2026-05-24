
import os

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

if not os.path.exists(target_file):
    print(f"File not found: {target_file}")
    exit(1)

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
inserted_class = False
added_init = False

for i, line in enumerate(lines):
    # Step 3: Insert class GOBEKLITEPE_Constants:
    if "LATITUDE = 37.223" in line and not inserted_class:
        # Check if class is already there (safety check)
        if "class GOBEKLITEPE_Constants:" not in lines[max(0, i-5):i]:
            new_lines.append("\nclass GOBEKLITEPE_Constants:\n")
            inserted_class = True
    
    new_lines.append(line)
    
    # Step 4: Add self.gobli = GOBEKLITEPE_Constants()
    if "class Modul_KarTopu_V5_V3_Phase3:" in line:
        # Search for the __init__ and add the line after self.phase3
        pass

# Second pass for Step 4 since searching for context is easier with modified list
final_lines = []
for i, line in enumerate(new_lines):
    final_lines.append(line)
    if "self.phase3 = KarTopu_V3_Phase3_Constants()" in line and not added_init:
        # Check if already there
        if i + 1 < len(new_lines) and "self.gobli =" in new_lines[i+1]:
            continue
        final_lines.append("        self.gobli = GOBEKLITEPE_Constants()\n")
        added_init = True

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print(f"Structural repair complete.")
print(f"Inserted class header: {inserted_class}")
print(f"Added gobli initialization: {added_init}")
