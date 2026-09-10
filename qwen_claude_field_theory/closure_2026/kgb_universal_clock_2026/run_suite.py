#!/usr/bin/env python3
"""Reproducible bounded checkpoint; execution success is not theory closure."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
OLD=HERE.parent/'kgb_nonaffine_clock_2026'
LEAN=HERE.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    py=[sys.executable,'-B']
    cases=[('root tests',py+['-m','unittest','-v','test_universal_seed','test_w_match',
        'test_reduced_match','test_high_precision_gate'],HERE,0)]
    for name in ('universal_seed.py','w_match.py','reduced_match.py','high_precision_gate.py','continue_seeds.py'):
        cases.append((name,py+[name],HERE,0))
    cases.append(('strict next-preservation gate',py+['high_precision_gate.py','--require-next-preservation'],HERE,2))
    for name in ('structure/run_checks.py','health/run_health.py','health_search/run_matched_audit.py'):
        cases.append((name,py+[str(HERE/name)],HERE,0))
    # Proportionate old-action variation, principal, flow, and cosmology checks
    # follow all new work; no old snapshots or concurrent code are overwritten.
    cases.append(('previous nonaffine flow/health tests',py+['-m','unittest','-v',
        'test_nonaffine','test_quadratic_flow','test_curvature_window','test_controlled_flow'],OLD,0))
    for name in ('variation/test_nonaffine_variation.py','dictionary/test_general.py',
                 'cosmology/test_cosmology.py','l123_review/test_power_law_counterclaim.py'):
        cases.append((name,py+[str(OLD/name)],REPO,0))
    records=[]
    for label,argv,cwd,expected in cases:
        record=dict(label=label,argv=argv,cwd=str(cwd),expected_exit=expected)
        try:
            p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=120)
            record.update(exit_status=p.returncode,stdout=p.stdout,stderr=p.stderr)
        except (OSError,subprocess.TimeoutExpired) as exc:
            record.update(exit_status=124 if isinstance(exc,subprocess.TimeoutExpired) else 127,
                stdout='',stderr=str(exc),error=type(exc).__name__)
        record['expected_execution_outcome']=record['exit_status']==expected
        record['reported_unittest_counts']=[int(v) for v in re.findall(r'Ran (\d+) tests?',record['stdout']+record['stderr'])]
        records.append(record)
        print('CASE='+json.dumps({k:v for k,v in record.items() if k not in ('stdout','stderr')}),flush=True)
    result=dict(cases=records,physics_status='OPEN',
        scope='Regular initial shared-action jets found; evaluated seeds fail next preservation. No full theory or universal no-go.')
    if args.result_file:args.result_file.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    else:print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if all(r['expected_execution_outcome'] for r in records) else 1


if __name__=='__main__':raise SystemExit(main())
