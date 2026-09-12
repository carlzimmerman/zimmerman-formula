#!/usr/bin/env python3
"""Two conserved scalar-potential currents: action, constraints and principal symbol.

Dimensionless local units c=1, density unit n_* and energy-density unit E_*.
This is a prospective matter/clock sector, not a certified MOND gravity action.
No phenomenological kick rate, expected rank, or wave speed is an input.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import sympy as s


TIME = [0, 4]
SPACE = [1, 2, 3, 5, 6, 7]
CURRENT = s.symbols("r1 j1x j1y j1z r2 j2x j2y j2z", real=True)


def master():
    j = CURRENT
    n1 = s.sqrt(j[0]**2-s.Add(*(v*v for v in j[1:4])))
    n2 = s.sqrt(j[4]**2-s.Add(*(v*v for v in j[5:8])))
    cross = j[0]*j[4]-sum(j[i]*j[i+4] for i in range(1, 4))
    relative = cross-n1*n2
    # Fixed rational witness selected by health search, NOT first principles.
    lagrangian = (-n1-n2+relative/16
                  +(s.Rational(5, 2)-(n1+n2)**2/8
                    -s.Rational(5, 3)*(n1-n2)**2)*relative**2)
    return lagrangian, n1, n2, relative


def background(v, density=s.Integer(1)):
    gamma = 1/s.sqrt(1-v*v)
    return dict(zip(CURRENT, [density*gamma, density*gamma*v, 0, 0,
                              density*gamma, -density*gamma*v, 0, 0]))


def hessian_at(lagrangian, v):
    return s.hessian(lagrangian, CURRENT).subs(background(v)).applyfunc(s.simplify)


def principal(hessian):
    """Eliminate algebraic currents from L2=δJ·∂δθ+δJ H δJ/2.

    L2_reduced=-∂δθ H^{-1} ∂δθ/2. The two scalar wave symbol is
    D=P H^{-1} P^T, P_A=(-ω,kx,ky,kz) on the A-th current block.
    Axial symmetry allows kz=0 and kx=z, ky=sqrt(1-z²), |k|=1.
    """
    c, z, t, u = s.symbols("c z t u", real=True)
    inverse = hessian.inv()
    projection = s.zeros(2, 8)
    for a in range(2):
        projection[a, 4*a:4*a+4] = s.Matrix([[-c, z, s.sqrt(1-z*z), 0]])
    symbol = (projection*inverse*projection.T).applyfunc(s.simplify)
    determinant = s.factor(symbol.det())
    numerator = s.Poly(s.fraction(determinant)[0], c, z).primitive()[1].as_expr()
    polynomial = s.Poly(numerator, c, z)
    assert all(i % 2 == 0 and j % 2 == 0 for (i, j), _ in polynomial.terms())
    reduced = sum(coef*u**(i//2)*t**(j//2) for (i, j), coef in polynomial.terms())
    if s.Poly(reduced, u).LC() < 0:
        reduced = -reduced
    return inverse, s.expand(reduced), (u, t), symbol


def bernstein_quadratic(expression, t):
    polynomial = s.Poly(expression, t)
    assert polynomial.degree() <= 2
    a, b, c = (polynomial.nth(i) for i in range(3))
    coefficients = [a, a+b/2, a+b+c]
    reconstructed = (coefficients[0]*(1-t)**2
                     +2*coefficients[1]*t*(1-t)+coefficients[2]*t*t)
    assert s.expand(reconstructed-expression) == 0
    return coefficients


def dirac(hessian, nonzero_k):
    """Actual canonical matrix for a homogeneous quadratic background.

    k=0: one real zero mode. k=1: BOTH real Fourier quadratures,
    including the mixed density/current Hessian entries. No frozen parity
    truncation is made on a flowing background.
    """
    harmonics = 2 if nonzero_k else 1
    nt = 2*harmonics
    theta = s.Matrix(s.symbols(f"theta0:{nt}"))
    currents = s.Matrix(s.symbols(f"J0:{8*harmonics}"))
    coordinates = s.Matrix([*theta, *currents])
    momenta = s.Matrix(s.symbols(f"p0:{len(coordinates)}"))
    phase = s.Matrix([*coordinates, *momenta])
    nq = len(coordinates)
    omega = s.zeros(2*nq)
    omega[:nq, nq:] = s.eye(nq)
    omega[nq:, :nq] = -s.eye(nq)
    kinetic_cross = 0
    if nonzero_k:
        for a in range(2):
            kinetic_cross += currents[4*a+1]*theta[2+a]
            kinetic_cross -= currents[8+4*a+1]*theta[a]
    hamiltonian = -kinetic_cross
    for parity in range(harmonics):
        block = currents[8*parity:8*parity+8, :]
        hamiltonian -= (block.T*hessian*block)[0]/2
    primary = [momenta[2*p+a]-currents[8*p+4*a]
               for p in range(harmonics) for a in range(2)]
    primary += list(momenta[nt:])
    primary_matrix = s.Matrix(primary).jacobian(phase)
    hamiltonian_matrix = s.hessian(hamiltonian, phase)
    # Preservation of each spatial-current momentum generates its EL equation.
    secondary = [s.diff(hamiltonian, currents[8*p+i])
                 for p in range(harmonics) for i in SPACE]
    constraints = primary+secondary
    constraint_matrix = s.Matrix(constraints).jacobian(phase)
    bracket = constraint_matrix*omega*constraint_matrix.T
    rank = bracket.rank()
    independent = constraint_matrix.rank()
    first_class = independent-rank
    # Stabilize on the ACTUAL constraint surface, represented by its nullspace.
    surface = s.Matrix.hstack(*constraint_matrix.nullspace())
    multiplier_matrix = constraint_matrix*omega*primary_matrix.T
    preservation = -constraint_matrix*omega*hamiltonian_matrix*surface
    multipliers, free = multiplier_matrix.gauss_jordan_solve(preservation)
    residual = multiplier_matrix*multipliers-preservation
    assert residual == s.zeros(*residual.shape)
    return {
        "quadratures": harmonics, "phase_dimension": len(phase),
        "primary_count": len(primary), "secondary_count": len(secondary),
        "primary_constraints": list(map(str, primary)),
        "secondary_constraints": list(map(str, secondary)),
        "poisson_matrix": [[str(x) for x in bracket.row(i)] for i in range(bracket.rows)],
        "poisson_determinant": str(bracket.det()), "poisson_rank": rank,
        "first_class": first_class, "second_class": rank,
        "physical_canonical_pairs": str((len(phase)-2*first_class-rank)/s.Integer(2)),
        "free_multiplier_parameters": len(free),
        "closure_residual_zero": residual == s.zeros(*residual.shape),
        "scope": "current sector quadratic about the specified fixed metric/background; NOT the coupled gravity Dirac algebra"}


def spectrum_scan(hessian):
    inverse, polynomial, (u, t), _ = principal(hessian)
    a = polynomial.coeff(u, 2)
    b = polynomial.coeff(u, 1)
    c = polynomial.coeff(u, 0)
    samples = []
    for tv in np.linspace(0, 1, 101):
        roots = np.roots([float(a), float(b.subs(t, tv)), float(c.subs(t, tv))])
        samples.append({"cos_angle_squared": float(tv),
                        "speed_squared_roots": [[float(z.real), float(z.imag)] for z in roots]})
    return inverse, polynomial, (u, t), samples


def calculate():
    lagrangian, n1, n2, relative = master()
    coflow = hessian_at(lagrangian, s.Integer(0))
    witness = hessian_at(lagrangian, s.Rational(3, 5))
    inverse, polynomial, (u, t), samples = spectrum_scan(witness)
    A, B, C = (polynomial.coeff(u, p) for p in (2, 1, 0))
    certificates = {"C": bernstein_quadratic(C, t),
                    "discriminant": bernstein_quadratic(B*B-4*A*C, t),
                    "polynomial_at_one": bernstein_quadratic(A+B+C, t)}
    assert all(x > 0 for values in certificates.values() for x in values)
    assert all(B.subs(t, x) < 0 and (2*A+B).subs(t, x) > 0 for x in (0, 1))
    assert all(x < 0 for x in witness.extract(TIME, TIME).eigenvals())
    assert all(x > 0 for x in witness.extract(SPACE, SPACE).eigenvals())
    # Exact baseline comparison, directly varied rather than assigned speeds.
    baseline = -n1-n2+relative/10
    _, baseline_p, (bu, bt), _ = principal(hessian_at(baseline, s.Rational(3, 5)))
    transverse_roots = s.solve(baseline_p.subs(bt, 0), bu)
    assert any(r < 0 for r in transverse_roots)
    # Attack the path from coflow to the healthy point using the SAME action.
    path = []
    for v in (s.Rational(1, 1000), s.Rational(1, 100), s.Rational(1, 10),
              s.Rational(1, 5), s.Rational(2, 5), s.Rational(1, 2), s.Rational(3, 5)):
        h = hessian_at(lagrangian, v)
        inv, p, (pu, pt), _ = principal(h)
        roots = s.solve(p.subs(pt, 0), pu)
        kinetic = -inv.extract(TIME, TIME)
        path.append({"v": str(v), "transverse_speed_squared": list(map(str, roots)),
                     "transverse_numeric": [float(s.N(r)) for r in roots],
                     "kinetic_eigenvalues": {str(a): b for a, b in kinetic.eigenvals().items()},
                     "spatial_current_hessian_determinant": str(h.extract(SPACE, SPACE).det())})
    # Homogeneous interaction and its first derivatives vanish, even though its
    # spatial Hessian (entrainment) need not vanish. Avoid the common false step.
    interaction = lagrangian+n1+n2
    q1, q2 = s.symbols("q1 q2", positive=True)
    comoving_subs = dict(zip(CURRENT, [q1, 0, 0, 0, q2, 0, 0, 0]))
    assert s.simplify(interaction.subs(comoving_subs)) == 0
    assert all(s.simplify(s.diff(interaction, j).subs(comoving_subs)) == 0 for j in CURRENT)
    assert coflow.extract(TIME, TIME) == s.zeros(2)
    # An exact neighbourhood test, not just the seven path samples.
    v = s.Symbol("v", positive=True)
    symbolic_inverse = hessian_at(lagrangian, v).inv()
    transverse_symmetric = s.factor(
        -(symbolic_inverse[2, 2]+symbolic_inverse[2, 6])
        /(symbolic_inverse[0, 0]+symbolic_inverse[0, 4]))
    low_v_limit = s.limit(transverse_symmetric/v**2, v, 0, dir="+")
    return {
        "action_master": str(lagrangian),
        "scope": "explicit two-current continuum sector; fixed rational coefficients chosen by mathematical search; not a complete MOND action",
        "coflow": {"interaction_and_first_variation_zero": True,
                   "temporal_current_hessian": str(coflow.extract(TIME, TIME)),
                   "spatial_current_hessian": str(coflow.extract(SPACE, SPACE)),
                   "dirac_k0": dirac(coflow, False), "dirac_k1": dirac(coflow, True)},
        "healthy_witness": {"proper_densities": [1, 1], "velocities": ["3/5", "-3/5"],
                            "current_hessian": str(witness),
                            "temporal_hessian_eigenvalues": {str(a): b for a, b in witness.extract(TIME, TIME).eigenvals().items()},
                            "spatial_hessian_eigenvalues": {str(a): b for a, b in witness.extract(SPACE, SPACE).eigenvals().items()},
                            "polynomial_in_speed_squared": str(polynomial),
                            "bernstein_coefficients": {k: list(map(str, v)) for k, v in certificates.items()},
                            "all_angles_polynomial_certificate": True,
                            "samples": samples,
                            "dirac_k0": dirac(witness, False), "dirac_k1": dirac(witness, True)},
        "baseline": {"polynomial": str(baseline_p), "transverse_speed_squared": list(map(str, transverse_roots))},
        "same_action_path": path,
        "small_velocity_branch": {"exact_squared_speed": str(transverse_symmetric),
                                  "limit_speed_squared_over_v_squared": str(low_v_limit)},
        "nonclaims": ["No action-derived value of kappa or any new coefficient",
                      "No CMB likelihood, MOND force, lensing, PPN or halo depletion calculation",
                      "No coupled metric-clock-current nonlinear constraint count",
                      "Two current scalar modes are actual field matter modes, not auxiliaries",
                      "Coflow dust degeneracy/caustics and connection to healthy counterflow remain physical gates",
                      "No inference from stale L191 output; no new particle decay mechanism"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = calculate()
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2)+"\n")
    for branch in ("coflow", "healthy_witness"):
        for sector in ("dirac_k0", "dirac_k1"):
            d = result[branch][sector]
            print(branch, sector, "primary", d["primary_count"], "secondary", d["secondary_count"],
                  "PB rank", d["poisson_rank"], "pairs", d["physical_canonical_pairs"],
                  "closure", d["closure_residual_zero"])
    print("Exact all-angle local witness:", result["healthy_witness"]["polynomial_in_speed_squared"])
    print("Path transverse speeds:", [(p["v"], p["transverse_numeric"]) for p in result["same_action_path"]])
    print("Algebra checks completed. Full theory OPEN; read same-action path before inferring health.")


if __name__ == "__main__":
    main()
