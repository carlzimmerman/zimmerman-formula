#!/usr/bin/env python3
"""CFG467: the alpha_c axis of the relativistic chassis (filtered C-H/K, beta = 0) and the sign tension.

Criteria: FROZEN_CRITERIA.md in this folder (committed alone before this script existed).

Every committed gate that depends on alpha_c is mapped onto the real alpha_c axis at each c_2 of CFG320's 9-point grid
(L340's window, leaf-average branch). Each gate carries a strict and a lenient allowed set (A), a shown-excluded set
(X), and the kind of evidence (PROOF / NUM / LIT / ARG). The sets are intersected with sympy; the verdict follows the
frozen rule:
  CONSISTENT    union over c_2 of I_strict non-empty;
  TENSION       I_strict empty everywhere, I_len non-empty somewhere;
  INCONSISTENT  I_len empty everywhere too.

Theory only, offline, no downloads; read-only on every source lane. kappa = 1/2 is FITTED and plays no role; a0 enters
no gate (both footings identical). Chassis only: candidate B has no action, so nothing here is computed for B.

Run from anywhere:
    python3 campaign_fresh_gravity/CFG467_alpha_c_sign_tension/cfg467_alpha_c_axis.py
    CFG467_MUTATE=1 python3 campaign_fresh_gravity/CFG467_alpha_c_sign_tension/cfg467_alpha_c_axis.py
"""
import os, sys, json, math, itertools, time
import numpy as np
import sympy as sp
import mpmath as mp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG467_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OUT_TXT = os.path.join(HERE, f"cfg467_alpha_c_axis{SUF}.out")
OUT_JSON = os.path.join(HERE, f"cfg467_results{SUF}.json")
mp.mp.dps = 50

LINES = []
def P(s=""):
    print(s); LINES.append(s)
def banner(s):
    P(""); P("=" * 118); P(s); P("=" * 118)

CHECKS = {}
def check(name, measured, ok, load_bearing=True, note=""):
    CHECKS[name] = {"ok": bool(ok), "measured": measured, "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reading)'} {name}")
    P(f"         measured: {measured}")
    if note:
        P(f"         note: {note}")

def rel(p):
    return os.path.join(REPO, p)
def load(p):
    with open(rel(p)) as f:
        return json.load(f)

# ------------------------------------------------------------------------------------------------ sources (read-only)
SRC = {
    "L340": "real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json",
    "XC1": "real_research/extra_crispy_2026/XC1_strong_coupling_chk_results.json",
    "CFG291": "campaign_fresh_gravity/CFG291_khronon_binary_pulsar/cfg291_khronon_binary_pulsar_results.json",
    "CFG292": "campaign_fresh_gravity/CFG292_khronon_strong_hyperbolicity/cfg292_khronon_strong_hyperbolicity_results.json",
    "CFG294": "campaign_fresh_gravity/CFG294_chassis_nonlinear_wellposedness/cfg294_chassis_nonlinear_wellposedness_results.json",
    "CFG311": "campaign_fresh_gravity/CFG311_ns_sensitivity/cfg311_ns_sensitivity_results.json",
    "CFG312": "campaign_fresh_gravity/CFG312_lapse_condition_W/cfg312_lapse_condition_W_results.json",
    "CFG318": "campaign_fresh_gravity/CFG318_strong_field_bh/cfg318_strong_field_bh_results.json",
    "CFG319": "campaign_fresh_gravity/CFG319_moving_black_hole/cfg319_moving_bh_results.json",
    "CFG320": "campaign_fresh_gravity/CFG320_radiative_stability_g12/cfg320_radiative_stability_results.json",
}
J = {k: load(v) for k, v in SRC.items()}

banner("CFG467  the alpha_c axis of the chassis (C-H/K, beta = 0)" + ("   *** MUTATE: G1's sign convention flipped ***" if MUTATE else ""))
P("Source verdicts as committed (read-only):")
for k in ("CFG291", "CFG292", "CFG294", "CFG311", "CFG312", "CFG318", "CFG319", "CFG320"):
    P(f"    {k:7s} {str(J[k].get('verdict'))[:110]}")

L340P1 = J["L340"]["numbers"]["P1"]
AC_MIN, AC_MAX = L340P1["alpha_c_min"], L340P1["alpha_c_max"]
C2_GRID = [float(c) for c in J["CFG320"]["numbers"]["inputs"]["c2_scored"]]
M_RED = 2.435e18                    # reduced Planck mass in GeV (XC1, CFG320)
LHC = 1.3e4                         # GeV (XC1 PROBES)
LAMBDA_HL_MAX = J["CFG320"]["numbers"]["summary"]["Lambda_HL_max_GeV"]
FOOTINGS = {"canonical": 9.3603e-11, "alt": 1.1312e-10}   # labels only: no gate takes a0 (K9)
P(f"L340 P1 window: alpha_c in [{AC_MIN:.4e}, {AC_MAX:.4e}], c_2 in [{L340P1['c2_min']:.4e}, {L340P1['c2_max']:.4e}]")
P("c_2 grid (CFG320 c2_scored): " + ", ".join(f"{c:.4e}" for c in C2_GRID))

a = sp.Symbol("alpha", real=True)
oo = sp.oo
def F(x, n=40):
    if isinstance(x, mp.mpf):
        return sp.Float(mp.nstr(x, n + 5), n)
    return sp.Float(x, n)
def R(x):
    return sp.Rational(repr(float(x)))

# ------------------------------------------------------------------------------------------------ set utilities
def mirror(S):
    """alpha -> -alpha on unions of intervals and finite sets."""
    if S is sp.S.EmptySet:
        return S
    if S == sp.S.Reals:
        return S
    if isinstance(S, sp.FiniteSet):
        return sp.FiniteSet(*[-x for x in S.args])
    if isinstance(S, sp.Interval):
        return sp.Interval(-S.end, -S.start, S.right_open, S.left_open)
    if isinstance(S, sp.Union):
        return sp.Union(*[mirror(x) for x in S.args])
    raise TypeError(f"mirror: unsupported set {S!r}")

def comp(S):
    return sp.Complement(sp.S.Reals, S)

