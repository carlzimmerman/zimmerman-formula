#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG187 -- AeST with a Henneaux-Teitelboim Lambda-tie: the time-flow reading assembled as one candidate, and its scorecard.

Frozen question: FROZEN_QUESTION.md (sha256 in FROZEN_QUESTION_SHA256.txt), written before this script.

Part A (load-bearing, sympy): the tie written into the record's transcription of the AeST action
(real_research/bridge1_aest_equations.md): the MOND normalisation a0 -> alpha(Lambda) = kappa sqrt(Lambda/8 pi)
(c = 1), Lambda the HT field with multiplier T^mu, as XR20 T1 / CFG43.  L1 tie, L2 Lambda global, L3 same as AeST on
shell, L4 no local dof (lattice Dirac count), L5 flat a0(z), L6 FRW and linear order a0-blind, L7 constant count,
L8 the HT term is metric-free.
Part B (controls and reported numbers): C1 a0 and 32 pi; C2 without the multiplier Lambda is local; C3 the record's
AeST overshoot; C4 the kernel tails (CFG185); C5 E(z) (FP0); C6 source anchors.  Reported: the Solar-System tails, the
alpha_1 formula over backgrounds, the kinematic boost of Y, the horn-D overshoot with the current kernels, the aether's
expansion in AeST's vector sector.
Part C (reported): the scorecard against closure_map/GATES.md, candidate B beside it.

