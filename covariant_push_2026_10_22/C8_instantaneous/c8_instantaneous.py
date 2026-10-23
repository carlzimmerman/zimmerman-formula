#!/usr/bin/env python3
"""C8_instantaneous: is the C4-literal leaf-elliptic (P, lapse) system well posed, and does its instantaneous
response have consequences that existing data constrain?

Theory (C4-literal, C5's family at beta = eta = gamma_F = 0, xi = 1), weak-field leaf problem, c = 1, K = 4 pi G:
  L_static = -|grad Phi|^2/2K + P.grad Phi - W(K|P|) - (gamma_L/2)(div P)^2 - rho Phi,
  W(u) = (a0^2/K)[-u/a0 - ln(1 - u/a0)],   gamma_L = K Lstar^2/2.
Energy functional E = -L_static = |grad Phi - K P|^2/2K + g(K|P|) + (gamma_L/2)(div P)^2 + rho Phi,
g(u) = W(u) - u^2/2K.

Checks K1..K10 as frozen in FROZEN_CRITERIA.md (commit f2399aaf5e). K6 and K10 are not scored.
External bounds are record transcriptions (see README input ledger); no network.
kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 m/s^2, never pooled.

Run: OMP_NUM_THREADS=1 nice -n 15 python3 c8_instantaneous.py        (C8_MUTATE=1 flips the sign of gamma_L)
"""
import json
import os
import resource
import sys
import time

import numpy as np
import scipy.sparse as sps
import sympy as sp
from scipy.integrate import solve_bvp
from scipy.optimize import minimize

T0 = time.time()
MUTATE = os.environ.get("C8_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
GSIGN = -1 if MUTATE else 1
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, f"c8_instantaneous{TAG}.out")
JSON = os.path.join(HERE, f"c8_instantaneous_results{TAG}.json")

c_SI = 2.99792458e8
G_SI = 6.67430e-11
MSUN = 1.98847e30
GMSUN = 1.32712440018e20
PC = 3.0856775814913673e16
AU = 1.495978707e11
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LSTARS = [20, 24, 90]

lines, checks, res = [], [], {"mutate": MUTATE}


def log(s):
    print(s, flush=True)
    lines.append(s)


def check(kid, ok, value, thr, scored=True):
    checks.append({"id": kid, "pass": bool(ok), "value": str(value), "threshold": thr, "scored": scored})
    log(f"{kid} {'PASS' if ok else 'FAIL'} {value} {thr}{'' if scored else '  [not scored]'}")


# ============================================================ K2: convexity identity (needed by K1)
log("== K2 convexity of the leaf functional")
u, a0, K, gam = sp.symbols("u a0 K gamma_L", positive=True)
W = (a0 ** 2 / K) * (-u / a0 - sp.log(1 - u / a0))
gfun = W - u ** 2 / (2 * K)
g1 = sp.simplify(sp.diff(gfun, u))
g2 = sp.simplify(sp.diff(gfun, u, 2))
g1_target = u ** 2 / (K * (a0 - u))
g2_target = u * (2 * a0 - u) / (K * (a0 - u) ** 2)
r_g1 = sp.simplify(g1 - g1_target)
r_g2 = sp.simplify(g2 - g2_target)
# identity: L_static(a, p) = -|a - K p|^2/2K - g(K|p|)   (Phi-part, P-part; gamma and rho terms identical)
ax, ay, az, px, py, pz = sp.symbols("a_x a_y a_z p_x p_y p_z", real=True)
pn = sp.sqrt(px ** 2 + py ** 2 + pz ** 2)
Lst = -(ax ** 2 + ay ** 2 + az ** 2) / (2 * K) + (px * ax + py * ay + pz * az) - W.subs(u, K * pn)
Lid = -((ax - K * px) ** 2 + (ay - K * py) ** 2 + (az - K * pz) ** 2) / (2 * K) - gfun.subs(u, K * pn)
r_id = sp.simplify(sp.expand(Lst - Lid))
cap = sp.limit(W, u, a0, dir="-")
# sign on [0, a0): numerators/denominators manifestly >= 0; confirm on a dense grid too
ug = np.linspace(0, 1 - 1e-12, 20001)
g1n = ug ** 2 / (1 - ug)
g2n = ug * (2 - ug) / (1 - ug) ** 2
ok2 = (r_g1 == 0) and (r_g2 == 0) and (r_id == 0) and (cap == sp.oo) and g1n.min() >= 0 and g2n.min() >= 0
res["K2"] = {"g_prime": str(g1_target), "g_second": str(g2_target), "identity_residual": str(r_id),
             "W_at_cap": str(cap), "min_g1": float(g1n.min()), "min_g2": float(g2n.min())}
check("K2", ok2, f"residuals ({r_g1},{r_g2},{r_id}); W(a0-)={cap}; min g'={g1n.min():.1e}, g''={g2n.min():.1e}",
      "all residuals 0, W->oo, g',g''>=0")