def fmt(S):
    if S is sp.S.EmptySet:
        return "EMPTY"
    def g(x):
        if x in (oo, -oo):
            return "inf" if x == oo else "-inf"
        xv = float(x)
        return "0" if xv == 0 else (f"{xv:.6g}" if (abs(xv) >= 1e-3 and abs(xv) < 1e4) else f"{xv:.4e}")
    if isinstance(S, sp.FiniteSet):
        return "{" + ", ".join(g(x) for x in S.args) + "}"
    if isinstance(S, sp.Interval):
        return ("(" if S.left_open else "[") + g(S.start) + ", " + g(S.end) + (")" if S.right_open else "]")
    if isinstance(S, sp.Union):
        parts = sorted(S.args, key=lambda s: float(s.inf) if s.inf not in (-oo, oo) else (-1e300 if s.inf == -oo else 1e300))
        return " U ".join(fmt(x) for x in parts)
    if S == sp.S.Reals:
        return "(-inf, inf)"
    return str(S)

def setjson(S):
    return fmt(S)

def bisect(fun, lo, hi, it=200):
    """fun(lo) False, fun(hi) True, monotone; returns the threshold (mpmath)."""
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    assert (not fun(lo)) and fun(hi), "bisect: bracket"
    for _ in range(it):
        mid = mp.sqrt(lo * hi) if lo > 0 else (lo + hi) / 2
        if fun(mid):
            hi = mid
        else:
            lo = mid
        if hi - lo <= abs(hi) * mp.mpf("1e-30"):
            break
    return hi

# ================================================================================================ K7 set engine
banner("K7  the set engine on toy sets")
t1 = sp.Intersection(sp.Interval.open(0, 1), sp.FiniteSet(0))
t2 = sp.Intersection(sp.Interval.open(0, 1), sp.Interval(sp.Rational(1, 2), 2))
t3 = sp.Intersection(sp.Union(sp.Interval.open(0, sp.Rational(1, 2)), sp.Interval.open(sp.Rational(1, 2), 2)),
                     sp.Interval(sp.Rational(1, 2), 1))
okK7 = (t1 is sp.S.EmptySet and t2 == sp.Interval.Ropen(sp.Rational(1, 2), 1) and t3 == sp.Interval.Lopen(sp.Rational(1, 2), 1)
        and mirror(sp.Interval.Lopen(1, 2)) == sp.Interval.Ropen(-2, -1))
check("K7 toy intersections: (0,1) n {0} = EMPTY; (0,1) n [1/2,2] = [1/2,1); ((0,1/2) U (1/2,2)) n [1/2,1] = (1/2,1]; "
      "mirror((1,2]) = [-2,-1)", f"{fmt(t1)}; {fmt(t2)}; {fmt(t3)}", okK7)

# ================================================================================================ G1 hyperbolicity
banner("G1  strong hyperbolicity + criterion B in F2a (CFG292 T1/COND; CFG294 S1; XC2 B6)  [PROOF, linear principal symbol]")
k_, lam_, al_, be_, c2_ = sp.symbols("k lam alpha beta c_2")
poly_str = J["CFG292"]["numbers"]["T1"]["F2a"]["scalar"].replace("lambda", "lam")
scal = sp.sympify(poly_str, locals={"k": k_, "lam": lam_, "alpha": al_, "beta": be_, "c_2": c2_})
lapse_str = J["CFG292"]["numbers"]["COND"]["F2a"]["lapse_coeff"]
lapse_coeff = sp.sympify(lapse_str, locals={"alpha": al_})
scal0 = sp.factor(scal.subs(be_, 0))
P(f"    committed F2a scalar characteristic polynomial at beta = 0: {scal0}")
# remove the gauge/constraint factors k^2 (k - lam)^2 (k + lam)^2 and read the physical scalar factor
Q = sp.cancel(scal0 / (k_**2 * (k_ - lam_)**2 * (k_ + lam_)**2))
Qp = sp.Poly(sp.expand(Q), lam_)
assert Qp.degree() == 2 and Qp.coeff_monomial(lam_) == 0, "Q is not of the form A lam^2 + B"
cs2_expr = sp.factor(-Qp.coeff_monomial(1) / (Qp.coeff_monomial(lam_**2) * k_**2))
P(f"    physical scalar factor Q = {sp.factor(Q)};  lam^2/k^2 = c_S^2 = {cs2_expr}")
P(f"    committed F2a lapse coefficient: {lapse_coeff}  (zero at alpha = {sp.solve(lapse_coeff, al_)})")
cs2_target = c2_ * (2 - al_) / (al_ * (2 + 3 * c2_))
okcs = sp.simplify(cs2_expr - cs2_target) == 0

def g1_sets(c2v):
    """Derived from the committed polynomial: real non-zero speeds iff c_S^2 in (0, inf)."""
    expr = cs2_expr.subs({c2_: R(c2v), al_: a})
    good = sp.solve_univariate_inequality(expr > 0, a, relational=False)
    half = sp.FiniteSet(*[sp.nsimplify(s) for s in sp.solve(lapse_coeff, al_)])
    A_len = good
    A_str = sp.Complement(good, half)
    return A_str, A_len, good

g1_derived = {}
okK1 = okcs and sp.solve(lapse_coeff, al_) == [sp.Rational(1, 2)]
for c2v in C2_GRID:
    A_str, A_len, good = g1_sets(c2v)
    g1_derived[c2v] = (A_str, A_len)
    okK1 = okK1 and (good == sp.Interval.open(0, 2))
P(f"    derived at every grid c_2: c_S^2 > 0 iff alpha in {fmt(g1_derived[C2_GRID[0]][1])}; strict set {fmt(g1_derived[C2_GRID[0]][0])}")
P("    alpha = 1/2: F2a gauge artefact (physical lapse coefficient alpha/2 != 0, CFG294 S1 table) -> lenient keeps it")

def gate_G1(c2v):
    A_str, A_len = g1_derived[c2v]
    X = sp.Union(sp.Interval(-oo, 0), sp.Interval(2, oo))
    Xs = sp.Union(X, sp.FiniteSet(sp.Rational(1, 2)))
    G = dict(A_str=A_str, A_len=A_len, X_str=Xs, X_len=X)
    if MUTATE:   # flip the sign convention of this ONE gate
        G = {k2: mirror(v) for k2, v in G.items()}
    return G

g1_used = gate_G1(C2_GRID[0])
okK1_used = okK1 and g1_used["A_len"] == sp.Interval.open(0, 2) and g1_used["A_str"] == sp.Union(
    sp.Interval.open(0, sp.Rational(1, 2)), sp.Interval.open(sp.Rational(1, 2), 2))
