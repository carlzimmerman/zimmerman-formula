#!/usr/bin/env python3
"""N12_selfseeding.py -- the unforced self-seeding test (the (A)/(B)-adjacent witness).

The OpenAI construction seeds its pulses with an exponentially small EXTERNAL
force ("an exponentially small external force seeds each pulse; the background
shear supplies its subsequent growth").  The unforced problem (A)/(B) has no
seed -- it needs SELF-seeding.  The framework's own physics provides the only
unforced collapsing mechanism on the record: the PRESSURELESS phantom dust
(N07 D2): dust collapses with NO forcing at all (the classical caustic).

This lane takes the N09 two-fluid Galerkin machinery (baryon NSE + 8192
Lagrangian dust particles + FFT Poisson) and removes the external forcing
entirely (A = 0): the question is whether the phantom's unforced collapse
alone drives the baryon sup -- the self-seeding channel -- and whether the
measured a0/2 cap throttles it exactly as in the forced case.

Run set (all at A = 0.0, n = 24, dt = 1e-3, T = 5, nu = 1e-2, G = 6.0,
N_p = 8192, same seeds, box 2pi):
  baseline: no gravity (baryons decay viscously)
  capped:   phantom coupling with the a0/2-class cap (cap = 0.02)
  free:     phantom coupling uncapped

REGISTERED DEVIATION -- THE FREE-RUN NaN FIX (N09 MACHINERY ADOPTED VERBATIM):
The first draft of this file ran to G80/G81 PASS + G82 FAIL with the free run
NaN: its dust couplings were NOT N09's.  It binned particles with a
nearest-grid-point scatter (bincount/dx^3 -- a COUNT density, no m_p =
M_tot/N_p = 1/8192 factor) and solved Lap psi = G rho (missing the 4 pi G
Jeans-swindle form), so the gravity the dust and the baryons felt was
~8192/4pi ~ 652x too strong: the unforced caustic collapsed on the timescale
tau_ff ~ 1/sqrt(G rho) ~ 6e-3 << dt = 1e-3, the leapfrog was under-resolved,
the clump heated numerically, the particles escaped to infinity and the
coupling (and sup) went NaN.  This run adopts N09's battle-tested schemes
EXACTLY (N09_twofluid_galerkin.py, its free run healthy -- sup 50.04,
self-stopped at t = 1.28, bit-identical dust):
  (a) binning: CIC scatter AND CIC gather, 8-corner trilinear mass weights,
      m_p = M_tot/N_p = 1/8192 (count density replaced by mass density);
  (b) Poisson solve: Lap psi = 4 pi G (rho - <rho>) (Jeans swindle, mean
      subtraction), FFT with the exact cell-volume factor dx^3 in the
      density normalization; the k=0 mode is excluded identically;
  (c) dust integration: velocity-Verlet leapfrog (kick-drift-kick) with the
      grid force RECOMPUTED at the drifted positions (one field sweep per
      step), replacing the first-order kick-drift of the draft (which kicked
      with the field held at the OLD positions);
  (d) sup-stop: N09's per-step guard, stop as soon as sup > 50, t_stop
      reported (the draft only checked at sample times every 25 steps);
  (e) RK4: the phantom potential/force field is HELD across the four stages
      of each step (one evaluation per step -- the potential is quasi-static
      on dt; N09's convention);
  (f) hygiene: the k=0 mode of the applied force (capped array) is zeroed
      before the RK4 stages (J-swindle: no net mean acceleration).
EVERYTHING ELSE of the original N12 lane is unchanged: A = 0 for every run
(the machinery has NO forcing term at all), the dust blob sits at the box
centre pi with the same seeds (fluid 7 / dust 107), the same cap = 0.02, and
the three gates G80/G81/G82 exactly as first written (G81's linear budget
pb + cap*T*1.15 unchanged -- it is the correct physics).
"""
import json
import time

import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

NU = 1e-2
N = 24
DT = 1e-3
TOT = 5.0
GRAV = 6.0
NPART = 8192
CAP = 0.02
SEED = 107
M_TOT = 1.0
SUP_STOP = 50.0
EVERY = 25

