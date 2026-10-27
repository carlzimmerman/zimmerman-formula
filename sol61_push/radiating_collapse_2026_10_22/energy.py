import argparse,ast,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,solve_bvp,quad
from scipy.optimize import brentq
from model import Model
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args()
tree=ast.parse(Path('sol61_push/compact_surplus_2026_10_22/checks.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['interior','exterior','one']],type_ignores=[]),'profile_source','exec'))
checks=[];targets=[];seeds=[];mref=.08408132497418408
cache={}
def profile(sc):
 if sc not in cache:cache[sc]=one(sc,0,0,2e-7,30)
 return cache[sc]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v,flush=True)
for ratio in [.5,1,2,4]:
 sc=brentq(lambda s:profile(s)['mass_c']-ratio*mref,.01,1.,xtol=1e-10);row=profile(sc);sol,_=interior(sc,0,0,1e-11);x=np.linspace(1e-9,row['R'],20001);Q,s=sol.sol(x);q=Q/x**2;mass=x*x*(q+np.sqrt(q*q+4*q))/2
 for n,ns in [(256,128),(512,256)]:
  mo=Model(n=n,ns=ns,mass_ratio=ratio);rr=np.interp((np.arange(ns)+.5)/ns*ratio*mref,mass,x);w,z,stat=mo.static(rr);energy=mo.potential(rr,w,z)
  targets.append(dict(mass_ratio=ratio,n=n,ns=ns,edge=row['R'],energy=energy,static=stat))
  ck('endpoint_%g_%d'%(ratio,n),stat['gradient_max']<2e-5,dict(energy=energy,gradient=stat['gradient_max']))
for ratio in [.5,1,2,4]:
 for spin in [0,.02,.05]:
  mo=Model(mass_ratio=ratio,spin=spin);w,z,stat=mo.static(mo.r0);ee=mo.potential(mo.r0,w,z);seeds.append(dict(mass_ratio=ratio,spin=spin,energy=ee))
target=next(r['energy'] for r in targets if r['mass_ratio']==1 and r['n']==512)
for r in seeds:r['canonical_endpoint_energy_deficit']=target-r['energy'];r['canonical_endpoint_energetically_forbidden']=r['energy']<target
ck('high_inventory_endpoint_obstruction',all(r['canonical_endpoint_energetically_forbidden'] for r in seeds if r['mass_ratio']>=2),seeds)
ck('low_inventory_not_false_exclusion',all(not r['canonical_endpoint_energetically_forbidden'] for r in seeds if r['mass_ratio']<=1),'energy is necessary, not sufficient; mass conservation separately applies')
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(dict(checks=checks,targets=targets,seeds=seeds),indent=2)+'\n');raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
