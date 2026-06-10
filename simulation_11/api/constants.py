"""Sacred constants for dashboard synthesis — sourced from levhi_mahfuz (PR 6)."""

from __future__ import annotations

from levhi_mahfuz import LevhiMahfuzConstants as LMC


def build_kadim_sabitler() -> dict[float, str]:
    """Build the dashboard tolerance dictionary from Levhi-Mahfuz constants."""
    return {
        float(LMC.BASE_SYSTEM): "11 BOYUTLU TEMEL MATRİS (11)",
        float(LMC.CELALI_CYCLE): "ÜÇLÜ SİGMA (33)",
        float(LMC.VERTEBRAE_TOTAL): "ORTA DİKME PİRAMİT SABİTİ (66)",
        float(LMC.YEAR_IDEAL_11T): "ORGANİK SİMÜLASYON YILI (363)",
        1331.0: "HACİM SABİTİ İHLALİ (11³)",
        3333.0: "KADİM DOSYA MESAFESİ (3333)",
        3630.0: "KOZMİK KOORDİNAT - AY/HATAY (3630)",
        float(LMC.IDEAL_EARTH_RADIUS): "DÜNYA/KAILASH RADYAL KESİŞİMİ (6666)",
        float(LMC.EARTH_CIRCUMFERENCE_EQUATOR): "DÜNYA ÇEVRESİ (40075 km)",
        float(LMC.SPEED_LIGHT_KMS_CODATA): "IŞIK HIZI EŞLEŞMESİ (299,792 km/s)",
        6.626: "PLANCK SABİTİ (6.626)",
        6.666: "MATRİS LAMBDA KIRILIMI (6.666)",
        3.14159: "Pİ SABİTİ (π)",
        float(LMC.PHI_GOLDEN): "ALTIN ORAN (Φ) FREKANSI",
        1.1091: "FREKANS GENİŞLEME ÇARPANI (1.1091)",
        1.1454: "HACİM VE KÜTLE GENLEŞME SABİTİ (1.1454)",
        0.8602: "MİKRO UZUNLUK SAPMASI (0.8602)",
        0.9016: "EVRENSEL ZAMAN SAPMASI (0.9016)",
    }


KADIM_SABITLER: dict[float, str] = build_kadim_sabitler()


def oran_kontrol(
    deger: float,
    sabitler: dict[float, str] | None = None,
    tolerance: float = 0.01,
) -> tuple[bool, str | None, float | None]:
    """Return whether *deger* matches a sacred constant within *tolerance*."""
    lookup = sabitler if sabitler is not None else KADIM_SABITLER
    for sabit, isim in lookup.items():
        lower = sabit * (1.0 - tolerance)
        upper = sabit * (1.0 + tolerance)
        if lower <= deger <= upper:
            return True, isim, sabit
    return False, None, None


def get_key_constants() -> dict[str, float | int]:
    """Expose a small canonical subset for dashboard status panels."""
    return {
        "BASE_SYSTEM": LMC.BASE_SYSTEM,
        "IDEAL_EARTH_RADIUS": LMC.IDEAL_EARTH_RADIUS,
        "SIMULATION_END": LMC.SIMULATION_END,
        "YEAR_IDEAL_11T": LMC.YEAR_IDEAL_11T,
        "PHI_GOLDEN": LMC.PHI_GOLDEN,
    }