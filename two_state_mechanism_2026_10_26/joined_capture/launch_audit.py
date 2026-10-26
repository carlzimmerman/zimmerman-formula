from pathlib import Path
import json,subprocess
b=Path('two_state_mechanism_2026_10_26/joined_capture');ins=[str(x) for x in sorted(b.glob('*.py'))]+[str(b/'DESIGN.md')]+[str(x) for pattern in ['run_*/results.json','run_*/*.npz','inputs/*'] for x in sorted(b.glob(pattern))]+[str(b.parent/'continuum/run_physical_radial25/h2+.molden')]+[str(b.parent/'nuclear_flux'/('run_capture_R%d'%R)/'h2+.molden') for R in [3,4]]
c=json.loads((b/'map_contract.json').read_text());c['claim_id']='JOINED_CAPTURE_AGGREGATE';c['execution_artifacts']=ins;c['mathematics'].update(assertion_tested='Aggregate finite operator, mapping and convergence evidence; hash all auxiliary arrays',inputs=ins,bounds=dict(nuclear_runs=13,map_cases=27,nonlocal_energies=2),non_claims=['No complete physical DR calculation','No new photon trajectory or galaxy separation'])
p=b/'audit_contract.json';assert not p.exists();p.write_text(json.dumps(c,indent=2)+'\n');r=b/'run_audit';argv=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root','.','--contract',str(p)]
for x in ins:argv+=['--input',x]
argv+=['--output',str(r),'--result',str(r/'results.json'),'--timeout','60','--max-threads','1','--','python3',str(b/'audit.py'),'--output',str(r/'results.json')];subprocess.run(argv,check=True)
