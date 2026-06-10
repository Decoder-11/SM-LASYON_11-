import os

with open(r'C:\Users\soldi\IdeaProjects\simülation-11\append_synthesis.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('Sentezleri:\\")', 'Sentezleri:")')

with open(r'C:\Users\soldi\IdeaProjects\simülation-11\SIMULASYON_11_FINAL.py', 'a', encoding='utf-8') as f:
    f.write('\n' + code)

print("Appended successfully.")
