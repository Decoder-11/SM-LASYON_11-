
import os
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find: print(...) followed by code that doesn't belong on that line
# Especially when multiple prints are merged.
# We look for ') print(' or ') kailash_coords' etc.
# But specifically, the Select-String showed 'print(...) print(' is the main culprit.

# Simple split for 'print(...) print('
def split_joined(content):
    # Regex to find print(...) followed by another print or code
    # We look for the closing parenthesis of a print statement followed by whitespace and then another keyword
    # We'll use a specific replacement for the ones found in Select-String
    
    # 1. Handle common print/print split
    content = re.sub(r'(print\(.*?\))\s+(print\()', r'\1\n        \2', content)
    
    # 2. Handle the complex line 1382
    # print("-" * 100) # ELON MUSK AND STARBASE kailash_coords = ...
    # We should probably do this line by line or with a very smart regex
    return content

# Line by line processing is safer for indentation
lines = content.splitlines()
new_lines = []

for line in lines:
    if 'print(' in line and ' print(' in line:
        # Multiple statements on one line
        # Split by ') print('
        parts = re.split(r'(?<=\)) (?=print\()', line)
        if len(parts) > 1:
            indent = line[:len(line) - len(line.lstrip())]
            print(f"Splitting line with multiple prints")
            for p in parts:
                new_lines.append(indent + p.strip())
            continue
            
    if 'print("-" * 100) # ELON MUSK' in line:
        # Special case for line 1382
        indent = line[:len(line) - len(line.lstrip())]
        # This line is very mangled. Let's split it manually by identifying sub-statements.
        # It has: print, kailash_coords, starbase_coords, dist_real, print
        print(f"Special split for line 1382")
        p1 = 'print("-" * 100)'
        p2 = 'kailash_coords = (self.const.KAILASH_LAT, 81.3119)'
        p3 = 'starbase_coords = self.const.COORDS["Starbase"]'
        p4 = 'dist_real = GeoUtils.haversine( kailash_coords[0], kailash_coords[1], starbase_coords[0], starbase_coords[1] )'
        p5 = 'print(f"{Colors.CYAN}1. ELON MUSK AND STARBASE LOCATION:{Colors.RESET}")'
        new_lines.append(indent + p1)
        new_lines.append(indent + p2)
        new_lines.append(indent + p3)
        new_lines.append(indent + p4)
        new_lines.append(indent + p5)
        continue
        
    new_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Splitter complete.")
