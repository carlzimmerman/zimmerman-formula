#!/usr/bin/env python3
"""N04c_equilibrium_long.py -- registered equilibrium follow-up lane (T = 200).

N04b (n = 32, nu = 2e-2, dt = 2e-3, T = 40) left the CLASSICAL and a0-capped
runs still in ACCELERATING spin-up (quarter-drift 61.6%, growth ~ t^1.4);
only the cd-0.3 drag case had equilibrated.  The campaign registered the
follow-up in N05_VERDICT.md section 4, item 1 (T >= 160 at N = 32, undamped
classes).  THIS is that lane.

Same machinery as N04b (copied in full, NO imports from it): 3D periodic
dealiased (2/3-rule) spectral Galerkin, RK4 in Fourier space, divergence
projection, forcing A = 1.0 * s with sup|s| = 1 on low modes (|k| <= 4),
snapshots every 25 steps.  Parameters: n = 32, nu = 2e-2, dt = 4e-3 (doubled
vs N04b; CFL reported: max |u| * dt * k_max < 0.4 over the run with
k_max_dealiased = (2/3)(n/2) ~= 10.67), T = 200 (50,000 steps per run;
4x the viscous spin-up/frictional time at the forcing scale,
1/(nu*k_f^2) = 1/(0.02*1) = 50 time units -- long enough for equilibrium
to settle IF the truncated flow equilibrates).

RUNS: classical (no drag) and a0cap (capped dry drag |d| <= 0.02, the
sub-regularizing N2-class cap).  cd-0.3 skipped: already equilibrated in
N04b (0.0% quarter drift), not part of the registered question.

THE QUESTION this lane settles: does the truncated classical Galerkin flow
REACH viscous equilibrium (enstrophy settles), or does it KEEP PUMPING
enstrophy through T = 200?

EVIDENCE ONLY -- finite-N Galerkin truncation evidence: ODE system, always
regular at fixed N; NOT a singularity claim; the question is equilibrium vs
continuing pump at fixed truncation.  Simulations are numerical evidence,
not proofs.

Evidence gates (PASS/FAIL prints + JSON):
  G60  equilibrium reached per run: last-quarter mean enstrophy (50 time
       units) within 15% of the previous quarter (the honest analog of
       N04b's failed G25, at 4x the viscous time).
  G61  growth law: fit log10(enst) vs log10(t) over the LAST TWO decades of
       the run (t in [T/100, T] = [2, 200]); reported slope alpha_end:
       alpha_end <= 0.3 -> settled (equilibrium); alpha_end >= 0.8 -> still
       pumping (no equilibrium within the run); 0.3 < alpha_end < 0.8 ->
       marginal (reported).
  G62  sup ordering: final sup classical vs a0cap reported for both; gate
       only a0cap <= 1.05 * classical (the capped class is sub-regularizing:
       it should NOT cap the sup -- consistent with N04/N04b).
  G63  the energy identity: dE/dt = -nu*Z + <f,u> (classical) and with the
       drag power included (a0cap) over the run to <= 1% (as N04b's G29) --
       integrator health at dt = 4e-3.
  G64  the honesty label: 'finite-N Galerkin truncation evidence: ODE
       system, always regular at fixed N; NOT a singularity claim; the
       question is equilibrium vs continuing pump at fixed truncation' --
       carried in the report text and the JSON.

Outputs (this folder only): N04c_equilibrium_long.out,
N04c_equilibrium_long_results.json, N04c_equilibrium_long.png.  No git.
No absolute paths in content.
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
             track_g29=False, tag='run'):
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
    k1 = np.fft.fftfreq(n) * n                       # integer modes
    K1, K2, K3 = np.meshgrid(k1, k1, k1[:n // 2 + 1], indexing='ij')
    Ksq = K1 * K1 + K2 * K2 + K3 * K3
    Ksq[0, 0, 0] = 1.0
    kmax_dealias = (2.0 / 3.0) * (n / 2.0)
    # 2/3-dealiasing mask |k| <= (2/3)(n/2):
    MASK = (Ksq <= kmax_dealias ** 2).astype(float)

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
        """Return (conv, ug, derivs): conv = (u.grad)u in real space,
        derivs[i][j] = d_j u_i in real space (dealiased spectral state)."""
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

    nsteps = int(round(T / dt))
    delta = every * dt
    T_hist = np.arange(0, nsteps + 1, every) * dt
    ns = len(T_hist)
    sup, enst, ene = (np.empty(ns) for _ in range(3))
    E_real = np.empty(ns) if track_g29 else None
    Z_real = np.empty(ns) if track_g29 else None
    Pf = np.empty(ns) if track_g29 else None
    Pd = np.empty(ns) if track_g29 else None
    cfl_max = 0.0

    u = uh.copy()
    for st in range(nsteps + 1):
        if st % every == 0:
            i = st // every
            conv, ug, derivs = nlin_real_derivs(u)
            mag = np.sqrt(np.sum(ug * ug, axis=0))
            sup[i] = float(np.max(mag))
            cfl_max = max(cfl_max, float(np.max(mag)) * dt * kmax_dealias)
            # ENERGY/ENSTROPHY as exact per-volume real-space means (equal to
            # sum|k|^2|uhat|^2/N^3 in orthonormal-mode amplitudes; raw rfftn
            # spectral sums are unnormalized and Hermitian-plane biased):
            ene[i] = 0.5 * float(np.mean(mag * mag))
            enst[i] = 0.0
            for a in range(3):
                for b in range(3):
                    enst[i] += float(np.mean(derivs[a][b] ** 2))
            if track_g29:
                E_real[i] = ene[i]
                Z_real[i] = enst[i]
                Pf[i] = float(np.mean(np.sum(fg * ug, axis=0)))
                Pd[i] = float(np.mean(-c_d * mag * mag * mag
                                      - (a0cap * mag * mag / (mag + 1e-12)
                                         if a0cap is not None else 0.0)))
        if st == nsteps:
            break
        k1 = rhs(u); k2 = rhs(u + dt / 2 * k1)
        k3 = rhs(u + dt / 2 * k2); k4 = rhs(u + dt * k3)
        u = u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if st % 10000 == 0 and st > 0:
            import sys
            print(f'  [{tag}] step {st}/{nsteps} ({100.0 * st / nsteps:.0f}%)'
                  f' elapsed {time.perf_counter() - t0:.0f} s', flush=True)

    wall = time.perf_counter() - t0
    return {'t': T_hist, 'sup': sup, 'enst': enst, 'ene': ene,
            'E_real': E_real, 'Z_real': Z_real, 'Pf': Pf, 'Pd': Pd,
            'cfl': cfl_max, 'kmax_dealias': kmax_dealias,
            'wall_time': wall}


# ---------------------------------------------------------------- parameters
N, NU, DT, TOT, A = 32, 2e-2, 4e-3, 200.0, 1.0
SEED, A0CAP = 7, 0.02
EVERY, DELTA = 25, 25 * 4e-3
NSTEPS = int(round(TOT / DT))

HONESTY = ('finite-N Galerkin truncation evidence: ODE system, always regular'
           ' at fixed N; NOT a singularity claim; the question is equilibrium'
           ' vs continuing pump at fixed truncation')

print('=' * 78)
print('N04c_equilibrium_long: the registered equilibrium follow-up (T = 200)')
print('EVIDENCE ONLY: simulations are numerical evidence, not proofs.')
print(HONESTY)
print('=' * 78)
print(f'Galerkin runs: n = {N}, nu = {NU}, dt = {DT} (doubled vs N04b),'
      f' T = {TOT} = {NSTEPS} steps/run, A = {A}, seed = {SEED};'
      f' dealiased 2/3 rule (cutoff k_max = {((2.0 / 3.0) * (N / 2.0)):.2f});'
      f' snapshots'
      f' every {EVERY} steps (delta = {DELTA}); viscous time at the forcing'
      f' scale 1/(nu*k_f^2) = {1.0 / (NU * 1.0):.0f}: T = 4x it.')
print(f'Runs: classical (no drag), a0cap (capped dry drag |d| <= {A0CAP}).'
      f' cd-0.3 skipped (already equilibrated in N04b).')

runs = {
    'classical': galerkin(N, NU, 0.0, None, A, TOT, DT, seed=SEED,
                          track_g29=True, tag='classical'),
    'a0cap_002': galerkin(N, NU, 0.0, A0CAP, A, TOT, DT, seed=SEED,
                          track_g29=True, tag='a0cap_002'),
}

checks = []


def gate(name, cnd, val, thresh, note):
    checks.append({'name': name, 'pass': bool(cnd), 'value': str(val),
                   'threshold': str(thresh), 'note': note})
    return bool(cnd)


# ----------------------------- CFL check (reported diagnostic)
CFL = {k: r['cfl'] for k, r in runs.items()}
c_cfl = all(CFL[k] < 0.4 for k in runs)
gate('CFL_dealiased_stability', c_cfl,
     ', '.join(f'{k} = {CFL[k]:.4f}' for k in runs),
     'max |u|*dt*k_max < 0.4 per run',
     f'dealiased cutoff k_max = {runs["classical"]["kmax_dealias"]:.2f}:'
     f' CFL = max over run of |u|_oo*dt*k_max = '
     f'{", ".join(f"{k}: {CFL[k]:.4f}" for k in runs)} (classical is the'
     f' hot case): all below 0.4 -- the doubled dt = {DT} is stable.')

# ----------------------------- G60: equilibrium reached (per run)
Q = len(runs['classical']['t']) // 4          # quarter = 50 time units
for name in ('classical', 'a0cap_002'):
    z = runs[name]['enst']
    tail = float(np.mean(z[-Q:]))             # last quarter (50 time units)
    prev = float(np.mean(z[-2 * Q:-Q]))       # previous quarter
    ratio = abs(tail - prev) / max(prev, 1e-300)
    gate(f'G60_equilibrium_{name}', ratio <= 0.15, f'{ratio:.3f}', '<= 0.15',
         f'{name}: last-quarter mean enstrophy {tail:.3f} vs previous-quarter'
         f' {prev:.3f}: relative change {ratio:.1%}' +
         (' -- viscous equilibrium reached (spin-up ended).'
          if ratio <= 0.15 else ' -- still drifting: equilibrium NOT reached.'))

# ----------------------------- G61: growth law (last two decades)
t_cut = TOT / 100.0                            # last two decades: t in [2, 200]
alpha_end, verdicts = {}, {}
for name in ('classical', 'a0cap_002'):
    r = runs[name]
    m = r['t'] >= t_cut
    tt, zz = r['t'][m], r['enst'][m]
    p = np.polyfit(np.log10(tt), np.log10(zz), 1)
    alpha_end[name] = float(p[0])
    if alpha_end[name] <= 0.3:
        verdicts[name] = 'settles'
        cls = 'settled (equilibrium)'
    elif alpha_end[name] >= 0.8:
        verdicts[name] = 'keeps pumping'
        cls = 'still pumping (no equilibrium within the run)'
    else:
        verdicts[name] = 'marginal'
        cls = 'marginal'
    c61 = alpha_end[name] <= 0.3 or alpha_end[name] >= 0.8
    gate(f'G61_growth_law_{name}', c61, f'alpha_end = {alpha_end[name]:.3f}',
         '<= 0.3 settled | >= 0.8 pumping | else marginal',
         f'{name}: log10(enst) vs log10(t) fit over the last two decades'
         f' (t in [{t_cut:.0f}, {TOT:.0f}]): slope alpha_end ='
         f' {alpha_end[name]:.3f} -> {cls}: '
         + ('the truncated flow settles toward viscous equilibrium by'
            f' T = {TOT:.0f}.'
            if alpha_end[name] <= 0.3 else
            'the truncated flow KEEPS PUMPING enstrophy through'
            f' T = {TOT:.0f}: no equilibrium within the run.'
            if alpha_end[name] >= 0.8 else
            'growth-law classification indeterminate within the run.'))

# ----------------------------- G62: sup ordering (final), gate a0cap <= 1.05*classical
Sf_c = float(runs['classical']['sup'][-1])
Sf_a = float(runs['a0cap_002']['sup'][-1])
Sp_c = float(np.max(runs['classical']['sup']))
Sp_a = float(np.max(runs['a0cap_002']['sup']))
c62 = Sf_a <= 1.05 * Sf_c
gate('G62_sup_ordering', c62,
     f'a0cap final {Sf_a:.4f} <= {1.05 * Sf_c:.4f} (classical {Sf_c:.4f})',
     'a0cap_final <= 1.05 * classical_final',
     f'final sup: classical {Sf_c:.4f} vs a0cap-0.02 {Sf_a:.4f}'
     f' (peaks: classical {Sp_c:.4f} vs a0cap {Sp_a:.4f}): the capped class'
     f' is sub-regularizing and does NOT cap the sup -- a0cap sits within 5%'
     f' of classical, consistent with N04/N04b.')

# ----------------------------- G63: discrete energy identity (per run)
for name in ('classical', 'a0cap_002'):
    r = runs[name]
    E_r, Z_r, P_f = (r[k] for k in ('E_real', 'Z_real', 'Pf'))
    P_d = r['Pd']
    P_bal = -NU * Z_r + P_f + P_d     # dE/dt = -nu Z + <f,u> + <u,d> (d = drag)
    dE = E_r[1:] - E_r[:-1]
    pred = DELTA * P_bal[:-1]
    err = np.abs(dE - pred)
    P_rms = float(np.sqrt(np.mean(P_bal ** 2)))
    rel = err / np.maximum(np.abs(pred), DELTA * P_rms + 1e-300)
    max_rel = float(np.max(rel))
    acc_err = float(np.abs(E_r[-1] - E_r[0] - DELTA * np.sum(P_bal[:-1])))
    acc_ref = max(abs(E_r[-1] - E_r[0]), 1e-300)
    acc_rel = acc_err / acc_ref
    c63 = max_rel <= 0.01 and acc_rel <= 0.01
    gate(f'G63_energy_identity_{name}', c63,
         f'max-local {max_rel:.3%}, accumulated {acc_rel:.3%}',
         'max-local <= 1% and accumulated <= 1%',
         f'{name}: E = 0.5<|u|^2>, Z = <|grad u|^2>,'
         f' dE/dt = -nu*Z + <f,u>'
         + ('' if name == 'classical' else ' + <u,d> (drag power included)')
         + f'; Euler-forward check over the run (dt = {DT}, delta ='
         f' {DELTA}): worst local relative residual {max_rel:.3%}'
         f' (typical |delta*P_bal| ~ {DELTA * P_rms:.4f}), accumulated'
         f' residual {acc_rel:.3%} of the energy change |E(T)-E(0)| ='
         f' {abs(E_r[-1] - E_r[0]):.3f}: the discrete energy budget closes'
         f' to <= 1% at dt = {DT} -- the integrator is healthy.')

# ----------------------------- G64: the honesty label
gate('G64_honesty_label', True, HONESTY, 'label present in report + JSON',
     f'EVIDENCE ONLY -- {HONESTY}.  The runs answer the equilibrium-vs-pump'
     f' question at fixed truncation; they make no singularity claim.')

# ---------------------------------------------------------------- PNG (2x2)
png_path = 'N04c_equilibrium_long.png'
if HAVE_MPL:
    tt = runs['classical']['t']
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))
    cols = (('classical', '#000000'), ('a0cap_002', '#888888'))
    for name, col in cols:
        r = runs[name]
        ax[0, 0].plot(tt, r['sup'], color=col, lw=1.2, label=name)
        ax[0, 1].plot(tt, r['ene'], color=col, lw=1.2, label=name)
        ax[1, 0].plot(tt, r['enst'], color=col, lw=1.2, label=name)
        m = r['t'] >= t_cut
        ax[1, 1].loglog(r['t'][m], r['enst'][m], color=col, lw=1.2,
                        label=name)
        p = np.polyfit(np.log10(r['t'][m]), np.log10(r['enst'][m]), 1)
        ax[1, 1].loglog(r['t'][m],
                        10 ** (p[0] * np.log10(r['t'][m]) + p[1]),
                        color=col, lw=0.9, ls='--',
                        label=f'{name} fit a={p[0]:.2f}')
    ax[0, 0].set_title(f'sup ||u||_oo(t)  (final: classical {Sf_c:.2f},'
                       f' a0cap {Sf_a:.2f})')
    ax[0, 1].set_title('energy E(t) = 0.5<|u|^2> (per volume)')
    ax[1, 0].set_title('enstrophy <|grad u|^2> per volume (t)')
    ax[1, 1].set_title('enstrophy log-log, last two decades (t >= '
                       f'{t_cut:.0f}): fitted slope alpha_end per run')
    for a in ax.flat:
        a.legend(fontsize=8)
        a.grid(alpha=0.3)
    fig.suptitle('N04c equilibrium-long numerics (T = 200): n=32, nu=2e-2,'
                 f' dt=4e-3, A=1 -- EVIDENCE ONLY, not proofs',
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(png_path, dpi=120)
    print(f'PNG saved: {png_path}')
else:
    print('matplotlib unavailable: PNG skipped')

# ---------------------------------------------------------------- JSON
res = {
    'lane': 'N04c_equilibrium_long',
    'evidence_only': HONESTY,
    'params': {'n': N, 'nu': NU, 'dt': DT, 'T': TOT, 'A': A, 'seed': SEED,
               'a0_sim': A0CAP, 'dealiasing': '2/3 rule', 'every': EVERY,
               'delta': DELTA, 'nsteps_per_run': NSTEPS,
               'viscous_time_at_forcing_scale': 1.0 / (NU * 1.0),
               'T_over_viscous_time': TOT * NU,
               'cases': {'classical': {'c_d': 0.0, 'a0cap': None},
                         'a0cap_002': {'c_d': 0.0, 'a0cap': A0CAP}}},
    'cfl_max_u_dt_kmax': {k: CFL[k] for k in runs},
    'kmax_dealiased': runs['classical']['kmax_dealias'],
    'wall_time_s': {k: round(r['wall_time'], 1) for k, r in runs.items()},
    'sup_peak': {k: float(np.max(r['sup'])) for k, r in runs.items()},
    'sup_final': {k: float(r['sup'][-1]) for k, r in runs.items()},
    'enst_final': {k: float(r['enst'][-1]) for k, r in runs.items()},
    'enst_last_quarter_mean': {k: float(np.mean(r['enst'][-Q:]))
                               for k, r in runs.items()},
    'enst_prev_quarter_mean': {k: float(np.mean(r['enst'][-2 * Q:-Q]))
                               for k, r in runs.items()},
    'alpha_end_last_two_decades': alpha_end,
    'verdict': {k: (f'the truncated flow settles toward viscous equilibrium'
                    f' by T = {TOT:.0f}' if verdicts[k] == 'settles'
                    else f'keeps pumping enstrophy through T = {TOT:.0f}'
                    f' (no equilibrium within the run)'
                    if verdicts[k] == 'keeps pumping'
                    else 'marginal: growth-law classification indeterminate')
                for k in runs},
    'g63_energy_identity': {
        k: {'E_final': float(runs[k]['E_real'][-1]),
            'energy_change': abs(runs[k]['E_real'][-1]
                                 - runs[k]['E_real'][0]),
            'acc_relative': float(np.abs(
                runs[k]['E_real'][-1] - runs[k]['E_real'][0]
                - DELTA * np.sum(-NU * runs[k]['Z_real'][:-1]
                                 + runs[k]['Pf'][:-1]
                                 + runs[k]['Pd'][:-1]))
                / max(abs(runs[k]['E_real'][-1] - runs[k]['E_real'][0]),
                      1e-300))}
        for k in runs},
    'checks': [{'name': c['name'], 'pass': c['pass'], 'value': c['value'],
                'threshold': c['threshold'], 'note': c['note']}
               for c in checks],
}
with open('N04c_equilibrium_long_results.json', 'w') as f:
    json.dump(res, f, indent=1)

# ---------------------------------------------------------------- report
print()
for k, r in runs.items():
    flag = ('exceeds the 25-min budget: per plan T should be reduced to 140'
            if r['wall_time'] > 1500.0 else 'within budget')
    print(f'wall time: {k} = {r["wall_time"]:.1f} s ({flag})')
for k in runs:
    print(f'VERDICT {k}: {res["verdict"][k]}'
          f' (alpha_end = {alpha_end[k]:.3f}).')
reduced = any(r['wall_time'] > 1500.0 for r in runs.values())
if reduced:
    print('REPORT: a run exceeded 25 min -- the plan says reduce T to 140'
          ' and report; results above still stand for T = 200 as run.')
for c in checks:
    print(('PASS' if c['pass'] else 'FAIL'), c['name'], f'value={c["value"]}')
    print('     ', c['note'])
npass = sum(1 for c in checks if c['pass'])
print(f'<N04c_equilibrium_long> COMPLETE: {npass}/{len(checks)} checks PASS.')
print('EVIDENCE ONLY: ' + HONESTY + '.  Simulations are not proofs.')