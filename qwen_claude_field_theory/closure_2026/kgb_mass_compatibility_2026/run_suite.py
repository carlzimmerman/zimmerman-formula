#!/usr/bin/env python3
"""Reproduce this checkpoint and relevant previous closure tests.

All command lines and exit statuses are emitted. Zero means the computations
and their stated checks ran, NEVER that the full gravity requirements passed.
"""
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
LEAN=HERE.parent/'clock_constitutive_construction_2026/lean_formalization_2026'


def run_case(label,argv,cwd):
    record=dict(label=label,argv=argv,cwd=str(cwd))
    try:
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=300)
        record['exit_status']=p.returncode
        return record,p.stdout,p.stderr
    except subprocess.TimeoutExpired as exc:
        record.update(exit_status=124,error='TimeoutExpired')
        output=exc.stdout or ''
        if isinstance(output,bytes):output=output.decode('utf-8',errors='replace')
        return record,output,'TimeoutExpired: '+str(exc)+'\n'
    except OSError as exc:
        record.update(exit_status=127,error=type(exc).__name__)
        return record,'',type(exc).__name__+': '+str(exc)+'\n'


def main():
    mains=('triple_seed.py','triple_flow.py','conformal_dictionary.py',
           'conformal_inverse.py','gradient_inverse.py','conformal_flow.py','l119_scope.py')
    cases=[(name,[sys.executable,'-B',name],HERE) for name in mains]
    cases += [('root regressions',[sys.executable,'-B','-m','unittest','-v',
        'test_triple','test_dictionary','test_conformal_inverse','test_gradient_inverse','test_runner'],HERE)]
    for file in ('structure/test_structure.py','structure/test_derivative_curvature_variation.py',
                 'structure/test_conformal_inverse_structure.py','extension/conformal_extension.py',
                 'extension/test_extension.py','extension/ef_principal.py','extension/inverse_audit.py'):
        cases.append((file,[sys.executable,'-B',str(HERE/file)],REPO))
    for file in ('structure/CompatibilityAlgebra.lean','structure/ConformalInverseAlgebra.lean'):
        cases.append((file,['lake','env','lean',str(HERE/file)],LEAN))
    cases += [('previous closure regressions',[sys.executable,'-B','run_suite.py'],HERE.parent/'kgb_joint_action_2026'),
              ('concurrent L119 literal checks',[sys.executable,'-B','fable_independent_2026/L119_health_passing_architecture.py'],REPO)]
    records=[]
    for label,argv,cwd in cases:
        record,out,err=run_case(label,argv,cwd)
        print('CASE='+json.dumps(record),flush=True)
        print(out,end='');print(err,end='');records.append(record)
    print('SUITE_RESULTS='+json.dumps(records))
    print('PHYSICS_STATUS=OPEN; no global healthy universal action or full Dirac/PPN/FLRW certificate')
    return 0 if all(r['exit_status']==0 for r in records) else 1


if __name__=='__main__':raise SystemExit(main())