# ============================================================ K1: symbol positivity
log("== K1 symbol positivity of the linearised leaf operator")
# Quadratic form E2 = |i xi phi - K p|^2/2K + p^H H p/2 + (gamma/2)|xi.p|^2 ; M = A^H A/K + diag(0,H) + gamma [0;xi][0,xi]^T
xs = sp.symbols("xi1:4", real=True)
xi = sp.Matrix(xs)
Hs = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"H{min(i, j)}{max(i, j)}", real=True))
A = sp.Matrix.hstack(sp.I * xi, -K * sp.eye(3))
gs = sp.Symbol("g_s", real=True)
M = (A.H * A) / K
M[1:, 1:] += Hs + gs * xi * xi.T
xi2 = (xi.T * xi)[0]
Schur = M[1:, 1:] - M[1:, 0] * M[0, 0] ** -1 * M[0, 1:]
Schur_target = K * (sp.eye(3) - xi * xi.T / xi2) + Hs + gs * xi * xi.T
r_schur = sp.simplify(Schur - Schur_target)
schur_ok = all(e == 0 for e in r_schur)
log(f"   Schur complement = K(I - xihat xihat) + H_g + gamma xi xi^T : residual zero = {schur_ok}")


def Hg_num(uu, phat, Kn=1.0, a0n=1.0):
    gp_over_u = Kn ** 2 * (uu / (a0n - uu)) / Kn            # K^2 g'(u)/u with g' = u^2/(K(a0-u))
    gpp = Kn ** 2 * uu * (2 * a0n - uu) / (Kn * (a0n - uu) ** 2)
    pp = np.outer(phat, phat)
    return gpp * pp + gp_over_u * (np.eye(3) - pp)


gnum = GSIGN * 0.5     # gamma_L = K L*^2/2 with K = L* = 1
import mpmath as mp
mp.mp.dps = 50
# Run 1 used float64 eigvalsh: the bound held to 5e-9 relative only (rounding at |xi|L* = 1e4); run 2 uses mpmath.
worst_ratio, min_eig_M, npts = mp.inf, mp.inf, 0
for uu in [0, mp.mpf("1e-6"), mp.mpf("0.1"), mp.mpf("0.5"), mp.mpf("0.9"), mp.mpf("0.999"), 1 - mp.mpf("1e-9")]:
    uu = mp.mpf(uu)
    gpu = uu / (1 - uu)
    gpp = uu * (2 - uu) / (1 - uu) ** 2
    for th in [mp.pi * kk / 8 for kk in range(9)]:
        xh = [mp.sin(th), mp.mpf(0), mp.cos(th)]
        for kl in [mp.mpf(10) ** (mp.mpf(e) / 2) for e in range(-8, 9)]:
            xv = [kl * c for c in xh]
            Hm_ = mp.matrix(3, 3)
            S = mp.matrix(3, 3)
            for i_ in range(3):
                for j_ in range(3):
                    pp = 1 if (i_ == 2 and j_ == 2) else 0          # phat = z
                    Hm_[i_, j_] = gpp * pp + gpu * ((1 if i_ == j_ else 0) - pp)
                    S[i_, j_] = ((1 if i_ == j_ else 0) - xh[i_] * xh[j_]) + Hm_[i_, j_] + gnum * xv[i_] * xv[j_]
            Mn = mp.matrix(4, 4)
            Mn[0, 0] = kl ** 2
            for i_ in range(3):
                Mn[0, 1 + i_] = -1j * xv[i_]
                Mn[1 + i_, 0] = 1j * xv[i_]
                for j_ in range(3):
                    Mn[1 + i_, 1 + j_] = (1 if i_ == j_ else 0) + Hm_[i_, j_] + gnum * xv[i_] * xv[j_]
            es = min(mp.eigsy(S)[0])
            ev = min(mp.eighe(Mn)[0])
            bound = min(mp.mpf(1), abs(gnum) * kl ** 2)
            min_eig_M = min(min_eig_M, ev / max(1, kl ** 2))
            worst_ratio = min(worst_ratio, es / bound)
            npts += 1
worst_ratio, min_eig_M = float(worst_ratio), float(min_eig_M)
ok1 = schur_ok and worst_ratio >= 1 - 1e-10 and min_eig_M > 0
res["K1"] = {"schur_closed_form": schur_ok, "points": npts, "min_schur_over_bound": worst_ratio,
             "min_eig_M_normalised": min_eig_M, "gamma_L": gnum}
check("K1", ok1, f"{npts} pts; min Schur/min(K,gamma xi^2) = {worst_ratio:.15g}; min eig(M)/max(1,xi^2) = {min_eig_M:.3g}",
      ">= 1-1e-10 and > 0")

