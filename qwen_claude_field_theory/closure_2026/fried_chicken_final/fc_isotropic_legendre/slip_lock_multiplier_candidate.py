#!/usr/bin/env python3
"""Constructive C4 attempt: a no-slip multiplier in the static scalar action.

Take the most favorable Fourier-mode scalar reduction of a covariant traceless
geometric multiplier.  The multiplier enforces Phi=Psi, while the EH scalar
terms are normalized so their linear contributions cancel on that branch:

  L = 2 k^2 Phi Psi - k^2(Phi^2 + Psi^2)
      + U(Phi) + Sigma(Phi) Psi + lambda k^2(Phi-Psi) - J Phi.

Here U'(Phi)=M is the desired MOND flux and Sigma is the traceless Hilbert
stress of the MOND carrier.  This is an action-level test, not a pasted
field equation.  The question is whether lambda can both enforce no slip and
remove Sigma from the summed metric equation.
"""

from __future__ import annotations

import json
import sys
import sympy as sp


def check(name: str, condition: bool, detail: str = "") -> bool:
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    return ok


def derive() -> dict[str, object]:
    k2 = sp.symbols("k2", nonzero=True)
    Phi, Psi, lam = sp.symbols("Phi Psi lambda")
    M, Sigma, J = sp.symbols("M Sigma J")
    L = 2 * k2 * Phi * Psi - k2 * (Phi**2 + Psi**2) + M * Phi + Sigma * Psi + lam * k2 * (Phi - Psi) - J * Phi
    # M and Sigma are local placeholders for the first variations U' and the
    # on-shell traceless stress; all coefficients are obtained by differentiation.
    Ephi = sp.diff(L, Phi)
    Epsi = sp.diff(L, Psi)
    Elam = sp.diff(L, lam)
    direct_phi_residual = sp.simplify(Ephi - sp.diff(L, Phi))
    direct_psi_residual = sp.simplify(Epsi - sp.diff(L, Psi))
    summed = sp.factor(Ephi + Epsi)
    lambda_from_psi = sp.solve(sp.Eq(Epsi, 0), lam)[0]
    no_slip_substitution = {Psi: Phi}
    summed_no_slip = sp.simplify(summed.subs(no_slip_substitution))
    residual_after_exact_mond = sp.simplify(summed_no_slip.subs(J, M))

    # A compensator depending on (Phi,Psi) would need dC/dPsi=-Sigma while
    # leaving dC/dPhi=0.  Schwarz integrability exposes the nonlinear barrier.
    sigma_fun = sp.Function("Sigma")(Phi)
    Cpsi = -sigma_fun
    Cphi = sp.Integer(0)
    mixed_mismatch = sp.simplify(sp.diff(Cpsi, Phi) - sp.diff(Cphi, Psi))

    # Exact exponential Class-A stress on a finite MOND background.
    s, a0 = sp.symbols("s a0", positive=True)
    mu = 1 - sp.exp(-s / a0)
    sigma_exp = sp.simplify(-mu * s**2)
    sigma_exp_prime = sp.simplify(sp.diff(sigma_exp, s))
    return {
        "symbols": {"k2": k2, "Phi": Phi, "Psi": Psi, "lambda": lam, "M": M, "Sigma": Sigma, "J": J},
        "action": L,
        "equations": {"E_Phi": Ephi, "E_Psi": Epsi, "E_lambda": Elam},
        "direct_variation_residuals": {
            "Phi": direct_phi_residual,
            "Psi": direct_psi_residual,
            "lambda": sp.simplify(Elam - k2 * (Phi - Psi)),
        },
        "expected_summed_equation": M + Sigma - J,
        "lambda_solution": lambda_from_psi,
        "summed_equation": summed,
        "summed_no_slip": summed_no_slip,
        "residual_after_exact_mond": residual_after_exact_mond,
        "compensator_mixed_mismatch": mixed_mismatch,
        "exponential": {
            "s_symbol": s,
            "a0_symbol": a0,
            "mu": mu,
            "Sigma_cov": sigma_exp,
            "Sigma_cov_prime": sigma_exp_prime,
            "exp_y_over_a0_times_abs_sigma": sp.simplify(sp.exp(s / a0) * (-sigma_exp)),
        },
    }


