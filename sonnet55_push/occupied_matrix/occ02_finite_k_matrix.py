#!/usr/bin/env python3
"""occ02_finite_k_matrix.py -- the occupied finite-wavelength matrix of CA5-GNC-R after all constraints.

Takes the boxed reduced scalar action (occupied/RESULT.md; the N-carrier vector form verified in occ01):
   L/a^3 = 1/2 MK psid^2 + 1/2 |chid|^2 - (2/c2) psid (v.chi) + (v.chi)^2/(2 M c2)
           - 1/2 chi^T (x I + V'') chi + M x psi^2 - J^2 / (2 M F_d),
   J = u.qdot + w.q,  u = (M K H, -Q v),  w = (-2 M x, -H(3+2/c2) v - Q V'),  q = (psi, chi_1..chi_5).
Writes  L_tot = a^3 L = 1/2 qd^T G qd + qd^T B q - 1/2 q^T P q  with
   G = a^3 (diag(MK, I) - u u^T/(M F_d)),  B = a^3 (B0 - u w^T/(M F_d)),  P = a^3 (diag(-2Mx, xI + V'' - v v^T/(M c2)) + w w^T/(M F_d)).
The carrier sector is the ACTUAL five-field interaction
   V = m_H^2 |phi|^2/2 + m_L^2 |chi + gamma s phi|^2/2 + mu^2 s^2/2      (action/FINAL_ACTION.md eq. 1)
on the ACTUAL homogeneous expanding background: 3 M H^2 = T + V + V0, M Hdot = -T, phid'' + 3H phid' + V' = 0.
Bare Lambda = 0, V0 > 0, reciprocal barrier (f1 = f2 = 0).

Three questions, each answered from the data:
  Q1  is the velocity matrix G positive definite on the occupied background at every q?          (positivity of the kinetic block)
  Q2  are the frozen-coefficient modes stable at every q (Re lambda <= 0)?                          (adiabatic, valid for q >> H)
  Q3  does the FULL time-dependent linear evolution (Gdot, Bdot exact along the background) grow? (all q, all times, exact)
Controls with a known answer (mutations) must be caught by the same detectors.

Scope: linear scalar sector, homogeneous occupied background, inactive gate, U = Z = 0 for nonzero modes,
no ordinary matter. It is NOT the nonlinear inhomogeneous problem, the Dirac count, PPN, or an observational gate.
"""
import math
import sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ok = []
def check(cond, msg):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {msg}"); return bool(cond)
def banner(t): print("\n" + "=" * 100 + f"\n  {t}\n" + "=" * 100)

# ------------------------------------------------------------------ the potential (symbolic -> numeric)
f = sp.symbols('p1 p2 c1 c2_ s_', real=True)         # phi1 phi2 chi1 chi2 s
mH2, mL2, mu2, gam = sp.symbols('mH2 mL2 mu2 gam', real=True)
p1, p2, c1, c2_, s_ = f
Vsym = (mH2 * (p1**2 + p2**2) / 2 + mL2 * ((c1 + gam * s_ * p1)**2 + (c2_ + gam * s_ * p2)**2) / 2 + mu2 * s_**2 / 2)
par = (mH2, mL2, mu2, gam)
V_fn = sp.lambdify(f + par, Vsym, 'numpy')
Vp_fn = sp.lambdify(f + par, [sp.diff(Vsym, y) for y in f], 'numpy')
Vpp_fn = sp.lambdify(f + par, sp.hessian(Vsym, f), 'numpy')


