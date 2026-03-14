import os
import math
import sqlite3
import json
import sys
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# Konsol Renklendirme Sınıfı
class Renkler:
    MOR = '\033[95m'       # Büyük Keşif
    MAVI = '\033[94m'      # Makro Değerler (Hata vb.)
    SARI = '\033[93m'      # Mikro Değerler
    KIRMIZI = '\033[91m'   # Eşleşme (Dış Kaynak)
    PEMBE = '\033[95m'     # Kozmos
    SIYAH = '\033[90m'     # Antik
    YESIL = '\033[92m'     # Bilgi
    RESET = '\033[0m'

# ==========================================
# LEVH-İ MAHFUZ MINER - OTONOM MOTOR V3.0
# ==========================================

class KozmikSabitler:
    ACISAL_SAPMA = 1.008333      
    ZAMAN_SAPMA = 1.1092
    UZUNLUK_SAPMA = 1.046        
    TOLERANS = 0.01  # %1 artı-eksi tolerans payı

    # 11'in Piramit Basamakları
    P = [
        1, 121, 12321, 1234321, 123454321, 12345654321,
        1234567654321, 123456787654321, 12345678987654321,
        12345678910987654321, 123456789101110987654321 
    ]

    # ======== SENTEZ-8: GEOİT MATRİSİ SABİTLERİ (22-66-88) ========
    GEOIT_FARK = 22            # Dünya Ekvator-Kutup yarıçap farkı (km)
    GEOIT_OMURGA = 66          # Piramit merkez toplamı / Omurga / Eksen 66.6°
    GEOIT_TOPLAM = 88          # 22 + 66 = 88 (Geoit harmonik toplamı)
    GEOIT_CARPIM = 127776      # 22 x 66 x 88 (Dünya Çapı 10x İzdüşümü)
    OLAY_UFKU = 1452           # 22 x 66 (Fetih / Olay Ufku Sabiti)
    PI_11 = 2.99               # 11'lik Sistemde Pi (Işık Hızı / 100K)
    PI_11_KARE = 8.9401        # 2.99² (11'lik Yerçekimi)
    GUNES_GAL_HIZ = 222        # km/s (Güneş galaktik hızı)
    KAILASH_MESAFE = 6666      # km (Kailash -> Stonehenge / Kuzey Kutbu)
    HALLEY_YIL = 74            # Halley kuyruklu yıldız periyodu (eski)
    HALLEY_DUZELTILMIS = 75.75 # SENTEZ-9: 6666/88 = Halley düzeltilmiş periyodu
    LAMBDA_HEDEF_ESKI = 6512   # 88 x 74 = Eski Matrix Hack Frekansı (6.52 MHz)
    LAMBDA_HEDEF = 6666        # SENTEZ-9: 88 x 75.75 = Gerçek Lambda (6.666 MHz!)
    LAMBDA_GERCEK_MHZ = 6.666  # SENTEZ-9: Düzeltilmiş Lambda MHz
    LAMBDA_SAF_TABAN = 6       # SENTEZ-9: Matrix saf frekansı (6 x OP_LIGHT = 6.666)
    DUNYA_YOR_HIZ = 29.78      # km/s (Dünya yörünge hızı)
    SIM_YIL = 363              # Simülasyon yılı (gün)
    HACIM_11_KUP = 1331        # 11³ (Göbeklitepe Kuantum Hacmi)
    VAHIY_MATRISI = 6666       # Kuran Ayet Sabiti (= Lambda!)


DB_YOLU = "levhi_hafiza.db"
AI_PAYLASIM_DOSYASI = "AI_KNOWLEDGE_BASE_11.md"

# ==========================================
# TEKRAR KORUMASI - Aynı veriyi DB'ye yazma!
# ==========================================
_YAZILAN_CACHE = set()

