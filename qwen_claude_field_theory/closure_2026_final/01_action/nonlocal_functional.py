"""
nonlocal_functional.py
======================
Exact definition of the constitutive function F and the C^2 regulator F_eps,
plus verification of the MOND interpolation identity mu(y) = 1 - e^{-y}.

This module is the foundational algebra for the repaired-normalization candidate.
It is imported by the gate tests and the independent-check modules.

Claim-status labels used in docstrings:
  DERIVED  - follows from the frozen definitions by calculation
  IMPOSED   - a manual regularity / boundary choice
  FITTED   - chosen from observation
  UNKNOWN  - not established
"""
import sympy as sp

# ----------------------------------------------------------------------------
# Symbol setup
# ----------------------------------------------------------------------------
Z, y, w, eps = sp.symbols('Z y w epsilon', positive=True, real=True)
Zr = sp.symbols('Z', real=True)  # real Z (can be negative)


# ----------------------------------------------------------------------------
# 1. The positive-branch constitutive function  (FROZEN, Section 3.4)
#    F_+(Z) = 4 [ 1 - (1 + sqrt(Z)/2) e^{-sqrt(Z)/2} ],   Z >= 0
# ----------------------------------------------------------------------------
def F_plus(z):
    return 4 * (1 - (1 + sp.sqrt(z) / 2) * sp.exp(-sp.sqrt(z) / 2))


def Fp_plus(z):
    """F_+'(Z). FROZEN: (1/2) e^{-sqrt(Z)/2}."""
    return sp.Rational(1, 2) * sp.exp(-sp.sqrt(z) / 2)


def Fpp_plus(z):
    """F_+''(Z). DERIVED: -(1/(8 sqrt(Z))) e^{-sqrt(Z)/2}."""
    return -sp.exp(-sp.sqrt(z) / 2) / (8 * sp.sqrt(z))


def verify_F_derivatives():
    """Verify F_+' and F_+'' against direct differentiation of F_+."""
    F = sp.simplify(F_plus(Z))
    d1 = sp.simplify(sp.diff(F, Z) - Fp_plus(Z))
    d2 = sp.simplify(sp.diff(F_plus(Z), Z, 2) - Fpp_plus(Z))
    # high-precision mpmath derivative checks (robust to cancellation)
    import mpmath as mp
    mp.mp.dps = 50
    def Fnum(z):
        return 4 * (1 - (1 + mp.sqrt(z) / 2) * mp.e**(-mp.sqrt(z) / 2))
    ok1, ok2 = True, True
    for zv in [1e-4, 1e-2, 1.0, 10.0, 100.0]:
        zmp = mp.mpf(zv)
        numd1 = mp.diff(lambda t: Fnum(t), zmp)
        ana1 = float(Fp_plus(Z).subs(Z, zv).evalf(40))
        ok1 = ok1 and abs(float(numd1) - ana1) < 1e-8
        numd2 = mp.diff(lambda t: Fnum(t), zmp, 2)
        ana2 = float(Fpp_plus(Z).subs(Z, zv).evalf(40))
        ok2 = ok2 and abs(float(numd2) - ana2) < 1e-6 * max(1.0, abs(ana2))
    return {
        "Fp_symbolic_residual": d1,
        "Fpp_symbolic_residual": d2,
        "Fp_numeric_ok": bool(ok1),
        "Fpp_numeric_ok": bool(ok2),
        "F_plus_at_0": sp.simplify(F_plus(0)),
        "Fp_plus_at_0": sp.simplify(Fp_plus(0)),
        "Fpp_plus_diverges_at_0": True,  # F_+'' ~ -1/(8 sqrt(Z)) -> -inf as Z->0+
    }


# ----------------------------------------------------------------------------
# 2. MOND interpolation identity  (FROZEN, Section 3.4)
#    mu(y) = 1 - 2 F'(Z)  with Z = 4 y^2  =>  mu(y) = 1 - e^{-y}
# ----------------------------------------------------------------------------
def mu_of_y(yy):
    """mu(y) = 1 - 2 F_+'(Z=4 y^2)."""
    return sp.simplify(1 - 2 * Fp_plus(4 * yy**2))


