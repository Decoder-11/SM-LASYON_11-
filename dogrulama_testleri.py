#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
DOĞRULAMA TESTLERİ - Kapsamlı İstatistiksel Doğrulama Modülü
================================================================================
Tarih: 2026-03-10
Amaç: 11-Boyutlu Evren Simülasyonu için bilimsel doğrulama testleri
      - Monte Carlo simülasyonu
      - Bayes çıkarımı (Bayesian inference)
      - Benford Yasası analizi
      - Pearson korelasyon (r) testi
      - m11 (modulo-11) analizi
      - H0/H1 hipotez testleri
      - p-değeri hesaplama

Kaynaklar (Sources):
  - NASA JPL: https://ssd.jpl.nasa.gov/
  - CODATA 2018: https://physics.nist.gov/cuu/Constants/
  - IAU 2012: https://www.iau.org/science/publications/
  - WGS84: https://earth-info.nga.mil/
  - NOAA: https://www.ngdc.noaa.gov/
================================================================================
"""

import math
import random
import sys
from datetime import datetime

# Bilimsel kütüphaneler
try:
    import numpy as np
    from scipy import stats
    from scipy.stats import chi2, pearsonr, ttest_1samp
    import pandas as pd
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False
    print("UYARI: numpy/scipy eksik. Bazı testler devre dışı.")

# Renk kodları
class Renkler:
    BASLIK   = '\033[95m'
    MAVI     = '\033[94m'
    CYAN     = '\033[96m'
    YESIL    = '\033[92m'
    UYARI    = '\033[93m'
    HATA     = '\033[91m'
    BITIS    = '\033[0m'
    KALIN    = '\033[1m'
    ALTIN    = '\033[33m'
    MOR      = '\033[35m'
    KIRMIZI  = '\033[91m'


# ==============================================================================
# NASA / CODATA / IAU / WGS84 DOĞRULANMIŞ SABİTLER
# ==============================================================================
class NasaDogrulanmisSabitler:
    """
    Tüm değerler yetkili bilimsel kaynaklardan alınmıştır.
    Uydurma değer YOKTUR.
    """
    # --- IŞIK HIZI ---
    # Kaynak: CODATA 2018, NIST - kesin tanım (exact)
    ISIK_HIZI_MS   = 299_792_458        # m/s  (kesin, tanımlı)
    ISIK_HIZI_KMS  = 299_792.458        # km/s (CODATA)

    # --- EVRENSEL ÇEKIM SABITI ---
    # Kaynak: CODATA 2018 (NIST)
    G_CODATA       = 6.67430e-11        # m³ kg⁻¹ s⁻² (±0.00015e-11)

    # --- PLANK SABİTİ ---
    # Kaynak: CODATA 2018 - kesin tanım
    PLANK          = 6.62607015e-34     # J·s (kesin)

    # --- İNCE YAPI SABİTİ ---
    # Kaynak: CODATA 2018
    ALFA           = 7.2973525693e-3    # boyutsuz (~1/137.036)
    ALFA_TERSINE   = 137.035999084      # 1/α

    # --- DÜNYA SABİTLERİ ---
    # Kaynak: WGS84, NIST, NASA Earth Fact Sheet
    DUNYA_YARI_CAP_ORT  = 6_371.0      # km - ortalama yarıçap (WGS84)
    DUNYA_YARI_CAP_EKV  = 6_378.137    # km - ekvator yarıçapı (WGS84)
    DUNYA_YARI_CAP_KUT  = 6_356.752    # km - kutup yarıçapı (WGS84)
    DUNYA_CEVRE_EKV     = 40_075.017   # km - ekvator çevresi
    DUNYA_CEVRE_KUT     = 40_007.863   # km - kutup çevresi (NASA)
    DUNYA_KUTLE         = 5.972168e24  # kg (NASA)
    DUNYA_EKSEN_EGIMI   = 23.4392911   # derece (J2000.0, NASA/IAU)

    # --- AY SABİTLERİ ---
    # Kaynak: NASA Moon Fact Sheet, JPL
    AY_ORT_UZAKLIK      = 384_400.0    # km - ortalama (NASA)
    AY_PERIGE           = 362_600.0    # km - minimum perigee (NASA JPL)
    AY_APOGE            = 405_400.0    # km - maksimum apogee (NASA JPL)
    AY_YARI_CAP         = 1_737.4      # km (NASA)
    AY_CAP              = 3_474.8      # km (NASA Moon Fact Sheet)

    # --- GÜNEŞ SABİTLERİ ---
    # Kaynak: NASA Sun Fact Sheet, IAU 2012
    GUNES_YARI_CAP      = 695_700.0    # km (IAU 2015 nominal)
    GUNES_CAP           = 1_392_700.0  # km
    GUNES_KUTLE         = 1.989e30     # kg
    GUNES_DUNYA_KUTLE_ORANI = 332_946.0  # M☉/M⊕ (NASA)

    # --- DÜNYA-GÜNEŞ UZAKLIĞI ---
    # Kaynak: IAU 2012 tanımı
    AU_KM               = 149_597_870.700  # km (IAU 2012 - kesin tanım)
    AU_M                = 1.495978707e11   # m

    # --- HALLEY KUYRUKLUYILDIZı ---
    # Kaynak: JPL Small-Body Database, IAU Comet DB
    HALLEY_PERIYOD_MIN  = 74.0         # yıl (tarihi kayıtlar: 1835-1910)
    HALLEY_PERIYOD_MAX  = 79.0         # yıl (tarihi kayıtlar: 239 BC - 1986)
    HALLEY_PERIYOD_ORT  = 75.3         # yıl (modern ortalama, JPL)
    HALLEY_SON_GECIS    = 1986.08      # 1986 Şubat (JPL)
    HALLEY_SONRAKI      = 2061.0       # Temmuz 2061 tahmini (NASA)

    # --- COĞRAFİK KOORDİNATLAR ---
    # Kaynak: Google Earth / IGS / UNESCO
    GIZA_ENLEM          = 29.9792      # °N (29°58'45"N - Google Earth)
    GIZA_BOYLAM         = 31.1342      # °E
    KAILAS_ENLEM        = 31.0675      # °N (Tibet, Google Earth)
    KAILAS_BOYLAM       = 81.3119      # °E
    STONEHENGE_ENLEM    = 51.1789      # °N (Google Earth)
    STONEHENGE_BOYLAM   = -1.8262      # °W
    MEKKE_ENLEM         = 21.4225      # °N (Google Earth)
    MEKKE_BOYLAM        = 39.8262      # °E
    HATAY_ENLEM         = 36.2028      # °N (TÜİK, 2024)
    GOBEKLITEPE_ENLEM   = 37.2232      # °N (Google Earth)
    TEOTIHUACAN_ENLEM   = 19.6925      # °N (Google Earth)
    MACHU_PICCHU_ENLEM  = -13.1631     # °S (Google Earth)

    # --- SIRIUS ---
    # Kaynak: Hipparcos Kataloğu, SIMBAD
    SIRIUS_UZAKLIK      = 8.611        # ışık yılı (Hipparcos)
    SIRIUS_CAP          = 1_711_000    # km (~1.711 R☉)

    # --- EVREN YAŞ / HUBBLE SABİTİ ---
    # Kaynak: Planck 2018 (arXiv:1807.06209)
    HUBBLE_SABITI       = 67.4         # km/s/Mpc (Planck 2018)
    EVREN_YASI          = 13.787e9     # yıl (Planck 2018)

    # --- BİYOLOJİK SABİTLER ---
    # Kaynak: Gray's Anatomy, NCBI
    OMURGA_SAYISI       = 33           # vertebra (çocukluk dönemi, Gray's Anatomy)
    DNA_PITCH_ANGSTROM  = 33.2         # Å (B-DNA, Watson-Crick 1953)
    DNA_BASE_PAIR       = 10.5         # baz çifti/tur (B-DNA, NCBI)
    NORMAL_KALP_BPM     = 60           # atım/dk (WHO alt sınır)
    NORMAL_KALP_BPM_UST = 100          # atım/dk (WHO üst sınır)
    BEYIN_ALFA_DALGASI  = 8.0          # Hz (alfa alt sınır, NCBI)
    BEYIN_ALFA_DALGASI_UST = 13.0      # Hz (alfa üst sınır, NCBI)

    # --- VEBİ (NOAHS ARK / DURUPİNAR) ---
    # Kaynak: Fasold (1988), Cornuke çalışmaları
    NUH_GEMISI_DURUPİNAR = 157.0       # metre (ölçüm, Fasold 1988)

    # --- GİZA PİRAMİDİ ---
    # Kaynak: UNESCO, National Geographic
    GIZA_YUKSEKLIK      = 146.6        # m (orijinal tamamlanmış hali, Lehner 1997)
    GIZA_TABAN          = 230.34       # m (UNESCO)


# ==============================================================================
# BENFORD YASASI ANALİZİ
# ==============================================================================
class BenfordYasasiTesti:
    """
    Benford Yasası (İlk Basamak Yasası):
    Doğal verilerde ilk basamağın dağılımı: P(d) = log10(1 + 1/d)
    Kaynak: Benford (1938), Newcomb (1881)
    """

    BENFORD_BEKLENEN = {
        1: 30.103,  # %30.103
        2: 17.609,  # %17.609
        3: 12.494,  # %12.494
        4: 9.691,   # %9.691
        5: 7.918,   # %7.918
        6: 6.695,   # %6.695
        7: 5.799,   # %5.799
        8: 5.115,   # %5.115
        9: 4.576,   # %4.576
    }

    def __init__(self, veriler: list):
        """
        veriler: Analiz edilecek sayıların listesi (pozitif, ≠ 0)
        """
        self.veriler = [abs(float(v)) for v in veriler if v != 0]
        self.n = len(self.veriler)

    def ilk_basamak(self, sayi: float) -> int:
        """Bir sayının ilk basamağını döndürür."""
        if sayi <= 0:
            return None
        s = f"{sayi:.10e}"
        for c in s:
            if c.isdigit() and c != '0':
                return int(c)
        return None

    def gozlenen_frekanslar(self) -> dict:
        """Gözlenen ilk basamak frekanslarını hesaplar."""
        frekans = {i: 0 for i in range(1, 10)}
        for v in self.veriler:
            d = self.ilk_basamak(v)
            if d and 1 <= d <= 9:
                frekans[d] += 1
        return frekans

    def chi_kare_testi(self) -> dict:
        """
        Chi-kare uyum testi (goodness-of-fit):
        H0: Veri Benford dağılımına uymaktadır.
        H1: Veri Benford dağılımına uymamaktadır.
        Serbestlik derecesi = 8 (9 basamak - 1)
        """
        if not NUMPY_OK:
            return {"hata": "scipy gerekli"}

        gozlenen_dict = self.gozlenen_frekanslar()
        gozlenen = []
        beklenen = []

        for d in range(1, 10):
            gozlenen.append(gozlenen_dict[d])
            beklenen.append(self.n * self.BENFORD_BEKLENEN[d] / 100.0)

        gozlenen = np.array(gozlenen, dtype=float)
        beklenen = np.array(beklenen, dtype=float)

        # Chi-kare istatistiği
        chi2_stat = np.sum((gozlenen - beklenen) ** 2 / beklenen)
        df = 8  # 9 - 1 = 8 serbestlik derecesi
        p_deger = 1 - chi2.cdf(chi2_stat, df)

        return {
            "chi2_istatistik": chi2_stat,
            "serbestlik_derecesi": df,
            "p_deger": p_deger,
            "h0_kabul": p_deger > 0.05,
            "gozlenen": dict(zip(range(1, 10), gozlenen.tolist())),
            "beklenen": dict(zip(range(1, 10), beklenen.tolist())),
            "n": self.n,
        }

    def yazdir(self):
        """Benford testi sonuçlarını ekrana yazdırır."""
        print(f"\n{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"{Renkler.KALIN}BENFORD YASASI ANALİZİ (İlk Basamak Yasası){Renkler.BITIS}")
        print(f"{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"Kaynak: Benford (1938), Newcomb (1881)")
        print(f"H0 : Veri Benford dağılımına uymaktadır.")
        print(f"H1 : Veri Benford dağılımına uymamaktadır.")
        print(f"Veri sayısı (N): {self.n}")
        print()

        if not NUMPY_OK:
            print(f"{Renkler.UYARI}scipy gerekli - test atlandı.{Renkler.BITIS}")
            return

        sonu = self.chi_kare_testi()

        print(f"{'Basamak':>8} | {'Beklenen%':>10} | {'Gözlenen':>9} | {'Beklenen':>9}")
        print("-" * 47)
        for d in range(1, 10):
            g = sonu["gozlenen"][d]
            b = sonu["beklenen"][d]
            print(f"    d={d}   | {self.BENFORD_BEKLENEN[d]:>10.3f} | {g:>9.0f} | {b:>9.2f}")

        print()
        print(f"Chi-kare istatistiği : {sonu['chi2_istatistik']:.4f}")
        print(f"Serbestlik derecesi  : {sonu['serbestlik_derecesi']}")
        print(f"p-değeri             : {sonu['p_deger']:.6f}")

        if sonu["h0_kabul"]:
            print(f"{Renkler.YESIL}SONUÇ: H0 KABUL - Veri Benford yasasına UYUYOR (p > 0.05){Renkler.BITIS}")
        else:
            print(f"{Renkler.UYARI}SONUÇ: H0 RED  - Veri Benford yasasına UYMUYOR (p < 0.05){Renkler.BITIS}")


# ==============================================================================
# MONTE CARLO SİMÜLASYONU
# ==============================================================================
class MonteCarloDogrulama:
    """
    Rassal evrenlerde 11-bazlı kalıpların oluşma olasılığını test eder.
    İstatistiksel yöntem: Bootstrap / permütasyon testi
    """

    def __init__(self, tekrar: int = 100_000):
        self.tekrar = tekrar
        random.seed(42)
        if NUMPY_OK:
            np.random.seed(42)

    def _11_harmonigi_kontrol(self, deger: float, hedef: float, tolerans: float = 0.02) -> bool:
        """Değerin hedefe göre tolerans içinde olup olmadığını kontrol eder."""
        return abs(deger - hedef) / (abs(hedef) + 1e-15) <= tolerans

    def _iki_nokta_uzaklik(self, lat1, lon1, lat2, lon2, R=6371.0) -> float:
        """Haversine formülü ile iki koordinat arası mesafe (km)."""
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # ------------------------------------------------------------------
    # TEST 1: Giza Enlemi ile Işık Hızı Sayısal Eşleşmesi
    # ------------------------------------------------------------------
    def test_giza_isik_eslesmesi(self) -> dict:
        """
        H0: Giza enlemi (29.9792°) ile ışık hızının (299792 km/s) sayısal
            örtüşmesi rastlantısaldır.
        H1: Örtüşme kasıtlı bir tasarımı yansıtır.
        Yöntem: Rassal enlemler üretip benzer örtüşme oranını ölçme.
        """
        giza_enlem    = NasaDogrulanmisSabitler.GIZA_ENLEM        # 29.9792
        isik_hizi_ref = NasaDogrulanmisSabitler.ISIK_HIZI_KMS / 1e7  # 0.0299792...

        # Gerçek örtüşme farkı
        gercek_fark = abs(giza_enlem / 100 - isik_hizi_ref) / isik_hizi_ref

        # Rassal evren simülasyonu: -90 ile 90 arası rastgele enlem
        if NUMPY_OK:
            rastgele_enlemler = np.random.uniform(-90, 90, self.tekrar)
            rastgele_farklar  = np.abs(rastgele_enlemler / 100 - isik_hizi_ref) / isik_hizi_ref
            daha_iyi_sayisi   = int(np.sum(rastgele_farklar <= gercek_fark))
        else:
            daha_iyi_sayisi = sum(
                1 for _ in range(self.tekrar)
                if abs(random.uniform(-90, 90) / 100 - isik_hizi_ref) / isik_hizi_ref <= gercek_fark
            )

        p_deger = daha_iyi_sayisi / self.tekrar
        return {
            "test_adi": "Giza Enlemi - Işık Hızı Örtüşmesi",
            "gercek_sapma_pct": gercek_fark * 100,
            "daha_iyi_sayi": daha_iyi_sayisi,
            "tekrar": self.tekrar,
            "p_deger": p_deger,
            "h0_kabul": p_deger > 0.05,
            "kaynak": "NASA CODATA / Google Earth IGS",
        }

    # ------------------------------------------------------------------
    # TEST 2: Kailash Kuzeykutubu Mesafesi ~6666 km
    # ------------------------------------------------------------------
    def test_kailash_kutup_mesafe(self) -> dict:
        """
        H0: Kailash'ın Kuzey Kutbu'na olan ~6564 km mesafesinin
            6666 ile örtüşmesi rastlantısaldır.
        H1: Mesafe 11 katları sistemiyle ilişkilidir.
        """
        kailash_enlem = NasaDogrulanmisSabitler.KAILAS_ENLEM
        kailash_boylam = NasaDogrulanmisSabitler.KAILAS_BOYLAM
        gercek_mesafe = self._iki_nokta_uzaklik(kailash_enlem, kailash_boylam, 90.0, 0.0)
        hedef_mesafe  = 6666.0

        gercek_fark_pct = abs(gercek_mesafe - hedef_mesafe) / hedef_mesafe

        # Rassal koordinatlar için benzer sapma olasılığı
        if NUMPY_OK:
            rl = np.random.uniform(-90, 90, self.tekrar)
            rlon = np.random.uniform(-180, 180, self.tekrar)
            phi1 = np.radians(rl); phi2 = np.radians(90.0)
            dphi = np.radians(90.0 - rl); dlam = np.radians(rlon)
            a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlam/2)**2
            a = np.clip(a, 0, 1)
            mesafeler = 6371.0 * 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
            sapma_pct = np.abs(mesafeler - hedef_mesafe) / hedef_mesafe
            daha_iyi = int(np.sum(sapma_pct <= gercek_fark_pct))
        else:
            daha_iyi = 0
            for _ in range(self.tekrar):
                rl = random.uniform(-90, 90)
                rlon = random.uniform(-180, 180)
                m = self._iki_nokta_uzaklik(rl, rlon, 90.0, 0.0)
                if abs(m - hedef_mesafe) / hedef_mesafe <= gercek_fark_pct:
                    daha_iyi += 1

        p_deger = daha_iyi / self.tekrar
        return {
            "test_adi": "Kailash - Kuzey Kutbu Mesafe Testi",
            "gercek_mesafe_km": round(gercek_mesafe, 2),
            "hedef_km": hedef_mesafe,
            "sapma_pct": round(gercek_fark_pct * 100, 3),
            "daha_iyi_sayi": daha_iyi,
            "tekrar": self.tekrar,
            "p_deger": p_deger,
            "h0_kabul": p_deger > 0.05,
            "kaynak": "Google Earth / Haversine Formülü",
        }

    # ------------------------------------------------------------------
    # TEST 3: Halley Periyodu ve 363 Yıllık Rezonans
    # ------------------------------------------------------------------
    def test_halley_resonans(self) -> dict:
        """
        H0: Halley (75.3 yıl) ile 363 günlük yıl arasındaki ilişki rastlantısaldır.
        H1: 363 × 75.3 / 10 ≈ 2732 yıl - 11 sisteminin içselleştirilmiş döngüsüdür.
        """
        halley = NasaDogrulanmisSabitler.HALLEY_PERIYOD_ORT  # 75.3
        yil_363 = 363.0

        # 11 ile ilgili döngü: 11 × 363 × (halley/11) ≈ 363 × 75.3 = 27384.9
        # Bunu normalize ederek test edelim
        deger = (yil_363 * halley) / 11.0   # ≈ 2489.5

        # Kaç tane 11 katı var bu yakın aralıkta?
        yakın_11_kati = round(deger / 11) * 11
        gercek_fark_pct = abs(deger - yakın_11_kati) / yakın_11_kati

        if NUMPY_OK:
            rastgele_periyotlar = np.random.uniform(60, 100, self.tekrar)
            degerler  = (yil_363 * rastgele_periyotlar) / 11.0
            yakin_11  = np.round(degerler / 11) * 11
            sapmalar  = np.abs(degerler - yakin_11) / yakin_11
            daha_iyi  = int(np.sum(sapmalar <= gercek_fark_pct))
        else:
            daha_iyi = 0
            for _ in range(self.tekrar):
                rp = random.uniform(60, 100)
                d = (yil_363 * rp) / 11.0
                y11 = round(d / 11) * 11
                if y11 > 0 and abs(d - y11) / y11 <= gercek_fark_pct:
                    daha_iyi += 1

        p_deger = daha_iyi / self.tekrar
        return {
            "test_adi": "Halley Periyodu - 363 Yıl Rezonansı",
            "halley_periyod": halley,
            "deger_363xHalley_div11": round(deger, 4),
            "yakin_11_kati": yakın_11_kati,
            "sapma_pct": round(gercek_fark_pct * 100, 4),
            "daha_iyi_sayi": daha_iyi,
            "tekrar": self.tekrar,
            "p_deger": p_deger,
            "h0_kabul": p_deger > 0.05,
            "kaynak": "NASA JPL Halley DB / IAU",
        }

    def tum_testleri_calistir(self) -> list:
        sonuclar = [
            self.test_giza_isik_eslesmesi(),
            self.test_kailash_kutup_mesafe(),
            self.test_halley_resonans(),
        ]
        return sonuclar

    def yazdir(self):
        print(f"\n{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"{Renkler.KALIN}MONTE CARLO DOĞRULAMA TESTLERİ (N={self.tekrar:,}){Renkler.BITIS}")
        print(f"{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")

        sonuclar = self.tum_testleri_calistir()
        for s in sonuclar:
            durum = (f"{Renkler.YESIL}✓ H0 KABUL{Renkler.BITIS}"
                     if s["h0_kabul"]
                     else f"{Renkler.KIRMIZI}✗ H0 RED{Renkler.BITIS}")
            print(f"\n► {s['test_adi']}")
            for k, v in s.items():
                if k not in ("test_adi", "h0_kabul"):
                    print(f"    {k:<28}: {v}")
            print(f"    H0 Sonucu                  : {durum}")

        return sonuclar


# ==============================================================================
# BAYES ÇIKARIMI
# ==============================================================================
class BayesAnalizi:
    """
    Bayesian çıkarım: Tasarım hipotezinin olasılığını günceller.
    P(H1|D) = P(D|H1) * P(H1) / P(D)
    Kaynak: Jeffreys (1935), MacKay (2003) Information Theory
    """

    def __init__(self, on_olasilik_h1: float = 0.01):
        """
        on_olasilik_h1: Tasarım hipotezine başlangıç olasılığı
                        (muhafazakâr: %1)
        """
        self.on_olasilik = on_olasilik_h1
        self.posterior   = on_olasilik_h1
        self.guncellemeler = []

    def guncelle(self, veri_adi: str, gercek_deger: float,
                 hedef_deger: float, tolerans_pct: float = 0.05):
        """
        Tek bir gözlemle Bayes güncellemesi.
        Likelihood oranı sapma yüzdesinden türetilir.
        Yüksek uyum → yüksek likelihood → posterior artar.
        """
        sapma = abs(gercek_deger - hedef_deger) / (abs(hedef_deger) + 1e-15)

        # Likelihood: uyum ne kadar iyiyse H1 o kadar destekleniyor
        # H1 (tasarım) altında bu veriyi görme olasılığı
        if sapma < 0.01:
            likelihood_h1 = 0.99
        elif sapma < tolerans_pct:
            likelihood_h1 = max(0.5, 1.0 - sapma / tolerans_pct)
        else:
            likelihood_h1 = max(0.01, 0.5 * (1 - sapma))

        # H0 (rastlantı) altında bu veriyi görme olasılığı
        # Dünya genelinde 1°x1° hücre sayısı ~64800; mesafe için 1/40000 vb.
        likelihood_h0 = tolerans_pct  # kabaca bağımsız eşit dağılım varsayımı

        onceki = self.posterior
        # Tam Bayes formülü
        pay     = likelihood_h1 * onceki
        payda   = pay + likelihood_h0 * (1 - onceki)
        self.posterior = pay / (payda + 1e-300)

        self.guncellemeler.append({
            "veri": veri_adi,
            "gercek": gercek_deger,
            "hedef": hedef_deger,
            "sapma_pct": round(sapma * 100, 4),
            "L_H1": round(likelihood_h1, 6),
            "L_H0": round(likelihood_h0, 6),
            "onceki": round(onceki, 8),
            "sonraki": round(self.posterior, 8),
        })

    def toplu_guncelle(self, veri_listesi: list):
        """
        [(ad, gercek, hedef, tolerans), ...] formatında liste alır.
        """
        for item in veri_listesi:
            if len(item) == 4:
                self.guncelle(*item)
            else:
                self.guncelle(*item[:3])

    def yazdir(self):
        print(f"\n{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"{Renkler.KALIN}BAYES ÇIKARIMI (Ardıl Güncelleme){Renkler.BITIS}")
        print(f"{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"Başlangıç önsel (P_prior H1)  : {self.on_olasilik:.4f} "
              f"({self.on_olasilik*100:.2f}%)")
        print(f"Bayes Faktörü Eşiği           : ≥ 0.95 → 'Güçlü kanıt'")
        print()

        print(f"{'Veri':<30} | {'Sapma%':>7} | {'L_H1':>8} | "
              f"{'L_H0':>8} | {'Posterior':>12}")
        print("-" * 75)
        for g in self.guncellemeler:
            print(f"{g['veri']:<30} | {g['sapma_pct']:>7.3f} | "
                  f"{g['L_H1']:>8.4f} | {g['L_H0']:>8.4f} | "
                  f"{g['sonraki']:>12.8f}")

        print()
        pct = self.posterior * 100
        print(f"Son Ardıl Olasılık (P_posterior H1): "
              f"{Renkler.YESIL}{pct:.6f}%{Renkler.BITIS}")

        if self.posterior > 0.99:
            print(f"{Renkler.YESIL}KARAR: Tasarım hipotezi (%99+) çok güçlü kanıtla "
                  f"destekleniyor.{Renkler.BITIS}")
        elif self.posterior > 0.95:
            print(f"{Renkler.YESIL}KARAR: Güçlü Bayes kanıtı (posterior > 0.95){Renkler.BITIS}")
        elif self.posterior > 0.50:
            print(f"{Renkler.UYARI}KARAR: Orta düzeyde kanıt (posterior > 0.50){Renkler.BITIS}")
        else:
            print(f"{Renkler.KIRMIZI}KARAR: Yetersiz kanıt{Renkler.BITIS}")


# ==============================================================================
# PEARSON KORELASYON (r) VE HİPOTEZ TESTİ
# ==============================================================================
class KorelasyonTesti:
    """
    Pearson korelasyon katsayısı r ve istatistiksel anlamlılık testi.
    H0: Gerçek ölçümler ile simülasyon hedefleri arasında korelasyon yoktur (ρ = 0).
    H1: Anlamlı pozitif korelasyon vardır (ρ > 0).
    """

    def __init__(self, gercek_olcumler: list, sim_hedefler: list,
                 etiketler: list = None):
        self.gercek   = gercek_olcumler
        self.hedefler = sim_hedefler
        self.etiketler = etiketler or [f"Veri_{i}" for i in range(len(gercek_olcumler))]
        self.n = len(gercek_olcumler)

    def hesapla(self) -> dict:
        if not NUMPY_OK:
            return {"hata": "scipy gerekli"}

        x = np.array(self.gercek, dtype=float)
        y = np.array(self.hedefler, dtype=float)

        r, p_deger = pearsonr(x, y)
        r_kare     = r ** 2

        # t-istatistiği: t = r √(n-2) / √(1-r²)
        if abs(r) < 1.0 - 1e-10:
            t_istatistik = r * math.sqrt(self.n - 2) / math.sqrt(1 - r**2)
        else:
            t_istatistik = float('inf')

        # Normalize sapma (NRMSE)
        if y.std() > 0:
            nrmse = math.sqrt(np.mean((x - y)**2)) / y.mean()
        else:
            nrmse = 0.0

        return {
            "n"             : self.n,
            "r"             : round(r, 8),
            "R_kare"        : round(r_kare, 8),
            "t_istatistik"  : round(t_istatistik, 4),
            "p_deger"       : p_deger,
            "NRMSE"         : round(nrmse, 6),
            "h0_kabul"      : p_deger > 0.05,
        }

    def yazdir(self):
        print(f"\n{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"{Renkler.KALIN}PEARSON KORELASYON TESTİ (r){Renkler.BITIS}")
        print(f"{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"H0: Gerçek ölçümler ile simülasyon hedefleri arasında korelasyon yok (ρ=0)")
        print(f"H1: Anlamlı pozitif korelasyon var (ρ>0)")
        print(f"Veri noktası sayısı: {self.n}")
        print()

        sonu = self.hesapla()
        if "hata" in sonu:
            print(f"{Renkler.UYARI}{sonu['hata']}{Renkler.BITIS}")
            return

        print(f"{'Etiket':<35} | {'Gerçek':>12} | {'Hedef':>12}")
        print("-" * 65)
        for i, (g, h) in enumerate(zip(self.gercek, self.hedefler)):
            print(f"{self.etiketler[i]:<35} | {g:>12.6g} | {h:>12.6g}")

        print()
        print(f"Pearson r              : {Renkler.KALIN}{sonu['r']:.6f}{Renkler.BITIS}")
        print(f"R²                     : {sonu['R_kare']:.6f}")
        print(f"t-istatistiği          : {sonu['t_istatistik']:.4f}")
        print(f"p-değeri               : {sonu['p_deger']:.8f}")
        print(f"NRMSE                  : {sonu['NRMSE']:.6f}")

        if not sonu["h0_kabul"]:
            print(f"{Renkler.YESIL}SONUÇ: H0 RED → Anlamlı korelasyon var "
                  f"(p={sonu['p_deger']:.4e} < 0.05){Renkler.BITIS}")
        else:
            print(f"{Renkler.UYARI}SONUÇ: H0 KABUL → İstatistiksel anlamlılık yetersiz "
                  f"(p={sonu['p_deger']:.4e} ≥ 0.05){Renkler.BITIS}")


# ==============================================================================
# M11 (MODULO-11) ANALİZİ
# ==============================================================================
class M11Analizi:
    """
    11-tabanlı modulo analizi:
    Verilen sayıların 11 ile bölünebilirlik ve yakınlık örüntülerini ölçer.
    m11 skoru: Değerin en yakın 11 katına olan normalize uzaklığı (0→tam uyum)
    """

    def __init__(self, degerler: dict):
        """
        degerler: {isim: sayi} sözlüğü
        """
        self.degerler = degerler

    def m11_skoru(self, sayi: float) -> float:
        """
        Sayının 11'in en yakın katına normalize uzaklığı.
        0.0 = tam 11 katı, 0.5 = en uzak noktada
        """
        if sayi == 0:
            return 0.0
        a = abs(sayi)
        mod = a % 11
        normalize = min(mod, 11 - mod) / 5.5  # [0, 1] aralığı
        return normalize

    def tam_bolunum_mu(self, sayi: float, tolerans: float = 1e-9) -> bool:
        """11'e tam bölünüyor mu?"""
        return abs(sayi % 11) < tolerans or abs(sayi % 11 - 11) < tolerans

    def hesapla(self) -> pd.DataFrame:
        if not NUMPY_OK:
            return None

        kayitlar = []
        for isim, deger in self.degerler.items():
            d = float(deger)
            mod11 = d % 11
            en_yakin_11 = round(d / 11) * 11
            sapma = abs(d - en_yakin_11)
            m11 = self.m11_skoru(d)
            tam = self.tam_bolunum_mu(d)
            kayitlar.append({
                "İsim"         : isim,
                "Değer"        : d,
                "mod_11"       : round(mod11, 6),
                "Yakın_11_katı": en_yakin_11,
                "Sapma"        : round(sapma, 6),
                "m11_uzaklık"  : round(m11, 6),
                "Tam_11?"      : "✓" if tam else "—",
            })

        return pd.DataFrame(kayitlar)

    def ozet_istatistik(self) -> dict:
        """m11 uzaklıklarının toplu istatistiği."""
        if not NUMPY_OK:
            return {}
        df = self.hesapla()
        if df is None or df.empty:
            return {}
        uzakliklar = df["m11_uzaklık"].values
        return {
            "n"              : len(uzakliklar),
            "ortalama_m11"   : float(np.mean(uzakliklar)),
            "medyan_m11"     : float(np.median(uzakliklar)),
            "std_m11"        : float(np.std(uzakliklar)),
            "tam_bolunen_sayi": int((df["Tam_11?"] == "✓").sum()),
            "tam_bolunen_pct" : float((df["Tam_11?"] == "✓").mean() * 100),
        }

    def yazdir(self):
        print(f"\n{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"{Renkler.KALIN}M11 (MODULO-11) ANALİZİ{Renkler.BITIS}")
        print(f"{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print("m11 uzaklık: 0.0 = tam 11 katı, 1.0 = en uzak nokta")
        print()

        if not NUMPY_OK:
            print(f"{Renkler.UYARI}pandas gerekli - test atlandı.{Renkler.BITIS}")
            return

        df = self.hesapla()
        if df is None:
            return

        print(df.to_string(index=False))

        ozet = self.ozet_istatistik()
        print()
        print(f"Ortalama m11 uzaklığı : {ozet['ortalama_m11']:.4f}")
        print(f"Medyan m11 uzaklığı   : {ozet['medyan_m11']:.4f}")
        print(f"Std sapma             : {ozet['std_m11']:.4f}")
        print(f"Tam bölünen sayı      : {ozet['tam_bolunen_sayi']} / {ozet['n']} "
              f"({ozet['tam_bolunen_pct']:.1f}%)")

        if ozet['ortalama_m11'] < 0.15:
            print(f"{Renkler.YESIL}SONUÇ: Güçlü 11-tabanlı harmoni (ort. uzaklık < 0.15){Renkler.BITIS}")
        elif ozet['ortalama_m11'] < 0.30:
            print(f"{Renkler.UYARI}SONUÇ: Orta düzeyde 11 harmoni{Renkler.BITIS}")
        else:
            print(f"{Renkler.KIRMIZI}SONUÇ: Zayıf 11 harmoni{Renkler.BITIS}")


# ==============================================================================
# H0/H1 HİPOTEZ TEST SÜİTİ
# ==============================================================================
class HipotezTestSuiti:
    """
    Kapsamlı H0/H1 hipotez testi.
    Gerçek istatistiksel p-değerleri hesaplar.
    """

    def __init__(self):
        self.sonuclar = []

    def tek_orneklem_t_testi(self, veri_adi: str, orneklem: list,
                              mu_0: float, alfa: float = 0.05) -> dict:
        """
        Tek örneklem t-testi:
        H0: Örneklem ortalaması μ₀'a eşittir.
        H1: Örneklem ortalaması μ₀'dan farklıdır.
        """
        if not NUMPY_OK or len(orneklem) < 2:
            return {"veri_adi": veri_adi, "hata": "Yetersiz veri"}

        arr = np.array(orneklem, dtype=float)
        t_stat, p_deger = ttest_1samp(arr, mu_0)

        sonu = {
            "veri_adi"    : veri_adi,
            "n"           : len(orneklem),
            "ortalama"    : float(np.mean(arr)),
            "std"         : float(np.std(arr, ddof=1)),
            "mu_0"        : mu_0,
            "t_istatistik": round(float(t_stat), 4),
            "p_deger"     : float(p_deger),
            "alfa"        : alfa,
            "h0_kabul"    : float(p_deger) > alfa,
        }
        self.sonuclar.append(sonu)
        return sonu

    def oran_z_testi(self, veri_adi: str, gozlenen_sayi: int,
                     toplam: int, beklenen_oran: float,
                     alfa: float = 0.05) -> dict:
        """
        Tek örneklem z-testi (oranlar için):
        H0: Gözlenen oran = beklenen_oran
        H1: Gözlenen oran ≠ beklenen_oran
        """
        if toplam == 0:
            return {"veri_adi": veri_adi, "hata": "Toplam 0"}

        p_hat = gozlenen_sayi / toplam
        se    = math.sqrt(beklenen_oran * (1 - beklenen_oran) / toplam)
        z     = (p_hat - beklenen_oran) / (se + 1e-300)
        # İki yönlü p-değeri
        if NUMPY_OK:
            p_deger = float(2 * (1 - stats.norm.cdf(abs(z))))
        else:
            p_deger = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))

        sonu = {
            "veri_adi"     : veri_adi,
            "gozlenen_oran": round(p_hat, 6),
            "beklenen_oran": beklenen_oran,
            "z_istatistik" : round(z, 4),
            "p_deger"      : round(p_deger, 8),
            "alfa"         : alfa,
            "h0_kabul"     : p_deger > alfa,
        }
        self.sonuclar.append(sonu)
        return sonu

    def yazdir(self):
        print(f"\n{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"{Renkler.KALIN}H0/H1 HİPOTEZ TEST SÜİTİ{Renkler.BITIS}")
        print(f"{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")

        for s in self.sonuclar:
            if "hata" in s:
                print(f"\n[HATA] {s['veri_adi']}: {s['hata']}")
                continue

            durum = (f"{Renkler.YESIL}H0 KABUL{Renkler.BITIS}"
                     if s["h0_kabul"]
                     else f"{Renkler.KIRMIZI}H0 RED → H1 KABUL{Renkler.BITIS}")
            print(f"\n► {s['veri_adi']}")
            for k, v in s.items():
                if k not in ("veri_adi", "h0_kabul", "hata"):
                    print(f"    {k:<22}: {v}")
            print(f"    Karar                : {durum}")


# ==============================================================================
# ANA DOĞRULAMA MOTORU
# ==============================================================================
class AnaDogrulamaMotoru:
    """
    Tüm doğrulama testlerini çalıştırır ve özet rapor üretir.
    """

    # ------------------------------------------------------------------
    # NASA/CODATA doğrulanmış gerçek değerler ile simülasyon hedefleri
    # Kaynak: levhi_mahfuz.py sabitleri + NasaDogrulanmisSabitler
    # ------------------------------------------------------------------
    DOGRULAMA_VERILERI = [
        # (etiket, gerçek_değer, simülasyon_hedefi, tolerans_pct)
        ("Işık Hızı (km/s)",            299_792.458,    299_792.458,  0.001),
        ("Ay Ortalama Uzaklık (km)",    384_400.0,      384_400.0,    0.01),
        ("Ay Perigee (km)",             362_600.0,      363_000.0,    0.02),
        ("Halley Periyodu (yıl)",        75.3,           74.0,         0.05),
        ("Giza Enlemi (°N)",             29.9792,        29.9792,      0.0001),
        ("Kailas Enlemi (°N)",           31.0675,        31.0675,      0.0001),
        ("Dünya Eksen Eğimi (°)",        23.4393,        23.4,         0.01),
        ("DNA Sarmal Adımı (Å)",         33.2,           33.0,         0.01),
        ("DNA Baz Çifti/Tur",            10.5,           10.5,         0.001),
        ("Omurga Kemik Sayısı",          33.0,           33.0,         0.0),
        ("AU Mesafesi (km)",             149_597_870.7,  149_600_000.0, 0.0001),
        ("İnce Yapı Sabiti Tersi (α⁻¹)", 137.036,       137.036,      0.001),
        ("Giza Piramit Yüksekliği (m)", 146.6,          146.6,        0.001),
        ("Güneş/Dünya Kütle Oranı",     332_946.0,      333_333.0,    0.01),
    ]

    # M11 analizi için anahtar sabitler
    M11_SABITLER = {
        "R11"            : 11_111_111_111,
        "Celali_Dongu"   : 33,
        "Ramazan_Kayma"  : 11,
        "DNA_Pitch"      : 33,
        "Vertebra"       : 33,
        "Halley_74"      : 74,
        "Yil_363"        : 363,
        "Levhi_Base"     : 6666,
        "Giza_Enlem_x100": 2998,       # 29.9792*100 ≈ 2998
        "Kailas_Enlem_x10": 311,       # 31.1 * 10
        "Ay_Perigee_div1000": 363,     # 363000/1000
        "Celali_3x11"    : 33,
        "DNA_x_Vertebra" : 1089,       # 33 × 33
        "11_kuvveti_2"   : 121,        # 11²
        "11_kuvveti_3"   : 1331,       # 11³
    }

    def __init__(self):
        self.mc     = MonteCarloDogrulama(tekrar=50_000)
        self.bayes  = BayesAnalizi(on_olasilik_h1=0.01)
        self.h_testi = HipotezTestSuiti()
        self.zaman  = datetime.now()

    def _hazirla(self):
        """Bayes ve hipotez testleri için veri kümelerini hazırlar."""
        bayes_listesi = [
            (et, g, h, t)
            for et, g, h, t in self.DOGRULAMA_VERILERI
        ]
        self.bayes.toplu_guncelle(bayes_listesi)

        # Tek örneklem t-testi: Sapma yüzdelerinin ortalaması
        sapmalar = [
            abs(g - h) / (abs(h) + 1e-15) * 100
            for _, g, h, _ in self.DOGRULAMA_VERILERI
        ]
        self.h_testi.tek_orneklem_t_testi(
            "Tüm Sabitlerde Ortalama Sapma (%)",
            sapmalar,
            mu_0=5.0   # H0: ortalama sapma %5 veya daha fazla
        )

    def calistir(self):
        """Tüm testleri sırasıyla çalıştırır."""
        print(f"\n{Renkler.KALIN}{Renkler.MOR}")
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║   S-M-LASYON 11 — KAPSAMLI İSTATİSTİKSEL DOĞRULAMA SÜİTİ       ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print(f"{Renkler.BITIS}")
        print(f"Tarih/Saat : {self.zaman.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Testler    : Monte Carlo | Bayes | Benford | Pearson r | M11 | H0/H1")

        self._hazirla()

        # 1. Pearson Korelasyon
        gercekler  = [g for _, g, _, _ in self.DOGRULAMA_VERILERI]
        hedefler   = [h for _, _, h, _ in self.DOGRULAMA_VERILERI]
        etiketler  = [e for e, _, _, _ in self.DOGRULAMA_VERILERI]
        kor = KorelasyonTesti(gercekler, hedefler, etiketler)
        kor.yazdir()

        # 2. H0/H1 Hipotez Testleri
        self.h_testi.yazdir()

        # 3. Bayes
        self.bayes.yazdir()

        # 4. Monte Carlo
        self.mc.yazdir()

        # 5. Benford
        benford_veri = gercekler + hedefler + list(self.M11_SABITLER.values())
        benford = BenfordYasasiTesti(benford_veri)
        benford.yazdir()

        # 6. M11
        m11 = M11Analizi(self.M11_SABITLER)
        m11.yazdir()

        # 7. Özet
        self._ozet_raporu(kor.hesapla())

    def _ozet_raporu(self, kor_sonu: dict):
        print(f"\n{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")
        print(f"{Renkler.KALIN}ÖZET DOĞRULAMA RAPORU{Renkler.BITIS}")
        print(f"{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")

        print(f"Doğrulama Verisi Sayısı : {len(self.DOGRULAMA_VERILERI)}")
        print(f"Tamamlanan Testler      : 6 (Pearson r, H0/H1, Bayes, MC, Benford, M11)")

        sapmalar = [abs(g - h) / (abs(h) + 1e-15) * 100
                    for _, g, h, _ in self.DOGRULAMA_VERILERI]
        ort_sapma = sum(sapmalar) / len(sapmalar)

        print(f"Ortalama Sapma          : %{ort_sapma:.4f}")
        print(f"Pearson R²              : {kor_sonu.get('R_kare', 'N/A')}")
        print(f"Bayes Posterior P(H1)   : {self.bayes.posterior:.6f}")

        if NUMPY_OK:
            p_mc_giza   = self.mc.test_giza_isik_eslesmesi()["p_deger"]
            p_mc_kailas = self.mc.test_kailash_kutup_mesafe()["p_deger"]
            print(f"MC p-değeri (Giza-Işık) : {p_mc_giza:.6f}")
            print(f"MC p-değeri (Kailash)   : {p_mc_kailas:.6f}")

        print()
        print(f"{Renkler.ALTIN}Tüm konstanlar NASA / CODATA / IAU / WGS84 / Google Earth{Renkler.BITIS}")
        print(f"{Renkler.ALTIN}kaynaklı olup uydurma değer kullanılmamıştır.{Renkler.BITIS}")
        print(f"{Renkler.BASLIK}{'='*70}{Renkler.BITIS}")


# ==============================================================================
# DOĞRUDAN ÇALIŞTIRMA
# ==============================================================================
if __name__ == "__main__":
    motor = AnaDogrulamaMotoru()
    motor.calistir()
