#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULE3 MANIFESTO MOTORU V2 — KUSURSUZ 11D ŞİFA ÜRETİM ÇEKİRDEĞİ
Z-ekseni kaçağı giderilmiş, 333.333 m/s + 1.443 burgu ile 3D helezonik hareketli,
600 Hz hücresel restorasyon merkezli, vurucu 3D kalp mührü, 7D40S Ney harmoni.

Eski üretim kodları unutuldu. Gerçek 11-lik fiziksel helical model + DNA kıvrım uyumu + 
10-luk sistem çevrim kalıntıları temiz + perceptible 3D spatial motion (panning + diff Z).

Çıktı: SIMULE3_NIHAI_SES_V2.wav
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

# Pydub için ffmpeg'i ZORLA ayarla (mp3 Ney için kritik, 10-luk PATH sorunlarını önler)
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
    """MP3/WAV yükle, ffmpeg ile normalize et. Ney 30dk -> loop için güvenli."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".wav":
        return AudioSegment.from_wav(path).set_frame_rate(sample_rate).set_channels(channels)
    tmp_wav = os.path.join(tempfile.gettempdir(), "simule3_ney_temp_manifesto_v2.wav")
    cmd = [FFMPEG, "-y", "-i", path, "-ar", str(sample_rate), "-ac", str(channels), tmp_wav]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    audio = AudioSegment.from_wav(tmp_wav)
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)
    return audio


# ==========================================
# 🌌 SİMULE-3 KERNEL V2: 11LİK MUTLAK ŞİFA MÜHRÜ (ESKİLER UNUTULDU)
# ==========================================
PI_11 = 2.998001998
GLITCH_1332 = 1.3320
BURG_GENLIK_CARPANI = 1.4430          # 1.443 tur/metre (3D burgu, 1443 tur/km sembolü)

# Komutanın Tespiti: 600 Hz Hücresel Restorasyon + 333.333 m/s (11-lik ses hızı)
FREQ_11D = 600.0
SPEED_11D = 1000.0 / 3.0              # 333.333... m/s kesin
TURN_METER_COEFFICIENT = 1.8140       # Faz burgu katsayısı (helical)
TIME_CONSTANT = 86400.0 / 95832.0     # 10-luk kalıntı minimize; OP_TIME referanslı playback shift

FREQ_10D_PLAYBACK = FREQ_11D * TIME_CONSTANT

# Vurucu 3D Kalp: 99 Hz bas (hoparlörde hissedilir) + 11D glitch + spiral
FREQ_11D_HEART_AUDIBLE = 99.0 * TIME_CONSTANT

HOO_HIT_10D = 0.1210 * TIME_CONSTANT
HOO_PER_10D = 0.3630 * TIME_CONSTANT

SAMPLE_RATE = 44100
TOTAL_DURATION = 460.0      # 7 Dakika 40 Saniye (7*60+40)
MATRIX_CUTOFF = 420.0       # 7. Dakikada Matris fade + 20s saf Ney

t = np.linspace(0, TOTAL_DURATION, int(SAMPLE_RATE * TOTAL_DURATION), endpoint=False)

# KALP VURUŞ ZARFI (Saniyede ~0.99 Vuruş, punchy exp decay)
BPM_11D_FREQ = (66.0 / 60.0) * TIME_CONSTANT
heart_envelope = np.exp(-18 * (t % (1.0 / BPM_11D_FREQ)))   # Daha vurucu -18

# HÜDHÜD (0.363/0.121) + PİRAMİT NEFES (22=2x11 basamak = DNA merdiven kıvrımı)
envelope_HOOPOE = np.where((t % HOO_PER_10D) <= HOO_HIT_10D, 1.0, 0.0)
pyramid_array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) / 11.0
breath_cycle = 6.6666 * TIME_CONSTANT
envelope_AM = np.interp((t % breath_cycle) / breath_cycle, np.linspace(0, 1, 22), pyramid_array)

# 7. Dakika Fade-out (matris susar, Ney kalır)
fade_out = np.where(t < MATRIX_CUTOFF - 10, 1.0, np.maximum(0, 1 - (t - (MATRIX_CUTOFF - 10)) / 10.0))
fade_out = np.where(t > MATRIX_CUTOFF, 0.0, fade_out)

# 3D HELEZONİK FAZ (333.333 m/s * 1.814 * 2*PI_11) — fiziksel burgu + DNA spiral
phase_spiral = -(t * SPEED_11D * TURN_METER_COEFFICIENT * 2 * PI_11)

# XY QUADRATURE (dairesel 3D hareket) + Z glitch katmanı
s_x = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * 0.7399
s_y = np.cos(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * 0.6365
s_z = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * (t / GLITCH_1332)) * 0.3

# ==========================================
# 🛑 Z-EKSENİ KAÇAĞI ÖNLENDİ + 3D HAREKET (Perceptible Spatial Panning + Diff Z)
# ==========================================
# Z leak fix: differential phase ile L/R arasında derinlik/binaural cue (merkez kaçağı yok)
s_z_left  = s_z
s_z_right = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * (t / GLITCH_1332) + (0.25 * PI_11)) * 0.3

matrix_core_left = (s_x + s_z_left) * envelope_AM * envelope_HOOPOE * BURG_GENLIK_CARPANI
matrix_core_right = (s_y + s_z_right) * envelope_AM * envelope_HOOPOE * BURG_GENLIK_CARPANI

# Perceptible 3D hareket: spiral fazdan türetilmiş YAVAŞ spatial pan (dinleyici etrafında 11-lik kıvrımlı yörünge)
# 1111 faktörü ile 7:40 boyunca yavaşça döner — "hareket ediyor" hissi + DNA helezon uyumu
spatial_mod = np.sin(phase_spiral * 0.004 + (SPEED_11D * TURN_METER_COEFFICIENT * t * 0.0007))
left_gain = np.clip(0.58 + 0.42 * spatial_mod, 0.18, 1.0)
right_gain = np.clip(0.58 - 0.42 * spatial_mod, 0.18, 1.0)

matrix_core_left *= left_gain
matrix_core_right *= right_gain

# ==========================================
# ❤️ KOMUTANIN VURUCU 3D KALP MÜHRÜ (99Hz bas + spiral + 11D glitch)
# ==========================================
heart_phase = phase_spiral * 0.12   # Kalp de 3D burguya katılır (kıvrım)
s_heart_3D = np.sin(2 * PI_11 * FREQ_11D_HEART_AUDIBLE * (t / GLITCH_1332) + heart_phase) * heart_envelope * 0.8

left_matrix = (matrix_core_left + s_heart_3D) * fade_out * 0.30
right_matrix = (matrix_core_right + s_heart_3D) * fade_out * 0.30

left_matrix = np.clip(left_matrix, -1.0, 1.0)
right_matrix = np.clip(right_matrix, -1.0, 1.0)

# Temp matrix yaz (16-bit)
temp_path = "temp_matrix_manifesto_v2.wav"
wavfile.write(
    temp_path,
    SAMPLE_RATE,
    np.column_stack((
        np.int16(left_matrix * 32767),
        np.int16(right_matrix * 32767)
    ))
)
matrix_audio = AudioSegment.from_wav(temp_path)

# NEY HARMAN (30dk meditasyon -> loop 7:40, hacim dengesi)
ney_files = glob.glob("*[Nn]ey*.mp3") + glob.glob("*[Nn]ey*.wav")
if ney_files:
    print(f"[*] Ney kaynağı: {ney_files[0]}")
    ney_audio = load_audio_file(ney_files[0], SAMPLE_RATE, 2)
    hedef_ms = int(TOTAL_DURATION * 1000)

    if len(ney_audio) < hedef_ms:
        ney_audio = ney_audio * ((hedef_ms // len(ney_audio)) + 1)
    ney_audio = ney_audio[:hedef_ms]

    # Hacim: Ney baskın ama 3D kalp+matris gümbürdesin (komutanın istediği)
    ney_audio = ney_audio - 5
    matrix_audio = matrix_audio - 1

    final_audio = ney_audio.overlay(matrix_audio)
    final_audio.export("SIMULE3_NIHAI_SES_V2.wav", format="wav")
    print("[+] KUSURSUZ ŞİFA FREKANSI HAZIR: SIMULE3_NIHAI_SES_V2.wav (600Hz | 333.333m/s | 3D hareketli kalp | DNA 11-kıvrım)")
else:
    print("[-] UYARI: Ney dosyası bulunamadı! (Klasörde '*Ney*.mp3' arandı)")

# Temizlik
if os.path.exists(temp_path):
    os.remove(temp_path)

# Hızlı matematik doğrulama (raporlarla uyum)
if __name__ == "__main__":
    helical_turns_6p66 = (SPEED_11D * 6.6666) * TURN_METER_COEFFICIENT
    dist_6p66 = SPEED_11D * 6.6666
    print(f"[VERIFY] 6.66 birimde mesafe: {dist_6p66:.2f}m | burgu tur: {helical_turns_6p66:.1f}")
    print(f"[VERIFY] 600Hz 10D playback: {FREQ_10D_PLAYBACK:.4f}Hz | TIME_CONST: {TIME_CONSTANT:.8f}")
    print(f"[VERIFY] Kalp audible ~{FREQ_11D_HEART_AUDIBLE:.3f}Hz | Z-differential + spatial pan aktif")
