import json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent
raw=json.loads((p/'run_026/results.json').read_text())
core=(np.sqrt(17)-1)/2;dm=(5-core)/64;S=5.
checks=[]
def check(name,c):
 checks.append(dict(name=name,passed=bool(c)))
 if not c:raise AssertionError(name)
def w(x):
 x=np.asarray(x);out=np.empty_like(x);sm=x<.05
 out[sm]=sum(x[sm]**i/i for i in range(3,25))
 out[~sm]=-x[~sm]**2/2-x[~sm]-np.log1p(-x[~sm]);return out
def ground(n):
 low=core+dm*np.arange(n);high=low+dm
 lo=np.sqrt(high)*(1+1e-12);hi=np.maximum(high+2,2*lo)
 for _ in range(100):
  mid=(lo+hi)/2;a=low/mid**2;b=high/mid**2;f=-1/mid**2+(w(b)-w(a))/(b-a)
  lo=np.where(f>0,mid,lo);hi=np.where(f>=0,hi,mid)
 r=(lo+hi)/2;nodes,weights=np.polynomial.legendre.leggauss(128)
 bounds=np.r_[0.,1/r[::-1],.5];mass=np.r_[high[::-1],core]
 lowq,hiq=bounds[:-1],bounds[1:];q=(hiq+lowq)[:,None]/2+(hiq-lowq)[:,None]*nodes/2
 field=np.sum((hiq-lowq)/2*np.sum(weights*w(mass[:,None]*q*q)/q**4,axis=1))
 return float(-dm*np.sum(1/r)+field)
rows=[]
for name in ['coarse','fine']:
 t=raw[name];r=np.array(t['r']);v=np.array(t['v']);ek=v*v/2-1/r
 ids=np.flatnonzero((v>0)&(ek>0)&(r*r>S))
 check('nonempty certificate '+name,len(ids)>0)
 tail=S*S/(3*r[ids]**3*(1-S/r[ids]**2))
 lo=dm*np.sum(ek[ids]);hi=dm*np.sum(ek[ids]+tail)
 g=ground(64-len(ids));initial=t['initial_energy']
 remainder=[initial-hi-g,initial-lo-g]
 check('tail positive '+name,np.all(tail>0))
 check('remainder above same-mass discrete ground '+name,remainder[0]>0)
 rows.append(dict(source=name,ids=ids.tolist(),escaped_mass=float(dm*len(ids)),
  escape_KE_infinity_bounds=[float(lo),float(hi)],
  remaining_ground_energy=g,remaining_excess_bounds=[float(x) for x in remainder],
  minimum_specific_certificate_margin=float(min(ek[ids]))))
check('same certified IDs across verified short adaptive runs',rows[0]['ids']==rows[1]['ids'])
out=dict(checks=checks,rows=rows,scope='Conditional escape comparison proof; raw adaptive trajectories verified only to t20. Retained allocation is asymptotic bookkeeping for this subset, not final stationary halo evidence.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
