# linker.py
import os
import sys

# Define absolute paths for reliability
base_path = r'c:\Users\soldi\.gemini\antigravity\scratch\SM-LASYON_11-'
files = ['simulasyon_11.py', 'levhi_mahfuz.py', 'kar_topu_v5_v2_synthesis.py', 'kar_topu_v5_v3_synthesis.py']
output_file = os.path.join(base_path, 'simulasyon_11_MEGA.py')

try:
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for f in files:
            full_path = os.path.join(base_path, f)
            if not os.path.exists(full_path):
                print(f"ERROR: {f} not found at {full_path}")
                continue
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as infile:
                outfile.write(f'\n\n# ' + '='*20 + f' START OF {f} ' + '='*20 + '\n')
                outfile.write(infile.read())
                outfile.write(f'\n# ' + '='*20 + f' END OF {f} ' + '='*20 + '\n')
    print(f"Successfully generated Mega-Kernel at: {output_file}")
    print(f"Final size estimate: {os.path.getsize(output_file)} bytes")
except Exception as e:
    print(f"CRITICAL ERROR: {str(e)}")
    sys.exit(1)
