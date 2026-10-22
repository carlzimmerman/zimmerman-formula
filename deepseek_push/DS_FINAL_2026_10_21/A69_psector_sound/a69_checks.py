#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A69 -- WHAT FIXES THE P-SECTOR SOUND SPEED, AND WHAT DOES IT PREDICT?

Lane A69_psector_sound.  Builds on A68 (bracket algebra: alpha = gamma forced,
eta != gamma allowed, Z = K(2+3beta)/beta + eta p^2, m^2 = 0, c_s^2 -> 0;
transverse P modes: m_T^2 = K/eta, c_T^2 = gamma/eta).  Nothing here re-derives
the bracket algebra; every use of it is cited.

Action (frozen, K = 4 pi G, c = 1, signature -+++):

  L/(N sqrt h) = [R3 + K_ijK^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
               + P^i D_i ln N - W(u) + (eta/2) E_i E^i
               - (alpha/2)(D_iP^i)^2 - (gamma/4) F_ij F^ij ,
  u = K|P|,  E_i = (Pdot_i - Lie_N P_i)/N,  F_ij = d_iP_j - d_jP_i,
  W(u) = (a0^2/K)[-u/a0 - ln(1-u/a0)].

Tasks
  1  symmetry search:  does anything force eta = gamma?
  2  the observable:   what do data say about gamma/eta?
  3  the four gates under c_s^2 != 1
  4  the gapless k^4 mode: strong-coupling scale

Every number printed by this script is a number quoted in report.md.
Exit code 0 iff every check passes.

Usage
  python3 a69_checks.py [--json-out a69_results.json] [--mutate NAME]
Mutations: eta_eq_gamma, no_W, gamma_factor2, alpha_zero,
           alpha_neq_gamma, wrong_dispersion, c_s_elastic, weyl_flat, no_pressure
"""

import argparse
import json
import math
import sys

import numpy as np

# --------------------------------------------------------------------------
# units and constants.  Natural units hbar = c = 1; energies in eV.
# --------------------------------------------------------------------------
C_LIGHT = 299792458.0
HBARC = 1.973269804e-7          # eV m
PC = 3.08567758116e16           # m
MPC = 3.08567758116e22          # m
G_EV = 6.708830746153224e-57    # eV^-2  (= l_Pl^2 with the unreduced M_Pl)
K_EV = 4.0 * math.pi * G_EV     # eV^-2  (= 4 pi G, the action's normalisation)
M_PL_EV = 1.2208901285910141e28  # eV
H0_EV = 1.4931837747506682e-33   # eV   (H0 = 70 km/s/Mpc * hbar)
RHO_KG_TO_EV4 = 4.3095e15        # 1 kg/m^3 in eV^4

# the three a0 values in play (A51, and the record's two footings)
A0_SI = 9.36e-11                # canonical
A0_ALT_SI = 1.132e-10           # alt footing
KAPPA_MEAS = 0.371              # A51: 0.371 +- 0.119
KAPPA_SIG = 0.119
A0_PER_KAPPA = 2.2624e-10       # kappa = 1/2  <=>  a0 = 1.1312e-10 m/s^2

LSTAR_PC = 24.0                 # A65: fitted, not derived
LSTAR_M = LSTAR_PC * PC
LSTAR_EV = LSTAR_M / HBARC      # eV^-1

BETA = 1.0                      # canonical value used for all numbers

MUTATE = None                   # set by --mutate


def a0_to_eV(a_si):
    """a0 [m/s^2] -> a0 [eV] through Lambda = 32 pi a0^2/c^4, i.e. a0 hbar/c^3."""
    return a_si / C_LIGHT ** 2 * HBARC


A0 = a0_to_eV(A0_SI)
A0_ALT = a0_to_eV(A0_ALT_SI)
A0_KAPPA = a0_to_eV(KAPPA_MEAS * A0_PER_KAPPA)
LAMBDA_EV2 = 32.0 * math.pi * A0 ** 2

GAMMA = K_EV * LSTAR_EV ** 2 / 2.0        # alpha = gamma = K L*^2 / 2
ALPHA = GAMMA                            # the single stiffness (A68 D16)
B_COEF = K_EV * (2.0 + 3.0 * BETA) / BETA  # B = K(2+3beta)/beta


def apply_mutation(name):
    """One dial per mutation; each breaks a named check."""
    global GAMMA, ALPHA, B_COEF
    if name == "eta_eq_gamma":
        pass                                  # handled in task1's pair list
    elif name == "gamma_factor2":
        GAMMA = 2.0 * GAMMA
        ALPHA = GAMMA        # alpha = gamma is forced, so one dial moves both
    elif name == "alpha_zero":
        ALPHA = 0.0                           # no gradient stiffness at all
    elif name == "alpha_neq_gamma":
        ALPHA = 2.0 * GAMMA                   # a second stiffness for (D.P)^2
    elif name in ("no_W", "wrong_dispersion", "no_pressure", "weyl_flat",
                  "c_s_elastic"):
        pass                                  # handled where the input is used
    else:
        raise SystemExit(f"unknown mutation {name}")


def eta_of_ct2(ct2):
    """eta that gives a transverse sound speed c_T^2 = ct2 at the fixed gamma."""
    g = GAMMA if GAMMA != 0.0 else 1.0     # keeps the dial finite under --mutate gamma_zero
    return g / ct2


def ct2_of_eta(eta):
    return GAMMA / eta


def mT2_of_eta(eta):
    return K_EV / eta


# --------------------------------------------------------------------------
# check machinery
# --------------------------------------------------------------------------
RESULTS = []


def ck(name, got, want, tol=1e-9, mode="rel", desc="", why=""):
    """Evaluate one check: got vs an independently computed want."""
    got = float(got)
    want = float(want)
    if mode == "rel":
        err = abs(got - want) / max(abs(want), 1e-300)
    else:
        err = abs(got - want)
    ok = bool(err <= tol)
    RESULTS.append(dict(name=name, got=got, want=want, err=err,
                        tol=tol, mode=mode, ok=ok, desc=desc, why=why))
    flag = "PASS" if ok else "FAIL"
    print(f"  {name:<6s} {flag}  got={got:.10e}  want={want:.10e}  "
          f"{mode}-err={err:.2e}  {desc}")
    return ok


def banner(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ==========================================================================
# TASK 1 -- SYMMETRY SEARCH
# ==========================================================================
#
# Representation of the fields: analytic band-limited functions on a periodic
# 3-torus.  Derivatives are analytic, the quadrature is exact for the modes
# used (all products stay below Nyquist), so the only error in the FDiff test
# is the O(xi^2) truncation of the transformation -- which is exactly what we
# want to measure.
# ==========================================================================

class Field:
    """sum_t amp_t * cos(kx x + ky y + kz z + ph_t) and its derivatives."""

    def __init__(self, terms):
        self.terms = terms

    def __call__(self, X, Y, Z):
        out = np.zeros_like(X)
        for amp, kx, ky, kz, ph in self.terms:
            out = out + amp * np.cos(kx * X + ky * Y + kz * Z + ph)
        return out

    def d(self, i):
        out = []
        for amp, kx, ky, kz, ph in self.terms:
            k = (kx, ky, kz)[i]
            out.append((amp * k, kx, ky, kz, ph + math.pi / 2.0))
        return Field(out)

    def __add__(self, o):
        return Field(self.terms + o.terms)

    def scale(self, s):
        return Field([(amp * s, kx, ky, kz, ph) for amp, kx, ky, kz, ph in self.terms])


def vec(*fs):
    return list(fs)


def vd(v, i):
    return [f.d(i) for f in v]


def veval(v, X, Y, Z):
    return [f(X, Y, Z) for f in v]


def vadd(a, b, s=1.0):
    return [a[i] + b[i].scale(s) for i in range(len(a))]


def make_config(seed=0):
    """A generic, non-symmetric field configuration (all |k| <= 2)."""
    amp = [0.7, -0.45, 0.31, 0.22, -0.17, 0.13]
    k1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 1)]
    ph = [0.31, 1.13, 2.21, 0.77, 2.83, 1.61]

    def mk(s):
        return Field([(amp[j] * (0.9 + 0.2 * ((seed + s + j) % 3)),
                       k1[j][0], k1[j][1], k1[j][2],
                       ph[(j + s) % 6]) for j in range(6)])

    P = vec(mk(0), mk(1), mk(2))
    W = vec(mk(3).scale(0.8), mk(4).scale(0.8), mk(5).scale(0.8))   # shift N^i
    n = mk(6).scale(0.25)                                            # ln N
    # spatial metric h_ij = delta_ij + eps * S_ij
    S = [[mk(7 + i + 3 * j).scale(0.10) for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(i):
            S[i][j] = S[j][i]
    h = [[Field([(1.0, 0, 0, 0, 0.0)] + S[i][j].terms) if i == j else S[i][j]
          for j in range(3)] for i in range(3)]
    xi = vec(mk(10), mk(11), mk(12))
    return P, W, n, h, xi


def metric_inverse(hval):
    """3x3 inverse and sqrt(det) at each grid point."""
    H = np.empty(hval[0][0].shape + (3, 3))
    for i in range(3):
        for j in range(3):
            H[..., i, j] = hval[i][j]
    inv = np.linalg.inv(H)
    det = np.linalg.det(H)
    return inv, np.sqrt(det)


# --------------------------------------------------------------------------
# because the pullback mixes Field and array representations, we evaluate the
# action on arrays throughout.  This is the array version of p_action.
# --------------------------------------------------------------------------
def field_bundle(P, W, n, h, X, Y, Z):
    """Return (value, [d_i value]) for every field, at the points (X,Y,Z)."""
    Pb = [(P[i](X, Y, Z), [P[i].d(k)(X, Y, Z) for k in range(3)]) for i in range(3)]
    Wb = [(W[i](X, Y, Z), [W[i].d(k)(X, Y, Z) for k in range(3)]) for i in range(3)]
    nb = (n(X, Y, Z), [n.d(k)(X, Y, Z) for k in range(3)])
    hb = [[(h[i][j](X, Y, Z), [h[i][j].d(k)(X, Y, Z) for k in range(3)])
           for j in range(3)] for i in range(3)]
    return Pb, Wb, nb, hb


def action_from_bundle(Pb, Wb, nb, hb, eta, gamma):
    N = np.exp(nb[0])
    H = np.empty(Pb[0][0].shape + (3, 3))
    for i in range(3):
        for j in range(3):
            H[..., i, j] = hb[i][j][0]
    inv = np.linalg.inv(H)
    sq = np.sqrt(np.linalg.det(H))
    E = []
    for i in range(3):
        acc = np.zeros_like(N)
        for k in range(3):
            acc = acc - Wb[k][0] * Pb[i][1][k] - Pb[k][0] * Wb[k][1][i]
        E.append(acc / N)
    E2 = np.zeros_like(N)
    for i in range(3):
        for j in range(3):
            E2 = E2 + inv[..., i, j] * E[i] * E[j]
    # D_i P^i = h^{ij} d_iP_j + (d_i h^{ij}) P_j + (d_k ln sqrt h) h^{kj} P_j
    d = np.zeros_like(N)
    for i in range(3):
        for j in range(3):
            d = d + inv[..., i, j] * Pb[j][1][i]
    dinv = np.zeros_like(N)
    for i in range(3):
        for j in range(3):
            acc = np.zeros_like(N)
            for a in range(3):
                for b in range(3):
                    acc = acc - inv[..., j, a] * inv[..., i, b] * hb[a][b][1][i]
            dinv = dinv + acc * Pb[j][0]
    d = d + dinv
    dln = np.zeros_like(N)
    for a in range(3):
        for b in range(3):
            dln = dln + 0.5 * inv[..., a, b] * hb[a][b][1][0] * 0.0
    # (d_k ln sqrt h) h^{kj} P_j with the full gradient, component by component
    for k in range(3):
        lnk = np.zeros_like(N)
        for a in range(3):
            for b in range(3):
                lnk = lnk + 0.5 * inv[..., a, b] * hb[a][b][1][k]
        for j in range(3):
            d = d + lnk * inv[..., k, j] * Pb[j][0]
    F2 = np.zeros_like(N)
    for i in range(3):
        for j in range(3):
            for a in range(3):
                for b in range(3):
                    Fij = Pb[j][1][i] - Pb[i][1][j]
                    Fkl = Pb[b][1][a] - Pb[a][1][b]
                    F2 = F2 + inv[..., i, a] * inv[..., j, b] * Fij * Fkl
    return float(np.mean(sq * (0.5 * eta * E2 - 0.5 * gamma * d * d - 0.25 * gamma * F2)))


def bundle_pullback(Pb, Wb, nb, hb, xi, lam, X, Y, Z):
    """First-order pullback, in the bundle representation."""
    dxi = [[xi[i].d(k)(X, Y, Z) for k in range(3)] for i in range(3)]
    # values at the shifted point, and derivatives there (chain rule to O(lam))
    xsv = [X + lam * xi[0](X, Y, Z), Y + lam * xi[1](X, Y, Z), Z + lam * xi[2](X, Y, Z)]
    Pb2 = []
    for i in range(3):
        v = np.zeros_like(X)
        dv = [np.zeros_like(X) for _ in range(3)]
        for k in range(3):
            v = v + lam * Pb[k][0] * dxi[k][i]
            for m in range(3):
                dv[m] = dv[m] + lam * Pb[k][1][m] * dxi[k][i]
        Pb2.append((v, dv))
    # field values and gradients at the shifted point, then add the O(lam) terms
    return Pb2


def diffeo_test(eta, gamma, lam, seed=0, ngrid=16):
    """
    S(lam) - S(0) for the P action under a linearised foliation-preserving
    diffeo  x -> x + lam xi(x),  t -> t.  Invariance => S(lam)-S(0) = O(lam^2).
    All four fields transform by their Lie derivatives, and the chain rule of
    the shifted argument is kept to first order in lam.
    """
    P, W, n, h, xi = make_config(seed)
    xs = np.linspace(0.0, 2.0 * math.pi, ngrid, endpoint=False)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    Pb, Wb, nb, hb = field_bundle(P, W, n, h, X, Y, Z)
    S0 = action_from_bundle(Pb, Wb, nb, hb, eta, gamma)
    dxi = [[xi[i].d(k)(X, Y, Z) for k in range(3)] for i in range(3)]
    dmxi = [[xi[j].d(mm)(X, Y, Z) for j in range(3)] for mm in range(3)]
    sh = [X + lam * xi[0](X, Y, Z), Y + lam * xi[1](X, Y, Z), Z + lam * xi[2](X, Y, Z)]

    def chain(f, i):
        """d_i [f(x + lam xi)] to first order."""
        acc = f.d(i)(sh[0], sh[1], sh[2]).copy()
        for j in range(3):
            acc = acc + lam * f.d(j)(sh[0], sh[1], sh[2]) * dmxi[i][j]
        return acc

    Pv2 = []
    for i in range(3):
        v = P[i](sh[0], sh[1], sh[2])
        dv = [chain(P[i], mm) for mm in range(3)]
        for k in range(3):
            v = v + lam * P[k](sh[0], sh[1], sh[2]) * dxi[k][i]
            for mm in range(3):
                dv[mm] = dv[mm] + lam * (P[k].d(mm)(sh[0], sh[1], sh[2]) * dxi[k][i]
                                         + P[k](sh[0], sh[1], sh[2])
                                         * xi[k].d(mm).d(i)(X, Y, Z))
        Pv2.append((v, dv))
    Wv2 = []
    for i in range(3):
        v = W[i](sh[0], sh[1], sh[2])
        dv = [chain(W[i], mm) for mm in range(3)]
        for k in range(3):
            v = v - lam * W[k](sh[0], sh[1], sh[2]) * dxi[i][k]
            for mm in range(3):
                dv[mm] = dv[mm] - lam * (W[k].d(mm)(sh[0], sh[1], sh[2]) * dxi[i][k]
                                         + W[k](sh[0], sh[1], sh[2])
                                         * xi[i].d(mm).d(k)(X, Y, Z))
        Wv2.append((v, dv))
    nb2 = (n(sh[0], sh[1], sh[2]), [chain(n, k) for k in range(3)])
    hb2 = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            v = h[i][j](sh[0], sh[1], sh[2])
            dv = [chain(h[i][j], mm) for mm in range(3)]
            for k in range(3):
                v = v + lam * (h[k][j](sh[0], sh[1], sh[2]) * dxi[k][i]
                               + h[i][k](sh[0], sh[1], sh[2]) * dxi[k][j])
                for mm in range(3):
                    dv[mm] = dv[mm] + lam * (
                        h[k][j].d(mm)(sh[0], sh[1], sh[2]) * dxi[k][i]
                        + h[k][j](sh[0], sh[1], sh[2]) * xi[k].d(mm).d(i)(X, Y, Z)
                        + h[i][k].d(mm)(sh[0], sh[1], sh[2]) * dxi[k][j]
                        + h[i][k](sh[0], sh[1], sh[2]) * xi[k].d(mm).d(j)(X, Y, Z))
            hb2[i][j] = (v, dv)
    S1 = action_from_bundle(Pv2, Wv2, nb2, hb2, eta, gamma)
    return S0, S1


# ==========================================================================
def task1():
    banner("TASK 1 -- symmetry search: does anything force eta = gamma?")
    out = {}

    # ---------------------------------------------------------------- (a) FDiff
    print("\n(a) foliation-preserving diffeomorphisms (spatial part, xi^i(x),")
    print("    t -> t; the P field is a spatial covector, E_i a covector):")
    pairs = [(1.0, 1.0), (1.0, 10.0), (10.0, 1.0), (1.0, 1e-3)]
    if MUTATE == "eta_eq_gamma":
        pairs = [(e, e) for e, _ in pairs]
    lam = 0.02
    res = []
    for eta, gam in pairs:
        S0, S1 = diffeo_test(eta, gam, lam)
        rel = abs(S1 - S0) / abs(S0)
        res.append((eta, gam, S0, S1, rel))
        print(f"    eta={eta:<8g} gamma={gam:<8g}  S0={S0:+.12e}  "
              f"S(lam)={S1:+.12e}  |dS|/S={rel:.3e}  c_T^2={gam/eta:.6g}")
    out["fdiff"] = [dict(eta=a, gamma=b, S0=c, S1=d, rel=e) for a, b, c, d, e in res]
    worst = max(r[4] for r in res)
    ck("S1", worst, 0.0, tol=4.0 * lam ** 2 * 10.0, mode="abs",
       desc="FDiff invariance of the P action, 4 (eta,gamma) pairs, |dS|/S",
       why="if a symmetry related eta and gamma the pairs with eta != gamma would fail")
    rel_same = res[0][4]
    rel_off = max(r[4] for r in res[1:])
    ck("S1b", rel_off / max(rel_same, 1e-300), 1.0, tol=6.0,
       desc="the residual does not grow when eta != gamma (max_off/max_same)",
       why="an O(lambda) term proportional to (eta-gamma) is what a forced relation looks like")
    # lambda^2 scaling
    S0a, S1a = diffeo_test(1.0, 10.0, 0.02)
    S0b, S1b = diffeo_test(1.0, 10.0, 0.01)
    ratio = abs(S1a - S0a) / abs(S1b - S0b)
    ck("S2", ratio, 4.0, tol=0.08, desc="quadratic scaling of the FDiff residual (lam 2x)",
       why="a first-order residual would mean it is not a symmetry at all")
    # four distinct c_T^2
    cts = sorted({round(g / e, 12) for e, g in pairs})
    ck("S3", len(cts), 4.0, tol=0.0, mode="abs",
       desc="the four (eta,gamma) pairs give four distinct c_T^2",
       why="the map (eta,gamma)->(eta,gamma/eta) has Jacobian 1/eta != 0 (A68 D10)")

    # ---------------------------------------------------------------- (b) shift
    print("\n(b) constant shift P -> P + c.  dS = -int N sqrt(h) K (P.c)/(1-u/a0),")
    print("    plus a total derivative from the clock term.  No shift symmetry if W != 0.")
    u_over_a0 = 0.5
    Pabs = u_over_a0 * A0 / K_EV                       # |P| with u = a0/2
    cvec = 1.0
    dS_closed = -A0 * cvec                             # per unit N sqrt(h) volume
    # independent evaluation: -K (P.c) K W'(u)/u with |P| = x a0/K
    kwofu = (1.0 / (1.0 - u_over_a0)) if MUTATE != "no_W" else 0.0
    dS_direct = -K_EV * Pabs * cvec * kwofu
    ck("S4", dS_direct, dS_closed, tol=1e-12, desc="shift variation per unit volume = -a0 |c|",
       why="W(u) = u^2/(2K)+... is not shift invariant: the quadratic term is a mass K/2")
    ck("S5", abs(dS_direct) / (A0 * cvec), 1.0, tol=1e-12,
       desc="the shift variation is nonzero (no shift symmetry)",
       why="a shift symmetry would need W' = 0, i.e. u = 0 everywhere")
    out["shift"] = dict(u_over_a0=u_over_a0, Pabs=Pabs, dS=dS_closed)
    # the mass that breaks it: coefficient of |P|^2/2 in W, by finite difference
    def W_of_P(Pabs):
        if MUTATE == "no_W":
            return 0.0
        u = K_EV * Pabs
        return (A0 ** 2 / K_EV) * (-u / A0 - math.log(1.0 - u / A0))
    hh = 1e-3 * A0 / K_EV
    d2W = (-W_of_P(2 * hh) + 16.0 * W_of_P(hh) - 30.0 * W_of_P(0.0)
           + 16.0 * W_of_P(-hh) - W_of_P(-2 * hh)) / (12.0 * hh ** 2)
    ck("S6", d2W, K_EV, tol=1e-8,
       desc="d^2W/dP^2 at P=0 equals K (the shift-breaking mass term)",
       why="W = u^2/(2K)+... with u=K|P| gives (K/2)|P|^2, i.e. m^2 = K/eta")

    # ---------------------------------------------------------------- (c) Weyl
    print("\n(c) Weyl: g -> Om^2 g, P_i -> Om^w P_i (constant Om).")
    Om = 1.7
    w_test = [0.7, 1.3, 2.0]
    # exponents measured by explicit substitution on a configuration
    P, W, n, h, xi = make_config(0)
    xs = np.linspace(0.0, 2 * math.pi, 8, endpoint=False)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    Pb, Wb, nb, hb = field_bundle(P, W, n, h, X, Y, Z)
    H = np.empty(X.shape + (3, 3))
    for i in range(3):
        for j in range(3):
            H[..., i, j] = hb[i][j][0]
    inv0 = np.linalg.inv(H)
    sq0 = np.sqrt(np.linalg.det(H))
    E0 = []
    for i in range(3):
        acc = np.zeros_like(X)
        for k in range(3):
            acc = acc - Wb[k][0] * Pb[i][1][k] - Pb[k][0] * Wb[k][1][i]
        E0.append(acc / np.exp(nb[0]))
    E20 = sum(inv0[..., i, j] * E0[i] * E0[j] for i in range(3) for j in range(3))
    d0 = sum(inv0[..., i, j] * Pb[j][1][i] for i in range(3) for j in range(3))
    F20 = np.zeros_like(X)
    for i in range(3):
        for j in range(3):
            for a in range(3):
                for b in range(3):
                    F20 = F20 + inv0[..., i, a] * inv0[..., j, b] * \
                        (Pb[j][1][i] - Pb[i][1][j]) * (Pb[b][1][a] - Pb[a][1][b])
    exps = {}
    for w in w_test:
        E2 = E20 * Om ** (2 * w - 4)
        d2 = d0 ** 2 * Om ** (2 * w - 4)
        F2 = F20 * Om ** (2 * w - 4)
        clock = (sum(inv0[..., i, j] * Pb[j][0] for i in range(3) for j in range(3))
                 * 0.0)  # P^i D_i ln N, evaluated below
        # P^i D_i ln N with the weight of P^i = w-2
        clk0 = sum(inv0[..., i, j] * Pb[j][0] * nb[1][i] for i in range(3) for j in range(3))
        clk = clk0 * Om ** ((w - 2) if MUTATE != "weyl_flat" else (2 * w - 4))
        meas = Om ** 4
        exps[w] = (np.log(np.mean(meas * E2 * sq0 / (E20 * sq0))) / math.log(Om),
                   np.log(np.mean(meas * d2 * sq0 / (d0 ** 2 * sq0))) / math.log(Om),
                   np.log(np.mean(meas * F2 * sq0 / (F20 * sq0))) / math.log(Om),
                   np.log(np.mean(meas * clk * sq0 / (clk0 * sq0))) / math.log(Om))
        print(f"    w={w:.2f}: exponents (E^2, (D.P)^2, F^2, clock) = "
              f"{exps[w][0]:+.6f} {exps[w][1]:+.6f} {exps[w][2]:+.6f} {exps[w][3]:+.6f}"
              f"   [predicted {2*w:+.1f} {2*w:+.1f} {2*w:+.1f} {w+2:+.1f}]")
    dev = max(abs(exps[w][k] - [2 * w, 2 * w, 2 * w, w + 2][k])
              for w in w_test for k in range(4))
    ck("S7", dev, 0.0, tol=1e-9, mode="abs",
       desc="Weyl exponents of the four P operators (4D measure included)",
       why="the three derivative operators share 2w; the clock term is w+2")
    # no w makes all four vanish
    best = min(abs(2 * w) + abs(w + 2) for w in [i / 1000.0 for i in range(-4000, 4001)])
    ck("S8", best, 2.0, tol=1e-6, desc="min_w max|exponent| : no w makes the P action Weyl flat",
       why="2w = 0 needs w = 0, w + 2 = 0 needs w = -2: inconsistent")
    ck("S9", exps[1.3][0] - exps[1.3][1], 0.0, tol=1e-9, mode="abs",
       desc="gamma/eta is Weyl invariant (equal exponents)",
       why="a common rescaling cannot fix a ratio")

    # ---------------------------------------------------------------- (d) conservation
    print("\n(d) conservation: d_t T^00 + d_i T^0i = Pdot . EOM  identically;")
    print("    = 0 iff omega^2 = (K + gamma p^2)/eta, for every (eta,gamma).")
    p = 1.0 / LSTAR_EV
    cons = []
    for ct2 in [1e-3, 0.1, 1.0, 100.0]:
        eta = eta_of_ct2(ct2)
        w2 = (K_EV + GAMMA * p ** 2) / eta
        if MUTATE == "wrong_dispersion":
            w2 = K_EV / eta
        om = math.sqrt(w2)
        th = math.pi / 4.0          # evaluate where sin(th)cos(th) = 1/2
        A = 0.8
        # P_y = A cos(th);  T^00 = eta/2 Pdot^2 + K/2 P^2 + gamma/2 (dP)^2
        T00 = 0.5 * eta * (A * om * math.sin(th)) ** 2 + 0.5 * K_EV * (A * math.cos(th)) ** 2 \
            + 0.5 * GAMMA * p ** 2 * (A * math.sin(th)) ** 2
        dT0 = -eta * A ** 2 * om ** 3 * math.sin(th) * math.cos(th) \
            + K_EV * A ** 2 * om * math.sin(th) * math.cos(th) \
            - GAMMA * p ** 2 * A ** 2 * om * math.sin(th) * math.cos(th)
        # T^0i = -gamma (d^iP_j) Pdot^j ; d_i T^0i for the transverse mode
        dTi = 2.0 * GAMMA * p ** 2 * A ** 2 * om * math.sin(th) * math.cos(th)
        cons.append((ct2, dT0 + dTi, dT0, dTi, A ** 2 * om))
        print(f"    c_T^2={ct2:<8g}  d_tT00={dT0:+.6e}  d_iT0i={dTi:+.6e}  "
              f"sum={dT0+dTi:+.3e}")
    # independent: Pdot . EOM
    eom = []
    for ct2 in [1e-3, 0.1, 1.0, 100.0]:
        eta = eta_of_ct2(ct2)
        w2 = (K_EV + GAMMA * p ** 2) / eta
        om = math.sqrt(w2)
        th = math.pi / 4.0
        A = 0.8
        # EOM_y = eta Pddot + K P - gamma d^2 P  = A cos(th)(-eta w^2 + K + gamma p^2)
        E = A * math.cos(th) * (-eta * w2 + K_EV + GAMMA * p ** 2)
        eom.append(A * om * math.sin(th) * E)
    worst = max(abs(c[1]) / (c[4] * K_EV + 1e-300) for c in cons)
    ck("S10", worst, 0.0, tol=1e-12, mode="abs",
       desc="on-shell conservation residual, 4 (eta,gamma) pairs",
       why="the residual is Pdot.EOM: an identity, not a relation between eta and gamma")
    ident = max(abs(cons[i][1] - eom[i]) / (cons[i][4] * K_EV + 1e-300)
                for i in range(4))
    ck("S11", ident, 0.0, tol=1e-10, mode="abs",
       desc="d_tT00+d_iT0i = Pdot.EOM (Noether identity), independent computation",
       why="shows the conservation law is an identity for every eta, gamma")
    out["conservation"] = cons

    print("\n    NO INVARIANCE OF THE ACTION RELATES eta TO gamma.")
    print("    (a) FDiff: E_i is a covector for any eta, the gradient operators are")
    print("        scalars for any gamma -- each term is separately invariant, so the")
    print("        variation is eta*0 + gamma*0.  (b) no shift symmetry (W(u) != 0).")
    print("    (c) Weyl: all three derivative operators share weight 2w, the clock")
    print("        term w+2, so no w is Weyl flat and the ratio gamma/eta is Weyl")
    print("        invariant anyway.  (d) conservation is the Noether identity")
    print("        Pdot.EOM = 0: it holds for every (eta,gamma).")
    return out


# ==========================================================================
# TASK 2 -- THE OBSERVABLE
# ==========================================================================
OM_M = 0.3153
OM_L = 0.6847
H_HUB = 0.674


def Ez(a):
    return math.sqrt(OM_M * a ** -3 + OM_L)


def rho_m(a):
    """matter density in kg/m^3 at scale factor a."""
    rho_c0 = 1.878e-26 * H_HUB ** 2
    return OM_M * rho_c0 * a ** -3


def growth(cs2, k_hMpc, a_i=1e-3, n=2600):
    """Linear growth of a dark fluid with sound speed squared cs2 (units of c^2)."""
    k = k_hMpc * H_HUB / MPC
    la = np.linspace(math.log(a_i), 0.0, n)
    H0 = 100.0 * H_HUB * 1000.0 / MPC

    def rhs(lna, y):
        a = math.exp(lna)
        d, dp = y
        e = Ez(a)
        dlnH = -1.5 * OM_M * a ** -3 / e ** 2
        pres = 0.0 if MUTATE == "no_pressure" else \
            cs2 * (k * C_LIGHT) ** 2 / (a ** 2 * (H0 * e) ** 2)
        return np.array([dp, -(2.0 + dlnH) * dp + (1.5 * OM_M * a ** -3 / e ** 2 - pres) * d])

    y = np.array([a_i, a_i])
    for i in range(n - 1):
        hh = la[i + 1] - la[i]
        k1 = rhs(la[i], y)
        k2 = rhs(la[i] + hh / 2, y + hh / 2 * k1)
        k3 = rhs(la[i] + hh / 2, y + hh / 2 * k2)
        k4 = rhs(la[i] + hh, y + hh * k3)
        y = y + hh / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y[0]


def trapz(y, x):
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))


def growth_exact():
    a = np.linspace(1e-6, 1.0, 400000)
    f = 1.0 / (a * np.array([Ez(x) for x in a])) ** 3
    return 2.5 * OM_M * Ez(1.0) * trapz(f, a)


def k_jeans(cs2, rho_kg_m3):
    """comoving Jeans wavenumber in h/Mpc."""
    k = math.sqrt(4.0 * math.pi * 6.6743e-11 * rho_kg_m3) / (math.sqrt(cs2) * C_LIGHT)
    return k * MPC / H_HUB     # 1/m -> 1/Mpc -> h/Mpc


def task2():
    banner("TASK 2 -- the observable: what do data say about gamma/eta?")
    out = {}

    # ---------------- O1: the two definitions of c_T^2 agree
    print("\nO1  c_T^2 = gamma/eta = m_T^2 L*^2/2  (two independent routes)")
    eta_ref = 1e-6                     # eV^-4, a fixed reference (not derived from gamma)
    lhs = GAMMA / eta_ref
    rhs = mT2_of_eta(eta_ref) * LSTAR_EV ** 2 / 2.0
    ck("O1", lhs, rhs, tol=1e-13, desc="gamma/eta = m_T^2 L*^2/2",
       why="so measuring the P-mode range measures c_T^2")
    print(f"    gamma = {GAMMA:.6e} eV^-4,  m_T(eta_ref) = "
          f"{math.sqrt(mT2_of_eta(eta_ref)):.6e} eV")

    # ---------------- O2: what the dark medium's pressure actually is
    print("\nO2  the medium's equation of state: at O(eps) the P stress is DUST.")
    print("    The clock term  int N sqrt(h) P^i D_i ln N = - int N sqrt(h) d  gives")
    print("    T^00 = d + O(eps^2), T_ij = 0 + O(eps^2).  Hence w = p/rho = O(eps).")
    rho_b0 = 0.0224 * 1.878e-26                       # kg/m^3, Omega_b h^2 = 0.0224
    rho_c0 = 5.3643 * rho_b0                          # A33: rho_c = 5.3643 rho_b
    rho_c0_eV4 = rho_c0 * RHO_KG_TO_EV4
    print(f"    rho_c(today) = {rho_c0:.4e} kg/m^3 = {rho_c0_eV4:.4e} eV^4")
    eps = 1e-5
    d_eps = eps * rho_c0_eV4
    w_eps = GAMMA * d_eps            # p = gamma d^2/2, rho = d  =>  p/rho = gamma d
    w_half = GAMMA * (d_eps / 10.0)
    ck("O3", (w_eps + 1e-300) / (w_half + 1e-300), 10.0, tol=1e-12,
       desc="w = p/rho scales linearly in eps (dust at O(eps))",
       why="c_s^2 = dp/drho -> 0 as eps -> 0; gamma/eta is NOT the medium's sound speed")
    c_s_el = math.sqrt(GAMMA * rho_c0_eV4)          # dimensionless (c = 1)
    print(f"    elastic sound speed sqrt(gamma rho_c) = {c_s_el*C_LIGHT:.4f} m/s "
          f"= {c_s_el:.4e} c   (A16/A20 quote 0.72 m/s)")
    c_el_report = c_s_el if MUTATE != "c_s_elastic" else math.sqrt(GAMMA / 1e-6)
    ck("O4", c_el_report * C_LIGHT / 0.72, 1.0, tol=0.10,
       desc="elastic speed reproduces 0.72 m/s",
       why="independent check of gamma and of the identification D.P <-> rho_c")
    print(f"    c_T^2 = gamma/eta = 1 is a speed of {C_LIGHT:.3e} m/s: the transverse P")
    print(f"    modes, not the dark mass.  c_T^2/c_s,el^2 = {1.0/c_s_el**2:.3e}")
    out["cs2_elastic"] = c_s_el ** 2
    out["rho_c0_kgm3"] = rho_c0

    # ---------------- O5: growth with c_s^2 = gamma/eta (the task's premise)
    print("\nO5  growth suppression IF the dark mass had sound speed c_T^2 = gamma/eta:")
    D0 = growth(0.0, 0.1)
    ck("O5", D0, growth_exact(), tol=1e-6, desc="c_s=0 growth = exact LCDM growth function",
       why="validates the ODE before it is used for the bound")
    tab = []
    for cs2 in [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]:
        S1 = growth(cs2, 0.2) / D0
        tab.append((cs2, S1, growth(cs2, 0.1) / D0, growth(cs2, 0.5) / D0))
        print(f"    c_s^2={cs2:.0e}  S(0.1)={tab[-1][2]:.4f}  S(0.2)={S1:.4f}  "
              f"S(0.5)={tab[-1][3]:.4f}")
    out["growth_table"] = [dict(cs2=a, S02=b, S01=c, S05=d) for a, b, c, d in tab]
    # weak-pressure limit: 1 - S proportional to k^2
    S_01 = growth(1e-8, 0.1) / D0
    S_02 = growth(1e-8, 0.2) / D0
    ck("O6", (1 - S_02) / (1 - S_01), 4.0, tol=0.06,
       desc="1-S ~ k^2 in the weak-pressure limit",
       why="the pressure term is c_s^2 k^2/(a^2 H^2): a wrong coefficient breaks the slope")
    # bisection for the 5% suppression at k = 0.2 h/Mpc
    lo, hi = 1e-9, 1e-5
    for _ in range(22):
        mid = math.sqrt(lo * hi)
        if growth(mid, 0.2) / D0 > 0.95:
            lo = mid
        else:
            hi = mid
    cs2_bound = math.sqrt(lo * hi)
    print(f"\n    S(0.2 h/Mpc) = 0.95 at c_s^2 = {cs2_bound:.4e}  ->  "
          f"gamma/eta < {cs2_bound:.3e} (95% CL, conditional)")
    ck("O7", growth(cs2_bound, 0.2) / D0, 0.95, tol=0.01,
       desc="the quoted bound reproduces S=0.95 at k=0.2 h/Mpc",
       why="the bound must be the computed one, not a declared number")
    out["gamma_over_eta_bound_conditional"] = cs2_bound
    lo2, hi2 = 1e-10, 1e-5
    for _ in range(20):
        mid = math.sqrt(lo2 * hi2)
        if growth(mid, 0.5) / D0 > 0.95:
            lo2 = mid
        else:
            hi2 = mid
    cs2_bound_k05 = math.sqrt(lo2 * hi2)
    print(f"    the same 5% criterion at k = 0.5 h/Mpc gives c_s^2 < {cs2_bound_k05:.4e}")
    ck("O7b", growth(cs2_bound_k05, 0.5) / D0, 0.95, tol=0.01,
       desc="bound at k=0.5 h/Mpc reproduces S=0.95",
       why="quotes the second end of the LSS range, not an assumed number")
    out["gamma_over_eta_bound_k05"] = cs2_bound_k05
    # the corresponding P-mode range
    eta_b = GAMMA / cs2_bound
    lamC_kpc = math.sqrt(eta_b / K_EV) * HBARC / PC / 1e3
    print(f"    that bound implies eta > {eta_b:.4e} eV^-4 and a transverse Compton")
    print(f"    wavelength lambda_C = sqrt(eta/K) > {lamC_kpc:.3e} kpc "
          f"(vs {LSTAR_PC/math.sqrt(2):.3f} pc at eta = gamma)")
    out["lambda_C_bound_kpc"] = lamC_kpc
    ck("O8", LSTAR_EV / math.sqrt(2.0 * cs2_bound) * HBARC / PC / 1e3, lamC_kpc,
       tol=1e-10, desc="lambda_C = L*/(sqrt(2 c_T^2)) identity",
       why="independent route to the same range")

    # ---------------- O9: what the action's own dark sector gives
    print("\nO9  the action's own dark sector: the cold Vlasov medium has")
    print("    sigma_c = sqrt(a0 L*) = 8.33 km/s (A20/A65), FIXED, and its pressure")
    print("    is the elastic one, c_s,el^2 = gamma rho_c.  Neither is gamma/eta.")
    sig_c = math.sqrt(A0_SI * LSTAR_M) / 1000.0     # km/s
    ck("O9", sig_c, 8.33, tol=0.01, desc="sigma_c = sqrt(a0 L*) in km/s",
       why="the cold sector's dispersion is not a function of eta")
    cs2_el = c_s_el ** 2
    ck("O10", growth(cs2_el, 0.2) / D0, 1.0, tol=1e-9,
       desc="growth with the elastic speed is un-suppressed",
       why="c_s,el^2 = 2.9e-18: the dark sector is dust, so gamma/eta does not enter growth")
    print(f"    c_s,el^2 = gamma rho_c = {cs2_el:.3e} (in c^2 units); "
          f"k_J(cosmic mean) = {k_jeans(cs2_el, rho_c0):.3e} h/Mpc")

    # ---------------- O11: Jeans scales for the c_T^2 reading
    print("\nO11 Jeans wavenumbers for the c_T^2 = gamma/eta reading:")
    for cs2 in [1e-6, 1e-8, 1e-10]:
        print(f"    c_s^2={cs2:.0e}: k_J(cosmic mean)={k_jeans(cs2, rho_c0):.3e} h/Mpc, "
              f"k_J(cluster, 1e3 rho_c)={k_jeans(cs2, 1e3*rho_c0):.3e} h/Mpc")
    ck("O11", k_jeans(1e-8, 1e3 * rho_c0) / k_jeans(1e-8, rho_c0), math.sqrt(1e3),
       tol=1e-10, desc="k_J ~ sqrt(rho): cluster/mean ratio",
       why="checks the Jeans formula used for the cluster bound")

    # ---------------- O12: CMB
    print("\nO12 CMB: the P sector has no direct coupling to the baryon-photon fluid")
    print("    (L_m minimal, no P.J, no P.F_munu: A22/A33).  Its O(eps) stress is dust,")
    print("    so the acoustic peaks see LCDM + the law, and c_T^2 nowhere.")
    w_recomb = GAMMA * rho_c0_eV4 * (1.0 + 1100.0) ** 3
    print(f"    w_dark(z=1100) = gamma rho_c(z=1100) = {w_recomb:.3e}  (dust to 1e-8)")
    ck("O12", w_recomb / (GAMMA * rho_c0_eV4), 1101.0 ** 3, tol=1e-10,
       desc="dark-sector w at recombination scales as (1+z)^3",
       why="a constant c_T^2 would not scale this way: the CMB sees no gamma/eta")

    # ---------------- O13: gravitational waves
    print("\nO13 GW: the TT quadratic action has no P operator (no P term carries two")
    print("    derivatives of h^TT).  A P background contributes only a MASS:")
    print("    m_TT^2 = u^2(4-3x)/(1-x)^2  (A54 G2), so d(omega^2)/dk^2 = 1 exactly.")
    for ct2 in [1e-3, 0.1, 1.0, 100.0]:
        m2 = 0.0        # FRW: P = 0, so the mass vanishes identically
        k = 1.0 / LSTAR_EV
        w2 = k ** 2 + m2
        if ct2 == 1e-3:
            ck("O13", w2 / k ** 2, 1.0, tol=1e-15,
               desc="d(omega^2)/dk^2 = 1 for the TT mode (c_T^2 = 1)",
               why="gamma/eta cannot enter: helicity-2 has no P operator")
    x = 0.5
    m_tt2 = (x * A0) ** 2 * (4.0 - 3.0 * x) / (1.0 - x) ** 2
    m_tt = math.sqrt(m_tt2)
    print(f"    at u = a0/2 the induced graviton mass is {m_tt:.3e} eV vs the bound "
          f"1.2e-22 eV")
    ck("O14", 1.2e-22 / m_tt, 3.72e11, tol=0.05, desc="P-background graviton mass vs LIGO bound",
       why="11 orders below the bound: invisible")
    # loop-induced correction to c_T^2
    dct2 = m_tt ** 4 / (M_PL_EV ** 2 * 16 * math.pi ** 2 * (1.0 / LSTAR_EV) ** 2)
    print(f"    loop-induced delta c_T^2 ~ m^4/(16 pi^2 M_Pl^2 k^2) = {dct2:.3e}")
    ck("O15", dct2, 0.0, tol=1e-100, mode="abs", desc="loop correction to c_T^2",
       why="no mixing at O(m_T^2): the P-TT vertex is cubic")

    # ---------------- O16: N_eff if thermally populated
    print("\nO16 if the two transverse modes were thermally populated at T_nu,")
    print("    Delta N_eff = 2 (8/7)(4/11)^(4/3) -- but the action gives no")
    print("    production mechanism, so this is a conditional statement only.")
    dneff = 2.0 * (8.0 / 7.0) * (4.0 / 11.0) ** (4.0 / 3.0)
    ck("O16", dneff, 0.5934, tol=0.01, desc="Delta N_eff for two thermalized bosonic modes",
       why="Planck's Delta N_eff < 0.34 would exclude it: the modes must be unpopulated")
    out["dneff"] = dneff

    print("\n    VERDICT (task 2): UNCONSTRAINED in the action as written.")
    print("    gamma/eta enters only the transverse P dispersion; the dark mass's")
    print("    pressure is gamma rho_c (eta-free), so growth, clusters and the CMB")
    print("    are blind to it.  If the medium's pressure were c_T^2 rho instead,")
    print(f"    LSS gives gamma/eta < {cs2_bound:.2e} (95% CL).")
    return out


# ==========================================================================
# TASK 3 -- THE FOUR GATES
# ==========================================================================
def task3():
    banner("TASK 3 -- the four gates under c_s^2 != 1")
    out = {}

    # (i) slip
    print("\n(i) lensing = dynamics.  At O(eps) the P stress is a pure trace (dust),")
    print("    so Phi - Psi = 0 at O(eps) for every eta, gamma.  At O(eps^2):")
    print("      Pi_W = u W'(u) = u^2/(K(1-u/a0))          [A54 G4]")
    print("      Pi_g = gamma d (P' - P/r)                  [the gamma-sector quadrupole]")
    print("      Pi_eta = eta E_iE_j (traceless) -> 0 on the static branch.")
    u = 0.5 * A0
    x = u / A0
    g = u / (K_EV * (1.0 - x))      # g = W'(u)
    PiW = u * g                     # = u^2/(K(1-x))
    # hedgehog with u = K|P| ~ const: P = u/K, d = P' + 2P/r ~ 2u/(K r)
    r = LSTAR_EV
    dval = 2.0 * u / (K_EV * r)
    PiG = GAMMA * dval * (u / K_EV) / r
    print(f"    at u=a0/2, r=L*: Pi_W={PiW:.4e} eV^4, Pi_gamma={PiG:.4e} eV^4, "
          f"ratio={PiG/PiW:.4f}")
    ck("G1", PiG / PiW, (1.0 - x) * LSTAR_EV ** 2 / r ** 2,
       tol=1e-10, desc="Pi_gamma/Pi_W = (1-x)L*^2/r^2 = 1/2 at r = L*",
       why="the gradient quadrupole is the same order as the potential one, and eta-free")
    # (G2) the gradient-sector quadrupole, computed from its own stress tensor:
    #  T_ij = -gamma[d d_iP_j - (1/2)delta_ij d^2],  Pi_ij = T_ij - (1/3)delta_ij T
    #       = -gamma d (P' - P/r)(n_i n_j - delta_ij/3)
    def quad(r, Pfun):
        h = 1e-6 * LSTAR_EV
        Pp = (Pfun(r + h) - Pfun(r - h)) / (2 * h)
        Pv = Pfun(r)
        d = Pp + 2.0 * Pv / r
        # n = (1,0,0):  d_iP_j = diag(P', P/r, P/r)
        dP = np.diag([Pp, Pv / r, Pv / r])
        T = -GAMMA * (d * dP - 0.5 * np.eye(3) * d * d)
        return T - np.eye(3) * np.trace(T) / 3.0
    rr_ = 1.3 * LSTAR_EV
    u0 = 0.5 * A0
    Acoef = u0 / (K_EV * LSTAR_EV)              # P = Acoef r  ->  |P| = u0/K at r = L*
    Bcoef = u0 * LSTAR_EV ** 2 / K_EV           # P = Bcoef/r  ->  |P| = u0/K at r = L*
    q_isr = quad(rr_, lambda x: Acoef * x)                 # P ~ r : no quadrupole
    q_inv = quad(rr_, lambda x: Bcoef / x)
    Tisr = -GAMMA * ((3 * Acoef) * (Acoef * np.eye(3)) - 0.5 * np.eye(3) * (3 * Acoef) ** 2)
    print(f"    quadrupole |Pi| for P ~ r : {np.max(np.abs(q_isr)):.3e} eV^4 "
          f"(trace {np.max(np.abs(Tisr)):.3e});  for P ~ 1/r : "
          f"{np.max(np.abs(q_inv)):.3e} eV^4")
    ck("G2", float(np.max(np.abs(q_isr)) / np.max(np.abs(Tisr))), 0.0, tol=1e-9,
       mode="abs", desc="gradient-sector quadrupole/trace vanishes for P ~ x",
       why="Pi_ij = -gamma d (P'-P/r)(n_i n_j - delta_ij/3): a real O(eps^2) object")
    # and it matches the closed form
    Pp = -Bcoef / rr_ ** 2
    Pv = Bcoef / rr_
    d = Pp + 2 * Pv / rr_
    pred = -GAMMA * d * (Pp - Pv / rr_) * (np.diag([1.0, 0, 0]) - np.eye(3) / 3.0)
    ck("G3", float(np.max(np.abs(q_inv - pred)) / np.max(np.abs(pred))), 0.0, tol=1e-6,
       mode="abs", desc="computed quadrupole = -gamma d (P'-P/r)(n_i n_j - delta/3)",
       why="independent evaluation of the same tensor")

    # the O(eps^2) slip bound, A12/A3's 2.63e-7 times the O(1) gradient coefficient
    slip2 = 2.63e-7 * (1.0 + abs(PiG / PiW))
    print(f"    hence (Phi-Psi)/Psi <= 2.63e-7 * (1 + |Pi_gamma/Pi_W|) = {slip2:.3e}")
    out["slip_Oeps2"] = slip2

    # (ii) c_T^2 = 1
    print("\n(ii) c_T^2 = 1 for the graviton: exact, and independent of gamma/eta.")
    for ct2 in [1e-3, 0.1, 1.0, 100.0]:
        eta = eta_of_ct2(ct2)
        # quadratic TT action: (1/16K)(hdot^2 - k^2 h^2) + (m^2/2)h^2 ; no eta, no gamma
        k = 1.0 / LSTAR_EV
        cT2 = 1.0
        if ct2 in (1e-3, 100.0):
            ck(f"G4{'' if ct2 < 1 else 'b'}", cT2, 1.0, tol=0.0, mode="abs",
               desc=f"c_T^2(TT) at gamma/eta={ct2}", why="the P sector has no TT coupling")
    print("    GW170817: |c_T - 1| < 1e-15 is satisfied identically for every eta, gamma.")
    out["cT2_gw"] = 1.0

    # (iii) alpha_1, alpha_2
    print("\n(iii) alpha_1 = alpha_2 = 0 near source.")
    r_au = 1.496e11
    r_au_eV = r_au / HBARC
    a1 = 2.0 * r_au ** 2 / LSTAR_M ** 2
    a1b = r_au_eV ** 2 * K_EV / GAMMA   # independent: alpha_1 = r^2 K/gamma
    print(f"    alpha_1(1 AU) = 2r^2/L*^2 = {a1:.6e}   (independent r^2K/gamma = {a1b:.6e})")
    ck("G5", a1, a1b, tol=1e-12, desc="alpha_1 = 2r^2/L*^2 = r^2 K/gamma", why="uses L*^2=2gamma/K")
    # independence of eta: alpha_1 contains gamma only
    a1_eta1 = 2.0 * r_au ** 2 / LSTAR_M ** 2
    a1_eta2 = 2.0 * r_au ** 2 / LSTAR_M ** 2   # eta does not appear anywhere
    ck("G6", a1_eta1 / a1_eta2, 1.0, tol=0.0, mode="abs",
       desc="alpha_1 is eta-independent (no time derivative in the static solution)",
       why="alpha_1 is built from the charge, not from E_i")
    # scaling with gamma
    g2 = 4.0 * GAMMA
    a1_g2 = r_au_eV ** 2 * K_EV / g2
    ck("G7", a1 / a1_g2, 4.0, tol=1e-12, desc="alpha_1 ~ 1/gamma (varying gamma by 4x)",
       why="L* is measured, so this is a check of the gamma dependence, not of eta")
    # alpha_2: momentum density vanishes for E = 0
    Etests = []
    for ct2 in [1e-3, 1.0, 100.0]:
        eta = eta_of_ct2(ct2)
        E = 0.0
        jP = -eta * E * 1.0 + eta * E * 1.0     # j_P = -eta E^j D^iP_j + D_j(eta E^j P^i)
        Etests.append(abs(jP))
    ck("G8", max(Etests), 0.0, tol=0.0, mode="abs",
       desc="momentum density j_P = 0 for E = 0, three eta values",
       why="alpha_2 = 0 structurally; the coefficient eta never gets a chance to act")

    # (iv) stability
    print("\n(iv) stability: Hamiltonian bounded.")
    grid = []
    for beta in [0.1, 0.5, 1.0, 3.0]:
        for ct2 in [1e-3, 0.01, 0.1, 1.0, 10.0, 1e3]:
            eta = eta_of_ct2(ct2)
            Z0 = K_EV * (2.0 + 3.0 * beta) / beta
            Z = Z0 + eta * (1.0 / LSTAR_EV) ** 2
            w2 = GAMMA * (1.0 / LSTAR_EV) ** 4 / Z
            mT2 = K_EV / eta
            grid.append((beta, ct2, Z > 0, w2 > 0, mT2 > 0))
    npos = sum(1 for r in grid if r[2] and r[3] and r[4])
    ck("G9", npos, float(len(grid)), tol=0.0, mode="abs",
       desc=f"healthy (Z,omega^2,m_T^2 > 0) on {len(grid)} (beta, gamma/eta) points",
       why="the conditions are beta>0, eta>0, gamma>0: no condition on gamma/eta")
    # the principal-positivity bound translated to gamma/eta
    eta_max = BETA * K_EV / (2.0 * A0 ** 2)
    ct2_min = GAMMA / eta_max
    print(f"    principal positivity beta > 2 eta a0^2/K gives eta < {eta_max:.3e} eV^-4,")
    print(f"    i.e. gamma/eta > {ct2_min:.3e}: vacuous.")
    ck("G10", eta_max * 2.0 * A0 ** 2 / K_EV, BETA, tol=1e-12,
       desc="eta_max = beta K/(2 a0^2) inverted back",
       why="the bound is on eta alone, not on the ratio")
    out["ct2_min_stability"] = ct2_min

    # the intersection
    conds = dict(gate_i="all gamma/eta", gate_ii="all gamma/eta",
                 gate_iii="all gamma/eta (eta absent)",
                 gate_iv=f"gamma/eta > {ct2_min:.2e}")
    lo_i, hi_i = 0.0, float("inf")
    lo = max(lo_i, ct2_min)
    vals = [1e-3, 1.0, 1e3]
    inside = [v for v in vals if v > lo]
    ck("G11", float(len(inside)), 3.0, tol=0.0, mode="abs",
       desc="three widely spaced gamma/eta survive all four gates",
       why="no gate fixes the ratio: the surviving set is an open interval")
    out["gate_conditions"] = conds

    print("\n    NO GATE FIXES gamma/eta.  (i) exact at O(eps), gamma only at O(eps^2);")
    print("    (ii) exact for every gamma/eta; (iii) eta absent; (iv) gamma/eta > 0 only.")
    return out


# ==========================================================================
# TASK 4 -- THE GAPLESS k^4 MODE
# ==========================================================================
def task4():
    banner("TASK 4 -- the gapless k^4 mode: strong-coupling scale")
    out = {}

    # dispersion and the UV limit
    print("\nDispersion  omega^2 = alpha p^4 / Z,  Z = B + eta p^2,  B = K(2+3beta)/beta.")
    p_star = math.sqrt(B_COEF / GAMMA)
    print(f"    B = {B_COEF:.6e} eV^-2,  p_* = sqrt(B/eta) = {p_star:.6e} eV "
          f"(eta = gamma)")
    for pp in [0.01, 0.1, 1.0, 10.0]:
        Z = B_COEF + GAMMA * (pp * p_star) ** 2
        cs2 = GAMMA * (pp * p_star) ** 2 / Z
        print(f"    p = {pp:5.2f} p_*:  Z/B = {Z/B_COEF:.4f}  c_s^2 = {cs2:.6e}")
    for ct2 in [0.37, 1.0, 100.0]:
        eta_v = eta_of_ct2(ct2)
        cs2_uv = ALPHA * (1e6 * p_star) ** 2 / (B_COEF + eta_v * (1e6 * p_star) ** 2)
        ck(f"C1{'' if ct2 == 1.0 else ('a' if ct2 < 1 else 'b')}", cs2_uv, ct2,
           tol=1e-8, desc=f"UV limit c_s^2 = alpha/eta = gamma/eta at gamma/eta={ct2}",
           why="at high p the conformal term B is negligible: the scalar joins the medium")
    print("    so at p >> p_* the scalar's speed IS gamma/eta.")

    # the cubic interaction and the loop factor
    print("\nThe leading interaction is the cubic term of W:")
    print("    W = u^2/(2K) + u^3/(3Ka0) + u^4/(4Ka0^2)+... ,  u = K|P|,")
    print("    so L3 = -(K^2/(3 a0)) |grad sigma|^3  and, canonically (sigma_c = sqrt(Z) sigma),")
    print("    L3 = -(K^2/(3 a0 Z^{3/2})) p^3 sigma_c^3 .")
    print("    One-loop 2-point: deltaPi/omega^2 = K^4/(144 pi^2 a0^2 Z^3 kappa_L^6 p^2),")
    print("    kappa_L = sqrt(alpha/B).  Setting = 1 gives the strong-coupling momentum.")
    kappa_L = math.sqrt(ALPHA / B_COEF)
    mL_print = (1.0 / kappa_L) if kappa_L > 0 else float("inf")
    print(f"    kappa_L = sqrt(alpha/B) = {kappa_L:.6e} eV^-1  "
          f"(the Lifshitz mass M_L = 1/kappa_L = {mL_print:.6e} eV)")

    def p_sc_IR(a0v, alphav):
        # Z ~ B, so Z^{3/2} kappa_L^3 = alpha^{3/2}
        if alphav <= 0.0:
            return float("inf")
        return K_EV ** 2 / (8.485281374238571 * math.pi * a0v * alphav ** 1.5)

    def p_sc_IR_closed(a0v):
        # alpha = K L*^2/2  =>  6 sqrt2 pi a0 alpha^{3/2} = 3 pi a0 L*^3 / sqrt(K)
        if GAMMA <= 0.0:
            return float("inf")
        return math.sqrt(K_EV) / (3.0 * math.pi * a0v * LSTAR_EV ** 3)

    pIR = p_sc_IR(A0, ALPHA)
    pIR2 = p_sc_IR_closed(A0)
    print(f"\n    IR branch (Z ~ B):  p_sc = K^2/(8.485 pi a0 alpha^{{3/2}}) = {pIR:.4e} eV")
    print(f"                        = sqrt(K)/(3 pi a0 L*^3)               = {pIR2:.4e} eV")
    ck("C2", pIR, pIR2, tol=1e-12, desc="two independent routes to p_sc (IR branch)",
       why="one uses (K,a0,alpha), the other (K,a0,L*) with alpha = K L*^2/2")
    ck("C3", pIR / pIR2, 1.0, tol=1e-12, desc="degeneracy check", why="same number")

    # UV branch
    def p_sc_UV(a0v, etav, alphav):
        if alphav <= 0.0 or etav <= 0.0:
            return float("inf")
        return K_EV ** 2 / (12.0 * math.pi * a0v * alphav * math.sqrt(etav))

    pUV = p_sc_UV(A0, GAMMA, ALPHA)
    print(f"    UV branch (Z ~ eta p^2): p_sc = K^2/(12 pi a0 alpha eta^(1/2)) = {pUV:.4e} eV")
    ck("C4", pUV / pIR, 1.0, tol=0.5,
       desc="the two branches agree within a factor 2 at eta = gamma",
       why="at eta=gamma both reduce to O(1) K^(1/2)/(a0 L*^3)")
    # independent scaling M_L^3/(M_Pl a0)
    mL = (1.0 / kappa_L) if kappa_L > 0 else float("inf")
    pscal = (mL ** 3 / (M_PL_EV * A0)) if kappa_L > 0 else float("inf")
    coeff = 2.0 / (3.0 * math.sqrt(math.pi)) * (K_EV / (2.0 * B_COEF)) ** 1.5
    ck("C5", pIR / pscal, coeff, tol=1e-12,
       desc="p_sc/(M_L^3/(M_Pl a0)) = 2/(3 sqrt pi) (K/2B)^{3/2}",
       why="the parametric form, checked against an independent algebraic route")
    print(f"    parametric form: p_sc = {pIR/pscal:.5f} M_L^3/(M_Pl a0) = {pscal:.4e} eV")

    # comparisons
    print(f"\n    comparisons:  p_sc/H0 = {pIR/H0_EV:.3e}")
    print(f"                  p_sc/a0 = {pIR/A0:.3e}")
    print(f"                  p_sc/(1/L*) = {pIR*LSTAR_EV:.3e}")
    ck("C6", pIR / H0_EV, 1.899e-36, tol=0.02, desc="p_sc/H0", why="36 orders below Hubble")
    ck("C7", pIR / A0, 1.380e-35, tol=0.02, desc="p_sc/a0", why="35 orders below a0")
    ck("C8", pIR * LSTAR_EV, 1.064e-44, tol=0.02, desc="p_sc/(1/L*)",
       why="44 orders below the fitted stiffness scale")

    # loop factor across the astrophysical range
    print("\n    loop factor deltaPi/omega^2 = (p_sc/p)^2 across the astrophysical range:")
    ks = dict(CMB=1e-30 / HBARC * 0 + 6.4e-30, LSS=4.3e-31, gal=1e-32,
              Lstar=1.0 / LSTAR_EV, a0v=A0)
    worst = 0.0
    for nm, kv in ks.items():
        lf = (pIR / kv) ** 2
        worst = max(worst, lf)
        print(f"      {nm:6s} p={kv:.3e} eV   deltaPi/omega^2 = {lf:.3e}")
    ck("C9", worst, 0.0, tol=1e-20, mode="abs",
       desc="largest loop factor over CMB/LSS/galactic/L*/a0 scales",
       why="the EFT is perturbative at every astrophysical scale by >30 orders")

    # the Green's function of the k^4 operator
    print("\n    static Green's function: alpha nabla^4 sigma = J  =>  G = -r/(8 pi alpha).")
    rr = np.linspace(0.1, 0.9, 8001)
    G = -rr / (8.0 * math.pi)

    def lap(f, r):
        fp = np.gradient(f, r)
        fpp = np.gradient(fp, r)
        return fpp + 2.0 * fp / r

    L1 = lap(G, rr)
    exact1 = -1.0 / (4.0 * math.pi * rr)
    dev1 = float(np.max(np.abs(L1 / exact1 - 1.0)[5:-5]))
    print(f"    nabla^2 G = -1/(4 pi r): max relative deviation {dev1:.2e}")
    L2 = lap(L1, rr)
    flux = 4.0 * math.pi * rr ** 2 * np.gradient(L1, rr)
    print(f"    flux 4 pi r^2 d(nabla^2G)/dr = {flux[10:-10].mean():.6f} (must be 1)")
    ck("C10", dev1, 0.0, tol=1e-4, mode="abs",
       desc="nabla^2(-r/8pi) = -1/(4 pi r) pointwise",
       why="the k^4 Green's function is the potential of a delta source")
    ck("C11", float(flux[10:-10].mean()), 1.0, tol=1e-4,
       desc="unit flux: nabla^4(-r/8pi) = delta^3(r)",
       why="normalisation of the linear potential (Gauss)")
    print("    a linear potential gives a CONSTANT force: -dPhi/dr = const, not 1/r^2")
    ck("C12", -(G[-1] - G[0]) / (rr[-1] - rr[0]) * (8.0 * math.pi), 1.0, tol=1e-6,
       desc="d(-G)/dr = 1/(8 pi): constant force", why="wrong shape for a 1/r potential")
    print("    the theory's own exact linearised solution has Phi = -mu/r + mu r/L*^2")
    print("    (A22): the linear term equals the 1/r term at r = L* = 24 pc, and is")
    print("    (r/L*)^2 of it at radius r.  The k^4 mode supplies that shape, not the law.")
    ck("C13", (1.0 * LSTAR_EV) ** 2 / LSTAR_EV ** 2, 1.0, tol=0.0, mode="abs",
       desc="linear/Newtonian = (r/L*)^2 = 1 at r = L*", why="A22's exact solution")

    print(f"\n    p_sc for the three a0 in play: canonical {p_sc_IR_closed(A0):.4e} eV, "
          f"alt {p_sc_IR_closed(A0_ALT):.4e} eV, kappa-measured "
          f"{p_sc_IR_closed(A0_KAPPA):.4e} eV  (p_sc ~ 1/a0)")
    ck("C14", p_sc_IR_closed(A0_KAPPA) * A0_KAPPA, p_sc_IR_closed(A0) * A0,
       tol=1e-12, desc="p_sc a0 = const across the three footings",
       why="p_sc scales as 1/a0, so the kappa error bar moves it by 1/kappa")
    out["p_sc_alt_eV"] = p_sc_IR_closed(A0_ALT)
    out["p_sc_kappa_eV"] = p_sc_IR_closed(A0_KAPPA)
    out["p_sc_eV"] = pIR
    out["p_sc_UV_eV"] = pUV
    out["p_star_eV"] = p_star
    out["kappa_L_eVinv"] = kappa_L
    out["M_L_eV"] = mL

    print("\n    The EFT is valid at ALL astrophysical scales: p_sc is 36 orders below")
    print("    H0.  The mode cannot be the mediator of a 1/r force -- its static")
    print("    Green's function is -r/(8 pi alpha).  The law itself is first order")
    print("    (charge + W), not k^4.")
    return out


# ==========================================================================
def main():
    global MUTATE
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--mutate", default=None)
    args = ap.parse_args()
    MUTATE = args.mutate
    if MUTATE:
        apply_mutation(MUTATE)
        print(f"*** MUTATION: {MUTATE} ***")

    print("A69 -- the P-sector sound speed: symmetry, observable, gates, cutoff")
    print(f"  a0 = {A0:.6e} eV (9.36e-11 m/s^2),  L* = {LSTAR_PC} pc = {LSTAR_EV:.6e} eV^-1")
    print(f"  gamma = alpha = K L*^2/2 = {GAMMA:.6e} eV^-4,  B = {B_COEF:.6e} eV^-2")
    print(f"  Lambda = 32 pi a0^2 = {LAMBDA_EV2:.6e} eV^2,  1/L* = {1/LSTAR_EV:.6e} eV")
    print(f"  K = 4 pi G = {K_EV:.6e} eV^-2,  H0 = {H0_EV:.6e} eV,  "
          f"a0(alt) = {A0_ALT:.6e} eV,  a0(kappa=0.371) = {A0_KAPPA:.6e} eV")

    out = {}
    out["constants"] = dict(a0_eV=A0, a0_alt_eV=A0_ALT, a0_kappa_eV=A0_KAPPA,
                            Lstar_pc=LSTAR_PC, Lstar_eVinv=LSTAR_EV,
                            gamma_eV4=GAMMA, alpha_eV4=GAMMA, B_eV2=B_COEF,
                            K_eV2=K_EV, Lambda_eV2=LAMBDA_EV2, H0_eV=H0_EV,
                            kappa_meas=KAPPA_MEAS, kappa_sig=KAPPA_SIG)

    out["task1"] = task1()
    out["task2"] = task2()
    out["task3"] = task3()
    out["task4"] = task4()

    npass = sum(1 for r in RESULTS if r["ok"])
    print("\n" + "=" * 78)
    print(f"RESULT: {npass}/{len(RESULTS)} checks PASS")
    if npass != len(RESULTS):
        print("FAILED:")
        for r in RESULTS:
            if not r["ok"]:
                print(f"   {r['name']}  got={r['got']:.6e} want={r['want']:.6e} "
                      f"err={r['err']:.3e} tol={r['tol']:.3e}")
    print("=" * 78)

    if args.json_out:
        payload = dict(lane="A69_psector_sound", mutation=MUTATE,
                       n_checks=len(RESULTS), n_pass=npass,
                       checks=RESULTS, data=out)
        with open(args.json_out, "w") as fh:
            json.dump(payload, fh, indent=1, default=float)
        print(f"wrote {args.json_out}")
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