# ============================================================ K3: uniqueness kernel
log("== K3 uniqueness: kernel of the 'affine along a segment' conditions")
Ccond = sp.Matrix.vstack(sp.Matrix.hstack(sp.I * xi, -K * sp.eye(3)), sp.Matrix.hstack(sp.zeros(1, 1), xi.T))
detC = sp.factor(Ccond.det())
xi_test = {xs[0]: sp.Rational(3, 7), xs[1]: sp.Rational(-2, 5), xs[2]: sp.Rational(1, 3)}
rank_gam = Ccond.subs(xi_test).subs(K, 1).rank()
rank_nogam = Ccond[:3, :].subs(xi_test).subs(K, 1).rank()
# The affine-segment argument needs every term of E convex, i.e. gamma_L >= 0 (with gamma_L < 0 the div-P term is
# concave and the argument is void, whatever the rank).
rank_used = rank_gam if GSIGN * 0.5 > 0 else 0
res["K3"] = {"det": str(detC), "rank_gamma_pos": int(rank_gam), "rank_gamma_zero": int(rank_nogam),
             "rank_used": int(rank_used)}
check("K3", rank_used == 4 and GSIGN > 0, f"det = {detC}; rank(gamma>0) = {rank_gam}; rank(gamma=0) = {rank_nogam} (kernel p = i xi phi/K,"
      f" then uniqueness rests on strict convexity of g)", "rank 4 with gamma_L > 0")

# ============================================================ K4: spherical BVP
log("== K4 spherical boundary-value problem (a0 = L* = K = 1, point mass)")
# Run 1 used scipy solve_bvp (collocation); it hit max_nodes (status 1) in every case and used 2.3 GB RSS
# (kept: *_RUN1.*). Run 2 solves the same Euler-Lagrange problem as the minimiser of the spherical reduced functional
# (Phi eliminated exactly by Gauss: Phi' = g_N + K P):
#   E_red[P] = Int r^2 [ -g_N P + g(K P) + (gamma/2) ((r^2 P)'/r^2)^2 ] dr ,
# natural boundary conditions (r^2 P -> 0 inside, psi = 0 at R). Its EL equation is gamma psi' = K g'(KP) - g_N,
# i.e. (L*^2/2) psi' = u^2/(a0-u) - g_N, the frozen ODE. Newton with backtracking, barrier u < a0 kept exactly.


