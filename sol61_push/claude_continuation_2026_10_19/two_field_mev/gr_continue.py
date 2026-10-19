"""Full-GR static two-field BVP, continued in Gamma at fixed central f (PLAN C1).

Independent re-implementation of the polar-areal equations of
full_two_field_2026_10_19/equilibria/DERIVATION.txt in z = sqrt(Gamma) r, v = Gamma^(3/2) M_enc,
b = ln alpha:  states (f, f_z, h, h_z, v, b), eigenparameter omega (logit).
Center: regular Taylor start at z0 with f(z0) = f_c + f2 z0^2/2. Outer (Z): f = h = 0,
alpha = sqrt(1 - 2v/Z) (vacuum Schwarzschild normalization; finite-box tail truncation).
Independent checks: (i) KG residuals in the ORIGINAL r-form recomputed by 4th-order finite
differences of the interpolated solution on a dense grid; (ii) Hamiltonian-constraint
residual; (iii) charge/mass by Simpson quadrature on a separate dense grid.
"""
import argparse, json, math
import numpy as np
from scipy.integrate import solve_bvp, cumulative_trapezoid, simpson
from scipy.optimize import brentq
from scipy.special import expit
from common import M2, G_HAT, LAM, FC_BENCH, dump, peak_rss_mb, Timer


def make(G, fc, z0):
    def rhs(z, y, p):
        f, fz, h, hz, v, b = y
        w = expit(p[0])
        N = 1 - 2 * v / z
        a2 = np.exp(2 * b)
        S = f * f + 4 * h * h
        V = f * f + M2 * h * h - 2 * G_HAT * h * f * f + LAM * f ** 4
        K = G * N * (fz * fz + hz * hz)
        T = w * w * S / a2
        e, pr = T + K + V, T + K - V
        vz = 4 * math.pi * z * z * e
        bz = (v / z ** 2 + 4 * math.pi * z * pr) / N
        az = (vz / z - v / z ** 2) / N          # (ln a)_z with a = N^-1/2
        B = 2 / z + bz - az
        fzz = -B * fz + ((1 - w * w / a2) * f - 2 * G_HAT * h * f + 2 * LAM * f ** 3) / (G * N)
        hzz = -B * hz + ((M2 - 4 * w * w / a2) * h - G_HAT * f * f) / (G * N)
        return np.vstack([fz, fzz, hz, hzz, vz, bz])

    def bc(ya, yb, p):
        w = expit(p[0])
        f, h, b = ya[0], ya[2], ya[5]
        a2 = math.exp(2 * b)
        S = f * f + 4 * h * h
        V = f * f + M2 * h * h - 2 * G_HAT * h * f * f + LAM * f ** 4
        e0 = w * w * S / a2 + V
        f2 = ((1 - w * w / a2) * f - 2 * G_HAT * h * f + 2 * LAM * f ** 3) / (3 * G)
        h2 = ((M2 - 4 * w * w / a2) * h - G_HAT * f * f) / (3 * G)
        Z = yb_z[0]
        return np.array([f - 0.5 * z0 * z0 * f2 - fc, ya[1] - z0 * f2, ya[3] - z0 * h2,
                         ya[4] - 4 * math.pi * e0 * z0 ** 3 / 3, yb[0], yb[2],
                         yb[5] - 0.5 * math.log(1 - 2 * yb[4] / Z)])
    yb_z = [1.0]
    return rhs, bc, yb_z


def fd4_second(y, x):
    """4th-order second derivative on a uniform grid (interior points)."""
    hx = x[1] - x[0]
    d2 = np.full_like(y, np.nan)
    d2[2:-2] = (-y[4:] + 16 * y[3:-1] - 30 * y[2:-2] + 16 * y[1:-3] - y[:-4]) / (12 * hx * hx)
    return d2


def fd4_first(y, x):
    hx = x[1] - x[0]
    d1 = np.full_like(y, np.nan)
    d1[2:-2] = (-y[4:] + 8 * y[3:-1] - 8 * y[1:-3] + y[:-4]) / (12 * hx)
    return d1


