#!/usr/bin/env python3
"""Reproduce the parameter reduction; successful checks do not certify gravity."""
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
LEAN=HERE.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    cases=[]
    for name in ('nonaffine_inverse.py','quadratic_flow.py','curvature_window.py','controlled_flow.py'):
        cases.append((name,[sys.executable,'-B',name],HERE))
    cases.append(('root tests',[sys.executable,'-B','-m','unittest','-v',
        'test_nonaffine','test_quadratic_flow','test_curvature_window','test_controlled_flow'],HERE))
    for name in ('variation/test_nonaffine_variation.py','dictionary/general_ef.py',
                 'dictionary/test_general.py','cosmology/cosmology_checks.py','cosmology/test_cosmology.py'):
        cases.append((name,[sys.executable,'-B',str(HERE/name)],REPO))
    for name in ('variation/NonaffineAlgebra.lean','variation/ConeWindow.lean','cosmology/CosmologyGates.lean'):
        cases.append((name,['lake','env','lean',str(HERE/name)],LEAN))
    cases.extend([
        ('previous closure regressions',[sys.executable,'-B','run_suite.py'],HERE.parent/'kgb_mass_compatibility_2026'),
        ('concurrent L121 literal checks',[sys.executable,'-B','fable_independent_2026/L121_a0_scaling_cmb_recheck.py'],REPO),
        ('concurrent AQUAL Lean certificate',['lake','env','lean',str(REPO/'fable_independent_2026/lean_2026/Mondlean.lean')],LEAN)])
    records=[]
    for label,argv,cwd in cases:
        record=dict(label=label,argv=argv,cwd=str(cwd))
        try:
            p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=300)
            record['exit_status']=p.returncode;out,err=p.stdout,p.stderr
        except (OSError,subprocess.TimeoutExpired) as exc:
            record['exit_status']=124 if isinstance(exc,subprocess.TimeoutExpired) else 127
            out='';err=str(exc);record['error']=type(exc).__name__
        print('CASE='+json.dumps(record),flush=True);print(out,end='');print(err,end='')
        records.append(record)
    print('SUITE_RESULTS='+json.dumps(records))
    print('PHYSICS_STATUS=OPEN; no universal sourced action, full Dirac/PPN/CMB/strong-coupling certificate')
    return 0 if all(r['exit_status']==0 for r in records) else 1


if __name__=='__main__':raise SystemExit(main())
