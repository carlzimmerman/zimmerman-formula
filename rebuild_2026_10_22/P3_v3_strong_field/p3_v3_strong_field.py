#!/usr/bin/env python3
"""P3_v3_strong_field: black holes, ringdown, neutron stars and strong coupling for v3 (C4-literal Khronon + P).

v3 (covariant_push_2026_10_22/THEORY_V3_DRAFT.md section 1; C5's Lagrangian at beta = eta = gamma_F = 0, xi = 1):
  L = sqrt(-g) [ R/(4K) + xi P^mu A_mu - W(K|P|) - (gamma_L/2)(D.P)^2 + mu_K^2 (Q-1)^2/(2K) ],  K = 4 pi G,
  W'(u) = u a0/(K (a0 - u)) (capped, C8), gamma_L = K L*^2/2, A_mu the khronon acceleration, Q = |d tau|.
Frozen criteria: FROZEN_CRITERIA.md (f28b8c6a92) + AMENDMENT A1 (c58afc3b20) + AMENDMENT A2 (988eb4940d).

Static spherical sector built covariantly in sympy: metric -e^(2 Phi) f dt^2 + 2 b dt dr + dr^2/f + R^2 dOmega^2,
khronon tau = t + h(r), P = p e^mu (e the unit radial vector orthogonal to n). Scaled units GM = c = 1:
a_hat = a0 GM/c^4, sigma = a0 L*^2/(2GM), p = (a_hat/K) p_tilde (|p_tilde| < 1 is the cap), eps_mu = mu_K^2 GM/a0.

Run: OMP_NUM_THREADS=1 nice -n 15 python3 p3_v3_strong_field.py      (P3_MUTATE=1: clock coefficient xi = 2)
kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 m/s^2, never pooled. No dark-matter particle. Not "theory closed".
"""
import json
import math
import os
import resource
import sys
import time

if os.environ.get("PYTHONHASHSEED") != "0":      # determinism: sympy's simplify paths depend on the hash seed
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, PYTHONHASHSEED="0"))

import numpy as np
import sympy as sp
from numpy.polynomial import chebyshev as Cb
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

T0 = time.time()
MUTATE = os.environ.get("P3_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
XI = 2 if MUTATE else 1
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, f"p3_v3_strong_field{TAG}.out")
JSON = os.path.join(HERE, f"p3_v3_strong_field_results{TAG}.json")

# ------------------------------------------------------------------ constants (SI)
c_SI = 2.99792458e8
G_SI = 6.67430e-11
GMSUN = 1.32712440018e20
PC = 3.0856775814913673e16
KPC = 1e3 * PC
AU = 1.495978707e11
LPLANCK = 1.616255e-35
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LSTARS = [20, 24, 90]
MU_K = 1.0 / (100 * KPC)          # m^-1, BS24 Eq. 39 cap via C4
BH = {"M87*": 6.5e9, "SgrA*": 4.3e6, "BH10": 10.0, "BH63": 63.0}       # Msun, ILLUSTRATIVE
R_DYN = {"SgrA*": 2000 * AU, "M87*": 100 * PC}                       # ILLUSTRATIVE dynamical-mass radii

lines, checks, res = [], [], {"mutate": MUTATE, "xi": XI}


def log(s):
    print(s, flush=True)
    lines.append(s)


def check(kid, ok, value, thr):
    checks.append({"id": kid, "pass": bool(ok), "value": str(value), "threshold": thr})
    log(f"{kid} {'PASS' if ok else 'FAIL'} {value} {thr}")


log(f"P3_v3_strong_field  mutate={MUTATE} (xi = {XI})")

# ==================================================================================== PART A: sympy
r, th = sp.symbols("r theta", positive=True)
M, K, gL, mu2, xi, a0s = sp.symbols("M K gamma_L mu2 xi a0", positive=True)
sig, epsm = sp.symbols("sigma epsilon_mu", positive=True)
NJ = 4


def jet(name):
    return [sp.Symbol(f"{name}{k}") for k in range(NJ + 1)]


Ph, fj, Rj, bj, hj, pj = jet("Phi"), jet("f"), jet("R"), jet("b"), jet("h"), jet("p")
JETS = {"Phi": Ph, "f": fj, "R": Rj, "b": bj, "h": hj, "p": pj}


def D(e, jets=None):
    jets = JETS.values() if jets is None else jets
    out = sp.diff(e, r)
    for q in jets:
        for k in range(NJ):
            d = sp.diff(e, q[k])
            if d != 0:
                out += q[k + 1] * d
    return out


Phi, f, R, b = Ph[0], fj[0], Rj[0], bj[0]
g = sp.Matrix([[-sp.exp(2 * Phi) * f, b, 0, 0], [b, 1 / f, 0, 0], [0, 0, R ** 2, 0], [0, 0, 0, R ** 2 * sp.sin(th) ** 2]])
ginv = sp.simplify(g.inv())


def dc(e, m):
    return D(e) if m == 1 else (sp.diff(e, th) if m == 2 else 0)


Gam = [[[sp.simplify(sum(ginv[a, d] * (dc(g[d, bb], c) + dc(g[d, c], bb) - dc(g[bb, c], d)) for d in range(4)) / 2)
         for c in range(4)] for bb in range(4)] for a in range(4)]
Ric = sp.zeros(4)
for bb in range(4):
    for d in range(4):
        e_ = 0
        for a in range(4):
            e_ += dc(Gam[a][bb][d], a) - dc(Gam[a][bb][a], d)
            for c in range(4):
                e_ += Gam[a][a][c] * Gam[c][bb][d] - Gam[a][d][c] * Gam[c][bb][a]
        Ric[bb, d] = e_
Rs = sp.simplify(sum(ginv[a, d] * Ric[a, d] for a in range(4) for d in range(4)))
sqg = R ** 2 * sp.sqrt(sp.exp(2 * Phi) + b ** 2)          # per sin(theta)
dtau = [1, hj[1], 0, 0]
X = sp.simplify(-sum(ginv[a, d] * dtau[a] * dtau[d] for a in range(4) for d in range(4)))   # Q^2
nl = [-dtau[a] / sp.sqrt(X) for a in range(4)]
nu = [sum(ginv[a, d] * nl[d] for d in range(4)) for a in range(4)]
dl = D(-sp.log(X) / 2)                                     # (ln N)', N = 1/Q
ndl = nu[1] * dl
Al = [nl[0] * ndl, dl + nl[1] * ndl, 0, 0]                 # A_mu = q_mu^nu d_nu ln N
s2 = sp.sqrt(sp.exp(2 * Phi) + b ** 2)
el = [-s2 * nu[1], s2 * nu[0], 0, 0]                       # e_mu: unit, orthogonal to n, e^r > 0
eu = [sum(ginv[a, d] * el[d] for d in range(4)) for a in range(4)]
pp = pj[0]
PA = pp * (eu[0] * Al[0] + eu[1] * Al[1])
DP = D(sqg * pp * eu[1]) / sqg - PA                        # leaf divergence = div P - P.A
Wexpr = lambda u: (a0s / K) * (-u - a0s * sp.log(1 - u / a0s))   # the record's capped W
LGR = sqg * Rs / (4 * K)
LP = sqg * (xi * PA - Wexpr(K * pp) - gL / 2 * DP ** 2)
LK = sqg * mu2 * (sp.sqrt(X) - 1) ** 2 / (2 * K)
Ltot = LGR + LP + LK
ee = sp.simplify(sum(eu[a] * el[a] for a in range(4)))
en = sp.simplify(sum(eu[a] * nl[a] for a in range(4)))
log(f"A: covariant reduced Lagrangian built ({time.time() - T0:.1f} s); e.e = {ee}, e.n = {en}")

eS = 1 - 2 * M / r
BGS = {}
for k in range(NJ + 1):
    BGS[Ph[k]] = 0
    BGS[bj[k]] = 0
    BGS[fj[k]] = sp.diff(eS, r, k)
    BGS[Rj[k]] = r if k == 0 else (1 if k == 1 else 0)
HPJ = [hj, pj]


def ELbg(L, q):
    """Euler-Lagrange derivative on the Schwarzschild metric (Phi = 0, f = e, R = r, b = 0); h, p jets kept."""
    out = 0
    for k in range(NJ + 1):
        t = sp.diff(L, q[k])
        if t == 0:
            continue
        t = t.subs(BGS)
        for _ in range(k):
            t = -D(t, HPJ)
        out += t
    return out


def Jh(L):
    """khronon first integral dL/dh' - (dL/dh'')' on the Schwarzschild metric."""
    return sp.diff(L, hj[1]).subs(BGS) - D(sp.diff(L, hj[2]).subs(BGS), HPJ)


Hf = sp.Rational(7, 10) * sp.sqrt(2 * M / r) / eS + sp.Rational(1, 10) / r   # generic test foliation
Pf = sp.Rational(3, 10) / r ** 2 + sp.Rational(1, 7) / r + sp.Rational(1, 20)  # generic test P profile


def jsub(H, P):
    s = {hj[0]: 0}
    for k in range(1, NJ + 1):
        s[hj[k]] = sp.diff(H, r, k - 1)
    for k in range(NJ + 1):
        s[pj[k]] = sp.diff(P, r, k)
    return s


PTS = [{r: sp.Rational(37, 10), M: 1}, {r: sp.Rational(123, 10), M: sp.Rational(3, 2)},
       {r: sp.Rational(71, 10), M: sp.Rational(1, 2)}]
PAR = {K: 4 * sp.pi, gL: sp.Rational(7, 3), mu2: sp.Rational(1, 5), xi: XI, a0s: sp.Integer(5)}


def nres(expr):
    return max(abs(complex(sp.N(expr.subs(PAR).subs(pt), 40))) for pt in PTS)


