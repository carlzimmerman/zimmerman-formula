#!/usr/bin/env python3
"""X01 -- THE FIRST-FLIGHT EXPOSURE LADDER, CLOSED FORM + m=4 AUDIT + EXTENSION.

Door: M05 left the ladder open ("symmetry puzzle"); P/Q/R certified m=2..8;
T01's r=10 rung NON-CLOSED (K1 fired: q=97020>1e4). This lane closes the whole
EVEN ladder in one exact rational formula (X01-I), audits the m=4 entry (landed
1/4 vs the three-route value), and extends to m=12/14/16.

Measure EXACTLY as P01_r6_moment.py / M05_geometric_anchors.py:
  R ~ 3 R^2 on [0,1]; mu ~ U(-1,1); chord = -R mu + sqrt(1-R^2+R^2 mu^2);
  M_n := E[ int_0^chord (R^2 + 2 R mu s + s^2)^n ds ]   (r^2(s) = center distance^2)

X01-I (derived, u = s + R mu, y = R sqrt(1-mu^2), Fubini, Beta):
  M_n = (3/(2(n+1)(n+2))) * sum_{k=0}^n (k+1)/(2k+1)
      = (3/4) * [(n+1) + H_{2n+1} - H_n/2] / ((n+1)(n+2))

Routes: A = X01-I (exact rationals); B = sympy-exact mu->t reduction with the
antiderivative from sp.integrate of the FULL power (NOT hand-expanded);
C = 40-dps original-variable quadrature of the definition.
Kills pre-registered in X-WAVE_BRIEF.md (K1-K5) BEFORE this run.
"""
import json, os, sys, time
import sympy as sp
import mpmath as mp
import numpy as np

mp.mp.dps = 40
BASE = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

R, t, s = sp.symbols('R t s', positive=True)
mu_s = sp.Symbol('mu', real=True)
muof = (1 - R**2 - t**2)/(2*R*t)

# ---------------- route B: sympy-exact reduction (clean: full-power integrate) ----
def routeB(n):
    g = sp.expand(sp.integrate(sp.expand((R**2 + 2*R*mu_s*s + s**2)**n), s).subs(s, t))
    g = sp.expand(g.subs(mu_s, muof))
    integrand = sp.Rational(3,4)*R*((t**2 + 1 - R**2)/t**2)*g
    inner = sp.integrate(integrand, (t, 1 - R, 1 + R))
    F = sp.expand(sp.expand_log(sp.expand(inner), force=True))
    h = sp.symbols('h')
    Fh = sp.expand(F.subs(sp.log(1 - R), -h).subs(sp.log(1 + R), h))
    poly = Fh.subs(h, 0)
    Q = sp.cancel(sp.expand((Fh - poly)/h))
    Vanti = sp.integrate(Q, R)
    V = sp.expand(Vanti - Vanti.subs(R, 1))
    qout, rem = sp.div(V, 1 - R**2, R)
    if sp.simplify(rem) != 0:
        raise ValueError(f"divisibility failed n={n}")
    Ptil = sp.expand(poly - qout)
    return sp.integrate(Ptil, (R, 0, 1)), sp.Poly(Ptil, R)

def routeA(n):
    S = sum(sp.Rational(k+1, 2*k+1) for k in range(n+1))
    return sp.Rational(3,2)*S/sp.Rational((n+1)*(n+2))

def chord(Rv, muv): return -Rv*muv + mp.sqrt(1 - Rv**2 + Rv**2*muv**2)
def routeC(n):
    expr = sp.integrate(sp.expand((R**2 + 2*R*mu_s*s + s**2)**n), s)
    f = sp.lambdify((R, mu_s, s), expr, 'mpmath')
    inner = lambda Rv: mp.quad(lambda muv: 0.5*f(Rv, muv, chord(Rv, muv)), [-1, 0, 1])
    return 3*mp.quad(lambda Rv: Rv**2*inner(Rv), [0, 1])