check("K1 G1's sets agree with CFG292's committed F2a scalar polynomial (c_S^2 = c_2(2-alpha)/(alpha(2+3c_2)) > 0 iff "
      "0 < alpha < 2 at every grid c_2 > 0) and its lapse coefficient (2 alpha - 1)/4 (zero only at 1/2)",
      f"c_S^2 reproduced: {okcs}; sets used by the gate: A_len {fmt(g1_used['A_len'])}, A_str {fmt(g1_used['A_str'])}",
      okK1_used, note="MUTATE flips this gate's sign convention, so K1 must FAIL there" if MUTATE else "")

# ================================================================================================ G2 lapse/U ellipticity
banner("G2  lapse/U leaf system: ellipticity (CFG294 S4b, joint det 4 N alpha k^4) and UV positivity (CFG329)  [PROOF]")
Cs, Nn, kk = sp.symbols("C N k", positive=True)
coef329 = (2 * Cs + al_ * (1 + Cs)) / (1 + Cs)
uv = sp.limit(coef329, Cs, 0)
g2_pos = sp.solve_univariate_inequality(uv.subs(al_, a) > 0, a, relational=False)
det_joint = 4 * Nn * al_ * kk**4
g2_ell = sp.Complement(sp.S.Reals, sp.FiniteSet(*sp.solve(det_joint, al_)))
P(f"    CFG329 lapse coefficient (2C + alpha(1+C))/(1+C) -> {uv} as C -> 0 (the heat filter removes C at k >> 1/xi, XC1 A3)")
P(f"    positivity set {fmt(g2_pos)};  joint-system ellipticity set {fmt(g2_ell)};  "
  f"low-k (C > 0) reading: positive for alpha > -2C/(1+C)")
G2 = dict(A_str=sp.Intersection(g2_pos, g2_ell), A_len=sp.Intersection(g2_pos, g2_ell), X_str=sp.Interval(-oo, 0),
          X_len=sp.Interval(-oo, 0))
P(f"    G2: A = {fmt(G2['A_str'])}, X = {fmt(G2['X_str'])}")

# ================================================================================================ G3 F2a kernel
banner("G3  F2a lapse kernel with W <= 0, W != 0 (CFG294 S4c; CFG312 Hardy factor 1/2 - alpha)  [PROOF, homogeneous class]")
Kq, Wn = sp.symbols("K W_abs", positive=True)        # K = |k|^2 >= 0, W = -W_abs < 0
h_f2a = (al_ - sp.Rational(1, 2)) * Kq - Wn
root = sp.solve(sp.Eq(h_f2a, 0), Kq)[0]              # = W_abs/(alpha - 1/2)
res_set = sp.solve_univariate_inequality((root > 0).subs(Wn, 1).subs(al_, a), a, relational=False)
P(f"    h_F2a(K) = (alpha - 1/2) K + W, W < 0: zero at K* = {root}; K* > 0 (a resonance, non-trivial kernel) iff alpha in "
  f"{fmt(res_set)}; at alpha = 1/2 the k^2 term vanishes (not elliptic)")
X3 = sp.Union(sp.Interval(sp.Rational(1, 2), oo), sp.FiniteSet(0))
G3 = dict(A_str=comp(X3), A_len=comp(X3), X_str=X3, X_len=X3)
P(f"    G3: A = {fmt(G3['A_str'])}, X = {fmt(G3['X_str'])}  (alpha = 0 is excluded through CFG294's joint ellipticity)")
okG3 = res_set == sp.Interval.open(sp.Rational(1, 2), oo)
h_phys = al_ * Kq - Wn
res_phys = sp.solve_univariate_inequality((sp.solve(sp.Eq(h_phys, 0), Kq)[0] > 0).subs(Wn, 1).subs(al_, a), a, relational=False)
P(f"    reading r1 (not scored): CFG294's physical velocity-fixed form alpha K + W has a resonance K* = W_abs/alpha > 0 for "
  f"alpha in {fmt(res_phys)}; it is resonance-free with W < 0 only for alpha <= 0. CFG294 records this resonance and "
  f"states that F2a, the operator the scheme inverts, has none.")

# ================================================================================================ G4 strong coupling
banner("G4  strong coupling G8 (XC1 A4; Guemruekcueoglu, Saravani & Sotiriou 2018 eq. 15)  [NUM from LIT formula, tree level]")
def cs2_bps(al, c2):
    return c2 * (2 - al) / (al * (2 + 3 * c2))
def k_sc(al, c2):
    al = mp.mpf(al); c2 = mp.mpf(c2)
    if al <= 0 or al >= 2:
        return mp.mpf(0)
    cs = mp.sqrt(cs2_bps(al, c2))
    return mp.sqrt(al) * M_RED * (cs**mp.mpf(1.5) if cs < 1 else cs**mp.mpf(-0.5))

def g4_interval(c2, thr):
    acr = mp.mpf(c2) / (1 + 2 * mp.mpf(c2))          # c_s = 1: the maximum of k_sc in alpha
    lo = bisect(lambda x: k_sc(x, c2) >= thr, mp.mpf("1e-60"), acr)
    # upper root: k_sc decreases on (acr, 2); find the largest alpha with k_sc >= thr
    f_hi = lambda x: k_sc(x, c2) < thr
    l2, h2 = acr, mp.mpf(2)
    for _ in range(400):
        mid = (l2 + h2) / 2
        if f_hi(mid):
            h2 = mid
        else:
            l2 = mid
    return lo, l2

G4c = {}
for c2v in C2_GRID:
    lo_s, hi_s = g4_interval(c2v, 1e3 * LHC)
    lo_l, hi_l = g4_interval(c2v, LHC)
    A_s = sp.Interval(F(lo_s), F(hi_s)); A_l = sp.Interval(F(lo_l), F(hi_l))
    G4c[c2v] = dict(A_str=A_s, A_len=A_l, X_str=comp(A_s), X_len=comp(A_l))
P(f"    k_sc(alpha <= 0) = 0 by XC1's definition (no UV kinetic term): alpha <= 0 is strongly coupled at every scale")
for c2v in (C2_GRID[0], C2_GRID[4], C2_GRID[-1]):
    P(f"    c_2 {c2v:.4e}: strict (>= 1e3 x LHC) A = {fmt(G4c[c2v]['A_str'])};  lenient (>= LHC) A = {fmt(G4c[c2v]['A_len'])};"
      f"  upper edges 2 - {float(2 - G4c[c2v]['A_str'].end):.3e} / 2 - {float(2 - G4c[c2v]['A_len'].end):.3e} (c_s -> 0 as alpha -> 2)")