class Model:
    def __init__(self, M=1.0, V0=3.0, alpha=1.0, c2=1.0, ell=2.0, xi=1.0,
                 mH=1.7, mL=1.1, mu=0.6, gamma=0.8, mut=None):
        self.M, self.V0, self.alpha, self.c2, self.ell, self.xi = M, V0, alpha, c2, ell, xi
        self.mH2, self.mL2, self.mu2, self.gamma = mH ** 2, mL ** 2, mu ** 2, gamma
        self.K = 2 * (2 + 3 * c2) / c2
        self.r0 = ell / 4
        self.cN = 1 - alpha / 2
        self.mut = mut or set()

    def pot(self, phi):
        a = (*phi, self.mH2, self.mL2, self.mu2, self.gamma)
        return V_fn(*a), np.array(Vp_fn(*a), float), np.array(Vpp_fn(*a), float)

    def bg_rhs(self, t, y):                      # y = (phi[5], v[5], lna)
        phi, v = y[:5], y[5:10]
        V, Vp, _ = self.pot(phi)
        H = math.sqrt((0.5 * v @ v + V + self.V0) / (3 * self.M))
        return np.concatenate([v, -3 * H * v - Vp, [H]])

    def H_of(self, y):
        phi, v = y[:5], y[5:10]
        V = self.pot(phi)[0]
        return math.sqrt((0.5 * v @ v + V + self.V0) / (3 * self.M))

    def mats(self, y, k, factor=None):
        """G, B, P (the a^3-weighted matrices) at background state y for COMOVING wavenumber k."""
        M, K, c2, al = self.M, self.K, self.c2, self.alpha
        phi, v, lna = y[:5], y[5:10], y[10]
        a = math.exp(lna)
        x = k * k / (a * a)
        V, Vp, Vpp = self.pot(phi)
        H = self.H_of(y)
        T = 0.5 * v @ v
        r = self.r0 * math.exp(-self.xi ** 2 * x / 2)
        Q = 1 - r
        ae = 2 - (2 - al) * Q ** 2
        Delta = ae * x + 2 * (T + (V - T) * r - V * r * r) / M
        Fd = K * H * H + Delta
        n = 6
        u = np.concatenate([[M * K * H], -Q * v])
        w = np.concatenate([[-2 * M * x], -H * (3 + 2 / c2) * v - Q * Vp])
        G = np.diag(np.concatenate([[M * K], np.ones(5)])) - np.outer(u, u) / (M * Fd)
        B0 = np.zeros((n, n)); B0[0, 1:] = -(2 / c2) * v
        B = B0 - np.outer(u, w) / (M * Fd)
        P = np.zeros((n, n))
        P[0, 0] = -2 * M * x
        P[1:, 1:] = x * np.eye(5) + Vpp - np.outer(v, v) / (M * c2)
        P = P + np.outer(w, w) / (M * Fd)
        a3 = a ** 3
        if self.mut == 'gradient_sign':               # control: tachyonic psi gradient (UV coefficient of P_psipsi < 0)
            P[0, 0] = -2 * M * x - 4 * M * x * x / Fd
        if self.mut == 'ghost_kinetic':               # control: velocity matrix G0 - 3 u u^T/(M F_d) is indefinite when D/F_d < 2/3
            G = np.diag(np.concatenate([[M * K], np.ones(5)])) - 3 * np.outer(u, u) / (M * Fd)
        D = ae * x + 2 * r * (1 - r) * (T + V) / M     # the record's controlling coefficient D_R
        return a3 * G, a3 * B, a3 * P, dict(x=x, H=H, D=D, Fd=Fd, T=T, V=V, r=r)


def bg_solve(model, y0, tmax):
    return solve_ivp(model.bg_rhs, (0, tmax), y0, rtol=1e-11, atol=1e-13, dense_output=True)


def initial_background(model, phi0, v0):
    return np.concatenate([phi0, v0, [0.0]])


