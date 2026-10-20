#!/usr/bin/env python3
"""CFG899 -- alpha door D08: the charged vector boson in dS_4 with a covariant (R_xi, Higgs/Goldstone) completion; closes S1.

Pre-registered in CFG899_PREREGISTRATION.md (frozen, commit e56c96770; Amendment A1 appended post hoc after the first execution).  STRUCTURAL CLOSURE: alpha (e) stays a free symbol,
no number is compared with 137.036, N_mech is unchanged (374).  Units H = 1, planar patch a = -1/tau, signature (-+++), MTW curvature.

Usage (from any directory; one core, a few minutes, watchdog at 900 MB):
    OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 python3 -B cfg899_d08.py               real run     -> exit 0 iff CLOSED (A, B, C, E pass)
    OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 python3 -B cfg899_d08.py MUTATE_SPIN   g = 2 -> 1   -> exit 1 iff the control works
    OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 python3 -B cfg899_d08.py MUTATE_DIM    D = 4 -> 6   -> exit 1 iff the control works
Any other argument runs the real path.  The MUTATE_SPIN L-checks read the real run's cfg899_d08.json (run the real path first).

Parts:  A structure (operator identities in dS_4, sympy, exact);  B UV structure (a_2, regulators, proper-time factors);
        C heavy-mass current from the recalled a_3 with an explicit vector-bundle trace code + S2's current pipeline (imported read-only);
        D gauge-parameter dependence (flat momentum space, general xi, plus the exact formula H4);  E selection classifier.
Imported read-only (no file of another lane is written; bytecode disabled):
    real_research/alpha_principle_2026/S2_fermion_independent/s2_4_heavy_mass_current.py  (geometry, current_from_L, Dirac reduction)
    real_research/alpha_principle_2026/Q1_ds4_fermions/q1_lib.py                         (scalar_closed_f = AH4 (2.58), hfy_weak = Q1)
"""
import sys
sys.dont_write_bytecode = True
import os
import re
import json
import math
import time
import resource
import threading
import itertools
import sympy as sp
import mpmath as mp
from sympy.calculus.euler import euler_equations
from sympy.polys.rings import ring
from sympy.polys.domains import QQ

MODE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("MUTATE_SPIN", "MUTATE_DIM") else "REAL"
G_GRADED = 1 if MODE == "MUTATE_SPIN" else 2          # gyromagnetic ratio of the graded chain
D_COUNT = 6 if MODE == "MUTATE_DIM" else 4            # dimension used in the multiplicity count (B1, B4)

LIMIT = 900 * 1024 * 1024


def _watchdog():
    while True:
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > LIMIT:
            print("WATCHDOG: peak RSS above 900 MB, aborting", flush=True)
            os._exit(4)
        time.sleep(1.0)


threading.Thread(target=_watchdog, daemon=True).start()
T0 = time.time()

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
AP = os.path.join(ROOT, "real_research", "alpha_principle_2026")
S2DIR = os.path.join(AP, "S2_fermion_independent")
Q1DIR = os.path.join(AP, "Q1_ds4_fermions")
S1DIR = os.path.join(AP, "S1_vector_bosons")
AH4OUT = os.path.join(ROOT, "real_research", "alpha_schwinger_2026", "ah4_induced_current_ds4.out")
sys.path.insert(0, S2DIR)
sys.path.insert(0, Q1DIR)
_argv = sys.argv
sys.argv = [_argv[0]]                                  # imported modules must not see any control argument
import s2_4_heavy_mass_current as S2                    # noqa: E402  (read-only)
from q1_lib import scalar_closed_f, hfy_weak            # noqa: E402  (read-only)
sys.argv = _argv

CHECKS = {}          # tag -> bool
GROUP = {}           # tag -> part letter
RES = {"mode": MODE, "g_graded": G_GRADED, "D_count": D_COUNT}


def check(tag, part, ok, detail=""):
    CHECKS[tag] = bool(ok)
    GROUP[tag] = part
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def stamp(label):
    print(f"   [{label}: {time.time() - T0:.1f} s, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576:.0f} MB]", flush=True)


def is_zero(expr):
    return sp.simplify(sp.expand(expr)) == 0


# =============================================================================================== geometry (S2's, read-only)
X = S2.X                       # (tau, x, y, z)
tau = X[0]
fA = S2.f                      # A_z = f(tau)
Esym = S2.Esym
GEO = S2.build_geometry()
a_, gmet, gi, Gam, RM, Ric, Rs = GEO
sqrtg = a_ ** 4                # sqrt(-g) for a = -1/tau
esym, msym = sp.symbols("e m", positive=True)
lam, mu = sp.symbols("lambda mu", positive=True)
kx, kz = sp.symbols("k_x k_z", real=True)
N4 = range(4)


def Dcov(T, m, q, A):
    """U(1)-covariant partial derivative of a component of charge q (units of e): d_m - i q e A_m."""
    return sp.diff(T, X[m]) - sp.I * q * esym * A[m] * T


def field_strength(A):
    return [[sp.diff(A[n], X[m]) - sp.diff(A[m], X[n]) for n in N4] for m in N4]


def lagr_W(W, Wc, p, xi, A):
    """sqrt(-g)[ -(1/2) Wbar_mn W^mn - m^2 Wbar.W + p Wbar^m Omega_mn W^n - (1/xi) |D.W|^2 ],  Omega = -i e F."""
    F = field_strength(A)
    Om = [[-sp.I * esym * F[m][n] for n in N4] for m in N4]
    Wmn = [[Dcov(W[n], m, 1, A) - Dcov(W[m], n, 1, A) for n in N4] for m in N4]
    Wcmn = [[Dcov(Wc[n], m, -1, A) - Dcov(Wc[m], n, -1, A) for n in N4] for m in N4]
    kin = -sp.Rational(1, 2) * sum(gi[m] * gi[n] * Wcmn[m][n] * Wmn[m][n] for m in N4 for n in N4)
    mass = -msym ** 2 * sum(gi[m] * Wc[m] * W[m] for m in N4)
    pauli = p * sum(gi[m] * gi[n] * Wc[m] * Om[m][n] * W[n] for m in N4 for n in N4)
    divW = sum(sp.diff(sqrtg * gi[m] * W[m], X[m]) for m in N4) / sqrtg - sp.I * esym * sum(A[m] * gi[m] * W[m] for m in N4)
    divWc = sum(sp.diff(sqrtg * gi[m] * Wc[m], X[m]) for m in N4) / sqrtg + sp.I * esym * sum(A[m] * gi[m] * Wc[m] for m in N4)
    gf = -(1 / xi) * divWc * divW
    return sqrtg * (kin + mass + pauli + gf)


def nabla_vec(W, q, A):
    return [[Dcov(W[n], r, q, A) - sum(Gam[l][r][n] * W[l] for l in N4) for n in N4] for r in N4]


def box_vec(W, q, A):
    T = nabla_vec(W, q, A)
    out = []
    for n in N4:
        s_ = 0
        for m in N4:
            val = Dcov(T[m][n], m, q, A) - sum(Gam[l][m][m] * T[l][n] + Gam[l][m][n] * T[m][l] for l in N4)
            s_ += gi[m] * val
        out.append(s_)
    return out


def Delta_op(W, g_, A, q=1):
    """(Delta_g W)_n = -box W_n + R_n^s W_s + m^2 W_n - g Omega_n^s W_s   (xi = 1, Laplace type)."""
    F = field_strength(A)
    Om = [[-sp.I * esym * q * F[m][n] for n in N4] for m in N4]
    bx = box_vec(W, q, A)
    return [-bx[n] + sum(Ric[n][s] * gi[s] * W[s] for s in N4) + msym ** 2 * W[n] - g_ * sum(Om[n][s] * gi[s] * W[s] for s in N4) for n in N4]


def box_scalar(th, q, A):
    Dth = [Dcov(th, m, q, A) for m in N4]
    return sum(sp.diff(sqrtg * gi[m] * Dth[m], X[m]) for m in N4) / sqrtg - sp.I * q * esym * sum(A[m] * gi[m] * Dth[m] for m in N4)


def div_Omega(A):
    """nabla^m Omega_mn for Omega = -i e F (neutral 2-form)."""
    F = field_strength(A)
    Om = [[-sp.I * esym * F[m][n] for n in N4] for m in N4]
    out = []
    for n in N4:
        s_ = 0
        for m in N4:
            val = sp.diff(Om[m][n], X[m]) - sum(Gam[l][m][m] * Om[l][n] + Gam[l][m][n] * Om[m][l] for l in N4)
            s_ += gi[m] * val
        out.append(sp.simplify(s_))
    return out


