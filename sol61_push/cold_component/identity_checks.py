"""Exact toy-model discriminators for what the cold component does not derive.

These checks do not reconstruct FL1's full coupled action or its galaxy halos.
"""
import json
import sympy as sp

checks = {}
def check(name, condition):
    checks[name] = bool(condition)
    print(f"{'PASS' if condition else 'FAIL'} {name}")

t = sp.symbols('t', real=True)
phi = sp.Function('phi')(t)
m, amplitude, vacuum, scale, charge = sp.symbols('m amplitude vacuum scale charge', positive=True)
lag = sp.diff(phi,t)**2/2-m**2*phi**2/2-vacuum
eom = sp.diff(sp.diff(lag,sp.diff(phi,t)),t)-sp.diff(lag,phi)
check('vacuum_offset_absent_from_scalar_equation', sp.diff(eom,vacuum) == 0)
solution = amplitude*sp.cos(m*t)
check('every_amplitude_solves_fixed_mass_equation', sp.simplify(eom.subs(phi,solution).doit()) == 0)
energy = sp.simplify((sp.diff(solution,t)**2+m**2*solution**2)/2)
check('oscillation_energy_depends_on_amplitude', energy == m**2*amplitude**2/2)
pressure = (sp.diff(solution,t)**2-m**2*solution**2)/2
average = sp.simplify(sp.integrate(pressure,(t,0,2*sp.pi/m))*m/(2*sp.pi))
check('local_harmonic_average_pressure_zero', average == 0)
check('same_vacuum_double_amplitude_quadruples_dust', sp.simplify(energy.subs(amplitude,2*amplitude)-4*energy) == 0)
check('same_amplitude_vacuum_shift_leaves_dust', sp.diff(energy,vacuum) == 0)
rho_d = charge/scale**3
check('conserved_charge_amount_is_independent_input', sp.simplify(scale**3*rho_d) == charge)
check('charge_rescaling_changes_density', sp.simplify(rho_d.subs(charge,2*charge)-2*rho_d) == 0)
phantom, cold = 10, 6
check('max_bookkeeping_is_not_additive_mass', max(phantom,cold) == 10 and phantom+cold == 16)
print(json.dumps({'checks':checks,'scope':'Canonical real harmonic degree of freedom in fixed geometry; exact local oscillation, not an FRW source or halo solution.'},indent=2))
if not all(checks.values()):
    raise SystemExit(1)
