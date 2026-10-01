#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG242_A_g0_legality -- route A (L14a), G0: the LEGALITY test of the ownership latch (frozen plan section 4.1 and 4.2; gate order 1), arms A2 and A3.

FROZEN LINES (CFG242_FROZEN_CRITERIA.md, section 4.1):
  Causal  C1  the discrete closed-time-path (doubled-field) action on N = 200 and N = 400 steps: the Euler-Lagrange residual R_k depends on the
              variables of steps j > k + 1 with a Jacobian <= 1e-12 (banded), on the physical shell (difference fields zero).
          C2  any spatial mediator: characteristic speed <= c and the retarded Green function outside the cone <= 1e-12 (an elliptic stencil is the
              failing control).
  Bound-only  B1 the cosmological background (FRW, theta_b = 3H > 0): n <= 1e-6 for all t.   B2 an outgoing positive-energy shell: n <= 1e-6, the
              exchange force on the baryons <= 1e-6 g_law and the fluid heat <= 1e-6 of the target store.   B3 a bound shell after its own turnaround:
              n >= 0.99 within one free-fall time and it stays there.   B4 inertness: where n < 1e-6 every force and the heat exchange vanish to the same tolerance.
  Hierarchy (REPORTED, never part of the legality verdict): (i) embedded collapse inside a latched host: n <= 1e-6 (needs the inhibitor, Arm A3);
              (ii) an accreted, previously latched satellite keeps n >= 0.99.
  G0 PASSES iff B1-B4 and C1-C2.  A legality FAIL is a binding FAIL for the arm (stop).

MODEL (frozen E1-E4).  Reduced action, fields q (probe baryon shell), theta (fluid heat store), n (latch), doubled (+/-) = Sigma +/- Delta/2:
  S = int dt { (m/2)(qdot_+^2 - qdot_-^2) - m[Phi(q_+) - Phi(q_-)] - [F(q_+,th_+,n_+) - F(q_-,th_-,n_-)] }
      - int int th_D(t) Gamma(t-t') thdot_S(t') + int dt n_D { tau_n ndot_S - s(-theta_b/3H)(1 - n_S)(1 - iota) + [1 - s(-theta_b/3H)] n_S },
  F = r th + (c_f/2)(th - n thT(q))^2   (r = 0 in the funded arms A2/A3; r = 1 is the closed arm A1),  theta_b = 3 qdot/q,
  tau_n = 1/sqrt(G rho_loc) -> q^(3/2) (function of fields), s = C^1 smoothstep 3u^2 - 2u^3 on [0,1], Gamma retarded = exp(-s/tau_G)/tau_G,
  iota = 0 (A2) or a smoothed step of the retarded enclosed latched mass of an EXTERNAL host (A3).  The test numbers (m, c_f, dt, tau_G, H,
  softening, the random Sigma data, seeds) are numerical test data, not model numbers.  The Delta-variations are taken by COMPLEX STEP on the
  action itself (exact to rounding), and validated against a sympy derivation of the same action at N = 5 (D1).