# ---------------- K1: the m=4 audit ------------------------------------------------
# the repo's landed polynomial comes from the HAND-WRITTEN antiderivative (P01 I2 /
# M05_geometric_anchors I2 / Q01 g_m(4)): (2R^2 mu^2 + R^2) ch^3/3 + R mu ch^4/2 ...
# vs the TRUE one: 2(2R^2 mu^2 + R^2) ch^3/3 + R mu ch^4 (s^2 and s^3 coeffs halved).
def routeB_buggy_m4():
    """Route B applied to the REPO's hand-written m=4 antiderivative (the audit target)."""
    g = (R**4*t + 2*R**3*mu_s*t**2 + (2*R**2*mu_s**2 + R**2)*t**3/3
         + R*mu_s*t**4/2 + t**5/5)
    g = sp.expand(g.subs(mu_s, muof))
    integrand = sp.Rational(3,4)*R*((t**2 + 1 - R**2)/t**2)*g
    inner = sp.integrate(integrand, (t, 1 - R, 1 + R))
    F = sp.expand(sp.expand_log(sp.expand(inner), force=True))
    h = sp.symbols('h')
    Fh = sp.expand(F.subs(sp.log(1 - R), -h).subs(sp.log(1 + R), h))
    poly = Fh.subs(h, 0)
    Q = sp.cancel(sp.expand((Fh - poly)/h))
    Vanti = sp.integrate(Q, R)
    V = sp.expand(Vanti - Vanti.subs(R, 1))
    qout, rem = sp.div(V, 1 - R**2, R)
    if sp.simplify(rem) != 0:
        raise ValueError("divisibility failed (buggy m=4)")
    Ptil = sp.expand(poly - qout)
    return sp.integrate(Ptil, (R, 0, 1)), Ptil

try:
    buggy4, buggyP = routeB_buggy_m4()
except Exception as e:
    buggy4, buggyP = None, None
    print("buggy-route exception (recorded):", e)

A4, P4 = routeB(2)
C4 = routeC(2)
true4 = routeA(2)   # 17/60
k1_clean_agree = (sp.cancel(A4 - true4) == 0 and abs(C4 - mp.mpf(true4.p)/true4.q) < mp.mpf('1e-30'))
k1_disagrees_landed = abs(mp.mpf(true4.p)/true4.q - mp.mpf(1)/4) > mp.mpf('1e-9')
buggy_reproduces_landed = (buggy4 is not None and sp.cancel(buggy4 - sp.Rational(1,4)) == 0)
k1_verdict = k1_clean_agree and k1_disagrees_landed and buggy_reproduces_landed
check("K1 m=4 audit: three clean routes agree at 17/60", k1_clean_agree,
      f"A={A4} B={A4} C={mp.nstr(C4, 20)}")
check("K1 m=4 audit: clean value differs from landed 1/4", k1_disagrees_landed,
      f"|17/60 - 1/4| = {mp.nstr(abs(mp.mpf(true4.p)/true4.q - mp.mpf(1)/4), 6)}")
check("K1 m=4 audit: repo hand-written antiderivative reproduces the landed 1/4",
      buggy_reproduces_landed,
      f"buggy route = {buggy4 if buggy4 is not None else 'exception'} (mechanism confirmed)")
check("K1 VERDICT " + ("CORRECTED-TO-17/60" if k1_verdict else "LANDED-STANDS"), k1_verdict,
      "trail: M05_geometric_anchors.py I2, P01_r6_moment.py I2/I2_b, Q01_r6_lean.py g_m(4); "
      "m=4 absent from every K0 replication gate; q01CoreR4 certified the buggy core")

# ---------------- K2: closure of the ladder -------------------------------------------------
k2_ok = True
ladder_detail = []
for n in range(0, 7):
    A = routeA(n)
    B = routeB(n)[0] if n >= 1 else A
    C = routeC(n)
    okB = (n == 0) or (sp.cancel(A - B) == 0)
    okC = abs(C - mp.mpf(A.p)/A.q) < mp.mpf('1e-30')
    k2_ok = k2_ok and okB and okC
    ladder_detail.append(f"n={n}: {A}  B==A:{okB}  |C-A|<1e-30:{okC}  C={mp.nstr(C, 16)}")
check("K2 ladder closure: X01-I == route B exactly (n=1..6) AND |route C - X01-I| < 1e-30 (n=0..6)",
      k2_ok, " | ".join(ladder_detail))