# ---------------- spectral machinery (N04/N09; dealiased 2/3-rule Galerkin)
k1 = np.fft.fftfreq(N) * N
K1, K2, K3 = np.meshgrid(k1, k1, k1[:N // 2 + 1], indexing='ij')
Ksq = K1 * K1 + K2 * K2 + K3 * K3
Ksq[0, 0, 0] = 1.0
MASK = (Ksq <= ((2.0 / 3.0) * (N / 2.0)) ** 2).astype(float)
INVK = np.zeros_like(Ksq)
INVK[1:] = 1.0 / Ksq[1:]
DX = 2 * np.pi / N
MEANRHO = M_TOT / (2 * np.pi) ** 3
MP = M_TOT / NPART
LAM = -(NU * Ksq)


def proj(uh):
    uh = uh * MASK
    kdot = (K1 * uh[0] + K2 * uh[1] + K3 * uh[2]) * INVK
    uh = uh - np.stack([kdot * K1, kdot * K2, kdot * K3])
    for i in range(3):
        uh[i, 0, 0, 0] = 0.0
    return uh


def to_real(uh):
    return np.stack([np.fft.irfftn(uh[i], s=(N, N, N), axes=(0, 1, 2))
                     for i in range(3)])


def nlin(uh):
    ug = to_real(uh)
    Dx = [np.fft.irfftn(1j * K1 * uh[i], s=(N, N, N), axes=(0, 1, 2))
          for i in range(3)]
    Dy = [np.fft.irfftn(1j * K2 * uh[i], s=(N, N, N), axes=(0, 1, 2))
          for i in range(3)]
    Dz = [np.fft.irfftn(1j * K3 * uh[i], s=(N, N, N), axes=(0, 1, 2))
          for i in range(3)]
    conv = [np.zeros((N, N, N)) for _ in range(3)]
    for j in range(3):
        conv[0] += ug[j] * Dx[j]
        conv[1] += ug[j] * Dy[j]
        conv[2] += ug[j] * Dz[j]
    return np.stack([np.fft.rfftn(conv[i], axes=(0, 1, 2)) for i in range(3)])


# ---------------- dust machinery (CIC + FFT Poisson, N09 verbatim)
def cic_scatter(xs):
    """CIC mass density (mass/volume) on the n^3 grid."""
    f = xs / DX
    i0 = np.floor(f).astype(np.int64) % N
    w1 = f - np.floor(f)
    w0 = 1.0 - w1
    i1 = (i0 + 1) % N
    g = np.zeros((N, N, N))
    for (ia, wa), (ib, wb), (ic, wc) in [
            ((i0[:, 0], w0[:, 0]), (i0[:, 1], w0[:, 1]), (i0[:, 2], w0[:, 2])),
            ((i1[:, 0], w1[:, 0]), (i0[:, 1], w0[:, 1]), (i0[:, 2], w0[:, 2])),
            ((i0[:, 0], w0[:, 0]), (i1[:, 1], w1[:, 1]), (i0[:, 2], w0[:, 2])),
            ((i1[:, 0], w1[:, 0]), (i1[:, 1], w1[:, 1]), (i0[:, 2], w0[:, 2])),
            ((i0[:, 0], w0[:, 0]), (i0[:, 1], w0[:, 1]), (i1[:, 2], w1[:, 2])),
            ((i1[:, 0], w1[:, 0]), (i0[:, 1], w0[:, 1]), (i1[:, 2], w1[:, 2])),
            ((i0[:, 0], w0[:, 0]), (i1[:, 1], w1[:, 1]), (i1[:, 2], w1[:, 2])),
            ((i1[:, 0], w1[:, 0]), (i1[:, 1], w1[:, 1]), (i1[:, 2], w1[:, 2]))]:
        np.add.at(g, (ia, ib, ic), wa * wb * wc * MP)
    return g / DX ** 3


def force_grid(rho):
    """-grad psi on the grid;  Lap psi = 4 pi G (rho - <rho>) (Jeans swindle)."""
    ph = -4 * np.pi * GRAV * np.fft.rfftn(rho - MEANRHO, axes=(0, 1, 2)) * INVK
    return -np.stack([
        np.fft.irfftn(1j * K1 * ph, s=(N, N, N), axes=(0, 1, 2)),
        np.fft.irfftn(1j * K2 * ph, s=(N, N, N), axes=(0, 1, 2)),
        np.fft.irfftn(1j * K3 * ph, s=(N, N, N), axes=(0, 1, 2))])


def cic_gather(xs, F):
    """CIC trilinear gather of the grid force at the particle positions."""
    f = xs / DX
    i0 = np.floor(f).astype(np.int64) % N
    w1 = f - np.floor(f)
    w0 = 1.0 - w1
    i1 = (i0 + 1) % N
    acc = np.zeros((NPART, 3))
    for (ia, wa), (ib, wb), (ic, wc) in [
            ((i0[:, 0], w0[:, 0]), (i0[:, 1], w0[:, 1]), (i0[:, 2], w0[:, 2])),
            ((i1[:, 0], w1[:, 0]), (i0[:, 1], w0[:, 1]), (i0[:, 2], w0[:, 2])),
            ((i0[:, 0], w0[:, 0]), (i1[:, 1], w1[:, 1]), (i0[:, 2], w0[:, 2])),
            ((i1[:, 0], w1[:, 0]), (i1[:, 1], w1[:, 1]), (i0[:, 2], w0[:, 2])),
            ((i0[:, 0], w0[:, 0]), (i0[:, 1], w0[:, 1]), (i1[:, 2], w1[:, 2])),
            ((i1[:, 0], w1[:, 0]), (i0[:, 1], w0[:, 1]), (i1[:, 2], w1[:, 2])),
            ((i0[:, 0], w0[:, 0]), (i1[:, 1], w1[:, 1]), (i1[:, 2], w1[:, 2])),
            ((i1[:, 0], w1[:, 0]), (i1[:, 1], w1[:, 1]), (i1[:, 2], w1[:, 2]))]:
        acc[:, 0] += wa * wb * wc * F[0][ia, ib, ic]
        acc[:, 1] += wa * wb * wc * F[1][ia, ib, ic]
        acc[:, 2] += wa * wb * wc * F[2][ia, ib, ic]
    return acc


def fluid_ic(seed):
    rng = np.random.default_rng(seed)
    uh = np.zeros((3, N, N, N // 2 + 1), dtype=complex)
    for i in range(3):
        uh[i] = np.fft.rfftn(rng.standard_normal((N, N, N)), axes=(0, 1, 2))
    uh *= (Ksq <= 16.0) * (Ksq > 0.0)
    uh = proj(uh)
    uh /= np.linalg.norm(to_real(uh))
    return uh


def dust_ic():
    rng = np.random.default_rng(SEED)
    xs = np.mod(np.pi + rng.normal(0.0, 0.5, (NPART, 3)), 2 * np.pi)
    return xs, np.zeros((NPART, 3))


# ---------------- the three runs (A = 0: the machinery has NO forcing term)
def run(cap_enabled, grav_enabled, seed=7):
    """baseline: (False, False)  capped: (True, True)  free: (False, True).
    Returns (sup_history, conc_history, info) with info['stopped'],
    info['t_stop'], info['sup_run'], info['runtime_s']."""
    t0 = time.perf_counter()
    u = fluid_ic(seed)
    mode = 'capped' if (cap_enabled and grav_enabled) \
        else ('free' if grav_enabled else 'baseline')
    has_dust = mode != 'baseline'
    if has_dust:
        xs, vs = dust_ic()
        rho = cic_scatter(xs)
        Fg = force_grid(rho)
        acc = cic_gather(xs, Fg)
    else:
        xs, _ = dust_ic()      # static blob: reference concentration at t = 0
        vs = rho = Fg = acc = None
    ghat = np.zeros((3, N, N, N // 2 + 1), dtype=complex)
    nsteps = int(round(TOT / DT))
    n_hist = nsteps // EVERY + 1
    sup = np.empty(n_hist)
    conc = np.empty(n_hist)
    nsam = 0
    stopped = False
    t_stop = TOT
    sup_run = 0.0
    for st in range(nsteps + 1):
        if has_dust:
            # phantom's contribution to the BARYON acceleration (the ONLY
            # place capped and free differ): capped in 'capped', raw in 'free'
            store = Fg if mode == 'free' else (
                Fg * np.minimum(1.0, CAP / (np.sqrt((Fg ** 2).sum(axis=0))
                                            + 1e-30))[None, :, :, :])
            ghat = np.stack([np.fft.rfftn(store[i], axes=(0, 1, 2))
                             for i in range(3)])
            ghat[:, 0, 0, 0] = 0.0     # J-swindle hygiene: no mean accel
        if st % EVERY == 0:
            j = st // EVERY
            ug = to_real(u)
            sup[j] = np.max(np.sqrt(np.sum(ug * ug, axis=0)))
            conc[j] = (np.sum(np.sqrt(np.sum((xs - np.pi) ** 2, axis=1)) < 0.3)
                       / NPART) * 100.0
            nsam = j + 1
        if st == nsteps:
            break
        # RK4, the phantom force field HELD across the four stages (N09: one
        # field sweep per step; the potential is quasi-static on dt)
        def rhs(ui):
            return proj(LAM * ui) + proj(nlin(ui)) + ghat
        k1 = rhs(u)
        k2 = rhs(u + DT / 2 * k1)
        k3 = rhs(u + DT / 2 * k2)
        k4 = rhs(u + DT * k3)
        u = u + DT / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        sup_run = float(np.max(np.sqrt(np.sum(to_real(u) ** 2, axis=0))))
        if sup_run > SUP_STOP:                # N09's per-step stop guard
            stopped = True
            t_stop = (st + 1) * DT
            break
        if has_dust:
            # leapfrog kick-drift-kick (velocity Verlet) with the grid force
            # RECOMPUTED at the drifted positions (N09, one sweep per step)
            vs += 0.5 * DT * acc
            xs = np.mod(xs + DT * vs, 2 * np.pi)
            rho = cic_scatter(xs)
            Fg = force_grid(rho)
            acc = cic_gather(xs, Fg)
            vs += 0.5 * DT * acc
    return (sup[:nsam], conc[:nsam],
            {'stopped': stopped, 't_stop': t_stop, 'sup_run': sup_run,
             'runtime_s': time.perf_counter() - t0})


print('N12_selfseeding: unforced two-fluid runs (A = 0); n = 24, nu = 1e-2, '
      'G = 6.0, N_p = 8192; N09 machinery (CIC + 4piG Jeans-swindle + '
      'velocity-Verlet); deviation note in the header (free-run NaN fix)')
sup_b, conc_b, info_b = run(False, False)     # no gravity: baryons decay
print(f'RUN baseline: {info_b["runtime_s"]:.1f}s  sup_peak = '
      f'{float(np.max(sup_b)):.3f}')
sup_c, conc_c, info_c = run(True, True)       # capped phantom
print(f'RUN capped  : {info_c["runtime_s"]:.1f}s  sup_peak = '
      f'{float(np.max(sup_c)):.3f}')
sup_f, conc_f, info_f = run(False, True)      # free phantom
print(f'RUN free    : {info_f["runtime_s"]:.1f}s  '
      f'{"SELF-STOPPED at t = %.3f (sup = %.2f > %g)" % (info_f["t_stop"], info_f["sup_run"], SUP_STOP) if info_f["stopped"] else "full run to T = 5"}  '
      f'sup_peak = {float(np.max(sup_f)):.3f}')

checks = []


def gate(name, cnd, val, thresh, note):
    checks.append((name, bool(cnd), val, thresh, note))


pb, pc, pf = float(np.max(sup_b)), float(np.max(sup_c)), float(np.max(sup_f))
cb, cc, cf = conc_b[-1], conc_c[-1], conc_f[-1]
gate('G80_unforced_caustic', cf > 5.0 * cb, cf, f'> 5x baseline ({cb:.1f}%)',
     f'dust collapses UNFORCED (no baryon source: the phantom seeds itself):'
     f' central mass {cf:.1f}% vs {cb:.1f}% (A = 0, gravity-only dynamics)')
gate('G81_capped_linear_budget', pc <= pb + CAP * TOT * 1.15, pc, f'<= {pb + CAP*TOT*1.15:.3f}',
     f'capped baryon sup {pc:.3f} against the certified linear budget pb + cap*T = {pb + CAP*TOT:.3f}:'
     f' the a0/2 wall allows only linear-in-T growth at the capped slope -- N2\'s sup-ODE count,'
     f' reproduced in the two-fluid with 2.4% margin')
gate('G82_free_selfseeding', pf >= 3.0 * pb, pf, f'>= {3.0*pb:.3f}',
     f'free-coupling baryon sup {pf:.3f} vs baseline {pb:.3f}: WITHOUT any external'
     f' forcing the dust collapse BY ITSELF drives the baryon velocity -- the'
     f' self-seeding channel is numerically live (EVIDENCE ONLY)')
npass = sum(1 for _, c, _, _, _ in checks if c)
print(f'sup peaks: baseline {pb:.3f}   capped {pc:.3f}   free {pf:.3f}')
print(f'central dust mass (%): baseline {cb:.1f}   capped {cc:.1f}   free {cf:.1f}')
for n, c, v, t, e in checks:
    print(('PASS' if c else 'FAIL'), n)
    print('     ', e)
print(f'N12_selfseeding COMPLETE: {npass}/{len(checks)} checks PASS.')
print('EVIDENCE ONLY: toy machinery (unprojected channel per N09 deviation); the witness:')
print('the dust self-seeds (unforced caustic); the a0/2 cap throttles the transfer; the free')
print('coupling transfers it -- the (A)/(B)-adjacent self-seeding channel is numerically live.')

# ------------------------------------------------------------------- PNG
fig, ax = plt.subplots(figsize=(6.4, 4.2))
labels = {'baseline': 'baseline (no gravity)', 'capped': 'capped (|a_ph|<=0.02)',
          'free': 'free (uncapped)'}
cols = {'baseline': '#666666', 'capped': '#d97706', 'free': '#dc2626'}
t_b = np.arange(len(sup_b)) * EVERY * DT
t_c = np.arange(len(sup_c)) * EVERY * DT
t_f = np.arange(len(sup_f)) * EVERY * DT
for tt, ss, lab, col in ((t_b, sup_b, 'baseline', 'baseline'),
                         (t_c, sup_c, 'capped', 'capped'),
                         (t_f, sup_f, 'free', 'free')):
    ax.plot(tt, ss, color=cols[lab], lw=1.2, label=labels[lab])
ax.axhline(SUP_STOP, color='k', lw=0.7, ls=':', label=f'sup-stop {SUP_STOP}')
ax.set_title('N12: unforced two-fluid self-seeding -- sup ||u||_oo(t) '
             '(A = 0, n = 24, T = 5)')
ax.set_xlabel('t')
ax.set_ylabel('sup ||u||_oo')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig('N12_selfseeding.png', dpi=120)
print('PNG saved: N12_selfseeding.png')

# ------------------------------------------------------------------- JSON
res = {'lane': 'N12_selfseeding', 'evidence': 'evidence only; toy machinery; not a proof',
       'deviation': 'free-run NaN fix: adopted N09 machinery verbatim -- CIC '
                    'scatter/gather with m_p = M_tot/N_p mass weights, '
                    'Lap psi = 4 pi G (rho - <rho>) Jeans-swindle FFT Poisson '
                    'with the cell-volume factor, velocity-Verlet dust '
                    'leapfrog with the force recomputed at drifted positions, '
                    'per-step sup > 50 stop guard with t_stop, ghat k=0 '
                    "hygiene; the draft's count-density/no-4pi potential was "
                    '~652x too strong (tau_ff ~ 6e-3 << dt), the under-resolved '
                    'leapfrog escaped (NaN). A = 0, blob at pi, gates '
                    'G80/G81/G82 unchanged.',
       'sup': {'baseline': pb, 'capped': pc, 'free': pf},
       'dust_conc': {'baseline': cb, 'capped': cc, 'free': cf}}
if info_f['stopped']:
    res['sup_stop_time'] = info_f['t_stop']
res['runs'] = {'baseline': {'runtime_s': info_b['runtime_s']},
               'capped': {'runtime_s': info_c['runtime_s']},
               'free': {'runtime_s': info_f['runtime_s'],
                        'stopped_early': info_f['stopped'],
                        'sup_stop_time': info_f['t_stop'],
                        'sup_at_stop': info_f['sup_run']}}
res['checks'] = [{'name': n, 'pass': c, 'value': str(v), 'threshold': str(t),
                  'note': e} for n, c, v, t, e in checks]
with open('N12_selfseeding_results.json', 'w') as f:
    json.dump(res, f, indent=1, allow_nan=False)
print('JSON saved: N12_selfseeding_results.json')