MUTATE=1 unties a0 from Lambda (must fail L1, L7).  MUTATE=2 ties a0 to the aether's expansion theta = div A (must
fail L1, L5).  Outputs are named by mode.  kappa = 1/2 is FITTED; the tie is POSTULATED.  Nothing here says the theory
is closed.
"""
import os
import sys
import re
import json
import math
import time

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
REPO = os.path.dirname(CFGDIR)
MODE = os.environ.get("MUTATE", "0").strip() or "0"
assert MODE in ("0", "1", "2"), "MUTATE must be 0, 1 or 2"
SUF = "" if MODE == "0" else f"_MUTATE{MODE}"

sys.path.insert(0, CFGDIR)
import numpy as np                      # noqa: E402
import sympy as sp                      # noqa: E402
import CFG4_common as C4                # noqa: E402  (read-only: constants and kernels; its Run harness is NOT used)


# ================================================================================================ harness (own files)
class Tee:
    def __init__(self, path):
        self.f = open(path, "w", encoding="utf-8")
        self.o = sys.stdout

    def write(self, t):
        self.o.write(t)
        self.f.write(t)

    def flush(self):
        self.o.flush()
        self.f.flush()


OUT_PATH = os.path.join(HERE, f"CFG187_aest_tie{SUF}.out")
JSON_PATH = os.path.join(HERE, f"CFG187_aest_tie_results{SUF}.json")
_tee = Tee(OUT_PATH)
sys.stdout = _tee
T0 = time.time()
CHECKS = []
NUM = {}


def check(name, ok, detail="", load=True):
    ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    lb = "" if load else " (reported)"
    print(f"  [{tag}] {name}{lb}" + (f"\n         {detail}" if detail else ""))
    CHECKS.append({"name": name, "ok": ok, "load_bearing": load, "detail": detail})
    return ok


def head(t):
    print("\n" + "=" * 116 + f"\n{t}\n" + "=" * 116)


print(__doc__)
print(f"MODE = {MODE}  ({'main' if MODE == '0' else 'MUTATE=' + MODE})")

# ================================================================================================ constants
A0 = C4.A0                       # {'canonical': 9.3603e-11, 'alt': 1.1312e-10}  (FP0 committed)
RHO_L = C4.RHO_LAMBDA            # kg/m^3 (FP0 committed)
G_SI, C_SI = C4.G_SI, C4.C_SI
KAPPA = 0.5                      # FITTED
FP0 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026",
                                  "FP0_core_postulates_results.json")))["numbers"]
OMEGA_M = 0.3153                 # flat, no radiation (FP0/XR20's rival E(z) convention; checked in C5)
ZS = [0.5, 1.0, 2.5, 5.0, 1100.0]

# ================================================================================================ PART A: the action
head("PART A -- the tie in the AeST action (sympy; 1+1 toys for the variations, FRW and a general linear perturbation)")

t, x = sp.symbols("t x", real=True)
KB, kap, Lam0, a0c, kth = sp.symbols("K_B kappa Lambda_0 a_0 kappa_theta", positive=True)
Lam = sp.Function("Lam")(t, x)
Tt, Tx = sp.Function("T_t")(t, x), sp.Function("T_x")(t, x)
phi = sp.Function("phi")(t, x)
At, Ax = sp.Function("A_t")(t, x), sp.Function("A_x")(t, x)        # contravariant components A^t, A^x
lmul = sp.Function("lambda_u")(t, x)                                  # unit-norm multiplier
j = sp.Function("j")                                                   # the kernel shape (generic)
Kq = sp.Function("K")                                                  # AeST's dust sector K(Q) (generic)

# flat 1+1 metric eta = diag(-1, 1); A_mu = (-A^t, A^x)
dphi = (sp.diff(phi, t), sp.diff(phi, x))
Q = At * dphi[0] + Ax * dphi[1]
Y = -dphi[0] ** 2 + dphi[1] ** 2 + Q ** 2                               # (eta^{mn} + A^m A^n) d_m phi d_n phi
Ftx = sp.diff(Ax, t) + sp.diff(At, x)                                  # F_tx = d_t A_x - d_x A_t (covariant A_t = -A^t)
F2 = -2 * Ftx ** 2                                                     # F^{mn} F_mn
Jt = At * sp.diff(At, t) + Ax * sp.diff(At, x)                         # J^mu = A^nu d_nu A^mu (flat)
Jx = At * sp.diff(Ax, t) + Ax * sp.diff(Ax, x)
JdPhi = Jt * dphi[0] + Jx * dphi[1]
theta = sp.diff(At, t) + sp.diff(Ax, x)                                # the aether's expansion (flat)


def alpha_of(mode):
    """the MOND normalisation alpha = a0/c^2 as written into the action, by mode."""
    if mode == "0":
        return kap * sp.sqrt(Lam / (8 * sp.pi))      # the HT tie (POSTULATED), kappa FITTED
    if mode == "1":
        return a0c                                   # untied: an independent constant (plain AeST)
    return kth * theta / 3                           # tied to the flow's expansion theta (the 'compaction' reading)


def lagrangian(alpha, with_ht=True, lam_field=Lam):
    Fcal = (2 - KB) * alpha ** 2 * j(Y / alpha ** 2) + Kq(Q)
    L = (-(KB / 2) * F2 + 2 * (2 - KB) * JdPhi - (2 - KB) * Y - Fcal - 2 * lam_field
         - lmul * (-At ** 2 + Ax ** 2 + 1))
    if with_ht:
        L += 2 * lam_field * (sp.diff(Tt, t) + sp.diff(Tx, x))
    return L


def el(L, f):
    """Euler-Lagrange expression dL/df - d_t dL/d(f_t) - d_x dL/d(f_x) (first-derivative Lagrangians)."""
    ft, fx = sp.diff(f, t), sp.diff(f, x)
    return sp.diff(L, f) - sp.diff(sp.diff(L, ft), t) - sp.diff(sp.diff(L, fx), x)


# numeric identity test (used when symbolic simplification is inconclusive)
_s, _q = sp.symbols("s q")
J_TEST = sp.Lambda(_s, sp.Rational(2, 3) * _s ** sp.Rational(3, 2) / (1 + sp.sqrt(_s)) + _s / 5)
K_TEST = sp.Lambda(_q, 3 * (_q - sp.Rational(1, 2)) ** 2 + _q ** 4 / 7)
FIELD_TEST = {phi: sp.Rational(3, 10) * t + sp.sin(x) / 5 + t * x / 7,
              At: 1 + t ** 2 / 9 + sp.cos(x) / 11, Ax: sp.sin(t + x) / 6,
              lmul: sp.Rational(1, 3) + x / 13, Tt: t * x / 3, Tx: sp.sin(t) / 4}


def numeric_zero(expr, extra=None, pts=((0.3, 0.7), (1.1, -0.4), (-0.6, 1.9))):
    e = expr.replace(j, J_TEST).replace(Kq, K_TEST)
    sub = dict(FIELD_TEST)
    if extra:
        sub.update(extra)
    e = e.subs(sub).doit()
    vals = []
    for tv, xv in pts:
        v = complex(sp.N(e.subs({t: tv, x: xv, KB: sp.Rational(1, 5), kap: sp.Rational(1, 2), Lam0: sp.Rational(7, 5),
                                  a0c: sp.Rational(9, 10), kth: sp.Rational(1, 2)}), 30))
        vals.append(abs(v))
    return max(vals)


def is_zero(expr, extra=None):
    e = sp.expand(expr)
    if e == 0:
        return True, 0.0
    m = numeric_zero(expr, extra)
    return m < 1e-18, m


ALPHA = alpha_of(MODE)
L_TIED = lagrangian(ALPHA)

# ------------------------------------------------------------------------------------------------ L1
tA = time.time()
dalpha = sp.simplify(sp.diff(ALPHA, Lam))
fs_alpha = ALPHA.free_symbols - {kap, kth}
funcs_alpha = {f.func for f in ALPHA.atoms(sp.Function)} if ALPHA.atoms(sp.Function) else set()
depends_only_on_Lambda = (dalpha != 0) and funcs_alpha <= {Lam.func} and not (ALPHA.free_symbols & {a0c})
a0_tie = KAPPA * C_SI * math.sqrt(G_SI * RHO_L)
kappa_alt = A0["alt"] / (C_SI * math.sqrt(G_SI * RHO_L))
NUM["a0_from_tie_canonical"] = a0_tie
NUM["kappa_alt_on_rho_Lambda"] = kappa_alt
print(f"  alpha as written (mode {MODE}): {ALPHA};  d alpha / d Lambda = {dalpha}")
print(f"  a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2, FP0 rho_Lambda = {RHO_L:.6e}: {a0_tie:.6e} m/s^2 (FP0 canonical "
      f"{A0['canonical']:.6e});  alt footing on rho_Lambda needs kappa = {kappa_alt:.4f}")
check("L1 TIE: a0 is a function of the HT field Lambda alone (d alpha/d Lambda != 0, no independent a0), and "
      "kappa c sqrt(G rho_Lambda) reproduces FP0's canonical a0 to 1e-6",
      depends_only_on_Lambda and abs(a0_tie / A0["canonical"] - 1) < 1e-6,
      f"d alpha/d Lambda = {dalpha}; functions in alpha: {sorted(str(f) for f in funcs_alpha)}; "
      f"a0 ratio - 1 = {a0_tie / A0['canonical'] - 1:.2e}")

# ------------------------------------------------------------------------------------------------ L2
EL_Tt, EL_Tx = el(L_TIED, Tt), el(L_TIED, Tx)
aest_funcs = [phi, At, Ax, lmul]
t_eqs_clean = all((not e.has(f)) for e in (EL_Tt, EL_Tx) for f in aest_funcs) and \
    all((not e.has(j)) and (not e.has(Kq)) for e in (EL_Tt, EL_Tx))
t_eqs_are_dLam = (sp.simplify(EL_Tt + 2 * sp.diff(Lam, t)) == 0) and (sp.simplify(EL_Tx + 2 * sp.diff(Lam, x)) == 0)
EL_Lam = el(L_TIED, Lam)
divT = sp.diff(Tt, t) + sp.diff(Tx, x)
rest = sp.expand(EL_Lam - 2 * divT)
lam_eq_solvable = (not rest.has(Tt)) and (not rest.has(Tx))
others = {f: el(L_TIED, f) for f in aest_funcs}
no_T_elsewhere = all((not e.has(Tt)) and (not e.has(Tx)) for e in others.values())
print(f"  delta T^t : {sp.simplify(EL_Tt)} = 0;   delta T^x : {sp.simplify(EL_Tx)} = 0")
print(f"  delta Lambda : 2 d_mu T^mu + R_Lambda = 0, with R_Lambda free of T (so it fixes the clock T, not the AeST "
      f"fields): {lam_eq_solvable}; T absent from the phi, A^t, A^x, lambda equations: {no_T_elsewhere}")
check("L2 GLOBAL: varying T^mu gives d_t Lambda = d_x Lambda = 0 with no AeST field in those equations; varying Lambda "
      "only fixes d_mu T^mu (the unimodular clock); T appears in no other field equation",
      t_eqs_clean and t_eqs_are_dLam and lam_eq_solvable and no_T_elsewhere,
      f"T-equations are -2 d Lambda: {t_eqs_are_dLam}; clean of AeST fields/functions: {t_eqs_clean}")
NUM["time_L1_L2_s"] = round(time.time() - tA, 2)

# ------------------------------------------------------------------------------------------------ L3
tA = time.time()
alpha_at0 = ALPHA.subs(Lam, Lam0) if not ALPHA.atoms(sp.Derivative) else a0c   # plain AeST: a constant a0
L_PLAIN = lagrangian(alpha_at0, with_ht=False, lam_field=Lam0)
l3 = {}
for f in aest_funcs:
    e_tied = others[f].subs(Lam, Lam0).doit()
    e_plain = el(L_PLAIN, f)
    ok, m = is_zero(e_tied - e_plain)
    l3[str(f.func)] = (ok, m)
print("  on shell (Lambda = Lambda_0) minus plain AeST at a0 = alpha(Lambda_0): " +
      ", ".join(f"{k}: {'0' if v[0] else 'NONZERO'} (numeric max {v[1]:.1e})" for k, v in l3.items()))
check("L3 SAME AS AeST ON SHELL: with Lambda = Lambda_0 the phi, A^t, A^x and lambda equations of the tied action equal "
      "plain AeST's at a0 = alpha(Lambda_0), for generic j and K",
      all(v[0] for v in l3.values()), f"(generic j, K; symbolic expand, else a numeric identity test at 3 points)")
NUM["time_L3_s"] = round(time.time() - tA, 2)

# ------------------------------------------------------------------------------------------------ L4 (lattice Dirac count)
tA = time.time()
N = 5
LamS = sp.symbols(f"Lam0:{N}", real=True)
PS = sp.symbols(f"P0:{N}", real=True)            # conjugate to Lambda_n (the HT T^t density, up to a constant)
PhS = sp.symbols(f"ph0:{N}", real=True)
PiS = sp.symbols(f"pi0:{N}", real=True)
thS = sp.symbols(f"th0:{N}", real=True)          # a local stand-in for theta (mode 2 only)
jl = sp.Function("jl")


def alpha_lat(n):
    if MODE == "0":
        return kap * sp.sqrt(LamS[n] / (8 * sp.pi))
    if MODE == "1":
        return a0c
    return kth * thS[n] / 3


H0 = sum(PiS[n] ** 2 / 2 + (2 - KB) * alpha_lat(n) ** 2 * jl((PhS[(n + 1) % N] - PhS[n]) ** 2 / alpha_lat(n) ** 2)
         + 2 * LamS[n] for n in range(N))
CAN = list(zip(LamS, PS)) + list(zip(PhS, PiS))


def pb(f, g):
    return sp.expand(sum(sp.diff(f, q) * sp.diff(g, p) - sp.diff(f, p) * sp.diff(g, q) for q, p in CAN))


Gc = [LamS[(n + 1) % N] - LamS[n] for n in range(N)]
secondary = [sp.simplify(pb(g, H0)) for g in Gc]
firstclass = all(pb(Gc[a], Gc[b]) == 0 for a in range(N) for b in range(N))
Jac = sp.Matrix([[sp.diff(g, v) for v in list(LamS) + list(PS) + list(PhS) + list(PiS)] for g in Gc])
rank = Jac.rank()
ht_count = 2 * N - 2 * rank
loc_count = 2 * N                                  # (ph_n, pi_n): no constraint touches them
print(f"  periodic lattice N = {N}: constraints G_n = Lambda_(n+1) - Lambda_n, rank {rank}; {{G_n, H}} = "
      f"{secondary}; all {{G_a, G_b}} = 0: {firstclass}")
print(f"  HT sector phase-space dimension after constraints: 2N - 2 rank = {ht_count} (one global pair: Lambda_0 and "
      f"its conjugate 4-volume); local sector 2N = {loc_count}, unchanged")
check("L4 NO LOCAL DOF: the HT constraints are first class (rank N - 1), generate no secondary constraint for a "
      "Hamiltonian with arbitrary Lambda-dependence, and leave one global pair; the local count is unchanged",
      all(s == 0 for s in secondary) and firstclass and rank == N - 1 and ht_count == 2,
      f"rank {rank}, count {ht_count}")
NUM["lattice"] = {"N": N, "rank": int(rank), "ht_phase_space": int(ht_count), "local_phase_space": loc_count}
NUM["time_L4_s"] = round(time.time() - tA, 2)

# ------------------------------------------------------------------------------------------------ FRW objects (L5, L6, R-theta)
tf = sp.Symbol("t", real=True)
Nl, aS = sp.Function("N")(tf), sp.Function("a")(tf)
X = sp.symbols("x1 x2 x3", real=True)
co = [tf] + list(X)
g_frw = sp.diag(-Nl ** 2, aS ** 2, aS ** 2, aS ** 2)
gi_frw = g_frw.inv()
sqrtg = Nl * aS ** 3
A_up = [1 / Nl, 0, 0, 0]
theta_frw = sp.simplify(sum(sp.diff(sqrtg * A_up[m], co[m]) for m in range(4)) / sqrtg)


def christoffel(g, gi, coords):
    n = len(coords)
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
                                          - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]


GAM = christoffel(g_frw, gi_frw, co)
J_frw = [sp.simplify(sum(A_up[nn] * (sp.diff(A_up[m], co[nn]) + sum(GAM[m][nn][k] * A_up[k] for k in range(4)))
                         for nn in range(4))) for m in range(4)]
A_dn = [sp.simplify(sum(g_frw[m, k] * A_up[k] for k in range(4))) for m in range(4)]
F_frw = [[sp.simplify(sp.diff(A_dn[nu], co[mu]) - sp.diff(A_dn[mu], co[nu])) for nu in range(4)] for mu in range(4)]
F_zero = all(F_frw[a][b] == 0 for a in range(4) for b in range(4))
Hsym = sp.diff(aS, tf) / (aS * Nl)

# ------------------------------------------------------------------------------------------------ L5
tA = time.time()
lam_sol = sp.dsolve(sp.Eq(sp.Function("Lg")(tf).diff(tf), 0))           # d_t Lambda = 0 (from L2) on the background
Lam_t = lam_sol.rhs
E_of_z = lambda z: math.sqrt(OMEGA_M * (1 + z) ** 3 + (1 - OMEGA_M))
ratios = {}
if MODE in ("0", "1"):
    al_t = ALPHA.subs(Lam, Lam_t) if MODE == "0" else ALPHA
    const_in_time = sp.diff(al_t, tf) == 0
    for z in ZS:
        ratios[z] = 1.0 if const_in_time else float("nan")
else:
    # alpha = kappa_theta theta/3 with theta the aether's expansion: on FRW theta = 3 H
    th_is_3H = sp.simplify(theta_frw - 3 * Hsym) == 0
    for z in ZS:
        ratios[z] = E_of_z(z) if th_is_3H else float("nan")
print(f"  aether expansion on FRW: theta = {theta_frw}  (= 3 H: {sp.simplify(theta_frw - 3 * Hsym) == 0})")
print("  a0(z)/a0(0): " + ", ".join(f"z = {z:g}: {r:.6g}" for z, r in ratios.items())
      + (f"   (log10 at z = 2.5: {math.log10(ratios[2.5]):+.3f} dex)" if MODE == "2" else ""))
NUM["a0z_ratio"] = {str(z): r for z, r in ratios.items()}
check("L5 FLAT: on shell a0(z)/a0(0) = 1 to 1e-12 at z = 0.5, 1, 2.5, 5, 1100",
      all(abs(r - 1) < 1e-12 for r in ratios.values()),
      "Lambda is a global constant (L2) and alpha reads Lambda only" if MODE == "0" else
      ("alpha is an independent constant (flat, but not tied)" if MODE == "1" else "alpha reads theta = 3H(z)"))

# ------------------------------------------------------------------------------------------------ L6
eps = sp.Symbol("epsilon")
tt, xx = sp.symbols("t x", real=True)
N1, a1, pb0 = sp.Function("N")(tt), sp.Function("a")(tt), sp.Function("phibar")(tt)
htt, htx, hxx = [sp.Function(n)(tt, xx) for n in ("h_tt", "h_tx", "h_xx")]
dAx, dph = sp.Function("dA_x")(tt, xx), sp.Function("dphi")(tt, xx)
dAt = sp.Symbol("dA_t")
gP = sp.Matrix([[-N1 ** 2 + eps * htt, eps * htx], [eps * htx, a1 ** 2 + eps * hxx]])
giP = sp.Matrix([[sp.series(e, eps, 0, 2).removeO() for e in row] for row in gP.inv().tolist()])
AP = [1 / N1 + eps * dAt, eps * dAx]
unit = sp.expand(sum(gP[m, n] * AP[m] * AP[n] for m in range(2) for n in range(2)) + 1)
dAt_sol = sp.solve(sp.expand(sp.diff(unit, eps).subs(eps, 0)), dAt)[0]
AP = [1 / N1 + eps * dAt_sol, eps * dAx]
phP = pb0 + eps * dph
dphP = [sp.diff(phP, tt), sp.diff(phP, xx)]
YP = sum((giP[m, n] + AP[m] * AP[n]) * dphP[m] * dphP[n] for m in range(2) for n in range(2))
Y0 = sp.simplify(YP.subs(eps, 0))
Y1 = sp.simplify(sp.diff(YP, eps).subs(eps, 0))
Y2 = sp.simplify(sp.diff(YP, eps, 2).subs(eps, 0) / 2)
YFRW = sp.simplify(sum((gi_frw[m, n] + A_up[m] * A_up[n]) * sp.diff(sp.Function("phibar")(tf), co[m])
                       * sp.diff(sp.Function("phibar")(tf), co[n]) for m in range(4) for n in range(4)))
print(f"  FRW (3+1): Y_bar = {YFRW};  general linear perturbation (1+1: metric h, aether with the unit constraint, "
      f"scalar): Y at O(1) = {Y0}, O(eps) = {Y1}, O(eps^2) != 0: {Y2 != 0}")
print("  so the a0-sector (prop. to Y^{3/2}) is O(eps^3): absent from the FRW background and from the second-order "
      "action (the linear equations), for any alpha -- the tie is invisible to the background and linear cosmology")
check("L6 FRW AND LINEAR ORDER: Y_bar = 0 on FRW and delta Y = 0 for a general linear perturbation, so the a0-sector "
      "does not enter the background or the linear equations", YFRW == 0 and Y0 == 0 and Y1 == 0 and Y2 != 0,
      "re-derives the record's bridge1 order counting with metric and aether perturbations included")
NUM["time_L5_L6_s"] = round(time.time() - tA, 2)

# ------------------------------------------------------------------------------------------------ L7
indep_a0 = bool(ALPHA.free_symbols & {a0c})
reads_other_field = not (funcs_alpha <= {Lam.func})
dimless = ALPHA.free_symbols - {a0c, t, x}
fixed_by_L0 = depends_only_on_Lambda and not reads_other_field
print(f"  dimensionful scales besides G: Lambda_0 (an integration constant){', a0 (independent)' if MODE == '1' else ''}"
      f"{', theta (a field: a0 read from the flow)' if MODE == '2' else ''}; dimensionless couplings in alpha: "
      f"{sorted(str(s) for s in dimless)}")
check("L7 COUNT: beyond AeST's own parameters the tie adds one dimensionless coupling (kappa, FITTED) and removes a0 as "
      "an independent constant: a0 is fixed by the HT integration constant Lambda_0",
      fixed_by_L0 and not indep_a0, f"a0 independent: {indep_a0}; fixed by Lambda_0: {fixed_by_L0}")

# ------------------------------------------------------------------------------------------------ L8
g00, g01, g11 = [sp.Function(n)(t, x) for n in ("g00", "g01", "g11")]
L_HT = 2 * Lam * (sp.diff(Tt, t) + sp.diff(Tx, x))
metric_var = [sp.simplify(el(L_HT, gg)) for gg in (g00, g01, g11)]
check("L8 METRIC-FREE: the HT term 2 Lambda d_mu T^mu (T a vector density) has zero metric variation, so the tie changes "
      "neither the tensor sector (c_T) nor the PPN metric", all(m == 0 for m in metric_var), f"delta/delta g: {metric_var}")

# ------------------------------------------------------------------------------------------------ R-theta
print(f"  R-theta: on FRW the cosmic aether has theta = {theta_frw}, but F_mu nu = 0: {F_zero} and J^mu = {J_frw}")
check("R-theta: AeST's vector sector (K_B F^2 and J.grad phi) is blind to the aether's expansion theta = 3H on the "
      "cosmic background (F = 0, J = 0); the owner's 'compaction' has no dynamics in AeST's vector sector at the "
      "background level (its MOND force is the scalar's spatial gradient Y)", F_zero and all(v == 0 for v in J_frw),
      load=False)

# ================================================================================================ PART B: controls
head("PART B -- controls C1-C6 (mode-independent) and reported numbers")

# C1
alpha_c = KAPPA * math.sqrt(1.0 / (8 * math.pi))       # alpha/sqrt(Lambda)
lam_over_alpha2 = 1.0 / alpha_c ** 2
check("C1 CONTROL: a0 = kappa c sqrt(G rho_Lambda) = 9.3603e-11 (FP0) and Lambda/alpha^2 = 8 pi/kappa^2 = 32 pi = "
      "100.530965 (XR20 C3)", abs(a0_tie - 9.3603e-11) < 1e-15 and abs(lam_over_alpha2 - 100.530965) < 1e-6,
      f"a0 = {a0_tie:.6e}; Lambda/alpha^2 = {lam_over_alpha2:.6f}")

# C2 (tied alpha, no multiplier; deep-MOND j = c3 s^{3/2}); mode-independent
c3 = sp.Symbol("c_3", positive=True)
Ys, Ls = sp.symbols("Y L", positive=True)
al_t = kap * sp.sqrt(Ls / (8 * sp.pi))
Fdeep = (2 - KB) * al_t ** 2 * c3 * (Ys / al_t ** 2) ** sp.Rational(3, 2)
EL_L_noHT = sp.simplify(-2 - sp.diff(Fdeep, Ls))          # d/dLambda of (-F - 2 Lambda); no derivative terms
sols = sp.solve(sp.Eq(EL_L_noHT, 0), Ls)
lam_of_Y = [s for s in sols if s.has(Ys)]
s_pinned = [sp.simplify(Ys / al_t.subs(Ls, s) ** 2) for s in lam_of_Y]
print(f"  C2: without T^mu, Lambda's equation is algebraic: {EL_L_noHT} = 0  ->  (real root) Lambda = {lam_of_Y[0]};  "
      f"s = Y/alpha^2 = {s_pinned[0]}  ({len(lam_of_Y)} roots, all with d Lambda/d Y != 0)")
check("C2 CONTROL: without the multiplier Lambda's own equation is local; for the deep-MOND j it makes Lambda "
      "proportional to the local Y (so a0 varies in space) and pins s = Y/alpha^2 to a constant (MOND's y fixed "
      "everywhere): the multiplier is what makes the tie global (FP5 D3 / XR20 T1b, re-derived for AeST's J)",
      len(lam_of_Y) >= 1 and all(sp.diff(s, Ys) != 0 for s in lam_of_Y) and all(not s.has(Ys) for s in s_pinned),
      f"d Lambda/d Y != 0 and s independent of Y")

# C3: the record's jeans Part E overshoot (Route A = nu_rar) and the horn-D overshoot with the current kernels
F_BAR = 0.93 * 0.167
LCDM_DARK = 1 / F_BAR - 1
REG = [("cluster R500", 0.0684), ("bright spiral", 1.0), ("dwarf, deep MOND", 0.01), ("LSB dwarf", 0.003)]


def overshoot(nu):
    out = []
    for lbl, yb in REG:
        obs = 1 / F_BAR if lbl.startswith("cluster") else float(nu(yb))
        tot = (1 + LCDM_DARK) * float(nu(yb * (1 + LCDM_DARK)))
        out.append(tot / obs)
    return out


ov_rar = overshoot(C4.nu_rar)
ov_p2 = overshoot(C4.nu_p2)
ov_mono = overshoot(C4.nu_mono)
print("  horn D (dust clusters like CDM, the AQUAL sector sourced by the total density; the record's Part E arithmetic, "
      "cosmic ratio at the radius, crude): overshoot by regime " + ", ".join(r[0] for r in REG))
print(f"    Route A (nu_RAR, the record's): {', '.join(f'{v:.2f}' for v in ov_rar)}")
print(f"    P2: {', '.join(f'{v:.2f}' for v in ov_p2)};   nu_mono: {', '.join(f'{v:.2f}' for v in ov_mono)}")
NUM["overshoot"] = {"route_A": ov_rar, "P2": ov_p2, "nu_mono": ov_mono}
check("C3 CONTROL: the record's AeST overshoot with a CDM-clustering dust (mi_aest_jeans_nonlinear_verdict_2026.py E1: "
      "2.06-4.42x, Route A kernel) is reproduced", abs(min(ov_rar) - 2.06) < 0.006 and abs(max(ov_rar) - 4.42) < 0.006,
      f"min {min(ov_rar):.3f}, max {max(ov_rar):.3f}")

# C4 and R-tail: Solar-System monopole tails
GM_SUN, AU = 1.32712440018e20, 1.495978707e11
BOUND = {"Earth": (1.0, 3.66e-14), "Mars": (1.5237, 3.72e-14)}
ysym = sp.Symbol("y", positive=True)
hp2 = ysym * (sp.sqrt(1 + 1 / ysym) - 1)
p2_ok = sp.limit(hp2, ysym, sp.oo) == sp.Rational(1, 2) and \
    sp.limit(ysym * (hp2 - sp.Rational(1, 2)), ysym, sp.oo) == -sp.Rational(1, 8)   # h = 1/2 - 1/(8y) + O(1/y^2)
YP = C4.Y_PEAK_RAR
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(np.sqrt(y) > 700.0, 0.0, y / np.expm1(np.minimum(np.sqrt(y), 700.0)))  # < 1e-300 beyond
HP = float(h_rar(YP))
ygrid = np.logspace(np.log10(YP * 1.001), 4, 400)
rar_decays = bool(np.all(np.diff(h_rar(ygrid)) < 0))


def h_of(kern, y):
    if kern == "P2":
        return y * math.expm1(0.5 * math.log1p(1 / y))
    if kern == "RAR":
        return float(h_rar(y))
    return y * (float(C4.nu_mono(y)) - 1)


tails = {}
for foot in ("canonical", "alt"):
    for planet, (r_au, bnd) in BOUND.items():
        y = GM_SUN / (r_au * AU) ** 2 / A0[foot]
        for kern in ("nu_mono", "P2", "RAR"):
            h = h_of(kern, y)
            tails[f"{foot}/{planet}/{kern}"] = {"y": y, "h": h, "a_anom": h * A0[foot], "ratio": h * A0[foot] / bnd}
CFG185 = {"canonical/Earth/nu_mono": 3011, "canonical/Mars/nu_mono": 2894, "alt/Earth/nu_mono": 3620,
          "alt/Mars/nu_mono": 3479, "canonical/Earth/P2": 1279, "canonical/Mars/P2": 1258, "alt/Earth/P2": 1545,
          "alt/Mars/P2": 1520}
dev185 = max(abs(tails[k]["ratio"] / v - 1) for k, v in CFG185.items())
for k, v in tails.items():
    print(f"    {k:26s} y = {v['y']:.3e}  h = {v['h']:.4f}  a_anom = {v['a_anom']:.3e} m/s^2  = {v['ratio']:.4g} x bound")
NUM["tails"] = tails
check("C4 CONTROL: P2's tail h -> 1/2 - 1/(8y) (sympy); the RAR kernel's h decays above Y_P; nu_mono's floor value "
      "H_P = 0.648; CFG185's committed Earth/Mars ratios (both footings) reproduced to 0.5%",
      p2_ok and rar_decays and abs(HP - 0.648) < 1e-3 and dev185 < 0.005,
      f"P2 series ok {p2_ok}; RAR decays {rar_decays}; H_P = {HP:.4f}; max deviation from CFG185 {dev185:.2e}")

# C5
E_fp0 = FP0["a0z_rival_E"]
devE = max(abs(E_of_z(float(z)) / v - 1) for z, v in E_fp0.items())
check("C5 CONTROL: E(z) = sqrt(Om (1+z)^3 + 1 - Om), Om = 0.3153, reproduces FP0's committed a0z_rival_E "
      "(1.322, 1.791, 3.769, 8.294, 20513.65) to 1e-6", devE < 1e-6, f"max relative deviation {devE:.1e}")

# R-alpha1: the v9 verdict's formula over backgrounds (conditional on the formula's validity)
Jy, kb = sp.symbols("J_Y k_B", positive=True)
etaK = (kb * Jy + 2) / (Jy + 1)
detadJ = sp.simplify(sp.diff(etaK, Jy))
eta_at1 = sp.simplify(etaK.subs(Jy, 1))
amin = float(4 * eta_at1.subs(kb, 1e-12))
eta_star = 1e-4 / 4
J_needed = (2 - eta_star) / (eta_star - 1e-6)                    # at K_B = 1e-6 (< eta_star), the most favourable case
print(f"  R-alpha1: eta_K = (K_B J_Y + 2)/(J_Y + 1), d eta/d J_Y = {detadJ} (< 0 for K_B < 2), eta(J_Y = 1) = {eta_at1}; "
      f"min |alpha_1| over J_Y in [0, 1], K_B in (0, 0.25] = 4 eta(1) -> {amin:.4f}; |alpha_1| < 1e-4 needs K_B < 2.5e-5 "
      f"and J_Y > {J_needed:.3g} (at K_B = 1e-6)")
check("R-alpha1: IF the verdict's formula holds with J_Y the local AQUAL mu (<= 1 on every background, deep-MOND to "
      "Newtonian), no background rescues alpha_1: |alpha_1| >= 4; the escape needs J_Y >~ 8e4 (outside mu <= 1) and "
      "K_B < 2.5e-5 -- conditional; it does not discharge the verdict's named residual",
      sp.simplify(detadJ - (kb - 2) / (Jy + 1) ** 2) == 0 and abs(amin - 4) < 1e-6 and J_needed > 7e4, load=False)
NUM["alpha1"] = {"min_abs_alpha1_Jle1": amin, "J_needed_at_KB_1e-6": J_needed}

# R-KM: kinematic boost of Y and Q for a galaxy moving at speed beta through the aether frame
bet = sp.Symbol("beta", positive=True)
gx, gy, gz = sp.symbols("g_x g_y g_z", real=True)
gam = 1 / sp.sqrt(1 - bet ** 2)
eta4 = sp.diag(-1, 1, 1, 1)
Aup = [gam, -gam * bet, 0, 0]                    # the aether as seen in the galaxy's rest frame
dph4 = [0, gx, gy, gz]                           # a static scalar gradient in the galaxy frame
Y4 = sp.simplify(sum((eta4.inv()[m, n] + Aup[m] * Aup[n]) * dph4[m] * dph4[n] for m in range(4) for n in range(4)))
Q4 = sp.simplify(sum(Aup[m] * dph4[m] for m in range(4)))
dY = sp.simplify(Y4 - (gx ** 2 + gy ** 2 + gz ** 2))
w600 = 600e3 / C_SI
frac600 = float((gam ** 2 * bet ** 2).subs(bet, w600))
print(f"  R-KM: Y = {Y4};  Q = {Q4};  Y - |grad phi|^2 = {dY};  max fractional shift gamma^2 beta^2 at 600 km/s = "
      f"{frac600:.3e}")
check("R-KM: kinematically the MOND argument Y of a galaxy moving at w through the aether frame shifts by at most "
      "gamma^2 beta^2 = 4.0e-6 at 600 km/s (G7's line is 10%), and a0 itself is frame-independent (Lambda global); a "
      "boosted gradient also enters Q (the dust sector) -- the dynamical aether response (KM1-type) is NOT computed",
      abs(frac600 - 4.0e-6) < 2e-8 and sp.simplify(dY - gam ** 2 * bet ** 2 * gx ** 2) == 0, load=False)
NUM["km_kinematic_frac_600kms"] = frac600

# C6: anchors for every carried number
ANCHORS = [
    ("campaign_fresh_gravity/CFG4_galaxy_law.out", "canonical: P2 0.1083 dex (Upsilon_disk 0.70); nu_mono 0.1003 dex (Upsilon 0.61)"),
    ("campaign_fresh_gravity/CFG4_galaxy_law.out", "alt      : P2 0.1035 dex (Upsilon_disk 0.65); nu_mono 0.0991 dex (Upsilon 0.57)"),
    ("campaign_fresh_gravity/CFG7_hierarchy_fg001.out", "the law with the external field (boost 1.82) needs M/L_V 1.04 +- 0.15"),
    ("campaign_fresh_gravity/CFG7_hierarchy_fg001.out", "the law with the external field (boost 1.68) needs M/L_V 0.99 +- 0.11"),
    ("campaign_fresh_gravity/CFG8_README.md", "P2: +0.021 (1.7σ) canonical, +0.032 (2.7σ) alt. ν_mono: +0.034 (2.2σ) canonical, +0.041 (3.0σ) alt"),
    ("campaign_fresh_gravity/CFG8_README.md", "Spearman p 0.57–0.87"),
    ("campaign_fresh_gravity/CFG8_README.md", "The weighted slope, 0.55–0.87 ± 0.25"),
    ("campaign_fresh_gravity/CFG31_coma_udgs_under_b.out", "(L23: +1.159 / +1.112 dex, 4.9 / 4.7 sigma)"),
    ("campaign_fresh_gravity/closure_map/GATES.md", "+0.280 / +0.254 dex (x1.91 / 1.79) = 1.70 / 1.58 sigma"),
    ("campaign_fresh_gravity/closure_map/GATES.md", "Gap +0.15-0.17 dex = 1.5-1.7 sigma with floor"),
    ("campaign_fresh_gravity/closure_map/GATES_STATUS_2026-09-29.md", "+0.097 ± 0.024 (4.0σ; alt 3.65σ)"),
    ("campaign_fresh_gravity/closure_map/GATES_STATUS_2026-09-29.md", "the law's JAM-calibrated deficit stays at 3.6σ (alt 3.2σ"),
    ("campaign_fresh_gravity/closure_map/GATES.md", "PASS +0.026 (0.3 sigma) / +0.011 (0.13)"),
    ("campaign_fresh_gravity/closure_map/GATES_STATUS_2026-09-29.md", "All 23: +0.105 ± 0.063 (1.67σ"),
    ("campaign_fresh_gravity/closure_map/GATES_STATUS_2026-09-29.md", "PASS (law −0.028 ± 0.066 after the width-selection correction)"),
    ("campaign_fresh_gravity/CFG4_README.md", "| additive / measured | 1.27 ± 0.11 | 1.32 ± 0.12 | 1.32 ± 0.12 | 1.37 ± 0.12 |"),
    ("campaign_fresh_gravity/CFG4_README.md", "| significance (median of 12) | 8.4σ | 9.7σ | 9.4σ | 10.6σ |"),
    ("campaign_fresh_gravity/CFG4_clusters.out", "can/P2: eta 2.03, residual 3.47 M_b (17 sigma)"),
    ("campaign_fresh_gravity/CFG4_clusters.out", "alt/nu_mono: eta 1.68, residual 2.75 M_b (13 sigma)"),
    ("campaign_fresh_gravity/CFG4_clusters.out", "= 4.6 x the galaxy aperture's baryons"),
    ("campaign_fresh_gravity/CFG4_clusters.out", "= 4.9 x the galaxy aperture's baryons"),
    ("real_research/reviews/mi_aest_jeans_nonlinear_verdict_2026.py", "Part F needed lambda_J"),
    ("real_research/reviews/mi_aest_jeans_nonlinear_verdict_2026.py", "22 ORDERS below the natural scale"),
    ("qwen_claude_field_theory/closure_2026/condensate_pincer_2026/AEST_BOUNDARY_CONDITION_CLOSURE.md", "Their escape is a non-quadratic K: of their three CMB-fitting parameter sets, only the \"Exp\" function"),
    ("qwen_claude_field_theory/closure_2026/condensate_pincer_2026/aest_boundary_condition_closure_2026.out", "(min Delta chi2 = +106 over 28 cases)"),
    ("qwen_claude_field_theory/closure_2026/condensate_pincer_2026/aest_boundary_condition_closure_2026.out", "(Delta chi2 = -0.52, -4.72, -0.56, -4.94)"),
    ("qwen_claude_field_theory/closure_2026/condensate_pincer_2026/condensate_mu_pincer_2026.out", "(min c_s(z=3) over the table = 23 km/s)"),
    ("qwen_claude_field_theory/closure_2026/condensate_pincer_2026/CONDENSATE_NOGO_THEOREM.md", "cannot both (a) be cold enough for the CMB and the Lyman-$\\alpha$ forest and (b) be absent from galaxies"),
    ("real_research/switch_audit_2026/BS3_isolated_field_two_halo.out", "Delta chi^2 +404.3 / +415.2 (all points) and +47.1 / +51.5 inside 0.3 Mpc"),
    ("campaign_fresh_gravity/CFG1_evidence_audit.out", "framework: the strict law (no screening) gives Q2 = 3.99-5.69 x the ceiling"),
    ("campaign_fresh_gravity/CFG185_kernel_tail/README.md", "| ν_mono | 3011× | 2894× | 3620× | 3479× |"),
    ("campaign_fresh_gravity/CFG185_kernel_tail/README.md", "| P2 | 1279× | 1258× | 1545× | 1520× |"),
    ("real_research/bridge1_aest_equations.md", "keeps $c_{\\rm GW}=c$"),
    ("real_research/reviews/mi_relativistic_completion_aest_2026.py", "C2  gamma_PPN = 1"),
    ("qwen_claude_field_theory/closure_2026/V9_PPN_KILL_VERDICT.md", "**α₁ = −4η_K = −2(K_B+2) ∈ (−4.5, −4]  on all 0<K_B≤0.25.**"),
    ("qwen_claude_field_theory/closure_2026/V9_PPN_KILL_VERDICT.md", "The AeST scalar's drag term 2(2−K_B)J·∇φ **renormalizes the transverse aether anisotropy**"),
    ("campaign_fresh_gravity/CFG172_door11C/README.md", "This is a live unresolved item, not a pass."),
    ("prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md", "canonical **1.1614–1.1814**, alt **1.1917–1.2267**"),
    ("campaign_fresh_gravity/closure_map/GATES.md", "kappa = 1/2 vs 0.465 ± 0.076, 0.55 ± 0.17 | 1 sigma | consistent (0.46, 0.29 sigma)"),
    ("campaign_fresh_gravity/CFG61_README.md", "rejects B, with or without the rule, at χ² = 28.1 / 7 (p = 2.1 × 10⁻⁴, about 3.7σ)"),
    ("real_research/khronon_momentum_2026/README.md", "a₀ would track CMB-frame speed by 2w²/(εc²)"),
]
CFG7_PATH = os.path.join(REPO, "campaign_fresh_gravity/CFG7_hierarchy_fg001.out")
cfg7_txt = open(CFG7_PATH, encoding="utf-8").read()
RIVAL = {}
for foot in ("canonical", "alt"):
    for m in re.finditer(rf"^\s+{foot}\s+(G\d+) (.+?)\s*: FG001\s+([\d.]+|inf) (pass|FAIL) \| rival\s+([\d.]+|inf) (pass|FAIL)\s*$",
                         cfg7_txt, re.M):
        RIVAL[(foot, m.group(1))] = {"name": m.group(2).strip(), "fg001": m.group(3), "fg001_v": m.group(4),
                                     "rival": m.group(5), "rival_v": m.group(6)}
missing = []
for rel, txt in ANCHORS:
    src = open(os.path.join(REPO, rel), encoding="utf-8").read()
    if txt not in src:
        missing.append((rel, txt[:60]))
check("C6 CONTROL: every carried number's anchor text is present in its cited committed file, and CFG7 H0's 14 gates are "
      "parsed on both footings", not missing and len(RIVAL) == 28,
      f"{len(ANCHORS)} anchors, missing {missing}; CFG7 rows parsed {len(RIVAL)}")


def rv(g):
    c, a = RIVAL[("canonical", g)], RIVAL[("alt", g)]
    return f"{c['rival']} / {a['rival']}σ ({'FAIL' if 'FAIL' in (c['rival_v'], a['rival_v']) else 'pass'})"


# ================================================================================================ PART C: the scorecard
head("PART C -- the scorecard against closure_map/GATES.md (reported; statuses assembled from committed numbers and Part A)")


def tie_rows(props):
    """the rows whose content depends on the tie construction (Part A results)."""
    tied, flat, r25 = props["tied"], props["flat"], props["r25"]
    rows = {}
    if tied:
        rows["3.11"] = ("TIED in the action (L1-L4); kappa FITTED; consistent with the BTFR kappa 0.465 ± 0.076 "
                        "(0.46σ) and 0.55 ± 0.17 (0.29σ)", "PASS")
        rows["5.13"] = ("TIED via the HT multiplier (POSTULATED coupling alpha(Lambda)); kappa FITTED; not derived", "PASS")
    elif props["mode"] == "1":
        rows["3.11"] = ("FREE: a0 is an independent constant of the action; a0 ≈ ½c√(Gρ_Λ) is a coincidence, not "
                        "structural (the fit itself is unchanged)", "UNSCORED")
        rows["5.13"] = ("not tied (a0 independent)", "FAIL")
    else:
        rows["3.11"] = ("tied to the flow's expansion theta, not to Lambda: a0 = kappa_theta H(z) (the rival footing)",
                        "UNSCORED")
        rows["5.13"] = ("tied to theta, not to Lambda", "FAIL")
    if flat:
        rows["3.10"] = ("prediction: flat a0(z) exactly (L5); no data can score it yet (CFG52/54/99/140-170: "
                        "non-diagnostic; the KURVS lean is weak, CFG165)", "NS")
    else:
        rows["3.10"] = (f"prediction: a0 prop. to H(z): {math.log10(r25):+.3f} dex at z = 2.5 (the rival law); no data can "
                        "score it yet", "NS")
    return rows


def scorecard(props):
    TR = tie_rows(props)
    ov_p2_rng = f"{min(props['ov_p2']):.2f}-{max(props['ov_p2']):.2f}"
    ov_mono_rng = f"{min(props['ov_mono']):.2f}-{max(props['ov_mono']):.2f}"
    T = props["tails"]
    R = []

    def add(rid, obs, cand, status, phys, bstat, src):
        R.append({"id": rid, "observable": obs, "candidate": cand, "status": status, "physics": phys, "B": bstat,
                  "source": src})

    add("1.01", "SPARC RAR (the law)",
        f"horn N: same law, same numbers, ν_mono 0.1003/0.0991, P2 0.1083/0.1035 dex (no EFE in the carried rms); horn D: overshoot P2 {ov_p2_rng}x, "
        f"ν_mono {ov_mono_rng}x (crude, cosmic ratio at the radius); N9 says horn N costs the forest (3.12)",
        "CONDITIONAL", "SAME (N) / HERE (D)", "PASS (ν_mono 0.1003/0.0991)", "CFG4_galaxy_law.out; this script C3")
    add("1.07", "MW classical dSphs", f"external field applies: {rv('G4')}", "FAIL", "SAME", "PASS 1.06/0.74σ",
        "CFG7_hierarchy_fg001.out H0 (rival column)")
    add("1.08", "M31 dSphs (LVD, Collins)", f"LVD {rv('G5')}; Collins {rv('G6')}", "FAIL", "SAME",
        "MARGINAL (1.21-1.63σ, after CFG18)", "CFG7 H0 rival")
    add("1.09", "MW ultra-faints", f"{rv('G7')} (harness, statistical only; B's harness 7.97/7.52 was refereed to 3.8/3.5)",
        "FAIL", "SAME", "FAIL (refereed 3.8/3.5σ)", "CFG7 H0 rival")
    add("1.10", "LV dwarfs, host statistic", f"{rv('G8')}", "FAIL", "SAME", "PASS 1.71σ", "CFG7 H0 rival")
    add("1.11", "cluster-infall BTFR", f"slope {rv('G9')}; zero point {rv('G10')}", "FAIL", "SAME", "PASS",
        "CFG7 H0 rival")
    add("1.12", "tidal dwarfs", f"{rv('G3')}", "PASS", "SAME", "PASS (rests on ownership, CFG58)", "CFG7 H0 rival")
    add("1.13", "outer-halo GCs", "the law with the host's field needs M/L_V 1.04/0.99, inside [1.0, 2.5] (does not "
        "discriminate)", "PASS", "SAME", "PASS (does not discriminate)", "CFG7 H2")
    add("1.14", "NGC 1052-DF2 / DF4 at 20 Mpc", f"DF2 {rv('G11')}; DF4 {rv('G12')}; distance CONTESTED", "FAIL", "SAME",
        "PASS (rests on ownership)", "CFG7 H0 rival (XR27)")
    add("1.15", "Chae external-field signal", f"D1 {rv('G13')}, D2 {rv('G14')} (CFG7's EFE column); CFG8 refit: median e > 0 at 1.7-3.0σ, "
        "as an EFE theory expects; environmental slope 0.55-0.87 ± 0.25 lies 0.5-1.8σ from the EFE's 1; no rank "
        "correlation (p 0.57-0.87)", "PASS", "SAME", "FAIL (refit 1.7-3.0σ)", "CFG7 H0 rival; CFG8_README.md")
    add("1.16", "Coma UDGs", "external-field prediction: +1.159/+1.112 dex = 4.9/4.7σ", "FAIL", "SAME",
        "PASS 1.33/1.11σ", "CFG31 .out (L23)")
    add("1.17", "binary galaxies", "not computed for an EFE law", "UNSCORED", "-", "UNDECIDED", "CFG30 (B only)")
    add("1.18", "X-ray ellipticals (bare law)", "+0.280/+0.254 dex = 1.70/1.58σ; B's derived rule is not available "
        "(EFE omitted in the carried number)", "MARGINAL", "CARRIED", "MARGINAL/FAIL (rule 1.04σ)", "GATES.md 1.18")
    add("1.19", "SLACS lensing vs dynamics", "gap +0.15-0.17 dex = 1.5-1.7σ with the floor (law)", "MARGINAL", "CARRIED",
        "MARGINAL", "GATES.md 1.19")
    add("1.20", "SLUGGS massive early types (bare law)", "+0.097 ± 0.024 (4.0σ, JAM masses); 3.6σ with published GC "
        "slopes; below 2σ only at the favourable slope-orbit corner (CFG114)", "FAIL", "CARRIED",
        "FAIL (rule 1.55σ with published slopes)", "GATES_STATUS 1.20 + addenda")
    add("1.21", "passive disks", "+0.026 (0.3σ)", "PASS", "CARRIED", "PASS", "GATES.md 1.21")
    add("1.25", "super spirals", "+0.105 (1.67σ); nine fastest 2.34σ, shared with ΛCDM (CFG68)", "MARGINAL", "CARRIED",
        "MARGINAL/FAIL", "GATES_STATUS 1.25")
    add("1.26", "massive HI disks", "law −0.028 ± 0.066", "PASS", "CARRIED", "PASS", "GATES_STATUS 1.26")
    add("1.24", "environmental null (a0 vs ambient density)", "a0 global (Lambda constant, L2); the EFE is a different "
        "effect", "PASS", "HERE", "consistent", "Part A L2/L5")
    add("2.01", "X-COP at 0.8 R500",
        "FAIL on both horns: D additive >= 1.27-1.37 (8.4-10.6σ; a lower bound, since AeST's phantom is also sourced by "
        "the dust); N law alone short, eta 1.68-2.03 (13-17σ); the middle (11-26% of the dust at R500) needs "
        "lambda_J ~ 2.7 Mpc, 22 orders from AeST's natural condensate scale", "FAIL", "CARRIED", "PASS 0.946 ± 0.080",
        "CFG4_README.md; CFG4_clusters.out; jeans verdict C1")
    add("2.02", "Bullet Cluster", "horn D: collisionless dust at the cosmic share, as B (4.6x/4.9x needed); horn N: no "
        "committed MOND-alone score (literature: fails, UNVERIFIED)", "CONDITIONAL", "CARRIED (D)", "PASS 4.6x/4.9x",
        "CFG4_clusters.out H5")
    add("2.03", "Lovisari X-ray groups", "not computed for this candidate", "UNSCORED", "-", "R500 MARGINAL; R2500 FAIL",
        "CFG34 (B only)")
    add("2.04", "Local Group R0", "B's edge construct; not framework-specific", "UNSCORED", "-", "FAIL (shared)", "CFG20/23")
    add("3.01", "CMB TT/TE/EE", "AeST's published fit (LIT, UNVERIFIED); the tie is invisible at linear order (L6); the "
        "record reads SZ21 as: only the 'Exp' K meets the galactic mu bound; N9: a charge dust cannot be both CMB/forest-"
        "cold and absent from galaxies", "CONDITIONAL", "LIT + HERE", "met by construction",
        "bridge1_aest_equations.md; AEST_BOUNDARY_CONDITION_CLOSURE.md; CONDENSATE_NOGO_THEOREM.md")
    add("3.02", "CMB lensing", "not computed", "UNSCORED", "-", "PASS (bound-only switch)", "-")
    add("3.03", "growth, S8, RSD", "AeST's P(k) fit (LIT, UNVERIFIED); not computed here", "UNSCORED", "LIT",
        "met by allowance", "-")
    add("3.04", "BAO, background", "FRW is AeST's with Lambda constant (L5, L6)", "PASS", "HERE + LIT",
        "unchanged by construction", "Part A")
    add("3.05", "KiDS isolated lenses", "the record's AeST closure: charge-fixed boundary Δχ² >= +106 for every m², both "
        "footings; passes (Δχ² −0.5 to −4.9) only with a free per-galaxy constant at m² <= 1e-3 /Mpc² (MMH23's regime); "
        "a kernel that sees the web's total field: +404/+415 (+47/+52 inside 0.3 Mpc; BS3, base model C-H/K)", "FAIL",
        "SAME (closure) / CARRIED (BS3)", "PASS at x_e = 0.4", "aest_boundary_condition_closure_2026.out; BS3 .out")
    add("KiDS-split", "KiDS early/late split (CFG61/67/110)", "an EFE theory predicts an environment-correlated "
        "difference; its size and sign were not computed", "UNSCORED", "-", "FAIL ~3.7σ (B-specific vs colour-split ΛCDM)",
        "CFG61_README.md")
    add("3.06-3.09", "budget, edge", "B's constructs (phantom budget, edge x_e); this candidate has neither", "N/A", "-",
        "mixed (see GATES_STATUS)", "-")
    add("3.10", "a0(z) at z ≈ 2.5", TR["3.10"][0], TR["3.10"][1], "HERE", "NS (flat, TIED)", "Part A L5")
    add("3.11", "a0 = kappa c sqrt(G rho_Lambda)", TR["3.11"][0], TR["3.11"][1], "HERE", "consistent; kappa FITTED",
        "Part A L1; GATES.md 3.11")
    add("3.12", "Lyman-alpha forest", "horn D: cold dust (as CDM, not scored numerically); horn N: FAIL by N9 F1 (a "
        "galaxy-shielding dust is >= 20 km/s at z = 3; min 23 km/s)", "CONDITIONAL", "SAME (N9)", "PASS 0.00",
        "condensate_mu_pincer_2026.out")
    add("3.13", "shear, JWST, Li-7, BBN, tau", "not computed", "NS", "-", "NS", "-")
    add("4.01", "Cassini, ephemeris", f"the Sun owns its phantom: EFE quadrupole 3.99-5.69x the Q2 ceiling (strict P2 "
        f"law); monopole ν_mono {T['canonical/Earth/nu_mono']['ratio']:.0f}/{T['alt/Earth/nu_mono']['ratio']:.0f}x, P2 "
        f"{T['canonical/Earth/P2']['ratio']:.0f}/{T['alt/Earth/P2']['ratio']:.0f}x the Earth bound; the RAR kernel "
        "removes the monopole, not the quadrupole", "FAIL", "SAME + HERE", "PASS via ownership",
        "CFG1_evidence_audit.out A01; CFG185; this script C4")
    add("4.02", "GW170817", "c_T = c by AeST's construction (LIT, as the record's transcription states; UNVERIFIED); the "
        "HT term is metric-free (L8)", "PASS" if props["metric_free"] else "UNSCORED", "LIT + HERE", "NS (no action)",
        "bridge1_aest_equations.md; Part A L8")
    add("4.03", "gamma = 1 (lensing = dynamics)", "Phi = Psi in AeST's quasi-static limit (the record's completion script "
        "C1-C2, from LIT)", "PASS", "LIT", "NS as derivation", "mi_relativistic_completion_aest_2026.py")
    add("4.04", "PPN alpha_1, alpha_2", "alpha_1 = −2(K_B+2), >= 4.4e4x over |alpha_1| < 1e-4 (the v9 kill, attributed "
        "there to AeST's J.grad phi term, which this candidate shares); named residual: the Sun's own background, "
        "unresolved (CFG172 §3); if J_Y <= 1 on every background, |alpha_1| >= 4 everywhere (R-alpha1, conditional); "
        "alpha_2 UNSCORED (v9's number carries v9's own tie factor)", "FAIL", "CARRIED", "NS",
        "V9_PPN_KILL_VERDICT.md; CFG172 README; R-alpha1")
    add("4.05", "wide binaries DR3", "contested (1.0-1.4)", "CONT", "-", "CONT", "GATES.md 4.05")
    add("4.06", "wide binaries DR4 (2 Dec 2026)", "this candidate predicts Arm A: 1.1614-1.1814 (can) / 1.1917-1.2267 "
        "(alt); dies if Newtonian", "NS", "SAME", "NS; B predicts Arm C 1.000", "PREREGISTRATION_DR4.md")
    add("4.07", "external-field effect", "present: supported by Chae (1.15), against the satellites, Coma UDGs and DF2 "
        "(1.07-1.16)", "MIXED", "SAME", "absent by ownership (CONT)", "rows 1.07-1.16")
    add("4.08", "preferred frame / KM1", f"a0 frame-independent (Lambda global); kinematic shift of Y <= {frac600:.1e} "
        "at 600 km/s; the aether-drag response not computed; CFG186 (SPARC vs CMB speed) pending", "UNSCORED", "HERE (kin.)",
        "NS", "R-KM; KM1 README")
    add("5.01", "one explicit action", "yes: AeST + HT (one action); not an action for B, and it fails rows above",
        "PASS", "HERE", "FAIL/OPEN", "Part A")
    add("5.02", "stability", "not analysed here (the record: the dust condensate's c_s^2 in [0, 1/3]; AeST's ghost-"
        "freedom LIT, UNVERIFIED)", "UNSCORED", "-", "FAIL as varied (V0)", "jeans verdict A1-A3")
    add("5.05", "local degrees of freedom", "the tie adds 0 local, +1 global (L4); AeST's own count not re-derived",
        "PASS" if props["dof"] else "FAIL", "HERE", "orphaned", "Part A L4")
    add("5.10", "FLRW", "background = AeST's with constant Lambda (L6); growth UNSCORED",
        "PASS" if props["frw"] else "FAIL", "HERE", "partial", "Part A L6")
    add("5.11", "dark mass as a state of the field", "structurally yes: the dust is the scalar's Q-sector (no particle; "
        "the mass still required); N9 excludes the version absent from galaxies", "CONDITIONAL", "SAME (N9)", "OPEN",
        "CONDENSATE_NOGO_THEOREM.md")
    add("5.13", "a0-Lambda relation", TR["5.13"][0], TR["5.13"][1], "HERE", "declared input; kappa FITTED", "Part A")
    return R


def props_for(mode, tied, flat, r25, metric_free, dof, frw):
    return {"mode": mode, "tied": tied, "flat": flat, "r25": r25, "metric_free": metric_free, "dof": dof, "frw": frw,
            "ov_p2": ov_p2, "ov_mono": ov_mono, "tails": tails}


def ck(name):
    return next(c["ok"] for c in CHECKS if c["name"].startswith(name))


props_run = props_for(MODE, ck("L1") and ck("L7"), ck("L5"), ratios[2.5], ck("L8"), ck("L4"), ck("L6"))
props_ref = props_for("0", True, True, 1.0, True, True, True)     # the declared construction (main mode), for the diff
SC = scorecard(props_run)
SC_REF = scorecard(props_ref)
for r in SC:
    print(f"  {r['id']:>9s}  {r['status']:<11s} | {r['observable']}: {r['candidate']}\n{'':24s}B: {r['B']}   "
          f"[{r['physics']}; {r['source']}]")

# tallies and the head-to-head
RANK = {"PASS": 3, "MARGINAL": 2, "CONDITIONAL": 1, "FAIL": 0}


def bcode(s):
    s = s.upper()
    for k in ("FAIL", "MARGINAL", "PASS"):
        if s.startswith(k) or s.startswith("CONSISTENT") and k == "PASS" or s.startswith("MET") and k == "PASS":
            return k
    return None


better, worse, same = [], [], []
for r in SC:
    b = bcode(r["B"])
    c = r["status"] if r["status"] in RANK else None
    if b is None or c is None:
        continue
    (better if RANK[c] > RANK[b] else worse if RANK[c] < RANK[b] else same).append(r["id"])
tally = {}
for r in SC:
    tally[r["status"]] = tally.get(r["status"], 0) + 1
print("\n  candidate status tally (rows are not equally weighted): " + ", ".join(f"{k} {v}" for k, v in sorted(tally.items())))
print(f"  head-to-head against B where both have a data status: better on {better}; worse on {worse}; same on {same}")
changed = [r["id"] for r, q in zip(SC, SC_REF) if (r["status"], r["candidate"]) != (q["status"], q["candidate"])]
print(f"  rows that differ from the main construction in this mode: {changed if changed else 'none'}")
data_rows_changed = [i for i in changed if i not in ("3.10", "3.11", "5.13")]
check("R-DIFF: rows changed relative to the main construction are limited to the tie rows (3.10, 3.11, 5.13)",
      not data_rows_changed, f"changed {changed}", load=False)
NUM.update({"tally": tally, "better_than_B": better, "worse_than_B": worse, "same_as_B": same,
            "rows_changed_vs_main": changed})

# ================================================================================================ verdict
head("VERDICT")
lb_fail = [c["name"].split(":")[0] for c in CHECKS if c["load_bearing"] and not c["ok"]]
rep_fail = [c["name"].split(":")[0] for c in CHECKS if not c["load_bearing"] and not c["ok"]]
n_pass = sum(c["ok"] for c in CHECKS)
if MODE == "0":
    print("  The tie can be written into AeST exactly as XR20 T1 / CFG43 write it: Lambda is a global constant, a0(z) is "
          "flat, no local degree of freedom is added, and on shell the theory IS AeST at a0 = alpha(Lambda_0). The tie "
          "is POSTULATED and kappa = 1/2 FITTED. Whether untying it changes any data row is MUTATE=1's R-DIFF line.")
    print(f"  Scorecard: better than B on {better}; worse on {worse}. The EFE rows, the Solar System, X-COP and the "
          "KiDS closure go against it; Chae, GW170817/gamma and 'one action' go for it.")
else:
    need = {"1": ["L1", "L7"], "2": ["L1", "L5"]}[MODE]
    bit = all(any(f.split()[0] == n for f in lb_fail) for n in need)
    print(f"  MUTATE={MODE}: required failures {need}: {'present' if bit else 'MISSING'}; load-bearing failures {lb_fail}")
print(f"\n  {n_pass}/{len(CHECKS)} checks pass; load-bearing failures: {len(lb_fail)} {lb_fail}; reported failures: "
      f"{rep_fail}; {time.time() - T0:.1f} s")
rc = 1 if lb_fail else 0
json.dump({"lane": "CFG187", "mode": MODE, "checks": CHECKS, "numbers": NUM, "scorecard": SC, "rc": rc},
          open(JSON_PATH, "w", encoding="utf-8"), indent=1, default=str)
print(f"  wrote {os.path.relpath(OUT_PATH, REPO)} and {os.path.relpath(JSON_PATH, REPO)}; rc = {rc}")
sys.stdout = _tee.o
_tee.f.close()
sys.exit(rc)