def sph_solve(rM, R, guess, rmin=1e-4, n=3000, gam_=None):
    gam_ = GSIGN * 0.5 if gam_ is None else gam_
    GM = rM ** 2
    r = np.logspace(np.log10(rmin), np.log10(R), n)
    w_ = np.gradient(r)                      # node weights (trapezoid-like)
    # inner ball [0, r_0] (P ~ P_0 there): its load Int r^2 g_N = GM r_0 and Int r^2 g = g(P_0) r_0^3/3 go to node 0
    wl = w_ * r ** 2
    wl[0] += r[0] ** 3          # so that wl * gN = GM (w_0 + r_0) at node 0
    wg = w_ * r ** 2
    wg[0] += r[0] ** 3 / 3
    rm = 0.5 * (r[1:] + r[:-1])
    dr = np.diff(r)
    # psi_mid = (r_{i+1}^2 P_{i+1} - r_i^2 P_i)/(dr r_mid^2) = Dm @ P
    Dm = sps.diags([-(r[:-1] ** 2) / (dr * rm ** 2), (r[1:] ** 2) / (dr * rm ** 2)], [0, 1], shape=(n - 1, n), format="csr")
    cmid = gam_ * dr * rm ** 2
    # innermost interval [0, r_0] with r^2 P = 0 at r = 0 (regularity); without it the truncated grid imposes the
    # wrong natural condition psi(r_min) = 0, which forces r^2 P = const and drives u to the cap at r_min.
    r0m = r[0] / 2
    row0 = sps.csr_matrix(([r[0] ** 2 / (r[0] * r0m ** 2)], ([0], [0])), shape=(1, n))
    Dm = sps.vstack([row0, Dm], format="csr")
    cmid = np.concatenate([[gam_ * r[0] * r0m ** 2], cmid])
    Hg = (Dm.T @ sps.diags(cmid) @ Dm).tocsc()
    gN = GM / r ** 2

    def gfun(P):                       # g(K|P|) is even and convex on |P| < a0 = 1
        a = np.abs(P)
        return (-a - np.log1p(-a)) - a ** 2 / 2, np.sign(P) * a ** 2 / (1 - a), a * (2 - a) / (1 - a) ** 2

    def E(P):
        if np.any(np.abs(P) >= 1):
            return np.inf
        g0, _, _ = gfun(P)
        psi = Dm @ P
        return np.sum(-wl * gN * P + wg * g0) + 0.5 * np.sum(cmid * psi ** 2)

    def grad_hess(P):
        _, g1, g2 = gfun(P)
        gr = -wl * gN + wg * g1 + Hg @ P
        H = Hg + sps.diags(wg * g2)
        return gr, H.tocsc()

    uaq = (-gN + np.sqrt(gN ** 2 + 4 * gN)) / 2
    if guess == "aqual":
        P = np.minimum(uaq, 0.999)
    else:
        # second guess: flat P = 0.5. (In development, Newton alone from this guess jammed at the barrier for rM = 3:
        # rel |grad| 0.88 after 399 iterations, a solver stall; the L-BFGS stage below was added; see README.)
        P = np.full(n, 0.5)
    from scipy.sparse.linalg import spsolve
    # stage 1 (globalisation): L-BFGS on q = artanh(P), an unconstrained diffeomorphic reparametrisation of |P| < a0
    # (critical points correspond one to one, so the unique minimiser is the only target). Stage 2: Newton in P.
    sc = np.sqrt(np.abs(Hg.diagonal()) + 1.0)

    def Eq(q):
        Pq = np.tanh(q)
        ev = E(Pq)
        gr_, _ = grad_hess(Pq)
        return ev, gr_ * (1 - Pq ** 2)

    P = np.clip(P, -0.999, 0.999)
    rq = minimize(Eq, np.arctanh(P), jac=True, method="L-BFGS-B",
                  options={"maxiter": 20000, "maxcor": 30, "ftol": 1e-15, "gtol": 1e-12, "maxfun": 25000})
    P = np.tanh(rq.x)
    del sc
    e_old = E(P)
    g0n = None
    for it in range(400):
        gr, H = grad_hess(P)
        gn = np.linalg.norm(gr)
        g0n = gn if g0n is None else g0n
        if gn < 1e-13 * max(1.0, g0n):
            break
        try:
            step = spsolve(H, -gr)
        except Exception:
            step = -gr
        if gr @ step >= 0:          # not a descent direction (non-convex, e.g. mutate): gradient step
            step = -gr / max(1.0, np.abs(gr).max())
        # fraction-to-boundary rule (interior point): never step past 99.5% of the way to |P| = a0
        tb = (1 - np.abs(P)) / np.maximum(np.abs(step), 1e-300)
        t = min(1.0, 0.995 * tb.min())
        while t > 1e-14:
            Pn = P + t * step
            en = E(Pn)
            if en < e_old - 1e-4 * t * abs(gr @ step):
                break
            # near the barrier E is dominated by large terms and its decrease drops below float resolution;
            # then accept a feasible step that does not raise E beyond rounding and reduces |grad E|
            if np.isfinite(en) and en <= e_old + 1e-13 * abs(e_old) and \
                    np.linalg.norm(grad_hess(Pn)[0]) < np.linalg.norm(gr):
                break
            t *= 0.5
        if t <= 1e-14:
            break
        P, e_old = Pn, en
    gr, _ = grad_hess(P)
    return r, P, uaq, np.linalg.norm(gr) / max(1.0, g0n), it


k4 = {}
ok4 = True
for rM in [0.3, 3.0]:
    big = 30 * max(rM, 1 / rM)
    R = 10 * big
    r1, P1, uaq1, gr1, it1 = sph_solve(rM, R, "aqual")
    r2, P2, _, gr2, it2 = sph_solve(rM, R, "flat")
    r3, P3, _, gr3, it3 = sph_solve(rM, 2 * R, "aqual", n=3300)
    rr = np.logspace(-3, np.log10(big), 400)
    U1 = np.interp(np.log(rr), np.log(r1), P1)
    U2 = np.interp(np.log(rr), np.log(r2), P2)
    U3 = np.interp(np.log(rr), np.log(r3), P3)
    conv = bool(max(gr1, gr2, gr3) < 1e-9)
    d12 = float(np.max(np.abs(U1 - U2) / np.abs(U1)))
    d13 = float(np.max(np.abs(U1 - U3)[rr <= 1] / np.abs(U1[rr <= 1])))
    umax = float(P1.max())
    GM = rM ** 2
    u_in = float(np.interp(np.log(0.01), np.log(r1), P1))
    hedge = GM          # GM/L*^2
    u_far = float(np.interp(np.log(big), np.log(r1), P1))
    deep = np.sqrt(GM / big ** 2)
    far_ratio = u_far / deep
    inner_ok = (abs(u_in / hedge - 1) < 0.02) if hedge < 1 else (u_in < 1)   # unscreened core: u -> a0, not GM/L*^2
    ok_case = conv and d12 < 1e-6 and umax < 1 and inner_ok and abs(far_ratio - 1) < 0.02 and d13 < 1e-3
    ok4 = ok4 and ok_case
    k4[f"rM_{rM}"] = {"converged": conv, "rel_grad": [gr1, gr2, gr3], "newton_its": [it1, it2, it3],
                      "max_rel_diff_guesses": d12, "max_rel_diff_domain_doubling_r<=L": d13, "max_u_over_a0": umax,
                      "u_at_0.01L": u_in, "GM_over_L2": hedge,
                      "inner_test": "hedgehog GM/L*^2" if hedge < 1 else "u<a0 (unscreened core; GM/L*^2 > a0)",
                      "far_r": big, "u_far_over_sqrt(a0 gN)": far_ratio,
                      "u_far_over_uAQUAL": u_far / float(np.interp(np.log(big), np.log(r1), uaq1)), "pass": bool(ok_case)}
    log(f"   rM/L*={rM}: rel|grad| {gr1:.1e},{gr2:.1e},{gr3:.1e} (its {it1},{it2},{it3}); guesses diff {d12:.2e}; "
        f"doubling {d13:.2e}; max u/a0 {umax:.6f}; u(0.01)={u_in:.6g} vs GM/L*^2={hedge:.4g}; "
        f"far u/sqrt(a0 gN) at r={big:.0f}: {far_ratio:.5f}")
