"""Launch bounded immutable version experiments with complete declared closure."""
import sys,json,subprocess,numpy,scipy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent
name,script,*extra=sys.argv[1:];out=HERE/('run_'+name);rout=out.relative_to(ROOT)
base=['reviews/weak_completion_2026_11_04/vectors/basis.py','reviews/weak_completion_2026_11_04/vectors/'+script,'reviews/collision_completion_2026_11_04/cascades/network.py','reviews/finite_matching_2026_11_01/two_loop/model.py','reviews/three_priorities_2026_11_01/spectrum_pressure/spectrum.py','reviews/collision_completion_2026_11_04/cascades/capture.py']
inputs=list(dict.fromkeys(base+extra));contract=HERE/(name+'_contract.json')
contract.write_text(json.dumps(dict(claim_id='CC11_VECTOR_'+name.upper(),mathematics=dict(assertion_tested='Bounded actual gauge-current and polarized vector transport computation; only checks explicitly returned are claimed',coefficient_domain='float64/complex128',conventions='mu units, canonical scalar/Weyl/vector fields; physical Y=gWf/(2pi2)',inputs=inputs,bounds=dict(wall_seconds=240,cpu_seconds=235,threads=1),non_claims=['No full candidate viability claim; finite tested domain only']),execution_artifacts=inputs,software=[dict(name='Python',version=sys.version),dict(name='numpy',version=numpy.__version__),dict(name='scipy',version=scipy.__version__)],randomness=dict(used=False,generator='',seed=None)),indent=2)+'\n')
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
cmd=[sys.executable,runner,'--root',str(ROOT),'--contract',str(contract),'--output',str(rout),'--result',str(rout/'result.json'),'--result',str(rout/'metrics.json'),'--timeout','240','--max-cpu-seconds','235','--max-threads','1']
for p in inputs:cmd+=['--input',p]
cmd+=['--',sys.executable,'-B','reviews/collision_completion_2026_11_04/cascades/capture.py',str(rout/'metrics.json'),'reviews/weak_completion_2026_11_04/vectors/'+script,str(rout/'result.json')]
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
