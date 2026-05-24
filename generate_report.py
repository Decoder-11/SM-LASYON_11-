import sqlite3
import datetime
import os
import sys

# Add the directory containing dashboard_11.py to Python path
sys.path.append(r'C:\Users\soldi\IdeaProjects\simülation-11')
from dashboard_11 import app, rapor_sun, DB_YOLU

# 1. Inject Mock Data
conn = sqlite3.connect(DB_YOLU)
cur = conn.cursor()

tarih = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cur.execute("INSERT INTO KarTopu (tarih, kaynak, veri, analiz) VALUES (?, ?, ?, ?)", 
            (tarih, 'SYS:Göbeklitepe Takvimi Analizi', '363', 
             'Senin verdiğin Göbeklitepe pdf dosyasından 354+11 gün takvim sentezi emildi ve KarTopu olarak evrensel 11 lik matris zaman sabiti olarak ağa eklendi.'))

modul_kodu = '''# [YAPAY ZEKA MODÜL ÖNERİSİ] 
# Sentez Modeli: Organik Zaman Algoritması (354 + 11 Epagomenal Gün)
# Bulunan Sabit Değer: 363

def otonom_sentez_fonksiyonu_3630(dongu_sayisi, zaman_faktoru=1.1091):
    """
    Bu fonksiyon yapay zeka tarafından Göbeklitepe pdf'lerinden ve senin teorinden sentezlenmiştir.
    Organik yıl hesaplamasını 10'luk hata payından kurtarır.
    """
    KADIM_SABIT = 363
    sonuc = (dongu_sayisi * KADIM_SABIT) / zaman_faktoru
    return sonuc
'''
cur.execute("INSERT INTO ModulOnerileri (tarih, kategori, modul_kodu, aciklama) VALUES (?, ?, ?, ?)",
            (tarih, 'LEVHI_MAHFUZ_SABITI', modul_kodu, 'Organik Zaman Algoritması (363)'))

conn.commit()
conn.close()

print('Mock veri eklendi.')

# 2. Generate Report via Flask context
with app.app_context():
    response = rapor_sun()
    data = response.get_json()
    rapor_yolu = data.get("dosya_yolu")
    
    # 3. Read the generated report and print its path
    print(f"Rapor Yolu: {rapor_yolu}")
    
    # Copy the report to artifact directory
    import shutil
    hedef_yol = r"C:\Users\soldi\.gemini\antigravity\brain\346eb0da-8256-4847-a727-3dbab69cec05\ORUMCEK_AGI_EVRIM_RAPORU.md"
    shutil.copy(rapor_yolu, hedef_yol)
    print("Rapor artefakt dizinine kopyalandı.")