res["K4"] = k4
check("K4", ok4, "; ".join(f"{k}: {'ok' if v['pass'] else 'BAD'}" for k, v in k4.items()),
      "unique (<1e-6), u<a0, inner limit 2%, far AQUAL 2%, doubling <1e-3")

# ============================================================ K5: 3D non-symmetric solve
log("== K5 3D two-mass solve (convex functional, L-BFGS, two initial guesses)")
n, B = 26, 3.0
h = 2 * B / (n + 1)
x1 = -B + h * np.arange(1, n + 1)
X, Y, Z = np.meshgrid(x1, x1, x1, indexing="ij")
I1 = sps.identity(n, format="csr")
d1 = sps.diags([-np.ones(n), np.ones(n - 1)], [0, 1], format="csr") / h      # forward diff, Phi = 0 outside
Dx = sps.kron(sps.kron(d1, I1), I1, format="csr")
Dy = sps.kron(sps.kron(I1, d1), I1, format="csr")
Dz = sps.kron(sps.kron(I1, I1), d1, format="csr")
N3 = n ** 3


def blob(c, s):
    return np.exp(-((X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2) / (2 * s ** 2)) / ((2 * np.pi) ** 1.5 * s ** 3)


Kn = 1.0
GM1, GM2 = 0.5, 0.2
# K = 4 pi G = 1 -> G = 1/(4 pi); rho = (G rho)/G
rho = (GM1 * blob((-0.8, 0.3, 0.0), 0.3) + GM2 * blob((0.9, -0.2, 0.4), 0.3)).ravel() * 4 * np.pi
UC = 0.99


def gext(uu):
    uu = np.asarray(uu)
    out = np.empty_like(uu)
    d = np.empty_like(uu)       # g'(u)/u
    m = uu <= UC
    um = uu[m]
    out[m] = (-um - np.log1p(-um)) - um ** 2 / 2
    d[m] = um / (1 - um)
    ue = uu[~m]
    g0 = (-UC - np.log1p(-UC)) - UC ** 2 / 2
    gp = UC ** 2 / (1 - UC)
    gpp = UC * (2 - UC) / (1 - UC) ** 2
    out[~m] = g0 + gp * (ue - UC) + gpp * (ue - UC) ** 2 / 2
    d[~m] = (gp + gpp * (ue - UC)) / ue
    return out, d


gam3 = GSIGN * 0.5


def energy(z):
    phi = z[:N3]
    P = z[N3:].reshape(3, N3)
    Gx, Gy, Gz = Dx @ phi - Kn * P[0], Dy @ phi - Kn * P[1], Dz @ phi - Kn * P[2]
    divP = -(Dx.T @ P[0] + Dy.T @ P[1] + Dz.T @ P[2])
    uu = Kn * np.sqrt(P[0] ** 2 + P[1] ** 2 + P[2] ** 2)
    gv, gd = gext(uu)
    E = np.sum((Gx ** 2 + Gy ** 2 + Gz ** 2) / (2 * Kn) + gv + gam3 / 2 * divP ** 2 + rho * phi) * h ** 3
    gphi = (Dx.T @ Gx + Dy.T @ Gy + Dz.T @ Gz) / Kn + rho
    gdiv = -gam3 * divP   # d/dP of (gam/2) divP^2 with divP = -D^T P  ->  -gam * D divP
    gP0 = -Gx + Kn ** 2 * gd * P[0] + (-(Dx @ (gam3 * divP)))
    gP1 = -Gy + Kn ** 2 * gd * P[1] + (-(Dy @ (gam3 * divP)))
    gP2 = -Gz + Kn ** 2 * gd * P[2] + (-(Dz @ (gam3 * divP)))
    del gdiv
    return E, np.concatenate([gphi, gP0, gP1, gP2]) * h ** 3


rng = np.random.default_rng(20261022)
z0a = np.zeros(4 * N3)
z0b = np.concatenate([rng.normal(0, 0.3, N3), rng.uniform(-0.3, 0.3, 3 * N3)])
# gradient check (finite difference, one direction)
e0, gr0 = energy(z0b)
dirv = rng.normal(size=4 * N3)
eps_fd = 1e-6
fd = (energy(z0b + eps_fd * dirv)[0] - energy(z0b - eps_fd * dirv)[0]) / (2 * eps_fd)
gcheck = abs(fd - gr0 @ dirv) / abs(fd)
log(f"   grid {n}^3, h={h:.3f}; gradient FD check rel err {gcheck:.2e}")
sols = []
for z0 in (z0a, z0b):
    g_init = np.linalg.norm(energy(z0)[1])
    r_ = minimize(energy, z0, jac=True, method="L-BFGS-B",
                  options={"maxiter": 30000, "maxcor": 30, "ftol": 1e-16, "gtol": 1e-13, "maxfun": 40000})
    g_fin = np.linalg.norm(energy(r_.x)[1])
    sols.append((r_, g_init, g_fin))
    log(f"   L-BFGS: nit={r_.nit} E={r_.fun:.10g} |grad| {g_init:.3e} -> {g_fin:.3e} ({r_.message})")


def fields(z):
    phi = z[:N3]
    P = z[N3:].reshape(3, N3)
    gphi = np.vstack([Dx @ phi, Dy @ phi, Dz @ phi])
    return gphi, P


ga, Pa = fields(sols[0][0].x)
gb, Pb = fields(sols[1][0].x)
scale_g = np.max(np.abs(ga))
scale_P = np.max(np.abs(Pa))
dg = float(np.max(np.abs(ga - gb)) / scale_g)
dP = float(np.max(np.abs(Pa - Pb)) / scale_P)
umax3 = float(max(np.max(np.sqrt((Pa ** 2).sum(0))), np.max(np.sqrt((Pb ** 2).sum(0)))) * Kn)
gred = float(max(s[2] / s[1] for s in sols))
ok5 = bool(np.isfinite(dg) and dg < 1e-4 and dP < 1e-4 and umax3 < UC and gred < 1e-6 and gcheck < 1e-5)
res["K5"] = {"grid": n, "h": h, "fd_grad_rel_err": gcheck, "max_rel_diff_gradPhi": dg, "max_rel_diff_P": dP,
             "max_u_over_a0": umax3, "max_grad_reduction": gred,
             "energies": [float(s[0].fun) for s in sols], "nit": [int(s[0].nit) for s in sols]}
check("K5", ok5, f"diff gradPhi {dg:.2e}, P {dP:.2e}; max u/a0 {umax3:.4f}; |grad| reduction {gred:.2e}",
      "<1e-4, <1e-4, <0.99, <1e-6")

# ============================================================ K6: no time derivatives of N, P (by construction)
log("== K6 (by construction) conjugate momenta of N and P vanish at beta = eta = 0")
tt, xx = sp.symbols("t x", real=True)
Nf, Pf, hf, Sf = [sp.Function(nm)(tt, xx) for nm in ("N", "P", "h", "S")]   # 1+1 toy: lapse, P_x, h_xx, shift
Kxx = (sp.diff(hf, tt) - 2 * sp.diff(Sf, xx)) / (2 * Nf)
theta = Kxx / hf
Lg = Nf * sp.sqrt(hf) * (Kxx ** 2 / hf ** 2 - theta ** 2) / (4 * K)        # (1+beta) theta^2 at beta=0
Lp = sp.sqrt(hf) * (Pf / hf) * sp.diff(Nf, xx) - Nf * sp.sqrt(hf) * W.subs(u, K * sp.sqrt(Pf ** 2 / hf)) \
    - Nf * sp.sqrt(hf) * gam / 2 * (sp.diff(sp.sqrt(hf) * Pf / hf, xx) / sp.sqrt(hf)) ** 2
Ltot = Lg + Lp
piN = sp.simplify(sp.diff(Ltot, sp.diff(Nf, tt)))
piP = sp.simplify(sp.diff(Ltot, sp.diff(Pf, tt)))
res["K6"] = {"pi_N": str(piN), "pi_P": str(piP)}
check("K6", piN == 0 and piP == 0, f"pi_N = {piN}, pi_P = {piP}", "both 0 (by construction)", scored=False)

# ============================================================ K7: binary pulsars
log("== K7 binary pulsars (record-transcribed bounds)")
PSR = {
    "J0737-3039A/B": dict(Pb=0.1022515592973, M=2.587052, frac=6.3e-5,
                          src="Kramer et al. 2021 PRX 11 041050: Pbdot_obs/Pbdot_GR = 0.999963(63) [record transcription]"),
    "B1913+16": dict(Pb=0.322997448911, M=2.828378, frac=1.6e-3,
                     src="Weisberg & Huang 2016 ApJ 829 55: 0.9983(16) [record transcription]"),
    "J1738+0333": dict(Pb=0.3547907398724, M=1.641, frac=3.2 / 27.7,
                       src="Freire et al. 2012 MNRAS 423 3328: Pbdot_int = -25.9(32)e-15 vs GR -27.7e-15 [record transcription]"),
}
k7 = {}
worst7 = 0.0
for nm, d in PSR.items():
    a = (GMSUN * d["M"] * (d["Pb"] * 86400) ** 2 / (4 * np.pi ** 2)) ** (1 / 3)
    row = {"a_m": a, "frac_Pbdot_precision": d["frac"], "src": d["src"]}
    for Ls in LSTARS:
        L = Ls * PC
        eps = (a / L) ** 2
        uP = GMSUN * d["M"] / L ** 2
        row[f"L{Ls}"] = {"eps": eps, "eps_over_precision": eps / d["frac"],
                         "nonlinear": {fk: eps * uP / fa for fk, fa in A0.items()}}
        worst7 = max(worst7, eps / d["frac"])
    k7[nm] = row
    log(f"   {nm}: a = {a:.4e} m; eps(L*=20/24/90 pc) = "
        + ", ".join(f"{row[f'L{Ls}']['eps']:.3e}" for Ls in LSTARS) + f"; precision {d['frac']:.2g}")
res["K7"] = {"systems": k7, "radiative": "none: no propagating non-tensor mode at beta=eta=0 (C5 DOF); leaf equations "
             "have no d/dt and are T-even, so the force is -dE_min/dx of the instantaneous configuration (zero work per orbit)",
             "worst_ratio": worst7}
check("K7", worst7 < 1, f"max eps/precision = {worst7:.3e}", "< 1 (UNCONSTRAINED)")

# ============================================================ K8: preferred frame, instantaneous-slice elongation
log("== K8 preferred frame: field of a body moving at w through the leaves")
w, X1, X2, X3 = sp.symbols("w X1 X2 X3", real=True)
rr_ = sp.sqrt(X1 ** 2 + X2 ** 2 + X3 ** 2)
gw = 1 / sp.sqrt(1 - w ** 2)
fP = sp.sqrt((X1 / gw) ** 2 + X2 ** 2 + X3 ** 2)            # Phi_c ~ r, evaluated on the tilted leaf (x'_par / gamma_w)
ser = sp.series(fP, w, 0, 3).removeO()
coef = sp.simplify((ser - rr_).coeff(w, 2) / rr_ * rr_ ** 2 / X1 ** 2)
# induced metric on the tilted leaf: t' = -w x_par + const  -> h = diag(1 - w^2, 1, 1)
tp = -w * X1
hpar = sp.simplify(1 - sp.diff(tp, X1) ** 2)
k8 = {"coef_(w.n)^2": str(coef), "leaf_metric_par": str(hpar)}
worst8 = 0.0
for Ls in LSTARS:
    L = Ls * PC
    a2_AU = (AU / L) ** 2
    a2_NS = (12e3 / L) ** 2
    k8[f"L{Ls}"] = {"alpha2_equiv_1AU": a2_AU, "ratio_vs_2.4e-7": a2_AU / 2.4e-7,
                    "alpha2hat_equiv_NS12km": a2_NS, "ratio_vs_1.6e-9": a2_NS / 1.6e-9}
    worst8 = max(worst8, a2_AU / 2.4e-7, a2_NS / 1.6e-9)
wcmb = 369.0e3 / c_SI
k8["w_CMB"] = wcmb
k8["delta_aP_rel"] = wcmb ** 2 / 2
k8["delta_aP_abs_L24_msun"] = wcmb ** 2 / 2 * GMSUN / (24 * PC) ** 2
k8["A22_D5_statement"] = "isotropic (1+2w^2) only; the tilt of the T-leaves (h_par = 1 - w^2) is not included"
res["K8"] = k8
log(f"   leaf metric along w: {hpar}; Phi_c anisotropy coefficient of (w.n)^2: {coef}; "
    f"alpha2-equiv at 1 AU (L*=24) {k8['L24']['alpha2_equiv_1AU']:.3e}; delta a_P = {k8['delta_aP_abs_L24_msun']:.2e} m/s^2")
check("K8", (coef == sp.Rational(-1, 2)) and worst8 < 1,
      f"coef = {coef}; max ratio to bounds = {worst8:.3e}", "coef -1/2 (sympy); ratios < 1")

# ============================================================ K9: GW170817
log("== K9 GW170817: tensor mass induced by the P background")
hp_, hx_, P0, gb_ = sp.symbols("h_p h_x P0 g_b", real=True)
Hm = sp.Matrix([[1 + hp_, hx_, 0], [hx_, 1 - hp_, 0], [0, 0, 1]])
sqrth = sp.sqrt(Hm.det())
Hinv = Hm.inv()
uexpr = K * sp.sqrt(Hinv[0, 0] * P0 ** 2)                    # P_i = (P0, 0, 0)
Wexpr = W.subs(u, uexpr)
clock = sqrth * Hinv[0, 0] * P0 * gb_                       # sqrt(h) P^x d_x N, background d_x N = g_b
Lmass = -sqrth * Wexpr + clock
c2p = sp.simplify(sp.diff(Lmass, hp_, 2).subs({hp_: 0, hx_: 0}) / 2)
c2x = sp.simplify(sp.diff(Lmass, hx_, 2).subs({hp_: 0, hx_: 0}) / 2)
# tensor kinetic normalisation: L_T = (1/8K)[hdot^2 - (grad h)^2]  ->  m^2 = -8K * c2
mp2 = sp.simplify(-8 * K * c2p)
mx2 = sp.simplify(-8 * K * c2x)
log(f"   m_+^2 = {mp2}\n   m_x^2 = {mx2}")
k9 = {"m_plus2": str(mp2), "m_cross2": str(mx2)}
fGW = 100.0
kGW = 2 * np.pi * fGW / c_SI
worst9 = 0.0
for fk, fa in A0.items():
    for gname, gval in [("galactic_g=a0", fa), ("Earth_surface_g", 9.81)]:
        # u <= a0 (cap), P0 = u/K, background lapse gradient g_b; all in 1/m (divide accelerations by c^2)
        vals = []
        for uf in [0.5, 0.9, 0.99]:
            sub = {K: 1, a0: fa / c_SI ** 2, P0: uf * fa / c_SI ** 2, gb_: gval / c_SI ** 2}
            vals.append(max(abs(float(mp2.subs(sub))), abs(float(mx2.subs(sub)))))
        m2 = max(vals)
        dv = m2 / (2 * kGW ** 2)
        k9[f"{fk}_{gname}"] = {"m2_per_m2": m2, "dv_over_c": dv}
        worst9 = max(worst9, dv)
        log(f"   {fk}, {gname}: |m^2| <= {m2:.3e} m^-2, dv/c at 100 Hz <= {dv:.3e}")
k9["tensor_principal_speed"] = "1 exactly (K_ij K^ij coefficient 1, beta = 0; C5 H1)"
res["K9"] = k9
check("K9", worst9 < 1e-15, f"max dv/c = {worst9:.3e}", "< 1e-15 (GW170817, record EMPIRICAL_TESTS A6)")

# ============================================================ K10: lensing vs dynamics (estimate, not scored)
log("== K10 lensing vs dynamics during time variation (ILLUSTRATIVE, not scored)")
RJ = 7.1492e7
k10 = {"jupiter_P_fraction_L24": (RJ / (24 * PC)) ** 2}
v_cl, r_cl, t_cl = 3.0e6, 3.0857e22, 0.3e9 * 3.156e7
k10["cluster_v2_over_c2"] = (v_cl / c_SI) ** 2
k10["cluster_a_r_over_c2"] = (v_cl / t_cl) * r_cl / c_SI ** 2
k10["note"] = "illustrative inputs (v=3000 km/s, r=1 Mpc, t_acc=0.3 Gyr); Phi = Psi at O(rho) at all times (A22 D3)"
res["K10"] = k10
check("K10", True, f"Jupiter P part {(RJ / (24 * PC)) ** 2:.2e}; cluster v^2/c^2 {k10['cluster_v2_over_c2']:.1e}, "
      f"a r/c^2 {k10['cluster_a_r_over_c2']:.1e}", "estimate only", scored=False)

# ============================================================ signal-size illustration (README item 3)
m_lab, dx_lab, r_lab = 1000.0, 1.0, 1000.0
res["signal_illustration"] = {fmt: G_SI * m_lab / (Ls * PC) ** 2 * dx_lab / r_lab for fmt, Ls in
                              [("L20", 20), ("L24", 24), ("L90", 90)]}
res["signal_illustration"]["setup"] = "1000 kg moved 1 m, test mass 1 km away: delta a ~ (G m/L*^2)(dx/r)"

# ============================================================ summary
scored = [c for c in checks if c["scored"]]
npass = sum(c["pass"] for c in scored)
wp = all(c["pass"] for c in scored if c["id"] in ("K1", "K2", "K3", "K4", "K5"))
obs = all(c["pass"] for c in scored if c["id"] in ("K7", "K8", "K9"))
verdict = ("WELL-POSED + UNCONSTRAINED" if wp and obs else
           "WELL-POSED + CONSTRAINED" if wp else "ILL-POSED (see failing K1-K5)")
res["verdict"] = verdict
res["checks"] = checks
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_gb = rss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
res["runtime_s"] = time.time() - T0
res["peak_rss_gb"] = rss_gb
log(f"VERDICT: {verdict}")
log(f"runtime {res['runtime_s']:.1f} s, peak RSS {rss_gb:.2f} GB")
log(f"C8_INSTANTANEOUS COMPLETE: {npass}/{len(scored)} checks PASS.")
with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(JSON, "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(0 if npass == len(scored) else 1)
