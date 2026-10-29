"""Bounded checks of the kinetic/current-coupling composition theorem.

The proofs are in REPORT.md. This script checks exact algebra and a finite
set of trajectories in a declared collective-coordinate model; it never
evolves the full Vlasov/mediator equations.
"""
import json
import math
import sys
from pathlib import Path

import scipy
from scipy.integrate import solve_ivp
import sympy as s


a = s.symbols('a', positive=True)
adot = s.symbols('adot', real=True)
eye = s.eye(3)
zero = s.zeros(3)
canonical = s.BlockMatrix([[a * eye, zero], [adot * eye, eye / a]]).as_explicit()
symplectic = s.BlockMatrix([[zero, eye], [-eye, zero]]).as_explicit()
symplectic_residual = s.simplify(canonical.T * symplectic * canonical - symplectic)
w = s.Matrix(s.symbols('w1:4'))
magnetic = s.Matrix(s.symbols('b1:4'))
trace_residual = s.expand(w.dot(w.cross(magnetic)))

# Unequal weights and nonzero bulk velocity: no isotropy assumption in the
# force-trace cancellation. All arithmetic through this check is rational.
weights = list(map(s.Rational, [1, 2, 3, 4, 5, 6, 7]))
velocities = [s.Matrix(v) for v in [
    [1, 0, 0], [-2, 0, 0], [0, 3, 0], [0, -4, 0],
    [0, 0, 5], [0, 0, -6], [2, -1, 3]]]
rho = sum(weights)
mean = sum((n * v for n, v in zip(weights, velocities)), s.zeros(3, 1)) / rho
electric = s.Matrix([s.Rational(2, 3), -5, s.Rational(7, 4)])
btest = s.Matrix([2, s.Rational(-1, 3), 5])
power = sum(n * (v - mean).dot(electric + v.cross(btest))
            for n, v in zip(weights, velocities))

# A=1 and fixed material reference density. The two derivatives are with
# respect to log(a) at a=1; they need not agree for an equilibrium EOS.
p = s.symbols('p', positive=True)
kinetic_tangent = s.diff(p / a**5, a).subs(a, 1)
log_tangent = s.diff(p - 3 * s.log(a), a).subs(a, 1)
stiffness = []
for x in [0.03, 0.1, 0.249, 0.25, 0.5, 1.0]:
    pressure = -math.log(x) + 2.0 / 3.0
    stiffness.append({
        'x': x, 'p_over_A': pressure,
        'kinetic_bulk_modulus_over_log_modulus': 5.0 * pressure / 3.0,
        'Dp_minus_Dp_log_over_A_H': -5.0 * pressure + 3.0,
    })

# K0=1/2, W0=-1, I0=1, gamma=0.4. The Hamiltonian/outlet reduction
# is part of the contract; this is not a solution of Vlasov-Poisson.
gamma = 0.4
def potential(radius):
    return 0.5 / radius**2 - 1.0 / radius

def rhs(t, y):
    radius, speed, exported = y
    return [speed, (1.0 - radius) / radius**3 - gamma * speed,
            gamma * speed**2]

trajectories = []
for radius0, speed0 in [(0.55, 0.0), (0.8, 0.0), (1.2, 0.0),
                         (3.0, 0.0), (0.8, 0.4), (2.0, -0.25)]:
    energy0 = 0.5 * speed0**2 + potential(radius0)
    assert energy0 < 0
    sol = solve_ivp(rhs, [0.0, 160.0], [radius0, speed0, 0.0],
                    method='DOP853', rtol=2e-11, atol=2e-13,
                    max_step=0.1)
    assert sol.success
    radius, speed, exported = sol.y
    energy = 0.5 * speed**2 + 0.5 / radius**2 - 1.0 / radius
    trajectories.append({
        'initial_radius': radius0, 'initial_speed': speed0,
        'initial_energy': energy0, 'final_radius': float(radius[-1]),
        'final_speed': float(speed[-1]), 'minimum_radius': float(min(radius)),
        'maximum_radius': float(max(radius)),
        'exported_energy': float(exported[-1]),
        'maximum_absolute_energy_ledger_error':
            float(max(abs(energy + exported - energy0))),
    })

checks = {
    'canonical_homology_preserves_symplectic_form': symplectic_residual == s.zeros(6),
    'general_lorentz_random_work_exactly_zero': trace_residual == 0,
    'unequal_weight_beam_random_work_exactly_zero': power == 0,
    'kinetic_tangent_is_minus_5p': kinetic_tangent == -5 * p,
    'log_tangent_is_minus_3A': log_tangent == -3,
    'compact_log_inner_stiffness_is_strictly_larger':
        all(row['kinetic_bulk_modulus_over_log_modulus'] > 1 for row in stiffness),
    'all_six_reduced_trajectories_return':
        all(abs(row['final_radius'] - 1) < 2e-9 and
            abs(row['final_speed']) < 2e-9 for row in trajectories),
    'reciprocal_reduced_energy_ledger':
        max(row['maximum_absolute_energy_ledger_error'] for row in trajectories) < 2e-9,
}
result = {
    'checks': checks, 'exact_beam_random_work': str(power),
    'compact_inner_stiffness_samples': stiffness,
    'reduced_trajectories': trajectories,
    'software': {'Python': sys.version.split()[0], 'SymPy': s.__version__,
                 'SciPy': scipy.__version__},
    'non_claims': [
        'No full kinetic or mediator evolution, nonlinear halo stability, or formation calculation',
        'No vacuum coefficient or central density selection',
        'Reduced homology is not invariant under Vlasov evolution for the compact log halo',
        'Current-only theorem does not exclude relative-velocity couplings or nonlocal heat transport',
    ],
}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
assert all(checks.values())
