import re

file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. interpolate
content = content.replace("method='interpolate'", "")

# 2. gemini model
content = content.replace("gemini-1.5-pro-latest", "gemini-2.5-pro")
content = content.replace("gemini-1.5-pro", "gemini-2.5-pro")
content = content.replace("gemini-3.5-flash", "gemini-2.5-pro")

# 3. levhi_mahfuz imports
content = re.sub(r'(?m)^\s*from levhi_mahfuz import.*$', '', content)
content = re.sub(r'(?m)^\s*import levhi_mahfuz.*$', '', content)

# 4. empty try blocks
content = re.sub(r'(?m)^(\s*)try:\s*\r?\n\s*except ImportError:', r'\1try:\n\1    pass\n\1except ImportError:', content)

# 5. Constants, Formulas, LMC
content = re.sub(r'\bConstants\.', 'LevhiMahfuzConstants.', content)
content = re.sub(r'\bFormulas\.', 'LevhiMahfuzFormulas.', content)
content = re.sub(r'\bLMC\.', 'LevhiMahfuzConstants.', content)

# 6. __file__ fixes
content = content.replace('BASE_DIR = os.path.dirname(os.path.abspath(__file__))', "BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()")
content = content.replace('target_file = __file__', "target_file = __file__ if '__file__' in globals() else 'SIMULASYON_11_FINAL.py'")
content = content.replace('os.path.dirname(os.path.abspath(__file__))', "(os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd())")
content = content.replace('pytest.main([__file__, "-v"])', "pytest.main([__file__ if '__file__' in globals() else 'SIMULASYON_11_FINAL.py', '-v'])")

# 7. sys.stdout issues
content = content.replace("sys.stdout.reconfigure(encoding='utf-8')", "pass # sys.stdout.reconfigure(encoding='utf-8')")
content = content.replace("sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')", "pass # Colab bypass")

# 8. the final block
marker = 'if __name__ == "__main__":'
idx = content.rfind(marker)  # FIND THE LAST OCCURRENCE!

if idx != -1:
    new_tail = '''if __name__ == "__main__":
    run_phase6_and_report()

    print("\\n[!] OTONOM BÜYÜK SENTEZ RAPORU OLUÞTURULUYOR (Colab için öne alýndý)...\\n")
    import sys
    import time
    class TeeOutput(object):
        def __init__(self, *files):
            self.files = files
        def write(self, obj):
            for f in self.files:
                f.write(obj)
                f.flush()
            if len(obj.strip()) > 0:
                time.sleep(0.01) # Hizlandirildi
        def flush(self):
            for f in self.files:
                f.flush()
                
    rapor_dosyasi = "MEGA_RAPOR_CIKTISI.md"
    try:
        with open(rapor_dosyasi, "w", encoding="utf-8") as f_out:
            eski_stdout = sys.stdout
            sys.stdout = TeeOutput(sys.stdout, f_out)
            
            print_mega_sentez_raporu()
            
            sys.stdout = eski_stdout
            
        print("\\n[?] OTONOM KAYITLAR VE RAPORLAMA TAMAMLANDI.")
        print(f"[?] BÜYÜK RAPOR '{rapor_dosyasi}' DOSYASINA KAYDEDÝLDÝ!")
    except Exception as e:
        print(f"Rapor hatasi: {e}")
        try: sys.stdout = eski_stdout
        except: pass

    try:
        print("\\n[!] Levhi-Mahfuz Dashboard Sunucusu Baslatiliyor. Cikmak icin hucreyi (STOP) durdurun.")
        start_dashboard()
    except KeyboardInterrupt:
        print("\\n[!] SÝSTEM DURDURULDU (Kullanýcý Ýptali).")
    except Exception as e:
        print(f"[!] Hata oluþtu: {e}")
'''
    content = content[:idx] + new_tail

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