# =============================================================================================== PART A
def part_A():
    print("\n" + "=" * 118 + "\nPART A. Structure of the R_xi completion in dS_4 (sympy, exact)\n" + "=" * 118, flush=True)
    A = [0, 0, 0, fA(tau)]
    # A1 geometry
    okR = sp.simplify(Rs - 12) == 0
    okRic = all(sp.simplify(Ric[i][j] - 3 * gmet[i, j]) == 0 for i in N4 for j in N4)
    okRiem = all(sp.simplify(RM[i][j][k][l] - (gmet[i, k] * gmet[j, l] - gmet[i, l] * gmet[j, k])) == 0 for i, j, k, l in itertools.product(N4, repeat=4))
    okDR = True
    for l, r, s, m, n in itertools.product(N4, repeat=5):
        val = sp.diff(RM[r][s][m][n], X[l]) - sum(Gam[p][l][r] * RM[p][s][m][n] + Gam[p][l][s] * RM[r][p][m][n] + Gam[p][l][m] * RM[r][s][p][n] + Gam[p][l][n] * RM[r][s][m][p] for p in N4)
        if sp.simplify(val) != 0:
            okDR = False
            break
    dOm = div_Omega(A)
    Vz = sp.simplify((dOm[3] / (-sp.I * esym)).subs(fA(tau), -Esym / tau).doit())
    Vphys = sp.simplify(Vz / a_)
    okV = sp.simplify(sp.Abs(Vphys.subs(tau, -1)) - 2 * Esym) == 0
    check("A1", "A", okR and okRic and okRiem and okDR and okV,
          f"R = 12, R_mn = 3 g_mn, R_mnrs = g g - g g, nabla Riem = 0, |nabla^n F_nz| = 2E at tau = -1 (coordinate {Vz}; AH4 V3, S2 D0c)")
    stamp("A1")

    # A2 operator identity at xi = 1 for g = 1, 2 (generic complex W)
    W = [sp.Function(f"W{i}")(*X) for i in N4]
    Wc = [sp.Function(f"Wc{i}")(*X) for i in N4]
    okA2 = True
    for g_ in (1, 2):
        L = lagr_W(W, Wc, g_ - 1, 1, A)
        EL = euler_equations(L, Wc, X)
        Op = Delta_op(W, g_, A)
        for n in N4:
            res = sp.expand(EL[n].lhs + sqrtg * gi[n] * Op[n])
            if sp.simplify(res) != 0:
                okA2 = False
                print(f"     A2 residual g = {g_}, n = {n}: {sp.simplify(res)}")
    check("A2", "A", okA2, "Euler-Lagrange(Wbar) of the xi = 1 action = -sqrt(-g) g^nn (-box + Ric + m^2 - g Omega) W_n, for g = 1 (p = 0) and g = 2 (p = 1)")
    stamp("A2")

    # A3 W-phi mixing cancels for symbolic xi
    xi = sp.symbols("xi", positive=True)
    ph = sp.Function("phi")(*X)
    phc = sp.Function("phic")(*X)
    Dph = [Dcov(ph, m, 1, A) for m in N4]
    Dphc = [Dcov(phc, m, -1, A) for m in N4]
    divW = sum(sp.diff(sqrtg * gi[m] * W[m], X[m]) for m in N4) / sqrtg - sp.I * esym * sum(A[m] * gi[m] * W[m] for m in N4)
    divWc = sum(sp.diff(sqrtg * gi[m] * Wc[m], X[m]) for m in N4) / sqrtg + sp.I * esym * sum(A[m] * gi[m] * Wc[m] for m in N4)
    # full phi-sector + gauge fixing, expanded: -|D phi - m W|^2 - (1/xi)|D.W - xi m phi|^2 ; keep only the W-phi cross terms
    L_full = sqrtg * (-sum(gi[m] * (Dphc[m] - msym * Wc[m]) * (Dph[m] - msym * W[m]) for m in N4) - (1 / xi) * (divWc - xi * msym * phc) * (divW - xi * msym * ph))
    L_noW = sqrtg * (-sum(gi[m] * Dphc[m] * Dph[m] for m in N4) - xi * msym ** 2 * phc * ph)
    L_noPhi = sqrtg * (-msym ** 2 * sum(gi[m] * Wc[m] * W[m] for m in N4) - (1 / xi) * divWc * divW)
    L_cross = sp.expand(L_full - L_noW - L_noPhi)
    ELc = euler_equations(L_cross, W + Wc + [ph, phc], X)
    okA3 = all(sp.simplify(sp.expand(eq.lhs)) == 0 for eq in ELc)
    check("A3", "A", okA3, "the W-phi cross terms of -|D phi - m W|^2 - (1/xi)|D.W - xi m phi|^2 are a total derivative (all Euler-Lagrange derivatives vanish, symbolic xi)")
    stamp("A3")

    # A4 intertwining, generic theta, g = 1, 2
    th = sp.Function("theta")(*X)
    Wth = [Dcov(th, m, 1, A) for m in N4]
    D0th = -box_scalar(th, 1, A) + msym ** 2 * th
    F = field_strength(A)
    Om = [[-sp.I * esym * F[m][n] for n in N4] for m in N4]
    okA4 = True
    for g_ in (1, 2):
        lhs = Delta_op(Wth, g_, A)
        for n in N4:
            defect = (2 - g_) * sum(Om[n][s] * gi[s] * Wth[s] for s in N4) - dOm[n] * th
            res = sp.expand(lhs[n] - Dcov(D0th, n, 1, A) - defect)
            if sp.simplify(res) != 0:
                okA4 = False
                print(f"     A4 residual g = {g_}, n = {n}: {sp.simplify(res)}")
    check("A4", "A", okA4, "Delta_g(D theta) = D(Delta_0 theta) + (2 - g) Omega.D theta - (nabla^n Omega_nm) theta identically (generic theta and f), g = 1, 2")
    # A4b at the graded g: on-shell (vacuum Maxwell, F_tau z = c0 const) defect vanishes iff g = 2; dS background defect nonzero
    c0 = sp.symbols("c0", real=True)
    Avac = [0, 0, 0, c0 * tau]
    dOm_vac = div_Omega(Avac)
    Fv = field_strength(Avac)
    Omv = [[-sp.I * esym * Fv[m][n] for n in N4] for m in N4]
    Wv = [Dcov(th, m, 1, Avac) for m in N4]
    onshell_zero = all(is_zero((2 - G_GRADED) * sum(Omv[n][s] * gi[s] * Wv[s] for s in N4) - dOm_vac[n] * th) for n in N4)
    dS_defect = sp.simplify(dOm[3].subs(fA(tau), -Esym / tau).doit())
    check("A4b", "A", onshell_zero and dS_defect != 0,
          f"graded g = {G_GRADED}: defect on the vacuum-Maxwell background {'vanishes' if onshell_zero else 'does NOT vanish'}; on the dS background nabla^n Omega_nz = {dS_defect} (nonzero: BRST decoupling broken by the non-vacuum background)")
    RES["A4b_dS_defect"] = str(dS_defect)
    stamp("A4")

    # A5 Goldstone/ghost mode equation -> AH4 (xi = 1: mass m, minimal)
    Ab = [0, 0, 0, -Esym / tau]
    u = sp.Function("u")(tau)
    uc = sp.Function("uc")(tau)
    ph_pw = u * sp.exp(sp.I * (kx * X[1] + kz * X[3]))
    phc_pw = uc * sp.exp(-sp.I * (kx * X[1] + kz * X[3]))
    Lph = sqrtg * (-sum(gi[m] * Dcov(phc_pw, m, -1, Ab) * Dcov(ph_pw, m, 1, Ab) for m in N4) - msym ** 2 * phc_pw * ph_pw)
    Lph = sp.expand(sp.powsimp(sp.expand(Lph)))
    ELu = euler_equations(Lph, [uc], [tau])[0].lhs
    chi = sp.Function("chi")(tau)
    ode = sp.expand(sp.simplify(ELu.subs(u, -tau * chi).doit()))
    c2 = ode.coeff(sp.Derivative(chi, (tau, 2)))
    odeN = sp.expand(sp.simplify(ode / c2))
    c1 = odeN.coeff(sp.Derivative(chi, tau))
    c0_ = sp.simplify(odeN.coeff(chi))
    target = kx ** 2 + (kz + esym * Esym / tau) ** 2 + (msym ** 2 - 2) / tau ** 2
    okA5 = sp.simplify(c1) == 0 and sp.simplify(c0_ - target) == 0
    idx = sp.expand(sp.Rational(1, 4) - sp.limit(c0_ * tau ** 2, tau, 0)).subs(esym, lam / Esym).subs(msym, mu)
    okA5 = okA5 and sp.simplify(idx - (sp.Rational(9, 4) - lam ** 2 - mu ** 2)) == 0
    check("A5", "A", okA5, f"Goldstone/ghost (xi = 1): chi = a phi obeys chi'' + [k_x^2 + (k_z + lambda/tau)^2 + (mu^2 - 2)/tau^2] chi = 0: Whittaker index mu_w^2 = {sp.expand(idx)} (AH4: 9/4 - lambda^2 - mu^2)")

    # A6 W_y decouples in Feynman gauge (k_y = 0), S1's equation
    w = [sp.Function(f"w{i}")(tau) for i in N4]
    wc = [sp.Function(f"wc{i}")(tau) for i in N4]
    E_pw = sp.exp(sp.I * (kx * X[1] + kz * X[3]))
    Wpw = [w[i] * E_pw for i in N4]
    Wcpw = [wc[i] * sp.exp(-sp.I * (kx * X[1] + kz * X[3])) for i in N4]
    okA6 = True
    block = {}
    for g_ in (1, 2):
        Lpw = sp.expand(sp.powsimp(sp.expand(lagr_W(Wpw, Wcpw, g_ - 1, 1, Ab))))
        ELw = euler_equations(Lpw, wc, [tau])
        ey = sp.expand(ELw[2].lhs)
        others = [w[i] for i in N4 if i != 2]
        dec = all(sp.simplify(ey.diff(o)) == 0 and sp.simplify(ey.diff(sp.Derivative(o, tau))) == 0 and sp.simplify(ey.diff(sp.Derivative(o, (tau, 2)))) == 0 for o in others)
        cyy = ey.coeff(sp.Derivative(w[2], (tau, 2)))
        eyN = sp.expand(sp.simplify(ey / cyy))
        okeq = sp.simplify(eyN.coeff(sp.Derivative(w[2], tau))) == 0 and sp.simplify(eyN.coeff(w[2]) - (kx ** 2 + (kz + esym * Esym / tau) ** 2 + msym ** 2 / tau ** 2)) == 0
        okA6 = okA6 and dec and okeq
        for i in (0, 1, 3):
            e_i = sp.expand(ELw[i].lhs)
            block[(g_, i)] = [j for j in N4 if sp.simplify(e_i.diff(w[j])) != 0 or sp.simplify(e_i.diff(sp.Derivative(w[j], tau))) != 0]
    check("A6", "A", okA6, "W_y (k_y = 0) decouples in Feynman gauge and obeys W_y'' + [k_x^2 + (k_z + lambda/tau)^2 + mu^2/tau^2] W_y = 0 (S1: index 1/4 - lambda^2 - mu^2), g = 1, 2")
    print(f"     coupled block (components entering the W_tau, W_x, W_z equations; 0 = tau, 1 = x, 3 = z): g = 2: { {k: v for k, v in block.items() if k[0] == 2} }")
    RES["A6_block_g2"] = {str(k): v for k, v in block.items() if k[0] == 2}

    # A7 AH3 premise: (e, A) -> (s e, A/s) leaves the operators invariant
    s_ = sp.symbols("s", positive=True)
    tt = sp.symbols("tt")
    Op = Delta_op(W, G_GRADED, A)
    okA7 = True
    for n in N4:
        sub = Op[n].subs(esym, s_ * esym).replace(fA, sp.Lambda(tt, fA(tt) / s_)).doit()
        okA7 = okA7 and is_zero(sub - Op[n])
    gb = -box_scalar(th, 1, A) + msym ** 2 * th
    gbs = gb.subs(esym, s_ * esym).replace(fA, sp.Lambda(tt, fA(tt) / s_)).doit()
    okA7 = okA7 and is_zero(gbs - gb)
    check("A7", "A", okA7, "AH3 premise: Delta_g and the Goldstone/ghost operator are invariant under (e, A) -> (s e, A/s): e and E enter only through e A, i.e. lambda")
    stamp("A")


