import sqlite3
import os
from datetime import datetime

DB_YOLU = r"C:\Users\soldi\IdeaProjects\simülation-11\levhi_hafiza.db"
BASE_DIR = r"C:\Users\soldi\IdeaProjects\simülation-11"
GITHUB_DIR = os.path.join(BASE_DIR, "SM-LASYON_11-")

uzantilar = [".pdf", ".md", ".py", ".jpg", ".png", ".txt", ".docx", ".html"]

def ekle():
    conn = sqlite3.connect(DB_YOLU)
    cursor = conn.cursor()
    
    # Get existing files
    cursor.execute("SELECT yol FROM Kaynaklar")
    mevcut_yollar = {row[0] for row in cursor.fetchall()}
    
    tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    eklenenler = 0
    
    # Tarama listesi
    dizinler = [BASE_DIR, GITHUB_DIR]
    
    for ana_dizin in dizinler:
        if not os.path.exists(ana_dizin):
            print(f"Uyarı: {ana_dizin} bulunamadı.")
            continue
            
        print(f"Taranıyor: {ana_dizin}")
        for root, dirs, files in os.walk(ana_dizin):
            # Skip hidden or specific dirs
            if ".git" in root or "__pycache__" in root or ".gemini" in root or ".venv" in root:
                continue
                
            for f in files:
                if any(f.lower().endswith(uz) for uz in uzantilar):
                    tam_yol = os.path.join(root, f)
                    if tam_yol not in mevcut_yollar:
                        cursor.execute("INSERT INTO Kaynaklar (tarih, tur, yol) VALUES (?, ?, ?)", (tarih, "DOSYA", tam_yol))
                        mevcut_yollar.add(tam_yol)
                        eklenenler += 1
                        
    conn.commit()
    conn.close()
    print(f"TOPLAM EKLENEN YENİ DOSYA: {eklenenler}")

if __name__ == '__main__':
    ekle()
