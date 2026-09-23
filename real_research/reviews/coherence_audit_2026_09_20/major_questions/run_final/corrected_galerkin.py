"""Isolated N04c repair: contraction, convection sign, matching diagnostic.
Derived from the pinned original; benchmark returns states for audit.
No claim of continuum regularity or numerical convergence in N.
"""
import numpy as np
import time

def galerkin(n, nu, c_d, a0cap, A, T, dt, seed=7, every=25, track_g29=False, tag='run'):
    """Run one dealiased Galerkin case; return recorded histories + checks.

    Copied machinery from N04b_equilibrium.galerkin (no import): spectral
    (u.grad)u with 2/3-dealiasing, RK4, div projection, forcing A*s with
    sup|s| = 1 on low modes, exact real-space per-volume means for energy
    and enstrophy (raw rfftn spectral sums carry a time-dependent ~N^3
    plane-pairing bias), snapshots every `every` steps.

    track_g29: additionally record E = 0.5<|u|^2>, Z = <|grad u|^2>,
    Pf = <f.u> and Pd = <u.d> (drag power) real-space volume means for the
    discrete energy-identity check (dE/dt = -nu*Z + <f,u> + <u.d>).

    Returns also 'cfl': max over the run of |u|_oo * dt * k_max with
    k_max = (2/3)(n/2) (the dealiased cutoff).
    """
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)
    k1 = np.fft.fftfreq(n) * n
    (K1, K2, K3) = np.meshgrid(k1, k1, k1[:n // 2 + 1], indexing='ij')
    Ksq = K1 * K1 + K2 * K2 + K3 * K3
    Ksq[0, 0, 0] = 1.0
    kmax_dealias = 2.0 / 3.0 * (n / 2.0)
    MASK = (Ksq <= kmax_dealias ** 2).astype(float)

    def proj(uh):
        uh = uh * MASK
        kdot = (K1 * uh[0] + K2 * uh[1] + K3 * uh[2]) / Ksq
        uh = uh - np.stack([kdot * K1, kdot * K2, kdot * K3])
        for i in range(3):
            uh[i, 0, 0, 0] = 0.0
        return uh

    def to_real(uh):
        return np.stack([np.fft.irfftn(uh[i], s=(n, n, n), axes=(0, 1, 2)) for i in range(3)])

    def nlin(uh):
        ug = to_real(uh)
        waves = (K1, K2, K3)
        D = [[np.fft.irfftn(1j * waves[j] * uh[i], s=(n, n, n), axes=(0, 1, 2)) for i in range(3)] for j in range(3)]
        conv = [sum((ug[j] * D[j][i] for j in range(3))) for i in range(3)]
        return np.stack([np.fft.rfftn(c, axes=(0, 1, 2)) for c in conv])

    def nlin_real_derivs(uh):
        """Return (conv, ug, derivs): conv = (u.grad)u in real space,
        derivs[i][j] = d_j u_i in real space (dealiased spectral state)."""
        ug = to_real(uh)
        derivs = [[np.fft.irfftn(1j * K1 * uh[i], s=(n, n, n), axes=(0, 1, 2)), np.fft.irfftn(1j * K2 * uh[i], s=(n, n, n), axes=(0, 1, 2)), np.fft.irfftn(1j * K3 * uh[i], s=(n, n, n), axes=(0, 1, 2))] for i in range(3)]
        conv = np.zeros((3, n, n, n))
        for i in range(3):
            for j in range(3):
                conv[i] += ug[j] * derivs[i][j]
        return (conv, ug, derivs)

    def drag_hat(uh):
        ug = to_real(uh)
        mag = np.sqrt(np.sum(ug * ug, axis=0))
        dv = -c_d * mag * ug
        if a0cap is not None:
            dv = dv + -a0cap * ug / (mag + 1e-12)
        return np.stack([np.fft.rfftn(dv[i], axes=(0, 1, 2)) for i in range(3)])
    gx = np.linspace(0, 2 * np.pi, n, endpoint=False)
    s = np.sin(gx)[:, None, None] + np.cos(gx)[None, :, None] + np.sin(gx)[None, None, :] + np.cos(gx[:, None, None] + gx[None, :, None])
    s = s / np.max(np.abs(s))
    fhat = proj(np.stack([A * np.fft.rfftn(s * 1.0, axes=(0, 1, 2)), A * np.fft.rfftn(s * 0.7, axes=(0, 1, 2)), A * np.fft.rfftn(s * 0.4, axes=(0, 1, 2))]))
    fg = to_real(fhat)
    uh = np.zeros((3, n, n, n // 2 + 1), dtype=complex)
    for i in range(3):
        uh[i] = np.fft.rfftn(rng.standard_normal((n, n, n)), axes=(0, 1, 2))
    uh *= (Ksq <= 16.0) * (Ksq > 0.0)
    uh = proj(uh)
    uh /= np.linalg.norm(to_real(uh))
    lam = -(nu * Ksq)

    def rhs(u):
        return proj(lam * u) - proj(nlin(u)) + proj(drag_hat(u)) + fhat
    nsteps = int(round(T / dt))
    delta = every * dt
    T_hist = np.arange(0, nsteps + 1, every) * dt
    ns = len(T_hist)
    (sup, enst, ene) = (np.empty(ns) for _ in range(3))
    E_real = np.empty(ns) if track_g29 else None
    Z_real = np.empty(ns) if track_g29 else None
    Pf = np.empty(ns) if track_g29 else None
    Pd = np.empty(ns) if track_g29 else None
    cfl_max = 0.0
    u = uh.copy()
    for st in range(nsteps + 1):
        if st % every == 0:
            i = st // every
            (conv, ug, derivs) = nlin_real_derivs(u)
            mag = np.sqrt(np.sum(ug * ug, axis=0))
            sup[i] = float(np.max(mag))
            cfl_max = max(cfl_max, float(np.max(mag)) * dt * kmax_dealias)
            ene[i] = 0.5 * float(np.mean(mag * mag))
            enst[i] = 0.0
            for a in range(3):
                for b in range(3):
                    enst[i] += float(np.mean(derivs[a][b] ** 2))
            if track_g29:
                E_real[i] = ene[i]
                Z_real[i] = enst[i]
                Pf[i] = float(np.mean(np.sum(fg * ug, axis=0)))
                Pd[i] = float(np.mean(-c_d * mag * mag * mag - (a0cap * mag * mag / (mag + 1e-12) if a0cap is not None else 0.0)))
        if st == nsteps:
            break
        k1 = rhs(u)
        k2 = rhs(u + dt / 2 * k1)
        k3 = rhs(u + dt / 2 * k2)
        k4 = rhs(u + dt * k3)
        u = u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if st % 10000 == 0 and st > 0:
            import sys
            print(f'  [{tag}] step {st}/{nsteps} ({100.0 * st / nsteps:.0f}%) elapsed {time.perf_counter() - t0:.0f} s', flush=True)
    wall = time.perf_counter() - t0
    return {'t': T_hist, 'sup': sup, 'enst': enst, 'ene': ene, 'E_real': E_real, 'Z_real': Z_real, 'Pf': Pf, 'Pd': Pd, 'cfl': cfl_max, 'kmax_dealias': kmax_dealias, 'wall_time': wall, 'state': u, 'initial': uh, 'forcing': fhat, 'Ksq': Ksq}
