#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix import requests issue in simulasyon_11.py"""

# simulasyon_11.py düzelt - import requests hatasını kaldır
with open('simulasyon_11.py', encoding='utf-8') as f:
    content = f.read()

# Tüm "        import requests" (function içinde) satırlarını bul ve değiştir
# Pattern: boşluklar + "import requests"
import re

# Function içindeki requests import'ını global variable kullanımıyla değiştir
pattern = r'(\n\s{8,12})import requests(\n)'
replacement = r'\1# requests modulü başında import edilmiş (global scope)\n\1if requests is None:\n\1    print(f"{Colors.FAIL}requests modülü yüklü değil{Colors.RESET}")\n\1    return\2'

content_fixed = re.sub(pattern, replacement, content)

# Yaz
with open('simulasyon_11.py', 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print(f"✅ Dosya düzeltildi")
if content != content_fixed:
    print(f"✅ import requests hatası düzeltildi")
else:
    print(f"⚠️  Değişiklik yapılmadı")

