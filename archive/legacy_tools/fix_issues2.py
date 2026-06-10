import re

file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix UnboundLocalError by injecting import os at the start of arkaplan_madencisi
content = content.replace(
    'def arkaplan_madencisi():\n    global MINER_DURUM',
    'def arkaplan_madencisi():\n    import os\n    global MINER_DURUM'
)

# 2. Fix the MEGA RAPOR logic for CTRL+C / Colab STOP
marker = 'if __name__ == "__main__":'
idx = content.rfind(marker)

if idx != -1:
    new_tail = '''if __name__ == "__main__":
    run_phase6_and_report()

    import sys
    import time
    class TeeOutput(object):
        def __init__(self, *files):
            self.files = files
        def write(self, obj):
            for f in self.files:
                f.write(obj)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()

    try:
        print("\\n[!] Levhi-Mahfuz Dashboard Sunucusu Baslatiliyor. Cikmak icin hucreyi (STOP) durdurun.")
        start_dashboard()
    except KeyboardInterrupt:
        print("\\n[!] SISTEM DURDURULDU (Kullanici Iptali). OTONOM BUYUK SENTEZ RAPORU OLUSTURULUYOR...\\n")
        
        rapor_dosyasi = "MEGA_RAPOR_CIKTISI.md"
        try:
            with open(rapor_dosyasi, "w", encoding="utf-8") as f_out:
                eski_stdout = sys.stdout
                sys.stdout = TeeOutput(sys.stdout, f_out)
                
                print_mega_sentez_raporu()
                
                sys.stdout = eski_stdout
                
            print("\\n[OK] OTONOM KAYITLAR VE RAPORLAMA TAMAMLANDI.")
            print(f"[OK] BUYUK RAPOR '{rapor_dosyasi}' DOSYASINA KAYDEDILDI!")
        except Exception as e:
            print(f"Rapor hatasi: {e}")
            try: sys.stdout = eski_stdout
            except: pass
            
    except Exception as e:
        print(f"[!] Hata olustu: {e}")
'''
    content = content[:idx] + new_tail

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