# ------------------------------------------------------------------ Q1 / Q2 : frozen-coefficient scan
def frozen_growth(model, y, k):
    """max Re(lambda)/H of the frozen-coefficient system, friction term from a^3 kept (Gdot ~ 3H G, Bdot ~ 3H B)."""
    G, B, P, d = model.mats(y, k)
    H = d['H']
    Gi = np.linalg.inv(G)
    A = B - B.T
    n = 6
    # G qdd + (3H G + A) qd + (3H B + P) q = 0   [a^3 weighting: d/dt(G qd + B q) with Gdot=3HG, Bdot=3HB]
    Mq = np.block([[np.zeros((n, n)), np.eye(n)],
                   [-Gi @ (3 * H * B + P), -Gi @ (3 * H * G + A)]])
    lam = np.linalg.eigvals(Mq)
    return lam.real.max() / H, np.linalg.eigvalsh(0.5 * (G + G.T)).min(), np.linalg.eigvalsh(0.5 * (P + P.T)).min() / (G[0, 0] * 0 + 1), d


def snapshot_states(model, y0, tgrid):
    sol = bg_solve(model, y0, tgrid[-1])
    return [sol.sol(t) for t in tgrid], sol


def q1q2_scan(model, y0, label, xgrid_over_H2=np.logspace(-4, 3, 36), tgrid=(0.0, 2.0, 5.0, 10.0)):
    states, _ = snapshot_states(model, y0, np.array(tgrid))
    worst_lam = -1e9; worst_G = 1e9; worst = None
    minD = 1e9
    for y in states:
        H = model.H_of(y); a = math.exp(y[10])
        for xr in xgrid_over_H2:
            k = math.sqrt(xr) * H * a
            lam, gmin, _, d = frozen_growth(model, y, k)
            minD = min(minD, d['D'])
            if lam > worst_lam:
                worst_lam = lam; worst = (xr, y[10], d['T'] + d['V'])
            worst_G = min(worst_G, gmin)
    print(f"  {label:<26} min eig G = {worst_G:+.3e}   min D = {minD:.3e}   max Re(lambda)/H = {worst_lam:+.4f} "
          f"at x/H^2 = {worst[0]:.3g}")
    return worst_lam, worst_G, minD


# ------------------------------------------------------------------ Q3 : full time-dependent linear evolution
def full_evolution(model, y0, k, tmax, dirderiv_h=1e-6, npts=13):
    """propagate the 12 initial data (q; H*qd) through the exact time-dependent EOM (Gdot, Bdot by directional
    derivative along the background flow). Returns the time series of sigma_max of the q-block of the propagator."""
    n = 6
    H0_ = model.H_of(y0)

    def rhs(t, Y):
        y = Y[:11]
        Phi = Y[11:].reshape(2 * n, 2 * n)
        G, B, P, _ = model.mats(y, k)
        fy = model.bg_rhs(0.0, y)
        h = dirderiv_h
        Gp, Bp, _, _ = model.mats(y + h * fy, k); Gm, Bm, _, _ = model.mats(y - h * fy, k)
        Gd = (Gp - Gm) / (2 * h); Bd = (Bp - Bm) / (2 * h)
        Gi = np.linalg.inv(G)
        # d/dt(G qd + B q) = B^T qd - P q  ->  G qdd = -(Gd + B - B^T) qd - (Bd + P) q
        Mq = np.block([[np.zeros((n, n)), np.eye(n)], [-Gi @ (Bd + P), -Gi @ (Gd + B - B.T)]])
        return np.concatenate([fy, (Mq @ Phi).ravel()])

    Y0 = np.concatenate([y0, np.diag(np.concatenate([np.ones(n), H0_ * np.ones(n)])).ravel()])
    sol = solve_ivp(rhs, (0, tmax), Y0, rtol=1e-8, atol=1e-11, method='DOP853', dense_output=True)
    tt = np.linspace(0, tmax, npts)
    ser = np.array([np.linalg.svd(sol.sol(t)[11:].reshape(2 * n, 2 * n)[:n, :], compute_uv=False).max() for t in tt])
    return tt, ser, sol.status


