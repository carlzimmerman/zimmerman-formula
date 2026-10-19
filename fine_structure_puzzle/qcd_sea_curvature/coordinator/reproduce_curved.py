"""Rerun a byte-identical author script in a fresh owned output directory."""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

src=Path('fine_structure_puzzle/qcd_sea_curvature/curved_response/checks/check_trace_cut.py')
dst=Path(sys.argv[1])/'reproduction/checks/check_trace_cut.py'
dst.parent.mkdir(parents=True,exist_ok=False)
shutil.copyfile(src,dst)
assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(dst.read_bytes()).digest()
# The unchanged script locates RESULTS.json relative to __file__, so its copy
# writes solely below this fresh run. Original results cannot be overwritten.
subprocess.run([sys.executable,str(dst)],check=True,timeout=20)