kxc = float(k_sc(J["XC1"]["numbers"]["A4"]["worst"]["alpha_c"], J["XC1"]["numbers"]["A4"]["worst"]["c2"]))
kxc_c = J["XC1"]["numbers"]["A4"]["min_k_sc_GeV"]
check("K2 the G4 formula reproduces XC1's committed minimum k_sc at its worst point to 1e-6 relative",
      f"{kxc:.6e} vs {kxc_c:.6e} GeV (rel {abs(kxc / kxc_c - 1):.1e})", abs(kxc / kxc_c - 1) < 1e-6)

# ================================================================================================ G5 negative lobes
banner("G5  negative-phantom-lobe health (L340 H4)  [PROOF that alpha <= 0 fails; NUM edge]")
Gn, cc, Msun, PCm = 6.6743e-11, 2.99792458e8, 1.98892e30, 3.0857e16
C2V_L340 = 1.0e-2
LOBES = {"Solar nbhd lobe": (-0.01, 0.157, 0.045, 0.03), "galaxy-in-group lobe": (-0.05, 0.3, 4.0, 50.0),
         "cluster-outskirt lobe": (-1e-4, 1.0, 50.0, 3e5), "galaxy transition (rho > 0)": (0.05, 0.3, 4.0, 1000.0)}
def lobe_eval(nm, acv, c2v):
    rho_pc3, C0, xi_pc, L_pc = LOBES[nm]
    rho = rho_pc3 * Msun / PCm**3; lam0 = 16 * math.pi * Gn * rho / cc**2; xi = xi_pc * PCm; L = L_pc * PCm
    ks = np.logspace(math.log10(2 * math.pi / L), math.log10(1e3 / xi), 4000)
    bb = xi**2 / 2
    inertia = 2 * ks**2 * C0 * np.exp(-(xi * ks)**2) / (1 + C0) + acv * ks**2 + lam0 * (0.5 - np.exp(-bb * ks**2))
    restoring = lam0 / 2 * ks**2 + c2v * ks**4
    with np.errstate(divide="ignore", invalid="ignore"):
        w2 = restoring / np.where(inertia != 0, inertia, np.nan)
    return bool((inertia > 0).all()), bool((w2 > 0).all()), lam0, float(inertia[-1])
okK3 = True; rep = []
for nm in LOBES:
    for acv, key in ((0.0, "alpha_c=0"), (1e-9, "alpha_c=1e-9")):
        r_ = lobe_eval(nm, acv, C2V_L340)
        com = J["L340"]["numbers"]["H4"][nm][key]
        okK3 = okK3 and [r_[0], r_[1]] == list(com)
        rep.append(f"{nm[:14]} a={acv:g}: {r_[0], r_[1]} vs {tuple(com)}")
    if J["L340"]["numbers"]["H4"][nm]["lam0_m-2"] < 0:
        for acv in (0.0, -1e-20):
            okK3 = okK3 and lobe_eval(nm, acv, C2V_L340)[3] < 0
P("    " + "; ".join(rep))
check("K3 the re-implemented L340 symbol reproduces the committed H4 booleans (alpha = 0, 1e-9; four lobes), and in every "
      "negative lobe the inertia at the grid's top k is negative for alpha = 0 and alpha = -1e-20",
      "all match" if okK3 else "MISMATCH", okK3,
      note="large-k limit: inertia -> alpha k^2 + lambda0/2 with lambda0 < 0, so alpha <= 0 fails in every negative lobe (proof)")
alpha_bis = {}
for c2v in C2_GRID:
    th = []
    for nm in LOBES:
        if J["L340"]["numbers"]["H4"][nm]["lam0_m-2"] >= 0:
            continue
        f_ok = lambda x, nm=nm: all(lobe_eval(nm, float(x), c2v)[:2])
        th.append(float(bisect(f_ok, mp.mpf("1e-30"), mp.mpf("1e-9"), it=120)))
    alpha_bis[c2v] = max(th)
lobe_thr = {}
for nm in LOBES:
    if J["L340"]["numbers"]["H4"][nm]["lam0_m-2"] < 0:
        lobe_thr[nm] = float(bisect(lambda x, nm=nm: all(lobe_eval(nm, float(x), C2V_L340)[:2]), mp.mpf("1e-30"), mp.mpf("1e-9"), it=120))
P("    bisected thresholds on L340's k grid (c_2 = 1e-2): " + "; ".join(f"{k2}: {v:.4e} (L340 estimate "
  f"{J['L340']['numbers']['H4'][k2]['alpha_min']:.4e})" for k2, v in lobe_thr.items()))
P(f"    binding lobe threshold over the c_2 grid: {min(alpha_bis.values()):.4e} .. {max(alpha_bis.values()):.4e} "
  f"(record edge {AC_MIN:.4e} is the estimate |lambda0| xi^2/20)")
def gate_G5(c2v):
    ab = F(alpha_bis[c2v])
    return dict(A_str=sp.Interval(F(AC_MIN), oo), A_len=sp.Interval(ab, oo), X_str=sp.Interval.open(-oo, ab),
                X_len=sp.Interval.open(-oo, ab))

# ================================================================================================ G6, G7 PPN
banner("G6/G7  PPN alpha2 and alpha1 (exact khronometric formulas at beta = 0; L340 P1, CFG291)  [LIT, provisional]")
lam_s = sp.Symbol("lam", positive=True)
alpha2_expr = -al_ * (2 * al_ * lam_s + al_ - lam_s) / (lam_s * (al_ - 2))
alpha1_expr = -4 * al_
f2 = sp.lambdify((al_, lam_s), alpha2_expr, "mpmath")
okK4 = True; rep = []
for key, v in J["CFG291"]["numbers"]["PPN"]["corners"].items():
    acs = AC_MIN if key.startswith("alpha_c=9.62") else AC_MAX
    c2s = L340P1["c2_min"] if "7.289e-03" in key else L340P1["c2_max"]
    a2 = float(f2(mp.mpf(acs), mp.mpf(c2s))); a1 = -4 * acs
    okK4 = okK4 and abs(a2 / v["alpha2"] - 1) < 1e-6 and abs(a1 / v["alpha1"] - 1) < 1e-6
    rep.append(f"{key}: a1 {a1:.4e}/{v['alpha1']:.4e}, a2 {a2:.6e}/{v['alpha2']:.6e}")
P("    " + "; ".join(rep))
check("K4 the G6/G7 formulas reproduce CFG291's committed PPN corners to 1e-6 relative", "match" if okK4 else "MISMATCH", okK4)