# ---------------- K3: extension rungs m=12/14/16 (n=6/7/8) ------------------------------------
ext = {}
k3_ok = True
mc_cache = {}
def mc_moment(n, draws=10_000_000, seed=20260925):
    rng = np.random.default_rng(seed + n)
    Rv = rng.random(draws)**(1/3.0)
    muv = rng.uniform(-1, 1, draws)
    ch = -Rv*muv + np.sqrt(np.maximum(0.0, 1 - Rv**2*(1 - muv**2)))
    f = sp.lambdify((R, mu_s, s), sp.integrate(sp.expand((R**2 + 2*R*mu_s*s + s**2)**n), s), 'numpy')
    G = f(Rv, muv, ch)
    est = float(np.mean(G))
    blocks = G.reshape(20, -1).mean(axis=1)
    se = float(np.std(blocks, ddof=1)/np.sqrt(20))
    return est, se
for n in [6, 7, 8]:
    A = routeA(n)
    C = routeC(n)
    est, se = mc_moment(n)
    z = abs(est - float(A))/se if se > 0 else 0.0
    okC = abs(C - mp.mpf(A.p)/A.q) < mp.mpf('1e-30')
    okMC = z <= 5
    k3_ok = k3_ok and okC and okMC
    ext[n] = {"exact": str(A), "quad": mp.nstr(C, 18), "mc": est, "se": se, "z": z}
    check(f"K3 rung m={2*n} (n={n}): exact {A}  quad<1e-30:{okC}  MC z={z:.2f}<=5:{okMC}",
          okC and okMC, f"C={mp.nstr(C,18)} est={est:.9f} se={se:.2e}")

# ---------------- K4: odd rungs (FIX-FORWARD 2026-09-25, recorded): run-1 K4 evaluated
# r(s)^m at the ENDPOINT s=chord (identically 1 on the sphere wall) instead of integrating
# over the flight — the "E[int r ds] = 1.0 exactly" reading was that artifact (zero-variance
# MC exposed it: se = 0).  Withdrawn; K4 re-pointed (both-ways): m=1,3 odd rungs via the
# EXACT antiderivative in s (asinh/log structure), rational reconstruction q<=1e6, either
# outcome recorded.  The pre-brief guess "odd rungs not rational" carried no evidence and
# is not asserted either way.
def odd_moment(m, draws=10_000_000, seed=20260925):
    expr = sp.integrate(sp.expand(sp.sqrt(R**2 + 2*R*mu_s*s + s**2)**m), s)  # exact antiderivative
    f = sp.lambdify((R, mu_s, s), expr, 'mpmath')
    inner = lambda Rv: mp.quad(lambda muv: 0.5*f(Rv, muv, chord(Rv, muv)), [-1, 0, 1])
    v = 3*mp.quad(lambda Rv: Rv**2*inner(Rv), [0, 1])
    rng = np.random.default_rng(seed + m)
    Rv = rng.random(draws)**(1/3.0); muv = rng.uniform(-1, 1, draws)
    ch = -Rv*muv + np.sqrt(np.maximum(0.0, 1 - Rv**2*(1 - muv**2)))
    g = sp.lambdify((R, mu_s, s), expr, 'numpy')
    G = g(Rv, muv, ch)
    est = float(np.mean(G)); bl = G.reshape(20, -1).mean(axis=1)
    se = float(np.std(bl, ddof=1)/np.sqrt(20))
    return v, est, se
def reconstruct(x, qmax=10000, tol=1e-15):
    # P01-conventional criterion: continued-fraction convergents, q<=1e4, err<1e-15.
    # FIX-FORWARD (run-2, recorded): run-2's q<=1e6 @ 1e-12 flushed a spurious hit
    # (466159/865454 for M1) that is manifestly not a discovery — loose reconstruction
    # always finds SOME large-denominator rational; the P01 ceiling (convergents,
    # q<=1e4, 1e-15) is the repo's clean-rational standard.
    xx = mp.mpf(x); p2, p1, q2, q1 = 0, 1, 1, 0
    for _ in range(80):
        a = int(mp.floor(xx))
        pp, qq = a*p1 + p2, a*q1 + q2
        p2, p1, q2, q1 = p1, pp, q1, qq
        if qq == 0 or qq > qmax:
            break
        if abs(mp.mpf(pp)/qq - x) < mp.mpf(tol):
            return (pp, qq)
        fr = xx - a
        if abs(fr) < mp.mpf('1e-40'):
            break
        xx = 1/fr
    return None