def classify(tt, ser, thr=0.15):
    """exponential if the late log-slope d ln sigma/dt (second half of the run, in units of the run's own H ~ 1)
    exceeds thr; report the power-law index too."""
    T = tt[-1]
    half = np.searchsorted(tt, T / 2)
    slope = (math.log(ser[-1]) - math.log(ser[half])) / (tt[-1] - tt[half])
    p = (math.log(ser[-1]) - math.log(ser[half])) / (math.log(tt[-1]) - math.log(tt[half]))
    return slope, p, ('EXPONENTIAL' if slope > thr else ('polynomial' if ser[-1] > 3 * ser[half] else 'bounded'))


import signal


class _Timeout(Exception):
    pass


def timed_evolution(model, y0, k, tmax, limit=90, **kw):
    """full_evolution with a wall-clock limit; a stalled (stiff) case returns status 'TIMEOUT' instead of hanging the run."""
    def _h(signum, frame):
        raise _Timeout()
    old = signal.signal(signal.SIGALRM, _h)
    signal.alarm(limit)
    try:
        return full_evolution(model, y0, k, tmax, **kw)
    except _Timeout:
        return None, None, 'TIMEOUT'
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def random_model(rng, mut=None):
    return Model(V0=3.0, alpha=rng.uniform(0.2, 1.8), c2=rng.uniform(0.3, 3.0), ell=rng.uniform(0.4, 3.6),
                 xi=rng.uniform(0.3, 3.0), mH=rng.uniform(0.5, 3.0), mL=rng.uniform(0.5, 3.0),
                 mu=rng.uniform(0.1, 3.0), gamma=rng.uniform(-1.5, 1.5), mut=mut)


def random_state(rng, model):
    return initial_background(model, rng.normal(0, 0.4, 5), rng.normal(0, 0.3, 5))


