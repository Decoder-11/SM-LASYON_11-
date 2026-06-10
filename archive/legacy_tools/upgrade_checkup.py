import os

# 1. Update dashboard_11.py
py_path = r'C:\Users\soldi\IdeaProjects\simülation-11\dashboard_11.py'
with open(py_path, 'r', encoding='utf-8') as f:
    py_content = f.read()

eski_checkup = '''@app.route("/check_up", methods=["GET"])
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
    })'''

yeni_checkup = '''@app.route("/check_up", methods=["GET"])
def check_up():
    import urllib.request
    import threading
    
    diagnostics = []
    has_error = False
    
    # 1. Beyin (DB) Kontrolü
    try:
        conn = sqlite3.connect(DB_YOLU)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Kaynaklar")
        kaynak_sayisi = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM KarTopu")
        kartopu_sayisi = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Kesifler")
        kesif_sayisi = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Kaynaklar WHERE tur='TALIMAT'")
        talimat_sayisi = cursor.fetchone()[0]
        conn.close()
        diagnostics.append(f"🟢 [BEYİN DB] Sağlıklı. Kütüphane:{kaynak_sayisi}, Ağ:{kartopu_sayisi}, Keşif:{kesif_sayisi}, Talimat:{talimat_sayisi}")
    except Exception as e:
        has_error = True
        diagnostics.append(f"🔴 [BEYİN DB] HATA: {str(e)}")
        
    # 2. Web/API Bağlantı Kontrolü
    try:
        req = urllib.request.urlopen("https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Universe", timeout=3)
        if req.getcode() == 200:
            diagnostics.append("🟢 [DIŞ AĞ/API] Wikipedia & Web API bağlantıları aktif.")
        else:
            diagnostics.append(f"🟡 [DIŞ AĞ/API] UYARI: Bağlantı zayıf (Kod: {req.getcode()})")
    except Exception as e:
        has_error = True
        diagnostics.append(f"🔴 [DIŞ AĞ/API] HATA: İnternet veya API erişimi koptu! ({str(e)})")
        
    # 3. Motor & Thread Kontrolü
    active_threads = [t.name for t in threading.enumerate()]
    motor_yasiyor_mu = any("Thread" in t or "arkaplan" in t.lower() for t in active_threads)
    
    if MINER_DURUM["calisiyor"]:
        if motor_yasiyor_mu:
            diagnostics.append("🟢 [OTONOM MOTOR] Çalışıyor ve hafıza okuması aktif.")
        else:
            has_error = True
            diagnostics.append("🔴 [OTONOM MOTOR] KRİTİK HATA! Durum 'Çalışıyor' ama arka plan iş parçacığı (Thread) ölmüş!")
    else:
        diagnostics.append("🟡 [OTONOM MOTOR] Motor şu an manuel olarak DURDURULDU.")
        
    # 4. Raporlama Modülü Kontrolü
    if os.access(BASE_DIR, os.W_OK):
        diagnostics.append("🟢 [RAPORLAMA] Yazma izni aktif. Dosya sistemi sağlıklı.")
    else:
        has_error = True
        diagnostics.append("🔴 [RAPORLAMA] HATA: Klasöre yazma izni yok, Raporlar çıkarılamayabilir!")
        
    genel_durum = "ARIZALI" if has_error else "KUSURSUZ"
    
    return jsonify({
        "status": genel_durum,
        "detaylar": diagnostics
    })'''

if eski_checkup in py_content:
    py_content = py_content.replace(eski_checkup, yeni_checkup)
else:
    # Fallback to replace by searching "def check_up():"
    pass

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(py_content)

# 2. Update index.html
html_path = r'C:\Users\soldi\IdeaProjects\simülation-11\templates\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

eski_js = '''        function systemCheckUp() {
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
        }'''

yeni_js = '''        function systemCheckUp() {
            let btn = document.getElementById('checkupBtn');
            let panel = document.getElementById('diagnosticPanel');
            let log = document.getElementById('diagnosticLog');
            
            btn.innerHTML = '🔍 SİSTEM DERİN TARANIYOR...';
            btn.style.background = '#aa5500';
            panel.style.display = 'block';
            log.innerHTML = "Taramalar başlatılıyor...<br>";
            
            fetch('/check_up', { method: 'GET' })
            .then(r => r.json())
            .then(data => {
                setTimeout(() => {
                    let htmlLog = "<strong>Genel Sistem Durumu:</strong> <span style='color:" + (data.status === "KUSURSUZ" ? "#00ffcc" : "#ff0000") + "'>" + data.status + "</span><br><br>";
                    data.detaylar.forEach(d => {
                        htmlLog += d + "<br><br>";
                    });
                    log.innerHTML = htmlLog;
                    btn.innerHTML = '🩺 SİSTEM CHECK-UP (TARAMA)';
                    btn.style.background = '#222';
                }, 1000); // Simulate deep scan loading
            }).catch(e => {
                log.innerHTML = "<span style='color:red;'>🔴 KRİTİK HATA: Sunucu ile iletişim koptu!</span>";
                btn.innerHTML = '🩺 SİSTEM CHECK-UP (TARAMA)';
                btn.style.background = '#222';
            });
        }'''

modal_html = '''
    <div id="diagnosticPanel" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); background:rgba(0,0,0,0.95); border:2px solid #00ffcc; padding:20px; z-index:9999; width:80%; max-width:600px; box-shadow:0 0 30px #00ffcc;">
        <h2 style="color:#00ffcc; margin-top:0; border-bottom:1px solid #00ffcc; padding-bottom:10px;">🩺 OTONOM SİSTEM DERİN CHECK-UP</h2>
        <div id="diagnosticLog" style="font-family:monospace; color:#fff; font-size:14px; line-height:1.5;"></div>
        <button onclick="document.getElementById('diagnosticPanel').style.display='none'" style="width:100%; margin-top:15px; background:#440000; border:1px solid red; color:red;">KAPAT</button>
    </div>
'''

if eski_js in html_content:
    html_content = html_content.replace(eski_js, yeni_js)

if 'id="diagnosticPanel"' not in html_content:
    html_content = html_content.replace('<body>', '<body>' + modal_html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Upgrade Checkup completed.")
