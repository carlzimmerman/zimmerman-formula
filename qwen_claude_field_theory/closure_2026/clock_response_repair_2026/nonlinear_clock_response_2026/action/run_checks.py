#!/usr/bin/env python3
"""Execute every new scientific script and its regression suite."""
import argparse
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path,required=True)
    args = parser.parse_args()
    subprocess.run([sys.executable,'-m','unittest','discover','-s',str(HERE),
                    '-p','test_action.py'],check=True)
    subprocess.run([sys.executable,str(HERE/'adm_action.py'),
                    '--result-file',str(args.result_file)],check=True)
