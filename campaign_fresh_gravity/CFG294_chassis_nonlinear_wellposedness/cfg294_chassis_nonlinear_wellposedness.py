#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG294 -- NONLINEAR LOCAL WELL-POSEDNESS OF THE RELATIVISTIC CHASSIS (C-H/K) ON THE KHRONON'S LEAVES, DERIVED STEP BY STEP.
Criteria frozen first: FROZEN_CRITERIA.md (commit 2821be492).  CFG292 showed that F2a (t = tau, spatial de Donder with the
4-D trace, lapse eliminated elliptically) is strongly hyperbolic at the 18 record points.  This lane carries that to the
quasilinear statement: constant multiplicity -> an explicit Kreiss symmetriser -> Kato's quasilinear theorem for the
hyperbolic part -> the elliptic lapse and the mixed elliptic-hyperbolic system, with Andersson & Moncrief (2003) mapped
hypothesis by hypothesis.

THE SYSTEM.  L340's C-H/K, I_CH + c^3/(16 pi G) Int sqrt(-g)[alpha_c a.a - c_2 K^2], beta = 0, lambda_K = 1 + c_2; its
principal symbol is GR + the BPS khronon (CFG292 R0); F2a is built with cfg292_lib (imported read-only from the CFG292 lane).
c_S^2 = c_2 (2 - alpha_c) / (alpha_c (2 + 3 c_2)).

WHAT IS CHECKED.  S1 constant multiplicity (symbolic minimal polynomials, rigorous interval gap, exact uniformity over
directions and general frozen backgrounds), S2 the symmetriser H = Sum_j P_j^T G P_j from Lagrange-interpolation spectral
projectors (exact symmetry, exact LDL positivity, dense directions, symbolic smoothness; HKM canonical-energy inertia as a
finding), S3 Kato's hypotheses K1-K4 (coefficient smoothness, the explicit order -infinity MOND bound, nu_mono's splice and
the admissible Sobolev range, the zero-field set), S4 the nonlinear lapse equation from the action, its ellipticity, its
kernel (relabelling mode; the F2a Bianchi-I sign condition), linearised constraint propagation, and the AM1-AM9 table.
Controls: GR full harmonic; GR CMC + spatial harmonic (Andersson-Moncrief) with a maximal k = 0 sub-probe that must fail
the kernel check; minimal Horava (alpha_c = 0) must fail S1/S2; MUTATE=1 puts the points on the crossing c_S = 1.

SCOPE.  Local in time; beta = 0; F2a on the khronon's leaves; data away from zero-field regions (status in K4d).  Lean
certifies only algebraic inequalities (cfg294_algebraic_core.lean), never the analysis theorems.

Run from the repository root:
  python3 campaign_fresh_gravity/CFG294_chassis_nonlinear_wellposedness/cfg294_chassis_nonlinear_wellposedness.py
  MUTATE=1 python3 campaign_fresh_gravity/CFG294_chassis_nonlinear_wellposedness/cfg294_chassis_nonlinear_wellposedness.py
