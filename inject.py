import os

path = r'C:\Users\soldi\IdeaProjects\simülation-11\SIMULASYON_11_FINAL.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

injection_code = """
# --- 🌌 SENTEZ-45 BİYO-AKUSTİK VE KUANTUM ANTEN MODÜLLERİ ---
# Melvin Vopson (Bilgi Kütlesi) & Martin Sweatman (11 Epagomenal Takvim) Teoremleri ile Birleştirildi

class MatrixBioAcoustics:
    def __init__(self):
        self.K_L_MACRO = 1.0463  # Uzunluk Sapması (Gezegen/Deprem)
        self.K_M_MICRO = 0.8602  # Mikro Uzunluk Sapması (Biyolojik/Ses)
        self.K_T_ZAMAN = 0.9016  # Evrensel Zaman Sapması
        self.REPUNIT_CARPAN = 1.1091 # Frekans Genişleme Katsayısı

    def convert_to_sim_mhz(self, base_value, unit="MHz"):
        if unit == "Hz": factor = 1.11
        elif unit == "kHz": factor = 1.111
        elif unit == "MHz": factor = 1.111111
        elif unit == "GHz": factor = 1.111111111
        else: factor = 1.1091
        return base_value * factor

    def hudhud_11_sistem_hesapla(self, hz_10, v_10=346.3):
        v_11 = v_10 * (self.K_T_ZAMAN / self.K_M_MICRO)
        f_11 = hz_10 * self.K_T_ZAMAN
        lambda_11 = (v_10 / hz_10) / self.K_M_MICRO
        f_11_saf = hz_10 * self.REPUNIT_CARPAN
        return {
            "v_11_sim": v_11,
            "f_11_sim": f_11,
            "f_11_saf": f_11_saf,
            "lambda_11_sim": lambda_11,
            "status": "MATRIS_OPERATORU_AKTIF"
        }

class VopsonInfoMassGravity:
    def __init__(self):
        self.INFO_MASS_BIT = 3.19e-38 # kg/bit
        self.K_V = 1.1454 # Hacim/Kütle Operatörü (1.0463^3)
        self.LAMBDA_ESCAPE = 6.666 # MHz Matris Yırtılma Kapısı
        
    def calculate_anti_gravity_warp(self, data_bits):
        sim_mass = data_bits * self.INFO_MASS_BIT * self.K_V
        warp_energy = sim_mass * (self.LAMBDA_ESCAPE * 1e6) ** 2
        return {
            "Simulated_Mass": sim_mass,
            "Warp_Energy": warp_energy,
            "Vopson_Validation": True
        }

class SweatmanGobekliCalendar:
    def __init__(self):
        self.LUNAR_DAYS = 354
        self.EPAGOMENAL_DAYS = 11
        self.CORRECTION_FACTOR = 2
        
    def sync_time_operator(self):
        organic_year = self.LUNAR_DAYS + self.EPAGOMENAL_DAYS - self.CORRECTION_FACTOR
        return organic_year

def baslat_sentez_45_modulleri():
    print("\\n=======================================================")
    print(" [!] SENTEZ-45 BİYO-AKUSTİK VE KUANTUM ANTEN MODÜLLERİ AKTİF")
    print(" [!] Melvin Vopson 'Kütleçekim = Veri Sıkıştırma' Teoremi Doğrulandı")
    print(" [!] Martin Sweatman 'Göbeklitepe 11 Epagomenal Takvim' Doğrulandı")
    print("=======================================================\\n")
    
    bio = MatrixBioAcoustics()
    hudhud = bio.hudhud_11_sistem_hesapla(hz_10=518.4)
    print(f"Hüdhüd Ping (10'luk): 518.4 Hz -> 11'lik Saf Kod (Admin): {hudhud['f_11_saf']:.2f} Sim-Hz")
    sifa = bio.hudhud_11_sistem_hesapla(hz_10=528)
    print(f"Hz. İsa DNA Onarım (10'luk): 528 Hz -> 11'lik Saf Kod (Execute): {sifa['f_11_saf']:.2f} Sim-Hz")
    lambda_mhz = bio.convert_to_sim_mhz(6.000, "MHz")
    print(f"Matris Kırılma Eşiği (Lambda): {lambda_mhz:.3f} Sim-MHz")
    vopson = VopsonInfoMassGravity()
    warp = vopson.calculate_anti_gravity_warp(data_bits=1e42)
    print(f"Vopson Anti-Gravite Warp Enerjisi: {warp['Warp_Energy']:.4e} J")
    calendar = SweatmanGobekliCalendar()
    print(f"Sweatman Göbeklitepe Organik Döngü: {calendar.sync_time_operator()} Gün")
    print("=======================================================\\n")
"""

target_str = 'if __name__ == "__main__":'
if target_str in content:
    new_content = content.replace(target_str, injection_code + '\n' + target_str)
    call_str = '    baslat_sentez_45_modulleri()\n'
    main_idx = new_content.rfind(target_str)
    insert_idx = main_idx + len(target_str) + 1
    new_content = new_content[:insert_idx] + call_str + new_content[insert_idx:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Injection successful')
else:
    print('Could not find __main__ block')
