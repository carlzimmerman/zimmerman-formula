"""NR-GPP: nonrelativistic two-component Gross-Pitaevskii-Poisson reduction of the
unchanged two-field action (LABELLED leading-order approximation; see PLAN.md 2/N2).

Rotating-frame fields Phi = (f + u1 + i v1) e^{-i mu t}, X = -(x + u2 + i v2) e^{-2 i mu t}
(t-dependence relative to the rest-mass phases e^{-it}, e^{-2it}).
H - mu N = int |grad Phi|^2 + |grad X|^2 + Delta|X|^2 + g(X* Phi^2 + c.c.) + lam|Phi|^4
           - 2 mu (|Phi|^2 + 4|X|^2) - (Gamma/2) int int rho rho'/|x-x'|,
rho = 2(|Phi|^2 + 4|X|^2) (mass = charge density at this order), N = int rho.
Radial functions w(r) = y(r)/r on r_i = i dr (i = 1..N), Dirichlet at 0 and R_box.
Two kinetic discretizations: 'fd' (2nd-order) and 'dvr' (sine-DVR, spectral).
Each l-sector uses the exact multipole kernel r_<^l / r_>^(l+1) / (2l+1) (no Cowling).
Second variation  E2 = <u, L+ u> + <v, L- v>  (Euclidean in y times dr),
dynamics u_t = W^-1 L- v, v_t = -W^-1 L+ u, W = diag(2,4)  =>  sigma^2 = eig(W^-1 L- W^-1 L+).
"""
import argparse, gc, json, math, sys
import numpy as np
import scipy.linalg as la
from common import (DELTA, G_HAT, LAM, peak_rss_mb, Timer, dump)


def kinetic(N, dr, disc):
    if disc == 'fd':
        T = np.zeros((N, N))
        i = np.arange(N)
        T[i, i] = 2.0 / dr ** 2
        T[i[:-1], i[:-1] + 1] = -1.0 / dr ** 2
        T[i[:-1] + 1, i[:-1]] = -1.0 / dr ** 2
        return T
    j = np.arange(1, N + 1)
    S = math.sqrt(2.0 / (N + 1)) * np.sin(np.pi * np.outer(j, j) / (N + 1))
    k = np.pi * j / ((N + 1) * dr)
    return (S * k ** 2) @ S


def kernel(r, l):
    rl = np.minimum.outer(r, r)
    rg = np.maximum.outer(r, r)
    K = (rl / rg) ** l
    K /= rg
    K /= (2 * l + 1)
    return K


