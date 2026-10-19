"""Gamma -> 0 limit of the fixed-f_c branch (PLAN C2 and C4).

C2  GR TF limit: TOV in z = sqrt(Gamma) r with the algebraic two-field TF EOS
    (gradients dropped; exact leading order of the z-scaled full equations as Gamma -> 0).
C4  Newtonian TF star + irrotational barotropic hydrodynamic modes (single superfluid:
    relative phase and composition locked by conversion; full linearized Poisson):
      delta q_t = -div(q grad theta),  theta_t = -(e''(q) delta q + delta U),
      lap delta U = 4 pi delta q (z units)  =>  sigma^2/Gamma = eig(A B).
    Finite-volume, cell-centred; A from faces (q -> 0 at the TF surface: natural BC).
    l = 0 is restricted to fixed mass and quotiented by the constant-phase mode.
The TF EOS at local d = Omega^2 - 1 (GR) or d = 2(mu - U) (NR):
  n = f^2 = d D/(2A), h = g n/D, D = Delta - 4d, A = lam D - g^2;  q = 2(n + 4h^2) (NR),
  GR: T = (1+d)(n+4h^2), p = n d/2, e = 2T - p, charge density 2 sqrt(1+d)(n+4h^2).
"""
import json, math, sys
import numpy as np
import scipy.linalg as la
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from common import (DELTA, G_HAT, LAM, ZETA, FC_BENCH, tf_point, dump, peak_rss_mb, Timer)


def nh_of_d(d):
    D = DELTA - 4 * d
    A = LAM * D - G_HAT ** 2
    n = d * D / (2 * A)
    h = G_HAT * n / D
    return n, h


def dq_dd(d, eps=1e-9):
    def q(dd):
        n, h = nh_of_d(dd)
        return 2 * (n + 4 * h * h)
    return (q(d + eps * ZETA) - q(d - eps * ZETA)) / (2 * eps * ZETA)


def d_center_from_fc(fc):
    return brentq(lambda d: nh_of_d(d)[0] - fc * fc, 1e-14, ZETA * 0.999999, xtol=1e-18, rtol=1e-15)


# ---------------------------------------------------------------- C2: GR TOV + TF EOS
def gr_tf(dc):
    def eos(d):
        if d <= 0:
            return 0.0, 0.0, 0.0
        n, h = nh_of_d(d)
        S = n + 4 * h * h
        T = (1 + d) * S
        p = 0.5 * n * d
        return p, 2 * T - p, 2 * math.sqrt(1 + d) * S
    Hc = 0.5 * math.log1p(dc)        # H = ln Omega, d = e^{2H} - 1

    def rhs(z, y):
        v, H, Qs = y
        d = math.expm1(2 * H)
        p, e, q = eos(d)
        N = 1 - 2 * v / z
        return [4 * math.pi * z * z * e, -(v / z ** 2 + 4 * math.pi * z * p) / N, 4 * math.pi * z * z * q / math.sqrt(N)]

    def surf(z, y):
        return y[1]
    surf.terminal = True
    surf.direction = -1
    z0 = 1e-8
    p0, e0, q0 = eos(dc)
    sol = solve_ivp(rhs, (z0, 5.0), [4 * math.pi * e0 * z0 ** 3 / 3, Hc, 4 * math.pi * q0 * z0 ** 3 / 3],
                    method='DOP853', rtol=1e-12, atol=1e-16, events=surf, dense_output=True, max_step=1e-3)
    zs = float(sol.t_events[0][0])
    vs, _, Qs = sol.y_events[0][0]
    z99 = brentq(lambda z: sol.sol(z)[0] - 0.99 * vs, z0, zs, xtol=1e-15)
    w = math.sqrt(1 - 2 * vs / zs)
    alpha_c = w / math.sqrt(1 + dc)
    return dict(d_c=dc, x_c=dc / ZETA, z_surface=zs, v_ADM=float(vs), Q_scaled=float(Qs), z99=float(z99),
                C99=float(vs / z99), C_surface=float(vs / zs), omega=w, one_minus_omega=1 - w,
                alpha_center=alpha_c, Omega_center=math.sqrt(1 + dc))


# ---------------------------------------------------------------- C4: Newtonian TF + hydro
def nr_tf(dc):
    def rhs(z, y):
        d, dp = y
        n, h = nh_of_d(max(d, 0.0))
        q = 2 * (n + 4 * h * h)
        return [dp, -8 * math.pi * q - 2 * dp / z]

    def surf(z, y):
        return y[0]
    surf.terminal = True
    surf.direction = -1
    z0 = 1e-8
    n0, h0 = nh_of_d(dc)
    q0 = 2 * (n0 + 4 * h0 * h0)
    y0 = [dc - 8 * math.pi * q0 * z0 ** 2 / 6, -8 * math.pi * q0 * z0 / 3]
    sol = solve_ivp(rhs, (z0, 5.0), y0, method='DOP853', rtol=1e-13, atol=1e-18, events=surf, dense_output=True, max_step=1e-3)
    zs = float(sol.t_events[0][0])
    return sol, zs, q0


