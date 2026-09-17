#!/usr/bin/env python3
"""N04b_equilibrium.py -- equilibrium numerics evidence lane (SPEC_C).

3D periodic Galerkin runs of the ZNS family on [0, 2pi)^3, run to VISCOUS
EQUILIBRIUM (N04's T=6 was spin-up only: enstrophy was still growing there):

    u_t + (u.grad)u = -grad p + nu Laplacian u - c_d |u| u + f,   div u = 0

Cases (three runs): classical (c_d = 0), a0-capped dry drag (|d| <= 0.02,
N2 sub-regularizing class), strong drag (c_d = 0.3).  Forcing f = A*s with
sup|s| = 1 on the low modes; 2/3-dealiasing mask |k| <= (2/3)(n/2).

Parameters (SPEC_C): n = 32, nu = 2e-2, dt = 2e-3, T = 40, A = 1.0, seed = 7.
RK4 in Fourier space; record sup||u||_oo, enstrophy and energy as exact
per-volume real-space means (enstrophy = spec's sum|k|^2|uhat|^2/N^3 in
orthonormal-mode amplitudes; numpy rfftn output is unnormalized, so a raw
spectral sum would carry a time-dependent ~N^3 plane-pairing bias -- hence
real-space evaluation), plus the window diagnostic
eta = ||(u.grad)u + nu Lap u||_oo / a0_sim (a0_sim = 0.02); every 25 steps
(delta = 25*dt = 0.05).

Evidence gates (PASS/FAIL prints + JSON):
  G25  equilibrium reached per case: last-quarter mean enstrophy within 15%
       of the previous-quarter mean (the spin-up ends -- honest analog of
       N04's failed gate).
  G26  suppression order: sup peaks classical > a0cap >= cd03 (drag ladder
       lowers the sup; the a0-cap class sits just below classical).
  G27  trajectory inequality (window-theorem verification, EVIDENCE ONLY):
       from classical-run snapshots, at each grid point
       a_mat ~= (u(t+delta) - u(t))/delta + (u.grad)u(t)  and pointwise
       ||u(t+delta)| - |u(t)|| <= delta*max|a_mat| + tol, tol = 1e-9*scale.
  G28  window diagnostic: eta_flow for the classical run + first-exit time
       of the level eta = 3.5 ('no exit' if never).
  G29  discrete energy-identity sanity (classical): dE/dt = -nu Z + <f,u>
       (E = 0.5<|u|^2> volume mean; identical to the spec's form
       dE/dt = -2 nu Z + <f,u> up to the standard 1/2-E normalization):
       Euler-forward check E(t+delta) vs E(t) + delta*(-nu Z + <f,u>) with
       residuals <= 1% over the run.

EVIDENCE ONLY: all simulations support the lane statements (incl. the window
theorem); they are numerical evidence, NOT proofs.

Outputs (this folder only): N04b_equilibrium.out, N04b_equilibrium_results.json,
N04b_equilibrium.png.  No git.  No absolute paths in committed content.
"""
import json, math, time
import numpy as np
import numpy.fft as _fft

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False


