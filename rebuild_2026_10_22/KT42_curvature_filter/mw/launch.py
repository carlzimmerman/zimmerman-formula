"""Create prospective contract and invoke the bounded computation runner."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
ap=argparse.ArgumentParser()
ap.add_argument('name')
ap.add_argument('arguments',nargs=argparse.REMAINDER)
args=ap.parse_args()
if args.arguments and args.arguments[0]=='--': args.arguments=args.arguments[1:]
old=json.loads((ROOT/'rebuild_2026_10_22/KT40_mechanism/mw/force_contract.json').read_text())
deps=old['execution_artifacts']+[str(p.relative_to(ROOT)) for p in [HERE/'launch.py',HERE/'calculate.py',HERE/'filtered_model.py',HERE.parent/'PLAN.md']]
deps=list(dict.fromkeys(deps))
contract=dict(claim_id='KT42_CURVATURE_FILTER_MW_'+args.name.upper(),
 mathematics=dict(assertion_tested='Verify finite energy/heat identities or evaluate two unchanged KT39 baryon witnesses at the declared Gaussian curvature widths; no population exclusion.',
 coefficient_domain='IEEE754 float64; sparse weighted finite adjoints',
 conventions='KT39 units and full action; gradient unfiltered, Hessian of heat-filtered potential. Numerical backward-Euler heat tends to isotropic Gaussian; heat-step and spatial convergence separate.',
 inputs=['KT39 fixed baryons/a0/cuts/p9/8/ell3kpc','KT42 PLAN.md width list'],
 bounds=dict(arguments=args.arguments,wall_seconds=1800,cpu_seconds=1750,threads=1,
 checks=dict(adjoint=1e-12,energy_difference=2e-7,zero_width=1e-13,gaussian_error_over_peak=.004,reciprocity=1e-6)),
 non_claims=['No global novelty proof','No viability inferred from primary MW cuts alone','Two witnesses are not an exhaustive baryon population scan','No relativistic, lensing, cosmological or microphysical completion']),
 execution_artifacts=deps,software=old['software'],randomness=dict(used=False,generator='',seed=None))
cp=HERE/(args.name+'_contract.json')
if cp.exists():raise FileExistsError(cp)
cp.write_text(json.dumps(contract,indent=2)+'\n')
out=HERE/args.name
argv=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),'--contract',str(cp),'--output',str(out.relative_to(ROOT)),'--result',str((out/'results.json').relative_to(ROOT)),'--timeout','1800','--max-cpu-seconds','1750','--max-output-bytes','4194304','--max-threads','1']
for dep in deps:argv+=['--input',dep]
argv+=['--',sys.executable,str(HERE/'calculate.py'),'--output',str(out/'results.json')]+args.arguments
sys.exit(subprocess.run(argv).returncode)
