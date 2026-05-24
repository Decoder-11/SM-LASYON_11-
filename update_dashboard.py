import os
path = r'C:\Users\soldi\IdeaProjects\simülation-11\dashboard_11.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. KADIM_SABITLER guncelleme
eski_sabitler = '''    KADIM_SABITLER = {
        11: "11 BOYUTLU TEMEL MATRİS (11)",
        33: "ÜÇLÜ SİGMA (33)",
        66: "ORTA DİKME PİRAMİT SABİTİ (66)",
        1331: "HACİM SABİTİ İHLALİ (11³)",
        3333: "KADİM DOSYA MESAFESİ (3333)",
        3630: "KOZMİK KOORDİNAT - AY/HATAY (3630)",
        6666: "DÜNYA/KAILASH RADYAL KESİŞİMİ (6666)",
        40075: "DÜNYA ÇEVRESİ (40075 km)",
        299792: "IŞIK HIZI EŞLEŞMESİ (299,792 km/s)",
        6.626: "PLANCK SABİTİ (6.626)",
        3.14159: "Pİ SABİTİ (π)",
        1.618: "ALTIN ORAN (Φ) FREKANSI"
    }'''

yeni_sabitler = '''    # KADİM SABİTLER SÖZLÜĞÜ (Fizik, Astronomi, Kadim Yapılar ve Sentez-45/46)
    KADIM_SABITLER = {
        11: "11 BOYUTLU TEMEL MATRİS (11)",
        33: "ÜÇLÜ SİGMA (33)",
        66: "ORTA DİKME PİRAMİT SABİTİ (66)",
        363: "ORGANİK SİMÜLASYON YILI (363)",
        1331: "HACİM SABİTİ İHLALİ (11³)",
        3333: "KADİM DOSYA MESAFESİ (3333)",
        3630: "KOZMİK KOORDİNAT - AY/HATAY (3630)",
        6666: "DÜNYA/KAILASH RADYAL KESİŞİMİ (6666)",
        40075: "DÜNYA ÇEVRESİ (40075 km)",
        299792: "IŞIK HIZI EŞLEŞMESİ (299,792 km/s)",
        6.626: "PLANCK SABİTİ (6.626)",
        6.666: "MATRİS LAMBDA KIRILIMI (6.666)",
        3.14159: "Pİ SABİTİ (π)",
        1.618: "ALTIN ORAN (Φ) FREKANSI",
        1.1091: "FREKANS GENİŞLEME ÇARPANI (1.1091)",
        1.1454: "HACİM VE KÜTLE GENLEŞME SABİTİ (1.1454)",
        0.8602: "MİKRO UZUNLUK SAPMASI (0.8602)",
        0.9016: "EVRENSEL ZAMAN SAPMASI (0.9016)"
    }'''

content = content.replace(eski_sabitler, yeni_sabitler)

# 2. piramit_koda_yaz fonksiyonunu yeni_modul_teklifi_olustur ile degistirme
eski_piramit = '''def piramit_koda_yaz(sabit_deger, islem_aciklama):
    try:
        hedef_yol = os.path.join(BASE_DIR, "S-M-LASYON_11-main", "simulasyon_11.py")
        if os.path.exists(hedef_yol):
            with open(hedef_yol, "a", encoding="utf-8") as f:
                tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                func_id = random.randint(1000, 9999)
                f.write(f"\\n# [OTONOM KUANTUM KOD ENJEKSİYONU] {tarih}\\n")
                f.write(f"def kozmik_dalga_fonksiyonu_gen{func_id}(psi):\\n")
                f.write(f"    # SENTEZ MODELİ: {islem_aciklama}\\n")
                f.write(f"    SIGMA_SABITI = {sabit_deger}\\n")
                f.write(f"    return (psi ** 2 + SIGMA_SABITI) / 11.0\\n")
    except:
        pass'''