sJ = jsub(Hf, Pf)
Nbg = (X ** sp.Rational(-1, 2)).subs(BGS).subs({hj[1]: Hf})
Dd = Nbg * sp.diff(r ** 2 * Pf, r) / r ** 2
# A1
LPb = LP.subs(BGS).subs(sJ)
targetA1 = r ** 2 * Pf * sp.diff(Nbg, r) - r ** 2 * Wexpr(K * Pf) - gL / 2 * Nbg ** 2 * sp.diff(r ** 2 * Pf, r) ** 2 / r ** 2
a1res, a1sc = nres(LPb - targetA1), nres(targetA1)
gamrr = (1 / X).subs(BGS).subs({hj[1]: Hf})                # N^2 on Schwarzschild
FFbg = sp.simplify((ginv[1, 1] + (nu[1]) ** 2).subs(BGS)) # gamma^rr = g^rr + n^r n^r
a1F = nres(FFbg.subs({hj[1]: Hf}) - gamrr)
# leaf divergence: D.P computed as div P - P.A must equal q^{mu nu} nabla_mu P_nu (P orthogonal to n); hence
# P.A = div P - D.P and the clock term is -xi D.P up to a total divergence (covariant identity).
Pl = [pp * el[a] for a in range(4)]
qU = [[ginv[a, d] + nu[a] * nu[d] for d in range(4)] for a in range(4)]
covP = sum(qU[a][d] * (dc(Pl[d], a) - sum(Gam[l_][a][d] * Pl[l_] for l_ in range(4))) for a in range(4) for d in range(4))
sGen = {Ph[0]: sp.Rational(1, 7) / r, Ph[1]: -sp.Rational(1, 7) / r ** 2, fj[0]: 1 - 2 * M / r + sp.Rational(1, 9) / r ** 2,
        fj[1]: 2 * M / r ** 2 - sp.Rational(2, 9) / r ** 3, Rj[0]: r * (1 + sp.Rational(1, 11) / r), Rj[1]: 1,
        bj[0]: sp.Rational(1, 13) / r, bj[1]: -sp.Rational(1, 13) / r ** 2}
a1D = nres((covP - DP).subs(sGen).subs({th: sp.Rational(1, 3)}).subs(sJ))
res["A1"] = {"residual": a1res, "scale": a1sc, "gamma_rr_minus_N2": a1F, "leaf_divergence_identity": a1D}
check("A1", a1res < 1e-25 * a1sc and a1F < 1e-25 and a1D < 1e-25,
      f"|L_P - [r^2 p N' - r^2 W - (gL/2) N^2 ((r^2p)')^2/r^2]| = {a1res:.2e} (scale {a1sc:.2e}); |gamma^rr - N^2| = "
      f"{a1F:.2e}; |q^mn nabla_m P_n - (div P - P.A)| on a general (Phi, f, R, b) background = {a1D:.2e} "
      f"(so xi P.A = xi div P - xi D.P: the clock is -xi D.P up to a total divergence)", "residual 0 (< 1e-25 of scale)")

# A2: PG solution, all Euler-Lagrange equations (h via its first integral)
h1PG = sp.sqrt(2 * M / r) / eS
sPG = jsub(h1PG, sp.Integer(0))


a2 = {}
for nm in ("Phi", "f", "R", "b", "p"):
    t1 = time.time()
    E = ELbg(Ltot, JETS[nm]).subs(sPG)
    a2[nm] = nres(E)
    log(f"  A2 EL_{nm} at PG: |residual| = {a2[nm]:.2e} ({time.time() - t1:.1f} s)")
Jpg = Jh(Ltot).subs(sPG)
a2["h_first_integral"] = nres(Jpg)
log(f"  A2 khronon first integral at PG: {a2['h_first_integral']:.2e} (C = 0)")
# uniqueness among p = 0 stationary foliations of Schwarzschild: EL_p = r^2 N' (so N' = 0); J = s N E_N with
# E_N = -mu^2 r^2 (1-N)/(K N^3): s = 0 (static, but then N = sqrt(e), N' != 0) or N = 1 (PG).
Ep0 = ELbg(Ltot, pj).subs(jsub(Hf, sp.Integer(0)))
a2["p_eq_at_p0_minus_r2Nprime"] = nres(Ep0 - XI * r ** 2 * sp.diff(Nbg, r))
J0 = Jh(Ltot).subs(jsub(Hf, sp.Integer(0)))
sHf = eS * Hf * Nbg ** 2
a2["J_at_p0_minus_sNE_N"] = nres(J0 - sHf * Nbg * (-mu2 * r ** 2 * (1 - Nbg) / (K * Nbg ** 3)))
res["A2"] = a2
okA2 = all(v < 1e-25 for v in a2.values())
check("A2", okA2, f"PG-Schwarzschild, p = 0: max residual over EL(Phi, f, R, b, p) and the khronon integral "
      f"{max(a2.values()):.2e}; p = 0 => EL_p = xi r^2 N', J = s N (-mu^2 r^2 (1-N)/(K N^3)) (residuals "
      f"{a2['p_eq_at_p0_minus_r2Nprime']:.1e}, {a2['J_at_p0_minus_sNE_N']:.1e}) => N' = 0 and N = 1 (PG unique)",
      "all residuals 0 (< 1e-25)")

# A3: khronon first integral and p equation on Schwarzschild (identities written for xi = 1)
J = Jh(Ltot).subs(sJ)
EN = -sp.diff(r ** 2 * Pf, r) * (1 + gL * Dd) - mu2 * r ** 2 * (1 - Nbg) / (K * Nbg ** 3)
a3k, a3ks = nres(J - sHf * Nbg * EN), nres(J)
Ep = ELbg(Ltot, pj).subs(sJ)
Wp = K * Pf * a0s / (a0s - K * Pf)
tgtp = r ** 2 * (sp.diff(Nbg, r) - Wp + gL * sp.diff(Nbg * Dd, r))
a3p, a3ps = nres(Ep - tgtp), nres(tgtp)
res["A3"] = {"khronon": [a3k, a3ks], "p_eq": [a3p, a3ps]}
check("A3", a3k < 1e-25 * a3ks and a3p < 1e-25 * a3ps,
      f"J - s N E_N: {a3k:.2e} (scale {a3ks:.2e}); EL_p - r^2[N' - K W'(Kp) + gL (N D)']: {a3p:.2e} (scale {a3ps:.2e})",
      "residual 0 (< 1e-25 of scale)")
log(f"A done ({time.time() - T0:.1f} s)")

# ------------------------------------------------------------------ scaled stress tensor (O(a_hat); W is O(a_hat^2))
PAt = pp * (eu[0] * Al[0] + eu[1] * Al[1])
DPt = D(sqg * pp * eu[1]) / sqg - PAt
Lt = sqg * (xi * PAt - sig / 2 * DPt ** 2 + epsm / 2 * (sp.sqrt(X) - 1) ** 2)
EPhi, Ef, ER, Eb = ELbg(Lt, Ph), ELbg(Lt, fj), ELbg(Lt, Rj), ELbg(Lt, bj)
Jt = Jh(Lt)
Ept = ELbg(Lt, pj)
Ttt = EPhi / r ** 2
Trr = Ttt - 2 * eS * Ef / r ** 2
Tthth = ER / (2 * r)
Trt = -eS * Eb / r ** 2
Ldens = (Lt / sqg).subs(BGS)
ARGS = [r, M, hj[1], hj[2], hj[3], pj[0], pj[1], pj[2], sig, epsm, xi]
fT = sp.lambdify(ARGS, [Ttt, Trr, Tthth, Trt, Jt, Ept, Ldens], "numpy", cse=True)
Nn, N1s, N2s = sp.symbols("Nn N1 N2")
Nfun = sp.Function("N")(r)
h1N = sp.sqrt(1 - eS / Nfun ** 2) / eS


def toN(ex):
    ex = ex.subs(sp.Derivative(Nfun, (r, 2)), N2s).subs(sp.Derivative(Nfun, r), N1s)
    return ex.subs(Nfun, Nn)


fH = sp.lambdify([r, M, Nn, N1s, N2s], [toN(h1N), toN(sp.diff(h1N, r)), toN(sp.diff(h1N, r, 2))], "numpy")

# static foliation on a general static background (neutron stars): h = 0, R = r, b = 0; Phi, f jets free
BGN = {bj[k]: 0 for k in range(NJ + 1)}
BGN.update({Rj[k]: (r if k == 0 else (1 if k == 1 else 0)) for k in range(NJ + 1)})
BGN.update({hj[k]: 0 for k in range(NJ + 1)})


def ELns(L, q):
    out = 0
    for k in range(NJ + 1):
        t = sp.diff(L, q[k])
        if t == 0:
            continue
        t = t.subs(BGN)
        for _ in range(k):
            t = -D(t, [Ph, fj, pj])
        out += t
    return out


EPhiN, EfN = ELns(Lt, Ph), ELns(Lt, fj)
sqgN = (sqg.subs(BGN))
TttN = EPhiN / sqgN
TrrN = TttN - 2 * fj[0] * EfN / sqgN
fTN = sp.lambdify([r] + Ph[:4] + fj[:4] + pj[:3] + [sig, epsm, xi], [TttN, TrrN], "numpy", cse=True)
log(f"stress tensor lambdified ({time.time() - T0:.1f} s)")


# ==================================================================================== PART B/C: foliations + observables
def eF(x):
    return 1 - 2 / x


def chebfit(fun, a, bnd, deg):
    xx = np.cos(np.pi * (np.arange(deg + 1) + 0.5) / (deg + 1))
    rr = (a + bnd) / 2 + (bnd - a) / 2 * xx
    return Cb.Chebyshev.fit(rr, np.array([fun(v) for v in rr]), deg, domain=[a, bnd])


def hS(N, x):
    e = eF(x)
    return (1 - N) * math.sqrt(max(N * N - e, 0.0)) * x * x / N


def peakN(x):
    e = eF(x)
    lo = max(math.sqrt(max(e, 0)) + 1e-14, 1e-12)
    rr_ = minimize_scalar(lambda N: -hS(N, x), bounds=(lo, 1 - 1e-14), method="bounded", options={"xatol": 1e-15})
    return rr_.x, -rr_.fun


_rc = minimize_scalar(lambda x: peakN(x)[1], bounds=(3.0, 4.5), method="bounded", options={"xatol": 1e-13}).x
NC, KSTAR = peakN(_rc)
RC = _rc


