#!/usr/bin/env python3
"""Bounded reproducible continuation checks; a failed gate remains a failure.

The optional output directory must be new. The suite runs independent processes,
preserves every exit and output, and exits nonzero if any numerical gate fails.
Compilation of conditional theorems is never labelled full-theory closure.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PACKAGE=HERE/'nonlinear_evolution_2026'


def main():
    destination=Path(sys.argv[1]) if len(sys.argv)>1 else PACKAGE/'verification_001'
    if not destination.is_absolute():destination=ROOT/destination
    destination.mkdir(parents=True,exist_ok=False)
    names=['equations','constitutive','center','project','static_dust_gate','pressure_supported_baryons',
           'test_equations','test_constitutive','test_center','test_derivatives']
    jobs=[(name,[sys.executable,'-B',str(PACKAGE/(name+'.py'))],ROOT,60) for name in names]
    jobs += [('diagnose',[sys.executable,'-B',str(PACKAGE/'diagnose.py'),'--time','.005','--points','65','129'],ROOT,90),
             ('short_evolution',[sys.executable,'-B',str(PACKAGE/'evolve.py'),'--tend','.005','--dt','.001','--points','65'],ROOT,60),
             ('evolution_tests',[sys.executable,'-B',str(PACKAGE/'test_evolve.py')],ROOT,150)]
    for name,path in [('old_initial',HERE/'nonlinear_infall_2026/test_initial.py'),
                      ('old_potentials',HERE/'nonlinear_infall_2026/test_potentials.py'),
                      ('old_action',HERE/'spherical_baryon_bridge/action/derive.py'),
                      ('old_matter',HERE/'spherical_baryon_bridge/action/matter.py'),
                      ('tensor',HERE/'cubic_finite_wavelength/tensor_gate.py')]:
        jobs.append((name,[sys.executable,'-B',str(path)],ROOT,45))
    lake_cwd=HERE.parent/'clock_constitutive_construction_2026/lean_formalization_2026'
    jobs.append(('lean',['/opt/homebrew/bin/lake','env','lean',str(PACKAGE/'FiniteTimeMOND.lean')],lake_cwd,45))
    files=sorted(set(PACKAGE.glob('*.py'))|set(PACKAGE.glob('*.lean'))|{Path(__file__).resolve(),
           HERE/'spherical_baryon_bridge/action/derive.py',HERE/'spherical_baryon_bridge/action/matter.py',
           HERE/'nonlinear_infall_2026/background.py',HERE/'nonlinear_infall_2026/initial.py',
           HERE/'nonlinear_infall_2026/potentials.py'})
    def hashes():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    before=hashes();env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        env[key]='1'
    def run(job):
        name,cmd,cwd,limit=job;start=time.monotonic()
        try:
            p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=limit)
            code,stdout,stderr=p.returncode,p.stdout,p.stderr
        except subprocess.TimeoutExpired as error:
            code=124
            def decode(v):return v.decode(errors='replace') if isinstance(v,bytes) else (v or '')
            stdout,stderr=decode(error.stdout),decode(error.stderr)+'\nTIMEOUT: declared wall bound reached\n'
        (destination/(name+'.stdout.txt')).write_text(stdout)
        (destination/(name+'.stderr.txt')).write_text(stderr)
        row=dict(name=name,command=cmd,cwd=str(cwd.relative_to(ROOT)),exit_status=code,
                 wall_bound_seconds=limit,seconds=round(time.monotonic()-start,3))
        print(json.dumps(row),flush=True);return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,jobs))
    after=hashes()
    status='checks_passed' if before==after and all(x['exit_status']==0 for x in results) else 'checks_failed'
    report=dict(status=status,full_theory='OPEN',jobs=results,inputs_before=before,inputs_after=after,
                inputs_stable=before==after,python=platform.python_version(),platform=platform.platform(),
                scope='formal identities and bounded numerical controls; finite-time and full-theory claims require their own gates')
    (destination/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    return 0 if status=='checks_passed' else 1

if __name__=='__main__':sys.exit(main())
