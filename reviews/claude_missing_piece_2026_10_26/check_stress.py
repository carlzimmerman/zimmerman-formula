"""Bounded diagnostic, not a halo-formation model or a fitted mechanism."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, simpson


def shape(x):
    return 1.0 / ((1.0 + x) * (1.0 + x*x))


def mass_shape(x):
    # M = pi rho0 r0^3 B(x). Avoid cancellation at the origin.
    if x < 0.01:
        return 4.0 * sum((x**(4*k+3)/(4*k+3) - x**(4*k+4)/(4*k+4))
                         for k in range(5))
    return 2.0*math.log1p(x) + math.log1p(x*x) - 2.0*math.atan(x)


def integrand(x):
    return 0.0 if x == 0 else math.pi * shape(x) * mass_shape(x) / x**2


def covariance(velocities):
    v = np.asarray(velocities, dtype=float)
    u = v.mean(axis=0)
    w = v-u
    return w.T @ w / len(v)


def gate(p):
    # Illustrative smooth diagnostic: P_star = 1 in these test units.
    d = max(0.0, float(np.linalg.det(p)))
    return d / (1.0 + d)


C, err = quad(integrand, 0, np.inf, epsabs=1e-11, epsrel=1e-11)
lx = np.linspace(-16, 18, 40001)
xx = np.exp(lx)
C_grid = simpson(np.array([integrand(x)*x for x in xx]), x=lx)
# Independent enclosed mass quadrature at nontrivial radii.
mass_errors = []
for x in (0.001, 0.02, 0.3, 1., 10., 100.):
    mq = quad(lambda t: 4*t*t*shape(t), 0, x, epsabs=1e-12)[0]
    mass_errors.append(abs(mass_shape(x)-mq)/mq)

streams = {
    "single": [[2, 3, 4]],
    "sheet": [[-1, 0, 0], [1, 0, 0]],
    "filament": [[-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0]],
    "three_dimensional": [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]],
}
states = {k: {"covariance": covariance(v).tolist(), "gate": gate(covariance(v))}
          for k, v in streams.items()}
boost = np.array([3., -2., 5.])
boost_error = max(np.max(np.abs(covariance(v)-covariance(np.array(v)+boost)))
                  for v in streams.values())
theta = 0.7
rot = np.array([[math.cos(theta), -math.sin(theta), 0],
                [math.sin(theta), math.cos(theta), 0], [0, 0, 1]])
rotation_error = max(abs(gate(covariance(v))-gate(covariance(np.array(v)@rot.T)))
                     for v in streams.values())
checks = {
    "quadrature_agreement": abs(C-C_grid) < 1e-9,
    "mass_identity": max(mass_errors) < 1e-8,
    "off_single_sheet_filament": all(states[k]["gate"] == 0 for k in
                                     ("single", "sheet", "filament")),
    "on_three_dimensional": abs(states["three_dimensional"]["gate"]-.5) < 1e-14,
    "galilean_invariance": boost_error < 1e-12,
    "rotation_invariance": rotation_error < 1e-12,
    "nonzero_warm_background": gate(.1*np.eye(3)) > 0,
    "nonzero_core_center_stress": C > 0,
}
checks = {key: bool(value) for key, value in checks.items()}
result = {
    "claim": "Conditional Jeans stress identity and finite kinetic-selector counterexamples only",
    "assumptions": ["spherical isotropic self-gravitating Burkert halo", "no baryons",
                    "zero pressure at infinity", "no Lambda force in local Jeans calculation",
                    "positive classical kinetic covariance; no field-action bridge asserted"],
    "C_in_P0_equals_C_G_Sigma_squared": C,
    "quad_error_estimate": err,
    "independent_log_simpson_C": float(C_grid),
    "floor_P0_over_a0_squared_over_G": C/(4*math.pi**2),
    "canonical_floor_P0_over_rhoLambda_c_squared": C/(16*math.pi**2),
    "floor_pressure_Pa": {name: C*a0*a0/(4*math.pi**2*6.67430e-11)
                          for name, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10))},
    "finite_outer_radius_C": {str(x): quad(integrand, 0, x, epsabs=1e-11)[0]
                              for x in (3., 10., 30., 100.)},
    "states": states,
    "warm_isotropic_covariance_0p1_gate": gate(.1*np.eye(3)),
    "galilean_error": float(boost_error),
    "rotation_error": float(rotation_error),
    "checks": checks,
    "non_claims": ["No action, selected coefficient, floor, stable attractor, cooling, RAR or fit derived",
                   "No guarantee of early-universe safety for finite primordial dispersion",
                   "No claim that full-rank stress implies boundness"],
}
out = Path(sys.argv[1])
out.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"C": C, "canonical_pressure_ratio": C/(16*math.pi**2),
                  "checks": checks}, indent=2))
assert all(checks.values())
