#!/usr/bin/env python3
"""W4-22 -- a model in W4-21's wt R = 1 class: Gauss-normalized Newtonian stiffness x 3D one-loop MOND cubic x tree vacuum.
Criteria: FROZEN_CRITERIA.md (committed alone, f0294ae1c). Light: sympy only, single core. Run from the repo root:
    python3 why_4_puzzle/W4_22_gauss_times_loop_model/w4_22.py > why_4_puzzle/W4_22_gauss_times_loop_model/w4_22.out
    W4_22_MUTATE=1 ... > .../w4_22_MUTATE.out   (MU1 N 2 -> 1, MU2 8piG -> 4piG, each run separately; exit 1 when both bite)
kappa = 1/2 FITTED. Not theory closed.
"""
import json, os, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("W4_22_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
OUT, checks, res = [], [], {}
pi = sp.pi


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def wt(e):
    """pi-weight on the class r*pi^w (r algebraic nonzero, w integer); symbols other than pi are treated as pi-free."""
    e = sp.simplify(e)
    num, den = sp.fraction(sp.together(e))
    try:
        pn, pd = sp.Poly(num, pi), sp.Poly(den, pi)
    except sp.PolynomialError:
        return None
    if len(pn.terms()) != 1 or len(pd.terms()) != 1:
        return None
    return int(pn.degree() - pd.degree())


P("W4-22 Gauss stiffness x 3D one-loop cubic" + ("  [MUTATE: MU1 N -> 1 and MU2 8piG -> 4piG, run separately]" if MUT else ""))
P("Model-building lane; footing rho_DE. kappa = 1/2 FITTED; not theory closed.\n")

# ---------------- K0: W4-21's three shapes are one class ----------------
v = sp.Matrix([[1, 2, -3]])
k1, k2 = sp.Matrix([1, 1, 1]), sp.Matrix([0, 3, 2])
in_ker = (v * k1)[0] == 0 and (v * k2)[0] == 0
# integer kernel basis (-2,1,0), (3,0,1) expressed in {k1, k2} with integer coefficients, and back
a, b = sp.symbols("a b")
combos = {}
for kb in (sp.Matrix([-2, 1, 0]), sp.Matrix([3, 0, 1])):
    s_ = sp.solve(list(a * k1 + b * k2 - kb), [a, b], dict=True)
    combos[tuple(kb)] = s_[0] if s_ else None
integral = all(c is not None and all(val.is_integer for val in c.values()) for c in combos.values())
shapes = [sp.Matrix(s) for s in ((1, 0, 0), (-1, 1, 0), (0, -1, -1))]
diffs_in_ker = all((v * (shapes[i] - shapes[0]))[0] == 0 for i in (1, 2))
P(f"kernel basis in {{(1,1,1),(0,3,2)}}: {combos}")
check("K0 one class", f"common-factor and field-rescaling shifts span the kernel lattice: {in_ker and integral}; "
      f"W4-21 shapes differ by kernel vectors: {diffs_in_ker}", in_ker and integral and diffs_in_ker)

# ---------------- the model ----------------
eps, kT, lam, G, c, h = sp.symbols("epsilon kT lambda G c h", positive=True)
Ns = sp.Symbol("N", positive=True, integer=True)
Y = eps * kT ** 2 * lam ** 6 * G ** 3 / c ** 12


def model(N, gauss):
    C2 = c ** 4 / (gauss * pi * G)                 # M1: field energy g^2/(gauss*pi*G), g = c^2 h
    C3 = N * kT * lam ** 3 / (12 * pi)             # M2: zero-mode threshold, magnitude
    R = sp.simplify(eps * C3 ** 2 / C2 ** 3)
    xi = sp.simplify(32 * pi / (9 * R))           # A1 at n = 3 with q = 1
    return C2, C3, R, xi


variants = [("normal", 2, 8)] if not MUT else [("MU1 N = 1", 1, 8), ("MU2 4piG", 2, 4)]
for tag, Nv, gauss in variants:
    C2, C3, R, xi = model(Nv, gauss)
    pref = sp.simplify(R / Y)
    P(f"[{tag}] C2 = {C2}, |C3| = {C3}")
    P(f"[{tag}] R = {R} = ({pref}) * Y;  xi = {xi};  wt(R/Y) = {wt(pref)}")
    res[tag] = {"R_over_Y": str(pref), "xi": str(xi), "wt": wt(pref)}
    Cg2, Cg3, Rg, xig = model(Ns, 8)
    if tag == "normal":
        gen = sp.simplify(Rg - 32 * pi * Ns ** 2 * Y / 9) == 0 and sp.simplify(xig - 1 / (Ns ** 2 * Y)) == 0
        check("K1 pi matched", f"R = (32 pi N^2/9) Y and xi = 1/(N^2 Y) for every N: {gen}; N = 2 prefactor {pref} "
              f"= (8pi)^3/(6pi)^2: {sp.simplify(pref - (8 * pi) ** 3 / (6 * pi) ** 2) == 0}; wt 1",
              gen and sp.simplify(pref - sp.Rational(128, 9) * pi) == 0 and wt(pref) == 1)
    else:
        check(f"K1 under {tag}", f"prefactor {pref} (frozen normal 128pi/9), xi = {xi}",
              sp.simplify(pref - sp.Rational(128, 9) * pi) == 0)

# ---------------- K2: Y dimensionless ----------------
dims = {eps: (1, -1, -2), kT: (1, 2, -2), G: (-1, 3, -2), c: (0, 1, -1)}      # (kg, m, s)
powY = {eps: 1, kT: 2, G: 3, c: -12}
tot = tuple(sum(powY[s] * dims[s][i] for s in powY) for i in range(3))
check("K2 Y dimensionless", f"(kg, m, s) exponents of eps (kT)^2 G^3 / c^12 = {tot}", tot == (0, 0, 0))

# ---------------- K3: R2 the 4 relocates ----------------
kappa = 1 / (Ns * sp.sqrt(Y))
dep = {str(s): sp.simplify(sp.diff(kappa, s)) != 0 for s in (eps, kT, lam, G, c)}
k_half = kappa.subs(Ns, 2).subs(eps, 1 / (kT ** 2 * lam ** 6 * G ** 3 / c ** 12))
P(f"\nkappa = 1/(N sqrt(Y)) = {kappa};  depends on {dep}")
check("K3 TRADE", f"kappa depends on every scale {all(dep.values())}; N = 2, Y = 1 gives kappa = {sp.simplify(k_half)} "
      f"-> the excluded H061 class (kappa = 1/channel count)", all(dep.values()) and sp.simplify(k_half) == sp.Rational(1, 2))

# ---------------- K4: R3 shape no-go (natural units hbar = c = 1 for the loop) ----------------
C2t, C3t, T, e0 = sp.symbols("C2t C3t T e0", positive=True)
ratio_low = sp.limit(C3t * h ** 3 / (C2t * h ** 2), h, 0)
C2c = Ns * lam ** 2 * T ** 2 / 24                 # cancellation: tree C2 = loop low-field quadratic
C3c = Ns * lam ** 3 * T / (12 * pi)
Rc_tree = sp.simplify(e0 * C3c ** 2 / C2c ** 3)
xi_tree = sp.simplify(32 * pi / (9 * Rc_tree))
Rc_loop = sp.simplify((Ns * pi ** 2 * T ** 4 / 90) * C3c ** 2 / C2c ** 3)
xi_loop = sp.simplify(32 * pi / (9 * Rc_loop))
P(f"\nlow-h ratio C3 h^3/(C2 h^2) -> {ratio_low} (Newton-leading at low h)")
P(f"cancellation C2 = N lam^2 T^2/24: tree vacuum R = {Rc_tree}, xi = {xi_tree} (wt {wt(xi_tree)}); "
  f"loop vacuum R = {Rc_loop}, xi = {xi_loop} (wt {wt(xi_loop)})")
check("K4 shape no-go", "tree + loop is Newton-leading at low h; with the cancellation a MOND shape needs, xi = "
      f"{xi_tree} (wt {wt(xi_tree)}) or {xi_loop} (wt {wt(xi_loop)}): pi-odd, never 1/4",
      ratio_low == 0 and sp.simplify(xi_tree - pi ** 3 * Ns * T ** 4 / (27 * e0)) == 0 and wt(xi_tree) == 3
      and Rc_loop == sp.Rational(16, 15) and sp.simplify(xi_loop - 10 * pi / 3) == 0)
res["K4"] = {"xi_tree": str(xi_tree), "xi_loop": str(xi_loop)}

# ---------------- K5: R4 sign ----------------
X, aa, bb = sp.symbols("X a b", real=True)
F = aa * X + bb * X ** sp.Rational(3, 2)
F2 = sp.simplify(sp.diff(F, X, 2))
conc = sp.solve(sp.Eq(F2.subs(X, 1), 0), bb)        # F'' = (3b/4) X^(-1/2): sign set by b alone
N_, gam, th = sp.symbols("N gamma theta", positive=True)
Fth = N_ * (-pi ** 2 * th ** 4 / 90 + gam * th ** 2 * X / 24 - gam ** sp.Rational(3, 2) * th * X ** sp.Rational(3, 2) / (12 * pi))
cub = sp.expand(Fth).coeff(X ** sp.Rational(3, 2))
P(f"\nF''(X) = {F2}: concave on X > 0 iff b <= 0.  Thermal cubic coefficient {cub} (< 0).  "
  f"(-1)^F flip gives {-cub} and quadratic {-sp.expand(Fth).coeff(X, 1)}: the signs the cancellation needs; not a state.")
check("K5 sign wall", f"F'' = {F2}; thermal cubic {cub} is negative", sp.simplify(F2 - sp.Rational(3, 4) * bb / sp.sqrt(X)) == 0
      and cub.is_negative)

# ---------------- identity checks ----------------
src = open(os.path.abspath(__file__)).read()
bad = ["5." + "7888", "0." + "1727", "9." + "36e-11", "9." + "3603e-11", "1." + "13e-10", "1." + "1312e-10",
       "1." + "2e-10", "0." + "417", "0." + "465", "0." + "551"]
hits = [x for x in bad if x in src]
check("I1 forbidden constants", f"hits {hits}", not hits)
A_, B_ = sp.symbols("A B", positive=True)
k_sc = sp.simplify(kappa.subs({G: A_ * G, eps: B_ * eps}, simultaneous=True) / kappa)
check("I3 scaling", f"kappa ratio under G -> A G, eps -> B eps at fixed kT lam^3: {k_sc} (moves: TRADE, as expected)",
      k_sc != 1)
P("I2 dependence printed in K3.  I4 no law kappa read.  I5 no Friedmann.  I6 rho_DE only.  "
  "I7 hbar-free (zero-mode term classical in T).  I8 weights printed.")

# ---------------- verdict / controls ----------------
res["checks"] = checks
if not MUT:
    ok = all(c["pass"] for c in checks)
    verdict = "pi MATCHED, 1/2 NOT REACHED (TRADE N^2 Y = 4; shape no-go; sign wall)" if ok else "CHECK FAILED"
    code = 0 if ok else 1
else:
    _, _, R1, xi1 = model(1, 8)
    _, _, R2, xi2 = model(2, 4)
    mu1 = sp.simplify(R1 / Y - sp.Rational(32, 9) * pi) == 0 and sp.simplify(xi1 - 1 / Y) == 0
    mu2 = sp.simplify(xi2 - 8 / (4 * Y)) == 0 and wt(sp.simplify(R2 / Y)) == 1
    P(f"\nMU1 N -> 1: prefactor 32pi/9, xi = 1/Y: {mu1}")
    P(f"MU2 8piG -> 4piG: xi = 8/(N^2 Y) at N = 2 and wt R still 1: {mu2}")
    verdict = "CONTROLS BITE" if (mu1 and mu2) else "CONTROL DID NOT BITE: lane void"
    code = 1 if (mu1 and mu2) else 2
    res["MU1"], res["MU2"] = mu1, mu2
P(f"\nVERDICT: {verdict}" + ("" if MUT else ". kappa = 1/2 FITTED; not theory closed."))
res["verdict"] = verdict
with open(os.path.join(HERE, f"w4_22_results{SUF}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(code)
