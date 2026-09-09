#!/usr/bin/env python3
"""Action-level principal-symbol gate for the affine F(Q)Theta route.

This is the next check after ``fqtheta_adm_scalar_dirac.py``.  The earlier
gate kept the lower-derivative scalar jet generic.  Here the three load-bearing
spatial coefficients are derived from the displayed action itself:

    S = int sqrt(-g) [ M2 R/2 - K(Q) + F(Q) Theta
                       + 2 M2 a0**2 G(|V|/a0) ] + S_m,
    G(y) = y**2 + 2(1+y) exp(-y) - 2.

For a one-dimensional weak-field Fourier mode the Einstein part gives
U_zz=4 M2 and U_nz=-4 M2, while expansion of the constitutive term around a
nonzero longitudinal background y0 gives U_pp=2 M2 G''(y0).  These values are
obtained by differentiating and averaging the action, not inserted as a
rank/determinant/DOF target.  They are then fed into a fresh Dirac chain.

The result is deliberately narrow.  On every sampled y0>0 and expanding
H0!=0 branch, k!=0 has one scalar configuration DOF, with

    lambda^2 + Q0^2 G''(y0)/2 = 0

and a reduced symplectic coefficient proportional to k^2.  At k=0 the same
jet has zero scalar DOF.  As y0->0, G''(y0)->0 and the constitutive operator
loses ellipticity.  This is a concrete non-uniform-limit obstruction to a
controlled auxiliary field; it is not a universal no-go for other actions.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def avg_theta(expr, theta):
    """Average a trigonometric polynomial over one spatial period."""
    return sp.simplify(sp.integrate(sp.expand_trig(expr), (theta, 0, 2 * sp.pi))
                       / (2 * sp.pi))


def derive_action_jet():
    """Differentiate the weak-field static action to obtain Uzz, Unz, Upp."""
    eps, theta, k = sp.symbols("epsilon theta k", real=True, positive=True)
    M2, a0, y0 = sp.symbols("M2 a0 y0", positive=True, real=True)
    nA, zA, pA = sp.symbols("nA zA pA", real=True)
    G = lambda y: y**2 + 2 * (1 + y) * sp.exp(-y) - 2

    # All perturbations use the same real sine mode.  Spatial derivatives are
    # k*d/dtheta; the background MOND gradient is a0*y0 along the mode axis.
    n = eps * nA * sp.sin(theta)
    z = eps * zA * sp.sin(theta)
    p = eps * pA * sp.sin(theta)
    dn = k * sp.diff(n, theta)
    dz = k * sp.diff(z, theta)
    dp = k * sp.diff(p, theta)

    # The independently varied weak-field Einstein potentials are the same
    # ones used by fqtheta_gate.py: M2(2 Psi'^2 - 4 Phi' Psi').
    L_eh = M2 * (2 * dz**2 - 4 * dn * dz)
    # Longitudinal V-gradient; y0>0 fixes the smooth local branch of |V|.
    L_mond = 2 * M2 * a0**2 * G(y0 + dp / a0)
    L2 = sp.diff(L_eh + L_mond, eps, 2).subs(eps, 0) / 2
    # Remove the harmless <sin^2>/<cos^2>=1/2 mode normalization.
    L2_mode = sp.simplify(2 * avg_theta(L2, theta))

    Uzz = sp.simplify(sp.diff(L2_mode, zA, zA) / k**2)
    Unz = sp.simplify(sp.diff(L2_mode, nA, zA) / k**2)
    Upp = sp.simplify(sp.diff(L2_mode, pA, pA) / k**2)
    Unn = sp.simplify(sp.diff(L2_mode, nA, nA) / k**2)
    Unp = sp.simplify(sp.diff(L2_mode, nA, pA) / k**2)
    Gpp = sp.simplify(sp.diff(G(sp.Symbol("yy", positive=True)),
                             sp.Symbol("yy", positive=True), 2))
    # The symbol yy is used only to keep the displayed closed form compact.
    yy = sp.Symbol("yy", positive=True)
    Gpp = sp.simplify(sp.diff(yy**2 + 2 * (1 + yy) * sp.exp(-yy) - 2, yy, 2))
    return {
        "L2_mode": L2_mode,
        "Uzz": Uzz,
        "Unz": Unz,
        "Upp": Upp,
        "Unn": Unn,
        "Unp": Unp,
        "Gpp": Gpp,
        "symbols": {"M2": M2, "a0": a0, "y0": y0, "k": k},
    }


def poisson(A, B, qs, ps):
    return sp.simplify(sum(sp.diff(A, q) * sp.diff(B, p)
                           - sp.diff(A, p) * sp.diff(B, q)
                           for q, p in zip(qs, ps)))


def dirac_from_action_jet(jet):
    """Build the affine principal action and derive its full displayed chain."""
    z, p, beta, n = sp.symbols("z p beta n", real=True)
    pz, pp, pb, pn = sp.symbols("p_z p_p p_beta p_n", real=True)
    M2, Fq, Q0, k, y0, H0 = sp.symbols(
        "M2 Fq Q0 k y0 H0", nonzero=True, real=True
    )
    Uzz, Unz, Upp, Unn, Unp = [jet[name].subs({
        jet["symbols"]["M2"]: M2,
        jet["symbols"]["y0"]: y0,
    }) for name in ("Uzz", "Unz", "Upp", "Unn", "Unp")]
    alpha = sp.simplify(Fq / (2 * M2))
    zdot, pdot = sp.symbols("zdot pdot", real=True)
    svel = zdot - alpha * (pdot - Q0 * n)
    U = (sp.Rational(1, 2) * Uzz * k**2 * z**2
         + sp.Rational(1, 2) * Upp * k**2 * p**2
         + Unz * k**2 * n * z + Unp * k**2 * n * p
         + sp.Rational(1, 2) * Unn * k**2 * n**2)
    L = -3 * M2 * svel**2 + 2 * M2 * k**2 * beta * svel + U

    qs = [z, p, beta, n]
    ps = [pz, pp, pb, pn]
    W = sp.simplify(sp.hessian(L, [zdot, pdot]))
    detW = sp.factor(W.det())

    # Legendre transform on the one null direction.  Every constraint below
    # is generated from this H, rather than assumed from a desired count.
    Hc = sp.simplify(- (2 * M2 * k**2 * beta - pz)**2 / (12 * M2)
                     - alpha * Q0 * n * pz - U)
    primary = [pb, pn, pp + alpha * pz]
    secondary = [
        sp.simplify(k**2 * (2 * M2 * k**2 * beta - pz) / 3),
        sp.simplify(alpha * Q0 * pz + sp.diff(U, n)),
        sp.simplify(sp.diff(U, p) + alpha * sp.diff(U, z)),
    ]
    constraints = primary + secondary
    PB = sp.Matrix([[poisson(A, B, qs, ps) for B in constraints]
                    for A in constraints])
    detPB = sp.factor(PB.det())
    Cjac = sp.Matrix([[sp.diff(c, v) for v in qs + ps]
                      for c in constraints])

    # The sample is a genuine expanding branch (H0=1), nonzero Q0 and y0,
    # and uses only exact action-derived coefficients.
    sample = {M2: sp.Integer(1), Fq: sp.Integer(1), Q0: sp.Integer(1),
              k: sp.Integer(1), y0: sp.Integer(1), H0: sp.Integer(1)}
    pb_sample = PB.subs(sample)
    jac_sample = Cjac.subs(sample)
    count = len(constraints)
    pb_rank = pb_sample.rank()
    jac_rank = jac_sample.rank()
    second = pb_rank
    first = count - second
    dof = sp.simplify(len(qs) - first - sp.Rational(second, 2))

    # k=0 is a separate sector.  Do not carry the k!=0 count across it.
    zero_constraints = [sp.simplify(c.subs(k, 0)) for c in constraints]
    zero_constraints = [c for c in zero_constraints if c != 0]
    zero_pb = sp.Matrix([[poisson(A, B, qs, ps) for B in zero_constraints]
                         for A in zero_constraints])
    zero_jac = sp.Matrix([[sp.diff(c, v) for v in qs + ps]
                          for c in zero_constraints])
    zero_sample = {M2: 1, Fq: 1, Q0: 1, y0: 1, H0: 1}
    zero_pb_rank = zero_pb.subs(zero_sample).rank()
    zero_jac_rank = zero_jac.subs(zero_sample).rank()
    zero_second = zero_pb_rank
    zero_first = len(zero_constraints) - zero_second
    zero_dof = sp.simplify(len(qs) - zero_first - sp.Rational(zero_second, 2))

    # On the diffeomorphism-compatible jet Unn=Unp=0, solve the secondary
    # constraints and derive the reduced symplectic form and characteristic
    # polynomial.  No polynomial is inserted: it is obtained from the flow.
    Uzz0, Unz0, Upp0 = Uzz, Unz, Upp
    pz_red = sp.simplify(-k**2 * Unz0 * z / (alpha * Q0))
    pp_red = sp.simplify(-alpha * pz_red)
    omega = sp.factor(sp.diff(pp_red, z) - sp.diff(pz_red, p))
    Hred = sp.factor(Hc.subs({
        beta: pz_red / (2 * M2 * k**2), pz: pz_red, pp: pp_red,
        n: -(Upp0 * p + alpha * Uzz0 * z) / (alpha * Unz0),
        Unp: 0, Unn: 0,
    }))
    Hz = sp.diff(Hred, z)
    Hp = sp.diff(Hred, p)
    flow = sp.Matrix([[-sp.diff(Hp, z) / omega, -sp.diff(Hp, p) / omega],
                      [sp.diff(Hz, z) / omega, sp.diff(Hz, p) / omega]]).applyfunc(sp.simplify)
    lam = sp.symbols("lambda")
    characteristic = sp.factor(flow.charpoly(lam).as_expr())

    return {
        "quadratic_L": str(L),
        "velocity_hessian": [[str(x) for x in row] for row in W.tolist()],
        "velocity_hessian_determinant": str(detW),
        "primary_constraints": [str(c) for c in primary],
        "secondary_constraints": [str(c) for c in secondary],
        "poisson_matrix": [[str(x) for x in row] for row in PB.tolist()],
        "poisson_determinant": str(detPB),
        "poisson_determinant_constitutive_derivative": str(sp.simplify(sp.diff(detPB, y0))),
        "poisson_determinant_independent_of_y0": sp.simplify(sp.diff(detPB, y0)) == 0,
        "sample": {str(k0): str(v0) for k0, v0 in sample.items()},
        "expanding_branch": {"H0": "1", "Q0": "1", "y0": "1", "k": "1"},
        "local_k_nonzero": {
            "constraint_count": count,
            "constraint_jacobian_rank": jac_rank,
            "poisson_rank": pb_rank,
            "second_class_count": second,
            "first_class_count": first,
            "configuration_dof": str(dof),
        },
        "k_zero": {
            "active_constraints": [str(c) for c in zero_constraints],
            "constraint_jacobian_rank": zero_jac_rank,
            "poisson_rank": zero_pb_rank,
            "second_class_count": zero_second,
            "first_class_count": zero_first,
            "configuration_dof": str(zero_dof),
        },
        "reduced": {
            "symplectic_coefficient": str(omega),
            "Hamiltonian": str(Hred),
            "flow_matrix": [[str(x) for x in row] for row in flow.tolist()],
            "characteristic_polynomial": str(characteristic),
            "frequency_square": str(sp.simplify(Upp0 * Uzz0 * Q0**2 / Unz0**2)),
        },
        "symbols": {"M2": str(M2), "Fq": str(Fq), "Q0": str(Q0),
                    "k": str(k), "y0": str(y0), "H0": str(H0)},
    }


def dust_braiding_dichotomy():
    """Derive the f=0 versus f!=0 expanding-dust alternatives."""
    a, H, M2, f, A, B, Q = sp.symbols("a H M2 f A B Q", real=True)
    k2 = sp.simplify(3 * f**2 / (4 * M2))
    K = k2 * Q**2 + A * Q + B
    charge = sp.simplify(a**3 * (-sp.diff(K, Q) + 3 * H * f))
    rho = sp.simplify(K - Q * sp.diff(K, Q) + 3 * H * Q * f)
    charge_f0 = sp.simplify(charge.subs(f, 0))
    rho_f0 = sp.simplify(rho.subs(f, 0))
    # Along an expanding branch adot=aH, dC/dt is the derivative of the
    # explicit f=0 charge with respect to a.  H!=0 forces A=0.
    dcharge_f0 = sp.simplify(sp.diff(charge_f0, a) * a * H)
    return {
        "affine_K": str(K),
        "charge": str(charge),
        "rho": str(rho),
        "f_zero_charge": str(charge_f0),
        "f_zero_density": str(rho_f0),
        "f_zero_charge_time_derivative_on_FLRW": str(dcharge_f0),
        "f_zero_expanding_requires_A_zero": sp.simplify(dcharge_f0.subs(H, 1) / (-3 * a**3)) == A,
        "f_zero_has_no_dust_term": sp.simplify(sp.diff(rho_f0, A)) == 0,
        "interpretation": "For H!=0, f=0 makes C=-A a^3 and conservation forces A=0, hence C=0; rho=B has no a^-3 component. A nonzero affine dust charge therefore requires f!=0, which is exactly the branch with a nonzero local Poisson determinant for k!=0.",
    }


def build_gate():
    jet = derive_action_jet()
    dirac = dirac_from_action_jet(jet)
    dichotomy = dust_braiding_dichotomy()
    M2, a0, y0 = [jet["symbols"][name] for name in ("M2", "a0", "y0")]
    Gpp = jet["Gpp"]
    # These are independently evaluated constitutive limits, not rank targets.
    constitutive = {
        "Gpp": str(Gpp),
        "Gpp_at_y0_1": str(sp.simplify(Gpp.subs({sp.Symbol("yy", positive=True): 1}))),
        "Gpp_limit_y0_to_0": str(sp.limit(Gpp, sp.Symbol("yy", positive=True), 0, dir="+")),
        "lambda_parallel": str(sp.simplify(Gpp / 2)),
        "lambda_parallel_limit_y0_to_0": str(sp.limit(Gpp / 2, sp.Symbol("yy", positive=True), 0, dir="+")),
    }
    return {
        "action": "M2 R/2 - K(Q) + F(Q) Theta + 2 M2 a0^2 G(|V|/a0)",
        "jet": {k: str(v) for k, v in jet.items() if k not in ("symbols",)},
        "dirac": dirac,
        "dust_braiding_dichotomy": dichotomy,
        "constitutive_limits": constitutive,
        "status": "OPEN",
        "verdict": (
            "The actual exponential action has one local scalar for generic k!=0, "
            "while k=0 has zero scalar DOF; its reduced symplectic coefficient "
            "collapses as k^2 and G''(y)->0 removes longitudinal ellipticity as y->0. "
            "The determinant is independent of the constitutive stiffness. "
            "On the affine dust locus, f=0 makes the expanding conserved charge "
            "trivial, so the nonzero dust branch necessarily has f!=0 and the "
            "one-scalar local sector. This closes the displayed dust mechanism "
            "as a two-tensor-plus-auxiliary theory, but is not a universal no-go."
        ),
        "non_claims": [
            "does not certify the omitted khronon/aether tensor/vector sectors",
            "does not derive PPN coefficients or an inhomogeneous galactic solution",
            "does not turn a finite exact-rank sample into a theorem for every action",
        ],
        "provenance": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "script": str(Path(__file__).resolve()),
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_001" / "actual_principal.json")
    args = parser.parse_args(argv)
    result = build_gate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

    # Executable assertions are identities/structural checks only.  Ranks and
    # determinants are read from the matrices above, never prescribed here.
    jet = derive_action_jet()
    assert sp.simplify(jet["Uzz"] - 4 * jet["symbols"]["M2"]) == 0
    assert sp.simplify(jet["Unz"] + 4 * jet["symbols"]["M2"]) == 0
    assert sp.simplify(jet["Unn"]) == 0 and sp.simplify(jet["Unp"]) == 0
    if result["dirac"]["velocity_hessian_determinant"] != "0":
        raise SystemExit("affine velocity Hessian did not degenerate")
    if result["dirac"]["poisson_determinant"] == "0":
        raise SystemExit("actual local Poisson determinant vanished identically")
    if not result["dirac"]["poisson_determinant_independent_of_y0"]:
        raise SystemExit("local Poisson determinant unexpectedly depends on constitutive y0")
    if not (result["dust_braiding_dichotomy"]["f_zero_expanding_requires_A_zero"]
            and result["dust_braiding_dichotomy"]["f_zero_has_no_dust_term"]):
        raise SystemExit("f=0 expanding-dust dichotomy did not derive")


if __name__ == "__main__":
    main()
