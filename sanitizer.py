
import os

target_file = r"c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-\simulasyon_11.py"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Character mapping for math symbols
mapping = {
    '×': '*',
    '÷': '/',
    '−': '-',
    '—': '-',
    '‘': "'",
    '’': "'",
    '“': '"',
    '”': '"',
    '…': '...',
    '°': '',
    '≈': '==', # Or just replace with = depending on context, but == is safer syntactically
    '·': '*',
    '±': '+-',
    '≥': '>=',
    '≤': '<=',
    '≠': '!=',
    'Ω': 'OMEGA',
    'Λ': 'LAMBDA',
    'μ': 'mu'
}

for char, replacement in mapping.items():
    content = content.replace(char, replacement)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Sanitization complete.")
