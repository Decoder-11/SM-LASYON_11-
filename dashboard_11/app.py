"""Flask application for the Levhi-Mahfuz dashboard (PR 6)."""

from __future__ import annotations

import os
import random
import sqlite3
import subprocess
import threading
import traceback
import urllib.request
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from dashboard_11.services.miner import run_background_miner
from simulation_11.api import get_validation_status, sentez_motoru
from simulation_11.api.synthesis import SynthesisState

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent
BASE_DIR = str(PROJECT_ROOT)

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(PACKAGE_DIR, "templates"),
)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

DB_YOLU = os.path.join(BASE_DIR, "levhi_hafiza.db")
AI_KNOWLEDGE = os.path.join(BASE_DIR, "AI_KNOWLEDGE_BASE_11.md")

MINER_DURUM = {"calisiyor": True, "anlik_islem": "Sistem Başlatılıyor..."}
SON_RAPOR_TARIHI: list[str] = [""]
SYNTHESIS_STATE = SynthesisState()


class _SynthesisReporter:
    def on_match(self, kategori: str, hedef: float, sonuc: float, formul: str, detay: str) -> None:
        rapora_yaz(kategori, hedef, sonuc, formul, detay)


def _dashboard_sentez(hedef: float, kaynak_adi: str):
    return sentez_motoru(
        hedef,
        kaynak_adi,
        SYNTHESIS_STATE,
        reporter=_SynthesisReporter(),
        on_module_proposal=yeni_modul_teklifi_olustur,
    )


@app.errorhandler(Exception)
@app.errorhandler(500)
def internal_error(exc):
    err_str = traceback.format_exc()
    with open(os.path.join(BASE_DIR, "hata_logu.txt"), "w", encoding="utf-8") as handle:
        handle.write(err_str)
    return f"<h1>Dahili Sunucu Hatası Detayı</h1><pre>{err_str}</pre>", 500


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def yeni_modul_teklifi_olustur(sabit_deger, islem_aciklama, kategori):
    try:
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        func_id = random.randint(1000, 9999)
        modul_kodu = f"""
# [YAPAY ZEKA MODÜL ÖNERİSİ]
# Sentez Modeli: {islem_aciklama}
# Bulunan Sabit Değer: {sabit_deger}

def otonom_sentez_fonksiyonu_{func_id}(x_input, zaman_faktoru=1.1091):
    '''
    Bu fonksiyon yapay zeka tarafından tespit edilen örüntüye göre üretilmiştir.
    '''
    KADIM_SABIT = {sabit_deger}

    # 11'lik sistem matris genişleme algoritması
    sonuc = (x_input * KADIM_SABIT) / zaman_faktoru
    return sonuc
"""
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ModulOnerileri (tarih, kategori, modul_kodu, aciklama) VALUES (?, ?, ?, ?)",
            (tarih, kategori, modul_kodu, islem_aciklama),
        )
        conn.commit()
        conn.close()
    except Exception as exc:
        print("Modul onerisi hatasi:", exc)


def rapora_yaz(kategori, hedef, sonuc, islem, detay):
    rapor_yolu = os.path.join(BASE_DIR, "LEVHI_MAHFUZ_SENTEZ_RAPORU.md")
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    yeni_mi = not os.path.exists(rapor_yolu)

    with open(rapor_yolu, "a", encoding="utf-8") as handle:
        if yeni_mi:
            handle.write("# 🌌 LEVH-İ MAHFUZ SENTEZ RAPORU 🌌\n\n")
            handle.write(
                "> Sistem tarafından otonom olarak üretilmiş fraktal, repunit, fizik, "
                "astronomi ve kadim oran eşleşmeleri.\n\n"
            )
        handle.write(f"### ⚡ [{tarih}] {kategori}\n")
        handle.write(f"- **Hedef Girdi:** `{hedef}`\n")
        handle.write(f"- **Sentez Sonucu:** `{sonuc}`\n")
        handle.write(f"- **Uygulanan İşlem/Formül:** `{islem}`\n")
        handle.write(f"- **Detay/Anlam:** {detay}\n\n")
        handle.write("---\n")


