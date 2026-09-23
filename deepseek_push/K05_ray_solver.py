#!/usr/bin/env python3
r"""
K05 -- CHARACTERISTIC (RAY) SOLVER FOR THE DETERMINISTIC MOMENT HIERARCHY
2026-09-23.  The registered J04 cure (b): replace the P_N algebraic BVP --
whose Marshak half-range rows leave a near-null constant mode
(cond ~ 1e17) -- by integration of the backward transport equation along
exact straight rays, carrying the exact half-range boundary data
(r = 1, mu > 0) only.

    L F = S,   L := u.grad + kappa(P . - .),
    u.grad = mu d_r + (1-mu^2)/r d_mu

Hierarchy (J01/J02/J04; kappa = T = 1, uniform sphere radius 1):
    L F^10 = 1,             F^10|_b = mu    ->  -F^10(0) = E[D]   (= 0.5)
    L F^02 = 2 kappa T,     F^02|_b = 0     ->  -F^02(0) = E[v^2] (~2.8061)
    L F^12 = F^02 + 2 kappa T G F^10, F^12|_b = 0
                                           ->   F^12(0) = E[D v^2] (~3.7316)

Method.  Every target point (r, mu) lies on the straight ray x(t) = x + u t.
Ray invariants:   sigma(t) := x(t).u = r mu + t   (strictly monotone),
                  b^2      := |x|^2 - (x.u)^2 = r^2 (1 - mu^2).
The ray escapes the unit sphere at sigma_esc = sqrt(1 - b^2) with
mu_esc = sigma_esc > 0 -- ALWAYS in the outgoing half-range.  Hence the
boundary data at r = 1, mu < 0 (incoming rays) is never queried: the
half-range data (mu > 0) is necessary AND sufficient.  This is exactly the
well-posedness the J04 algebraic BVP lacked (its Marshak rows left the
constant mode near-null).

Along the ray, dF/dt = S + kappa(F - PF)  (from L F = S); integrating
backward from the escape point with F_esc = bc(mu_esc):

    F(r,mu) = e^{-kappa T} bc(mu_esc)
                  - int_0^T e^{-kappa t} [S - kappa (PF)](r(t), mu(t)) dt,
    T = sigma_esc - r mu,
    r(t) = sqrt((r mu + t)^2 + b^2),   mu(t) = (r mu + t)/r(t).

Collision averages (PF) and mixing terms (G F^10) are computed from the
J04-VERIFIED Legendre projectors Pmat/Gmat: the field is carried on the
mu-grid (Gauss-Legendre nodes), re-projected at every radial step to P_N
mode coefficients

    psi_l(r_i) = (2l+1)/2 * sum_j w_j F(r_i, mu_j) P_l(mu_j),

and ray integrands (which need F at arbitrary (r(t), mu(t))) are evaluated
as Legendre series with 3-point Lagrange interpolation of the modes in r.

The scattering coupling is a strict contraction (P is a probability
kernel: ||P f||_inf <= ||f||_inf, attenuated by e^{-kappa t}), so source
iteration converges; iterations run to a max-relative-change tolerance
(tuned to CONVERGENCE, never to the moment targets).  Deterministic
throughout: no RNG, no Monte Carlo.

Built-in honesty battery (closed forms the solver must reproduce):
  V1  kappa=0, S=1, bc=mu        ->  F^10 = r mu exactly   (geometry+quadrature)
  V2  kappa=1, S=1-kappa r mu,
      bc=mu                      ->  F^10 = r mu exactly   (collision term ON)
  V3  projector checks: Pmat.1 = 1  (normalization) and
      Pmat.(r mu modes) ~ 1e-15  (Thomson isotropy, J04-verified repro)

Moments are the r = 0 node value: F(0) is evaluated by the same ray integral
(all directions equivalent there; the mu-average and its spread are reported).
"""
import json
import sys
import time

import numpy as np


# ------------------------------------------------------------------------
# Legendre quadrature + the VERIFIED J04 projectors Pmat / Gmat
# ------------------------------------------------------------------------

