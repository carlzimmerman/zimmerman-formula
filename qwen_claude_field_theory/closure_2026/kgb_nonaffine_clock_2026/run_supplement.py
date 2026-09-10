#!/usr/bin/env python3
"""Bounded new-claim audit after the main run; no repeated large scan."""
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
LEAN=HERE.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    cases=[
        ('L123 exact counterclaim',[sys.executable,'-B',str(HERE/'l123_review/test_power_law_counterclaim.py')],REPO),
        ('L123 conditional Lean certificate',['lake','env','lean',str(HERE/'l123_review/PowerLawCounterclaim.lean')],LEAN),
        ('L123 literal checks, not physical certification',[sys.executable,'-B','fable_independent_2026/L123_cmb_pincer_tightness.py'],REPO),
        ('root regressions after supplement',[sys.executable,'-B','-m','unittest','-v',
         'test_nonaffine','test_quadratic_flow','test_curvature_window','test_controlled_flow'],HERE),
        ('cosmology regressions after supplement',[sys.executable,'-B',str(HERE/'cosmology/test_cosmology.py')],REPO)]
    records=[]
    for label,argv,cwd in cases:
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=60)
        r=dict(label=label,argv=argv,cwd=str(cwd),exit_status=p.returncode)
        print('CASE='+json.dumps(r),flush=True);print(p.stdout,end='');print(p.stderr,end='');records.append(r)
    print('SUPPLEMENT_RESULTS='+json.dumps(records))
    print('PHYSICS_STATUS=OPEN; power-law counterexample is not the MOND action or a CMB fit')
    return 0 if all(r['exit_status']==0 for r in records) else 1


if __name__=='__main__':raise SystemExit(main())
