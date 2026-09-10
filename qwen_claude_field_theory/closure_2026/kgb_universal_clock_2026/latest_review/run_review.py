#!/usr/bin/env python3
"""Record exact new audit and read-only reproduction of the old assertions."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import unittest
import cutoff_counterexample as c
import test_cutoff_counterexample

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    tests=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_cutoff_counterexample))
    commands=[]
    for label,argv,cwd in (
        ('new conditional Lean cutoff proof',['lake','env','lean',str(HERE/'ScaleCounterexample.lean')],LEAN),
        ('existing L123 counterexample, reused not rewritten',[sys.executable,'-B','qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/l123_review/test_power_law_counterclaim.py'],ROOT),
        ('literal L125 execution, not physics certification',[sys.executable,'-B','fable_independent_2026/L125_final_verdict_health_vs_cosmology.py'],ROOT)):
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=60)
        commands.append(dict(label=label,argv=argv,cwd=str(cwd),exit_status=p.returncode,stdout=p.stdout,stderr=p.stderr))
    result=dict(tests=dict(run=tests.testsRun,passed=tests.wasSuccessful()),commands=commands,
        ordered_counterexample=c.ordered_counterexample(),literal_law_counterexample=c.literal_law_counterexample(),
        scope='Exact counterexample to a scale-substitution implication; no physical MOND/CMB fit or additional matter sector')
    payload=json.dumps(c.serial(result),indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
    return 0 if tests.wasSuccessful() and all(p['exit_status']==0 for p in commands) else 1


if __name__=='__main__':raise SystemExit(main())
