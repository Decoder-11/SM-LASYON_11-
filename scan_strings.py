
import os
import re

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

if not os.path.exists(target_file):
    print(f"File not found: {target_file}")
    exit(1)

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Scanning for unclosed f-strings or suspicious prints...")

unbalanced = []
for i, line in enumerate(lines):
    # Check for print(f" or print(f' or similar
    if "print(f" in line:
        # Simplified check: count occurrences of " and '
        # This is rough but good for finding the obvious culprits
        dquotes = line.count('"')
        squotes = line.count("'")
        
        # If it's a single line and quotes are odd, it's likely broken
        # unless it's a triple quote multiline string
        if '"""' not in line and "'''" not in line:
            if dquotes % 2 != 0 and '"' in line:
                unbalanced.append((i+1, "dquote", line.strip()))
            if squotes % 2 != 0 and "'" in line:
                unbalanced.append((i+1, "squote", line.strip()))

if unbalanced:
    print(f"Found {len(unbalanced)} potentially unbalanced lines:")
    for num, type, content in unbalanced:
        print(f"Line {num} ({type}): {content}")
else:
    print("No obviously unbalanced single-line prints found.")

print("\nChecking for multi-line tri-quote issues...")
# Search for starts of tri-quotes that don't have an end in the same file
# or just look for the last few hundred lines.
