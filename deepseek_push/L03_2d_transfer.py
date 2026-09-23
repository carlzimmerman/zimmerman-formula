#!/usr/bin/env python3
r"""L03 -- DETERMINISTIC 2D TRANSFER FUNCTION Psi(tau, v^2) + NOISE-RECOVERY.

2026-09-23.  The N4 observational door (synthetic).  Extends the K05 ray
solver to kappa(r) = t0(1+q r^2) and constructs the FULL 2D transfer
function deterministically on a 40x40 (tau, v^2) grid using the
conditional-Gaussian spine (J08/J09):

    V := v^2/(2 ang) | (D, ang) ~ chi2_1, independent of (D, ang)
    Psi(i, y) = p_i * E[ F_chi1(y/(2 ang)) | D in bin_i ]

with the within-bin ang law entering through a 16-point cross-bin quantile
slice (trapezoid layer-cake quadrature), renormalized to the EXACT solver
moments (E[D], E[ang]=E[v^2]/2, E[D ang]=E[Dv^2]/2), and the exact atom
A = exp(-t0(1+q/3)) of the two-component law.

Pre-registered protocol: see deepseek_push/L03_2D_TRANSFER.md (written
before this run).  In particular the JWST-reach rule:

    reach = smallest S in {50,20,10,5} with coverage(tau0)>=0.95,
    coverage(q)>=0.95, median 3 sig_tau0 <= 0.3 tau0, median 3 sig_q
    <= 0.5 (1+|q0|); else report the tau0-only reach.

No git commit.  MC legs capped at n=8e6 per cloud (4e6 cross-bin + 4e6
verification, independent seeds).
"""
import json
import sys
import time
import os

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from K05_ray_solver import legendre_quad, build_pg, eval_legendre_at
from J02_moment_hierarchy import simulate

from scipy import stats
from scipy.stats import chi2 as chi2_dist

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# 1. extended ray solver with kappa(r) = t0 (1 + q r^2)
# ----------------------------------------------------------------------

