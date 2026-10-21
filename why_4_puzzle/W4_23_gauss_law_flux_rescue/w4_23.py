#!/usr/bin/env python3
"""W4-23 -- the Gauss-law (fixed-flux) rescue of the sign wall. Model + audit lane; no kappa is derived.
Criteria: FROZEN_CRITERIA.md (committed alone, f98069665). Light: sympy only, single core. Run from the repo root:
    python3 why_4_puzzle/W4_23_gauss_law_flux_rescue/w4_23.py > why_4_puzzle/W4_23_gauss_law_flux_rescue/w4_23.out
    W4_23_MUTATE=1 ... > .../w4_23_MUTATE.out   (MU1 field-sector sign flip, MU2 p = n+1; exit 1 when both bite)
kappa = 1/2 FITTED. Not theory closed.
"""
import json, os, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("W4_23_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
SIGN = -1 if MUT else 1          # MU1: flip the field-sector sign
PSHIFT = 1 if MUT else 0         # MU2: one quantum per (n+1)-cell
OUT, checks, res = [], [], {}
pi = sp.pi


def P(s=""):
    print(s); OUT.append(str(s))


def check(name, detail, ok):
    checks.append({"name": name, "detail": str(detail), "pass": bool(ok)})
    P(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


P("W4-23 Gauss-law (fixed-flux) rescue of the sign wall" + ("  [MUTATE: MU1 sign flip, MU2 p = n+1]" if MUT else ""))
P("kappa = 1/2 FITTED; not theory closed.\n")

# ---------------- K1: duality dE/ds = mu/2, dU/dt = nu/2; monotonicity ----------------
y = sp.Symbol("y", positive=True)                      # y = gN/a0
laws = {"simple": (1 + sp.sqrt(1 + 4 / y)) / 2,
        "standard n=2": sp.sqrt(sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / y ** 2)),
        "additive": 1 + 1 / sp.sqrt(y)}
grid = [sp.Rational(1, 10 ** 4), sp.Rational(1, 100), sp.Rational(1, 3), 1, 3, 100, 10 ** 4]
k1 = True
for name, nu in laws.items():
    gN = y; g = nu * y                                  # a0 = 1
    # check each law really is g = nu gN with the stated mu (simple / standard) by substitution
    resid = {"simple": g ** 2 / (1 + g) - gN, "standard n=2": g ** 2 / sp.sqrt(1 + g ** 2) - gN,
             "additive": g - (gN + sp.sqrt(gN))}[name]
    ok_law = all(abs(resid.subs(y, v).evalf(30)) < 1e-20 for v in grid)
    dnu = sp.diff(nu, y)
    dg = sp.diff(g, y)
    mu = 1 / nu
    dmu_dx = sp.diff(mu, y) / dg                        # d mu / d(g), parametric
    nu_dec = all(dnu.subs(y, v).evalf() < 0 for v in grid)
    g_inc = all(dg.subs(y, v).evalf() > 0 for v in grid)
    mu_inc = all(dmu_dx.subs(y, v).evalf() > 0 for v in grid)
    # U_tt sign = sign(nu') (t = y^2, dy/dt > 0); E_ss sign = sign(mu') (s = g^2, ds/dg > 0)
    k1 &= ok_law and nu_dec and g_inc and mu_inc
    P(f"  {name}: law ok {ok_law}; nu decreasing {nu_dec} -> U concave in t; mu increasing {mu_inc} -> E convex in s")
check("K1 duality", "dE/ds = mu/2 (increasing), dU/dt = nu/2 (decreasing) for all three laws: every MOND law is convex "
      "in s and concave in t, so I-a forbids every MOND interpolation for stable s-affine media", k1)

# ---------------- K2: minimal fixed-flux medium, exponent fixed by dimension ----------------
a, b, t, x, K, eps, B = sp.symbols("a b t x K epsilon B", positive=True)
k2, res["K2"] = True, {}
for n in (3, 4, 5):
    p, q = n + PSHIFT, n - 2
    f = a * x ** (-p) + b * t * x ** q
    xs = sp.solve(sp.diff(f, x), x)
    xs = [s_ for s_ in xs if s_.is_positive][0]
    fmin = sp.simplify(f.subs(x, xs))
    e = sp.simplify(t * sp.diff(sp.log(fmin), t))
    want = sp.Rational(n, 2 * (n - 1))
    res["K2"][n] = str(e)
    k2 &= (e == want)
    P(f"  n = {n}: inf_x[a x^-{p} + b t x^{q}] ~ t^{e} (deep MOND needs t^{want})")
# n = 3 law reconstruction
D = sp.Symbol("D", positive=True)
c3 = sp.simplify((a * x ** (-3 - PSHIFT) + b * t * x).subs(x, [s_ for s_ in sp.solve(sp.diff(a * x ** (-3 - PSHIFT) + b * t * x, x), x) if s_.is_positive][0]))
U = eps + t / (2 * K) + c3
h = sp.simplify(sp.diff(U.subs(t, D ** 2), D))            # field = dU/dD
gN = D / K
a0 = sp.Symbol("a0", positive=True)
cc = sp.simplify(c3 / t ** sp.Rational(3, 4)) if not MUT else None
law_ok = False
if not MUT:
    a0_val = sp.simplify(sp.Rational(9, 4) * cc ** 2 * K)
    law_ok = sp.simplify(h - (gN + sp.sqrt(a0_val * gN))) == 0
    P(f"  n = 3: g = dU/dD = {h};  = gN + sqrt(a0 gN) with a0 = {a0_val}: {law_ok}")
check("K2 exponent and law", f"exponents {res['K2']} = n/(2(n-1)); n = 3 gives g = gN + sqrt(a0 gN): {law_ok}", k2 and law_ok)

# ---------------- K3 / K4: stability set by the field-sector sign ----------------
f0, D0, th = sp.symbols("f0 D0 theta", positive=True)
F = f0 + b * x
Uflux = a / x ** 3 + F * D0 ** 2
xstar = (3 * a / (b * D0 ** 2)) ** sp.Rational(1, 4)
assert sp.simplify(sp.diff(Uflux, x).subs(x, xstar)) == 0
Uxx = sp.simplify(sp.diff(Uflux, x, 2).subs(x, xstar))
hval = 2 * F * D0
Wfun = sp.Symbol("hh", positive=True) ** 2 / (4 * F) - a / x ** 3
W_x = sp.simplify(sp.diff(Wfun, x).subs(sp.Symbol("hh", positive=True), hval).subs(x, xstar))
Wxx = sp.simplify(sp.diff(Wfun, x, 2).subs(sp.Symbol("hh", positive=True), hval).subs(x, xstar))
stiff = lambda s2: sp.simplify(SIGN * (Uxx - 2 * (b ** 2 / F.subs(x, xstar)) * D0 ** 2 * s2))
s_par, s_perp = stiff(0), stiff(1)
num = {a: sp.Rational(7, 3), b: sp.Rational(2, 5), f0: sp.Rational(3, 2), D0: sp.Rational(5, 4)}
es_ok = (sp.simplify(s_perp - SIGN * (-Wxx)) == 0 and s_par.subs(num).evalf() > 0 and s_perp.subs(num).evalf() > 0)
P(f"\nbranch x* = {xstar}: W_x(x*) = {W_x} (same branch);  U_xx = {Uxx};  W_xx = {Wxx}")
P(f"electrostatic-sign x-stiffness: k||D0 {s_par};  k_|_D0 {s_perp} (= -W_xx: {sp.simplify(s_perp - SIGN*(-Wxx)) == 0})")
check("K3 Gauss-law sign stable", "x-stiffness positive at both ends (U_xx and -W_xx) and linear in sin^2 theta: stable "
      "for every direction", es_ok and W_x == 0)
grav_unstable = (SIGN * Wxx).subs(num).evalf() < 0
lim0 = sp.limit((sp.Symbol("hh", positive=True) ** 2 / (4 * F) - a / x ** 3).subs(sp.Symbol("hh", positive=True), 1), x, 0, "+")
check("K4 gravity sign unstable", f"on the MOND branch W_xx = {Wxx} < 0 (a maximum; Phi relaxation only lowers it); "
      f"W -> {lim0} as x -> 0: no stable ground state", grav_unstable and lim0 == -sp.oo)

# ---------------- K5: flux-affine = field-affine; QUMOND sign structure ----------------
Dv, hv, Fx, Vx = sp.symbols("D_v h_v F_x V_x", positive=True)
Dst = sp.solve(sp.diff(hv * Dv - (Vx + Fx * Dv ** 2), Dv), Dv)[0]
leg = sp.simplify((hv * Dv - (Vx + Fx * Dv ** 2)).subs(Dv, Dst))
qm = sp.Matrix([[0, 1], [1, 0]]).eigenvals()
dPhi, dPhiN = sp.symbols("dPhi dPhiN", positive=True)   # radial gradient magnitudes (first run used real=True: K5 Piecewise/Abs artefact)
q1, q2, zz = sp.symbols("q1 q2 zz", positive=True)
Qf = lambda z: q1 * z + q2 * z ** sp.Rational(3, 4)          # a generic concave medium function
Lq = -(2 * dPhi * dPhiN - Qf(dPhiN ** 2))
el = sp.solve(sp.diff(Lq, dPhiN), dPhi)[0]
nu_q = sp.simplify(el / dPhiN)
nu_ok = sp.simplify(nu_q - sp.diff(Qf(zz), zz).subs(zz, dPhiN ** 2)) == 0
P(f"\nLegendre at fixed x: sup_D[hD - V - F D^2] = {leg} (affine in s = h^2)")
P(f"QUMOND cross term eigenvalues {qm}; Phi_N equation gives grad Phi = {nu_q} grad Phi_N, i.e. nu = Q'(t)")
check("K5 sign structure", "flux-affine is field-affine at fixed x; QUMOND's cross term is indefinite (+1, -1) and nu = Q'",
      sp.simplify(leg - (hv ** 2 / (4 * Fx) - Vx)) == 0 and set(qm.keys()) == {1, -1}
      and nu_ok)

# ---------------- K6: vacuum and the 4 ----------------
fB = a / x ** 3 + B * x + b * t * x
xB = [s_ for s_ in sp.solve(sp.diff(fB, x), x) if s_.is_positive][0]
UB = sp.simplify(fB.subs(x, xB))
dU0 = sp.limit(sp.diff(UB, t), t, 0, "+")
dU0_free = sp.limit(sp.diff(c3, t), t, 0, "+") if not MUT else None
cfix = sp.Rational(4, 3) * (3 * a) ** sp.Rational(1, 4) * b ** sp.Rational(3, 4)
hh = sp.Symbol("hh", positive=True)
Dlow = sp.solve(sp.diff(hh * D - cfix * D ** sp.Rational(3, 2), D), D)[0]
Elow = sp.simplify((hh * D - cfix * D ** sp.Rational(3, 2)).subs(D, Dlow))
C3 = sp.simplify(Elow / hh ** 3)
C2 = K / 2
R = sp.simplify(eps * C3 ** 2 / C2 ** 3)
xi = sp.simplify(32 * pi / (9 * R))
P(f"\nsame-amplitude vacuum (B > 0): U'(0+) = {dU0} (finite: Newtonian IR);  separate vacuum (B = 0): U'(0+) = {dU0_free}")
P(f"C3 = {C3}, C2 = K/2, R = {R}, xi = {xi}")
k6 = (dU0.is_finite and dU0_free == sp.oo and sp.simplify(R - eps / (54 * a * b ** 3 * K ** 3)) == 0
      and sp.simplify(xi - 192 * pi * a * b ** 3 * K ** 3 / eps) == 0) if not MUT else False
check("K6 vacuum and the 4", "same-amplitude vacuum is analytic at t = 0; separate eps gives R = eps/(54 a b^3 K^3), "
      "xi = 192 pi a b^3 K^3/eps: TRADE, weight 1 with pi-free inputs", k6)

# ---------------- identity checks ----------------
src = open(os.path.abspath(__file__)).read()
bad = ["5." + "7888", "0." + "1727", "9." + "36e-11", "9." + "3603e-11", "1." + "13e-10", "1." + "1312e-10",
       "1." + "2e-10", "0." + "417", "0." + "465", "0." + "551"]
hits = [s_ for s_ in bad if s_ in src]
check("I1 forbidden constants", f"hits {hits}", not hits)
Z = sp.Symbol("Z", positive=True)
i3 = sp.simplify(R.subs({eps: Z * eps, a: Z * a, b: Z * b, K: K / Z}, simultaneous=True) - R) == 0 if not MUT else True
check("I3 invariance", "R unchanged under the common energy rescaling (eps, a, b, K) -> (Z eps, Z a, Z b, K/Z)", i3)
P("I2 symbolic.  I4 no law kappa read.  I5 no Friedmann.  I6 rho_DE footing.  I7 classical, hbar-free.  I8 xi weight 1.")

# ---------------- verdict / controls ----------------
res["checks"] = checks
byname = {c["name"]: c["pass"] for c in checks}
if not MUT:
    ok = all(byname.values())
    verdict = ("GAUSS-LAW REWRITE DOES NOT ESCAPE FOR GRAVITY'S SIGN; THE ESCAPE IS THE OPPOSITE-SIGN FLUX SECTOR (X15); "
               "1/2 NOT REACHED") if ok else "CHECK FAILED"
    code = 0 if ok else 1
else:
    mu1 = (not byname["K3 Gauss-law sign stable"]) and (not byname["K4 gravity sign unstable"])
    mu2 = (res["K2"][3] == "4/5") and not byname["K2 exponent and law"]
    P(f"\nMU1 sign flip: electrostatic-stable and gravity-unstable checks both fail: {mu1}")
    P(f"MU2 p = n+1: n = 3 exponent -> {res['K2'][3]} (expected 4/5), law check fails: {mu2}")
    verdict = "CONTROLS BITE" if (mu1 and mu2) else "CONTROL DID NOT BITE: lane void"
    code = 1 if (mu1 and mu2) else 2
    res["MU1"], res["MU2"] = mu1, mu2
P(f"\nVERDICT: {verdict}" + ("" if MUT else ". kappa = 1/2 FITTED; not theory closed."))
res["verdict"] = verdict
with open(os.path.join(HERE, f"w4_23_results{SUF}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(code)
