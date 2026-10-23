#!/usr/bin/env python3
"""v3 constraint algebra (FROZEN_CRITERIA.md, committed e86f83df5e before this script existed).

v3 in unitary gauge (tau = t, Q = 1/N, A_i = d_i ln N; H4 FROZEN_CRITERIA L33; C4):
  H_T = int { N[(sqrt h/4K)(2 Lambda - R3) + (4K/sqrt h)(pi_ij pi^ij - pi^2/2) + sqrt h D.P + sqrt h W
              + (gamma_L/2) sqrt h (D.P)^2] - sqrt h mu_K^2 (1 - N)^2/(2 K N) + N^i H_i },   pi_P ~ 0 (eta = 0).
V1 exact reduced scalar sector (k || x) Dirac chain + bracket rank on four backgrounds; V2 frozen-coefficient 3D
symbol of the multiplier matrix A (sympy identity + sweep); V3 J(Y) vs P-sector lapse operator; V4 H4's rho_tau < 0
regions vs the degeneracy locus.  --mutate deletes the clock term.
"""
import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
clock = 0 if MUTATE else 1
checks, out = [], {"mutate": MUTATE}


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


# ================================================================ V1: exact reduced scalar sector
X = sp.symbols("X", real=True)
K, gL, mu, lam, k = sp.symbols("K gamma_L mu_K Lambda k", positive=True)
names_q, names_p = ["a", "b", "P", "N", "s"], ["p_a", "p_b", "Pi", "p_N", "p_s"]
Q = [sp.Function(n)(X) for n in names_q]
Pm = [sp.Function(n)(X) for n in names_p]
a, b, P, N, s = Q
pa, pb, Pi, pN, ps = Pm
hm = sp.diag(1 + a, 1 + b, 1 + b)
hinv = hm.inv()
crd = [X, sp.Symbol("Y"), sp.Symbol("Z")]
Gam = [[[sp.simplify(sum(hinv[kk, l] * (sp.diff(hm[j, l], crd[i]) + sp.diff(hm[i, l], crd[j]) - sp.diff(hm[i, j], crd[l]))
                         for l in range(3)) / 2) for j in range(3)] for i in range(3)] for kk in range(3)]
Ric = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Ric[i, j] = (sum(sp.diff(Gam[kk][i][j], crd[kk]) for kk in range(3))
                     - sum(sp.diff(Gam[kk][i][kk], crd[j]) for kk in range(3))
                     + sum(Gam[kk][kk][l] * Gam[l][i][j] for kk in range(3) for l in range(3))
                     - sum(Gam[kk][j][l] * Gam[l][i][kk] for kk in range(3) for l in range(3)))
R3 = sp.simplify(sum(hinv[i, j] * Ric[i, j] for i in range(3) for j in range(3)))
sh = sp.sqrt(1 + a) * (1 + b)
pi_sq = (1 + a) ** 2 * pa ** 2 + 2 * (1 + b) ** 2 * (pb / 2) ** 2
pi_tr = (1 + a) * pa + (1 + b) * pb
shDP = sp.diff((1 + b) * P / sp.sqrt(1 + a), X)       # sqrt h D.P
DP = shDP / sh
Wd = K * P ** 2 / (2 * (1 + a))                         # W = u^2/(2K), u^2 = K^2 h^xx P^2 (fixes 2nd derivatives at P = 0)
G = ((sh / (4 * K)) * (2 * lam - R3) + (4 * K / sh) * (pi_sq - pi_tr ** 2 / 2) + clock * shDP + sh * Wd
     + (gL / 2) * sh * DP ** 2)
Hx = -2 * sp.diff((1 + a) * pa, X) + sp.diff(a, X) * pa + sp.diff(b, X) * pb - sp.diff(Pi, X) * P
HT = N * G - sh * mu ** 2 * (1 - N) ** 2 / (2 * K * N) + s * Hx


def vder(dens, f, maxm=6):
    o = sp.diff(dens, f)
    for m in range(1, maxm + 1):
        dm = sp.Derivative(f, (X, m))
        if dens.has(dm):
            o += (-1) ** m * sp.diff(sp.diff(dens, dm), X, m)
    return o