def ppn2_set(c2v, B):
    lv = R(c2v); Bv = R(B)
    e = alpha2_expr.subs({lam_s: lv, al_: a})
    s1 = sp.solve_univariate_inequality(e <= Bv, a, relational=False)
    s2 = sp.solve_univariate_inequality(e >= -Bv, a, relational=False)
    S = sp.Intersection(s1, s2)
    # endpoints to 40-digit floats (algebraic numbers otherwise slow the intersections)
    def tofl(X):
        if isinstance(X, sp.Interval):
            return sp.Interval(F(sp.N(X.start, 45)) if X.start not in (-oo, oo) else X.start,
                               F(sp.N(X.end, 45)) if X.end not in (-oo, oo) else X.end, X.left_open, X.right_open)
        if isinstance(X, sp.Union):
            return sp.Union(*[tofl(y) for y in X.args])
        if isinstance(X, sp.FiniteSet):
            return sp.FiniteSet(*[F(sp.N(y, 45)) for y in X.args])
        return X
    return tofl(S)

G6c, G7 = {}, None
for c2v in C2_GRID:
    As = ppn2_set(c2v, 1.6e-9); Al = ppn2_set(c2v, 2.4e-7)
    G6c[c2v] = dict(A_str=As, A_len=Al, X_str=comp(As), X_len=comp(Al))
for c2v in (C2_GRID[0], C2_GRID[-1]):
    P(f"    c_2 {c2v:.4e}: |alpha2| <= 1.6e-9 -> {fmt(G6c[c2v]['A_str'])}")
    P(f"                    |alpha2| <= 2.4e-7 -> {fmt(G6c[c2v]['A_len'])}")
P("    the second island sits at alpha = c_2/(1 + 2 c_2), where c_S = 1 and alpha2 vanishes again; alpha1 excludes it (G7)")
A7s = sp.Interval(F(-1.1e-5 / 4), F(1.1e-5 / 4)); A7l = sp.Interval.open(F(-3.3e-5 / 4), F(3.5e-5 / 4))
G7 = dict(A_str=A7s, A_len=A7l, X_str=comp(A7s), X_len=comp(A7l))
P(f"    G7: alpha1 = -4 alpha; strict |alpha1| <= 1.1e-5 -> {fmt(A7s)}; lenient -3.5e-5 < alpha1 < 3.3e-5 -> {fmt(A7l)}")

# ================================================================================================ G8 pulsars
banner("G8  binary-pulsar dipole (CFG291 + CFG311)  [NUM with LIT formulas]")
G8 = dict(A_str=sp.Interval(F(AC_MIN), F(AC_MAX)), A_len=sp.Interval.Lopen(0, F(AC_MAX)), X_str=sp.S.EmptySet,
          X_len=sp.S.EmptySet)
P(f"    tested pass on {fmt(G8['A_str'])} (CFG291 625/625 under B0-B2; CFG311 PASS at its scope, margin >= 4.9e5);"
  f" lenient {fmt(G8['A_len'])} via CFG291 C6 (flux -> 0 monotonically as alpha -> 0+); alpha <= 0 and alpha > 3.2e-9: untested")

# ================================================================================================ G9, G10
banner("G9/G10  cosmological G / BBN (L350 G1, G5) and G_N > 0  [PROOF formula + LIT bound; PROOF]")
A9 = sp.Interval.open(F(-0.2), F(0.2))
G9 = dict(A_str=A9, A_len=A9, X_str=comp(A9), X_len=comp(A9))
G10 = dict(A_str=sp.Interval.open(-oo, 2), A_len=sp.Interval.open(-oo, 2), X_str=sp.Interval(2, oo), X_len=sp.Interval(2, oo))
P(f"    G9 leaf-average branch |G_cos/G_N - 1| = |alpha|/2 < 0.1 -> {fmt(A9)};  G10 G_N = G/(1 - alpha/2) > 0 -> {fmt(G10['A_str'])}")
plain = {}
for c2v in (C2_GRID[0], C2_GRID[-1]):
    lo = 2 - 2.2 * (1 + 1.5 * c2v); hi = 2 - 1.8 * (1 + 1.5 * c2v)
    plain[c2v] = (lo, hi)
    P(f"    reading r3 (plain branch, (2 - alpha)/(2 + 3 c_2) within 10% of 1) at c_2 {c2v:.4e}: alpha in ({lo:.4f}, {hi:.4f})")

# ================================================================================================ G11 radiative stability
banner("G11  radiative stability G12 (CFG320)  [NUM + LIT, provisional]")
def lam_sc(al, c2):
    al = mp.mpf(al); c2 = mp.mpf(c2)
    return mp.sqrt(al) * M_RED * mp.sqrt(cs2_bps(al, c2))**mp.mpf(-0.5)
Ls = J["CFG320"]["numbers"]["summary"]
lmin = float(lam_sc(AC_MIN, L340P1["c2_max"])); lmax = float(lam_sc(AC_MAX, L340P1["c2_min"]))
alpha_grid320 = sorted(set(g["alpha_c"] for g in J["CFG320"]["numbers"]["grid"]))
sub = [(al, c2) for al in alpha_grid320 for c2 in C2_GRID if lam_sc(al, c2) <= LAMBDA_HL_MAX]
sub_c = [(d["alpha_c"], d["c2"]) for d in J["CFG320"]["numbers"]["UV_subwindow"]]
okK5 = (abs(lmin / Ls["Lambda_sc_min"] - 1) < 1e-6 and abs(lmax / Ls["Lambda_sc_max"] - 1) < 1e-6 and len(sub) == len(sub_c) == 3
        and all(abs(x[0] / y[0] - 1) < 1e-9 and abs(x[1] / y[1] - 1) < 1e-9 for x, y in zip(sorted(sub), sorted(sub_c))))
check("K5 Lambda_sc reproduces CFG320's committed min/max to 1e-6 and its no-hierarchy sub-window holds exactly CFG320's "
      "3 committed grid points", f"min {lmin:.6e}/{Ls['Lambda_sc_min']:.6e}, max {lmax:.6e}/{Ls['Lambda_sc_max']:.6e}; "
      f"sub-window points {len(sub)}: " + ", ".join(f"({x:.3e}, {y:.4f})" for x, y in sorted(sub)), okK5)
