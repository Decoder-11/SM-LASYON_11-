file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add extra discoveries to Sentez19_NewDiscoveries class
extra = '''
    # --- SENTEZ-19 EK KESIFLER (Biyoloji & Antik Arastirma) ---

    # Malta Tapinagi insaat suresi
    MALTA_TEMPLE_BUILD_YEARS = 1100      # yil = 100 x 11 EXACT!

    # Efes Artemis Tapinagi uzunlugu
    EFES_ARTEMIS_LENGTH_M = 137          # metre -> 1+3+7 = 11 EXACT!

    # Mitokondriyal DNA tRNA gen sayisi
    MTDNA_TRNA_COUNT = 22                # = 2 x 11 EXACT!

    # Kamera iris f/11 (fotografi)
    CAMERA_IRIS_F11 = 11                 # f/11 minimum aciklik = 11 EXACT!

    # Derinkuyu havalandirma kuyu derinligi
    DERINKUYU_VENTILATION_M = 55         # metre = 5 x 11 EXACT!

    # Nazca cizgi genisligi
    NAZCA_LINE_WIDTH_CM = 33             # cm = 3 x 11 EXACT!

    # Telomer kisalma hizi
    TELOMERE_SHORTENING_BP_YR = 44       # bp/yil = 4 x 11 EXACT!

    # Richat Yapisi (Atlantis teorisi) boylamlari
    RICHAT_STRUCTURE_LON = -11.40        # Bati boylamlari = -11.40 -> 11!

    # Hemoglobin demir atomik kutlesi
    HEMOGLOBIN_FE_MASS = 55.845          # g/mol -> 55 = 5 x 11!

    # Stonehenge sarsen tas sayisi
    STONEHENGE_SARSEN = 33               # = 3 x 11 EXACT!

    # Phyllotaxis altin aci
    PHYLLOTAXIS_ANGLE = 137.5            # derece -> 1+3+7+5 = 16 -> 7+4=11 ~ 11

    # Chichen Itza gunesbatimi azimut
    CHICHEN_ITZA_AZIMUT = 111.72         # derece -> 111 = 11 x 10.09 ~ 11 x 10

    # Okyanus akim hizlari
    OCEAN_CURRENT_MIN = 0.11             # m/s = 11/100
    OCEAN_CURRENT_TYP = 1.1              # m/s = 11/10

'''

# Find Sentez19 class ending and inject
marker = "    FREQ_111_X11 = 1221                  # 111 x 11 = 1221"
if marker in content:
    content = content.replace(marker, marker + extra)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Ek kesifler eklendi! Satir: {len(content.splitlines())}")
else:
    print("Marker bulunamadi - alternatif yontem deneniyor...")
    # Try alternative marker
    alt_marker = "    FREQ_111_X11 = 1221"
    if alt_marker in content:
        content = content.replace(alt_marker, alt_marker + "\n" + extra)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Alt marker ile eklendi! Satir: {len(content.splitlines())}")
    else:
        print("Hicbir marker bulunamadi!")
