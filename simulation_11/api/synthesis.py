"""Synthesis engine for dashboard discovery matching (PR 6)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Protocol

from simulation_11.api.constants import KADIM_SABITLER, oran_kontrol


class MatchReporter(Protocol):
    """Optional hook for persisting synthesis matches."""

    def on_match(
        self,
        kategori: str,
        hedef: float,
        sonuc: float,
        formul: str,
        detay: str,
    ) -> None: ...


@dataclass
class SynthesisState:
    """Rolling window of recent numeric observations."""

    son_veriler: list[float] = field(default_factory=list)
    max_history: int = 15

    def append(self, value: float) -> None:
        if len(self.son_veriler) > self.max_history:
            self.son_veriler.pop(0)
        self.son_veriler.append(value)


_DEFAULT_STATE = SynthesisState()


def sentez_motoru(
    hedef: float,
    kaynak_adi: str,
    state: SynthesisState | None = None,
    *,
    reporter: MatchReporter | None = None,
    on_module_proposal: Callable[[float, str, str], None] | None = None,
) -> tuple[bool, float | None, str | None, str | None]:
    """Match *hedef* against sacred constants via synthesis operations."""
    del kaynak_adi  # retained for dashboard/miner call-site compatibility

    active = state if state is not None else _DEFAULT_STATE
    hedef = round(abs(hedef), 5)
    if hedef <= 0:
        return False, None, None, None

    islemler: list[tuple[str, float, str]] = []

    for eski in active.son_veriler:
        if eski <= 0:
            continue
        bolme_integral = round(abs(math.log(hedef / eski) * 11) if hedef / eski > 0 else 0, 5)
        carpim_sigma = round(math.sqrt(hedef * eski) * 1.61803, 5)
        frekans_f = round((hedef + eski) / 11.0, 5)
        kozmik_fark = round(abs(hedef**2 - eski**2) / 1331.0, 5)

        islemler.extend(
            [
                ("Boyutsal İntegral (∫)", bolme_integral, f"∫_({eski})^({hedef}) Φ(x)dx"),
                ("Kuantum Düğüm Çarpanı (Σ)", carpim_sigma, f"Σ_({eski},{hedef}) (Ψ * Φ)"),
                ("Simülasyon Frekans Yansıması", frekans_f, f"({hedef}+{eski}) / 11"),
                ("Hacimsel Dalga Çökmesi (Δ)", kozmik_fark, f"|{hedef}²-{eski}²| / 11³"),
            ]
        )

    faktoriyel_11 = 39916800
    islemler.extend(
        [
            ("Logaritmik Sentez (ln)", round(math.log(hedef) * 11 if hedef > 1 else 0, 5), f"ln({hedef}) * 11"),
            ("Fraktal Repunit (1/1x1x2..)", round((hedef / 11.0) * math.pi, 5), f"({hedef} / 11) * π"),
            (
                "11'inci Basamak İzdüşümü",
                round(abs(faktoriyel_11 - (hedef * 1000)) / 1000.0, 5),
                f"|11! - {hedef}*1000| / 1000",
            ),
        ]
    )

    eslesme_bulundu = False
    en_iyi_sonuc: float | None = None
    en_iyi_kategori: str | None = None
    en_iyi_detay: str | None = None

    for _islem_adi, sonuc, formul in islemler:
        if sonuc <= 0:
            continue

        uyusuyor_mu, sabit_isim, _sabit_deger = oran_kontrol(sonuc, KADIM_SABITLER)
        if uyusuyor_mu and sabit_isim is not None:
            eslesme_bulundu = True
            kategori_etiketi = "LEVHI_MAHFUZ_SABITI"
            detay = f"Hesap: {formul} = {sonuc} -> {sabit_isim} ile eşleşti!"

            if reporter is not None:
                reporter.on_match(kategori_etiketi, hedef, sonuc, formul, detay)
            if on_module_proposal is not None:
                on_module_proposal(sonuc, detay, kategori_etiketi)

            en_iyi_sonuc = sonuc
            en_iyi_kategori = kategori_etiketi
            en_iyi_detay = detay
            break

    active.append(hedef)

    if eslesme_bulundu:
        return True, en_iyi_sonuc, en_iyi_kategori, en_iyi_detay

    uyusuyor_mu, sabit_isim, _sabit_deger = oran_kontrol(hedef, KADIM_SABITLER)
    if uyusuyor_mu and sabit_isim is not None:
        detay = f"Doğrudan Eşleşme: Girdi {hedef} = {sabit_isim}"
        if reporter is not None:
            reporter.on_match("LEVHI_MAHFUZ_SABITI", hedef, hedef, "Doğrudan Tespit", detay)
        return True, hedef, "LEVHI_MAHFUZ_SABITI", detay

    kok = math.sqrt(hedef)
    uyusuyor_mu_kok, sabit_isim_kok, _sabit_deger_kok = oran_kontrol(kok, KADIM_SABITLER)
    if uyusuyor_mu_kok and sabit_isim_kok is not None:
        detay = f"Kök Eşleşmesi: √{hedef} = {kok} -> {sabit_isim_kok}"
        if reporter is not None:
            reporter.on_match("LEVHI_MAHFUZ_SABITI", hedef, kok, f"√{hedef}", detay)
        return True, kok, "LEVHI_MAHFUZ_SABITI", detay

    return True, hedef, "GÖZLEM BAĞINTISI", f"Ağ üzerinden t_sabit(x) = {hedef} yansıması tespit edildi."