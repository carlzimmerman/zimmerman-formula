#!/usr/bin/env python3
"""Run each new script plus the existing matter and initial-data regressions."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]


if __name__=='__main__':
    names=['derive','solve','test_branch','cases']
    jobs=[(n,[sys.executable,'-B',str(HERE/(n+'.py'))],ROOT) for n in names]
    for n,p in [('old_initial',HERE.parent/'nonlinear_infall_2026/test_initial.py'),
                ('old_matter',HERE.parent/'spherical_baryon_bridge/action/matter.py'),
                ('matter_extension',HERE.parent/'nonlinear_evolution_2026/pressure_supported_baryons.py')]:
        jobs.append((n,[sys.executable,'-B',str(p)],ROOT))
    jobs.append(('lean',['/opt/homebrew/bin/lake','env','lean',str(HERE/'BindingThreshold.lean')],
                 HERE.parent.parent/'clock_constitutive_construction_2026/lean_formalization_2026'))
    def run(job):
        name,argv,cwd=job
        try:
            result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=60)
            return dict(name=name,argv=argv,cwd=str(cwd),exit_status=result.returncode,
                        stdout=result.stdout,stderr=result.stderr)
        except subprocess.TimeoutExpired:
            return dict(name=name,argv=argv,cwd=str(cwd),exit_status=124,status='timeout')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,jobs))
    print(json.dumps({'checks':rows,'full_theory':'OPEN',
                      'scope':'initial pressure balance; no stationary galaxy or MOND certification'},indent=2))
    sys.exit(0 if all(row['exit_status']==0 for row in rows) else 1)
