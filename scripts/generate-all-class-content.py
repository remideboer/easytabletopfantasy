#!/usr/bin/env python3
"""Regenerate classes.html and all class ability pages."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
scripts = [
    ROOT / "generate-class-abilities.py",
    ROOT / "generate-classes-html.py",
    ROOT / "generate-character-options-html.py",
]

for script in scripts:
    print(f"Running {script.name}...")
    subprocess.check_call([sys.executable, str(script)])

print("Done.")