def legendre_quad(L, Nq):
    """Gauss-Legendre nodes/weights on [-1,1] and P_l(mu) at the nodes."""
    x, w = np.polynomial.legendre.leggauss(Nq)
    P = np.zeros((Nq, L + 1))
    for l in range(L + 1):
        P[:, l] = np.polynomial.legendre.legval(x, np.eye(L + 1)[l])
    return x, w, P


def build_pg(L, Nq):
    """Thomson projection Pmat and mix kernel Gmat, EXACTLY (kernels are
    low-degree polynomials; Gaussian quadrature of order Nq integrates them
    exactly).  Construction and normalisation identical to the J04 file, where
    they were verified at 1e-15 against fine-grid quadrature."""
    x, w, Pg = legendre_quad(L, Nq)
    Pmat = np.zeros((L + 1, L + 1))
    Gmat = np.zeros((L + 1, L + 1))
    for ll in range(L + 1):
        for lp in range(L + 1):
            pp = gg = 0.0
            for j in range(Nq):
                m = x[j]
                for k in range(Nq):
                    mp = x[k]
                    kernelP = 0.375 * (1.0 + m*m*mp*mp
                                       + 0.5*(1 - m*m)*(1 - mp*mp))
                    kernelG = 0.375 * (1.0 - m*mp + m*m*mp*mp - m**3*mp**3
                                       + 0.5*(1 - m*m)*(1 - mp*mp)
                                       - 1.5*m*mp*(1 - m*m)*(1 - mp*mp))
                    pp += w[j]*w[k]*Pg[j, ll]*kernelP*Pg[k, lp]
                    gg += w[j]*w[k]*Pg[j, ll]*kernelG*Pg[k, lp]
            Pmat[ll, lp] = pp
            Gmat[ll, lp] = gg
    for ll in range(L + 1):                       # Legendre norm (2l+1)/2
        Pmat[ll, :] *= (2.0*ll + 1.0)/2.0
        Gmat[ll, :] *= (2.0*ll + 1.0)/2.0
    return Pmat, Gmat


def eval_legendre_at(mu_vals, L):
    """P_l(mu) for l = 0..L at arbitrary mu (recurrence).  Shape (n, L+1)."""
    n = len(mu_vals)
    P = np.zeros((n, L + 1))
    P[:, 0] = 1.0
    if L >= 1:
        P[:, 1] = mu_vals
        for l in range(1, L):
            P[:, l + 1] = ((2*l + 1.0)*mu_vals*P[:, l]
                           - l*P[:, l - 1]) / (l + 1.0)
    return P


# ------------------------------------------------------------------------
# Characteristic (ray) solver
# ------------------------------------------------------------------------

