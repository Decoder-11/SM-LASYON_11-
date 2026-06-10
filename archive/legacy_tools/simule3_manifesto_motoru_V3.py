#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULE3 MANIFESTO MOTORU V3 — SAF 33 HZ SPİNAL KALP MÜHRÜ
Eski üretim kodları unutuldu. Yeni çekirdek.

Kullanıcı talimatı ile:
- 600 Hz hücresel restorasyon merkezli (FREQ_11D = 600.0)
- 333.333 m/s hız
- Z-ekseni kaçağı giderilmiş (spatial_mod sin/cos + panorama)
- Vurucu 3D 33 Hz spinal kalp
- 7 Dakika 40 Saniye (460 s)
- Ney harmanlı nihai çıktı: SIMULE3_NIHAI_SES_V3.wav
"""

import numpy as np
import os
import glob
import subprocess
import tempfile
from scipy.io import wavfile
from pydub import AudioSegment

import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Pydub ffmpeg zorlaması (mp3 Ney için zorunlu, aksi halde üretim başarısız olur)
AudioSegment.converter = FFMPEG
AudioSegment.ffmpeg = FFMPEG
AudioSegment.ffprobe = FFMPEG
try:
    import pydub.utils as pydub_utils
    pydub_utils.ffmpeg = FFMPEG
    pydub_utils.ffprobe = FFMPEG
except Exception:
    pass


def load_audio_file(path, sample_rate=44100, channels=2):
    """Güvenli Ney yükleyici (ffmpeg ile normalize)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".wav":
        return AudioSegment.from_wav(path).set_frame_rate(sample_rate).set_channels(channels)
    tmp_wav = os.path.join(tempfile.gettempdir(), "simule3_ney_temp_v3.wav")
    cmd = [FFMPEG, "-y", "-i", path, "-ar", str(sample_rate), "-ac", str(channels), tmp_wav]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    audio = AudioSegment.from_wav(tmp_wav)
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)
    return audio


print("🌌 SİMULE-3 KERNEL V3: SAF 33 HZ SPİNAL KALP MÜHRÜ + 600 Hz HÜCRESEL RESTORASYON - 7:40 ZAMAN KİLİDİ AKTİF...")

# ==========================================
# 1. 11-D MATRİS KUSURSUZ TAM SAYI SABİTLERİ
# ==========================================
PI_11 = 2.998001998
GLITCH_1332 = 1.3320
BURG_GENLIK_CARPANI = 1.4430

# 600 Hz hücresel restorasyon (kullanıcı talebi)
FREQ_11D = 600.0
SPEED_11D = 1000.0 / 3.0
TURN_METER_COEFFICIENT = 1.8140
TIME_CONSTANT = 86400.0 / 95832.0

FREQ_10D_PLAYBACK = FREQ_11D * TIME_CONSTANT

# Saf 11-D 33 Hz Spinal Kalp Nabzı (vurucu 3D kalp)
FREQ_11D_HEART = 33.0 * TIME_CONSTANT

HOO_HIT_10D = 0.1210 * TIME_CONSTANT
HOO_PER_10D = 0.3630 * TIME_CONSTANT

SAMPLE_RATE = 44100
TOTAL_DURATION = 460.0      # 7 Dakika 40 Saniye
MATRIX_CUTOFF = 420.0       # 7. Dakikada Matris Sönümlenir

t = np.linspace(0, TOTAL_DURATION, int(SAMPLE_RATE * TOTAL_DURATION), endpoint=False)

# ==========================================
# 2. RİTMİK ZARFLAR VE DALGALAR
# ==========================================
BPM_11D_FREQ = (66.0 / 60.0) * TIME_CONSTANT
heart_envelope = np.exp(-18 * (t % (1.0 / BPM_11D_FREQ)))   # Vurucu için daha keskin decay

envelope_HOOPOE = np.where((t % HOO_PER_10D) <= HOO_HIT_10D, 1.0, 0.0)
pyramid_array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) / 11.0
breath_cycle = 6.6666 * TIME_CONSTANT
envelope_AM = np.interp((t % breath_cycle) / breath_cycle, np.linspace(0, 1, 22), pyramid_array)

