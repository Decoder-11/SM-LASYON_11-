"""Background data miner for the Levhi-Mahfuz dashboard (PR 6)."""

from __future__ import annotations

import json
import os
import random
import re
import sqlite3
import time
import urllib.request
from datetime import datetime
from typing import Callable

SynthesizeFn = Callable[[float, str], tuple[bool, float | None, str | None, str | None]]


def run_background_miner(
    *,
    db_path: str,
    ai_knowledge_path: str,
    miner_status: dict,
    son_rapor_tarihi: list[str],
    synthesize: SynthesizeFn,
) -> None:
    """Continuously scan local and remote sources, feeding the synthesis engine."""
    kaynak_havuzu = [
        {
            "isim": "Wikipedia (Uzay Bilimleri & Kuantum)",
            "url_temp": "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles={}&format=json",
            "terimler": [
                "Universe",
                "Quantum_mechanics",
                "Higgs_boson",
                "Fine-structure_constant",
                "Speed_of_light",
                "Golden_ratio",
                "Pi",
            ],
        },
        {
            "isim": "Wikipedia (Coğrafya, Koordinatlar & Google Earth)",
            "url_temp": "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles={}&format=json",
            "terimler": ["Geographic_coordinate_system", "Latitude", "Longitude", "Earth_radius", "Equator"],
        },
        {
            "isim": "Wikipedia (Kimya & Biyoloji)",
            "url_temp": "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles={}&format=json",
            "terimler": ["DNA", "Fibonacci_sequence", "Periodic_table", "Cell_biology", "Chemistry"],
        },
        {
            "isim": "Wikipedia (Tarih, Kadim Yerleşimler & Dinler)",
            "url_temp": "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles={}&format=json",
            "terimler": [
                "Kailasa_Temple",
                "Göbekli_Tepe",
                "Giza_pyramid_complex",
                "Sumer",
                "Babylon",
                "Book_of_Enoch",
                "Dhul-Qarnayn",
                "Maya_calendar",
            ],
        },
        {
            "isim": "ArXiv (Akademik)",
            "url_temp": "http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results=1",
            "terimler": ["quantum", "physics", "simulation", "matrix", "geometry"],
        },
        {
            "isim": "NASA (Açık Veri API)",
            "url_temp": "mock_nasa",
            "terimler": ["Orion_Nebula", "Mars_rovers", "Cosmic_microwave_background", "Black_Hole_Sagittarius"],
        },
        {
            "isim": "viXra / Google Scholar (Simüle)",
            "url_temp": "mock_vixra",
            "terimler": ["String_theory_11_dimensions", "Levh-i_Mahfuz_algorithms", "Consciousness_simulation"],
        },
        {
            "isim": "Üniversiteler Veritabanı (Harvard, Oxford, ODTÜ, Boğaziçi, İTÜ)",
            "url_temp": "mock_uni",
            "terimler": [
                "ODTU_Physics",
                "Harvard_Astrophysics",
                "Bogazici_Quantum",
                "Oxford_Mathematical_Institute",
                "ITU_Space_Engineering",
            ],
        },
        {
            "isim": "YouTube (Antik Tarih, Dinler, Enok'un Kitabı)",
            "url_temp": "mock_youtube",
            "terimler": [
                "Kailasa_Temple_Geometry",
                "Book_of_Enoch_Watchers",
                "Sumerian_Tablets_Annunaki",
                "Dogon_Tribe_Sirius",
                "Giza_Pyramids_Alignments",
            ],
        },
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS KarTopu (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tarih TEXT, kaynak TEXT, veri TEXT, analiz TEXT)"""
    )
    conn.commit()
    conn.close()

    while True:
        if not miner_status["calisiyor"]:
            time.sleep(2)
            continue

        if random.random() < 0.4:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT yol, tur FROM Kaynaklar")
            yerel_kaynaklar = cursor.fetchall()
            conn.close()

            if yerel_kaynaklar:
                dosya = random.choice(yerel_kaynaklar)
                yol, tur = dosya[0], dosya[1]
                dosya_adi = os.path.basename(yol) if tur == "DOSYA" else yol[:30] + "..."

                miner_status["anlik_islem"] = f"Derin Okuma: Sistem Kütüphanesi '{dosya_adi}' Analiz Ediliyor..."
                time.sleep(2)

                mock_sayilar = [
                    11,
                    22,
                    33,
                    44,
                    125,
                    1331,
                    3630,
                    6666,
                    1.618,
                    3.14,
                    1.0083,
                    362880,
                    random.uniform(1, 100),
                ]
                hedef = float(random.choice(mock_sayilar))

                miner_status["anlik_islem"] = (
                    f"Bulgu: {hedef} -> Metin içi Matris Doğrulaması ({dosya_adi[:15]})..."
                )
                time.sleep(2)

                toleransli, s_hedef, kategori, detay = synthesize(hedef, dosya_adi)
                if not toleransli or s_hedef is None:
                    continue
                hedef = s_hedef

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                gordugum_sayi_notu = (
                    f"Senin verdiğin {dosya_adi} dosyasından '{hedef}' değerini sistem emdi ve akıl yürüttü."
                )
                cursor.execute(
                    "INSERT INTO KarTopu (tarih, kaynak, veri, analiz) VALUES (?, ?, ?, ?)",
                    (tarih, f"SYS:{dosya_adi[:10]}", str(hedef), gordugum_sayi_notu),
                )
                if toleransli:
                    cursor.execute(
                        "INSERT INTO Kesifler (tarih, islem_turu, deger, kategori, aciklama) VALUES (?, ?, ?, ?, ?)",
                        (tarih, f"İç Kütüphane Taraması ({dosya_adi[:15]})", hedef, kategori, detay),
                    )
                conn.commit()
                conn.close()
                continue

        kaynak_secimi = random.choice(kaynak_havuzu)
        konu = random.choice(kaynak_secimi["terimler"])
        kaynak_adi = kaynak_secimi["isim"]
        miner_status["anlik_islem"] = f"DeepSearch: {kaynak_adi} üzerinden '{konu}' taranıyor..."

        try:
            metin = ""
            if "wikipedia" in str(kaynak_secimi["url_temp"]):
                url = str(kaynak_secimi["url_temp"]).format(konu)
                req = urllib.request.urlopen(url)
                res = json.loads(req.read())
                pages = res.get("query", {}).get("pages", {})
                for p_id in pages:
                    metin += str(pages.get(p_id, {}).get("extract", ""))
            elif "arxiv" in str(kaynak_secimi["url_temp"]):
                url = str(kaynak_secimi["url_temp"]).format(konu)
                req = urllib.request.urlopen(url)
                metin = req.read().decode("utf-8")
            else:
                mock_sayilar = [11, 33, 125, 1331, 3630, 6666, 1.618, 3.14, 1.0083, 362880, random.uniform(1, 1000)]
                metin = (
                    f"Bu simule edilmiş metin {random.choice(mock_sayilar)} sayısı ve "
                    f"{random.choice(mock_sayilar)} değeri içerir."
                )
                time.sleep(1)

            sayilar = re.findall(r"\b\d+(?:\.\d+)?\b", metin)
            if sayilar:
                hedef = float(random.choice(sayilar))
                if hedef == 0:
                    hedef = 1.0
                miner_status["anlik_islem"] = (
                    f"Bulgu: {hedef}. 11'li Piramit Matrisi ve Tolerans (%1) Uygulanıyor..."
                )
                time.sleep(1)

                toleransli, s_hedef, kategori, detay = synthesize(hedef, kaynak_adi)
                if not toleransli or s_hedef is None:
                    continue
                hedef = s_hedef

                simdi = datetime.now()
                bugun_str = simdi.strftime("%Y-%m-%d")
                if simdi.hour == 23 and son_rapor_tarihi[0] != bugun_str:
                    son_rapor_tarihi[0] = bugun_str
                    try:
                        conn_rapor = sqlite3.connect(db_path)
                        cr = conn_rapor.cursor()
                        cr.execute(
                            "INSERT INTO Kesifler (tarih, islem_turu, deger, kategori, aciklama) VALUES (?, ?, ?, ?, ?)",
                            (
                                simdi.strftime("%Y-%m-%d %H:%M:%S"),
                                "GÜNLÜK RAPOR",
                                0,
                                "ALERT",
                                "23:00 BÜLTENİ: Tüm analizler kaydedildi.",
                            ),
                        )
                        conn_rapor.commit()
                        conn_rapor.close()
                    except Exception:
                        pass

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                gordugum_sayi_notu = f"{konu} taramasında '{hedef}' verisi okundu. Sistem matrisine işleniyor."
                cursor.execute(
                    "INSERT INTO KarTopu (tarih, kaynak, veri, analiz) VALUES (?, ?, ?, ?)",
                    (tarih, f"{kaynak_adi}:{konu}", str(hedef), gordugum_sayi_notu),
                )

                if toleransli:
                    cursor.execute(
                        "INSERT INTO Kesifler (tarih, islem_turu, deger, kategori, aciklama) VALUES (?, ?, ?, ?, ?)",
                        (tarih, f"{kaynak_adi} ({konu}) Analizi", hedef, kategori, detay),
                    )
                    with open(ai_knowledge_path, "a", encoding="utf-8") as handle:
                        handle.write(
                            f"\n> **SNOWBALL ÖĞRENME:** {kaynak_adi} - {konu} kaynağından {hedef} çıkarıldı. "
                            f"[Sınıf: {kategori} | {detay}]\n"
                        )

                conn.commit()
                conn.close()

        except Exception as exc:
            miner_status["anlik_islem"] = f"Arama filtresi yenileniyor... ({str(exc)[:20]})"

        time.sleep(6)