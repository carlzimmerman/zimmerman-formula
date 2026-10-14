import math,json,sys
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.integrate import quad
from scipy.special import spherical_jn
from numpy.polynomial.legendre import leggauss
prior=json.loads(Path('sol61_push/nuclear_coulomb_wall_2026_10_14/run/results.json').read_text())
hc=1.973269804e-7; ml=105658375.5; alpha=1/137.035999084; g=1e-20
b=ml*prior['material_inputs']['uniform_sphere_radius_m']/hc
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def loop(r,order=64):
    x,w=leggauss(order); x=(x+1)/2; w=w/2; u=x*(1-x)
    return float(np.dot(w,6*u/(1+r*r*u)))
mp.mp.dps=60
for r in [0.,.01,.3,1.,3.,10.]:
    numeric=loop(r)
    rr=mp.mpf(str(r))
    exact=mp.mpf(1) if not r else 6/rr**2*(1-4/(rr*mp.sqrt(4+rr**2))*mp.atanh(rr/mp.sqrt(4+rr**2)))
    ck('parameter_integral_vs_closed_form',abs(numeric/float(exact)-1),3e-12)
    # Differentiate the mass dependence before a subtraction that would hold low-energy alpha fixed.
    def bare_log(M):return mp.quad(lambda x:x*(1-x)*mp.log(M*M+rr*rr*x*(1-x)),[0,1])
    derivative=mp.diff(bare_log,mp.mpf(1))
    ck('mass_derivative_normalization',float(abs(3*derivative-exact)),1e-50)
    assert 1/(1+r*r/5)-1e-14<=numeric<=1+1e-14
# Radial nuclear charge transform. Tail bound uses |sin x-x cos x|<=1+x.
xs,ws=leggauss(256); uu=(xs+1)/2; ww=ws/2; uu=uu*(1-uu)
def fastloop(r):
    if r<=.1:return float(np.dot(ww,6*uu/(1+r*r*uu)))
    return 6/r**2*(1-4/(r*math.sqrt(4+r*r))*math.atanh(r/math.sqrt(4+r*r)))
def nuclear(x):return 1. if x==0 else 3*spherical_jn(1,x)/x
def integrate(L,withloop):
    total=0.
    for left in np.arange(0,L,math.pi):
        right=min(L,left+math.pi)
        total+=quad(lambda x:nuclear(x)**2*(fastloop(x/b) if withloop else 1),left,right,epsabs=1e-13,epsrel=1e-11)[0]
    return total
I0=3*math.pi/5
ratios=[]
for L in [200.,400.]:
    norm=integrate(L,False); weighted=integrate(L,True)
    tail=9*(1/(3*L**3)+1/(2*L**4)+1/(5*L**5))
    ck('nuclear_normalization_tail',max(0.,abs(norm-I0)-tail),1e-12)
    ratios.append(dict(cutoff=L,ratio=weighted/I0,absolute_ratio_tail_bound=tail/I0))
ck('radial_cutoff_refinement',abs(ratios[1]['ratio']-ratios[0]['ratio']),ratios[0]['absolute_ratio_tail_bound'])
ratio=ratios[-1]['ratio']; lower=1/(1+.5/(b*b))
assert lower<=ratio<=1
# High-momentum closed form is checked against 60-decimal arithmetic.
for r in [.3,3.,30.,100.]:
    rr=mp.mpf(str(r))
    reference=6/rr**2*(1-4/(rr*mp.sqrt(4+rr**2))*mp.atanh(rr/mp.sqrt(4+rr**2)))
    ck('high_momentum_closed_form_precision',abs(fastloop(r)/float(reference)-1),1e-10)
result=dict(muon_yukawa_signed=-3*math.pi*ml*g/(2*alpha),muon_mass_times_nuclear_radius=b,
    momentum_weighted_ratio=ratio,quadrature_tail_records=ratios,
    analytic_Jensen_lower_bound=lower,
    matched_Coulomb_energy_eV=prior['Coulomb_pair_energy_eV']*ratio,
    stronger_wall_eV=prior['cases'][0]['Coulomb_only_wall_eV']*ratio,
    weaker_wall_eV=prior['cases'][1]['Coulomb_only_wall_eV']*ratio,
    checks=checks,passed=len(checks),
    scope='One-muon-loop zero-scalar-momentum matching of a uniform nuclear pair Coulomb contribution; not full material scalar charge')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
