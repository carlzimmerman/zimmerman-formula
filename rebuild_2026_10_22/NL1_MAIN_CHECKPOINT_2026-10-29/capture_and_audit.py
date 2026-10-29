import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import hashlib,json,shutil,resource,signal,time,datetime,subprocess
import numpy as np
resource.setrlimit(resource.RLIMIT_CPU,(90,90));signal.alarm(120)
p=Path(__file__).resolve().parent;r=p.parents[1];reb=p.parent;src=reb/'NL1_native_level_L';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();t0=time.monotonic()
items=[(src/'nl1_native_level_results.json','main_results.json'),(src/'nl1_native_level.out','main.out'),(src/'nl1_native_level.py','main_source.executed.py'),(src/'FROZEN_CRITERIA.md','FROZEN_CRITERIA.original.md'),(src/'AMENDMENTS.md','AMENDMENTS.original.md'),(src/'run1_pickle_error.log','run1_pickle_error.txt'),(reb/'LEE1_look_elsewhere/lee1.py','lee1_harness.executed.py')]
before={str(s.relative_to(r)):sha(s) for s,d in items}
for s,d in items:
 dest=p/d
 if dest.exists():assert sha(dest)==sha(s),'Never overwrite a captured main with a later run'
 else:shutil.copyfile(s,dest)
 assert sha(dest)==before[str(s.relative_to(r))]
assert all(sha(r/k)==h for k,h in before.items())
f=p/'main_results.json';j=json.loads(f.read_text());out=(p/'main.out').read_text();checks={'main_out_completion_hash':('results sha256 '+sha(f)) in out,'four_main_controls':len(j['checks'])==4 and all(j['checks'].values()),'non_mutated_main':j['mutate'] is False}
priorpath=reb/'NATIVE_PARTIAL_2026-10-28/measurement_007_nine/results.json';prior=json.loads(priorpath.read_text());priorhash=sha(priorpath);keys=['cf','rvir','rconv','rm2','n_inside_rm2','c_nfw_fit','seed','ng','N'];checks['all_nine_identity_and_measurement_reproduction']=set(j['runs'])=={f'M1e12_s{i}_ng64' for i in range(1,10)} and all(j['runs'][f'M1e12_s{i}_ng64']['flag']=='ok' and all(j['runs'][f'M1e12_s{i}_ng64'][k]==prior['runs'][str(i)][k] for k in keys) for i in range(1,10))
cf=[j['runs'][k]['cf'] for k in sorted(j['runs'])];a2=prior['A2'];median=float(np.median(cf));ratio=median/a2['1e+12'];level=round(7.31*ratio,4);rng=np.random.default_rng(20261028);boot=[np.median(rng.choice(cf,len(cf))) for _ in range(2000)];ci=[round(7.31*float(np.percentile(boot,q))/a2['1e+12'],4) for q in (16,84)];checks['median_ratio_and_frozen_bootstrap']=median==j['c64'] and ratio==j['R'] and level==j['L_nat'] and ci==j['L68'];checks['finite_measurements_and_bootstrap']=bool(np.isfinite(cf).all() and np.isfinite(boot).all())
pc=j['grades']['PRIMARY']['fails_canonical'];verdict='L DERIVED: THE NATIVE LEVEL PASSES' if not pc else 'NATIVE LEVEL FAILS: '+', '.join(pc)
if ci[0]<4.17 and ci[1]>3.64 and not (3.64<=ci[0] and ci[1]<=4.17):verdict+=' [CONVERGENCE INCONCLUSIVE]'
checks['frozen_verdict_reconstruction']=verdict==j['verdict'];checks['fixed_T_scope']=j['grades']['PRIMARY']['T']==12.3 and j['grades']['CL3_T']['L']==level
captured={str((p/d).relative_to(r)):sha(p/d) for s,d in items};checks['captured_files_stable']=all(sha(r/k)==v for k,v in captured.items());checks['prior_measurement_stable']=sha(priorpath)==priorhash
record=dict(status='MAIN_COMPLETE_VALIDATION_PARTIAL',checks=checks,observed_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),repository_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),original_observed_sha256=before,captured_sha256=captured,prior_measurement_sha256=priorhash,audit_source_sha256=sha(Path(__file__)),criteria_sha256=sha(p/'CRITERIA.md'),measurement=dict(c64=median,R=ratio,L_nat=level,L68=ci),main_verdict=verdict,main_grades=j['grades'],pending_controls=['byte-identical rerun','mutation K1 rejection/exit record'],corrected_CSM1_regrade=False,robust_derived_L=False,runtime_seconds=time.monotonic()-t0,scope='Completed frozen legacy main only; partial validation, no new physical model fit or full-model corrected linked-T claim')
(p/'audit.json').write_text(json.dumps(record,indent=2)+'\n');print(record['status'],len(checks),all(checks.values()),level,ci);assert all(checks.values())
