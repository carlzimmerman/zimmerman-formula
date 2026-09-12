#!/usr/bin/env python3
"""Archive this authorized numerical run with the computation-audit runner."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent/'cosmological_bridge_2026'
SKILL = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit')
INPUTS = [HERE/'initial_data.py',HERE/'test_initial_data.py',HERE/'run_bounded.py',HERE/'contract.json']
INPUTS += [BRIDGE/name for name in ('background_evolve.py','radiation_probe.py','transfer_evolve.py',
           'transfer_jets.py','branch_continuation.py','branch_kinetic.py','dark_energy_branches.py','derive.py')]
INPUTS += [HERE.parent/'nonlinear_evolution_2026'/'constitutive.py']


def relative(path):
    return str(path.relative_to(ROOT))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--name',required=True)
    parser.add_argument('--grid',type=int,default=1601)
    parser.add_argument('--refine-input',type=Path)
    args=parser.parse_args()
    output=HERE/args.name
    command=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
             '--contract',relative(HERE/'contract.json'),'--output',relative(output),
             '--timeout','420','--max-output-bytes','1048576','--max-threads','1']
    inputs=INPUTS+([args.refine_input.resolve()] if args.refine_input else [])
    for path in inputs:
        command+=['--input',relative(path)]
    command+=['--result',relative(output/'result.json'),'--',sys.executable,'-B',
              relative(HERE/'initial_data.py'),'--result-file',relative(output/'result.json'),
              '--grid',str(args.grid)]
    if args.refine_input:
        command+=['--refine-input',relative(args.refine_input.resolve())]
    print('EXECUTION ARGV:',repr(command),flush=True)
    result=subprocess.run(command,cwd=ROOT)
    print('EXPERIMENT EXIT:',result.returncode,flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    validation=[sys.executable,str(SKILL/'scripts/validate_manifest.py'),
                str(output/'manifest.json'),'--root',str(ROOT)]
    result=subprocess.run(validation,cwd=ROOT)
    print('MANIFEST VALIDATION EXIT:',result.returncode,flush=True)
    raise SystemExit(result.returncode)