yeni_modul = '''def yeni_modul_teklifi_olustur(sabit_deger, islem_aciklama, kategori):
    try:
        tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        func_id = random.randint(1000, 9999)
        
        # Dinamik Python kodu uretimi
        modul_kodu = f"""
# [YAPAY ZEKA MODÜL ÖNERİSİ] 
# Sentez Modeli: {islem_aciklama}
# Bulunan Sabit Değer: {sabit_deger}

def otonom_sentez_fonksiyonu_{func_id}(x_input, zaman_faktoru=1.1091):
    \"\"\"
    Bu fonksiyon yapay zeka tarafından tespit edilen örüntüye göre üretilmiştir.
    \"\"\"
    KADIM_SABIT = {sabit_deger}
    
    # 11'lik sistem matris genişleme algoritması
    sonuc = (x_input * KADIM_SABIT) / zaman_faktoru
    return sonuc
"""
        # Veritabanına kaydet
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ModulOnerileri (tarih, kategori, modul_kodu, aciklama) VALUES (?, ?, ?, ?)",
                       (tarih, kategori, modul_kodu, islem_aciklama))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Modul onerisi hatasi:", e)'''

content = content.replace(eski_piramit, yeni_modul)

# 3. sentez_motoru icindeki cagrinin guncellenmesi
content = content.replace("piramit_koda_yaz(sonuc, detay)", "yeni_modul_teklifi_olustur(sonuc, detay, kategori_etiketi)")

# 4. rapor_sun methoduna modul onerilerini ekleme
eski_rapor_yaz = '''        f.write(f"## ❄️ KAR TOPU ÖĞRENME ALGORİTMASI LOGLARI (Son 100 İşlem)\\n")
        for log in kartopu[:100]:
            f.write(f"- **[{log[0]}]** Kaynak: `{log[1]}` | Veri: {log[2]} | Analiz: {log[3]}\\n")
            
    return jsonify({"status": "ok", "dosya_yolu": rapor_yolu, "isim": dosya_adi})'''

yeni_rapor_yaz = '''        f.write(f"## ❄️ KAR TOPU ÖĞRENME ALGORİTMASI LOGLARI (Son 100 İşlem)\\n")
        for log in kartopu[:100]:
            f.write(f"- **[{log[0]}]** Kaynak: `{log[1]}` | Veri: {log[2]} | Analiz: {log[3]}\\n")
            
        f.write("\\n---\\n\\n")
        f.write("## 🤖 OTONOM YAPAY ZEKA MODÜL ÖNERİLERİ (ONAY BEKLİYOR)\\n\\n")
        f.write("> Sistem, yukarıdaki keşiflerden ve örüntülerden yola çıkarak aşağıdaki Python fonksiyonlarını tasarlamıştır.\\n")
        f.write("> Lütfen bu modülleri inceleyin. Uygun bulursanız ana koda (SIMULASYON_11_FINAL.py) entegre edilecektir.\\n\\n")
        
        try:
            conn2 = sqlite3.connect(DB_YOLU)
            cur2 = conn2.cursor()
            cur2.execute("SELECT tarih, aciklama, modul_kodu FROM ModulOnerileri ORDER BY id DESC LIMIT 10")
            oneriler = cur2.fetchall()
            conn2.close()
            
            if not oneriler:
                f.write("*Henüz üretilmiş yeni bir modül önerisi bulunmuyor.*\\n")
            else:
                for oner in oneriler:
                    f.write(f"### 💡 Öneri Tarihi: {oner[0]}\\n")
                    f.write(f"**Tespit & Akıl Yürütme:** {oner[1]}\\n\\n")
                    f.write("```python\\n")
                    f.write(f"{oner[2]}\\n")
                    f.write("```\\n\\n")
        except Exception as e:
            f.write(f"*Modül önerileri yüklenirken hata oluştu: {str(e)}*\\n")
            
    return jsonify({"status": "ok", "dosya_yolu": rapor_yolu, "isim": dosya_adi})'''

content = content.replace(eski_rapor_yaz, yeni_rapor_yaz)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Dashboard updated successfully')
