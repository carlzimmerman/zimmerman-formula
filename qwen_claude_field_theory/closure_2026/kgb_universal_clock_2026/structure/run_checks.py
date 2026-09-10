#!/usr/bin/env python3
"""Bounded reproducible structure package gate; no scans or file mutation."""
from pathlib import Path
import subprocess
import sys


def main():
    here=Path(__file__).resolve().parent
    lean=here.parents[1]/'clock_constitutive_construction_2026'/'lean_formalization_2026'
    commands=[([sys.executable,'-B',str(here/'test_shared_preservation.py')],here),
              (['lake','env','lean',str(here/'SharedControlAlgebra.lean')],lean),
              ([sys.executable,'-B',str(here/'check_next_preservation.py'),'--dps','60'],here),
              ([sys.executable,'-B',str(here/'check_next_preservation.py'),'--dps','80'],here)]
    for command,cwd in commands:
        print('RUN '+repr(command),flush=True)
        subprocess.run(command,cwd=cwd,check=True,timeout=30)


if __name__=='__main__':main()