# =============================================================================================== PART B
def gamma_euclid():
    I2 = sp.eye(2)
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])
    Z = sp.zeros(2)

    def blk(a, b, c, d):
        M = sp.zeros(4)
        M[:2, :2] = a
        M[:2, 2:] = b
        M[2:, :2] = c
        M[2:, 2:] = d
        return M
    return [blk(Z, -sp.I * s, sp.I * s, Z) for s in (sx, sy, sz)] + [blk(Z, I2, I2, Z)]


def a2_ratios(Dc, g_):
    """F^2 part of tr a_2 = (1/360)(30 tr Omega Omega + 180 tr E^2), flat Euclidean, constant integer F; ratios to one complex scalar."""
    Fm = sp.zeros(Dc)
    for i in range(Dc):
        for j in range(i + 1, Dc):
            v = (3 * i + 5 * j + 1) % 7 - 3
            Fm[i, j] = v
            Fm[j, i] = -v
    FF = sum(Fm[i, j] ** 2 for i in range(Dc) for j in range(Dc))
    a2_s = 30 * sum((-sp.I * Fm[i, j]) ** 2 for i in range(Dc) for j in range(Dc))
    Omat = -sp.I * Fm
    trOO = sum(((-sp.I * Fm[i, j]) * sp.eye(Dc) * (-sp.I * Fm[i, j]) * sp.eye(Dc)).trace() for i in range(Dc) for j in range(Dc))
    E = g_ * Omat
    a2_v = 30 * trOO + 180 * (E * E).trace()
    r_vec = sp.nsimplify(sp.simplify(a2_v / a2_s))
    return r_vec, FF


def a2_dirac_ratio():
    gam = gamma_euclid()
    ok_cl = all(sp.simplify(gam[m] * gam[n] + gam[n] * gam[m] - 2 * (1 if m == n else 0) * sp.eye(4)) == sp.zeros(4) for m in N4 for n in N4)
    Fm = sp.zeros(4)
    for i in range(4):
        for j in range(i + 1, 4):
            v = (3 * i + 5 * j + 1) % 7 - 3
            Fm[i, j] = v
            Fm[j, i] = -v
    Om = -sp.I * Fm
    EF = sp.zeros(4)
    for m in N4:
        for n in N4:
            EF += sp.Rational(1, 2) * gam[m] * gam[n] * Om[m, n]
    trOO = 4 * sum(Om[i, j] ** 2 for i in N4 for j in N4)
    a2_D = 30 * trOO + 180 * sp.expand((EF * EF).trace())
    a2_s = 30 * sum(Om[i, j] ** 2 for i in N4 for j in N4)
    return sp.nsimplify(sp.simplify(-sp.Rational(1, 2) * a2_D / a2_s)), ok_cl


def part_B():
    print("\n" + "=" * 118 + "\nPART B. UV structure: a_2, regulators, proper-time factors\n" + "=" * 118, flush=True)
    # B1
    rD, ok_cl = a2_dirac_ratio()
    rows = {}
    for Dc in sorted({4, D_COUNT}):
        for g_ in (1, 2):
            rv, _ = a2_ratios(Dc, g_)
            rows[(Dc, g_)] = dict(vec=rv, rxi=rv - 1, ym=rv - 2, b=sp.Rational(1, 3) * (rv - 1))
    for (Dc, g_), r in rows.items():
        print(f"     D = {Dc}, g = {g_}: Delta_1 / scalar = {r['vec']}, R_xi (vector + Goldstone - 2 ghosts) = {r['rxi']}, massless YM (vector - 2 ghosts) = {r['ym']};  b = {r['b']}")
    print(f"     Dirac / complex scalar = {rD} (gamma algebra {'ok' if ok_cl else 'BROKEN'})")
    gr = rows[(D_COUNT, G_GRADED)]
    okB1 = gr["b"] == -7 and sp.Rational(1, 3) * gr["ym"] == sp.Rational(-22, 3) and rD == 4 and ok_cl
    check("B1", "B", okB1, f"graded (g = {G_GRADED}, D = {D_COUNT}): b = {gr['b']} [gate -7], split {sp.Rational(1, 3) * gr['ym']} + 1/3 [gate -22/3 + 1/3]; Dirac {rD} [gate 4]")
    RES["B1"] = {f"D{Dc}_g{g_}": {k: str(v) for k, v in r.items()} for (Dc, g_), r in rows.items()}
    RES["B1_dirac"] = str(rD)
    RES["b_graded"] = str(gr["b"])
    RES["ratio_graded"] = str(gr["rxi"])
    RES["ratio_4D"] = {f"g{g_}": str(rows[(4, g_)]["rxi"]) for g_ in (1, 2)}

    # B1b K-tests on committed numbers
    txt4 = open(os.path.join(S1DIR, "s1_4_vector_uv_and_current.out")).read()
    txt2 = open(os.path.join(S1DIR, "s1_2_landau_and_beta.out")).read()
    txtA = open(AH4OUT).read()
    m2 = re.search(r"g = 2: total.*?c_inf = ([\d.]+)", txt4)
    m1 = re.search(r"g = 1: total.*?c_inf = ([\d.]+)", txt4)
    mr = re.search(r"ratio = (-?\d+); b = \(1/3\) x ratio = (-?\d+)", txt2)
    mrate = re.search(r"exactly 3 times the scalar", txt2)
    mA = re.search(r"coefficient of e\^2 E H ln\(m/H\) in the current:\s+([\d.e+-]+)", txtA)
    cinf2, cinf1 = float(m2.group(1)), float(m1.group(1))
    bs_AH4 = float(mA.group(1)) * 4 * math.pi ** 2
    r4 = {g_: rows[(4, g_)] for g_ in (1, 2)}
    ok_b1b = (abs(bs_AH4 - 1 / 3) < 1e-9 and int(mr.group(1)) == int(r4[2]["rxi"]) and int(mr.group(2)) == int(r4[2]["b"]) and mrate is not None
              and abs(cinf2 / float(-r4[2]["b"]) - 1) <= 0.05 and abs(cinf1 / float(-r4[1]["b"]) - 1) <= 0.05 and rD == 4)
    check("B1b", "B", ok_b1b, f"AH4 V3 b_s = {bs_AH4:.10f} [1/3]; Q1 Dirac = 4 b_s [{rD}]; S1 B3 ratio {mr.group(1)}, b {mr.group(2)} [{r4[2]['rxi']}, {r4[2]['b']}]; "
          f"S1 E4 exact-mode c_inf {cinf2} (g=2), {cinf1} (g=1) vs -b = {-r4[2]['b']}, {-r4[1]['b']} (5%: {cinf2 / 7 - 1:+.3f}, {cinf1 - 1:+.3f})")
    RES["S1_cinf"] = [cinf2, cinf1]

    # B2 tr E_F = 0 (no Lambda^2), a_2 F^2 part m-free, dS a_2 current ratio = flat ratio
    s_ = sp.symbols("s", positive=True)
    A = [0, 0, 0, s_ * fA(tau)]
    F = field_strength(A)
    OmU = [[-sp.I * F[m][n] for n in N4] for m in N4]
    Ev = sp.Matrix(4, 4, lambda al, be: -gi[al] * Ric[al][be] + G_GRADED * gi[al] * OmU[al][be])
    trE = sp.simplify(Ev.trace())
    okTr = sp.simplify(sp.diff(trE, s_)) == 0
    # a_2 F^2 part in dS (vector bundle) vs scalar
    a2v = a2_dS("vector", G_GRADED, 0, s_)
    a2s = a2_dS("scalar", 0, 0, s_)
    rat_dS = sp.simplify(a2v / a2s)
    okm = msym not in a2v.free_symbols
    # current of the a_2 term (per ln(Lambda^2/m^2)), scalar, via S2's pipeline:  Gamma_E = -(1/16 pi^2) L Int tr a_2
    Lag = a_ ** 4 * (+1 / (16 * sp.pi ** 2)) * a2s / 360
    J = S2.current_from_L(Lag, GEO)
    Glog_s = sp.simplify(4 * sp.pi * (-J.subs(tau, -1) / Esym))
    okB2 = okTr and okm and sp.simplify(rat_dS - (rows[(4, G_GRADED)]["vec"])) == 0 and sp.simplify(sp.diff(J, tau)) == 0
    check("B2", "B", okB2, f"tr E_V = {trE} (F-free: no Lambda^2 term); a_2 F^2 part has no m; dS a_2 ratio Delta_1/scalar = {rat_dS} = flat {rows[(4, G_GRADED)]['vec']}; "
          f"its dS current is tau-independent with a mu-independent coefficient (scalar: G per unit ln(Lambda^2/m^2) = {Glog_s})")
    RES["G_log_scalar_per_lnLambda2"] = str(Glog_s)
    print("     contrast S1 (unitary gauge): log coefficient c_inf + a/mu^2 (a = 5.12 at g = 2) and quadratic c1/lambda = -(8/3 + 4/(3 mu^2)); both mass-dependent pieces are absent in R_xi")

    # B3 regulators
    sv, M, m_, sig, muPS = sp.symbols("s M m sigma mu_PS", positive=True)
    pv2 = sp.simplify(sp.integrate((sp.exp(-sv * m_ ** 2) - sp.exp(-sv * M ** 2)) / sv, (sv, 0, sp.oo)))
    pv3 = sp.simplify(sp.integrate(sp.exp(-sv * m_ ** 2) - sp.exp(-sv * M ** 2), (sv, 0, sp.oo)))
    ok_pv = sp.simplify(pv2 - sp.log(M ** 2 / m_ ** 2)) == 0 and sp.simplify(pv3 - (1 / m_ ** 2 - 1 / M ** 2)) == 0
    # point-splitting: 2 K_0(m sqrt sigma) and (sqrt sigma / m) K_1(m sqrt sigma), small sigma (numerical check of the expansions, mpmath 40 digits)
    mp.mp.dps = 40
    okps = True
    for mv in (mp.mpf("0.7"), mp.mpf("3.1")):
        for sgv in (mp.mpf("1e-12"), mp.mpf("1e-16")):
            ps2 = 2 * mp.besselk(0, mv * mp.sqrt(sgv))
            ps2_ren = ps2 + mp.log(sgv / 4) + 2 * mp.euler           # Hadamard subtraction of the singular part at mu_PS = 1
            okps = okps and abs(ps2_ren - (-mp.log(mv ** 2))) < 1e-9
            ps3 = (mp.sqrt(sgv) / mv) * mp.besselk(1, mv * mp.sqrt(sgv))
            okps = okps and abs(ps3 * mv ** 2 - 1) < 1e-9
    diff2 = sp.simplify(sp.log(M ** 2 / m_ ** 2) - (-sp.log(m_ ** 2 / muPS ** 2)))
    okB3 = ok_pv and okps and sp.simplify(sp.diff(diff2, m_)) == 0
    check("B3", "B", okB3, f"PV: n=2 {pv2}, n=3 {pv3}; PS (Hadamard): n=2 -> -ln(m^2/mu_PS^2), n=3 -> 1/m^2 (mpmath, 1e-9); "
          f"PV - PS = {diff2} x (a_2 current): m-independent, so G_v^PV - G_v^PS is a mu-independent constant (a charge renormalisation)")

    # B4 proper-time factors
    x = sp.symbols("x")
    rows4 = {}
    for Dc in sorted({4, D_COUNT}):
        for g_ in (1, 2):
            fac = (x / sp.sinh(x)) * (Dc - 3 + 2 * sp.cosh(g_ * x))
            ser = sp.series(fac, x, 0, 4).removeO()
            c0_, c2_ = ser.coeff(x, 0), ser.coeff(x, 2)
            ratio = sp.simplify(c2_ / sp.Rational(-1, 6))
            el = (x / sp.sin(x)) * (Dc - 3 + 2 * sp.cos(g_ * x))
            w_ = sp.simplify(sp.limit((x - sp.pi) * el, x, sp.pi) / sp.limit((x - sp.pi) * x / sp.sin(x), x, sp.pi))
            rows4[(Dc, g_)] = (c0_, ratio, w_)
            print(f"     D = {Dc}, g = {g_}: (x/sinh x)(D - 3 + 2 cosh g x): polarizations {c0_}, x^2 ratio to scalar {ratio}; electric leading-pole weight {w_}")
    c0g, ratg, wg = rows4[(D_COUNT, G_GRADED)]
    okB4 = c0g == 3 and ratg == -21 and wg == 3 and mrate is not None
    check("B4", "B", okB4, f"graded (g = {G_GRADED}, D = {D_COUNT}): polarizations {c0g} [3], x^2 ratio {ratg} [-21], pair-rate weight {wg} [3 = S1 B4/B5]")
    RES["B4"] = {f"D{Dc}_g{g_}": [str(v) for v in r] for (Dc, g_), r in rows4.items()}
    RES["b_graded_ratio_B4"] = str(ratg)
    RES["weight_graded"] = str(wg)
    RES["weight_g1_4D"] = str(rows4[(4, 1)][2])
    stamp("B")