def NT(x, kap=None):
    kap = KSTAR if kap is None else kap
    Np, hp = peakN(x)
    e = eF(x)
    lo = max(math.sqrt(max(e, 0)) + 1e-15, 1e-13)
    if hp <= kap:
        return Np
    if x > RC:
        return brentq(lambda N: hS(N, x) - kap, lo, Np, xtol=1e-16, rtol=1e-15)
    return brentq(lambda N: hS(N, x) - kap, Np, 1 - 1e-15, xtol=1e-16, rtol=1e-15)


def capN(x, c, sigma, eps_):
    e = eF(x)

    def Gc(N):
        s = N * math.sqrt(max(N * N - e, 0.0))
        return s * x * x * ((2 * N / x) * (1 + 2 * sigma * N / x) + eps_ * (1 - N) / N ** 2) - c
    lo = max(math.sqrt(max(e, 0)) + 1e-15, 1e-12)
    return brentq(Gc, lo, 1.5, xtol=1e-16, rtol=1e-15)


def num_derivs(fun, x, hrel=2e-3):
    hh = hrel * x
    f0, fp, fm, fp2, fm2 = fun(x), fun(x + hh), fun(x - hh), fun(x + 2 * hh), fun(x - 2 * hh)
    d1 = (8 * (fp - fm) - (fp2 - fm2)) / (12 * hh)
    d2 = (-(fp2 + fm2) + 16 * (fp + fm) - 30 * f0) / (12 * hh * hh)
    return f0, d1, d2


class Member:
    """one stationary foliation + P profile on Schwarzschild (scaled units GM = 1)."""

    def __init__(self, kind, sigma, eps_, c=None, ph=None, a=1.9, bnd=12.0):
        if kind == "T":
            bnd = 52.0
        self.kind, self.sigma, self.eps, self.c, self.ph = kind, sigma, eps_, c, ph
        self.a, self.b = a, bnd
        if kind == "T":
            self.Nfun = lambda x: NT(x)
            self.cN = chebfit(self.Nfun, a, bnd, 260)
            self.c = KSTAR * (1 / sigma + eps_)
            integrand = lambda x: x * x * (1 - self.cN(x)) / (sigma * self.cN(x) ** 2)
            self.cIp = chebfit(integrand, a, bnd, 260)
            self.cI = self.cIp.integ(lbnd=2.0)
        elif kind == "C":     # exterior only (r >= 2M): the interior root structure is not used
            self.Nfun = lambda x: capN(x, c, sigma, eps_)
            if c < 0.05:
                self.cNs = [chebfit(self.Nfun, 2.0, 2.6, 160), chebfit(self.Nfun, 2.6, bnd, 160)]
            else:
                self.cNs = [chebfit(self.Nfun, 2.0, bnd, 160)]
        elif kind == "S":   # static foliation, capped zone: N = sqrt(e), p = 1
            pass

    def N(self, x, k=0):
        if self.kind == "T":
            return (self.cN if k == 0 else self.cN.deriv(k))(x)
        if self.kind == "C":
            cc = self.cNs[0] if (len(self.cNs) == 1 or x < 2.6) else self.cNs[1]
            return (cc if k == 0 else cc.deriv(k))(x)
        raise ValueError

    def p(self, x):
        if self.kind == "T":
            q = 4 * self.ph
            I, Ip = self.cI(x), self.cIp(x)
            Ipp = self.cIp.deriv()(x)
            p0 = (I + q) / x ** 2
            p1 = (Ip - 2 * x * p0) / x ** 2
            p2 = (Ipp - 2 * p0 - 4 * x * p1) / x ** 2
            return p0, p1, p2
        return 1.0, 0.0, 0.0

    def stress(self, x, far=False, xi_=None):
        xi_ = XI if xi_ is None else xi_
        if far:      # algebraic N beyond the Chebyshev domain (C members only)
            N0, N1, N2 = num_derivs(self.Nfun, x)
        else:
            N0, N1, N2 = self.N(x), self.N(x, 1), self.N(x, 2)
        h1, h2, h3 = fH(x, 1.0, N0, N1, N2)
        p0, p1, p2 = self.p(x)
        return [float(v) for v in fT(x, 1.0, h1, h2, h3, p0, p1, p2, self.sigma, self.eps, xi_)], (N0, N1, N2), (p0, p1, p2)


def conservation(mem, xs):
    out = []
    for v in xs:
        dd = 1e-4
        T, _, _ = mem.stress(v)
        Tp, _, _ = mem.stress(v + dd)
        Tm, _, _ = mem.stress(v - dd)
        e = eF(v)
        dT = (Tp[1] - Tm[1]) / (2 * dd)
        t2 = (1 / (v * v * e)) * (T[1] - T[0])
        t3 = 2 / v * (T[1] - T[2])
        out.append(abs(dT + t2 + t3) / max(abs(dT), abs(t2), abs(t3), 1e-300))
    return max(out)


def profile_tables(mem, rn):
    """m_tilde(r) = int_r^rn r^2 T^v_v, psi_tilde(r) = -int_r^rn r T_rr(EF), as Chebyshev series on [2.5, 12]
    plus the far contribution int_12^rn (log grid; C members use the algebraic N there)."""
    def Tv(x, far=False):
        T, _, _ = mem.stress(x, far=far)
        e = eF(x)
        Tvv = T[0] + T[3] / e
        TrrEF = (T[1] - T[0]) / e - 2 * T[3] / e ** 2
        return Tvv, TrrEF
    cm = chebfit(lambda x: x * x * Tv(x)[0], 2.5, 12.0, 120)
    cps = chebfit(lambda x: x * Tv(x)[1], 2.5, 12.0, 120)
    far_m, far_p = 0.0, 0.0
    if rn > 12.0:
        if mem.kind not in ("C", "PG") and rn > 52:
            raise ValueError("far integration only for C members")
        xs = np.exp(np.linspace(math.log(12.0), math.log(rn), 1601))
        if mem.kind in ("C", "PG"):
            vals = np.array([Tv(v, far=True) for v in xs])
        else:
            cm2 = chebfit(lambda x: x * x * Tv(x)[0], 12.0, rn, 120)
            cp2 = chebfit(lambda x: x * Tv(x)[1], 12.0, rn, 120)
            far_m = cm2.integ(lbnd=12.0)(rn)
            far_p = cp2.integ(lbnd=12.0)(rn)
            vals = None
        if vals is not None:
            lx = np.log(xs)
            ym, yp = xs * xs * vals[:, 0] * xs, xs * vals[:, 1] * xs
            far_m = float(np.sum(0.5 * (ym[1:] + ym[:-1]) * np.diff(lx)))
            far_p = float(np.sum(0.5 * (yp[1:] + yp[:-1]) * np.diff(lx)))
    Im = cm.integ(lbnd=12.0)    # int_12^x
    Ip = cps.integ(lbnd=12.0)
    mt = lambda x: -Im(x) + far_m          # int_x^rn = int_x^12 + int_12^rn
    pt = lambda x: Ip(x) - far_p           # -int_x^rn r T_rr = int_12^x - int_12^rn
    return mt, pt, Tv


def observables(dA, dB, ah):
    """Schwarzschild-type metric -A dt^2 + dr^2/B, A = e + ah dA, B = e + ah dB (dA, dB Chebyshev on [2.6, 11];
    the Schwarzschild part and its derivatives are analytic)."""
    if ah == 0.0:
        cdA = cdB = Cb.Chebyshev([0.0], domain=[2.6, 11.0])
    else:
        cdA = chebfit(dA, 2.6, 11.0, 90)
        cdB = chebfit(dB, 2.6, 11.0, 90)
    A = lambda x: 1 - 2 / x + ah * cdA(x)
    A1 = lambda x: 2 / x ** 2 + ah * cdA.deriv()(x)
    A2 = lambda x: -4 / x ** 3 + ah * cdA.deriv(2)(x)
    Bf = lambda x: 1 - 2 / x + ah * cdB(x)
    dAr2 = lambda x: A1(x) / x ** 2 - 2 * A(x) / x ** 3
    d2Ar2 = lambda x: A2(x) / x ** 2 - 4 * A1(x) / x ** 3 + 6 * A(x) / x ** 4
    rph = brentq(dAr2, 2.7, 3.4, xtol=1e-15, rtol=1e-15)
    bc = rph / math.sqrt(A(rph))
    Om = math.sqrt(A(rph)) / rph
    lam = math.sqrt(-A(rph) * Bf(rph) * bc ** 2 * d2Ar2(rph) / 2)
    L2p = lambda x: (3 * x * x * A1(x) + x ** 3 * A2(x)) * (2 * A(x) - x * A1(x)) \
        - x ** 3 * A1(x) * (A1(x) - x * A2(x))
    risco = brentq(L2p, 5.0, 7.5, xtol=1e-15, rtol=1e-15)
    Oisco = math.sqrt(A1(risco) / (2 * risco))
    return {"r_ph": rph, "b_c": bc, "Omega_c": Om, "lambda_L": lam, "r_isco": risco, "Omega_isco": Oisco}


OBS0 = observables(lambda x: 0.0, lambda x: 0.0, 0.0)
c1dev = max(abs(OBS0["b_c"] - 3 * math.sqrt(3)), abs(OBS0["r_ph"] - 3), abs(OBS0["r_isco"] - 6),
            abs(OBS0["Omega_isco"] - 6 ** -1.5), abs(OBS0["Omega_c"] - 1 / (3 * math.sqrt(3))),
            abs(OBS0["lambda_L"] - 1 / (3 * math.sqrt(3))))
res["C1"] = {"schwarzschild": OBS0, "max_dev": c1dev}
check("C1", c1dev < 1e-10, f"a_hat = 0 returns Schwarzschild: max |dev| = {c1dev:.2e}", "< 1e-10")


