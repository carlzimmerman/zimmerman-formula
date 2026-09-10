#!/usr/bin/env python3
"""Bounded reproducibility run; exit zero means execution, not a healthy theory."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'kgb_universal_clock_2026'
LEAN=HERE.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();py=[sys.executable,'-B']
    cases=[('root tests',py+['-m','unittest','-v','test_parametric','test_search','test_candidate_health'],HERE)]
    for name,extra in [('parametric.py',[]),('continue_y.py',[]),('search.py',['--max-nfev','500']),
                       ('clock_joint.py',[]),('refine_joint.py',[]),('candidate_health.py',[])]:
        cases.append((name,py+[name]+extra,HERE))
    for name in ('derivatives/test_fast.py','scaling/test_scaling.py','zero_braiding/test_zero_gamma.py'):
        cases.append((name,py+[str(HERE/name)],HERE))
    cases.append(('scaling algebra CLI',py+[str(HERE/'scaling/scaling_identities.py')],HERE))
    for name in ('scaling/PositiveScaling.lean','zero_braiding/ZeroBraiding.lean'):
        cases.append((name,['lake','--dir',str(LEAN),'env','lean',str(HERE/name)],HERE))
    cases.append(('previous matching and preservation tests',py+['-m','unittest','-v',
                  'test_universal_seed','test_w_match','test_reduced_match','test_high_precision_gate'],OLD))
    for name in ('variation/test_nonaffine_variation.py','dictionary/test_general.py','cosmology/test_cosmology.py'):
        cases.append((name,py+[str(HERE.parent/'kgb_nonaffine_clock_2026'/name)],HERE))
    records=[]
    for label,argv,cwd in cases:
        record=dict(label=label,argv=argv,cwd=str(cwd))
        try:
            out=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=120)
            record.update(exit_status=out.returncode,stdout=out.stdout,stderr=out.stderr)
        except (OSError,subprocess.TimeoutExpired) as exc:
            record.update(exit_status=124 if isinstance(exc,subprocess.TimeoutExpired) else 127,
                          stdout='',stderr=str(exc))
        record['reported_unittest_counts']=[int(v) for v in re.findall(r'Ran (\d+) tests?',record['stdout']+record['stderr'])]
        records.append(record)
        print(json.dumps({k:v for k,v in record.items() if k not in ('stdout','stderr')}),flush=True)
    result=dict(cases=records,physics_status='OPEN',
                specific_joint_point='REJECTED: angular instability and next tangency failure',
                scope='Finite numerical search plus conditional algebra; not complete theory or universal exclusion')
    args.result_file.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return int(any(row['exit_status']!=0 for row in records))


if __name__=='__main__':raise SystemExit(main())