class RaySolver:
    """Deterministic collision-source iteration on the exact ray integrals.

    Grid:  M = Nr + 1 radial nodes  rnodes = [0, (0.5+i)/Nr]  (the r=0 node
    included so inward radial rays never need extrapolation), and Nq
    Gauss-Legendre mu nodes on [-1,1]; the field is carried on (M, Nq),
    re-projected to L+1 Legendre modes at every radial step.  Each ray is
    integrated with Nt Gauss nodes on [0, T].
    """

    def __init__(self, Nr, Nq, L, Nt, kappa=1.0, chunk=24):
        self.Nr, self.Nq, self.L, self.Nt = Nr, Nq, L, Nt
        self.kappa = kappa
        self.rnodes = np.concatenate(([0.0], (np.arange(Nr) + 0.5)/Nr))
        self.M = Nr + 1
        self.dr = 1.0/Nr
        self.mu, self.wmu, self.Pg = legendre_quad(L, Nq)
        self.Pmat, self.Gmat = build_pg(L, Nq)
        self.xi, self.W = np.polynomial.legendre.leggauss(Nt)
        self.xi = 0.5*(self.xi + 1.0)              # [0,1] nodes
        self.W = 0.5*self.W
        self.chunk = chunk
        self._tables = {}                          # per-chunk ray tables

    # -- ray tables for a chunk of r-targets ----------------------------
    def _chunk_tables(self, c0, c1):
        key = (c0, c1)
        if key in self._tables:
            return self._tables[key]
        ri = self.rnodes[c0:c1]                    # (nc,)
        sig0 = ri[:, None] * self.mu[None, :]      # (nc, Nq) x.u
        b2 = ri[:, None]**2 * (1.0 - self.mu[None, :]**2)
        sig_esc = np.sqrt(np.maximum(1.0 - b2, 0.0))   # = mu_esc > 0
        T = sig_esc - sig0
        bc_eff = sig_esc                            # bc(mu_esc) = mu_esc
        eT = np.exp(-self.kappa*T)
        n = c1 - c0
        Nt = self.Nt
        sig_k = sig0[:, :, None] + T[:, :, None]*self.xi[None, None, :]
        t_k = T[:, :, None]*self.xi[None, None, :]
        r_k = np.sqrt(np.maximum(sig_k**2 + b2[:, :, None], 0.0))
        mu_k = np.where(r_k > 1e-300, sig_k/np.maximum(r_k, 1e-300), 1.0)
        wgt = (self.W[None, None, :]*T[:, :, None]
               * np.exp(-self.kappa*t_k))          # dt-weighted, e^{-kappa t}
        # flattened over (n_nodes = n*Nq*Nt,)
        rk = r_k.ravel()
        muk = mu_k.ravel()
        w = wgt.ravel()
        # 3-point Lagrange interpolation in r
        m = np.searchsorted(self.rnodes, rk, side='left')
        m = np.clip(m, 1, self.M - 2)
        ia = np.stack([m - 1, m, m + 1], axis=1).astype(np.int64)
        wa = np.ones((len(rk), 3))
        for a in range(3):
            for bb in range(3):
                if bb != a:
                    wa[:, a] *= (rk - self.rnodes[ia[:, bb]]) \
                        / (self.rnodes[ia[:, a]] - self.rnodes[ia[:, bb]])
        self._tables[key] = dict(ri=ri, sig0=sig0, b2=b2, sig_esc=sig_esc,
                                 T=T, bc_eff=bc_eff, eT=eT,
                                 rk=rk, muk=muk, w=w, ia=ia, wa=wa)
        return self._tables[key]

    # -- P_N projection at every radial node -----------------------------
    def project(self, F):
        """F (M, Nq) -> psi_l(r_i) = (2l+1)/2 sum_j w_j F P_l(mu_j)."""
        L = self.L
        psi = np.zeros((self.M, L + 1))
        for l in range(L + 1):
            psi[:, l] = (2.0*l + 1.0)/2.0 * np.sum(self.wmu*F*self.Pg[:, l],
                                                   axis=1)
        return psi

    # -- one source-iteration update pass over all chunks ----------------
    def _update(self, F, psi, S_kind, psi_src, bc_zero=False):
        """Return new F grid from the ray integrals using collision sources
        built from psi (the current iterate) and, for the F^12 equation, the
        fixed solved fields psi_src = (psi02, psi10, psi10G)."""
        kappa = self.kappa
        Nt = self.Nt
        L = self.L
        Fnew = np.zeros_like(F)
        for c0 in range(0, self.M, self.chunk):
            c1 = min(c0 + self.chunk, self.M)
            tb = self._chunk_tables(c0, c1)
            n = c1 - c0
            nn = n*self.Nq*Nt
            # interpolated mode vector at every ray node  (nn, L+1)
            PV = (psi[tb['ia'][:, 0]]*tb['wa'][:, 0, None]
                  + psi[tb['ia'][:, 1]]*tb['wa'][:, 1, None]
                  + psi[tb['ia'][:, 2]]*tb['wa'][:, 2, None])
            Ptbl = eval_legendre_at(tb['muk'], L)
            KM = Ptbl @ self.Pmat                    # (nn, L+1)
            PF = np.einsum('nl,nl->n', PV, KM)       # (P F)(r(t),mu(t))
            if S_kind == 'S10':
                S = np.ones(nn)
            elif S_kind == 'S02':
                S = 2.0 * np.ones(nn)                # 2 kappa T = 2
            elif S_kind == 'known':
                S = 1.0 - kappa*tb['rk']*tb['muk']   # S = 1 - kappa r mu
            elif S_kind == 'S12':
                psi02, psi10, psi10G = psi_src
                PV02 = (psi02[tb['ia'][:, 0]]*tb['wa'][:, 0, None]
                        + psi02[tb['ia'][:, 1]]*tb['wa'][:, 1, None]
                        + psi02[tb['ia'][:, 2]]*tb['wa'][:, 2, None])
                PV10 = (psi10[tb['ia'][:, 0]]*tb['wa'][:, 0, None]
                        + psi10[tb['ia'][:, 1]]*tb['wa'][:, 1, None]
                        + psi10[tb['ia'][:, 2]]*tb['wa'][:, 2, None])
                F02v = np.einsum('nl,nl->n', PV02, Ptbl)
                GM = Ptbl @ self.Gmat
                GF10 = np.einsum('nl,nl->n', PV10, GM)
                S = F02v + 2.0*GF10
            else:
                raise ValueError(S_kind)
            integ = S - kappa*PF
            bc_term = (tb['bc_eff']*tb['eT']) if not bc_zero \
                else np.zeros_like(tb['bc_eff'])
            val = (bc_term
                   - (tb['w'].reshape(n, self.Nq, Nt)
                      * integ.reshape(n, self.Nq, Nt)).sum(axis=2))
            Fnew[c0:c1] = val
        return Fnew

    # -- solve one hierarchy equation by source iteration -----------------
    def solve_equation(self, S_kind, bc_zero=False, tol=1e-8, max_iter=400,
                       psi_src=None):
        """Source iteration for L F = S with F|_b = bc.  bc = mu_esc unless
        bc_zero (F^02, F^12).  Returns (F, psi, info)."""
        kappa = self.kappa
        M, Nq = self.M, self.Nq
        F = np.zeros((M, Nq))
        psi = self.project(F)
        info = dict(iters=0, gap=float('inf'), moment_gap=float('inf'),
                    hist=[])
        t0 = time.time()
        for it in range(1, max_iter + 1):
            Fnew = self._update(F, psi, S_kind, psi_src, bc_zero=bc_zero)
            dF = np.max(np.abs(Fnew - F))
            scale = max(1e-12, np.max(np.abs(Fnew)))
            gap = dF/scale
            center = float(np.mean(Fnew[0]))
            dcenter = abs(float(np.mean(F[0])) - center)
            info['hist'].append((it, gap, center))
            F = Fnew
            psi = self.project(F)
            if gap < tol and dcenter < 1e-9 and it > 1:
                info['iters'] = it
                info['gap'] = gap
                info['moment_gap'] = dcenter
                break
        else:
            info['iters'] = max_iter
            info['gap'] = gap
            info['moment_gap'] = dcenter
            info['did_not_converge'] = True
        info['seconds'] = time.time() - t0
        # center value and the internal spread over directions
        info['center_spread'] = float(np.max(np.abs(F[0] - F[0][0])))
        return F, psi, info

    # --------------------------------------------------------------------
    def solve_hierarchy(self, tol=1e-8, max_iter=400):
        """Solve F^10, F^02, then F^12 (sequential; the last's source needs
        the first two).  Returns dict with moments, fields and diagnostics."""
        F10, psi10, i10 = self.solve_equation('S10', tol=tol,
                                              max_iter=max_iter)
        F02, psi02, i02 = self.solve_equation('S02', bc_zero=True, tol=tol,
                                              max_iter=max_iter)
        F12, psi12, i12 = self.solve_equation('S12', bc_zero=True, tol=tol,
                                              max_iter=max_iter,
                                              psi_src=(psi02, psi10, None))
        E_D = -float(np.mean(F10[0]))
        E_v2 = -float(np.mean(F02[0]))
        E_Dv2 = float(np.mean(F12[0]))
        return dict(E_D=E_D, E_v2=E_v2, E_Dv2=E_Dv2,
                    spread_D=float(np.max(np.abs(F10[0] - F10[0][0]))),
                    spread_v2=float(np.max(np.abs(F02[0] - F02[0][0]))),
                    spread_Dv2=float(np.max(np.abs(F12[0] - F12[0][0]))),
                    info10=i10, info02=i02, info12=i12,
                    fields=(F10, F02, F12), psi=(psi10, psi02, psi12))


