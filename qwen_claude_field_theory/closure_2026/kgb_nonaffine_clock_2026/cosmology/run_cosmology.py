#!/usr/bin/env python3
"""Run the bounded cosmology audit; success is not a CMB safety certificate."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import unittest
import cosmology_checks as c
import test_cosmology

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
LEAN=HERE.parents[1]/'clock_constitutive_construction_2026/lean_formalization_2026'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    tests=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_cosmology))
    records=[]
    for label,argv,cwd in (
        ('conditional Lean algebra',['lake','env','lean',str(HERE/'CosmologyGates.lean')],LEAN),
        ('L121 literal arithmetic, interpretation audited separately',[sys.executable,'-B','fable_independent_2026/L121_a0_scaling_cmb_recheck.py'],REPO)):
        p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=60)
        records.append(dict(label=label,argv=argv,cwd=str(cwd),exit_status=p.returncode,stdout=p.stdout,stderr=p.stderr))
    result=dict(tests=dict(run=tests.testsRun,passed=tests.wasSuccessful()),commands=records,
        fluid=c.fluid_variation(),homogeneous=c.homogeneous_action(),quadratic_F_only=c.quadratic_scan(),
        jet_ambiguity=c.jet_ambiguity(),L121=c.l121_recheck(),
        scope='Exact background/matter identities and bounded F exclusions; CMB safety unresolved, no new P/G high-X continuation')
    output=json.dumps(c.serial(result),indent=2)+'\n'
    if args.result_file:args.result_file.write_text(output)
    else:print(output)
    return 0 if tests.wasSuccessful() and all(r['exit_status']==0 for r in records) else 1


if __name__=='__main__':raise SystemExit(main())
