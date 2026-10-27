"""CE-FM-001: exact alternatives and approximation audit; no formation simulation."""
import json
import sys
from pathlib import Path
import numpy as np
import sympy as s

out = Path(sys.argv[1])
checks = []
def check(name, condition, detail=None):
    checks.append({'name': name, 'passed': bool(condition), 'detail': detail})
    if not condition:
        raise AssertionError(name)

def root(q):
    # u^2/(1-u)=q; cancellation-free positive root
    q = np.asarray(q)
    return 2*q/(np.sqrt(q*q+4*q)+q)

r = np.geomspace(.5, 1000., 2001)
y = 1/r**2
u0 = root(y)
m0 = r*r*u0
rows = []
for alpha in (0., .09, .36, .6, .9):
    u = root((1-alpha)*y)
    m = r*r*u
    l2 = alpha*r  # L^2=alpha G M_b r, NOT alpha times baryonic law speed squared
    force = -y + u*u/(1-u) + l2/r**3
    err = float(np.max(np.abs(force)/y))
    check(f'circular balance alpha={alpha}', err < 1e-10, err)
    check(f'positive density alpha={alpha}', np.all(np.diff(m)>0))
    check(f'within saturation alpha={alpha}', np.all((u>0)&(u<1)))
    # Radial linearization at fixed rank/enclosed mass and fixed individual L.
    omega2 = ((2*(1-alpha)*(2-u)/(1-u)-2+3*alpha)*y/r)
    check(f'ordered shell radial stability alpha={alpha}', np.all(omega2>0))
    rows.append({'alpha':alpha, 'mass_ratio_at_20':float(root((1-alpha)/400)/root(1/400)),
                 'deep_limit_ratio':float(np.sqrt(1-alpha)), 'max_relative_force_residual':err})

rr, mm, ll, aa = s.symbols('r m L2 alpha', positive=True)
f = -1/rr**2 + (mm/rr**2)**2/(1-mm/rr**2) + ll/rr**3
uu = s.symbols('u', positive=True)
# Direct differentiate BEFORE substituting the equilibrium relations.
minus_derivative = -s.diff(f, rr).subs(mm, uu*rr**2).subs(ll, aa*rr)
minus_derivative = minus_derivative.subs(rr**2, (1-aa)*(1-uu)/uu**2)
expected = (2*(1-aa)*(2-uu)/(1-uu)-2+3*aa)/rr**3
expected = expected.subs(rr**2, (1-aa)*(1-uu)/uu**2)
# Avoid fractional substitution conventions: compare expressions times r^3 first.
actual_scaled = s.simplify((-s.diff(f,rr)*rr**3).subs(mm,uu*rr**2).subs(ll,aa*rr))
actual_scaled = s.simplify(actual_scaled.subs(rr**2,(1-aa)*(1-uu)/uu**2))
expected_scaled = 2*(1-aa)*(2-uu)/(1-uu)-2+3*aa
check('symbolic fixed-rank frequency', s.simplify(actual_scaled-expected_scaled)==0)
check('symbolic stability lower bound', s.simplify(expected_scaled-(2-aa)-2*(1-aa)*uu/(1-uu))==0)

approx = []
for radius in (2.,5.,10.,20.,50.):
    full = float(radius*radius*root(1/radius**2))
    approx.append({'radius_rM':radius, 'full_mass':full,'cubic_mass':radius,
                   'cubic_mass_excess_fraction':radius/full-1,
                   'full_force_on_cubic_profile_over_gN':1/(1-1/radius)-1})
check('cubic surrogate differs by >25 percent at r=2', approx[0]['cubic_mass_excess_fraction']>.25)

alpha, radius = .6,20.
true_cubic = np.sqrt(1-alpha)
vt2 = alpha/radius
wrong = np.sqrt(1-vt2/(1+1/radius))
correct = np.sqrt(1-vt2/(1/radius))
check('CFG749 law-speed normalization fails exact cubic circular state', abs(wrong-true_cubic)>.3)
check('baryon-speed normalization matches circular state', abs(correct-true_cubic)<1e-14)
check('control omitted centrifugal force is rejected', alpha>0 and abs(-1/radius**2+(1-alpha)/radius**2)>1e-4)

detune = []
for eps in (-.01,0.,.01):
    b = y-eps
    disc = np.sqrt(b*b+4*(1+eps)*y)
    # Choose numerically stable quadratic evaluation by sign of b.
    u = np.empty_like(y)
    mask = b >= 0
    u[mask] = 2*y[mask]/(disc[mask]+b[mask])
    u[~mask] = (disc[~mask]-b[~mask])/(2*(1+eps))
    resid = u*u/(1-u)-y-eps*u
    err = float(np.max(np.abs(resid)/y))
    check(f'detuned force balance epsilon={eps}',err<1e-10,err)
    check(f'detuned admissibility epsilon={eps}',np.all((u>0)&(u<1)))
    detune.append({'epsilon':eps,'mass_ratio_to_exact_at_1000':float(u[-1]/u0[-1]),
                   'maximum_relative_residual':err})

result = {'checks':checks,'circular_equilibria':rows,'approximation_audit':approx,
          'normalization_counterexample':{'alpha':alpha,'radius':radius,'true_cubic_mass_ratio':float(true_cubic),
              'CFG749_predictor':float(wrong),'correct_predictor':float(correct)},
          'detuned_comparison':detune,
          'scope':'Finite algebra/numerical checks and self-reviewed analytical measure-valued equilibria; no formation or empirical proof.'}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'approximation':approx,'predictor':result['normalization_counterexample'],
                  'circular_equilibria':rows,'detune':detune},indent=2))
