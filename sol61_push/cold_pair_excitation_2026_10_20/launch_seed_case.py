"""Predeclare and run one quasistatic-chi initial-data comparison."""
from pathlib import Path
import json,subprocess,sys
here=Path(__file__).resolve().parent;root=here.parents[1]
seed_dir=Path(sys.argv[1]).resolve();K=int(sys.argv[2]);name=f'dressed_K{K}'
audit=seed_dir/'results.json';a=json.loads(audit.read_text())
row=next(x for x in a['rows'] if x['nominal_K']==K)
seed=seed_dir/row['snapshot_file'];out=here/(name+'_run_001')
case={'kind':'evolution','nominal_K':K,'omega':a['reference_omega'],
      'seed':str(seed.relative_to(root)),'seed_audit':str(audit.relative_to(root)),
      'evolution':{'nr':188,'nz':480,'dx':.75,'dt':.005,'T':240,'snapshot_interval':10},
      'bounds':{'E_relative_max':.0002,'Q_relative_max':1e-9},
      'interpretation':'Prepared quasistatic-chi Cauchy data at a nominal linear-coordinate amplitude; actual Q/E retained. Not a nonlinear mode or formation history.'}
cp=here/(name+'_case.json');cf=here/(name+'_contract.json')
if cp.exists() or cf.exists():raise FileExistsError('case/contract already frozen')
cp.write_text(json.dumps(case,indent=2)+'\n')
inputs=[here/'seed_driver.py',here/'launch_seed_case.py',here/'pair_axisym_seed.c',
        here/'pair_axisym_seed',here/'pair_axisym_v2.c',here/'build_seed_solver.py',
        here/'build_receipt_seed.json',here/'seed_loader_green_run_001/manifest.json',
        here/'profile_Q80000.bin',cp,seed,audit,seed_dir/'manifest.json']
arts=[str(p.relative_to(root)) for p in inputs]
contract={'claim_id':f'CE-QUASISTATIC-CHI-SEED-EVOLUTION-K{K}-2026-10-20',
 'mathematics':{'assertion_tested':'Evolve explicitly audited full-field initial data with the same conservative FV equations; measure E/Q conservation and finite inventories before separate conditional coordinate analysis.',
  'coefficient_domain':'Binary64 five-real-field cylindrical finite volumes and kick-drift-kick',
  'conventions':'Only initial chi/chi_dot were prepared through an explicit elliptic minimization/tangent solve; no added damping or constrained chi evolution. Loaded t0 full fields/velocities. Nominal coordinate is not accepted nonlinear energy and seed charges vary.',
  'inputs':['Pinned audited full Cauchy state','Replay-controlled initializer','Fixed prior action'],
  'bounds':case,
  'non_claims':['No energy-matched or fixed-Q nonlinear normal mode','No independent measurement of nonlinear mode damping from nominal K alone',
                'No galaxy capture law, orbital J, population selector or four-dwarf closure','No continuum/long-time escape theorem']},
 'execution_artifacts':arts,
 'software':[{'name':'Python','version':'3.9.6'},{'name':'NumPy','version':'1.26.2'},
             {'name':'Compiler','version':json.loads((here/'build_receipt_seed.json').read_text())['compiler']}],
 'randomness':{'used':False,'generator':'','seed':None}}
cf.write_text(json.dumps(contract,indent=2)+'\n')
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
argv=['python3',runner,'--root',str(root),'--contract',str(cf.relative_to(root)),
      '--output',str(out.relative_to(root)),'--timeout','180','--max-cpu-seconds','120',
      '--max-threads','1','--max-output-bytes','1048576']
for p in arts:argv+=['--input',p]
results=[out/'results.json']
results.extend(out/'evolution'/x for x in ['log.jsonl','enclosed_energy.jsonl','solver_stdout.txt','solver_stderr.txt'])
results.extend(out/'evolution'/f'snap_t{t*1000:09d}.bin' for t in range(0,241,10))
for p in results:argv+=['--result',str(p.relative_to(root))]
argv+=['--','python3',str((here/'seed_driver.py').relative_to(root)),str(cp.relative_to(root)),str(out.relative_to(root))]
raise SystemExit(subprocess.run(argv,cwd=root).returncode)
