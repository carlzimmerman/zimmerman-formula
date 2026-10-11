import json,sys,itertools
from pathlib import Path
import numpy as np
import sympy as sp
P=Path('sol61_push'); checks=[]
def ck(n,b): checks.append([n,bool(b)])
s,a=sp.symbols('s a',positive=True);q=sp.sqrt(1-s*s/a**2);f=s/(a*a*(1+q))
ck('exact_radial_derivative',sp.simplify(sp.diff(f,s)-1/(a*a*q*(1+q)))==0)
ck('centre_limit',sp.simplify(sp.limit(f/s,s,0)-1/(2*a*a))==0)
def alpha(t,a):return t/(a*a*(1+np.sqrt(1-np.sum(t*t,axis=-1,keepdims=True)/a**2)))
def bound(m,R):
 q=np.sqrt(1-(m/R)**2);return 1/(R*R*q*(1+q))
rng=np.random.default_rng(11012)
for R in [1.01,1.1,2,4]:
 for rep in range(50):
  angles=rng.uniform(0,2*np.pi,2);r=rng.uniform(0,1,2);t=r[:,None]*np.column_stack([np.cos(angles),np.sin(angles)])
  sep=np.linalg.norm(t[0]-t[1]);m=max(r)
  diff=np.linalg.norm(alpha(t,R)[0]-alpha(t,R)[1]);ck(f'shell_{R}_{rep}',diff<=bound(m,R)*sep*(1+1e-10))
  radii=R*rng.uniform(1,4,20);weights=rng.uniform(.01,1,20)
  v=sum(w*alpha(t,aa) for w,aa in zip(weights,radii));ck(f'mixture_{R}_{rep}',np.linalg.norm(v[0]-v[1])<=weights.sum()*bound(m,R)*sep*(1+1e-10))
t=np.array([[.5,0],[-.5,0]]);diff=np.linalg.norm(alpha(t,2)[0]-alpha(t,2)[1])
ck('MUTATE_interior_lensing_zero',diff>.1)
ck('MUTATE_3D_exterior_not_projected_exterior',1-np.sqrt(1-(.5/2)**2)>0)
old=np.load(P/'gas_image_operator_2026_10_11/run_v2/operator.npz');gas=np.load(P/'gas_distance_2026_10_11/run/operator.npz');theta=old['theta_arcsec'];r=np.linalg.norm(theta,axis=1)
g=gas['ICRS_linear_alpha_infinity_native'];w=gas['source_weight_native_PM_flat'];meta=json.loads((P/'gas_distance_2026_10_11/run/results.json').read_text());rows=json.loads((P/'native_lensing_2026_10_11/run_v2/results.json').read_text())['gold_rows']
pairs=[(i,j) for i,j in itertools.combinations(range(len(rows)),2) if rows[i]['feature']==rows[j]['feature']]
unit=4*6.67430e-11*1.98847e30/(299792458.**2*meta['distance_native_Mpc']*3.085677581491367e22)*206264.80624709636**2
out=[]
for mult in [1.1,1.5,2,4]:
 R=mult*r.max();v=[]
 for i,j in pairs:
  delta=theta[i]-theta[j]-w[i]*(g[i]-g[j]);B=np.linalg.norm(delta)/(w[i]*np.linalg.norm(theta[i]-theta[j])*bound(max(r[i],r[j]),R));v.append((B,i,j))
 B,i,j=max(v);out.append(dict(R_over_image_radius=mult,R_kpc=float(R/206264.80624709636*meta['distance_native_Mpc']*1000),solar_mass_bound=float(B/unit),pair=[rows[i]['id'],rows[j]['id']]))
ck('finite_bounds',all(np.isfinite(o['solar_mass_bound']) for o in out))
res=dict(checks=checks,conditional_gas_only_remainder_bounds=out,caveat='Spherical shell support condition, hypothetical all non-gas remainder; not a cold-mass estimate or theory verdict')
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(f'{sum(b for _,b in checks)}/{len(checks)} checks');print(json.dumps(out,indent=2));assert all(b for _,b in checks)
