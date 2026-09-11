#!/usr/bin/env python3
"""Bounded parallel source/action/formal checks; a zero exit is not closure."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    p=argparse.ArgumentParser();p.add_argument('--result-file',required=True,type=Path)
    args=p.parse_args();out=args.result_file.parent
    cases=[
        ('sourced_variation',[sys.executable,'-B',str(HERE/'source.py'),'--result-file',str(out/'source.json')],ROOT),
        ('sourced_response_refinement',[sys.executable,'-B',str(HERE/'response.py'),'--modes','129','--refine','--result-file',str(out/'response.json')],ROOT),
        ('full_spherical_variation',[sys.executable,'-B',str(HERE/'action/derive.py')],ROOT),
        ('dynamical_spherical_dust',[sys.executable,'-B',str(HERE/'action/matter.py')],ROOT),
        ('source_behavior_tests',[sys.executable,'-B',str(HERE/'test_source.py')],ROOT),
        ('Newton_radial_control',[sys.executable,'-B',str(HERE/'test_response.py')],ROOT),
        ('SourceSchur.lean',['lake','env','lean',str(HERE/'SourceSchur.lean')],LEAN),
        ('prior_current_regression',[sys.executable,'-B',str(HERE.parent/'cubic_current_audit/derive.py')],ROOT),
        ('prior_background_regression',[sys.executable,'-B',str(HERE.parent/'cubic_background_completion/derive.py')],ROOT),
        ('prior_tensor_regression',[sys.executable,'-B',str(HERE.parent/'cubic_finite_wavelength/tensor_gate.py')],ROOT)]
    def one(case):
        name,argv,cwd=case
        try:
            result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=480)
            row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=result.returncode,stdout=result.stdout,stderr=result.stderr)
        except subprocess.TimeoutExpired as exc:
            row=dict(name=name,argv=argv,cwd=str(cwd.relative_to(ROOT)),exit_status=None,status='timeout',stdout=str(exc.stdout),stderr=str(exc.stderr))
        print(json.dumps({key:row[key] for key in ('name','exit_status')}),flush=True)
        return row
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows=list(pool.map(one,cases))
    args.result_file.write_text(json.dumps(dict(cases=rows,full_theory_status='OPEN'),indent=2)+'\n')
    return int(any(r['exit_status']!=0 for r in rows))


if __name__=='__main__':raise SystemExit(main())