# =============================================================================================== a_2 / a_3 trace code
A3COEF = [8, 2, 12, -12, -6, -4, 5, 6, 60, 30, 60, 30, 10, 4, 12, 30, 12, 5, -2, 2]     # Vassilevich's 1/360 group, as recalled in S2


def bundle_data(kind, g_, xiR, A, coords, ginv, Gm, Riem, Ricc, Rsc):
    F = [[sp.diff(A[n], coords[m]) - sp.diff(A[m], coords[n]) for n in N4] for m in N4]
    OmU = [[-sp.I * F[m][n] for n in N4] for m in N4]
    if kind == "vector":
        Omb = [[sp.Matrix(4, 4, lambda al, be: ginv[al] * Riem[al][be][i][j] + (OmU[i][j] if al == be else 0)) for j in N4] for i in N4]
        E = sp.Matrix(4, 4, lambda al, be: -ginv[al] * Ricc[al][be] + g_ * ginv[al] * OmU[al][be])
        om = [sp.Matrix(4, 4, lambda al, be: Gm[al][l][be]) for l in N4]
        Nb = 4
    else:
        Omb = [[sp.Matrix([[OmU[i][j]]]) for j in N4] for i in N4]
        E = sp.Matrix([[-xiR * Rsc]])
        om = [sp.zeros(1) for _ in N4]
        Nb = 1
    return F, OmU, Omb, E, om, Nb


def a2_dS(kind, g_, xiR, s_):
    A = [0, 0, 0, s_ * fA(tau)]
    F, OmU, Omb, E, om, Nb = bundle_data(kind, g_, xiR, A, X, gi, Gam, RM, Ric, Rs)
    trOO = sum(gi[i] * gi[j] * (Omb[i][j] * Omb[i][j]).trace() for i in N4 for j in N4)
    tot = 30 * trOO + 180 * (E * E).trace() + 60 * Rs * E.trace()
    tot = sp.expand(sp.simplify(tot))
    return sp.simplify(tot.coeff(s_, 2))


def a3_lagrangian(kind, g_, xiR, A, coords, ginv, Gm, Riem, Ricc, Rsc, sq, s_):
    """Sum_t c_t tr(term_t) of the recalled a_3 (1/360 group), with explicit bundle matrices; returns (s^2 coefficient, s^1 coefficient)."""
    F, OmU, Omb, E, om, Nb = bundle_data(kind, g_, xiR, A, coords, ginv, Gm, Riem, Ricc, Rsc)

    def nab(T, idx, l):
        """nabla_l of a matrix-valued tensor with lower tensor indices idx (tuple), T given as a function of idx."""
        out = sp.diff(T(idx), coords[l])
        for p_ in range(len(idx)):
            for m_ in N4:
                if Gm[m_][l][idx[p_]] != 0:
                    j2 = idx[:p_] + (m_,) + idx[p_ + 1:]
                    out = out - Gm[m_][l][idx[p_]] * T(j2)
        return out + om[l] * T(idx) - T(idx) * om[l]

    Omk = {(i, j, k): nab(lambda t: Omb[t[0]][t[1]], (i, j), k) for i in N4 for j in N4 for k in N4}
    Omkk = {}
    for i in N4:
        for j in N4:
            acc = sp.zeros(Nb)
            for k in N4:
                acc += ginv[k] * nab(lambda t: Omk[(t[0], t[1], t[2])], (i, j, k), k)
            Omkk[(i, j)] = acc
    Omdiv = {i: sum((ginv[j] * Omk[(i, j, j)] for j in N4), sp.zeros(Nb)) for i in N4}
    Ek = {k: nab(lambda t: E, (), k) for k in N4}
    Ekk = sp.zeros(Nb)
    for k in N4:
        Ekk += ginv[k] * nab(lambda t: Ek[t[0]], (k,), k)
    trE = E.trace()

    def sbox(fn):
        return sum(sp.diff(sq * ginv[m] * sp.diff(fn, coords[m]), coords[m]) for m in N4) / sq

    hess = [[sp.diff(trE, coords[j], coords[k]) - sum(Gm[m_][j][k] * sp.diff(trE, coords[m_]) for m_ in N4) for k in N4] for j in N4]
    RV = lambda i, j, k, n: -Riem[i][j][k][n]
    T = [0] * 20
    T[0] = sum(ginv[i] * ginv[j] * ginv[k] * (Omk[(i, j, k)] * Omk[(i, j, k)]).trace() for i in N4 for j in N4 for k in N4)
    T[1] = sum(ginv[i] * (Omdiv[i] * Omdiv[i]).trace() for i in N4)
    T[2] = sum(ginv[i] * ginv[j] * (Omkk[(i, j)] * Omb[i][j]).trace() for i in N4 for j in N4)
    T[3] = sum(ginv[i] * ginv[j] * ginv[k] * (Omb[i][j] * Omb[j][k] * Omb[k][i]).trace() for i in N4 for j in N4 for k in N4)
    T[4] = sum(RV(i, j, k, n) * ginv[i] * ginv[j] * ginv[k] * ginv[n] * (Omb[i][j] * Omb[k][n]).trace() for i in N4 for j in N4 for k in N4 for n in N4 if Riem[i][j][k][n] != 0)
    T[5] = sum(Ricc[j][k] * ginv[j] * ginv[k] * ginv[n] * (Omb[j][n] * Omb[k][n]).trace() for j in N4 for k in N4 for n in N4 if Ricc[j][k] != 0)
    T[6] = Rsc * sum(ginv[k] * ginv[n] * (Omb[k][n] * Omb[k][n]).trace() for k in N4 for n in N4)
    T[7] = sbox(sbox(trE))
    T[8] = (E * Ekk).trace()
    T[9] = sum(ginv[k] * (Ek[k] * Ek[k]).trace() for k in N4)
    T[10] = (E * E * E).trace()
    T[11] = sum(ginv[i] * ginv[j] * (E * Omb[i][j] * Omb[i][j]).trace() for i in N4 for j in N4)
    T[12] = Rsc * sbox(trE)
    T[13] = sum(Ricc[j][k] * ginv[j] * ginv[k] * hess[j][k] for j in N4 for k in N4)
    T[14] = sum(ginv[k] * sp.diff(Rsc, coords[k]) * sp.diff(trE, coords[k]) for k in N4)
    T[15] = Rsc * (E * E).trace()
    T[16] = trE * sbox(Rsc)
    T[17] = trE * Rsc ** 2
    T[18] = trE * sum(ginv[i] * ginv[j] * Ricc[i][j] ** 2 for i in N4 for j in N4)
    T[19] = trE * sum(ginv[i] * ginv[j] * ginv[k] * ginv[n] * Riem[i][j][k][n] ** 2 for i in N4 for j in N4 for k in N4 for n in N4)
    tot = sum(c * t for c, t in zip(A3COEF, T))
    tot = sp.expand(tot)
    return sp.simplify(tot.coeff(s_, 2)), sp.simplify(tot.coeff(s_, 1)), None


