from pathlib import Path
import subprocess,sys,os,json,time,hashlib,platform,datetime
HERE=Path(__file__).resolve().parent
MIRROR=HERE/'mirror'
JOBS=[('XR36_gate_action',False),('XR36_gate_action',True),('XR36_bound_regions',False),('XR36_web_lensing',False),('XR36_bound_regions',True),('XR36_web_lensing',True)]
for name,mut in JOBS:
 key=name+('_MUTATE' if mut else '')
 out=HERE/'runs'/key; out.mkdir(parents=True,exist_ok=True)
 env=os.environ.copy(); env['MUTATE']='1' if mut else '0'; env['PYTHONDONTWRITEBYTECODE']='1'
 argv=[sys.executable,str(MIRROR/'real_research/cross_thread_review_2026_09_26'/f'{name}.py')]
 start=time.time()
 rec={'job':key,'argv':argv,'cwd':str(MIRROR),'base_head':'48905ae11213afcb9ff1b7726530bb5dd1933fe3','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'status':'running','source_sha256':hashlib.sha256(Path(argv[1]).read_bytes()).hexdigest(),'mutate':mut,'wall_cap_seconds':1800,'thread_cap':'source sets numerical-library thread variables to 2; cooperative'}
 (out/'provenance.json').write_text(json.dumps(rec,indent=2)); print('START',key,flush=True)
 with (out/'stdout.txt').open('w') as so,(out/'stderr.txt').open('w') as se:
  try:
   p=subprocess.run(argv,cwd=MIRROR,env=env,stdout=so,stderr=se,timeout=1800); rec.update(exit_code=p.returncode,status='completed' if p.returncode==0 else 'failed')
  except subprocess.TimeoutExpired: rec.update(exit_code=None,status='timeout')
 rec['elapsed_seconds']=time.time()-start
 result=MIRROR/'real_research/cross_thread_review_2026_09_26'/f"{name}_results{'_MUTATE' if mut else ''}.json"
 if result.exists():
  import shutil
  shutil.copy2(result,out/'results.json'); rec['result_sha256']=hashlib.sha256(result.read_bytes()).hexdigest()
 (out/'provenance.json').write_text(json.dumps(rec,indent=2)); print('END',key,rec['status'],rec['elapsed_seconds'],flush=True)