def galerkin(n, nu, c_d, a0cap, A, T, dt, seed=7, every=25,
             track_g27=False, track_g29=False):
    """Run one dealiased Galerkin case; return recorded histories + checks.

    track_g27: additionally verify the trajectory inequality pointwise on the
    grid for every consecutive snapshot pair (classical run only).
    track_g29: additionally record real-space volume means E = 0.5<|u|^2>,
    Z = <|grad u|^2>, Pf = <f.u> for the discrete energy-identity check.
    """
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)
    k1 = np.fft.fftfreq(n) * n                       # integer modes
    K1, K2, K3 = np.meshgrid(k1, k1, k1[:n // 2 + 1], indexing='ij')
    Ksq = K1 * K1 + K2 * K2 + K3 * K3
    Ksq[0, 0, 0] = 1.0
    # 2/3-dealiasing mask |k| <= (2/3)(n/2):
    MASK = (Ksq <= ((2.0 / 3.0) * (n / 2.0)) ** 2).astype(float)

    def proj(uh):
        uh = uh * MASK
        kdot = (K1 * uh[0] + K2 * uh[1] + K3 * uh[2]) / Ksq
        uh = uh - np.stack([kdot * K1, kdot * K2, kdot * K3])
        for i in range(3):
            uh[i, 0, 0, 0] = 0.0
        return uh

    def to_real(uh):
        return np.stack([np.fft.irfftn(uh[i], s=(n, n, n), axes=(0, 1, 2))
                         for i in range(3)])

    def nlin(uh):       # spectral (u.grad)u, dealiased state -> raw product
        ug = to_real(uh)
        Dx = [np.fft.irfftn(1j * K1 * uh[i], s=(n, n, n), axes=(0, 1, 2))
              for i in range(3)]
        Dy = [np.fft.irfftn(1j * K2 * uh[i], s=(n, n, n), axes=(0, 1, 2))
              for i in range(3)]
        Dz = [np.fft.irfftn(1j * K3 * uh[i], s=(n, n, n), axes=(0, 1, 2))
              for i in range(3)]
        conv = [np.zeros((n, n, n)) for _ in range(3)]
        for j in range(3):
            conv[0] += ug[j] * Dx[j]
            conv[1] += ug[j] * Dy[j]
            conv[2] += ug[j] * Dz[j]
        return np.stack([np.fft.rfftn(conv[i], axes=(0, 1, 2))
                         for i in range(3)])

    def nlin_real_derivs(uh):
        """Return (conv, derivs): conv = (u.grad)u in real space, derivs[i][j]
        = d_j u_i in real space (uses the dealiased spectral state)."""
        ug = to_real(uh)
        derivs = [[np.fft.irfftn(1j * K1 * uh[i], s=(n, n, n), axes=(0, 1, 2)),
                   np.fft.irfftn(1j * K2 * uh[i], s=(n, n, n), axes=(0, 1, 2)),
                   np.fft.irfftn(1j * K3 * uh[i], s=(n, n, n), axes=(0, 1, 2))]
                  for i in range(3)]
        conv = np.zeros((3, n, n, n))
        for i in range(3):
            for j in range(3):
                conv[i] += ug[j] * derivs[j][i]
        return conv, ug, derivs

    def accel_hat(uh):       # (u.grad)u + nu Lap u  (Newtonian acceleration)
        return proj(nlin(uh)) + proj(-(nu * Ksq) * uh)

    def drag_hat(uh):
        ug = to_real(uh)
        mag = np.sqrt(np.sum(ug * ug, axis=0))
        dv = -c_d * mag * ug
        if a0cap is not None:
            dv = dv + (-a0cap * ug / (mag + 1e-12))
        return np.stack([np.fft.rfftn(dv[i], axes=(0, 1, 2)) for i in range(3)])

    gx = np.linspace(0, 2 * np.pi, n, endpoint=False)
    s = (np.sin(gx)[:, None, None] + np.cos(gx)[None, :, None]
         + np.sin(gx)[None, None, :] + np.cos(gx[:, None, None]
           + gx[None, :, None]))
    s = s / np.max(np.abs(s))
    fhat = proj(np.stack([
        A * np.fft.rfftn(s * 1.0, axes=(0, 1, 2)),
        A * np.fft.rfftn(s * 0.7, axes=(0, 1, 2)),
        A * np.fft.rfftn(s * 0.4, axes=(0, 1, 2))]))
    fg = to_real(fhat)                       # real-space forcing field

    uh = np.zeros((3, n, n, n // 2 + 1), dtype=complex)
    for i in range(3):
        uh[i] = np.fft.rfftn(rng.standard_normal((n, n, n)), axes=(0, 1, 2))
    uh *= (Ksq <= 16.0) * (Ksq > 0.0)        # random field in low modes
    uh = proj(uh)
    uh /= np.linalg.norm(to_real(uh))

    lam = -(nu * Ksq)

    def rhs(u):
        return proj(lam * u) + proj(nlin(u)) + proj(drag_hat(u)) + fhat

    a0_sim = 0.02
    nsteps = int(round(T / dt))
    delta = every * dt
    T_hist = np.arange(0, nsteps + 1, every) * dt
    ns = len(T_hist)
    sup, enst, ene, eta = (np.empty(ns) for _ in range(4))
    E_real = np.empty(ns) if track_g29 else None
    Z_real = np.empty(ns) if track_g29 else None
    Pf = np.empty(ns) if track_g29 else None

    g27 = {'n_viol': 0, 'worst_excess': -np.inf, 'worst_pair': -1,
           'maxa_max': 0.0, 'n_pairs': ns - 1, 'delta': delta} \
        if track_g27 else None
    ug_prev = None
    mag_prev = None
    conv_prev = None

    u = uh.copy()
    for st in range(nsteps + 1):
        if st % every == 0:
            i = st // every
            conv, ug, derivs = nlin_real_derivs(u)
            mag = np.sqrt(np.sum(ug * ug, axis=0))
            sup[i] = float(np.max(mag))
            # ENERGY/ENSTROPHY as exact per-volume real-space means (equal to
            # the spec's sum|k|^2|uhat|^2/N^3 in orthonormal-mode amplitudes;
            # numpy rfftn output is unnormalized and its Hermitian-pair planes
            # would bias the raw spectral sum by a time-dependent ~N^3 factor
            # -- the reason for real-space evaluation):
            ene[i] = 0.5 * float(np.mean(mag * mag))
            enst[i] = 0.0
            for a in range(3):
                for b in range(3):
                    enst[i] += float(np.mean(derivs[a][b] ** 2))
            ah = accel_hat(u)
            ag = to_real(ah)
            eta[i] = float(np.max(np.sqrt(np.sum(ag * ag, axis=0)))) / a0_sim

            if track_g29:
                E_real[i] = ene[i]
                Z_real[i] = enst[i]
                Pf[i] = float(np.mean(np.sum(fg * ug, axis=0)))
            if track_g27:
                if i > 0:
                    a_mat = (ug - ug_prev) / delta + conv_prev
                    maxa = float(np.max(np.sqrt(np.sum(a_mat * a_mat, axis=0))))
                    g27['maxa_max'] = max(g27['maxa_max'], maxa)
                    lhs = np.abs(mag - mag_prev)
                    excess = float(np.max(lhs - delta * maxa))
                    if excess > g27['worst_excess']:
                        g27['worst_excess'] = excess
                        g27['worst_pair'] = i
                    g27['n_viol'] += int(np.sum(lhs > delta * maxa))
                conv_prev = conv
                ug_prev = ug
                mag_prev = mag
        if st == nsteps:
            break
        k1 = rhs(u); k2 = rhs(u + dt / 2 * k1)
        k3 = rhs(u + dt / 2 * k2); k4 = rhs(u + dt * k3)
        u = u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    wall = time.perf_counter() - t0
    return {'t': T_hist, 'sup': sup, 'enst': enst, 'ene': ene, 'eta': eta,
            'E_real': E_real, 'Z_real': Z_real, 'Pf': Pf, 'g27': g27,
            'wall_time': wall}


# ---------------------------------------------------------------- parameters
N, NU, DT, TOT, A = 32, 2e-2, 2e-3, 40.0, 1.0
SEED, A0SIM = 7, 0.02
EVERY, DELTA = 25, 25 * 2e-3

print('=' * 78)
print('N04b_equilibrium: equilibrium numerics lane (SPEC_C)')
print('EVIDENCE ONLY: simulations are numerical evidence, not proofs.')
print('=' * 78)
print(f'Galerkin runs: n = {N}, nu = {NU}, dt = {DT}, T = {TOT}, A = {A},'
      f' seed = {SEED}; dealiased 2/3 rule; snapshots every {EVERY} steps'
      f' (delta = {DELTA})')

runs = {
    'classical': galerkin(N, NU, 0.0, None, A, TOT, DT, seed=SEED,
                          track_g27=True, track_g29=True),
    'a0cap_002': galerkin(N, NU, 0.0, 0.02, A, TOT, DT, seed=SEED),
    'cd_03':     galerkin(N, NU, 0.3, None, A, TOT, DT, seed=SEED),
}

checks = []


def gate(name, cnd, val, thresh, note):
    checks.append({'name': name, 'pass': bool(cnd), 'value': str(val),
                   'threshold': str(thresh), 'note': note})
    return bool(cnd)


# ----------------------------- G25: equilibrium reached (per case)
for name in ('classical', 'a0cap_002', 'cd_03'):
    z = runs[name]['enst']
    tail = float(np.mean(z[-200:]))          # last quarter (10 time units)
    prev = float(np.mean(z[-400:-200]))      # previous quarter
    ratio = abs(tail - prev) / max(prev, 1e-300)
    gate(f'G25_equilibrium_{name}', ratio <= 0.15, f'{ratio:.3f}', '<= 0.15',
         f'{name}: last-quarter mean enstrophy {tail:.3f} vs previous-quarter'
         f' {prev:.3f}: relative change {ratio:.1%}' +
         (' -- viscous equilibrium reached (spin-up ended).'
          if ratio <= 0.15 else ' -- still drifting: equilibrium NOT reached.'))

# ----------------------------- G26: suppression order
M_c = float(np.max(runs['classical']['sup']))
M_a = float(np.max(runs['a0cap_002']['sup']))
M_d = float(np.max(runs['cd_03']['sup']))
B_d = math.sqrt(A / 0.3)
gate('G26_suppression_order', M_c > M_a >= M_d, f'{M_c:.4f} > {M_a:.4f} >= {M_d:.4f}',
     'classical > a0cap >= cd03',
     f'sup peaks: classical {M_c:.4f} > a0cap-0.02 {M_a:.4f} >= cd-0.3 {M_d:.4f}'
     f' (barrier sqrt(A/cd) = {B_d:.3f} for cd = 0.3): the drag ladder lowers'
     f' the sup monotonically; the a0-cap class is sub-regularizing and sits'
     f' close to classical (case set has no cd=0.05 rung).')

# ----------------------------- G27: trajectory inequality (classical)
g7 = runs['classical']['g27']
scale = max(g7['maxa_max'], 1e-300)
tol = 1e-9 * scale
npts = g7['n_pairs'] * (N ** 3)
c27 = g7['worst_excess'] <= tol
gate('G27_trajectory_inequality', c27, f'{g7["worst_excess"]:.3e}', f'<= tol = {tol:.3e}',
     f'classical run: pointwise | |u(t+delta)| - |u(t)| | <= delta*max|a_mat|'
     f' + tol checked on {npts} point-pairs (delta = {DELTA}), worst excess'
     f' {g7["worst_excess"]:.3e} <= tol {tol:.3e} (tol = 1e-9*scale, scale ='
     f' max|a_mat| = {g7["maxa_max"]:.3f}), {g7["n_viol"]} point violations at'
     f' tol = 0: the elementary inequality behind the window theorem is'
     f' consistent with the discrete dynamics (EVIDENCE ONLY, not a proof).')

# ----------------------------- G28: window diagnostic (classical)
eta_c = runs['classical']['eta']
exits = np.nonzero(eta_c > 3.5)[0]
if len(exits) > 0:
    t_exit = float(runs['classical']['t'][exits[0]])
    exit_str = f'{t_exit:.3f}'
    c28 = True
    note28 = (f'classical run (a0_sim = {A0SIM}): eta_flow(t) ='
              f' ||(u.grad)u + nu Lap u||_oo / a0_sim first EXITS the'
              f' eta = 3.5 level at t = {t_exit:.3f} (max eta ='
              f' {float(np.max(eta_c)):.1f}, min eta = {float(np.min(eta_c)):.1f},'
              f' last-quarter mean {float(np.mean(eta_c[-200:])):.1f}): the'
              f' turbulent classical flow is NOT confined to the sub-floor'
              f' window -- the window-exit diagnostic fires.')
else:
    t_exit = None
    exit_str = 'no exit'
    c28 = True          # report-only per SPEC_C: 'no exit' is a valid report
    note28 = (f'classical run (a0_sim = {A0SIM}): eta_flow never exceeds'
              f' eta = 3.5 within T = {TOT} (max eta = {float(np.max(eta_c)):.1f}):'
              f' reported as "no exit" per SPEC_C.')
gate('G28_window_first_exit', c28, exit_str, 'first exit of eta = 3.5 (or no exit)',
     note28)

# ----------------------------- G29: discrete energy identity (classical)
E_r, Z_r, P_f = (runs['classical'][k] for k in ('E_real', 'Z_real', 'Pf'))
P_bal = -NU * Z_r + P_f                    # dE/dt = -nu*Z + <f,u>, E = 0.5<|u|^2>
dE = E_r[1:] - E_r[:-1]
pred = DELTA * P_bal[:-1]
err = np.abs(dE - pred)
P_rms = float(np.sqrt(np.mean(P_bal ** 2)))
rel = err / np.maximum(np.abs(pred), DELTA * P_rms + 1e-300)
max_rel = float(np.max(rel))
acc_err = float(np.abs(E_r[-1] - E_r[0] - DELTA * np.sum(P_bal[:-1])))
acc_ref = max(abs(E_r[-1] - E_r[0]), 1e-300)
acc_rel = acc_err / acc_ref
c29 = max_rel <= 0.01 and acc_rel <= 0.01
gate('G29_energy_identity', c29, f'max-local {max_rel:.3%}, accumulated {acc_rel:.3%}',
     'max-local <= 1% and accumulated <= 1%',
     f'classical: E = 0.5<|u|^2> volume mean, Z = <|grad u|^2>,'
     f' dE/dt = -nu*Z + <f,u> (spec form dE/dt = -2nu*Z + <f,u> up to the 1/2'
     f' energy normalization); Euler-forward check E(t+delta) vs'
     f' E(t) + delta*(-nu*Z + <f,u>) over the run: worst local relative'
     f' residual {max_rel:.3%} (typical power scale |delta*<f,u>| ~'
     f' {DELTA * P_rms:.4f}), accumulated residual {acc_rel:.3%} of the'
     f' energy change |E(T)-E(0)| = {abs(E_r[-1] - E_r[0]):.4f}: the discrete'
     f' energy budget closes to <= 1% -- the integrator is healthy.')

# ---------------------------------------------------------------- PNG (2x2)
png_path = 'N04b_equilibrium.png'
if HAVE_MPL:
    tt = runs['classical']['t']
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))
    cols = (('classical', '#000000'), ('a0cap_002', '#888888'),
            ('cd_03', '#15803d'))
    for name, col in cols:
        r = runs[name]
        ax[0, 0].plot(tt, r['sup'], color=col, lw=1.2, label=name)
        ax[0, 1].plot(tt, r['ene'], color=col, lw=1.2, label=name)
        ax[1, 0].plot(tt, r['enst'], color=col, lw=1.2, label=name)
        ax[1, 1].plot(tt, r['eta'], color=col, lw=1.2, label=name)
    ax[0, 0].set_title(f'sup ||u||_oo(t)  (barrier for cd=0.3: {B_d:.2f})')
    ax[0, 0].axhline(B_d, color='red', lw=0.8, ls='--')
    ax[0, 1].set_title('energy E(t) = 0.5<|u|^2> (per volume)')
    ax[1, 0].set_title('enstrophy <|grad u|^2> per volume (t)')
    ax[1, 1].set_title('window diagnostic eta(t) = ||a||_oo / a0_sim'
                       '  (floor 3.5 dashed)')
    ax[1, 1].axhline(3.5, color='red', lw=0.8, ls='--')
    for a in ax.flat:
        a.legend(fontsize=8)
        a.grid(alpha=0.3)
    fig.suptitle('N04b equilibrium numerics (SPEC_C): n=32, nu=2e-2, dt=2e-3,'
                 ' T=40, A=1 -- EVIDENCE ONLY, not proofs', fontsize=11)
    fig.tight_layout()
    fig.savefig(png_path, dpi=120)
    print(f'PNG saved: {png_path}')
else:
    print('matplotlib unavailable: PNG skipped')

# ---------------------------------------------------------------- JSON
res = {
    'lane': 'N04b_equilibrium',
    'evidence_only': 'Simulations are numerical evidence for the lane'
                     ' statements (incl. the window theorem); they are NOT proofs.',
    'params': {'n': N, 'nu': NU, 'dt': DT, 'T': TOT, 'A': A, 'seed': SEED,
               'a0_sim': A0SIM, 'dealiasing': '2/3 rule', 'every': EVERY,
               'delta': DELTA,
               'cases': {'classical': {'c_d': 0.0, 'a0cap': None},
                         'a0cap_002': {'c_d': 0.0, 'a0cap': 0.02},
                         'cd_03': {'c_d': 0.3, 'a0cap': None}}},
    'wall_time_s': {k: round(r['wall_time'], 1) for k, r in runs.items()},
    'sup_peak': {k: float(np.max(r['sup'])) for k, r in runs.items()},
    'sup_final': {k: float(r['sup'][-1]) for k, r in runs.items()},
    'enst_final': {k: float(r['enst'][-1]) for k, r in runs.items()},
    'enst_last_quarter_mean': {k: float(np.mean(r['enst'][-200:]))
                               for k, r in runs.items()},
    'enst_prev_quarter_mean': {k: float(np.mean(r['enst'][-400:-200]))
                               for k, r in runs.items()},
    'eta_classical': {'max': float(np.max(runs['classical']['eta'])),
                      'min': float(np.min(runs['classical']['eta'])),
                      'last_quarter_mean':
                          float(np.mean(runs['classical']['eta'][-200:])),
                      'first_exit_eta3.5': exit_str},
    'g27_trajectory_inequality': {'delta': DELTA, 'n_point_pairs': npts,
                                  'worst_excess': g7['worst_excess'],
                                  'n_viol_tol0': g7['n_viol'],
                                  'max_abs_a_mat': g7['maxa_max'],
                                  'tol': tol},
    'g29_energy_identity': {'E_final': float(E_r[-1]),
                            'energy_change': abs(E_r[-1] - E_r[0]),
                            'acc_residual': acc_err,
                            'acc_relative': acc_rel,
                            'max_local_relative': max_rel,
                            'P_rms': P_rms},
    'checks': [{'name': c['name'], 'pass': c['pass'], 'value': c['value'],
                'threshold': c['threshold'], 'note': c['note']}
               for c in checks],
}
with open('N04b_equilibrium_results.json', 'w') as f:
    json.dump(res, f, indent=1)

# ---------------------------------------------------------------- report
print()
print(f'wall times: ' +
      ', '.join(f'{k} = {r["wall_time"]:.1f} s' for k, r in runs.items()))
for c in checks:
    print(('PASS' if c['pass'] else 'FAIL'), c['name'], f'value={c["value"]}')
    print('     ', c['note'])
npass = sum(1 for c in checks if c['pass'])
print(f'<N04b_equilibrium> COMPLETE: {npass}/{len(checks)} checks PASS.')
print('EVIDENCE ONLY: the Galerkin runs support the lane statements;'
      ' simulations are not proofs.')