alpha_rs = {}
G11c = {}
for c2v in C2_GRID:
    ars = bisect(lambda x: lam_sc(x, c2v) > LAMBDA_HL_MAX, mp.mpf("1e-30"), mp.mpf("1e-6"))   # first alpha with Lambda_sc > cap
    alpha_rs[c2v] = float(ars)
    win = sp.Interval(F(AC_MIN), F(AC_MAX))
    A_s = sp.Intersection(win, sp.Interval(-oo, F(ars)))
    X_s = sp.Intersection(win, sp.Interval.Lopen(F(ars), oo))
    G11c[c2v] = dict(A_str=A_s, A_len=win, X_str=X_s, X_len=sp.S.EmptySet)
P(f"    Lambda_HL_max (CFG320) = {LAMBDA_HL_MAX:.4e} GeV; alpha_rs(c_2) where Lambda_sc = cap: " +
  ", ".join(f"{c:.3e}: {alpha_rs[c]:.4e}" for c in C2_GRID))
P(f"    strict (no hierarchy) A non-empty for c_2 >= {min([c for c in C2_GRID if alpha_rs[c] >= AC_MIN] or [float('nan')]):.4e}"
  f" on the grid; lenient (M_* <= 9.9e8 GeV granted) A = {fmt(sp.Interval(F(AC_MIN), F(AC_MAX)))}")

# ================================================================================================ G12 black holes
banner("G12  black-hole regularity G11 (CFG318, CFG319; RB2019, FHB2021; Kovachik-Sibiryakov provisional)  [NUM + ARG + LIT]")
vi = J["CFG319"]["numbers"]["verdict_inputs"]; runs = J["CFG319"]["numbers"]["runs"]
w5 = sorted(float(v["alpha"]) for k2, v in runs.items() if k2.startswith("W5"))
ladder = sorted(float(v["alpha"]) for k2, v in runs.items() if k2.startswith("ladder"))
okK6 = (all(x is False for x in vi["full_regular"]) and all(x is True for x in vi["optC_admissible"])
        and J["CFG319"]["checks"][[c for c in J["CFG319"]["checks"] if c.startswith("C1")][0]]["ok"] and len(w5) == 5
        and abs(min(w5) / AC_MIN - 1) < 1e-12)
check("K6 CFG319's committed JSON: no fully regular moving BH at the five window points, option C admissible at all five, "
      "the alpha = 0 stealth control C1 passed; window and ladder alphas read from numbers.runs",
      f"full_regular {vi['full_regular']}; optC_admissible {vi['optC_admissible']}; W5 alphas {[f'{x:.3e}' for x in w5]}; "
      f"ladder {[f'{x:.0e}' for x in ladder]} (c_2 = 0.05)", okK6)
S22s = J["CFG319"]["numbers"]["symbolic"]["S22"]
Wy, Yy, lam2, bet2 = sp.symbols("W Y lambda beta", real=True)
S22 = sp.sympify(S22s.replace("lambda", "lam_x"), locals={"W": Wy, "Y": Yy, "alpha": al_, "beta": bet2, "lam_x": lam2})
num = sp.numer(sp.factor(S22)).subs(bet2, 0)
neg_alpha = sp.Symbol("n", positive=True); lpos = sp.Symbol("l", positive=True)
num_neg = sp.expand(num.subs({al_: -neg_alpha, lam2: lpos}))
P(f"    CFG319 S22 numerator at beta = 0: {sp.factor(num)}; with alpha = -n < 0, lambda = l > 0: {sp.factor(num_neg)}")
P("    reading r2 (not scored): for alpha < 0 the bracket -(n W^2 + l Y^2) never vanishes, so there is no spin-0 horizon and")
P("    CFG319's r_S condition drops out of the count (4 constants vs 4 conditions). Existence is NOT computed; alpha < 0 is U.")
A12s = sp.FiniteSet(0)
A12l = sp.Union(sp.FiniteSet(0), sp.Interval(F(min(w5)), F(max(ladder))))
G12 = dict(A_str=A12s, A_len=A12l, X_str=sp.Interval.open(0, oo), X_len=sp.S.EmptySet)
P(f"    G12 strict (reading S): A = {fmt(A12s)}, X = {fmt(G12['X_str'])} (count over-determined by one for every alpha > 0,")
P(f"      test-khronon limit; numerically at the 5 window points and the ladder)")
P(f"    G12 lenient (reading W, option C accepted): A = {fmt(A12l)}")

# ================================================================================================ assemble
GATE_INFO = {
    "G1": ("strong hyperbolicity + criterion B (F2a)", "CFG292, CFG294 S1, XC2 B6", "PROOF (linear principal symbol)"),
    "G2": ("lapse/U ellipticity + UV positivity", "CFG294 S4b, CFG329", "PROOF"),
    "G3": ("F2a lapse kernel with W <= 0", "CFG294 S4c, CFG312", "PROOF (homogeneous class; Hardy sufficient)"),
    "G4": ("strong coupling G8", "XC1 A4 (GSS2018 eq. 15)", "NUM from LIT formula (tree level)"),
    "G5": ("negative-lobe health", "L340 H4", "PROOF alpha<=0 fails; NUM edge"),
    "G6": ("PPN alpha2", "L340 P1, CFG291 (Shao+2013)", "LIT (provisional)"),
    "G7": ("PPN alpha1", "CFG291, L340 P1", "LIT (provisional)"),
    "G8": ("binary-pulsar dipole", "CFG291, CFG311", "NUM with LIT formulas"),
    "G9": ("cosmological G / BBN", "L350 G1, G5", "PROOF formula + LIT bound"),
    "G10": ("G_N > 0", "L350 G1, CFG320 K4", "PROOF"),
    "G11": ("radiative stability G12", "CFG320", "NUM + LIT (provisional)"),
    "G12": ("black-hole regularity G11", "CFG318, CFG319 (+RB2019, FHB2021)", "NUM + ARG (count) + LIT"),
}
GIDS = list(GATE_INFO)

def build_gates(c2v, footing="canonical", flip_all=False):
    _ = FOOTINGS[footing]           # a0 label only: no gate below takes it (K9)
    G = {"G1": gate_G1(c2v), "G2": G2, "G3": G3, "G4": G4c[c2v], "G5": gate_G5(c2v), "G6": G6c[c2v], "G7": G7,
         "G8": G8, "G9": G9, "G10": G10, "G11": G11c[c2v], "G12": G12}
    if flip_all:
        G = {g: {k2: mirror(v) for k2, v in d.items()} for g, d in G.items()}
    return G

def intersect_cfg(G, lenient_set):
    sets = [G[g]["A_len"] if g in lenient_set else G[g]["A_str"] for g in GIDS]
    return sp.Intersection(*sets)

