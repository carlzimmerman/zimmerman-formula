#!/usr/bin/env python3
"""Bounded local-current checks plus prior coupled-pressure regression suite."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]


if __name__=='__main__':
    jobs=[('derive',[sys.executable,'-B',str(HERE/'derive.py')],ROOT),
          ('scan',[sys.executable,'-B',str(HERE/'scan.py')],ROOT),
          ('pressure_regressions',[sys.executable,'-B',str(HERE.parent/'pressure_baryon_branch_2026/run_checks.py')],ROOT),
          ('lean',['/opt/homebrew/bin/lake','env','lean',str(HERE/'Transport.lean')],
           HERE.parent.parent/'clock_constitutive_construction_2026/lean_formalization_2026')]
    def run(job):
        name,argv,cwd=job
        try:
            p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=90)
            return dict(name=name,argv=argv,cwd=str(cwd),exit_status=p.returncode,stdout=p.stdout,stderr=p.stderr)
        except subprocess.TimeoutExpired:return dict(name=name,argv=argv,exit_status=124)
    with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,jobs))
    print(json.dumps(dict(checks=rows,full_theory='OPEN'),indent=2))
    sys.exit(0 if all(r['exit_status']==0 for r in rows) else 1)