class RaySolverKappa(object):
    """K05 characteristic solver with kappa(r)=t0(1+q r^2).  Identical
    ray geometry (sigma, b^2, half-range escape at mu_esc = sigma_esc > 0)
    and Legendre projectors; the optical-depth attenuation along the ray is
    the exact closed form

        Phi(t) = int_0^t kappa(r(s)) ds
               = t0 [ t + q ( sig0^2 t + sig0 t^2 + t^3/3 + b^2 t ) ],
        r(s)^2 = (sig0 + s)^2 + b^2.

    Validity gate: kappa=1 must reproduce the K05 ladder values
    (0.50000, 2.80675, 3.70896 at Nr=160); and the closed form V2
    (S = 1 - kappa(r) r mu  ->  F = r mu exactly) must hold for kappa(r).
    """

    def __init__(self, Nr, Nq, L, Nt, t0=1.0, q=0.0, chunk=24):
        self.Nr, self.Nq, self.L, self.Nt = Nr, Nq, L, Nt
        self.t0, self.q = t0, q
        self.rnodes = np.concatenate(([0.0], (np.arange(Nr) + 0.5)/Nr))
        self.M = Nr + 1
        self.mu, self.wmu, self.Pg = legendre_quad(L, Nq)
        self.Pmat, self.Gmat = build_pg(L, Nq)
        self.xi, self.W = np.polynomial.legendre.leggauss(Nt)
        self.xi = 0.5*(self.xi + 1.0)
        self.W = 0.5*self.W
        self.chunk = chunk
        self._tables = {}

    def _phi(self, t, sig0, b2):
        """Exact integral kappa optical depth along the ray, Phi(t)."""
        t0, q = self.t0, self.q
        return t0*(t + q*(sig0*sig0*t + sig0*t*t + t*t*t/3.0 + b2*t))

    def _chunk_tables(self, c0, c1):
        key = (c0, c1)
        if key in self._tables:
            return self._tables[key]
        ri = self.rnodes[c0:c1]
        sig0 = ri[:, None]*self.mu[None, :]
        b2 = ri[:, None]**2*(1.0 - self.mu[None, :]**2)
        sig_esc = np.sqrt(np.maximum(1.0 - b2, 0.0))
        T = sig_esc - sig0
        bc_eff = sig_esc
        eT = np.exp(-self._phi(T, sig0, b2))
        n = c1 - c0
        Nt = self.Nt
        sig_k = sig0[:, :, None] + T[:, :, None]*self.xi[None, None, :]
        t_k = T[:, :, None]*self.xi[None, None, :]
        r_k = np.sqrt(np.maximum(sig_k**2 + b2[:, :, None], 0.0))
        mu_k = np.where(r_k > 1e-300, sig_k/np.maximum(r_k, 1e-300), 1.0)
        phi_t = self._phi(t_k, sig0[:, :, None], b2[:, :, None])
        wgt = (self.W[None, None, :]*T[:, :, None]*np.exp(-phi_t))
        kappa_k = self.t0*(1.0 + self.q*r_k*r_k)
        rk = r_k.ravel(); muk = mu_k.ravel(); w = wgt.ravel()
        kapk = kappa_k.ravel()
        m = np.searchsorted(self.rnodes, rk, side='left')
        m = np.clip(m, 1, self.M - 2)
        ia = np.stack([m - 1, m, m + 1], axis=1).astype(np.int64)
        wa = np.ones((len(rk), 3))
        for a in range(3):
            for bb in range(3):
                if bb != a:
                    wa[:, a] *= (rk - self.rnodes[ia[:, bb]]) \
                        / (self.rnodes[ia[:, a]] - self.rnodes[ia[:, bb]])
        self._tables[key] = dict(ri=ri, sig0=sig0, b2=b2, T=T, bc_eff=bc_eff,
                                 eT=eT, rk=rk, muk=muk, w=w, kapk=kapk,
                                 ia=ia, wa=wa)
        return self._tables[key]

    def project(self, F):
        L = self.L
        psi = np.zeros((self.M, L + 1))
        for l in range(L + 1):
            psi[:, l] = (2.0*l + 1.0)/2.0 * np.sum(self.wmu*F*self.Pg[:, l],
                                                   axis=1)
        return psi

    def _update(self, F, psi, S_kind, psi_src, bc_zero=False):
        kappa = None
        Nt = self.Nt
        L = self.L
        Fnew = np.zeros_like(F)
        for c0 in range(0, self.M, self.chunk):
            c1 = min(c0 + self.chunk, self.M)
            tb = self._chunk_tables(c0, c1)
            n = c1 - c0
            nn = n*self.Nq*Nt
            PV = (psi[tb['ia'][:, 0]]*tb['wa'][:, 0, None]
                  + psi[tb['ia'][:, 1]]*tb['wa'][:, 1, None]
                  + psi[tb['ia'][:, 2]]*tb['wa'][:, 2, None])
            Ptbl = eval_legendre_at(tb['muk'], L)
            KM = Ptbl @ self.Pmat
            PF = np.einsum('nl,nl->n', PV, KM)
            if S_kind == 'S10':
                S = np.ones(nn)
            elif S_kind == 'S02':
                S = 2.0*tb['kapk']             # 2 kappa(r) T, T = 1
            elif S_kind == 'known':
                S = 1.0 - tb['kapk']*tb['rk']*tb['muk']
            elif S_kind == 'S12':
                psi02, psi10 = psi_src
                PV02 = (psi02[tb['ia'][:, 0]]*tb['wa'][:, 0, None]
                        + psi02[tb['ia'][:, 1]]*tb['wa'][:, 1, None]
                        + psi02[tb['ia'][:, 2]]*tb['wa'][:, 2, None])
                PV10 = (psi10[tb['ia'][:, 0]]*tb['wa'][:, 0, None]
                        + psi10[tb['ia'][:, 1]]*tb['wa'][:, 1, None]
                        + psi10[tb['ia'][:, 2]]*tb['wa'][:, 2, None])
                F02v = np.einsum('nl,nl->n', PV02, Ptbl)
                GM = Ptbl @ self.Gmat
                GF10 = np.einsum('nl,nl->n', PV10, GM)
                S = F02v + 2.0*tb['kapk']*GF10
            else:
                raise ValueError(S_kind)
            integ = S - tb['kapk']*PF              # kappa(r(t)) (PF)
            bc_term = (tb['bc_eff']*tb['eT']) if not bc_zero \
                else np.zeros_like(tb['bc_eff'])
            val = (bc_term
                   - (tb['w'].reshape(n, self.Nq, Nt)
                      * integ.reshape(n, self.Nq, Nt)).sum(axis=2))
            Fnew[c0:c1] = val
        return Fnew

    def _kappa_field(self, tb):
        return tb['kapk']

    def solve_equation(self, S_kind, bc_zero=False, tol=1e-8, max_iter=400,
                       psi_src=None):
        M, Nq = self.M, self.Nq
        F = np.zeros((M, Nq))
        psi = self.project(F)
        gap = float('inf'); iters = 0; dcenter = float('inf')
        t0t = time.time()
        for it in range(1, max_iter + 1):
            Fnew = self._update(F, psi, S_kind, psi_src, bc_zero=bc_zero)
            dF = np.max(np.abs(Fnew - F))
            scale = max(1e-12, np.max(np.abs(Fnew)))
            gap = dF/scale
            center = float(np.mean(Fnew[0]))
            dcenter = abs(float(np.mean(F[0])) - center)
            F = Fnew
            psi = self.project(F)
            if gap < tol and dcenter < 1e-9 and it > 1:
                iters = it
                break
        else:
            iters = max_iter
        return F, psi, dict(iters=iters, gap=gap, dcenter=dcenter,
                            seconds=time.time() - t0t)

    def solve_hierarchy(self, tol=1e-8, max_iter=400):
        F10, psi10, i10 = self.solve_equation('S10', tol=tol,
                                              max_iter=max_iter)
        F02, psi02, i02 = self.solve_equation('S02', bc_zero=True, tol=tol,
                                              max_iter=max_iter)
        F12, psi12, i12 = self.solve_equation('S12', bc_zero=True, tol=tol,
                                              max_iter=max_iter,
                                              psi_src=(psi02, psi10))
        return dict(E_D=-float(np.mean(F10[0])),
                    E_v2=-float(np.mean(F02[0])),
                    E_Dv2=float(np.mean(F12[0])),
                    info=[i10, i02, i12])


