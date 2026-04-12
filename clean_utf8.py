import os
import re

path = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"
# Read using utf-8-sig to automatically handle BOM
with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
    content = f.read()

# Unified cleanup of corrupted or problematic characters
replacements = {
    "\u252c\u2591": "(deg)",
    "\u252c\u2592": "(deg)",
    "\u2500\u2591": "i",
    "\u2500\u2592": "i",
    "┬░": "(deg)",
    "âœ“": "[V]",
    "â†“": "->",
    "├ù": "x",
    "╬╝": "u",
    "┬ö": "-",
    "Ô£ô": "[V]",
    "ÔåÆ": "->",
    "ÔÇö": "--",
    "Ô£à": "[V]",
    "âœ…": "[V]",
    "┬░": "(deg)",
    "\u00b0": "(deg)",
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Final aggressive pass: 
# Instead of replacing the whole file, let's only replace non-ASCII 
# if they are within print() or quote marks. 
# But to be safe and simple, we'll just remove the leading '?' created by the previous run.
content = content.lstrip("?")

# Also ensure we don't have any '?' at the start of lines like '?import'
content = content.replace("\n?import", "\nimport")
content = content.replace("\n?from", "\nfrom")
content = content.replace("\n?class", "\nclass")
content = content.replace("\n?def", "\ndef")

with open(path, "w", encoding="utf8") as f:
    f.write(content)

print("Targeted ASCII cleanup complete.")
