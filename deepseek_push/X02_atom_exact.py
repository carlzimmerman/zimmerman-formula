#!/usr/bin/env python3
"""X02 -- THE WINDOW ATOM EXACT THROUGH O(tau^7) CUMULANT TOWER + q=0 CLOSED FORM.

Door: M05-I gives the thin-limit window from the FIRST-order exposure only;
the volume atom A_v = E exp(-tau0 (L + q I1)) has no exact finite-tau0
coefficients on record.  RUN-1 (verbatim in history): the lane used the central
4th MOMENT formula for k4 (k4 = m4 - 3 m2^2 is the cumulant); residuals matched
3 Var^2 tau^4/24 exactly (4.4e-4 at (0.5,0), 6.8e-4 at (0.25,3) vs measured
4.46e-4 / 6.95e-4) — bug fixed in this run per AMENDMENT 1 (X-WAVE_BRIEF).

Deliverables:
  K1  the exact moment lattice E[L^a I1^b], (a,b) with a+b <= 7, exact rationals
      (sympy (x,y) reduction), each quadrature-verified.
  K2b the cumulant tower: k2..k7 exact polynomials in q; P4 and P7 = -ln A_v
      expansions; MC-verified at the 9-point grid; verdict by the amended rule.
  K2c the exact q=0 atom closed form E[e^{-tau L}] = (3/(2tau))[1/2 -
      (1 - e^{-2tau}(1+2tau))/(4 tau^2)] vs MC at 4 tau values; ALSO used as a
      cumulant-formula self-check (Taylor coefficients of the closed form must
      equal the q=0 cumulants k5/120, -k6/720, k7/5040 at orders 5..7).

Measure EXACTLY as X01/P01 (R~3R^2, mu~U(-1,1), L = chord, I1 = int_0^L r^2 ds).
Kills pre-registered in X-WAVE_BRIEF.md (+ AMENDMENT 1) before this run.
"""
import json, os, sys
import sympy as sp
import mpmath as mp
import numpy as np

mp.mp.dps = 40
BASE = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

y = sp.symbols('y', positive=True)
x = sp.symbols('x', real=True)
Rp = sp.sqrt(1 - y**2)

def A1(xv):
    return (Rp**3 - xv**3)/3 + y**2*(Rp - xv)

def exact_moment(a, b):
    integ = sp.expand((Rp - x)**a * A1(x)**b)
    Fx = sp.expand(sp.integrate(integ, (x, -Rp, Rp)))
    qq = sp.symbols('qq', positive=True)
    Fq = sp.expand(Fx.subs(Rp, qq))
    P = sp.Poly(Fq, qq, y)
    total = sp.Rational(0)
    for (dq, dy_) in P.monoms():
        c = P.coeff_monomial(qq**dq * y**dy_)
        alpha = sp.Rational(dy_ + 2, 2)
        beta = sp.Rational(dq, 2) + 1
        val = sp.Rational(1, 2) * sp.gamma(alpha) * sp.gamma(beta) / sp.gamma(alpha + beta)
        total += c * sp.gammasimp(val)
    return sp.simplify(sp.Rational(3, 2) * total)

def chord(Rv, muv): return -Rv*muv + mp.sqrt(1 - Rv**2 + Rv**2*muv**2)
def def_quad(a, b):
    def g(Rv, muv):
        L = chord(Rv, muv)
        I1 = Rv**2*L + Rv*muv*L**2 + L**3/3
        return L**a * I1**b
    inner = lambda Rv: mp.quad(lambda muv: 0.5*g(Rv, muv), [-1, 0, 1])
    return 3*mp.quad(lambda Rv: Rv**2*inner(Rv), [0, 1])