# ------------------------------------------------------------------------
# main: honesty battery V1-V3 + grid-convergence ladder + target compare
# ------------------------------------------------------------------------

def run_closed_forms():
    """V1: kappa=0, S=1, bc=mu -> F^10 = r*mu (exact, pure geometry).
    V2: kappa=1, S=1-kappa r mu, bc=mu -> F^10 = r*mu (collision ON).
    V3: Pmat.1 = 1 ; Pmat.(r mu) ~ 1e-15 (projector repro of J04)."""
    res = {}
    # V3
    L, Nq = 16, 64
    Pmat, Gmat = build_pg(L, Nq)
    e0 = np.zeros(L + 1); e0[0] = 1.0
    v3a = float(np.max(np.abs(Pmat @ e0 - e0)))     # projection of constant
    v3c = float(np.max(np.abs(Gmat @ e0 - e0)))     # G kernel also averages 1
    rmu_modes = np.zeros(L + 1); rmu_modes[1] = 1.0
    v3b = float(np.max(np.abs(Pmat @ rmu_modes)))
    res['V3_Pmat_const'] = v3a
    res['V3_Gmat_const'] = v3c
    res['V3_Pmat_rmu'] = v3b

    # V1 (kappa=0): one exact pass
    for (Nr, Nq, L, Nt) in ((80, 48, 12, 24), (160, 64, 16, 32)):
        s = RaySolver(Nr, Nq, L, Nt, kappa=0.0)
        F, psi, info = s.solve_equation('S10', tol=1e-12, max_iter=3)
        rnodes = s.rnodes
        err = np.max(np.abs(F - rnodes[:, None]*s.mu[None, :]))
        res[f'V1_{Nr}_{Nq}_{L}_{Nt}'] = dict(max_field_err=float(err),
                                             E_D=float(-np.mean(F[0])))
    # V2 (kappa=1, exact solution r mu): source iteration
    for (Nr, Nq, L, Nt) in ((80, 48, 12, 24), (160, 64, 16, 32)):
        s = RaySolver(Nr, Nq, L, Nt, kappa=1.0)
        F, psi, info = s.solve_equation('known', tol=1e-9, max_iter=200)
        err = np.max(np.abs(F - s.rnodes[:, None]*s.mu[None, :]))
        res[f'V2_{Nr}_{Nq}_{L}_{Nt}'] = dict(
            max_field_err=float(err), E_D=float(-np.mean(F[0])),
            iters=info['iters'], gap=info['gap'])
    return res


