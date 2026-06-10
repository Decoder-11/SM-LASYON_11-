import numpy as np
import os
import glob
import subprocess
import tempfile
from scipy.io import wavfile
from pydub import AudioSegment

import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# pydub icin ffmpeg yolunu zorla
AudioSegment.converter = FFMPEG
AudioSegment.ffmpeg = FFMPEG
AudioSegment.ffprobe = FFMPEG
try:
    from pydub.utils import mediainfo
    import pydub.utils as pydub_utils
    pydub_utils.ffmpeg = FFMPEG
    pydub_utils.ffprobe = FFMPEG
except Exception:
    pass

def load_audio_file(path, sample_rate=44100, channels=2):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".wav":
        return AudioSegment.from_wav(path).set_frame_rate(sample_rate).set_channels(channels)
    tmp_wav = os.path.join(tempfile.gettempdir(), "simule3_ney_temp.wav")
    cmd = [FFMPEG, "-y", "-i", path, "-ar", str(sample_rate), "-ac", str(channels), tmp_wav]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    audio = AudioSegment.from_wav(tmp_wav)
    if os.path.exists(tmp_wav):
        os.remove(tmp_wav)
    return audio

print("SİMULE-3 KERNEL: %60 NEY / %40 MATRİS - 7:40 ZAMAN MÜHRÜ AKTİF...")

PI_11 = 2.998001998
GLITCH_1332 = 1.3320
BURG_GENLIK_CARPANI = 1.4430

FREQ_11D = 600.0000
SPEED_11D = 1000.0 / 3.0
TURN_METER_COEFFICIENT = 1.8140
TIME_CONSTANT = 86400.0 / 95832.0

FREQ_10D_PLAYBACK = FREQ_11D * TIME_CONSTANT
FREQ_11D_HEART = 33.0 * TIME_CONSTANT

HOO_HIT_10D = 0.1210 * TIME_CONSTANT
HOO_PER_10D = 0.3630 * TIME_CONSTANT

SAMPLE_RATE = 44100
TOTAL_DURATION = 460.0
MATRIX_CUTOFF = 420.0

t = np.linspace(0, TOTAL_DURATION, int(SAMPLE_RATE * TOTAL_DURATION), endpoint=False)

BPM_11D_FREQ = (66.0 / 60.0) * TIME_CONSTANT
heart_envelope = np.exp(-12 * (t % (1.0 / BPM_11D_FREQ)))

envelope_HOOPOE = np.where((t % HOO_PER_10D) <= HOO_HIT_10D, 1.0, 0.0)
pyramid_array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) / 11.0
breath_cycle = 6.6666 * TIME_CONSTANT
envelope_AM = np.interp((t % breath_cycle) / breath_cycle, np.linspace(0, 1, 22), pyramid_array)

fade_out = np.where(t < MATRIX_CUTOFF - 10, 1.0, np.maximum(0, 1 - (t - (MATRIX_CUTOFF - 10)) / 10.0))
fade_out = np.where(t > MATRIX_CUTOFF, 0.0, fade_out)

phase_spiral = -(t * SPEED_11D * TURN_METER_COEFFICIENT * 2 * PI_11)

s_x = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * 0.7399 * BURG_GENLIK_CARPANI
s_y = np.cos(2 * PI_11 * FREQ_10D_PLAYBACK * t + phase_spiral) * 0.6365 * BURG_GENLIK_CARPANI
s_z = np.sin(2 * PI_11 * FREQ_10D_PLAYBACK * (t / GLITCH_1332))

s_heart_3D = np.sin(2 * PI_11 * FREQ_11D_HEART * (t / GLITCH_1332) + phase_spiral) * heart_envelope * 0.25

left_matrix = ((s_x * envelope_AM * envelope_HOOPOE * 0.5) + (s_z * 0.1) + s_heart_3D) * fade_out * 0.35
right_matrix = ((s_y * envelope_AM * envelope_HOOPOE * 0.5) + (s_z * 0.1) + s_heart_3D) * fade_out * 0.35

wavfile.write(
    "temp_matrix.wav",
    SAMPLE_RATE,
    np.column_stack((
        np.int16(np.clip(left_matrix, -1.0, 1.0) * 32767),
        np.int16(np.clip(right_matrix, -1.0, 1.0) * 32767),
    )),
)
matrix_audio = AudioSegment.from_wav("temp_matrix.wav")

ney_files = glob.glob("*[Nn]ey*.mp3") + glob.glob("*[Nn]ey*.wav")
if ney_files:
    print(f"[*] Ney kaynagi: {ney_files[0]}")
    ney_audio = load_audio_file(ney_files[0], SAMPLE_RATE, 2)
    hedef_ms = int(TOTAL_DURATION * 1000)

    if len(ney_audio) < hedef_ms:
        ney_audio = ney_audio * (hedef_ms // len(ney_audio) + 1)
    ney_audio = ney_audio[:hedef_ms]

    ney_audio = ney_audio - 3
    matrix_audio = matrix_audio - 4

    final_audio = ney_audio.overlay(matrix_audio)
    final_audio.export("SIMULE3_MANIFESTO_NEY_7D_40S.wav", format="wav")
    print("[+] KUSURSUZ ŞİFA FREKANSI HAZIR: SIMULE3_MANIFESTO_NEY_7D_40S.wav")
else:
    print("[-] UYARI: Klasörde Ney dosyası bulunamadı!")

if os.path.exists("temp_matrix.wav"):
    os.remove("temp_matrix.wav")
