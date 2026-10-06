"""Independent exact reduction and bounded checks of CFG347's trigger sector.

The omitted nonlinear switch interaction is not silently included: README.md
records the additional quadratic term it produces and the resulting open gate.
"""
import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
checks = {}
def check(name, condition):
    checks[name] = bool(condition)
    print(f"{'PASS' if condition else 'FAIL'} {name}")

A, b, G, w, d = sp.symbols('A b G w d', positive=True)
p = (A-w)*(b-w)-G*w
exact_limit = d*(b-(1-d)*A)/(1-d)
check('fidelity_boundary_exact', sp.simplify(p.subs({w:(1-d)*A, G:exact_limit})) == 0)
check('ten_percent_boundary', sp.simplify(exact_limit.subs(d,sp.Rational(1,10))-(b/sp.Integer(9)-A/sp.Integer(10))) == 0)
check('reported_loose_bound_difference',
      sp.simplify((b/sp.Integer(9)+A/sp.Integer(10))-exact_limit.subs(d,sp.Rational(1,10))) == A/5)
check('discriminant_positive_form', sp.expand((A+b+G)**2-4*A*b-((A-b)**2+2*G*(A+b)+G**2)) == 0)

# The full gate-on local sector includes B f(sigma). Its quadratic curvature
# shifts b by -B f''/Z in the convention L = Z(sdot^2-b s^2)/2.
Z, B, F2, rho, omega, k, C, F1 = sp.symbols('Z B F2 rho omega k C F1', real=True)
b_eff = b-B*F2/Z
matrix = sp.Matrix([[rho*(A-w), -sp.I*omega*C*k],
                    [sp.I*omega*C*k, Z*(b-w)-B*F2]])
det = sp.expand(matrix.det().subs(omega**2,w)/(rho*Z))
check('full_gate_quadratic_curvature', sp.simplify(det-((A-w)*(b_eff-w)-C*C*k*k*w/(rho*Z))) == 0)
check('negative_b_eff_creates_unstable_root', (A*b_eff).subs({A:1,b:1,B:2,F2:1,Z:1}) == -1)
# δB f' δsigma is an additional coupling if B is not frozen.
q, s = sp.symbols('q s', real=True)
product = (B+q)*(1+F1*s+F2*s*s/2)
check('constitutive_gate_cross_term', sp.diff(product,q,s).subs({q:0,s:0}) == F1)

samples = []
for aa, bb in ((1,2),(1,1),(sp.Rational(1,100),100)):
    glimit = exact_limit.subs({A:aa,b:bb,d:sp.Rational(1,10)})
    for factor in (sp.Rational(1,2), sp.Rational(3,2)):
        gg = glimit*factor
        low = (aa+bb+gg-sp.sqrt((aa+bb+gg)**2-4*aa*bb))/2
        # These examples have b > 0.9 A; the low root crosses 0.9 A
        # precisely at the derived limit. For b<A the field identities exchange;
        # do not call the low root the uncoupled gas mode in that regime.
        if bb > sp.Rational(9,10)*aa:
            check(f'fidelity_discriminator_{aa}_{bb}_{factor}', bool((low >= sp.Rational(9,10)*aa) == (factor <= 1)))
        samples.append(dict(A=str(aa), b=str(bb), G=str(gg), low_root=float(low.evalf())))

record = json.loads((ROOT/'campaign_fresh_gravity/CFG347_first_principles_switch/cfg347_switch_results.json').read_text())
# Independently vary the homogeneous switch action, including its trigger.
# u_b is the comoving unit velocity, theta_b=3 adot/(a N), c=1 here.
time = sp.symbols('time', real=True)
scale = sp.Function('a')(time)
lapse = sp.Function('N')(time)
sig = sp.Function('sigma')(time)
mass2 = sp.symbols('mass2', positive=True)
adot, sdot = sp.diff(scale,time), sp.diff(sig,time)
lag = scale**3*(Z*sdot**2/(2*lapse)-lapse*Z*mass2*sig**2/2)+3*C*scale**2*adot*sig
rho_sig = sp.simplify(-sp.diff(lag,lapse).subs(lapse,1)/scale**3)
p_sig = sp.simplify((sp.diff(lag,scale)-sp.diff(sp.diff(lag,adot),time)).subs(lapse,1)/(3*scale**2))
H = adot/scale
sigma_eq = Z*sp.diff(sig,time,2)+3*Z*H*sdot+Z*mass2*sig-3*C*H
check('FRW_switch_density', sp.simplify(rho_sig-Z*(sdot**2+mass2*sig**2)/2) == 0)
check('FRW_trigger_pressure', sp.simplify(p_sig-(Z*(sdot**2-mass2*sig**2)/2-C*sdot)) == 0)
check('FRW_conservation_on_switch_equation', sp.simplify(sp.diff(rho_sig,time)+3*H*(rho_sig+p_sig)-sdot*sigma_eq) == 0)
Hc, Mpl2 = sp.symbols('Hc Mpl2', positive=True)
rho_ds = rho_sig.subs({sdot:0,sig:3*C*Hc/(Z*mass2)})
check('FRW_deSitter_nonzero_switch_energy', sp.simplify(rho_ds-9*C**2*Hc**2/(2*Z*mass2)) == 0)
frw_fraction = {name:12*math.pi*6.67430e-11*record['numbers']['R3_lenient_point']['B_edge']/a0**2
                for name,a0 in [('canonical',9.3619e-11),('alt',1.1279e-10)]}
check('FRW_costed_stress_is_not_zero', all(0.08 < value < 0.13 for value in frw_fraction.values()))
print(json.dumps(dict(checks=checks, samples=samples,
                     recorded_verdict=record['verdict'],
                     recorded_fidelity_ratios=record['numbers']['T5_ratio'],
                     exact_fidelity_bound=str(exact_limit),
                     gate_mass_shift=str(b_eff),
                     FRW_density=str(rho_sig), FRW_pressure=str(p_sig),
                     deSitter_density=str(rho_ds),
                     frozen_H_deSitter_energy_fraction=frw_fraction), indent=2))
if not all(checks.values()):
    raise SystemExit(1)