CN = vder(HT, N)       # {p_N, H_T} = -CN
phiP = vder(HT, P)     # {Pi, H_T}  = -phiP
dQ = [sp.Function("d" + n)(X) for n in names_q]
dP = [sp.Function("d" + n)(X) for n in names_p]
ep = sp.symbols("ep")


def linearise(C, bg):
    sub = {f: bg[f] + ep * df for f, df in zip(Q + Pm, dQ + dP)}
    return sp.expand(sp.simplify(sp.diff(C.subs(sub).doit(), ep).subs(ep, 0)))


def coeffs(C, f, maxm=8):
    o = {}
    for m in range(maxm, 0, -1):
        dm = sp.Derivative(f, (X, m))
        if C.has(dm):
            o[m] = sp.diff(C, dm)
            C = sp.expand(C - o[m] * dm)
    if C.has(f):
        o[0] = sp.diff(C, f)
    return o


def symbol(C1, C2):
    tot = 0
    for qf, pf in zip(dQ, dP):
        c1q, c1p, c2q, c2p = coeffs(C1, qf), coeffs(C1, pf), coeffs(C2, qf), coeffs(C2, pf)
        s1q = sum(c * (sp.I * k) ** m for m, c in c1q.items())
        s1p = sum(c * (sp.I * k) ** m for m, c in c1p.items())
        s2q = sum(c * (-sp.I * k) ** m for m, c in c2q.items())
        s2p = sum(c * (-sp.I * k) ** m for m, c in c2p.items())
        tot += s1q * s2p - s1p * s2q
    return sp.simplify(tot)


qs, q1s = sp.symbols("q q1", real=True)
base = {a: 0, b: 0, P: 0, Pi: 0, s: 0, pN: 0, ps: 0}
par = {K: 1, gL: sp.Rational(3, 10)}
backgrounds = {}
backgrounds["B1 Minkowski, mu_K = 0"] = ({**base, N: 1, pa: 0, pb: 0}, {**par, lam: 0, mu: 0})
backgrounds["B2 Minkowski, mu_K = 0.3"] = ({**base, N: 1, pa: 0, pb: 0}, {**par, lam: 0, mu: sp.Rational(3, 10)})
N0 = sp.Rational(9, 10)
p3 = {**par, lam: sp.Rational(1, 2), mu: sp.Rational(3, 10)}
CN3 = sp.simplify(CN.subs({**base, N: N0, pa: qs, pb: 2 * qs}).doit().subs(p3))
q3 = [r for r in sp.solve(CN3, qs) if r.is_real and r > 0][0]
backgrounds["B3 FRW point, BS dust (N0 = 0.9)"] = ({**base, N: N0, pa: q3, pb: 2 * q3}, p3)
q2 = sp.Rational(2, 5)
CN4 = sp.simplify(CN.subs({**base, N: N0, pa: q1s, pb: 2 * q2}).doit().subs(p3))
q4 = max([r for r in sp.solve(CN4, q1s) if r.is_real], key=lambda r: float(r))
backgrounds["B4 sheared momentum + BS dust"] = ({**base, N: N0, pa: q4, pb: 2 * q2}, p3)

cons_full = [pN, ps, Pi, CN, Hx, phiP]
names = ["p_N", "p_s", "Pi", "C_N", "H_x", "phi_P"]
V1 = {}
v1_ok = True
for label, (bg, pv) in backgrounds.items():
    resid = [sp.simplify(C.subs(bg).doit().subs(pv)) for C in (CN, Hx, phiP)]
    lin = [linearise(C, bg).subs(pv) for C in cons_full]
    M = sp.zeros(6, 6)
    for i in range(6):
        for j in range(6):
            M[i, j] = sp.simplify(symbol(lin[i], lin[j]))
    zero_rows = [names[i] for i in range(6) if all(sp.simplify(M[i, j]) == 0 for j in range(6))]
    Amat = sp.Matrix([[M[3, 0], M[3, 2]], [M[5, 0], M[5, 2]]])     # {C_N, p_N} {C_N, Pi}; {phi_P, p_N} {phi_P, Pi}
    detA = sp.factor(sp.simplify(Amat.det()))
    ranks = {str(kv): int(M.subs(k, kv).rank(simplify=True)) for kv in (sp.Rational(7, 10), sp.Rational(13, 10), 3)}
    r = ranks["13/10"]
    dof = sp.Rational(10 - 2 * (6 - r) - r, 2)
    ok = (all(x == 0 for x in resid) and all(v == 4 for v in ranks.values()) and sorted(zero_rows) == ["H_x", "p_s"]
          and detA != 0)
    v1_ok &= ok
    V1[label] = {"residuals": [str(x) for x in resid], "ranks": ranks, "zero_rows": zero_rows, "det_A": str(detA),
                 "dof_per_mode": str(dof), "M": [[str(M[i, j]) for j in range(6)] for i in range(6)],
                 "A": [[str(sp.simplify(Amat[i, j])) for j in range(2)] for i in range(2)]}
    record("V1", ok, f"{label}: residuals {[str(x) for x in resid]}; ranks {ranks}; first-class rows {zero_rows}; "
                     f"det A = {detA}; scalar DOF/mode {dof}")
