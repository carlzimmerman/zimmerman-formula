#!/usr/bin/env python3
"""D-YM3: can ANY single-scalar action f(K) realise the Hardy-marginal 1/4?

Door H (opus_49_doorH) proved that for the committed interpolant
mu_2(u) = u(2+u)/(1+u)^2 the canonical radial potential V(u) equals the
I14 Hardy-marginal value 1/4 at one isolated radius only.  The reopen
directive says resurrection needs "a DIFFERENT action".  This script swings
that door for the whole class L = Lambda^4 f(K), K = u^2, f'(K) = mu(u), on
sourceless radial backgrounds in n space dimensions, with mu arbitrary.

Exact identities (sympy, generic mu):
  flux     H(u) := u mu(u), sourceless background r^{n-1} H(u0) = J, H' = a_r
  weight   w = r^{n-2} a_r(u0(r)),  a_r = mu + u mu'
  shift    s = (1/2) d ln w / d ln r
  potential V = s^2 + ds/dt,  t = ln r.
Results checked below:
  (1) Newtonian limit mu -> 1 gives s = (n-2)/2 and V = ((n-2)/2)^2, the
      classical Hardy constant of the n-dimensional Laplacian: 1/4 at n = 3.
      So "kappa = 1/2" at n = 3 is a dimension count shared by EVERY theory
      with a Newtonian limit, not framework-specific physics.
  (2) Deep-MOND limit mu(u) = u (1 + O(u)) gives V -> 0 as u -> 0 for every
      such mu (exactly V = 0 for mu = u).  Every EFE-capped physical halo
      lives in this corner (door H: u(r_break) ~ 1e-19).
  (3) V = 1/4 on an interval with s = +1/2 forces a_r = const, i.e.
      mu = A + B/u (Newton plus a sqrt(K) cuscuton-type term): never MOND.
  (4) Door H's committed-mu_2 potential on its log profile u0 = b/r is
      reproduced exactly (consistency); the on-shell flux-conserving
      background is the one used in (1)-(3).
"""
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
u, c = sp.symbols("u c", positive=True)
A, B = sp.symbols("A B", real=True)
mu = sp.Function("mu")


def radial_data(mu_expr, dim):
    """s(u), V(u) along the sourceless background, parametrised by u0 = u.

    Flux conservation in `dim` dimensions: r^{dim-1} mu(u) u = J, so
    H(u) := u mu(u) = J r^{1-dim}.  Quadratic form (L = 0):
    int r^{dim-1} a_r eta_r^2 dr = int w eta_t^2 dt with w = r^{dim-2} a_r.
    With r = (J/H)^{1/(dim-1)}:  d/dt = -(dim-1) (H/H') d/du.
    """
    H = u * mu_expr
    a_r = sp.diff(H, u)                      # = mu + u mu'
    r = (c / H) ** (1 / (dim - 1))
    lnw = (dim - 2) * sp.log(r) + sp.log(a_r)
    d_dt = lambda expr: -(dim - 1) * H / sp.diff(H, u) * sp.diff(expr, u)
    s = sp.simplify(d_dt(lnw) / 2)
    V = sp.simplify(s ** 2 + d_dt(s))
    return a_r, s, V


def radial_data_log(mu_expr):
    """Door H's (off-shell) committed log profile u0 = b/r in n = 3:
    w = r a_r(b/r), d/dt = -u d/du."""
    a_r = sp.diff(u * mu_expr, u)
    lnw = sp.log(c / u) + sp.log(a_r)
    d_dt = lambda expr: -u * sp.diff(expr, u)
    s = sp.simplify(d_dt(lnw) / 2)
    V = sp.simplify(s ** 2 + d_dt(s))
    return a_r, s, V


