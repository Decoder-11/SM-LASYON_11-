import runpy
import os
import sys

if __name__ == "__main__":
    # This bridge allows running the directory directly (e.g., 'python .')
    # It redirects execution to the main simulation kernel.
    script_path = os.path.join(os.path.dirname(__file__), 'simulasyon_11.py')
    
    if os.path.exists(script_path):
        runpy.run_path(script_path, run_name='__main__')
    else:
        print(f"Error: {script_path} not found.")
        sys.exit(1)
