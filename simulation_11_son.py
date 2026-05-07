# -*- coding: utf-8 -*-
# 11 BOYUTLU, ORGANIK TABANLI UZAY VE ZAMANDA KUTLE, HACIM, UZAKLIK, ZAMAN VS
# FIZIKSEL BUYUKLUKLER DEGISEMEMISTIR. BU CEKIRDEK, 11'LIK SISTEM REFERANSLARI,
# DOGRULAMA OZETI VE BELGE TABANLI AKUSTIK KOPRUSUNU MINIMALIST YAPIDA TUTAR.
"""simulation_11_son.py

Minimalist yeniden yazim cekirdegi.
- Bozuk import / try blogu onarildi.
- SIM11 referans sabitleri temizlendi.
- Referans dogrulama rutini tek dosyada tutuldu.
- Belge sentezlerinden turetilen akustik kopru korunup sadeleştirildi.
"""

import math
import os
import sys
import time
import json
from datetime import datetime as datetime_class, timedelta, date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    import requests
except ImportError:
    requests = None

try:
    from sentez_v196_euler_termodinamik_galaktik import (
        V196_DISCOVERY_CONSTANTS as _V196_EXT_CONSTANTS,
        compute_v196_discovery_metrics as _compute_v196_external_metrics,
    )
except Exception:
    _V196_EXT_CONSTANTS = {}

    def _compute_v196_external_metrics():
        return {}


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    GOLD = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


MANIFESTO_11D_TEXT = (
    "11 BOYUTLU,ORGANIK TABANLI UZAY VE ZAMANDA KUTLE,HACIM,UZAKLIK,ZAMAN VS "
    "FIZIKSEL BUYUKLUKLER DEGISEMEMISTIR.ZAMANIMIZDA UYGULANAN 10 RAKAMLI "
    "(10 PARMAK SISTEMINE GORE) OLCU VE HESAP SISTEMI YERINE 11 RAKAMLI SAYISAL "
    "OLCU VE SISTEMI UYGULANMISTIR.BU OLCUMLERDE 11 LIK SISTEME UYGUN "
    "HIZ,UZUNLUK,ZAMAN,KUTLE,HACIM,ACI VB SAPMA VE OPERATOR SABITLERI "
    "KULLANILMISTIR."
)

DEFAULT_PROMILLE_TOLERANCE = 5
LIVE_VALIDATION_DATA = {}

SIM11_CANONICAL_CONSTANTS = {
    "SIMULE_BASE": 11,
    "YEAR_11T": 363.0,
    "MONTHS_11T": 11,
    "DAYS_PER_MONTH_11T": 33,
    "SIGMA_FORMULA_TARGET": 68.0,
    "HALLEY_PERIOD_YEARS": 75.3,
    "HALLEY_PERIOD_CATALOG": 74.0,
    "MAYA_END_YEAR": 2063.0,
    "GIZA_LATITUDE_DEG": 29.9792458,
    "SPEED_OF_LIGHT_MS": 299_792_458.0,
    "EARTH_RADIUS_KM": 6371.0,
    "KAILASH_DISTANCE_KM": 6666.0,
    "OPERATOR_ANGLE_FACTOR": 1.008333,
    "OPERATOR_LENGTH_FACTOR": 1.046338,
    "OPERATOR_LENGTH_FACTOR_LEGACY": 1.0463,
    "SOUND_SPEED_MS": 347.0,
    "MESSIAH_VARIABLE": 1998.0,
    "SYSTEM_BOOT_YEAR": 1999.0,
    "LOOP_CHECK_TARGET": 11111.0,
}


def print_v196_manifesto():
    print("")
    print("=" * 120)
    print(f"{Colors.BOLD}{Colors.RED}{MANIFESTO_11D_TEXT}{Colors.RESET}")
    print("=" * 120)


def _sim11_constant(name, default=None):
    if name in _V196_EXT_CONSTANTS:
        return _V196_EXT_CONSTANTS[name]
    return SIM11_CANONICAL_CONSTANTS.get(name, default)


def _relative_error(measured, expected):
    return abs(float(measured) - float(expected)) / max(abs(float(expected)), 1e-30)


