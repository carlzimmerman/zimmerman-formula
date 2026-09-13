#!/usr/bin/env python3
"""Record fresh same-action regression exits and the exact Lean axiom sets."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    base=here.parents[1]
    root=base.parents[2]
    lean=root/'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026'
    out=args.output.resolve()
    if root not in out.parents:
        raise ValueError('output must be inside repository')
    out.mkdir(exist_ok=False)
    paths=[here/'test_evolve.py',here/'identity/derive_identity.py',here/'identity/NoSlip.lean',
           here.parent/'finite_wavelength/probe.py',here.parent/'finite_wavelength/adm/derive_chi_adm.py',
           here.parent/'finite_wavelength/history/derive_history.py',here.parent/'finite_wavelength/history/HistorySigns.lean',
           base/'nonlinear_evolution_2026/constitutive.py',base/'nonlinear_evolution_2026/FiniteTimeMOND.lean',
           base/'cubic_principal_audit/derive.py',base/'cubic_background_completion/derive.py',
           here.parent/'metric_response/derive_static_metric.py']
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
    guard=subprocess.run([sys.executable,'-B','-c',"assert False, 'negative control'"],
                         env=env,cwd=root,capture_output=True,text=True,timeout=10)
    if guard.returncode==0 or 'negative control' not in guard.stderr:
        raise AssertionError('disabled assertions')
    def check(path):
        islean=path.suffix=='.lean'
        argv=['/opt/homebrew/bin/lake','env','lean',str(path)] if islean else [sys.executable,'-B',str(path)]
        before=hashlib.sha256(path.read_bytes()).hexdigest()
        start=time.monotonic()
        proc=subprocess.run(argv,cwd=lean if islean else root,env=env,capture_output=True,text=True,timeout=90)
        after=hashlib.sha256(path.read_bytes()).hexdigest()
        stem=path.parent.name+'_'+path.stem
        (out/(stem+'.stdout.txt')).write_text(proc.stdout)
        (out/(stem+'.stderr.txt')).write_text(proc.stderr)
        axiomsets=[set(y.strip() for y in x.split(',')) for x in re.findall(r'depends on axioms: \[([^]]*)\]',proc.stdout)]
        proofs=not islean or (bool(axiomsets) and all(x<={'propext','Classical.choice','Quot.sound'} for x in axiomsets))
        ok=proc.returncode==0 and before==after and proofs
        print(stem,'exit',proc.returncode,'checked',ok,flush=True)
        return dict(argv=argv,cwd=str(lean if islean else root),exit_status=proc.returncode,
                    checked_ok=ok,seconds=time.monotonic()-start,sha256_before=before,sha256_after=after,
                    axioms=[sorted(x) for x in axiomsets])
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows=list(pool.map(check,paths))
    result=dict(theory_status='OPEN',negative_control_exit=guard.returncode,checks=rows,
                all_checked=all(x['checked_ok'] for x in rows))
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['all_checked'] else 1


if __name__=='__main__':
    raise SystemExit(main())
