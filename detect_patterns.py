
import os
import re
import sys
from collections import Counter

# Set stdout to UTF-8 to avoid encoding errors on Windows
sys.stdout.reconfigure(encoding='utf-8')

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

if not os.path.exists(target_file):
    print(f"File not found: {target_file}")
    exit(1)

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()
    lines = text.splitlines()

# Extract content between triple quotes on single lines
pattern = re.compile(r'"""(.*?)"""')
docstring_counts = Counter()

for line in lines:
    matches = pattern.findall(line)
    for m in matches:
        docstring_counts[f'"""{m}"""'] += 1

print("Docstring frequency (Top 20):")
for doc, count in docstring_counts.most_common(20):
    print(f"{count}: {doc}")

print("\nChecking for odd occurrences of triple quotes (potential unclosed strings):")
triple_quote_count = text.count('"""')

print(f"Total triple quotes (''' or \"\"\"):")
print(f'Double triple quotes ("""): {text.count('"""')}')
print(f"Single triple quotes ('''): {text.count("'''")}")

if text.count('"""') % 2 != 0:
    print('WARNING: Odd number of """ detected!')
if text.count("'''") % 2 != 0:
    print("WARNING: Odd number of ''' detected!")

# Find double definitions or suspicious patterns
print("\nSuspicious repeated single-line docstrings:")
for doc, count in docstring_counts.items():
    if count > 1:
        print(f"REPEATED ({count}): {doc}")

