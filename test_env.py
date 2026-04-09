import sys
print("Starting test...")
try:
    import pandas as pd
    print("Pandas imported")
except ImportError:
    print("Pandas NOT found")
