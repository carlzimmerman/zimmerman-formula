#!/usr/bin/env python3
"""Bounded independent audit of two legacy constraint-closure claims.

Reference checkpoint: 92ff5f9703bfa9fccc1097fcbbc081e004b548ec.
Audited definitions:
  sf58_full_nonlinear_adm_four_constraint_closure.py, lines 29-81;
  elliptic_corner/constrained_hamiltonian.py, lines 10-31 and 58-80.
The old modules are neither imported nor changed.

Part A is the actual two-canonical-pair mechanical model, not an ADM field
theory. Its four Poisson brackets, full simultaneous weak surface and
multiplier solution are reconstructed from the stated constraint functions.
In particular, solving preservation equations does not waive C_P=K p_q=0.

Part B derives the complete linearized Einstein tensor from the perturbation
h_mu_nu=diag(-2 Phi,-2 Psi,-2 Psi,-2 Psi) of Minkowski space. It then computes
ALL FOUR raised-index divergences, with and without the symmetric tandem
modification G_0mu -> mu G_0mu, G_ij unchanged. mu is constant on the mode;
this bounded case already decides the claimed identity.

A compact C-infinity no-slip witness is
  Phi=Psi=(t^2 x/2) chi(t)chi(x)chi(y)chi(z),
  chi(r)=exp(1-1/(1-r^2)) for |r|<1, zero otherwise.
At the origin, with mu=1/2, the actual divergence is nonzero. The witness can
be multiplied by an arbitrarily small amplitude to stay perturbative.

Default exit 0 means the audit's derivations/checks completed. The optional
--require-legacy-closure gate exits 2 when the computed legacy claims fail.
No conclusion about a new full field theory or its gravitational DOF follows.
No files are written.
"""

import argparse
from functools import lru_cache
import json

import sympy as s


@lru_cache(maxsize=1)
def derive_toy():
    """Use canonical functions, never an assigned Dirac matrix."""
    phi, q, p_phi, p_q, rho = s.symbols("phi q p_phi p_q rho", real=True)
    K, L, A = s.symbols("K L A_kin", positive=True)
    coordinates, momenta = (phi, q), (p_phi, p_q)

    def poisson(left, right):
        return s.expand(sum(s.diff(left, coordinate)*s.diff(right, momentum)
                            - s.diff(left, momentum)*s.diff(right, coordinate)
                            for coordinate, momentum in zip(coordinates, momenta)))

    constraints = s.Matrix([p_phi, phi+q, L*(phi-q)-rho, K*p_q])
    H0 = A*p_q**2/2
    matrix = s.Matrix(len(constraints), len(constraints),
                      lambda i, j: poisson(constraints[i], constraints[j]))
    drift = s.Matrix([poisson(constraint, H0) for constraint in constraints])
    phase_variables = (*coordinates, *momenta)
    weak_surface = s.solve(list(constraints), phase_variables, dict=True)[0]
    weak_residuals = constraints.subs(weak_surface).applyfunc(s.simplify)
    multipliers = s.Matrix(s.symbols("a b c d"))
    solution = s.solve(list(drift+matrix*multipliers), list(multipliers), dict=True)[0]
    weak_multipliers = {symbol: s.simplify(value.subs(weak_surface))
                        for symbol, value in solution.items()}
    preservation_residuals = (drift+matrix*multipliers).subs(solution).applyfunc(s.simplify)
    zero_constraints = constraints.subs({K: 0, L: 0})
    zero_source_equations = [equation for equation in zero_constraints if equation.has(rho)]
    zero_source_solution = s.solve(zero_source_equations, [rho], dict=True)
    zero_nonzero_source = s.solve(list(zero_constraints.subs(rho, 1)), phase_variables, dict=True)
    return {
        "phi": phi, "q": q, "p_phi": p_phi, "p_q": p_q, "rho": rho,
        "K": K, "L": L, "A": A, "constraints": constraints, "H0": H0,
        "dirac_matrix": matrix, "determinant": s.factor(matrix.det()), "rank": matrix.rank(),
        "derived_secondary": drift[2], "weak_surface": weak_surface,
        "constraint_residuals": weak_residuals,
        "multipliers": solution, "weak_multipliers": weak_multipliers,
        "preservation_residuals": preservation_residuals,
        "zero_mode_constraints": zero_constraints,
        "zero_mode_rank": matrix.subs({K: 0, L: 0}).rank(),
        "zero_mode_source_solution": zero_source_solution,
        "zero_mode_nonzero_source_solutions": zero_nonzero_source,
    }


