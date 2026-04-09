
import os
import re


target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace 3 or more newlines with 2 newlines
new_content = re.sub(r'\n{3,}', '\n\n', content)

# Also fix the weird split at SOURCE_ALIGNMENT_STRONG
new_content = new_content.replace('# "Source (1)\n    alignment strong"', '# "Source (1) alignment strong"')

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Collapse complete.")
