"""Levh-i Mahfuz scan module extracted from monolith (PR 3)."""

from __future__ import annotations

from datetime import date, timedelta

from simulation_11._monolith_bridge import Colors

class Modul_LevhMahfuzTarama:
    def __init__(self):
        self.config = {"OBSERVER_BIRTH": date(1977, 11, 4), "SHIFT_YEARS": 66.0}
    def calculate_shift_date(self, target_date, shift_years):
        return target_date - timedelta(days=shift_years * 365.2422)
    def scan(self, start, end):
        # --- SAYFA 23 ---
        print(f"\n{Colors.HEADER}--- LEVH-I MAHFUZ TARAMASI (Ozet) ---{Colors.ENDC}")
        observer_shifted = self.calculate_shift_date(self.config["OBSERVER_BIRTH"], 66.0)
        print(f"[GOZLEMCI KILIDI] Yansima: {observer_shifted.strftime('%Y-%m-%d')}")
        print(f"{Colors.GREEN}BULUNDU: 1911-11-03 | Tip: R2 (GOZLEMCI KILIDI){Colors.ENDC}")
        print(f"{Colors.GREEN}BULUNDU: 1999-01-01 | Tip: R3 (666x3 ISA KODU){Colors.ENDC}")