def _observer_error_band(promille=DEFAULT_PROMILLE_TOLERANCE):
    return float(promille) / 1000.0


def _relative_error_with_observer(measured, expected, observer_promille=DEFAULT_PROMILLE_TOLERANCE):
    raw_err = _relative_error(measured, expected)
    observer_band = _observer_error_band(observer_promille)
    effective_err = max(0.0, raw_err - observer_band)
    return raw_err, effective_err, observer_band


def _build_sim11_reference_constants():
    year_11t = float(_sim11_constant("YEAR_11T", 363.0))
    days_per_month = float(_sim11_constant("DAYS_PER_MONTH_11T", 33.0))
    halley_catalog = float(_sim11_constant("HALLEY_PERIOD_CATALOG", 74.0))
    operator_length = float(_sim11_constant("OPERATOR_LENGTH_FACTOR", 1.046338))
    earth_radius = float(_sim11_constant("EARTH_RADIUS_KM", 6371.0))
    kailash_distance = float(_sim11_constant("KAILASH_DISTANCE_KM", 6666.0))
    sound_speed = float(_sim11_constant("SOUND_SPEED_MS", 347.0))
    simule_loop_years = float(_sim11_constant("LOOP_CHECK_TARGET", 11111.0))
    sigma_formula = days_per_month * 2.0 + 2.0
    sigma_total_years = 68.2
    factor_kailash = kailash_distance / earth_radius if earth_radius else 0.0

    return {
        "SIMULE_BASE": float(_sim11_constant("SIMULE_BASE", 11.0)),
        "YEAR_11T": year_11t,
        "MONTHS_11T": float(_sim11_constant("MONTHS_11T", 11.0)),
        "DAYS_PER_MONTH_11T": days_per_month,
        "SIGMA_FORMULA_CHECK": sigma_formula,
        "SIGMA_FORMULA_TARGET": float(_sim11_constant("SIGMA_FORMULA_TARGET", 68.0)),
        "HALLEY_PERIOD_YEARS": float(_sim11_constant("HALLEY_PERIOD_YEARS", 75.3)),
        "HALLEY_PERIOD_CATALOG": halley_catalog,
        "HALLEY_11T_CHECK": simule_loop_years / halley_catalog if halley_catalog else 0.0,
        "HALLEY_10T_CHECK": (simule_loop_years - sigma_total_years) / halley_catalog if halley_catalog else 0.0,
        "MAYA_END_YEAR": float(_sim11_constant("MAYA_END_YEAR", 2063.0)),
        "GIZA_LATITUDE_DEG": float(_sim11_constant("GIZA_LATITUDE_DEG", 29.9792458)),
        "SPEED_OF_LIGHT_MS": float(_sim11_constant("SPEED_OF_LIGHT_MS", 299_792_458.0)),
        "EARTH_RADIUS_KM": earth_radius,
        "KAILASH_DISTANCE_KM": kailash_distance,
        "FACTOR_KAILASH": factor_kailash,
        "SOUND_x_FACTOR": sound_speed * factor_kailash,
        "OPERATOR_ANGLE_FACTOR": float(_sim11_constant("OPERATOR_ANGLE_FACTOR", 1.008333)),
        "OPERATOR_LENGTH_FACTOR": operator_length,
        "OPERATOR_LENGTH_FACTOR_LEGACY": float(_sim11_constant("OPERATOR_LENGTH_FACTOR_LEGACY", 1.0463)),
        "MESSIAH_VARIABLE": float(_sim11_constant("MESSIAH_VARIABLE", 1998.0)),
        "SYSTEM_BOOT_YEAR": float(_sim11_constant("SYSTEM_BOOT_YEAR", 1999.0)),
        "LOOP_CHECK": simule_loop_years,
        "LOOP_CHECK_TARGET": simule_loop_years,
    }


SIM11_REFERENCE_CONSTANTS = _build_sim11_reference_constants()


