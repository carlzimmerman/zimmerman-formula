"""CFG807 script 2: is the P-sector vacuum energy of the stiffened action well-defined, and does the action fix it?

Criteria: FROZEN_CRITERIA.md (committed alone first). Checks V0-V4.
Units: K = 4 pi G, a = a0, x = u/a, y = g_N/a. S2 vacuum energy eps = (a^2/K) C. kappa = 1/2 <=> C = 16 pi
(<=> rho_DE c^2 = 4 a0^2/G <=> Lambda c^4/a0^2 = 2C = 32 pi; single-field units, no BIMOND 1/(1+alpha) factor).

Two normalisations of the PAPER42 premise "no vacuum constant in the strong-field state" exist in S2:
  (a) potential form:   eps_W = W_rem(0) - W_rem(u_strong)          (u is the field, g_N = R(u) = K W_rem'(u))
  (b) QUMOND-dual form: eps_Q = (1/K) int_0^inf u dg_N               (Legendre dual; PAPER42's Lambda c^4 = int (g - g_N) dg_N)
They differ by the boundary term u g_N / K, which diverges when u saturates.

Run:  nice python3 cfg807_vacuum.py                  (seconds)
      CFG807_MUTATE=M2 nice python3 cfg807_vacuum.py  (monotonicity detector restricted to y <= 1; control check must FAIL)
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy import integrate, optimize

MODE = os.environ.get("CFG807_MUTATE", "")
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = f"_MUTATE_{MODE}" if MODE else ""
OUTF = open(os.path.join(HERE, f"cfg807_vacuum{SUF}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUTF.write(s + "\n")


RES = {"lane": "CFG807", "script": "vacuum", "mutate": MODE, "checks": {}, "numbers": {}}
FAILS = []


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=str(detail))
    if not ok:
        FAILS.append(name)


G = 6.67430e-11
C_LIGHT = 2.99792458e8
PC = 3.0856775814913673e16
MSUN = 1.98847e30
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
TARGET = 16 * math.pi

P("CFG807 script 2: the P-sector vacuum energy in the stiffened action" + (f"  [MUTATE {MODE}]" if MODE else ""))

# ================================================================ V0 sympy
P("\nV0  sympy: EL equations vs an additive constant in W_rem; criticality K W_rem''(0) = 0")
xx = sp.symbols("x")
K, a, gam, Cc, rho = sp.symbols("K a gamma C rho", positive=True)
u = sp.symbols("u", positive=True)
Wrem = (a ** 2 / K) * (-u / a - sp.log(1 - u / a) - (u / a) ** 2 / 2) + Cc
v0a = sp.simplify(K * sp.diff(Wrem, u) - u ** 2 / (a - u)) == 0
v0b = sp.simplify(sp.diff(Wrem, u, 2).subs(u, 0)) == 0
Phi, Pf = sp.Function("Phi")(xx), sp.Function("P")(xx)
uP = K * Pf                                  # 1D, P > 0 branch
Wf = (a ** 2 / K) * (-uP / a - sp.log(1 - uP / a) - (uP / a) ** 2 / 2)
L0 = -(sp.diff(Phi, xx) - K * Pf) ** 2 / (2 * K) - rho * Phi - Wf - gam / 2 * sp.diff(Pf, xx) ** 2
from sympy.calculus.euler import euler_equations
e0 = euler_equations(L0, [Phi, Pf], xx)
e1 = euler_equations(L0 - Cc, [Phi, Pf], xx)
v0c = all(sp.simplify(p.lhs - q.lhs) == 0 for p, q in zip(e0, e1))
# uniform state: stiffness term vanishes identically -> gamma (hence L*) cannot enter the uniform-state energy
Lunif = L0.subs({Pf: sp.Symbol("P0"), Phi: sp.Symbol("g0") * xx}).doit()
v0d = sp.diff(Lunif, gam) == 0
check("V0a K W_rem' = u^2/(a-u) for the explicit W_rem (any C)", v0a, "exact")
check("V0b K W_rem''(0) = 0 for every additive C (criticality)", v0b, "exact")
check("V0c Euler-Lagrange equations identical with and without the constant C", v0c, "exact")
check("V0d gamma (stiffness) absent from the uniform-state Lagrangian", v0d, "d L_uniform / d gamma = 0")

# ================================================================ V1 the two normalisations, frozen W_rem
P("\nV1  the vacuum energy with the PAPER42 premise, frozen W_rem (units a^2/K)")
xs = sp.symbols("xs", positive=True)
w_strong = sp.limit(-xs - sp.log(1 - xs) - xs ** 2 / 2, xs, 1, "-")
P(f"  (a) potential form: K W_rem(u)/a^2 - const -> {w_strong} as u -> a  =>  eps_W = W(0) - W(strong) = -oo (log wall, AdS sign)")
uy = lambda y: 2 * y / (y + math.sqrt(y * y + 4 * y))   # frozen law u/a vs y = g_N/a (simple mu), cancellation-free form
ys = sp.symbols("ys", positive=True)
I_sym = sp.integrate(sp.simplify((-ys + sp.sqrt(ys ** 2 + 4 * ys)) / 2), (ys, 0, sp.Symbol("Y", positive=True)))
Yb = sp.Symbol("Y", positive=True)
lead = sp.limit(I_sym / Yb, Yb, sp.oo)
nxt = sp.limit(I_sym - Yb + sp.log(Yb), Yb, sp.oo)
P(f"  (b) QUMOND-dual: I(Y) = int_0^Y (u/a) dy: I/Y -> {lead}; I - Y + ln Y -> {sp.nsimplify(nxt)} = {float(nxt):.6f}")
Inum = {Y: integrate.quad(uy, 0, Y, limit=400)[0] for Y in (1e2, 1e4, 1e6)}
for Y, v in Inum.items():
    P(f"      I({Y:.0e}) = {v:.6g}   (asymptote Y - ln Y + {float(nxt):.4f} = {Y - math.log(Y) + float(nxt):.6g})")
P("      => eps_Q = +oo (linear, de Sitter sign): the phantom saturates at u -> a0, so int u dg_N grows like a0 g_N,max")
v1_defined = bool((w_strong != sp.oo) and (lead == 0))   # eps_W finite needs no log wall; eps_Q finite needs I/Y -> 0
check("V1 vacuum energy well-defined (finite and positive) for the frozen W_rem", v1_defined,
      "eps_W = -oo (log wall), eps_Q = +oo (linear): NOT well-defined")
RES["numbers"]["V1"] = dict(eps_W="-oo", I_Q_lead=str(lead), I_Q_next=float(nxt), I_Q_num={str(k): v for k, v in Inum.items()})

# ================================================================ V2 can a turn-off be a single-valued W_rem(u)?
P("\nV2  representability: a finite eps_Q needs u -> 0 at strong field; is u(g_N) then monotone (single-valued R(u))?")
YMAX = 1.0 if MODE == "M2" else 1e6
ygrid = np.logspace(-6, math.log10(YMAX), 4000)
kernels = {
    "frozen S2 law (simple mu)": lambda y: uy(y),
    "exponential RAR": lambda y: y * math.exp(-math.sqrt(y)) / (-math.expm1(-math.sqrt(y))),
    "S2 law + k=2 turn-off y_t=32": lambda y: uy(y) / (1 + (y / 32.0) ** 2),
    "S2 law + k=2 turn-off y_t=128.9": lambda y: uy(y) / (1 + (y / 128.915) ** 2),
}
mono = {}
for nm, fn in kernels.items():
    v = np.array([fn(y) for y in ygrid])
    mono[nm] = bool(np.all(np.diff(v) > 0))
    Ifin = integrate.quad(fn, 0, np.inf, limit=800)[0] if "frozen" not in nm else float("inf")
    P(f"  {nm:34s}: u(g_N) monotone = {mono[nm]!s:5s}  -> single-valued W_rem(u) {'EXISTS' if mono[nm] else 'does NOT exist'};"
      f"  int (u/a) dy = {Ifin:.5g}")
    RES["numbers"].setdefault("V2", {})[nm] = dict(monotone=mono[nm], I=Ifin)
ctrl = mono["frozen S2 law (simple mu)"] and not mono["exponential RAR"] and not mono["S2 law + k=2 turn-off y_t=128.9"]
check("V2-control detector: frozen law monotone, RAR and turn-off non-monotone", ctrl, mono)
P("  RAR control: int = %.4f (record p21: 12.99)" % RES["numbers"]["V2"]["exponential RAR"]["I"])

P("  General statement, numerically: continuous R(u) = K W_rem'(u), R(0) = 0, onto [0, inf):")
P("    for g_N > max R on [0, d] every stationary u exceeds d > 0, so int u dg_N >= d (g_N - const) -> +oo.")
fams = {
    "frozen u^2/(a-u)": lambda x: x * x / (1 - x),
    "u^2 a/(a^2-u^2)": lambda x: x * x / (1 - x * x),
    "integrable wall u^2/(a sqrt(1-u/a))": lambda x: x * x / math.sqrt(1 - x),
    "non-saturating u^2 (1+u/a)/a": lambda x: x * x * (1 + x),
}
gen = {}
for nm, R in fams.items():
    sat = "non-saturating" not in nm
    def ustar(y):
        if sat:
            return optimize.brentq(lambda x: R(x) - y, 0.0, 1 - 1e-15, xtol=1e-16)
        return optimize.brentq(lambda x: R(x) - y, 0.0, 1e7, xtol=1e-14)
    Iv = [integrate.quad(ustar, 0, Y, limit=400)[0] for Y in (1e2, 1e3, 1e4)]
    if sat:
        w6 = integrate.quad(R, 0, 1 - 1e-6, limit=400)[0]
        w12 = integrate.quad(R, 0, 1 - 1e-12, limit=400)[0]
        epsW = -w12 if abs(w12 - w6) < 1e-2 * abs(w12) else float("-inf")   # converged at the wall?
    else:
        epsW = float("-inf")
    ok = Iv[2] / Iv[1] > 9 and Iv[1] / Iv[0] > 9            # at least linear growth
    gen[nm] = dict(I=Iv, epsW=epsW, at_least_linear=ok)
    P(f"    {nm:38s}: I(1e2,1e3,1e4) = {Iv[0]:.4g}, {Iv[1]:.4g}, {Iv[2]:.4g}  (>= linear: {ok});  eps_W = {epsW:.4g}")
check("V2-general eps_Q diverges (>= linear) for every continuous admissible R", all(g["at_least_linear"] for g in gen.values()),
      "4 families")
P("    eps_W is NEGATIVE whenever finite (W_rem increases with u because R = g_N >= 0): anti-de Sitter sign.")
RES["numbers"]["V2_general"] = gen
v2_repr = any(mono[nm] and math.isfinite(RES["numbers"]["V2"][nm]["I"]) for nm in kernels)   # finite AND single-valued
check("V2 a finite turn-off representable by a single-valued W_rem(u)", v2_repr,
      "finite eps_Q requires non-monotone u(g_N) => R(u) double-valued => no W_rem(u)")

# ================================================================ V3 does the action fix y_t or C?
P("\nV3  candidate turn-offs from the action's own elements (L*, gamma = K L*^2/2, K = 4 pi G)")
v3 = {}
for f, a0 in A0.items():
    for Lpc in (5.75, 11.5, 1000.0):
        L = Lpc * PC
        y_cL = C_LIGHT ** 2 / (a0 * L)
        v3[f"{f}|L*={Lpc}|c2/(a0 L*)"] = dict(y_t=y_cL, C=math.pi / 2 * y_cL)
        for Msun in (1.0, 1e5, 1e6, 1e11):
            y_M = G * Msun * MSUN / (a0 * L ** 2)
            v3[f"{f}|L*={Lpc}|M={Msun:g}"] = dict(y_t=y_M)
c0 = v3["canonical|L*=5.75|c2/(a0 L*)"]
P(f"  (i) c^2/(a0 L*) at L* = 5.75 pc: y_t = {c0['y_t']:.3e} -> C ~ (pi/2) y_t = {c0['C']:.3e} = {c0['C'] / TARGET:.2e} x 16 pi;"
  f" at 1 kpc: y_t = {v3['canonical|L*=1000.0|c2/(a0 L*)']['y_t']:.3e}")
for Msun in (1.0, 1e5, 1e6, 1e11):
    P(f"  (ii) point-mass screening edge y_t(M) = (r_M/L*)^2, M = {Msun:7.0e} Msun: L* 5.75 pc {v3[f'canonical|L*=5.75|M={Msun:g}']['y_t']:.3e};"
      f" L* x2 {v3[f'canonical|L*=11.5|M={Msun:g}']['y_t']:.3e}")
yM1, yM10 = v3["canonical|L*=5.75|M=100000"]["y_t"], v3["canonical|L*=5.75|M=1e+06"]["y_t"]
yL2 = v3["canonical|L*=11.5|M=100000"]["y_t"]
universal = abs(yM10 / yM1 - 1) < 1e-6 and abs(yL2 / yM1 - 1) < 1e-6
check("V3-tooth: screening cut-off moves with M (x10) and L* (x2) => not a universal vacuum number", not universal,
      f"y_t ratios M x10: {yM10 / yM1:.3g}, L* x2: {yL2 / yM1:.3g}")
P("  (iii) gamma enters only gradients (V0d): the uniform vacuum state has zero stiffness energy.")
P("  (iv) K = 4 pi G fixes only the unit a0^2/K; with it the target reads C = 16 pi (D_kappa Route D).")
v3_fixed = False
check("V3 an action element fixes y_t or C with no hand-set number", v3_fixed, "none of L*, gamma, K does")
RES["numbers"]["V3"] = v3

# ================================================================ V4 hand-set turn-off: coefficient
P("\nV4  (reported) hand-set turn-off in the QUMOND-dual form: C(y_t) = int_0^inf (u/a)/(1+(y/y_t)^k) dy")
v4 = {}
for k in (2, 3, 4):
    Cf = lambda yt: integrate.quad(lambda y: uy(y) / (1 + (y / yt) ** k), 0, np.inf, limit=800)[0]
    root = optimize.brentq(lambda yt: Cf(yt) - TARGET, 5, 500, xtol=1e-10)
    ck = (math.pi / k) / math.sin(math.pi / k)
    v4[k] = dict(yt_16pi=root, slope=ck, C_at_32=Cf(32.0), C_at_128=Cf(128.915))
    P(f"  k = {k}: slope c_k = {ck:.5f}; C = 16 pi at y_t = {root:.4f}; C(32) = {Cf(32.0):.4f}; C(128.9) = {Cf(128.915):.3f}")
for f, a0 in A0.items():
    gt = v4[2]["yt_16pi"] * a0
    P(f"  {f}: k = 2 turn-off g_t = {gt:.3e} m/s^2 (needed, hand-set)")
P(f"  Lambda c^4/a0^2 = 2C: at y_t = {v4[2]['yt_16pi']:.3f} this is 32 pi = {32 * math.pi:.4f} by construction")
P("  NOTE: the turn-off is NOT representable in S2 (V2); this is the QUMOND-dual number, outside the frozen action.")
RES["numbers"]["V4"] = v4

# ================================================================ verdict (frozen classes)
solar = json.load(open(os.path.join(HERE, "cfg807_solar_results.json")))["checks"] if os.path.exists(
    os.path.join(HERE, "cfg807_solar_results.json")) else {}
s1 = solar.get("S1 Cassini Q2 < ceiling for every y_t", {}).get("ok")
s2 = solar.get("S2 TNO: |w_anom/w_pl| < 0.1 for all 90 and anomaly period > 4.5 Gyr for >= 80/90", {}).get("ok")
if s1 and s2 and v1_defined and v3_fixed:
    verdict = "ROUTE REVIVED"
elif s1 and s2 and (v1_defined or v2_repr):
    verdict = "ROUTE UNBLOCKED"
elif not (s1 and s2):
    verdict = "STILL BLOCKED (BLOCKED-SOLAR as frozen)"
else:
    verdict = "STILL BLOCKED (BLOCKED-STRUCTURAL)"
P(f"\nVERDICT (frozen rule): S1 {s1}, S2 {s2}, V1 {v1_defined}, V2 {v2_repr}, V3 {v3_fixed} -> {verdict}")
if not v1_defined and not v2_repr:
    P("  Independently of S2: the vacuum energy is not well-defined in the stiffened action => BLOCKED-STRUCTURAL as well.")
RES["verdict"] = verdict

if MODE == "M2":
    bite = "V2-control detector: frozen law monotone, RAR and turn-off non-monotone" in FAILS
    P(f"\nM2 tooth (detector restricted to y <= 1 -> control must FAIL): {'bites' if bite else 'DID NOT BITE'}")
    if not bite:
        FAILS.append("M2 tooth did not bite")
# the V1/V2/V3 'False' results are findings, not script failures; exit code reflects control checks only
CTRL = [n for n in FAILS if n.startswith(("V0", "V2-control", "V2-general", "V3-tooth", "M2"))]
RES["fails_findings"] = [n for n in FAILS if n not in CTRL]
RES["fails_controls"] = CTRL
json.dump(RES, open(os.path.join(HERE, f"cfg807_vacuum_results{SUF}.json"), "w"), indent=1, default=str)
P("\nfindings (negative answers):", RES["fails_findings"])
P("control failures:", CTRL if CTRL else "none")
OUTF.close()
sys.exit(1 if CTRL else 0)
