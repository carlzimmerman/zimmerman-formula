#!/usr/bin/env python3
"""Compile field-transport algebra and audit all axiom dependencies."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
here=Path(__file__).resolve().parent;repo=here.parents[2]
source=here/'CommonTransport20260926.lean'
cmd=['lake','env','lean','-j','1',str(source)]
p=subprocess.run(cmd,cwd=repo/'fable_independent_2026/lean_2026',capture_output=True,text=True,timeout=150)
print(p.stdout,end='');print(p.stderr,end='')
rows=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",p.stdout,re.S)
axioms={name:sorted({a.strip()for a in row.split(',')if a.strip()})for name,row in rows}
allowed={'propext','Classical.choice','Quot.sound'}
passed=(p.returncode==0 and len(axioms)==13 and all(set(a)<=allowed for a in axioms.values())
        and 'warning:'not in p.stdout and 'error:'not in p.stdout)
out={'result':'accepted field-transport real algebra'if passed else'Lean verification failed',
 'returncode':p.returncode,'child_command':cmd,'child_timeout_seconds':150,
 'source':str(source.relative_to(repo)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'theorem_count':len(axioms),'axioms':axioms,'passed':passed,
 'non_claims':['No formal PDE or global gravity theorem','No particle or halo evacuation derivation','No global timelike clock theorem']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');assert passed,out
