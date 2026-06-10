import re
file_path = 'SIMULASYON_11_FINAL.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the faulty imports
content = re.sub(r'(?m)^from quantum_gravity_11d import QuantumGravity11D\r?\n?', '', content)
content = re.sub(r'(?m)^from biological_neurological_simulations import ConsciousnessQuantumField11D\r?\n?', '', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
