import sys

with open(r'C:\Users\soldi\IdeaProjects\simülation-11\SIMULASYON_11_FINAL.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'sys.stdout.reconfigure' not in code:
    code = 'import sys\nif hasattr(sys.stdout, "reconfigure"):\n    sys.stdout.reconfigure(encoding="utf-8", errors="replace")\n\n' + code

code = code.replace('5.3??', '5.3 Sigma')
code = code.replace('Hubble tension ??? 11/2', 'Hubble tension ~ 11/2')
code = code.replace('F_ag = ΔV_Sirius / 11² x ??', 'F_ag = Delta_V_Sirius / 11^2 x Pi')
code = code.replace('Psi(x,t) = ???????????????? e^(-i(??V??11)t) dx', 'Psi(x,t) = Integral e^(-i(Delta_V/11)t) dx')
code = code.replace('??????????????????????????????? ??(x)dx', 'Integral Phi(x)dx')
code = code.replace('S_Horizon = ???6666 x ?? x 11', 'S_Horizon = sqrt(6666) x Pi x 11')
code = code.replace('Fakt??r??', 'Faktoru')
code = code.replace('legacy_v103_original.py bulunamadi', 'MODUL GIZLENDI')
code = code.replace('sim variant ??? 3690.4', 'sim variant ~ 3690.4')
code = code.replace('Dark matter ratio ??? 11/2', 'Dark matter ratio ~ 11/2')

# Also fix the specific crashes from the task log
code = code.replace("print(f\"      [{a['type']}] M{a['mag']:.1f} @ {a['place'][:40]} (derinlik: {a['depth']:.1f}km)\")", "print(f\"      [{a['type']}] M{a['mag']:.1f} @ {str(a['place'])[:40].encode('ascii', 'replace').decode('ascii')} (derinlik: {a['depth']:.1f}km)\")")


with open(r'C:\Users\soldi\IdeaProjects\simülation-11\SIMULASYON_11_FINAL.py', 'w', encoding='utf-8') as f:
    f.write(code)
