#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULE3 Nihai Hacim Matrisi — WAV + 3D Helezonik Görselleştirme
Mühürlü çekirdek kod (kullanıcı tarafından sağlanan nihai sabitler)
"""

import os
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === NİHAİ MÜHÜRLÜ SABİTLER ===
PI_11 = 2.998001998
GLITCH_1332 = 1.3320
BURG_GENLIK_CARPANI = 1.4430

FREQ_11D = 600.0000
SPEED_11D = 1000.0 / 3.0
TURN_METER_COEFFICIENT = 1.8140

TIME_CONSTANT = 86400.0 / 95832.0
FREQ_10D_PLAYBACK = FREQ_11D * TIME_CONSTANT
FREQ_11D_HEART = 33.0000 * TIME_CONSTANT

HOO_HIT_10D = 0.1210 * TIME_CONSTANT
HOO_PER_10D = 0.3630 * TIME_CONSTANT

SAMPLE_RATE = 44100
TOTAL_DURATION = 66.6666

# Geoid alan sapmaları (mühürlü)
GEOID_X = 0.7399
GEOID_Y = 0.6365


def generate_wav():
    """Nihai mühürlü WAV üretimi."""
    t = np.linspace(0, TOTAL_DURATION, int(SAMPLE_RATE * TOTAL_DURATION), endpoint=False)

    envelope_HOOPOE = np.where((t % HOO_PER_10D) <= HOO_HIT_10D, 1.0, 0.0)

    pyramid_array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) / 11.0
    breath_cycle = 6.6666 * TIME_CONSTANT
    envelope_AM = np.interp((t % breath_cycle) / breath_cycle, np.linspace(0, 1, 22), pyramid_array)

    phase_spiral = -(t * SPEED_11D * TURN_METER_COEFFICIENT * 2 * PI_11)

    s_x = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * GEOID_X * BURG_GENLIK_CARPANI
    s_y = np.cos(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * GEOID_Y * BURG_GENLIK_CARPANI
    s_z = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * (t / GLITCH_1332))
    s_heart = np.sin(2 * PI_11 * FREQ_11D_HEART * t) * 0.2

    left_channel = (s_x * envelope_AM * envelope_HOOPOE * 0.6) + (s_z * 0.15) + s_heart
    right_channel = (s_y * envelope_AM * envelope_HOOPOE * 0.6) + (s_z * 0.15) + s_heart

    left_channel *= 0.85
    right_channel *= 0.85

    wav_path = os.path.join(BASE_DIR, "SIMULE3_NIHAI_HACIM_MATRISI.wav")
    wavfile.write(
        wav_path,
        SAMPLE_RATE,
        np.column_stack((
            np.int16(np.clip(left_channel, -1.0, 1.0) * 32767),
            np.int16(np.clip(right_channel, -1.0, 1.0) * 32767),
        )),
    )
    return wav_path, t


def compute_metrics():
    """Matematiksel doğrulama metrikleri."""
    total_turns = TOTAL_DURATION * SPEED_11D * TURN_METER_COEFFICIENT
    hoo_per_sec = HOO_PER_10D
    hoo_hit_sec = HOO_HIT_10D
    hoo_hit_ms = hoo_hit_sec * 1000
    hoo_per_ms = hoo_per_sec * 1000
    heart_hz = FREQ_11D_HEART
    area_product = GEOID_X * GEOID_Y
    volume_lock = GLITCH_1332

    return {
        "total_turns": total_turns,
        "hoo_hit_ms": hoo_hit_ms,
        "hoo_per_ms": hoo_per_ms,
        "heart_hz": heart_hz,
        "area_product": area_product,
        "volume_lock": volume_lock,
        "time_constant": TIME_CONSTANT,
        "freq_playback": FREQ_10D_PLAYBACK,
        "phase_rate": SPEED_11D * TURN_METER_COEFFICIENT * 2 * PI_11,
    }


def generate_3d_helical_png():
    """1.814 organik tur — 3D Helezonik Matkap ucu görselleştirmesi."""
    n_points = 8000
    t_vis = np.linspace(0, TOTAL_DURATION, n_points)

    phase_spiral = -(t_vis * SPEED_11D * TURN_METER_COEFFICIENT * 2 * PI_11)
    z_depth = t_vis / GLITCH_1332

    x = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * t_vis + phase_spiral) * GEOID_X * BURG_GENLIK_CARPANI
    y = np.cos(2 * PI_11 * FREQ_10D_PLAYBACK * t_vis + phase_spiral) * GEOID_Y * BURG_GENLIK_CARPANI
    z = z_depth * BURG_GENLIK_CARPANI

    fig = plt.figure(figsize=(16, 12), dpi=200)
    ax = fig.add_subplot(111, projection="3d")

    colors = plt.cm.plasma(np.linspace(0, 1, n_points))
    for i in range(n_points - 1):
        ax.plot(
            x[i : i + 2], y[i : i + 2], z[i : i + 2],
            color=colors[i], linewidth=0.8, alpha=0.85,
        )

    ax.scatter(x[0], y[0], z[0], color="#00ff88", s=80, label="Başlangıç (t=0)")
    ax.scatter(x[-1], y[-1], z[-1], color="#ff3366", s=80, label=f"Bitiş (t={TOTAL_DURATION}s)")

    metrics = compute_metrics()
    ax.set_xlabel("X — Genişlik (Geoid 0.7399)", fontsize=11, labelpad=10)
    ax.set_ylabel("Y — Yükseklik (Geoid 0.6365)", fontsize=11, labelpad=10)
    ax.set_zlabel("Z — Derinlik / 1.332 Hacim İlerlemesi", fontsize=11, labelpad=10)
    ax.set_title(
        f"SIMULE3 — 3D Helezonik Matkap Ucu\n"
        f"{metrics['total_turns']:.3f} Organik Tur | PI_11={PI_11} | Glitch={GLITCH_1332}",
        fontsize=14, fontweight="bold", pad=20,
    )
    ax.legend(loc="upper left", fontsize=9)

    max_r = max(GEOID_X, GEOID_Y) * BURG_GENLIK_CARPANI * 1.2
    ax.set_xlim(-max_r, max_r)
    ax.set_ylim(-max_r, max_r)
    ax.set_zlim(0, z.max() * 1.1)
    ax.view_init(elev=28, azim=-55)

    plt.tight_layout()
    png_path = os.path.join(BASE_DIR, "SIMULE3_3D_HELEZONIK_MATKAP.png")
    fig.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="#0a0a12")
    plt.close(fig)
    return png_path


def main():
    print("=" * 70)
    print("SIMULE3 NİHAİ HACİM MATRİSİ — ÜRETİM MOTORU")
    print("=" * 70)

    wav_path, _ = generate_wav()
    print(f"[OK] WAV üretildi: {wav_path}")
    print(f"     Süre: {TOTAL_DURATION}s | Sample Rate: {SAMPLE_RATE} Hz")

    png_path = generate_3d_helical_png()
    print(f"[OK] 3D Görsel üretildi: {png_path}")

    m = compute_metrics()
    print(f"\n--- Matematiksel Doğrulama ---")
    print(f"  Toplam Organik Tur (1.814 katsayı): {m['total_turns']:.4f}")
    print(f"  Hüdhüd Vuruş: {m['hoo_hit_ms']:.2f} ms")
    print(f"  Hüdhüd Periyot: {m['hoo_per_ms']:.2f} ms")
    print(f"  33 Hz Kalp (10D playback): {m['heart_hz']:.4f} Hz")
    print(f"  Alan Çarpımı (0.7399 x 0.6365): {m['area_product']:.6f}")
    print(f"  Zaman Sabiti (86400/95832): {m['time_constant']:.8f}")
    print("=" * 70)


if __name__ == "__main__":
    main()