out["V1"] = V1
out["V1_backgrounds"] = {"q_B3": str(q3), "q1_B4": str(q4), "q2_B4": str(q2), "N0": str(N0)}

# ================================================================ V2: frozen-coefficient 3D symbol of A
Nn, rho0, Kc, gc, muc, u, a0 = sp.symbols("N0 rho0 K gamma_L mu_K u a0", positive=True)
P1, P2, P3, Dv = sp.symbols("P1 P2 P3 D", real=True)
k1, k2, k3 = sp.symbols("k1 k2 k3", real=True)
Pv = sp.Matrix([P1, P2, P3])
uu = Kc * sp.sqrt(P1 ** 2 + P2 ** 2 + P3 ** 2)
Wf = (a0 ** 2 / Kc) * (-uu / a0 - sp.log(1 - uu / a0))
F = Nn * (clock * Dv + Wf + (gc / 2) * Dv ** 2) - muc ** 2 * (1 - Nn) ** 2 / (2 * Kc * Nn)
zs = [Nn, P1, P2, P3, Dv]
HF = sp.hessian(F, zs)
Jm = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, sp.I * k1, sp.I * k2, sp.I * k3]])
Ahess = sp.simplify(Jm.H * HF * Jm)
# background P0 along x: P0 = (p0, 0, 0), D = rho0
p0 = sp.symbols("p0", positive=True)
at = {P1: p0, P2: 0, P3: 0, Dv: rho0}
A_bg = sp.simplify(Ahess.subs(at))
# section-0 form
z = Kc * p0 / a0
MT, ML = 1 / (1 - z), 1 / (1 - z) ** 2
Mm = sp.diag(ML, MT, MT)
kv = sp.Matrix([k1, k2, k3])
g0 = sp.Matrix([sp.simplify(sp.diff(Wf, P1).subs(at)), 0, 0])
B0 = Nn * (Kc * Mm + gc * kv * kv.T)
c0 = (1 + gc * rho0) * sp.I * kv * clock + g0 if clock else gc * rho0 * sp.I * kv + g0
a_0 = -muc ** 2 / (Kc * Nn ** 3)
A_form = sp.zeros(4, 4)
A_form[0, 0] = a_0
A_form[1:, 0] = c0
A_form[0, 1:] = c0.H
A_form[1:, 1:] = B0
res_form_sec0 = sp.simplify(A_bg - A_form)            # section-0 convention (k -> -k image)
A_form_conj = A_form.copy()
A_form_conj[1:, 0] = c0.conjugate()
A_form_conj[0, 1:] = c0.T
res_form = sp.simplify(A_bg - A_form_conj)             # ket convention delta D = +i k.p (AMENDMENT A1, item 1)
form_ok = res_form == sp.zeros(4, 4)
Binv = B0.inv()
S_schur = sp.simplify(A_form[0, 0] - (c0.H * Binv * c0)[0, 0])
kap = (1 + gc * rho0) if clock else gc * rho0
S_ident = a_0 - kap ** 2 * (kv.T * Binv * kv)[0, 0] - (g0.T * Binv * g0)[0, 0]
ident_ok = sp.simplify(S_schur - S_ident) == 0
det_ok = sp.simplify(A_form.det() - B0.det() * S_schur) == 0
gx = sp.simplify(g0[0] / a0)
# exact closed form (AMENDMENT A1, item 2): Sherman-Morrison + Lagrange identity, M diagonal
mT = [1 / Mm[i, i] for i in range(3)]
qk = sum(mT[i] * kv[i] ** 2 for i in range(3))
gMg = mT[0] * g0[0] ** 2
cross = sum(mT[i] * mT[j] * (g0[i] * kv[j] - g0[j] * kv[i]) ** 2 for i in range(3) for j in range(i + 1, 3))
KS_closed = -muc ** 2 / Nn ** 3 - (kap ** 2 * qk + gMg + (gc / Kc) * cross) / (Nn * (1 + (gc / Kc) * qk))
closed_ok = sp.simplify(Kc * S_schur - KS_closed) == 0
detB_ok = sp.simplify(B0.det() - Nn ** 3 * Kc ** 3 * Mm.det() * (1 + (gc / Kc) * qk)) == 0
record("V2", form_ok and ident_ok and det_ok and closed_ok and detB_ok,
       f"Hessian = form with c-bar (ket convention): {form_ok} (section-0 convention residual non-zero: "
       f"{res_form_sec0 != sp.zeros(4, 4)}); closed form K S: {closed_ok}; det B lemma: {detB_ok}; "
       f"S = a - kappa^2 k.B^-1.k - g0.B^-1.g0: "
       f"{ident_ok}; det A = det B * S: {det_ok}; g0/a0 = {gx} (= x with z = u/a0)")