fade_out = np.where(t < MATRIX_CUTOFF - 10, 1.0, np.maximum(0, 1 - (t - (MATRIX_CUTOFF - 10)) / 10.0))
fade_out = np.where(t > MATRIX_CUTOFF, 0.0, fade_out)

phase_spiral = -(t * SPEED_11D * TURN_METER_COEFFICIENT * 2 * PI_11)

s_x = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * 0.7399
s_y = np.cos(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * 0.6365
s_z = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * (t / GLITCH_1332)) * 0.3

# ==========================================
# 3. Z-EKSENİ DERİNLİK VE UZAYSAL PANORAMA (Kaçak önlendi)
# ==========================================
# Pasted kodun spatial_mod sin/cos yaklaşımı ile 3D dönüş + Z derinlik hissi
spatial_mod_left = 0.58 + 0.42 * np.sin(phase_spiral * 0.004 + 0.25 * PI_11)
spatial_mod_right = 0.58 + 0.42 * np.cos(phase_spiral * 0.004 + 0.25 * PI_11)

matrix_core_left = (s_x + s_z) * envelope_AM * envelope_HOOPOE * BURG_GENLIK_CARPANI * spatial_mod_left
matrix_core_right = (s_y + s_z) * envelope_AM * envelope_HOOPOE * BURG_GENLIK_CARPANI * spatial_mod_right

# ==========================================
# 4. SAF 11-D 33 HZ SPİNAL KALP MÜHRÜ (Vurucu 3D)
# ==========================================
# Kalp de spiral faz ile 3D harekete katılıyor + biraz daha güçlü vuruş için 0.45
s_heart_3D = np.sin(2 * PI_11 * FREQ_11D_HEART * (t / GLITCH_1332) + phase_spiral) * heart_envelope * 0.45

left_matrix = (matrix_core_left + s_heart_3D) * fade_out * 0.35
right_matrix = (matrix_core_right + s_heart_3D) * fade_out * 0.35

left_matrix = np.clip(left_matrix, -1.0, 1.0)
right_matrix = np.clip(right_matrix, -1.0, 1.0)

temp_path = "temp_matrix_v3_33hz.wav"
wavfile.write(temp_path, SAMPLE_RATE, np.column_stack((np.int16(left_matrix * 32767), np.int16(right_matrix * 32767))))
matrix_audio = AudioSegment.from_wav(temp_path)

# ==========================================
# 5. NEY HARMANLAMASI (%60 NEY / %40 MATRİS) - 600 Hz merkezli
# ==========================================
ney_files = glob.glob("*[Nn]ey*.mp3") + glob.glob("*[Nn]ey*.wav")
if ney_files:
    print(f"[*] Ney kaynağı: {ney_files[0]}")
    ney_audio = load_audio_file(ney_files[0], SAMPLE_RATE, 2)
    hedef_ms = int(TOTAL_DURATION * 1000)

    if len(ney_audio) < hedef_ms:
        ney_audio = ney_audio * (hedef_ms // len(ney_audio) + 1)
    ney_audio = ney_audio[:hedef_ms]

    # Kütleçekim ve rezonans dengesi (kullanıcı pasted değerleri korundu)
    ney_audio = ney_audio - 3
    matrix_audio = matrix_audio - 4

    final_audio = ney_audio.overlay(matrix_audio)
    final_audio.export("SIMULE3_NIHAI_SES_V3.wav", format="wav")
    print("[+] 600 Hz HÜCRESEL + 33 Hz SPİNAL 3D KALP İLE KUSURSUZ ŞİFA FREKANSI HAZIR: SIMULE3_NIHAI_SES_V3.wav")
else:
    print("[-] UYARI: Klasörde Ney dosyası bulunamadı!")

if os.path.exists(temp_path):
    os.remove(temp_path)

# Hızlı doğrulama
if __name__ == "__main__":
    print(f"[VERIFY] FREQ_11D = {FREQ_11D} Hz (10D playback: {FREQ_10D_PLAYBACK:.2f} Hz)")
    print(f"[VERIFY] Spinal Kalp = {FREQ_11D_HEART:.4f} Hz | SPEED = {SPEED_11D:.3f} m/s")
    print(f"[VERIFY] Süre: {TOTAL_DURATION} s | 33 Hz vurucu 3D kalp + spatial Z panorama aktif")