def run():
    checks = []

    def check(name, predicate, **data):
        checks.append({"name": name, "passed": bool(predicate),
                       **{k: str(v) for k, v in data.items()}})

    # identity h' = a_r for generic mu (n = 3)
    Hg = u * mu(u)
    check("h_prime_equals_a_r",
          sp.simplify(sp.diff(Hg, u) - (mu(u) + u * sp.diff(mu(u), u))) == 0)

    # (1) Newtonian limit, general dimension: Hardy constant ((n-2)/2)^2
    for dim in (3, 4, 5, 6):
        _, s, V = radial_data(sp.Integer(1), dim)
        hardy = sp.Rational(dim - 2, 2) ** 2
        check(f"newtonian_hardy_constant_n{dim}", sp.simplify(V - hardy) == 0,
              s=s, V=V, hardy=hardy)

    # (2) deep MOND: mu = u exactly gives V = 0; generic mu = u + a u^2 + b u^3
    _, s, V = radial_data(u, 3)
    check("pure_deep_mond_V_is_0", sp.simplify(V) == 0, s=s, V=V)
    a2, a3 = sp.symbols("a2 a3", real=True)
    _, s, V = radial_data(u + a2 * u ** 2 + a3 * u ** 3, 3)
    lim = sp.limit(V, u, 0)
    check("generic_deep_mond_V_to_0", lim == 0, limit=lim)
    families = {
        "mu2_committed": u * (2 + u) / (1 + u) ** 2,
        "simple": u / (1 + u),
        "standard": u / sp.sqrt(1 + u ** 2),
    }
    rows = {}
    for name, m in families.items():
        _, s, V = radial_data(m, 3)
        deep = sp.limit(V, u, 0)
        newton = sp.limit(V, u, sp.oo)
        # mu2 and "simple" have mu ~ 2u, u at u -> 0; all have mu -> 1 at infinity
        check(f"{name}_deep_limit_V_0", deep == 0, V_deep=deep)
        check(f"{name}_newton_limit_V_quarter", newton == sp.Rational(1, 4), V_newton=newton)
        rows[name] = {"V_deep": str(deep), "V_newton": str(newton)}

    # (4) consistency with door H's closed form for mu_2 (its log profile)
    _, s2, V2 = radial_data_log(families["mu2_committed"])
    doorH_V = u * (u ** 5 + 8 * u ** 4 + 42 * u ** 3 + 64 * u ** 2 + 17 * u - 72) / (
        4 * (1 + u) ** 2 * (u ** 2 + 3 * u + 4) ** 2)
    check("reproduces_doorH_V_mu2", sp.simplify(V2 - doorH_V) == 0)
    doorH_s = u * (u ** 2 + 4 * u + 9) / (2 * (1 + u) * (u ** 2 + 3 * u + 4))
    check("reproduces_doorH_s_mu2", sp.simplify(s2 - doorH_s) == 0)

    # (3) the s = +1/2 branch: a_r constant  <=>  mu = A + B/u
    _, s, V = radial_data(A + B / u, 3)
    check("cuscuton_branch_s_half", sp.simplify(s - sp.Rational(1, 2)) == 0, s=s)
    check("cuscuton_branch_V_quarter", sp.simplify(V - sp.Rational(1, 4)) == 0, V=V)
    # conversely s = 1/2 identically forces H a_r' = 0 (n = 3):
    # s = (1/2)(1 - 2 H a_r'/a_r^2) for n = 3
    Hs = u * mu(u)
    ar = sp.diff(Hs, u)
    s_gen = sp.Rational(1, 2) * (1 - 2 * Hs * sp.diff(ar, u) / ar ** 2)
    r = (c / Hs) ** sp.Rational(1, 2)
    lnw = sp.log(r) + sp.log(ar)
    s_direct = -2 * Hs / ar * sp.diff(lnw, u) / 2
    check("s_general_formula", sp.simplify(s_gen - s_direct) == 0)
    # mu = A + B/u has no deep-MOND regime (mu/u -> finite positive constant):
    Ap, Bp = sp.symbols("A_p B_p", positive=True)
    lim_B = sp.limit((Ap + Bp / u) / u, u, 0, "+")
    lim_0 = sp.limit(Ap / u, u, 0, "+")
    check("cuscuton_branch_has_no_deep_mond_regime",
          lim_B == sp.oo and lim_0 == sp.oo, limit_B_pos=lim_B, limit_B_zero=lim_0)
    # and on the log profile the deep-MOND corner also gives V -> 0 (door H)
    _, _, Vlog = radial_data_log(u + a2 * u ** 2 + a3 * u ** 3)
    check("log_profile_generic_deep_mond_V_to_0", sp.limit(Vlog, u, 0) == 0)

    return {"families": rows, "checks": checks,
            "all_passed": all(ch["passed"] for ch in checks)}


if __name__ == "__main__":
    rep = run()
    (HERE / "results.json").write_text(json.dumps(rep, indent=2) + "\n")
    for ch in rep["checks"]:
        print(("PASS " if ch["passed"] else "FAIL ") + ch["name"])
    print("ALL CHECKS PASSED" if rep["all_passed"] else "CHECKS FAILED")