# ------------------------------------------------------------------------
# V4: collision-average discretization cross-check (direct mu-grid
# quadrature, no Legendre modes -- structurally independent of the P_N
# path).  Solves the expected-collision-count equation u.grad N +
# kappa(PN - N) = -kappa, bc = 0, whose center value is E[N].  The J01/J02
# chain pins E[N] = E[v^2]/2 = 1.4031 (with E[v^2] = 2.8061 from MC).
# ------------------------------------------------------------------------

def run_mugrid_crosscheck(Nr=160, Nq=64, Nt=32, kappa=1.0):
    def kernelP(m, mp):
        return 0.375*(1.0 + m*m*mp*mp + 0.5*(1-m*m)*(1-mp*mp))

    rnodes = np.concatenate(([0.0], (np.arange(Nr) + 0.5)/Nr))
    M = Nr + 1
    mu, wmu = np.polynomial.legendre.leggauss(Nq)
    xi, W = np.polynomial.legendre.leggauss(Nt)
    xi = 0.5*(xi + 1.0); W = 0.5*W
    chunk = 24
    tables = {}
    F = np.zeros((M, Nq))
    hist = []
    for it in range(1, 400):
        Fn = np.zeros_like(F)
        for c0 in range(0, M, chunk):
            c1 = min(c0 + chunk, M)
            key = (c0, c1)
            if key not in tables:
                ri = rnodes[c0:c1]
                sig0 = ri[:, None]*mu[None, :]
                b2 = ri[:, None]**2*(1.0 - mu[None, :]**2)
                sig_esc = np.sqrt(np.maximum(1.0 - b2, 0.0))
                T = sig_esc - sig0
                n = c1 - c0
                sig_k = sig0[:, :, None] + T[:, :, None]*xi[None, None, :]
                t_k = T[:, :, None]*xi[None, None, :]
                r_k = np.sqrt(np.maximum(sig_k**2 + b2[:, :, None], 0.0))
                mu_k = np.where(r_k > 1e-300, sig_k/np.maximum(r_k, 1e-300),
                                1.0)
                wgt = W[None, None, :]*T[:, :, None]*np.exp(-kappa*t_k)
                rk = r_k.ravel()
                mnd = np.searchsorted(rnodes, rk, side='left')
                mnd = np.clip(mnd, 1, M - 2)
                ia = np.stack([mnd - 1, mnd, mnd + 1], axis=1).astype(np.int64)
                wa = np.ones((len(rk), 3))
                for a in range(3):
                    for bb in range(3):
                        if bb != a:
                            wa[:, a] *= (rk - rnodes[ia[:, bb]]) \
                                / (rnodes[ia[:, a]] - rnodes[ia[:, bb]])
                Kt = kernelP(mu_k.ravel()[:, None], mu[None, :]) \
                    * wmu[None, :]
                tables[key] = dict(w=wgt.reshape(n, Nq, Nt), ia=ia, wa=wa,
                                   Kt=Kt)
            tb = tables[key]
            n = c1 - c0
            nn = n*Nq*Nt
            Fg = F[tb['ia']]
            Fr = np.einsum('naq,na->nq', Fg, tb['wa'])
            PF = np.einsum('nq,nq->n', Fr, tb['Kt'])
            integ = 1.0 - kappa*PF            # L N = -kappa, bc = 0
            val = -(tb['w']*integ.reshape(n, Nq, Nt)).sum(axis=2)
            Fn[c0:c1] = val
        gap = np.max(np.abs(Fn - F))/max(1e-12, np.max(np.abs(Fn)))
        hist.append((it, gap, float(np.mean(Fn[0]))))
        F = Fn
        if gap < 1e-9 and it > 1:
            break
    return dict(E_N=float(-np.mean(F[0])), E_v2_from_2EN=float(-2*np.mean(F[0])),
                iters=hist[-1][0], gap=hist[-1][1],
                MC_reference=dict(E_N=1.4031, E_v2=2.8061))


