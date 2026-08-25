import os
import sys

# so `from server.app import ...` resolves however pytest is launched
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