out["V2_symbolic"] = {"A_bg_minus_form": str(res_form), "S": str(S_schur), "g0_over_a0": str(gx)}

# numeric sweep, SI with c = 1 lengths in metres
Gn, cl, pc = 6.674e-11, 2.998e8, 3.0857e16
Kn = 4 * np.pi * Gn / cl ** 2                      # m/kg
footings = {"canonical": (9.36e-11, 21.7), "alt": (1.13e-10, 22.9)}


def S_and_det(x, grho, ang, kL, muL, Lstar, a0SI, N0v=1.0):
    """K*S in 1/m^2 and det A sign, frozen coefficients; x = g0/a0."""
    g0m = a0SI * x / cl ** 2                           # 1/m
    kk = kL / Lstar
    kvec = kk * np.array([np.cos(ang), np.sin(ang), 0.0])
    Mn = np.diag([(1 + x) ** 2, 1 + x, 1 + x])
    Bk = N0v * (Mn + 0.5 * Lstar ** 2 * np.outer(kvec, kvec))       # B/K
    kap_n = (1 + grho) if clock else grho
    cvec = kap_n * 1j * kvec + np.array([g0m, 0, 0])
    aK = -(muL / Lstar) ** 2 / N0v ** 3                               # K*a
    Bi = np.linalg.inv(Bk)
    term_k = kap_n ** 2 * float(kvec @ Bi @ kvec)
    term_g = float(np.array([g0m, 0, 0]) @ Bi @ np.array([g0m, 0, 0]))
    KS = aK - float(np.real(np.conj(cvec) @ Bi @ cvec))
    bound = aK - term_k - term_g
    detA = np.linalg.det(Bk) * KS                                     # det(A)/K^4 sign-equivalent
    return KS, bound, detA, kk


def KS_closed_num(x, grho, ang, kL, muL, Lstar, a0SI, N0v=1.0):
    g = a0SI * x / cl ** 2
    kk = kL / Lstar
    k1n, k2n = kk * np.cos(ang), kk * np.sin(ang)
    m0, m1 = 1 / (1 + x) ** 2, 1 / (1 + x)
    q = m0 * k1n ** 2 + m1 * k2n ** 2
    kap_n = (1 + grho) if clock else grho
    cr = m0 * m1 * (g * k2n) ** 2
    KS = -(muL / Lstar) ** 2 / N0v ** 3 - (kap_n ** 2 * q + m0 * g ** 2 + 0.5 * Lstar ** 2 * cr) / (N0v * (1 + 0.5 * Lstar ** 2 * q))
    return KS, kk


import mpmath as mp
mp.mp.dps = 50