def independent_checks(sol, G, w, fc, Zbox):
    out = {}
    # dense uniform grid in z over the occupied region and edge
    zz = np.linspace(sol.x[0], Zbox, 400001)
    f, fz, h, hz, v, b = sol.sol(zz)
    alpha = np.exp(b)
    N = 1 - 2 * v / zz
    # r-form quantities (r = z/sqrt(G)); use z derivatives of the interpolated f (not f_z state)
    fzz_fd = fd4_second(f, zz)
    hzz_fd = fd4_second(h, zz)
    fz_fd = fd4_first(f, zz)
    hz_fd = fd4_first(h, zz)
    Om2 = w * w / alpha ** 2
    S = f * f + 4 * h * h
    V = f * f + M2 * h * h - 2 * G_HAT * h * f * f + LAM * f ** 4
    K = G * N * (fz_fd ** 2 + hz_fd ** 2)
    e, pr = Om2 * S + K + V, Om2 * S + K - V
    bz = (v / zz ** 2 + 4 * math.pi * zz * pr) / N
    Nz = np.gradient(N, zz)
    B = 2 / zz + bz + Nz / (2 * N)
    Ff = G * N * (fzz_fd + B * fz_fd)
    Rf = (1 - Om2) * f - 2 * G_HAT * h * f + 2 * LAM * f ** 3
    Fh = G * N * (hzz_fd + B * hz_fd)
    Rh = (M2 - 4 * Om2) * h - G_HAT * f * f
    sel = (np.arange(zz.size) > 3) & (np.arange(zz.size) < zz.size - 4) & (f > 1e-6 * fc)
    scale_f = np.max(np.abs(Rf[sel])) + np.max(np.abs(Ff[sel]))
    scale_h = np.max(np.abs(Rh[sel])) + np.max(np.abs(Fh[sel]))
    out['KG_f_rel_residual_max'] = float(np.max(np.abs(Ff[sel] - Rf[sel])) / scale_f)
    out['KG_h_rel_residual_max'] = float(np.max(np.abs(Fh[sel] - Rh[sel])) / scale_h)
    vz_fd = fd4_first(v, zz)
    selv = np.isfinite(vz_fd) & (zz > zz[10])
    out['mass_constraint_rel_residual_max'] = float(np.max(np.abs(vz_fd[selv] - 4 * math.pi * zz[selv] ** 2 * e[selv])) / np.max(4 * math.pi * zz[selv] ** 2 * e[selv]))
    q = 2 * w * S / alpha
    Qs = simpson(4 * math.pi * zz ** 2 * q / np.sqrt(N), x=zz) / G ** 1.5
    e_state = Om2 * S + G * N * (fz ** 2 + hz ** 2) + V      # uses the state derivatives (finite at the ends)
    Ms = simpson(4 * math.pi * zz ** 2 * e_state, x=zz) / G ** 1.5
    out['Q_simpson'] = float(Qs)
    out['M_simpson'] = float(Ms)
    return out