def response(mem, rn, rdyn=None):
    """d ln X / d a_hat for the observables, with mass and time normalised at rn; also M_dyn at rdyn (= rn)."""
    mt, pt, Tv = profile_tables(mem, rn)
    if rn > 12.0:
        # values of m, psi at r <= 11 already include the far part; A = e^(2 a psi)(1 - 2(1 + a m)/r)
        pass
    dA = lambda x: 2 * pt(x) * eF(x) - 2 * mt(x) / x
    dB = lambda x: -2 * mt(x) / x
    scl = max(1.0, max(max(abs(dA(x)), abs(dB(x))) for x in np.linspace(2.6, 11.0, 50)))
    out = {}
    for j_, ah in enumerate((1e-6 / scl, 1e-7 / scl)):
        ob = observables(dA, dB, ah)
        out[j_] = {k_: (ob[k_] / OBS0[k_] - 1) / ah for k_ in ob}
    coef = out[0]
    lin = max(abs(out[0][k_] - out[1][k_]) / max(abs(out[0][k_]), 1e-30) for k_ in coef)
    mdyn = 0.0
    if rdyn is not None:
        # Keplerian mass at rdyn: M_dyn = r^2 A'/2 with A = e^(2 a psi)(1 - 2(1 + a m)/r); m = psi = 0 at rdyn
        Tvv, TrrEF = Tv(rdyn, far=(mem.kind == "C"))
        mprime = -rdyn ** 2 * Tvv
        psiprime = rdyn * TrrEF
        mdyn = (-rdyn * mprime) + rdyn ** 2 * psiprime * eF(rdyn)     # d M_dyn / d a_hat
    return coef, lin, mdyn


# ------------------------------------------------------------------ benchmarks
def scaled(mass_msun, a0, Lpc):
    GM = GMSUN * mass_msun
    rg = GM / c_SI ** 2
    ah = a0 * rg / c_SI ** 2
    sigma = a0 * (Lpc * PC) ** 2 / (2 * GM)
    eps_ = MU_K ** 2 * GM / a0
    return ah, sigma, eps_, rg


log("")
log("B: stationary foliations on Schwarzschild")
log(f"  screened transonic X-point: kappa* = {KSTAR:.10f}, r_c = {RC:.8f} M, N_c = {NC:.8f}")
res["Xpoint"] = {"kappa_star": KSTAR, "r_c": RC, "N_c": NC}

# B1: static branch (capped zone p = 1, N = sqrt(e), h = 0)
b1 = {}
okB1 = True
for nm, ms in BH.items():
    for foot, a0 in A0.items():
        for Lpc in LSTARS:
            ah, sigma, eps_, rg = scaled(ms, a0, Lpc)
            es = np.logspace(-10, -6, 9)
            vals = []
            for e in es:
                v = 2 / (1 - e)
                Nst = math.sqrt(e)
                N1 = 1 / (v * v * Nst)
                N2 = -(2 / v ** 3) / Nst - 1 / (v ** 4 * 2 * Nst ** 3)
                T = [float(x_) for x_ in fT(v, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, sigma, eps_, XI)]
                vals.append((T[0], T[1], T[2], T[6], T[0] ** 2 + T[1] ** 2 + 2 * T[2] ** 2))
            vals = np.array(vals)
            sl = [float(np.polyfit(np.log(es), np.log(np.abs(vals[:, j]) + 1e-300), 1)[0]) for j in range(5)]
            # cap: 1 - p = a/(w + a), w = N' + sigma (2 N^2/r)' at e = 1e-8
            e8 = 1e-8
            v8 = 2 / (1 - e8)
            w8 = 1 / (v8 * v8 * math.sqrt(e8)) + sigma * (2 * (2 / v8 ** 2) / v8 - 2 * e8 / v8 ** 2)
            onemp = ah / (w8 + ah)
            key = f"{nm}|{foot}|{Lpc}pc"
            b1[key] = {"slope_Trr": sl[1], "slope_Tthth": sl[2], "slope_Ttt": sl[0], "slope_L": sl[3],
                       "slope_TT": sl[4], "one_minus_u_over_a0_at_e1e-8": onemp, "sigma": sigma}
            okB1 &= (onemp <= 1e-3) and (-0.6 <= sl[1] <= -0.4)
res["B1"] = b1
smp = b1["SgrA*|canonical|24pc"]
log(f"  B1 sample SgrA* canonical 24 pc: exponents Trr {smp['slope_Trr']:.3f}, Tthth {smp['slope_Tthth']:.3f}, "
    f"L_P {smp['slope_L']:.3f}, T.T {smp['slope_TT']:.3f}; 1 - u/a0 = {smp['one_minus_u_over_a0_at_e1e-8']:.2e}")
check("B1", okB1, f"static branch: max 1 - u/a0 at e = 1e-8: {max(v['one_minus_u_over_a0_at_e1e-8'] for v in b1.values()):.2e}; "
      f"T^r_r exponent range [{min(v['slope_Trr'] for v in b1.values()):.3f}, {max(v['slope_Trr'] for v in b1.values()):.3f}]; "
      f"(reading, A1(a): T^th_th exponent range [{min(v['slope_Tthth'] for v in b1.values()):.3f}, "
      f"{max(v['slope_Tthth'] for v in b1.values()):.3f}], L_P [{min(v['slope_L'] for v in b1.values()):.3f}, "
      f"{max(v['slope_L'] for v in b1.values()):.3f}], T.T [{min(v['slope_TT'] for v in b1.values()):.3f}, "
      f"{max(v['slope_TT'] for v in b1.values()):.3f}])",
      "cap reached (1 - u/a0 <= 1e-3) AND T^r_r exponent in [-0.6, -0.4] (frozen; A1(a): expected FAIL)")

# B2/B3/B4 members per benchmark
members, memrows = {}, {}
okB2, okB3, okB4 = True, True, True
b4_open = []
PH_GRID = [-1.0, -0.5, 0.0, 0.5, 1.0]
C_GRID = [0.01, 0.1, 0.3, 1.0]
cmax_rec = {}
for nm, ms in BH.items():
    for foot, a0 in A0.items():
        for Lpc in LSTARS:
            ah, sigma, eps_, rg = scaled(ms, a0, Lpc)
            key = f"{nm}|{foot}|{Lpc}pc"
            mems = []
            if sigma < 0.5:
                for c in C_GRID:
                    m_ = Member("C", sigma, eps_, c=c)
                    xs = np.linspace(2.0 + 1e-9, 200.0, 4000)
                    Ns = np.array([capN(v, c, sigma, eps_) for v in xs])
                    dN = np.gradient(Ns, xs)
                    w = dN + sigma * np.gradient(2 * Ns ** 2 / xs, xs)
                    ok = (Ns[0] > 0) and (w.min() > 0)
                    mems.append((m_, ok, {"c": c, "N(2M)": float(Ns[0]), "min_w": float(w.min())}))
                    okB3 &= ok
                # largest valid c on a 0.05 grid
                cm_ = 0.0
                for c in np.arange(0.05, 3.0001, 0.05):
                    xs = np.linspace(2.0 + 1e-9, 200.0, 4000)
                    try:
                        Ns = np.array([capN(v, c, sigma, eps_) for v in xs])
                    except ValueError:
                        break
                    w = np.gradient(Ns, xs) + sigma * np.gradient(2 * Ns ** 2 / xs, xs)
                    if w.min() > 0:
                        cm_ = c
                    else:
                        break
                cmax_rec[key] = cm_
            else:
                for ph in PH_GRID:
                    m_ = Member("T", sigma, eps_, ph=ph)
                    xs = np.linspace(2.0, 51.5, 3000)
                    ps = np.array([m_.p(v)[0] for v in xs])
                    # beyond 52 M the screened p decays monotonically to 1/(2 sigma): p ~ 1/(2 sigma) + 5/(2 sigma r)
                    ok = (np.max(np.abs(ps)) < 1.0 - 1e-9) and (m_.N(2.0) > 0)     # u < a0 strictly
                    mems.append((m_, ok, {"p(2M)": ph, "max|p|": float(np.max(np.abs(ps))), "N(2M)": float(m_.N(2.0))}))
                if sigma >= 2:
                    okB2 &= any(o for _, o, _ in mems)
                else:
                    if not any(o for _, o, _ in mems):
                        okB4 = False
                        b4_open.append(key)
            members[key] = mems
            memrows[key] = {"sigma": sigma, "a_hat": ah, "eps_mu": eps_, "r_g_m": rg,
                            "members": [dict(info, valid=bool(o)) for _, o, info in mems]}

# B2 structural checks on one screened member (any sigma >= 2; the T profile is sigma-independent)
mT = Member("T", 1.93e4, 1.5e-12, ph=0.0)
alg = max(abs(hS(mT.N(v), v) - KSTAR) / KSTAR for v in np.linspace(2.05, 11.9, 400) if abs(v - RC) > 1e-3)
slope_l = (mT.N(RC - 1e-5) - mT.N(RC - 2e-5)) / 1e-5
slope_r = (mT.N(RC + 2e-5) - mT.N(RC + 1e-5)) / 1e-5
far = NT(200.0) / math.sqrt(eF(200.0)) - 1
chebT = max(abs(mT.N(v) - NT(v)) for v in np.linspace(1.95, 51.5, 600))
res["B2"] = {"alg_residual_rel": alg, "slopes_at_rc": [slope_l, slope_r], "N(2M)": float(mT.N(2.0)),
             "N_over_sqrt_e_minus_1_at_200M": far, "cheb_err": chebT}
okB2 &= alg < 1e-10 and abs(slope_l - slope_r) < 1e-4 and mT.N(2.0) > 0 and abs(far) < 1e-3 and chebT < 1e-12
check("B2", okB2, f"kappa* = {KSTAR:.6f}, r_c = {RC:.4f} M; transonic N(2M) = {mT.N(2.0):.6f}; algebraic residual "
      f"{alg:.1e}; slopes at r_c {slope_l:.6f}/{slope_r:.6f}; N/sqrt(e) - 1 at 200 M = {far:.2e}; every sigma >= 2 "
      f"benchmark has a valid p(2M) member", "residual <= 1e-10, slopes agree 1e-4, N(2M) > 0, |N/sqrt(e)-1| <= 1e-3")
check("B3", okB3, f"cap family (sigma < 1/2): all c in {C_GRID} regular (N(2M) > 0, w > 0 on [2, 200] M); "
      f"largest valid c per benchmark: min {min(cmax_rec.values()):.2f}, max {max(cmax_rec.values()):.2f}",
      "N(2M) > 0 and w > 0 for every c in the grid")