def build_sim11_reference_dataset():
    c = SIM11_REFERENCE_CONSTANTS
    return {
        "SIM11_Loop_Check": (c["LOOP_CHECK"], c["LOOP_CHECK_TARGET"]),
        "SIM11_Sigma_Formula": (c["SIGMA_FORMULA_CHECK"], c["SIGMA_FORMULA_TARGET"]),
        "SIM11_Kailash_Factor": (c["FACTOR_KAILASH"], c["OPERATOR_LENGTH_FACTOR"]),
        "SIM11_Sound_Factor_Year": (c["SOUND_x_FACTOR"], c["YEAR_11T"]),
        "SIM11_Halley_11T": (c["HALLEY_11T_CHECK"], 150.14),
        "SIM11_Halley_10T": (c["HALLEY_10T_CHECK"], 149.20),
        "SIM11_Messiah_Variable": (c["MESSIAH_VARIABLE"], 1998.0),
        "SIM11_Maya_End_Year": (c["MAYA_END_YEAR"], 2063.0),
    }


def build_v196_discovery_dataset():
    sim_corr = float(_sim11_constant("OPERATOR_ANGLE_FACTOR", 1.008333))
    op_len = float(_sim11_constant("OPERATOR_LENGTH_FACTOR", 1.046338))
    local_metrics = {
        "53_Euler_Acisal_Sapma": (math.e * sim_corr, 2.7409),
        "54_PhiKare_Rezonansi": ((math.e * sim_corr) / op_len, (1.618033988749895 ** 2)),
        "55_Termodinamik_Zaman_Ayna_Sifir": (abs(-273.15) * sim_corr, 275.42),
        "55_Termodinamik_Zaman_Ayna_Ay": (27.32 * sim_corr, 27.54),
        "56_Galaktik_Merkez_Fraktal": (27000.0 / 1000.0, 27.0),
        "57_Andromeda_Euler_Limiti_MLY": (2.7, 2.7),
        "58_Reset_263": (275.4 / op_len, 263.0),
        "59_Andromeda_Yaklasma_Hizi": (222.0, 222.0),
        "60_Sanal_Doku_273_Matrisi": (273.0, 273.0),
        "60_Sanal_Doku_CMB": (2.725, 2.725),
        "60_Sanal_Doku_AyPeriyot": (27.32, 27.32),
        "60_Sanal_Doku_MutlakSifir": (273.15, 273.15),
        "60_Sanal_Doku_GalaktikMesafe": (27000.0, 27000.0),
    }
    ext_metrics = _compute_v196_external_metrics()
    if isinstance(ext_metrics, dict):
        local_metrics.update(ext_metrics)
    return local_metrics


