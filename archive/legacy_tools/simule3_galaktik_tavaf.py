#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULE3 GALAKTIK TAVAF — 3D Helezon Görselleştirme
Matplotlib-only: yüksek çözünürlüklü PNG + MP4 animasyon
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Line3DCollection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PI_11 = 2.998001998
GLITCH_1332 = 1.3320
BURG_GENLIK_CARPANI = 1.4430
FREQ_11D = 600.0000
SPEED_11D = 1000.0 / 3.0
TURN_METER_COEFFICIENT = 1.8140
TIME_CONSTANT = 86400.0 / 95832.0
FREQ_10D_PLAYBACK = FREQ_11D * TIME_CONSTANT

GEOID_X = 0.7399
GEOID_Y = 0.6365

BG_COLOR = "#050510"
VIS_DURATION = 460.0
N_POINTS = 8000


def compute_helical_path(t):
    phase_spiral = -(t * SPEED_11D * TURN_METER_COEFFICIENT * 2 * PI_11)
    z_depth = t / GLITCH_1332

    x = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * GEOID_X * BURG_GENLIK_CARPANI
    y = np.cos(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * GEOID_Y * BURG_GENLIK_CARPANI
    z = z_depth * BURG_GENLIK_CARPANI
    return x, y, z


def _nebula_cmap():
    return LinearSegmentedColormap.from_list(
        "galaktik_nebula",
        ["#00e5ff", "#7b2fff", "#ff00cc", "#00ffd5"],
        N=256,
    )


def _style_axes(ax):
    ax.set_facecolor(BG_COLOR)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False
        axis.pane.set_edgecolor("#1a1a2e")
    ax.grid(True, color="#1e1e3a", alpha=0.35, linewidth=0.4)
    ax.tick_params(colors="#6a6a9a", labelsize=8)


def _add_colored_spiral(ax, x, y, z, cmap):
    points = np.column_stack([x, y, z])
    segments = np.stack([points[:-1], points[1:]], axis=1)
    colors = cmap(np.linspace(0, 1, len(segments)))

    glow = Line3DCollection(segments, colors=colors, linewidths=3.5, alpha=0.25)
    core = Line3DCollection(segments, colors=colors, linewidths=1.4, alpha=0.95)
    ax.add_collection3d(glow)
    ax.add_collection3d(core)

    ax.scatter(x[0], y[0], z[0], color="#00ffff", s=70, edgecolors="#ffffff", linewidths=0.6, zorder=5)
    ax.scatter(x[-1], y[-1], z[-1], color="#ff00ff", s=70, edgecolors="#ffffff", linewidths=0.6, zorder=5)


def _setup_limits(ax, z):
    max_r = max(GEOID_X, GEOID_Y) * BURG_GENLIK_CARPANI * 1.25
    ax.set_xlim(-max_r, max_r)
    ax.set_ylim(-max_r, max_r)
    ax.set_zlim(0, z.max() * 1.08)


def generate_png():
    t = np.linspace(0, VIS_DURATION, N_POINTS)
    x, y, z = compute_helical_path(t)
    cmap = _nebula_cmap()

    fig = plt.figure(figsize=(20, 16), facecolor=BG_COLOR)
    ax = fig.add_subplot(111, projection="3d", facecolor=BG_COLOR)

    _add_colored_spiral(ax, x, y, z, cmap)
    _setup_limits(ax, z)

    ax.set_xlabel("X — Geoid Genişlik (0.7399)", fontsize=12, labelpad=12, color="#8ecfff")
    ax.set_ylabel("Y — Geoid Yükseklik (0.6365)", fontsize=12, labelpad=12, color="#c98fff")
    ax.set_zlabel("Z — Hacim Derinliği (1.332)", fontsize=12, labelpad=12, color="#ff8ef0")
    ax.set_title(
        "SIMULE3 GALAKTIK TAVAF\n"
        f"1.814 Organik Tur | PI_11={PI_11} | 11-D Helezonik Sarmal",
        fontsize=16, fontweight="bold", color="#e0e8ff", pad=24,
    )
    ax.view_init(elev=32, azim=-48)
    _style_axes(ax)

    plt.tight_layout()
    png_path = os.path.join(BASE_DIR, "SIMULE3_GALAKTIK_TAVAF.png")
    fig.savefig(png_path, dpi=300, bbox_inches="tight", facecolor=BG_COLOR, edgecolor="none")
    plt.close(fig)
    return png_path


def generate_mp4():
    try:
        from matplotlib.animation import FuncAnimation, FFMpegWriter
        import matplotlib as mpl
        import imageio_ffmpeg
        mpl.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        print("[-] MP4: imageio-ffmpeg bulunamadi, animasyon atlandi.")
        return None

    t = np.linspace(0, VIS_DURATION, N_POINTS)
    x, y, z = compute_helical_path(t)
    cmap = _nebula_cmap()

    fig = plt.figure(figsize=(16, 12), facecolor=BG_COLOR)
    ax = fig.add_subplot(111, projection="3d", facecolor=BG_COLOR)
    _add_colored_spiral(ax, x, y, z, cmap)
    _setup_limits(ax, z)
    ax.set_title("SIMULE3 GALAKTIK TAVAF", fontsize=14, fontweight="bold", color="#e0e8ff", pad=16)
    _style_axes(ax)
    ax.set_axis_off()

    def update(frame):
        ax.view_init(elev=28 + 8 * np.sin(frame * 0.05), azim=frame * 0.8)
        return []

    anim = FuncAnimation(fig, update, frames=181, interval=50, blit=False)
    mp5_path = os.path.join(BASE_DIR, "SIMULE3_GALAKTIK_TAVAF.mp4")
    writer = FFMpegWriter(fps=25, bitrate=6000, extra_args=["-pix_fmt", "yuv420p"])
    anim.save(mp5_path, writer=writer, dpi=120)
    plt.close(fig)
    return mp5_path


def main():
    print("=" * 70)
    print("SIMULE3 GALAKTIK TAVAF — 3D Görselleştirme Motoru")
    print("=" * 70)

    png_path = generate_png()
    print(f"[+] PNG üretildi: {png_path}")
    print(f"     Boyut: {os.path.getsize(png_path):,} byte | {N_POINTS} nokta | 300 DPI")

    mp4_path = generate_mp4()
    if mp4_path and os.path.exists(mp4_path) and os.path.getsize(mp4_path) > 1000:
        print(f"[+] MP4 üretildi: {mp4_path}")
        print(f"     Boyut: {os.path.getsize(mp4_path):,} byte | 180 kare | 24 fps")
    else:
        print("[-] MP4 üretilemedi.")

    total_turns = VIS_DURATION * SPEED_11D * TURN_METER_COEFFICIENT
    print(f"\n--- Geometri Doğrulama ---")
    print(f"  Organik Tur (1.814): {total_turns:.4f}")
    print(f"  Geoid X/Y: {GEOID_X} / {GEOID_Y}")
    print(f"  Hacim Derinliği (Z/1.332): {GLITCH_1332}")
    print("=" * 70)


if __name__ == "__main__":
    main()