def hydro_modes(dc, Ncell, ls, nev=5):
    sol, zs, qc = nr_tf(dc)
    hz = zs / Ncell
    zc = (np.arange(Ncell) + 0.5) * hz
    zf = np.arange(1, Ncell + 1) * hz          # faces (last = surface)
    dcell = sol.sol(zc)[0]
    dface = np.array([sol.sol(z)[0] if z < zs else 0.0 for z in zf])
    def qof(d):
        n, h = nh_of_d(np.maximum(d, 0.0))
        return 2 * (n + 4 * h * h)
    qcell, qface = qof(dcell), qof(dface)
    qface[-1] = 0.0
    epp = 0.5 / np.array([dq_dd(d) for d in dcell])
    w = zc ** 2 * hz                            # cell weights (int z^2 dz)
    mass = 4 * math.pi * np.sum(w * qcell)
    res = dict(N_cells=Ncell, z_surface=zs, q_center=qc, mass_scaled=mass, sectors=[])
    sq = np.sqrt(w)
    for l in ls:
        # A: <th, A th> = sum_faces q_f z_f^2 (dth/dz)^2 hz + sum_c q_c l(l+1) th^2 hz
        A = np.zeros((Ncell, Ncell))
        for i in range(Ncell - 1):
            c = qface[i] * zf[i] ** 2 / hz
            A[i, i] += c
            A[i + 1, i + 1] += c
            A[i, i + 1] -= c
            A[i + 1, i] -= c
        A[np.arange(Ncell), np.arange(Ncell)] += qcell * l * (l + 1) * hz
        zl = np.minimum.outer(zc, zc)
        zg = np.maximum.outer(zc, zc)
        Kl = (zl / zg) ** l / zg * (4 * math.pi / (2 * l + 1))
        B = np.diag(epp * w) - (w[:, None] * Kl * w[None, :])
        SA = A / sq[:, None] / sq[None, :]
        SB = B / sq[:, None] / sq[None, :]
        sec = dict(l=l)
        sec['B_lowest'] = la.eigh(SB, eigvals_only=True, subset_by_index=[0, nev - 1]).tolist()
        if l == 0:
            zeta = sq / np.linalg.norm(sq)
            v = zeta.copy(); v[0] += 1.0; v /= np.linalg.norm(v)
            def red(M):
                Mv = M @ v; vMv = v @ Mv; ww = Mv - vMv * v
                M2_ = M - 2 * np.outer(v, ww) - 2 * np.outer(ww, v)
                return M2_[1:, 1:]
            SA, SB = red(SA), red(SB)
            sec['B_constrained_lowest'] = la.eigh(SB, eigvals_only=True, subset_by_index=[0, nev - 1]).tolist()
        C = la.cholesky(SA, lower=True)
        s2 = la.eigh(C.T @ SB @ C, eigvals_only=True, subset_by_index=[0, nev - 1])
        sec['sigma2_over_Gamma'] = s2.tolist()
        sec['s2_natural'] = (s2 / (4 * math.pi * qc)).tolist()
        res['sectors'].append(sec)
    return res


def main():
    out = sys.argv[1]
    tm = Timer()
    fc = FC_BENCH
    dc = d_center_from_fc(fc)
    rec = dict(branch=dict(f_c=fc, d_c=dc, x_c=dc / ZETA, h_c=nh_of_d(dc)[1]))
    rec['GR_TF_limit'] = gr_tf(dc)
    sol, zs, qc = nr_tf(dc)
    rec['NR_TF_limit'] = dict(z_surface=zs, q_center=qc,
                              mu=float(sol.sol(zs)[0] * 0 + 0.0))
    # NR chemical potential: d = 2(mu - U), U(zs) = -M/zs  =>  mu = U(zs) (d=0 at surface)
    zz = np.linspace(1e-8, zs, 200001)
    dd = sol.sol(zz)[0]
    n, h = nh_of_d(np.maximum(dd, 0))
    q = 2 * (n + 4 * h * h)
    Ms = np.trapz(4 * math.pi * zz ** 2 * q, zz)
    rec['NR_TF_limit'].update(mass_scaled=float(Ms), mu=float(-Ms / zs),
                              z99=float(np.interp(0.99, np.cumsum(zz ** 2 * q) / np.sum(zz ** 2 * q), zz)))
    rec['hydro'] = [hydro_modes(dc, Nc, [0, 1, 2, 3, 4]) for Nc in (400, 800, 1600)]
    rec['runtime_s'] = tm()
    rec['peak_rss_MB'] = peak_rss_mb()
    dump(out, rec)
    print(json.dumps(rec['GR_TF_limit']))
    for H in rec['hydro']:
        print(H['N_cells'], [(s['l'], s['s2_natural'][:2]) for s in H['sectors']])


if __name__ == '__main__':
    main()
