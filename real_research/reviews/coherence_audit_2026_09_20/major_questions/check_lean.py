"""Compile the algebraic bridge and reject admitted or unexpected axioms."""
import json
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
HOST=ROOT/'fable_independent_2026/lean_2026'
version=subprocess.run(['lake','env','lean','--version'],cwd=HOST,text=True,capture_output=True,check=True).stdout.strip()
run=subprocess.run(['lake','env','lean',str(HERE/'AdvectionBridge.lean')],cwd=HOST,text=True,capture_output=True)
print(run.stdout, end='')
print(run.stderr, end='',file=sys.stderr)
assert run.returncode == 0
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",run.stdout,re.S)
assert len(axioms)==6
allowed={'propext','Classical.choice','Quot.sound'}
for theorem,values in axioms:
    assert set(x.strip() for x in values.split(',')) <= allowed
Path(sys.argv[1]).write_text(json.dumps({'lean':version,'theorems':{name:[x.strip() for x in values.split(',')] for name,values in axioms},'scope':'Exact finite-dimensional algebra; no PDE regularity theorem'},indent=2)+'\n')