def run_closed_form_kappa(cfgs):
    """V2-with-kappa(r): S = 1 - kappa(r) r mu has exact solution F = r mu."""
    out = {}
    for (Nr, Nq, L, Nt, t0, q) in cfgs:
        s = RaySolverKappa(Nr, Nq, L, Nt, t0=t0, q=q)
        F, psi, info = s.solve_equation('known', tol=1e-9, max_iter=200)
        err = float(np.max(np.abs(F - s.rnodes[:, None]*s.mu[None, :])))
        out[f'V2k_t0{t0}_q{int(q)}_{Nr}'] = dict(
            max_field_err=err, E_D=float(-np.mean(F[0])))
    return out


# ----------------------------------------------------------------------
# 2. MC legs (J02 engine)
# ----------------------------------------------------------------------

def mc_leg(n, t0, q, seed):
    r = simulate(n, t0, q, 'central', seed)
    D = r['D']; v2 = r['v2']; ang = r['ang']
    return D, v2, ang


def crossbins(D, ang, tedges, K=16):
    """Per-row: row masses (continuous), quantile slice of ang|row,
    conditional D-centroids (continuous), m1..m4."""
    nT = len(tedges) - 1
    cont = ang > 1e-12
    ti = np.clip(np.searchsorted(tedges, D, side='right') - 1, 0, nT - 1)
    p_cont = np.zeros(nT)
    slices = [None]*nT
    moments = np.zeros((nT, 4))
    p_all = np.zeros(nT)
    tau_cb = np.zeros(nT)
    for i in range(nT):
        m = ti == i
        p_all[i] = m.mean()
        a = ang[m & cont]
        p_cont[i] = (m & cont).mean()
        d_i = D[m & cont]
        tau_cb[i] = d_i.mean() if len(d_i) else 0.0
        if len(a) >= 60:
            qlv = np.quantile(a, np.linspace(0.005, 0.995, K))
        else:
            qlv = np.full(K, a.mean() if len(a) else 1.0)
        slices[i] = qlv
        if len(a):
            moments[i, 0] = a.mean(); moments[i, 1] = (a*a).mean()
            moments[i, 2] = (a**3).mean(); moments[i, 3] = (a**4).mean()
    return dict(p_all=p_all, p_cont=p_cont, slices=slices, moments=moments,
                tau_cb=tau_cb)


def spine_chi2_cdf(x):
    return chi2_dist(1).cdf(x)


# ----------------------------------------------------------------------
# 3. deterministic Psi construction
# ----------------------------------------------------------------------

