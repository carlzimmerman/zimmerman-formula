#!/usr/bin/env python3
"""w1_5_couplings_and_scale -- what can a division-algebra / exceptional construction say about a gauge COUPLING?  Pre-registered K1-K4.

K1  number of independent kinetic coefficients (Ad-invariant symmetric bilinear forms) of the gauge algebras that occur (numerical SVD of the invariance equations);
K2  embedding table alpha_i / alpha_G and sin^2 theta_W from Killing-form norms of Cartan vectors (exact Fractions);
K3  ratio-only joint running test against the SM trajectories of lane U3 (imported READ-ONLY; no value of alpha is tested, only ratio rules);
K4  extra charged spectrum bookkeeping (exact one-loop coefficients) and its effect on 1/alpha_em(M_P).
Run (real):    python3 w1_5_couplings_and_scale.py          -> exit 0 if every check passes (2 otherwise)
Run (control): python3 w1_5_couplings_and_scale.py MUTATE   -> uses the SHORT-root Cartan vector for colour in the F4 row (wrong embedding index); exit 1 if the control bites, 3 if it does not.
Needs ../U3_invented_uv_boundary/u3_lib.py (and, through it, lanes B and N1) to be present; nothing outside this directory is written.
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import itertools
from fractions import Fraction as F
import numpy as np
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w1_lib as W

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
chk = W.Checks(MUT)
np.seterr(all="ignore")

# ============================================================ K1: invariant symmetric forms
def gellmann(n):
    """Hermitian traceless basis of su(n), normalised tr(T_a T_b) = delta/2 (unnormalised generalised Gell-Mann)."""
    mats = []
    for i in range(n):
        for j in range(i + 1, n):
            m = np.zeros((n, n), complex); m[i, j] = m[j, i] = 1; mats.append(m / 2)
            m = np.zeros((n, n), complex); m[i, j] = -1j; m[j, i] = 1j; mats.append(m / 2)
    for k in range(1, n):
        m = np.zeros((n, n), complex)
        for i in range(k): m[i, i] = 1
        m[k, k] = -k
        mats.append(m / math.sqrt(2 * k * (k + 1)))
    return mats
def blockdiag(*blocks):
    n = sum(b.shape[0] for b in blocks)
    out = np.zeros((n, n), complex); o = 0
    for b in blocks:
        out[o:o + b.shape[0], o:o + b.shape[0]] = b; o += b.shape[0]
    return out
def embed(m, sizes, pos):
    blocks = [np.zeros((s, s), complex) for s in sizes]; blocks[pos] = m
    return blockdiag(*blocks)
def so_basis(n):
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            m = np.zeros((n, n), complex); m[i, j] = 1; m[j, i] = -1; out.append(1j * m)      # hermitian generators i*(E_ij - E_ji)
    return out
def invariant_form_dim(herm_gens, n_random=0, seed=0):
    X = [1j * g for g in herm_gens]                                   # anti-hermitian
    n = len(X)
    Gm = np.array([[np.real(np.trace(a.conj().T @ b)) for b in X] for a in X])
    def coords(M):
        rhs = np.array([np.real(np.trace(a.conj().T @ M)) for a in X])
        c = np.linalg.solve(Gm, rhs)
        assert np.max(np.abs(sum(ci * a for ci, a in zip(c, X)) - M)) < 1e-9, "not closed"
        return c
    def ad(v):                                                        # ad(x) for x = sum v_a X_a in the basis
        x = sum(vi * a for vi, a in zip(v, X))
        return np.array([coords(x @ b - b @ x) for b in X]).T
    if n_random:
        rng = np.random.default_rng(seed)
        vs = [rng.standard_normal(n) for _ in range(n_random)]
    else:
        vs = [np.eye(n)[i] for i in range(n)]
    idx = [(a, b) for a in range(n) for b in range(a, n)]
    pos = {p: k for k, p in enumerate(idx)}
    rows = []
    for v in vs:
        A = ad(v)                                                     # (ad_v)^d_c
        for c in range(n):
            for d in range(c, n):
                row = np.zeros(len(idx))
                # (A^T B + B A)_{cd} = sum_e A_ec B_ed + B_ce A_ed
                for e in range(n):
                    row[pos[(min(e, d), max(e, d))]] += A[e, c]
                    row[pos[(min(c, e), max(c, e))]] += A[e, d]
                rows.append(row)
    sv = np.linalg.svd(np.array(rows), compute_uv=False)
    return len(idx) - int(np.sum(sv > 1e-9))
s3 = gellmann(3); s2 = [np.array(m, complex) / 2 for m in ([[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]])]
sizes = (3, 2, 1)
SM12 = [embed(m, sizes, 0) for m in s3] + [embed(m, sizes, 1) for m in s2] + [embed(np.eye(1, dtype=complex), sizes, 2)]
sizes2 = (3, 2, 1, 1)
SMBL = [embed(m, sizes2, 0) for m in s3] + [embed(m, sizes2, 1) for m in s2] + [embed(np.eye(1, dtype=complex), sizes2, 2), embed(np.eye(1, dtype=complex), sizes2, 3)]
sizes3 = (3, 1)
SU3U1 = [embed(m, sizes3, 0) for m in s3] + [embed(np.eye(1, dtype=complex), sizes3, 1)]
U3 = list(s3) + [np.eye(3, dtype=complex)]
dims = {"su(3)+su(2)+u(1) (the SM algebra)": (invariant_form_dim(SM12), 3),
        "SM + u(1)_(B-L)": (invariant_form_dim(SMBL), 5),
        "su(3)+u(1)_em (unbroken)": (invariant_form_dim(SU3U1), 2),
        "u(3) (Furey's ladder symmetry)": (invariant_form_dim(U3), 2),
        "su(4)  (= spin(6), Cl(6) bivectors)": (invariant_form_dim(gellmann(4)), 1),
        "spin(10) (random-element method, 4 generic elements)": (invariant_form_dim(so_basis(10), n_random=4, seed=3), 1)}
for k, (got, exp) in dims.items():
    print(f"      invariant symmetric forms on {k}: {got} (expected {exp})")
chk("K1 the number of independent gauge kinetic coefficients equals the number of simple factors + a symmetric matrix per abelian block: SM 3, SM+B-L 5, su(3)+u(1) 2, u(3) 2, su(4) 1, spin(10) 1 (Schur): each algebraic construction leaves EXACTLY that many free real parameters 1/g^2",
    all(got == exp for (got, exp) in dims.values()))
print("      K1 statement: the algebras have integer or rational structure constants and no length scale; a coupling can only enter as the free coefficient of the invariant form.")

# ============================================================ K2: embedding table
def dotv(u, v): return sum(a * b for a, b in zip(u, v))
def alpha_ratio(v): return 1 / (2 * dotv(v, v))                     # alpha_H / alpha_G for a U(1) direction with Cartan vector v (roots of norm^2 2 for the long roots)
rows = {}
# SU(5) / Spin(10)  (roots norm^2 2 in the R^5 realisation)
v_T3 = (0, 0, 0, F(1, 2), F(-1, 2))
v_Y = (F(-1, 3), F(-1, 3), F(-1, 3), F(1, 2), F(1, 2))
v_c = (F(1, 2), F(-1, 2), 0, 0, 0)
v_Q = tuple(a + b for a, b in zip(v_T3, v_Y))
rows["SU(5) (5bar + 10), Spin(10) (16), E6 (27)"] = dict(a3=alpha_ratio(v_c), a2=alpha_ratio(v_T3), aY=alpha_ratio(v_Y), aem=alpha_ratio(v_Q))
# F4: colour = long A2 root e1-e2 (norm^2 2), SU(2) = short root e4 (norm^2 1), Y = (e1+e2+e3)/3 as a Cartan vector
vc4 = (F(1, 2), F(-1, 2), 0, 0)
if MUT:
    vc4 = (F(1), 0, 0, 0)                                          # MUTATE: a SHORT root (norm^2 1) used as the colour A2
vT34 = (0, 0, 0, F(1))
vY4 = (F(1, 3), F(1, 3), F(1, 3), 0)
vQ4 = tuple(a + b for a, b in zip(vT34, vY4))
rows["F4 (26)"] = dict(a3=alpha_ratio(vc4), a2=alpha_ratio(vT34), aY=alpha_ratio(vY4), aem=alpha_ratio(vQ4))
# Spin(6) = SU(4) alone (Cl(6)): the non-constant part of Q is (B-L)/2 = diag(1/6,1/6,1/6,-1/2) on the 4
v_x = (F(1, 6), F(1, 6), F(1, 6), F(-1, 2))
rows["Spin(6)=SU(4) alone: (B-L)/2 vs colour"] = dict(a3=F(1), a2=None, aY=None, aem=None, aX=alpha_ratio(v_x))
for k, r in rows.items():
    s2w = None if r["aY"] is None else r["aY"] / (r["aY"] + r["a2"])
    print(f"      {k}: alpha_3 = {r['a3']}, alpha_2 = {r['a2']}, alpha_Y = {r['aY']}, alpha_em = {r['aem']} (units of alpha_G)" + (f", (B-L)/2: {r['aX']}" if 'aX' in r else "") + (f", sin^2 = {s2w}" if s2w is not None else ""))
r5 = rows["SU(5) (5bar + 10), Spin(10) (16), E6 (27)"]; r4 = rows["F4 (26)"]
chk("K2a SU(5)/Spin(10)/E6: alpha_3 = alpha_2 = alpha_G, alpha_Y = (3/5) alpha_G, alpha_em = (3/8) alpha_G, sin^2 theta_W = 3/8", (r5["a3"], r5["a2"], r5["aY"], r5["aem"]) == (F(1), F(1), F(3, 5), F(3, 8)) and r5["aY"] / (r5["aY"] + r5["a2"]) == F(3, 8))
chk("K2b F4: alpha_3 : alpha_2 : alpha_Y = 1 : 1/2 : 3/2, alpha_em = (3/8) alpha_G, sin^2 theta_W = 3/4 (the SAME alpha_em/alpha_3 = 3/8 but a different weak mixing angle)", (r4["a3"], r4["a2"], r4["aY"], r4["aem"]) == (F(1), F(1, 2), F(3, 2), F(3, 8)) and r4["aY"] / (r4["aY"] + r4["a2"]) == F(3, 4))
chk("K2c Spin(6) alone: the em generator Q = (B-L)/2 + 1/2 has its constant part outside spin(6), so alpha_em is NOT tied to alpha_4 by Cl(6) (only alpha_{(B-L)/2} = (3/2) alpha_4 is)", rows["Spin(6)=SU(4) alone: (B-L)/2 vs colour"]["aX"] == F(3, 2))
# Pati-Salam: three couplings
g4, gL, gR = sp.symbols("a4 aL aR", positive=True)                  # alphas
aX = sp.Rational(3, 2) * g4
aY_ps = 1 / (1 / gR + 1 / aX)
a_em = 1 / (1 / gL + 1 / aY_ps)
s2_ps = sp.simplify(a_em / gL)
chk("K2d Pati-Salam SU(4) x SU(2)_L x SU(2)_R: sin^2 theta_W is a free function of the three couplings; it equals 3/8 iff alpha_4 = alpha_L = alpha_R (a coupling relation IMPOSED, not derived) and is homogeneous of degree 0 (the overall scale drops out)",
    sp.simplify(s2_ps.subs({g4: 1, gL: 1, gR: 1}) - sp.Rational(3, 8)) == 0 and sp.simplify(s2_ps.subs({g4: 2 * g4, gL: 2 * gL, gR: 2 * gR}) - s2_ps) == 0 and sp.simplify(s2_ps.subs({g4: 1, gL: 1, gR: 2}) - sp.Rational(3, 8)) != 0)

# ============================================================ K3: ratio rules against the SM running (lane U3 library, read only)
try:
    sys.path.insert(0, os.path.join(HERE, "..", "U3_invented_uv_boundary"))
    import u3_lib as U3
    have_u3 = True
except Exception as ex:                                            # pragma: no cover
    have_u3 = False
    print("      u3_lib import failed:", repr(ex))
chk("K3-0 lane U3's library imports read-only", have_u3)
if have_u3:
    from scipy.optimize import brentq
    res3 = {}
    for name in ("2L-T", "1L-T"):
        sh = U3.Shifted(U3.get_traj(name), None)
        X12 = U3.solve_cross(sh, "a1", "a2")
        A12 = sh.A(X12)
        mis = U3.coup(A12, "a3") / U3.coup(A12, "a1") - 1
        # F4 rule: a_2 = 2 a_3 (alpha_3 = 2 alpha_2), and then a_Y = a_2 / 3
        lo, hi = math.log(U3.MZ * 1.001), min(math.log(U3.XP), sh.lnmax - 1e-6)
        f = lambda lm: sh.A(math.exp(lm))[1] - 2 * sh.A(math.exp(lm))[2]
        xs = np.linspace(lo, hi, 600)
        fx = [f(x) for x in xs]
        cross = [i for i in range(len(xs) - 1) if fx[i] * fx[i + 1] < 0]
        if cross:
            i = cross[0]
            lm = brentq(f, xs[i], xs[i + 1])
            Ax = sh.A(math.exp(lm))
            ratio_YZ = Ax[0] / Ax[1]
            res3[name] = (X12, mis, math.exp(lm), ratio_YZ)
        else:
            res3[name] = (X12, mis, None, None)
        # is a_Y / a_2 = 1/3 attained anywhere below M_P ?
        g = lambda lm: sh.A(math.exp(lm))[0] / sh.A(math.exp(lm))[1] - 1 / 3
        gx = [g(x) for x in xs]
        res3[name] += (any(gx[i] * gx[i + 1] < 0 for i in range(len(xs) - 1)),)
        print(f"      {name}: GUT-normalised a_1 = a_2 at {X12:.3e} GeV, a_3 mismatch {mis * 100:+.1f}%; F4 rule a_2 = 2 a_3 at " + (f"{res3[name][2]:.3e} GeV where a_Y/a_2 = {res3[name][3]:.3f} (F4 needs 1/3)" if res3[name][2] else "no scale below M_P") + f"; a_Y/a_2 = 1/3 reached below M_P: {res3[name][4]}")
    ok_a = all(abs(v[1]) > 0.01 for v in res3.values())
    ok_b = all((v[2] is None) or abs(v[3] - 1 / 3) > 0.01 * (1 / 3) for v in res3.values()) and not any(v[4] for v in res3.values())
    chk("K3a the SU(5)/Spin(10)/E6 rule a_1 = a_2 = a_3 is NOT met by the SM-only running: alpha_3 misses by more than 1% at the a_1 = a_2 crossing (-13% at one loop, as in lanes G and U3 V03-V05)", ok_a)
    chk("K3b the F4 rule (a_3 : a_2 : a_Y = 1 : 2 : 2/3, i.e. alpha_2 = alpha_3/2 and alpha_Y = 3 alpha_3/2) is NOT met at any scale below M_P by SM-only running", ok_b)
    print("      K3 statement: these are ratio rules; they say nothing about the constructions themselves (none of the papers claims coupling unification) -- they bound what a UNIFIED reading of the embedding would predict.")

# ============================================================ K4: extra charged spectrum
Fr = F
def bcoef(weyl, scal):
    """(b_Y, b_2, b_3) increments: weyl list of (d3, d2, Y), scal list of complex scalar multiplets, Weyl fermions contribute (2/3)*, complex scalars (1/3)*."""
    T2 = lambda d: Fr(1, 2) if d == 2 else (Fr(2) if d == 3 else Fr(0))
    T3 = lambda d: Fr(1, 2) if d == 3 else Fr(0)
    bY = sum(Fr(2, 3) * d3 * d2 * y * y for d3, d2, y in weyl) + sum(Fr(1, 3) * d3 * d2 * y * y for d3, d2, y in scal)
    b2 = sum(Fr(2, 3) * T2(d2) * d3 for d3, d2, y in weyl) + sum(Fr(1, 3) * T2(d2) * d3 for d3, d2, y in scal)
    b3 = sum(Fr(2, 3) * T3(d3) * d2 for d3, d2, y in weyl) + sum(Fr(1, 3) * T3(d3) * d2 for d3, d2, y in scal)
    return bY, b2, b3
SMw = [(3, 2, Fr(1, 6)), (3, 1, Fr(-2, 3)), (3, 1, Fr(1, 3)), (1, 2, Fr(-1, 2)), (1, 1, Fr(1)), (1, 1, Fr(0))] * 3
SMh = [(1, 2, Fr(1, 2))]
bY0, b20, b30 = bcoef(SMw, SMh)
bY0, b20, b30 = bY0, b20 - Fr(22, 3), b30 - Fr(11)
chk("K4a the one-loop coefficients of the field content of construction A (3 x one generation incl. nu_R, one Higgs doublet) are the SM values (41/6, -19/6, -7): nu_R is neutral and adds nothing", (bY0, b20, b30) == (Fr(41, 6), Fr(-19, 6), Fr(-7)))
exo_w = [(3, 1, Fr(-1, 3)), (3, 1, Fr(1, 3)), (1, 2, Fr(1, 2)), (1, 2, Fr(-1, 2)), (1, 1, Fr(0))]              # 10 + 1 of E6 per generation (as Weyl multiplets)
dbY, db2, db3 = bcoef(exo_w, [])
chk("K4b one E6 exotic set (5 + 5bar + 1) per generation shifts (b_Y, b_2, b_3) by (10/9, 2/3, 2/3)", (dbY, db2, db3) == (Fr(10, 9), Fr(2, 3), Fr(2, 3)), f"({dbY}, {db2}, {db3})")
if have_u3:
    chk("K4c cross-check of the bookkeeping against lane U3's multiplet increments: Y=1 Dirac singlet 4/3, vector-like doublet 2/3, vector-like triplet 2/3", (bcoef([(1, 1, Fr(1)), (1, 1, Fr(-1))], [])[0], bcoef([(1, 2, Fr(0)), (1, 2, Fr(0))], [])[1], bcoef([(3, 1, Fr(0)), (3, 1, Fr(0))], [])[2]) == tuple(Fr(x).limit_denominator(3) for x in U3.DB_MULT))
    XP = U3.XP
    a_em_SM = 104.94
    for Mex in (1e3, 1e10):
        shift = 3 * (float(dbY) + float(db2)) / (2 * math.pi) * math.log(XP / Mex)
        print(f"      three E6 exotic sets at {Mex:.0e} GeV: 1/alpha_em(M_P) shifts by -{shift:.1f}  (SM: {a_em_SM}) -> {a_em_SM - shift:.1f} ({-shift / a_em_SM * 100:.0f}%)")
    shift3 = 3 * (float(dbY) + float(db2)) / (2 * math.pi) * math.log(XP / 1e3)
    chk("K4d if the exotic states of the 27 were at 1 TeV the running of 1/alpha_em to M_P would change by more than 20% relative to the SM value: the spectrum (its masses) is not fixed by the algebra, so the ultraviolet value of any coupling is not either", shift3 / a_em_SM > 0.2)
    print("      K4 statement: construction A carries the SM charged content only (best case); the Jordan constructions add vector-like charged states (E6: 8 charged per 27; F4: a charged isospin triplet and vector-like doublets) with unfixed masses.")
chk.finish("w1_5")