def sigma_from_L3(L3, pref):
    """L_E = pref * L3/360 (per 1/m^2, q = 1), L_M = -L_E, sqrt(-g) L_M -> current (S2's pipeline) -> sigma_HFY M^2 and the tau-check."""
    Lag = a_ ** 4 * (-pref * L3 / 360)
    J = S2.current_from_L(Lag, GEO)
    cf = sp.simplify(-J.subs(tau, -1) / Esym)
    return cf, sp.simplify(sp.diff(J, tau)) == 0


# =============================================================================================== PART C
def part_C():
    print("\n" + "=" * 118 + "\nPART C. Heavy-mass current from the recalled a_3 (explicit bundle traces) in dS_4\n" + "=" * 118, flush=True)
    s_ = sp.symbols("s", positive=True)
    A = [0, 0, 0, s_ * fA(tau)]
    PB = -sp.Rational(1, 16) / sp.pi ** 2                  # bosonic complex field: Gamma_E = -(1/16 pi^2 m^2) Int tr a_3
    # C0 scalar with MY trace code
    okS = True
    sc = {}
    for xiR in (sp.Integer(0), sp.Rational(1, 6), sp.Rational(1, 12)):
        L3, L1, _ = a3_lagrangian("scalar", 0, xiR, A, X, gi, Gam, RM, Ric, Rs, sqrtg, s_)
        cf, tok = sigma_from_L3(L3, PB)
        target = (sp.Rational(7, 18) - 2 * xiR) / (4 * sp.pi ** 2)
        ok_ = sp.simplify(cf - target) == 0 and sp.simplify(L1) == 0 and tok
        okS &= ok_
        sc[xiR] = cf
        print(f"     scalar xi_R = {xiR}: sigma_HFY M^2 = {cf}  (target {target}; linear part {'0' if sp.simplify(L1) == 0 else L1}; tau-independent {tok})")
    stamp("C0 scalar")
    # Dirac via S2's committed reduction
    Sst = S2.structures(GEO, S2.field_tensors(GEO))
    Ls = sum(c * Sst[k] for c, k in zip(S2.dirac_coefs(), ("S1", "S2", "S3", "S4", "S5", "S6")))
    LagD = a_ ** 4 * (-(sp.Rational(1, 32) / sp.pi ** 2) * Ls / 360)
    JD = S2.current_from_L(LagD, GEO)
    cD = sp.simplify(-JD.subs(tau, -1) / Esym)
    okD = sp.simplify(cD + 1 / (36 * sp.pi ** 2)) == 0
    # AH4 closed form (Kobayashi-Afshordi 2.58 via Q1's copy): Richardson of mu^2 G_s
    lam_s = 1e-6
    vals = []
    for mv in (10, 20, 40):
        f = scalar_closed_f(lam_s, mv)
        vals.append((f / lam_s) / math.pi * mv ** 2)
    c0A = richardson([10, 20, 40], vals)
    relA = abs(c0A / (7 / (18 * math.pi)) - 1)
    # Q1 closed form
    valsQ = [4 * math.pi * hfy_weak(Mv) * Mv ** 2 for Mv in (20, 40, 80)]
    c0Q = richardson([20, 40, 80], valsQ)
    relQ = abs(c0Q / (-1 / (9 * math.pi)) - 1)
    print(f"     Dirac (S2 reduction): sigma_HFY M^2 = {cD} [-1/(36 pi^2)]")
    print(f"     AH4 closed form: mu^2 G_s at mu = 10, 20, 40: {[f'{v:.10f}' for v in vals]};  Richardson {c0A:.12f} vs 7/(18 pi) = {7 / (18 * math.pi):.12f} (rel {relA:.2e})")
    print(f"     Q1 closed form:  mu^2 G_f at mu = 20, 40, 80: {[f'{v:.10f}' for v in valsQ]};  Richardson {c0Q:.12f} vs -1/(9 pi) = {-1 / (9 * math.pi):.12f} (rel {relQ:.2e})")
    check("C0", "C", okS and okD and relA <= 1e-5 and relQ <= 1e-6,
          "positive controls: my trace code gives the scalar law (7/18 - 2 xi_R)/(4 pi^2) exactly; S2's Dirac reduction -1/(36 pi^2); AH4's and Q1's closed forms tend to 7/(18 pi) and -1/(9 pi)")
    RES["C0"] = dict(AH4_richardson=c0A, AH4_rel=relA, Q1_richardson=c0Q, Q1_rel=relQ)
    stamp("C0")

    # C1 vector bundle, g = 0, 1, 2; and single-structure currents u_i via S2's pipeline
    vec = {}
    okC1 = True
    for g_ in (0, 1, 2):
        L3, L1, Tl = a3_lagrangian("vector", g_, 0, A, X, gi, Gam, RM, Ric, Rs, sqrtg, s_)
        cf, tok = sigma_from_L3(L3, PB)
        hand = sp.Rational(3 * g_ ** 2 - 3 * g_ - 2, 18) / sp.pi ** 2
        ok_ = sp.simplify(cf - hand) == 0 and sp.simplify(L1) == 0 and tok
        okC1 &= ok_
        vec[g_] = cf
        print(f"     Delta_1(g = {g_}): sigma_HFY M^2 = {cf}  (hand (3g^2 - 3g - 2)/(18 pi^2) = {hand}; linear part {'0' if sp.simplify(L1) == 0 else L1}; tau-independent {tok})")
        stamp(f"C1 g={g_}")
    u_hand = [sp.Rational(1, 360), sp.Rational(-1, 720), sp.Rational(-1, 360), sp.Rational(1, 360), sp.Rational(-1, 240), sp.Rational(-1, 60)]
    u = []
    for k, uh in zip(("S1", "S2", "S3", "S4", "S5", "S6"), u_hand):
        Lag = a_ ** 4 * (-PB * Sst[k] / 360)
        Jk = S2.current_from_L(Lag, GEO)
        uk = sp.simplify(-Jk.subs(tau, -1) / Esym)
        u.append(uk)
        okC1 &= sp.simplify(uk - uh / sp.pi ** 2) == 0
    print(f"     single-structure currents u_i (sigma_HFY M^2 per unit coefficient, bosonic prefactor): {u}")
    check("C1", "C", okC1, "vector-bundle trace code = hand reduction (3g^2 - 3g - 2)/(18 pi^2) for g = 0, 1, 2; linear-in-F parts vanish; u_i = hand values")
    RES["u"] = [str(v) for v in u]
    RES["sigma_Delta1"] = {str(g_): str(v) for g_, v in vec.items()}

    # C2 R_xi total at xi = 1
    tot = {g_: sp.simplify(vec[g_] - sc[sp.Integer(0)]) for g_ in (0, 1, 2)}
    Gmu2 = {g_: sp.simplify(4 * sp.pi * tot[g_]) for g_ in tot}
    for g_ in (1, 2):
        print(f"     R_xi total (xi = 1), g = {g_}: sigma_HFY M^2 = {tot[g_]} = {float(tot[g_]):.10e};  G_v mu^2 -> {Gmu2[g_]} = {float(Gmu2[g_]):.6f}")
    print(f"     comparators: scalar G_s mu^2 -> 7/(18 pi) = {7 / (18 * math.pi):.6f};  Dirac G_f mu^2 -> -1/(9 pi) = {-1 / (9 * math.pi):.6f}")
    check("C2", "C", tot[G_GRADED] != 0, f"graded g = {G_GRADED}: R_xi heavy coefficient sigma_HFY M^2 = {tot[G_GRADED]} (expected 1/(8 pi^2) at g = 2), G_v mu^2 -> {Gmu2[G_GRADED]}; current tau-independent (dS invariant)")
    RES["sigma_Rxi"] = {str(g_): str(tot[g_]) for g_ in (1, 2)}
    RES["Gmu2_Rxi"] = {str(g_): str(Gmu2[g_]) for g_ in (1, 2)}
    RES["Gmu2_graded"] = float(Gmu2[G_GRADED])
    RES["sigma_Rxi_graded"] = str(tot[G_GRADED])

    # C3 flat Euclidean plane wave: q^4 ratio R_xi / scalar
    ys = sp.symbols("y1:5", real=True)
    Q = sp.symbols("Q", positive=True)
    Af = [s_ * sp.cos(Q * ys[3]), 0, 0, 0]
    gflat = [1, 1, 1, 1]
    Gm0 = [[[0] * 4 for _ in N4] for _ in N4]
    R0 = [[[[0] * 4 for _ in N4] for _ in N4] for _ in N4]
    Ric0 = [[0] * 4 for _ in N4]
    flat = {}
    for kind, g_ in (("scalar", 0), ("vector", 1), ("vector", 2)):
        L3, _, _ = a3_lagrangian(kind, g_, 0, Af, ys, gflat, Gm0, R0, Ric0, 0, 1, s_)
        avg = sp.simplify(sp.integrate(L3, (ys[3], 0, 2 * sp.pi / Q)) * Q / (2 * sp.pi))
        flat[(kind, g_)] = avg
    rflat = {g_: sp.simplify((flat[("vector", g_)] - flat[("scalar", 0)]) / flat[("scalar", 0)]) for g_ in (1, 2)}
    print(f"     flat plane-wave a_3 (period average): scalar {flat[('scalar', 0)]}; R_xi/scalar q^4 ratio: g = 1: {rflat[1]}, g = 2: {rflat[2]} (hand 3 - 10 g^2: -7, -37)")
    RES["C3_flat_ratio"] = {str(g_): str(rflat[g_]) for g_ in (1, 2)}
    stamp("C")
    return dict(u2=u[1], rflat=rflat, tot=tot, Gmu2=Gmu2)


