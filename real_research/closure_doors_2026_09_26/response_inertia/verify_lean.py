#!/usr/bin/env python3
"""Compile the scoped theorem file, record every printed axiom dependency."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
here=Path(__file__).resolve().parent;repo=here.parents[2]
source=here/'DoorsResponse20260926.lean'
command=['lake','env','lean','-j','1',str(source)]
proc=subprocess.run(command,cwd=repo/'fable_independent_2026'/'lean_2026',capture_output=True,text=True,timeout=160)
print(proc.stdout,end='');print(proc.stderr,end='')
decls=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",proc.stdout,re.S)
allowed={'propext','Classical.choice','Quot.sound'}
axioms={n:sorted({x.strip()for x in a.split(',')if x.strip()})for n,a in decls}
passed=proc.returncode==0 and len(axioms)==11 and all(set(v)<=allowed for v in axioms.values())
result={'result':'accepted scoped Lean algebra'if passed else'Lean check failed','returncode':proc.returncode,
        'child_command':command,'child_timeout_seconds':160,
        'source':str(source.relative_to(repo)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'theorems':axioms,'expected_theorem_count':11,'passed':passed,
        'scope':'real algebra for supplied action coefficients; no formal action variation, PDE, causal-support or full-physics theorem'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
assert passed,result