check("B4", okB4, f"intermediate sigma in [1/2, 2): a valid T member exists for every benchmark; OPEN: {b4_open}",
      "valid type-T or type-C member for each benchmark (A1(b))")
res["members"] = memrows
res["cmax"] = cmax_rec

# A4 conservation + C3 horizon finiteness on representative members
a4 = {}
xsA4 = [v for v in np.linspace(2.3, 11.5, 30) if abs(v - RC) > 0.05]
reps = {"T sigma=1.93e4 p(2M)=0": Member("T", 1.93e4, 1.5e-12, ph=0.0),
        "T sigma=0.63 p(2M)=-0.5": Member("T", 0.63, 6e-7, ph=-0.5),
        "C sigma=3e-5 c=0.3": Member("C", 3e-5, 1e-3, c=0.3),
        "C sigma=0.045 c=1.0": Member("C", 0.045, 6e-7, c=1.0)}
c3 = {}
for lab, m_ in reps.items():
    a4[lab] = conservation(m_, xsA4)
    Tn, _, _ = m_.stress(2.001)
    Tf, _, _ = m_.stress(2.5)
    en_, ef_ = eF(2.001), eF(2.5)
    vv = (abs(Tn[0] + Tn[3] / en_), abs(Tf[0] + Tf[3] / ef_))
    rrEF = (abs((Tn[1] - Tn[0]) / en_ - 2 * Tn[3] / en_ ** 2), abs((Tf[1] - Tf[0]) / ef_ - 2 * Tf[3] / ef_ ** 2))
    Jv = [m_.stress(v)[0][4] for v in (2.3, 4.0, 9.0)]
    c3[lab] = {"Tvv_2.001_vs_2.5": vv, "TrrEF_2.001_vs_2.5": rrEF, "J(2.3,4,9)": Jv, "c": m_.c,
               "r2Trt": [v * v * m_.stress(v)[0][3] for v in (2.3, 4.0, 9.0)]}
res["A4"] = a4
res["C3"] = c3
check("A4", max(a4.values()) <= 1e-5, f"radial conservation residual (relative) max {max(a4.values()):.2e} over "
      f"{list(a4.keys())}", "<= 1e-5 on [2.3, 11.5] M away from r_c")
okC3 = all(v["Tvv_2.001_vs_2.5"][0] <= 10 * max(v["Tvv_2.001_vs_2.5"][1], 1e-12) and
           v["TrrEF_2.001_vs_2.5"][0] <= 10 * max(v["TrrEF_2.001_vs_2.5"][1], 1e-12) for v in c3.values())
check("C3", okC3, "T^v_v and T_rr(EF) at 2.001 M vs 2.5 M: " +
      "; ".join(f"{k_}: {v['Tvv_2.001_vs_2.5'][0]:.2e}/{v['Tvv_2.001_vs_2.5'][1]:.2e}, "
                f"{v['TrrEF_2.001_vs_2.5'][0]:.2e}/{v['TrrEF_2.001_vs_2.5'][1]:.2e}" for k_, v in c3.items()),
      "finite at the horizon (<= 10 x the 2.5 M value) (A1(c))")
log(f"B/A4 done ({time.time() - T0:.1f} s)")

# C2 + observables per benchmark
log("")
log("C: observables (d ln X / d a_hat; physical shift = coefficient x a_hat)")
obs = {}
lin_max = 0.0
pg_zero = None
worst = {"shadow_dyn": 0.0, "shadow_local": 0.0, "r_ph": 0.0, "r_isco": 0.0, "Omega_isco": 0.0, "f_qnm": 0.0,
         "tau_qnm": 0.0}
worst_key = {}
for key, mems in members.items():
    nm = key.split("|")[0]
    row = memrows[key]
    ah = row["a_hat"]
    obs[key] = []
    for m_, ok, info in mems:
        if not ok:
            continue
        coef, lin, _ = response(m_, 50.0)
        lin_max = max(lin_max, lin)
        dyn = None
        if nm == "SgrA*":
            rdyn = R_DYN[nm] / row["r_g_m"]
            if m_.kind == "C":
                coefd, lind, mdyn = response(m_, rdyn, rdyn=rdyn)
                dyn = coefd["b_c"] - mdyn
            else:
                dyn = None      # screened member: near-zone mass offset bounded below by the C-member value (reported)
        elif nm == "M87*":
            law = (A0[key.split("|")[1]] * R_DYN[nm] ** 2 / (GMSUN * BH[nm]))   # unscreened offset a0/g_N(r_dyn)
            dyn = coef["b_c"] + law / ah
        rec = {"info": info, "coef": coef, "linearity": lin}
        vals = {"shadow_local": abs(coef["b_c"]) * ah, "r_ph": abs(coef["r_ph"]) * ah,
                "r_isco": abs(coef["r_isco"]) * ah, "Omega_isco": abs(coef["Omega_isco"]) * ah,
                "f_qnm": abs(coef["Omega_c"]) * ah, "tau_qnm": abs(coef["lambda_L"]) * ah}
        if dyn is not None:
            vals["shadow_dyn"] = abs(dyn) * ah
            rec["shadow_dyn_coef"] = dyn
        rec["shifts"] = vals
        obs[key].append(rec)
        for k_, v in vals.items():
            if v > worst[k_]:
                worst[k_], worst_key[k_] = v, key
res["observables"] = obs
# khronon-sector energy inflow on regular members: r^2 T^r_t = c (scaled; checked in C3) => dM/dt / M = c a0 / c_light
acc = {}
for key, mems in members.items():
    foot = key.split("|")[1]
    cs = [m_.c for m_, o, _ in mems if o]
    acc[key] = {"c_range": [min(cs), max(cs)], "Mdot_over_M_per_Gyr": [min(cs) * A0[foot] / c_SI * 3.15576e16,
                                                                       max(cs) * A0[foot] / c_SI * 3.15576e16]}
res["accretion_reading"] = acc
amax = max(v["Mdot_over_M_per_Gyr"][1] for v in acc.values())
log(f"  reading: regular members carry an ingoing khronon-sector energy flux r^2 T^r_t = c, dM/dt/M = c a0/c_light; "
    f"max over computed members {amax:.3e} per Gyr (SMBH cap family, c up to 1.0; c is not fixed here)")
res["worst_shifts"] = {k_: [v, worst_key.get(k_)] for k_, v in worst.items()}
# PG control: exact Schwarzschild => zero response


_hpg = sp.sqrt(2 / r) / (1 - 2 / r)
_fpg = sp.lambdify(r, [_hpg, sp.diff(_hpg, r), sp.diff(_hpg, r, 2)], "math")


class PG(Member):
    def __init__(self):
        self.kind, self.sigma, self.eps, self.c = "PG", 1.0, 0.0, 0.0

    def stress(self, x, far=False, xi_=None):
        h1, h2, h3 = _fpg(x)
        T = [float(v) for v in fT(x, 1.0, h1, h2, h3, 0.0, 0.0, 0.0, 1.0, 0.0, XI)]
        return T, (1.0, 0.0, 0.0), (0.0, 0.0, 0.0)


pgc, _, _ = response(PG(), 50.0)
pg_zero = max(abs(v) for v in pgc.values())
res["C2"] = {"linearity_max": lin_max, "PG_response_max": pg_zero}
check("C2", lin_max < 1e-3 and pg_zero < 1e-12, f"linearity (1e-6 vs 1e-7) max rel diff {lin_max:.2e}; PG control "
      f"max |coefficient| {pg_zero:.1e}", "< 1e-3 and PG exactly 0")
for k_, (v, kk) in res["worst_shifts"].items():
    log(f"  worst |shift| {k_:13s} = {v:.3e} ({kk})")
log(f"C done ({time.time() - T0:.1f} s)")

# ==================================================================================== PART D: neutron stars (SLy)
log("")
log("D: neutron stars (SLy as recalled in CFG318; static foliation, screened P)")
KAPPA = 7.42591549e-29 * 1e10
MSUN_KM = 1.4766250614
C_CGS = 2.99792458e10
CRUST = [(6.80110e-9, 1.58425, 0.0), (1.06186e-6, 1.28733, 2.44034e7), (5.32697e1, 0.62223, 3.78358e11),
         (3.99874e-8, 1.35692, 2.62780e12)]
SLY = (34.384, 3.005, 2.988, 2.851)


class PWP:
    def __init__(self, core):
        lp1, g1, g2, g3 = core
        rho1, rho2 = 10 ** 14.7, 10 ** 15.0
        K1 = 10 ** lp1 / C_CGS ** 2 / rho1 ** g1
        K2 = K1 * rho1 ** (g1 - g2)
        K3 = K2 * rho2 ** (g2 - g3)
        Kc, gc = CRUST[-1][0], CRUST[-1][1]
        rho0 = (Kc / K1) ** (1 / (g1 - gc))
        self.pieces = CRUST + [(K1, g1, rho0), (K2, g2, rho1), (K3, g3, rho2)]
        a = [0.0]
        for i in range(1, len(self.pieces)):
            Kp, gp, _ = self.pieces[i - 1]
            Kk, gg, rb = self.pieces[i]
            a.append(a[-1] + Kp * rb ** (gp - 1) / (gp - 1) - Kk * rb ** (gg - 1) / (gg - 1))
        self.a = a
        self.pb = [Kk * rb ** gg for (Kk, gg, rb) in self.pieces]

    def e_of_p(self, p):
        pc = p / KAPPA
        i = max(j for j in range(len(self.pieces)) if self.pb[j] <= pc)
        Kk, gg, _ = self.pieces[i]
        rho = (pc / Kk) ** (1 / gg)
        return ((1 + self.a[i]) * rho + Kk * rho ** gg / (gg - 1)) * KAPPA

    def p_of_rho(self, rho):
        i = max(j for j in range(len(self.pieces)) if self.pieces[j][2] <= rho)
        Kk, gg, _ = self.pieces[i]
        return Kk * rho ** gg * KAPPA


EOS = PWP(SLY)


