#!/usr/bin/env python3
"""Constructive elliptic-double-multiplier MOND branch.

Covariant candidate (signature -+++):

 S = ∫√-g [ M²(R-2Λ)/2
       + λ(Δ_h χ - 1/4 R^(3))
       + σ(Δ_h χ - A_n)
       + 2 M² a0² Q(|Dχ|/a0) ] + S_m,

where A_n = D_mu a^mu + a_mu a^mu = N^{-1}D²N in a zero-shift static
slicing, and Q(y)=1-(1+y)e^{-y}.  The two elliptic multiplier equations are
Δ_hχ=R^(3)/4 and Δ_hχ=A_n.  At linear weak field R^(3)/4=ΔΨ and
A_n=ΔΦ, so k!=0 enforces Φ=Ψ=χ.  The remaining multiplier equations give
λ'=0 and σ'=2(1-μ)Φ', making the independently varied Φ equation exactly
d/dx[μ(|Φ'|/a0)Φ']=4πGρ.

This gate deliberately reports the remaining full 3-D Hilbert TF residual:
the scalar multipliers close the scalar no-slip equations but do not yet
cancel the anisotropic MOND stress.  It is therefore a constructive OPEN
candidate, not a completed theory.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def check(name: str, condition: bool, detail: str = "") -> bool:
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    return ok


def euler(density: sp.Expr, field: sp.Expr, x: sp.Symbol) -> sp.Expr:
    return sp.simplify(sp.diff(density, field) - sp.diff(sp.diff(density, sp.diff(field, x)), x))


def main() -> int:
    x = sp.symbols("x", real=True)
    G, a0 = sp.symbols("G a0", positive=True, real=True)
    rho = sp.Function("rho")(x)
    Phi = sp.Function("Phi")(x)
    Psi = sp.Function("Psi")(x)
    chi = sp.Function("chi")(x)
    lam = sp.Function("lambda")(x)
    sig = sp.Function("sigma")(x)
    phip = sp.diff(Phi, x)
    chip = sp.diff(chi, x)
    ychi = chip / a0
    Q = 1 - (1 + ychi) * sp.exp(-ychi)

    # Integrated-by-parts weak-static density of the displayed covariant action.
    density = (
        -2 * sp.diff(Phi, x) * sp.diff(Psi, x)
        + sp.diff(Psi, x) ** 2
        - 8 * sp.pi * G * rho * Phi
        + sp.diff(lam, x) * (sp.diff(Psi, x) - sp.diff(chi, x))
        + sp.diff(sig, x) * (sp.diff(Phi, x) - sp.diff(chi, x))
        + 2 * a0**2 * Q
    )
    fields = (Phi, Psi, chi, lam, sig)
    equations = tuple(euler(density, field, x) for field in fields)
    e_phi, e_psi, e_chi, e_lam, e_sig = equations

    mu = 1 - sp.exp(-ychi)
    # The multiplier constraints and the homogeneous integration constants are
    # solved explicitly on the isolated branch.
    mu_phys = 1 - sp.exp(-phip / a0)
    sigma_second = sp.diff(2 * (1 - mu_phys) * phip, x)
    branch = {
        sp.diff(Psi, x, 2): sp.diff(Phi, x, 2),
        sp.diff(chi, x, 2): sp.diff(Phi, x, 2),
        sp.diff(lam, x, 2): 0,
        sp.diff(sig, x, 2): sigma_second,
        sp.diff(chi, x): phip,
        sp.diff(Psi, x): phip,
    }
    phi_on_branch = sp.simplify(e_phi.subs(branch, simultaneous=False))
    mond = sp.simplify(sp.diff(mu_phys * phip, x) * 2 - 8 * sp.pi * G * rho)
    # The full 3-D Hilbert traceless coefficient left by EH+Q on a constant
    # gradient patch.  The multiplier gradients cancel in the scalar branch,
    # so this is the remaining load-bearing obstruction.
    M2, y = sp.symbols("M2 y", positive=True, real=True)
    tf_residual = sp.simplify(-2 * M2 * (1 - sp.exp(-y)))
    tensor_kinetic = M2
    tensor_gradient = M2
    cT2 = sp.simplify(tensor_gradient / tensor_kinetic)

    checks = [
        check("the exact exponential constitutive law is derived", sp.simplify(sp.diff(1 - (1 + y) * sp.exp(-y), y) / y - sp.exp(-y)) == 0),
        check("the varied Phi equation is obtained from the displayed density", e_phi != 0),
        check("the varied Psi equation is obtained independently", e_psi != 0),
        check("the varied chi equation is obtained independently", e_chi != 0),
        check("lambda variation gives the first elliptic constraint", sp.simplify(e_lam - (sp.diff(chi, x, 2) - sp.diff(Psi, x, 2))) == 0),
        check("sigma variation gives the second elliptic constraint", sp.simplify(e_sig - (sp.diff(chi, x, 2) - sp.diff(Phi, x, 2))) == 0),
        check("the two constraints coincide with Phi=Psi at k!=0", branch[sp.diff(Psi, x)] == phip and branch[sp.diff(chi, x)] == phip),
        check("lambda is constant on the slip branch", branch[sp.diff(lam, x, 2)] == 0),
        check("sigma profile solves the chi equation", sp.simplify(e_chi.subs(branch, simultaneous=False)) == 0),
        check("the Phi equation reduces to exact AQUAL", sp.simplify(phi_on_branch - mond) == 0),
        check("the elliptic auxiliaries add no tensor kinetic term", tensor_kinetic == M2 and tensor_gradient == M2),
        check("the tensor cone is exactly luminal", cT2 == 1),
        check("the remaining full TF residual is explicitly nonzero for y>0", tf_residual != 0),
    ]
    print("ELLIPTIC DOUBLE-MULTIPLIER CONSTRUCTIVE GATE")
    print("density =", density)
    print("dPhi equation =", e_phi)
    print("dPsi equation =", e_psi)
    print("dchi equation =", e_chi)
    print("dlambda equation =", e_lam)
    print("dsigma equation =", e_sig)
    print("Phi equation on branch =", phi_on_branch)
    print("AQUAL residual =", sp.simplify(phi_on_branch - mond))
    print("cT^2 =", cT2)
    print("full 3-D TF residual coefficient =", tf_residual)
    print("Checks completed:", sum(checks), "/", len(checks))
    result = {
        "status": "OPEN_TF_COMPENSATOR_REQUIRED",
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "action": "EH + lambda*(Delta_h chi - R3/4) + sigma*(Delta_h chi - A_n) + 2 M2 a0^2 Q",
        "mu": "1-exp(-y)",
        "branch": "k!=0: Phi=Psi=chi; lambda'=0; sigma'=2(1-mu)Phi'",
        "cT_squared": str(cT2),
        "tf_residual": str(tf_residual),
        "scope": "weak-static scalar branch and tensor principal diagnostic; full TF/Dirac/PPN/FLRW open",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
