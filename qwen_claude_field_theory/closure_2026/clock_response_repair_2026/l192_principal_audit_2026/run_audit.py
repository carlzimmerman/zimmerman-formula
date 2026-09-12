#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BRIDGE=HERE.parent/'cosmological_bridge_2026'
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit')
inputs=[HERE/name for name in ('principal_audit.py','test_principal_audit.py','contract.json','run_audit.py')]
inputs += [ROOT/'fable_independent_2026'/name for name in ('L192_gradient_criticality.py','L192_results.json')]
inputs += [BRIDGE/name for name in ('radiation_probe.py','background_evolve.py','transfer_evolve.py','transfer_jets.py','derive.py','radiation_002/result.json')]
inputs += [HERE.parent/'nonlinear_evolution_2026/constitutive.py']
relative=lambda p:str(p.relative_to(ROOT))
output=HERE/'run_001'
command=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
         '--contract',relative(HERE/'contract.json'),'--output',relative(output),
         '--timeout','120','--max-output-bytes','1048576','--max-threads','1']
for path in inputs:
    command+=['--input',relative(path)]
command+=['--result',relative(output/'result.json'),'--',sys.executable,'-B',relative(HERE/'principal_audit.py'),
          '--result-file',relative(output/'result.json')]
print('EXECUTION ARGV:',repr(command),flush=True)
result=subprocess.run(command,cwd=ROOT)
print('EXPERIMENT EXIT:',result.returncode,flush=True)
if result.returncode:
    raise SystemExit(result.returncode)
result=subprocess.run([sys.executable,str(SKILL/'scripts/validate_manifest.py'),str(output/'manifest.json'),
                       '--root',str(ROOT)],cwd=ROOT)
print('VALIDATION EXIT:',result.returncode,flush=True)
raise SystemExit(result.returncode)