def verify_mu_identity():
    mu = mu_of_y(y)
    target = 1 - sp.exp(-y)
    return {
        "mu(y)": mu,
        "target": target,
        "residual": sp.simplify(mu - target),
        "identity_holds": bool(sp.simplify(mu - target) == 0),
        "mu_small_y": sp.series(mu, y, 0, 4).removeO(),   # y + O(y^2)
        "mu_large_y": sp.limit(mu, y, sp.oo),            # -> 1
    }


# ----------------------------------------------------------------------------
# 3. C^2 regulator on the Z >= 0 side near Z = 0  (GATE 6 core)
#
# Motivation: F_+''(Z) ~ -1/(8 sqrt(Z)) diverges as Z -> 0+. The regulator
# P_{5,eps}(Z) replaces F_+ on [0, eps] with a degree-5 polynomial that is
# C^2 at Z = eps (matching F_+, F_+', F_+'') and C^2-regular at Z = 0.
#
# Conditions (6 total => unique degree-5 polynomial):
#   P(eps)   = F_+(eps)
#   P'(eps)  = F_+'(eps)
#   P''(eps) = F_+''(eps)
#   P(0)    = 0            (F_+(0) = 0)
#   P'(0)   = 1/2          (F_+'(0) = 1/2; preserves deep-MOND mu -> 0)
#   P''(0)   = 0            (IMPOSED regularity; F_+''(0) diverges)
#
# The two-sided matching at Z = -eps (to the F_- branch) is NOT fully
# determined by the frozen candidate because F_- is not specified. See
# action_derivation.md, Section "F_- gap".
# ----------------------------------------------------------------------------
def build_regulator(eps_val):
    """Return (P(Z) symbolic-in-eps, coefficients) for the [0,eps] C^2 regulator."""
    # Use a scaled variable s = Z/eps in [0,1] for a well-conditioned construction,
    # then return P as a function of Z.
    a  = F_plus(eps)
    ap = Fp_plus(eps)
    app = Fpp_plus(eps)
    # P(Z) = sum_{k=0}^5 c_k Z^k
    c = sp.symbols('c0:6')
    P = sum(c[k] * Z**k for k in range(6))
    eqs = [
        sp.Eq(P.subs(Z, eps), a),
        sp.Eq(sp.diff(P, Z).subs(Z, eps), ap),
        sp.Eq(sp.diff(P, Z, 2).subs(Z, eps), app),
        sp.Eq(P.subs(Z, 0), 0),
        sp.Eq(sp.diff(P, Z).subs(Z, 0), sp.Rational(1, 2)),
        sp.Eq(sp.diff(P, Z, 2).subs(Z, 0), 0),
    ]
    sol = sp.solve(eqs, list(c), dict=True)[0]
    P_sol = sp.simplify(sum(sol[c[k]] * Z**k for k in range(6)))
    return P_sol, sol


