#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAZ-3 modülünü SIMULASYON_11_FINAL.py sonuna ekler."""
import sys
import os

def main():
    # Faz3 modülünü oku
    faz3_path = r'sm_lasyon_repo\faz3_yeni_kesifler_modulu.py'
    with open(faz3_path, 'r', encoding='utf-8') as f:
        faz3_content = f.read()
    
    # Shebang satırını atla
    lines = faz3_content.split('\n')
    if lines[0].startswith('#!/usr/bin/env python'):
        lines = lines[1:]
    faz3_clean = '\n'.join(lines)
    
    # Ayırıcı yorum bloğu
    separator = '''
# =============================================================================
# FAZ-3: 85 YENİ KEŞİF MODÜLÜ (PDF+JPG+PNG+DOCX+MD+PY sentezi)
# Entegrasyon Tarihi: 2026-05-13
# Kategoriler: 11D Fizik, Hüdhüd, Karanlık Enerji, Anti-Gravite, 
#              Kozmik Döngüler, Geoid Matris, Pi_11, DECODER-11/Grok
# =============================================================================
'''
    
    # Sonlandırma yorumu
    footer = '''
# =============================================================================
# FAZ-3 ENTEGRASYONU TAMAMLANDI
# Entegrasyon Tarihi: 2026-05-13
# Eklenen modül: faz3_yeni_kesifler_modulu.py (85 keşif, 8 kategori)
# =============================================================================
'''
    
    # Hedef dosyaya ekle
    target = r'C:\Users\soldi\IdeaProjects\simülation-11\SIMULASYON_11_FINAL.py'
    
    # Önce mevcut satır sayısını al
    with open(target, 'r', encoding='utf-8') as f:
        old_content = f.read()
    old_lines = old_content.split('\n')
    old_count = len(old_lines)
    
    # Sonuna ekle
    with open(target, 'a', encoding='utf-8') as f:
        f.write(separator)
        f.write(faz3_clean)
        f.write(footer)
    
    # Yeni satır sayısını al
    with open(target, 'r', encoding='utf-8') as f:
        new_content = f.read()
    new_lines = new_content.split('\n')
    new_count = len(new_lines)
    
    # Doğrulama
    has_faz3 = 'FAZ-3: 85 YENİ KEŞİF MODÜLÜ' in new_content
    has_main = 'if __name__ == "__main__":' in new_content
    
    # Sonuçları dosyaya yaz
    report_path = r'sm_lasyon_repo\entegrasyon_sonuc.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f'Entegrasyon öncesi satır: {old_count}\n')
        f.write(f'Entegrasyon sonrası satır: {new_count}\n')
        f.write(f'Eklenen satır: {new_count - old_count}\n')
        f.write(f'FAZ-3 modülü bulundu: {has_faz3}\n')
        f.write(f'__main__ blogu korundu: {has_main}\n')
        f.write(f'Null byte sayisi: {new_content.count(chr(0))}\n')
        f.write(f'BOM: {new_content.startswith(chr(0xfeff))}\n')
    
    print(f'OK: {old_count} -> {new_count} satir, FAZ-3={has_faz3}, main={has_main}')

if __name__ == '__main__':
    main()
