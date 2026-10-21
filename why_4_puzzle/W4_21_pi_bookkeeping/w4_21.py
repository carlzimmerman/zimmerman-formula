#!/usr/bin/env python3
"""W4-21 -- pi bookkeeping for the single-mediator ratio R = eps C3^2/C2^3. Screen lane: no kappa is output.
Criteria: FROZEN_CRITERIA.md (committed alone, a67f9ed9c). Light: sympy + mpmath, single core. Run from the repo root:
    python3 why_4_puzzle/W4_20_pi_bookkeeping/w4_21.py > why_4_puzzle/W4_20_pi_bookkeeping/w4_21.out
    W4_21_MUTATE=1 ... > .../w4_21_MUTATE.out   (MU1 un-glue eps, MU2 n = 4; exit 1 when the controls bite)
kappa = 1/2 FITTED. Not theory closed.
"""
import itertools, json, os, sys
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("W4_21_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
N_SPACE = 4 if MUT else 3            # MU2: spatial dimension 3 -> 4
OUT, checks, res = [], [], {}
pi = sp.pi


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def wt(e):
    """pi-weight on the D1 class r*pi^w (r algebraic, nonzero; w integer). None outside the class."""
    e = sp.nsimplify(sp.simplify(e)) if e.is_number else sp.simplify(e)
    if e == 0:
        return None
    num, den = sp.fraction(sp.together(e))
    try:
        pn, pd = sp.Poly(num, pi), sp.Poly(den, pi)
    except sp.PolynomialError:
        return None
    if len(pn.terms()) != 1 or len(pd.terms()) != 1:
        return None
    w = pn.degree() - pd.degree()
    r = sp.simplify(e / pi ** w)
    if r.has(pi) or r == 0 or (r.is_number and r.is_algebraic is False):
        return None
    return int(w)


def omega(n):
    return sp.simplify(2 * pi ** sp.Rational(n, 2) / sp.gamma(sp.Rational(n, 2)))


P("W4-21 pi bookkeeping for R = eps C3^2/C2^3" + ("  [MUTATE: MU1 un-glue eps, MU2 n = 4]" if MUT else ""))
P("Screen lane; no kappa output. kappa = 1/2 FITTED; not theory closed.\n")

# ---------------- K1: A1 dictionary from the asymptotes and the flux law ----------------
q, M, C2, C3, eps, r, h, Om = sp.symbols("q M C2 C3 epsilon r h Omega", positive=True)
n = N_SPACE
hN = sp.solve(sp.Eq(Om * r ** (n - 1) * 2 * C2 * h, q * M), h)[0]
Gn = sp.simplify(q * hN * r ** (n - 1) / M)                       # g = q h = Gn M / r^(n-1)
hD = sp.solve(sp.Eq(Om * r ** (n - 1) * 3 * C3 * h ** 2, q * M), h)[0]
hstar = sp.solve(sp.Eq(2 * C2 * h, 3 * C3 * h ** 2), h)[0]       # crossover of the derivative asymptotes
a0 = q * hstar
deep_ok = sp.simplify((q * hD) ** 2 - (q * hN) * a0) == 0         # deep regime is g^2 = g_N a0 with this a0
xi = sp.simplify(a0 ** 2 / (Gn * eps))
xi_ok = sp.simplify(xi - 8 * Om * C2 ** 3 / (9 * eps * C3 ** 2)) == 0
Rs = sp.Symbol("R", positive=True)
xi_of_R = sp.simplify((xi * eps * C3 ** 2 / C2 ** 3).subs(Om, omega(n)) / Rs)     # xi = 8 Omega_n/(9R)
Rstar = sp.solve(sp.Eq(xi_of_R, sp.Rational(1, 4)), Rs)[0]
P(f"G_n = {Gn};  a0 = {sp.simplify(a0)};  xi = {xi}")
P(f"n = {n}: Omega_n = {omega(n)};  xi = {xi_of_R};  target R* = {Rstar}  (wt {wt(Rstar)})")
check("K1 dictionary", f"G_n, a0, xi re-derived; deep g^2 = g_N a0: {deep_ok}; xi = 8 Omega C2^3/(9 eps C3^2): {xi_ok}",
      deep_ok and xi_ok)
check("K1 target weight", f"R* = {Rstar}, wt {wt(Rstar)} (frozen: 128pi/9, wt 1 at n = 3)",
      sp.simplify(Rstar - sp.Rational(128, 9) * pi) == 0 and wt(Rstar) == 1)
res["n"] = n; res["Rstar"] = str(Rstar); res["wt_Rstar"] = wt(Rstar)

# ---------------- K2: A2 thermal coefficients ----------------
N, gam, th, X = sp.symbols("N gamma theta X", positive=True)
lead = (pi * th ** 4 / 90) if MUT else (pi ** 2 * th ** 4 / 90)  # MU1 un-glues one pi in eps
F = N * (-lead + gam * th ** 2 * X / 24 - gam ** sp.Rational(3, 2) * th * X ** sp.Rational(3, 2) / (12 * pi))
F0 = F.subs(X, 0)
c2 = sp.expand(F).coeff(X, 1)
c3 = sp.expand(F).coeff(X ** sp.Rational(3, 2))
eps_rad = 3 * sp.Abs(F0)
R_rad = sp.simplify(eps_rad * c3 ** 2 / c2 ** 3)
R_F0 = sp.simplify(sp.Abs(F0) * c3 ** 2 / c2 ** 3)
P(f"\nthermal: |F(0)| = {sp.Abs(F0)}, C2 = {c2}, C3 = {c3}")
P(f"R_th(eps_rad) = {R_rad} (wt {wt(R_rad)});  R_th(|F0|) = {R_F0} (wt {wt(R_F0)})")
check("K2 thermal ratios", f"R = {R_rad} and {R_F0}; frozen 16/5 and 16/15, wt 0 (L1 on the thermal medium)",
      R_rad == sp.Rational(16, 5) and R_F0 == sp.Rational(16, 15) and wt(R_rad) == 0 and wt(R_F0) == 0)
res["R_th_rad"] = str(R_rad); res["R_th_F0"] = str(R_F0); res["wt_R_th"] = wt(R_rad)

# K2b: each coefficient = r * pi^-2 * (pi theta)^p with r pi-free (common Q = pi^-2, glue g = 1)
glue = {}
for name, coef, p in (("eps(|F0|)", sp.Abs(F0), 4), ("C2", c2, 2), ("C3", sp.Abs(c3), 1)):
    rr = sp.simplify(coef / (pi ** -2 * (pi * th) ** p))
    glue[name] = rr
    P(f"  {name} = [{rr}] * pi^-2 * (pi theta)^{p}")
k2b = all(not v.has(pi) and not v.has(th) for v in glue.values())
check("K2b glued form", "every r_i is pi-free and theta-free" if k2b else f"not glued: {glue}", k2b)

# K2c: the three high-T coefficients from the bosonic thermal integral
mp.mp.dps = 30


def J(y):
    f = lambda x: x ** 2 * mp.log(1 - mp.exp(-mp.sqrt(x ** 2 + y ** 2)))
    return mp.quad(f, [0, y, 2 * y, 1, 4, 16, 50, 110], error=True)


ratios = {}
for y in (mp.mpf("0.02"), mp.mpf("0.01")):
    val, err = J(y)
    resid = val - (-mp.pi ** 4 / 45 + mp.pi ** 2 * y ** 2 / 12 - mp.pi * y ** 3 / 6)
    ratios[float(y)] = float(abs(resid) / (mp.pi * y ** 3 / 6))
    P(f"  y = {float(y)}: J = {mp.nstr(val, 20)}, quad err {mp.nstr(err, 3)}, residual/cubic = {ratios[float(y)]:.4f}")
check("K2c high-T coefficients", f"residual/cubic {ratios[0.01]:.4f} at y 0.01 (< 0.05), falling from {ratios[0.02]:.4f}",
      ratios[0.01] < 0.05 and ratios[0.01] < ratios[0.02])
res["K2c_ratios"] = ratios

# ---------------- K3: L1 symbolic ----------------
re_, r2, r3, Q, s, g, p2, p3 = sp.symbols("r_e r_2 r_3 Q s g p_2 p_3", positive=True)
pe = 3 * p2 - 2 * p3                                                 # R dimensionless in s
E_, C2g, C3g = (rr * Q * (pi ** g * s) ** p for rr, p in ((re_, pe), (r2, p2), (r3, p3)))
Rg = sp.powsimp(sp.expand_power_base(E_ * C3g ** 2 / C2g ** 3, force=True), force=True)
Rg = sp.simplify(Rg)
k3 = Rg.free_symbols <= {re_, r2, r3} and not Rg.has(pi)
P(f"\nglued one-scale R = {Rg}")
t, u = sp.symbols("t u", positive=True)                            # two glued scales, each with zero net power
E2 = re_ * Q * (pi * s) ** 2 * (pi ** 2 * t) ** 2
C22 = r2 * Q * (pi * s) ** 2
C32 = r3 * Q * (pi * s) ** 2 / (pi ** 2 * t)
R2 = sp.simplify(E2 * C32 ** 2 / C22 ** 3)
k3b = not R2.has(pi) and not R2.has(s) and not R2.has(t)
thx, Mx = sp.symbols("theta_x M_x", positive=True)                  # control: two independent scales
Rc = sp.simplify((re_ * Q * (pi * thx) ** 4) * (r3 * Q * pi * thx) ** 2 / (r2 * Q * (pi * Mx) ** 2) ** 3)
k3c = Rc.has(thx) and Rc.has(Mx)
P(f"two glued scales R = {R2};  two-scale control R = {Rc}")
check("K3 L1 symbolic", f"glued R = {Rg} (free of Q, s, pi); two glued scales {R2}; control keeps theta/M: {k3c}",
      k3 and k3b and k3c)

# ---------------- K4: L1 on the record's H-type kappa^2 (n = 3; four-dimensional record values) ----------------
rec = {"W4-05 EiBI": (8 * pi, sp.Rational(4, 9)), "W4-05 f(R)": (32 * pi / sp.sqrt(3), sp.sqrt(3) / 9),
       "W4-01/05 DGP": (8 * pi / 3, sp.Rational(4, 3)), "W4-07 B1/B2": (16 * pi / 3, sp.Rational(2, 3)),
       "W4-19 L1 Zhao": (8 * pi, sp.Rational(4, 9))}
k4, res["K4"] = True, {}
P("")
for k, (k2, hand) in rec.items():
    Rr = sp.simplify(8 * omega(3) / (9 * k2))
    ok = sp.simplify(Rr - hand) == 0 and wt(Rr) == 0
    k4 &= ok
    res["K4"][k] = str(Rr)
    P(f"  {k}: kappa^2 = {k2} -> R = {Rr} (wt {wt(Rr)}; hand {hand})")
check("K4 H-type routes", "every record H-type kappa^2 maps to an algebraic R (wt 0): the thermal failure", k4)

# ---------------- K5: L2 table ----------------
P("")
k5, res["K5"] = True, {}
for nn in (2, 3, 4, 5):
    w = wt(omega(nn))
    k5 &= (w is not None and w >= 1)
    res["K5"][nn] = w
    P(f"  n = {nn}: Omega_n = {omega(nn)}, wt {w}; xi = 8 Omega_n/(9R) has wt {w} for algebraic R, so xi != 1/4")
check("K5 every dimension", f"wt(Omega_n) = {list(res['K5'].values())} (frozen 1, 1, 2, 2)",
      k5 and list(res["K5"].values()) == [1, 1, 2, 2])

# ---------------- K6: L3 solution set ----------------
need = wt(Rstar)
sols = [w for w in itertools.product((-1, 0, 1), repeat=3) if w[0] + 2 * w[1] - 3 * w[2] == need]
hand = [(1, 0, 0), (-1, 1, 0), (0, -1, -1)]
P(f"\nL3 (wt eps, wt C3, wt C2) with wt eps + 2 wt C3 - 3 wt C2 = {need}, all |w| <= 1: {sols}")
check("K6 L3 solutions", f"{sols} (frozen {hand})", sorted(sols) == sorted(hand))
res["L3_rhs"] = need; res["L3"] = sols

# ---------------- identity checks ----------------
src = open(os.path.abspath(__file__)).read()
bad = ["5." + "7888", "0." + "1727", "9." + "36e-11", "9." + "3603e-11", "1." + "13e-10", "1." + "1312e-10",
       "1." + "2e-10", "0." + "417", "0." + "465", "0." + "551"]
hits = [b for b in bad if b in src]
check("I1 forbidden constants", f"hits {hits}", not hits)
Z_ = sp.Symbol("Z", positive=True); sc = sp.Symbol("s_f", positive=True)
Rexp = eps * C3 ** 2 / C2 ** 3
i3 = (sp.simplify(Rexp.subs({eps: Z_ * eps, C2: Z_ * C2, C3: Z_ * C3}, simultaneous=True) - Rexp) == 0
      and sp.simplify(Rexp.subs({C2: C2 / sc ** 2, C3: C3 / sc ** 3}, simultaneous=True) - Rexp) == 0
      and sp.simplify(Gn.subs({q: q / sc, C2: C2 / sc ** 2}, simultaneous=True) - Gn) == 0
      and sp.simplify(a0.subs({q: q / sc, C2: C2 / sc ** 2, C3: C3 / sc ** 3}, simultaneous=True) - a0) == 0)
check("I3 invariances", "R under common Z and phi -> s phi; G_n and a0 under phi -> s phi", i3)
P("I2 symbolic: all R and xi above are sympy expressions.  I4 n/a (no kappa read or output).  I5 no Friedmann matching.")
P("I6 footing rho_DE (eps = rho_DE c^2).  I7 hbar only in the common Q; no Bekenstein-Hawking 1/4.  I8 weights printed.")

# ---------------- verdict / controls ----------------
K = [c for c in checks if c["name"].startswith(("K", "I1"))]
allpass = all(c["pass"] for c in K)
res["checks"] = checks
code = 0
if not MUT:
    verdict = "FILTER HOLDS" if allpass else "FILTER FAILS"
    code = 0 if allpass else 1
else:
    mu1 = wt(R_rad) == -1 and not next(c for c in checks if c["name"] == "K2 thermal ratios")["pass"]
    mu2 = wt(Rstar) == 2 and need == 2
    P(f"\nMU1 un-glue eps: wt(R_th) -> {wt(R_rad)} (expected -1), L1 thermal check failed: {mu1}")
    P(f"MU2 n = 4: wt(R*) -> {wt(Rstar)}, L3 rhs -> {need} (expected 2, 2): {mu2}")
    verdict = "CONTROLS BITE" if (mu1 and mu2) else "CONTROL DID NOT BITE: lane void"
    code = 1 if (mu1 and mu2) else 2
    res["MU1"] = mu1; res["MU2"] = mu2
P(f"\nVERDICT: {verdict}" + ("" if MUT else " (screen only; it selects nothing). kappa = 1/2 FITTED; not theory closed."))
res["verdict"] = verdict
with open(os.path.join(HERE, f"w4_21_results{SUF}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(code)
