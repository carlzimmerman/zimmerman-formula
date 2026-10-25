import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,pathlib,numpy as np
from scipy.interpolate import CubicSpline
from sphere_v2 import Sphere
from budget import initial,shells
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];rows=[]
for jf in sorted(list((P/'runs').glob('*_v[23]_*.json'))+list((P/'runs').glob('*pulse*.json'))):
 meta=json.loads(jf.read_text());a=meta['parameters'];f=np.load(P/'runs'/(a['tag']+'.npz'));name=a['galaxy'];parent=ROOT/(f'sol61_push/cold_envelope_formation_2026_10_24/runs/{name}_escape_long_fields.npz' if name in ('draco','sextans') else f'sol61_push/cold_material_transport_2026_10_24/runs/{name}_matched_L8_fields.npz');old=np.load(parent);r,v,lm=[old[k] for k in ['r','initial','lm']];eta=meta['physical']['eta_code'];j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(r<21.8)&(abs(v[:,j])>1e-20);rv=r[valid];sp=CubicSpline(rv,eta*np.unwrap(np.angle(v[valid,j])))
 def phase(x,der=0):
  if der:return np.where(x<=rv[-1],sp(x,1),sp(rv[-1],1))
  return np.where(x<=rv[-1],sp(x),sp(rv[-1])+sp(rv[-1],1)*(x-rv[-1]))
 s=Sphere(a['ne'],a['nt'],a['nf'],eta=eta,phase=phase);u0=initial(s,old);selected=meta['history']
 if a.get('resume'):
  u0=np.load(P/'runs'/(a['resume']+'.npz'))['u'];start=meta['finite_transport_start'];selected=[h for h in selected if h['t']>=start]
 radii=meta['history'][0]['flux']['r'];b0=shells(s,u0,s.poisson(u0),radii);b1=shells(s,f['u'],f['phi'],radii);tt=np.array([h['t'] for h in selected]);ints={k:np.trapz([h['flux'][k] for h in selected],tt,axis=0) for k in ['mass','energy','Jz']}
 finite_error=None
 if 'finite_mass_transport' in meta:
  change=np.cumsum(np.sum(abs(f['u'])**2-abs(u0)**2,axis=(1,2)))[:-1];finite_error=float(np.max(abs(change+np.array(meta['finite_mass_transport']))))
 row=dict(finite_mass_budget_residual=finite_error,tag=a['tag'],galaxy=name,status=meta['status'],T=tt[-1],initial_shell=b0,final_shell=b1,net_outward_integral={k:v.tolist() for k,v in ints.items()},budget_residual={k:(np.array(b1[q])-b0[q]+ints[k]).tolist() for k,q in [('mass','M'),('energy','E_canonical'),('Jz','Jz')]},energy_budget_residual_over_transport=(abs(np.array(b1['E_canonical'])-b0['E_canonical']+ints['energy'])/np.maximum(abs(ints['energy']),1e-30)).tolist(),last=meta['history'][-1],peak_RSS_bytes=meta['peak_RSS_bytes']);rows.append(row)
(P/'analysis.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows:print(row['tag'],row['T'],row['last']['field_aperture_Msun'],'Eerr',row['last']['E_relative_error'],'budgets',row['budget_residual'])
