"""Create bounded-run contract from actual pilot-read dependency closure, then launch audited run."""
import sys,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[3];D=pathlib.Path(__file__).resolve().parent
j=json.loads((D/'run_002/results.json').read_text());paths={}
for x in j['baseline'].values():
 if isinstance(x,dict):paths.update(x.get('inputs',{}))
inputs=sorted([str(pathlib.Path(p).relative_to(ROOT)) for p in paths if pathlib.Path(p).is_relative_to(ROOT)])
inputs += [str((D/x).relative_to(ROOT)) for x in ['launch_audited.py','calibrate_audited.py','FROZEN_CRITERIA.md','ASSUMPTION_LEDGER.md','AMENDMENTS.md']]
inputs += [str((D.parent/'FROZEN_CRITERIA.md').relative_to(ROOT))]
inputs=sorted(set(inputs));outname=sys.argv[1];extras=sys.argv[2:];out=D/outname;program='calibrate_audited.py'
if '--skip-baseline' in extras:
 program='calibrate_replay.py';rp=D/'run_003_audited/results.json';rj=json.loads(rp.read_text());assert rj['checks']['baseline'] and rj['checks']['cached_baseline']
 inputs+= [str((D/program).relative_to(ROOT)),str(rp.relative_to(ROOT))];inputs=sorted(set(inputs));extras+=['--reference',str(rp.relative_to(ROOT))]
contract=dict(claim_id='CSM1_CORRECTED_CALIBRATION_'+outname,mathematics=dict(assertion_tested='Reproduce old baseline and actual primary corrected same-core/switch calibration on both footings at prespecified levels; independent column logs and actual flag mutation control',coefficient_domain='IEEE754binary64',conventions='X43 exactEPS perbackground; X53 retained coarse table; original units/floors; canonical/alt separate; same mass-dependent S9 core function for amplitude and flag',inputs=['175SPARC each background/footing','63groups','15cluster keys at2hcells perfoot','KiDS isolated-lens actual positiveweight inventory'],bounds={'levels':extras,'footings':['canonical','alt'],'memory_observed_lt_GB':1},non_claims=['Not EPS/physical basin/native convergence validation','Dwarfs and MW delegated','No global-L impossibility from three cells']),execution_artifacts=inputs,software=[{'name':'Python','version':'3.13.9'},{'name':'NumPy','version':'1.26.4'},{'name':'SciPy','version':'1.14.1'},{'name':'classy','version':'v3.3.4'}],randomness={'used':True,'generator':'numpy PCG64','seed':20261027},external_input_hashes={p:h for p,h in paths.items() if not pathlib.Path(p).is_relative_to(ROOT)},external_input_provenance='External files are read-hashed before/after by child; full actual read closure is declared in input_hashes.json. Runner input list covers project-contained dependency closure from baseline.')
cp=D/(outname+'_contract.json');cp.write_text(json.dumps(contract,indent=2)+'\n')
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
cmd=[sys.executable,runner,'--root',str(ROOT),'--contract',str(cp),'--output',str(out.relative_to(ROOT)),'--result',str((out/'results.json').relative_to(ROOT)),'--result',str((out/'input_hashes.json').relative_to(ROOT)),'--timeout','900','--max-output-bytes','1048576','--max-cpu-seconds','600','--max-threads','1']
for p in inputs:cmd+=['--input',p]
cmd+=['--','/opt/homebrew/Caskroom/miniconda/base/bin/python3','-I',str((D/program).relative_to(ROOT)),'--output',str(out.relative_to(ROOT))]+extras
print('Run:',outname,'project inputs',len(inputs),'external',len(contract['external_input_hashes']),flush=True)
raise SystemExit(subprocess.call(cmd,cwd=str(ROOT)))
