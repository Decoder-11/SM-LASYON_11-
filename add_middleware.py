import os

py_path = r'C:\Users\soldi\IdeaProjects\simülation-11\dashboard_11.py'
with open(py_path, 'r', encoding='utf-8') as f:
    py_content = f.read()

middleware = '''
class ExceptionCatchMiddleware:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            import traceback
            err = traceback.format_exc()
            with open("hata_logu.txt", "w", encoding="utf-8") as f:
                f.write(err)
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
            return [f"<h1>MİDDLEWARE HATA YAKALADI</h1><pre>{err}</pre>".encode('utf-8')]

app.wsgi_app = ExceptionCatchMiddleware(app.wsgi_app)
'''

if 'ExceptionCatchMiddleware' not in py_content:
    # insert before app.run
    py_content = py_content.replace("if __name__ == '__main__':", f"{middleware}\nif __name__ == '__main__':")
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(py_content)
    print("Middleware added!")
else:
    print("Middleware already exists.")