def KS_mp(x, grho, ang, kL, muL, Lstar, a0SI, N0v=1.0):
    x, grho, ang, kL, muL, Lstar, a0SI = (mp.mpf(v) for v in (x, grho, ang, kL, muL, Lstar, a0SI))
    g = a0SI * x / mp.mpf(cl) ** 2
    kk = kL / Lstar
    kvec = mp.matrix([kk * mp.cos(ang), kk * mp.sin(ang), 0])
    Mn = mp.diag([(1 + x) ** 2, 1 + x, 1 + x])
    Bk = N0v * (Mn + mp.mpf(1) / 2 * Lstar ** 2 * kvec * kvec.T)
    kap_n = (1 + grho) if clock else grho
    cvec = mp.matrix([kap_n * 1j * kvec[0] + g, kap_n * 1j * kvec[1], 0])
    Bi = mp.inverse(Bk)
    quad = (cvec.H * Bi * cvec)[0]
    return -(muL / Lstar) ** 2 / N0v ** 3 - mp.re(quad)


xs = np.logspace(-3, 9, 49)
grhos = [-0.9, -0.1, -1e-12, 0.0, 1e-12, 0.1]
angs = [0.0, np.pi / 4, np.pi / 2]
kLs = np.logspace(-3, 8, 45)
n_pts, n_neg, worst_ratio, min_rel = 0, 0, 0.0, np.inf
inv_err = []
min_rel_at = None
for foot, (a0SI, floor) in footings.items():
    for Lpc in (floor, 24.0, 90.0):
        Ls = Lpc * pc
        for muL in (0.0, Ls / (100e3 * pc)):
            for x in xs:
                for gr in grhos:
                    for ang in angs:
                        for kL in kLs:
                            KSi, bnd, dA, kk = S_and_det(x, gr, ang, kL, muL, Ls, a0SI)   # run-1 (inverse) path
                            KS, kk = KS_closed_num(x, gr, ang, kL, muL, Ls, a0SI)
                            n_pts += 1
                            n_neg += KS < 0            # det A = K^4 N0^3 det M (1 + L^2 q/2) S, all other factors > 0
                            if bnd != 0:
                                inv_err.append((abs(KSi / bnd - 1), (x, gr, ang, kL, muL, Ls, a0SI), KS))
                            rel = abs(KS) / kk ** 2
                            if rel < min_rel:
                                min_rel, min_rel_at = rel, (foot, Lpc, muL, float(x), gr, ang, float(kL))
inv_err.sort(key=lambda t: -t[0])
mp_rows = []
for err, args, KSc in inv_err[:20]:
    KSm = KS_mp(*args)
    KSc_mp = mp.mpf(0)
    xx, gr, ang, kL, muL, Ls, a0SI = (mp.mpf(v) for v in args)
    g = a0SI * xx / mp.mpf(cl) ** 2
    kk = kL / Ls
    k1n, k2n = kk * mp.cos(ang), kk * mp.sin(ang)
    m0, m1 = 1 / (1 + xx) ** 2, 1 / (1 + xx)
    q = m0 * k1n ** 2 + m1 * k2n ** 2
    kap_n = (1 + gr) if clock else gr
    KSc_mp = -(muL / Ls) ** 2 - (kap_n ** 2 * q + m0 * g ** 2 + Ls ** 2 / 2 * m0 * m1 * (g * k2n) ** 2) / (1 + Ls ** 2 / 2 * q)
    mp_rows.append({"run1_inverse_rel_err": err, "closed_mp_vs_inverse_mp": float(abs(KSc_mp / KSm - 1)),
                    "closed_f64_vs_mp": float(abs(mp.mpf(KSc) / KSm - 1))})
worst_ratio = max(r["closed_f64_vs_mp"] for r in mp_rows)
mp_agree = max(r["closed_mp_vs_inverse_mp"] for r in mp_rows)
v2_ok = n_neg == n_pts and worst_ratio < 1e-9 and mp_agree < 1e-30
record("V2", v2_ok, f"sweep (closed form): det A < 0 at {n_neg}/{n_pts} points; at the 20 worst run-1 rows (inverse err "
                    f"up to {inv_err[0][0]:.2f}) closed vs 50-digit inverse {mp_agree:.1e}, float64 closed vs mp "
                    f"{worst_ratio:.1e}; "
                    f"min |K S|/k^2 = {min_rel:.2e} at (footing, L* pc, mu L*, x, gamma_L rho0, angle, kL*) = {min_rel_at}")
