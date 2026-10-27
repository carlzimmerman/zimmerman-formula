"""Finite assertions for the reduced compliant-medium model; no data fitting."""
import argparse
import json
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as s

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
p.add_argument('--mutate', action='store_true')
args = p.parse_args()
out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
checks = []

def check(name, ok, detail):
    checks.append(dict(name=name, passed=bool(ok), detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ') + name + ': ' + str(detail))

K, k, A, B, C, d = s.symbols('K k A B C d', positive=True)
E = (-1 if not args.mutate else 1)*K*(B+C)**2/(2*k**2) + K*d**2/(2*k**2) + A*(C-d)**2/2
dstar = s.solve(s.diff(E, d), d)[0]
Eeff = s.factor(E.subs(d,dstar))
check('schur_self_gravity', s.simplify(s.diff(Eeff,C,2)+K/(k*k*(1+A*k*k/K)))==0,
      s.diff(Eeff,C,2))
check('reciprocal_baryon_force', s.simplify(s.diff(Eeff,B,C)+K/k**2)==0, s.diff(Eeff,B,C))

z, e, t = s.symbols('z e t', positive=True)
poly = s.expand((1+z+e*t)*(t-1+z)-z*z)
check('two_mode_polynomial', s.simplify(poly-(e*t*t+(1+z+e*(z-1))*t-1))==0, poly)
qbound = s.factor(poly.subs(t,1/(1+z)))
check('inertia_bound', s.simplify(qbound-e*z*z/(1+z)**2)==0, qbound)
max_ratio = 0.
min_t = 1.
for zv in np.logspace(-4,4,17):
    for ev in np.logspace(-4,4,17):
        b = 1+zv+ev*(zv-1)
        disc = np.sqrt(b*b+4*ev)
        root = 2/(b+disc) if b>=0 else (-b+disc)/(2*ev)
        max_ratio = max(max_ratio, root*(1+zv))
        min_t = min(min_t, root)
check('inertia_grid_289', max_ratio<=1+1e-10 and min_t>0, dict(max_ratio=max_ratio,min_root=min_t))

x, rr = s.symbols('x rr', positive=True)
integ = s.integrate(x*x*s.log(rr/x),(x,0,rr))
check('radial_bound_integral', s.simplify(integ-rr**3/9)==0, integ)

# Constants are declared numerical conventions, not fitted observational inputs.
G=6.67430e-11
Msun=1.98847e30
pc=3.085677581491367e16
Mpc=1e6*pc
fb=1/(1+5.364)
fc=1-fb
def growth(zv):
    S=1/(1+zv)
    lam=(fb+fc*S+np.sqrt((fb-fc*S)**2+4*fb*fc))/2
    return (-1+np.sqrt(1+24*lam))/4
zmax=brentq(lambda q:growth(q)-.999,0.,1.)
ellmax=np.sqrt(zmax)/(.1*1101)*Mpc
hard_lam=max(np.linalg.eigvals(np.array([[fb,fc],[fb,0.]])))
hard_n=(-1+np.sqrt(1+24*hard_lam))/4
check('growth_limits', abs(growth(0)-1)<1e-14 and abs(growth(1e16)-hard_n)<1e-14,
      dict(dust=growth(0),hard_identity=growth(1e16),zmax=zmax,ellmax_pc=ellmax/pc))

rows=[]
for label,a0 in [('canonical',9.3603e-11),('alternative',1.1312e-10)]:
    mass=1e10*Msun
    radius=50e3*pc
    gN=G*mass/radius**2
    glaw=(gN+np.sqrt(gN*gN+4*a0*gN))/2
    gcap=1.1*glaw
    hcap=gcap*gcap/(gcap+a0)
    v2=np.sqrt(G*mass*a0)
    ellmin=np.sqrt(v2*radius/(9*(hcap-gN)))
    row=dict(footing=label,a0=a0,rM_pc=np.sqrt(G*mass/a0)/pc,
             ell_min_pc=ellmin/pc,ell_max_pc=ellmax/pc,
             interval_ratio=ellmin/ellmax,
             growth_at_ell_min=growth((.1*1101*ellmin/Mpc)**2))
    rows.append(row)
    check('empty_constant_interval_'+label, ellmin>ellmax, row)

# Follow-up algebra: A(rho) varies with material density. No frozen constant-A
# observational verdict is transferred to this model.
rho, bg, ap, app, aval = s.symbols('rho bg ap app aval', real=True)
af=s.Function('A')(rho)
ep=rho-bg-d
V=af*ep**2/2
H=s.hessian(V,(rho,d))
det=s.factor(H.det())
target=ep**2*(af*s.diff(af,rho,2)/2-s.diff(af,rho)**2)
check('variable_compliance_convexity',s.simplify(det-target)==0,det)
m, a = s.symbols('m a', positive=True)
power=s.simplify(target.subs(af,a*rho**(-m)).doit())
check('power_convexity_interval',s.simplify(power-a*a*m*(1-m)*ep**2/(2*rho**(2*m+2)))==0,power)
mu=s.diff(V,rho)
check('chemical_potential_extra_term', s.simplify(mu-af*ep-s.diff(af,rho)*ep**2/2)==0,mu)

result=dict(status='checks_passed' if all(c['passed'] for c in checks) else 'checks_failed',
            mutation=args.mutate,checks=checks,footings=rows,
            conventions=dict(G=G,Msun_kg=Msun,pc_m=pc,mass_Msun=1e10,radius_kpc=50,
                             allowed_acceleration_error=.1,redshift=1100,k_com_Mpc_inverse=.1,
                             cold_baryon_ratio=5.364,allowed_local_growth_error=.001),
            software=dict(numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__),
            non_claims=['No covariant completion','No CMB likelihood','No dwarf or cluster data fit',
                        'No exclusion of density-dependent or phase-dependent parent actions'])
out.write_text(json.dumps(result,indent=2)+'\n')
print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)}")
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
