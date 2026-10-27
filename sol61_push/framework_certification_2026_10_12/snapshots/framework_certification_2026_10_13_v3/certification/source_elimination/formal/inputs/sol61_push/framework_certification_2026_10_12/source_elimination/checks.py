"""Exact source-memory diagnostics in the supplied leading NR approximation."""
import json
from pathlib import Path
import sys
import sympy as s

dest = Path(sys.argv[1])
t, u = s.symbols('t u', real=True)
a, delta, c, F, n, m = s.symbols('a delta c F n m', positive=True, real=True)
omega, k = s.symbols('omega k', real=True)
checks = []

def z(name, expr):
    residual = s.simplify(s.expand(expr))
    checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})

def yes(name, condition):
    checks.append({'name': name, 'passed': bool(condition), 'condition': str(condition)})

drive = F * s.exp(-s.I * omega * t)
b = -c * F * (s.exp(-s.I * omega * t) - s.exp(-s.I * a * t)) / (a - omega)
z('harmonic forcing source ODE away from resonance', s.I * s.diff(b, t) - a*b - c*drive)
z('zero initial source retained', b.subs(t, 0))
bp = -c * drive / (a - omega)
z('well-prepared particular response solves ODE', s.I*s.diff(bp,t)-a*bp-c*drive)
z('initial mismatch propagates homogeneously', b-bp-c*F*s.exp(-s.I*a*t)/(a-omega))
br = -s.I*c*F*t*s.exp(-s.I*a*t)
z('resonant response ODE', s.I*s.diff(br,t)-a*br-c*F*s.exp(-s.I*a*t))
z('resonant response initial condition', br.subs(t,0))
z('resonance limit of nonresonant solution', s.limit(b, omega, a)-br)
bc = b.subs({a:delta, omega:0})
memory = -s.I*c*s.integrate(s.exp(-s.I*delta*(t-u))*F, (u,0,t))
z('constant retarded integral equals actual solution', memory-bc)
storage = 2*c**2*F**2*(1-s.cos(delta*t))/delta**2
z('source storage equals actual complex norm', s.expand_complex(bc*s.conjugate(bc))-storage)
z('source storage derivative', s.diff(storage,t)-2*c**2*F**2*s.sin(delta*t)/delta)
yes('positive storage derivative at quarter cycle', s.simplify(s.diff(storage,t).subs(t,s.pi/(2*delta))).is_positive)
yes('negative storage derivative at three-quarter cycle', s.simplify(s.diff(storage,t).subs(t,3*s.pi/(2*delta))).is_negative)
z('source storage returns to zero after full cycle', storage.subs(t,2*s.pi/delta))
keff = k-c**2/(delta-omega)
z('frequency-dependent quartic correction', keff-(k-c**2/delta)+c**2*omega/(delta*(delta-omega)))
z('particular source weighted charge fraction', 2*(c*s.sqrt(n)**2/(delta-omega))**2/n-2*c**2*n/(delta-omega)**2)
exactp = ((2*m+delta)**2-4*m**2)/4
z('relativistic minus NR momentum squared', exactp-m*delta-delta**2/4)
z('relative NR momentum squared error', (exactp-m*delta)/(m*delta)-delta/(4*m))
z('NR pair production resonance', (m*delta)/m-delta)
wrong = -b
yes('mutation wrong memory sign rejected', s.simplify((s.I*s.diff(wrong,t)-a*wrong-c*drive).subs(t,0)) == -2*c*F)
yes('mutation removed initial transient rejected', s.simplify(bp.subs(t,0)) != 0)
yes('mutation instantaneous gap at finite frequency rejected', s.simplify((keff-(k-c**2/delta)).subs(omega,delta/2)) == -c**2/delta)
out = {'all_passed': all(x['passed'] for x in checks), 'check_count': len(checks), 'checks': checks,
       'scope': 'Exact driven Fourier-source and off-resonant algebra within supplied leading NR model; forcing is prescribed for response diagnostic. No derived damping, collision rate, quantum reduction, nonlinear backreaction, gravity or selector.',
       'assumptions': 'delta,c,F,m,n positive; omega real; nonresonant formulas require a!=omega; resonance checked separately; source Fourier operator eigenvalue a=delta+P^2/(2M)'}
(dest/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_passed':out['all_passed'],'check_count':len(checks)}))
assert out['all_passed'], [x for x in checks if not x['passed']]
