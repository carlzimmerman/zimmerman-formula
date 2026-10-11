import json,sys,itertools
from pathlib import Path
import numpy as np
import sympy as sp
P=Path('sol61_push');checks=[]
def ck(n,b):checks.append([n,bool(b)])
x1,x2,y1,y2=sp.symbols('x1 x2 y1 y2',real=True)
x=sp.Matrix([x1,x2]);y=sp.Matrix([y1,y2]);k=x/x.dot(x)-y/y.dot(y)
ck('exact_kernel_identity',sp.factor(k.dot(k)-(x-y).dot(x-y)/(x.dot(x)*y.dot(y)))==0)
def K(z):return z/np.sum(z*z,axis=-1,keepdims=True)
# Exact pair-distance bound saturates with one collinear exterior mass.
a=np.array([-.3,0]);b=np.array([.3,0]);m=np.array([2.,0])
ck('single_mass_saturation',abs(np.linalg.norm(K(a-m)-K(b-m))-np.linalg.norm(a-b)/(np.linalg.norm(a-m)*np.linalg.norm(b-m)))<1e-12)
ck('MUTATE_signed_total',np.linalg.norm((K(a-m)-K(b-m))-(K(a+m)-K(b+m)))>1e-3 if False else np.linalg.norm(K(a-np.array([2.,1.]))-K(b-np.array([2.,1.]))-K(a-np.array([3.,-1.]))+K(b-np.array([3.,-1.])))>1e-3)
ck('MUTATE_inside_support',np.linalg.norm(K(a)-K(b))>np.linalg.norm(a-b)/((2-np.linalg.norm(a))*(2-np.linalg.norm(b))))
old=np.load(P/'gas_image_operator_2026_10_11/run_v2/operator.npz');gas=np.load(P/'gas_distance_2026_10_11/run/operator.npz')
meta=json.loads((P/'gas_distance_2026_10_11/run/results.json').read_text()); rows=json.loads((P/'native_lensing_2026_10_11/run_v2/results.json').read_text())['gold_rows']
theta=old['theta_arcsec'];alpha=gas['ICRS_linear_alpha_infinity_native'];w=gas['source_weight_native_PM_flat'];r=np.linalg.norm(theta,axis=1)
pairs=[(i,j) for i,j in itertools.combinations(range(len(rows)),2) if rows[i]['feature']==rows[j]['feature']]
ck('source_weights',all(abs(w[i]-w[j])<1e-14 for i,j in pairs))
G=6.67430e-11;c=299792458.;Ms=1.98847e30;Mpc=3.085677581491367e22;asec=206264.80624709636
unit=4*G*Ms/(c*c*meta['distance_native_Mpc']*Mpc)*asec**2
ck('mass_roundtrip',abs((1e14*unit)/unit/1e14-1)<1e-12)
rng=np.random.default_rng(11011);out=[];maxratio=0
for mult in [1.1,1.5,2.,4.]:
 R=mult*r.max();bounds=[]
 for i,j in pairs:
  sep=np.linalg.norm(theta[i]-theta[j]);res=theta[i]-theta[j]-w[i]*(alpha[i]-alpha[j])
  B=np.linalg.norm(res)*(R-r[i])*(R-r[j])/(w[i]*sep)
  bounds.append((B,i,j))
 B,i,j=max(bounds)
 out.append(dict(R_over_image_radius=mult,R_arcsec=float(R),R_kpc=float(R/asec*meta['distance_native_Mpc']*1000),angular_mass_lower_bound=float(B),solar_mass_lower_bound=float(B/unit),limiting_pair=[rows[i]['id'],rows[j]['id']]))
 for rep in range(50):
  angle=rng.uniform(0,2*np.pi,40); rr=R*rng.uniform(1.001,4,40);pts=rr[:,None]*np.column_stack([np.cos(angle),np.sin(angle)]);mass=rng.uniform(.01,1,40)
  fields=np.einsum('imc,m->ic',K(theta[:,None,:]-pts[None,:,:]),mass,optimize=False)
  ratios=[np.linalg.norm(fields[i]-fields[j])*(R-r[i])*(R-r[j])/(mass.sum()*np.linalg.norm(theta[i]-theta[j])) for i,j in pairs]
  maxratio=max(maxratio,max(ratios));ck(f'positive_configuration_{mult}_{rep}',max(ratios)<=1+1e-12)
ck('finite_outputs',all(np.isfinite(q['solar_mass_lower_bound']) for q in out))
res=dict(checks=checks,pair_count=len(pairs),max_positive_toy_bound_ratio=maxratio,conditional_bounds=out,interpretation='All non-gas mass exterior to declared disk: necessary bound only, not actual cold mass or observational verdict')
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(f'{sum(v for _,v in checks)}/{len(checks)} checks');print(json.dumps(out,indent=2));assert all(v for _,v in checks)
