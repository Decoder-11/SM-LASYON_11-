file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# run_sentez19 cagrisini run_phase6_and_report icine ekle
old_text = 'def run_phase6_and_report():'
if old_text in content:
    # Find the function and add sentez19 call at start
    new_text = '''def run_phase6_and_report():
    # --- SENTEZ-19 YENI KESIFLER ---
    try:
        run_sentez19()
    except Exception as _s19e:
        print(f"[S19] Sentez-19 hatasi: {_s19e}")
    # --- SENTEZ-19 SONU ---'''
    content = content.replace(old_text, new_text, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("run_sentez19 cagirisi eklendi!")
else:
    print("Fonksiyon bulunamadi!")