def nx(G):
    return sp.Intersection(*[comp(G[g]["X_str"]) for g in GIDS])

ALL = set(GIDS)
RELAXABLE = [g for g in GIDS if any(build_gates(c)[g]["A_str"] != build_gates(c)[g]["A_len"] for c in C2_GRID)]

banner("THE INTERVAL TABLE (strict A / lenient A / shown-excluded X), per gate, at c_2 min / max")
TABLE = {}
for g in GIDS:
    nm, src, kind = GATE_INFO[g]
    rows = {}
    for c2v in (C2_GRID[0], C2_GRID[-1]):
        Gx = build_gates(c2v)[g]
        rows[f"{c2v:.4e}"] = {"A_str": fmt(Gx["A_str"]), "A_len": fmt(Gx["A_len"]), "X_str": fmt(Gx["X_str"])}
    TABLE[g] = {"gate": nm, "source": src, "kind": kind, "by_c2": rows}
    P(f"  {g:4s} {nm}  [{src}; {kind}]")
    for c2s, r_ in rows.items():
        P(f"        c_2 {c2s}: strict A {r_['A_str']}")
        P(f"                       lenient A {r_['A_len']}")
        P(f"                       X {r_['X_str']}")
P(f"  relaxable gates (strict != lenient somewhere): {RELAXABLE}")

banner("INTERSECTIONS per c_2")
PER_C2 = {}
U_str, U_len, U_nx, U_S = [], [], [], []
for c2v in C2_GRID:
    G = build_gates(c2v)
    Is = intersect_cfg(G, set()); Il = intersect_cfg(G, ALL); Nx = nx(G); IS = intersect_cfg(G, ALL - {"G12"})
    PER_C2[f"{c2v:.4e}"] = {"I_strict": fmt(Is), "I_len": fmt(Il), "NX": fmt(Nx), "I_len_but_G12_strict": fmt(IS)}
    U_str.append(Is); U_len.append(Il); U_nx.append(Nx); U_S.append(IS)
    P(f"  c_2 {c2v:.4e}:  I_strict {fmt(Is):28s} I_len {fmt(Il):28s} NX {fmt(Nx):10s} I_len with G12 strict {fmt(IS)}")
Ustr = sp.Union(*U_str); Ulen = sp.Union(*U_len); Unx = sp.Union(*U_nx); US = sp.Union(*U_S)
P(f"  union over c_2:  I_strict {fmt(Ustr)};  I_len {fmt(Ulen)};  NX {fmt(Unx)};  I_len with G12 strict {fmt(US)}")

def binding(Iset, cfg_len, c2v):
    """gates whose allowed set (in the given configuration) ends at each edge of Iset (component-wise)."""
    if Iset is sp.S.EmptySet:
        return {}
    G = build_gates(c2v); out = {}
    comps = Iset.args if isinstance(Iset, sp.Union) else (Iset,)
    for cp in comps:
        if isinstance(cp, sp.FiniteSet):
            continue
        for side, e in (("lower", cp.start), ("upper", cp.end)):
            if e in (oo, -oo):
                continue
            ev = float(e); d = abs(ev) * 1e-9 if ev != 0 else 1e-30
            probe = F(ev - d) if side == "lower" else F(ev + d)
            gs = [g for g in GIDS if (G[g]["A_len"] if g in cfg_len else G[g]["A_str"]).contains(probe) != sp.true]
            out[f"{side} {fmt(sp.FiniteSet(e))}"] = gs
    return out

BIND = {"I_len": {f"{c:.4e}": binding(intersect_cfg(build_gates(c), ALL), ALL, c) for c in (C2_GRID[0], C2_GRID[-1])},
        "relax_G12_only": {f"{c:.4e}": binding(intersect_cfg(build_gates(c), {"G12"}), {"G12"}, c) for c in (C2_GRID[-1],)}}
P("  binding gates at the edges (a point 1e-9 outside the edge is not allowed by):")
for k2, v in BIND.items():
    for c2s, d in v.items():
        P(f"    {k2} at c_2 {c2s}: " + "; ".join(f"{e}: {','.join(gs)}" for e, gs in d.items()))

def verdict_of(us, ul):
    if us is not sp.S.EmptySet:
        return "CONSISTENT"
    if ul is not sp.S.EmptySet:
        return "TENSION"
    return "INCONSISTENT"
VERDICT = verdict_of(Ustr, Ulen)

banner("WHO EXCLUDES WHAT (strict sets; 'X' = shown excluded, 'not-A' = not shown allowed)")
PROBES = [-1e-9, 0.0, 1e-15, 1e-13, 1e-11, 3e-9, 1e-6, 0.1, 0.5, 1.0]
WHO = {}
for c2v in (C2_GRID[0], C2_GRID[4], C2_GRID[-1]):
    G = build_gates(c2v); wrow = {}
    for pa in PROBES:
        xv = sp.Float(pa) if pa != 0 else sp.Integer(0)
        exc = [g for g in GIDS if G[g]["X_str"].contains(xv) == sp.true]
        nota = [g for g in GIDS if G[g]["A_str"].contains(xv) != sp.true and g not in exc]
        wrow[f"{pa:g}"] = {"X": exc, "not_A_only": nota}
    WHO[f"{c2v:.4e}"] = wrow
    P(f"  c_2 {c2v:.4e}:")
    for pa, d in wrow.items():
        P(f"     alpha {pa:>7s}: X by {','.join(d['X']) or '-':34s} not shown allowed by {','.join(d['not_A_only']) or '-'}")

banner("MINIMAL RELAXATIONS that open the intersection (all subsets of the relaxable gates)")
opening = []
for r in range(len(RELAXABLE) + 1):
    for sub in itertools.combinations(RELAXABLE, r):
        s = set(sub)
        if any(t <= s for t in opening):
            continue
        U = sp.Union(*[intersect_cfg(build_gates(c), s) for c in C2_GRID])
        if U is not sp.S.EmptySet:
            opening.append(s)
MIN_OPEN = [sorted(s, key=GIDS.index) for s in opening]
for s in MIN_OPEN:
    U = sp.Union(*[intersect_cfg(build_gates(c), set(s)) for c in C2_GRID])
    P(f"  relax {s}: opens {fmt(U)}")
if not MIN_OPEN:
    P("  none: no combination of the stated relaxations opens the intersection")
single = {}
for g in RELAXABLE:
    U = sp.Union(*[intersect_cfg(build_gates(c), {g}) for c in C2_GRID])
    single[g] = fmt(U)
