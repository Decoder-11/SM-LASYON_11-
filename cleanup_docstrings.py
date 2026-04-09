
import os

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"
patterns = [
    '"""Gobekli Tepe Temple - Oldest Known Religious Structure (~11,500 BCE)"""',
    '"""33 Vertebrae - Spinal Quantum Code (Human Biology Lock)"""'
]

if not os.path.exists(target_file):
    print(f"File not found: {target_file}")
    exit(1)

print(f"Cleaning up {target_file}...")

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
count = 0
for line in lines:
    skip = False
    for pattern in patterns:
        if pattern in line:
            skip = True
            break
    if skip:
        count += 1
        continue
    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Removed {count} problematic lines total.")
