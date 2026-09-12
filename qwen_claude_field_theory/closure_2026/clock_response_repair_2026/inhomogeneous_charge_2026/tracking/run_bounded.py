#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPAIR=HERE.parents[1]
ROOT=next(p for p in HERE.parents if (p/'.git').exists())
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit')
inputs=[HERE/name for name in ('tracking_audit.py','test_tracking_audit.py','contract.json','run_bounded.py')]
inputs += [ROOT/'fable_independent_2026'/name for name in ('L194_tracking_dynamics.py','L192_results.json')]
inputs += [REPAIR/'cosmological_bridge_2026'/name for name in ('radiation_002/result.json',
    'radiation_probe.py','background_evolve.py','transfer_evolve.py','transfer_jets.py','derive.py')]
inputs += [REPAIR/'nonlinear_evolution_2026/constitutive.py']
relative=lambda p:str(p.relative_to(ROOT))
output=HERE/'run_001'
command=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
         '--contract',relative(HERE/'contract.json'),'--output',relative(output),
         '--timeout','90','--max-output-bytes','1048576','--max-threads','1']
for path in inputs:command+=['--input',relative(path)]
command+=['--result',relative(output/'result.json'),'--',sys.executable,'-B',
          relative(HERE/'tracking_audit.py'),'--result-file',relative(output/'result.json')]
run=subprocess.run(command,cwd=ROOT)
if run.returncode:raise SystemExit(run.returncode)
raise SystemExit(subprocess.run([sys.executable,str(SKILL/'scripts/validate_manifest.py'),
    str(output/'manifest.json'),'--root',str(ROOT)],cwd=ROOT).returncode)
