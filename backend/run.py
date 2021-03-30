import sys
#sys.path.append('/Users/jainsh/Documents/cmpe295/NLP-based-QA-System-for-custom-KG-demo')
from pathlib import Path

import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
print(path)
sys.path.append(path)
from backend.app._base import run_app
from os import path

#sys.path.join(path.dirname(path.abspath(__file__)))
print(sys.path)
run_app()