def richardson(ms, vals):
    import numpy as np
    Am = np.array([[1.0, 1.0 / m ** 2, 1.0 / m ** 4] for m in ms])
    return float(np.linalg.solve(Am, np.array(vals))[0])


# =============================================================================================== PART D (route D and the K-formula)
RG, k1, k2, k3, k4, Qv, xiv, ixv, gv, Am_, Ax_ = ring("k1,k2,k3,k4,Q,xi,ix,g,Am,Ax", QQ)
QPOS = 4
HALFM = RG(QQ(-1, 2))
R2, K2r, Q2r, xi2, ix2, g2, Am2, Ax2 = ring("K2,Q,xi,ix,g,Am,Ax", QQ)


def trunc(p, n=4):
    return RG.from_dict({mon: c for mon, c in p.terms() if mon[QPOS] <= n}) if p != 0 else RG(0)


def mm(A_, B_):
    return [[trunc(sum((A_[i][k] * B_[k][j] for k in N4), RG(0))) for j in N4] for i in N4]


def tr(A_):
    return sum((A_[i][i] for i in N4), RG(0))


def dot(u, v):
    return sum((u[i] * v[i] for i in N4), RG(0))


def series_inv(Asym, t):
    out = RG(0)
    tp = RG(1)
    for n in range(5):
        out += tp * Asym ** (n + 1)
        tp = trunc(tp * (-t))
    return trunc(out)


KV = [k1, k2, k3, k4]
QV = [RG(0), RG(0), RG(0), Qv]


def vadd(u, v, s=1):
    return [u[i] + s * v[i] for i in N4]


def Gvec(p, Sm, Sx, xi_factor=True):
    """P_T/(p^2+1) + xi P_L/(p^2+xi) = delta Sm - (1-xi) p p^T Sm Sx  (m = 1)."""
    if not xi_factor:
        return [[Sm if i == j else RG(0) for j in N4] for i in N4]
    SmSx = trunc(Sm * Sx)
    return [[trunc((Sm if i == j else RG(0)) - (1 - xiv) * p[i] * p[j] * SmSx) for j in N4] for i in N4]


def Vvec(pin, pout, b, Dl, with_L=True):
    """absorbing a background mode of polarisation b and momentum Dl = pout - pin:  -(b.(pin+pout)) 1 + (1 - 1/xi)[pout b^T + b pin^T] - g (Dl b^T - b Dl^T)."""
    s_ = dot(b, vadd(pin, pout))
    M = [[(-s_ if i == j else RG(0)) - gv * (Dl[i] * b[j] - b[i] * Dl[j]) for j in N4] for i in N4]
    if with_L:
        M = [[M[i][j] + (1 - ixv) * (pout[i] * b[j] + b[i] * pin[j]) for j in N4] for i in N4]
    return M


def df(n):
    return 1 if n <= 0 else n * df(n - 2)


def ang_avg(p):
    """4D angular average of the k-monomials -> polynomial in K2 (ring R2)."""
    out = {}
    for mon, c in p.terms():
        e = mon[:4]
        if any(x % 2 for x in e):
            continue
        n = sum(e) // 2
        fac = QQ(df(e[0] - 1) * df(e[1] - 1) * df(e[2] - 1) * df(e[3] - 1))
        den = 1
        for j in range(n):
            den *= 4 + 2 * j
        key = (n,) + mon[4:]
        out[key] = out.get(key, QQ(0)) + c * fac / den
    return R2.from_dict(out) if out else R2(0)


K2s = sp.Symbol("K2", positive=True)
XIs = sp.Symbol("xi", positive=True)
Gs = sp.Symbol("g")


def to_groups(p2, qpow, xi_val=None, g_val=None):
    """coefficient of Q^qpow including the radial measure K2 (common 1/(16 pi^2) dropped), grouped by the denominator powers
    (a, b) of (K2 + 1)^a (K2 + xi)^b:  {(a, b): numerator polynomial in K2}."""
    groups = {}
    for mon, c in p2.terms():
        if mon[1] != qpow:
            continue
        nK, _, exi, eix, eg, eAm, eAx = mon
        coef = sp.Rational(int(c.numerator), int(c.denominator)) * XIs ** (exi - eix) * Gs ** eg
        if xi_val is not None:
            coef = coef.subs(XIs, xi_val)
        if g_val is not None:
            coef = coef.subs(Gs, g_val)
        key = (eAm, eAx)
        groups[key] = groups.get(key, 0) + coef * K2s ** (nK + 1)
    return groups


def to_radial(p2, qpow, xi_val=None, g_val=None):
    groups = to_groups(p2, qpow, xi_val, g_val)
    xv = XIs if xi_val is None else xi_val
    return sum((P / ((K2s + 1) ** a * (K2s + xv) ** b) for (a, b), P in groups.items()), sp.Integer(0))


def _laurent(P, a, b, xv):
    """partial fractions of P/((K2+1)^a (K2+xv)^b): (polynomial part, {j: A_j}, {j: B_j}); xv != 1."""
    P = sp.Poly(sp.expand(P), K2s)
    Dn = sp.Poly(sp.expand((K2s + 1) ** a * (K2s + xv) ** b), K2s)
    q_, r_ = sp.div(P, Dn)
    R = r_.as_expr()
    A, B = {}, {}
    for j in range(1, a + 1):
        h = R / (K2s + xv) ** b
        A[j] = sp.diff(h, K2s, a - j).subs(K2s, -1) / sp.factorial(a - j)
    for j in range(1, b + 1):
        h = R / (K2s + 1) ** a
        B[j] = sp.diff(h, K2s, b - j).subs(K2s, -xv) / sp.factorial(b - j)
    return q_.as_expr(), A, B


def integrate_groups(groups, xv):
    """Int_0^oo dK2 of Sum P/((K2+1)^a (K2+xv)^b); requires convergence (checked: no polynomial part, A_1 + B_1 = 0)."""
    poly = sp.Integer(0)
    A, B = {}, {}
    if xv == 1:
        for (a, b), P in groups.items():
            n = a + b
            Pp = sp.Poly(sp.expand(P.subs(K2s, K2s - 1)), K2s)          # P in powers of u = K2 + 1
            for (deg,), c in Pp.terms():
                pw = n - deg
                if pw <= 0:
                    poly += c * K2s ** (-pw)
                else:
                    A[pw] = A.get(pw, 0) + c
        poly = sp.expand(poly)
        if poly != 0 or sp.simplify(A.get(1, 0)) != 0:
            raise ValueError("divergent radial integral")
        return sp.nsimplify(sum(A[j] / (j - 1) for j in A if j >= 2))
    for (a, b), P in groups.items():
        if b == 0 or a == 0:
            M_, n = (1, a) if b == 0 else (xv, b)
            Pp = sp.Poly(sp.expand(P.subs(K2s, K2s - M_)), K2s)
            for (deg,), c in Pp.terms():
                pw = n - deg
                if pw <= 0:
                    poly += c * K2s ** (-pw)
                elif b == 0:
                    A[pw] = A.get(pw, 0) + c
                else:
                    B[pw] = B.get(pw, 0) + c
            continue
        q_, Aj, Bj = _laurent(P, a, b, xv)
        poly += q_
        for j, v in Aj.items():
            A[j] = A.get(j, 0) + v
        for j, v in Bj.items():
            B[j] = B.get(j, 0) + v
    poly = sp.simplify(sp.expand(poly))
    a1 = sp.simplify(A.get(1, 0))
    b1 = sp.simplify(B.get(1, 0))
    if poly != 0 or sp.simplify(a1 + b1) != 0:
        raise ValueError("divergent radial integral")
    val = a1 * sp.log(xv) + sum(A[j] / (j - 1) for j in A if j >= 2) + sum(B[j] / ((j - 1) * xv ** (j - 1)) for j in B if j >= 2)
    return sp.factor(sp.cancel(sp.together(val - a1 * sp.log(xv)))) + sp.factor(sp.cancel(a1)) * sp.log(xv)


