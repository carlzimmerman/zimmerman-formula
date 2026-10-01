#!/usr/bin/env python3
"""One explicit bounded run, copied-input hashes, no automatic job queue."""
from pathlib import Path
import subprocess,sys,os,json,time,hashlib,platform,datetime,shutil
HERE=Path(__file__).resolve().parent; MIRROR=HERE/'mirror'
name=sys.argv[1]; mut=len(sys.argv)>2 and sys.argv[2]=='mutate'; label=sys.argv[3] if len(sys.argv)>3 else 'verified'
key=name+('_MUTATE' if mut else '')+'_'+label; out=HERE/'runs'/key
out.mkdir(parents=True,exist_ok=False)
source=HERE/f'{name}.py' if (HERE/f'{name}.py').exists() else MIRROR/'real_research/cross_thread_review_2026_09_26'/f'{name}.py'
env=os.environ.copy(); env.update(MUTATE='1' if mut else '0',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='/private/tmp/handoff-classy-20260927/site',L357_THREADS='2')
argv=[sys.executable,str(source)]; start=time.time(); started=datetime.datetime.now(datetime.timezone.utc).isoformat(); before=hashlib.sha256(source.read_bytes()).hexdigest()
with (out/'stdout.txt').open('w') as so,(out/'stderr.txt').open('w') as se:
 try:
  p=subprocess.run(argv,cwd=MIRROR,env=env,stdout=so,stderr=se,timeout=1800); code=p.returncode; status='completed' if code==0 else 'failed'
 except subprocess.TimeoutExpired: code=124; status='timeout'
elapsed=time.time()-start
if name=='frame_tide_audit': result=HERE/f"frame_tide_results{'_MUTATE' if mut else ''}.json"
else: result=source.parent/f"{name}_results{'_MUTATE' if mut else ''}.json"
parsed={}
if result.exists() and result.stat().st_mtime>=start:
 shutil.copy2(result,out/'results.json'); parsed=json.loads(result.read_text())
outputs=[{'path':str(p.relative_to(HERE)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in out.glob('*') if p.is_file()]
rec={'schema_version':1,'claim_id':'HR01-T/'+key,'repository':{'commit':'48905ae11213afcb9ff1b7726530bb5dd1933fe3','dirty':True},'command':argv,'environment':{'software':['Python '+sys.version,'numpy 1.26.2','scipy 1.11.4','sympy 1.14.0','CLASS 3.3.4.0 local rebuilt vanilla'],'hardware':platform.platform()},'mathematics':{'assertion_tested':'Reproduce specified XR36 finite assertions or independent frame/tide controls; mutation changes its named headline','coefficient_domain':'float64 plus symbolic SymPy identities where present','conventions':'potential-gradient field, P2 nu; a0=9.3603e-11 and 1.1312e-10; kappa=1/2 fitted','inputs':[str(source),'mirror_sources.json'],'bounds':{'wall_seconds':1800,'footings':2,'web_grid_if_used':'128^3,64 Mpc/h,seed19','frame_if_used':'96x192 sphere quadrature; 48 cells seed361','XR36_range':'exact unmodified source script, no reduced bounds'},'non_claims':['Not a covariant completion or proof of global well-posedness','Not a derived kappa or joint observational theory pass']},'randomness':{'used':name in ('XR36_web_lensing','frame_tide_audit'),'generator':'numpy default_rng PCG64','seed':361 if name=='frame_tide_audit' else 19},'run':{'started_at':started,'runtime_seconds':elapsed,'exit_status':code},'outputs':outputs,'checks':list(parsed.get('checks',{}).values()),'result':status+'; '+str(parsed.get('verdict','no result JSON produced')),'residual_risks':['Schema v1 does not machine-enforce dependency completeness; independent mirror hashes retained','Library thread limit is cooperative; XR36 source sets 2','Finite proxy and frozen-domain limitations are in report'],'source_hash_before':before,'source_hash_after':hashlib.sha256(source.read_bytes()).hexdigest(),'runtime_environment':{'PYTHONPATH':env['PYTHONPATH'],'MUTATE':env['MUTATE'],'L357_THREADS':env['L357_THREADS']}}
(out/'manifest.json').write_text(json.dumps(rec,indent=2)); print(key,status,code,elapsed,parsed.get('verdict')); sys.exit(code)
