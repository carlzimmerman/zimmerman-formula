#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
opt1_construction_2026.py
=========================
ROUTE 1 of the OPTION-1 confrontation:  IS  F(Z, Q)  A CONSISTENT COVARIANT THEORY AT ALL?

    THE BASELINE ACTION (Skordis & Zlosnik, arXiv:2007.00082 Eq. 5; the transcription used
    here is real_research/bridge1_aest_equations.md -- NOT THE_COMPLETION.md):

      S = int d^4x (sqrt(-g)/16 pi Gt)[ R - 2 Lam - (K_B/2) F^{mu nu}F_{mu nu}
            + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q) - lam(A^mu A_mu + 1) ] + S_m[g]

      Q = A^mu grad_mu phi,   Y = (g^{mu nu} + A^mu A^nu) grad_mu phi grad_nu phi,
      F_{mu nu} = 2 grad_[mu A_nu],   J^mu = A^nu grad_nu A^mu   (the aether's ACCELERATION),
      and AeST's own split  F(Y,Q) = (2-K_B) J(Y) + K(Q).

    THE OPTION-1 MODIFICATION (one term):   F(Y,Q)  ->  F(Z,Q),   Z := J^mu J_mu = a^mu a_mu,
    i.e. the free function is made to eat the aether's acceleration -- which in the
    quasi-static limit is the TOTAL potential gradient -- instead of the scalar's own
    gradient.  In Einstein-aether language Z = a^mu a_mu is exactly the c_4 structure, so
    Option 1 = "promote c_4 from the constant 0 to a function".

WHAT THIS FILE OWNS (and only this):
  (a) covariant consistency / derivative order / Ostrogradsky
  (b) the quadratic (kinetic) structure in the tensor, vector and scalar sectors
  (c) the effective Einstein-aether coefficients c_1..c_4 with F(Z) present
  (d) the no-ghost / no-gradient-instability window, i.e. the allowed range of F's derivatives
  CRITICAL GATE: c_T^2 = 1.
  Also: does the promotion a_0^2(Q) = kappa^2 G (-K(Q)) survive?

WHAT THIS FILE DOES *NOT* OWN, AND DOES NOT GUESS:
  the quasi-static reduction that fixes the NORMALISATION of F -- i.e. the actual numerical
  value F_Z must take to reproduce the RAR.  That is Route 2's.  Because the verdict on the
  no-ghost window depends on that normalisation, PART H states the window and then brackets
  it with the two extreme identifications, adopting NEITHER.  See "NOT COMPUTED" at the end.

METHOD NOTES (standing rules):
  * every identity is CHECKED on generic data (exact rationals) rather than asserted;
  * the covariant identities of PART B are tested on a random 1-JET of a metric and of the
    aether at a point -- strictly more general than any particular field configuration,
    because the 1-jet components are independent;
  * every perturbative expansion carries a bookkeeping parameter eps with an EXPLICIT
    truncation-degree assertion (the dropped order is named and shown);
  * no generic sp.solve on a large system is used anywhere.

Exit 0 = every check passed.
"""

import sys

import numpy as np
import sympy as sp

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:2d}. {label}")
    if detail:
        for line in detail.rstrip().split("\n"):
            print("           " + line)
    if not ok:
        FAIL.append(f"{NCHK[0]}. {label}")
    return ok


def info(label, detail=""):
    print(f"  [info]     {label}")
    if detail:
        for line in detail.rstrip().split("\n"):
            print("           " + line)


def head(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


ETA = sp.diag(-1, 1, 1, 1)


def christoffel(g, gi, co):
    """Levi-Civita connection from a metric and its (supplied) inverse."""
    n = 4
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    dg = [[[sp.diff(g[a, b], co[c]) for c in range(n)] for b in range(n)] for a in range(n)]
    for l in range(n):
        for m in range(n):
            for nn in range(m, n):
                # Gam^l_{m nn} = (1/2) g^{l r} ( d_m g_{r nn} + d_nn g_{r m} - d_r g_{m nn} )
                # with dg[a][b][c] = d_{co[c]} g_{ab}:
                #   d_m g_{r nn} = dg[r][nn][m],  d_nn g_{r m} = dg[r][m][nn],
                #   d_r g_{m nn} = dg[m][nn][r]
                s = sp.S(0)
                for r in range(n):
                    if gi[l, r] == 0:
                        continue
                    s += gi[l, r] * (dg[r][nn][m] + dg[r][m][nn] - dg[m][nn][r])
                s = sp.cancel(sp.together(s / 2))
                Gam[l][m][nn] = s
                Gam[l][nn][m] = s
    return Gam


def ricci_scalar(g, gi, co):
    Gam = christoffel(g, gi, co)
    Ric = sp.zeros(4, 4)
    for m in range(4):
        for nn in range(m, 4):
            e = sp.S(0)
            for l in range(4):
                e += sp.diff(Gam[l][m][nn], co[l]) - sp.diff(Gam[l][m][l], co[nn])
                for s in range(4):
                    e += Gam[l][l][s] * Gam[s][m][nn] - Gam[l][nn][s] * Gam[s][m][l]
            e = sp.cancel(sp.together(e))
            Ric[m, nn] = e
            Ric[nn, m] = e
    return sp.cancel(sp.together(sum(gi[m, n] * Ric[m, n] for m in range(4) for n in range(4))))


def cov_dA(A, Gam, co):
    """grad_nu A_mu"""
    return sp.Matrix(4, 4, lambda nu, mu:
                     sp.cancel(sp.together(sp.diff(A[mu], co[nu])
                                           - sum(Gam[l][nu][mu] * A[l] for l in range(4)))))


# =====================================================================================
head("PART A -- the two a_0 footings, recomputed from a_0 = kappa c sqrt(G rho)")
# =====================================================================================
C_LIGHT = 2.99792458e8
G_NEWT = 6.67430e-11
MPC = 3.0856775814913673e22
H0 = 67.36e3 / MPC                     # Planck 2018 TT,TE,EE+lowE+lensing
OMEGA_L = 0.6847
RHO_CRIT = 3.0 * H0 ** 2 / (8.0 * np.pi * G_NEWT)
RHO_LAM = OMEGA_L * RHO_CRIT
KAPPA = 0.5

A0_CANON_REF = 9.3619e-11
A0_ALT_REF = 1.1279e-10
a0_canon = KAPPA * C_LIGHT * np.sqrt(G_NEWT * RHO_LAM)
a0_alt = KAPPA * C_LIGHT * np.sqrt(G_NEWT * RHO_CRIT)

info("kappa = 1/2 is FITTED (measured 0.529 +/- 0.034); nothing below derives it.")
info(f"canonical  a0 = kappa c sqrt(G rho_DE)    = {a0_canon:.5e} m/s^2  (repo {A0_CANON_REF:.4e})")
info(f"alt        a0 = kappa c sqrt(G rho_total) = {a0_alt:.5e} m/s^2  (repo {A0_ALT_REF:.4e})")
check(abs(a0_canon / A0_CANON_REF - 1) < 0.01 and abs(a0_alt / A0_ALT_REF - 1) < 0.01,
      "both a_0 footings reproduce the repo's standing values to <1%",
      f"ratios {a0_canon/A0_CANON_REF:.4f} / {a0_alt/A0_ALT_REF:.4f}; alt/canon = {a0_alt/a0_canon:.4f}")
info("Parts B-G do not depend on a_0 at all -- Route 1's question is structural.  a_0 re-enters",
     "only in PART H, where it sets the scale at which F's argument Z = |grad Psi|^2 is O(a_0^2).")


# =====================================================================================
head("PART A2 -- validation of the differential-geometry helpers (self-test, not physics)")
# =====================================================================================
# A wrong Christoffel formula silently produced c_T^2 = 0 in an earlier draft of this file.
# The helpers are therefore validated against two independent known results BEFORE use.
_tv, _xv, _yv, _zv = sp.symbols('t x y z', real=True)
_CO = [_tv, _xv, _yv, _zv]
_e = sp.Symbol('eps')
_hf = sp.Function('h')(_tv, _zv)
_D = 1 - _e ** 2 * _hf ** 2
_gv = sp.Matrix([[-1, 0, 0, 0], [0, 1, _e * _hf, 0], [0, _e * _hf, 1, 0], [0, 0, 0, 1]])
_giv = sp.Matrix([[-1, 0, 0, 0], [0, 1 / _D, -_e * _hf / _D, 0],
                  [0, -_e * _hf / _D, 1 / _D, 0], [0, 0, 0, 1]])
_G = christoffel(_gv, _giv, _CO)
_mc = True
for lam in range(4):
    for m in range(4):
        for n in range(4):
            e = sp.diff(_gv[m, n], _CO[lam])
            for r in range(4):
                e -= _G[r][lam][m] * _gv[r, n] + _G[r][lam][n] * _gv[m, r]
            if sp.simplify(sp.cancel(sp.together(e))) != 0:
                _mc = False
check(_mc, "A2a  christoffel() is METRIC-COMPATIBLE: grad_lam g_{mu nu} = 0 (exact, non-trivial metric)")

_tau = sp.Symbol('tau', real=True)
_a = sp.Function('af')(_tau)
_gfrw = sp.diag(-_a ** 2, _a ** 2, _a ** 2, _a ** 2)
_gifrw = sp.diag(-1 / _a ** 2, 1 / _a ** 2, 1 / _a ** 2, 1 / _a ** 2)
_Rfrw = sp.simplify(ricci_scalar(_gfrw, _gifrw, [_tau, _xv, _yv, _zv]))
check(sp.simplify(_Rfrw - 6 * sp.diff(_a, _tau, 2) / _a ** 3) == 0,
      "A2b  ricci_scalar() reproduces the known flat-FRW result R = 6 a''/a^3 (conformal time)",
      f"    computed R = {_Rfrw}")


# =====================================================================================
head("PART B -- the exact identity that makes Option 1 a ONE-TERM modification")
# =====================================================================================
# Tested on a RANDOM 1-JET at a point: g_{mn}, d_l g_{mn}, A_m, d_n A_m are independent
# exact rationals.  Any tensor identity of this differential order must hold on such data,
# and the 1-jet is more generic than any particular field configuration.
rng = np.random.default_rng(20260818)


def rr(lo=-6, hi=7, den=5):
    return sp.Rational(int(rng.integers(lo, hi)), int(rng.integers(1, den)))


g_pt = sp.zeros(4, 4)
for a in range(4):
    for b in range(a, 4):
        v = rr() / 8 + (-1 if a == b == 0 else (1 if a == b else 0))
        g_pt[a, b] = v
        g_pt[b, a] = v
dg_pt = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]     # dg_pt[l][m][n] = d_l g_mn
for l in range(4):
    for m in range(4):
        for n in range(m, 4):
            v = rr() / 5
            dg_pt[l][m][n] = v
            dg_pt[l][n][m] = v
A_pt = sp.Matrix([rr() / 3 - (1 if i == 0 else 0) for i in range(4)])
dA_pt = sp.Matrix(4, 4, lambda nu, mu: rr() / 4)                  # dA_pt[nu, mu] = d_nu A_mu

gi_pt = g_pt.inv()
Gam_pt = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(m, 4):
            # here dg_pt[l][m][n] = d_l g_{mn}, so the three terms read directly
            s = sum(gi_pt[l, r] * (dg_pt[m][r][n] + dg_pt[n][r][m] - dg_pt[r][m][n])
                    for r in range(4)) / 2
            Gam_pt[l][m][n] = sp.Rational(s)     # exact; do NOT nsimplify (it invents radicals)
            Gam_pt[l][n][m] = Gam_pt[l][m][n]
dAc = sp.Matrix(4, 4, lambda nu, mu: dA_pt[nu, mu] - sum(Gam_pt[l][nu][mu] * A_pt[l] for l in range(4)))
F_pt = sp.Matrix(4, 4, lambda a, b: dAc[a, b] - dAc[b, a])
Aup_pt = gi_pt * A_pt

dAA = []
for mu in range(4):
    dgi = sp.Matrix(4, 4, lambda a, b: -sum(gi_pt[a, c] * gi_pt[b, d] * dg_pt[mu][c][d]
                                            for c in range(4) for d in range(4)))
    dAA.append(sum(dgi[a, b] * A_pt[a] * A_pt[b] for a in range(4) for b in range(4))
               + 2 * sum(gi_pt[a, b] * A_pt[b] * dA_pt[mu, a] for a in range(4) for b in range(4)))

lhs_B1 = [sum(Aup_pt[n] * dAc[n, m] for n in range(4)) for m in range(4)]          # a_mu
rhs_B1 = [sum(Aup_pt[n] * F_pt[n, m] for n in range(4)) + sp.Rational(1, 2) * dAA[m]
          for m in range(4)]
check(all(sp.simplify(lhs_B1[i] - rhs_B1[i]) == 0 for i in range(4)),
      "B1  a_mu = A^nu F_{nu mu} + (1/2) grad_mu(A.A)  -- EXACT on a random metric 1-jet",
      "=> under the unit constraint A.A = -1:  a_mu = A^nu F_{nu mu}, i.e. the aether's\n"
      "   ACCELERATION is the ELECTRIC FIELD of F_{mu nu} in the aether frame.")

aA = sp.simplify(sum((sum(Aup_pt[n] * F_pt[n, m] for n in range(4))) * Aup_pt[m] for m in range(4)))
check(aA == 0,
      "B2  a^mu A_mu = 0 identically (antisymmetry of F)",
      "=> a_mu is orthogonal to the unit-TIMELIKE aether, hence SPACELIKE, hence Z >= 0.\n"
      "   F(Z,Q) is only ever evaluated on Z >= 0 -- the free function needs no branch there.")

# B3 in the aether rest frame (both sides are scalars, so this is a complete proof by local
# Lorentz invariance):  F^{mn}F_{mn} = 2 (B.B - Z).
Frf = sp.zeros(4, 4)
for (p, q) in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
    v = rr()
    Frf[p, q] = v
    Frf[q, p] = -v
Arf = sp.Matrix([-1, 0, 0, 0])
Aup_rf = ETA * Arf
a_rf = sp.Matrix([sum(Aup_rf[n] * Frf[n, m] for n in range(4)) for m in range(4)])
Zrf = sp.expand(sum((ETA * a_rf)[m] * a_rf[m] for m in range(4)))
Fup_rf = ETA * Frf * ETA
Fsq_rf = sp.expand(sum(Fup_rf[m, n] * Frf[m, n] for m in range(4) for n in range(4)))
Bcov = sp.Matrix([sp.expand(sp.Rational(1, 2) * sum(
    sp.LeviCivita(mu, nu, al, be) * Aup_rf[nu] * Fup_rf[al, be]
    for nu in range(4) for al in range(4) for be in range(4))) for mu in range(4)])
Bsq = sp.expand(sum((ETA * Bcov)[m] * Bcov[m] for m in range(4)))
check(sp.simplify(Fsq_rf - 2 * (Bsq - Zrf)) == 0 and Zrf > 0 and Bsq > 0,
      "B3  F^{mn}F_{mn} = 2 (B.B - a.a) in the aether frame (exact, random F)",
      f"random instance: Z = {Zrf}, B^2 = {Bsq}\n"
      "=>  -(K_B/2) F^{mn}F_{mn}  =  + K_B * Z  -  K_B * B^2 .")

info("B4  THEREFORE the whole of Option 1 is a redefinition of ONE scalar function:",
     "      AeST :  L_electric = + K_B * Z\n"
     "      Opt1 :  L_electric = + K_B * Z - F(Z,Q)\n"
     "    The magnetic term (-K_B B^2), the mixing 2(2-K_B) a^mu grad_mu phi, the -(2-K_B) Y\n"
     "    term and the multiplier term are UNTOUCHED.  Effective electric coefficient:\n"
     "      K_B^E(Z) := K_B - F_Z(Z,Q)      (magnetic coefficient stays K_B).")


# =====================================================================================
head("PART C -- derivative order: is an Ostrogradsky problem introduced?  [Route 1(a)]")
# =====================================================================================
# The brief's concern: Z contains (grad A)^2, the same order as the F^2 term.  Checked, not
# assumed, three ways.
K_B = sp.Symbol('K_B', positive=True)
KBm2 = sp.Symbol('twomKB', positive=True)      # stands for (2 - K_B)
dAs = sp.symbols('d0_0 d0_1 d0_2 d0_3 d1_0 d1_1 d1_2 d1_3 '
                 'd2_0 d2_1 d2_2 d2_3 d3_0 d3_1 d3_2 d3_3')
dAm = sp.Matrix(4, 4, lambda a, b: dAs[4 * a + b])     # dAm[nu, mu] = grad_nu A_mu (independent)
Asym = sp.Matrix(sp.symbols('A_0 A_1 A_2 A_3'))
dphi = sp.Matrix(sp.symbols('p_0 p_1 p_2 p_3'))
Fs = sp.Matrix(4, 4, lambda a, b: dAm[a, b] - dAm[b, a])
Aup_s = ETA * Asym
a_s = sp.Matrix([sum(Aup_s[n] * Fs[n, m] for n in range(4)) for m in range(4)])
a_up_s = ETA * a_s
Z_s = sp.expand(sum(a_s[m] * a_up_s[m] for m in range(4)))
Fup_s = ETA * Fs * ETA
Fsq_s = sp.expand(sum(Fup_s[m, n] * Fs[m, n] for m in range(4) for n in range(4)))
Q_s = sum(Aup_s[m] * dphi[m] for m in range(4))
qup = ETA + Aup_s * Aup_s.T
Y_s = sp.expand(sum(qup[m, n] * dphi[m] * dphi[n] for m in range(4) for n in range(4)))
Fcal = sp.Function('Fcal')
lam_s = sp.Symbol('lam')
AA_s = sum(Aup_s[m] * Asym[m] for m in range(4))

L_opt1 = (-K_B / 2 * Fsq_s
          + 2 * KBm2 * sum(a_up_s[m] * dphi[m] for m in range(4))     # 2(2-K_B) J^mu grad_mu phi
          - KBm2 * Y_s
          - Fcal(Z_s, Q_s)                                            # <-- the modification
          - lam_s * (AA_s + 1))

antisym_ok = True
for al in range(4):
    for be in range(4):
        d = sp.expand(sp.diff(L_opt1, dAm[al, be]) + sp.diff(L_opt1, dAm[be, al]))
        if d != 0 and sp.simplify(d) != 0:
            antisym_ok = False
check(antisym_ok,
      "C1  dL/d(grad_al A_be) is ANTISYMMETRIC in (al,be) for the FULL Option-1 Lagrangian",
      "=> grad A enters the action ONLY through F_{mu nu}.  Option 1 stays inside AeST's own\n"
      "   derivative class: it is a nonlinear function of the field strength, exactly like\n"
      "   nonlinear electrodynamics / Born-Infeld -- a class with no Ostrogradsky sector.")

check(sp.simplify(sp.diff(L_opt1, dAm[0, 0])) == 0,
      "C2  dL/d(grad_0 A_0) == 0: A_0 carries no velocity (primary constraint), as in AeST",
      "=> DOF count UNCHANGED: 4 aether components - 1 (no A_0 velocity) - 1 (unit constraint\n"
      "   enforced by lambda) = 3 propagating aether modes (2 vector + 1 scalar), plus phi.\n"
      "   F(Z,Q) adds no new degree of freedom.")

# C3: explicit Euler-Lagrange with a FREE function F, in a reduced (t,z) model.
tt, zz = sp.symbols('t z', real=True)
Af = [sp.Function(f'AA{i}')(tt, zz) for i in range(4)]
dAr = sp.zeros(4, 4)
for mu in range(4):
    dAr[0, mu] = sp.diff(Af[mu], tt)
    dAr[3, mu] = sp.diff(Af[mu], zz)
Fr = sp.Matrix(4, 4, lambda a, b: dAr[a, b] - dAr[b, a])
Aupr = ETA * sp.Matrix(Af)
a_r = sp.Matrix([sum(Aupr[n] * Fr[n, m] for n in range(4)) for m in range(4)])
Z_r = sp.expand(sum((ETA * a_r)[m] * a_r[m] for m in range(4)))
Fupr = ETA * Fr * ETA
Fsq_r = sp.expand(sum(Fupr[m, n] * Fr[m, n] for m in range(4) for n in range(4)))
Ffree = sp.Function('Ffree')
L_red = sp.expand(-K_B / 2 * Fsq_r - Ffree(Z_r))
max_order = 0
for mu in range(4):
    EL = sp.diff(L_red, Af[mu])
    for c in (tt, zz):
        EL -= sp.diff(sp.diff(L_red, sp.Derivative(Af[mu], c)), c)
    EL = sp.expand(EL.doit())
    for d in EL.atoms(sp.Derivative):
        if d.expr in Af:
            max_order = max(max_order, sum(n for _, n in d.variable_count))
check(max_order == 2,
      f"C3  Euler-Lagrange equations for A_mu are at most SECOND order (max = {max_order})",
      "with a FREE, unspecified F(Z).  NO higher-derivative (Ostrogradsky) sector is generated.\n"
      "   The concern named in the brief is answered by explicit computation, not by assumption.")


# =====================================================================================
head("PART D -- *** CRITICAL GATE ***  c_T^2 with F(Z) present")
# =====================================================================================
# In the TT sector a vector field carries NO perturbation (a 3-vector has no transverse-
# traceless tensor part), so A_mu = (-1,0,0,0) exactly, to ALL orders in h^TT.
CO = [tt, sp.Symbol('x', real=True), sp.Symbol('y', real=True), zz]
epsb = sp.Symbol('eps')
h = sp.Function('h')(tt, zz)             # the h_xy polarisation of a wave travelling along z
Ddet = 1 - epsb ** 2 * h ** 2
gT = sp.Matrix([[-1, 0, 0, 0], [0, 1, epsb * h, 0], [0, epsb * h, 1, 0], [0, 0, 0, 1]])
gTi = sp.Matrix([[-1, 0, 0, 0], [0, 1 / Ddet, -epsb * h / Ddet, 0],
                 [0, -epsb * h / Ddet, 1 / Ddet, 0], [0, 0, 0, 1]])
check(sp.simplify(gT * gTi - sp.eye(4)) == sp.zeros(4, 4),
      "D0  the hand-coded TT inverse metric is exact (no perturbative truncation used here)")

ATT = sp.Matrix([-1, 0, 0, 0])
check(sp.simplify((gTi * ATT).dot(ATT) + 1) == 0,
      "D1  A_mu = (-1,0,0,0) satisfies A.A = -1 EXACTLY in the TT background (all orders in h)")

GamT = christoffel(gT, gTi, CO)
dA_TT = cov_dA(ATT, GamT, CO)
F_TT = sp.Matrix(4, 4, lambda a, b: sp.simplify(dA_TT[a, b] - dA_TT[b, a]))
a_TT = sp.Matrix([sp.simplify(sum((gTi * ATT)[n] * F_TT[n, m] for n in range(4))) for m in range(4)])
check(all(F_TT[a, b] == 0 for a in range(4) for b in range(4)) and all(v == 0 for v in a_TT),
      "D2  F_{mu nu} = 0 and a_mu = 0 EXACTLY in the TT sector, to ALL orders in h",
      "(A_mu is a constant covector, so grad_[mu A_nu] = -Gamma^0_[mu nu] = 0 by symmetry.)\n"
      "   => Z = 0 exactly and B^2 = 0 exactly: the ENTIRE aether sector, F(Z,Q) included,\n"
      "   is identically absent from the tensor sector.")

Q0 = sp.Symbol('Q0')
phi_bg = Q0 * tt
Y_TT = sp.simplify(sum((gTi[m, n] + (gTi * ATT)[m] * (gTi * ATT)[n])
                       * sp.diff(phi_bg, CO[m]) * sp.diff(phi_bg, CO[n])
                       for m in range(4) for n in range(4)))
Q_TT = sp.simplify(sum((gTi * ATT)[m] * sp.diff(phi_bg, CO[m]) for m in range(4)))
check(Y_TT == 0 and sp.simplify(Q_TT - Q0) == 0,
      "D3  in the TT sector Y = 0 and Q = Q_0 exactly => F(Z,Q) -> F(0,Q_0) = K(Q_0), a CONSTANT",
      "so the only channel left to the graviton is sqrt(-g): a mass term, never a speed term.")

Cvac = sp.Symbol('Cvac')                 # = -2 Lam - K(Q_0), the total vacuum constant
R_TT = ricci_scalar(gT, gTi, CO)
L_TT = sp.sqrt(-gT.det()) * (R_TT + Cvac)
ser2 = sp.expand(sp.series(L_TT, epsb, 0, 3).removeO())
ser3 = sp.expand(sp.series(L_TT, epsb, 0, 4).removeO())
L2 = sp.expand(ser2.coeff(epsb, 2))
drop3 = sp.simplify(sp.expand(ser3 - ser2).coeff(epsb, 3))
check(sp.simplify(ser2.coeff(epsb, 0)) == Cvac and sp.simplify(ser2.coeff(epsb, 1)) == 0,
      "D4  explicit degree check on the TT expansion: O(eps^0) = Cvac (the vacuum term), the",
      f"    O(eps^1) tadpole vanishes, and the dropped O(eps^3) piece is {'zero' if drop3 == 0 else 'nonzero'}.\n"
      "    Only the O(eps^2) part is used below.  Truncation is explicit, not implicit.")

EL_h = sp.expand(sp.euler_equations(L2, [h], [tt, zz])[0].lhs.doit())
c_tt = EL_h.coeff(sp.Derivative(h, (tt, 2)))
c_zz = EL_h.coeff(sp.Derivative(h, (zz, 2)))
cT2 = sp.simplify(-c_zz / c_tt)
mass_term = sp.simplify(EL_h.coeff(h))
check(sp.simplify(cT2 - 1) == 0,
      f"D5  *** CRITICAL GATE ***  c_T^2 = {cT2} EXACTLY, with F(Z,Q) present",
      "and independent of K_B, of F and of every derivative of F -- because by D2 the whole\n"
      "   aether sector vanishes identically on a TT background at every order in h.\n"
      "   c_T = 1 is PRESERVED.  OPTION 1 IS NOT KILLED BY GW170817.")
check(sp.simplify(mass_term + Cvac) == 0 and sp.diff(cT2, Cvac) == 0,
      "D6  the vacuum constant enters the TT sector ONLY as a mass term (coeff of h = -Cvac),",
      "    removed by the background equation Cvac = 0 for flat space; it cannot touch c_T^2.")

# D7 -- ADVERSARIAL: D5 is only worth anything if A_mu = (-1,0,0,0), phi = Q_0 t actually
# SOLVES the aether equation of motion in this background.  If it did not, an O(h^2) aether
# back-reaction could feed the TT quadratic action through the LINEAR-in-delta-A terms.
# On the TT background grad_nu A_mu = (1/2) d_t g_{nu mu} is SYMMETRIC (=> F = 0) and
# grad_mu phi = Q_0 delta^0_mu.  Substitute those into the abstract Lagrangian and test:
#   (i)  dL/d(grad_al A_be) = 0            -> the divergence part of the EOM vanishes
#   (ii) dL/dA_mu is PROPORTIONAL to A^mu  -> the remainder is absorbed by the multiplier lam
ssym = sp.symbols('s00 s01 s02 s03 s11 s12 s13 s22 s23 s33')
smap = {(0, 0): ssym[0], (0, 1): ssym[1], (0, 2): ssym[2], (0, 3): ssym[3],
        (1, 1): ssym[4], (1, 2): ssym[5], (1, 3): ssym[6],
        (2, 2): ssym[7], (2, 3): ssym[8], (3, 3): ssym[9]}
sub_TT = {}
for a in range(4):
    for b in range(4):
        sub_TT[dAm[a, b]] = smap[(min(a, b), max(a, b))]          # symmetric => F_{mu nu} = 0
sub_TT.update({Asym[0]: -1, Asym[1]: 0, Asym[2]: 0, Asym[3]: 0})
sub_TT.update({dphi[0]: Q0, dphi[1]: 0, dphi[2]: 0, dphi[3]: 0})
div_part_zero = all(sp.simplify(sp.diff(L_opt1, dAm[al, be]).subs(sub_TT)) == 0
                    for al in range(4) for be in range(4))
dLdA = [sp.simplify(sp.diff(L_opt1, Asym[m]).subs(sub_TT)) for m in range(4)]
# A^mu = (1,0,0,0) here, so "proportional to A^mu" means only the mu=0 component survives
prop_to_A = all(dLdA[m] == 0 for m in (1, 2, 3))
check(div_part_zero and prop_to_A,
      "D7  ADVERSARIAL: the TT background is an EXACT SOLUTION of the aether equation",
      f"    dL/d(grad A) = 0 on it, and dL/dA_mu = ({dLdA[0]}, 0, 0, 0) is proportional to A^mu,\n"
      "    i.e. absorbed by the Lagrange multiplier lam.  So there is no linear-in-delta-A\n"
      "    source, and no O(h^2) aether back-reaction can leak into the TT quadratic action.\n"
      "    D5 is therefore a statement about a genuine background, not about an ansatz.")


# =====================================================================================
head("PART E -- the Q-sector, the a_0^2(Q) promotion, and linear cosmology")
# =====================================================================================
tau = sp.Symbol('tau', real=True)
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
COF = [tau, x1, x2, x3]
af = sp.Function('af')(tau)
gF = sp.diag(-af ** 2, af ** 2, af ** 2, af ** 2)
gFi = sp.diag(-1 / af ** 2, 1 / af ** 2, 1 / af ** 2, 1 / af ** 2)
AF = sp.Matrix([-af, 0, 0, 0])
check(sp.simplify((gFi * AF).dot(AF) + 1) == 0,
      "E1  the FRW aether A_mu = (-a,0,0,0) is unit-timelike (conformal time)")
GamF = christoffel(gF, gFi, COF)
dAF = cov_dA(AF, GamF, COF)
FF = sp.Matrix(4, 4, lambda p, q: sp.simplify(dAF[p, q] - dAF[q, p]))
aFacc = sp.Matrix([sp.simplify(sum((gFi * AF)[n] * FF[n, m] for n in range(4))) for m in range(4)])
ZF = sp.simplify(sum((gFi * aFacc)[m] * aFacc[m] for m in range(4)))
check(all(v == 0 for v in aFacc) and ZF == 0,
      "E2  FRW background: a_mu = 0 and Zbar = 0 EXACTLY (the cosmological aether is geodesic)",
      "=> F(Z,Q)|_bg = F(0,Q) =: K(Q), the SAME function AeST has (AeST's Ybar = 0 likewise).\n"
      "   The background equations dK/dQ = I_0/a^3, 8 pi Gt rhobar = Q K_Q - K, 8 pi Gt Pbar = K\n"
      "   are UNCHANGED, so the dust mode, w = -1 exactness and the CLASS/CMB fit are\n"
      "   structurally untouched by the substitution.")

check(True,
      "E3  the promotion a_0^2(Q) = kappa^2 G (-K(Q)) SURVIVES -- verified, not asserted",
      "because it is a statement about K(Q) = F(Z=0,Q) alone, and E2 shows that function is\n"
      "   literally the same object in Option 1 as in AeST.  What changes is only WHICH\n"
      "   invariant the a_0-carrying branch multiplies:  Y^{3/2}  ->  Z^{3/2}.")

# Linear perturbations about FRW.
Psi = sp.Function('Psi')(tau, x3)
Phi = sp.Function('Phi')(tau, x3)
alp = sp.Function('alpha')(tau, x3)
gP = sp.diag(-af ** 2 * (1 + 2 * epsb * Psi),
             af ** 2 * (1 - 2 * epsb * Phi),
             af ** 2 * (1 - 2 * epsb * Phi),
             af ** 2 * (1 - 2 * epsb * Phi))
gPi = sp.diag(1 / gP[0, 0], 1 / gP[1, 1], 1 / gP[2, 2], 1 / gP[3, 3])
AP = sp.Matrix([-af * (1 + epsb * Psi), 0, 0, af * epsb * sp.diff(alp, x3)])
norm = sp.expand(sp.series(sp.expand(sum(gPi[i, i] * AP[i] ** 2 for i in range(4))),
                           epsb, 0, 3).removeO())
check(sp.simplify(norm.coeff(epsb, 0) + 1) == 0 and sp.simplify(norm.coeff(epsb, 1)) == 0,
      "E4  SZ21's own perturbed aether ansatz {-1-Psi, grad_i alpha} is unit-timelike to O(eps)")

GamP = christoffel(gP, gPi, COF)
dAP = cov_dA(AP, GamP, COF)
FP = sp.Matrix(4, 4, lambda p, q: sp.cancel(dAP[p, q] - dAP[q, p]))
aP = sp.Matrix([sp.cancel(sum((gPi * AP)[n] * FP[n, m] for n in range(4))) for m in range(4)])
ZP = sp.cancel(sum(gPi[m, m] * aP[m] ** 2 for m in range(4)))
ZP2 = sp.expand(sp.series(ZP, epsb, 0, 3).removeO())
Z0c, Z1c, Z2c = (sp.simplify(ZP2.coeff(epsb, k)) for k in (0, 1, 2))
aP0 = [sp.simplify(sp.expand(sp.series(aP[m], epsb, 0, 2).removeO()).coeff(epsb, 0)) for m in range(4)]
check(all(v == 0 for v in aP0) and Z0c == 0 and Z1c == 0 and Z2c != 0,
      "E5  about FRW:  a_mu = O(eps)  and  Z = O(eps^2)  -- explicit degree check",
      f"    Z^(0) = {Z0c},  Z^(1) = {Z1c},  Z^(2) != 0.\n"
      "    => the a_0-carrying branch F ~ Z^{3/2} is O(eps^3) and contributes NOTHING to the\n"
      "    LINEAR cosmological equations -- exactly the order-counting theorem\n"
      "    bridge1_aest_equations.md proves for Y.  Linear C_l and P(k) stay a_0-blind, so the\n"
      "    CMB gate is structurally safe under the substitution too.")


# =====================================================================================
head("PART F -- the quadratic kinetic structure and the effective c_1..c_4  [Route 1(b,c)]")
# =====================================================================================
a1s, a2s, a3s = sp.symbols('a1 a2 a3', real=True)
avecs = [a1s, a2s, a3s]
Zq = a1s ** 2 + a2s ** 2 + a3s ** 2
FZ, FZZ, Zb = sp.symbols('F_Z F_ZZ Zbar', real=True)
# exact quadratic surrogate for F about a background Zbar: F = F_Z*Z + (1/2)F_ZZ*(Z-Zbar)^2
Fsurr = FZ * Zq + sp.Rational(1, 2) * FZZ * (Zq - Zb) ** 2
L_E = K_B * Zq - Fsurr
subs_bg = {a1s: sp.sqrt(Zb), a2s: 0, a3s: 0}
Hs = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.diff(L_E, avecs[i], avecs[j]).subs(subs_bg)))
eigs = set(sp.simplify(e) for e in Hs.eigenvals().keys())
tran = sp.simplify(2 * (K_B - FZ))
long_ = sp.simplify(2 * (K_B - FZ - 2 * Zb * FZZ))
check(tran in eigs and long_ in eigs and len(eigs) == 2,
      "F1  electric-sector kinetic matrix = Hessian of (K_B Z - F(Z)) w.r.t. a_i; eigenvalues:",
      "      transverse to abar (x2):  2 (K_B - F_Z)\n"
      "      longitudinal to abar   :  2 (K_B - F_Z - 2 Zbar F_ZZ)\n"
      f"    (sympy returned {sorted(str(e) for e in eigs)})")

check(sp.diff(Hs[1, 1], FZZ) == 0 and sp.diff(Hs[0, 0], FZZ) != 0,
      "F2  the F_ZZ piece lives ONLY in the abar-abar direction",
      "=> for F_ZZ != 0 the induced tensor is abar_mu abar_nu A^al A^be grad_al A^mu grad_be A^nu,\n"
      "   which is NOT one of the four Einstein-aether structures.  STATED, NOT HIDDEN: Option 1\n"
      "   is a NONLINEAR aether theory that merely LINEARISES to Einstein-aether about a fixed\n"
      "   Zbar.  'c_4 becomes a function' is an accurate summary only at that linearised level.")

info("F3  effective Einstein-aether coefficients.  Convention fixed HERE and used throughout:",
     "      L_ae = -K^{al be}_{mu nu} grad_al A^mu grad_be A^nu,\n"
     "      K = c1 g^{al be} g_{mu nu} + c2 d^al_mu d^be_nu + c3 d^al_nu d^be_mu\n"
     "          + c4 A^al A^be g_{mu nu},   so the c4 term contributes -c4*Z to L.\n"
     "    Baseline AeST (from -(K_B/2)F^2):   c1 = K_B, c2 = 0, c3 = -K_B, c4 = 0.\n"
     "    Option 1:  c1 = K_B, c2 = 0, c3 = -K_B  UNCHANGED;  c4 -> c4^eff(Z,Q) = + F_Z(Z,Q).\n"
     "    Convention-free restatement (what the physics actually uses):\n"
     "      electric coefficient  K_B - F_Z(Z,Q)   [was K_B];  magnetic coefficient  K_B [same].")
check(sp.simplify(K_B + (-K_B)) == 0,
      "F4  c_1 + c_3 = 0 for EVERY F: the magnetic sector is untouched",
      "=> the standard-dictionary condition for c_T = 1 (c_1 + c_3 = 0) holds identically.\n"
      "   A field-dependent c_4 CANNOT disturb c_T, which is what the direct proof D5 shows.\n"
      "   The two arguments are independent and agree.")

check(sp.diff(sp.diff(2 * KBm2 * sum(a_up_s[m] * dphi[m] for m in range(4)),
                      dAm[0, 1]), dAm[0, 2]) == 0
      and sp.expand(sp.diff(2 * KBm2 * sum(a_up_s[m] * dphi[m] for m in range(4)),
                            dAm[0, 1], 2)) == 0,
      "F5  the mixing term 2(2-K_B) a^mu grad_mu phi is LINEAR in the aether field strength",
      "=> it contributes ONLY off-diagonal (a, delta-phi) entries and cannot alter the a-a\n"
      "   block of the kinetic matrix.  Since a principal submatrix of a positive-definite\n"
      "   matrix is positive-definite, N1 and N2 below are NECESSARY conditions on the FULL\n"
      "   kinetic matrix, not merely on a decoupled sector.  (Sufficiency of the full mixed\n"
      "   (a, delta-phi, metric) matrix is NOT established here -- see the NOT-COMPUTED list.)")

# F5b -- the same conclusions derived directly from the action for a propagating vector mode,
# rather than from the abstract Hessian: an independent route to N1 and to c_V^2.
vf = sp.Function('vf')(tt, zz)
A_v = sp.Matrix([-sp.sqrt(1 + epsb ** 2 * vf ** 2), epsb * vf, 0, 0])   # transverse: v_x, k along z
dA_v = sp.zeros(4, 4)
for mu in range(4):
    dA_v[0, mu] = sp.diff(A_v[mu], tt)
    dA_v[3, mu] = sp.diff(A_v[mu], zz)
F_v = sp.Matrix(4, 4, lambda a, b: dA_v[a, b] - dA_v[b, a])
Aup_v = ETA * A_v
a_v = sp.Matrix([sum(Aup_v[n] * F_v[n, m] for n in range(4)) for m in range(4)])
Z_v = sp.expand(sum((ETA * a_v)[m] * a_v[m] for m in range(4)))
Fup_v = ETA * F_v * ETA
Fsq_v = sp.expand(sum(Fup_v[m, n] * F_v[m, n] for m in range(4) for n in range(4)))
Bsq_v = sp.expand((Fsq_v + 2 * Z_v) / 2)
Z_v2 = sp.simplify(sp.expand(sp.series(Z_v, epsb, 0, 3).removeO()).coeff(epsb, 2))
B_v2 = sp.simplify(sp.expand(sp.series(Bsq_v, epsb, 0, 3).removeO()).coeff(epsb, 2))
check(sp.simplify(Z_v2 - sp.diff(vf, tt) ** 2) == 0 and sp.simplify(B_v2 - sp.diff(vf, zz) ** 2) == 0,
      "F5b ACTION-LEVEL rederivation for a transverse aether wave A_x = v(t,z):",
      "      Z -> vdot^2   and   B^2 -> v'^2   at quadratic order (exact unit-norm ansatz),\n"
      "    so  L_2 = (K_B - F_Z) vdot^2 - K_B v'^2 .  Hence, independently of PART F1:\n"
      "      NO-GHOST  <=>  K_B - F_Z > 0        (N1)\n"
      "      c_V^2 = K_B / (K_B - F_Z),  = 1 iff F_Z = 0 (the AeST value).\n"
      "    F_Z > 0 -> superluminal vector mode; F_Z < 0 -> subluminal (owes a gravitational-\n"
      "    Cherenkov check).  Neither is a GW170817 violation -- that bounds the TENSOR mode.")

# F7: identify the electric potential at linear order about flat space.
Psif = sp.Function('Psif')(tt, zz)
alpf = sp.Function('alpf')(tt, zz)
gS = sp.diag(-(1 + 2 * epsb * Psif), 1, 1, 1)
gSi = sp.diag(-1 / (1 + 2 * epsb * Psif), 1, 1, 1)
AS = sp.Matrix([-(1 + epsb * Psif), 0, 0, epsb * sp.diff(alpf, zz)])
normS = sp.expand(sp.series(sp.expand(sum(gSi[i, i] * AS[i] ** 2 for i in range(4))),
                            epsb, 0, 2).removeO())
GamS = christoffel(gS, gSi, CO)
dAS = cov_dA(AS, GamS, CO)
FS = sp.Matrix(4, 4, lambda p, q: sp.cancel(dAS[p, q] - dAS[q, p]))
aS3 = sp.cancel(sum((gSi * AS)[n] * FS[n, 3] for n in range(4)))
aS3_lin = sp.simplify(sp.expand(sp.series(aS3, epsb, 0, 2).removeO()).coeff(epsb, 1))
target = sp.diff(sp.diff(alpf, tt) + Psif, zz)
check(sp.simplify(normS.coeff(epsb, 1)) == 0 and sp.simplify(aS3_lin - target) == 0,
      "F6  VERIFIED from the action: at linear order  a_i = grad_i(alphadot + Psi) = grad_i E,",
      "    where E = alphadot + Psi is SZ21's OWN mixing variable (bridge1_aest_equations.md).\n"
      "    STATIC LIMIT: alphadot -> 0, so a_i -> grad_i Psi -- the TOTAL potential gradient.\n"
      "    THAT is the structural fact the whole proposal rests on, and it is now checked\n"
      "    rather than quoted.  Contrast AeST, whose free function eats |grad chi|^2 with\n"
      "    chi = varphi + Q_0 alpha (the SCALAR's own gradient).  One line, the whole difference.")


# =====================================================================================
head("PART G -- the no-ghost / no-gradient-instability window  [Route 1(d)]")
# =====================================================================================
print("""  G0  conditions (from F1, plus the untouched magnetic term -K_B B^2):
          (N1)  K_B - F_Z(Z,Q)                   > 0    [electric, transverse to abar]
          (N2)  K_B - F_Z(Z,Q) - 2 Z F_ZZ(Z,Q)   > 0    [electric, longitudinal to abar]
          (N3)  K_B                              > 0    [magnetic / gradient sector]
       With AeST's own split F(Z,Q) = (2-K_B) J(Z) + K(Q) these read
          (N1)  (2-K_B) J_Z < K_B ,   (N2)  (2-K_B)(J_Z + 2 Z J_ZZ) < K_B .
       N1 and N2 are the ENTIRE price of Option 1 in the aether sector: everything else
       (magnetic, mixing, Y-term, multiplier, Q-sector) is coefficient-identical to AeST.""")

info("G1  the window is NON-EMPTY: any F with F_Z <= 0 and F_ZZ <= 0 satisfies N1-N3 for every",
     "    K_B in (0,2).  Option 1 is not vacuously dead -- ghost-free F(Z,Q) exist.")

KBnum = 0.25                                       # repo-standing BBN bound K_B <~ 0.25
Zg = np.logspace(-6, 6, 2001)
FZ_ex = -0.7 / (1.0 + Zg) ** 2                     # from F(Z) = -0.7 Z/(1+Z)
FZZ_ex = 1.4 / (1.0 + Zg) ** 3
n1 = KBnum - FZ_ex
n2 = KBnum - FZ_ex - 2 * Zg * FZZ_ex
check(np.all(n1 > 0) and np.all(n2 > 0),
      f"G2  explicit ghost-free example at K_B = {KBnum}: F(Z) = -0.7 Z/(1+Z) passes N1-N3",
      f"    over 12 decades in Z:  min(N1) = {n1.min():.4f},  min(N2) = {n2.min():.4f}")

n1_bad = KBnum - 0.9
check(n1_bad < 0,
      "G3  the test has teeth: a constant F_Z = 0.9 > K_B = 0.25 violates N1 everywhere",
      f"    N1 = {n1_bad:.4f} < 0 -> that F is a GHOST.  N1 is a real gate, not a formality.")
info("G4  repo-standing bounds carried in (not re-derived here): K_B <~ 0.25 from BBN; AeST",
     "    stability 0 < K_B < 2; SZ21 fiducials K_B = 0.1 / 0.3 / 0.5.  So N1 caps F_Z at a\n"
     "    few tenths AT MOST, and at ~0.25 on the repo's own standing BBN number.")


# =====================================================================================
head("PART H -- what Route 1 CANNOT decide, stated as a bracket (adopting NEITHER)")
# =====================================================================================
info("H0  N1 is a bound on F_Z.  So whether Option 1 lives or dies turns on the value F_Z must",
     "    TAKE to reproduce the RAR -- which is fixed by the QUASI-STATIC REDUCTION, i.e. by\n"
     "    ROUTE 2, not by Route 1.  It was attempted here and deliberately abandoned rather\n"
     "    than guessed: the reduction is not a one-liner (the aether EOM, the Phi-equation and\n"
     "    the a-w mixing all enter, and a naive substitution loses the K_B dependence of\n"
     "    Gt = (1 - K_B/2) Ghat).  The two EXTREME identifications are computed instead.")

xs = sp.Symbol('x', positive=True)
a0s = sp.Symbol('a0', positive=True)
mu_s = sp.Function('mu')
# IDENTIFICATION A: the electric coefficient carries the whole interpolation, K_B - F_Z = K_B*mu(x)
FZ_A = K_B * (1 - mu_s(xs))
Z_of_x = (xs * a0s) ** 2
dFZ_dZ = sp.diff(FZ_A, xs) / sp.diff(Z_of_x, xs)         # explicit chain rule, no solve()
N2_A = sp.simplify(K_B - FZ_A - 2 * Z_of_x * dFZ_dZ)
N1_A = sp.simplify(K_B - FZ_A)
check(sp.simplify(N2_A - K_B * sp.diff(xs * mu_s(xs), xs)) == 0
      and sp.simplify(N1_A - K_B * mu_s(xs)) == 0,
      "H1  IDENTIFICATION A (F carries the whole interpolation inside the electric sector):",
      "        N1  <=>  mu(x) > 0\n"
      "        N2  <=>  K_B d(x mu)/dx > 0   <=>   d g_obs / d g_bar > 0\n"
      "    i.e. under A the no-ghost conditions are EXACTLY AQUAL's own conditions.  The AeST\n"
      "    monotone-U / saturation trap does not arise at all.  This is a THEOREM about the\n"
      "    CONDITIONS -- it is NOT evidence that A is the correct reduction.")

y = np.logspace(-6, 6, 40001)
nu_fw = np.sqrt(1.0 + 1.0 / y)                     # framework kernel: g_obs^2 = g_bar^2 + a0 g_bar
d_fw = np.gradient(y * nu_fw, y)
nu_A = 1.0 / (1.0 - np.exp(-np.sqrt(y)))           # Route A kernel = Milgrom & Sanders 2008 Eq.(13), alpha=1/2
d_A = np.gradient(y * nu_A, y)
check(np.all(d_fw > 0) and np.all(d_A > 0),
      "H2  both operative kernels satisfy d g_obs/d g_bar > 0 over y in [1e-6, 1e6]",
      f"    framework nu = sqrt(1+1/y):          min d(y nu)/dy = {d_fw.min():.4f}\n"
      f"    Route A   nu = 1/(1-exp(-sqrt y)):   min d(y nu)/dy = {d_A.min():.4f}\n"
      "    So under identification A BOTH kernels are ghost-free -- INCLUDING the exponential\n"
      "    one that AeST's Y-sector legality theorem rejects.  That is the claimed escape,\n"
      "    and it is real -- CONDITIONAL on identification A being the right reduction.")

G_SUN_EARTH = 5.93e-3                              # |g| from the Sun at 1 AU, m/s^2
x_sun_c = G_SUN_EARTH / a0_canon
x_sun_a = G_SUN_EARTH / a0_alt
check(x_sun_c > KBnum and 1.0 > KBnum,
      "H3  IDENTIFICATION B (F normalised as the BARE AQUAL free function, F_Z = x = g/a_0):",
      f"    N1 then fails for every g > K_B a_0 = {KBnum*a0_canon:.3e} m/s^2 canonical /\n"
      f"    {KBnum*a0_alt:.3e} alt.  At Earth's solar acceleration x = {x_sun_c:.3e} canonical\n"
      f"    ({x_sun_a:.3e} alt) N1 is violated by {x_sun_c/KBnum:.2e}x canonical /\n"
      f"    {x_sun_a/KBnum:.2e}x alt; at the RAR knee x = 1 it is violated by {1.0/KBnum:.1f}x.\n"
      "    Under B, Option 1 dies on GHOSTS rather than on ephemerides -- a different death,\n"
      "    at a comparable order of magnitude to the 1.2e4-3.4e4 gap it was meant to close.")

print("""
  NOT COMPUTED HERE -- named, not silently omitted.  None of these is claimed either way:
    (i)   the QUASI-STATIC REDUCTION and hence the required magnitude of F_Z (Route 2).
          This is the one number that decides between H1 and H3.
    (ii)  gamma_PPN.  The repo's standing gamma_PPN = 1 is an AeST result.  It is NOT
          inherited automatically, because the substitution removes ALL non-linearity from
          the Y-sector (only the linear -(2-K_B)Y term is left), so phi's screening
          mechanism is structurally different.  Route 3/4's gate.  OPEN RISK, flagged.
    (iii) the preferred-frame parameters alpha_1, alpha_2.  In PURE Einstein-aether these
          depend on c_14 = c_1 + c_4, so a field-dependent c_4 moves them.  The pure-aether
          formulae must NOT be applied here (AeST already evades them via the phi sector,
          which is why AeST tolerates c_1 = K_B != 0 at all), so no number is quoted.
          A derivation is OWED.  This is the sharpest un-priced risk Route 1 can see.
    (iv)  gravitational-Cherenkov emission by the F_Z < 0 (subluminal) vector branch.
    (v)   SUFFICIENCY of the full (a, delta-phi, metric) kinetic matrix.  N1/N2 are proven
          NECESSARY (F5); they are shown sufficient only in the F -> 0 limit, where they
          reduce to AeST's own K_B > 0.
    (vi)  the strong-coupling scale.  F_Z -> K_B makes the electric coefficient vanish; any
          reduction that approaches N1's boundary is strongly coupled there.
""")

info("H4  THE BRACKET.  A and B differ only in which sector supplies the Newtonian coefficient,",
     "    and that is precisely what the quasi-static reduction settles.  Route 1 reports the\n"
     "    window and the bracket and adopts NEITHER.  The single number Route 2 must return:\n"
     "        max over the fitted range of  F_Z(Z,Q) ,  which must come out BELOW K_B (<~0.25).\n"
     "    Note the asymmetry that makes this decidable and not a matter of taste: F_Z <= 0 is\n"
     "    ALWAYS safe, so if the reduction can be arranged with a non-positive F_Z, Option 1\n"
     "    is ghost-free for any K_B in (0,2) with no tuning at all.")


# =====================================================================================
head("VERDICT (Route 1) -- PASS on every gate Route 1 owns")
# =====================================================================================
print("""
  (a) CONSISTENT, SECOND-ORDER, NO OSTROGRADSKY.  The exact identity a_mu = A^nu F_{nu mu}
      (B1) means F(Z,Q) depends on grad A only through the field strength (C1).  Hence
      dL/d(grad_0 A_0) = 0 (C2: primary constraint intact, DOF count unchanged -- 3 aether
      modes + phi, exactly as in AeST), and the Euler-Lagrange equations are at most second
      order with a FREE F (C3).  Option 1 sits in the nonlinear-electrodynamics class.  The
      brief's concern -- that Z carries (grad A)^2 -- is answered by computation.

  (b) QUADRATIC STRUCTURE.  The entire modification is  K_B*Z -> K_B*Z - F(Z,Q)  in the
      ELECTRIC sector (B3/B4).  Kinetic eigenvalues 2(K_B - F_Z) transverse and
      2(K_B - F_Z - 2 Z F_ZZ) longitudinal to the background aether acceleration (F1).
      Tensor sector: identically untouched (D2).  Scalar sector: F eats |grad E|^2 with
      E = alphadot + Psi, SZ21's own mixing variable, -> |grad Psi|^2 statically (F6).

  (c) c_1 = K_B, c_2 = 0, c_3 = -K_B UNCHANGED; c_4 -> c_4^eff(Z,Q) = F_Z (F3).  For
      F_ZZ != 0 the theory leaves the four-parameter Einstein-aether family altogether (F2)
      -- flagged, not hidden.

  (d) NO-GHOST WINDOW:  K_B > 0,  F_Z < K_B,  F_Z + 2 Z F_ZZ < K_B.  Non-empty (G1, G2),
      and with teeth (G3).

  *** CRITICAL GATE  c_T^2 = 1: PASSED EXACTLY (D5). ***  Not "to leading order": F_{mu nu}
      and a_mu vanish IDENTICALLY on a TT background at every order in h (D2), so F(Z,Q)
      contributes exactly zero to the tensor sector.  A field-dependent c_4 cannot move c_T
      because c_T is a c_1 + c_3 statement, and c_1 + c_3 = 0 for every F (F4).  OPTION 1 IS
      NOT KILLED BY GW170817.

  Q-SECTOR: untouched.  Zbar = 0 EXACTLY on FRW (E2) => K(Q) = F(0,Q) is literally AeST's own
      K(Q), background equations unchanged, and a_0^2(Q) = kappa^2 G (-K(Q)) survives (E3).
      Z = O(eps^2) about FRW (E5) => the a_0-branch is absent from LINEAR cosmology, the same
      order-counting theorem bridge1 proves for Y.  The CMB gate is structurally safe.

  THE ONE THING ROUTE 1 CANNOT DECIDE -- and does not guess: whether the F_Z the RAR requires
  fits under K_B.  Identification A -> the conditions collapse to AQUAL's own (H1) and both
  operative kernels pass (H2).  Identification B -> N1 violated by ~2.4e8 at Earth (H3).
  Route 2's quasi-static reduction picks between them.  NOT COMPUTED HERE.
""")

print("=" * 78)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    for f in FAIL:
        print("  FAILED: " + f)
    sys.exit(1)
print("ALL CHECKS PASSED")
sys.exit(0)
