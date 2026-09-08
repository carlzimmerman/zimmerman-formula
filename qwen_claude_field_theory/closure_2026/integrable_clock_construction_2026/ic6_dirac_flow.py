#!/usr/bin/env python3
"""Bounded IC6 six-component Bianchi I secondary-preservation calculation.

Unit coordinate cell, no matter, no spatial gradients or shift sector. This is
the homogeneous restriction of the IC6 Hamiltonian, not a discretized field
theory. All six metric components and their six canonical momenta are varied.
Actual constraint Jacobians determine the Poisson matrix, ranks and multipliers.
No auxiliary projection occurs during the RK4 evolution.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import time

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = "0b75e72bf5797e451beb258847ade528cd9c4551"
INPUTS = {
    "IC4_ACTION.md": "cb37292e21e0b1fbeef59a20f7800cb3d32c0cd20a46d36fd286cc3dd0f467a8",
    "IC5_ACTION.md": "3a466a7e4d29431bddb9c50a5aff0394c7188f434d562a36cf4c548615396987",
    "TENSOR_BALANCE.md": "9f08824e080a9989c5773cc0d85e53b573b7d69e2e2236d780b6ddf3051ce81c",
    "NONLINEAR_HAMILTONIAN.md": "404909a7e748bab61f0330ca575510da31326cdc8784baa17ba0f3c7fc1130fa",
    "NONLINEAR_SQUARE_REPORT.md": "2a020d25e6b72ec622b13a9674d8ff64fe30c5375c759bfba8338c383f2782bc",
}
ELL = math.log(9./5.)
TCAL = -27./16.+54./(5.*ELL)
A02 = 27.*math.exp(-.5)/(8.*ELL**2)
PR = 8./3.+4.*(3.-81./(4.*TCAL))/3.
AR = 3.*PR/(16.*ELL**2)
BR = 3.*(-1.-3.*PR/8.)/(16.*ELL**2)
PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def verify_sources(expected=None):
    for name, digest in (INPUTS if expected is None else expected).items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != digest:
            raise RuntimeError("Pinned action input changed: " + name)
    return True


class Jet:
    """Value, full gradient and full Hessian by forward second-order AD."""
    def __init__(self, value, gradient=None, hessian=None):
        self.v = float(value)
        self.g = np.zeros(14) if gradient is None else gradient
        self.h = np.zeros((14, 14)) if hessian is None else hessian

    def __add__(self, other):
        if not isinstance(other, Jet):
            other = Jet(other)
        return Jet(self.v+other.v, self.g+other.g, self.h+other.h)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, -self.g, -self.h)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, other):
        if not isinstance(other, Jet):
            other = Jet(other)
        return Jet(self.v*other.v, self.g*other.v+self.v*other.g,
                   self.h*other.v+self.v*other.h
                   +np.outer(self.g, other.g)+np.outer(other.g, self.g))

    __rmul__ = __mul__

    def unary(self, value, first, second):
        return Jet(value, first*self.g, first*self.h+second*np.outer(self.g, self.g))

    def __pow__(self, exponent):
        return self.unary(self.v**exponent, exponent*self.v**(exponent-1.),
                          exponent*(exponent-1.)*self.v**(exponent-2.))

    def __truediv__(self, other):
        return self * (other**-1. if isinstance(other, Jet) else 1./other)

    def __rtruediv__(self, other):
        return other * self**-1.


def exp(value):
    if isinstance(value, Jet):
        result = math.exp(value.v)
        return value.unary(result, result, result)
    return np.exp(value)


def log(value):
    if isinstance(value, Jet):
        return value.unary(math.log(value.v), 1./value.v, -1./value.v**2)
    return np.log(value)


def potential(c):
    ell = log(1.-c)
    return (1.-c)*(ell*ell-2.*ell+2.)-2.


LAMBDA = 6.*math.exp(-.5)-A02*potential(4./9.)


def matrices(y):
    """Coordinate p_12 is 2*pi^12 because pi^ij dg_ij sums both entries."""
    dtype = object if isinstance(y[0], Jet) else np.asarray(y).dtype
    g = np.zeros((3, 3), dtype=dtype)
    pi = np.zeros((3, 3), dtype=dtype)
    for a, (i, j) in enumerate(PAIRS):
        g[i, j] = g[j, i] = y[a]
        pi[i, j] = pi[j, i] = y[6+a]/(1. if i == j else 2.)
    return g, pi


def invariants(y):
    g, pi = matrices(y)
    determinant = (g[0, 0]*g[1, 1]*g[2, 2]+2.*g[0, 1]*g[0, 2]*g[1, 2]
                   -g[0, 0]*g[1, 2]**2-g[1, 1]*g[0, 2]**2-g[2, 2]*g[0, 1]**2)
    volume = determinant**.5
    mixed = g @ pi
    trace = np.trace(mixed)
    shear2 = np.trace(mixed @ mixed)-trace*trace/3.
    return volume, trace, shear2


def invariant_hamiltonian(volume, trace, shear2, xi, u):
    w = (u-1.)*xi
    F = AR*(xi-.25)+BR*(u-2./3.)
    JT = 1.+exp(-6.*w)*trace*trace*F/(volume*volume*A02)
    kinetic = 2.*exp((4.-3.*u)*xi)*(shear2/JT-trace*trace/6.)/volume
    return (kinetic+volume*exp((3.*u-2.)*xi)*(LAMBDA+A02*potential(u*u))
            -3.*volume*exp((3.*u-4.)*xi))


def hamiltonian(y):
    """Exact homogeneous IC6 density in barred canonical variables; m=h0=1."""
    return invariant_hamiltonian(*invariants(y), *y[-2:])


def covariant_value(y, wrong_offdiagonal_factor=False):
    """Independent scalar path: physical metric and physical momentum density."""
    g, pi = matrices(y)
    if wrong_offdiagonal_factor:
        for i, j in PAIRS[3:]:
            pi[i, j] *= 2.
            pi[j, i] *= 2.
    xi, u = y[-2:]
    N, w = np.exp(xi), (u-1.)*xi
    # Cross-product determinant avoids this NumPy/LAPACK build's spurious
    # warnings for tiny imaginary complex-step perturbations.
    determinant = lambda mat: np.dot(mat[0], np.cross(mat[1], mat[2]))
    V = np.sqrt(determinant(g))
    physical_metric = np.exp(2.*w)*g
    physical_momentum = np.exp(-5.*w)*pi/V
    mixed = physical_metric @ physical_momentum
    trace = np.trace(mixed)
    tf = mixed-trace*np.eye(3)/3.
    F = AR*(xi-.25)+BR*(u-2./3.)
    JT = 1.+trace*trace*F/A02
    density = (2.*np.trace(tf @ tf)/JT-trace*trace/3.+LAMBDA
               +A02*potential(u*u)-3./(N*N))
    return N*np.sqrt(determinant(physical_metric))*density


def branches(y):
    g, _ = matrices(y)
    mineig = float(np.linalg.eigvalsh(g)[0])
    if mineig <= 0.:
        raise ValueError("Metric is outside the positive-definite branch")
    xi, u = y[-2:]
    if not 0. < u < 1.:
        raise ValueError("Auxiliary u is outside (0,1)")
    volume, trace, shear2 = invariants(y)
    F = AR*(xi-.25)+BR*(u-2./3.)
    JT = 1.+np.exp(-6.*(u-1.)*xi)*trace*trace*F/(volume*volume*A02)
    r = -trace*np.exp((4.-3.*u)*xi)/(3.*volume)
    if JT <= 0.:
        raise ValueError("IC6 J_T denominator is nonpositive")
    if abs(r*r-1.) >= .25:
        raise ValueError("The reported fixture left the expanding activation plateau")
    return dict(metric_min=mineig, volume=float(volume), trace=float(trace),
                shear_squared=float(shear2), JT=float(JT), F=float(F),
                activation_distance=float(abs(r*r-1.)))


def jets(y):
    eye = np.eye(14)
    return hamiltonian([Jet(value, eye[i]) for i, value in enumerate(y)])


def canonical_matrix():
    """Ordering (g[6], p_g[6], xi, u, p_xi, p_u), all brackets canonical."""
    J = np.zeros((16, 16))
    for i, j in list(zip(range(6), range(6, 12)))+[(12, 14), (13, 15)]:
        J[i, j], J[j, i] = 1., -1.
    return J


CANONICAL = canonical_matrix()
RANK_TOLERANCE = 1e-9


def evaluate(y):
    y = np.asarray(y, dtype=float)
    branch = branches(y)
    H = jets(y)
    S, K = H.g[12:], H.h[12:, 12:]
    constraint_jacobian = np.zeros((4, 16))
    constraint_jacobian[0, 14] = constraint_jacobian[1, 15] = 1.
    constraint_jacobian[2:, :14] = H.h[12:]
    poisson = constraint_jacobian @ CANONICAL @ constraint_jacobian.T
    singular = np.linalg.svd(poisson, compute_uv=False)
    rank = int(np.count_nonzero(singular > RANK_TOLERANCE))
    metric_velocity = np.concatenate((H.g[6:12], -H.g[:6]))
    drift = H.h[12:, :12] @ metric_velocity
    multipliers = np.linalg.solve(K, -drift)
    velocity = np.concatenate((metric_velocity, multipliers))
    # Explicit preservation, not a zero inserted into the output.
    tangency = H.h[12:] @ velocity
    # Deliberately omit {S,H}'s first term for a load-bearing mutation control.
    frozen_metric_drift = -H.h[12:, 6:12] @ H.g[:6]
    wrong_multipliers = np.linalg.solve(K, -frozen_metric_drift)
    return dict(hamiltonian=H.v, secondary=S, K=K, Omega=poisson[2:, 2:],
                drift=drift, multipliers=multipliers, velocity=velocity,
                tangency=tangency, poisson_matrix=poisson,
                poisson_singular_values=singular, constraint_rank=rank,
                constraint_jacobian_rank=int(np.linalg.matrix_rank(constraint_jacobian,
                                                                   tol=RANK_TOLERANCE)),
                homogeneous_configuration_count=(16-rank)/2. if rank == 4 else None,
                frozen_metric_tangency=drift+K @ wrong_multipliers,
                zero_multiplier_tangency=drift, branch=branch)


def initial_state(constrained=True):
    """Deterministic nondiagonal SPD metric and nondiagonal genuine shear."""
    g = np.array([[1.03, .012, -.008], [.012, .98, .009], [-.008, .009, 1.01]])
    values, vectors = np.linalg.eigh(g)
    invroot = (vectors/np.sqrt(values)) @ vectors.T
    shear = np.array([[.04, .012, -.009], [.012, -.025, .007], [-.009, .007, -.015]])
    rho = -3.*math.exp(-.5)*1.007
    pi = np.sqrt(np.linalg.det(g))*invroot @ (rho*np.eye(3)/3.+shear) @ invroot
    y = np.array([g[i, j] for i, j in PAIRS]
                 +[pi[i, j]*(1. if i == j else 2.) for i, j in PAIRS]+[.25, 2./3.])
    if not constrained:
        return y
    for iteration in range(12):
        H = jets(y)
        residual = np.max(np.abs(H.g[12:]))
        if residual < 2e-13:
            branches(y)
            return y
        update = np.linalg.solve(H.h[12:, 12:], -H.g[12:])
        accepted = False
        for power in range(16):
            trial = y.copy()
            trial[12:] += update*2.**(-power)
            try:
                branches(trial)
            except ValueError:
                continue
            if np.max(np.abs(jets(trial).g[12:])) < residual:
                y = trial
                accepted = True
                break
        if not accepted:
            raise RuntimeError("Initial auxiliary Newton step did not descend")
    raise RuntimeError("Initial auxiliary solve exceeded its fixed iteration bound")


def derivative_audit(y):
    """Complex-step covariant first derivatives, then centered Hessian checks."""
    def independent_gradient(state):
        result = np.empty(14)
        for i in range(14):
            shifted = np.asarray(state, dtype=complex).copy()
            shifted[i] += 1e-25j
            result[i] = covariant_value(shifted).imag/1e-25
        return result
    H = jets(y)
    gradient = independent_gradient(y)
    hessian = np.empty((14, 14))
    for j in range(14):
        shift = np.zeros(14)
        shift[j] = 2e-6
        hessian[:, j] = (independent_gradient(y+shift)-independent_gradient(y-shift))/(4e-6)
    return dict(covariant_value_error=float(abs(H.v-covariant_value(y))),
                complex_step_gradient_error=float(np.max(np.abs(H.g-gradient))),
                finite_difference_hessian_error=float(np.max(np.abs(H.h-hessian))),
                hessian_symmetry_error=float(np.max(np.abs(H.h-H.h.T))),
                wrong_offdiagonal_factor_error=float(abs(H.v-covariant_value(y, True))))


def invariant_audit(y):
    """Independent exact invariant Poisson reduction and actual matrix inverse."""
    import sympy as s
    gvars, pvars = s.symbols("g0:6"), s.symbols("p0:6")
    g, pi = s.zeros(3), s.zeros(3)
    for a, (i, j) in enumerate(PAIRS):
        g[i, j] = g[j, i] = gvars[a]
        pi[i, j] = pi[j, i] = pvars[a]/(1 if i == j else 2)
    determinant = g.det()
    trace = s.trace(g*pi)
    shear2 = s.trace(g*pi*g*pi)-trace**2/3
    def bracket(a, b):
        return s.expand(sum(s.diff(a, q)*s.diff(b, p)-s.diff(a, p)*s.diff(b, q)
                            for q, p in zip(gvars, pvars)))
    residuals = [bracket(determinant, trace)-3*determinant,
                 bracket(determinant, shear2), bracket(trace, shear2)]
    residuals = [s.expand(value) for value in residuals]
    volume, trace, shear2 = invariants(y)
    eye = np.eye(14)
    H = invariant_hamiltonian(Jet(volume, eye[0]), Jet(trace, eye[1]),
                             Jet(shear2, eye[2]), Jet(y[12], eye[12]), Jet(y[13], eye[13]))
    invariant_drift = 1.5*volume*(H.h[12:, 0]*H.g[1]-H.h[12:, 1]*H.g[0])
    invariant_Omega = 1.5*volume*(np.outer(H.h[12:, 0], H.h[12:, 1])
                                 -np.outer(H.h[12:, 1], H.h[12:, 0]))
    actual = evaluate(y)
    inverseK = np.linalg.inv(actual["K"])
    inverse = np.block([[inverseK @ actual["Omega"] @ inverseK, inverseK],
                        [-inverseK, np.zeros((2, 2))]])
    return dict(exact_polynomial_residuals=[str(value) for value in residuals],
                invariant_drift_error=float(np.max(np.abs(invariant_drift-actual["drift"]))),
                invariant_Omega_error=float(np.max(np.abs(invariant_Omega-actual["Omega"]))),
                left_inverse_residual=float(np.max(np.abs(inverse @ actual["poisson_matrix"]-np.eye(4)))),
                right_inverse_residual=float(np.max(np.abs(actual["poisson_matrix"] @ inverse-np.eye(4)))))


def integrate(steps=32, end_time=.08):
    """Evolve all metric/auxiliary variables; primary momenta also integrated.

    The multiplier is a prescribed feedback value at each stage. As in Dirac
    preservation it is not differentiated inside the Hamiltonian Poisson bracket.
    Both auxiliary equations are solved only once to initialize the trajectory.
    """
    if not isinstance(steps, int) or not 1 <= steps <= 256 or not 0. < end_time <= .1:
        raise ValueError("Declared run bounds: integer steps 1..256, 0<T<=0.1")
    initial = np.concatenate((initial_state(), [0., 0.]))
    state = initial.copy()
    H0 = evaluate(state[:14])["hamiltonian"]
    dt = end_time/steps
    records = []
    accepted = [evaluate(state[:14])]
    max_accepted_primary = 0.
    max_primary = 0.
    def rhs(point):
        nonlocal max_primary
        data = evaluate(point[:14])
        records.append(data)
        max_primary = max(max_primary, float(np.max(np.abs(point[14:]))))
        return np.concatenate((data["velocity"], -data["secondary"]))
    for step in range(steps):
        k1 = rhs(state)
        k2 = rhs(state+dt*k1/2.)
        k3 = rhs(state+dt*k2/2.)
        k4 = rhs(state+dt*k3)
        state = state+dt*(k1+2.*k2+2.*k3+k4)/6.
        accepted.append(evaluate(state[:14]))
        max_accepted_primary = max(max_accepted_primary, float(np.max(np.abs(state[14:]))))
    rhs(state)
    # Stage values are included: no claim that only accepted endpoints stayed regular.
    branches_seen = [record["branch"] for record in records]
    endpoint = evaluate(state[:14])
    return dict(steps=steps, end_time=end_time, initial_state=initial, final_state=state,
                state_displacement=float(np.linalg.norm(state[:12]-initial[:12])),
                auxiliary_displacement=float(np.linalg.norm(state[12:14]-initial[12:14])),
                max_secondary_residual=max(float(np.max(np.abs(r["secondary"]))) for r in records),
                endpoint_secondary_residual=float(np.max(np.abs(endpoint["secondary"]))),
                max_accepted_secondary_residual=max(float(np.max(np.abs(r["secondary"]))) for r in accepted),
                max_accepted_primary_residual=max_accepted_primary,
                max_accepted_energy_error=max(abs(r["hamiltonian"]-H0) for r in accepted),
                max_primary_residual=max_primary,
                max_tangency_residual=max(float(np.max(np.abs(r["tangency"]))) for r in records),
                max_energy_error=max(abs(r["hamiltonian"]-H0) for r in records),
                endpoint_energy_error=abs(endpoint["hamiltonian"]-H0),
                computed_ranks=sorted(set(r["constraint_rank"] for r in records)),
                computed_constraint_jacobian_ranks=sorted(set(r["constraint_jacobian_rank"] for r in records)),
                inferred_homogeneous_configuration_counts=sorted(set(r["homogeneous_configuration_count"] for r in records)),
                min_poisson_singular_value=min(float(np.min(r["poisson_singular_values"])) for r in records),
                min_abs_K_eigenvalue=min(float(np.min(np.abs(np.linalg.eigvalsh(r["K"])))) for r in records),
                maximum_Omega_entry=max(float(np.max(np.abs(r["Omega"]))) for r in records),
                maximum_multiplier=max(float(np.max(np.abs(r["multipliers"]))) for r in records),
                minimum_metric_eigenvalue=min(r["metric_min"] for r in branches_seen),
                minimum_JT=min(r["JT"] for r in branches_seen),
                maximum_activation_distance=max(r["activation_distance"] for r in branches_seen),
                minimum_shear_squared=min(r["shear_squared"] for r in branches_seen),
                auxiliary_newton_solves_after_initialization=0,
                all_RK_stages_checked=len(records))


def json_safe(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {key: json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(val) for val in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def run():
    import sympy
    start = time.monotonic()
    verify_sources()
    y = initial_state()
    fixture = evaluate(y)
    audit = derivative_audit(initial_state(constrained=False))
    invariant_check = invariant_audit(y)
    trajectories = [integrate(steps) for steps in (16, 32, 64)]
    verify_sources()
    checks = {
        "covariant_value": audit["covariant_value_error"] < 2e-13,
        "all_canonical_first_derivatives": audit["complex_step_gradient_error"] < 2e-11,
        "all_canonical_second_derivatives": audit["finite_difference_hessian_error"] < 2e-7,
        "initial_constraints": np.max(np.abs(fixture["secondary"])) < 1e-11,
        "nonzero_shear_Omega": np.max(np.abs(fixture["Omega"])) > 1e-3,
        "tangent_at_every_stage": all(r["max_tangency_residual"] < 1e-11 for r in trajectories),
        "all_computed_ranks_four": all(r["computed_ranks"] == [4] for r in trajectories),
        "unprojected_endpoint_constraint_refinement": all(
            b["endpoint_secondary_residual"] < a["endpoint_secondary_residual"]/8.
            for a, b in zip(trajectories, trajectories[1:])),
        "all_regular": all(r["minimum_JT"] > .9 and r["maximum_activation_distance"] < .25 for r in trajectories),
        "frozen_metric_mutation_rejected": np.max(np.abs(fixture["frozen_metric_tangency"])) > 1e-3,
        "exact_invariant_brackets": invariant_check["exact_polynomial_residuals"] == ["0", "0", "0"],
        "invariant_drift_and_Omega": max(invariant_check["invariant_drift_error"],
                                         invariant_check["invariant_Omega_error"]) < 1e-11,
        "actual_block_inverse": max(invariant_check["left_inverse_residual"],
                                    invariant_check["right_inverse_residual"]) < 2e-12,
    }
    result = dict(base_commit=BASE, arithmetic="IEEE-754 float64; exact analytic AD formulas, numerical values",
                  convention="(g11,g22,g33,g12,g13,g23,p11,p22,p33,2pi12,2pi13,2pi23,xi,u,p_xi,p_u)",
                  inputs_sha256=INPUTS, implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  software=dict(python=platform.python_version(), numpy=np.__version__,
                                sympy=sympy.__version__),
                  randomness="none", resource_bounds=dict(max_steps=256, max_time=.1,
                  numerical_thread_environment={key: os.environ.get(key) for key in
                    ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")},
                  requested_individual_run_wall_limit_seconds=180,
                  wall_limit_enforcement="external runner; this script itself enforces only step/time bounds"),
                  derivative_audit=audit, invariant_audit=invariant_check,
                  initial_fixture=fixture, trajectories=trajectories,
                  checks=checks, finite_checks_pass=all(checks.values()),
                  field_theory_closure=False,
                  non_claims=["Spatial curvature and auxiliary gradients vanish identically in Bianchi I.",
                              "No spatial momentum constraints, shift constraints, matter or field DOF count are tested.",
                              "No inhomogeneous rank persistence, continuum well-posedness, physical stability or causality proof."],
                  elapsed_seconds=time.monotonic()-start)
    return json_safe(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-field-closure", action="store_true")
    args = parser.parse_args()
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["finite_checks_pass"]:
        return 1
    return 2 if args.require_field_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
