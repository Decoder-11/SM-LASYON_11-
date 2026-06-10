import codecs
file_path = 'C:/Users/soldi/IdeaProjects/simülation-11/SIMULASYON_11_FINAL.py'
with codecs.open(file_path, 'r', 'utf-8') as f:
    content = f.read()

target = '''if not os.path.exists(target_file):
    print(f"File not found: {target_file}")
    pass

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()
    lines = text.splitlines()'''

replacement = '''if not os.path.exists(target_file):
    print(f"File not found: {target_file}")
    text = ""
    lines = []
else:
    with open(target_file, 'r', encoding='utf-8') as f:
        text = f.read()
        lines = text.splitlines()'''

c2 = content.replace(target, replacement)
if c2 == content:
    target = target.replace('\n', '\r\n')
    c2 = content.replace(target, replacement)

with codecs.open(file_path, 'w', 'utf-8') as f:
    f.write(c2)
print("Done patching.")