def radial_integral_groups(p2, qpow, xi_val=None, g_val=None):
    xv = XIs if xi_val is None else xi_val
    return integrate_groups(to_groups(p2, qpow, xi_val, g_val), xv)


def radial_integral(expr):
    """fallback for an explicit expression (numeric xi only)."""
    e = sp.together(sp.expand(expr))
    if e == 0:
        return sp.Integer(0)
    pf = sp.apart(e, K2s)
    anti = sp.integrate(pf, K2s)
    val = sp.limit(anti, K2s, sp.oo) - anti.subs(K2s, 0)
    return sp.simplify(val)


def log_coef(expr):
    return sp.simplify(sp.limit(sp.together(expr) * K2s, K2s, sp.oo))


def routeD_integrand(pol, kind="Rxi", graded_g=True):
    """-(1/2) Sum_+- tr[G(k) V(k <- k+-q) G(k+-q) V(k+-q <- k)] for the vector (general xi) minus one scalar of mass xi; or a single scalar of mass 1."""
    t_p = trunc(2 * k4 * Qv + Qv ** 2)
    t_m = trunc(-2 * k4 * Qv + Qv ** 2)
    tot = RG(0)
    for sgn, t in ((1, t_p), (-1, t_m)):
        kq = vadd(KV, QV, sgn)
        Dl_in = [sgn * x for x in QV]                  # k -> k+-q absorbs +-q
        Dl_out = [-sgn * x for x in QV]
        if kind in ("Rxi", "vector"):
            Gk = Gvec(KV, Am_, Ax_)
            Gkq = Gvec(kq, series_inv(Am_, t), series_inv(Ax_, t))
            V_in = Vvec(KV, kq, pol, Dl_in)             # k -> k+-q
            V_out = Vvec(kq, KV, pol, Dl_out)           # k+-q -> k
            tot += HALFM * tr(mm(mm(mm(Gk, V_out), Gkq), V_in))
        if kind in ("Rxi", "scalar_xi"):
            vs_in = -dot(pol, vadd(KV, kq))
            vs_out = -dot(pol, vadd(kq, KV))
            tot -= HALFM * trunc(Ax_ * vs_out * series_inv(Ax_, t) * vs_in)
        if kind == "scalar1":
            vs_in = -dot(pol, vadd(KV, kq))
            vs_out = -dot(pol, vadd(kq, KV))
            tot += HALFM * trunc(Am_ * vs_out * series_inv(Am_, t) * vs_in)
    return trunc(tot)


def kformula_integrand(pol):
    """T1 + T2 of H4 at O(a abar): -(1 - xi) Tr X - (1/2)(1 - xi)^2 Tr X^2  (Feynman vector propagators, scalar of mass xi, g = graded symbol gv)."""
    t_p = trunc(2 * k4 * Qv + Qv ** 2)
    t_m = trunc(-2 * k4 * Qv + Qv ** 2)
    q2 = Qv ** 2
    qa = dot(QV, pol)
    Kt = [trunc(q2 * pol[i] - QV[i] * qa) for i in N4]       # K = -i Kt for both +-q (a real)
    trX = RG(0)
    for sgn, t in ((1, t_p), (-1, t_m)):
        kq = vadd(KV, QV, sgn)
        Smt, Sxt = series_inv(Am_, t), series_inv(Ax_, t)
        # (i)
        trX += trunc(Ax_ * Smt * dot(pol, Kt))
        # (ii)  V1(k <- k+-q): absorbs -+q
        Dl = [-sgn * x for x in QV]
        V1 = Vvec(kq, KV, pol, Dl, with_L=False)
        V1K = [trunc(sum((V1[i][j] * Kt[j] for j in N4), RG(0))) for i in N4]
        trX += trunc(Ax_ * Am_ * Smt * dot(KV, V1K))
        # (iii)
        trX += trunc(-Ax_ * dot(pol, vadd(KV, kq)) * trunc(Sxt * Smt) * dot(kq, Kt))
    T1 = trunc(-(1 - xiv) * trX)
    X2 = RG(0)
    for sgn, t in ((1, t_p), (-1, t_m)):
        X2 += trunc(dot(KV, Kt) * dot(KV, Kt) * Ax_ * Am_ * trunc(series_inv(Ax_, t) * series_inv(Am_, t)))
    T2 = trunc(HALFM * (1 - xiv) ** 2 * X2)
    return trunc(T1 + T2)


def part_D(cres):
    print("\n" + "=" * 118 + "\nPART D. Gauge-parameter dependence: flat Euclidean momentum space, general xi (route D) and the exact formula H4\n" + "=" * 118, flush=True)
    aT = [RG(1), RG(0), RG(0), RG(0)]
    aL = [RG(0), RG(0), RG(0), RG(1)]
    # scalar reference (mass 1)
    s1 = ang_avg(routeD_integrand(aT, "scalar1"))
    cL_s = log_coef(to_radial(s1, 2))
    c4_s = radial_integral_groups(s1, 4, 1)
    okG2 = sp.simplify(c4_s / cL_s + sp.Rational(1, 10)) == 0
    check("D-G2", "D", okG2, f"scalar positive control: log coefficient {cL_s}, q^4 coefficient {c4_s}, ratio {sp.simplify(c4_s / cL_s)} [-1/10] (common 1/(16 pi^2) dropped)")
    stamp("D scalar")
    rxT = ang_avg(routeD_integrand(aT, "Rxi"))
    stamp("D route-D transverse integrand")
    rxL = ang_avg(routeD_integrand(aL, "Rxi"))
    stamp("D route-D longitudinal integrand")
    # D-G1 Ward identity
    okG1 = True
    for xv in (sp.Rational(1, 2), 1, 2):
        for g_ in (1, 2):
            l2 = log_coef(to_radial(rxL, 2, xv, g_))
            i4 = radial_integral_groups(rxL, 4, xv, g_)
            okG1 &= (l2 == 0 and i4 == 0)
            print(f"     longitudinal a: xi = {xv}, g = {g_}: q^2 log coefficient {l2}, q^4 integral {i4}")
    check("D-G1", "D", okG1, "Ward identity: the longitudinal (pure-gauge) background gives no q^2 log and no q^4 term")
    # D-G4 log ratio xi-independent, = 4D a_2 ratio
    okG4 = True
    okG4A1 = True
    r4D = {1: sp.Integer(-3), 2: sp.Integer(-21)}
    logrows = {}
    for g_ in (1, 2):
        r4D[g_] = a2_ratios(4, g_)[0] - 1
        for xv in (sp.Rational(1, 2), 1, 2, 3):
            lr = sp.simplify(log_coef(to_radial(rxT, 2, xv, g_)) / cL_s)
            ok_ = sp.simplify(lr - r4D[g_]) == 0
            okG4 &= ok_
            if g_ == G_GRADED:
                okG4A1 &= ok_
            logrows[f"g{g_}_xi{xv}"] = str(lr)
            print(f"     transverse: g = {g_}, xi = {xv}: log ratio to scalar {lr} (a_2: {r4D[g_]})")
    check("D-G4", "D", okG4, "AS FROZEN (both g): charge-renormalisation (log) coefficient is xi-independent and equals the a_2 ratio 3 - 6 g^2")
    check("D-G4(A1)", "D", okG4A1, f"AMENDMENT A1 (post hoc; graded g = {G_GRADED} only, where H4 applies): log coefficient xi-independent and = a_2 ratio {r4D[G_GRADED]}")
    print("     (g = 1 is not a gauge theory: its R_xi family is not a family of gauges, cf. A4's (2 - g) defect; its log ratio 3 xi - 6 is a finding)")
    RES["D_G4_logrows"] = logrows
    stamp("D-G1/G4")
    # q^4 coefficients
    c4 = {}
    for g_ in (1, 2):
        c4[(1, g_)] = radial_integral_groups(rxT, 4, 1, g_)
    okG3 = True
    for g_ in (1, 2):
        rr = sp.simplify(c4[(1, g_)] / c4_s)
        okG3 &= sp.simplify(rr - cres["rflat"][g_]) == 0
        print(f"     xi = 1, g = {g_}: q^4 ratio R_xi/scalar = {rr} (a_3 flat, C3: {cres['rflat'][g_]})")
    check("D-G3", "D", okG3, "Feynman gauge: route-D q^4 ratio = the a_3 flat ratio (validates the vector-bundle flat terms)")
    stamp("D-G3")
    # symbolic xi
    c4sym = {}
    for g_ in (1, 2):
        c4sym[g_] = radial_integral_groups(rxT, 4, None, g_)
        print(f"     route D, g = {g_}: c4(xi) = {c4sym[g_]}")
    stamp("D symbolic xi")
    cont = all(sp.simplify(sp.limit(c4sym[g_], XIs, 1) - c4[(1, g_)]) == 0 for g_ in (1, 2))
    r_xi = {g_: sp.simplify((c4sym[g_] - c4[(1, g_)]) / c4_s) for g_ in (1, 2)}
    # D-G5 K-formula (g = graded)
    kf = ang_avg(kformula_integrand(aT))
    kf_l2 = log_coef(to_radial(kf, 2, None, G_GRADED))
    kf_c4 = radial_integral_groups(kf, 4, None, G_GRADED)
    kf_c2fin = None
    try:
        kf_c2fin = radial_integral_groups(kf, 2, None, G_GRADED)
    except Exception as exc:                            # divergent remainder: reported only
        kf_c2fin = f"not convergent ({type(exc).__name__})"
    diffD = sp.simplify(c4sym[G_GRADED] - c4[(1, G_GRADED)])
    okG5 = kf_l2 == 0 and sp.simplify(kf_c4 - diffD) == 0
    check("D-G5", "D", okG5, f"graded g = {G_GRADED}: K-formula q^4 = {sp.simplify(kf_c4)}; route D c4(xi) - c4(1) = {diffD}; K-formula q^2 log {kf_l2} (finite q^2 part {kf_c2fin})")
    stamp("D-G5")
    # report r(xi)
    for g_ in (1, 2):
        rv = r_xi[g_]
        vals = {str(xv): float(rv.subs(XIs, xv)) for xv in (sp.Rational(1, 10), sp.Rational(1, 2), 2, 3, 10, 100)}
        lin = sp.limit(rv / XIs, XIs, sp.oo)
        big = sp.limit((rv - lin * XIs) / sp.log(XIs), XIs, sp.oo)
        small = sp.limit(rv * XIs, XIs, 0)
        small_log = sp.limit(rv / sp.log(XIs), XIs, 0)
        print(f"     r(xi) (g = {g_}) = {rv}")
        print(f"        values: {vals};  xi -> oo: r/xi -> {lin}, (r - {lin} xi)/ln xi -> {big};  xi -> 0: xi r -> {small}, r/ln xi -> {small_log}")
        RES[f"r_xi_g{g_}"] = dict(expr=str(rv), values=vals, xi_coef_large=str(lin), lnxi_coef_large=str(big), xi_r_small=str(small), lnxi_coef_small=str(small_log))
    dG = sp.simplify(4 * sp.pi * 6 * r_xi[G_GRADED] * cres["u2"])
    Gfey = cres["Gmu2"][G_GRADED]
    tab = {str(xv): float(Gfey + sp.limit(dG, XIs, xv)) for xv in (sp.Rational(1, 10), sp.Rational(1, 2), 1, 2, 3, 10)}
    print(f"     dS shift of the heavy coefficient (graded g): delta(G_v mu^2) = 4 pi x 6 r(xi) u2 = {dG}  (hand: -r/(30 pi))")
    print(f"     G_v mu^2 (heavy limit) in R_xi gauge, graded g: {tab}")
    RES["Gmu2_vs_xi_graded"] = tab
    print(f"     continuity of the symbolic c4(xi) at xi = 1: {cont}")
    RES["dG_shift_graded"] = str(dG)
    # finite q^2 difference (4D cutoff, NOT graded)
    try:
        gA = to_groups(rxT, 2, None, G_GRADED)
        gB = to_groups(rxT, 2, 1, G_GRADED)
        for (aa, bb), P in gB.items():
            gA[(aa + bb, 0)] = gA.get((aa + bb, 0), 0) - P
        dq2 = integrate_groups(gA, XIs)
        print(f"     (not graded) finite q^2 part, c0(xi) - c0(1) in this 4D routing: {dq2}")
        RES["c0_diff_not_graded"] = str(dq2)
    except Exception as exc:
        print(f"     (not graded) finite q^2 difference not evaluated: {type(exc).__name__}")
    gate_ok = all(CHECKS.get(t, False) for t in ("D-G1", "D-G2", "D-G3", "D-G4", "D-G5"))
    gate_okA1 = all(CHECKS.get(t, False) for t in ("D-G1", "D-G2", "D-G3", "D-G4(A1)", "D-G5"))
    nonzero = sp.simplify(r_xi[G_GRADED]) != 0
    found = "GAUGE DEPENDENT at O(1/mu^2)" if nonzero else "GAUGE INDEPENDENT at O(1/mu^2)"
    verdict = found if gate_ok else "NOT ESTABLISHED"
    verdictA1 = found if gate_okA1 else "NOT ESTABLISHED"
    print(f"  PART-D VERDICT as frozen: {verdict};  as frozen + A1: {verdictA1}")
    RES["partD_verdict_A1"] = verdictA1
    print("     (informational, heuristic) the unitary limit xi -> oo diverges like xi and ln xi: the R_xi images of S1's quadratic (4/(3 mu^2)) and logarithmic (a/mu^2) unitary-gauge terms")
    RES["partD_verdict"] = verdict
    RES["c4_scalar"] = str(c4_s)
    RES["c4_xi1"] = {str(g_): str(c4[(1, g_)]) for g_ in (1, 2)}
    RES["c4_sym"] = {str(g_): str(c4sym[g_]) for g_ in (1, 2)}
    RES["flat_q4_ratio_graded"] = str(sp.simplify(c4[(1, G_GRADED)] / c4_s))
    stamp("D")