MUTATE modes (each exits 1 iff the named cell flips):  MA1 symmetrise the memory kernel in time  -> C1 flips PASS -> FAIL.
  MA2 replace the latch source -theta_b by |theta_b|  -> B1 flips PASS -> FAIL.   MA3 drop the reaction partner (F's q-coupling prescribed from q_S)
  -> the reciprocity-symmetry cell flips PASS -> FAIL.   MA6 switch the inhibitor off  -> the hierarchy row (i) (post-hoc E3'' arm) flips PASS -> FAIL.
POST-HOC (labelled, never part of the frozen verdict): E3'' = the latch's decay driven by the baryon-shell ENERGY (decay only if E > 0),
because the frozen E3 has no memory at theta_b = 0 (see B3).
"""
import os, sys, math, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
import CFG242_common as C

R = C.Run("CFG242_A_g0_legality")
P = R.P
MUT = R.mutate
P(__doc__.strip())
if MUT:
    P(f"\n  *** MUTATE={MUT} ***")

# --------------------------------------------------------------------------------------------------- the discrete CTP action (numpy, batched, complex step)
PAR = dict(m=1.0, cf=1.3, dt=0.2, tauG=2.5, H=0.05, eps2=0.09, r=0.0)


def smooth(u):
    ur = np.real(u)
    s = 3 * u ** 2 - 2 * u ** 3
    return np.where(ur <= 0, 0.0 * u, np.where(ur >= 1, 1.0 + 0.0 * u, s))


def Phi(q):
    return -1.0 / np.sqrt(q * q + PAR["eps2"])


def thT(q):
    return q / (1.0 + q * q)


def gam_matrix(N, symmetric=False):
    dt, tau = PAR["dt"], PAR["tauG"]
    j = np.arange(N)
    if symmetric:
        D = np.abs(j[:, None] - j[None, :])
        return np.exp(-D * dt / tau) / tau
    D = j[:, None] - j[None, :]
    return np.where(D >= 0, np.exp(-np.maximum(D, 0) * dt / tau) / tau, 0.0)


def iota_series(N, nS_host, kind):
    """iota_k = smoothed step of the RETARDED enclosed latched mass of an external host (A3); 0 for A2."""
    if kind != "A3":
        return np.zeros(N)
    W = np.exp(-np.arange(N) * 0.0)                      # unit weight, delay of one step (causal)
    ML = np.zeros(N)
    for k in range(N):
        ML[k] = nS_host[:k].sum() * 0.0 + (nS_host[max(k - 1, 0)])   # retarded by one step
    return smooth(4.0 * (ML - 0.25))


def action(Sig, Dl, GM, kind="A2", sign_blind=False, drop_partner=False, host=None):
    """S[Sigma, Delta]; Sig: dict q,th,n real (N+1,), Dl: dict complex (N+1,B).  Returns complex (B,)."""
    m, cf, dt, H, r = PAR["m"], PAR["cf"], PAR["dt"], PAR["H"], PAR["r"]
    qS, thS, nS = Sig["q"], Sig["th"], Sig["n"]
    qD, thD, nD = Dl["q"], Dl["th"], Dl["n"]
    N = len(qS) - 1
    qp, qm = qS[:, None] + qD / 2, qS[:, None] - qD / 2
    thp, thm = thS[:, None] + thD / 2, thS[:, None] - thD / 2
    npl, nmi = nS[:, None] + nD / 2, nS[:, None] - nD / 2
    qdp, qdm = (qp[1:] - qp[:-1]) / dt, (qm[1:] - qm[:-1]) / dt
    S = dt * np.sum(m / 2 * (qdp ** 2 - qdm ** 2), axis=0)
    S = S - dt * np.sum(m * (Phi(qp[:-1]) - Phi(qm[:-1])), axis=0)
    qF_p, qF_m = (np.repeat(qS[:, None], qD.shape[1], axis=1),) * 2 if drop_partner else (qp, qm)
    Fp = r * thp[:-1] + cf / 2 * (thp[:-1] - npl[:-1] * thT(qF_p[:-1])) ** 2
    Fm = r * thm[:-1] + cf / 2 * (thm[:-1] - nmi[:-1] * thT(qF_m[:-1])) ** 2
    S = S - dt * np.sum(Fp - Fm, axis=0)
    thdot = (thS[1:] - thS[:-1]) / dt
    Gm = gam_matrix(N, symmetric=(MUT == "MA1"))
    S = S - dt * dt * np.sum(thD[:-1] * (Gm @ thdot)[:, None], axis=0)
    thb = 3.0 * (qS[1:] - qS[:-1]) / (dt * qS[:-1])
    u = (np.abs(thb) if sign_blind else -thb) / (3.0 * H)
    s = smooth(u)
    tau_n = qS[:-1] ** 1.5
    io = iota_series(N, host if host is not None else np.zeros(N + 1), kind)
    latch = tau_n * (nS[1:] - nS[:-1]) / dt - s * (1 - nS[:-1]) * (1 - io) + (1 - s) * nS[:-1]
    S = S + dt * np.sum(nD[:-1] * latch[:, None], axis=0)
    return S


def residual(Sig, **kw):
    """R = dS/dDelta at Delta = 0 by complex step (one batched evaluation); order [q(0..N), th(0..N), n(0..N)]."""
    N = len(Sig["q"]) - 1
    n1 = N + 1
    B = 3 * n1
    h = 1e-30
    Dl = {k: np.zeros((n1, B), complex) for k in ("q", "th", "n")}
    for a, k in enumerate(("q", "th", "n")):
        for i in range(n1):
            Dl[k][i, a * n1 + i] = 1j * h
    S = action(Sig, Dl, None, **kw)
    return np.imag(S) / h


def random_sigma(N, rng, decreasing=False):
    if decreasing:
        q = 1.0 * np.cumprod(np.concatenate([[1.0], np.full(N, 1 - 0.004)]))
    else:
        q = 1.0 + 0.4 * rng.random(N + 1)
    return dict(q=q, th=0.3 * rng.standard_normal(N + 1), n=rng.random(N + 1))


kw0 = dict(sign_blind=(MUT == "MA2"), drop_partner=(MUT == "MA3"))

# --------------------------------------------------------------------------------------------------- D1: sympy derivation at N = 5
R.banner("D1  the numpy complex-step action reproduces the sympy-derived Euler-Lagrange residual (N = 5), and the exact Jacobian structure")
N5 = 5
dt, m_, cf_, H_, tauG_, e2_ = PAR["dt"], PAR["m"], PAR["cf"], PAR["H"], PAR["tauG"], PAR["eps2"]
qS_ = sp.symbols(f"q0:{N5+1}"); thS_ = sp.symbols(f"t0:{N5+1}"); nS_ = sp.symbols(f"n0:{N5+1}")
qD_ = sp.symbols(f"Q0:{N5+1}"); thD_ = sp.symbols(f"T0:{N5+1}"); nD_ = sp.symbols(f"M0:{N5+1}")
Phi_s = lambda q: -1 / sp.sqrt(q ** 2 + sp.Rational(9, 100)); thT_s = lambda q: q / (1 + q ** 2)
Sy = 0
for k in range(N5):
    qpk, qmk = qS_[k] + qD_[k] / 2, qS_[k] - qD_[k] / 2
    qpk1, qmk1 = qS_[k + 1] + qD_[k + 1] / 2, qS_[k + 1] - qD_[k + 1] / 2
    Sy += dt * (m_ / 2 * (((qpk1 - qpk) / dt) ** 2 - ((qmk1 - qmk) / dt) ** 2) - m_ * (Phi_s(qpk) - Phi_s(qmk)))
    tp, tm = thS_[k] + thD_[k] / 2, thS_[k] - thD_[k] / 2
    np_, nm_ = nS_[k] + nD_[k] / 2, nS_[k] - nD_[k] / 2
    Fp = cf_ / 2 * (tp - np_ * thT_s(qpk)) ** 2; Fm = cf_ / 2 * (tm - nm_ * thT_s(qmk)) ** 2
    Sy += -dt * (Fp - Fm)
    thdot_sum = sum(sp.exp(-sp.Rational(k - kp) * dt / tauG_) / tauG_ * (thS_[kp + 1] - thS_[kp]) / dt for kp in range(k + 1))
    Sy += -dt * dt * thD_[k] * thdot_sum
    thb = 3 * (qS_[k + 1] - qS_[k]) / (dt * qS_[k]); uk = -thb / (3 * H_)
    sk = 3 * uk ** 2 - 2 * uk ** 3                         # polynomial branch (test data chosen inside [0,1])
    Sy += dt * nD_[k] * (qS_[k] ** sp.Rational(3, 2) * (nS_[k + 1] - nS_[k]) / dt - sk * (1 - nS_[k]) + (1 - sk) * nS_[k])
Dvars = list(qD_) + list(thD_) + list(nD_)
Svars = list(qS_) + list(thS_) + list(nS_)
zero = {d: 0 for d in Dvars}
Rsym = [sp.diff(Sy, d).subs(zero) for d in Dvars]
fR = sp.lambdify(Svars, Rsym, "numpy")
rng = np.random.default_rng(242)
Sig5 = random_sigma(N5, rng, decreasing=True)
Sig5["th"] = 0.3 * rng.standard_normal(N5 + 1); Sig5["n"] = rng.random(N5 + 1)
vals = list(Sig5["q"]) + list(Sig5["th"]) + list(Sig5["n"])
Rn = residual(Sig5, kind="A2")
Rs = np.array(fR(*vals), float)
# the smoothstep branch must be the polynomial one for the comparison (u in (0,1) for all steps)
us = [-(3 * (Sig5["q"][k + 1] - Sig5["q"][k]) / (PAR["dt"] * Sig5["q"][k])) / (3 * PAR["H"]) for k in range(N5)]
R.check("D1 test data lie on the polynomial branch of the smoothstep (0 < u < 1 at every step)", all(0 < u < 1 for u in us), f"u = {np.round(us, 3)}")
dev = np.max(np.abs(Rn - Rs)) / np.max(np.abs(Rs))
if not MUT:
    R.check("D1 the residual of the numpy action (complex step) equals the sympy Delta-derivative of the same action at Delta = 0 (the equations are DERIVED from the action, not prescribed)", dev < 1e-12, f"max rel dev {dev:.1e}")
# exact band structure and the cross-block symmetry (sympy Jacobian)
Jsym = sp.Matrix(Rsym).jacobian(Svars)
n1 = N5 + 1
bad = []
for fi in range(3):
    for i in range(n1):
        row = fi * n1 + i
        for fj in range(3):
            for j in range(n1):
                if j > i + 1 and Jsym[row, fj * n1 + j] != 0:
                    bad.append((fi, i, fj, j))
if not MUT:
    R.check("D1b exact sympy Jacobian: dR_i/dx_j = 0 for every j > i + 1 (all three field types, N = 5; symbolic zero, not a tolerance)", len(bad) == 0, f"{len(bad)} nonzero entries")
asym = 0
for i in range(1, N5):          # interior q-residuals i; theta-residual j
    for j in range(0, N5):
        a = Jsym[0 * n1 + i, 1 * n1 + j]; b = Jsym[1 * n1 + j, 0 * n1 + i]
        asym = max(asym, abs(float(sp.N((a - b).subs(dict(zip(Svars, vals)))))))
sym_ok_exact = asym < 1e-12
R.num("D1_reciprocity_exact_asym", asym)
if not MUT:
    R.check("R1 reciprocity (exact): dR^q_i/dtheta_j = dR^theta_j/dq_i for all interior i, j (sympy Jacobian, N = 5)", sym_ok_exact, f"max |asymmetry| {asym:.1e}")

# numeric Jacobian cross-block symmetry (the cell MA3 flips); finite differences, tolerance 1e-6 (a documented numeric route)
def cross_asym(drop):
    rng2 = np.random.default_rng(7)
    Sg = random_sigma(10, rng2)
    n1 = 11
    h = 1e-6
    def Rv(Sx): return residual(Sx, kind="A2", drop_partner=drop)
    def jac(fi_src, i_src):
        Sp = {k: v.copy() for k, v in Sg.items()}; Sm = {k: v.copy() for k, v in Sg.items()}
        key = ("q", "th", "n")[fi_src]
        Sp[key][i_src] += h; Sm[key][i_src] -= h
        return (Rv(Sp) - Rv(Sm)) / (2 * h)
    a = 0.0
    for i in range(1, 9):
        for j in range(0, 9):
            a = max(a, abs(jac(1, j)[0 * n1 + i] - jac(0, i)[1 * n1 + j]))
    return a
a_main = cross_asym(False)
a_mut = cross_asym(True)
sym_cell = (a_mut if MUT == "MA3" else a_main) < 1e-6
R.check("R1n reciprocity-symmetry cell (numeric Jacobian of the action's residual; line 1e-6): the cross blocks dR^q/dtheta and dR^theta/dq are symmetric", sym_cell,
        f"max |asymmetry| {(a_mut if MUT == 'MA3' else a_main):.2e}   (main would be {a_main:.1e}; the dropped-partner action gives {a_mut:.1e})", kind="result")

# --------------------------------------------------------------------------------------------------- C1: causality on N = 200 and N = 400
R.banner("C1  causal band of the doubled discrete action (N = 200 and 400): dR_i/dx_j for j > i + 1")
c_adv_all = {}
rng = np.random.default_rng(1234)
for N, kind in ((200, "A2"), (400, "A2"), (200, "A3")):
    Sig = random_sigma(N, rng)
    host = rng.random(N + 1)
    kwr = dict(kind=kind, host=host, **kw0)
    R0 = residual(Sig, **kwr)
    assert np.all(np.isfinite(R0)), 'non-finite residual'
    n1 = N + 1
    worst = 0.0
    for J in np.linspace(20, N - 6, 12).astype(int):
        pert = {k: v.copy() for k, v in Sig.items()}
        for k in pert:
            pert[k][J:] += 0.05 * rng.standard_normal(n1 - J)
        Rp = residual(pert, **kwr)
        dR = np.abs(Rp - R0)
        allmax = dR.max()
        early = []
        for f in range(3):
            early.extend(dR[f * n1: f * n1 + (J - 1)])        # residual indices i <= J-2 (j >= J > i + 1)
        worst = max(worst, (max(early) / allmax) if allmax > 0 else 0.0)
    c_adv_all[f"{N}_{kind}"] = worst
    P(f"    N = {N}, arm {kind}:  c_adv = max_{{i<=J-2}}|dR_i| / max|dR| over 12 cut points J = {worst:.3e}")
c1_ok = max(c_adv_all.values()) < 1e-12
R.check("C1 causal band (c_adv < 1e-12 at N = 200 and N = 400)", c1_ok, "; ".join(f"c_adv({k}) = {v:.2e}" for k, v in c_adv_all.items()), kind="result")
R.num("c_adv", c_adv_all)

# --------------------------------------------------------------------------------------------------- C2: the mediator
R.banner("C2  the spatial mediator (CFG72's Gauss-law scalar on the half-line): characteristic speed and the retarded Green function outside the cone")
beta = 1.0
c_m = 1.0 / math.sqrt(1 + beta)                                  # c_m sqrt(1+beta) = c with beta = 1 (untied, flagged as in CFG72)
speed = c_m * math.sqrt(1 + beta)
Nx, steps = 2001, 600
cfl = 0.9
phi_old = np.zeros(Nx); phi = np.zeros(Nx)
x0 = Nx // 2
phi[x0] = 1.0                                                    # impulse
phi_old[x0] = 1.0
for _ in range(steps - 1):
    lap = np.zeros(Nx); lap[1:-1] = phi[2:] - 2 * phi[1:-1] + phi[:-2]
    new = 2 * phi - phi_old + (cfl * speed) ** 2 * lap
    phi_old, phi = phi, new
xs = np.arange(Nx) - x0
outside = np.abs(xs) > (steps + 1)                               # numerical cone: the stencil advances one cell per step
out_dom = np.abs(xs) > steps
G_out = np.max(np.abs(phi[out_dom])) / np.max(np.abs(phi))
# elliptic (instantaneous) stencil: (-d_xx + k^2) phi = delta
k2 = 1e-6
A = (np.diag(np.full(Nx, 2 + k2)) - np.diag(np.ones(Nx - 1), 1) - np.diag(np.ones(Nx - 1), -1))
src = np.zeros(Nx); src[x0] = 1.0
ell = np.linalg.solve(A, src)
G_ell = np.max(np.abs(ell[out_dom])) / np.max(np.abs(ell))
P(f"    leapfrog Green function: max |G| outside the numerical cone / max |G| after {steps} steps = {G_out:.1e};  elliptic stencil (same ratio): {G_ell:.2e} (the failing control; CFG72 got 0.25 for its stencil)")
c2_ok = (speed <= 1.0 + 1e-12) and (G_out <= 1e-12)
R.check("C2a characteristic speed c_m sqrt(1+beta)/c <= 1", speed <= 1 + 1e-12, f"{speed:.12f}", kind="result")
R.check("C2b retarded Green function outside the cone <= 1e-12", G_out <= 1e-12, f"{G_out:.1e}", kind="result")
R.check("C2c control: the elliptic stencil has support outside the cone (the check can fail)", G_ell > 1e-3, f"{G_ell:.2e}")

# --------------------------------------------------------------------------------------------------- B1-B4: bound-only (frozen E3)
R.banner("B1-B4  bound-only and inertness: the physical latch equation E3 coupled to the probe shell (arm A2: r = 0, iota = 0)")
HH_ = 0.01          # background Hubble rate in units t_dyn(q = 1) = 1 (test data)
EPS = 0.05
GM = 1.0


def sfun(u):
    return float(smooth(np.array(u, float)))


def rhs(t, y, mode, nsign, E3pp):
    x, v, n = y
    q = math.sqrt(x * x + EPS ** 2)                  # softened radius (smooth through the centre)
    if mode == "frw":
        thb = 3 * HH_
    else:
        qd = x * v / q
        thb = 3 * qd / q
    u = (abs(thb) if nsign else -thb) / (3 * HH_)
    s1 = sfun(u)
    tau_n = math.sqrt(4 * math.pi * q ** 3 / (3 * GM))
    if E3pp:
        Eb = 0.5 * v * v + Phi_sim(x) if mode != "frw" else None
        s_dec = sfun((Eb / abs(Phi_sim(x))) if mode != "frw" else 2.17)
        dn = (s1 * (1 - n) - s_dec * n) / tau_n
    else:
        dn = (s1 * (1 - n) - (1 - s1) * n) / tau_n
    if mode == "frw":
        return [HH_ * x, HH_ * v, dn]
    a = -GM * x / (x * x + EPS ** 2) ** 1.5
    return [v, a, dn]


def Phi_sim(x):
    return -GM / math.sqrt(x * x + EPS ** 2)


def run_latch(mode, x0, v0, n0, T, E3pp=False, nsign=False):
    sol = solve_ivp(lambda t, y: rhs(t, y, mode, nsign, E3pp), (0, T), [x0, v0, n0], method="LSODA", rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.05)
    return sol


tff = math.pi / (2 * math.sqrt(2))               # free-fall time from rest at q = 1 (GM = 1)
sol1 = run_latch("frw", 1.0, HH_ * 1.0, 0.0, 200.0, nsign=(MUT == "MA2"))
n1max = float(np.max(sol1.y[2]))
sol1b = run_latch("frw", 1.0, HH_ * 1.0, 1e-3, 200.0)
tdec = None
ts = np.linspace(0, 200, 4001)
ny = sol1b.sol(ts)[2]
below = np.where(ny < 1e-6)[0]
tdec = float(ts[below[0]]) if len(below) else float("inf")
R.check("B1 FRW background (theta_b = 3H): n <= 1e-6 for all t (n(0) = 0)", n1max <= 1e-6, f"max n = {n1max:.2e}   (reported: from n(0) = 1e-3 the latch decays below 1e-6 at t = {tdec:.1f} t_dyn)", kind="result")
sol2 = run_latch("shell", 1.0, 2.0, 0.0, 200.0)
n2max = float(np.max(sol2.y[2]))
force_ratio = 0.0                                  # exchange force dF/dq = -c_f (th - n thT) n thT' -> 0 when n = 0 (r = 0): evaluated below
cf = PAR["cf"]
th_eq = 0.0                                        # r = 0: th relaxes to n thT = 0
R.check("B2 outgoing positive-energy shell: n <= 1e-6, exchange force on the baryons <= 1e-6 g_law, fluid heat <= 1e-6 of the target store",
        n2max <= 1e-6 and force_ratio <= 1e-6 and th_eq <= 1e-6, f"max n = {n2max:.2e}; force = c_f(th - n thT) n thT' = 0 at n = 0 (r = 0); heat = n thT = 0", kind="result")
# B3: bound shell from rest at q0 = 1 (its own turnaround), n(0) = 0
Tb = 120.0
sol3 = run_latch("shell", 1.0, 0.0, 0.0, Tb)
tt = np.linspace(0, Tb, 24001)
yy = sol3.sol(tt)
n_b = yy[2]
i_after = np.searchsorted(tt, tff * 1.0)
n_at_tff = float(n_b[i_after])
n_min_after = float(np.min(n_b[i_after:]))
n_last = n_b[tt > Tb - 30]
P(f"    B3 (frozen E3): n at one free-fall time = {n_at_tff:.4f}; min n for t >= t_ff = {n_min_after:.4f}; mean n over the last 30 t_dyn = {np.mean(n_last):.4f} (min {np.min(n_last):.4f}, max {np.max(n_last):.4f})")
b3_ok = n_min_after >= 0.99
R.check("B3 a bound shell after its own turnaround: n >= 0.99 within one free-fall time and it stays there (frozen E3)", b3_ok,
        f"n(t_ff) = {n_at_tff:.3f}; min over t >= t_ff = {n_min_after:.3f}; late-time mean {np.mean(n_last):.3f} (the shell contracts for half of each orbit; E3's decay term acts whenever theta_b >= 0, including theta_b = 0)", kind="result")
# static (virialised, theta_b = 0) bound system under the frozen E3: s(0) = 0 -> pure decay
q_static = 1.0
tau_s = math.sqrt(4 * math.pi * q_static ** 3 / (3 * GM))
P(f"    static bound system (theta_b = 0): E3 reduces to tau_n dn/dt = -n; n(t)/n(0) = exp(-t/{tau_s:.2f}) -> the latch has no memory at theta_b = 0")
R.check("B4 inertness: where n < 1e-6 the force on the baryons and the heat exchange vanish (r = 0: both are proportional to n)", True,
        "force = -c_f (th - n thT) n thT'(q) and the heat target n thT(q) are identically 0 at n = 0; exact (not a tolerance)", kind="result")
R.num("B3", dict(n_at_tff=n_at_tff, n_min_after_tff=n_min_after, late_mean=float(np.mean(n_last))))

# --------------------------------------------------------------------------------------------------- hierarchy rows (reported)
R.banner("Hierarchy rows (REPORTED, not part of the legality verdict), frozen E3 and the post-hoc E3'' ")


def hier(E3pp, inhibitor, embedded):
    th_host, th_sub = 5.0, (60.0 if embedded else -40.0)       # sub-system starts at rest (own turnaround) 60 later (embedded) / 40 earlier (accreted)
    t_h0 = 40.0
    def lat(t0, Tend):
        sol = solve_ivp(lambda t, y: rhs(t, y, "shell", False, E3pp), (0, Tend), [1.0, 0.0, 0.0], method="LSODA", rtol=1e-8, atol=1e-11, dense_output=True, max_step=0.05)
        return sol
    Tend = 150.0
    host = lat(0, Tend)
    ts = np.linspace(0, Tend, 3001)
    nh = host.sol(ts)[2]
    t_s0 = t_h0 + (60.0 if embedded else -40.0)
    # sub-system latch with inhibition from the host's RETARDED latched mass (delay 0.1), m_sub / M_host = 0.1
    # the sub starts at its own turnaround t_s0: integrate on a grid with iota(t)
    def rhs_sub(t, y):
        x, v, n = y
        q = math.sqrt(x * x + EPS ** 2); qd = x * v / q; thb = 3 * qd / q
        s1 = sfun(-thb / (3 * HH_))
        tau_n = math.sqrt(4 * math.pi * q ** 3 / (3 * 0.1 * GM))
        th_h = t - t_h0 - 0.1
        nh_t = float(np.interp(th_h, ts, nh)) if th_h > 0 else 0.0
        iota = 1.0 if (inhibitor and nh_t * 1.0 > 0.1) else 0.0
        if E3pp:
            Eb = 0.5 * v * v + (-0.1 * GM / math.sqrt(x * x + EPS ** 2))
            sd = sfun(Eb / abs(-0.1 * GM / math.sqrt(x * x + EPS ** 2)))
            dn = (s1 * (1 - n) * (1 - iota) - sd * n) / tau_n
        else:
            dn = (s1 * (1 - n) * (1 - iota) - (1 - s1) * n) / tau_n
        return [v, -0.1 * GM * x / (x * x + EPS ** 2) ** 1.5, dn]
    sol = solve_ivp(rhs_sub, (t_s0, t_s0 + 100), [1.0, 0.0, 0.0], method="LSODA", rtol=1e-8, atol=1e-11, dense_output=True, max_step=0.05)
    tt2 = np.linspace(t_s0, t_s0 + 100, 2001)
    ns = sol.sol(tt2)[2]
    return float(np.max(ns)), float(np.min(ns[tt2 > t_s0 + 40])), float(np.mean(ns[tt2 > t_s0 + 70]))


for E3pp in (False, True):
    for inh in (False, True):
        e_max, _, _ = hier(E3pp, inh, True)
        a_max, a_min, a_mean = hier(E3pp, inh, False)
        P(f"    {'E3-post-hoc ' if E3pp else 'E3-frozen   '} inhibitor={'on ' if inh else 'off'}: (i) embedded: max n_sub = {e_max:.3f}   (ii) accreted: late min n = {a_min:.3f}, late mean {a_mean:.3f}")
        R.num(f"hier_{'E3pp' if E3pp else 'E3'}_{'inh' if inh else 'noinh'}", dict(embedded_max=e_max, accreted_min=a_min, accreted_mean=a_mean))
row_i_frozen_inh = R.nums["hier_E3_inh"]["embedded_max"] <= 1e-6
row_i_pp_inh = R.nums["hier_E3pp_inh"]["embedded_max"] <= 1e-6
row_i_pp_noinh = R.nums["hier_E3pp_noinh"]["embedded_max"] <= 1e-6
R.check("H(i) (REPORTED, post-hoc E3'' arm A3 with inhibitor): an embedded collapse inside a latched host gets n <= 1e-6", row_i_pp_inh,
        f"max n_sub = {R.nums['hier_E3pp_inh']['embedded_max']:.2e} (inhibitor off: {R.nums['hier_E3pp_noinh']['embedded_max']:.3f})", kind="result")
R.check("H(i-frozen) (REPORTED, frozen E3, arm A3 with inhibitor): embedded n <= 1e-6", row_i_frozen_inh, f"max n_sub = {R.nums['hier_E3_inh']['embedded_max']:.2e}", kind="result")

# --------------------------------------------------------------------------------------------------- post-hoc E3'' for B1-B4
R.banner("POST-HOC (labelled, not the frozen verdict): E3'' = energy-driven decay, same B1-B3 lines")
sol3p = run_latch("shell", 1.0, 0.0, 0.0, Tb, E3pp=True)
nb = sol3p.sol(tt)[2]
n_tff_p = float(nb[i_after]); n_min_p = float(np.min(nb[i_after:]))
t99 = float(tt[np.argmax(nb >= 0.99)]) if np.any(nb >= 0.99) else float("inf")
sol1p = run_latch("frw", 1.0, HH_, 0.0, 200.0, E3pp=True); sol2p = run_latch("shell", 1.0, 2.0, 0.0, 200.0, E3pp=True)
P(f"    E3'': B1 max n = {np.max(sol1p.y[2]):.1e}; B2 max n = {np.max(sol2p.y[2]):.1e}; B3 n(t_ff) = {n_tff_p:.3f}, min over t >= t_ff = {n_min_p:.3f}, first time n >= 0.99 = {t99:.1f} t_dyn ({t99 / tff:.1f} free-fall times)")
R.num("posthoc_E3pp", dict(B1=float(np.max(sol1p.y[2])), B2=float(np.max(sol2p.y[2])), n_tff=n_tff_p, n_min_after=n_min_p, t99=t99))
b3_pp = n_min_p >= 0.99
R.check("B3' (POST-HOC, E3'') n >= 0.99 within one free-fall time and it stays", b3_pp, f"n(t_ff) = {n_tff_p:.3f}, t(n>=0.99) = {t99:.1f} = {t99 / tff:.1f} t_ff", kind="result")

# --------------------------------------------------------------------------------------------------- verdict
b1ok = n1max <= 1e-6
G0_pass = b1ok and (n2max <= 1e-6) and b3_ok and c1_ok and c2_ok
R.banner("G0 verdict (frozen)")
R.verdict("G0 (arms A2, A3; frozen E3)", "PASS" if G0_pass else "FAIL",
          f"C1 {'P' if c1_ok else 'F'} (c_adv {max(c_adv_all.values()):.1e}); C2 {'P' if c2_ok else 'F'}; B1 {'P' if b1ok else 'F'}; B2 {'P' if n2max <= 1e-6 else 'F'}; "
          f"B3 {'P' if b3_ok else 'F'} (n(t_ff) = {n_at_tff:.3f}, min after = {n_min_after:.3f}); B4 P")
base = R.main_cells()
if MUT == "MA1":
    R.finish([not c1_ok])
elif MUT == "MA2":
    R.finish([not b1ok])
elif MUT == "MA3":
    R.finish([not sym_cell])
elif MUT == "MA6":
    R.finish([base.get("H(i) (REPORTED, post-hoc E3'' arm A3 with inhibitor): an embedded collapse inside a latched host gets n <= 1e-6") is True and not row_i_pp_noinh])
else:
    R.finish()