M1, m1est, m1se = odd_moment(1)
M3, m3est, m3se = odd_moment(3)
r1 = reconstruct(M1)
r3 = reconstruct(M3)
m1_ok = (abs(m1est - float(M1))/m1se <= 5) if m1se > 0 else False
m3_ok = (abs(m3est - float(M3))/m3se <= 5) if m3se > 0 else False
# both-ways: a clean small rational (P01 criterion) -> claim it; none -> MEASURED-NOT-SMALL-RATIONAL
# (consistent with the asinh/log structure of the odd integrand).  Only an MC/quadrature
# disagreement fails the check.
k4a = m1_ok and (r1 is None or abs(M1 - mp.mpf(r1[0])/r1[1]) < mp.mpf('1e-15'))
check("K4a (fix-forward, both-ways): E[int r ds] measured; clean rational: " + (str(r1) if r1 else "NONE (not small-rational)"),
      k4a, f"M1={mp.nstr(M1,20)} MC={m1est:.9f} z={abs(m1est-float(M1))/m1se:.2f}")
k4b = m3_ok and (r3 is None or abs(M3 - mp.mpf(r3[0])/r3[1]) < mp.mpf('1e-15'))
check("K4b (probe): E[int r^3 ds] measured; clean rational: " + (str(r3) if r3 else "NONE (not small-rational)"),
      k4b, f"M3={mp.nstr(M3,20)} MC={m3est:.9f} z={abs(m3est-float(M3))/m3se:.2f}")

# ---------------- assemble ----------------------------------------------------------------
allpass = all(c["pass"] for c in checks)
res = {
 "lane": "X01_ladder_closure", "date": "2026-09-25",
 "measure": "M05/P01 first-flight measure (R uniform in ball, mu isotropic); M_n = E[int (R^2+2Rmu s+s^2)^n ds]",
 "closed_form": "M_n = (3/(2(n+1)(n+2))) * sum_{k=0}^n (k+1)/(2k+1)",
 "ladder": {f"M_{2*n if n>0 else 0}": {"n": n, "exact": str(routeA(n)), "float": float(routeA(n))} for n in range(9)},
 "m4_audit": {"landed": "1/4", "true": "17/60", "buggy_route_reproduces_landed": bool(buggy_reproduces_landed),
              "affected_files": ["deepseek_push/M05_geometric_anchors.py (I2, E_int_r4_quarter)",
                                 "deepseek_push/P01_r6_moment.py (I2, I2_b, G1/G2 gates)",
                                 "deepseek_push/Q01_r6_lean.py (g_m(4))",
                                 "fable_independent_2026/lean_2026/Q01_r6_core.lean (q01CoreR4)",
                                 "deepseek_push/M05_FIRST_FLIGHT_MOMENTS.md (table)",
                                 "register ladder strings (P/Q/R/S/T/W rows)"],
              "mechanism": "s^2 and s^3 coefficients of (R^2+2Rmu s+s^2)^2 halved in the hand-written antiderivative"},
 "extension": {f"m=2*n": v for n, v in ext.items()},
 "odd_rung": {"M_half": mp.nstr(M1, 20), "rational_hit": r1, "M_3half": mp.nstr(M3, 20), "rational_hit_m3": r3},
 "checks": checks,
 "summary": f"{sum(1 for c in checks if c['pass'])}/{len(checks)} checks PASS",
 "exit_ok": bool(allpass),
}
with open(os.path.join(BASE, "X01_ladder_closure_results.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)
with open(os.path.join(BASE, "X01_ladder_closure.out"), "w") as f:
    f.write(f"X01: {res['summary']}\n")
    for c in checks: f.write(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}  {c['detail']}\n")
print(open(os.path.join(BASE, "X01_ladder_closure.out")).read())
print("X01 COMPLETE — EXIT", 0 if allpass else 1)
sys.exit(0 if allpass else 1)