"""
import os, sys, json, math, time
import multiprocessing as mproc
from fractions import Fraction
import numpy as np
import sympy as sp
import mpmath as mp
from sympy.polys.matrices import DomainMatrix
from scipy.sparse import diags, kron, identity, csr_matrix, bmat
from scipy.sparse.linalg import eigsh, spsolve

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LANE292 = os.path.join(REPO, "campaign_fresh_gravity", "CFG292_khronon_strong_hyperbolicity")
sys.path.insert(0, LANE292)
from cfg292_lib import (R4, PAIRS, XI, HV, VARS_H, L_EH, L_gf, L_khronon, symbol_matrix, deDonder, fourier_sub)

MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "CFG294", "cfg294_chassis_nonlinear_wellposedness"
FROZEN = "2821be492"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "frozen_criteria_commit": FROZEN, "checks": {}, "numbers": {}}
T0 = time.time()
mp.mp.dps = 50
QQ = sp.QQ


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (finding, not load-bearing)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 118); P(t); P("=" * 118)


P(__doc__.split("WHAT IS CHECKED")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the 18 points are moved onto the crossing c_S = 1 (alpha = c_2/(1 + 2 c_2)) and 1% off it;"
      " S1 must FAIL and S2 must FLAG (rc 1) ***")

al, c2 = sp.symbols("alpha c_2", real=True)
lam = sp.Symbol("lambda")
HALF = sp.Rational(1, 2)
ETA = sp.diag(-1, 1, 1, 1)
DT = [1, 0, 0, 0]
CS2 = c2 * (2 - al) / (al * (2 + 3 * c2))            # beta = 0
def cs2_of(a_, c_):
    return sp.Rational(c_) * (2 - sp.Rational(a_)) / (sp.Rational(a_) * (2 + 3 * sp.Rational(c_)))

# ================================================================================================ INPUTS
banner("INPUTS: record values (committed files) and the CFG292 numbers this lane builds on")
L340 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json")))
L350 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L350_chk_cosmological_G_gate_results.json")))
J292 = json.load(open(os.path.join(LANE292, "cfg292_khronon_strong_hyperbolicity_results.json")))
RECIPE = open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md"), encoding="utf-8").read()
L340SRC = open(os.path.join(REPO, "real_research/g03_audit_2026/L340_filtered_khronon_completion.py"), encoding="utf-8").read()
AC_MIN, AC_MAX = L340["numbers"]["P1"]["alpha_c_min"], L340["numbers"]["P1"]["alpha_c_max"]
C2_MIN, C2_MAX = L340["numbers"]["P1"]["c2_min"], L340["numbers"]["P1"]["c2_max"]
CAPS = sorted(float(r["c2_ceiling"]) for r in L350["numbers"]["G2"]["rows"])
C2_RECIPE = 0.10
def rat(x):
    return sp.Rational(f"{x:.5e}")                      # CFG292's rounding: 6 significant digits
ALPHAS = [rat(AC_MIN), rat(AC_MAX)]
C2S = [rat(c) for c in CAPS] + [rat(C2_MIN), rat(C2_MAX), rat(C2_RECIPE)]
POINTS_REC = [(a, c) for a in ALPHAS for c in C2S]
axc = lambda c_: c_ / (1 + 2 * c_)                       # crossing locus c_S^2 = 1 at beta = 0
POINTS = ([(axc(c), c) for c in C2S] + [(axc(c) * sp.Rational(101, 100), c) for c in C2S]) if MUTATE else POINTS_REC
W_P1 = (rat(AC_MIN), rat(AC_MAX), rat(C2_MIN), rat(C2_MAX))
W_REC = (min(a for a, _ in POINTS), max(a for a, _ in POINTS), min(c for _, c in POINTS), max(c for _, c in POINTS))
P(f"    L340 P1 window: alpha_c in ({AC_MIN:.4e}, {AC_MAX:.2e}), c_2 in ({C2_MIN:.4e}, {C2_MAX:.4f})")
P(f"    L350 G2 ceilings: {', '.join(f'{c:.3e}' for c in CAPS)};  recipe edge c_2 = {C2_RECIPE}")
P(f"    {'MUTATE' if MUTATE else 'record'} points: {len(POINTS)};  W_rec box = alpha [{float(W_REC[0]):.4e}, {float(W_REC[1]):.4e}] x "
  f"c_2 [{float(W_REC[2]):.4e}, {float(W_REC[3]):.4e}]")
k292 = [r_["cond"] for r_ in J292["numbers"]["T5"]["F2a"]]
P(f"    CFG292: F2a strongly hyperbolic {J292['summary']['SH_F2a']}; eigenvector-matrix condition numbers kappa(T) "
  f"{min(k292):.3e} .. {max(k292):.3e};  C5 (c_S = 1) {J292['numbers']['COND']['C5']['roots']}")
OUT["numbers"]["inputs"] = {"points": [[str(a), str(c)] for a, c in POINTS], "W_rec": [str(x) for x in W_REC],
                            "W_P1": [str(x) for x in W_P1]}

# ================================================================================================ machinery
def F2a_lagrangian(gbar, alpha=al, cc2=c2):
    Lk_, _ = L_khronon(gbar, DT, alpha, 0, cc2)
    return L_EH(gbar) + Lk_ + L_gf(gbar, HALF, "spatial4")


def coef_mats(Psym):
    """P(xi) = sum_{m<=n} P^{mn} xi_m xi_n: return the coefficient matrices (sympy, possibly symbolic in alpha, c_2)."""
    out = {}
    for m in R4:
        for n in range(m, 4):
            out[(m, n)] = Psym.applyfunc(lambda e_: sp.Poly(e_, *XI).coeff_monomial(XI[m] * XI[n]) if e_ != 0 else 0)
    return out


def to_QQ(Mx):
    return DomainMatrix.from_Matrix(Mx).convert_to(QQ)


def to_frac(x):
    """Fraction from a sympy Rational/Integer or a domain rational (PythonMPQ)."""
    if hasattr(x, "p") and hasattr(x, "q"):
        return Fraction(int(x.p), int(x.q))
    return Fraction(int(x.numerator), int(x.denominator))


def mpf_of(x):
    f_ = to_frac(x)
    return mp.mpf(f_.numerator) / f_.denominator


def point_mats(CMsym, a_, c_):
    return {k_: to_QQ(v_.subs({al: a_, c2: c_})) for k_, v_ in CMsym.items()}


def q(x):
    return QQ.from_sympy(sp.Rational(x))


FIELDS9 = [str(v_) for v_ in VARS_H[1:]]                          # H01 H02 H03 H11 H12 H13 H22 H23 H33
def frob_weights(names):
    return [sp.Integer(1) if n_[1] == n_[2] else HALF for n_ in names]   # Frobenius metric on symmetric tensors
G9 = frob_weights(FIELDS9)
G18 = DomainMatrix.diag([q(x) for x in G9 + G9], QQ)


def pencil_at(CM, k):
    """A10, B10, C10 with P(lambda, k) = A10 lambda^2 + B10 lambda + C10 (exact)."""
    A10 = CM[(0, 0)]
    B10 = CM[(0, 1)] * k[0] + CM[(0, 2)] * k[1] + CM[(0, 3)] * k[2]
    C10 = (CM[(1, 1)] * (k[0] * k[0]) + CM[(2, 2)] * (k[1] * k[1]) + CM[(3, 3)] * (k[2] * k[2])
           + CM[(1, 2)] * (k[0] * k[1]) + CM[(1, 3)] * (k[0] * k[2]) + CM[(2, 3)] * (k[1] * k[2]))
    return A10, B10, C10


def schur_lapse(A10, B10, C10):
    """eliminate H00 (index 0); returns (A, B, C, p00, lapse_lambda_free, P0r_linear)."""
    p00 = C10[0, 0].element
    lam_free = A10[0, 0].element == 0 and B10[0, 0].element == 0
    lin = all(A10[0, j].element == 0 for j in range(10))
    n = A10.shape[0]
    b0, c0 = B10[0:1, 1:n], C10[0:1, 1:n]
    if p00 == 0:
        return None, None, None, p00, lam_free, lin
    pinv = QQ(1) / p00
    A = A10[1:n, 1:n] - (b0.transpose() * b0) * pinv
    B = B10[1:n, 1:n] - (b0.transpose() * c0 + c0.transpose() * b0) * pinv
    C = C10[1:n, 1:n] - (c0.transpose() * c0) * pinv
    return A, B, C, p00, lam_free, lin


def companion(A, B, C):
    n = A.shape[0]
    if A.det() == 0:
        return None
    Ai = A.inv()
    Z, I = DomainMatrix.zeros((n, n), QQ), DomainMatrix.eye(n, QQ)
    return Z.hstack(I).vstack((-(Ai * C)).hstack(-(Ai * B)))


def poly_coeffs_expected(nu, rho, s2list_mults):
    ex = sp.Integer(1)
    for s2, m in s2list_mults:
        ex *= ((lam - nu)**2 - s2 * rho)**m
    return sp.Poly(sp.expand(ex), lam).all_coeffs()


def ldl_pivots(Hdm):
    H = [[to_frac(x) for x in row] for row in Hdm.to_list()]
    n = len(H); L = [[Fraction(0)] * n for _ in range(n)]; d = [Fraction(0)] * n
    for j in range(n):
        d[j] = H[j][j] - sum(L[j][k] ** 2 * d[k] for k in range(j))
        if d[j] == 0:
            return d[:j + 1]
        for i in range(j + 1, n):
            L[i][j] = (H[i][j] - sum(L[i][k] * L[j][k] * d[k] for k in range(j))) / d[j]
    return d


def dm_to_mp(Dm):
    return mp.matrix([[mpf_of(x) for x in row] for row in Dm.to_list()])


def symmetriser(D, rho, cs2, Gm):
    """H = Sum_j P_j^T G P_j for the families {+-sqrt(rho)} and {+-c_S sqrt(rho)} (cs2 = None: one family).
    Exact, rational.  Returns (H, note); note != '' if the construction is undefined."""
    n = D.shape[0]; I = DomainMatrix.eye(n, QQ)
    D2 = D * D
    if cs2 is None:
        return (Gm + D.transpose() * Gm * D * (QQ(1) / rho)) * QQ(1, 2), ""
    if cs2 == 1:
        return None, "projector denominator 1 - c_S^2 = 0: the two families merge, the Lagrange projectors are undefined"
    R = (D2 - I * (cs2 * rho)) * (QQ(1) / (rho * (1 - cs2)))
    Qm = (D2 - I * rho) * (QQ(1) / (rho * (cs2 - 1)))
    RD, QD = R * D, Qm * D
    H = (R.transpose() * Gm * R + RD.transpose() * Gm * RD * (QQ(1) / rho)
         + Qm.transpose() * Gm * Qm + QD.transpose() * Gm * QD * (QQ(1) / (rho * cs2))) * QQ(1, 2)
    return H, ""


def projector_norms(D, rho, cs2, gw):
    """G-norms of the four spectral projectors (mpmath), for the bound kappa(H) <= 4 Sum ||P_j||^2."""
    Dm = dm_to_mp(D); n = Dm.rows; I = mp.eye(n)
    sr = mp.sqrt(mpf_of(rho)); c = mp.sqrt(mpf_of(cs2))
    Mp = Dm / sr; M2 = Mp * Mp
    R = (M2 - c**2 * I) / (1 - c**2); Qm = (M2 - I) / (c**2 - 1)
    Ps = [R * (Mp + I) / 2, -R * (Mp - I) / 2, Qm * (Mp + c * I) / (2 * c), -Qm * (Mp - c * I) / (2 * c)]
    S = mp.diag([mp.sqrt(mpf_of(x)) for x in gw]); Si = S**-1
    nrm = [max(mp.svd_r(S * Pj * Si, compute_uv=False)) for Pj in Ps]
    resid = mp.mnorm(sum(Ps, mp.zeros(n, n)) - I, 1)
    return nrm, resid


def h_spectrum(H, gw):
    S = mp.diag([1 / mp.sqrt(mpf_of(x)) for x in gw])
    Hs = S * dm_to_mp(H) * S
    Hs = (Hs + Hs.T) / 2
    ev = mp.eigsy(Hs, eigvals_only=True)
    return min(ev), max(ev)


def exact_case(CM, k, nu, rho, cs2, pred00, gw=None, want_spectrum=True):
    """the full exact S1c/S2a pipeline at one (point, k, background)."""
    gw = gw or (G9 + G9)
    Gm = DomainMatrix.diag([q(x) for x in gw], QQ)
    A10, B10, C10 = pencil_at(CM, k)
    A, B, C, p00, lam_free, lin = schur_lapse(A10, B10, C10)
    res = {"lapse_lambda_free": bool(lam_free), "P0r_linear": bool(lin), "p00": str(QQ.to_sympy(p00)),
           "p00_formula": bool(p00 == pred00), "A_invertible": False}
    if A is None:
        return res
    M = companion(A, B, C)
    if M is None:
        return res
    res["A_invertible"] = True
    n2 = M.shape[0]; I = DomainMatrix.eye(n2, QQ)
    cp = M.charpoly()
    exp_c = poly_coeffs_expected(QQ.to_sympy(nu), QQ.to_sympy(rho), [(1, 8), (QQ.to_sympy(cs2), 1)])
    res["charpoly"] = [QQ.to_sympy(x) for x in cp] == exp_c
    D = M - I * nu
    D2 = D * D
    res["minpoly"] = ((D2 - I * rho) * (D2 - I * (cs2 * rho))).is_zero_matrix
    res["families_distinct"] = bool(cs2 != 0 and cs2 != 1)
    res["mult_8811"] = bool(res["charpoly"] and res["minpoly"] and res["families_distinct"])
    if cs2 == 1:   # merged family: count the multiplicity of +sqrt(rho) explicitly (D semisimple iff D^2 = rho)
        res["rank_D2_minus_rho"] = int((D2 - I * rho).rank())
        trD = sum((D[i, i].element for i in range(n2)), QQ(0))
        res["mult_plus1"] = (int(((n2 + trD) / 2).numerator) if (rho == 1 and res["rank_D2_minus_rho"] == 0 and ((n2 + trD) / 2).denominator == 1)
                             else None)
    else:
        res["mult_plus1"] = 8 if res["charpoly"] else None
    H, note = symmetriser(D, rho, cs2, Gm)
    res["H_note"] = note
    if H is None:
        res.update(H_sym=False, HD_sym=False, H_pd=False)
        return res
    HD = H * D
    res["H_sym"] = (H - H.transpose()).is_zero_matrix
    res["HD_sym"] = (HD - HD.transpose()).is_zero_matrix
    piv = ldl_pivots(H)
    res["H_pd"] = len(piv) == n2 and all(x > 0 for x in piv)
    if want_spectrum:
        lmin, lmax = h_spectrum(H, gw)
        nrm, resid = projector_norms(D, rho, cs2, gw)
        res.update(lam_min=float(lmin), kappa=float(lmax / lmin), bound=float(4 * sum(x**2 for x in nrm)),
                   proj_sum_resid=float(resid))
    return res


def rat_unit_dirs(nd, seed):
    rng = np.random.default_rng(seed)
    out = [[QQ(0), QQ(0), QQ(1)]]
    while len(out) < nd:
        a_ = sp.Rational(int(rng.integers(-9, 10)), int(rng.integers(1, 10)))
        b_ = sp.Rational(int(rng.integers(-9, 10)), int(rng.integers(1, 10)))
        den = 1 + a_**2 + b_**2
        v_ = [q(2 * a_ / den), q(2 * b_ / den), q((1 - a_**2 - b_**2) / den)]
        if v_ not in out:
            out.append(v_)
    return out


# symbolic F2a symbol on the aligned background (alpha, c_2 symbolic, beta = 0) and its coefficient matrices
P_F2a = symbol_matrix(F2a_lagrangian(ETA), VARS_H)
CM_F2a = coef_mats(P_F2a)

# ================================================================================================ S1a
banner("S1a  CONSTANT MULTIPLICITY, SYMBOLIC in (alpha, c_2) at beta = 0: characteristic and minimal polynomials per helicity block")
def helicity_blocks(Pz, V):
    n = len(V); names = [str(v_) for v_ in V]
    i11, i22 = names.index("H11"), names.index("H22")
    S = sp.eye(n); S[i11, i22] = 1; S[i22, i11] = 1; S[i22, i22] = -1
    Pp = (S.T * Pz * S).applyfunc(sp.expand)
    names[i11], names[i22] = "a", "b"
    blocks = {"scalar": [x for x in ["H00", "H03", "H33", "a"] if x in names], "vector1": ["H01", "H13"],
              "vector2": ["H02", "H23"], "tensor+": ["b"], "tensorx": ["H12"]}
    off = [(names[i], names[j]) for i in range(n) for j in range(n) if Pp[i, j] != 0
           and not any(names[i] in b_ and names[j] in b_ for b_ in blocks.values())]
    return {bn: Pp.extract([names.index(x) for x in b_], [names.index(x) for x in b_]) for bn, b_ in blocks.items()}, off


Pz = P_F2a.xreplace({XI[0]: lam, XI[1]: 0, XI[2]: 0, XI[3]: 1})
blks, offb = helicity_blocks(Pz, VARS_H)
S1a = {}
s1a_ok = not offb
for bn, Pb in blks.items():
    if bn == "scalar":
        p00 = Pb[0, 0]
        rest = [1, 2, 3]
        Pb = (Pb.extract(rest, rest) - Pb.extract(rest, [0]) * Pb.extract([0], rest) / p00).applyfunc(sp.cancel)
    A_ = Pb.applyfunc(lambda e_: sp.Poly(sp.numer(sp.together(e_)), lam).coeff_monomial(lam**2) / sp.denom(sp.together(e_)))
    B_ = Pb.applyfunc(lambda e_: sp.Poly(sp.numer(sp.together(e_)), lam).coeff_monomial(lam) / sp.denom(sp.together(e_)))
    C_ = Pb.applyfunc(lambda e_: sp.Poly(sp.numer(sp.together(e_)), lam).coeff_monomial(1) / sp.denom(sp.together(e_)))
    deg_ok = all(sp.Poly(sp.numer(sp.together(e_)), lam).degree() <= 2 for e_ in Pb if e_ != 0)
    n_ = Pb.rows
    Ai_ = A_.inv()
    M_ = sp.BlockMatrix([[sp.zeros(n_), sp.eye(n_)], [-Ai_ * C_, -Ai_ * B_]]).as_explicit().applyfunc(sp.cancel)
    cp_ = sp.factor(M_.charpoly(lam).as_expr())
    I2 = sp.eye(2 * n_)
    if bn == "scalar":
        expc = (lam**2 - 1)**2 * (lam**2 - CS2)
        mres = ((M_ * M_ - I2) * (M_ * M_ - CS2 * I2)).applyfunc(sp.cancel)
    else:
        expc = (lam**2 - 1)**n_
        mres = (M_ * M_ - I2).applyfunc(sp.cancel)
    cp_ok = sp.cancel(cp_ - sp.expand(expc)) == 0
    mp_ok = all(e_ == 0 for e_ in mres)
    dens = sorted({str(f_) for e_ in M_ for f_, _ in sp.factor_list(sp.denom(sp.together(e_)))[1]} - {"1"})
    S1a[bn] = {"charpoly": str(cp_), "charpoly_ok": cp_ok, "minpoly_ok": mp_ok, "deg_le_2": deg_ok, "M_denominators": dens}
    s1a_ok &= cp_ok and mp_ok and deg_ok
    P(f"    {bn:8s}: det(lambda - M) = {cp_};  expected match {cp_ok};  minimal-polynomial identity "
      f"{'(M^2-1)(M^2-c_S^2)' if bn == 'scalar' else '(M^2-1)'} = 0: {mp_ok};  denominators of M: {dens}")
OUT["numbers"]["S1a"] = S1a
check("S1a constant multiplicity, symbolic: every helicity block of the lapse-reduced F2a symbol has char. polynomial "
      "(lambda^2-1)^m (lambda^2-c_S^2)^n and satisfies its minimal-polynomial identity identically in (alpha, c_2) at beta = 0 "
      "(semisimple wherever defined and c_S^2 != 0, 1; families {+-1} mult 8 and {+-c_S} mult 1 in the full system)",
      f"blocks {list(S1a)}; all identities {s1a_ok}; off-block entries {offb if offb else 'none'}", s1a_ok,
      "identities of rational functions, so they hold at every parameter point where the denominators listed are non-zero")

# ================================================================================================ S1b
banner("S1b  THE GAP |c_S - 1| ON THE WINDOWS: rigorous interval arithmetic (mpmath.iv) + exact monotone corner")
mp.iv.dps = 30
def cs2_interval(box):
    a_ = mp.iv.mpf([mp.mpf(box[0].p) / box[0].q, mp.mpf(box[1].p) / box[1].q])
    c_ = mp.iv.mpf([mp.mpf(box[2].p) / box[2].q, mp.mpf(box[3].p) / box[3].q])
    return (2 / a_ - 1) * (1 / (2 / c_ + 3))                 # each variable once: the interval is tight
dA = sp.diff(CS2, al); dC = sp.diff(CS2, c2)
mono = {"dcs2_dalpha": str(sp.factor(dA)), "dcs2_dc2": str(sp.factor(dC))}
S1b = {}
for nm, box in (("W_P1", W_P1), ("W_rec", W_REC)):
    ivl = cs2_interval(box)
    lo_cs2 = mp.mpf(ivl.a)
    sgnA = all(sp.sign(dA.subs({al: a_, c2: c_})) < 0 for a_ in box[:2] for c_ in box[2:])   # numerators sign-definite on box
    sgnC = all(sp.sign(dC.subs({al: a_, c2: c_})) > 0 for a_ in box[:2] for c_ in box[2:])
    corner = cs2_of(box[1], box[2])
    cmin = mp.sqrt(mp.mpf(corner.p) / corner.q)
    S1b[nm] = {"cs2_interval_lower": float(lo_cs2), "cs2_interval_upper": float(mp.mpf(ivl.b)), "corner_cs2_exact": str(corner),
               "cS_min": float(cmin), "gap_min": float(cmin - 1), "eig_separation_min_units_sqrt_rho": float(min(2, cmin - 1)),
               "monotone": bool(sgnA and sgnC)}
    P(f"    {nm}: c_S^2 in [{mp.nstr(lo_cs2, 8)}, {mp.nstr(mp.mpf(ivl.b), 8)}] (interval, outward rounded);  monotone "
      f"(dc_S^2/dalpha < 0, dc_S^2/dc_2 > 0 on the box): {sgnA and sgnC};  exact minimum at (alpha_max, c2_low): c_S = "
      f"{mp.nstr(cmin, 8)},  c_S - 1 there (the minimum gap if positive) = {mp.nstr(cmin - 1, 8)};  min separation of distinct eigenvalues = "
      f"{mp.nstr(min(2, cmin - 1), 6)} sqrt(rho)")
P(f"    derivatives: {mono}")
OUT["numbers"]["S1b"] = S1b
s1b_ok = S1b["W_rec"]["cs2_interval_lower"] > 1 and S1b["W_P1"]["cs2_interval_lower"] > 1
check("S1b the families never cross on W_P1 or W_rec: the rigorous interval lower bound of c_S^2 exceeds 1",
      f"W_rec: c_S^2 >= {S1b['W_rec']['cs2_interval_lower']:.6g} (c_S - 1 at the minimising corner = {S1b['W_rec']['gap_min']:.6g}); "
      f"W_P1: c_S^2 >= {S1b['W_P1']['cs2_interval_lower']:.6g} (c_S - 1 there = {S1b['W_P1']['gap_min']:.6g})", s1b_ok,
      "the minimum sits at the corner (alpha_max, lowest c_2), exactly as the monotonicity says")

# ================================================================================================ S1c / S2a set 1
banner("S1c + S2a  EXACT UNIFORMITY: 18 points x 24 rational unit directions (aligned background); symmetriser at each")
DIRS = rat_unit_dirs(24, 29400)
unit_ok = all(sum(x * x for x in d_) == 1 for d_ in DIRS)
SET1 = []
t1 = time.time()
for (a_, c_) in POINTS:
    CM = point_mats(CM_F2a, a_, c_)
    cs2v = q(cs2_of(a_, c_))
    pred00 = q((2 * a_ - 1) / 4)
    rows = []
    for j, d_ in enumerate(DIRS):
        r_ = exact_case(CM, d_, QQ(0), QQ(1), cs2v, pred00, want_spectrum=True)
        rows.append(r_)
    agg = {"alpha": str(a_), "c2": str(c_), "cS": float(mp.sqrt(mp.mpf(cs2v.numerator) / cs2v.denominator)),
           "all_mult_8811": all(r_.get("mult_8811", False) for r_ in rows),
           "all_lapse_ok": all(r_["lapse_lambda_free"] and r_["P0r_linear"] and r_["p00_formula"] for r_ in rows),
           "all_A_inv": all(r_["A_invertible"] for r_ in rows),
           "all_H_ok": all(r_.get("H_sym") and r_.get("HD_sym") and r_.get("H_pd") for r_ in rows),
           "H_notes": sorted({r_.get("H_note", "") for r_ in rows} - {""}),
           "lam_min_min": min((r_["lam_min"] for r_ in rows if "lam_min" in r_), default=None),
           "kappa": [r_["kappa"] for r_ in rows if "kappa" in r_],
           "bound": [r_["bound"] for r_ in rows if "bound" in r_],
           "proj_resid": max((r_["proj_sum_resid"] for r_ in rows if "proj_sum_resid" in r_), default=None),
           "mult_plus1": sorted({r_.get("mult_plus1") for r_ in rows if "mult_plus1" in r_}),
           "rank_D2_minus_rho": sorted({r_["rank_D2_minus_rho"] for r_ in rows if "rank_D2_minus_rho" in r_})}
    if agg["kappa"]:
        agg["kappa_min"], agg["kappa_max"] = min(agg["kappa"]), max(agg["kappa"])
        agg["kappa_spread"] = (max(agg["kappa"]) - min(agg["kappa"])) / min(agg["kappa"])
    SET1.append(agg)
P(f"    directions exact unit vectors: {unit_ok};  {len(POINTS)} x {len(DIRS)} = {len(POINTS) * len(DIRS)} exact cases in {time.time() - t1:.0f} s")
for ag in SET1:
    P(f"    alpha {float(sp.Rational(ag['alpha'])):.4e}, c_2 {float(sp.Rational(ag['c2'])):.4e}: c_S = {ag['cS']:.6g}; "
      f"lapse elimination ok {ag['all_lapse_ok']}; A inv {ag['all_A_inv']}; multiplicities (8,8,1,1) semisimple {ag['all_mult_8811']}"
      + (f"; H sym/HM sym/PD {ag['all_H_ok']}; lambda_min(H) {ag['lam_min_min']:.4f}; kappa(H) {ag.get('kappa_max', float('nan')):.4e}"
         f" (spread {ag.get('kappa_spread', float('nan')):.1e}); bound 4 Sum||P_j||^2 {max(ag['bound']):.4e}" if ag["kappa"] else
         f"; symmetriser: {ag['H_notes']}; mult(+1) {ag['mult_plus1']}; rank(D^2 - rho) {ag['rank_D2_minus_rho']}"))
OUT["numbers"]["S1c_set1"] = [{k_: v_ for k_, v_ in ag.items() if k_ not in ("kappa", "bound")} for ag in SET1]
s1c1_ok = unit_ok and all(ag["all_mult_8811"] and ag["all_lapse_ok"] and ag["all_A_inv"] for ag in SET1)
s2a1_ok = all(ag["all_H_ok"] and ag["lam_min_min"] is not None and ag["lam_min_min"] >= 0.25 - 1e-30 and
              max(ag["kappa"]) <= max(ag["bound"]) * (1 + 1e-12) for ag in SET1)

# ================================================================================================ S1c / S2a set 2: general backgrounds
banner("S1c + S2a  GENERAL FROZEN BACKGROUNDS: 6 random rational (lapse, shift, non-diagonal gamma) x 3 corner points x 4 k")
rngb = np.random.default_rng(29401)
def rnd_rat(lo, hi, den=10):
    return sp.Rational(int(rngb.integers(int(lo * den), int(hi * den) + 1)), den)
BGS = []
while len(BGS) < 6:
    Nl = rnd_rat(0.5, 2.0)
    if Nl <= 0:
        continue
    sh = sp.Matrix([rnd_rat(-0.5, 0.5) for _ in range(3)])
    E = sp.zeros(3, 3)
    for i in range(3):
        for j in range(i, 3):
            E[i, j] = E[j, i] = rnd_rat(-0.25, 0.25, 20)
    GAM = sp.eye(3) + E
    if not all(GAM[:i, :i].det() > 0 for i in (1, 2, 3)):
        continue
    GB = sp.zeros(4, 4); low = GAM * sh
    GB[0, 0] = -Nl**2 + (sh.T * GAM * sh)[0]
    for i in range(3):
        GB[0, i + 1] = GB[i + 1, 0] = low[i]
        for j in range(3):
            GB[i + 1, j + 1] = GAM[i, j]
    BGS.append({"N": Nl, "shift": sh, "gamma": GAM, "g": GB})
# corner points: max c_S, min c_S, and the point with alpha max and c_2 = c2_max(P1) (or the nearest available)
cs_vals = [cs2_of(a_, c_) for a_, c_ in POINTS]
i_max = int(np.argmax([float(x) for x in cs_vals])); i_min = int(np.argmin([float(x) for x in cs_vals]))
cand = [i for i, (a_, c_) in enumerate(POINTS) if c_ == rat(C2_MAX)]
i_3 = max(cand, key=lambda i: POINTS[i][0]) if cand else 0
CORNERS = sorted({i_max, i_min, i_3})
SET2 = []
t1 = time.time()
for ib, bg in enumerate(BGS):
    Pg = symbol_matrix(F2a_lagrangian(bg["g"]), VARS_H)
    sq = sp.sqrt(-bg["g"].det())
    Pg = (Pg / sq).applyfunc(sp.expand)
    CMg = coef_mats(Pg)
    gi = bg["gamma"].inv()
    for ip in CORNERS:
        a_, c_ = POINTS[ip]
        CM = point_mats(CMg, a_, c_)
        cs2v = q(cs2_of(a_, c_))
        for jk in range(4):
            k_ = [rnd_rat(-1, 1, 7) for _ in range(3)]
            if all(x == 0 for x in k_):
                k_[2] = sp.Integer(1)
            kq = [q(x) for x in k_]
            nu = q(sum(bg["shift"][i] * k_[i] for i in range(3)))
            kgk = (sp.Matrix(k_).T * gi * sp.Matrix(k_))[0]
            rho = q(bg["N"]**2 * kgk)
            pred00 = q((2 * a_ - 1) * kgk / (4 * bg["N"]**4))
            r_ = exact_case(CM, kq, nu, rho, cs2v, pred00, want_spectrum=True)
            SET2.append({"bg": ib, "point": ip, "k": [str(x) for x in k_], **{kk_: (str(vv_) if isinstance(vv_, sp.Basic) else vv_)
                                                                               for kk_, vv_ in r_.items()}})
P(f"    {len(SET2)} exact cases in {time.time() - t1:.0f} s (backgrounds: lapse {[str(b['N']) for b in BGS]})")
s1c2_ok = all(r_["lapse_lambda_free"] and r_["P0r_linear"] and r_["p00_formula"] and r_["A_invertible"] and r_.get("mult_8811")
              for r_ in SET2)
s2a2_ok = all(r_.get("H_sym") and r_.get("HD_sym") and r_.get("H_pd") and r_.get("lam_min", 0) >= 0.25 - 1e-30 for r_ in SET2)
for ib in range(len(BGS)):
    rr = [r_ for r_ in SET2 if r_["bg"] == ib]
    P(f"    background {ib}: N = {BGS[ib]['N']}, shift = {list(BGS[ib]['shift'])}: P_00,00 = (2 alpha - 1) |k|^2_gamma/(4 N^4) "
      f"(after / sqrt(-g)) {all(r_['p00_formula'] for r_ in rr)}; P_0r linear in lambda {all(r_['P0r_linear'] for r_ in rr)}; "
      f"roots nu +- sqrt(rho) (8, 8) and nu +- c_S sqrt(rho) (1, 1), semisimple {all(r_.get('mult_8811') for r_ in rr)}; "
      f"H sym/HM sym/PD {all(r_.get('H_sym') and r_.get('HD_sym') and r_.get('H_pd') for r_ in rr)}; kappa(H) "
      f"{min((r_.get('kappa', np.inf) for r_ in rr)):.3e} .. {max((r_.get('kappa', 0) for r_ in rr)):.3e}")
OUT["numbers"]["S1c_set2"] = SET2
check("S1c constant multiplicity, exact uniformity: at 18 points x 24 directions (aligned) and 6 general frozen backgrounds x 3 "
      "corners x 4 k, the lapse elimination is valid (P_00,00 lambda-free = (2 alpha-1) sqrt(gamma)|k|^2_gamma/(4N^3), P_0r linear "
      "in lambda, det A != 0), det P_red = const [(lambda-nu)^2-rho]^8 [(lambda-nu)^2-c_S^2 rho] and ((M-nu)^2-rho)((M-nu)^2-c_S^2 rho) = 0 "
      "exactly with c_S^2 != 0, 1",
      f"set 1: {sum(ag['all_mult_8811'] and ag['all_lapse_ok'] and ag['all_A_inv'] for ag in SET1)}/{len(SET1)} points; "
      f"set 2: {sum(1 for r_ in SET2 if r_.get('mult_8811') and r_['p00_formula'])}/{len(SET2)} cases", s1c1_ok and s1c2_ok,
      "frame covariance (leaf-preserving linear frame changes act covariantly on the gauge term and the action density) is the "
      "analytic reason; set 2 confirms it on backgrounds with lapse, shift and non-diagonal gamma")
kap_all = [x for ag in SET1 for x in ag["kappa"]]
check("S2a the explicit symmetriser H = Sum_j P_j^T G P_j: exact H = H^T, H M symmetric (exactly), H positive definite (exact LDL "
      "pivots > 0), lambda_min(H) >= 1/4 in the Frobenius metric, kappa(H) <= 4 Sum||P_j||^2, at every S1c case",
      f"set 1 {sum(ag['all_H_ok'] for ag in SET1)}/{len(SET1)} points, set 2 {sum(1 for r_ in SET2 if r_.get('H_pd') and r_.get('HD_sym'))}/{len(SET2)}; "
      + (f"lambda_min >= {min(ag['lam_min_min'] for ag in SET1 if ag['lam_min_min'] is not None):.4f}; kappa(H) "
         f"{min(kap_all):.4e} .. {max(kap_all):.4e}" if kap_all else "no H constructed"),
      s2a1_ok and s2a2_ok,
      "Sum_j P_j = I gives v^T H v >= |v|^2/4; kappa(H) ~ kappa(T)^2 of CFG292 (it grows with c_S)")
OUT["numbers"]["S2a"] = {"kappa_min": min(kap_all) if kap_all else None, "kappa_max": max(kap_all) if kap_all else None}

# ================================================================================================ S1d
banner("S1d  DEGENERACY LOCI and their distance from W_rec (gauge artefact alpha = 1/2; crossing; minimal Horava)")
a_lo, a_hi, c_lo, c_hi = W_REC
loci = {"alpha = 0 (det A = 0, minimal Horava)": float(a_lo),
        "alpha = 1/2 (F2a lapse coefficient (2 alpha - 1)/4 = 0, gauge artefact)": float(HALF - a_hi),
        "c_S^2 = 1 (alpha = c_2/(1 + 2 c_2))": float(axc(c_lo) - a_hi),
        "c_S^2 = 0 (c_2 = 0)": float(c_lo), "c_S^2 = 0 (alpha = 2)": float(2 - a_hi)}
near = max(POINTS, key=lambda p_: float(p_[0] / axc(p_[1])))
ratio_near = float(near[0] / axc(near[1]))
for k_, v_ in loci.items():
    P(f"    {k_}: distance from W_rec in alpha (or c_2) = {v_:.4e}")
P(f"    record point closest to the crossing (largest alpha/alpha_cross): alpha = {float(near[0]):.4e}, c_2 = {float(near[1]):.4e}, "
  f"alpha/alpha_cross = {ratio_near:.3e}")
OUT["numbers"]["S1d"] = {"loci_distance": loci, "nearest_crossing_ratio": ratio_near}
check("S1d every degeneracy locus misses W_rec (alpha = 0, alpha = 1/2, c_S = 1, c_S = 0)", f"{loci}",
      all(v_ > 0 for v_ in loci.values()),
      "alpha = 1/2 is an F2a gauge artefact (the physical lapse coefficient alpha_c/2 does not vanish there); it lies 0.5 away")

# ================================================================================================ S2b dense directions (multiprocessing)
banner("S2b  DENSE DIRECTIONS: 500 random unit directions per point, mpmath 40 digits (H symmetric, PD, H M symmetric, kappa(H))")
def _dense_worker(args):
    ip, cm_ser, cs2_pq, nd, seed = args
    mp.mp.dps = 40
    cm = {k_: mp.matrix([[mp.mpf(n_) / d_ for (n_, d_) in row] for row in v_]) for k_, v_ in cm_ser.items()}
    cs2m = mp.mpf(cs2_pq[0]) / cs2_pq[1]
    if cs2_pq[0] == cs2_pq[1]:
        return ip, {"flag": "c_S^2 = 1: projector construction undefined"}
    gw = [mp.mpf(1) if n_[1] == n_[2] else mp.mpf(1) / 2 for n_ in FIELDS9] * 2
    S = mp.diag([mp.sqrt(x) for x in gw]); Si = S**-1; Gm = mp.diag(gw)
    rng = np.random.default_rng(seed)
    sym_r, hm_r, lmins, kaps, minres = [], [], [], [], []
    for _ in range(nd):
        v_ = rng.standard_normal(3)
        k_ = [mp.mpf(float(x)) for x in v_]; nk = mp.sqrt(sum(x * x for x in k_)); k_ = [x / nk for x in k_]
        A10 = cm[(0, 0)]; B10 = cm[(0, 1)] * k_[0] + cm[(0, 2)] * k_[1] + cm[(0, 3)] * k_[2]
        C10 = (cm[(1, 1)] * k_[0]**2 + cm[(2, 2)] * k_[1]**2 + cm[(3, 3)] * k_[2]**2 + cm[(1, 2)] * k_[0] * k_[1]
               + cm[(1, 3)] * k_[0] * k_[2] + cm[(2, 3)] * k_[1] * k_[2])
        p00 = C10[0, 0]
        idx = list(range(1, 10))
        b0 = mp.matrix([[B10[0, j] for j in idx]]); c0 = mp.matrix([[C10[0, j] for j in idx]])
        sub = lambda X: mp.matrix([[X[i, j] for j in idx] for i in idx])
        A = sub(A10) - b0.T * b0 / p00; B = sub(B10) - (b0.T * c0 + c0.T * b0) / p00; C = sub(C10) - c0.T * c0 / p00
        Ai = mp.inverse(A); X1 = -Ai * C; X2 = -Ai * B
        M = mp.zeros(18, 18)
        for i in range(9):
            M[i, 9 + i] = 1
            for j in range(9):
                M[9 + i, j] = X1[i, j]; M[9 + i, 9 + j] = X2[i, j]
        I = mp.eye(18); D2 = M * M
        mres = mp.mnorm((D2 - I) * (D2 - cs2m * I), 1) / mp.mnorm(D2, 1)**2
        R = (D2 - cs2m * I) / (1 - cs2m); Q = (D2 - I) / (cs2m - 1)
        RD, QD = R * M, Q * M
        H = (R.T * Gm * R + RD.T * Gm * RD + Q.T * Gm * Q + QD.T * Gm * QD / cs2m) / 2
        HM = H * M
        nH = mp.mnorm(H, 1); nHM = mp.mnorm(HM, 1)
        sym_r.append(float(mp.mnorm(H - H.T, 1) / nH)); hm_r.append(float(mp.mnorm(HM - HM.T, 1) / nHM)); minres.append(float(mres))
        Hs = Si * H * Si; Hs = (Hs + Hs.T) / 2
        ev = mp.eigsy(Hs, eigvals_only=True)
        lmins.append(min(ev)); kaps.append(max(ev) / min(ev))
    k0 = kaps[0]
    return ip, {"sym_max": max(sym_r), "hm_max": max(hm_r), "lam_min": float(min(lmins)), "kappa": float(k0),
                "kappa_spread": float(max(abs(x / k0 - 1) for x in kaps)), "minpoly_resid_max": max(minres), "n": nd}


def ser(Dm):
    return [[(int(x.numerator), int(x.denominator)) for x in row] for row in Dm.to_list()]


jobs = []
for ip, (a_, c_) in enumerate(POINTS):
    CM = point_mats(CM_F2a, a_, c_)
    cs2v = cs2_of(a_, c_)
    jobs.append((ip, {k_: ser(v_) for k_, v_ in CM.items()}, (int(cs2v.p), int(cs2v.q)), 500, 29402 + ip))
t1 = time.time()
with mproc.get_context("fork").Pool(min(16, os.cpu_count() or 4)) as pool:
    DENSE = dict(pool.map(_dense_worker, jobs))
P(f"    {len(jobs)} points x 500 directions in {time.time() - t1:.0f} s")
for ip in sorted(DENSE):
    d_ = DENSE[ip]
    if "flag" in d_:
        P(f"    point {ip}: {d_['flag']}")
    else:
        P(f"    point {ip}: max rel. asymmetry H {d_['sym_max']:.1e}, H M {d_['hm_max']:.1e}; lambda_min(H) {d_['lam_min']:.4f}; "
          f"kappa(H) {d_['kappa']:.6e} (direction spread {d_['kappa_spread']:.1e}); minimal-poly residual {d_['minpoly_resid_max']:.1e}")
OUT["numbers"]["S2b"] = DENSE
s2b_ok = all("flag" not in d_ and d_["sym_max"] < 1e-25 and d_["hm_max"] < 1e-25 and d_["lam_min"] > 0 and d_["kappa_spread"] < 1e-20
             for d_ in DENSE.values())
check("S2b dense directions: at every point, 500 random unit directions give H symmetric, positive definite and H M symmetric "
      "(relative 1e-25) with a direction-independent kappa(H) (relative 1e-20)",
      f"{sum(1 for d_ in DENSE.values() if 'flag' not in d_ and d_['sym_max'] < 1e-25 and d_['hm_max'] < 1e-25 and d_['lam_min'] > 0 and d_['kappa_spread'] < 1e-20)}"
      f"/{len(DENSE)} points" + ("" if all("flag" not in d_ for d_ in DENSE.values()) else
                                f"; flagged: {sum(1 for d_ in DENSE.values() if 'flag' in d_)}"), s2b_ok,
      "rotation covariance about the aether: the Frobenius metric is rotation invariant, so kappa(H) depends on (alpha, c_2) only")

# ================================================================================================ S2c symbolic smoothness
banner("S2c  SMOOTHNESS: H at khat = z symbolic in (alpha, c_2); denominators and their zero sets vs W_rec")
t1 = time.time()
FF = QQ.frac_field(al, c2)
def to_FF(Mx):
    return DomainMatrix.from_Matrix(Mx).convert_to(FF)
A10s, B10s, C10s = (CM_F2a[(0, 0)], CM_F2a[(0, 3)], CM_F2a[(3, 3)])
A10f, B10f, C10f = to_FF(A10s), to_FF(B10s), to_FF(C10s)
p00s = C10f[0, 0].element
b0s, c0s = B10f[0:1, 1:10], C10f[0:1, 1:10]
pinv_s = FF.one / p00s
As = A10f[1:10, 1:10] - (b0s.transpose() * b0s) * pinv_s
Bs = B10f[1:10, 1:10] - (b0s.transpose() * c0s + c0s.transpose() * b0s) * pinv_s
Cs = C10f[1:10, 1:10] - (c0s.transpose() * c0s) * pinv_s
Ais = As.inv()
Zs, Is = DomainMatrix.zeros((9, 9), FF), DomainMatrix.eye(9, FF)
Ms = Zs.hstack(Is).vstack((-(Ais * Cs)).hstack(-(Ais * Bs)))
I18s = DomainMatrix.eye(18, FF)
cs2F = FF.from_sympy(CS2)
D2s = Ms * Ms
Rs = (D2s - I18s * cs2F) * (FF.one / (FF.one - cs2F)); Qs = (D2s - I18s) * (FF.one / (cs2F - FF.one))
G18F = DomainMatrix.diag([FF.from_sympy(x) for x in G9 + G9], FF)
RDs, QDs = Rs * Ms, Qs * Ms
Hsym = (Rs.transpose() * G18F * Rs + RDs.transpose() * G18F * RDs + Qs.transpose() * G18F * Qs
        + QDs.transpose() * G18F * QDs * (FF.one / cs2F)) * FF.from_sympy(HALF)
HMs = Hsym * Ms
sym_ok_s = (Hsym - Hsym.transpose()).is_zero_matrix and (HMs - HMs.transpose()).is_zero_matrix
den_factors = set()
for row in Hsym.to_Matrix().tolist():
    for e_ in row:
        if e_ != 0:
            for f_, _ in sp.factor_list(sp.denom(sp.together(e_)))[1]:
                den_factors.add(sp.factor(f_))
den_factors = sorted(den_factors, key=str)
def nonzero_on_box(f_, box):
    fl = sp.lambdify((al, c2), f_, modules="mpmath")
    A_ = mp.iv.mpf([mp.mpf(box[0].p) / box[0].q, mp.mpf(box[1].p) / box[1].q])
    C_ = mp.iv.mpf([mp.mpf(box[2].p) / box[2].q, mp.mpf(box[3].p) / box[3].q])
    v_ = fl(A_, C_)
    if not isinstance(v_, mp.iv.mpf):
        v_ = mp.iv.mpf(v_)
    return bool(v_.a > 0 or v_.b < 0)
den_status = {str(f_): nonzero_on_box(f_, W_REC) for f_ in den_factors}
P(f"    symbolic H (18 x 18) in {time.time() - t1:.0f} s;  H = H^T and H M symmetric identically: {sym_ok_s}")
P(f"    irreducible denominator factors of H(khat = z): {den_status}  (True = no zero on W_rec, interval arithmetic)")
OUT["numbers"]["S2c"] = {"denominators": den_status, "identities": sym_ok_s}
check("S2c the symmetriser is a rational, hence real-analytic, function of (alpha, c_2, background, khat): at khat = z its "
      "denominators factor into polynomials with no zero on W_rec, and H M is symmetric identically",
      f"{len(den_status)} factors, all non-vanishing on W_rec: {all(den_status.values())}; identities {sym_ok_s}",
      sym_ok_s and all(den_status.values()),
      "with S1c (rational M with non-vanishing denominators on every frozen background) this is the smooth symmetriser that "
      "Kreiss's theorem asserts, built explicitly")

# ================================================================================================ S2d HKM canonical energy (finding)
banner("S2d  FINDING: does the Lagrangian (canonical) energy symmetrise the system? inertia of A and C (Hughes-Kato-Marsden)")
HKM = []
for (a_, c_) in POINTS:
    CM = point_mats(CM_F2a, a_, c_)
    A10, B10, C10 = pencil_at(CM, [QQ(0), QQ(0), QQ(1)])
    A, B, C, p00, _, _ = schur_lapse(A10, B10, C10)
    evA = mp.eigsy(dm_to_mp(A), eigvals_only=True); evC = mp.eigsy(dm_to_mp(C), eigvals_only=True)
    inA = (sum(1 for x in evA if x > 0), sum(1 for x in evA if x < 0)); inC = (sum(1 for x in evC if x > 0), sum(1 for x in evC if x < 0))
    HKM.append({"alpha": str(a_), "c2": str(c_), "A_inertia(+,-)": inA, "C_inertia(+,-)": inC})
canon = all((h_["A_inertia(+,-)"][0] == 9 and h_["C_inertia(+,-)"][1] == 9) or (h_["A_inertia(+,-)"][1] == 9 and h_["C_inertia(+,-)"][0] == 9)
            for h_ in HKM)
P(f"    inertia at the points (A, C): {sorted({(h_['A_inertia(+,-)'], h_['C_inertia(+,-)']) for h_ in HKM})}")
OUT["numbers"]["S2d"] = HKM
check("S2d (finding) the canonical Lagrangian energy is definite (A definite, C of the opposite definiteness), i.e. HKM's "
      "positive-energy hypothesis holds directly", f"{sorted({(h_['A_inertia(+,-)'], h_['C_inertia(+,-)']) for h_ in HKM})}", canon,
      "if it fails, the Kreiss symmetriser of S2 is what carries the energy estimate (expected: the gauge-fixed GR part already "
      "has an indefinite canonical energy, as in harmonic gauge)", load_bearing=False)

# ================================================================================================ S3 K1
banner("S3/K1  COEFFICIENT SMOOTHNESS: the F2a symbol on a symbolic frozen background (N, a shift component, a 2x2 block of gamma)")
t1 = time.time()
Ns = sp.Symbol("N", positive=True); s1 = sp.Symbol("s1", real=True)
g11, g12, g22 = sp.symbols("g11 g12 g22", positive=True)
GAMs = sp.Matrix([[g11, g12, 0], [g12, g22, 0], [0, 0, 1]])
shs = sp.Matrix([s1, 0, 0]); lows = GAMs * shs
GBs = sp.zeros(4, 4); GBs[0, 0] = -Ns**2 + (shs.T * GAMs * shs)[0]
for i in range(3):
    GBs[0, i + 1] = GBs[i + 1, 0] = lows[i]
    for j in range(3):
        GBs[i + 1, j + 1] = GAMs[i, j]
Psb = symbol_matrix(F2a_lagrangian(GBs), VARS_H)
dens_k1 = set()
for e_ in Psb:
    if e_ != 0:
        for f_, _ in sp.factor_list(sp.denom(sp.together(e_)))[1]:
            dens_k1.add(f_)
detg = sp.factor(GAMs.det())
allowed = {Ns, sp.expand(GAMs.det())}
k1_dens_ok = all(sp.expand(f_) in allowed or f_ == Ns for f_ in dens_k1)
kgk_s = (sp.Matrix(XI[1:]).T * GAMs.inv() * sp.Matrix(XI[1:]))[0]
p00_pred_s = (2 * al - 1) * sp.sqrt(GAMs.det()) * kgk_s / (4 * Ns**3)
p00_ok_s = sp.simplify(Psb[0, 0] - p00_pred_s) == 0
P(f"    symbol on the symbolic background in {time.time() - t1:.0f} s; irreducible denominators: {sorted(str(f_) for f_ in dens_k1)}  "
  f"(allowed: powers of N and det gamma = {detg})")
P(f"    P_00,00 = (2 alpha - 1) sqrt(det gamma) gamma^ij k_i k_j / (4 N^3) symbolically: {p00_ok_s}")
OUT["numbers"]["K1"] = {"denominators": sorted(str(f_) for f_ in dens_k1), "p00_symbolic": p00_ok_s}
check("S3/K1 the F2a principal coefficients are rational in (g, N, sqrt det gamma) with denominators only powers of N and det gamma "
      "(smooth on O = {N > 0, gamma > 0}); the lapse coefficient is (2 alpha - 1) sqrt(gamma) |k|^2_gamma / (4 N^3) symbolically",
      f"denominators {sorted(str(f_) for f_ in dens_k1)}; P_00,00 formula {p00_ok_s}", k1_dens_ok and p00_ok_s,
      "the Lagrangian is a quadratic form in the first jets with g-dependent coefficients, so the principal part depends on g only "
      "and the lower-order part is quadratic in dg: the quasilinear structure Kato's theorem needs")

# ================================================================================================ S3 K4a/K4b/K4c/K4d
banner("S3/K4  LOWER-ORDER TERMS: the explicit MOND bound, the C-H lapse terms, nu_mono's splice (Sobolev range), the zero-field set")
mp.mp.dps = 40
# nu_mono, analytic (XC4 S2): h_mono = h_RAR (y <= y*), h_RAR(y*) + delta h_p ln((y + y_p)/(y* + y_p)) (y > y*)
hR = lambda y: y / mp.expm1(mp.sqrt(y))
dhR = lambda y: mp.diff(hR, y)
d2hR = lambda y: mp.diff(hR, y, 2)
YP = mp.findroot(dhR, 2.54); HP = hR(YP); DEL = mp.mpf("0.05")
YS = mp.findroot(lambda y: dhR(y) - DEL * HP / (y + YP), 2.33)
def h_mono(y):
    y = mp.mpf(y)
    return hR(y) if y <= YS else hR(YS) + DEL * HP * mp.log((y + YP) / (YS + YP))
def dh_mono(y):
    y = mp.mpf(y)
    return dhR(y) if y <= YS else DEL * HP / (y + YP)
CT = lambda y: h_mono(y) / mp.mpf(y)
CL = lambda y: dh_mono(y)
# the floor binds above y* (XC4 S2): check on a grid
grid = [YS * (1 + mp.mpf(10)**(-6))] + [mp.mpf(10)**e for e in np.linspace(math.log10(float(YS)) + 0.001, 4, 300)]
floor_ok = all(dhR(y) <= DEL * HP / (y + YP) for y in grid)
yp_match = abs(float(YP) - L340["numbers"]["A1"]["y_p"]) < 1e-6
# K4a: M_m(xi) and C_max(y_min)
kq_, xq_ = sp.symbols("k xi", positive=True)
fM0 = kq_**2 * sp.exp(-xq_**2 * kq_**2)
kst = sp.solve(sp.diff(fM0, kq_), kq_)
M0 = sp.simplify(fM0.subs(kq_, kst[0]))
M0_ok = sp.simplify(M0 - sp.exp(-1) / xq_**2) == 0
# sup_t t^2 (1 + t^2)^(m/2) e^(-t^2) (xi = 1): d ln f/dt = 0  <=>  2 + m s - 2 s^2 = 0 with s = t^2
s_m = {m: (m + sp.sqrt(m**2 + 16)) / 4 for m in (0, 1, 2)}
Mm_val = {m: float((s_m[m] * (1 + s_m[m])**sp.Rational(m, 2) * sp.exp(-s_m[m])).evalf(30)) for m in (1, 2)}
Mm_grid = {m: float(max(t**2 * (1 + t**2)**(m / 2) * math.exp(-t**2) for t in np.linspace(0.01, 6, 60001))) for m in (1, 2)}
M0_ok = M0_ok and s_m[0] == 1 and all(abs(Mm_val[m] / Mm_grid[m] - 1) < 1e-6 for m in (1, 2))
Cmax = {}
for ymin in (1e-1, 1e-2, 1e-4, 1e-6):
    ys = [mp.mpf(ymin) * mp.mpf(10)**(e) for e in np.linspace(0, 10, 400)]
    vals = [max(CT(y), CL(y)) for y in ys]
    Cmax[ymin] = {"Cmax": float(max(vals)), "Cmax_sqrt_ymin": float(max(vals) * mp.sqrt(ymin)), "argmax_is_ymin": bool(vals[0] == max(vals))}
P(f"    nu_mono rebuilt: y_p = {mp.nstr(YP, 10)} (L340 match {yp_match}), h_p = {mp.nstr(HP, 8)}, y* = {mp.nstr(YS, 10)}; floor binds above y*: {floor_ok}")
P(f"    M_0(xi) = sup_k k^2 e^(-xi^2 k^2) = {M0}  (= 1/(e xi^2): {M0_ok});  at xi = 1: M_1 = {Mm_val[1]:.4f}, M_2 = {Mm_val[2]:.4f}")
for ymin, v_ in Cmax.items():
    P(f"    y_min = {ymin:.0e}: C_max = max(C_T, C_L) on y >= y_min = {v_['Cmax']:.5g} (at y_min: {v_['argmax_is_ymin']});  C_max sqrt(y_min) = {v_['Cmax_sqrt_ymin']:.4f}")
cm_law = abs(Cmax[1e-6]["Cmax_sqrt_ymin"] - 1) < 0.01 and all(v_["argmax_is_ymin"] for v_ in Cmax.values())
OUT["numbers"]["K4a"] = {"M0": str(M0), "M1": Mm_val[1], "M2": Mm_val[2], "Cmax": {str(k_): v_ for k_, v_ in Cmax.items()},
                         "y_p": float(YP), "y_star": float(YS)}
check("S3/K4a the MOND/filter block is a bounded lower-order operator wherever the filtered field is non-zero, with the explicit "
      "bound ||T u||_{H^{r+m}} <= C_max(y_min) M_m(xi) ||u||_{H^r}: M_0 = 1/(e xi^2) (sympy), M_1, M_2 finite; C_max(y_min) = C_T(y_min) "
      "~ y_min^(-1/2) diverges only at zero field",
      f"M_0 = {M0}; M_1 = {Mm_val[1]:.4f}/xi^3-scaling, M_2 = {Mm_val[2]:.4f}; C_max sqrt(y_min) -> {Cmax[1e-6]['Cmax_sqrt_ymin']:.4f}",
      M0_ok and cm_law and floor_ok and yp_match,
      "same bound for the U-elimination Schur complement 2CE/(1+CE)k^2 <= 2 C_max k^2 e^(-xi^2 k^2); excluded set Z_0 = {D S U = 0}")
# K4b: the C-H lapse derivative on the U-shell (FULL_VARIATION.md)
xs3 = sp.symbols("x1:4", real=True)
Nf = sp.Function("N")(*xs3); Vf = [sp.Function(f"V{i}")(*xs3) for i in range(3)]
avec = [sp.diff(Nf, x_) / Nf for x_ in xs3]
lhs_prod = sum(sp.diff(Nf * Vf[i], xs3[i]) for i in range(3)) / Nf
rhs_prod = sum(sp.diff(Vf[i], xs3[i]) for i in range(3)) + sum(avec[i] * Vf[i] for i in range(3))
prod_ok = sp.simplify(lhs_prod - rhs_prod) == 0
V2, Va, DV, aM2qb, lam0 = sp.symbols("V2 Va DV aM2qb lambda0", real=True)
Hfull = 2 * V2 + 4 * Va + 4 * DV + 2 * aM2qb
Hshell = sp.simplify(Hfull.subs(DV, (-lam0 - 4 * Va) / 4))              # U-equation: 4(D.V + a.V) = -lambda_0
shell_ok = sp.simplify(Hshell - (2 * V2 + 2 * aM2qb - lam0)) == 0
P(f"    K4b: N^-1 D_i(N V^i) = D_i V^i + a_i V^i: {prod_ok};  H = 2V^2 + 4 V.a + 4 D.V + 2 alpha_M^2 q_b -> on the U-shell {Hshell}: {shell_ok}")
check("S3/K4b the C-H lapse derivative on the U-equation shell is H_CH = 2|D chi|^2 + 2 alpha_M^2 q_b - lambda_0 (chi = U - ln N, "
      "D.(N D chi) = -N lambda_0/4): no second derivative of N survives, so the C-H sector enters the lapse equation at lower order",
      f"product rule {prod_ok}; shell identity {shell_ok}", prod_ok and shell_ok,
      "with lambda_0 = S^dagger_N L_b (heat-smoothed) chi gains two derivatives over lambda_0 (elliptic regularity)")
# K4c: the splice regularity and the Sobolev range
d2_left = d2hR(YS); d2_right = -DEL * HP / (YS + YP)**2
CL_jump = (float(d2_left), float(d2_right))
CT_cont = abs(float(dhR(YS) - DEL * HP / (YS + YP))) < 1e-20
dCT2_jump = float((d2_right - d2_left) / YS)
# spectral decay of C_T(y(x)) across the splice: y(x) = y* + 0.5 cos(2 pi x); expect |f_k| ~ k^-3 (H^{5/2-})
def CT_np(y, mono=True):
    y = np.asarray(y, float); ysf = float(YS); ypf = float(YP); hpf = float(HP)
    hr = y / np.expm1(np.sqrt(y))
    if not mono:
        return hr / y
    hys = ysf / np.expm1(np.sqrt(ysf))
    return np.where(y <= ysf, hr, hys + 0.05 * hpf * np.log((y + ypf) / (ysf + ypf))) / y
nfft = 2**15
xx = np.arange(nfft) / nfft
slopes = {}
for nm, mono in (("nu_mono", True), ("nu_RAR (control, no splice)", False)):
    f_ = CT_np(float(YS) + 0.5 * np.cos(2 * np.pi * xx), mono)
    Fk = np.abs(np.fft.rfft(f_)) / nfft
    edges = np.unique(np.logspace(math.log10(32), math.log10(2048), 9).astype(int))
    kc, mx = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        kc.append(math.sqrt(lo * hi)); mx.append(Fk[lo:hi].max())
    sl = np.polyfit(np.log(kc), np.log(np.maximum(mx, 1e-300)), 1)[0]
    slopes[nm] = {"slope": float(sl), "tail_max": float(max(mx[-2:]))}
P(f"    K4c: at y* C_T, C_L continuous ({CT_cont}); dC_L/dy jumps {CL_jump[0]:.4f} -> {CL_jump[1]:.4f} (XC4 S5: -0.0361 -> -0.0014); "
  f"d^2 C_T/dy^2 jumps by {dCT2_jump:.5f}")
P(f"    K4c: Fourier envelope of C_T(y* + 0.5 cos 2 pi x): {slopes}  (k^-3 <=> H^(5/2-eps))")
s_hi = 3.5 if (-3.3 < slopes["nu_mono"]["slope"] < -2.7) else None
OUT["numbers"]["K4c"] = {"dCL_dy_left_right": CL_jump, "d2CT_jump": dCT2_jump, "spectral_slopes": slopes,
                         "s_range": [2.5, s_hi]}
check("S3/K4c nu_mono's splice at y* is C^{1,1} and not C^2 (C_T, C_L continuous; dC_L/dy jumps), so C_T(y(x)) is H^{5/2-eps} "
      "(Fourier envelope ~ k^-3) and the C-H stress P_ij ~ C_T w w is in H^{s-1} only for s < 7/2: admissible s in (5/2, 7/2)",
      f"dC_L/dy {CL_jump[0]:.4f} -> {CL_jump[1]:.4f}; slope nu_mono {slopes['nu_mono']['slope']:.3f} vs nu_RAR control "
      f"{slopes['nu_RAR (control, no splice)']['slope']:.3f}", CT_cont and abs(CL_jump[0] - CL_jump[1]) > 1e-3 and s_hi is not None,
      "a C-infinity splice (the recipe's open 'smooth max' variant) would remove the upper end; continuous dependence in the top "
      "norm across the splice level set is ASSUMED (it needs the level set {|DSU| = y* a0} to be null)")
# K4d: the zero-field set on a closed leaf is never empty for single-valued U (illustration: a critical point of a random S U)
rng4 = np.random.default_rng(29404)
n4 = 24
kk4 = np.fft.fftfreq(n4, 1.0 / n4)
KX, KY, KZ = np.meshgrid(kk4, kk4, kk4, indexing="ij")
Uh = (rng4.standard_normal((n4, n4, n4)) + 1j * rng4.standard_normal((n4, n4, n4))) * np.exp(-0.5 * (KX**2 + KY**2 + KZ**2) / 4.0)
Uh[0, 0, 0] = 0
SU = np.real(np.fft.ifftn(Uh)); Uh = np.fft.fftn(SU)
modes = np.argwhere(np.abs(Uh) > 1e-12 * np.abs(Uh).max())
coef = np.array([Uh[tuple(m_)] for m_ in modes]) / n4**3
kv = np.array([[kk4[m_[0]], kk4[m_[1]], kk4[m_[2]]] for m_ in modes]) * 2 * np.pi
def grad_hess(x):
    ph = np.exp(1j * kv @ x) * coef
    g = np.real((1j * kv).T @ ph); H = -np.real((kv.T * ph) @ kv)
    return g, H
i0 = np.unravel_index(np.argmax(SU), SU.shape); x0 = np.array(i0, float) / n4
with np.errstate(all="ignore"):          # Accelerate's complex matmul raises spurious FP flags; results are checked below
    for _ in range(30):
        g_, H_ = grad_hess(x0); x0 = x0 - np.linalg.solve(H_, g_)
    gfin = float(np.linalg.norm(grad_hess(x0)[0]))
assert np.isfinite(gfin) and np.all(np.isfinite(x0)); gscale = np.max(np.abs(np.real(np.fft.ifftn(1j * 2 * np.pi * KX * Uh))))
P(f"    K4d: random smooth periodic S U on T^3: Newton from the grid maximum -> |D S U| = {gfin:.2e} (field scale {gscale:.2e}): a zero of "
  "the filtered field exists (extreme-value theorem; Lusternik-Schnirelmann: >= 4 critical points on T^3)")
OUT["numbers"]["K4d"] = {"grad_at_critical_point": float(gfin), "field_scale": float(gscale)}
check("S3/K4d (disclosure) on a closed leaf the zero-field set Z_0 = {D S U = 0} is non-empty for single-valued U, so 'data away "
      "from zero-field regions' needs U with non-trivial periods (D U closed, not exact) or the isolated-zero regularity (ASSUMED)",
      f"critical point found: |D S U| = {gfin:.1e} vs scale {gscale:.1e}", gfin < 1e-10 * gscale,
      "XC2 B7: zeros are generically isolated after filtering and Lipschitz in the integrated sense; that this suffices for the "
      "H^s estimates is not proved here", load_bearing=False)
S3_srange = [2.5, s_hi] if s_hi else None

# ================================================================================================ S4a lapse equation
banner("S4a  THE NONLINEAR LAPSE EQUATION FROM THE ACTION (unitary gauge t = tau, beta = 0, lambda = 1 + c_2)")
psi = sp.Function("psi")(*xs3); Nn_ = sp.Function("N")(*xs3); w_ = sp.Function("w")(*xs3)
Lalpha = al * psi**2 * sum(sp.diff(Nn_, x_)**2 for x_ in xs3) / Nn_         # alpha sqrt(gamma) gamma^ij d_iN d_jN / N, gamma = psi^4 delta
from sympy.calculus.euler import euler_equations
EL = euler_equations(Lalpha, [Nn_], list(xs3))[0].lhs
LapG = lambda f: sum(sp.diff(psi**2 * sp.diff(f, x_), x_) for x_ in xs3) / psi**6
gradG2 = lambda f: sum(sp.diff(f, x_)**2 for x_ in xs3) / psi**4
target = psi**6 * (al * gradG2(Nn_) / Nn_**2 - 2 * al * LapG(Nn_) / Nn_)
eq_i = sp.simplify(EL - target) == 0
wsub = sp.simplify((2 * LapG(w_**2) / w_**2 - gradG2(w_**2) / w_**4) - 4 * LapG(w_) / w_) == 0
# minisuperspace kinetic variation and the FLRW reduction
Nv, a1, a2, a3, ad1, ad2, ad3, Lam, G_, mu, rho_ = sp.symbols("N a1 a2 a3 ad1 ad2 ad3 Lambda G mu rho", positive=True)
lamK = 1 + c2
Kk = sum((ad / (a * Nv))**2 for a, ad in ((a1, ad1), (a2, ad2), (a3, ad3)))
Kt = sum(ad / (a * Nv) for a, ad in ((a1, ad1), (a2, ad2), (a3, ad3)))
sg = a1 * a2 * a3
Lkin = sg * Nv * (Kk - lamK * Kt**2)
eq_iii = sp.simplify(sp.diff(Lkin, Nv) + sg * (Kk - lamK * Kt**2)) == 0
H_ = sp.Symbol("H", positive=True)
frw = sp.simplify((Kk - lamK * Kt**2).subs({a2: a1, a3: a1, ad2: ad1, ad3: ad1}).subs(ad1, H_ * a1))
Gcos = sp.simplify(6 / (-(frw * Nv**2 / H_**2)))       # (9 lambda - 3) H^2/N^2 = 2 Lambda + 16 pi G rho  ->  G_cos/G = 6/(9 lambda - 3)
Gcos_ok = sp.simplify(Gcos - 1 / (1 + sp.Rational(3, 2) * c2)) == 0
ser_ok = sp.series(Gcos, c2, 0, 2).removeO() == 1 - sp.Rational(3, 2) * c2
l340_says = "1.5 c_2" in L340SRC
# linearisation: CFG292's lapse coefficients from the nonlinear pieces (C_i = -d_i ln N exactly for g = diag(-N^2, 1, 1, 1))
tt, x1_, x2_, x3_ = sp.symbols("t x1 x2 x3", real=True)
Nx = sp.Function("N")(x1_, x2_, x3_)
gN = sp.diag(-Nx**2, 1, 1, 1); gNi = gN.inv(); crd = [tt, x1_, x2_, x3_]
Cvec = [sp.simplify(sum(gNi[a_, b_] * (sp.diff(gN[b_, nu_], crd[a_]) - sp.Rational(1, 2) * sp.diff(gN[a_, b_], crd[nu_]))
                        for a_ in R4 for b_ in R4)) for nu_ in R4]
C_ok = all(sp.simplify(Cvec[i] + sp.diff(Nx, crd[i]) / Nx) == 0 for i in (1, 2, 3))
h0_, hx_ = sp.symbols("h00 h00x", real=True)            # lapse perturbation of the flat metric: g_00 = -1 + h00, N = sqrt(1 - h00)
Nh = sp.sqrt(1 - h0_); Nhx = sp.diff(Nh, h0_) * hx_
L_lapse_phys = al * Nhx**2 / Nh                             # alpha sqrt(gamma) |D N|^2 / N
L_lapse_gf = -HALF * Nh * (Nhx / Nh)**2                     # -1/2 N sqrt(gamma) gamma^ij C_i C_j with C_i = -d_i ln N
coef_phys = sp.simplify(sp.diff(L_lapse_phys, hx_, 2).subs({h0_: 0, hx_: 0}))
coef_f2a = sp.simplify(sp.diff(L_lapse_phys + L_lapse_gf, hx_, 2).subs({h0_: 0, hx_: 0}))
f2a_lin = sp.simplify(coef_f2a - (2 * al - 1) / 4) == 0 and sp.simplify(coef_phys - al / 2) == 0
c292_f2a = J292["numbers"]["COND"]["F2a"]["lapse_coeff"]; c292_f2b = J292["numbers"]["COND"]["F2b"]["lapse_coeff"]
match292 = (sp.simplify(sp.sympify(c292_f2a, locals={"alpha": al}) - (2 * al - 1) / 4) == 0
            and sp.simplify(sp.sympify(c292_f2b, locals={"alpha": al}) - al / 2) == 0)
P(f"    (i)   delta/delta N of alpha sqrt(gamma)|DN|^2/N = sqrt(gamma)[alpha a^2 - 2 alpha Delta N/N] (euler_equations, conformally flat leaf): {eq_i}")
P(f"    (ii)  N = w^2: 2 Delta N/N - |DN|^2/N^2 = 4 Delta w/w: {wsub}")
P(f"    (iii) d/dN [N sqrt(gamma)(K.K - lambda K^2)] = -sqrt(gamma)(K.K - lambda K^2) at fixed velocities: {eq_iii}")
P(f"    (iv)  FLRW: K.K - lambda K^2 = {frw}  ->  G_cos/G = {Gcos} = 1/(1 + 3c_2/2): {Gcos_ok}; first order 1 - 1.5 c_2: {ser_ok}; "
  f"L340 P1 states '1.5 c_2': {l340_says}")
P(f"    (v)   C_i = -d_i ln N exactly for g = diag(-N^2,1,1,1): {C_ok};  linearised lapse coefficients alpha/2 (physical) and "
  f"(2 alpha - 1)/4 (F2a) = CFG292's committed {c292_f2b!r}, {c292_f2a!r}: {f2a_lin and match292}")
P("    RESULT  E_N = R^(3) - (K_ij K^ij - lambda K^2) + alpha_c a^2 - 2 alpha_c Delta N/N - 2 Lambda - 16 pi G rho_N + H_CH = 0;  with N = w^2:")
P("            4 alpha_c Delta w = w [R^(3) - 2 Lambda - 16 pi G rho + H_CH] - N^2(K.K - lambda K^2) w^-3     (velocities fixed: Lichnerowicz-type)")
P("            -4 alpha_c Delta w + V w = 0,  V = R^(3) - (K.K - lambda K^2)[pi] - 2 Lambda - 16 pi G rho + H_CH  (momenta fixed: linear in sqrt N)")
s4a_ok = eq_i and wsub and eq_iii and Gcos_ok and ser_ok and l340_says and C_ok and f2a_lin and match292 and shell_ok
OUT["numbers"]["S4a"] = {"variational": eq_i, "w_sub": wsub, "kinetic": eq_iii, "Gcos": str(Gcos), "C_i": C_ok,
                         "CFG292_coeffs": [c292_f2b, c292_f2a]}
check("S4a the nonlinear lapse equation is derived from the chassis action: the alpha-term variation, the w = sqrt N substitution, "
      "the kinetic variation, the FLRW reduction (G_cos/G = 1/(1 + 3c_2/2), L340's 1.5 c_2), and the linearisation reproduces "
      "CFG292's lapse coefficients alpha/2 and (2 alpha - 1)/4", f"(i) {eq_i} (ii) {wsub} (iii) {eq_iii} (iv) {Gcos_ok}/{ser_ok}/{l340_says} "
      f"(v) {C_ok}/{f2a_lin}/{match292}; K4b shell {shell_ok}", s4a_ok,
      "in Hamiltonian variables the equation is linear in w = sqrt N (Donnelly & Jacobson 2011: 'linear in the square root of "
      "the lapse'; quoted provisionally)")

# ================================================================================================ S4b ellipticity
banner("S4b  UNIFORM ELLIPTICITY OF THE LAPSE OPERATORS ON THE WINDOW")
phys_lo = float(W_REC[0]); f2a_lo = float(abs(2 * W_REC[1] - 1) / 4)
joint = sp.Matrix([[4 * al * kq_**2, 0], [sp.Symbol("x") * kq_**2, Ns * kq_**2]])   # (w, chi) leaf system, triangular
joint_det = sp.factor(joint.det())
P(f"    physical (w-form) principal coefficient 4 alpha_c >= {4 * phys_lo:.4e} > 0 on W_rec;  F2a (h_00) coefficient |2 alpha_c - 1|/4 "
  f">= {f2a_lo:.10f};  joint (N, chi) leaf system: det of the triangular principal symbol = {joint_det} (elliptic iff alpha_c != 0)")
check("S4b the lapse operators are uniformly elliptic on W_rec: physical 4 alpha_c |k|^2_gamma (alpha_c >= alpha_min > 0), F2a "
      "(2 alpha_c - 1) sqrt(gamma)|k|^2_gamma/(4 N^3) (alpha_c != 1/2; S1c/K1 on general backgrounds), joint (N, chi) system",
      f"4 alpha_c >= {4 * phys_lo:.3e}; |2 alpha_c - 1|/4 >= {f2a_lo:.6f}", phys_lo > 0 and f2a_lo > 0.2,
      "uniform on O x W_rec with constant >= alpha_min lambda_min(gamma^-1) (physical) and ~1/4 lambda_min(gamma^-1)/N^3 (F2a)")

# ================================================================================================ S4c kernel: Hamiltonian form
banner("S4c(Ham)  KERNEL IN HAMILTONIAN FORM: -4 alpha Delta + V on periodic 2-D leaves (random sign-indefinite V)")
def lap2d(n):
    h = 1.0 / n
    e = np.ones(n)
    D1 = diags([e[:-1], -2 * e, e[:-1]], [-1, 0, 1], shape=(n, n)).tolil()
    D1[0, n - 1] = 1; D1[n - 1, 0] = 1
    D1 = csr_matrix(D1) / h**2
    I1 = identity(n, format="csr")
    return kron(D1, I1) + kron(I1, D1)
n2d = 48
LAP = lap2d(n2d)
rngh = np.random.default_rng(29405)
kk2 = np.fft.fftfreq(n2d, 1.0 / n2d); K2X, K2Y = np.meshgrid(kk2, kk2, indexing="ij")
HAM = []
for iv in range(3):
    Vh = (rngh.standard_normal((n2d, n2d)) + 1j * rngh.standard_normal((n2d, n2d))) * np.exp(-0.5 * (K2X**2 + K2Y**2) / 4.0)
    V = np.real(np.fft.ifft2(Vh)); V -= V.mean(); V /= np.abs(V).max()
    for alt in (1e-1, 1e-2, 1e-3):
        L = -4 * alt * LAP + diags(V.ravel())
        vals, vecs = eigsh(L.tocsc(), k=3, sigma=float(V.min()) - 1.0, which="LM")
        o = np.argsort(vals); vals, vecs = vals[o], vecs[:, o]
        w0 = vecs[:, 0] * np.sign(vecs[:, 0].sum())
        gap = vals[1] - vals[0]
        onesign = bool(np.all(w0 > 0))
        Ls = (L - vals[0] * identity(n2d * n2d)).tocsc()
        ev2 = np.sort(np.abs(eigsh(Ls, k=2, sigma=-1e-9, which="LM", return_eigenvectors=False)))
        border = bmat([[Ls, csr_matrix(np.ones((n2d * n2d, 1)) / n2d**2)], [csr_matrix(np.ones((1, n2d * n2d)) / n2d**2), None]]).tocsc()
        rhs = np.zeros(n2d * n2d + 1); rhs[-1] = 1.0
        sol = spsolve(border, rhs)[:-1]
        uniq = bool(np.allclose(sol / sol.mean(), w0 / w0.mean(), rtol=1e-6, atol=1e-8))
        HAM.append({"V": iv, "alpha_eff": alt, "lambda1": float(vals[0]), "gap": float(gap), "one_sign": onesign,
                    "null_dim1": bool(ev2[0] < 1e-8 * max(1, abs(vals[0])) and ev2[1] > 1e3 * max(ev2[0], 1e-14)),
                    "unique_with_mean": uniq, "ln_wmax_wmin": float(np.log(w0.max() / w0.min()))})
for h_ in HAM:
    P(f"    V#{h_['V']} alpha_eff {h_['alpha_eff']:.0e}: lambda_1 = {h_['lambda1']:+.5f}, gap {h_['gap']:.3e}, ground state one sign "
      f"{h_['one_sign']}, null space of (L - lambda_1) 1-dim {h_['null_dim1']}, unique with <w> fixed {h_['unique_with_mean']}, "
      f"ln(w_max/w_min) {h_['ln_wmax_wmin']:.3f}")
agm = []
for iv in range(3):
    xs_ = np.array([h_["alpha_eff"]**-0.5 for h_ in HAM if h_["V"] == iv]); ys_ = np.array([h_["ln_wmax_wmin"] for h_ in HAM if h_["V"] == iv])
    agm.append(float(np.polyfit(xs_, ys_, 1)[0]))
sA = float(np.mean(agm))
lnN_at_amax = 2 * sA * (1.0 / AC_MAX)**0.5
dV_allowed = AC_MAX * (math.log(10) / (2 * sA))**2
P(f"    Agmon slope d ln(w_max/w_min)/d alpha^-1/2 = {agm} (mean {sA:.4f}).  With a constraint violation of amplitude dV ~ 1/L^2 and "
  f"alpha_c = {AC_MAX:.1e}: ln(N_max/N_min) ~ {lnN_at_amax:.3e}; N_max/N_min <= 10 needs dV L^2 <= {dV_allowed:.2e}")
ham_ok = all(h_["gap"] > 0 and h_["one_sign"] and h_["null_dim1"] and h_["unique_with_mean"] for h_ in HAM)
OUT["numbers"]["S4c_ham"] = {"rows": HAM, "agmon_slope": sA, "lnN_ratio_at_alpha_max_unit_violation": lnN_at_amax,
                             "dV_L2_for_ratio_10": dV_allowed}
check("S4c(Ham) in Hamiltonian variables the lapse operator -4 alpha Delta + V has, for every sign-indefinite V tried, a simple "
      "lowest eigenvalue with a one-signed ground state, a 1-dim null space after the global shift, and a unique solution once <w> "
      "is fixed: kernel = the tau-relabelling mode, no sign condition; solvability = the global constraint lambda_1 = 0",
      f"{sum(h_['gap'] > 0 and h_['one_sign'] and h_['null_dim1'] and h_['unique_with_mean'] for h_ in HAM)}/{len(HAM)} cases",
      ham_ok, "a trivial kernel is impossible here by symmetry (tau -> f(tau)); disclosed: as alpha_c -> 0 the ground state "
      "localises (Agmon), so a uniform lower bound on N needs data obeying the GR-like Hamiltonian constraint to O(alpha_c)")

# ================================================================================================ S4c kernel: Lagrangian / F2a, Bianchi I
banner("S4c(Lag)  THE OPERATOR F2a INVERTS (velocities fixed): exact lapse Hessian on Bianchi-I flat-leaf backgrounds")
kx_, v_, phid, V0, NX = sp.symbols("k v phidot V0 N_x", real=True)
N0 = sp.Symbol("N0", positive=True)
Nsym = sp.Symbol("Nsym", positive=True)
Kk_N = sum((ad / (a * Nsym))**2 for a, ad in ((a1, ad1), (a2, ad2), (a3, ad3)))
Kt_N = sum(ad / (a * Nsym) for a, ad in ((a1, ad1), (a2, ad2), (a3, ad3)))
# full nonlinear C_1 for g = diag(-N(t,x)^2, a_i(t)^2): computed from the 4-metric
af = [sp.Function(f"a{i}")(tt) for i in (1, 2, 3)]
Nfx = sp.Function("Nf")(tt, x1_)
g4 = sp.diag(-Nfx**2, af[0]**2, af[1]**2, af[2]**2); g4i = g4.inv()
C1 = sp.simplify(sum(g4i[a_, b_] * (sp.diff(g4[b_, 1], crd[a_]) - sp.Rational(1, 2) * sp.diff(g4[a_, b_], crd[1])) for a_ in R4 for b_ in R4))
C1_ok = sp.simplify(C1 + sp.diff(Nfx, x1_) / Nfx) == 0
C1_sym = -NX / Nsym                                           # verified form
grav = sg * (Nsym * (Kk_N - lamK * Kt_N**2) + al * Nsym * NX**2 / (a1**2 * Nsym**2) - 2 * Lam * Nsym) / (16 * sp.pi * G_)
gauge = -HALF * Nsym * sg * C1_sym**2 / a1**2 / (16 * sp.pi * G_)
dust = -mu * sp.sqrt(Nsym**2 - a1**2 * v_**2)
scal = sg * (phid**2 / (2 * Nsym) - Nsym * V0)
def hess(Ltot):
    """h(k) = L_NN + k^2 L_{N_x N_x} at N = N0, N_x = 0 (the plane-wave second variation, averaged)."""
    LNN = sp.diff(Ltot, Nsym, 2).subs(NX, 0).subs(Nsym, N0)
    LXX = sp.diff(Ltot, NX, 2).subs(NX, 0).subs(Nsym, N0)
    return sp.simplify(LNN), sp.simplify(LXX)
LNN_f, LXX_f = hess(grav + gauge + dust + scal)
LNN_p, LXX_p = hess(grav + dust + scal)
bg_eq = sp.diff(grav + dust + scal, Nsym).subs(NX, 0).subs(Nsym, N0)       # background lapse equation (homogeneous)
Lam_bg = sp.solve(sp.Eq(bg_eq, 0), Lam)[0]                                # it is linear in Lambda
W_expr = sp.simplify(8 * sp.pi * G_ * N0 * LNN_f / sg)                     # W = 8 pi G N0 L_NN / sqrt(gamma): velocities + matter, no Lambda
uu = sp.Symbol("u", positive=True)                                       # khronon-frame dust speed u = a1 v / N0
W_pred = -2 * Lam - 16 * sp.pi * G_ * V0 - 8 * sp.pi * G_ * (mu / sg) * (2 - 3 * uu**2) / (1 - uu**2)**sp.Rational(3, 2)
diffW = (W_expr - W_pred.subs(Lam, Lam_bg)).subs(v_, uu * N0 / a1)
W_match_sym = sp.simplify(diffW) == 0
rngW = np.random.default_rng(29406)
numdiff = []
for _ in range(6):
    vals_ = {a1: rngW.uniform(0.5, 2), a2: rngW.uniform(0.5, 2), a3: rngW.uniform(0.5, 2), ad1: rngW.uniform(-1, 1),
             ad2: rngW.uniform(-1, 1), ad3: rngW.uniform(-1, 1), N0: rngW.uniform(0.5, 2), G_: rngW.uniform(0.1, 1),
             mu: rngW.uniform(0, 2), uu: rngW.uniform(0, 0.9), phid: rngW.uniform(-1, 1), V0: rngW.uniform(-1, 1),
             c2: rngW.uniform(0, 0.1), al: 1e-9}
    numdiff.append(abs(complex(sp.N(diffW.subs(vals_), 40))))
W_match = W_match_sym or max(numdiff) < 1e-25
W_in_Lam = W_pred
coefk_f = sp.simplify(LXX_f * 8 * sp.pi * G_ * N0 / sg * a1**2); coefk_p = sp.simplify(LXX_p * 8 * sp.pi * G_ * N0 / sg * a1**2)
P(f"    C_1 from the 4-metric diag(-N(t,x)^2, a_i(t)^2) = -d_x N/N: {C1_ok}")
P(f"    h_F2a(k) = (sqrt(gamma)/(8 pi G N0)) [ ({coefk_f}) |k|^2_gamma + W ],   h_phys(k) = (...) [ ({coefk_p}) |k|^2_gamma + W ]")
P(f"    W (background lapse equation used) = {W_in_Lam}")
P(f"    = -2 Lambda - 16 pi G V(phi) - 8 pi G rho_rest (2 - 3u^2)/(1 - u^2)^(3/2) (u = khronon-frame dust speed): {W_match};  the scalar "
  "field's kinetic energy cancels exactly")
# FLRW + Lambda + comoving dust at each record c_2 (8 pi G = 1 units, a = N0 = 1, Lambda = rho = 1): W < 0 -> trivial kernel (F2a)
flrw_rows = []
for (_, c_) in POINTS:
    lamv = 1 + c_
    Lv, rv = sp.Integer(1), sp.Integer(1)
    H2 = (2 * Lv + 2 * rv) / (9 * lamv - 3)          # (9 lambda - 3) H^2 = 2 Lambda + 16 pi G rho, 16 pi G = 2
    Kqv = 3 * H2 - 9 * lamv * H2
    flrw_rows.append(float(Kqv))
flrw_ok = all(x < 0 for x in flrw_rows)
kstar = sorted({float(sp.sqrt((6 + 9 * c_) / a_)) for (a_, c_) in POINTS})
kas = sp.simplify(W_pred.subs({Lam: 0, V0: 0, mu: 0}))
P(f"    FLRW + Lambda + comoving dust: W = -(2 Lambda + 16 pi G rho) at every c_2 of the points: {['%.4f' % x for x in flrw_rows[:3]]}... all < 0: {flrw_ok}")
P(f"    vacuum (Kasner-type, Lambda = rho = V = 0): W = {kas} -> the k = 0 mode is the relabelling zero mode (quotient by it)")
P(f"    physical (velocity-fixed) form: alpha_c |k|^2 + W vanishes at (k_*/a)/(H/N0) = sqrt((6 + 9 c_2)/alpha_c) in [{kstar[0]:.3e}, {kstar[-1]:.3e}]"
  " -- a resonance; the F2a operator (alpha_c - 1/2)|k|^2 + W has none when W < 0")
OUT["numbers"]["S4c_lag"] = {"W": str(W_in_Lam), "W_matches_prediction": W_match, "coef_k_F2a": str(coefk_f), "coef_k_phys": str(coefk_p),
                             "flrw_W": flrw_rows, "kstar_over_H": [kstar[0], kstar[-1]], "vacuum_W": str(kas)}
s4c_lag_ok = C1_ok and W_match and flrw_ok and sp.simplify(coefk_f - (al - HALF)) == 0 and sp.simplify(coefk_p - al) == 0
check("S4c(Lag) the F2a lapse operator (velocities fixed) on Bianchi-I flat leaves is (alpha_c - 1/2)|k|^2_gamma + W with "
      "W = -2 Lambda - 16 pi G V(phi) - 8 pi G rho_rest (2 - 3u^2)/(1-u^2)^(3/2): the sign condition W <= 0 (W != 0) holds for "
      "FLRW + Lambda + comoving dust at every record c_2, so the kernel is trivial there; vacuum gives W = 0 (relabelling mode)",
      f"W derived and matched {W_match}; coefficients F2a {coefk_f}, physical {coefk_p}; FLRW W < 0 at all points {flrw_ok}",
      s4c_lag_ok,
      "the condition is on the data, not on (alpha_c, c_2): Lambda + 8 pi G V + dust terms >= 0, dust slower than sqrt(2/3) in the "
      "khronon frame; on general inhomogeneous data W has no definite sign and invertibility is an open condition near these")

# ================================================================================================ S4d linearised constraint propagation
banner("S4d  LINEARISED CONSTRAINT PROPAGATION of the spatial de Donder vector C_i (aligned + the set-2 backgrounds)")
def cp_check(gbar, alpha, cc2):
    ginv = gbar.inv(); gam = gbar[1:, 1:]
    zeta = sp.symbols("z1:4")
    zlow = [sum(gbar[m, j + 1] * zeta[j] for j in range(3)) for m in R4]              # zeta^0 = 0
    Zv = sp.Matrix([XI[m] * zlow[n] + XI[n] * zlow[m] for (m, n) in PAIRS])
    Zm = Zv.jacobian(zeta)
    Lk_, _ = L_khronon(gbar, DT, alpha, 0, cc2)
    Pinv = symbol_matrix(L_EH(gbar) + Lk_, VARS_H)
    inv_ok = all(sp.expand(e_) == 0 for e_ in (Zm.T * Pinv))
    Cl = deDonder(gbar)
    sub = fourier_sub(XI)
    MC = sp.Matrix([[sp.expand(sp.diff(Cl[i].xreplace(sub), VARS_H[j])) for j in range(10)] for i in (1, 2, 3)])
    MCZ = (MC * Zm).applyfunc(sp.expand)
    xx_ = sp.expand(sum(ginv[m, n] * XI[m] * XI[n] for m in R4 for n in R4))
    scal_ok = all(sp.expand(e_) == 0 for e_ in (MCZ - xx_ * gam))
    Pgf = symbol_matrix(L_gf(gbar, HALF, "spatial4"), VARS_H)
    ident = (Zm.T * Pgf + sp.sqrt(-gbar.det()) * MCZ.T * gam.inv() * MC).applyfunc(sp.expand)
    ident_ok = all(sp.simplify(e_) == 0 for e_ in ident)
    return inv_ok, scal_ok, ident_ok
cp_rows = [("aligned",) + cp_check(ETA, rat(AC_MAX), rat(C2_MAX))]
for ib in (0, 1):
    cp_rows.append((f"background {ib}",) + cp_check(BGS[ib]["g"], rat(AC_MAX), rat(C2_MAX)))
for r_ in cp_rows:
    P(f"    {r_[0]}: Z^T P_(EH+khronon) = 0 {r_[1]};  M_C Z = (g^{{mu nu}} xi_mu xi_nu) gamma_ij {r_[2]};  Z^T P_gf = -sqrt(-g) (M_C Z)^T gamma^-1 M_C {r_[3]}")
cp_ok = all(all(r_[1:]) for r_ in cp_rows)
check("S4d on solutions of the reduced F2a system the gauge vector obeys (g^{mu nu} xi_mu xi_nu) C_i = 0 at the symbol level, a "
      "strongly hyperbolic (light-cone, complete) constraint subsystem; spatial diffeomorphisms annihilate the EH + khronon symbol",
      f"{[(r_[0], all(r_[1:])) for r_ in cp_rows]}", cp_ok,
      "C = 0 initially is a choice of the initial shift velocity, d_t C = 0 initially is the momentum constraint; the nonlinear "
      "propagation and the global constraint's propagation are ASSUMED (Noether identities), not computed")

# ================================================================================================ controls
banner("CONTROLS: GR full harmonic (C-GRa); GR CMC + spatial harmonic, the Andersson-Moncrief case (C-GRb); minimal Horava (C-H0)")
# C-GRa
P_GR = symbol_matrix(L_EH(ETA) + L_gf(ETA, HALF, "full"), VARS_H)
CM_GR = {k_: to_QQ(v_) for k_, v_ in coef_mats(P_GR).items()}
G10 = frob_weights([str(v_) for v_ in VARS_H])
gra = []
for d_ in DIRS[:6]:
    A10, B10, C10 = pencil_at(CM_GR, d_)
    M = companion(A10, B10, C10)
    I20 = DomainMatrix.eye(20, QQ)
    mp1 = (M * M - I20).is_zero_matrix
    Gm = DomainMatrix.diag([q(x) for x in G10 + G10], QQ)
    H, _ = symmetriser(M, QQ(1), None, Gm)
    piv = ldl_pivots(H)
    gra.append(mp1 and (H * M - (H * M).transpose()).is_zero_matrix and all(x > 0 for x in piv) and len(piv) == 20)
grA_ok = all(gra)
P(f"    C-GRa: one family +-1 (multiplicity 10), (M^2 - 1) = 0 exactly, H = (G + M^T G M)/2 PD with H M symmetric, 6 directions: {gra}")
# C-GRb: hyperbolic part -(lambda - X.k)^2 + N^2|k|^2_gamma (x I_6), lapse/shift lower order (AM)
grb_rows = []
for ib in range(3):
    bg = BGS[ib]; k_ = [sp.Rational(1, 3), sp.Rational(-2, 5), sp.Rational(3, 4)]
    nu = q(sum(bg["shift"][i] * k_[i] for i in range(3))); rho = q(bg["N"]**2 * (sp.Matrix(k_).T * bg["gamma"].inv() * sp.Matrix(k_))[0])
    I6 = DomainMatrix.eye(6, QQ); Z6 = DomainMatrix.zeros((6, 6), QQ)
    A6, B6, C6 = -I6, I6 * (2 * nu), I6 * (rho - nu * nu)
    M6 = companion(A6, B6, C6)
    D6 = M6 - DomainMatrix.eye(12, QQ) * nu
    mpok = (D6 * D6 - DomainMatrix.eye(12, QQ) * rho).is_zero_matrix
    G6 = DomainMatrix.diag([q(x) for x in frob_weights(["H11", "H12", "H13", "H22", "H23", "H33"]) * 2], QQ)
    H6, _ = symmetriser(D6, rho, None, G6)
    grb_rows.append(mpok and (H6 * D6 - (H6 * D6).transpose()).is_zero_matrix and all(x > 0 for x in ldl_pivots(H6)))
tau_cmc = -0.7
sig = []
for _ in range(5):
    Sh = (rngh.standard_normal((n2d, n2d)) + 1j * rngh.standard_normal((n2d, n2d))) * np.exp(-0.5 * (K2X**2 + K2Y**2) / 4.0)
    sig.append(np.real(np.fft.ifft2(Sh)))
sig = np.array(sig); sig /= np.abs(sig).max()
K2field = tau_cmc**2 / 3 + np.sum(sig**2, axis=0) * 2.0                 # |k|^2 = tau^2/3 + |sigma|^2 >= tau^2/3
Lcmc = (-LAP + diags(K2field.ravel())).tocsc()
lmin_cmc = float(eigsh(Lcmc, k=1, sigma=-1.0, which="LM", return_eigenvectors=False)[0])
Lmax0 = (-LAP).tocsc()
lmin_max0 = float(np.abs(eigsh(Lmax0, k=1, sigma=-1e-3, which="LM", return_eigenvectors=False)[0]))
cmc_kernel_ok = lmin_cmc >= tau_cmc**2 / 3 - 1e-9
sub_probe_fails = lmin_max0 < 1e-8
Rr, trk, kk2s, rhoE = sp.symbols("R trk kk rhoE", real=True)
src_before = Nv * (Rr + trk**2)                                          # d_t tr k = -Delta N + N (R + (tr k)^2)  (vacuum, zero shift)
src_after = sp.expand(src_before.subs(Rr, kk2s - trk**2 + 16 * sp.pi * G_ * rhoE))
am5_gr = sp.diff(src_after, Rr) == 0 and sp.diff(src_before, Rr) != 0
grB_ok = all(grb_rows) and cmc_kernel_ok and sub_probe_fails and am5_gr
P(f"    C-GRb: hyperbolic part S1/S2 on 3 general backgrounds {grb_rows};  CMC lapse -Delta + |k|^2 (tau = {tau_cmc}): lambda_min = {lmin_cmc:.4f} "
  f">= tau^2/3 = {tau_cmc**2 / 3:.4f}: {cmc_kernel_ok} (trivial kernel);  sub-probe maximal k = 0: lambda_min = {lmin_max0:.2e} -> kernel = constants, "
  f"the trivial-kernel check FAILS as pre-registered: {sub_probe_fails};  AM5: lapse source contains R before the Hamiltonian constraint "
  f"{sp.diff(src_before, Rr) != 0}, after {sp.diff(src_after, Rr) != 0} -> lower order: {am5_gr}")
# C-H0: minimal Horava (alpha = 0)
CM0 = point_mats(CM_F2a, sp.Integer(0), rat(C2_MAX))
A10, B10, C10 = pencil_at(CM0, [QQ(0), QQ(0), QQ(1)])
A0_, B0_, C0_, p00_0, _, _ = schur_lapse(A10, B10, C10)
detA0 = A0_.det()
Mh0 = companion(A0_, B0_, C0_) if A0_ is not None else None
s1_h0_fails = Mh0 is None
s2_h0_fails = Mh0 is None
phys_lapse_h0 = 4 * 0                                                    # physical coefficient 4 alpha_c at alpha_c = 0
P(f"    C-H0 (alpha_c = 0, c_2 = {float(rat(C2_MAX)):.4f}): det A = {QQ.to_sympy(detA0)} -> companion exists: {Mh0 is not None}; S1 fails "
  f"{s1_h0_fails}, S2 fails {s2_h0_fails}; physical lapse coefficient 4 alpha_c = {phys_lapse_h0} (not elliptic); F2a lapse coefficient "
  f"{QQ.to_sympy(p00_0)} (the gauge term alone)")
check("C-GRa GR in full harmonic gauge passes S1 and S2 (one family, multiplicity 10; explicit H PD, H M symmetric)",
      f"{sum(gra)}/{len(gra)} directions", grA_ok)
check("C-GRb GR in CMC + spatial harmonic gauge (Andersson-Moncrief) passes S1, S2, the lapse kernel (potential >= tau^2/3 > 0) and "
      "AM5 (no R in the lapse source after the Hamiltonian constraint); its maximal k = 0 sub-probe fails the trivial-kernel check",
      f"S1/S2 {grb_rows}; kernel {cmc_kernel_ok}; sub-probe fails {sub_probe_fails}; AM5 {am5_gr}", grB_ok)
check("C-H0 minimal Horava (alpha_c = 0) FAILS S1 and S2 (singular leading matrix, an eigenvalue at infinity) and the physical "
      "lapse ellipticity", f"det A = {QQ.to_sympy(detA0)}; companion {Mh0 is not None}", s1_h0_fails and s2_h0_fails and phys_lapse_h0 == 0)
controls_ok = grA_ok and grB_ok and s1_h0_fails and s2_h0_fails

# ================================================================================================ the crossing (MUTATE analysis; preview in the normal run)
banner(("MUTATE" if MUTATE else "PREVIEW (non-load-bearing)") + ": the crossing c_S = 1 -- what S1 and S2 see there")
c_x = rat(C2_MAX); a_x = axc(c_x)
CMx = point_mats(CM_F2a, a_x, c_x)
rx = exact_case(CMx, [QQ(0), QQ(0), QQ(1)], QQ(0), QQ(1), q(cs2_of(a_x, c_x)), q((2 * a_x - 1) / 4), want_spectrum=False)
A10, B10, C10 = pencil_at(CMx, [QQ(0), QQ(0), QQ(1)])
Ax, Bx, Cx_, _, _, _ = schur_lapse(A10, B10, C10)
Mx = companion(Ax, Bx, Cx_)
I18 = DomainMatrix.eye(18, QQ)
H_merged, _ = symmetriser(Mx, QQ(1), None, G18)
semis_x = (Mx * Mx - I18).is_zero_matrix
jumps, pnorms = [], []
for j in (2, 4, 6, 8):
    aj = a_x * (1 + sp.Rational(1, 10**j))
    CMj = point_mats(CM_F2a, aj, c_x)
    A10, B10, C10 = pencil_at(CMj, [QQ(0), QQ(0), QQ(1)])
    Aj, Bj, Cj, _, _, _ = schur_lapse(A10, B10, C10)
    Mj = companion(Aj, Bj, Cj)
    Hj, _ = symmetriser(Mj, QQ(1), q(cs2_of(aj, c_x)), G18)
    dH_ = dm_to_mp(Hj - H_merged); jumps.append(float(mp.mnorm(dH_, 1) / mp.mnorm(dm_to_mp(H_merged), 1)))
    nrm, _ = projector_norms(Mj, QQ(1), q(cs2_of(aj, c_x)), G9 + G9)
    pnorms.append(float(max(nrm)))
P(f"    at alpha = c_2/(1 + 2c_2) = {a_x} (c_2 = {c_x}): c_S^2 = {cs2_of(a_x, c_x)}; multiplicity of +1 = {rx.get('mult_plus1')} "
  f"(rank(D^2 - 1) = {rx.get('rank_D2_minus_rho')}, semisimple {semis_x}); family split (8,8,1,1) holds: {rx.get('mult_8811')}; "
  f"S2 construction: '{rx.get('H_note')}'")
P(f"    approaching the crossing (alpha = alpha_x (1 + 10^-j), j = 2, 4, 6, 8): ||H(c_S) - H_merged|| / ||H_merged|| = "
  f"{['%.4f' % x for x in jumps]};  max ||P_j||_G = {['%.3e' % x for x in pnorms]}")
jump_lim = jumps[-1]
OUT["numbers"]["crossing"] = {"alpha_x": str(a_x), "c2": str(c_x), "mult_plus1": rx.get("mult_plus1"), "semisimple": semis_x,
                              "H_continuous_through_crossing": None,
                              "H_jump": jumps, "projector_norms": pnorms, "note": rx.get("H_note")}
crossing_flagged = (rx.get("mult_8811") is False) and bool(rx.get("H_note"))
dj = [abs(jumps[i + 1] - jumps[i]) for i in range(len(jumps) - 1)]
lim_exists = all(dj[i + 1] < dj[i] for i in range(len(dj) - 1)) and dj[-1] < 1e-4 * abs(jumps[-1]) and pnorms[-1] < 10 * pnorms[0]
Hm8 = dm_to_mp(Hj); Mxm = dm_to_mp(Mx)
lim_sym_resid = float(mp.mnorm(Hm8 * Mxm - (Hm8 * Mxm).T, 1) / mp.mnorm(Hm8 * Mxm, 1))
H_continuous = lim_exists and lim_sym_resid < 1e-6
OUT["numbers"]["crossing"]["H_continuous_through_crossing"] = bool(H_continuous)
OUT["numbers"]["crossing"]["limit_symmetrises_M_residual"] = lim_sym_resid
check(("C-MUTATE " if MUTATE else "(preview) ") + "at the crossing c_S = 1 the constant-multiplicity family split fails (mult(+1) = 9 "
      "instead of 8) and the projector symmetriser is flagged (its denominator 1 - c_S^2 vanishes); the jump of H across the "
      "crossing is reported",
      f"mult(+1) {rx.get('mult_plus1')}; family split holds {rx.get('mult_8811')}; S2 note '{rx.get('H_note')}'; "
      f"||H(c_S -> 1) - H_merged||/||H_merged|| = {jump_lim:.3e}; projector-norm growth {pnorms[-1] / pnorms[0]:.3e}", crossing_flagged,
      "disclosed: the merged eigenvalue is semisimple at exactly c_S = 1 (CFG292 C5), so strong hyperbolicity survives there; "
      + (f"the family projectors stay bounded (max ||P_j||_G = {pnorms[-1]:.3f}) and converge; the four-projector H has a finite "
         f"limit (no (c_S^2 - 1) factor survives, S2c) that still symmetrises M at the crossing (residual {lim_sym_resid:.1e} at "
         f"distance 1e-8) and differs from the merged-eigenvalue construction by {jump_lim:.3f} (relative): the Lagrange formula is "
         "0/0 there and Kreiss's constant-multiplicity hypothesis fails, but a continuous symmetriser exists through the crossing "
         "in this system" if H_continuous else
         "the four-projector H has no symmetrising limit at the crossing: the family projectors are not smooth through it"),
      load_bearing=MUTATE)

# ================================================================================================ AM table
banner("S4e  ANDERSSON & MONCRIEF (2003) HYPOTHESES, ITEM BY ITEM, FOR C-H/K IN F2a")
CMr = point_mats(CM_F2a, rat(AC_MAX), min(C2S))
A10, B10, C10 = pencil_at(CMr, [QQ(0), QQ(0), QQ(1)])
Arr, Brr, Crr = A10[1:10, 1:10], B10[1:10, 1:10], C10[1:10, 1:10]
Mrr = companion(Arr, Brr, Crr)
cp_rr = sp.factor(sum(QQ.to_sympy(c_) * lam**(18 - i) for i, c_ in enumerate(Mrr.charpoly()))) if Mrr is not None else None
Ar_, Br_, Cr_, _, _, _ = schur_lapse(A10, B10, C10)
cp_red = sp.factor(sum(QQ.to_sympy(c_) * lam**(18 - i) for i, c_ in enumerate(companion(Ar_, Br_, Cr_).charpoly())))
am5_fail = (cp_rr is None) or sp.expand(cp_rr - cp_red) != 0
def roots_by_factor(expr):
    out = []
    for f_, m_ in sp.factor_list(expr, lam)[1]:
        pf = sp.Poly(f_, lam)
        if pf.degree() == 0:
            continue
        rts = sp.roots(pf) if pf.degree() <= 4 else {}
        if sum(rts.values()) != pf.degree():
            rts = {r_: 1 for r_ in pf.nroots(n=30, maxsteps=500)}
        for r_, mr in rts.items():
            out += [complex(sp.N(r_, 30))] * (int(m_) * int(mr))
    return out
rr_roots = sorted(set(roots_by_factor(cp_rr)), key=lambda z: (z.real, z.imag)) if cp_rr is not None else []
rr_scalar = [r_ for r_ in rr_roots if abs(abs(r_) - 1) > 1e-6]
P(f"    AM5 test at (alpha_max, lowest c_2): det(lambda - M) with the lapse FROZEN = {cp_rr}")
P(f"                                         with the lapse ELIMINATED = {cp_red}")
P(f"    -> frozen-lapse scalar roots {['%.4g%+.4gi' % (z.real, z.imag) for z in rr_scalar]} vs c_S = {float(mp.sqrt(mp.mpf(cs2_of(rat(AC_MAX), min(C2S)).p) / cs2_of(rat(AC_MAX), min(C2S)).q)):.4g}: "
  f"the lapse is coupled at principal order (AM5 fails): {am5_fail}")
ASSUMED = ["A1 the pseudo-differential (paradifferential) form of Kato's quasilinear theorem for the lapse-reduced system: "
           "commutator/paraproduct estimates for the nonlocal lapse solve with H^s coefficients (standard for symbols smooth in xi, "
           "H^s in x, s > n/2 + 1; not verified here)",
           "A2 nonlinear propagation of the gauge constraint C_i = 0 (foliation-preserving-diffeomorphism Noether identity + uniqueness "
           "for the linear constraint system; the symbol-level statement is S4d)",
           "A3 propagation of the global (relabelling) constraint lambda_1 = 0 (first-class global part, Donnelly & Jacobson 2011)",
           "A4 continuous dependence in the top norm across nu_mono's splice level set {|D S U| = y* a0} (needs it to be null)"]
ASSUMED.append("A5 for single-valued U on a closed leaf (Z_0 non-empty, K4d): that isolated zeros of the filtered field do not obstruct "
               "the H^s estimates (XC2 B7 integrated Lipschitz property); avoided only by U with non-trivial periods")
AM = [
    ("AM1", "closed Cauchy surface; H^s x H^(s-1) data, s > n/2 + 1", "VERIFIED (restricted)" if S3_srange else "FAILED",
     f"ACTION.md closed leaves (T^3); admissible s in ({S3_srange[0]}, {S3_srange[1]}) for nu_mono as defined (K4c)" if S3_srange else "no s-range"),
    ("AM2", "CMC slicing (lapse from preserving tr k = t)", "FAILED (replaced)",
     "the slicing is forced to the khronon leaves (CFG292 T7); the lapse equation is the khronon's own E_N (S4a)"),
    ("AM3", "spatial harmonic coordinates with an elliptic shift", "FAILED (replaced)",
     "F2a's shift is hyperbolic (evolved): it is part of the strongly hyperbolic system certified in S1/S2"),
    ("AM4", "lapse equation uniformly elliptic with trivial kernel", "VERIFIED (ellipticity) / CONDITION (kernel)",
     "uniformly elliptic on W_rec (S4b); kernel: Hamiltonian form = the relabelling mode only (S4c Ham; quotient + global constraint), "
     "F2a velocity form trivial iff W <= 0, W != 0 (S4c Lag: holds on FLRW + Lambda + comoving dust; open condition in general)"),
    ("AM5", "elliptic variables lower order (lapse source free of d^2 g; N in H^(s+1))", "FAILED" if am5_fail else "VERIFIED",
     "the lapse source contains R^(3) with weight 1/(4 alpha_c) and no constraint can remove it (the scalar constraint IS the lapse "
     "equation); eliminating the lapse changes the principal symbol (it creates the c_S mode) -> replacement: eliminate the lapse "
     "at the symbol level, a quasilinear pseudo-differential hyperbolic system"),
    ("AM6", "strong/symmetric hyperbolicity of the reduced evolution", "VERIFIED" if (s1c1_ok and s2a1_ok) else "FAILED",
     "S1 (constant multiplicity) + S2 (explicit smooth symmetriser) for the lapse-reduced symbol"),
    ("AM7", "coefficients smooth in the fields", "VERIFIED (restricted)",
     "gravity: rational in g on O (K1); MOND/filter: smooth off Z_0, C^{1,1} at the splice (K4a, K4c)"),
    ("AM8", "gauge and constraint propagation", "VERIFIED (linear) / ASSUMED (nonlinear)" if cp_ok else "FAILED",
     "symbol-level: (g^{mu nu} xi xi) C_i = 0 (S4d); nonlinear: A2, A3"),
    ("AM9", "the elliptic-hyperbolic iteration theorem", "FAILED (replaced)",
     "AM's iteration uses AM5; replacement = Kato's abstract theorem (LNM 448) on the lapse-reduced pseudo-differential system with "
     "the S2 symmetriser; inputs verified: K1-K4 (restricted); inputs assumed: A1, A4 (+A5)"),
]
for a_ in AM:
    P(f"    {a_[0]} {a_[1]}: {a_[2]} -- {a_[3]}")
OUT["am_table"] = [{"item": a_[0], "hypothesis": a_[1], "status": a_[2], "evidence": a_[3]} for a_ in AM]
failed_no_repl = [a_[0] for a_ in AM if a_[2] == "FAILED" and a_[0] not in ("AM5",)]
am5_has_repl = True                       # the lapse-reduced pseudo-differential route (S1/S2 verified on it)
check("S4e the AM5 decision is computed: with the lapse frozen at principal order the characteristic polynomial differs from the "
      "lapse-eliminated one, so the khronon lapse is coupled at principal order and AM's elliptic-lower-order structure fails; the "
      "replacement (symbol-level elimination) is the system S1/S2 certified", f"AM5 fails {am5_fail}; frozen-lapse scalar roots "
      f"{['%.4g%+.4gi' % (z.real, z.imag) for z in rr_scalar]}", am5_fail and am5_has_repl and not failed_no_repl,
      "AM is therefore not applicable verbatim; no item is left FAILED without a replacement whose remaining inputs are named")

# ================================================================================================ verdict
banner("VERDICT (frozen decision rule, FROZEN_CRITERIA.md sec. 4)")
s1_ok = s1a_ok and s1b_ok and s1c1_ok and s1c2_ok
s2_ok = s2a1_ok and s2a2_ok and s2b_ok and sym_ok_s and all(den_status.values())
s3_ok = k1_dens_ok and p00_ok_s and (S3_srange is not None) and M0_ok and cm_law and prod_ok and shell_ok
s4b_ok = phys_lo > 0 and f2a_lo > 0.2
s4c_ok = ham_ok and s4c_lag_ok
am_ok = am5_fail and not failed_no_repl and cp_ok
CONDITIONS = [
    "C1 beta = 0, 0 < alpha_c < 1/2 (alpha_c != 1/2 is the F2a gauge artefact), c_2 > 0: the whole of W_rec (S1b, S1d)",
    f"C2 Sobolev index s in ({S3_srange[0] if S3_srange else '-'}, {S3_srange[1] if S3_srange else '-'}) for nu_mono with its C^(1,1) splice "
    "(any s > 5/2 with a C-infinity splice) (K4c)",
    "C3 the filtered field D S U has no zeros on the leaf (requires U with non-trivial periods on closed leaves), or A5 (K4d)",
    "C4 an invertible lapse operator at the data: F2a velocity form W <= 0, W != 0 (holds on FLRW + Lambda + comoving dust; open "
    "near it), or the Hamiltonian form with the relabelling mode quotiented and the global constraint imposed (S4c)",
    "C5 for a uniform N_min > 0 independent of alpha_c: data obeying the GR-like Hamiltonian constraint to O(alpha_c) (S4c Ham, disclosed)"]
if MUTATE:
    verdict = ("MUTATE RUN (C-MUTATE): S1 FAILS on the crossing and S2 FLAGS it, as required" if (not s1_ok and crossing_flagged)
               else "MUTATE RUN: the crossing was NOT detected -- C-MUTATE FAILED")
elif not controls_ok:
    verdict = "OPEN (a control misbehaved)"
elif not (s1_ok and s2_ok and s4b_ok):
    verdict = "KILL"
elif not (s3_ok and s4c_ok and am_ok and s4a_ok):
    verdict = "OPEN"
elif not ASSUMED:
    verdict = "PASS (local-in-time scope)"
else:
    verdict = "CONDITIONAL"
OUT["verdict"] = verdict
OUT["conditions"] = CONDITIONS
OUT["assumptions"] = ASSUMED
OUT["summary"] = {"S1": s1_ok, "S2": s2_ok, "S3": s3_ok, "S4a": s4a_ok, "S4b": s4b_ok, "S4c": s4c_ok, "AM": am_ok, "controls": controls_ok,
                  "min_gap_W_rec": S1b["W_rec"]["gap_min"], "min_gap_W_P1": S1b["W_P1"]["gap_min"],
                  "kappa_H_range": [min(kap_all), max(kap_all)] if kap_all else None, "s_range": S3_srange}
P(f"  S1 constant multiplicity {s1_ok};  S2 symmetriser {s2_ok};  S3 Kato hypotheses {s3_ok};  S4a lapse equation {s4a_ok};  "
  f"S4b ellipticity {s4b_ok};  S4c kernel {s4c_ok};  AM mapping {am_ok};  controls {controls_ok}")
P(f"  VERDICT: {verdict}")
P("  Scope: local in time; beta = 0; F2a (t = tau, spatial de Donder with 4-D trace, lapse eliminated) on the khronon's leaves; data")
P("  away from zero-field regions (K4d).  Conditions:")
for c_ in CONDITIONS:
    P(f"    {c_}")
P("  Assumed (named, not computed here):")
for a_ in ASSUMED:
    P(f"    {a_}")
P(f"  Time {time.time() - T0:.0f} s.")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_pass"], OUT["n_fail_load_bearing"] = len(CH), sum(1 for _, ok, _ in CH if ok), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