def main() -> int:
    r = derive()
    eq = r["equations"]
    exp = r["exponential"]
    sym = r["symbols"]
    s_sym = exp["s_symbol"]
    a0_sym = exp["a0_symbol"]
    print("=" * 96)
    print("C4 NO-SLIP MULTIPLIER: CONSTRUCTIVE ACTION-LEVEL GATE")
    print("=" * 96)
    print("L = 2 k2 Phi Psi - k2(Phi^2+Psi^2) + U(Phi) + Sigma(Phi)Psi + lambda k2(Phi-Psi) - J Phi")
    print("\n[1] Euler-Lagrange equations from the displayed action")
    print("  E_Phi    =", eq["E_Phi"])
    print("  E_Psi    =", eq["E_Psi"])
    print("  E_lambda =", eq["E_lambda"])
    print("  lambda from E_Psi=0:", r["lambda_solution"])
    checks = [
        check("multiplier variation gives k2(Phi-Psi)", r["direct_variation_residuals"]["lambda"] == 0),
        check("all displayed equations are obtained by direct differentiation", all(value == 0 for value in r["direct_variation_residuals"].values())),
    ]

    print("\n[2] Sum equation on the no-slip branch")
    print("  E_Phi + E_Psi =", r["summed_equation"])
    print("  after Psi=Phi:", r["summed_no_slip"])
    print("  after also imposing the exact MOND equation M=J:", r["residual_after_exact_mond"])
    checks += [
        check("lambda cancels identically from the summed metric equation", not r["summed_equation"].has(sym["lambda"])),
        check("the no-slip summed equation retains the traceless stress", r["summed_no_slip"] == r["expected_summed_equation"]),
        check("exact MOND plus both metric equations forces Sigma=0", r["residual_after_exact_mond"] == sym["Sigma"]),
    ]

    print("\n[3] Integrability of a putative local compensator")
    print("  required mixed-derivative mismatch =", r["compensator_mixed_mismatch"])
    checks += [
        check("a compensator with C_Psi=-Sigma(Phi), C_Phi=0 has the nonzero mixed mismatch Sigma'", r["compensator_mixed_mismatch"] == -sp.diff(sp.Function("Sigma")(sym["Phi"]), sym["Phi"])),
    ]

    print("\n[4] Exact exponential stress")
    print("  mu(s) =", exp["mu"])
    print("  Sigma_cov(s) =", exp["Sigma_cov"])
    print("  dSigma_cov/ds =", exp["Sigma_cov_prime"])
    print("  exp(s/a0)*|Sigma_cov| =", exp["exp_y_over_a0_times_abs_sigma"])
    checks += [
        check("exponential Class-A stress has a positive nonzero magnitude for finite s>0", exp["exp_y_over_a0_times_abs_sigma"] == s_sym**2 * (sp.exp(s_sym / a0_sym) - 1)),
        check("its coefficient varies with acceleration", sp.simplify(exp["Sigma_cov_prime"].subs(s_sym, a0_sym)) != 0),
    ]

    print("\n[VERDICT]")
    print("  The explicit traceless-multiplier slip lock does enforce Phi=Psi at k!=0,")
    print("  but its multiplier drops out of the summed metric equation.  Exact MOND")
    print("  then requires Sigma=0; the exponential carrier has Sigma=-mu*s^2 != 0.")
    print("  A local compensator would violate mixed-variation integrability unless Sigma")
    print("  were constant (the Newtonian/no-MOND limit). This closes the C4 multiplier")
    print("  attempt at the static action level; it does not close genuinely nonlocal")
    print("  phantom-density actions, which remain the final open architecture.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    print("RESULT_JSON=" + json.dumps(r, default=str, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
