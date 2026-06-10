import sys

with open(r'C:\Users\soldi\IdeaProjects\simülation-11\SIMULASYON_11_FINAL.py', 'r', encoding='utf-8') as f:
    code = f.read()

prefix = 'import sys\nif hasattr(sys.stdout, "reconfigure"):\n    sys.stdout.reconfigure(encoding="utf-8", errors="replace")\n\n'
if not code.startswith("import sys\nif hasattr"):
    code = prefix + code

with open(r'C:\Users\soldi\IdeaProjects\simülation-11\SIMULASYON_11_FINAL.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Injected encoding fix at the top.")