@lru_cache(maxsize=1)
def derive_linear_bianchi():
    """Derive Christoffel -> Ricci -> Einstein -> raised-index divergence.

On the constant flat background, the linear Christoffel symbol uses the
background inverse metric. Products of perturbed Christoffels and the
perturbed inverse times a background metric derivative are higher order
or zero. No Einstein-tensor or divergence formula is inserted.
"""
    coordinates = s.symbols("t x y z", real=True)
    phi = s.Function("Phi")(*coordinates)
    psi = s.Function("Psi")(*coordinates)
    background = s.diag(-1, 1, 1, 1)
    inverse = background.inv()
    perturbation = s.diag(-2*phi, -2*psi, -2*psi, -2*psi)
    dimension = len(coordinates)
    gamma = [[[s.simplify(sum(
        inverse[a, d]*(s.diff(perturbation[d, b], coordinates[c])
                       + s.diff(perturbation[d, c], coordinates[b])
                       - s.diff(perturbation[b, c], coordinates[d]))/2
        for d in range(dimension)))
        for c in range(dimension)] for b in range(dimension)] for a in range(dimension)]
    ricci = s.Matrix(dimension, dimension, lambda b, d: s.simplify(sum(
        s.diff(gamma[a][b][d], coordinates[a])-s.diff(gamma[a][b][a], coordinates[d])
        for a in range(dimension))))
    scalar = s.simplify(sum(inverse[a, b]*ricci[a, b]
                            for a in range(dimension) for b in range(dimension)))
    einstein = (ricci-background*scalar/2).applyfunc(s.simplify)
    mu = s.Symbol("mu", positive=True)
    tandem = einstein.copy()
    for a in range(dimension):
        tandem[0, a] = mu*einstein[0, a]
        tandem[a, 0] = mu*einstein[a, 0]

    def divergence(tensor):
        return s.Matrix([s.simplify(sum(
            inverse[a, b]*s.diff(tensor[a, nu], coordinates[b])
            for a in range(dimension) for b in range(dimension)))
            for nu in range(dimension)])

    # Reproduce the old plus-sign expression on its actual one-direction
    # field family, while the substantive Bianchi audit above keeps all 3D jets.
    legacy_base = s.diff(einstein[0, 0], coordinates[0])+s.diff(einstein[0, 1], coordinates[1])
    psi_1d = s.Function("Psi")(*coordinates[:2])
    legacy_base = s.simplify(legacy_base.subs(psi, psi_1d).doit())

    return {
        "coordinates": coordinates, "Phi": phi, "Psi": psi, "mu": mu,
        "metric_perturbation": perturbation, "ricci": ricci,
        "einstein": einstein, "tandem_einstein": tandem,
        "gr_bianchi": divergence(einstein), "tandem_bianchi": divergence(tandem),
        "legacy_plus_sign_base": legacy_base,
    }


@lru_cache(maxsize=1)
def compact_witness():
    """Evaluate exact jets of a globally smooth compactly supported profile."""
    linear = derive_linear_bianchi()
    t, x, y, z = coordinates = linear["coordinates"]
    bumps = [s.Piecewise((s.exp(1-1/(1-coordinate**2)), s.Abs(coordinate) < 1), (0, True))
             for coordinate in coordinates]
    profile = t**2*x*s.prod(bumps)/2
    # The origin is strictly inside every support interval. All jets there
    # equal the jets of the interior expression; boundary extension is smooth
    # because exp(-1/(1-r^2)) and every derivative vanish at |r|=1.
    interior = t**2*x*s.prod(bump.args[0].expr for bump in bumps)/2
    origin = {coordinate: 0 for coordinate in coordinates}
    tensor_divergence = linear["tandem_bianchi"]
    jets = {derivative: s.simplify(s.diff(interior, *derivative.variables).subs(origin))
            for derivative in tensor_divergence.atoms(s.Derivative)}
    value = tensor_divergence.xreplace(jets).subs({linear["mu"]: s.Rational(1, 2), **origin})
    value = value.applyfunc(s.simplify)
    return {
        "profile": profile, "interior_profile": interior, "slip": s.simplify(profile-profile),
        "compact_support": all(bump.args[-1].expr == 0 for bump in bumps),
        "origin_divergence": value,
    }


def _strings(values):
    return {str(key): str(value) for key, value in values.items()}