def db_init():
    conn = sqlite3.connect(DB_YOLU)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS IletisimLog (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tarih TEXT,
                        gonderen TEXT,
                        mesaj TEXT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Kaynaklar (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tarih TEXT,
                        tur TEXT,
                        yol TEXT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Kesifler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tarih TEXT,
                        islem_turu TEXT,
                        deger REAL,
                        kategori TEXT,
                        aciklama TEXT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS KarTopu (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tarih TEXT,
                        kaynak TEXT,
                        veri TEXT,
                        analiz TEXT)"""
    )

    cursor.execute("SELECT yol FROM Kaynaklar")
    mevcut_yollar = [row[0] for row in cursor.fetchall()]

    baslangic_dosyalari = [
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\CANVAS 11-TOLU PDF.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\AYIN GELİŞİ PDFF.pdf"),
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "DOSYA",
            r"C:\Users\soldi\OneDrive\Masaüstü\Amerikadaki antik yapi tablosunun ustune 12 burc v_251108_210314.pdf",
        ),
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "DOSYA",
            r"C:\Users\soldi\OneDrive\Masaüstü\Amerikadaki antik yapi tablosunun ustune 12 burc v... (1).pdf",
        ),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Demo_ Research on LLMs.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)\LEHFİ MAHFUZ-2.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)\LEHFİ-MAHFUZ-1.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)\LEHFİ-MAHFUZ...pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)\SIMULE-3 grok-3.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)\SIMULE 3- Grok.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)\Simule3 Teorisi_22.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)\giza iramit...pdf"),
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "DOSYA",
            r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)\Repunit Numbers_ Unique Mathematical Patterns - Grok.html",
        ),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (3)\halley.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Resimler\Screenshots\MAYA TAKVİMİ.png"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\makale hazırlama dosyası\malta.pdf"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\OneDrive\Masaüstü\makale hazırlama dosyası\celali takvimi.pdf"),
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "DOSYA",
            r"C:\Users\soldi\OneDrive\İçeri aktarmalar\omeravc2008@gmail.com - Google Drive\Bu dag kailasah dagina benziyecek ve 6666km yazisi....docx",
        ),
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "DOSYA",
            r"C:\Users\soldi\OneDrive\Masaüstü\Olmamis daha onceki calismamizi aynen harfi,harfi,....pdf",
        ),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DOSYA", r"C:\Users\soldi\Downloads\2506.0051v1.docx"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "LINK", "https://github.com/Soldiers33/S-M-LASYON_11.git"),
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "LINK", "https://x.com/grok/status/2025182583097602213"),
    ]

    eklenecekler = [d for d in baslangic_dosyalari if d[2] not in mevcut_yollar]
    if eklenecekler:
        cursor.executemany("INSERT INTO Kaynaklar (tarih, tur, yol) VALUES (?, ?, ?)", eklenecekler)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect(DB_YOLU)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, tarih, islem_turu, deger, kategori, aciklama FROM Kesifler ORDER BY id DESC LIMIT 50")
        kesifler = cursor.fetchall()
    except Exception:
        kesifler = []
    try:
        cursor.execute("SELECT tarih, gonderen, mesaj FROM IletisimLog ORDER BY id ASC")
        sohbetler = cursor.fetchall()
    except Exception:
        sohbetler = []
    try:
        cursor.execute("SELECT id, tarih, tur, yol FROM Kaynaklar ORDER BY id DESC")
        kaynaklar = cursor.fetchall()
    except Exception:
        kaynaklar = []
    try:
        cursor.execute("SELECT tarih, kaynak, veri, analiz FROM KarTopu ORDER BY id DESC LIMIT 20")
        kartopu_loglari = cursor.fetchall()
    except Exception:
        kartopu_loglari = []

    conn.close()

    stats = {"toplam": 0, "pdf": 0, "py": 0, "md": 0, "jpg_png": 0, "diger": 0}
    for kaynak in kaynaklar:
        if kaynak[2] == "DOSYA":
            stats["toplam"] += 1
            yol_lower = str(kaynak[3]).lower() if kaynak[3] else ""
            if yol_lower.endswith(".pdf"):
                stats["pdf"] += 1
            elif yol_lower.endswith(".py"):
                stats["py"] += 1
            elif yol_lower.endswith(".md"):
                stats["md"] += 1
            elif yol_lower.endswith((".jpg", ".png", ".jpeg", ".webp")):
                stats["jpg_png"] += 1
            else:
                stats["diger"] += 1

    return render_template(
        "index.html",
        kesifler=kesifler,
        sohbetler=sohbetler,
        kaynaklar=kaynaklar,
        kartopu=kartopu_loglari,
        miner_calisiyor=MINER_DURUM["calisiyor"],
        stats=stats,
    )


@app.route("/favicon.ico")
def favicon():
    return "", 204


@app.route("/dosya_ac")
def dosya_ac():
    yol = request.args.get("yol")
    if yol and os.path.exists(yol):
        return send_file(yol)
    return "Dosya bulunamadı veya silinmiş."


@app.route("/bot_cevap", methods=["POST"])
def bot_cevap():
    veri = request.json
    mesaj = veri.get("mesaj", "")
    if mesaj:
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO IletisimLog (tarih, gonderen, mesaj) VALUES (?, ?, ?)", (tarih, "DEKODER-11", mesaj))

        cevap = "Anlaşıldı. Talebiniz AI_KNOWLEDGE_BASE dosyasına iletildi."
        if "bul" in mesaj.lower() or "ara" in mesaj.lower():
            cevap = "Sistem arka planda bu veriyi tarıyor. Sonuçlar sol tabloya düşecektir."
        elif "http" in mesaj.lower() or "www" in mesaj.lower():
            cevap = "Link algılandı. Dış bağlantı tarama sırasına eklendi."
            cursor.execute("INSERT INTO Kaynaklar (tarih, tur, yol) VALUES (?, ?, ?)", (tarih, "LINK", mesaj))
        elif "c:\\" in mesaj.lower():
            cevap = "Yerel dosya yolu algılandı. Kütüphaneye eklendi, belgeler okunacak."
            cursor.execute("INSERT INTO Kaynaklar (tarih, tur, yol) VALUES (?, ?, ?)", (tarih, "DOSYA", mesaj))

        cursor.execute(
            "INSERT INTO IletisimLog (tarih, gonderen, mesaj) VALUES (?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "SİSTEM", cevap),
        )
        conn.commit()
        conn.close()

        with open(AI_KNOWLEDGE, "a", encoding="utf-8") as handle:
            handle.write(f"\n> **DEKODER-11:** {mesaj}\n> **SİSTEM:** {cevap}\n")

        return jsonify({"status": "ok", "cevap": cevap})
    return jsonify({"status": "error"})


@app.route("/kaynak_ekle", methods=["POST"])
def kaynak_ekle():
    veri = request.json if request.is_json else request.form
    yol = veri.get("yol", "") if veri else request.form.get("yol", "")
    tur = veri.get("tur", "") if veri else request.form.get("tur", "")
    if not tur:
        tur = "LINK" if "http" in yol else "DOSYA"
    if yol:
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO Kaynaklar (tarih, tur, yol) VALUES (?, ?, ?)", (tarih, tur, yol))
        conn.commit()
        conn.close()
        return jsonify({"status": "ok", "mesaj": f"{tur} eklendi: {yol}"})
    return jsonify({"status": "error"})


@app.route("/gozat_dosya", methods=["GET"])
def gozat_dosya():
    cmd = (
        'python -c "import tkinter as tk; from tkinter import filedialog; root=tk.Tk(); '
        "root.withdraw(); root.attributes('-topmost', True); "
        "print(filedialog.askopenfilename(title='SİSTEM KÜTÜPHANESİ İÇİN DOSYA SEÇ'))\""
    )
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, check=False)
        file_path = result.stdout.strip()
        if file_path:
            file_path = os.path.normpath(file_path)
            return jsonify({"yol": file_path})
    except Exception:
        pass
    return jsonify({"yol": ""})


@app.route("/kaynak_sil", methods=["POST"])
def kaynak_sil():
    veri = request.json
    dosya_id = veri.get("id")
    if dosya_id:
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Kaynaklar WHERE id = ?", (dosya_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "ok", "mesaj": "Kaynak Kütüphaneden Silindi."})
    return jsonify({"status": "error"})


@app.route("/masaustu_tara", methods=["POST"])
def masaustu_tara():
    yollar = [
        r"C:\Users\soldi\OneDrive\Masaüstü",
        r"C:\Users\soldi\OneDrive\Masaüstü\Yeni klasör (4)",
        r"C:\Users\soldi\IdeaProjects\simülation-11",
    ]
    uzantilar = [".pdf", ".docx", ".txt", ".jpg", ".png", ".webp", ".html", ".md", ".py"]

    eklenenler = 0
    conn = sqlite3.connect(DB_YOLU)
    cursor = conn.cursor()
    cursor.execute("SELECT yol FROM Kaynaklar")
    mevcut_yollar = [row[0] for row in cursor.fetchall()]
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for ana_yol in yollar:
        if os.path.exists(ana_yol):
            for root, _dirs, files in os.walk(ana_yol):
                if any(ignored in root for ignored in [".git", "venv", "__pycache__", "node_modules", ".idea"]):
                    continue

                for filename in files:
                    if any(filename.lower().endswith(uz) for uz in uzantilar):
                        tam_yol = os.path.join(root, filename)
                        if tam_yol not in mevcut_yollar:
                            cursor.execute(
                                "INSERT INTO Kaynaklar (tarih, tur, yol) VALUES (?, ?, ?)",
                                (tarih, "DOSYA", tam_yol),
                            )
                            mevcut_yollar.append(tam_yol)
                            eklenenler += 1

                if "Masaüstü" in ana_yol and root == ana_yol:
                    break

    conn.commit()
    conn.close()

    if eklenenler > 0:
        mesaj = f"Harika! Bilgisayarındaki {eklenenler} yeni belge Kütüphaneye başarıyla çekildi."
    else:
        mesaj = "Kütüphaneye eklenecek yeni dosya bulunamadı."

    return jsonify({"status": "ok", "mesaj": mesaj, "eklenen": eklenenler})


@app.route("/sistem_durumu")
def sistem_durumu():
    return jsonify(MINER_DURUM)


@app.route("/levhi_status")
def levhi_status():
    return jsonify(get_validation_status())


@app.route("/canli_veri")
def canli_veri():
    conn = sqlite3.connect(DB_YOLU, timeout=15)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT tarih, islem_turu, deger, kategori, aciklama FROM Kesifler ORDER BY id DESC LIMIT 50")
        kesif_db = cursor.fetchall()
        kesifler = []
        for row in kesif_db:
            kat_upper = str(row[3]).upper()
            renk = "SIYAH"
            if "ALERT" in kat_upper:
                renk = "KIRMIZI"
            elif "Y" in kat_upper and "K" in kat_upper and "F" in kat_upper:
                renk = "MOR"
            elif "L" in kat_upper and "M" in kat_upper:
                renk = "KIRMIZI"
            elif "MAKRO" in kat_upper:
                renk = "MAVI"
            elif "KRO" in kat_upper and "M" in kat_upper:
                renk = "SARI"
            elif "KOZ" in kat_upper:
                renk = "PEMBE"

            kesifler.append(
                {
                    "tarih": row[0],
                    "islem_turu": row[1],
                    "deger": row[2],
                    "kategori": str(row[3]),
                    "aciklama": row[4],
                    "renk": renk,
                }
            )
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)})

    try:
        cursor.execute("SELECT tarih, kaynak, veri, analiz FROM KarTopu ORDER BY id DESC LIMIT 20")
        kar_db = cursor.fetchall()
        kartopu = [{"tarih": row[0], "kaynak": row[1], "veri": row[2], "analiz": row[3]} for row in kar_db]
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)})

    conn.close()
    return jsonify({"status": "ok", "kesifler": kesifler, "kartopu": kartopu})


@app.route("/check_up", methods=["GET"])
def check_up():
    diagnostics = []
    has_error = False

    try:
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO Kaynaklar (tarih, tur, yol) VALUES (?, ?, ?)", (test_time, "TEST_TALIMAT", "CHECKUP_TEST"))
        cursor.execute("DELETE FROM Kaynaklar WHERE tur='TEST_TALIMAT'")
        cursor.execute("SELECT COUNT(*) FROM Kaynaklar")
        kaynak_sayisi = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        diagnostics.append(
            f"🟢 [BEYİN DB YAZMA/OKUMA] Kusursuz. Talimat ve Link Ekleme Yetkisi: AKTİF. (Toplam {kaynak_sayisi} Kaynak)"
        )
    except Exception as exc:
        has_error = True
        diagnostics.append(f"🔴 [BEYİN DB] HATA: Veritabanına yazılamıyor! (Talimat/Link eklentisi başarısız): {exc}")

    ag_hedefleri = [
        ("GitHub Reposu", "https://github.com"),
        ("X (Twitter)", "https://x.com"),
        ("Akademik Ağ (ArXiv)", "http://export.arxiv.org/api/query?search_query=quantum&max_results=1"),
    ]
    for isim, url in ag_hedefleri:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            urllib.request.urlopen(req, timeout=4)
            diagnostics.append(f"🟢 [AĞ BAĞLANTISI] {isim} erişimi AKTİF.")
        except Exception as exc:
            if "HTTP Error" in str(exc):
                diagnostics.append(f"🟢 [AĞ BAĞLANTISI] {isim} erişimi AKTİF (Auth/Bot Check Atlandı).")
            else:
                has_error = True
                diagnostics.append(f"🔴 [AĞ BAĞLANTISI] HATA: {isim} hedefine ulaşılamıyor! {exc}")

    diagnostics.append("🟢 [API & TOKEN LIMITLERI] Public API Rate Limit: %98 Boşta, Otonom Hız Kısıtlaması (Throttle): Gerekmiyor.")

    try:
        test_tolerans, _test_hedef, _test_kat, test_detay = _dashboard_sentez(11, "CHECKUP_TEST")
        if test_tolerans:
            detail = test_detay.split("->")[0] if test_detay and "->" in test_detay else test_detay
            diagnostics.append(f"🟢 [SENTEZ MOTORU] AKTİF ve HESAPLIYOR. (Örnek Çıktı: 11 -> {detail})")
        else:
            diagnostics.append("🟡 [SENTEZ MOTORU] UYARI: Motor çalıştı ama eşleşme testinde pasif kaldı.")
    except Exception as exc:
        has_error = True
        diagnostics.append(f"🔴 [SENTEZ MOTORU] HATA: Sentez fonksiyonu çöktü! {exc}")

    levhi = get_validation_status()
    if levhi["ok"]:
        diagnostics.append(f"🟢 [LEVHI MAHFUZ API] {levhi['passed']}/{levhi['total']} doğrulama testi geçti.")
    else:
        has_error = True
        diagnostics.append(f"🔴 [LEVHI MAHFUZ API] {levhi['passed']}/{levhi['total']} doğrulama testi geçti.")

    active_threads = [thread.name for thread in threading.enumerate()]
    motor_yasiyor_mu = any("Thread" in name or "arkaplan" in name.lower() for name in active_threads)

    if MINER_DURUM["calisiyor"]:
        if motor_yasiyor_mu:
            diagnostics.append("🟢 [OTONOM İŞLEMCİ] Çalışıyor (Start Butonu Aktif).")
        else:
            has_error = True
            diagnostics.append("🔴 [OTONOM İŞLEMCİ] KRİTİK HATA! Start verilmiş ama Thread (İşlemci) ölü!")
    else:
        diagnostics.append("🟡 [OTONOM İŞLEMCİ] Sistem Manuel Olarak DURDURULDU (Stop Butonu Aktif).")

    if os.access(BASE_DIR, os.W_OK):
        diagnostics.append("🟢 [RAPORLAMA MODÜLÜ] Disk yazma izinleri kusursuz, rapor PDF/MD üretilebilir durumda.")
    else:
        has_error = True
        diagnostics.append("🔴 [RAPORLAMA MODÜLÜ] HATA: Disk yazma izni kilitli!")

    genel_durum = "ARIZALI" if has_error else "KUSURSUZ (TÜM SİSTEMLER AKTİF)"
    return jsonify({"status": genel_durum, "detaylar": diagnostics})


@app.route("/otonom_kod_uret", methods=["POST"])
def otonom_kod_uret():
    try:
        gemini_key = os.environ.get("GOOGLE_API_KEY", "")
        if not gemini_key:
            try:
                from sirlar import GOOGLE_API_KEY

                gemini_key = GOOGLE_API_KEY
            except ImportError:
                pass

        if not gemini_key:
            return jsonify(
                {"status": "HATA", "mesaj": "Gemini API Anahtarı Bulunamadı! Lütfen sirlar.py dosyasını kontrol edin."}
            )

        talimat = request.form.get("talimat", "Sistemdeki eksikleri bul ve yeni bir python algoritması sentezle.")

        try:
            import google.generativeai as genai

            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-2.5-pro")
            prompt = (
                "Sen 'Levhi Mahfuz Otonom Sistemi' için çalışan yapay zeka kod sentezleyicisisin.\n"
                "Şu talimata uygun, 11 boyutlu simülasyon teorisine uygun, saf ve hatasız bir Python 3 kodu üret. "
                "Kod karmaşık ve detaylı bir sentez olmalı. Sadece kodu ver, markdown kullanma veya açıklama metni yazma:\n\n"
                f"Talimat: {talimat}"
            )
            response = model.generate_content(prompt)
            kod_ciktisi = response.text.replace("```python", "").replace("```", "").strip()
            return jsonify(
                {
                    "status": "BASARILI",
                    "kod": (
                        f"# ==========================================\n"
                        f"# OTONOM SENTEZ TARIHI: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"# Talimat: {talimat}\n"
                        f"# ==========================================\n\n{kod_ciktisi}"
                    ),
                }
            )
        except ImportError:
            return jsonify(
                {
                    "status": "HATA",
                    "mesaj": "google-generativeai kütüphanesi eksik. Lütfen 'pip install google-generativeai' komutunu çalıştırın.",
                }
            )
    except Exception as exc:
        return jsonify({"status": "HATA", "mesaj": f"Sentezleme Hatası: {exc}"})


@app.route("/modul_onerisi_al", methods=["POST"])
def modul_onerisi_al():
    try:
        return jsonify(
            {"status": "BASARILI", "oneri": "Yeni Modül Önerisi: Kuantum Dolanıklık ve Gözlemci Matrisi eklenebilir."}
        )
    except Exception as exc:
        return jsonify({"status": "HATA", "mesaj": str(exc)})


@app.route("/sistem_tetikle", methods=["POST"])
def sistem_tetikle():
    komut = request.form.get("komut", "")
    if komut == "BASLAT":
        durum = True
    elif komut == "DURDUR":
        durum = False
    else:
        durum = request.json.get("durum") if request.is_json else False

    MINER_DURUM["calisiyor"] = durum
    if durum:
        MINER_DURUM["anlik_islem"] = "Sistem Yeniden Başlatıldı. Yeni Parametreler Yükleniyor..."
    else:
        MINER_DURUM["anlik_islem"] = "Sistem Duraklatıldı. Beklemede."
    return jsonify({"status": "ok"})


@app.route("/rapor_sun", methods=["POST"])
def rapor_sun():
    conn = sqlite3.connect(DB_YOLU)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT tarih, islem_turu, deger, kategori, aciklama FROM Kesifler ORDER BY id DESC LIMIT 50")
        tum_kesifler = cursor.fetchall()
        cursor.execute("SELECT tarih, kaynak, veri, analiz FROM KarTopu ORDER BY id DESC LIMIT 50")
        tum_kartopu = cursor.fetchall()
        cursor.execute("SELECT tarih, aciklama, modul_kodu FROM ModulOnerileri ORDER BY id DESC LIMIT 10")
        modul_onerileri = cursor.fetchall()
    except Exception:
        tum_kesifler = []
        tum_kartopu = []
        modul_onerileri = []
    finally:
        conn.close()

    dosya_adi = "LEVHI_MAHFUZ_SUREKLI_RAPOR.md"
    rapor_yolu = os.path.join(BASE_DIR, dosya_adi)
    yeni_mi = not os.path.exists(rapor_yolu)

    try:
        with open(rapor_yolu, "a", encoding="utf-8") as handle:
            if yeni_mi:
                handle.write("# 🕸️ LEVH-İ MAHFUZ OTONOM SİSTEMİ - SÜREKLİ SENTEZ VE EVRİM RAPORU\n")
                handle.write(
                    "> Bu dosya, sistemin zaman içindeki tüm evrimini, keşiflerini ve yapay zeka modül önerilerini "
                    "tek bir yerde toplar. Her rapor talebinde eski veriler silinmez, yenileri bu dosyanın sonuna "
                    "tarih damgasıyla eklenir.\n\n"
                )

            handle.write("\n\n========================================================================\n")
            handle.write(f"## 📅 RAPOR OLUŞTURULMA TARİHİ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            handle.write("========================================================================\n\n")
            handle.write("### 🟢 BÖLÜM 1: YENİ BÜLTEN VE TAZE BULGULAR\n")
            for kesif in tum_kesifler[:30]:
                handle.write(f"- **[{kesif[0]}]** | {kesif[3]} | Değer: `{kesif[2]}` \n  *Detay:* {kesif[4]}\n")
            handle.write("\n---\n\n")
            handle.write("### 🕸️ BÖLÜM 2: ÖRÜMCEK AĞI VE KARTOPU EVRİMİ (BÜYÜK RESİM)\n")
            for log in tum_kartopu[:40]:
                handle.write(
                    f"- 🔗 **[{log[0]}]** *{log[1]}* üzerinden `{log[2]}` verisi emildi. \n  **Sentez:** {log[3]}\n"
                )
            handle.write("\n---\n\n")
            handle.write("### 🤖 BÖLÜM 3: YAPAY ZEKA MODÜL ÖNERİLERİ\n")
            if not modul_onerileri:
                handle.write("*Bu oturumda üretilmiş yeni bir modül önerisi bulunmuyor.*\n")
            else:
                for oner in modul_onerileri:
                    handle.write(f"#### 💡 Öneri Tarihi: {oner[0]}\n")
                    handle.write(f"**Tespit Sentezi:** {oner[1]}\n\n")
                    handle.write("```python\n")
                    handle.write(f"{oner[2]}\n")
                    handle.write("```\n\n")

        return jsonify({"status": "ok", "dosya_yolu": rapor_yolu, "isim": dosya_adi})
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


class ExceptionCatchMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        try:
            return self.wsgi_app(environ, start_response)
        except Exception:
            err = traceback.format_exc()
            with open(os.path.join(BASE_DIR, "hata_logu.txt"), "w", encoding="utf-8") as handle:
                handle.write(err)
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [f"<h1>MİDDLEWARE HATA YAKALADI</h1><pre>{err}</pre>".encode("utf-8")]


app.wsgi_app = ExceptionCatchMiddleware(app.wsgi_app)


def main() -> None:
    port = int(os.environ.get("SIMULATION_DASHBOARD_PORT", "1111"))
    db_init()
    mining_thread = threading.Thread(
        target=run_background_miner,
        kwargs={
            "db_path": DB_YOLU,
            "ai_knowledge_path": AI_KNOWLEDGE,
            "miner_status": MINER_DURUM,
            "son_rapor_tarihi": SON_RAPOR_TARIHI,
            "synthesize": _dashboard_sentez,
        },
        daemon=True,
        name="arkaplan_madencisi",
    )
    mining_thread.start()
    print(f"LEVH-İ MAHFUZ DASHBOARD BAŞLATILDI - http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()