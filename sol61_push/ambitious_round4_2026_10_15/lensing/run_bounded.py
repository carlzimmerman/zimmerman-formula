"""Write a bounded contract before dispatch, preserving each fresh run."""
import argparse,json,subprocess,platform,sys
from pathlib import Path
import numpy,scipy
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[2]
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts')
p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--script',required=True);p.add_argument('--input',action='append',default=[]);p.add_argument('--result',action='append',default=['result.json']);p.add_argument('args',nargs=argparse.REMAINDER);a=p.parse_args()
out=BASE/a.name
if out.exists():raise SystemExit('Refuse existing run directory')
artifacts=[BASE/'model.py',BASE/a.script,BASE/'POST_DATA_CRITERIA.md',BASE/'UNIT_DISPOSITION.md']+sorted((BASE/'inputs').glob('*'))+[ROOT/v for v in a.input]
artifacts=list(dict.fromkeys(str(v.relative_to(ROOT)) for v in artifacts))
contract=dict(claim_id='ROUND4-LENSING-'+a.name,mathematics=dict(assertion_tested='Bounded post-data exact-law finite-catchment versus no-edge projection and full-covariance fit; inspect result for numerical controls and scientific interpretation.',coefficient_domain='IEEE754 float64 numpy/scipy',conventions='POST_DATA_CRITERIA.md and UNIT_DISPOSITION.md; native_h primary, legacy_physical secondary; h70=1 physical-data footing; finite-band smoothed native P.',inputs=artifacts,bounds=dict(max_wall_seconds=60,max_cpu_seconds=55,numerical_threads=1,simulation_steps=0,max_mass_optimizations_per_command=12,mass_range_log10_Msun=[9.5,12],command_arguments=a.args),non_claims=['No prospective claim or calibrated selection p value.','No full theory or inventory closure.','Old K2 remains failed.']),execution_artifacts=artifacts,software=[dict(name='Python',version=platform.python_version()),dict(name='numpy',version=numpy.__version__),dict(name='scipy',version=scipy.__version__),dict(name='platform',version=platform.platform())],randomness=dict(used=False,generator='',seed=None))
cp=BASE/(a.name+'_contract.json');cp.write_text(json.dumps(contract,indent=2)+'\n')
argv=['/opt/homebrew/bin/python3.12',str(SKILL/'run_experiment.py'),'--root',str(ROOT),'--contract',str(cp)]
for f in artifacts:argv+=['--input',f]
argv+=['--output',str(out.relative_to(ROOT))]
for v in a.result:argv+=['--result',str((out/v).relative_to(ROOT))]
argv+=['--timeout','60','--max-cpu-seconds','55','--max-output-bytes','1048576','--max-threads','1','--',sys.executable,str(BASE/a.script)]
extra=a.args[1:] if a.args[:1]==['--'] else a.args
argv += [v.replace('{OUT}',str(out)) for v in extra]
run=subprocess.run(argv)
subprocess.run(['/opt/homebrew/bin/python3.12',str(SKILL/'validate_manifest.py'),str(out/'manifest.json'),'--root',str(ROOT)],check=True)
raise SystemExit(run.returncode)
