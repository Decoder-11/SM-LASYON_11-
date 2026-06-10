import os

# 1. Update index.html
html_path = r'C:\Users\soldi\IdeaProjects\simülation-11\templates\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Add javascript function for check-up
js_insert = '''        function systemCheckUp() {
            let btn = document.getElementById('checkupBtn');
            btn.innerHTML = '🔍 Taranıyor...';
            btn.style.background = '#aa5500';
            
            fetch('/check_up', { method: 'GET' })
            .then(r => r.json())
            .then(data => {
                let msg = "SİSTEM CHECK-UP SONUCU:\\n\\n" +
                          "Durum: " + data.status + "\\n" +
                          "Beyin DB: " + data.db_status + "\\n" +
                          "Kütüphane (Kaynak): " + data.kaynak_sayisi + "\\n" +
                          "KarTopu (Ağ): " + data.kartopu_sayisi + "\\n" +
                          "Keşifler: " + data.kesif_sayisi + "\\n" +
                          "Motor: " + data.motor_status;
                alert(msg);
                btn.innerHTML = '🩺 SİSTEM CHECK-UP (TARAMA)';
                btn.style.background = '#222';
            }).catch(e => {
                alert('Check-up Başarısız!');
                btn.innerHTML = '🩺 SİSTEM CHECK-UP (TARAMA)';
                btn.style.background = '#222';
            });
        }
'''
if 'function systemCheckUp()' not in html_content:
    html_content = html_content.replace('function sendCommand(action) {', js_insert + '        function sendCommand(action) {')

# Add button
btn_insert = '''                <button class="stop" onclick="sendCommand('DURDUR')">⏹ SİSTEMİ DURDUR</button>
                <button id="checkupBtn" onclick="systemCheckUp()" style="background: #222; border-color: #00ffcc; color: #00ffcc;">🩺 SİSTEM CHECK-UP (TARAMA)</button>'''
if 'checkupBtn' not in html_content:
    html_content = html_content.replace('<button class="stop" onclick="sendCommand(\'DURDUR\')">⏹ SİSTEMİ DURDUR</button>', btn_insert)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)


# 2. Update dashboard_11.py
py_path = r'C:\Users\soldi\IdeaProjects\simülation-11\dashboard_11.py'
with open(py_path, 'r', encoding='utf-8') as f:
    py_content = f.read()

checkup_route = '''@app.route("/check_up", methods=["GET"])
def check_up():
    try:
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Kaynaklar")
        kaynak_sayisi = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM KarTopu")
        kartopu_sayisi = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Kesifler")
        kesif_sayisi = cursor.fetchone()[0]
        
        conn.close()
        db_status = "OK (Sağlıklı)"
    except Exception as e:
        db_status = f"HATA: {str(e)}"
        kaynak_sayisi = kartopu_sayisi = kesif_sayisi = 0
        
    motor_status = "AKTİF" if MINER_DURUM["calisiyor"] else "DURDURULMUŞ"
    
    return jsonify({
        "status": "TAMAMLANDI",
        "db_status": db_status,
        "kaynak_sayisi": kaynak_sayisi,
        "kartopu_sayisi": kartopu_sayisi,
        "kesif_sayisi": kesif_sayisi,
        "motor_status": motor_status
    })

@app.route("/sistem_tetikle"'''

if 'def check_up():' not in py_content:
    py_content = py_content.replace('@app.route("/sistem_tetikle"', checkup_route)
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(py_content)

print("Checkup button and logic added successfully!")