def tov(rho_c, src=None, lam=0.0):
    """TOV in km; src = (rho_P(r), pr_P(r)) extra stress in km^-2 times lam (linear response)."""
    pc = EOS.p_of_rho(rho_c)
    p_stop = EOS.p_of_rho(1e4)
    ec = EOS.e_of_p(pc)

    def rhs(x, Y):
        m, p, ph = Y
        p = max(p, p_stop)
        e = EOS.e_of_p(p)
        rp, pr = (src[0](x), src[1](x)) if src is not None else (0.0, 0.0)
        dm = 4 * math.pi * x * x * (e + lam * rp)
        dph = (m + 4 * math.pi * x ** 3 * (p + lam * pr)) / (x * (x - 2 * m))
        return [dm, -(e + p) * dph, dph]
    r0 = 1e-5 / math.sqrt(ec)
    ev = lambda x, Y: Y[1] - p_stop
    ev.terminal = True
    ev.direction = -1
    sol = solve_ivp(rhs, [r0, 100.0], [4 * math.pi * ec * r0 ** 3 / 3, pc, 0.0], method="DOP853", rtol=1e-12,
                    atol=1e-40, events=ev, dense_output=True)
    return sol


def star_MR(rho_c, src=None, lam=0.0):
    sol = tov(rho_c, src, lam)
    return sol.y[0, -1] / MSUN_KM, sol.t[-1], sol


lrs = np.linspace(15.0, 15.6, 13)
ms_ = [star_MR(10 ** v)[0] for v in lrs]
i_ = int(np.argmax(ms_))
rmx = minimize_scalar(lambda v: -star_MR(10 ** v)[0], bounds=(lrs[max(i_ - 1, 0)], lrs[min(i_ + 1, 12)]),
                      method="bounded", options={"xatol": 1e-8})
MMAX, LRC_MAX = -rmx.fun, rmx.x
check("D1", abs(MMAX - 2.0485) <= 0.002, f"SLy M_max = {MMAX:.5f} Msun at log10 rho_c = {LRC_MAX:.5f}",
      "2.0485 +- 0.002 (CFG318's in-lane value)")
lr14 = brentq(lambda v: star_MR(10 ** v)[0] - 1.4, 14.5, LRC_MAX, xtol=1e-10)


def ns_response(lrc, a0, Lpc):
    M_, R_, sol = star_MR(10 ** lrc)
    Mkm = M_ * MSUN_KM
    phR = sol.y[2, -1]
    shift = 0.5 * math.log(1 - 2 * Mkm / R_) - phR          # lapse N(R) = sqrt(1 - 2M/R)
    ah = a0 * (Mkm * 1e3) / c_SI ** 2
    sigma = a0 * (Lpc * PC) ** 2 / (2 * GMSUN * M_)
    eps_ = MU_K ** 2 * GMSUN * M_ / a0
    xR = R_ / Mkm
    Nin = lambda x: math.exp(float(sol.sol(x * Mkm)[2]) + shift)
    Fin = lambda x: 1 - 2 * float(sol.sol(x * Mkm)[0]) / (x * Mkm)
    lo = 1e-3
    cNn = chebfit(Nin, lo, xR, 90)
    cFn = chebfit(Fin, lo, xR, 90)
    cPh = chebfit(lambda x: math.log(Nin(x) / math.sqrt(Fin(x))), lo, xR, 90)
    integ = lambda x: x * x * (1 - cNn(x)) / (sigma * cNn(x) * math.sqrt(cFn(x)))   # (r^2 p)' = r^2 D/sqrt(F)
    cIg = chebfit(integ, lo, xR, 240)
    cI = cIg.integ(lbnd=lo)
    pfun = lambda x: cI(x) / x ** 2
    cp = chebfit(pfun, lo, xR, 90)
    xg = np.linspace(0.02, xR * 0.999, 400)
    # p equation (screened, w = 0) integrated once with the far-field constant: sigma N D + N = 1,
    # D = sqrt(F) (r^2 p)'/r^2; residual of that first integral on [0.05, 0.999] R
    NDf = lambda x: cNn(x) * math.sqrt(cFn(x)) * cIg(x) / x ** 2
    respe = max(abs(sigma * NDf(x) + cNn(x) - 1) / abs(1 - cNn(x)) for x in np.linspace(0.05 * xR, 0.999 * xR, 300))
    umax = float(max(abs(pfun(x)) for x in xg))
    T = np.array([[float(v) for v in fTN(x, cPh(x), cPh.deriv()(x), cPh.deriv(2)(x), cPh.deriv(3)(x),
                                          cFn(x), cFn.deriv()(x), cFn.deriv(2)(x), cFn.deriv(3)(x),
                                          cp(x), cp.deriv()(x), cp.deriv(2)(x), sigma, eps_, XI)] for x in xg])
    rhoP = -T[:, 0] * ah / (4 * math.pi) / Mkm ** 2       # km^-2  (T_phys = (a_hat/K) T_tilde, K = 4 pi)
    prP = T[:, 1] * ah / (4 * math.pi) / Mkm ** 2
    rkg = xg * Mkm
    srcf = (lambda x: float(np.interp(x, rkg, rhoP)), lambda x: float(np.interp(x, rkg, prP)))
    ecen = EOS.e_of_p(EOS.p_of_rho(10 ** lrc))
    lam0 = 1e-6 * ecen / max(np.max(np.abs(rhoP)), np.max(np.abs(prP)))
    out = []
    for lamb in (lam0, 2 * lam0):
        M2, R2, _ = star_MR(10 ** lrc, srcf, lamb)
        out.append(((M2 / M_ - 1) / lamb, (R2 / R_ - 1) / lamb))
    linr = max(abs(out[0][0] - out[1][0]) / max(abs(out[0][0]), 1e-300),
               abs(out[0][1] - out[1][1]) / max(abs(out[0][1]), 1e-300))
    a_orb = 1e9 / (Mkm * 1e3)
    dM_timing = ah * (a_orb ** 2 - xR ** 2) / (2 * sigma)   # screened hedgehog mass between R and a (weak field)
    return {"M": M_, "R_km": R_, "sigma": sigma, "a_hat": ah, "dlnM": out[0][0], "dlnR": out[0][1], "linearity": linr,
            "p_eq_residual": float(respe), "u_over_a0_max": umax, "timing_mass_offset": dM_timing,
            "(R/L*)^2": (R_ * 1e3 / (Lpc * PC)) ** 2, "lambda_used": lam0}


ns = {}
for foot, a0 in A0.items():
    for Lpc in LSTARS:
        ns[f"1.4|{foot}|{Lpc}pc"] = ns_response(lr14, a0, Lpc)
        ns[f"Mmax|{foot}|{Lpc}pc"] = ns_response(LRC_MAX, a0, Lpc)
res["NS"] = ns
d2ok = all(v["p_eq_residual"] <= 1e-8 and v["u_over_a0_max"] < 1 for v in ns.values())
check("D2", d2ok, f"screened static P on SLy stars: max p-eq residual {max(v['p_eq_residual'] for v in ns.values()):.1e}; "
      f"max u/a0 {max(v['u_over_a0_max'] for v in ns.values()):.2e}", "p equation residual <= 1e-8 and u/a0 < 1 "
      "(cap not reached)")
check("D3", max(v["linearity"] for v in ns.values()) <= 1e-3,
      f"linear response: max rel diff between amplifications {max(v['linearity'] for v in ns.values()):.2e}", "<= 1e-3")
dR = max(abs(v["dlnR"]) for k_, v in ns.items() if k_.startswith("1.4"))
dMm = max(abs(v["dlnM"]) for k_, v in ns.items() if k_.startswith("Mmax"))
dT = max(v["timing_mass_offset"] for v in ns.values())
log(f"  NS: max |dR/R| (1.4 Msun) = {dR:.3e}; max |dM_max/M_max| = {dMm:.3e}; timing-mass offset <= {dT:.3e}")
log(f"D done ({time.time() - T0:.1f} s)")

# ==================================================================================== PART E: strong coupling
log("")
log("E: strong coupling (decoupling limit tau = Qbar t + pi; P integrated out at tree level)")
z_ = sp.Symbol("z", real=True)
ep = sp.Symbol("epsilon")
gg, Qb = sp.symbols("g Qbar", positive=True)
pt_, pz_, ptt_, ptz_, pzz_ = sp.symbols("pi_t pi_z pi_tt pi_tz pi_zz", real=True)
Nb = 1 + gg * z_                                    # frozen lapse with gradient g (A0 = g z-hat at z = 0)
Xe = (Qb + ep * pt_) ** 2 / Nb ** 2 - ep ** 2 * pz_ ** 2    # Q^2 for tau = Qbar t + eps pi on -Nb^2 dt^2 + dx^2


def Dz_(f_):
    return sp.diff(f_, z_) + ptz_ * sp.diff(f_, pt_) + pzz_ * sp.diff(f_, pz_)


def Dt_(f_):
    return ptt_ * sp.diff(f_, pt_) + ptz_ * sp.diff(f_, pz_)


lnNt = -sp.log(Xe) / 2
n_t, n_z = -(Qb + ep * pt_) / sp.sqrt(Xe), -ep * pz_ / sp.sqrt(Xe)
nU_t, nU_z = -n_t / Nb ** 2, n_z
Az = Dz_(lnNt) + n_z * (nU_t * Dt_(lnNt) + nU_z * Dz_(lnNt))
Azs = sp.series(Az, ep, 0, 3).removeO()


def jrep(e_):
    return sp.expand(sp.simplify(e_).subs(z_, 0))


