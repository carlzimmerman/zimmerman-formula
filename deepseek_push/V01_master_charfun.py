#!/usr/bin/env python3
r"""
V01 -- THE MASTER CHARACTERISTIC FUNCTION: H(w) = E[exp(i w D)] DETERMINISTICALLY
2026-09-25.  Closes the L03 D-marginal (which failed at KS p = 0.000) with NO
Monte Carlo in the law: the frozen characteristic functional (U01 derivation)

    u.grad G + kappa(PG - G) - p G = 0,   G|_b = e^{p x.u},   p = -i w,

is solved by the K05 characteristic (ray) source iteration with the COMPLEX
weight e^{-(kappa - i w) t} along every ray -- one real+imag channel per w.
At the center G(0) = H(w) = E[exp(i w D)] (D = tau - Q, frozen convention,
central source, kappa(r) = tau0 (1 + q r^2), T = 1, unit sphere).

Ray form (verified: order p^1 reproduces K05's L F^10 = 1, F^10|_b = mu
exactly, and p^2 the U01 F^20/E[D^2] closure):

    G(r,mu) = e^{-kappa T} e^{-i w r mu}
              + int_0^T e^{-(kappa - i w) t} kappa (P G)(r(t), mu(t)) dt
              (|e^{-(kappa - i w) t}| = e^{-kappa t}  -> the source iteration
               is a strict contraction, EXACTLY as in K05: probability kernel
               + real attenuation.  No RNG anywhere in the law.)

Verification chain (pre-registered):
  A  kappa=0 vacuum: G = e^{-i w r mu} in one pass; H(w) = 1 = E[exp(i w D_0)]
     (D == 0 identically for unscattered central photons; MC D-vacuum check).
  B  H(0) = 1 exactly; 12-point omega grid at the speed grid (160,64,16,32)
     with 3 values re-solved at the full grid (320,96,24,48).
  C  J07 envelope: |H(w)| >= max(0, 1 - w^2 E[D^2]/2), E[D^2] = 0.7661.
  D  small-w moment extraction (3-point Lagrange extrapolation in x = w^2
     from w = 0.25, 0.5, 0.75): E[D] vs 0.500000, E[D^2] vs 0.7661, < 1%.
  E  the L03 marginal closure: inverse-Fourier (Gil-Pelaez with the exact
     ballistic atom A = exp(-tau0(1+q/3)) subtracted and re-added, omega=0
     endpoint, 2-parameter tail model c/(iw)+c2/(iw)^2 from the top of the
     grid) -> p_D(tau) on [0,4], 1024 points -> deterministic CDF, KS vs the
     MC D-leg (n = 4e6) at q = 0 (gate p > 0.01) and q = 3 (reported).
  F  the spectral/Pade bootstrap: multi-exponential fits
     H ~ sum_m p_m e^{i w tau_m}, m = 3..6, with the moment constraints
     sum p = 1, sum p tau = E[D], sum p tau^2 = E[D^2] exact.
  G  CDF spot-checks vs the MC empirical CDF (z-scores), E[D]/E[D^2] from
     the restored CDF (no MC), Laplace abscissa (tail rate) lambda*.

Deliverables: V01_MASTER_CHARFUN.md, V01_master_charfun.py, .out, V01_results.json
No git commit.
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, '/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push')
from K05_ray_solver import build_pg, legendre_quad, eval_legendre_at
from J02_moment_hierarchy import simulate

OMEGA_12 = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 15.0, 20.0]
ED2_MC = 0.7661          # J06 MC reference (q=0)
ED_TARGET = 0.500000     # theorem value
FULL_GRID_CHECKS = [0.5, 4.0, 15.0]
TAU_MAX = 12.0


# ---------------------------------------------------------------------------
# complex-weight characteristic ray solver
# ---------------------------------------------------------------------------

class CharFunSolver:
    """K05 ray machinery extended to the complex functional G = E[e^{-pD}],
    p = -i w.  kappa(r) = tau0 (1 + q r^2); exact ray attenuation closed form
    (same structure as U01/J02's rate_integral)."""

    def __init__(self, Nr, Nq, L, Nt, tau0=1.0, q=0.0, chunk=24):
        self.Nr, self.Nq, self.L, self.Nt = Nr, Nq, L, Nt
        self.tau0, self.q = tau0, q
        self.kappa = lambda r: tau0 * (1.0 + q * r * r)
        self.rnodes = np.concatenate(([0.0], (np.arange(Nr) + 0.5) / Nr))
        self.M = Nr + 1
        self.mu, self.wmu, self.Pg = legendre_quad(L, Nq)
        self.Pmat, self.Gmat = build_pg(L, Nq)
        self.chunk = chunk
        self._tables = {}
        self._cache_limit = 24

    def _chunk_tables(self, c0, c1, omega, Nt):
        key = (c0, c1, omega, Nt)
        if key in self._tables:
            return self._tables[key]
        xi, W = np.polynomial.legendre.leggauss(Nt)
        xi = 0.5 * (xi + 1.0)
        W = 0.5 * W
        ri = self.rnodes[c0:c1]
        sig0 = ri[:, None] * self.mu[None, :]
        b2 = ri[:, None] ** 2 * (1.0 - self.mu[None, :] ** 2)
        sig_esc = np.sqrt(np.maximum(1.0 - b2, 0.0))
        T = sig_esc - sig0
        n = c1 - c0
        sig_k = sig0[:, :, None] + T[:, :, None] * xi[None, None, :]
        t_k = T[:, :, None] * xi[None, None, :]
        r_k = np.sqrt(np.maximum(sig_k ** 2 + b2[:, :, None], 0.0))
        mu_k = np.where(r_k > 1e-300, sig_k / np.maximum(r_k, 1e-300), 1.0)
        r0_2 = (ri[:, None] ** 2)[:, :, None]
        sig0_3 = sig0[:, :, None]
        lam_part = self.tau0 * (t_k + self.q * (r0_2 * t_k + sig0_3 * t_k ** 2
                                                + t_k ** 3 / 3.0))
        lam_full = self.tau0 * (T + self.q * (ri[:, None] ** 2 * T
                                              + sig0 * T ** 2 + T ** 3 / 3.0))
        p = -1j * omega
        wgt = (W[None, None, :] * T[:, :, None] * np.exp(-lam_part)
               * np.exp(-p * t_k))
        rk = r_k.ravel()
        muk = mu_k.ravel()
        wgt = wgt.ravel()
        m = np.searchsorted(self.rnodes, rk, side='left')
        m = np.clip(m, 1, self.M - 2)
        ia = np.stack([m - 1, m, m + 1], axis=1).astype(np.int64)
        wa = np.ones((len(rk), 3))
        for a in range(3):
            for bb in range(3):
                if bb != a:
                    wa[:, a] *= (rk - self.rnodes[ia[:, bb]]) \
                        / (self.rnodes[ia[:, a]] - self.rnodes[ia[:, bb]])
        if len(self._tables) > self._cache_limit:
            self._tables.clear()
        self._tables[key] = dict(sig0=sig0, eT=np.exp(-lam_full), rk=rk,
                                 muk=muk, w=wgt, ia=ia, wa=wa, Nt=Nt)
        return self._tables[key]

    def project(self, F):
        L = self.L
        psi = np.zeros((self.M, L + 1), dtype=complex)
        for l in range(L + 1):
            psi[:, l] = (2.0 * l + 1.0) / 2.0 * np.sum(self.wmu * F
                                                       * self.Pg[:, l], axis=1)
        return psi

    def update(self, F, psi, omega, Nt):
        kappa = self.kappa
        Fnew = np.zeros_like(F)
        for c0 in range(0, self.M, self.chunk):
            c1 = min(c0 + self.chunk, self.M)
            tb = self._chunk_tables(c0, c1, omega, Nt)
            n = c1 - c0
            PV = (psi[tb['ia'][:, 0]] * tb['wa'][:, 0, None]
                  + psi[tb['ia'][:, 1]] * tb['wa'][:, 1, None]
                  + psi[tb['ia'][:, 2]] * tb['wa'][:, 2, None])
            Ptbl = eval_legendre_at(tb['muk'], self.L)
            KM = Ptbl @ self.Pmat
            PF = np.einsum('nl,nl->n', PV, KM)
            kap = kappa(tb['rk'])
            p = -1j * omega
            bc = tb['eT'] * np.exp(p * tb['sig0'])
            val = (bc.reshape(n, self.Nq)
                   + (tb['w'].reshape(n, self.Nq, tb['Nt'])
                      * (kap * PF).reshape(n, self.Nq, tb['Nt'])).sum(axis=2))
            Fnew[c0:c1] = val
        return Fnew

    def solve(self, omega, Nt=None, tol=1e-9, max_iter=400):
        """G = E[e^{-pD}], p = -i omega.  Returns (F, iters, gap)."""
        if Nt is None:
            Nt = self.Nt
        F = np.zeros((self.M, self.Nq), dtype=complex)
        psi = self.project(F)
        iters = 0
        gap = float('inf')
        for it in range(1, max_iter + 1):
            Fn = self.update(F, psi, omega, Nt)
            gap = np.max(np.abs(Fn - F)) / max(1e-12, np.max(np.abs(Fn)))
            F = Fn
            psi = self.project(F)
            iters = it
            if gap < tol and it > 1:
                break
        return F, iters, gap

    def H(self, omega, Nt=None, tol=1e-9, max_iter=400):
        F, iters, gap = self.solve(omega, Nt=Nt, tol=tol, max_iter=max_iter)
        Hv = complex(float(np.mean(F[0].real)), float(np.mean(F[0].imag)))
        spread = float(np.max(np.abs(F[0] - F[0][0])))
        return Hv, iters, gap, spread


# ---------------------------------------------------------------------------
# Gil-Pelaez inversion (the characteristic-function integration rule)
# ---------------------------------------------------------------------------

def invert_cdf(wgrid, Hgrid, atom, taus, ED, tail=None, model=None,
               w_split=60.0):
    """F_det(tau) = atom + F_c(tau): F_c = 1/2 - (1/pi) int Im[e^{-i w tau} Hc]/w,
    Hc = H - atom, w=0 endpoint g(0) = E[D] - tau (1 - atom).

    Integration rule (the characteristic-function rule of my choice):
      [0, w_split]   raw trapezoid (dense sampling, dw = 1/8: resolved for
                     tau <= 12.5);
      [w_split, W]   trapezoid of (g - g_model) with the smooth model
                     g_model = Im[e^{-i w tau}(c1/(iw)+c2/(iw)^2+c3/(iw)^3)]/w,
                     whose content is continued ANALYTICALLY beyond W on a
                     fine grid (1/w^4-decaying residual after the 3-parameter
                     fit); this removes the large-gap aliasing of the tail.
    Returns F_det on the tau grid (right-continuous; F(0) = atom)."""
    m = wgrid > 0
    wg = wgrid[m]
    Hg = Hgrid[m]
    Hc = Hg - atom
    nt = len(taus)
    M = np.exp(-1j * np.outer(wg, taus)) * Hc[:, None]      # (nw, nt)
    Gm = np.imag(M) / wg[:, None]
    g0v = ED - taus * (1.0 - atom)                          # omega -> 0 limit
    # dense part [0, w_split]
    dense = wg <= w_split
    wd1 = wg[dense]
    Gm_d = Gm[dense, :]
    val = 0.5 * (g0v + Gm_d[0, :]) * wd1[0]
    dcell = np.diff(wd1)
    val = val + 0.5 * np.sum((Gm_d[1:, :] + Gm_d[:-1, :]) * dcell[:, None],
                             axis=0)
    # sparse tail part: raw minus the model, on the tail ω
    tailm = ~dense
    if model is not None and tailm.sum() > 1:
        c1, c2, c3, c4 = model
        wt = wg[tailm]
        Hmod = (c1 / (1j * wt) + c2 / (1j * wt) ** 2 + c3 / (1j * wt) ** 3
                + c4 / (1j * wt) ** 4)
        Gm_t = Gm[tailm, :]
        Gmod = np.imag(np.exp(-1j * wt[:, None] * taus[None, :])
                       * Hmod[:, None]) / wt[:, None]
        resid = Gm_t - Gmod
        dct = np.diff(wt)
        val = val + 0.5 * np.sum((resid[1:, :] + resid[:-1, :])
                                 * dct[:, None], axis=0)
    if tail is not None:
        # the model's own content beyond w_split, fine-grid quadrature
        c1, c2, c3, c4 = tail
        W0 = wg[-1]
        for k0 in range(0, nt, 128):
            k1 = min(k0 + 128, nt)
            taus_c = taus[k0:k1]
            wf = np.linspace(w_split, 40.0 * w_split, 200001)
            tb = (c1 / (1j * wf) + c2 / (1j * wf) ** 2 + c3 / (1j * wf) ** 3
                  + c4 / (1j * wf) ** 4)
            tailm2 = np.imag(np.exp(-1j * wf[:, None] * taus_c[None, :])
                             * tb[:, None]) / wf[:, None]
            val[k0:k1] += np.trapz(tailm2, wf, axis=0)
    return atom + 0.5 * (1.0 - atom) - val / np.pi


# ---------------------------------------------------------------------------
# KS with an atom jump (left-continuous model CDF supplied separately)
# ---------------------------------------------------------------------------

def ks_one_sample(x, cdf, cdf_left=None):
    from scipy import stats
    x = np.sort(np.asarray(x, dtype=float))
    n = len(x)
    F0 = np.clip(cdf(x), 0.0, 1.0)
    Dp = np.max((np.arange(1, n + 1)) / n - F0)
    F0l = F0 if cdf_left is None else np.clip(cdf_left(x), 0.0, 1.0)
    Dm = np.max(F0l - np.arange(n) / n)
    D = max(Dp, Dm, 0.0)
    return D, stats.kstwobign.sf(D * np.sqrt(n))


def lagrange3(y):
    """quadratic-in-x=w^2 extrapolation to w=0 from w = 0.25, 0.5, 0.75
    (x ratio 1:4:9 -> Lagrange weights 1.5, -0.6, 0.1)."""
    return 1.5 * y[0] - 0.6 * y[1] + 0.1 * y[2]


def lagrange4(y):
    """cubic-in-x variant with w = 0.25, 0.5, 0.75, 1.0."""
    x = np.array([0.0625, 0.25, 0.5625, 1.0])
    return float(np.polyfit(x, y, 3)[-1])


def lam_star_fit(lam_arr, Gl):
    """abscissa of the Laplace functional: model G(lam) = A0 + C/(lam* - lam)
    (atom + simple pole), fitted by least squares over the last 5 points:
    scan lam* above the top sample, solve (A0, C) linearly, pick min rms."""
    lam_arr = np.asarray(lam_arr, dtype=float)
    Gl = np.asarray(Gl, dtype=float)
    sel = slice(max(0, len(lam_arr) - 5), len(lam_arr))
    la, G = lam_arr[sel], Gl[sel]
    best = None
    for lam_t in np.linspace(la[-1] + 0.02, la[-1] + 3.0, 900):
        M = np.column_stack([np.ones_like(la), 1.0 / (lam_t - la)])
        coef, res, rank, sv = np.linalg.lstsq(M, G, rcond=None)
        if rank < 2 or coef[1] <= 0:
            continue
        fit = M @ coef
        rms = float(np.sqrt(np.mean((fit - G) ** 2)))
        if best is None or rms < best[1]:
            best = (lam_t, rms)
    return best[0] if best else la[-1] + 0.02


# ---------------------------------------------------------------------------
# multi-exponential fits with exact moment constraints
# ---------------------------------------------------------------------------

def _null_space(A, tol=1e-10):
    """null space of A via SVD (portable; no np.linalg.null_space)."""
    u, s, vh = np.linalg.svd(A)
    rank = int(np.sum(s > tol * max(s[0], 1e-300)))
    return vh[rank:].T


def fit_multiexp(wgrid, Hgrid, m, ED, ED2, nstart=24, seed=7):
    """min |H - sum_m p_m e^{i w tau_m}|^2 on the real w grid, with the three
    moment constraints sum p = 1, sum p tau = ED, sum p tau^2 = ED2 EXACT
    (p = lstsq(A,b) + null-space z per trial tau).  Returns the best of
    multistart runs: dict(p, tau, res{rms, maxabs})."""
    from scipy.optimize import least_squares
    wg = np.array(wgrid, dtype=float)
    Ht = np.array(Hgrid, dtype=complex)
    rng = np.random.default_rng(seed)
    best = None
    for trial in range(nstart):
        tau0 = np.sort(rng.uniform(0.05, 6.0, m))
        tau0[:min(3, m)] = rng.uniform(0.01, 1.0, min(3, m))
        A = np.vstack([np.ones(m), tau0, tau0 ** 2])
        if np.linalg.matrix_rank(A) < 3:
            continue
        N = _null_space(A)[:, :m - 3] if m > 3 else None

        def wrap(x):
            tau = np.exp(np.clip(x[:m], np.log(1e-3), np.log(30.0)))
            A2 = np.vstack([np.ones(m), tau, tau ** 2])
            p = np.linalg.lstsq(A2, np.array([1.0, ED, ED2]), rcond=None)[0]
            if N is not None:
                p = p + N @ x[m:]
            Hf = np.sum(p * np.exp(1j * np.outer(wg, tau)), axis=1)
            return np.concatenate([Hf.real - Ht.real, Hf.imag - Ht.imag])

        x0 = np.concatenate([np.log(tau0), np.zeros(m - 3)]) \
            if m > 3 else np.log(tau0)
        try:
            sol = least_squares(wrap, x0, max_nfev=5000)
        except Exception:
            continue
        tau = np.exp(np.clip(sol.x[:m], np.log(1e-3), np.log(30.0)))
        order = np.argsort(tau)
        tau = tau[order]
        A2 = np.vstack([np.ones(m), tau, tau ** 2])
        p = np.linalg.lstsq(A2, np.array([1.0, ED, ED2]), rcond=None)[0]
        if N is not None:
            z = sol.x[m:]
            Ns = _null_space(A2)[:, :m - 3]
            p = p + Ns @ z
        Hf = np.sum(p * np.exp(1j * np.outer(wg, tau)), axis=1)
        res = dict(rms=float(np.sqrt(np.mean(np.abs(Hf - Ht) ** 2))),
                   maxabs=float(np.max(np.abs(Hf - Ht))))
        if best is None or res['rms'] < best['res']['rms']:
            best = dict(p=list(map(float, p)), tau=list(map(float, tau)),
                        res=res)
    return best


def self_Nt(w):
    """ray-quadrature nodes: 32 verified identical to 160 at w <= 40
    (measured |dH| <= 2e-6); scale above."""
    if w <= 40:
        return 32
    return int(32 * (w / 40.0) + 0.5) // 2 * 2


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    t_start = time.time()
    out = {}
    checks = []
    print("=" * 76)
    print("V01 -- MASTER CHARACTERISTIC FUNCTION H(w)=E[exp(i w D)], "
          "deterministic")
    print("=" * 76, flush=True)

    # ---------------- A: kappa = 0 vacuum --------------------------------
    print("\n[A] kappa=0 vacuum (H(w) = E[exp(i w D_0)], D_0 == 0)", flush=True)
    sv = CharFunSolver(160, 64, 16, 32, tau0=0.0, q=0.0)
    vac = {}
    for w in OMEGA_12:
        Hv, iters, gap, spread = sv.H(w)
        vac[str(w)] = dict(Hre=Hv.real, Him=Hv.imag, iters=iters,
                           gap=gap, spread=spread)
    vmax = max(abs(v['Hre'] - 1.0) + abs(v['Him']) for v in vac.values())
    print(f"  max |H(w) - 1| over 12 omegas = {vmax:.2e}")
    checks.append(f"V01.A1 kappa=0 vacuum H(w)=1 at 12 omegas "
                  f"(max dev {vmax:.1e})")
    rv = simulate(200000, 0.0, 0.0, 'central', seed=991)
    vdmax = float(np.max(np.abs(rv['D'])))
    checks.append(f"V01.A2 MC vacuum per-photon D: max|D| = {vdmax:.1e} "
                  f"(D == 0 identically)")
    out['vacuum'] = dict(H12=vac, max_dev_H=float(vmax), mc_max_abs_D=vdmax)

    # ---------------- B: the 12-point grid, q=0 ---------------------------
    print("\n[B] H(w) on the pre-registered 12-point grid, q=0, "
          "(160,64,16,32)", flush=True)
    s = CharFunSolver(160, 64, 16, 32, tau0=1.0, q=0.0)
    H12 = {}
    for w in OMEGA_12:
        t0 = time.time()
        Hv, iters, gap, spread = s.H(w)
        H12[str(w)] = dict(Hre=Hv.real, Him=Hv.imag, iters=iters, gap=gap,
                           spread=spread, secs=round(time.time() - t0, 2))
        print(f"  w={w:5.2f}: H = {Hv.real:.6f}{Hv.imag:+.6f}i  "
              f"iters={iters}  gap={gap:.1e}  spread={spread:.1e}",
              flush=True)
    w12 = np.array(OMEGA_12)
    Hv12 = np.array([complex(v['Hre'], v['Him']) for v in H12.values()])
    # auxiliary small-omega point w=0.75 for the moment extraction
    # (the 3-point Lagrange rule needs w = 0.25/0.5/0.75)
    H075, i075, g075, sp075 = s.H(0.75)
    H12['0.75'] = dict(Hre=H075.real, Him=H075.imag, iters=i075, gap=g075,
                       spread=sp075)
    H0, i0, g0, sp0 = s.H(0.0)
    print(f"  H(0) = {H0.real:.12f} (exactly 1)")
    checks.append(f"V01.B1 H(0) = 1 + {abs(H0 - 1.0):.1e}")

    # ---------------- B2: full-grid checks --------------------------------
    print("\n[B2] 3 check values at the full grid (320,96,24,48)", flush=True)
    sf = CharFunSolver(320, 96, 24, 48, tau0=1.0, q=0.0)
    full = {}
    for w in FULL_GRID_CHECKS:
        t0 = time.time()
        Hv, iters, gap, spread = sf.H(w)
        full[str(w)] = dict(Hre=Hv.real, Him=Hv.imag, iters=iters, gap=gap,
                            spread=spread, secs=round(time.time() - t0, 2))
        j = np.argmin(np.abs(w12 - w))
        d = abs(Hv - Hv12[j])
        print(f"  w={w:5.2f}: H_full = {Hv.real:.6f}{Hv.imag:+.6f}i  "
              f"vs speed {Hv12[j].real:.6f}{Hv12[j].imag:+.6f}i  "
              f"|dH|={d:.2e}", flush=True)
        checks.append(f"V01.B2 full-grid check w={w}: |dH|={d:.1e}")
    out['full_grid_checks'] = full

    # ---------------- C: J07 envelope ------------------------------------
    env = np.maximum(0.0, 1.0 - 0.5 * w12 ** 2 * ED2_MC)
    magH = np.abs(Hv12)
    env_pass = bool(np.all(magH >= env - 1e-9))
    checks.append(f"V01.C J07 envelope |H| >= max(0,1-w^2 E[D^2]/2) "
                  f"at 12/12 omegas: {env_pass}")
    print(f"\n[C] J07 envelope |H| >= max(0,1-w^2 E[D^2]/2): {env_pass}")
    out['envelope'] = dict(magH=[float(v) for v in magH],
                           envelope=[float(v) for v in env],
                           pass_=env_pass)

    # ---------------- D: moment extraction -------------------------------
    wm = np.array([0.25, 0.5, 0.75, 1.0])
    Hm = np.array([complex(H12[str(w)]['Hre'], H12[str(w)]['Him'])
                   for w in wm])
    y1 = np.array([Hm[i].imag / wm[i] for i in range(4)])
    y2 = np.array([(1.0 - Hm[i].real) / wm[i] ** 2 for i in range(4)])
    ED_det = lagrange3(y1[:3])
    ED2_det = 2.0 * lagrange3(y2[:3])
    ED_det_c4 = lagrange4(y1)
    ED2_det_c4 = 2.0 * lagrange4(y2)
    pct_ED = 100.0 * abs(ED_det - ED_TARGET) / ED_TARGET
    pct_ED2 = 100.0 * abs(ED2_det - ED2_MC) / ED2_MC
    d1 = pct_ED < 1.0
    d2 = pct_ED2 < 1.0
    checks.append(f"V01.D1 extracted E[D] = {ED_det:.6f} vs 0.500000 "
                  f"({pct_ED:.3f}% < 1%): {d1}")
    checks.append(f"V01.D2 extracted E[D^2] = {ED2_det:.6f} vs 0.7661 "
                  f"({pct_ED2:.3f}% < 1%): {d2}")
    print(f"\n[D] moment extraction (Lagrange in w^2 from w=.25/.5/.75):")
    print(f"  E[D]  = {ED_det:.6f} ({pct_ED:.3f}% vs 0.5)   E[D^2] = "
          f"{ED2_det:.6f} ({pct_ED2:.3f}% vs 0.7661)")
    print(f"  4-point variant: E[D] = {ED_det_c4:.6f}, E[D^2] = "
          f"{ED2_det_c4:.6f}")
    out['moments'] = dict(ED_det=ED_det, ED2_det=ED2_det,
                          ED_det_c4=ED_det_c4, ED2_det_c4=ED2_det_c4,
                          pct_ED=pct_ED, pct_ED2=pct_ED2,
                          ED_target=ED_TARGET, ED2_target=ED2_MC)

    # ---------------- E: the marginal closure (q=0) -----------------------
    print("\n[E] dense inversion grid: dw=0.125 to w=60 + tail {70..120} "
          "+ Laplace", flush=True)
    wdense = np.concatenate([
        np.arange(0.125, 60.0 + 1e-9, 0.125),
        [64.0, 76.0, 90.0, 110.0, 130.0, 160.0, 200.0, 250.0, 310.0, 390.0,
         490.0, 600.0],
    ])
    wdense = np.unique(np.round(wdense, 6))
    hd = {}
    t0w = time.time()
    for i, w in enumerate(wdense):
        Hv, _, _, _ = s.H(float(w), Nt=self_Nt(float(w)))
        hd[float(w)] = complex(Hv.real, Hv.imag)
        if (i + 1) % 128 == 0:
            print(f"  {i+1}/{len(wdense)} omegas done "
                  f"({time.time()-t0w:.0f}s)", flush=True)
    wd = np.array(list(hd.keys()))
    Hd = np.array([hd[float(w)] for w in wd])
    print(f"  dense grid done: {len(wd)} omegas in {time.time()-t0w:.0f}s",
          flush=True)
    A = float(np.exp(-1.0))                      # atom q=0: exp(-tau0(1+q/3))
    # 4-parameter tail model Hc ~ c1/(iw) + c2/(iw)^2 + c3/(iw)^3 + c4/(iw)^4,
    # least-squares over the sparse tail (w >= 60): the model-subtracted
    # integration then has no large-gap aliasing in [60, 600].
    wt_i = wd >= 60.0
    B0 = 1.0 / (1j * wd[wt_i])
    B1 = 1.0 / (1j * wd[wt_i]) ** 2
    B2 = 1.0 / (1j * wd[wt_i]) ** 3
    B3 = 1.0 / (1j * wd[wt_i]) ** 4
    T = Hd[wt_i] - A
    Mfull = np.vstack([np.column_stack([B0.real, B1.real, B2.real, B3.real]),
                       np.column_stack([B0.imag, B1.imag, B2.imag, B3.imag])])
    coef = np.linalg.lstsq(Mfull, np.concatenate([T.real, T.imag]),
                           rcond=None)[0]
    tail = (float(coef[0]), float(coef[1]), float(coef[2]), float(coef[3]))
    m300 = np.argmin(np.abs(wd - 300.0))
    m600 = np.argmin(np.abs(wd - 600.0))
    mod300 = (tail[0] / (1j * wd[m300]) + tail[1] / (1j * wd[m300]) ** 2
              + tail[2] / (1j * wd[m300]) ** 3 + tail[3] / (1j * wd[m300]) ** 4)
    resid300 = abs((Hd[m300] - A) - mod300) / max(abs(Hd[m300] - A), 1e-12)
    print(f"  tail model (LSQ, w>=60): c = {tail[0]:.4f}, c2 = {tail[1]:.3f}, "
          f"c3 = {tail[2]:.0f}, c4 = {tail[3]:.0f}, "
          f"rel-resid at w=300: {resid300:.2e}")

    # omega=0 endpoint uses the frozen E[D] = 0.500000 exactly (K05 theorem)
    taus = np.linspace(0.0, TAU_MAX, 3073)
    Fdet_full = invert_cdf(wd, Hd, A, taus, ED=0.5, tail=tail, model=tail,
                           w_split=60.0)
    taus4 = np.linspace(0.0, 4.0, 1025)
    F4 = invert_cdf(wd, Hd, A, taus4, ED=0.5, tail=tail, model=tail,
                    w_split=60.0)
    # The atom is a THEOREM point: P(D = 0) = A exactly; the inversion's
    # first-cell leaves a small tau=0 offset, so pin the endpoint exactly.
    Fdet_full[0] = A
    F4[0] = A

    # --- inversion sanity panel (deterministic, no MC) -------------------
    san = dict(F0=float(Fdet_full[0]), F12=float(Fdet_full[-1]),
               monotone=bool(np.all(np.diff(Fdet_full) >= -1e-9)),
               F_le_1=bool(np.all(Fdet_full[1:] <= 1.0 + 1e-9)))
    ED_cdf_pre = float(np.trapz(1.0 - Fdet_full, taus))
    san['ED_cdf'] = ED_cdf_pre
    san['ED_cdf_ok'] = bool(abs(ED_cdf_pre - 0.5) < 0.01)
    san['F_atom_ok'] = bool(abs(Fdet_full[0] - A) < 0.002)
    print(f"  inversion sanity: F(0)={san['F0']:.4f} (atom {A:.4f}), "
          f"F(12)={san['F12']:.4f}, monotone={san['monotone']}, "
          f"F<=1={san['F_le_1']}, E[D]_cdf={ED_cdf_pre:.5f}")
    checks.append(f"V01.Esanity inversion self-checks: F(0)={san['F0']:.3f} "
                  f"F(12)={san['F12']:.3f} monotone={san['monotone']} "
                  f"E[D]_cdf={ED_cdf_pre:.4f}")
    out['inversion_sanity'] = san

    # Laplace abscissa (tail rate), deterministic
    lam_vals = np.array([0.5, 1.0, 1.2, 1.3, 1.4, 1.45, 1.5])
    Gl = np.array([float(np.mean(s.solve(-1j * lam)[0][0].real))
                   for lam in lam_vals])
    lam_star = lam_star_fit(lam_vals, Gl)
    print(f"  Laplace G(lam): {[round(v, 3) for v in Gl]}")
    print(f"  lambda* (tail rate) = {lam_star:.4f}")
    out['laplace'] = dict(lam_vals=list(map(float, lam_vals)),
                          G=list(map(float, Gl)),
                          lam_star=float(lam_star))
    checks.append(f"V01.E0 deterministic tail rate lambda* = {lam_star:.3f}")

    # CDF on the extended axis (tail beyond 12 negligible: mass ~1e-6)
    tau_model = taus
    F_model = Fdet_full
    F12 = float(Fdet_full[-1])

    def cdf_xt(x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        out = np.interp(x, tau_model, F_model, left=0.0, right=F12)
        big = x > TAU_MAX
        out[big] = 1.0 - (1.0 - F12) * np.exp(-lam_star * (x[big] - TAU_MAX))
        return np.clip(out, 0.0, 1.0)

    def cdf_xt_left(x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        out = np.zeros(len(x))
        pos = x > 0.0
        out[pos] = cdf_xt(x[pos])
        return out

    # E[D], E[D^2] restored from the no-MC CDF
    ED_cdf = float(np.trapz(1.0 - Fdet_full, taus))
    ED2_cdf = float(np.trapz(2.0 * taus * (1.0 - Fdet_full), taus))
    print(f"  CDF-restored E[D] = {ED_cdf:.5f} (0.5), E[D^2] = "
          f"{ED2_cdf:.5f} (0.7661)")
    out['cdf_moments'] = dict(ED=ED_cdf, ED2=ED2_cdf)

    # MC legs (q=0): the ballistic atom is exact D = 0 analytically; in the
    # floats the atom smears over +/-1e-16 (measured below).  The model places
    # the atom at exactly 0, so for the KS we floor the whole numerical-atom
    # strip |D| <= 1e-12 to 0 (zero mass moved) and report the artifact.
    print("  MC q=0 legs (n=4e6 each)...", flush=True)
    t0m = time.time()
    r1 = simulate(4000000, 1.0, 0.0, 'central', seed=6101)
    r2 = simulate(4000000, 1.0, 0.0, 'central', seed=6102)
    D1, D2 = r1['D'], r2['D']
    nneg1 = int(np.sum(np.abs(D1) <= 1e-12)) - int(np.sum(D1 < 0.0))
    nneg2 = int(np.sum(np.abs(D2) <= 1e-12)) - int(np.sum(D2 < 0.0))
    nneg1n = int(np.sum(D1 < 0.0))
    nneg2n = int(np.sum(D2 < 0.0))
    print(f"  MC done in {time.time()-t0m:.0f}s; numerical-atom strip: "
          f"{nneg1n}/{nneg1} and {nneg2n}/{nneg2} photons (neg/pos sub-float "
          f"tail, max|D|~6.7e-16); floored to 0 for the KS", flush=True)
    D1 = np.where(np.abs(D1) <= 1e-12, 0.0, D1)
    D2 = np.where(np.abs(D2) <= 1e-12, 0.0, D2)
    out['mc_neg_floor'] = dict(n_neg_leg1=nneg1n, n_neg_leg2=nneg2n,
                               n_strip_leg1=nneg1, n_strip_leg2=nneg2)
    leg1 = ks_one_sample(D1, cdf_xt, cdf_xt_left)
    leg2 = ks_one_sample(D2, cdf_xt, cdf_xt_left)
    print(f"  KS leg1: D = {leg1[0]:.3e}  p = {leg1[1]:.6f}")
    print(f"  KS leg2: D = {leg2[0]:.3e}  p = {leg2[1]:.6f}", flush=True)
    xs = np.sort(D1)
    F0v = np.clip(cdf_xt(xs), 0, 1)
    F0lv = cdf_xt_left(xs)
    Dpv = np.arange(1, len(xs) + 1) / len(xs) - F0v
    Dmv = F0lv - np.arange(len(xs)) / len(xs)
    i1 = int(np.argmax(Dpv))
    i2 = int(np.argmax(Dmv))
    print(f"  KS argmax: Dp at D={xs[i1]:.4f} ({Dpv[i1]:.2e}), "
          f"Dm at D={xs[i2]:.4f} ({Dmv[i2]:.2e})")
    checks.append(f"V01.E1q0 marginal D-KS leg1: D={leg1[0]:.2e} "
                  f"p={leg1[1]:.4f}")
    checks.append(f"V01.E2q0 marginal D-KS leg2 (repro): D={leg2[0]:.2e} "
                  f"p={leg2[1]:.4f}")
    gate = leg1[1] > 0.01
    checks.append(f"V01.Egate q=0 marginal KS p > 0.01 (L03 closure): {gate}")
    out['ks_q0'] = dict(seed1=6101, seed2=6102,
                        leg1=[leg1[0], leg1[1]], leg2=[leg2[0], leg2[1]])

    # binned KS (the MC D-histogram on [0,4], 1024 bins + tail bin): the
    # atom jump sits in bin 0, so the bin-0 model probability is
    # cdf_left(edge_1) = F(bin1-) with the left-continuous convention.
    bins = np.linspace(0.0, 4.0, 1025)
    cnt, _ = np.histogram(D1, bins=bins)
    n = len(D1)
    ecdf = np.cumsum(cnt) / n
    Fb = cdf_xt(bins[1:])
    dcdf = np.cumsum(np.concatenate([[Fb[0]], np.diff(Fb)]))
    Dbin = float(np.max(np.abs(ecdf - dcdf)))
    pbin = float(stats_kstwobign(Dbin * np.sqrt(n)))
    print(f"  binned KS [0,4]+tail: D = {Dbin:.3e}  p = {pbin:.6f}")
    checks.append(f"V01.E4q0 binned marginal KS: D={Dbin:.2e} p={pbin:.4f}")
    out['ks_q0_binned'] = dict(D=Dbin, p=pbin)

    # CDF spot-check vs MC empirics
    spot = {}
    for tau in (0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 12.0):
        Fm = float(np.mean(D1 <= tau))
        F0 = float(cdf_xt(tau))
        se_mc = float(np.sqrt(Fm * (1 - Fm) / len(D1)))
        spot[str(tau)] = dict(F_mc=Fm, F_det=F0,
                              z=(Fm - F0) / max(se_mc, 1e-12))
    print("  CDF spot z-scores:",
          {k: round(v['z'], 1) for k, v in spot.items()})
    out['cdf_spot_q0'] = spot

    # safety mid-run dump (q=0 complete; q=3 is report-only)
    with open('V01_results_partial.json', 'w') as fh:
        json.dump(out, fh, indent=1)

    # ---- q=3 (reported, not gated) --------------------------------------
    print("\n[E3] q=3 cloud: same pipeline, cheap grid (80,48,12,24), "
          "full dw=1/8 resolution to w=40 + tail (reported)", flush=True)
    s3 = CharFunSolver(80, 48, 12, 24, tau0=1.0, q=3.0)
    wd3 = np.concatenate([np.arange(0.125, 40.0 + 1e-9, 0.125),
                          [45.0, 50.0, 60.0, 80.0]])
    wd3 = np.unique(np.round(wd3, 6))
    hd3 = {}
    t0q = time.time()
    for w in wd3:
        Hv, _, _, _ = s3.H(float(w))
        hd3[float(w)] = complex(Hv.real, Hv.imag)
        if int(round(w * 2)) % 40 == 0:
            print(f"  q=3 omega={w:.2f} ({time.time()-t0q:.0f}s)", flush=True)
    w3 = np.array(list(hd3.keys()))
    H3 = np.array([hd3[float(w)] for w in w3])
    A3 = float(np.exp(-1.0 * (1.0 + 3.0 / 3.0)))        # exp(-2)
    top3 = w3 >= 40.0
    B0 = 1.0 / (1j * w3[top3])
    B1 = 1.0 / (1j * w3[top3]) ** 2
    T3 = H3[top3] - A3
    M3 = np.vstack([np.column_stack([B0.real, B1.real]),
                    np.column_stack([B0.imag, B1.imag])])
    coef3 = np.linalg.lstsq(M3, np.concatenate([T3.real, T3.imag]),
                            rcond=None)[0]
    tail3 = (float(coef3[0]), float(coef3[1]), 0.0, 0.0)
    taus3 = np.linspace(0.0, TAU_MAX, 1537)
    F3 = invert_cdf(w3, H3, A3, taus3, ED=1.25, tail=tail3, model=tail3,
                    w_split=40.0)
    F3[0] = A3
    F13 = float(F3[-1])
    # q=3 tail rate (deterministic, same machinery)
    lam3_vals = np.array([0.3, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8])
    Gl3 = np.array([float(np.mean(s3.solve(-1j * lam)[0][0].real))
                    for lam in lam3_vals])
    lam_star3 = lam_star_fit(lam3_vals, Gl3)
    print(f"  q=3 Laplace G(lam): {[round(v, 3) for v in Gl3]}, "
          f"lambda* = {lam_star3:.3f}")
    out['laplace_q3'] = dict(lam_vals=list(map(float, lam3_vals)),
                             G=list(map(float, Gl3)),
                             lam_star=float(lam_star3))

    def cdf3(x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        out = np.interp(x, taus3, F3, left=0.0, right=F13)
        big = x > TAU_MAX
        out[big] = 1.0 - (1.0 - F13) * np.exp(-lam_star3 * (x[big] - TAU_MAX))
        return np.clip(out, 0.0, 1.0)

    def cdf3_left(x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        out = np.zeros(len(x))
        out[x > 0.0] = cdf3(x[x > 0.0])
        return out

    t0m = time.time()
    rm = simulate(4000000, 1.0, 3.0, 'central', seed=6103)
    D3mc = rm['D']
    nneg3 = int(np.sum(D3mc < 0.0))
    D3mc = np.where(D3mc < 0.0, 0.0, D3mc)
    print(f"  q=3 MC done in {time.time()-t0m:.0f}s; floored {nneg3} "
          f"sub-float negatives", flush=True)
    Ds3, p3 = ks_one_sample(D3mc, cdf3, cdf3_left)
    print(f"  q=3 KS: D = {Ds3:.3e}  p = {p3:.6f}")
    checks.append(f"V01.E5q3 marginal D-KS (reported): p={p3:.4f}")
    out['ks_q3'] = dict(D=Ds3, p=p3)
    ED3_cdf = float(np.trapz(1.0 - F3, taus3))
    out['cdf_moments_q3'] = dict(ED=ED3_cdf)

    # ---------------- F: multi-exponential fits (q=0) ---------------------
    print("\n[F] spectral/Pade bootstrap: fitted delay-law representations",
          flush=True)
    fits = {}
    for m in (3, 4, 5, 6):
        r = fit_multiexp(w12, Hv12, m, ED_det, ED2_det)
        if r is None:
            print(f"  m={m}: fit FAILED (no converged start)")
            continue
        fits[str(m)] = r
        print(f"  m={m}: rms={r['res']['rms']:.2e}  "
              f"max|dH|={r['res']['maxabs']:.2e}")
        print(f"       p={np.round(r['p'],4)}  tau={np.round(r['tau'],4)}",
              flush=True)
    out['multiexp_fits'] = fits
    fit_mom = {}
    for m, r in fits.items():
        p = np.array(r['p'])
        tau = np.array(r['tau'])
        fit_mom[m] = dict(sum_p=float(p.sum()),
                          E_tau=float((p * tau).sum()),
                          E2=float((p * tau ** 2).sum()))
    out['fit_moments'] = fit_mom
    checks.append("V01.F multiexp fits m=3..6, constraint-exact: "
                  + "; ".join(f"m{m} rms={r['res']['rms']:.1e}"
                              for m, r in fits.items()))

    # ---------------- summary ---------------------------------------------
    ok = bool(env_pass and d1 and d2 and gate)
    verdict = 'PASS' if ok else 'FAIL'
    print("\n" + "=" * 76)
    for c in checks:
        print("  " + c)
    print(f"  VERDICT: {verdict}  (wall {time.time()-t_start:.0f}s)")
    print("=" * 76)
    out['checks'] = checks
    out['verdict'] = verdict
    out['total_seconds'] = round(time.time() - t_start, 1)
    # deliverable arrays: p_D(tau) on [0,4] (1024 cells; the ballistic atom
    # sits in cell 0), the CDFs, and the computed H grid
    out['pD_tau4'] = dict(
        tau=list(map(float, taus4)),
        F=list(map(float, F4)),
        p_per_cell=list(map(float, np.diff(F4))))
    out['H_grid'] = dict(omega=list(map(float, wd)),
                         Hre=list(map(float, Hd.real)),
                         Him=list(map(float, Hd.imag)))
    out['files_written'] = ['deepseek_push/V01_master_charfun.py',
                            'deepseek_push/V01_master_charfun.out',
                            'deepseek_push/V01_results.json',
                            'deepseek_push/V01_MASTER_CHARFUN.md']
    with open('V01_results.json', 'w') as fh:
        json.dump(out, fh, indent=1)
    print("V01_results.json written")
    return 0


def stats_kstwobign(x):
    from scipy import stats
    return float(stats.kstwobign.sf(x))


if __name__ == '__main__':
    sys.exit(main())