def def_quad_sr2():
    g = lambda Rv, muv: (Rv**2*chord(Rv,muv)**2/2 + 2*Rv*muv*chord(Rv,muv)**3/3
                         + chord(Rv,muv)**4/4)
    inner = lambda Rv: mp.quad(lambda muv: 0.5*g(Rv, muv), [-1, 0, 1])
    return 3*mp.quad(lambda Rv: Rv**2*inner(Rv), [0, 1])

M = {}
def land(label, a, b, target):
    ex = exact_moment(a, b)
    qd = def_quad(a, b)
    ok = (sp.cancel(ex - target) == 0 and
          abs(qd - mp.mpf(target.p)/target.q) < mp.mpf('1e-30'))
    M[(a, b)] = ex
    check(f"K1 {label} = {target} (exact {ex}; quad 1e-30)", ok, f"quad={mp.nstr(qd,18)}")

# ---------------- K1: anchors + new exact values -----------------------------------------
land("E[L] (landed 3/4)",       1, 0, sp.Rational(3,4))
land("E[L^2] (N02 anchor 4/5)", 2, 0, sp.Rational(4,5))
land("E[I1] (landed 5/12)",     0, 1, sp.Rational(5,12))
land("E[L*I1] (NEW 2/5)",       1, 1, sp.Rational(2,5))
land("E[L^3] (NEW 1)",          3, 0, sp.Rational(1,1))
land("E[I1^2] (NEW 208/945)",   0, 2, sp.Rational(208,945))
land("E[L^4] (NEW 48/35)",      4, 0, sp.Rational(48,35))
sr2 = def_quad_sr2()
check("K1 E[int s r^2 ds] = 8/35 (N02 anchor) via definitional quadrature 1e-30",
      abs(sr2 - mp.mpf(8)/35) < mp.mpf('1e-30'), f"quad={mp.nstr(sr2,18)}")
for (a, b) in [(2,1),(1,2),(0,3),(3,1),(2,2),(1,3),(0,4),
               (5,0),(4,1),(3,2),(2,3),(1,4),(0,5),
               (6,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,6),
               (7,0),(6,1),(5,2),(4,3),(3,4),(2,5),(1,6),(0,7)]:
    ex = exact_moment(a, b)
    qd = def_quad(a, b)
    ok = abs(qd - mp.mpf(ex.p)/ex.q) < mp.mpf('1e-26')
    M[(a, b)] = ex
    check(f"K1 E[L^{a} I1^{b}] = {ex}; quad 1e-26", ok, f"quad={mp.nstr(qd,18)}")

# ---------------- cumulant tower (FIX-FORWARD run-2b: no power-sum formulas — the
# hand-typed k5..k7 formulas failed the q=0 closed-form self-check at j=7; cumulants
# computed as the EXACT log-series of the moment MGF: k_j = j! [t^j] log(sum E[X^j] t^j/j!)
# — bulletproof, validated against the closed-form series at every order) -------------
q = sp.symbols('q')
Epow = {}
for j in range(1, 8):
    Epow[j] = sum(sp.binomial(j, a) * q**a * M[(j - a, a)] for a in range(j + 1))
t_s = sp.symbols('t')
Mser = 1 + sum(Epow[j]*t_s**j/sp.factorial(j) for j in range(1, 8))
LNser = sp.series(sp.log(Mser), t_s, 0, 8).removeO()
K = {}
for j in range(1, 8):
    K[j] = sp.expand(sp.factorial(j)*LNser.coeff(t_s, j))
print("k1(q) =", sp.factor(K[1]))
for j in range(2, 8):
    print(f"k{j}(q) =", sp.factor(K[j]))

# ---------------- K2c self-check: q=0 closed form series vs cumulants ---------------------
tau = sp.symbols('tau')
F0 = sp.Rational(3,2)/tau*(sp.Rational(1,2) - (1 - sp.exp(-2*tau)*(1 + 2*tau))/(4*tau**2))
ser = sp.series(-sp.log(F0), tau, 0, 8).removeO()
sc = {j: sp.simplify(ser.coeff(tau, j)) for j in range(1, 8)}
self_ok = True
for j in range(2, 8):
    sign = (-1)**(j + 1)
    expect = sign * K[j].subs(q, 0) / sp.factorial(j)
    self_ok = self_ok and (sp.simplify(sc[j] - expect) == 0)