P("  single relaxations: " + "; ".join(f"{g}: {v}" for g, v in single.items()))
g12_only_byc2 = {f"{c:.4e}": fmt(intersect_cfg(build_gates(c), {"G12"})) for c in C2_GRID}
P("  relax G12 only, per c_2: " + "; ".join(f"{k2}: {v}" for k2, v in g12_only_byc2.items()))

banner("K8 mirror control and K9 footings")
okK8 = True
for c2v in C2_GRID:
    G = build_gates(c2v); Gm = build_gates(c2v, flip_all=True)
    for cfg in (set(), ALL):
        okK8 = okK8 and mirror(intersect_cfg(G, cfg)) == intersect_cfg(Gm, cfg)
    okK8 = okK8 and mirror(nx(G)) == nx(Gm)
Um_s = sp.Union(*[intersect_cfg(build_gates(c, flip_all=True), set()) for c in C2_GRID])
Um_l = sp.Union(*[intersect_cfg(build_gates(c, flip_all=True), ALL) for c in C2_GRID])
okK8 = okK8 and verdict_of(Um_s, Um_l) == VERDICT
check("K8 flipping EVERY gate's sign convention mirrors I_strict, I_len and NX exactly and leaves the verdict unchanged",
      f"mirrored I_len {fmt(Um_l)}; verdict {verdict_of(Um_s, Um_l)} vs {VERDICT}", okK8)
okK9 = all(build_gates(c, "canonical")[g][k2] == build_gates(c, "alt")[g][k2] for c in C2_GRID for g in GIDS
           for k2 in ("A_str", "A_len", "X_str", "X_len"))
check("K9 footings: every gate set is identical under the canonical and alt a0 labels (no gate takes a0; bookkeeping check)",
      "identical" if okK9 else "DIFFERENT", okK9)

MUT = {}
if MUTATE:
    banner("MUTATE response: the same intersections with G1 unflipped, computed in this process")
    MUTATE_FLAG = True
    def gate_G1_unflipped(c2v):
        A_str, A_len = g1_derived[c2v]
        X = sp.Union(sp.Interval(-oo, 0), sp.Interval(2, oo))
        return dict(A_str=A_str, A_len=A_len, X_str=sp.Union(X, sp.FiniteSet(sp.Rational(1, 2))), X_len=X)
    Ul_unf = []
    for c2v in C2_GRID:
        G = build_gates(c2v); G["G1"] = gate_G1_unflipped(c2v)
        Ul_unf.append(intersect_cfg(G, ALL))
    Ul_unf = sp.Union(*Ul_unf)
    resp = Ul_unf != Ulen
    P(f"  I_len with G1 flipped: {fmt(Ulen)}  (verdict {VERDICT});  with G1 unflipped: {fmt(Ul_unf)}")
    check("M1 the intersection logic responds to flipping ONE gate's sign convention (I_len differs)",
          f"{fmt(Ulen)} vs {fmt(Ul_unf)}", resp)
    MUT = {"I_len_flipped": fmt(Ulen), "I_len_unflipped": fmt(Ul_unf), "verdict_flipped": VERDICT, "responds": bool(resp)}

banner("VERDICT")
n_fail_lb = sum(1 for c in CHECKS.values() if c["load_bearing"] and not c["ok"])
P(f"  union over c_2 of I_strict = {fmt(Ustr)}")
P(f"  union over c_2 of I_len    = {fmt(Ulen)}")
P(f"  not-shown-excluded (strict X) = {fmt(Unx)};  lenient everywhere but G12 strict = {fmt(US)}")
P(f"  VERDICT (frozen rule): {VERDICT}")
if VERDICT == "TENSION":
    P("  The strict intersection is empty: G1 (proof) and G2 (proof) need alpha_c > 0, and the strict black-hole criterion")
    P("  allows only alpha_c = 0. It opens only when G12 is read as W (option C accepted); with every other gate relaxed and")
    P("  G12 strict it stays empty, i.e. under the strict black-hole criterion alone the emptiness is robust.")
P(f"  checks: {sum(c['ok'] for c in CHECKS.values())}/{len(CHECKS)} pass; load-bearing failures: {n_fail_lb}")
P("  Chassis only. Candidate B has no action: untested for B. kappa = 1/2 is FITTED; the cold mass is still required.")
P(f"  runtime {time.time() - T0:.1f} s")

OUT = {"lane": "CFG467", "mutate": MUTATE, "frozen_criteria": "FROZEN_CRITERIA.md (committed alone before the script)",
       "inputs": {"alpha_window_L340": [AC_MIN, AC_MAX], "c2_grid": C2_GRID, "Lambda_HL_max_GeV": LAMBDA_HL_MAX,
                  "sources": SRC},
       "table": TABLE, "per_c2": PER_C2,
       "edges": {"G4_strict": {f"{c:.4e}": [fmt(G4c[c]["A_str"])] for c in C2_GRID},
                 "G5_alpha_bis": {f"{c:.4e}": alpha_bis[c] for c in C2_GRID}, "G5_lobe_thresholds_c2_0.01": lobe_thr,
                 "G11_alpha_rs": {f"{c:.4e}": alpha_rs[c] for c in C2_GRID},
                 "G6_strict": {f"{c:.4e}": fmt(G6c[c]["A_str"]) for c in C2_GRID}},
       "union": {"I_strict": fmt(Ustr), "I_len": fmt(Ulen), "NX": fmt(Unx), "I_len_G12_strict": fmt(US)},
       "binding_edges": BIND, "who_excludes": WHO, "minimal_opening_relaxations": MIN_OPEN, "single_relaxations": single,
       "G12_only_by_c2": g12_only_byc2,
       "readings": {"r1_phys_lapse_resonance_alpha": fmt(res_phys), "r2_S22_numerator_alpha_neg": str(sp.factor(num_neg)),
                    "r3_plain_BBN": {f"{c:.4e}": v for c, v in plain.items()}},
       "mutate_response": MUT,
       "checks": CHECKS, "n_checks": len(CHECKS), "n_pass": sum(c["ok"] for c in CHECKS.values()),
       "n_fail_load_bearing": n_fail_lb, "verdict": VERDICT, "runtime_s": round(time.time() - T0, 1)}
with open(OUT_JSON, "w") as f:
    json.dump(OUT, f, indent=1, default=str)
with open(OUT_TXT, "w") as f:
    f.write("\n".join(LINES) + "\n")
sys.exit(1 if n_fail_lb else 0)
