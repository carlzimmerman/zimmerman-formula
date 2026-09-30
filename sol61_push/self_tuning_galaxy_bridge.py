"""Exact checks of a restricted tadpole/galaxy bridge; no dynamical proof."""
import argparse
import json
from pathlib import Path
import sympy as s

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
args = p.parse_args()
phi, shift, V, T, Kc, P = s.symbols('phi shift V T Kc P')
h, M, Mp, c0, c1, t, dv, stream = s.symbols('h M Mp c0 c1 t dv stream')
L = -V-T*phi-Kc*phi*P**3
transformed = L.subs({phi: phi+shift, V: V-T*shift}, simultaneous=True)
vacuum_constraint = V+(T-3*h**2*M)*c0-3*h**2*Mp**2+6*s.sqrt(2)*h*stream
solution = c0+c1*s.exp(3*h*t)
checks = {
    'vacuum_shift_cancels_at_zero_P': (transformed-L).subs(P,0),
    'galaxy_operator_breaking': transformed-L+Kc*shift*P**3,
    'constraint_compensation': vacuum_constraint.subs({V:V+dv,c0:c0-dv/(T-3*h**2*M)}, simultaneous=True)-vacuum_constraint,
    'on_shell_scalar': s.diff(solution,t,2)-3*h*s.diff(solution,t),
    'rolling_linear_galaxy_coefficient': s.diff(Kc*solution,t)-3*h*Kc*c1*s.exp(3*h*t),
    'shift_invariant_derivative': s.diff(solution+shift,t)-s.diff(solution,t),
}
results = {name:s.simplify(expr)==0 for name,expr in checks.items()}
assert all(results.values()), results
out = {'passed':len(results),'checks':results,
       'exclusions':['T-3*h**2*M must be nonzero for the constraint compensation identity'],
       'scope':'Restricted algebraic shift test and checked source background equations; not a combined theory, source solution, stability proof or 32pi derivation.'}
Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
