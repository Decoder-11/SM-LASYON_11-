import os
path = r'C:\Users\soldi\IdeaProjects\simülation-11\dashboard_11.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "def rapor_sun():" in line:
        skip = True
        
    if skip and "return jsonify" in line and "dosya_yolu" in line:
        skip = False
        new_lines.append('''def rapor_sun():
    conn = sqlite3.connect(DB_YOLU)
    cursor = conn.cursor()
    try:
        simdi = datetime.now()
        cursor.execute("SELECT tarih, islem_turu, deger, kategori, aciklama FROM Kesifler ORDER BY id DESC")
        tum_kesifler = cursor.fetchall()
        
        cursor.execute("SELECT tarih, kaynak, veri, analiz FROM KarTopu ORDER BY id DESC")
        tum_kartopu = cursor.fetchall()
        
        cursor.execute("SELECT tarih, aciklama, modul_kodu FROM ModulOnerileri ORDER BY id DESC LIMIT 10")
        modul_onerileri = cursor.fetchall()
        
    except Exception as e:
        tum_kesifler = []
        tum_kartopu = []
        modul_onerileri = []
    finally:
        conn.close()
        
    tarih_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    dosya_adi = f"LEVHI_MAHFUZ_EVRIM_RAPORU_{tarih_str}.md"
    rapor_yolu = os.path.join(BASE_DIR, dosya_adi)
    
    with open(rapor_yolu, "w", encoding="utf-8") as f:
        f.write("# 🕸️ LEVH-İ MAHFUZ OTONOM SİSTEMİ - BÜYÜK SENTEZ VE EVRİM RAPORU\\n\\n")
        f.write(f"**Oluşturulma Tarihi:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        f.write("> Sistem, veri tabanındaki PDF, JPG, MD, Word, Py dosyalarını ve Akademik Dış Ağları (arXiv, NASA, viXra, Üniversiteler, Wikipedia) süzerek evrensel sabitleri sentezlemiştir.\\n\\n")
        
        f.write("## 🟢 BÖLÜM 1: GÜNLÜK BÜLTEN VE TAZE BULGULAR\\n")
        f.write("> Son dönemde sisteme giren verilerden çıkarılan anlık taze eşleşmeler ve keşifler.\\n\\n")
        
        for k in tum_kesifler[:30]:
            f.write(f"- **[{k[0]}]** | {k[3]} | Değer: `{k[2]}` \\n  *Detay:* {k[4]}\\n")
        
        f.write("\\n---\\n\\n")
        
        f.write("## 🕸️ BÖLÜM 2: ÖRÜMCEK AĞI VE KARTOPU EVRİMİ (BÜYÜK RESİM)\\n")
        f.write("> Bu bölüm, sisteme bugüne kadar eklenen kadim sabitlerin, yeni formüllerle (örn: Göbeklitepe, Vopson, 1.1091 Frekans Sapması) nasıl birleştiğini, evrensel ağın nasıl örüldüğünü gösterir.\\n\\n")
        
        f.write("### Kar Topu Gelişim Logları (Örüntü Bağlantıları)\\n")
        for log in tum_kartopu[:70]:
            f.write(f"- 🔗 **[{log[0]}]** *{log[1]}* üzerinden `{log[2]}` verisi emildi. \\n  **Sentez ve Adaptasyon:** {log[3]}\\n")
            
        f.write("\\n---\\n\\n")
        
        f.write("## 🤖 BÖLÜM 3: YAPAY ZEKA MODÜL ÖNERİLERİ (ONAY BEKLİYOR)\\n")
        f.write("> Sistem, yukarıdaki devasa örümcek ağından yola çıkarak aşağıdaki Python formül/fonksiyon modüllerini tasarlamıştır. Bunlar SIMULASYON_11_FINAL.py çekirdeğine doğrudan ENJEKTE EDİLMEMİŞTİR. Otonom motor sadece sana önerir, sen onaylarsan eklersin.\\n\\n")
        
        if not modul_onerileri:
            f.write("*Henüz üretilmiş yeni bir modül önerisi bulunmuyor.*\\n")
        else:
            for oner in modul_onerileri:
                f.write(f"### 💡 Öneri Tarihi: {oner[0]}\\n")
                f.write(f"**Tespit & Akıl Yürütme Sentezi:** {oner[1]}\\n\\n")
                f.write("```python\\n")
                f.write(f"{oner[2]}\\n")
                f.write("```\\n\\n")
                
    return jsonify({"status": "ok", "dosya_yolu": rapor_yolu, "isim": dosya_adi})\n''')
        continue

    if not skip:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Dashboard reporting function fixed.")
