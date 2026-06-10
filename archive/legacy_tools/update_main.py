file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add run_sentez19 call inside run_phase6_and_report function
# Since function name search failed (likely due to encoding), use a different anchor
target = 'if __name__ == "__main__":'
idx = content.rfind(target)

if idx != -1:
    new_main = '''if __name__ == "__main__":
    # --- SENTEZ-19 YENI KESIFLER V.141 ---
    try:
        run_sentez19()
    except Exception as _s19e:
        print(f"[S19] Hata: {_s19e}")

    run_phase6_and_report()

    import sys
    import io
    import contextlib

    try:
        print("\\n[!] Levhi-Mahfuz Dashboard Sunucusu Baslatiliyor. Cikmak icin hucreyi (STOP) durdurun.")
        start_dashboard()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"[!] Hata olustu: {e}")

    print("\\n[!] SISTEM DURDURULDU. OTONOM BUYUK SENTEZ RAPORU OLUSTURULUYOR...\\n")

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
        print(f"[OK] BUYUK RAPOR \'{rapor_dosyasi}\' DOSYASINA KAYDEDILDI!")
        print("[BILGI] Google Colab kullaniyorsaniz raporu sol menuden (Dosyalar) indirebilirsiniz.")
    except Exception as e:
        print(f"Rapor hatasi: {e}")
'''
    content = content[:idx] + new_main
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Ana blok guncellendi! Satir: {len(content.splitlines())}")
else:
    print("Marker bulunamadi!")
