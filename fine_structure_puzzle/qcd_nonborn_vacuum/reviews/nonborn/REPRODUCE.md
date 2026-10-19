# Reproduce the independent checks

From `/Users/carlzimmerman/new_physics/zimmerman-formula`, choose fresh output
names. This constructs a fixed local Python command; it does not execute a
command stored in a manifest. The input lists are the authored contracts.

```bash
python3 - <<'PY'
from pathlib import Path
import json, subprocess
base=Path('fine_structure_puzzle/qcd_nonborn_vacuum/reviews/nonborn')
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
for contract,script,out,wall,cpu in [
 ('COMPUTATION_CONTRACT.json','independent_check.py','run_REPRODUCE',240,220),
 ('SYMBOLIC_CONTRACT.json','independent_symbolic.py','symbolic_REPRODUCE',30,20)]:
 cfg=json.loads((base/contract).read_text())
 args=['python3',runner,'--root',str(Path.cwd()),'--contract',str(base/contract)]
 for path in cfg['execution_artifacts']: args+=['--input',path]
 args+=['--output',str(base/out),'--result',str(base/out/'result.json'),
        '--timeout',str(wall),'--max-output-bytes','1048576',
        '--max-cpu-seconds',str(cpu),'--max-threads','1','--',
        'python3',str(base/script),str(base/out/'result.json')]
 subprocess.run(args,check=True)
PY
```

Validate each new manifest with
`python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula`.

The symbolic contract intentionally includes the original independent
run_001/result.json, whose archived-source checks authenticate its real
formulas. It is a fixed reviewed input, not a newly synthesized replacement.