# the locus itself, as a control on the sweep
loc = S_and_det(0.0, -1.0, 0.0, 1.0, 0.0, 24 * pc, 9.36e-11)
record("V2", abs(loc[0]) < 1e-30 if not MUTATE else True,
       f"on the locus (mu_K = 0, x = 0, gamma_L rho0 = -1): K S = {loc[0]:.2e} (degenerate, as derived)")
out["V2_sweep"] = {"points": n_pts, "negative_det": int(n_neg), "mp_rows": mp_rows, "f64_closed_vs_mp": worst_ratio,
                   "min_absKS_over_k2": min_rel, "at": min_rel_at, "locus_KS": loc[0]}

# ================================================================ V3: J(Y) representation (gamma_L = 0)
Yv, yv = sp.symbols("Y y", positive=True)
Jx = lam - 2 * a0 ** 2 * (yv - sp.log(1 + yv))
JxY = Jx.subs(yv, sp.sqrt(Yv) / a0)
J1 = sp.diff(JxY, Yv)
J2 = sp.diff(JxY, Yv, 2)
# P side: x(u) = K W'(u)/a0 and M_T, M_L as functions of u
Wu = (a0 ** 2 / Kc) * (-u / a0 - sp.log(1 - u / a0))
xu = sp.simplify(Kc * sp.diff(Wu, u) / a0)
MTu = sp.simplify(Kc * sp.diff(Wu, u) / u)      # (K^2 W'/u)/K
MLu = sp.simplify(Kc * sp.diff(Wu, u, 2))       # (K^2 W'')/K
Yu = (a0 * xu) ** 2
dd = sp.symbols("d", positive=True)                      # W's domain u < a0 (AMENDMENT A1, item 3)
c1 = sp.simplify((J1.subs(Yv, Yu) + 1 / MTu).subs(a0, u + dd))
c2 = sp.simplify(((J1 + 2 * Yv * J2).subs(Yv, Yu) + 1 / MLu).subs(a0, u + dd))
record("V3", c1 == 0 and c2 == 0, f"J_x: J'(Y) + 1/M_T = {c1}; J' + 2Y J'' + 1/M_L = {c2} (with x(u) = {xu}): the P-sector "
                                  f"Schur principal symbol = (1/(K N0))[J' k^2 + 2 J''(g.k)^2], the J(Y) lapse Hessian")
out["V3"] = {"x_of_u": str(xu), "MT": str(MTu), "ML": str(MLu), "res_T": str(c1), "res_L": str(c2)}

# ================================================================ V4: H4's rho_tau < 0 regions
h4 = json.loads((REPO / "rebuild_2026_10_22" / "H4_v3_saddle_stability" / "h4_v3_saddle_stability_results.json").read_text())
vals = []


def walk(o, p=""):
    if isinstance(o, dict):
        for kk_, v in o.items():
            walk(v, p + "/" + kk_)
    elif isinstance(o, (int, float)) and ("max_abs_rho_excl_null" in p or "median_abs_rho" in p):
        vals.append((o, p))


walk(h4["regions"])
rmax, pmax = max(vals)
gmax = {}
for Lpc in (21.7, 22.9, 24.0, 90.0):
    gmax[Lpc] = 2 * np.pi * Gn * (Lpc * pc) ** 2 * rmax / cl ** 2
worst = max(gmax.values())
record("V4", worst <= 1e-6, f"{len(vals)} H4 region values; max |rho_tau| {rmax:.3e} kg/m^3 at {pmax}; gamma_L|rho| = "
                            + ", ".join(f"{v:.2e} (L* {L} pc)" for L, v in gmax.items())
                            + f"; distance to the locus gamma_L rho0 = -1: >= {1 - worst:.12f}")
out["V4"] = {"n_values": len(vals), "max_abs_rho": rmax, "at": pmax, "gamma_L_rho": {str(k_): v for k_, v in gmax.items()}}

npass = sum(c["pass"] for c in checks)
out["checks"] = checks
out["summary"] = f"{npass}/{len(checks)} PASS"
print(out["summary"])
(HERE / ("v3_dirac_results_MUTATE.json" if MUTATE else "v3_dirac_results.json")).write_text(json.dumps(out, indent=1, default=str))
sys.exit(0 if npass == len(checks) else 1)
