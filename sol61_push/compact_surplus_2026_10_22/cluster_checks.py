import json,argparse
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
root=Path('campaign_fresh_gravity/CFG687_erass1_shear_stack');d=np.load(root/'cfg687_percluster.npz');ref=json.loads((root/'cfg687_results.json').read_text())
D=np.nan_to_num(d['D']);E=d['E'];W=np.where(np.isfinite(E)&(E>0),1/E**2,0);n=len(D)
edges=np.geomspace(.15,3,9);R=np.sqrt(edges[:-1]*edges[1:]);unit=1/(np.pi*(R*1e6)**2)
bands={'INNER':[0,1,2],'MID':[3,4,5],'OUTER':[6,7]};patch=np.empty(n,int);patch[np.argsort(d['ra'])]=np.arange(n)*30//n
checks=[];rows=[]
def ck(name,b,v):checks.append(dict(name=name,passed=bool(b),value=v));print(name,b,v)
def amp(base,sel):return {k:float(np.sum(W[sel][:,j]*D[sel][:,j])/np.sum(W[sel][:,j]*base[sel][:,j])) for k,j in bands.items()}
b=amp(d['PL'],np.ones(n,bool));expected=ref['A']['canonical|b0.67|rc0.15|f0.20'];err=max(abs(b[k]-expected[k][0]) for k in bands)
ck('baseline_reproduced',err<1e-10,err)
for name in ['PN','PL']:
 base=d[name]
 for scale in ['constant_mass','gas_scaled']:
  template=np.broadcast_to(unit,D.shape).copy()*(1e13 if scale=='constant_mass' else d['mg'][:,None])
  def fit(sel,data=D):
   j=bands['MID'];return np.sum(W[sel][:,j]*(data-base)[sel][:,j])/np.sum(W[sel][:,j]*template[sel][:,j])
  all_=np.ones(n,bool);q=fit(all_);model=base+q*template;A=amp(model,all_)
  reps=[];qs=[]
  for i in range(30):
   sel=patch!=i;qi=fit(sel);qs.append(qi);reps.append(amp(base+qi*template,sel))
  errors={k:float(np.sqrt(29/30*np.sum((np.array([r[k] for r in reps])-np.mean([r[k] for r in reps]))**2))) for k in bands}
  m=q*(np.ones(n)*1e13 if scale=='constant_mass' else d['mg'])
  rows.append(dict(baseline=name,scaling=scale,coefficient=float(q),mass_median_Msun=float(np.median(m)),mass_min_Msun=float(min(m)),mass_max_Msun=float(max(m)),bands={k:dict(A=A[k],jackknife_sigma=errors[k],Z=(A[k]-1)/errors[k] if errors[k]>1e-12 else None) for k in bands}))
  inj=fit(all_,base+3*template)
  ck('injection_'+name+'_'+scale,abs(inj-3)<1e-12,inj)
  ck('mid_fitted_'+name+'_'+scale,abs(A['MID']-1)<1e-12,A['MID'])
G=6.67430e-11;Msun=1.98847e30;kpc=3.085677581491367e19;ell=.4404221297174536*kpc
units=[dict(a0=a0,M0_Msun=a0*ell**2/G/Msun) for a0 in [9.3603e-11,1.1312e-10]]
rot=((1.1**2-1)*(200e3)**2*(10*kpc)/G/Msun)
ck('unit_pointmass',abs(1e13*unit[0]*np.pi*(R[0]*1e6)**2/1e13-1)<1e-14,float(1e13*unit[0]))
out=dict(checks=checks,rows=rows,R_Mpc=R.tolist(),baseline=b,units=units,rotation_mass_limit_Msun=rot,non_claims=['PL plus core is not a global action solution','No mass selector','No full covariance likelihood','No relativistic metric derivation'])
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(rows,indent=2));print('units',units,'rotation_limit',rot)
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
