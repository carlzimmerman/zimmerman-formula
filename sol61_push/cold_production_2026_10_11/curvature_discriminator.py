"""Exact local Ricci identities and limitations of a dust vacuum discriminator."""
from fractions import Fraction as F
from pathlib import Path
import json,math
p=Path(__file__).parent
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
def ricci(e,press,L):
    # Mixed components, signature -+++, Einstein coupling set to one.
    T=[-e]+list(press);tr=sum(T)
    return [v-tr/2+L for v in T]
for e in map(F,[1,10,100]):
 for pressure in [F(0),F(1,10),e/3]:
  L=F(2,7);r=ricci(e,[pressure]*3,L);R=sum(r)
  S=[v-R/4 for v in r];S2=sum(v*v for v in S)
  check('perfect-fluid Ricci trace',R==4*L+e-3*pressure)
  check('traceless Ricci norm',S2==F(3,4)*(e+pressure)**2)
  check('dust-discriminator identity',(R-(e+pressure))/4==L-pressure)
  d=F(1,100)
  check('same curvature different vacuum split',ricci(e-d,[pressure+d]*3,L+d)==r)
# General diagonal pressure identity; isolates the anisotropy contribution.
for pp in [(F(0),F(1,10),F(1,5)),(F(1),F(2),F(3))]:
 e=F(10);L=F(1);r=ricci(e,pp,L);R=sum(r);S2=sum((v-R/4)**2 for v in r)
 pm=sum(pp)/3;anis=sum((v-pm)**2 for v in pp)
 check('anisotropic norm decomposition',F(4,3)*S2==(e+pm)**2+F(4,3)*anis)
 check('anisotropy decreases proposed vacuum estimator',anis>0)
# The square-root norm has unequal two-sided derivatives along traceless direction.
S=[F(-3,4),F(1,4),F(1,4),F(1,4)]
check('non-differentiable norm at vacuum',sum(v*v for v in S)==F(3,4))
rhoL=6e-27;rho0=1e-21;sig=200000.;c=299792458.
rows=[]
for x in [0.,.5,1.,2.,4.]:
 rho=rho0/(1+x*x)**2.5;sig2=sig*sig/math.sqrt(1+x*x)
 ratio=rho*sig2/(rhoL*c*c)
 rows.append(dict(r_over_b=x,pressure_over_vacuum_energy_density=ratio,
                 inferred_Lambda_over_true=1-ratio))
out=dict(all_pass=all(v['passed'] for v in checks),checks=checks,rows=rows,
    non_claims=['Ricci reconstruction on Einstein backgrounds, not a new coupled action',
               'Dust formula does not isolate vacuum for pressured or anisotropic matter',
               'No universal halo selector or acceleration normalization derived'])
(p/'curvature_discriminator_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