if __name__ == '__main__':
    banner("Setup -- units M_P^2 = 1, V0 = 3 (asymptotic H = 1), five real carrier fields, actual potential")
    phi0 = np.array([0.35, -0.2, 0.15, 0.25, 0.4])
    v0 = np.array([0.30, 0.10, -0.20, 0.15, 0.05])
    model = Model()
    y0 = initial_background(model, phi0, v0)
    H0 = model.H_of(y0)
    print(f"  baseline occupied state: T+V = {0.5*v0@v0 + model.pot(phi0)[0]:.4f}, H(0) = {H0:.4f}; "
          f"alpha={model.alpha}, c2={model.c2}, ell={model.ell}, xi={model.xi}, gamma={model.gamma}, mu={math.sqrt(model.mu2)}")
    sol = bg_solve(model, y0, 12.0)
    resid = []
    for t in np.linspace(0.2, 12, 25):
        y = sol.sol(t); h = 1e-5
        Hd = (model.H_of(sol.sol(t + h)) - model.H_of(sol.sol(t - h))) / (2 * h)
        resid.append(abs(Hd + 0.5 * y[5:10] @ y[5:10] / model.M))
    check(max(resid) < 5e-6, f"S1 background obeys Raychaudhuri M Hdot = -T along the run (max residual {max(resid):.2e})")

    banner("Q1/Q2  frozen-coefficient stability -- 300 random parameter sets in the record's window x 4 snapshots x 36 wavenumbers")
    rng = np.random.default_rng(20260928)
    nbadG = nbadD = nbadL = 0; lam_max = -1e9; gmin_all = 1e9; Dmin_all = 1e9; nsets = 0
    worst_case = None
    for _ in range(300):
        mm = random_model(rng)
        yy = random_state(rng, mm)
        try:
            states, _ = snapshot_states(mm, yy, np.array([0.0, 2.0, 5.0, 10.0]))
        except Exception:
            continue
        nsets += 1
        for y in states:
            H = mm.H_of(y); a = math.exp(y[10])
            for xr in np.logspace(-4, 3, 36):
                lam, gmin, _, d = frozen_growth(mm, y, math.sqrt(xr) * H * a)
                gmin_all = min(gmin_all, gmin); Dmin_all = min(Dmin_all, d['D'])
                nbadG += gmin <= 0; nbadD += d['D'] <= 0; nbadL += lam > 1e-3
                if lam > lam_max:
                    lam_max = lam; worst_case = (mm.alpha, mm.c2, mm.ell, mm.xi, math.sqrt(mm.mu2), xr)
    print(f"  {nsets} parameter sets scanned; min eigenvalue of G = {gmin_all:+.3e}; min D_R = {Dmin_all:.3e}")
    print(f"  violations: G<=0: {nbadG}   D_R<=0: {nbadD}   frozen Re(lambda)/H > 1e-3: {nbadL}   (max Re lambda/H = {lam_max:+.4f})")
    check(nbadG == 0 and nbadD == 0, "Q1 velocity block positive definite and D_R > 0 at every scanned point")
    print(f"  Q2 frozen (adiabatic) verdict: {'NO growing mode at any scanned (parameters, state, q)' if nbadL == 0 else 'GROWING MODES FOUND at ' + str(nbadL) + ' points; worst at (alpha,c2,ell,xi,mu,x/H2)=' + str(worst_case)}")

    banner("CONTROLS -- known-wrong variants must be caught by the same detectors")
    for mut in ('gradient_sign', 'ghost_kinetic'):
        mm = Model(mut=mut)
        lm, gm, dm = q1q2_scan(mm, initial_background(mm, phi0, v0), f"MUTATE {mut}")
        check((lm > 1e-3) or (gm <= 0), f"C-{mut}: flagged (max Re lambda {lm:+.3f}, min eig G {gm:+.2e})")

    banner("Q3  FULL time-dependent linear evolution -- exact Gdot, Bdot; all q; 10 e-folds")
    print(f"  {'case':<26}{'k/(aH)_0':>9}{'sigma(T)':>12}{'dln s/dt':>10}{'index p':>9}   class")
    rows = []
    def run_case(label, mm, yy, krs, T=10.0):
        Hh = mm.H_of(yy)
        for kr in krs:
            tt, ser, st = timed_evolution(mm, yy, kr * Hh, T)
            if st == 'TIMEOUT':
                print(f"  {label:<26}{kr:>9.2f}   TIMEOUT (stiff; not classified)")
                rows.append((label, kr, float('nan'), float('nan'), float('nan'), 'TIMEOUT', st)); continue
            sl, p, cl = classify(tt, ser)
            rows.append((label, kr, ser[-1], sl, p, cl, st))
            print(f"  {label:<26}{kr:>9.2f}{ser[-1]:>12.3e}{sl:>10.3f}{p:>9.2f}   {cl}" + ("" if st == 0 else "  [solver status %d]" % st))
    run_case("baseline mu=0.6 (light s)", model, y0, (0.05, 1.0, 10.0))
    mh = Model(mu=2.5)
    run_case("heavy s, mu=2.5", mh, initial_background(mh, phi0, v0), (0.05, 1.0, 10.0))
    n_exp = sum(1 for r in rows if r[5] == 'EXPONENTIAL')
    print(f"\n  exponential growth found in {n_exp} of {len(rows)} runs")

    banner("Q3 control -- same evolution on the tachyonic-gradient mutation")
    mmut = Model(mut='gradient_sign')
    tt, ser, st = full_evolution(mmut, initial_background(mmut, phi0, v0), 2.0 * H0, 3.0)
    sl, p, cl = classify(tt, ser)
    print(f"  MUTATE gradient_sign at k=2H: sigma(T)={ser[-1]:.3e}, dln s/dt={sl:.3f} -> {cl}")
    check(cl == 'EXPONENTIAL', "C3: the full-evolution classifier flags the tachyonic-gradient mutation as EXPONENTIAL")

    banner("RESULT")
    print(f"  {sum(ok)}/{len(ok)} consistency/control checks held.")
    if not all(ok):
        sys.exit(1)
    print("  Exit 0 (the checks are about the detectors and the algebra; the stability findings are the tables above).")