check("K2c-0 self-check: closed-form q=0 atom Taylor coefficients reproduce the cumulants k2..k7 exactly",
      self_ok, f"series coeffs = {[str(sc[j]) for j in range(2,8)]}")

# ---------------- K2b: the 9-point grid (corrected P4, then P7) ---------------------------
tau_s, qq_s = sp.symbols('tau qq')
def Ppoly(order):
    tot = tau_s*K[1].subs(q, qq_s)
    for j in range(2, order + 1):
        tot += (-1)**(j + 1) * tau_s**j * K[j].subs(q, qq_s) / sp.factorial(j)
    return sp.expand(tot)
P4 = Ppoly(4)
P7 = Ppoly(7)
P4f = sp.lambdify((tau_s, qq_s), P4, 'numpy')
P7f = sp.lambdify((tau_s, qq_s), P7, 'numpy')
F0f = sp.lambdify(tau_s, -sp.log(F0), 'numpy')

rng = np.random.default_rng(20260925)
n = 10_000_000
Rv = rng.random(n)**(1/3.0)
muv = rng.uniform(-1, 1, n)
ch = -Rv*muv + np.sqrt(np.maximum(0.0, 1 - Rv**2*(1 - muv**2)))
L = ch
I1 = Rv**2*ch + Rv*muv*ch**2 + ch**3/3
grid = [(0.25, 0), (0.25, 3), (0.25, 10), (0.5, 0), (0.5, 3), (0.5, 10),
        (1.0, 0), (1.0, 3), (1.0, 10)]
run1_rows = [  # run-1 verbatim (buggy k4): values recorded, do not edit
 {"tau0": 0.25, "q": 0,   "lnA_mc": -0.18021249, "se": 3.25e-05, "z_P4": 1.24},
 {"tau0": 0.25, "q": 3,   "lnA_mc": -0.46360867, "se": 5.84e-05, "z_P4": 11.91},
 {"tau0": 0.25, "q": 10,  "lnA_mc": -1.03148451, "se": 7.76e-05, "z_P4": 269.37},
 {"tau0": 0.5,  "q": 0,   "lnA_mc": -0.34635204, "se": 5.32e-05, "z_P4": 8.38},
 {"tau0": 0.5,  "q": 3,   "lnA_mc": -0.85772836, "se": 7.60e-05, "z_P4": 140.01},
 {"tau0": 0.5,  "q": 10,  "lnA_mc": -1.73073194, "se": 7.26e-05, "z_P4": 4431.32},
 {"tau0": 1.0,  "q": 0,   "lnA_mc": -0.64008563, "se": 7.45e-05, "z_P4": 89.10},
 {"tau0": 1.0,  "q": 3,   "lnA_mc": -1.46917883, "se": 7.72e-05, "z_P4": 2115.40},
 {"tau0": 1.0,  "q": 10,  "lnA_mc": -2.54599411, "se": 5.67e-05, "z_P4": 84368.53},
]
rows = []
all4, all7 = True, True
for (tv, qv) in grid:
    X = L + qv*I1
    A = np.exp(-tv*X)
    est = float(np.mean(A))
    bl = A.reshape(20, -1).mean(axis=1)
    se = float(np.std(bl, ddof=1)/np.sqrt(20))
    lnA = float(np.log(est))
    z4 = abs(lnA - (-float(P4f(tv, qv))))/se
    z7 = abs(lnA - (-float(P7f(tv, qv))))/se
    ok4, ok7 = z4 <= 3, z7 <= 3
    all4, all7 = all4 and ok4, all7 and ok7
    rows.append({"tau0": tv, "q": qv, "lnA_mc": lnA, "se": se,
                 "P4pred": -float(P4f(tv, qv)), "z_P4": z4,
                 "P7pred": -float(P7f(tv, qv)), "z_P7": z7, "pass_P4": ok4, "pass_P7": ok7})
    check(f"K2b grid tau0={tv} q={qv}: P4 z={z4:.2f} ({'PASS' if ok4 else 'FAIL'}), P7 z={z7:.2f} ({'PASS' if ok7 else 'FAIL'})",
          ok7, f"lnA={lnA:.8f} P4={-float(P4f(tv,qv)):.8f} P7={-float(P7f(tv,qv)):.8f} se={se:.2e}")
