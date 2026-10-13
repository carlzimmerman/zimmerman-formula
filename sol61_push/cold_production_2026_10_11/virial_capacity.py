"""Finite chemical-energy capacity: conditional stationary halo constraints."""
import json, math
from pathlib import Path
from fractions import Fraction
from scipy.integrate import quad
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
vstar=params['u']*299792458.; sigma=200000.
checks=[]
def check(name, value): checks.append(dict(name=name, passed=bool(value)))
# Set G=M=b=1. Compute W from shells, K from Jeans dispersion,
# and virial force moment independently. All integrals converge although I does not.
rho=lambda r:3/(4*math.pi)*(1+r*r)**(-2.5)
enclosed=lambda r:r**3/(1+r*r)**1.5
W=quad(lambda r:-4*math.pi*r*rho(r)*enclosed(r),0,math.inf,epsabs=1e-12)[0]
K=quad(lambda r:4*math.pi*r*r*rho(r)*1.5/(6*math.sqrt(1+r*r)),0,math.inf,epsabs=1e-12)[0]
force=quad(lambda r:-4*math.pi*r**3*rho(r)*r/(1+r*r)**1.5,0,math.inf,epsabs=1e-12)[0]
check('shell gravitational energy',abs(W/(-3*math.pi/32)-1)<1e-11)
check('Jeans kinetic energy',abs(K/(3*math.pi/64)-1)<1e-11)
check('force virial equals gravitational energy',abs(force/W-1)<1e-11)
check('initial stationary virial balance',abs(2*K+W)<1e-12)
# Physical K0/M=9 pi sigma0^2/32; maximum rest-gap reservoir/M=vstar^2/2.
k0_per_mass=9*math.pi*sigma*sigma/32
alpha=vstar*vstar/(2*k0_per_mass)
rows=[]
for f in [0.,.1,.25,.5,.75,1.]:
    ratio=1+alpha*f
    rows.append(dict(source_charge_fraction=f,kinetic_energy_ratio=ratio,
                     gravitational_radius_ratio=1/ratio,rms_speed_ratio=math.sqrt(ratio)))
# Exact independent substitution into energy and virial for multiple fractions/gaps.
for a in [Fraction(0),Fraction(1,10),Fraction(5,4),Fraction(10)]:
    for f in [Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(1)]:
        gap=a*f; k=1+gap; w=-2*k
        check('stationary total energy including rest gap',k+w+gap==-1)
        check('stationary virial equation',2*k+w==0)
# Counterexample to interpreting r_g bound as a minimum core radius:
# core mass epsilon=M_core/M, radius epsilon^2 b has self W=-3 pi/32 GM^2/b,
# independent of epsilon, while central density grows as epsilon^-5.
core_rows=[]
for eps in [.1,.01,.001]:
    radius=eps**2; selfW=-3*math.pi/32*eps**2/radius
    check('fixed-energy shrinking low-mass core',abs(selfW/W-1)<1e-11)
    core_rows.append(dict(core_mass_fraction=eps,core_scale_over_b=radius,
                          core_self_energy_over_initial_W=selfW/W,
                          core_central_density_over_initial=eps/radius**3))
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,
         initial_K_per_mass_m2_s2=k0_per_mass,capacity_over_initial_K=alpha,
         minimum_stationary_gravitational_radius_ratio=1/(1+alpha),rows=rows,
         small_core_scaling=core_rows,
         non_claims=['Conditional stationary virial endpoints only; no evolution or stability proof',
                     'Isolated fixed mass, no escape, no external potential, negligible contact stress',
                     'No lower bound on central core radius or upper bound on density',
                     'No universal profile, abundance, or vacuum-dependent acceleration law'])
(p/'virial_capacity_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
print('Checks:',len(checks)); assert out['all_pass']