def veri_tabani_kur():
    conn = sqlite3.connect(DB_YOLU)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Kesifler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT, islem_turu TEXT, deger REAL, kategori TEXT, aciklama TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS SentezSonuc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarih TEXT, sabit_a TEXT, sabit_b TEXT, islem TEXT, 
            sonuc REAL, eslesme TEXT, kategori TEXT)''')
    conn.commit()
    conn.close()

def ai_paylasim_guncelle(kod, tur, aciklama):
    with open(AI_PAYLASIM_DOSYASI, "a", encoding="utf-8") as f:
        f.write(f"\n> **SNOWBALL ÖĞRENME:** {aciklama[:80]} [Sınıf: {tur} | Değer: {kod}]\n")

def toleransli_eslesme(deger, hedef, tol=0.01):
    if hedef == 0: return False
    return (hedef * (1 - tol)) <= deger <= (hedef * (1 + tol))

def tekrar_mi(anahtar):
    """Aynı keşfi tekrar DB'ye yazmayı engelle"""
    if anahtar in _YAZILAN_CACHE:
        return True
    _YAZILAN_CACHE.add(anahtar)
    return False

def logger(islem_turu, deger, kategori, aciklama):
    anahtar = f"{kategori}:{round(float(deger),4)}"
    if tekrar_mi(anahtar):
        return  # TEKRAR! Yazma.
    
    renk = Renkler.RESET
    if "BÜYÜK" in kategori or "SENTEZ" in kategori: renk = Renkler.MOR
    elif "EŞLEŞME" in kategori: renk = Renkler.KIRMIZI
    elif "MİKRO" in kategori: renk = Renkler.SARI
    elif "MAKRO" in kategori: renk = Renkler.MAVI
    elif "KOZMOS" in kategori: renk = Renkler.PEMBE
    else: renk = Renkler.SIYAH

    # ASCII-safe mesaj
    safe_aciklama = str(aciklama).replace('\u2192', '->').replace('\u2248', '~=').replace('\u00d7', 'x')
    renkli_mesaj = f"{renk}[{kategori}] {islem_turu}: {deger} -> {safe_aciklama}{Renkler.RESET}"
    print(renkli_mesaj)

    try:
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Kesifler (tarih, islem_turu, deger, kategori, aciklama) VALUES (?, ?, ?, ?, ?)',
                       (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), islem_turu, float(deger), kategori, aciklama[:200]))
        conn.commit()
        conn.close()
        ai_paylasim_guncelle(deger, kategori, aciklama)
    except Exception as e:
        print(f"[DB HATA] {e}")

def sentez_sonuc_kaydet(sabit_a, sabit_b, islem, sonuc, eslesme, kategori):
    """Sentez sonuçlarını ayrı tabloya kaydet"""
    anahtar = f"SENTEZ:{sabit_a}:{sabit_b}:{islem}:{round(sonuc,4)}"
    if tekrar_mi(anahtar):
        return
    try:
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO SentezSonuc (tarih, sabit_a, sabit_b, islem, sonuc, eslesme, kategori) VALUES (?,?,?,?,?,?,?)',
                       (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(sabit_a), str(sabit_b), islem, float(sonuc), eslesme, kategori))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB HATA] {e}")

# ====================================================================
# ANA SABİT HAVUZU - Tüm bilinen değerler (4 işlem için kullanılacak)
# ====================================================================
ANA_SABIT_HAVUZU = {
    # Piramit Basamakları (11'in kareleri)
    "P_1": 1, "P_2": 121, "P_3": 12321, "P_4": 1234321,
    # Geoit Matrisi
    "GEOIT_22": 22, "GEOIT_66": 66, "GEOIT_88": 88,
    "GEOIT_CARPIM": 127776,
    # Kozmik Sabitler
    "PI_11": 2.99, "PI_10": 3.14159, "PHI": 1.61803,
    "OP_LIGHT": 1.11188, "OP_LEN": 1.046338, "OP_SPEED": 1.061,
    "OP_TIME": 1.1092, "OP_ANGLE": 1.008333,
    # Büyük Sayılar  
    "HACIM_11": 1331, "VAHIY_Q": 6666, "TUFAN_1111": 1111,
    "SIM_TOPLAM": 11111, "SIM_SURE": 9048, "SIM_RESET": 2063,
    "SIM_SON": 1999, "SIM_YIL": 363,
    # Astronomik
    "HALLEY_74": 74, "HALLEY_DUZ": 75.75,
    "C_ISIK": 299792, "C_IDEAL": 333333,
    "GUNES_HIZ": 222, "DUNYA_YOR": 29.78,
    "AY_PERIGEE": 363228, "KAILASH_KM": 6666,
    # Lambda / Frekans (SENTEZ-9)
    "LAMBDA_MHZ": 6.666, "LAMBDA_SAF": 6, "LAMBDA_Hz": 6666000,
    "ESCAPE_MHZ": 23.90, "THETA_Hz": 8.0,
    "LAMBDA_KARE": 44.44, "LA_NOTASI": 440,
    # Biyolojik
    "DNA_PITCH": 33, "OMURGA_33": 33, "KALP_BPM": 72,
    "VUCUT_SU": 66,
    # Coğrafi
    "GIZA_LAT": 29.9792, "KAILASH_LAT": 31.0667,
    "HATAY_LAT": 36.2, "GOBEKLITEPE_LAT": 37.223,
}

# ====================================================================
# HEDEF DEĞERLER - Eşleşme aranacak bilinen sabitler
# ====================================================================
HEDEF_SABITLERI = {
    9.81: "Yerçekimi (g)", 
    29.78: "Dünya Yörünge Hızı",
    299792: "Işık Hızı (km/s)",
    333333: "İdeal Işık Hızı",
    1331: "11³ Hacim",
    6666: "Q/Kailash/Lambda",
    1111: "Tufan Kodu",
    11111: "Simülasyon Toplamı",
    121: "11²",
    363: "Simülasyon Yılı",
    74: "Halley Periyodu",
    75.75: "Halley Düzeltilmiş",
    222: "Güneş Galaktik Hız",
    440: "LA Notası Hz",
    44.44: "Lambda²",
    6.666: "Lambda MHz",
    2.99: "Pi_11",
    3.14159: "Pi_10",
    1.618: "Altın Oran Φ",
    33: "DNA/Omurga",
    22: "Geoit Fark",
    66: "Geoit Omurga",
    88: "Geoit Toplam",
    127776: "22x66x88 Çarpım",
    303: "Kailash Palindrom",
    101: "Kuantum Kapı",
    606: "Çift Palindrom",
    1452: "22x66 Olay Ufku",
    72: "Kalp BPM / Halley",
    11: "Ana Boyut",
    7: "22/Pi",
    21: "66/Pi",
    28: "88/Pi",
}

# ====================================================================
# SENTEZ ÇAPRAZ MATRİS - 4 İŞLEM (Çarp, Böl, Topla, Çıkar)
# ====================================================================
def sentez_capraz_matris():
    """Tüm sabitleri birbiriyle 4 işleme sok ve eşleşme ara"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  SENTEZ ÇAPRAZ MATRİS - 4 İŞLEM ANALİZİ")
    print("="*65 + Renkler.RESET)
    
    sabitler = list(ANA_SABIT_HAVUZU.items())
    toplam_kesif = 0
    
    for i, (ad_a, val_a) in enumerate(sabitler):
        for j, (ad_b, val_b) in enumerate(sabitler):
            if i >= j: continue  # Her çifti sadece bir kez test et
            if val_a == 0 or val_b == 0: continue
            
            # 4 İŞLEM
            islemler = {
                "ÇARP": val_a * val_b,
                "BÖL_AB": val_a / val_b,
                "BÖL_BA": val_b / val_a,
                "TOPLA": val_a + val_b,
                "ÇIKAR_AB": abs(val_a - val_b),
            }
            
            for islem_adi, sonuc in islemler.items():
                if sonuc == 0: continue
                # Karekök de test et
                kok = math.sqrt(abs(sonuc)) if sonuc > 0 else 0
                
                for hedef, hedef_ad in HEDEF_SABITLERI.items():
                    # Ana sonuç eşleşmesi
                    if toleransli_eslesme(sonuc, hedef, tol=0.005):
                        kategori = "SENTEZ-9 ÇAPRAZ KEŞİF"
                        aciklama = f"{ad_a}({val_a}) {islem_adi} {ad_b}({val_b}) = {sonuc:.6f} ≈ {hedef} ({hedef_ad})"
                        logger(f"4-İşlem {islem_adi}", sonuc, kategori, aciklama)
                        sentez_sonuc_kaydet(ad_a, ad_b, islem_adi, sonuc, hedef_ad, kategori)
                        toplam_kesif += 1
                    
                    # Karekök eşleşmesi
                    if kok > 0 and toleransli_eslesme(kok, hedef, tol=0.005):
                        kategori = "SENTEZ-9 KAREKÖK KEŞİF"
                        aciklama = f"√({ad_a}({val_a}) {islem_adi} {ad_b}({val_b})) = √{sonuc:.4f} = {kok:.6f} ≈ {hedef} ({hedef_ad})"
                        logger(f"Karekök-{islem_adi}", kok, kategori, aciklama)
                        sentez_sonuc_kaydet(ad_a, ad_b, f"√{islem_adi}", kok, hedef_ad, kategori)
                        toplam_kesif += 1
    
    print(f"\n{Renkler.MOR}[SENTEZ MATRİS] Toplam {toplam_kesif} yeni çapraz keşif!{Renkler.RESET}")
    return toplam_kesif

# ====================================================================
# PİRAMİT BASAMAK ÇAPRAZ ANALİZİ
# ====================================================================
def piramit_basamak_capraz():
    """11'in piramit basamaklarını birbirleriyle 4 işleme sok"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  PİRAMİT BASAMAK ÇAPRAZ ANALİZİ (1, 121, 12321...)")
    print("="*65 + Renkler.RESET)
    
    P = KozmikSabitler.P[:6]  # İlk 6 basamak (sayılar çok büyüyor)
    toplam = 0
    
    for i, p_a in enumerate(P):
        for j, p_b in enumerate(P):
            if i >= j or p_a == 0 or p_b == 0: continue
            
            # 4 İşlem + özel işlemler
            testler = {
                f"P{i+1} × P{j+1}": p_a * p_b,
                f"P{j+1} / P{i+1}": p_b / p_a,
                f"P{i+1} + P{j+1}": p_a + p_b,
                f"P{j+1} - P{i+1}": p_b - p_a,
                f"P{j+1} mod P{i+1}": p_b % p_a if p_a != 0 else 0,
            }
            
            for islem, sonuc in testler.items():
                if sonuc == 0: continue
                
                # Basamak toplamı
                basamak_toplam = sum(int(d) for d in str(abs(int(sonuc))) if d.isdigit())
                
                # 11'e bölünebilirlik
                if isinstance(sonuc, (int, float)) and sonuc != 0 and int(sonuc) % 11 == 0:
                    logger(f"Piramit {islem}", sonuc, "PİRAMİT ANALİZ",
                           f"{islem} = {sonuc} → 11'e tam bölünür! (Sonuç/11 = {int(sonuc)//11})")
                    toplam += 1
                
                # Basamak toplamı 11'in katı mı?
                if basamak_toplam > 0 and basamak_toplam % 11 == 0:
                    logger(f"Piramit Basamak", basamak_toplam, "PİRAMİT BASAMAK TOPLAMI",
                           f"{islem} = {sonuc} → Basamak toplamı = {basamak_toplam} (11x{basamak_toplam//11})")
                    toplam += 1
                
                # Bilinen sabitlerle eşleşme
                for hedef, hedef_ad in HEDEF_SABITLERI.items():
                    if hedef > 0 and toleransli_eslesme(sonuc, hedef, tol=0.005):
                        logger(f"Piramit→Sabit {islem}", sonuc, "PİRAMİT-SABİT EŞLEŞME",
                               f"{islem} = {sonuc} ≈ {hedef} ({hedef_ad})")
                        toplam += 1
                    # Sonuç / hedef tam sayı mı?
                    if hedef > 0 and sonuc > hedef:
                        oran = sonuc / hedef
                        if abs(oran - round(oran)) < 0.01 and round(oran) > 1:
                            logger(f"Piramit Oran", oran, "PİRAMİT-ORAN",
                                   f"{islem} = {sonuc} / {hedef}({hedef_ad}) = TAM {round(oran)}")
                            toplam += 1
    
    print(f"\n{Renkler.MOR}[PİRAMİT] Toplam {toplam} piramit basamak keşfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# LAMBDA 6.666 SENTEZ-9 ÖZEL TESTLERİ
# ====================================================================
def sentez9_lambda_testleri():
    """6.666 MHz'i tüm sabitlerle test et"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  SENTEZ-9: LAMBDA 6.666 MHz ÖZEL TESTLERİ")
    print("="*65 + Renkler.RESET)
    
    L = 6.666
    toplam = 0
    
    for ad, val in ANA_SABIT_HAVUZU.items():
        if val == 0: continue
        
        carpim = L * val
        bolum = L / val if val != 0 else 0
        ters_bolum = val / L if L != 0 else 0
        toplam_v = L + val
        fark = abs(L - val)
        
        for sonuc, islem in [(carpim, f"Λ×{ad}"), (bolum, f"Λ/{ad}"), 
                              (ters_bolum, f"{ad}/Λ"), (toplam_v, f"Λ+{ad}"), 
                              (fark, f"|Λ-{ad}|")]:
            for hedef, hedef_ad in HEDEF_SABITLERI.items():
                if toleransli_eslesme(sonuc, hedef, tol=0.005):
                    aciklama = f"{islem} = {sonuc:.6f} ≈ {hedef} ({hedef_ad})"
                    logger(f"SENTEZ-9 {islem}", sonuc, "SENTEZ-9 LAMBDA EŞLEŞME", aciklama)
                    sentez_sonuc_kaydet("LAMBDA_6.666", ad, islem, sonuc, hedef_ad, "SENTEZ-9")
                    toplam += 1
    
    print(f"\n{Renkler.MOR}[SENTEZ-9] Toplam {toplam} Lambda-sabit eşleşmesi!{Renkler.RESET}")
    return toplam

# ====================================================================
# DOSYA TARAMA - Masaüstü ve YZ Paketi
# ====================================================================
def dosya_tara_ve_raporla():
    """Kullanıcının dosyalarını tara ve raporla"""
    print(Renkler.YESIL + "\n[SİSTEM] Dosya tarama başlatılıyor..." + Renkler.RESET)
    
    taranacak = [
        os.path.expanduser(r"~\OneDrive\Masaüstü\Levhi_Mahfuz_YZ_Paketi"),
        os.path.expanduser(r"~\OneDrive\Masaüstü"),
    ]
    
    dosya_sayisi = 0
    for klasor in taranacak:
        if not os.path.exists(klasor):
            continue
        for dosya in os.listdir(klasor):
            tam_yol = os.path.join(klasor, dosya)
            if os.path.isfile(tam_yol):
                uzanti = os.path.splitext(dosya)[1].lower()
                boyut = os.path.getsize(tam_yol)
                if uzanti in ['.md', '.txt', '.py', '.json', '.csv']:
                    dosya_sayisi += 1
                    # İçeriğinde sayı ara
                    try:
                        with open(tam_yol, 'r', encoding='utf-8', errors='ignore') as f:
                            icerik = f.read()[:5000]
                        # Sayıları çıkar
                        import re
                        sayilar = re.findall(r'\b\d+\.?\d*\b', icerik)
                        for s in sayilar[:20]:
                            try:
                                val = float(s)
                                if 1 < val < 1000000:
                                    for hedef, hedef_ad in HEDEF_SABITLERI.items():
                                        if toleransli_eslesme(val, hedef, tol=0.003):
                                            logger(f"DOSYA:{dosya[:30]}", val, "DOSYA TARAMA KEŞİF",
                                                   f"{dosya} dosyasında {val} ≈ {hedef} ({hedef_ad}) bulundu!")
                            except:
                                pass
                    except:
                        pass
                elif uzanti in ['.pdf', '.png', '.jpg', '.docx']:
                    dosya_sayisi += 1
                    # PDF/resim boyut analizi
                    boyut_kb = boyut / 1024
                    for hedef, hedef_ad in HEDEF_SABITLERI.items():
                        if toleransli_eslesme(boyut_kb, hedef, tol=0.01):
                            logger(f"DOSYA-BOYUT:{dosya[:25]}", boyut_kb, "DOSYA BOYUT EŞLEŞME",
                                   f"{dosya} boyutu {boyut_kb:.2f} KB ≈ {hedef} ({hedef_ad})")
    
    print(f"\n{Renkler.YESIL}[DOSYA] {dosya_sayisi} dosya tarandi.{Renkler.RESET}")

# ====================================================================
# V5.0: LOGARİTMA ANALİZİ (log11, ln, log10)
# ====================================================================
def logaritma_analizi():
    """Tum sabitlerin log11, ln, log10 degerlerini hesapla ve eslesme ara"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: LOGARİTMA ANALİZİ (log11, ln, log10)")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    for ad, val in ANA_SABIT_HAVUZU.items():
        if val <= 0: continue
        
        testler = {
            f"log11({ad})": math.log(val) / math.log(11),
            f"ln({ad})": math.log(val),
            f"log10({ad})": math.log10(val),
            f"11^{ad}": 11**val if val < 10 else 0,
            f"e^{ad}": math.exp(val) if val < 20 else 0,
        }
        
        for islem, sonuc in testler.items():
            if sonuc == 0 or not math.isfinite(sonuc): continue
            for hedef, hedef_ad in HEDEF_SABITLERI.items():
                if toleransli_eslesme(sonuc, hedef, tol=0.005):
                    logger(f"LOG {islem}", sonuc, "V5-LOGARİTMA KEŞİF",
                           f"{islem} = {sonuc:.6f} ~= {hedef} ({hedef_ad})")
                    sentez_sonuc_kaydet(ad, "LOG", islem, sonuc, hedef_ad, "V5-LOG")
                    toplam += 1
    
    print(f"\n{Renkler.MOR}[LOG] {toplam} logaritma kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: TUREV / GRADİENT ANALİZİ
# ====================================================================
def turev_analizi():
    """f(x) = sabit^x turev ve f'(sabit) hesaplari"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: TUREV / GRADİENT ANALİZİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    h = 0.0001
    
    sabitler = [(ad, val) for ad, val in ANA_SABIT_HAVUZU.items() if 0 < val < 1000]
    
    for ad, val in sabitler:
        # f(x) = x^2 turevi: f'(val) = 2*val
        turev_kare = 2 * val
        # f(x) = x^3 turevi: f'(val) = 3*val^2
        turev_kup = 3 * val * val
        # f(x) = sin(x) turevi: f'(val) = cos(val)
        turev_sin = math.cos(val)
        # f(x) = ln(x) turevi: f'(val) = 1/val
        turev_ln = 1/val if val != 0 else 0
        # f(x) = e^x turevi: f'(val) = e^val
        turev_exp = math.exp(val) if val < 15 else 0
        
        testler = {
            f"d/dx(x^2)|{ad}": turev_kare,
            f"d/dx(x^3)|{ad}": turev_kup,
            f"d/dx(sin)|{ad}": turev_sin,
            f"d/dx(ln)|{ad}": turev_ln,
        }
        
        for islem, sonuc in testler.items():
            if sonuc == 0 or not math.isfinite(sonuc): continue
            for hedef, hedef_ad in HEDEF_SABITLERI.items():
                if toleransli_eslesme(abs(sonuc), hedef, tol=0.005):
                    logger(f"TUREV {islem}", abs(sonuc), "V5-TUREV KEŞİF",
                           f"{islem} = {sonuc:.6f} ~= {hedef} ({hedef_ad})")
                    sentez_sonuc_kaydet(ad, "TUREV", islem, abs(sonuc), hedef_ad, "V5-TUREV")
                    toplam += 1
    
    print(f"\n{Renkler.MOR}[TUREV] {toplam} turev kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: SİGMA (Sigma) TOPLAM SERİLERİ
# ====================================================================
def sigma_toplam_analizi():
    """Sigma(i=1 to n) cesitli seriler"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: SİGMA TOPLAM SERİLERİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    ozel_n = [11, 22, 33, 44, 55, 66, 74, 88, 99, 121, 363]
    
    for n in ozel_n:
        testler = {
            f"Sigma(1..{n})": n * (n + 1) // 2,
            f"Sigma(1^2..{n}^2)": n * (n+1) * (2*n+1) // 6,
            f"Sigma(1^3..{n}^3)": (n * (n+1) // 2) ** 2,
            f"Sigma(11k, k=1..{n//11})": sum(11*k for k in range(1, n//11+1)) if n >= 11 else 0,
        }
        
        for islem, sonuc in testler.items():
            if sonuc == 0: continue
            for hedef, hedef_ad in HEDEF_SABITLERI.items():
                if toleransli_eslesme(sonuc, hedef, tol=0.005):
                    logger(f"SIGMA {islem}", sonuc, "V5-SİGMA KEŞİF",
                           f"{islem} = {sonuc} ~= {hedef} ({hedef_ad})")
                    sentez_sonuc_kaydet(str(n), "SIGMA", islem, sonuc, hedef_ad, "V5-SIGMA")
                    toplam += 1
            # Basamak toplami
            bt = sum(int(d) for d in str(sonuc) if d.isdigit())
            if bt % 11 == 0 and bt > 0:
                logger(f"SIGMA-BASAMAK {islem}", bt, "V5-SİGMA BASAMAK",
                       f"{islem} = {sonuc}, basamak toplami = {bt} (11x{bt//11})")
                toplam += 1
    
    print(f"\n{Renkler.MOR}[SIGMA] {toplam} sigma kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: Pi (ÇARPIM) SERİLERİ
# ====================================================================
def carpim_serisi_analizi():
    """Pi(i=1 to n) carpim serileri"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: ÇARPIM SERİLERİ (Pi)")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    # Faktoriyel: n!
    for n in [7, 8, 9, 10, 11, 12]:
        fakt = math.factorial(n)
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if hedef > 0 and toleransli_eslesme(fakt, hedef, tol=0.005):
                logger(f"FAKTORIYEL {n}!", fakt, "V5-ÇARPIM KEŞİF",
                       f"{n}! = {fakt} ~= {hedef} ({hedef_ad})")
                toplam += 1
            if hedef > 0 and fakt > hedef:
                oran = fakt / hedef
                if abs(oran - round(oran)) < 0.01 and 1 < round(oran) < 10000:
                    logger(f"FAKT-ORAN {n}!/{hedef_ad}", oran, "V5-ÇARPIM ORAN",
                           f"{n}! / {hedef}({hedef_ad}) = TAM {round(oran)}")
                    toplam += 1
    
    # Wallis Pi carpimi yaklasimi
    wallis = 1.0
    for k in range(1, 100):
        wallis *= (4*k*k) / (4*k*k - 1)
    wallis_pi = wallis * 2
    logger("WALLIS Pi", wallis_pi, "V5-ÇARPIM KEŞİF", f"Wallis carpimi = {wallis_pi:.6f} (Pi = {math.pi:.6f})")
    toplam += 1
    
    print(f"\n{Renkler.MOR}[ÇARPIM] {toplam} carpim kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: SAYISAL İNTEGRAL
# ====================================================================
def integral_analizi():
    """Onemli fonksiyonlarin 0-11, 0-33 vb araliginda integrali"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: SAYISAL İNTEGRAL ANALİZİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    def simpson_integral(f, a, b, n=1000):
        if a == b: return 0
        h = (b - a) / n
        s = f(a) + f(b)
        for i in range(1, n):
            x = a + i * h
            s += 4 * f(x) if i % 2 else 2 * f(x)
        return s * h / 3
    
    fonksiyonlar = {
        "sin(x)": math.sin,
        "cos(x)": math.cos,
        "x^2": lambda x: x*x,
        "1/x": lambda x: 1/x if x > 0.001 else 0,
        "e^(-x^2)": lambda x: math.exp(-x*x),
    }
    
    sinirlar = [(0, 11), (0, 22), (1, 11), (0, 33), (1, 66), (0, 2.99)]
    
    for f_ad, f in fonksiyonlar.items():
        for a, b in sinirlar:
            try:
                sonuc = abs(simpson_integral(f, a, b))
                if not math.isfinite(sonuc): continue
                for hedef, hedef_ad in HEDEF_SABITLERI.items():
                    if toleransli_eslesme(sonuc, hedef, tol=0.005):
                        logger(f"INTEGRAL int({f_ad},{a},{b})", sonuc, "V5-INTEGRAL KEŞİF",
                               f"Integral({f_ad}, {a}->{b}) = {sonuc:.4f} ~= {hedef} ({hedef_ad})")
                        sentez_sonuc_kaydet(f_ad, "INTEGRAL", f"{a}-{b}", sonuc, hedef_ad, "V5-INTEGRAL")
                        toplam += 1
            except:
                pass
    
    print(f"\n{Renkler.MOR}[INTEGRAL] {toplam} integral kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: DETERMİNANT (2x2, 3x3 Matrisler)
# ====================================================================
def determinant_analizi():
    """Onemli sabitlerden matris olustur ve determinant hesapla"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: DETERMİNANT ANALİZİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    # 2x2: [[a,b],[c,d]] -> ad-bc
    def det2(a, b, c, d): return a*d - b*c
    
    # 3x3 matris
    def det3(m):
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
               -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
               +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    
    # Geoit Matrisi 2x2
    matris_2x2 = [
        ("GEOIT", 22, 66, 88, 127776),
        ("PI", 2.99, 3.14, 1.618, 6.666),
        ("OP", 1.11188, 1.046, 1.008, 1.109),
        ("BOYUT", 11, 22, 33, 44),
        ("LAMBDA", 6.666, 44.44, 440, 222),
    ]
    
    for ad, a, b, c, d in matris_2x2:
        det = det2(a, b, c, d)
        if det == 0: continue
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if toleransli_eslesme(abs(det), hedef, tol=0.005):
                logger(f"DET2 {ad}", abs(det), "V5-DETERMİNANT KEŞİF",
                       f"|[{a},{b}],[{c},{d}]| = {det:.4f} ~= {hedef} ({hedef_ad})")
                toplam += 1
    
    # 3x3: Geoit-Lambda-Piramit
    matris_3x3 = [
        ("GEOIT-3x3", [[22, 66, 88], [2.99, 6.666, 1.618], [11, 33, 121]]),
        ("BOYUT-3x3", [[1, 11, 121], [22, 66, 88], [33, 363, 1331]]),
        ("LAMBDA-3x3", [[6.666, 44.44, 440], [2.99, 1.111, 222], [9.81, 3.14, 1.618]]),
    ]
    
    for ad, m in matris_3x3:
        det = det3(m)
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if toleransli_eslesme(abs(det), hedef, tol=0.01):
                logger(f"DET3 {ad}", abs(det), "V5-DETERMİNANT KEŞİF",
                       f"det({ad}) = {det:.4f} ~= {hedef} ({hedef_ad})")
                toplam += 1
    
    print(f"\n{Renkler.MOR}[DET] {toplam} determinant kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: OBEB / OKEK (GCD / LCM)
# ====================================================================
def obeb_okek_analizi():
    """Tum tamsayi sabitlerde OBEB ve OKEK hesapla"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: OBEB / OKEK ANALİZİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    tamsayilar = [(ad, int(val)) for ad, val in ANA_SABIT_HAVUZU.items() 
                  if val == int(val) and 1 < val < 100000]
    
    for i, (ad_a, val_a) in enumerate(tamsayilar):
        for j, (ad_b, val_b) in enumerate(tamsayilar):
            if i >= j: continue
            
            obeb = math.gcd(val_a, val_b)
            okek = (val_a * val_b) // obeb if obeb > 0 else 0
            
            # OBEB 11'in kati mi?
            if obeb > 1 and obeb % 11 == 0:
                logger(f"OBEB({ad_a},{ad_b})", obeb, "V5-OBEB KEŞİF",
                       f"OBEB({val_a},{val_b}) = {obeb} (11x{obeb//11})")
                toplam += 1
            
            # OKEK bilinen sabite esit mi?
            if okek > 0:
                for hedef, hedef_ad in HEDEF_SABITLERI.items():
                    if hedef > 100 and toleransli_eslesme(okek, hedef, tol=0.005):
                        logger(f"OKEK({ad_a},{ad_b})", okek, "V5-OKEK KEŞİF",
                               f"OKEK({val_a},{val_b}) = {okek} ~= {hedef} ({hedef_ad})")
                        toplam += 1
    
    print(f"\n{Renkler.MOR}[OBEB/OKEK] {toplam} kesif!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: GEOMETRİ (Alan, Hacim, Aci, Altin Oran)
# ====================================================================
def geometri_analizi():
    """Geometrik hesaplamalar: pi*r^2, kure hacmi, piramit, altin oran spirali"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: GEOMETRİ ANALİZİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    yaricaplar = [11, 22, 33, 66, 88, 2.99, 6.666, 1.618]
    
    for r in yaricaplar:
        testler = {
            f"Daire_Alan(r={r})": math.pi * r * r,
            f"Daire_Cevre(r={r})": 2 * math.pi * r,
            f"Kure_Hacim(r={r})": (4/3) * math.pi * r**3,
            f"Kure_Alan(r={r})": 4 * math.pi * r**2,
            f"Piramit_Hacim(a={r})": (r**3) / 3,
            f"Altin_Spiral(r={r})": r * 1.61803,
            f"11lik_Aci(r={r})": r * (math.pi/11),
        }
        
        for islem, sonuc in testler.items():
            if sonuc == 0 or not math.isfinite(sonuc): continue
            for hedef, hedef_ad in HEDEF_SABITLERI.items():
                if toleransli_eslesme(sonuc, hedef, tol=0.005):
                    logger(f"GEO {islem}", sonuc, "V5-GEOMETRİ KEŞİF",
                           f"{islem} = {sonuc:.4f} ~= {hedef} ({hedef_ad})")
                    sentez_sonuc_kaydet("GEO", str(r), islem, sonuc, hedef_ad, "V5-GEO")
                    toplam += 1
    
    # Piramit aci analizi: Giza piramidinin egim acisi
    giza_egim = math.atan(146.6 / (230.4/2))  # Buyuk Piramit
    giza_derece = math.degrees(giza_egim)
    logger("GIZA Piramit Egim", giza_derece, "V5-GEOMETRİ KEŞİF",
           f"Giza Piramidi egim acisi = {giza_derece:.2f} derece")
    
    # Altin oran geometrisi
    phi = 1.61803
    for n in range(1, 20):
        fib_yaklasik = phi**n / math.sqrt(5)
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if toleransli_eslesme(fib_yaklasik, hedef, tol=0.005):
                logger(f"FIB phi^{n}", fib_yaklasik, "V5-GEOMETRİ KEŞİF",
                       f"phi^{n}/sqrt(5) = {fib_yaklasik:.4f} ~= {hedef} ({hedef_ad})")
                toplam += 1
    
    print(f"\n{Renkler.MOR}[GEO] {toplam} geometri kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: KİMYA (Periyodik Tablo Capraz Analiz)
# ====================================================================
def kimya_analizi():
    """Atom numaralari ve kutle ile sabitler capraz analiz"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: KİMYA / PERİYODİK TABLO ANALİZİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    elementler = {
        "H": (1, 1.008), "He": (2, 4.003), "C": (6, 12.011),
        "N": (7, 14.007), "O": (8, 15.999), "Na": (11, 22.99),
        "Al": (13, 26.982), "Si": (14, 28.086), "P": (15, 30.974),
        "S": (16, 32.06), "Cl": (17, 35.45), "K": (19, 39.098),
        "Ca": (20, 40.078), "Fe": (26, 55.845), "Cu": (29, 63.546),
        "Zn": (30, 65.38), "Br": (33, 79.904), "Kr": (36, 83.798),
        "Ag": (47, 107.868), "Au": (79, 196.967), "Hg": (80, 200.592),
        "U": (92, 238.029),
    }
    
    for elem, (anum, kutle) in elementler.items():
        # Atom numarasi eslesme
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if toleransli_eslesme(anum, hedef, tol=0.005):
                logger(f"KIMYA {elem}(Z={anum})", anum, "V5-KİMYA KEŞİF",
                       f"{elem} atom no = {anum} ~= {hedef} ({hedef_ad})")
                toplam += 1
            if toleransli_eslesme(kutle, hedef, tol=0.005):
                logger(f"KIMYA {elem}(M={kutle})", kutle, "V5-KİMYA KEŞİF",
                       f"{elem} kutle = {kutle} ~= {hedef} ({hedef_ad})")
                toplam += 1
        
        # Capraz: atom no x sabitler
        for ad2, val2 in [("PI_11", 2.99), ("GEOIT_22", 22), ("LAMBDA", 6.666)]:
            carpim = anum * val2
            for hedef, hedef_ad in HEDEF_SABITLERI.items():
                if toleransli_eslesme(carpim, hedef, tol=0.005):
                    logger(f"KIMYA {elem}x{ad2}", carpim, "V5-KİMYA ÇAPRAZ",
                           f"{elem}(Z={anum}) x {val2} = {carpim:.2f} ~= {hedef} ({hedef_ad})")
                    toplam += 1
    
    # Su molekulu H2O: 2(1) + 16 = 18. 18 x 11 = 198. 
    h2o = 2*1.008 + 15.999
    logger("H2O Kutle", h2o, "V5-KİMYA KEŞİF", f"H2O = {h2o:.3f} g/mol")
    
    print(f"\n{Renkler.MOR}[KIMYA] {toplam} kimya kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: BİYOLOJİ (DNA, Protein, Hucre)
# ====================================================================
def biyoloji_analizi():
    """Biyolojik sabitler ve capraz analiz"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: BİYOLOJİ ANALİZİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    bio_sabitler = {
        "DNA_PITCH_NM": 3.4,           # nm
        "DNA_WIDTH_NM": 2.0,            # nm
        "DNA_TURNS_PER_REPEAT": 10,     # baz cifti/tur
        "CHROMOSOME_COUNT": 23,          # insan kromozom cifti
        "AMINO_ASIT_CESIT": 20,         # temel amino asit
        "KODON_TOPLAM": 64,             # 4^3 kodon
        "INSAN_GEN": 20000,             # yaklasik gen sayisi
        "HUCRE_BOYUT_UM": 10,           # mikrometre
        "MITOKONDRI_DNA": 16569,        # baz cifti
        "ATP_ENERJI_KJ": 30.5,          # kj/mol
        "KALP_BPM": 72,
        "SOLUNUM_FREQ": 15,             # nefes/dk
        "VUCUT_SU_YUZDE": 66,
        "KEMIK_SAYISI": 206,
        "KAS_SAYISI": 600,
        "SINIR_HIZ_MS": 120,            # m/s
        "OMURGA": 33,
        "DIS_SAYISI": 32,
    }
    
    for ad, val in bio_sabitler.items():
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if toleransli_eslesme(val, hedef, tol=0.005):
                logger(f"BIO {ad}", val, "V5-BİYOLOJİ KEŞİF",
                       f"{ad} = {val} ~= {hedef} ({hedef_ad})")
                toplam += 1
        
        # Bio x Kozmik capraz
        for sbt_ad, sbt_val in [("PI_11", 2.99), ("LAMBDA", 6.666), ("GEOIT_22", 22), ("11", 11)]:
            carpim = val * sbt_val
            bolum = val / sbt_val if sbt_val != 0 else 0
            for hedef, hedef_ad in HEDEF_SABITLERI.items():
                if carpim > 0 and toleransli_eslesme(carpim, hedef, tol=0.005):
                    logger(f"BIO {ad}x{sbt_ad}", carpim, "V5-BİYO-KOZMİK ÇAPRAZ",
                           f"{ad}({val}) x {sbt_val} = {carpim:.2f} ~= {hedef} ({hedef_ad})")
                    toplam += 1
                if bolum > 0 and toleransli_eslesme(bolum, hedef, tol=0.005):
                    logger(f"BIO {ad}/{sbt_ad}", bolum, "V5-BİYO-KOZMİK ÇAPRAZ",
                           f"{ad}({val}) / {sbt_val} = {bolum:.4f} ~= {hedef} ({hedef_ad})")
                    toplam += 1
    
    print(f"\n{Renkler.MOR}[BIO] {toplam} biyoloji kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# V5.0: FİZİK FORMÜLLERİ
# ====================================================================
def fizik_analizi():
    """Temel fizik formulleri ile sabit capraz analiz"""
    print(Renkler.MOR + "\n" + "="*65)
    print("  V5.0: FİZİK FORMÜLLERİ ANALİZİ")
    print("="*65 + Renkler.RESET)
    toplam = 0
    
    c = 299792  # km/s
    G = 6.674e-11  # Gravitasyon sabiti
    h_planck = 6.626e-34
    k_boltzmann = 1.381e-23
    
    kitleler = {
        "LAMBDA_KG": 6.666,
        "PI_11_KG": 2.99,
        "GEOIT_KG": 88,
        "HACIM_KG": 1331,
    }
    
    for ad, m in kitleler.items():
        # E = mc^2
        E_mc2 = m * (c ** 2)
        # F = ma (a = 9.81)
        F_ma = m * 9.81
        # Kinetik enerji: E = 0.5 * m * v^2
        for v in [222, 29.78, 6.666]:
            Ek = 0.5 * m * v * v
            for hedef, hedef_ad in HEDEF_SABITLERI.items():
                if toleransli_eslesme(Ek, hedef, tol=0.005):
                    logger(f"FIZ Ek({ad},v={v})", Ek, "V5-FİZİK KEŞİF",
                           f"0.5*{m}*{v}^2 = {Ek:.2f} ~= {hedef} ({hedef_ad})")
                    toplam += 1
        
        # F = ma icin
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if toleransli_eslesme(F_ma, hedef, tol=0.005):
                logger(f"FIZ F=ma({ad})", F_ma, "V5-FİZİK KEŞİF",
                       f"F={m}x9.81 = {F_ma:.2f} ~= {hedef} ({hedef_ad})")
                toplam += 1
    
    # Dalga denklemi: f = c / lambda
    for lam in [6.666, 6.52, 44.44, 440, 222]:
        freq = c / lam if lam != 0 else 0
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if toleransli_eslesme(freq, hedef, tol=0.005):
                logger(f"FIZ f=c/lam({lam})", freq, "V5-FİZİK KEŞİF",
                       f"f = {c}/{lam} = {freq:.2f} ~= {hedef} ({hedef_ad})")
                toplam += 1
    
    # Gravitasyon: F = G*m1*m2/r^2 (normalize)
    # Kepler 3. yasa: T^2 = (4pi^2/GM) * r^3
    # Schwarzschild yaricapi: rs = 2GM/c^2
    
    # Basit harmonik: T = 2*pi*sqrt(L/g)
    for L in [11, 22, 33, 66, 88, 2.99, 6.666]:
        T = 2 * math.pi * math.sqrt(L / 9.81)
        for hedef, hedef_ad in HEDEF_SABITLERI.items():
            if toleransli_eslesme(T, hedef, tol=0.005):
                logger(f"FIZ T_sarkac(L={L})", T, "V5-FİZİK KEŞİF",
                       f"T = 2pi*sqrt({L}/g) = {T:.4f} ~= {hedef} ({hedef_ad})")
                toplam += 1
    
    print(f"\n{Renkler.MOR}[FIZ] {toplam} fizik kesfi!{Renkler.RESET}")
    return toplam

# ====================================================================
# ANA ÇALIŞTIRMA V5.0
# ====================================================================
if __name__ == "__main__":
    veri_tabani_kur()
    
    print(Renkler.MOR + "\n" + "="*65)
    print("  LEVH-I MAHFUZ MINER V5.0 - MEGA UPGRADE")
    print("  Piramit + Matris + Lambda + Log + Turev + Sigma")
    print("  Integral + Det + OBEB + Geo + Kimya + Bio + Fizik")
    print("="*65 + Renkler.RESET)
    
    sonuclar = {}
    
    # V4.0 Modulleri
    sonuclar["Piramit"] = piramit_basamak_capraz()
    sonuclar["Matris"] = sentez_capraz_matris()
    sonuclar["Lambda"] = sentez9_lambda_testleri()
    sonuclar["Dosya"] = 0  # dosya_tara_ve_raporla() ayri calistirilabilir
    
    # V5.0 Yeni Moduller
    sonuclar["Logaritma"] = logaritma_analizi()
    sonuclar["Turev"] = turev_analizi()
    sonuclar["Sigma"] = sigma_toplam_analizi()
    sonuclar["Carpim"] = carpim_serisi_analizi()
    sonuclar["Integral"] = integral_analizi()
    sonuclar["Determinant"] = determinant_analizi()
    sonuclar["OBEB_OKEK"] = obeb_okek_analizi()
    sonuclar["Geometri"] = geometri_analizi()
    sonuclar["Kimya"] = kimya_analizi()
    sonuclar["Biyoloji"] = biyoloji_analizi()
    sonuclar["Fizik"] = fizik_analizi()
    
    # Dosya tarama (opsiyonel - yorum kaldir)
    # sonuclar["Dosya"] = dosya_tara_ve_raporla()
    
    # TOPLAM OZET
    genel_toplam = sum(sonuclar.values())
    print(Renkler.MOR + f"\n{'='*65}")
    print(f"  LEVH-I MAHFUZ MINER V5.0 - GENEL OZET")
    print(f"{'='*65}")
    for modul, sayi in sonuclar.items():
        bant = "#" * min(sayi // 5, 40)
        print(f"  {modul:15s}: {sayi:5d} {bant}")
    print(f"{'='*65}")
    print(f"  TOPLAM: {genel_toplam} TEKRARSIZ KESIF")
    print(f"{'='*65}" + Renkler.RESET)