class Model:
    def __init__(self, gamma, N, rbox, disc):
        self.G = gamma
        self.N = N
        self.dr = rbox / (N + 1)
        self.r = self.dr * np.arange(1, N + 1)
        self.disc = disc
        self.T = kinetic(N, self.dr, disc)
        self.K0 = kernel(self.r, 0)
        self.c = gamma * 4 * math.pi * self.dr / 2.0

    def potential(self, y1, y2):
        P = 2 * (y1 ** 2 + 4 * y2 ** 2)
        return -self.G * 4 * math.pi * self.dr * (self.K0 @ P)

    def residual(self, y1, y2, mu):
        r = self.r
        f, x = y1 / r, y2 / r
        U = self.potential(y1, y2)
        R1 = self.T @ y1 + (2 * U - 2 * mu - 2 * G_HAT * x + 2 * LAM * f ** 2) * y1
        R2 = self.T @ y2 + (DELTA - 8 * mu + 8 * U) * y2 - G_HAT * f * y1
        return R1, R2, U

    def lplus(self, y1, y2, mu, U, l, K=None):
        N, r = self.N, self.r
        f, x = y1 / r, y2 / r
        Tl = self.T + np.diag(l * (l + 1) / r ** 2) if l else self.T
        K = self.K0 if (K is None and l == 0) else (kernel(r, l) if K is None else K)
        a1, a2 = 4 * y1, 16 * y2
        L = np.empty((2 * N, 2 * N))
        L[:N, :N] = Tl - self.c * (a1[:, None] * K * a1[None, :])
        L[:N, N:] = -self.c * (a1[:, None] * K * a2[None, :])
        L[N:, N:] = Tl - self.c * (a2[:, None] * K * a2[None, :])
        L[N:, :N] = L[:N, N:].T
        idx = np.arange(N)
        L[idx, idx] += 2 * U - 2 * mu - 2 * G_HAT * x + 6 * LAM * f ** 2
        L[idx, N + idx] += -2 * G_HAT * f
        L[N + idx, idx] += -2 * G_HAT * f
        L[N + idx, N + idx] += DELTA - 8 * mu + 8 * U
        return L

    def lminus(self, y1, y2, mu, U, l):
        N, r = self.N, self.r
        f, x = y1 / r, y2 / r
        Tl = self.T + np.diag(l * (l + 1) / r ** 2) if l else self.T
        L = np.zeros((2 * N, 2 * N))
        L[:N, :N] = Tl
        L[N:, N:] = Tl
        idx = np.arange(N)
        L[idx, idx] += 2 * U - 2 * mu + 2 * G_HAT * x + 2 * LAM * f ** 2
        L[idx, N + idx] += -2 * G_HAT * f
        L[N + idx, idx] += -2 * G_HAT * f
        L[N + idx, N + idx] += DELTA - 8 * mu + 8 * U
        return L

    def gravity_matrix(self, y1, y2, l):
        N = self.N
        K = kernel(self.r, l)
        a = np.concatenate([4 * y1, 16 * y2])
        Kb = np.block([[K, K], [K, K]])
        return -self.c * (a[:, None] * Kb * a[None, :])

    def solve(self, y1, y2, mu, center, value, tol=1e-13, maxit=60, log=None):
        """Newton for discrete E-L equations + linear central-amplitude constraint.
        center='f' fixes (8 y1_1 - y1_2)/(6 dr) = value; 'x' the same for y2."""
        N, dr = self.N, self.dr
        crow = np.zeros(2 * N)
        off = 0 if center == 'f' else N
        crow[off] = 8 / (6 * dr)
        crow[off + 1] = -1 / (6 * dr)
        hist = []
        for it in range(maxit):
            R1, R2, U = self.residual(y1, y2, mu)
            Rc = crow @ np.concatenate([y1, y2]) - value
            scale = np.linalg.norm(self.T @ y1) + np.linalg.norm(self.T @ y2) + \
                np.linalg.norm((2 * U - 2 * mu) * y1) + 1e-300
            rel = math.hypot(np.linalg.norm(R1), np.linalg.norm(R2)) / scale
            hist.append(dict(it=it, rel=rel, mu=mu, center_res=float(Rc)))
            if log:
                print(json.dumps(hist[-1]), file=log, flush=True)
            if rel < tol and abs(Rc) < 1e-14 * abs(value):
                break
            J = np.zeros((2 * N + 1, 2 * N + 1))
            J[:2 * N, :2 * N] = self.lplus(y1, y2, mu, U, 0)
            J[:N, -1] = -2 * y1
            J[N:2 * N, -1] = -8 * y2
            J[-1, :2 * N] = crow
            rhs = -np.concatenate([R1, R2, [Rc]])
            d = la.solve(J, rhs, check_finite=False)
            del J
            step = 1.0
            for _ in range(30):
                ny1, ny2, nmu = y1 + step * d[:N], y2 + step * d[N:2 * N], mu + step * d[-1]
                nR1, nR2, nU = self.residual(ny1, ny2, nmu)
                nrel = math.hypot(np.linalg.norm(nR1), np.linalg.norm(nR2)) / scale
                if nrel < rel or step < 1e-6 or rel < 1e-10:
                    break
                step *= 0.5
            y1, y2, mu = ny1, ny2, nmu
        return y1, y2, mu, hist


def householder_complement(A, z):
    """Return E^T A E where E = columns 2.. of the Householder reflector mapping z -> e1."""
    z = z / np.linalg.norm(z)
    v = z.copy()
    v[0] += math.copysign(1.0, z[0])
    v /= np.linalg.norm(v)
    Av = A @ v
    vAv = v @ Av
    # in place: A <- H A H with H = I - 2 v v^T (A is consumed)
    w = Av - vAv * v
    A -= 2 * np.outer(v, w)
    A -= 2 * np.outer(w, v)
    return np.ascontiguousarray(A[1:, 1:])