def run():
    """JSON-safe evidence with verdicts computed from actual violations."""
    toy, linear, witness = derive_toy(), derive_linear_bianchi(), compact_witness()
    checks = {
        "dirac_antisymmetry": toy["dirac_matrix"]+toy["dirac_matrix"].T == s.zeros(4),
        "full_weak_surface_solves_constraints": toy["constraint_residuals"] == s.zeros(4, 1),
        "multiplier_equations_solved": toy["preservation_residuals"] == s.zeros(4, 1),
        "all_four_gr_bianchi_components_vanish": linear["gr_bianchi"] == s.zeros(4, 1),
        "mu_one_control": linear["tandem_bianchi"].subs(linear["mu"], 1) == s.zeros(4, 1),
        "compact_witness_no_slip": witness["slip"] == 0 and witness["compact_support"],
    }
    violations = {
        "pq_unconstrained_claim": s.simplify(toy["weak_surface"].get(toy["p_q"], toy["p_q"])) == 0,
        "zero_mode_constraint_disappears_claim": toy["zero_mode_constraints"][2] != 0
                                                and not toy["zero_mode_nonzero_source_solutions"],
        "tandem_full_bianchi_claim": any(component != 0 for component in witness["origin_divergence"]),
    }
    algebra_ok = all(checks.values())
    closure = not any(violations.values()) if algebra_ok else None
    return {
        "reference_checkpoint": "92ff5f9703bfa9fccc1097fcbbc081e004b548ec",
        "scope": "Two-pair constant-coefficient mechanical constraints and time-dependent linear metric on Minkowski; not full nonlinear ADM.",
        "algebra_checks_passed": algebra_ok, "checks": checks,
        "violations": violations, "legacy_closure": closure,
        "verdict": "Legacy closure claims refuted within their implemented surrogates."
                   if algebra_ok and any(violations.values()) else
                   "No implemented violation found." if algebra_ok else "Audit inconclusive: algebra checks failed.",
        "toy": {
            "coordinates": [str(toy["phi"]), str(toy["q"])],
            "momenta": [str(toy["p_phi"]), str(toy["p_q"])],
            "constraints": [str(item) for item in toy["constraints"]],
            "dirac_matrix": [[str(item) for item in row] for row in toy["dirac_matrix"].tolist()],
            "determinant": str(toy["determinant"]), "rank": toy["rank"],
            "derived_secondary": str(toy["derived_secondary"]),
            "secondary_note": "K p_q is only a nonzero rescaling of {C_M,H0}; independent positive K does not equal -L A_kin.",
            "full_weak_surface": _strings(toy["weak_surface"]),
            "off_surface_multipliers": _strings(toy["multipliers"]),
            "on_surface_multipliers": _strings(toy["weak_multipliers"]),
            "zero_mode_constraints": [str(item) for item in toy["zero_mode_constraints"]],
            "zero_mode_rank": toy["zero_mode_rank"],
            "zero_mode_source_solution": [_strings(item) for item in toy["zero_mode_source_solution"]],
            "zero_mode_nonzero_source_solution_count": len(toy["zero_mode_nonzero_source_solutions"]),
            "limit": "Matter dynamics, nonlinear differential operators, homogeneous Friedmann constraints and the ADM tensor sector are absent.",
        },
        "linear_metric": {
            "einstein": [[str(item) for item in row] for row in linear["einstein"].tolist()],
            "correct_divergence": "partial^mu G_mu_nu = -partial_t G_0nu + sum_i partial_i G_inu",
            "gr_bianchi_all_four": [str(item) for item in linear["gr_bianchi"]],
            "tandem_bianchi_all_four": [str(item) for item in linear["tandem_bianchi"]],
            "legacy_plus_sign_base": str(linear["legacy_plus_sign_base"]),
            "compact_witness": "Phi=Psi=t^2*x/2 times product chi(t)chi(x)chi(y)chi(z), chi(r)=exp(1-1/(1-r^2)) inside |r|<1, zero otherwise",
            "compact_witness_mu": "1/2",
            "compact_witness_origin_divergence": [str(item) for item in witness["origin_divergence"]],
            "limit": "Constant mu already fails the identity; no scalar-ghost or full constraint-count result is inferred from G00 lacking second time derivatives.",
        },
        "gravitational_dof_count": None,
        "reusable_results": ["Canonical finite-matrix calculation with the full weak surface imposed",
                             "Unmodified linearized Einstein tensor and all four GR Bianchi identities"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-legacy-closure", action="store_true")
    arguments = parser.parse_args(argv)
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    if not result["algebra_checks_passed"]:
        return 1
    return 2 if arguments.require_legacy_closure and result["legacy_closure"] is not True else 0


if __name__ == "__main__":
    raise SystemExit(main())