def run_ladder(cfgs):
    rows = []
    for cfg in cfgs:
        Nr, Nq, L, Nt = cfg
        s = RaySolver(Nr, Nq, L, Nt, kappa=1.0)
        t0 = time.time()
        r = s.solve_hierarchy(tol=1e-8, max_iter=400)
        rows.append(dict(cfg=list(cfg),
                         E_D=r['E_D'], E_v2=r['E_v2'], E_Dv2=r['E_Dv2'],
                         spread=[r['spread_D'], r['spread_v2'],
                                 r['spread_Dv2']],
                         iters=[r['info10']['iters'], r['info02']['iters'],
                                r['info12']['iters']],
                         gaps=[r['info10']['gap'], r['info02']['gap'],
                               r['info12']['gap']],
                         secs=time.time() - t0))
        print(f"cfg {cfg}: E[D] = {r['E_D']:.5f}  E[v^2] = {r['E_v2']:.5f}  "
              f"E[Dv^2] = {r['E_Dv2']:.5f}  "
              f"iters = {r['info10']['iters']}/{r['info02']['iters']}/"
              f"{r['info12']['iters']}  "
              f"gaps = {r['info10']['gap']:.1e}/{r['info02']['gap']:.1e}/"
              f"{r['info12']['gap']:.1e}  ({time.time()-t0:.1f}s)")
    return rows