def observables(m, y1, y2, mu):
    r, dr = m.r, m.dr
    f, x = y1 / r, y2 / r
    P = 2 * (y1 ** 2 + 4 * y2 ** 2)
    Ncharge = 4 * math.pi * dr * P.sum()
    cum = np.cumsum(P) / P.sum()
    R99 = float(np.interp(0.99, cum, r))
    fc = (8 * y1[0] - y1[1]) / (6 * dr)
    xc = (8 * y2[0] - y2[1]) / (6 * dr)
    occ = f > 1e-12 * abs(fc)
    occx = x > 1e-12 * abs(xc)
    df, dx = np.diff(f), np.diff(x)
    h1 = dict(f_positive=bool(np.all(f[occ] > 0)), x_positive=bool(np.all(x[occx] > 0)),
              f_min=float(f.min()), x_min=float(x.min()),
              f_decreasing=bool(np.all(df[occ[:-1]] < 0)), x_decreasing=bool(np.all(dx[occx[:-1]] < 0)),
              max_df_occupied=float(df[occ[:-1]].max()), max_dx_occupied=float(dx[occx[:-1]].max()),
              occupied_radius_f=float(r[occ].max()), occupied_radius_x=float(r[occx].max()),
              f_at_box_over_fc=float(f[-1] / fc), x_at_box_over_xc=float(x[-1] / xc))
    U = m.potential(y1, y2)
    return dict(N_charge=Ncharge, mu=mu, omega_equiv=1 + mu, f_c=fc, x_c=xc,
                q_c=2 * (fc ** 2 + 4 * xc ** 2), R99=R99, U_center=float(U[0]),
                GM_over_R99=m.G * Ncharge / R99, H1=h1)


def bdg_sector(m, y1, y2, mu, U, l, nev=6):
    N = m.N
    w = np.sqrt(np.concatenate([np.full(N, 2.0), np.full(N, 4.0)]))
    out = dict(l=l)
    K = kernel(m.r, l)
    Lp = m.lplus(y1, y2, mu, U, l, K=K)
    del K
    Lp /= w[:, None]
    Lp /= w[None, :]          # S+
    Lm = m.lminus(y1, y2, mu, U, l)
    Lm /= w[:, None]
    Lm /= w[None, :]          # S-
    ev_p = la.eigh(Lp, eigvals_only=True, subset_by_index=[0, nev - 1], driver='evr')
    ev_m = la.eigh(Lm, eigvals_only=True, subset_by_index=[0, nev - 1], driver='evr')
    out['Splus_lowest'] = ev_p.tolist()
    out['Sminus_lowest'] = ev_m.tolist()
    out['Splus_negative_count'] = int(np.sum(la.eigh(Lp, eigvals_only=True, subset_by_value=[-np.inf, 0.0], driver='evr') < 0))
    if l == 0:
        zeta = w * np.concatenate([y1, 2 * y2])
        Smz = Lm @ zeta
        out['phase_kernel_rel_residual'] = float(np.linalg.norm(Smz) / (np.linalg.norm(zeta) * abs(la.eigh(Lm, eigvals_only=True, subset_by_index=[2 * N - 1, 2 * N - 1])[0])))
        Lp = householder_complement(Lp, zeta)
        Lm = householder_complement(Lm, zeta)
        gc.collect()
        out['Splus_constrained_lowest'] = la.eigh(Lp, eigvals_only=True, subset_by_index=[0, nev - 1], driver='evr').tolist()
        out['Sminus_quotient_lowest'] = la.eigh(Lm, eigvals_only=True, subset_by_index=[0, nev - 1], driver='evr').tolist()
    if l == 1:
        vals, vecs = la.eigh(Lp, subset_by_index=[0, 1], driver='evr')
        f, x = y1 / m.r, y2 / m.r
        tr = np.concatenate([m.r * np.gradient(f, m.r), m.r * np.gradient(x, m.r)]) * w
        out['translation_overlap'] = float(abs(vecs[:, 0] @ tr) / np.linalg.norm(tr))
        out['translation_eig_over_next'] = float(vals[0] / vals[1])
    C = la.cholesky(Lm, lower=True, check_finite=False)
    del Lm
    gc.collect()
    A = C.T @ Lp @ C
    del Lp, C
    gc.collect()
    s2 = la.eigh(A, eigvals_only=True, subset_by_index=[0, nev - 1], driver='evr')
    del A
    gc.collect()
    out['sigma2_lowest'] = s2.tolist()
    out['sigma_lowest'] = [float(math.copysign(math.sqrt(abs(s)), s)) for s in s2]
    return out


def coercivity(m, y1, y2, mu, U):
    r = m.r
    f, x = y1 / r, y2 / r
    A11 = 2 * U - 2 * mu - 2 * G_HAT * x + 6 * LAM * f ** 2
    A12 = -2 * G_HAT * f
    A22 = DELTA - 8 * mu + 8 * U
    lam_min = 0.5 * (A11 + A22) - np.sqrt(0.25 * (A11 - A22) ** 2 + A12 ** 2)
    Gm = m.gravity_matrix(y1, y2, 0)
    gnorm = -la.eigh(Gm, eigvals_only=True, subset_by_index=[0, 0])[0]
    del Gm
    vneg = max(0.0, -lam_min.min()) + gnorm
    return dict(local_min_eig=float(lam_min.min()), gravity_opnorm_l0=float(gnorm),
                k_negative_bound=math.sqrt(vneg), k_max_resolved=math.pi / m.dr,
                note='<u,L+u> >= <u,-lap u> - (|min local eig| + ||K_0||)|u|^2 and ||K_l||<=||K_0||; '
                     'a negative direction needs kinetic wavenumber below k_negative_bound')


