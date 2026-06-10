import re

file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

marker = 'if __name__ == "__main__":'
idx = content.rfind(marker)

if idx != -1:
    new_tail = '''if __name__ == "__main__":
    run_phase6_and_report()

    import sys
    import io
    import contextlib

    try:
        print("\\n[!] Levhi-Mahfuz Dashboard Sunucusu Baslatiliyor. Cikmak icin hucreyi (STOP) durdurun.")
        start_dashboard()
    except KeyboardInterrupt:
        print("\\n[!] SISTEM DURDURULDU (Kullanici Iptali). OTONOM BUYUK SENTEZ RAPORU OLUSTURULUYOR...\\n")
        
        rapor_dosyasi = "MEGA_RAPOR_CIKTISI.md"
        try:
            f_buf = io.StringIO()
            with contextlib.redirect_stdout(f_buf):
                print_mega_sentez_raporu()
            
            rapor_metni = f_buf.getvalue()
            
            with open(rapor_dosyasi, "w", encoding="utf-8") as f_out:
                f_out.write(rapor_metni)
                
            print(rapor_metni)
            sys.stdout.flush()
                
            print("\\n[OK] OTONOM KAYITLAR VE RAPORLAMA TAMAMLANDI.")
            print(f"[OK] BUYUK RAPOR '{rapor_dosyasi}' DOSYASINA KAYDEDILDI!")
            print("[BILGI] Google Colab kullaniyorsaniz raporu sol menuden (Dosyalar) indirebilirsiniz.")
        except Exception as e:
            print(f"Rapor hatasi: {e}")
            
    except Exception as e:
        print(f"[!] Hata olustu: {e}")
'''
    content = content[:idx] + new_tail

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