def main():
    t_start = time.time()
    out = {}
    print("=" * 72)
    print("K05 characteristic (ray) solver -- closed-form honesty battery")
    print("=" * 72)
    v = run_closed_forms()
    for k, val in v.items():
        if isinstance(val, dict):
            print(f"  {k}: {json.dumps(val)}")
        else:
            print(f"  {k}: {val:.3e}")
    out['closed_forms'] = v

    print("=" * 72)
    print("K05 ray solver -- grid-convergence ladder (kappa=1, T=1, sphere=1)")
    print("=" * 72)
    cfgs = [
        (80, 48, 12, 24),
        (160, 64, 16, 32),
        (240, 80, 20, 40),
        (320, 96, 24, 48),
    ]
    rows = run_ladder(cfgs)
    out['ladder'] = rows

    # L-truncation ladder at fixed spatial grid
    print("=" * 72)
    print("K05 -- angular truncation ladder at (Nr=160, Nq=80, Nt=32)")
    print("=" * 72)
    rowsL = run_ladder([(160, 80, L, 32) for L in (8, 12, 16, 20, 24)])
    out['ladder_L'] = rowsL

    print("=" * 72)
    print("V4 -- collision-average discretization cross-check "
          "(direct mu-grid quadrature, no Legendre)", flush=True)
    v4 = run_mugrid_crosscheck(160, 64, 32)
    print("  V4:", json.dumps(v4))
    out['V4_mugrid_crosscheck'] = v4

    # ---- target comparison on the finest grid -------------------------
    mc = dict(E_D=0.5008, E_v2=2.8061, E_Dv2=3.7316)
    tol = dict(E_D=0.01*0.5008, E_v2=0.03*2.8061, E_Dv2=0.10*3.7316)
    best = rows[-1]
    E_D, E_v2, E_Dv2 = best['E_D'], best['E_v2'], best['E_Dv2']
    c = {}
    c['S1_E_D_pct'] = 100.0*abs(E_D - mc['E_D'])/mc['E_D']
    c['S2_E_v2_pct'] = 100.0*abs(E_v2 - mc['E_v2'])/mc['E_v2']
    c['S3_E_Dv2_pct'] = 100.0*abs(E_Dv2 - mc['E_Dv2'])/mc['E_Dv2']
    c['S1_pass'] = abs(E_D - mc['E_D']) < tol['E_D']
    c['S2_pass'] = abs(E_v2 - mc['E_v2']) < tol['E_v2']
    c['S3_pass'] = abs(E_Dv2 - mc['E_Dv2']) < tol['E_Dv2']
    c['S5_converged'] = all(r['gaps'][2] < 1e-7 and r['gaps'][0] < 1e-7
                            for r in rows)
    out['targets'] = dict(mc=mc, tol=tol, moments=dict(E_D=E_D, E_v2=E_v2,
                                                       E_Dv2=E_Dv2),
                          pct=dict(E_D=c['S1_E_D_pct'], E_v2=c['S2_E_v2_pct'],
                                   E_Dv2=c['S3_E_Dv2_pct']),
                          checks=c)
    print("=" * 72)
    print(f"finest grid {best['cfg']}:  E[D] = {E_D:.5f} vs {mc['E_D']} "
          f"({c['S1_E_D_pct']:.2f}%)   E[v^2] = {E_v2:.5f} vs {mc['E_v2']} "
          f"({c['S2_E_v2_pct']:.2f}%)   E[Dv^2] = {E_Dv2:.5f} vs "
          f"{mc['E_Dv2']} ({c['S3_E_Dv2_pct']:.2f}%)")
    print("checks:", {k: v for k, v in c.items() if k.endswith('pass')
                      or k.endswith('converged')})
    print(f"total wall {time.time()-t_start:.1f}s")
    out['total_seconds'] = time.time() - t_start
    out['grid_params_finest'] = dict(Nr=best['cfg'][0], Nq=best['cfg'][1],
                                     L=best['cfg'][2], Nt=best['cfg'][3])
    print(json.dumps(out, indent=1))
    with open('K05_results.json', 'w') as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())