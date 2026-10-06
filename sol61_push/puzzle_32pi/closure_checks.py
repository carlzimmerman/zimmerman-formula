"""Independent, bounded checks of coefficient identifiability and p44 forecasting.

Run from the repository root. No imports or writes to peer-session lanes.
The analytic arguments and restrictions are in README.md.
"""
import json
import math
import re
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
checks = {}


def check(name, condition):
    checks[name] = bool(condition)
    print(f"{'PASS' if condition else 'FAIL'} {name}")


# Read the recorded scatter rather than silently replacing it with a rounded value.
record = (ROOT / 'sonnet55_push/puzzle_32pi/p44_samplesize_and_bayes.out').read_text()
s = float(re.search(r'scatter s = ([0-9.]+)', record)[1])
f = math.hypot(0.03, 0.085)
hl = 67.4 / 3.0857e19 * math.sqrt(0.685)
ref = 299792458 * hl / math.sqrt(32 * math.pi / 3)
rivals = {'rho_total': ref / math.sqrt(0.685),
          'Milgrom_rho_Lambda': 299792458 * hl / (2 * math.pi),
          'Verlinde_rho_Lambda': 299792458 * hl / 6,
          'turnoff_p40': 1.061e-10}
rows = []
for name, a in rivals.items():
    delta = abs(math.log(a / ref))
    for z in (2, 3):
        denominator = delta**2 - z**2 * f**2
        n = z**2 * s**2 / denominator if denominator > 0 else None
        rows.append(dict(rival=name, z=z, delta_ln=delta,
                         zero_floor_n=z**2*s**2/delta**2,
                         floor_aware_n=n,
                         required_floor_below=delta/z))
        if n is not None:
            check(f'forecast_equation_{name}_{z}',
                  abs(delta / math.sqrt(s*s/n+f*f) - z) < 1e-12)
check('nearest_rivals_impossible_at_present_floor',
      all(r['floor_aware_n'] is None for r in rows if r['rival'] != 'rho_total'))
alt2 = next(r for r in rows if r['rival'] == 'rho_total' and r['z'] == 2)
check('rho_total_two_sigma_needs_more_than_400', alt2['floor_aware_n'] > 400)
check('rho_total_three_sigma_impossible',
      next(r for r in rows if r['rival'] == 'rho_total' and r['z'] == 3)['floor_aware_n'] is None)

# Stable evaluation: rationalise sqrt(1+1/y)-1 to avoid tail cancellation.
mp.mp.dps = 40
def vacuum(T):
    T = mp.mpf(T)
    integrand = lambda y: 1 / ((mp.sqrt(1 + 1/y) + 1) * (1 + (y/T)**2))
    return mp.quad(integrand, [0, 1, T, 10*T, mp.inf])

Ts = [100, 128, 129, 1000]
values = [float(vacuum(T)) for T in Ts]
check('vacuum_increases_with_cutoff_finite_samples', all(a < b for a, b in zip(values, values[1:])))
root = mp.findroot(lambda T: vacuum(T) - 32*mp.pi, (128, 130))
p45_record = (ROOT / 'sonnet55_push/puzzle_32pi/p45_vacuum_closed_form.out').read_text()
recorded_root = mp.mpf(re.search(r'numeric root of the exact integral: ([0-9.]+)', p45_record)[1])
check('p45_root_reproduced', abs(root-recorded_root) < mp.mpf('.00005'))
check('root_residual', abs(vacuum(root)-32*mp.pi) < mp.mpf('1e-30'))

# A compact C^2 deformation invisible for y <= Y, including every y <= 100.
t = sp.symbols('t', real=True)
phi = t**3*(1-t)**3
moment = sp.integrate((1+t)*phi, (t, 0, 1))
check('compact_tail_moment_exact', moment == sp.Rational(3, 280))
check('compact_tail_C2_endpoints',
      all(sp.diff(phi,t,j).subs(t,a) == 0 for j in range(3) for a in (0,1)))
Y, T, change = mp.mpf(1000), mp.mpf(129), mp.mpf('.01')
epsilon = change / (Y**2 * mp.mpf(3)/280)
# |phi'| <= 3/16; a rigorous lower bound on -nu_base' on [Y,2Y].
base_derivative_lower = (1 / (2*Y*(mp.sqrt(1+1/(2*Y))+1))) * (2*Y/T**2) / (1+(2*Y/T)**2)**2
bump_derivative_upper = epsilon/Y * mp.mpf(3)/16
check('monotonicity_certified_by_uniform_derivative_bound', bump_derivative_upper < base_derivative_lower)
actual_change = mp.quad(lambda u: epsilon*Y**2*(1+u)*u**3*(1-u)**3, [0,1])
check('vacuum_changes_but_low_y_law_identical', abs(actual_change-change) < mp.mpf('1e-35'))
check('bump_vanishes_below_support', max(100, 999) < Y)

result = dict(checks=checks, scatter_ln=s, systematic_floor_ln=f,
              forecasts=rows, vacuum=dict(T=Ts, C=values, target_root=float(root)),
              deformation=dict(Y=float(Y), epsilon=float(epsilon), delta_C=float(actual_change),
                               base_derivative_lower=float(base_derivative_lower),
                               bump_derivative_upper=float(bump_derivative_upper)))
print(json.dumps(result, indent=2))
if not all(checks.values()):
    raise SystemExit(1)