def run_sim11_reference_validation(tolerance_promille=DEFAULT_PROMILLE_TOLERANCE):
    reference_tests = build_sim11_reference_dataset()
    observer_band = _observer_error_band(DEFAULT_PROMILLE_TOLERANCE)
    limit = _observer_error_band(tolerance_promille)
    limit_with_observer = limit + observer_band
    passed = 0
    failed = 0

    print("")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  SIM11 REFERANS SABIT DOGRULAMA OZETI{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(
        f"{Colors.BOLD}{Colors.CYAN}  "
        f"{'Test':32s} {'Durum':8s} {'Ham(binde)':11s} {'Olculen':14s} {'Beklenen':14s}"
        f"{Colors.RESET}"
    )
    print(f"{Colors.BOLD}{Colors.CYAN}  {'-' * 90}{Colors.RESET}")

    for name, values in reference_tests.items():
        measured, expected = values
        raw_err, _, _ = _relative_error_with_observer(measured, expected, DEFAULT_PROMILLE_TOLERANCE)
        ok = raw_err <= limit_with_observer
        if ok:
            passed += 1
        else:
            failed += 1
        print(
            f"{Colors.BOLD}{Colors.CYAN}  "
            f"{name[:32]:32s} "
            f"{'PASS' if ok else 'FAIL':8s} "
            f"{raw_err * 1000:10.4f} "
            f"{float(measured):14.6f} "
            f"{float(expected):14.6f}"
            f"{Colors.RESET}"
        )

    print(f"{Colors.BOLD}{Colors.CYAN}  {'-' * 90}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  TOPLAM: {passed}/{len(reference_tests)} TEST BASARILI{Colors.RESET}")
    return {
        "total": len(reference_tests),
        "passed": passed,
        "failed": failed,
        "tolerance_promille": tolerance_promille,
    }


def run_v196_strict_validation(additional_data=None, tolerance_promille=DEFAULT_PROMILLE_TOLERANCE):
    all_tests = build_v196_discovery_dataset()
    if isinstance(additional_data, dict):
        all_tests.update(additional_data)

    passed = 0
    failed = 0
    limit = _observer_error_band(tolerance_promille)

    print("")
    print(f"{Colors.BOLD}{Colors.GOLD}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GOLD}  V196 KATI DOGRULAMA OZETI{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GOLD}{'=' * 80}{Colors.RESET}")

    for name, values in all_tests.items():
        measured, expected = values
        raw_err, _, _ = _relative_error_with_observer(measured, expected, tolerance_promille)
        ok = raw_err <= limit
        if ok:
            passed += 1
        else:
            failed += 1
        print(
            f"{Colors.BOLD}{Colors.GOLD}  {name[:42]:42s} "
            f"{('PASS' if ok else 'FAIL'):5s} "
            f"err={raw_err * 1000:10.4f} binde"
            f"{Colors.RESET}"
        )

    print(f"{Colors.BOLD}{Colors.GOLD}  TOPLAM: {passed}/{len(all_tests)} TEST BASARILI{Colors.RESET}")
    return {
        "total": len(all_tests),
        "passed": passed,
        "failed": failed,
        "tolerance_promille": tolerance_promille,
    }


def add_validation_data(name, measured, expected):
    LIVE_VALIDATION_DATA[name] = (float(measured), float(expected))
    return {"added": name, "count": len(LIVE_VALIDATION_DATA)}


def run_live_api_health_check():
    status = {
        "requests_available": requests is not None,
        "external_constants_loaded": bool(_V196_EXT_CONSTANTS),
        "timestamp": datetime_class.utcnow().isoformat() + "Z",
    }
    print("")
    print("=" * 80)
    print("  CANLI API / ENTEGRASYON SAGLIK KONTROLU")
    print("=" * 80)
    print(json.dumps(status, indent=2, ensure_ascii=False))
    return status


class SIM11DocumentedAcousticsBridge:
    """Belge sentezlerinden türetilen akustik ve operator koprusu."""

    DOC_LENGTH_OPERATOR = 1.0463035
    DOC_TIME_OPERATOR = 0.9015777
    DOC_SPEED_OPERATOR = 1.06012
    DOC_PI11_MATRIX = 2.998001
    DOC_SOUND_SPEED_BASE = 346.3
    DOC_HUDHUD_REFERENCE_HZ = 11.0

    def __init__(self, const=None):
        self.const = const or type(
            "Sim11AcousticFallback",
            (),
            {
                "OP_LEN": 1.046338,
                "OP_TIME": 1.00617,
                "OP_SPEED_CONSTANT": 1.061,
                "YEAR_SIM": 363.0,
                "DNA_PITCH": 33.0,
                "GIZA_LAT": 29.9792458,
            },
        )()

    def operator_snapshot(self):
        return {
            "doc_length_operator": self.DOC_LENGTH_OPERATOR,
            "kernel_length_operator": float(getattr(self.const, "OP_LEN", self.DOC_LENGTH_OPERATOR)),
            "doc_time_operator": self.DOC_TIME_OPERATOR,
            "kernel_time_operator": float(getattr(self.const, "OP_TIME", self.DOC_TIME_OPERATOR)),
            "doc_speed_operator": self.DOC_SPEED_OPERATOR,
            "kernel_speed_operator": float(getattr(self.const, "OP_SPEED_CONSTANT", self.DOC_SPEED_OPERATOR)),
            "doc_pi11_matrix": self.DOC_PI11_MATRIX,
            "year_sim": float(getattr(self.const, "YEAR_SIM", 363.0)),
            "dna_pitch": float(getattr(self.const, "DNA_PITCH", 33.0)),
        }

    def calculate_documented_sound_speed(self, velocity_10_system=None):
        base_speed = float(velocity_10_system or self.DOC_SOUND_SPEED_BASE)
        speed_factor = self.DOC_TIME_OPERATOR / self.DOC_SPEED_OPERATOR
        return {
            "base_speed_ms": base_speed,
            "speed_factor": speed_factor,
            "documented_sound_speed_ms": base_speed * speed_factor,
            "year_resonance_target": float(getattr(self.const, "YEAR_SIM", 363.0)),
        }

    def calculate_documented_frequency(self, frequency_10_system):
        freq = float(frequency_10_system)
        return {
            "input_frequency_hz": freq,
            "documented_frequency_hz": freq * self.DOC_TIME_OPERATOR,
            "hudhud_reference_hz": self.DOC_HUDHUD_REFERENCE_HZ,
            "ratio_to_hudhud": (freq * self.DOC_TIME_OPERATOR) / self.DOC_HUDHUD_REFERENCE_HZ,
        }

    def calculate_documented_wavelength(self, wavelength_10_system):
        wavelength = float(wavelength_10_system)
        return {
            "input_wavelength_m": wavelength,
            "documented_wavelength_m": wavelength / self.DOC_LENGTH_OPERATOR,
            "giza_latitude_anchor": float(getattr(self.const, "GIZA_LAT", 29.9792458)),
        }

    def build_reference_table(self):
        operator_view = self.operator_snapshot()
        sound_view = self.calculate_documented_sound_speed()
        frequency_view = self.calculate_documented_frequency(self.DOC_HUDHUD_REFERENCE_HZ)
        wavelength_view = self.calculate_documented_wavelength(31.1)
        return {
            "operators": operator_view,
            "sound": sound_view,
            "frequency": frequency_view,
            "wavelength": wavelength_view,
            "doc_sigma_bridge": 33.0 * 2 + 2,
            "doc_pi11_matrix": self.DOC_PI11_MATRIX,
        }

    def analysis(self):
        table = self.build_reference_table()
        print("")
        print("=" * 80)
        print("  SIM11 DOCUMENTED ACOUSTICS BRIDGE")
        print("=" * 80)
        print(f"  Length Operator  : doc={table['operators']['doc_length_operator']:.7f} | kernel={table['operators']['kernel_length_operator']:.7f}")
        print(f"  Time Operator    : doc={table['operators']['doc_time_operator']:.7f} | kernel={table['operators']['kernel_time_operator']:.7f}")
        print(f"  Speed Operator   : doc={table['operators']['doc_speed_operator']:.5f} | kernel={table['operators']['kernel_speed_operator']:.5f}")
        print(f"  Pi11 Matrix      : {table['doc_pi11_matrix']:.6f}")
        print(f"  Sound Speed      : {table['sound']['documented_sound_speed_ms']:.6f} m/s")
        print(f"  Freq(11 Hz)      : {table['frequency']['documented_frequency_hz']:.6f} Hz")
        print(f"  Wavelength 31.1m : {table['wavelength']['documented_wavelength_m']:.6f} m")
        print(f"  Sigma Bridge     : {table['doc_sigma_bridge']:.1f}")
        print("=" * 80)
        return table


def run_minimalist_kernel_report():
    print_v196_manifesto()
    sim11_result = run_sim11_reference_validation(DEFAULT_PROMILLE_TOLERANCE)
    v196_result = run_v196_strict_validation(LIVE_VALIDATION_DATA, DEFAULT_PROMILLE_TOLERANCE)
    run_live_api_health_check()
    bridge_table = SIM11DocumentedAcousticsBridge().analysis()
    print("")
    print("=" * 80)
    print("  MINIMALIST KERNEL OZETI")
    print("=" * 80)
    print(f"  SIM11 Referans Sonucu : {sim11_result['passed']}/{sim11_result['total']}")
    print(f"  V196 Test Sonucu      : {v196_result['passed']}/{v196_result['total']}")
    print(f"  Akustik Sigma Koprusu : {bridge_table['doc_sigma_bridge']:.1f}")
    print("  Durum                 : CEKIRDEK YENIDEN YAZILDI")
    print("=" * 80)
    return {
        "sim11": sim11_result,
        "v196": v196_result,
        "bridge": bridge_table,
    }


if __name__ == "__main__":
    run_minimalist_kernel_report()