A0z = jrep(Azs.coeff(ep, 0))
A1z = jrep(Azs.coeff(ep, 1))
A2z = jrep(Azs.coeff(ep, 2))
log(f"  E1: background A_z = {sp.simplify(A0z)}; dA_1,z = {sp.simplify(A1z)}")
log(f"  E3: dA_2,z = {sp.simplify(A2z)}")
w_, k_ = sp.symbols("omega k", positive=True)
Kk, gLs, ML, N0s = sp.symbols("K gamma_L M_L N0", positive=True)
# leading WKB (g -> 0 in dA_1): dA_1 = -pi_tz/Qbar -> |dA_1|^2 = k^2 w^2 |pi|^2/Qbar^2
dA1_lead = sp.simplify(A1z.subs(gg, 0))
ZP = sp.simplify((dA1_lead.subs(ptz_, 1) ** 2) * k_ ** 2 / (Kk * ML + gLs * k_ ** 2))   # coefficient of w^2|pi|^2
ZP_expected = k_ ** 2 / (Qb ** 2 * (Kk * ML + gLs * k_ ** 2))
e1 = sp.simplify(ZP - ZP_expected)
check("E1", e1 == 0 and sp.simplify(dA1_lead + ptz_ / Qb) == 0,
      f"dA_1,z (leading WKB) = {dA1_lead}; Z_P(k) = {ZP} (minus k^2/(Qbar^2 (K M_L + gL k^2)): {e1}); "
      f"dust kinetic term mu^2/K in this normalisation (E3 expansion)", "Z_P = k^2/(Qbar^2 (K M_L + gamma_L k^2)) exactly")
# E2(i): unitary gauge, lapse n and longitudinal p_z, Hermitian form L = v^dagger Mu v (time-averaged plane waves)
Mu = sp.Matrix([[0, sp.I * k_ / 2], [-sp.I * k_ / 2, -N0s * (Kk * ML + gLs * k_ ** 2) / 2]])
Schur = sp.simplify(Mu[0, 0] - Mu[0, 1] * Mu[1, 1] ** -1 * Mu[1, 0])
Zu = sp.simplify(2 * Schur * N0s ** 2 / Qb ** 2)            # n = -N0 pidot/Qbar
e2i = sp.simplify(Zu.subs(N0s, 1) - ZP)
log(f"  E2(i): unitary-gauge Schur complement {Schur} |n|^2 -> Z = {Zu}; minus E1's Z_P at N0 = 1: {e2i}")
# E3: cubic and quartic vertices. With P integrated out at tree level the P sector gives
# dA1.G.dA2 + (1/2) dA2.G.dA2 - (K^3 W3/6) dP^3 (W3 = third derivative of W);
# in the screened regime G -> 1/(gamma_L k^2) on longitudinal vectors, so a gradient part dA2 = d_z chi2 gives the local
# vertex (1/gamma_L) pi_t chi2 = Z_P pi_t chi2. Monomials: pi_t pi_tz = d_z(pi_t^2/2), pi_z pi_zz = d_z(pi_z^2/2), pi_tt pi_z
# (the tilt term, not a gradient).
poly2 = sp.Poly(A2z.subs({Qb: 1, gg: 0}), pt_, pz_, ptt_, ptz_, pzz_)
mon = {sp.Mul(*[g_ ** e__ for g_, e__ in zip((pt_, pz_, ptt_, ptz_, pzz_), m__)]): sp.nsimplify(cc)
       for m__, cc in poly2.as_dict().items()}
c_tt = float(mon.get(pt_ * ptz_, 0))
c_zz = float(mon.get(pz_ * pzz_, 0))
c_tilt = float(mon.get(ptt_ * pz_, 0))
other = {str(k__): str(v) for k__, v in mon.items() if k__ not in (pt_ * ptz_, pz_ * pzz_, ptt_ * pz_)}
qq, gr, muS = sp.symbols("qd gr mu")
Qexp = Qb * sp.sqrt((1 + ep * qq / Qb) ** 2 - ep ** 2 * gr ** 2 / Qb ** 2)
KQs = sp.series(muS ** 2 * (Qexp - 1) ** 2 / (2 * Kk), ep, 0, 4).removeO()
Kc2, Kc3 = sp.factor(sp.expand(KQs.coeff(ep, 2))), sp.factor(sp.expand(KQs.coeff(ep, 3)))
VERT = {"V1 pidot (grad pi)^2 [clock]": "lam = Z_P c_zz/2",
        "V2 pidot^3 [clock]": "lam = Z_P c_tt/2",
        "V3 pidot d^-1(pi_tt grad pi) [tilt]": "lam = Z_P |c_tilt|",
        "V4 (grad pi)^4 [clock, quartic]": "lam4 = Z_P (c_zz/2)^2/2",
        "V5 pidot (grad pi)^2 [K(Q) dust]": "lam = mu^2/(2 K Qbar^2)",
        "V6 pidot^3 [W cubic]": "lam = W3 k^3/(6 (M + L*^2 k^2/2)^3), W3 = 2 a0^2/(K (a0 - u0)^3)"}
log(f"  E3: dA_2,z = c_tt pi_t pi_tz + c_zz pi_z pi_zz + c_tilt pi_tt pi_z (+ g terms) with c_tt = {c_tt}, c_zz = {c_zz}, "
    f"c_tilt = {c_tilt}; other monomials {other}")
log(f"  E3: K(Q) quadratic {Kc2}; cubic {Kc3}")
for k__, v in VERT.items():
    log(f"      {k__}: {v}")
res["E1"] = {"A0z": str(A0z), "dA1": str(A1z), "Z_P": str(ZP)}
res["E2"] = {"Schur": str(Schur), "Z_unitary": str(Zu), "difference": str(e2i)}
res["E3"] = {"dA2": str(A2z), "c_tt": c_tt, "c_zz": c_zz, "c_tilt": c_tilt, "other": other,
             "KQ_quadratic": str(Kc2), "KQ_cubic": str(Kc3), "vertices": VERT}


# E2(ii): G from the exact spherical first integral, static radial tilt about the static foliation (N^2 = e):
# c = r^2 h' G_eff with G_eff (scaled) = e^2 [D (1 + sigma D) + eps (1 - N)/N^2]
def Gw(e, Dt, sigma, eps_):
    N = math.sqrt(e)
    return e * e * (Dt * (1 + sigma * Dt) + eps_ * (1 - N) / N ** 2)


rat = []
for oneme in (1e-5, 1e-6):
    e = 1 - oneme
    N = math.sqrt(e)
    Dt = (1 - N) / (2.0 * N)
    rat.append(Gw(e, Dt, 2.0, 1e-3) / (Dt * (1 + 2.0 * Dt) + 1e-3 * (1 - N)))
e2ok = (e2i == 0) and all(abs(v - 1) < 1e-3 for v in rat)
check("E2", e2ok, f"(i) unitary-gauge Z - E1 Z_P = {e2i}; (ii) G_eff / [D.P (1 + gL D.P) + mu^2 (Qbar - 1)/K] at "
      f"1 - e = 1e-5, 1e-6: {[f'{v:.6f}' for v in rat]}", "(i) 0; (ii) within 1e-3 of 1 (A2)")
check("E3", c_zz != 0 and np.isfinite(c_tt + c_zz + c_tilt) and not other,
      f"clock-nonlinearity coefficients c_tt = {c_tt}, c_zz = {c_zz}, c_tilt = {c_tilt} (exact); K(Q) cubic {Kc3}",
      "derived exactly; no other monomials at g = 0")
SQK = math.sqrt(4 * math.pi) * LPLANCK                     # K^(1/2) in m (hbar = c = 1, G = l_P^2)


def scales(zh, zPh, gh, kk, om, a0m, du, Mkk, Lm, Qbar):
    """hatted quantities in m^-2: zh = K Z, zPh = K Z_P, gh = K G. Lambda per vertex (m^-1), eps = (E/Lambda)^4.
    Cubic with n_x spatial derivatives: Lambda^2 = Z^(3/2) c^(3/2 + n_x)/lam; quartic (grad pi)^4: Lambda^4 = Z^2 c^7/lam4."""
    if gh <= 0:
        return {"c_pi": None, "G<=0": True}
    cpi = math.sqrt(gh / zh)
    E = max(om / c_SI, cpi * kk)
    lam = {"V1 pidot (grad pi)^2 [clock]": (zPh * abs(c_zz) / 2, 2),
           "V2 pidot^3 [clock]": (zPh * abs(c_tt) / 2, 0),
           "V3 pidot d^-1(pi_tt grad pi) [tilt]": (zPh * abs(c_tilt), 0),
           "V5 pidot (grad pi)^2 [K(Q) dust]": (MU_K ** 2 / (2 * Qbar ** 2), 2),
           "V6 pidot^3 [W cubic]": (a0m ** 2 * kk ** 3 / (3 * du ** 3 * (Mkk + Lm ** 2 * kk ** 2 / 2) ** 3), 0)}
    out = {"c_pi": cpi, "E_m-1": E, "Z_hat": zh, "ZP_hat": zPh, "G_hat": gh, "vertices": {}}
    worst_ = (0.0, None)
    for vn, (lh, nx) in lam.items():
        if lh <= 0:
            continue
        L2_ = zh ** 1.5 * cpi ** (1.5 + nx) / (lh * SQK)
        Lam_ = math.sqrt(L2_)
        ep_ = (E / Lam_) ** 4
        out["vertices"][vn] = {"Lambda_m-1": Lam_, "eps": ep_, "k_sc_m-1": Lam_ / cpi}
        worst_ = max(worst_, (ep_, vn))
    l4 = zPh * (abs(c_zz) / 2) ** 2 / 2
    Lam4 = (zh ** 2 * cpi ** 7 / (l4 * SQK ** 2)) ** 0.25
    ep4 = (E / Lam4) ** 4
    out["vertices"]["V4 (grad pi)^4 [clock, quartic]"] = {"Lambda_m-1": Lam4, "eps": ep4, "k_sc_m-1": Lam4 / cpi}
    worst_ = max(worst_, (ep4, "V4 (grad pi)^4 [clock, quartic]"))
    out["eps_max"], out["worst_vertex"] = worst_
    out["mixing_eps"] = math.sqrt(zPh) * cpi / max(om / c_SI, cpi * kk)     # pi-metric mixing (A2), leakage ~ eps^2
    return out


def zP_of(kk, Lm, Mkk=1.0, Qbar=1.0):
    return kk ** 2 / (Qbar ** 2 * (Mkk + Lm ** 2 * kk ** 2 / 2))


