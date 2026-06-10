import re
file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('self.const = LMC', 'self.const = LevhiMahfuzConstants')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