# =============================================================================================== PART E
def classifier(G, mus):
    v = [G(m) for m in mus]
    same_sign = all(x > 0 for x in v) or all(x < 0 for x in v)
    spread = max(abs(x) for x in v) / min(abs(x) for x in v)
    return ("SELECTED" if (same_sign and spread <= 1 + 1e-6) else "NOT SELECTED"), spread


def part_E(cres):
    print("\n" + "=" * 118 + "\nPART E. Selection\n" + "=" * 118, flush=True)
    mus = [3, 5, 10, 20]
    C = float(cres["Gmu2"][G_GRADED])
    verdict, spread = classifier(lambda m: C / m ** 2, mus)
    pc1, _ = classifier(lambda m: 0.3, mus)
    pc2, _ = classifier(lambda m: 1 / (2 * math.pi * m ** 2), mus)
    okE1 = verdict == "NOT SELECTED" and pc1 == "SELECTED" and pc2 == "NOT SELECTED" and C != 0
    check("E1", "E", okE1, f"G_v(mu) = {C:.6f}/mu^2 over mu in {mus}: spread {spread:.1f} -> {verdict}; planted constant -> {pc1}, planted 1/(2 pi mu^2) -> {pc2}. "
          "A tie sigma/H = c gives alpha = c mu^2/C: a function of the mass, not a number")
    okE2 = all(CHECKS.get(t, False) for t in ("A7", "B1", "B3")) and RES.get("b_graded") is not None
    check("E2", "E", okE2, "no condition constrains e: renormalisability (B1-B3), on-shell gauge independence (A4/H4) and g = 2 hold for symbolic e; e enters only via e A (A7); all coefficients are e-free after the overall e^2")
    RES["E1"] = dict(verdict=verdict, spread=spread)


# =============================================================================================== main
def main():
    print("=" * 118)
    print(f"CFG899 alpha door D08 -- charged vector boson in dS_4, covariant R_xi completion -- mode {MODE} (graded g = {G_GRADED}, count dimension D = {D_COUNT})")
    print("STRUCTURAL CLOSURE: alpha stays a free symbol; no comparison with 137.036; N_mech unchanged (374).")
    print("=" * 118, flush=True)
    part_A()
    part_B()
    cres = part_C()
    part_D(cres)
    part_E(cres)

    closure_tags = [t for t in CHECKS if GROUP[t] in ("A", "B", "C", "E")]
    closed = all(CHECKS[t] for t in closure_tags)
    verdict = "CLOSED, NO SELECTION" if closed and RES.get("E1", {}).get("verdict") == "NOT SELECTED" else "NOT COMPLETED"
    print("\n" + "=" * 118)
    print(f"CHECKS: {sum(CHECKS.values())}/{len(CHECKS)} passed; closure gates (A, B, C, E): {sum(CHECKS[t] for t in closure_tags)}/{len(closure_tags)}")
    print(f"VERDICT: {verdict};  Part D: {RES.get('partD_verdict')} as frozen, {RES.get('partD_verdict_A1')} as frozen + A1")
    failed = [t for t, v in CHECKS.items() if not v]
    print(f"failed: {failed}")
    RES["checks"] = CHECKS
    RES["verdict"] = verdict
    RES["runtime_s"] = round(time.time() - T0, 1)
    RES["peak_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576)

    if MODE == "REAL":
        with open(os.path.join(HERE, "cfg899_d08.json"), "w") as fh:
            json.dump(RES, fh, indent=1, default=str)
        print("kappa = 1/2 FITTED; alpha stays an INPUT; SM mass sector walled; not theory closed.")
        sys.exit(0 if verdict.startswith("CLOSED") else 2)

    # ---------------------------------------------------------------- MUTATE controls
    lchecks = {}
    if MODE == "MUTATE_SPIN":
        targeted = ["B1", "A4b", "B4", "D-G5"]
        ref = json.load(open(os.path.join(HERE, "cfg899_d08.json")))
        lchecks["L-SPIN b"] = RES["b_graded"] == ref["B1"]["D4_g1"]["b"] == "-1"
        lchecks["L-SPIN weight"] = RES["weight_graded"] == ref["weight_g1_4D"] == "-1"
        lchecks["L-SPIN sigma_Rxi"] = sp.simplify(sp.sympify(RES["sigma_Rxi_graded"]) - sp.sympify(ref["sigma_Rxi"]["1"])) == 0 and sp.simplify(sp.sympify(RES["sigma_Rxi_graded"]) + sp.Rational(5, 24) / sp.pi ** 2) == 0
        lchecks["L-SPIN flat q^4 ratio"] = sp.sympify(RES["flat_q4_ratio_graded"]) == sp.sympify(ref["C3_flat_ratio"]["1"]) == -7
    else:
        targeted = ["B1", "B4"]
        lchecks["L-DIM ratio"] = sp.sympify(RES["ratio_graded"]) == D_COUNT - 25 and sp.sympify(RES["b_graded_ratio_B4"]) == D_COUNT - 25
        lchecks["L-DIM weight"] = sp.sympify(RES["weight_graded"]) == D_COUNT - 1
    for k, v in lchecks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    tfail = all(not CHECKS.get(t, True) for t in targeted)
    works = tfail and all(lchecks.values())
    print(f"MUTATE {MODE}: targeted checks {targeted} {'all FAILED as required' if tfail else 'did NOT all fail'}; L-checks {'all pass' if all(lchecks.values()) else 'FAIL'}")
    print("-> the control works (exit 1)" if works else "-> the control did NOT work (exit 3)")
    RES["lchecks"] = lchecks
    RES["targeted"] = targeted
    with open(os.path.join(HERE, f"cfg899_d08_{MODE}.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    sys.exit(1 if works else 3)


if __name__ == "__main__":
    main()
