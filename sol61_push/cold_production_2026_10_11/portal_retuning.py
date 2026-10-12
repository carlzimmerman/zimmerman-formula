"""Optimize crossover at fixed halo pressure support, in the declared coherent EOS."""
import math,json
from pathlib import Path
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.special import beta
p=Path(__file__).parent
cosmo=json.loads((p/'portal_cosmology_run/results.json').read_text());bg=cosmo['background']
G=6.67430e-11;c=299792458.;Mpc=3.0856775814913673e22
rm0=bg['rhom0_kg_m3'];rr0=bg['rhor0_kg_m3'];rL=bg['rhoLambda_kg_m3'];rhoh=1e-21;ch=200000.
Hm=math.sqrt(8*math.pi*G*rm0/3)
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
def strength(xh):return ch*ch*(1+xh*xh)**1.5/xh
def factor(xh):return (1+xh*xh)**.75/xh**(1/3)
coef=ch*(rm0/rhoh)**(1/6)*beta(1/6,7/12)/(6*Hm*Mpc)
opt=math.sqrt(2/7)
num=minimize_scalar(lambda l:factor(math.exp(l)),bounds=(math.log(.05),math.log(4.)),method='bounded')
check('analytic matter-era optimum',abs(math.exp(num.x)/opt-1)<1e-5)
I=quad(lambda x:x**(-2/3)/(1+x*x)**.75,0,math.inf,epsabs=1e-9,epsrel=1e-9)[0]
check('beta-function sound integral',abs(I/(.5*beta(1/6,7/12))-1)<1e-8)
def full(xh,epsrel=2e-9):
 Hs=strength(xh);rho_cross=rhoh/xh
 def kernel(l):
  a=math.exp(l);rm=rm0/a**3;rr=rr0/a**4
  H=math.sqrt(8*math.pi*G*(rm+rr+rL)/3)
  x=rm/rho_cross;cs=math.sqrt(Hs*x/(1+x*x)**1.5)
  return cs/(a*H*Mpc)
 return quad(kernel,math.log(.001),0,epsrel=epsrel,epsabs=1e-10)[0]
fullopt=minimize_scalar(lambda l:full(math.exp(l)),bounds=(math.log(.05),math.log(4)),method='bounded',options={'xatol':1e-10})
xopt=math.exp(fullopt.x)
check('full-background quadrature refinement',abs(full(xopt,2e-11)-fullopt.fun)<1e-8)
check('reproduced original sound distance',abs(full(1)/cosmo['comoving_sound_distance_from_ai_Mpc']-1)<1e-10)
rows=[]
for xh in [.05,.1,opt,xopt,1.,2.,4.]:
 Hs=strength(xh)
 check('fixed halo support',abs((Hs*xh/(1+xh*xh)**1.5)/(ch*ch)-1)<1e-14)
 rows.append(dict(halo_density_over_crossover=xh,crossover_density_kg_m3=rhoh/xh,
  strength_over_c2=Hs/c**2,matter_only_infinite_history_sound_Mpc=coef*factor(xh),
  declared_finite_history_sound_Mpc=full(xh)))
out=dict(all_pass=all(v['passed'] for v in checks),checks=checks,
 analytic_matter_era_optimum_xh=opt,analytic_matter_era_min_sound_Mpc=coef*factor(opt),
 finite_history_optimum_xh=xopt,finite_history_min_sound_Mpc=fullopt.fun,
 improvement_over_original_fraction=1-fullopt.fun/full(1),rows=rows,
 non_claims=['Fixed coherent softened EOS family and one illustrative halo-support requirement',
 'No universal lower bound over other interactions or evolved multimode states',
 'Matter-only infinite history is analytic control, not actual cosmic history',
 'Sound distance is not itself an observational exclusion or full transfer function'])
(p/'portal_retuning_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
