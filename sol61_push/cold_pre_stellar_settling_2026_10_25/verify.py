"""Recompute stored invariants and verify provenance; no physical success substitution."""
import argparse,json,hashlib,subprocess,sys,os,resource,time
from pathlib import Path
import numpy as np
from kernel import Solver
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);checks=[];start=time.monotonic()
 def check(name,ok):
  checks.append(dict(name=name,passed=bool(ok)))
  if not ok:raise AssertionError(name)
 for name in ['test_kernel.py','test_gated.py','test_pade9.py','test_prolongation.py']:
  p=subprocess.run([sys.executable,str(P/name)],capture_output=True,text=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'});(out/(name+'.log')).write_text(p.stdout+p.stderr);check(name,p.returncode==0)
 validators=[]
 for folder in sorted(P.iterdir()):
  mf=folder/'manifest.json'
  if not mf.exists():continue
  m=json.loads(mf.read_text());check(folder.name+' runner status accounted',(m['run']['status']=='failed' and m['run']['exit_status']==1) if folder.name=='prolong_001' else (m['run']['status']=='completed' and m['run']['exit_status']==0))
  for f in m['input_artifacts']:check(folder.name+' source '+f['path'],sha(ROOT/f['path'])==f['sha256']==f['sha256_after'])
  for f in m['outputs']:check(folder.name+' output '+f['path'],sha(ROOT/f['path'])==f['sha256'])
  if not (folder/'field.npz').exists():continue
  d=json.loads((folder/'result.json').read_text());check(folder.name+' own input stability',d['inputs_before']==d['inputs_after']);check(folder.name+' memory',d['peak_RSS_bytes']<750000000);check(folder.name+' local/solver gates',d['accepted_local_error_max']<=d['local_tolerance'] and d['accepted_solver_residual_max']<=1e-10)
  for f,v in d['raw_sha256'].items():check(folder.name+' raw '+f,sha(folder/f)==v)
  z=np.load(folder/'field.npz');uinfo=d['units'];s=Solver(d['ne'],eta=uinfo['eta_code'],vin=uinfo['vin_code'],alpha=d['alpha']);meta=json.loads((P.parent/'cold_full_envelope_data_2026_10_25/fit_002/result.json').read_text())['datasets'][d['galaxy']];aa=np.array(meta['tracer_scales_pc'])/uinfo['R_pc'];s.pb=sum(-uinfo['q']/len(aa)/np.sqrt(s.r*s.r+b*b) for b in aa);check(folder.name+' nodes',np.array_equal(z['r'],s.r) and np.array_equal(z['w'],s.w) and np.array_equal(z['p'],s.p))
  for i,t in enumerate(z['t']):
   u=z['u'][i];phi=s.phi(u);check(folder.name+' finite '+str(t),np.all(np.isfinite(u)));check(folder.name+' Phi '+str(t),np.max(abs(phi-z['phi'][i]))<1e-11);check(folder.name+' M '+str(t),abs(np.vdot(u,u).real/d['initial']['mass']-1)<=max(d['maxima']['mass']+1e-12,1e-8));check(folder.name+' E '+str(t),abs(s.energy(u,phi)-d['initial']['energy'])/d['initial']['energy_scale']<=max(d['maxima']['energy']+1e-10,1e-4))
  gates=dict(mass=1e-8,energy=1e-4,phase=.05,boundary=1e-4)
  if any(d['maxima'][k]>v for k,v in gates.items()):check(folder.name+' gate failure not hidden',d['status']=='spatial/invariant/boundary stop' and not d['history'][-1]['numerically_valid'])
  if 'resume_origin' in d:
   par=Path(d['resume_origin']['parent']);pd=json.loads((par/'result.json').read_text());pz=np.load(par/'field.npz');check(folder.name+' exact resumed field',np.array_equal(z['u'][0],pz['u'][-1]));check(folder.name+' invariant origin',d['initial']==pd['initial']);pz.close();parenthist={round(x['t'],10):x for x in pd['history']};childhist={round(x['t'],10):x for x in d['history']};check(folder.name+' inherited history',all(childhist.get(t)==v for t,v in parenthist.items()))
  hist=list({round(x['t'],10):x for x in d['history']}.values())
  qualified=[x['t'] for x in d['settling'] if x['qualifies']]
  check(folder.name+' first birth rule',d['birth_time']==(qualified[0] if qualified else None))
  for rec in d['settling']:
   window=[x for x in hist if rec['t']-1-1e-9<=x['t']<=rec['t']+1e-10];cc=np.array([x['cdf'] for x in window]);mm=np.array([x['cold_Mref'] for x in window]);rr=np.array([x['r50'] for x in window]);cd=float(np.max(np.ptp(cc,axis=0))/d['initial']['mass']);md=float(np.ptp(mm)/max(mm.mean(),1e-12));rd=float(np.ptp(rr)/rr.mean());qualifies=cd<=.01 and md<=.05 and rd<=.05
   check(folder.name+' settling '+str(rec['t']),rec['t']>=2 and len(window)>=20 and window[0]['t']<=rec['t']-1+1e-8 and max(np.diff([x['t'] for x in window]))<=.05000001 and all(x['numerically_valid'] for x in window) and np.isclose(cd,rec['CDF_range'],rtol=0,atol=1e-12) and np.isclose(md,rec['reference_mass_relative_range'],rtol=0,atol=1e-12) and np.isclose(rd,rec['r50_relative_range'],rtol=0,atol=1e-12) and qualifies==rec['qualifies'])
  if d['birth_time'] is None:check(folder.name+' no vacuous stellar pass',d['stellar_numerics_valid'] is None and not d['birth_controls'])
  z.close()
 # Detection controls operate on copies, never modify a saved physical result.
 d=json.loads((P/'Draco_base/result.json').read_text());z=np.load(P/'Draco_base/field.npz');u=z['u'][-1].copy();check('mass multiplication mutation rejected',abs(np.vdot(u*1.01,u*1.01).real/d['initial']['mass']-1)>1e-8);z.close();check('hash mutation rejected',hashlib.sha256(b'corrupt').hexdigest()!=d['raw_sha256']['field.npz'])
 check('audit self memory',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<750000000);check('audit child memory',resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss<750000000)
 result=dict(seconds=time.monotonic()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,child_peak_RSS_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,scope='integrity/operator/control audit, not a formation or convergence pass',checks=checks,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks));(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['passed','failed']}))
if __name__=='__main__':main()