def verify_regulator(eps_val=0.1):
    """Numerically verify C^2 continuity of F_eps at Z = eps and regularity at 0."""
    import mpmath as mp
    mp.mp.dps = 40
    ev = mp.mpf(eps_val)

    def Fp(z):  return 4 * (1 - (1 + mp.sqrt(z) / 2) * mp.e**(-mp.sqrt(z) / 2))
    def Fpp(z): return mp.e**(-mp.sqrt(z) / 2) / 2
    def Fppp(z): return -mp.e**(-mp.sqrt(z) / 2) / (8 * mp.sqrt(z))

    # Build regulator numerically via the symbolic coefficients
    P_sol, sol = build_regulator(eps)
    Pnum = sp.lambdify(Z, P_sol.subs(eps, ev), 'mpmath')
    Ppnum = sp.lambdify(Z, sp.diff(P_sol, Z).subs(eps, ev), 'mpmath')
    Pppnum = sp.lambdify(Z, sp.diff(P_sol, Z, 2).subs(eps, ev), 'mpmath')

    # C^2 match at Z = eps
    match_val = abs(float(Pnum(ev)) - float(Fp(ev)))
    match_d1 = abs(float(Ppnum(ev)) - float(Fpp(ev)))
    match_d2 = abs(float(Pppnum(ev)) - float(Fppp(ev)))

    # Regularity at Z = 0
    P0 = float(Pnum(0)); Pp0 = float(Ppnum(0)); Ppp0 = float(Pppnum(0))

    # Pathology checks on [0, eps]: F' should stay in (0, 1/2], mu in [0, 1)
    import numpy as np
    evf = float(ev)
    zs = np.linspace(1e-9, evf, 2000)
    Fp_vals = [float(Fpp(z)) for z in zs]
    P_vals = [float(Ppnum(z)) for z in zs]
    mu_P = [1 - 2 * v for v in P_vals]
    return {
        "C2_match_value_at_eps": match_val,
        "C2_match_d1_at_eps": match_d1,
        "C2_match_d2_at_eps": match_d2,
        "P(0)": P0, "P'(0)": Pp0, "P''(0)": Ppp0,
        "Fp_min_on_[0,eps]": min(Fp_vals),
        "Fp_max_on_[0,eps]": max(Fp_vals),
        "mu_min_on_[0,eps]": min(mu_P),
        "mu_max_on_[0,eps]": max(mu_P),
        "Fp_positive_on_[0,eps]": all(v > 0 for v in Fp_vals + P_vals),
        "mu_in_[0,1]_on_[0,eps]": all(0 <= m < 1 for m in mu_P),
        "regulator_polynomial": sp.simplify(P_sol),
    }


# ----------------------------------------------------------------------------
# 4. Run all foundational verifications
# ----------------------------------------------------------------------------
def run_all():
    out = {}
    out["F_derivatives"] = verify_F_derivatives()
    out["mu_identity"] = verify_mu_identity()
    out["regulator"] = verify_regulator(0.1)
    return out


if __name__ == "__main__":
    import json
    res = run_all()
    # print a human-readable summary (avoid sympy objects in json)
    print("=== F derivatives ===")
    fd = res["F_derivatives"]
    print("  F_+(0) =", fd["F_plus_at_0"], "  F_+'(0) =", fd["Fp_plus_at_0"])
    print("  F_+'' diverges at 0:", fd["Fpp_plus_diverges_at_0"])
    print("  F' numeric ok:", fd["Fp_numeric_ok"], "  F'' numeric ok:", fd["Fpp_numeric_ok"])
    print("=== mu identity ===")
    mi = res["mu_identity"]
    print("  mu(y) =", mi["mu(y)"])
    print("  residual:", mi["residual"], " holds:", mi["identity_holds"])
    print("  small-y expansion:", mi["mu_small_y"])
    print("  large-y limit:", mi["mu_large_y"])
    print("=== C^2 regulator (eps=0.1) ===")
    rg = res["regulator"]
    print("  match value@eps:", rg["C2_match_value_at_eps"])
    print("  match d1@eps:  ", rg["C2_match_d1_at_eps"])
    print("  match d2@eps:  ", rg["C2_match_d2_at_eps"])
    print("  P(0),P'(0),P''(0):", rg["P(0)"], rg["P'(0)"], rg["P''(0)"])
    print("  F' range on [0,eps]:", rg["Fp_min_on_[0,eps]"], rg["Fp_max_on_[0,eps]"])
    print("  mu range on [0,eps]:", rg["mu_min_on_[0,eps]"], rg["mu_max_on_[0,eps]"])
    print("  F' positive:", rg["Fp_positive_on_[0,eps]"], " mu in [0,1):", rg["mu_in_[0,1]_on_[0,eps]"])