def load_seed(path, gamma, seed_gamma, r):
    d = np.load(path)
    rs = np.asarray(d['r'], float)
    if seed_gamma is not None:
        rs = rs * math.sqrt(seed_gamma / gamma)
    f = np.asarray(d['f'], float)
    x = np.asarray(d['x'] if 'x' in d.files else d['h'], float)
    if 'mu' in d.files:
        mu = float(d['mu'])
    else:
        mu = float(d['omega']) - 1.0
    fi = np.interp(r, rs, f, right=0.0)
    xi = np.interp(r, rs, x, right=0.0)
    return fi * r, xi * r, mu


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--gamma', type=float, required=True)
    p.add_argument('--N', type=int, required=True)
    p.add_argument('--rbox', type=float, required=True)
    p.add_argument('--disc', choices=['fd', 'dvr'], default='fd')
    p.add_argument('--center', choices=['f', 'x'], default='f')
    p.add_argument('--value', type=float, required=True)
    p.add_argument('--seed', required=True)
    p.add_argument('--seed-gamma', type=float)
    p.add_argument('--ls', default='0,1,2,3,4')
    p.add_argument('--vk', action='store_true')
    p.add_argument('--coercivity', action='store_true')
    p.add_argument('--out', required=True)
    a = p.parse_args()
    tm = Timer()
    m = Model(a.gamma, a.N, a.rbox, a.disc)
    y1, y2, mu = load_seed(a.seed, a.gamma, a.seed_gamma, m.r)
    log = open(a.out + '.log', 'w')
    y1, y2, mu, hist = m.solve(y1, y2, mu, a.center, a.value, log=log)
    R1, R2, U = m.residual(y1, y2, mu)
    rec = dict(model='NR-GPP (leading-order Newtonian reduction; labelled approximation)',
               gamma=a.gamma, N=a.N, rbox=a.rbox, dr=m.dr, disc=a.disc, center=a.center,
               center_value=a.value, newton=hist[-1], newton_iterations=len(hist))
    rec['background'] = observables(m, y1, y2, mu)
    rec['background']['threshold_sigma_Phi'] = -mu
    rec['background']['threshold_sigma_X'] = DELTA / 4 - 2 * mu
    np.savez(a.out + '_bg.npz', r=m.r, f=y1 / m.r, x=y2 / m.r, U=U, mu=mu, gamma=a.gamma)
    if a.vk:
        vk = []
        for s in (-1, 1):
            v = a.value * (1 + s * 1e-3)
            z1, z2, zmu, h = m.solve(y1.copy(), y2.copy(), mu, a.center, v)
            P = 2 * (z1 ** 2 + 4 * z2 ** 2)
            vk.append(dict(value=v, mu=zmu, N_charge=4 * math.pi * m.dr * P.sum(), rel=h[-1]['rel']))
        rec['vakhitov_kolokolov'] = dict(points=vk, dN_dmu=(vk[1]['N_charge'] - vk[0]['N_charge']) / (vk[1]['mu'] - vk[0]['mu']),
                                         criterion='radial ground-state stability iff n(L+^(0))=1 and dN/dmu<0 (mu<0 convention)')
    if a.coercivity:
        rec['coercivity'] = coercivity(m, y1, y2, mu, U)
    rec['sectors'] = []
    for l in [int(s) for s in a.ls.split(',') if s != '']:
        sec = bdg_sector(m, y1, y2, mu, U, l)
        sec['s2_natural'] = [s / (4 * math.pi * a.gamma * rec['background']['q_c']) for s in sec['sigma2_lowest']]
        rec['sectors'].append(sec)
        print(json.dumps(dict(l=l, sigma2=sec['sigma2_lowest'][:3], Splus=sec['Splus_lowest'][:2])), file=log, flush=True)
        gc.collect()
    rec['runtime_s'] = tm()
    rec['peak_rss_MB'] = peak_rss_mb()
    dump(a.out + '.json', rec)
    log.close()
    print(json.dumps(dict(out=a.out, runtime=rec['runtime_s'], rss=rec['peak_rss_MB'])))


if __name__ == '__main__':
    main()
