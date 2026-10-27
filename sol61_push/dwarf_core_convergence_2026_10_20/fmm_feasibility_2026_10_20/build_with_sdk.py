"""Same build with the real Xcode SDK, bypassing Homebrew's stale SDK path."""
import os
from pathlib import Path
import runpy
import subprocess

os.environ['SDKROOT']=subprocess.check_output(['xcrun','--sdk','macosx','--show-sdk-path'],text=True).strip()
print('SDKROOT='+os.environ['SDKROOT'],flush=True)
runpy.run_path(str(Path(__file__).with_name('build_native.py')),run_name='__main__')
