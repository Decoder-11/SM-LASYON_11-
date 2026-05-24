import os

py_path = r'C:\Users\soldi\IdeaProjects\simülation-11\dashboard_11.py'
with open(py_path, 'r', encoding='utf-8') as f:
    py_content = f.read()

error_handler = '''@app.errorhandler(500)
def internal_error(e):
    import traceback
    err_str = traceback.format_exc()
    with open("hata_logu.txt", "w", encoding="utf-8") as f:
        f.write(err_str)
    return f"<h1>Dahili Sunucu Hatası Detayı</h1><pre>{err_str}</pre>", 500

@app.after_request'''

if '@app.errorhandler(500)' not in py_content:
    py_content = py_content.replace('@app.after_request', error_handler)
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(py_content)

print("Error handler added!")
