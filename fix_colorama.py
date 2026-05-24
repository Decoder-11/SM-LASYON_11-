import re

with open('simulasyon_11.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 1. Remove all colorama imports
content = re.sub(r'from colorama import[^\n]*\n', '', content)
content = re.sub(r'import colorama[^\n]*\n', '', content)

# 2. Remove time.sleep calls that came with colorama
content = re.sub(r'        time\.sleep\(0\.5\)\n', '', content)

# 3. Replace all Fore.X -> Colors.X mappings
color_map = {
    'Fore.RED':     'Colors.RED',
    'Fore.GREEN':   'Colors.GREEN',
    'Fore.YELLOW':  'Colors.YELLOW',
    'Fore.BLUE':    'Colors.BLUE',
    'Fore.MAGENTA': 'Colors.MAGENTA',
    'Fore.CYAN':    'Colors.CYAN',
    'Fore.WHITE':   'Colors.RESET',
    'Fore.RESET':   'Colors.RESET',
    'Style.RESET_ALL': 'Colors.RESET',
    'Style.BRIGHT':    'Colors.BOLD',
    'Style.DIM':       'Colors.RESET',
}
for old, new in color_map.items():
    content = content.replace(old, new)

# 4. Remove orphan corrupted fragments introduced by failed replacements
bad_lines = [
    'ter_energy_ev:.4f} eV")',
    'gy_ev:.4f} eV")',
    'f} eV")',
]
lines = content.split('\n')
clean_lines = []
for line in lines:
    skip = False
    for bad in bad_lines:
        if bad in line and 'print' not in line:
            skip = True
            break
    if not skip:
        clean_lines.append(line)
content = '\n'.join(clean_lines)

# 5. Fix broken multi-line print caused by f" # ===..." embed
content = re.sub(
    r'print\(f" # =+\n# SENTEZ-11.*?\n# =+\n\n',
    '',
    content,
    flags=re.DOTALL
)

# 6. Fix the broken comment-print mashup: print(f"      # Final\n -> proper closing
bad_pattern = r'print\(f"        # Final\n'
replacement = '# Final\n        '
content = re.sub(bad_pattern, replacement, content)

with open('simulasyon_11.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: simulasyon_11.py fixed successfully.")
print(f"Total lines: {len(content.splitlines())}")

# Verify no more colorama references
remaining = [i+1 for i, line in enumerate(content.splitlines()) if 'colorama' in line or 'Fore.' in line or ('Style.' in line and 'RESET_ALL' in line)]
if remaining:
    print(f"WARNING: Remaining colorama refs at lines: {remaining}")
else:
    print("OK: No colorama references remaining.")