def build_psi(cb, tedges, vedges, t0, q, E_D, E_ang, atom, K=16):
    """cb = crossbins output; returns Psi (nT,nV) normalized (sum=1),
    the continuous row-0 template phi0 (atom-free, row-normalized), and
    the continuous conditional D-centroids tau_cb (the first-moment slice)."""
    nT, nV = len(tedges) - 1, len(vedges) - 1
    tau_cb = cb['tau_cb'].copy()
    # row masses: replace the MC atom fraction by the exact atom
    p_cont = cb['p_cont'].copy()
    A_mc = cb['p_all'][0] - cb['p_cont'][0]
    p_cont[0] = cb['p_cont'][0] + (A_mc - atom)   # atom mass exact now
    # pin E[D] = E_D exactly (continuous part; atom sits at tau=0), using
    # the cross-bin conditional centroids as the first-moment slice
    E_D_cont = float(np.sum(tau_cb*p_cont))
    c = E_D / E_D_cont
    p_cont = p_cont*c
    # pin E[ang] = E_ang exactly (atom contributes 0)
    a_vec = np.array([np.mean(s) for s in cb['slices']])
    E_ang_cur = float(np.sum(p_cont*a_vec))
    r = E_ang / E_ang_cur
    slices = [s*r for s in cb['slices']]
    # cell law
    wq = np.full(K, 1.0/(K - 1)); wq[0] = wq[-1] = 0.5/(K - 1)
    Psi = np.zeros((nT, nV))
    ylo = vedges[:-1]; yhi = vedges[1:]
    for i in range(nT):
        s = slices[i]
        Fhi = np.zeros(nV); Flo = np.zeros(nV)
        for k in range(K):
            Fhi += wq[k]*spine_chi2_cdf(yhi/(2.0*s[k]))
            Flo += wq[k]*spine_chi2_cdf(ylo/(2.0*s[k]))
        Psi[i] = p_cont[i]*(Fhi - Flo)
    Psi[0, 0] += atom
    phi0 = Psi[0] - atom*(np.arange(nV) == 0)
    phi0 = phi0/np.sum(phi0)
    return Psi, phi0, p_cont, dict(E_D_check=float(np.sum(tau_cb*p_cont)),
                                   E_ang_check=float(np.sum(p_cont*a_vec*r)),
                                   E_Da_check=float(
                                       np.sum(tau_cb*p_cont*(a_vec*r)))), \
        tau_cb


# ----------------------------------------------------------------------
# 4. verification (leg B, independent)
# ----------------------------------------------------------------------

def ks_one_sample(x, cdf):
    """One-sample KS: D_n = sup |F_n - F0|, p = kstwobign.sf(D_n sqrt n)."""
    x = np.sort(np.asarray(x, dtype=float))
    n = len(x)
    F0 = cdf(x)
    F0 = np.clip(F0, 0.0, 1.0)
    Dp = np.max((np.arange(1, n + 1))/n - F0)
    Dm = np.max(F0 - np.arange(n)/n)
    D = max(Dp, Dm, 0.0)
    return D, stats.kstwobign.sf(D*np.sqrt(n))


def verify_row_v2(v2row, slices, atom_frac, tedges, vedges, Psi_i):
    """kstest of the v2|row sample vs the deterministic continuous row CDF
    (spine slice, atom jump included)."""
    nV = len(vedges) - 1
    wq = np.full(len(slices), 1.0/(len(slices) - 1))
    wq[0] = wq[-1] = 0.5/(len(slices) - 1)

    def cdf(v):
        v = np.atleast_1d(np.asarray(v, dtype=float))
        out = np.zeros(len(v))
        for k in range(len(slices)):
            out += wq[k]*spine_chi2_cdf(v/(2.0*slices[k]))
        return atom_frac + (1.0 - atom_frac)*out
    return ks_one_sample(v2row, cdf)


