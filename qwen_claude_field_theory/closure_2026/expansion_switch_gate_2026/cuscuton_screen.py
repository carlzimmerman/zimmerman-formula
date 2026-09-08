"""Extended-cuscuton + f((D ln N)^2): a lapse-constraint discriminator.

Source: Iyonaga, Takahashi, Kobayashi, arXiv:1809.10935v2 (2018-12-05),
https://arxiv.org/html/1809.10935v2, Eqs. 14, 24, 42, 48, 78, 84.
The published seed is two-tensor in unitary gauge on a timelike-clock branch.
This script does not transfer that count to the modified action.

Exact symbolic arithmetic. At a point choose h=diag(l1^2,l2^2,l3^2), li>0,
while retaining all six independent components of dot(h). This is a spatial
frame choice, not a diagonal-velocity or isotropic-kinetic truncation. Set the
shift to zero for the Legendre calculation: its restoration contributes the
usual momentum-constraint term, which does not change the lapse Hessian.
Kij=dot(hij)/(2N); unique off-diagonal coordinate momentum is 2*pi^ij.

The lapse functional test keeps a smooth homogeneous Nbar(t)>0 and a(t)>0,
uses fixed comoving k before taking the amplitude to zero, and requires only
f(s)=f(0)+alpha*s+o(s). There is no UV limit, cutoff or FLRW stability claim.
The (pn,C) symbol and multiplier equation are derived; no full constraint
matrix, gravitational DOF count, or k=0 rank is assigned.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import platform

import sympy as s


def _symmetric(values, off_diagonal_factor=1):
    x11, x22, x33, x12, x13, x23 = values
    return s.Matrix([[x11, x12/off_diagonal_factor, x13/off_diagonal_factor],
                     [x12/off_diagonal_factor, x22, x23/off_diagonal_factor],
                     [x13/off_diagonal_factor, x23/off_diagonal_factor, x33]])


def _pb(f, g, coordinates, momenta):
    return s.expand(sum(s.diff(f, q)*s.diff(g, p)-s.diff(f, p)*s.diff(g, q)
                        for q, p in zip(coordinates, momenta)))


@lru_cache(None)
def derive_seed():
    """Differentiate the actual symmetric metric Lagrangian, then invert."""
    scales = s.symbols("l1 l2 l3", positive=True)
    N = s.Symbol("N", positive=True)
    A2, A3, A4, B4, R = s.symbols("A2 A3 A4 B4 R", real=True)
    velocities = s.symbols("hd11 hd22 hd33 hd12 hd13 hd23", real=True)
    momenta = s.symbols("P11 P22 P33 P12 P13 P23", real=True)
    h = s.diag(*[x**2 for x in scales])
    hi, volume = h.inv(), s.prod(scales)
    K = _symmetric(velocities)/(2*N)
    Kmixed, Ktrace = hi*K, s.trace(hi*K)
    L = N*volume*(A2+A3*Ktrace+A4*(Ktrace**2-s.trace(Kmixed*Kmixed))+B4*R)
    raw_momenta = s.Matrix([s.diff(L, v) for v in velocities])
    velocity_hessian = raw_momenta.jacobian(velocities)
    offset = raw_momenta.subs(dict.fromkeys(velocities, 0))
    solution = [s.factor(x) for x in velocity_hessian.inv()*(s.Matrix(momenta)-offset)]
    inverse = dict(zip(velocities, solution))
    Hamiltonian = s.factor((sum(p*v for p, v in zip(momenta, velocities))-L).subs(inverse))
    pi = _symmetric(momenta, 2)
    pi_velocity = _symmetric(list(raw_momenta), 2)
    expected_pi = volume*(A3*hi/2+A4*(Ktrace*hi-hi*K*hi))
    ptrace = s.trace(pi*h)/volume
    J = (s.trace(pi*h*pi*h)-s.trace(pi*h)**2/2)/volume**2
    contracted = N*volume*(-J/A4-A3*ptrace/(2*A4)+3*A3**2/(8*A4)-A2-B4*R)

    u2, v2, v3, u4, b0, b1 = s.symbols("u2 v2 v3 u4 b0 b1", real=True)
    v4 = s.Symbol("v4", positive=True)
    seed_coefficients = {
        A2: u2+v2/N-3*v3**2/(8*v4*N*(N+u4)),
        A3: v3/(N+u4), A4: -v4*N/(N+u4), B4: b0+b1/N,
    }
    seed_H = s.factor(Hamiltonian.subs(seed_coefficients))
    expected_seed = volume*(N*(J/v4-u2-b0*R)+u4*J/v4+v3*ptrace/(2*v4)-v2-b1*R)
    trace = s.Symbol("Ktrace", real=True)
    trace_velocities = dict(zip(velocities, [2*N*scales[i]**2*trace/3
                                           for i in range(3)]+[0, 0, 0]))
    trace_hessian = s.diff(L.subs(trace_velocities), trace, 2)
    # Mutation control: delete precisely the correlated A2 contribution.
    uncorrelated = dict(seed_coefficients)
    uncorrelated[A2] = u2+v2/N
    return dict(
        N=N, A4=A4, scales=scales, velocities=velocities, momenta=momenta,
        h=h, K=K, raw_lagrangian=L, raw_momenta=raw_momenta,
        momentum_tensor_from_velocities=pi_velocity,
        tensor_momentum_residuals=[s.simplify(x) for x in pi_velocity-expected_pi],
        raw_velocity_hessian_determinant=s.factor(velocity_hessian.det()),
        inverse_momentum_residuals=[s.simplify(x) for x in
                                   raw_momenta.subs(inverse)-s.Matrix(momenta)],
        hamilton_velocity_residuals=[s.simplify(s.diff(Hamiltonian, p)-v)
                                    for p, v in zip(momenta, solution)],
        contracted_hamiltonian_residual=s.simplify(Hamiltonian-contracted),
        seed_hamiltonian=seed_H,
        seed_affine_expression=expected_seed,
        seed_affinity_residual=s.simplify(seed_H-expected_seed),
        seed_lapse_hessian=s.factor(s.diff(seed_H, N, 2)),
        seed_trace_hessian=s.factor(trace_hessian.subs(seed_coefficients)),
        uncorrelated_lapse_hessian=s.factor(s.diff(Hamiltonian.subs(uncorrelated), N, 2)),
        regularity="N>0, li>0, v4>0, N+u4!=0; arbitrary symmetric Kij",
    )


@lru_cache(None)
def derive_lapse_variation():
    """Vary the lapse-gradient functional before projecting a real mode."""
    e, x, theta, n, f0, alpha = s.symbols("epsilon x theta n f0 alpha", real=True)
    M, a, Nbar, k, a0, y = s.symbols("M a Nbar k a0 y", positive=True)
    eta = s.Function("eta")(x)
    lapse = Nbar+e*eta
    acceleration2 = s.diff(lapse, x)**2/(a**2*lapse**2)
    # Since s=O(epsilon^2), the omitted o(s) is o(epsilon^2) at fixed k.
    added_H = -M**2*a**3*lapse*(f0+alpha*acceleration2)
    quadratic = s.factor(s.diff(added_H, e, 2).subs(e, 0)/2)
    variation = s.simplify(s.diff(quadratic, eta)
                           -s.diff(s.diff(quadratic, s.diff(eta, x)), x))
    mode_quadratic = quadratic.subs({s.diff(eta, x): -n*k*s.sin(theta),
                                    eta: n*s.cos(theta)})
    # Twice the spatial average, consistent with a canonically normalized
    # real cosine mode. The homogeneous branch is reconstructed separately.
    mode_H = s.simplify(s.integrate(mode_quadratic, (theta, 0, 2*s.pi))/s.pi)
    projected_variation = variation.subs(s.diff(eta, x, 2), -n*k**2*s.cos(theta))
    functional_symbol = s.simplify(projected_variation/(n*s.cos(theta)))
    mode_hessian = s.diff(mode_H, n, 2)
    kernel = 2*a0**2*(1-(1+y)*s.exp(-y))
    kernel_slope = s.simplify(s.diff(kernel, y)/(2*a0**2*y))
    return dict(
        M=M, a=a, Nbar=Nbar, k=k, alpha=alpha, n=n,
        quadratic_functional_density=quadratic, functional_variation=variation,
        mode_hamiltonian=mode_H, mode_hessian=mode_hessian,
        functional_hessian_symbol=functional_symbol,
        mode_variation_residual=s.simplify(mode_hessian-functional_symbol),
        mond_alpha=s.limit(kernel_slope, y, 0, dir="+"),
        kernel_slope_residual=s.simplify(kernel_slope-s.exp(-y)),
    )


@lru_cache(None)
def derive_constraint_symbol():
    """Derive pn -> C and its multiplier coefficient, retaining all drift.

    C0 and Hrest are arbitrary differentiable functions of the remaining six
    metric canonical pairs and time. This parametrizes the affine seed without
    inventing its full spatial Poisson algebra. It proves that ANY remaining
    drift fixes the lapse multiplier when the derived symbol is invertible;
    it does not infer the rank of the other constraints or a full DOF count.
    """
    d = derive_lapse_variation()
    n, pn, t = d["n"], s.Symbol("pn", real=True), s.Symbol("t", real=True)
    qs, ps = s.symbols("q0:6", real=True), s.symbols("p0:6", real=True)
    coordinates, momenta = (n,)+qs, (pn,)+ps
    C0, Hrest = s.Function("C0")(*qs, *ps, t), s.Function("Hrest")(*qs, *ps, t)
    H = n*C0+Hrest+d["mode_hamiltonian"]
    multiplier = s.Symbol("lambda_N", real=True)
    adot, Ndot = s.symbols("adot Nbardot", real=True)

    def time_derivative(expr):
        return s.diff(expr, t)+s.diff(expr, d["a"])*adot+s.diff(expr, d["Nbar"])*Ndot

    secondary = _pb(pn, H, coordinates, momenta)
    constraints = (pn, secondary)
    matrix = s.Matrix([[_pb(f, g, coordinates, momenta) for g in constraints]
                       for f in constraints])
    drift = _pb(secondary, H, coordinates, momenta)+time_derivative(secondary)
    preservation = _pb(secondary, H+multiplier*pn, coordinates, momenta)+time_derivative(secondary)
    multiplier_coefficient = s.diff(preservation, multiplier)
    solved = s.solve(preservation, multiplier)[0]

    def exceptional_control(substitution):
        # Rebuild Hamiltonian and constraint BEFORE any inverse is formed.
        Hcontrol = H.subs(substitution)
        Ccontrol = _pb(pn, Hcontrol, coordinates, momenta)
        condition = _pb(Ccontrol, Hcontrol+multiplier*pn, coordinates, momenta)+time_derivative(Ccontrol)
        return dict(
            hamiltonian=Hcontrol, secondary=Ccontrol,
            primary_secondary_bracket=_pb(pn, Ccontrol, coordinates, momenta),
            multiplier_coefficient=s.diff(condition, multiplier),
            preservation_condition=condition, solved_multiplier=None,
            scope="No full rank or first-class claim; remaining preservation requires a separate analysis",
        )

    return dict(
        hamiltonian=H, primary=pn, secondary=secondary,
        secondary_definition_residual=s.simplify(secondary+s.diff(H, n)),
        primary_secondary_hessian_residual=s.simplify(matrix[0, 1]-d["mode_hessian"]),
        poisson_matrix=matrix, poisson_determinant=s.factor(matrix.det()),
        drift=drift, multiplier_coefficient=multiplier_coefficient,
        solved_multiplier=solved,
        multiplier_preservation_residual=s.simplify(preservation.subs(multiplier, solved)),
        homogeneous=exceptional_control({d["k"]: 0}),
        unmodified=exceptional_control({d["alpha"]: 0}),
    )


def run():
    """Return JSON-serializable scientific results for a combined manifest."""
    seed, lapse, canonical = derive_seed(), derive_lapse_variation(), derive_constraint_symbol()
    checks = {
        "metric_tensor_momenta": seed["tensor_momentum_residuals"] == [0]*9,
        "legendre_inverse": seed["inverse_momentum_residuals"] == [0]*6,
        "hamilton_metric_velocities": seed["hamilton_velocity_residuals"] == [0]*6,
        "legendre_contraction": seed["contracted_hamiltonian_residual"] == 0,
        "seed_affine_identity": seed["seed_affinity_residual"] == 0,
        "seed_lapse_affinity": seed["seed_lapse_hessian"] == 0,
        "seed_trace_not_deleted": seed["seed_trace_hessian"] != 0,
        "uncorrelated_seed_control": seed["uncorrelated_lapse_hessian"] != 0,
        "functional_mode_agreement": lapse["mode_variation_residual"] == 0,
        "derived_mond_slope": lapse["mond_alpha"] == 1,
        "derived_secondary_bracket": canonical["primary_secondary_hessian_residual"] == 0,
        "multiplier_closure": canonical["multiplier_preservation_residual"] == 0,
        "k0_recomputed": canonical["homogeneous"]["multiplier_coefficient"] == 0,
        "unmodified_recomputed": canonical["unmodified"]["multiplier_coefficient"] == 0,
    }
    mond_symbol = s.factor(lapse["mode_hessian"].subs(lapse["alpha"], lapse["mond_alpha"]))
    return {
        "name": "extended_cuscuton_bare_acceleration_screen",
        "source": {"url": "https://arxiv.org/html/1809.10935v2",
                   "version": "1809.10935v2, 2018-12-05", "equations": [14, 24, 42, 48, 78, 84]},
        "software": {"python": platform.python_version(), "sympy": s.__version__},
        "arithmetic": "exact symbolic, no random sampling",
        "checks": checks, "checks_passed": all(checks.values()),
        "two_tensor_gate": "FAIL" if mond_symbol != 0 else "NOT_REFUTED",
        "seed_lapse_hessian": str(seed["seed_lapse_hessian"]),
        "seed_trace_hessian": str(seed["seed_trace_hessian"]),
        "mond_lapse_hessian_symbol": str(mond_symbol),
        "primary_secondary_bracket": str(canonical["poisson_matrix"][0, 1]),
        "lapse_pair_poisson_determinant": str(canonical["poisson_determinant"]),
        "multiplier_coefficient": str(canonical["multiplier_coefficient"]),
        "multiplier_preservation_residual": str(canonical["multiplier_preservation_residual"]),
        "homogeneous_primary_secondary_bracket": str(canonical["homogeneous"]["primary_secondary_bracket"]),
        "homogeneous_scope": canonical["homogeneous"]["scope"],
        "full_nonlinear_dof_count_claimed": False,
        "domain": "M,a,Nbar>0; comoving k!=0; alpha=1; seed N+u4!=0 and v4>0",
        "interpretation": "The bare acceleration addition lifts the lapse-constraint null direction; the seed's scalar-removing preservation condition cannot be inherited.",
        "limitations": ["No full nonlinear constraint rank or stability certificate",
                        "No physical extra-mode kinetic or propagation sign determined",
                        "k=0 and alpha=0 controls rebuilt without dividing by the vanished symbol",
                        "No conclusion about correlated new kinetic or lapse-velocity modifications"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-two-tensor", action="store_true",
                        help="Exit 2 when the modified action fails the two-tensor gate")
    parser.add_argument("--output", type=Path,
                        help="Create a new JSON result exclusively; refuse to overwrite")
    args = parser.parse_args(argv)
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output is not None:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(payload)
    else:
        print(payload, end="")
    if not result["checks_passed"]:
        return 1
    return 2 if args.require_two_tensor and result["two_tensor_gate"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
