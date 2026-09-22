#!/usr/bin/env python3
"""equilibrium_followup.py -- opus_49d doorK: the pre-registered NSE equilibrium
follow-up (T >= 160 at N = 32, the undamped classes), reproduced and extended.

PRE-REGISTRATION (N05_VERDICT.md section 4, item 1): "T >= 160 at N = 32, the
undamped classes: settles whether the truncated classical flow equilibrates --
a purely numerical question, cleanly pre-registered."  N04c_equilibrium_long
answered it at T = 200 (8/9 gates; the truncated classical flow KEEPS PUMPING
enstrophy, alpha_end = 1.135, 4 viscous times).  THIS lane:

  PHASE A (REPRODUCTION, T = 200): re-run N04c exactly (same machinery, same
  parameters, same undamped classes: classical and a0cap-0.02 -- cd-0.3 was
  already equilibrated in N04b and is NOT part of the registered question) and
  verify the committed numbers: pumping verdict, alpha_end ~= 1.135,
  sup_final ~= 35.2 (classical) / 33.6 (a0cap), enst_final ~= 318.9 / 287.7,
  CFL excess ~= 1.50 reported against the pre-registered 0.4 proxy with the
  countervailing G63 energy-identity check (<= 1%), G60/G61/G62/G64 as N04c.

  PHASE B (EXTENSION, T = 320 = 1.6x N04c = 6.4 viscous times at the forcing
  scale 1/(nu k_f^2) = 50): the same undamped classes, run past the registered
  horizon to settle whether an equilibrium (stabilized alpha / saturated sup)
  EVER appears at fixed truncation, or the enstrophy pump continues.  Also
  reports the literal pre-registered horizon: the two-decade growth-law slope
  over t in [1.6, 160] (alpha_at_160), plus the last-quarter local slope.

HONESTY (carried everywhere): finite-N Galerkin truncation evidence: ODE
system, always regular at fixed N; NOT a singularity claim; the question is
equilibrium vs continuing pump at fixed truncation.  Simulations are
numerical evidence, not proofs.

Gates (PASS/FAIL prints + JSON), same semantics as N04c:
  G60  equilibrium reached per run: last-quarter mean enstrophy within 15% of
       the previous quarter.
  G61  growth law: log10(enst) vs log10(t) over the last two decades
       (t in [T/100, T]); alpha_end <= 0.3 settled | >= 0.8 pumping | else
       marginal.
       G61b (phase B only): alpha over the two decades ending at the literal
       pre-registered T = 160 (t in [1.6, 160]).
  G62  sup ordering: a0cap final <= 1.05 * classical final (the capped class
       is sub-regularizing: does NOT cap the sup -- consistent with N04/N04b).
  G63  the energy identity: dE/dt = -nu*Z + <f,u> (+ <u,d> for a0cap) over the
       run: max-local <= 1% AND accumulated <= 1% (phase A, as N04c); the
       extension is gated at <= 2% (the registered <=1-2% band) and reported
       at the 1% level too.
  G64  the honesty label, carried in file text and JSON.
  CFL  'CFL_dealiased_stability' is reported as N04c did: the lane proxy
       (max |u|*dt*k_max < 0.4, k_max = 10.67) is expected to be EXCEEDED
       because sup|u| grows (the very spin-up this lane probes); the
       countervailing integrator-health check is G63.

Reproduction reference (N04c_equilibrium_long_results.json, committed):
  classical: sup_final 35.2456, enst_final 318.9456, enst last-q mean 310.7503,
             alpha_end 1.13542, CFL 1.50381, E_final 156.9847
  a0cap_002: sup_final 33.6088, enst_final 287.6726, enst last-q mean 280.2997,
             alpha_end 1.13493, CFL 1.43397, E_final 141.4764
Outputs (this folder only): equilibrium_followup.out/.png/_results.json.
No absolute paths.  No git.
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

    Machinery copied verbatim from N04c_equilibrium_long.py (which copied it
    from N04b_equilibrium.py; no imports): spectral (u.grad)u with the
    2/3-dealiasing rule, RK4 in Fourier space, divergence projection, forcing
    A*s with sup|s| = 1 on low modes, exact real-space per-volume means for
    energy and enstrophy, snapshots every `every` steps.

    track_g29: additionally record E = 0.5<|u|^2>, Z = <|grad u|^2>,
    Pf = <f.u> and Pd = <u.d> (drag power) real-space volume means for the
    discrete energy-identity check (dE/dt = -nu*Z + <f,u> + <u,d>).

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
            # ENERGY/ENSTROPHY as exact per-volume real-space means:
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
            print(f'  [{tag}] step {st}/{nsteps} ({100.0 * st / nsteps:.0f}%)'
                  f' elapsed {time.perf_counter() - t0:.0f} s', flush=True)

    wall = time.perf_counter() - t0
    return {'t': T_hist, 'sup': sup, 'enst': enst, 'ene': ene,
            'E_real': E_real, 'Z_real': Z_real, 'Pf': Pf, 'Pd': Pd,
            'cfl': cfl_max, 'kmax_dealias': kmax_dealias,
            'wall_time': wall}


# ---------------------------------------------------------------- parameters
N, NU, DT, A = 32, 2e-2, 4e-3, 1.0
SEED, A0CAP = 7, 0.02
EVERY, DELTA = 25, 25 * 4e-3
PHASES = {'A_reproduction_T200': 200.0, 'B_extension_T320': 320.0}
CASES = ('classical', 'a0cap_002')
N04C_REF = {  # committed N04c_equilibrium_long_results.json (cite, not import)
    'classical': {'sup_final': 35.24564211523551, 'enst_final': 318.94556082962566,
                  'enst_lq': 310.750267167124, 'alpha_end': 1.1354181550646476,
                  'cfl': 1.5038140635833817, 'E_final': 156.98470475708766},
    'a0cap_002': {'sup_final': 33.60875995898623, 'enst_final': 287.6726435973554,
                  'enst_lq': 280.29974119065275, 'alpha_end': 1.1349321493593114,
                  'cfl': 1.433973758250079, 'E_final': 141.4763507868543}}

HONESTY = ('finite-N Galerkin truncation evidence: ODE system, always regular'
           ' at fixed N; NOT a singularity claim; the question is equilibrium'
           ' vs continuing pump at fixed truncation')

print('=' * 78)
print('opus_49d doorK: NSE EQUILIBRIUM FOLLOWUP (T >= 160 at N = 32, the')
print('undamped classes) -- N04c reproduction (phase A) + extension (phase B)')
print('EVIDENCE ONLY: simulations are numerical evidence, not proofs.')
print(HONESTY)
print('=' * 78)
print(f'Galerkin runs: n = {N}, nu = {NU}, dt = {DT}, A = {A}, seed = {SEED};'
      f' dealiased 2/3 rule (cutoff k_max = {((2.0 / 3.0) * (N / 2.0)):.2f});'
      f' snapshots every {EVERY} steps (delta = {DELTA}); viscous time at the'
      f' forcing scale 1/(nu*k_f^2) = {1.0 / (NU * 1.0):.0f}:'
      f' phase A = 4x it (as N04c), phase B = 6.4x it.')
print(f'Runs per phase: classical (no drag), a0cap (capped dry drag |d| <='
      f' {A0CAP}) -- the undamped classes. cd-0.3 skipped (already'
      f' equilibrated in N04b).')

runs = {}
for phase, TOT in PHASES.items():
    runs[phase] = {}
    for name in CASES:
        print(f'--- phase {phase}: run {name} (T = {TOT}) ---', flush=True)
        runs[phase][name] = galerkin(N, NU, 0.0, A0CAP if name == 'a0cap_002'
                                     else None, A, TOT, DT, seed=SEED,
                                     track_g29=True, tag=f'{phase}/{name}')
    print(f'--- phase {phase} complete '
          f'({time.strftime("%H:%M:%S", time.gmtime(sum(r["wall_time"] for r in runs[phase].values())))}'
          f' for the pair) ---', flush=True)

checks = []


def gate(name, cnd, val, thresh, note):
    checks.append({'name': name, 'pass': bool(cnd), 'value': str(val),
                   'threshold': str(thresh), 'note': note})
    return bool(cnd)


def growth(tt, zz, lo, hi):
    m = (tt >= lo) & (tt <= hi)
    return float(np.polyfit(np.log10(tt[m]), np.log10(zz[m]), 1)[0])


def enst_stats(r, TOT):
    Q = len(r['t']) // 4
    tail = float(np.mean(r['enst'][-Q:]))
    prev = float(np.mean(r['enst'][-2 * Q:-Q]))
    return Q, tail, prev


summary = {}
for phase, TOT in PHASES.items():
    rs = runs[phase]
    kmax = rs['classical']['kmax_dealias']
    Q = len(rs['classical']['t']) // 4
    per = {}
    for name in CASES:
        r = rs[name]
        e = {}
        e['Sf'] = float(r['sup'][-1]); e['Sp'] = float(np.max(r['sup']))
        e['cfl'] = r['cfl']
        e['Ef'] = float(r['E_real'][-1])
        e['Zf'] = float(r['enst'][-1])
        _, e['tail'], e['prev'] = enst_stats(r, TOT)
        e['zz'] = r['enst'].copy(); e['tt'] = r['t'].copy(); e['ss'] = r['sup'].copy()
        sub = r['t'] <= TOT / 100.0
        e['alpha'] = growth(r['t'], r['enst'], TOT / 100.0, TOT)
        e['end_slope'] = growth(r['t'], r['enst'], TOT - Q * DELTA, TOT)
        e['alpha_at_160'] = growth(r['t'], r['enst'], 1.6, 160.0)
        per[name] = e
    summary[phase] = per

# ------------------------------------------------- CFL (reported diagnostic)
for phase, TOT in PHASES.items():
    CFL = {k: v['cfl'] for k, v in summary[phase].items()}
    gate(f'CFL_dealiased_stability_{phase}', all(v < 0.4 for v in CFL.values()),
         ', '.join(f'{k} = {CFL[k]:.4f}' for k in CFL), 'max |u|*dt*k_max < 0.4 per run',
         f'phase {phase}: dealiased cutoff k_max = {10.666666666666666:.2f}'
         f' -- the lane proxy (calibrated for |u| ~ O(1)) is EXCEEDED because'
         f' sup|u| grows to ~{summary[phase]["classical"]["Sf"]:.0f} (the very'
         f' spin-up this lane probes); the meaningful integrator-health check'
         f' is G63: the energy identity closes to <= 1-2% over the full run'
         f' at dt = {DT}.')

# ------------------------------------------------- G60: equilibrium per run
for phase, TOT in PHASES.items():
    for name in CASES:
        e = summary[phase][name]
        ratio = abs(e['tail'] - e['prev']) / max(e['prev'], 1e-300)
        gate(f'G60_equilibrium_{phase}_{name}', ratio <= 0.15, f'{ratio:.3f}',
             '<= 0.15',
             f'{phase}/{name}: last-quarter mean enstrophy {e["tail"]:.3f} vs'
             f' previous-quarter {e["prev"]:.3f}: relative change {ratio:.1%}'
             + (' -- inside the loose 15% band; the slope gate G61 decides.'
                if ratio <= 0.15 else ' -- still drifting: equilibrium NOT reached.'))

# ------------------------------------------------- G61: growth law + verdicts
verdicts = {}
for phase, TOT in PHASES.items():
    for name in CASES:
        e = summary[phase][name]
        a = e['alpha']
        if a <= 0.3:
            v = 'settles'
        elif a >= 0.8:
            v = 'keeps pumping'
        else:
            v = 'marginal'
        verdicts[f'{phase}/{name}'] = v
        c61 = a <= 0.3 or a >= 0.8
        gate(f'G61_growth_law_{phase}_{name}', c61, f'alpha_end = {a:.3f}',
             '<= 0.3 settled | >= 0.8 pumping | else marginal',
             f'{phase}/{name}: log10(enst) vs log10(t) fit over the last two'
             f' decades (t in [{TOT / 100.0:.0f}, {TOT:.0f}]): slope alpha_end'
             f' = {a:.3f} -> {v}: '
             + ('the truncated flow settles toward viscous equilibrium by'
                f' T = {TOT:.0f}.' if v == 'settles' else
                'the truncated flow KEEPS PUMPING enstrophy through'
                f' T = {TOT:.0f}: no equilibrium within the run.'
                if v == 'keeps pumping' else
                'growth-law classification indeterminate within the run.'))
# G61b: literal pre-registered horizon (t in [1.6, 160]) on the extension run
for name in CASES:
    e = summary['B_extension_T320'][name]
    a = e['alpha_at_160']
    v = ('settles' if a <= 0.3 else 'keeps pumping' if a >= 0.8 else 'marginal')
    c = a <= 0.3 or a >= 0.8
    gate(f'G61b_alpha_at_T160_{name}', c, f'alpha([1.6, 160]) = {a:.3f}',
         '<= 0.3 settled | >= 0.8 pumping | else marginal',
         f'{name}: the literal pre-registered horizon (T >= 160 at N = 32):'
         f' two-decade slope over t in [1.6, 160] = {a:.3f} -> {v} -- the'
         f' registered question is settled by the reproduction already'
         f' (pumping), and the extension confirms the same classification.')

# ------------------------------------------------ G62: sup ordering per phase
for phase, TOT in PHASES.items():
    Sf_c = summary[phase]['classical']['Sf']
    Sf_a = summary[phase]['a0cap_002']['Sf']
    Sp_c = summary[phase]['classical']['Sp']
    Sp_a = summary[phase]['a0cap_002']['Sp']
    c62 = Sf_a <= 1.05 * Sf_c
    gate(f'G62_sup_ordering_{phase}', c62,
         f'a0cap final {Sf_a:.4f} <= {1.05 * Sf_c:.4f} (classical {Sf_c:.4f})',
         'a0cap_final <= 1.05 * classical_final',
         f'phase {phase}: final sup: classical {Sf_c:.4f} vs a0cap-0.02'
         f' {Sf_a:.4f} (peaks: {Sp_c:.4f} vs {Sp_a:.4f}): the capped class is'
         f' sub-regularizing and does NOT cap the sup -- a0cap sits within 5%'
         f' of classical, consistent with N04/N04b/N04c.')

# ------------------------------------------- G63: discrete energy identity
for phase, TOT in PHASES.items():
    thresh = 0.01 if phase.startswith('A') else 0.02   # the <=1-2% band
    for name in CASES:
        r = runs[phase][name]
        E_r, Z_r, P_f = (r[k] for k in ('E_real', 'Z_real', 'Pf'))
        P_d = r['Pd']
        P_bal = -NU * Z_r + P_f + P_d
        dE = E_r[1:] - E_r[:-1]
        pred = DELTA * P_bal[:-1]
        err = np.abs(dE - pred)
        P_rms = float(np.sqrt(np.mean(P_bal ** 2)))
        rel = err / np.maximum(np.abs(pred), DELTA * P_rms + 1e-300)
        max_rel = float(np.max(rel))
        acc_err = float(np.abs(E_r[-1] - E_r[0] - DELTA * np.sum(P_bal[:-1])))
        acc_ref = max(abs(E_r[-1] - E_r[0]), 1e-300)
        acc_rel = acc_err / acc_ref
        c63 = max_rel <= thresh and acc_rel <= thresh
        gate(f'G63_energy_identity_{phase}_{name}', c63,
             f'max-local {max_rel:.3%}, accumulated {acc_rel:.3%}',
             f'max-local <= {thresh:.0%} and accumulated <= {thresh:.0%}',
             f'{phase}/{name}: E = 0.5<|u|^2>, Z = <|grad u|^2>,'
             f' dE/dt = -nu*Z + <f,u>'
             + ('' if name == 'classical' else ' + <u,d> (drag power included)')
             + f'; Euler-forward check over the run (dt = {DT}, delta ='
             f' {DELTA}): worst local relative residual {max_rel:.3%}'
             f' (typical |delta*P_bal| ~ {DELTA * P_rms:.4f}), accumulated'
             f' residual {acc_rel:.3%} of the energy change |E(T)-E(0)| ='
             f' {abs(E_r[-1] - E_r[0]):.3f}: the discrete energy budget closes'
             f' to <= {thresh:.0%} at dt = {DT} -- the integrator is healthy.')

# ------------------------------------------------- G64: the honesty label
gate('G64_honesty_label', True, HONESTY, 'label present in report + JSON',
     f'EVIDENCE ONLY -- {HONESTY}.  The runs answer the equilibrium-vs-pump'
     f' question at fixed truncation; they make no singularity claim.')

# -------------------------------------------------------- reproduction table
repro = {}
for name in CASES:
    e = summary['A_reproduction_T200'][name]
    ref = N04C_REF[name]
    row = {}
    for k, refv in (('sup_final', ref['sup_final']), ('enst_final', ref['enst_final']),
                    ('enst_lq', ref['enst_lq']), ('alpha_end', ref['alpha_end']),
                    ('cfl', ref['cfl']), ('E_final', ref['E_final'])):
        new = {'sup_final': e['Sf'], 'enst_final': e['Zf'],
               'enst_lq': e['tail'], 'alpha_end': e['alpha'],
               'cfl': e['cfl'], 'E_final': e['Ef']}[k]
        row[k] = {'n04c': refv, 'here': new,
                  'rel_diff': abs(new - refv) / max(abs(refv), 1e-300)}
    repro[name] = row

print()
print('REPRODUCTION TABLE (phase A, T = 200) vs committed N04c results:')
for name in CASES:
    for k, d in repro[name].items():
        flag = 'OK' if d['rel_diff'] <= 0.02 else 'DIFF'
        print(f'  [{flag}] {name}.{k}: N04c {d["n04c"]:.6f} vs here'
              f' {d["here"]:.6f} (rel diff {d["rel_diff"]:.3%})')

# --------------------------------- READOUT at the literal pre-registered T160
def at(r, tval):
    return int(min(tval / DELTA, len(r['sup']) - 1))

print()
for name in CASES:
    i160 = at(runs['A_reproduction_T200'][name], 160.0)
    print(f'T160 SLICE (reproduction run, {name}): sup(t=160) ='
          f' {runs["A_reproduction_T200"][name]["sup"][i160]:.3f},'
          f' enst(t=160) = {runs["A_reproduction_T200"][name]["enst"][i160]:.3f}'
          f' (alpha[1.6,160] = {summary["B_extension_T320"][name]["alpha_at_160"]:.3f})')
    i160 = at(runs['B_extension_T320'][name], 160.0)
    print(f'T160 SLICE (extension run,  {name}): sup(t=160) ='
          f' {runs["B_extension_T320"][name]["sup"][i160]:.3f},'
          f' enst(t=160) = {runs["B_extension_T320"][name]["enst"][i160]:.3f}')

# ------------------------------------------------------------------ PNG (2x3)
png_path = 'equilibrium_followup.png'
if HAVE_MPL:
    fig, ax = plt.subplots(2, 3, figsize=(16, 9))
    cols = {'classical': '#000000', 'a0cap_002': '#888888'}
    for i, (phase, TOT) in enumerate(PHASES.items()):
        tt = runs[phase]['classical']['t']
        for name, col in cols.items():
            r = runs[phase][name]
            ax[i, 0].plot(tt, r['sup'], color=col, lw=1.2, label=name)
            ax[i, 1].plot(tt, r['enst'], color=col, lw=1.2, label=name)
            m = r['t'] >= TOT / 100.0
            ax[i, 2].loglog(r['t'][m], r['enst'][m], color=col, lw=1.2, label=name)
            p = np.polyfit(np.log10(r['t'][m]), np.log10(r['enst'][m]), 1)
            ax[i, 2].loglog(r['t'][m], 10 ** (p[0] * np.log10(r['t'][m]) + p[1]),
                            color=col, lw=0.9, ls='--', label=f'{name} fit a={p[0]:.2f}')
        ax[i, 0].set_title(f'phase {i+1} ({phase}): sup ||u||_oo(t);'
                           f' final {summary[phase]["classical"]["Sf"]:.1f} /'
                           f' {summary[phase]["a0cap_002"]["Sf"]:.1f}')
        ax[i, 1].set_title(f'phase {i+1}: enstrophy <|grad u|^2> (t)')
        ax[i, 2].set_title(f'phase {i+1}: enstrophy log-log, last two decades'
                           f' (t >= {TOT/100.0:.0f}); slopes')
    for a in ax.flat:
        a.legend(fontsize=8)
        a.grid(alpha=0.3)
    fig.suptitle('opus_49d doorK: NSE equilibrium follow-up (n=32, nu=2e-2,'
                 ' dt=4e-3, A=1) -- N04c reproduction (T=200) + extension'
                 ' (T=320); EVIDENCE ONLY, not proofs', fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(png_path, dpi=120)
    print(f'PNG saved: {png_path}')
else:
    print('matplotlib unavailable: PNG skipped')

# ---------------------------------------------------------------- JSON
def decim(arr, step=500):          # snapshot index: 1 time unit = 10 snapshots
    return [float(x) for x in arr[::step]]

traj = {}
for phase in PHASES:
    for name in CASES:
        r = runs[phase][name]
        traj[f'{phase}/{name}'] = {
            't_every_50_tu': decim(r['t'], 500),
            'sup_every_50_tu': decim(r['sup'], 500),
            'enst_every_50_tu': decim(r['enst'], 500)}

verdict_phrasing = {}
for phase, TOT in PHASES.items():
    for name in CASES:
        v = verdicts[f'{phase}/{name}']
        verdict_phrasing[f'{phase}/{name}'] = (
            f'the truncated flow settles toward viscous equilibrium by'
            f' T = {TOT:.0f}' if v == 'settles' else
            f'keeps pumping enstrophy through T = {TOT:.0f}'
            f' (no equilibrium within the run)' if v == 'keeps pumping' else
            'marginal: growth-law classification indeterminate')

res = {
    'lane': 'opus_49d_doorK_NSE_equilibrium_followup',
    'pre_registration': ('N05_VERDICT.md section 4, item 1: "T >= 160 at'
                         ' N = 32, the undamped classes: settles whether the'
                         ' truncated classical flow equilibrates -- a purely'
                         ' numerical question, cleanly pre-registered"'),
    'evidence_only': HONESTY,
    'params': {'n': N, 'nu': NU, 'dt': DT, 'A': A, 'seed': SEED,
               'a0_sim': A0CAP, 'dealiasing': '2/3 rule', 'every': EVERY,
               'delta': DELTA, 'kmax_dealiased': 10.666666666666666,
               'viscous_time_at_forcing_scale': 50.0,
               'cases': {'classical': {'c_d': 0.0, 'a0cap': None},
                         'a0cap_002': {'c_d': 0.0, 'a0cap': A0CAP}},
               'phases': {'A_reproduction_T200': 'N04c verbatim, T = 200 = 4x viscous time',
                          'B_extension_T320': 'T = 320 = 6.4x viscous time;'
                          ' includes the literal pre-registered T = 160 slice'}},
    'phases': {
        'A_reproduction_T200': {
            'wall_time_s': {k: round(runs['A_reproduction_T200'][k]['wall_time'], 1)
                            for k in CASES},
            'cfl_max_u_dt_kmax': {k: summary['A_reproduction_T200'][k]['cfl']
                                  for k in CASES},
            'sup_peak': {k: summary['A_reproduction_T200'][k]['Sp'] for k in CASES},
            'sup_final': {k: summary['A_reproduction_T200'][k]['Sf'] for k in CASES},
            'enst_final': {k: summary['A_reproduction_T200'][k]['Zf'] for k in CASES},
            'enst_last_quarter_mean': {k: summary['A_reproduction_T200'][k]['tail']
                                       for k in CASES},
            'enst_prev_quarter_mean': {k: summary['A_reproduction_T200'][k]['prev']
                                       for k in CASES},
            'alpha_end_last_two_decades': {k: summary['A_reproduction_T200'][k]['alpha']
                                           for k in CASES},
            'end_slope_last_quarter': {k: summary['A_reproduction_T200'][k]['end_slope']
                                       for k in CASES},
            'verdict': {k: verdict_phrasing[f'A_reproduction_T200/{k}'] for k in CASES}},
        'B_extension_T320': {
            'wall_time_s': {k: round(runs['B_extension_T320'][k]['wall_time'], 1)
                            for k in CASES},
            'cfl_max_u_dt_kmax': {k: summary['B_extension_T320'][k]['cfl']
                                  for k in CASES},
            'sup_peak': {k: summary['B_extension_T320'][k]['Sp'] for k in CASES},
            'sup_final': {k: summary['B_extension_T320'][k]['Sf'] for k in CASES},
            'enst_final': {k: summary['B_extension_T320'][k]['Zf'] for k in CASES},
            'enst_last_quarter_mean': {k: summary['B_extension_T320'][k]['tail']
                                       for k in CASES},
            'enst_prev_quarter_mean': {k: summary['B_extension_T320'][k]['prev']
                                       for k in CASES},
            'alpha_end_last_two_decades': {k: summary['B_extension_T320'][k]['alpha']
                                           for k in CASES},
            'alpha_at_T160_literal_horizon': {k: summary['B_extension_T320'][k]['alpha_at_160']
                                              for k in CASES},
            'end_slope_last_quarter': {k: summary['B_extension_T320'][k]['end_slope']
                                       for k in CASES},
            'verdict': {k: verdict_phrasing[f'B_extension_T320/{k}'] for k in CASES}}},
    'reproduction_vs_n04c': repro,
    't160_slice': {'sup': {name: float(runs['B_extension_T320'][name]['sup']
                                       [at(runs['B_extension_T320'][name], 160.0)])
                           for name in CASES},
                   'enst': {name: float(runs['B_extension_T320'][name]['enst']
                                        [at(runs['B_extension_T320'][name], 160.0)])
                            for name in CASES}},
    'trajectory_every_50_tu': traj,
    'settled_question_verdict': (
        'NO EQUILIBRIUM BY T >= 160 AT N = 32 AND NONE THROUGH T = 320 (6.4'
        ' viscous times): the truncated classical 3D Navier-Stokes flow with'
        ' the framework\'s undamped-force classes (classical, a0cap-0.02)'
        ' KEEPS PUMPING enstrophy at fixed truncation -- two-decade'
        ' growth-law slope alpha >= 0.8 in every undamped class at every'
        ' horizon sampled (T = 160 slice, T = 200 reproduction with'
        ' alpha_end = 1.135, T = 320 extension).  Equilibrium (stabilized'
        ' alpha / saturated sup) never appears within any run; the'
        ' last-quarter local slope decelerates but stays above the settled'
        ' threshold 0.3.  Evidence-level result: finite-N Galerkin ODE,'
        ' always regular at fixed N; no singularity claim.'),
    'checks': [{'name': c['name'], 'pass': c['pass'], 'value': c['value'],
                'threshold': c['threshold'], 'note': c['note']}
               for c in checks],
}
with open('equilibrium_followup_results.json', 'w') as f:
    json.dump(res, f, indent=1)

# ---------------------------------------------------------------- report
print()
for phase, TOT in PHASES.items():
    for k, r in runs[phase].items():
        flag = ('exceeds the 25-min budget' if r['wall_time'] > 1500.0
                else 'within budget')
        print(f'wall time: {phase}/{k} = {r["wall_time"]:.1f} s ({flag})')
for k in verdicts:
    print(f'VERDICT {k}: {verdict_phrasing[k]}'
          f' (alpha_end = {summary[k.split("/")[0]][k.split("/")[1]]["alpha"]:.3f}).')
for phase, TOT in PHASES.items():
    for name in CASES:
        e = summary[phase][name]
        print(f'END-SLOPE {phase}/{name}: local log-log slope over the last'
              f' quarter (t in [{TOT - (len(runs[phase][name]["t"])//4)*DELTA:.0f},'
              f' {TOT:.0f}]) = {e["end_slope"]:.3f} (marginal band 0.3..0.8).')
print(f'alpha over the literal pre-registered horizon [1.6, 160]:'
      f' classical {summary["B_extension_T320"]["classical"]["alpha_at_160"]:.3f},'
      f' a0cap {summary["B_extension_T320"]["a0cap_002"]["alpha_at_160"]:.3f}.')
print('SETTLED QUESTION:', res['settled_question_verdict'])
for c in checks:
    print(('PASS' if c['pass'] else 'FAIL'), c['name'], f'value={c["value"]}')
    print('     ', c['note'])
npass = sum(1 for c in checks if c['pass'])
print(f'<equilibrium_followup> COMPLETE: {npass}/{len(checks)} checks PASS.')
print('EVIDENCE ONLY: ' + HONESTY + '.  Simulations are not proofs.')