def run_verification(legB, Psi, slices, p_cont, atom, tedges, vedges,
                     tag, E_D, E_v2, E_Dv2):
    D, v2, ang = legB
    nT = len(tedges) - 1
    cont = ang > 1e-12
    ti = np.clip(np.searchsorted(tedges, D, side='right') - 1, 0, nT - 1)
    res = dict(tag=tag)
    rows = []
    atf0 = atom/Psi[0].sum() if Psi[0].sum() > 0 else 0.0
    for i in range(nT):
        m = ti == i
        nn = int(m.sum())
        if nn < 30:
            rows.append(dict(row=i, n=nn, p_v2=np.nan, p_W=np.nan,
                             Dn=np.nan))
            continue
        v2r = v2[m]
        a_i = slices[i]
        # deterministic conditional row CDF (atom only in row 0)
        atom_frac = atf0 if i == 0 else 0.0
        Dn, pv = verify_row_v2(v2r, a_i, atom_frac, tedges, vedges, None)
        # W-spine row: W = v2/(2 ang), continuous photons only, ~ chi2_1
        mc = m & cont
        W = v2[mc]/(2.0*ang[mc])
        _, pw = ks_one_sample(W, spine_chi2_cdf)
        rows.append(dict(row=i, n=nn, p_v2=pv, p_W=pw, Dn=Dn,
                         n_cont=int(mc.sum())))
    res['rows'] = rows
    res['n_pass_v2'] = sum(r['p_v2'] > 0.01 for r in rows)
    res['n_below_1e-3'] = sum(r['p_v2'] < 1e-3 for r in rows)
    res['n_pass_W'] = sum(r['p_W'] > 0.01 for r in rows)
    # marginal D
    p_all = p_cont.copy()
    p_all[0] += atom
    cum = np.cumsum(p_all)

    def cdfD(x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        ii = np.clip(np.searchsorted(tedges, x, side='right') - 1, 0, nT - 1)
        return cum[ii]
    _, pD = ks_one_sample(D, cdfD)
    res['marginal_D_ks_p'] = pD
    # moments panel (MC with SE vs deterministic)
    res['moments'] = dict(E_D_det=float(E_D), E_D_mc=float(D.mean()),
                          E_D_se=float(D.std(ddof=1)/np.sqrt(len(D))),
                          E_v2_det=float(E_v2), E_v2_mc=float(v2.mean()),
                          E_v2_se=float(v2.std(ddof=1)/np.sqrt(len(v2))),
                          E_Dv2_det=float(E_Dv2),
                          E_Dv2_mc=float((D*v2).mean()),
                          E_Dv2_se=float((D*v2).std(ddof=1)
                                         / np.sqrt(len(D))))
    return res


# ----------------------------------------------------------------------
# 5. recovery
# ----------------------------------------------------------------------

def recover(Psi, phi0, tau_cb, p_row, atom, S, nreals, seed, t0, q_truth):
    """Recovery per the pre-registered estimator.

    p_row: the constructed pre-grid continuous row masses (the grid row
    sums r_i^grid = Psi.sum(1) are calibrated to p_row, so the estimator
    is exactly unbiased against E[D] for any grid — the v^2>120
    truncation drops only continuous mass, whose first-moment share is
    restored by the calibration term p_row - r_grid; row 0 is calibrated
    on its continuous part only, r_grid[0] - atom)."""
    nT, nV = Psi.shape
    rng = np.random.default_rng(seed)
    sig2 = (Psi/S)**2
    r_grid = Psi.sum(axis=1)
    cal = p_row - r_grid                    # grid-truncation calibration
    cal[0] = p_row[0] - (r_grid[0] - atom)  # row 0: atom excluded
    ncell = nT*nV
    # LSQ geometry (row 0): J = [delta_0, phi0], weights 1/sig2[0,:]
    W0 = 1.0/sig2[0]
    JtWJ = np.array([[W0[0], W0[0]*phi0[0]], [W0[0]*phi0[0],
                     float(np.sum(W0*phi0*phi0))]])
    C = np.linalg.inv(JtWJ)
    CJtW = C @ np.vstack([np.eye(nV)[0], phi0]) * W0[None, :]  # (2, nV)
    pa = CJtW[0]                                   # dA/dPsi[0,j]
    # dbar Jacobian (cross-bin conditional centroids; atom at tau=0)
    Jd = np.zeros((nT, nV))
    for i in range(nT):
        Jd[i] = tau_cb[i]
    Jd[0] = tau_cb[0]*(1.0 - pa)
    # per-real loop
    A_hat = np.zeros(nreals); dbar = np.zeros(nreals)
    tau0 = np.zeros(nreals); qh = np.zeros(nreals)
    sA = np.zeros(nreals); s_tau0 = np.zeros(nreals); s_q = np.zeros(nreals)
    lost = 0; neg = 0
    for r in range(nreals):
        Psi_hat = Psi + rng.normal(0.0, np.sqrt(sig2))
        P0 = Psi_hat[0]
        y = np.array([W0[0]*P0[0], float(np.sum(W0*phi0*P0))])
        A, c = C @ y
        if A <= 1e-6:
            A = 1e-6; lost += 1
        A_hat[r] = A
        rsum = Psi_hat.sum(axis=1)
        # the atom mass is assigned to its exact location tau=0; the
        # continuous row masses enter at the cross-bin conditional
        # centroids tau_cb, with the observed grid row sums calibrated to
        # the constructed row masses p_row (deterministic tail calibration)
        d = float(np.sum(tau_cb[1:]*(rsum[1:] + cal[1:]))
                  + tau_cb[0]*(rsum[0] + cal[0] - A))
        dbar[r] = d
        t = -3.0*np.log(A) - 4.0*d
        if t <= 1e-9:
            t = 1e-9; neg += 1
        tau0[r] = t
        qh[r] = 4.0*d/t - 2.0
        # error propagation
        sA2 = C[0, 0]
        s_dbar2 = float(np.sum(Jd*Jd*sig2))
        cov = float(np.sum(pa*Jd[0]*sig2[0]))     # only row-0 cells couple
        sA[r] = np.sqrt(sA2)
        s_tau0[r] = np.sqrt((3.0/A)**2*sA2 + 16.0*s_dbar2
                            + 2.0*(-3.0/A)*(-4.0)*cov)
        # q Jacobian by finite differences
        eps = 1e-4
        qdA = (qp(A*(1+eps), d) - qp(A*(1-eps), d))/(2*A*eps)
        qdd = (qp(A, d*(1+eps)) - qp(A, d*(1-eps)))/(2*d*eps)
        s_q[r] = np.sqrt(qdA**2*sA2 + qdd**2*s_dbar2
                         + 2.0*qdA*qdd*cov)
    cov_tau0 = float(np.mean(np.abs(tau0 - t0) <= 3.0*s_tau0))
    cov_q = float(np.mean(np.abs(qh - q_truth) <= 3.0*s_q))
    return dict(S=S, bias_tau0=float(np.median(tau0) - t0),
                spread_tau0=float(np.std(tau0)),
                mad_tau0=float(1.4826*np.median(np.abs(tau0
                                                       - np.median(tau0)))),
                bias_q=float(np.median(qh) - q_truth),
                spread_q=float(np.std(qh)),
                mad_q=float(1.4826*np.median(np.abs(qh - np.median(qh)))),
                coverage_tau0=cov_tau0, coverage_q=cov_q,
                med_3sig_tau0=float(3.0*np.median(s_tau0)),
                med_3sig_q=float(3.0*np.median(s_q)),
                spike_lost=lost, broken=neg)


def qp(A, d):
    t = -3.0*np.log(max(A, 1e-9)) - 4.0*d
    return 4.0*d/t - 2.0


def jwst_reach(rec, t0, q_truth, rule_bars=(0.3, 0.5)):
    """PRE-REGISTERED rule (L03_2D_TRANSFER.md section 4)."""
    cand = {}
    for r in rec:
        S = r['S']
        ok4 = (r['coverage_tau0'] >= 0.95 and r['coverage_q'] >= 0.95
               and r['med_3sig_tau0'] <= rule_bars[0]*t0
               and r['med_3sig_q'] <= rule_bars[1]*(1.0 + abs(q_truth)))
        ok_tau0_only = (r['coverage_tau0'] >= 0.95
                        and r['med_3sig_tau0'] <= rule_bars[0]*t0)
        cand[S] = dict(pair=ok4, tau0_only=ok_tau0_only)
    pair = [S for S in sorted(cand) if cand[S]['pair']]
    tOnly = [S for S in sorted(cand) if cand[S]['tau0_only']]
    return dict(pair_reach=str(pair[0]) if pair else None,
                tau0_only_reach=str(tOnly[0]) if tOnly else None,
                per_S=cand)


# ----------------------------------------------------------------------
# 6. main
# ----------------------------------------------------------------------

def main():
    t_all = time.time()
    out = {}
    print("="*76)
    print("L03 deterministic 2D transfer function + recovery pipeline")
    print("pre-registered: deepseek_push/L03_2D_TRANSFER.md (written first)")
    print("="*76)
    import warnings as _w
    _w.filterwarnings('ignore', category=RuntimeWarning)

    # ---- extended solver validity gate (kappa=1 vs K05 ladder) ---------
    print("\n[1] extended ray solver (kappa(r)=t0(1+q r^2))")
    v2k = run_closed_form_kappa([(160, 64, 16, 32, 1.0, 0.0),
                                 (160, 64, 16, 32, 1.0, 2.0)])
    print("  V2(kappa(r)) closed form F=r mu:", v2k)
    out['closed_form_kappa'] = v2k

    sol = {}
    for (t0, q) in ((1.0, 0.0), (1.0, 2.0)):
        s = RaySolverKappa(160, 64, 16, 32, t0=t0, q=q)
        m = s.solve_hierarchy()
        sol[(t0, q)] = m
        print("  cloud t0=%.0f q=%.0f: E[D]=%.5f E[v2]=%.5f E[Dv2]=%.5f"
              "  iters=%s" % (t0, q, m['E_D'], m['E_v2'], m['E_Dv2'],
                              [i['iters'] for i in m['info']]))
    out['solver'] = {f't0{t0}_q{int(q)}': {k: v for k, v in m.items()
                                           if k != 'info'}
                     for (t0, q), m in sol.items()}
    gate = sol[(1.0, 0.0)]
    out['validity_gate_k05'] = dict(E_D=gate['E_D'], E_v2=gate['E_v2'],
                                    E_Dv2=gate['E_Dv2'],
                                    k05=dict(E_D=0.500000, E_v2=2.80674,
                                             E_Dv2=3.70900))

    # ---- grids, anchors ----
    tedges = np.linspace(0.0, 12.0, 41)
    vedges = np.linspace(0.0, 120.0, 41)
    clouds = {}
    seedsA = {0: 11, 2: 12}
    seedsB = {0: 20260923, 2: 20260924}
    for (t0, q) in ((1.0, 0.0), (1.0, 2.0)):
        tag = f"q{int(q)}"
        print(f"\n[2] cloud t0=1 q={q}  (leg A cross-bins n=4e6, "
              f"leg B verification n=4e6)")
        t0c = time.time()
        DA, v2A, angA = mc_leg(4_000_000, t0, q, seedsA[int(q)])
        cb = crossbins(DA, angA, tedges)
        del DA, v2A, angA
        atom = np.exp(-t0*(1.0 + q/3.0))
        m = sol[(t0, q)]
        E_D = float(m['E_D']); E_v2 = float(m['E_v2'])
        E_Dv2 = float(m['E_Dv2'])
        E_ang = E_v2/2.0
        Psi, phi0, p_cont, chk, tau_cb = build_psi(cb, tedges, vedges, t0, q,
                                                   E_D, E_ang, atom)
        print(f"  atom={atom:.6f}  Psi[0,0]={Psi[0,0]:.6f}  "
                  f"E[D]={chk['E_D_check']:.6f} E[ang]={chk['E_ang_check']:.6f} "
                  f"E[D ang]={chk['E_Da_check']:.6f}  mass={Psi.sum():.4f}")
        out[f'cloud_{tag}'] = dict(atom=atom,
                                   E_D=dr(E_D), E_v2=dr(E_v2),
                                   E_Dv2=dr(E_Dv2),
                                   construction_checks=chk)
        # leg B verification
        DB, v2B, angB = mc_leg(4_000_000, t0, q, seedsB[int(q)])
        ver = run_verification((DB, v2B, angB), Psi, cb['slices'],
                               p_cont, atom, tedges, vedges, tag,
                               E_D, E_v2, E_Dv2)
        del DB, v2B, angB
        out[f'verification_{tag}'] = ver
        pv = [r['p_v2'] for r in ver['rows']]
        pw = [r['p_W'] for r in ver['rows']]
        print(f"  per-row v2-KS : pass>0.01 {ver['n_pass_v2']}/40, "
              f"p<1e-3 in {ver['n_below_1e-3']} rows, min p={np.nanmin(pv):.4f}")
        print(f"  per-row W-spine: pass>0.01 {ver['n_pass_W']}/40, "
              f"min p={np.nanmin(pw):.4f}")
        print(f"  marginal D-KS p={ver['marginal_D_ks_p']:.3f}   "
              f"moments MC: E[D]={ver['moments']['E_D_mc']:.4f} "
              f"E[v2]={ver['moments']['E_v2_mc']:.4f} "
              f"E[Dv2]={ver['moments']['E_Dv2_mc']:.4f}")
        for r in ver['rows']:
            print("   row %2d n=%7d p_v2=%8.4f p_W=%8.4f" % (
                r['row'], r['n'], r['p_v2'], r['p_W']))
        # ---- recovery ----
        print(f"  [3] recovery (500 reals x S/N in {{50,20,10,5}})")
        rec = []
        for S in (50, 20, 10, 5):
            rc = recover(Psi, phi0, tau_cb, p_cont, atom, S, 500,
                         1000 + int(q)*100 + S, t0, q)
            rec.append(rc)
            print("   S/N=%3d: bias(t0)=%+.4f spread=%4.3f 3sig/t0=%5.3f "
                  "cov(t0)=%.3f | bias(q)=%+.4f spread=%4.3f "
                  "3sig_q=%5.3f cov(q)=%.3f lost=%d" % (
                      S, rc['bias_tau0'], rc['spread_tau0'],
                      rc['med_3sig_tau0']/t0, rc['coverage_tau0'],
                      rc['bias_q'], rc['spread_q'], rc['med_3sig_q'],
                      rc['coverage_q'], rc['spike_lost']))
        reach = jwst_reach(rec, t0, q)
        out[f'recovery_{tag}'] = dict(reals=500, curve=rec,
                                      jwst_reach=reach)
        clouds[tag] = reach
        o = reach['pair_reach'] or reach['tau0_only_reach']
        print(f"  JWST reach (pair / tau0-only): {reach['pair_reach']} / "
              f"{reach['tau0_only_reach']}")
        print(f"  leg time {time.time()-t0c:.0f}s")
    out['jwst_reach_summary'] = {k: v['pair_reach'] or v['tau0_only_reach']
                                 for k, v in clouds.items()}
    out['total_seconds'] = time.time() - t_all

    # ---- checks (machine-readable) ----
    checks = []
    for tag in ('q0', 'q2'):
        ver = out[f'verification_{tag}']
        checks.append(f"L03.{tag}: per-row v2-KS p>0.01 in "
                      f"{ver['n_pass_v2']}/40 rows")
        checks.append(f"L03.{tag}: p<1e-3 rows = {ver['n_below_1e-3']}"
                      f" (kill >3)")
        checks.append(f"L03.{tag}: W-spine p>0.01 in {ver['n_pass_W']}/40"
                      " rows (slice-free deterministic content)")
        checks.append(f"L03.{tag}: marginal D-KS p="
                      f"{ver['marginal_D_ks_p']:.3f}")
    gate_ok = abs(gate['E_D'] - 0.5) < 1e-3 and abs(gate['E_v2'] - 2.80674) \
        < 1e-3
    checks.append(f"L03.gate: kappa=1 re-solve vs K05 ladder: E[D]="
                  f"{gate['E_D']:.5f} E[v2]={gate['E_v2']:.5f} "
                  f"E[Dv2]={gate['E_Dv2']:.5f} (K05 0.5/2.80674/3.70900)")
    for tag in ('q0', 'q2'):
        rz = out[f'recovery_{tag}']['jwst_reach']
        checks.append(f"L03.recovery.{tag}: pair-reach S/N="
                      f"{rz['pair_reach']}, tau0-only reach S/N="
                      f"{rz['tau0_only_reach']}")
    out['checks'] = checks
    out['verdict'] = ('PASS' if all(
        out[f'verification_{t}']['n_below_1e-3'] <= 3
        and out[f'verification_{t}']['n_pass_v2'] >= 36
        for t in ('q0', 'q2')) else 'BROKEN')
    out['jwst_snr_reach'] = "; ".join(
        f"{k}: pair={v['pair_reach']} tau0only={v['tau0_only_reach']}"
        for k, v in clouds.items())
    print("="*76)
    print("verdict:", out['verdict'])
    print("jwst_snr_reach:", out['jwst_snr_reach'])
    for c in checks:
        print("  check:", c)
    print(f"total {time.time()-t_all:.0f}s")
    with open(os.path.join(HERE, 'L03_results.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=float)
    # append results section to the pre-registered md
    with open(os.path.join(HERE, 'L03_2D_TRANSFER.md'), 'a') as fh:
        fh.write("\n```\n" + json.dumps(
            dict(verification={k: out[f'verification_{k}']
                               for k in ('q0', 'q2')},
                 recovery={k: out[f'recovery_{k}'] for k in ('q0', 'q2')},
                 jwst_reach=out['jwst_reach_summary'],
                 verdict=out['verdict']), indent=1, default=float) + "\n```\n")
    return 0


def dr(x):
    return float(round(float(x), 6))


if __name__ == '__main__':
    sys.exit(main())