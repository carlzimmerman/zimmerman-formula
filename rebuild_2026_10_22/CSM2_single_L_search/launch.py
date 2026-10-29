"""Launch the fixed finite necessary-constraint grid with pinned dependencies."""
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CSM=HERE.parent/'CSM1_consistent_core_switch/calibration'
old=json.loads((CSM/'run_003_audited/manifest.json').read_text())
inputs=set(old['execution_artifacts'])
inputs.update(str(p.relative_to(ROOT)) for p in [HERE/'TARGET.md',HERE/'search.py',HERE/'launch.py',
    CSM/'calibrate_replay.py',CSM/'run_003_audited/results.json'])
contract=dict(claim_id='CSM2_NECESSARY_GRID',mathematics=dict(
    assertion_tested='Unchanged corrected group grade and necessary lensing delta-law criterion at 15 predeclared single-L values',
    coefficient_domain='IEEE binary64',conventions='Both footings separate; canonical necessary intersection; original full covariance and corrected same-core selector',
    inputs=['TARGET.md fixed grid','CSM1 baseline, corrected scorer and cached two-halo template'],
    bounds=dict(levels=15,groups=63,wall_seconds=1800,CPU_seconds_per_process=1200),
    non_claims=['No continuous-L exclusion','No candidate passes all criteria merely by surviving necessary tests','No new fitted parameter']),
    software=[dict(name='Python',version='3.13.9'),dict(name='NumPy',version='1.26.4'),dict(name='SciPy',version='1.14.1'),dict(name='classy',version='v3.3.4')],
    randomness=dict(used=True,generator='Inherited fixed source PCG64 controls',seed=20261027))
cp=HERE/'contract.json'
cp.write_text(json.dumps(contract,indent=2)+'\n')
out=HERE/sys.argv[1]
cmd=[sys.executable,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py',
    '--root',str(ROOT),'--contract',str(cp),'--output',str(out.relative_to(ROOT)),
    '--result',str((out/'results.json').relative_to(ROOT)),'--timeout','1800','--max-cpu-seconds','1200',
    '--max-output-bytes','1048576','--max-threads','1']
for p in sorted(inputs):cmd+=['--input',p]
cmd+=['--','/opt/homebrew/Caskroom/miniconda/base/bin/python3','-I',str(HERE/'search.py'),'--output',str(out)]
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