def observables(sol, G, fc, Zbox, z0):
    w = float(expit(sol.p[0]))
    zz = np.linspace(z0, Zbox, 200001)
    f, fz, h, hz, v, b = sol.sol(zz)
    alpha = np.exp(b)
    N = 1 - 2 * v / zz
    q = 2 * w * (f * f + 4 * h * h) / alpha
    Q = cumulative_trapezoid(4 * math.pi * zz * zz * q / np.sqrt(N), zz, initial=0)
    vZ = float(sol.sol(Zbox)[4])
    z99 = brentq(lambda s: float(sol.sol(s)[4]) - 0.99 * vZ, z0, Zbox, xtol=1e-14)
    def zlevel(level):
        idx = np.where(f * f > level * fc * fc)[0]
        i = idx[-1]
        return float(np.interp(level * fc * fc, [f[i + 1] ** 2, f[i] ** 2], [zz[i + 1], zz[i]]))
    return dict(G=G, omega=w, one_minus_omega=1 - w, alpha_center=float(alpha[0]), Omega_center=w / float(alpha[0]),
                f_center=float(f[0]), h_center=float(h[0]), v_ADM=vZ, M_ADM=vZ / G ** 1.5,
                Q=float(Q[-1]) / G ** 1.5, Q_scaled=float(Q[-1]), mass_over_mQ=vZ / float(Q[-1]),
                z99=z99, R99=z99 / math.sqrt(G), C99=vZ / z99, min_N=float(N.min()),
                max_2Gm_over_r=float(np.max(2 * v[1:] / zz[1:])),
                z_f2_1e_2=zlevel(1e-2), z_f2_1e_4=zlevel(1e-4), z_f2_1e_6=zlevel(1e-6),
                f_min=float(f.min()), h_min=float(h.min()),
                f_monotone=bool(np.all(np.diff(f[f > 1e-10 * fc]) < 0)),
                h_monotone=bool(np.all(np.diff(h[h > 1e-10 * float(h[0])]) < 0)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--gammas', required=True, help='comma list, decreasing')
    p.add_argument('--seed', required=True)
    p.add_argument('--fc', type=float, default=FC_BENCH)
    p.add_argument('--Z', type=float, default=1.0)
    p.add_argument('--z0', type=float, default=1e-6)
    p.add_argument('--tol', type=float, default=1e-7)
    p.add_argument('--max-nodes', type=int, default=60000)   # memory cap (~1.2 GB)
    p.add_argument('--out', required=True)
    a = p.parse_args()
    d = np.load(a.seed)
    if 'collocation_z' in d.files:
        xs = np.asarray(d['collocation_z'], float)
        ys = np.asarray(d['collocation_y'], float)
    else:   # saved dense profile (the benchmark NPZ stores the solution on a uniform z grid)
        xs = np.asarray(d['z'], float)
        ys = np.vstack([np.asarray(d[k], float) for k in ('f', 'fz', 'h', 'hz', 'v', 'b')])
    pars = np.array([float(d['logit_w'])])
    records = []
    for gs in a.gammas.split(','):
        G = float(gs)
        tm = Timer()
        rhs, bc, ybz = make(G, a.fc, a.z0)
        ybz[0] = a.Z
        sol = solve_bvp(rhs, bc, xs, ys, p=pars, tol=a.tol, max_nodes=a.max_nodes, verbose=0)
        rec = dict(G=G, status=int(sol.status), message=sol.message, nodes=int(len(sol.x)),
                   max_rms_residual=float(np.max(sol.rms_residuals)),
                   bc_max=float(np.max(np.abs(bc(sol.y[:, 0], sol.y[:, -1], sol.p)))))
        if sol.success:
            rec.update(observables(sol, G, a.fc, a.Z, a.z0))
            rec['independent'] = independent_checks(sol, G, rec['omega'], a.fc, a.Z)
            rec['Q_quadrature_rel_diff'] = abs(rec['independent']['Q_simpson'] / rec['Q'] - 1)
            rec['M_quadrature_rel_diff'] = abs(rec['independent']['M_simpson'] / rec['M_ADM'] - 1)
            tag = f"{a.out}_G{G:.3e}"
            zz = np.linspace(a.z0, a.Z, 20001)
            Y = sol.sol(zz)
            np.savez(tag + '.npz', z=zz, r=zz / math.sqrt(G), f=Y[0], fz=Y[1], h=Y[2], hz=Y[3], v=Y[4], b=Y[5],
                     alpha=np.exp(Y[5]), a=1 / np.sqrt(1 - 2 * Y[4] / zz), omega=rec['omega'], G=G,
                     m=1.0, lambda_total=LAM, g=G_HAT, M=math.sqrt(M2), logit_w=sol.p[0],
                     collocation_z=sol.x, collocation_y=sol.y, fp=math.sqrt(G) * Y[1], hp=math.sqrt(G) * Y[3])
            xs, ys, pars = sol.x, sol.y, sol.p
        rec['runtime_s'] = tm()
        rec['peak_rss_MB'] = peak_rss_mb()
        records.append(rec)
        dump(a.out + '.json', records)
        print(json.dumps({k: rec.get(k) for k in ('G', 'status', 'nodes', 'max_rms_residual', 'omega', 'C99', 'runtime_s', 'peak_rss_MB')}), flush=True)
        if not sol.success:
            break


if __name__ == '__main__':
    main()