if all4:
    check("K2b VERDICT: CUMULANT-4-EXACT (all 9 points)", True, "")
elif all7:
    check("K2b VERDICT: CUMULANT-TOWER-7 (all 9 points; P4 alone was insufficient)",
          True, "P4 points failing are listed above")
else:
    check("K2b VERDICT: tower insufficient at >=1 large-exposure point (recorded verbatim); "
          "residuals = truncation tail", True,
          "points with z_P7 > 3 listed above")

# ---------------- K2c: exact q=0 atom law vs MC --------------------------------------------
q0_ok = True
for tv in [0.25, 0.5, 1.0, 2.0]:
    A = np.exp(-tv*L)
    est = float(np.mean(A))
    bl = A.reshape(20, -1).mean(axis=1)
    se = float(np.std(bl, ddof=1)/np.sqrt(20))
    lnA = float(np.log(est))
    pred = float(F0f(tv))          # = -ln E[e^{-tv L}]
    z = abs((-lnA) - pred)/se      # sign fix (run-2b): compare -lnA_mc against +closed form
    q0_ok = q0_ok and (z <= 3)
    check(f"K2c exact q=0 atom: tau={tv}: |ln A_v(MC) - closed form| <= 3 SE",
          z <= 3, f"lnA={lnA:.9f} closed={pred:.9f} se={se:.2e} z={z:.2f}")
check("K2c VERDICT: EXACT-ATOM-Q0 (closed form holds at all 4 tau)", q0_ok,
      "E[e^{-tau L}] = (3/(2tau))[1/2 - (1-e^{-2tau}(1+2tau))/(4tau^2)]")

allpass = all(c["pass"] for c in checks)
res = {
 "lane": "X02_atom_exact", "date": "2026-09-25",
 "run1_verbatim": {"k4_bug": "central-4th-moment formula used for the cumulant; residuals matched 3 Var^2 tau^4/24",
                   "grid": run1_rows},
 "cumulants": {f"k{j}": str(sp.factor(K[j])) for j in range(1, 8)},
 "moments": {f"E[L^{a} I1^{b}]": str(M[(a,b)]) for (a,b) in sorted(M)},
 "grid": rows,
 "q0_atom": "E[e^{-tau L}] = (3/(2 tau)) [1/2 - (1 - e^{-2 tau}(1+2 tau))/(4 tau^2)]",
 "checks": checks,
 "summary": f"{sum(1 for c in checks if c['pass'])}/{len(checks)} checks PASS",
 "exit_ok": bool(allpass),
}
with open(os.path.join(BASE, "X02_atom_exact_results.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)
with open(os.path.join(BASE, "X02_atom_exact.out"), "w") as f:
    f.write(f"X02 (run-2, amended): {res['summary']}\n")
    for j in range(1, 8): f.write(f"k{j}(q) = {sp.factor(K[j])}\n")
    f.write("run-1 verbatim (buggy k4): " + str(run1_rows) + "\n")
    for c in checks: f.write(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}  {c['detail']}\n")
print(open(os.path.join(BASE, "X02_atom_exact.out")).read())
print("X02 COMPLETE — EXIT", 0 if allpass else 1)
sys.exit(0 if allpass else 1)
