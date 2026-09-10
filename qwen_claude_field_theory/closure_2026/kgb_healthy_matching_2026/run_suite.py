#!/usr/bin/env python3
"""Record actual bounded construction checks, not a theory pass counter."""
import argparse,json,subprocess,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True);a=parser.parse_args()
    cases=[['test_pressure_target.py'],['pressure_target.py'],['test_search.py'],
        ['search.py','--result-file',str(a.result_file.resolve().with_name('pressure_scan.json'))],
        ['test_radial_action.py'],['radial_action.py','--result-file',str(a.result_file.resolve().with_name('radial_equations.json'))],
        ['constant_sector/run_sector.py'],['constant_sector/sector.py'],
        ['dhost_kinetic/test_kinetic.py'],['dhost_kinetic/kinetic.py'],
        ['../kgb_logslip_joint_2026/reference/run_reference.py']]
    records=[]
    for script,*extra in cases:
        argv=[sys.executable,'-B',str(HERE/script),*extra]
        out=subprocess.run(argv,cwd=HERE,capture_output=True,text=True,timeout=60)
        records.append(dict(argv=argv,cwd=str(HERE),exit_status=out.returncode,stdout=out.stdout,stderr=out.stderr))
        print(json.dumps(dict(script=script,exit_status=out.returncode)),flush=True)
    lean_cwd=HERE.parent/'clock_constitutive_construction_2026/lean_formalization_2026'
    argv=['lake','env','lean',str(HERE/'dhost_kinetic/KineticDegeneracy.lean')]
    out=subprocess.run(argv,cwd=lean_cwd,capture_output=True,text=True,timeout=60)
    records.append(dict(argv=argv,cwd=str(lean_cwd),exit_status=out.returncode,stdout=out.stdout,stderr=out.stderr))
    print(json.dumps(dict(script='KineticDegeneracy.lean',exit_status=out.returncode)),flush=True)
    a.result_file.write_text(json.dumps(dict(cases=records,full_theory_status='OPEN'),indent=2)+'\n')
    return int(any(row['exit_status'] for row in records))

if __name__=='__main__':raise SystemExit(main())