sysres = {}
okE4 = True
ePASS, eFAIL = True, False
gneg = []
for foot, a0 in A0.items():
    a0m = a0 / c_SI ** 2
    for Lpc in LSTARS:
        L = Lpc * PC
        hed = lambda Phi_c2: 2 * Phi_c2 / L ** 2              # K D.P = 2 (1 - N)/(N L*^2), weak-field screened hedgehog
        phE = 3.986e14 / (6.371e6 * c_SI ** 2)
        phS = GMSUN / (AU * c_SI ** 2)
        phB = 2.59 * GMSUN / (8.79e8 * c_SI ** 2)
        systems = {   # k (m^-1), omega (s^-1), K D.P (m^-2), Qbar - 1, u0 (m^-1), M_kk
            "Eot-Wash (38.6 um)": (1 / 38.6e-6, 1e-3, hed(phS + phE), 1e-6, 2 * (phS + phE) / L, 1.0),
            "planets (1 AU)": (1 / AU, 2 * math.pi / 3.15576e7, hed(phS), 1e-6, 2 * phS / L, 1.0),
            "double pulsar": (1 / 8.79e8, 2 * math.pi / (2.45 * 3600), hed(phB), 1e-6, 2 * phB / L, 1.0),
            "galaxy (1 kpc; phantom 0.01 Msun/pc^3, ILLUSTRATIVE)": (1 / KPC, 200e3 / (10 * KPC),
                                                                       4 * math.pi * G_SI * 6.8e-22 / c_SI ** 2, 1e-6,
                                                                       a0m / 2, 4.0),
            "cosmology (10 h/Mpc; FRW, P0 = 0)": (10 * 0.675 / (1e3 * KPC), 2.2e-18, 0.0, 2e-10, 0.0, 1.0),
        }
        for sname, (kk, om, dP, Qm1, u0m, Mkk) in systems.items():
            Qbar = 1 + Qm1
            zPh = zP_of(kk, L, Mkk, Qbar)
            zh = zPh + MU_K ** 2
            gh = dP * (1 + dP * L ** 2 / 2) + MU_K ** 2 * Qm1 / Qbar
            sysres[f"{sname}|{foot}|{Lpc}pc"] = scales(zh, zPh, gh, kk, om, a0m, a0m - u0m, Mkk, L, Qbar)
        # strong-field: benchmark solutions at r = 3 M; NS surface
        for nm in ("BH10", "BH63", "SgrA*", "M87*"):
            ah, sigma, eps_, rg = scaled(BH[nm], a0, Lpc)
            key = f"{nm}|{foot}|{Lpc}pc"
            m_ = [m__ for m__, o, _ in members[key] if o][0]
            Nx = m_.N(3.0)
            e3 = eF(3.0)
            if m_.kind == "C":
                Dt = 2 * Nx / 3.0
                w3 = m_.N(3.0, 1) + sigma * (4 * Nx * m_.N(3.0, 1) / 3.0 - 2 * Nx ** 2 / 9.0)
                Mkk = (1 + w3 / ah) ** 2                      # M_L = (a0/(a0 - u))^2 at the cap
                du = (a0 / c_SI ** 2) * ah / (w3 + ah)           # a0 - u at the cap
            else:
                p3 = m_.p(3.0)[0]
                Dt = (1 - Nx) / (sigma * Nx)
                Mkk = (1 / (1 - abs(p3))) ** 2
                du = (a0 / c_SI ** 2) * (1 - abs(p3))
            gh = (ah / rg ** 2) * e3 ** 2 * (Dt * (1 + sigma * Dt) + eps_ * (1 - Nx) / Nx ** 2)
            kk = 1 / rg
            Qbar = 1 / Nx
            zPh = zP_of(kk, L, Mkk, Qbar)
            zh = zPh + MU_K ** 2
            om = c_SI / (3 * math.sqrt(3) * rg)
            s_ = scales(zh, zPh, gh, kk, om, a0m, du, Mkk, L, Qbar)
            sysres[f"{nm} (r = 3M)|{foot}|{Lpc}pc"] = s_
        nsr = ns[f"1.4|{foot}|{Lpc}pc"]
        Rm = nsr["R_km"] * 1e3
        eR = 1 - 2 * 1.4 * GMSUN / (Rm * c_SI ** 2)
        NR = math.sqrt(eR)
        gh = 2 * eR ** 2 * (1 - NR) / (NR ** 2 * L ** 2)
        zPh = zP_of(1 / Rm, L, 1.0, 1 / NR)
        sysres[f"NS surface|{foot}|{Lpc}pc"] = scales(zPh + MU_K ** 2, zPh, gh, 1 / Rm, c_SI / Rm, a0m, a0m, 1.0, L, 1 / NR)
for k_, s_ in sysres.items():
    if s_.get("G<=0"):
        gneg.append(k_)
        continue
    vals = [v["eps"] for v in s_["vertices"].values()] + [v["Lambda_m-1"] for v in s_["vertices"].values()]
    if not all(np.isfinite(vals)):
        okE4 = False
    if s_["eps_max"] > 1e-2:
        ePASS = False
    if s_["eps_max"] / (16 * math.pi ** 2) >= 1:
        eFAIL = True
res["E4"] = sysres
res["E4_G_nonpositive"] = gneg
check("E4", okE4, f"scales computed for {len(sysres)} system x footing x L* rows; G <= 0 (pair not propagating stably): "
      f"{gneg}", "all finite")
worst_e = max((s_["eps_max"], k_, s_["worst_vertex"]) for k_, s_ in sysres.items() if not s_.get("G<=0"))
dpm = max(s_["mixing_eps"] for k_, s_ in sysres.items() if k_.startswith("double pulsar"))
res["double_pulsar_mixing_eps_max"] = dpm
log(f"  E4 reading: double-pulsar pi-metric mixing eps <= {dpm:.2e} (energy leakage ~ eps^2 = {dpm ** 2:.1e}; "
    f"Pdot_b precision 6.3e-5)")
log(f"  E4 worst loop factor eps = {worst_e[0]:.3e} at {worst_e[1]} ({worst_e[2]})")
for k_ in [k_ for k_ in sysres if "canonical|24pc" in k_ or k_.startswith("Eot")]:
    s_ = sysres[k_]
    if s_.get("G<=0"):
        log(f"    {k_:62s}: G <= 0")
        continue
    v1 = s_["vertices"]["V1 pidot (grad pi)^2 [clock]"]
    log(f"    {k_:62s}: c_pi {s_['c_pi']:.3e}  E {s_['E_m-1']:.3e} m^-1  V1 k_sc {v1['k_sc_m-1']:.3e} m^-1  "
        f"eps_max {s_['eps_max']:.3e} ({s_['worst_vertex']})")

# ==================================================================================== VERDICTS
log("")
log("VERDICTS (frozen rules, section 3 + amendments)")
bh_exist = okB2 and okB3 and okB4
bh_shift = max(worst[k_] for k_ in ("shadow_dyn", "shadow_local", "r_ph", "r_isco", "Omega_isco"))
if bh_exist and bh_shift <= 1e-2:
    V1 = "PASS"
elif bh_shift > 0.10:
    V1 = "FAIL"
else:
    V1 = "OPEN"
mix = max((s_.get("mixing_eps", 0.0) or 0.0) for k_, s_ in sysres.items() if "r = 3M" in k_)
mixkey = max(((s_.get("mixing_eps", 0.0) or 0.0), k_) for k_, s_ in sysres.items() if "r = 3M" in k_)[1]
qnm = max(worst["f_qnm"], worst["tau_qnm"])
V2 = "PASS" if (mix ** 2 <= 1e-2 and qnm <= 1e-2) else ("FAIL" if (mix ** 2 > 3e-2 or qnm > 3e-2) else "OPEN")
nsmax = max(dR, dMm, dT)
V3 = "PASS" if nsmax <= 1e-2 else ("FAIL" if nsmax > 0.1 else "OPEN")
if e2ok and ePASS:
    V4 = "PASS"
elif e2ok and eFAIL:
    V4 = "FAIL"
else:
    V4 = "OPEN"
leafok = True
for key, mems in members.items():
    for m_, o, info in mems:
        if o:
            leafok &= info.get("N(2M)", 1) > 0 and (m_.kind == "C" or info.get("max|p|", 0) < 1.0)
leafok &= all(v["u_over_a0_max"] < 1 for v in ns.values())
V5 = "PASS" if leafok else "FAIL"
res["verdicts"] = {"V1_black_holes": V1, "V2_ringdown": V2, "V3_neutron_stars": V3, "V4_strong_coupling": V4,
                   "V5_strong_field_leaf": V5,
                   "numbers": {"bh_max_shift": bh_shift, "qnm_max_shift": qnm, "mixing_eps_max": mix,
                               "ns_max": nsmax, "E4_worst": worst_e, "E4_G_nonpositive": gneg}}
log(f"  V1 black holes (EHT): {V1}  (max |shift| {bh_shift:.3e}; regular members exist: {bh_exist}; B4 OPEN: {b4_open})")
log(f"  V2 ringdown: {V2}  (eikonal max |shift| {qnm:.3e}; mixing eps max {mix:.3e} at {mixkey}; leakage eps^2 {mix ** 2:.1e})")
log(f"  V3 neutron stars: {V3}  (|dR/R| {dR:.3e}, |dMmax/Mmax| {dMm:.3e}, timing-mass {dT:.3e})")
log(f"  V4 strong coupling: {V4}  (worst eps {worst_e[0]:.3e} at {worst_e[1]}; E2 {e2ok})")
log(f"  V5 strong-field leaf condition (static spherical): {V5}")

npass = sum(c_["pass"] for c_ in checks)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
log(f"run: {time.time() - T0:.1f} s, peak RSS {rss:.2f} GB, single thread")
log(f"P3_V3_STRONG_FIELD COMPLETE: {npass}/{len(checks)} checks PASS.")
res["checks"] = checks
res["runtime_s"] = time.time() - T0
res["peak_rss_GB"] = rss


def clean(o):
    if isinstance(o, dict):
        return {str(k_): clean(v) for k_, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, float) and not np.isfinite(o):
        return str(o)
    return o


with open(JSON, "w") as fh:
    json.dump(clean(res), fh, indent=1, default=str)
with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
sys.exit(0 if npass == len(checks) else 1)
