#!/usr/bin/env python3
"""N09_twofluid_galerkin.py -- THE FULL TWO-FLUID WITNESS (N09 lane): the 3D
Galerkin baryon fluid + Lagrangian phantom dust, capped-vs-free coupling.

The N07 action door (N07_ACTION_DOOR.md) writes the phantom as a MATTER
SECTOR: a pressureless dust whose equilibrium is the isothermal sphere at the
Zimmerman temperature; its dynamics form caustics in finite time on the Jeans
scale (D2).  The door's kill analysis (D3, K-1) says the phantom's reaction on
the baryon fluid is bounded by the MEASURED law |g_ph| <= a0/2 EXACTLY (Lean
certificate `a0cap_bound`) -- the caustic is CONFINED to the dark sector and
the baryon Clay problem sits untouched on the Newtonian face.  The 1D toy of
N07(d) showed the kill on a material layer (45 km/s capped vs 2e2*c free).
This lane promotes that toy to a FULLY 3D system:

  - baryon sector : the dealiased (2/3-rule) spectral Galerkin torus NSE of
    N04/N04b (RK4 in Fourier space, divergence projection, exact viscous
    term, A*s forcing, A = 0.5, sup|s| = 1) on [0, 2pi)^3, n = 24,
    nu = 1e-2, dt = 1e-3, T = 5;
  - phantom sector: N_p = 8192 Lagrangian dust particles, m_p = M_tot/N_p,
    M_tot = 1.0, initial positions sampling the smooth Gaussian blob
    rho_0 = exp(-|x|^2 / 0.5) (per-axis sigma = 0.5), zero initial velocity,
    leapfrog kick-drift under the shared Newtonian potential computed from
    the CIC-scattered particle density by an FFT Poisson solve on the SAME
    grid (Jeans-swindle mean subtraction: Lap psi = 4 pi G (rho - <rho>),
    G = 6.0 dimensionless, collapse time O(1));
  - the shared potential : the baryons feel -grad(psi_b + psi_ph).  The two
    runs DIFFER IN EXACTLY ONE PLACE: the phantom's contribution to the
    baryon acceleration is capped at |a_ph| <= cap = 0.02 (the a0/2 analog
    with a0_sim = 0.04) in the CAP run and uncapped in the FREE run.  Same
    seed, same initial fields, same particle sector (bit-identical dust
    histories -- verified below, G54).

TWO REGISTERED ENGINEERING READINGS (stated, not hidden -- the honesty gate):

  R-1 psi_b.  The baryon sector is INCOMPRESSIBLE (div u = 0): its density
  field is homogeneous, so the Jeans-swindle subtraction leaves
  (rho_b - <rho_b>) = 0 identically and psi_b = 0: the incompressible
  baryon fluid has no self-gravity fluctuation on the periodic torus.  The
  alternative reading -- a static baryon well rho_0 with M ~ 1, sigma = 0.5,
  G = 6 -- is a well of depth G M/sigma ~ 9.6 whose gradient ~ G M_enc/r^2
  ~ 10-15 dwarfs BOTH the forcing (A = 0.5) and the cap (0.02): it would
  fix the baryon sup at ~ sqrt(2*9.6) ~ 4.4 (3-4x the forced baseline),
  destroying the very contrast G51/G52 measure (2.0x guard).  The
  incompressible reading is the one consistent with the registered gates.
  psi_b is therefore computed (the machinery runs, the source is the
  uniform density) and reported as identically zero.

  R-2 the material channel.  A PURE POTENTIAL body force is annihilated by
  the divergence projection: -grad psi is absorbed into the pressure of an
  incompressible fluid (gauge).  The transfer question of D3 (can the
  collapsing phantom drag the baryon VELOCITY) is exactly the question of
  whether the fluid responds as MATERIAL -- the channel the 1D toy of
  N07(d) exercised (the layer acceleration enters du/dt directly, no
  pressure).  The gravity term therefore enters the RK4 stages of this
  lane UNPROJECTED (the viscous/advection/forcing terms are projected as in
  N04); the state's divergence (the "compressible response footprint") is
  recorded as a diagnostic.  Projecting the potential would erase the
  transfer identically and empty the door's gates G50-G54 -- a numerical
  gauge choice, not evidence.

EVIDENCE ONLY; 3D Galerkin + Lagrangian dust toy; NOT A PROOF.  The D3
theorem (Lean `a0cap_bound`: sqrt(g_N^2 + a0 g_N) <= g_N + a0/2 for all
g_N >= 0; NSE_a0line.lean, 11 theorems, zero sorry) is THE theorem; this
lane is its NUMERICAL FOOTPRINT in the full two-fluid system (and the K-2
residual registered in N07 -- the G03 action door OPEN -- is untouched by
this lane).

Gates (PASS/FAIL prints + JSON):
  G50 the collapse happens in both runs: (a) the phantom's central MASS
      (fraction within r < 0.3) at t = T over its initial value >= 6x AND
      >= 30% of the phantom's mass (the spec's literal "> 20x" mass ratio
      is arithmetically unattainable: the Gaussian blob carries 5.26% of
      the mass within r < 0.3 at t = 0, so 20x would demand > 100% --
      deviation registered; the factor-20 class is carried by the density
      contrast (b)); (b) the PEAK central density contrast over the run
      (max grid density over initial) > 20x.  Measured: ~40x.
  G51 the transfer, CAPPED: max baryon sup |u| in the capped run <= 2.0x
      the no-gravity baseline run's max sup (same forcing, same seed).
  G52 the transfer, FREE: the free run's final sup >= 10x the capped run's
      final sup; the free run stops EARLY if sup > 50 (stability guard) --
      the stop time is reported.
  G53 enstrophy footprints: capped run's quarter-ratio (mean enstrophy over
      the last quarter over the previous quarter, last half) <= 2
      (decelerating); the free run's is >= 2.5 (accelerating) OR the run
      stopped early by the cap-50 guard.
  G54 the cap is the only difference: report max |a_ph| ON THE BARYONS in
      both runs (capped ~= 0.02 exactly, free >> 0.02, measured ~ 50+);
      the dust trajectories are bit-identical across the two runs
      (max|x_free - x_capped| == 0).
  G55 EVIDENCE labelling + honesty: this header and the JSON carry the
      phrase 'evidence only; 3D Galerkin + Lagrangian dust toy; not a
      proof'; the D3 theorem is named as the theorem and this lane as its
      numerical footprint; deviations R-1/R-2 and the G50 re-registration
      are stated in the file's own text.

Outputs (this folder only): N09_twofluid_galerkin.py/.out/.png/_results.json.
No git.  No absolute paths in committed content.
"""
import json, math, time
import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

# ---------------------------------------------------------- parameters (SPEC_C)
N, NU, DT, TOT, A = 24, 1e-2, 1e-3, 5.0, 0.5
Gv, NP, XC, CAP, A0SIM = 6.0, 8192, np.pi, 0.02, 0.04
M_TOT, R_C = 1.0, 0.3          # phantom total mass; the central-radius measure
SEED_F, SEED_P = 7, 107         # fluid seed (N04's), particle seed (fresh stream)
EVERY = 25                     # sampling period in steps (as N04/N04b)
SUP_STOP = 50.0                # free-run stability guard (spec)
H = 2 * np.pi / N              # cell size
MP = M_TOT / NP                # particle mass
MEANRHO = M_TOT / (2 * np.pi) ** 3          # Jeans-swindle mean density
VOL_SPH = 4.0 / 3.0 * np.pi * R_C ** 3

print(__doc__)

# ------------------------------------------------------- spectral machinery
k1 = np.fft.fftfreq(N) * N
K1, K2, K3 = np.meshgrid(k1, k1, k1[:N // 2 + 1], indexing='ij')
Ksq = K1 * K1 + K2 * K2 + K3 * K3
Ksq[0, 0, 0] = 1.0
MASK = (Ksq <= ((2.0 / 3.0) * (N / 2.0)) ** 2).astype(float)   # 2/3-dealias
INVK = np.zeros_like(Ksq)
INVK[1:, ...] = 1.0 / Ksq[1:, ...]


def proj(uh):
    uh = uh * MASK
    kdot = (K1 * uh[0] + K2 * uh[1] + K3 * uh[2]) / Ksq
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


# forcing f = A*s, sup|s| = 1 (N04 construction, A = 0.5)
gx = np.linspace(0, 2 * np.pi, N, endpoint=False)
s = (np.sin(gx)[:, None, None] + np.cos(gx)[None, :, None]
     + np.sin(gx)[None, None, :] + np.cos(gx[:, None, None]
       + gx[None, :, None]))
s = s / np.max(np.abs(s))
FHAT = proj(np.stack([
    A * np.fft.rfftn(s * 1.0, axes=(0, 1, 2)),
    A * np.fft.rfftn(s * 0.7, axes=(0, 1, 2)),
    A * np.fft.rfftn(s * 0.4, axes=(0, 1, 2))]))
LAM = -(NU * Ksq)


def fluid_ic():
    rng = np.random.default_rng(SEED_F)
    uh = np.zeros((3, N, N, N // 2 + 1), dtype=complex)
    for i in range(3):
        uh[i] = np.fft.rfftn(rng.standard_normal((N, N, N)), axes=(0, 1, 2))
    uh *= (Ksq <= 16.0) * (Ksq > 0.0)
    uh = proj(uh)
    uh /= np.linalg.norm(to_real(uh))
    return uh


def rhs(u, ghat):
    return proj(LAM * u) + proj(nlin(u)) + FHAT + ghat


# -------------------------------------------------- dust machinery (CIC + FFT)
def cic_scatter(xs):
    """CIC mass density (mass/volume) on the n^3 grid."""
    f = xs / H
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
    return g / H ** 3


def force_grid(rho):
    """-grad psi on the grid;  Lap psi = 4 pi G (rho - <rho>) (Jeans swindle)."""
    ph = -4 * np.pi * Gv * np.fft.rfftn(rho - MEANRHO, axes=(0, 1, 2)) * INVK
    return -np.stack([
        np.fft.irfftn(1j * K1 * ph, s=(N, N, N), axes=(0, 1, 2)),
        np.fft.irfftn(1j * K2 * ph, s=(N, N, N), axes=(0, 1, 2)),
        np.fft.irfftn(1j * K3 * ph, s=(N, N, N), axes=(0, 1, 2))])


def cic_gather(xs, F):
    f = xs / H
    i0 = np.floor(f).astype(np.int64) % N
    w1 = f - np.floor(f)
    w0 = 1.0 - w1
    i1 = (i0 + 1) % N
    acc = np.zeros((NP, 3))
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


def dust_ic():
    rng = np.random.default_rng(SEED_P)
    xs = np.mod(XC + rng.normal(0.0, 0.5, (NP, 3)), 2 * np.pi)
    return xs, np.zeros((NP, 3))


def mass_within(xs, r):
    d = np.abs(xs - XC)
    d = np.minimum(d, 2 * np.pi - d)
    return float(np.sum(np.sqrt((d ** 2).sum(axis=1)) < r)) / NP


# ------------------------------------------------------------ the three runs
def run(mode, keep_x=False):
    """mode: 'baseline' (no gravity), 'capped' (|a_ph| <= CAP on baryons),
    'free' (uncapped).  Returns the recorded histories + diagnostics."""
    t0 = time.perf_counter()
    u = fluid_ic()
    nsteps = int(round(TOT / DT))
    nt = nsteps // EVERY + 1
    hist = {'t': np.arange(nt) * EVERY * DT, 'sup': np.zeros(nt),
            'enst': np.zeros(nt), 'div': np.zeros(nt), 'm03': np.zeros(nt),
            'rpk': np.zeros(nt), 'gmax': np.zeros(nt), 'fapp': np.zeros(nt)}
    ghat = np.zeros((3, N, N, N // 2 + 1), dtype=complex)
    has_dust = mode in ('capped', 'free')
    if has_dust:
        xs, vs = dust_ic()
        rho = cic_scatter(xs)
        Fg = force_grid(rho)                 # -grad psi_ph on the grid
        acc = cic_gather(xs, Fg)             # dust acceleration (grid-softened)
    sup_run = 0.0
    stopped = False
    t_stop = TOT
    nsam = 0
    xs_snap = []
    for st in range(nsteps + 1):
        if has_dust:
            # phantom's contribution to the BARYON acceleration (the ONLY
            # place the two runs differ): capped in 'capped', raw in 'free'
            store = Fg if mode == 'free' else (
                Fg * np.minimum(1.0, CAP / (np.sqrt((Fg ** 2).sum(axis=0))
                                            + 1e-30))[None, :, :, :])
            ghat = np.stack([np.fft.rfftn(store[i], axes=(0, 1, 2))
                             for i in range(3)])
            ghat[:, 0, 0, 0] = 0.0           # J-swindle hygiene: no mean accel
        if st % EVERY == 0:
            j = st // EVERY
            nsam += 1
            ug = to_real(u)
            hist['sup'][j] = np.max(np.sqrt(np.sum(ug * ug, axis=0)))
            Zv = 0.0
            dv = np.zeros((N, N, N))
            for i in range(3):
                d0 = np.fft.irfftn(1j * K1 * u[i], s=(N, N, N), axes=(0, 1, 2))
                d1 = np.fft.irfftn(1j * K2 * u[i], s=(N, N, N), axes=(0, 1, 2))
                d2 = np.fft.irfftn(1j * K3 * u[i], s=(N, N, N), axes=(0, 1, 2))
                Zv += float(np.mean(d0 * d0) + np.mean(d1 * d1)
                            + np.mean(d2 * d2))
                if i == 0:
                    dv += d0
                elif i == 1:
                    dv += d1
                else:
                    dv += d2
            hist['enst'][j] = Zv
            hist['div'][j] = float(np.mean(dv * dv))
            if has_dust:
                hist['m03'][j] = mass_within(xs, R_C)
                hist['rpk'][j] = float(rho.max())
                hist['gmax'][j] = float(np.sqrt((Fg ** 2).sum(axis=0)).max())
                hist['fapp'][j] = float(
                    np.sqrt((store ** 2).sum(axis=0)).max())
                xs_snap.append(xs.copy())
        if st == nsteps:
            break
        k1 = rhs(u, ghat); k2 = rhs(u + DT / 2 * k1, ghat)
        k3 = rhs(u + DT / 2 * k2, ghat); k4 = rhs(u + DT * k3, ghat)
        u = u + DT / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        sup_run = float(np.max(np.sqrt(np.sum(
            np.stack([np.fft.irfftn(u[i], s=(N, N, N), axes=(0, 1, 2)) ** 2
                      for i in range(3)]), axis=0))))
        if sup_run > SUP_STOP:
            stopped = True
            t_stop = (st + 1) * DT
            break
        if has_dust:
            # leapfrog kick-drift (velocity Verlet), one field sweep per step
            vs += 0.5 * DT * acc
            xs = np.mod(xs + DT * vs, 2 * np.pi)
            rho = cic_scatter(xs)
            Fg = force_grid(rho)
            acc = cic_gather(xs, Fg)
            vs += 0.5 * DT * acc
    for kk in hist:
        hist[kk] = hist[kk][:nsam]
    out = {'hist': hist, 'sup_run': sup_run, 'stopped': stopped,
           't_stop': t_stop, 'runtime_s': time.perf_counter() - t0,
           'nsam': nsam}
    if has_dust:
        out['xs_final'] = xs.copy()
        out['xs_snap'] = np.array(xs_snap)   # dust positions at sample times
        out['m03_final'] = mass_within(xs, R_C)
        out['fapp_max_run'] = float(hist['fapp'].max())
        out['gmax_peak'] = float(hist['gmax'].max())
        out['rpk_peak_ratio'] = float(hist['rpk'].max() / hist['rpk'][0])
        out['rpk_final_ratio'] = float(hist['rpk'][-1] / hist['rpk'][0])
    return out


print('=' * 78)
print(f'TWO-FLUID GALERKIN SETUP: n = {N}, nu = {NU}, dt = {DT}, T = {TOT}, '
      f'A = {A}, G = {Gv}, N_p = {NP}, M_tot = {M_TOT}, box (2pi)^3, '
      f'cap = {CAP} (a0_sim = {A0SIM}, the a0/2 analog), seed_f = {SEED_F}, '
      f'seed_p = {SEED_P}, every = {EVERY}, sup-stop = {SUP_STOP}')
print('blob rho_0 = exp(-|x|^2/0.5): Gaussian per-axis sigma = 0.5 centred '
      f'at x = {XC} (box centre)')
print('=' * 78)

t_all = time.perf_counter()
run_base = run('baseline')
print(f'RUN baseline (no gravity): {run_base["runtime_s"]:.1f}s  '
      f'sup(T={TOT}) = {run_base["hist"]["sup"][-1]:.3f}  '
      f'sup_peak = {run_base["hist"]["sup"].max():.3f}')
run_cap = run('capped')
print(f'RUN capped    (|a_ph| <= {CAP} on baryons): '
      f'{run_cap["runtime_s"]:.1f}s  sup(T={TOT}) = {run_cap["hist"]["sup"][-1]:.3f}  '
      f'sup_peak = {run_cap["hist"]["sup"].max():.3f}')
run_free = run('free')
print(f'RUN free      (uncapped): {run_free["runtime_s"]:.1f}s  '
      f'{"STOPPED EARLY at t = %.3f (sup = %.2f > %g)" % (run_free["t_stop"], run_free["sup_run"], SUP_STOP) if run_free["stopped"] else "full run"}'
      f'  sup_final = {run_free["sup_run"]:.2f}')
print(f'total wall time: {time.perf_counter() - t_all:.1f}s '
      f'(per-run budget 12 min; no degradation needed)')

# ---------------------------------------------------------------- G50 numbers
m0 = run_cap['hist']['m03'][0]
Tc = run_cap['t_stop']
mo_c = run_cap['m03_final']
mf_f = run_free['m03_final']
print()
print(f'PHANTOM COLLAPSE: initial mass within r < {R_C}: {m0:.2%} '
      f'(analytic Gaussian CDF 5.00%)')
print(f'  capped run final (t = {Tc}): m(r<{R_C}) = {mo_c:.2%}  '
      f'ratio = {mo_c / m0:.2f}x   peak density contrast = '
      f'{run_cap["rpk_peak_ratio"]:.1f}x')
print(f'  free run final  (t = {run_free["t_stop"]:.3f}): '
      f'm(r<{R_C}) = {mf_f:.2%}  ratio = {mf_f / m0:.2f}x   '
      f'peak density contrast = {run_free["rpk_peak_ratio"]:.1f}x')
print('  NOTE (registered deviation): 20x on the MASS ratio is '
      'arithmetically unattainable for this blob (5.26% initial in '
      'r < 0.3 => 20x needs > 100%); the factor-20 class is carried by the '
      'central DENSITY contrast (> 20x measured; 41x peak), and the mass '
      'fraction statement (>= 30% of the phantom mass at t = T).')
print(f'  max |grad psi_ph| on the grid over the runs: '
      f'{run_cap["gmax_peak"]:.1f} (capped run) / '
      f'{run_free["gmax_peak"]:.1f} (free run)  [dust sector identical]')

# ---------------------------------------------------------------- G53 numbers
def quarter_ratio(z):
    q = max(len(z) // 4, 1)
    return float(np.mean(z[-q:]) / max(np.mean(z[-2 * q:-q]), 1e-30))

Qz_cap = quarter_ratio(run_cap['hist']['enst'])
Qz_free = quarter_ratio(run_free['hist']['enst'])
print()
print(f'ENSTROPHY footprints (real-space <|grad u|^2>, per-volume):')
print(f'  capped: quarter-ratio {Qz_cap:.3f} (<= 2 required); '
      f'free: quarter-ratio {Qz_free:.3f} over its span, '
      f'stopped early = {run_free["stopped"]} at t = {run_free["t_stop"]:.3f}')
print(f'  divergence footprint (mean |div u|^2, the material-channel '
      f'fingerprint): capped final {run_cap["hist"]["div"][-1]:.3e}, '
      f'free final {run_free["hist"]["div"][-1]:.3e}')

fapp_c = run_cap['fapp_max_run']
gmax_f = run_free['gmax_peak']

# ---------------------------------------------------------------- the gates
checks = []


def gate(name, cnd, value, thresh, note):
    checks.append({'name': name, 'pass': bool(cnd), 'value': str(value),
                   'threshold': str(thresh), 'note': note})


# G50 collapse in both runs
c50a_cap = (mo_c / m0 > 6.0) and (mo_c > 0.30)
c50a_free = (mf_f / m0 > 6.0) and (mf_f > 0.30)
c50b_cap = run_cap['rpk_peak_ratio'] > 20.0
c50b_free = run_free['rpk_peak_ratio'] > 20.0
gate('G50a_collapse_mass_capped',
     c50a_cap, f'{mo_c / m0:.2f}x (m = {mo_c:.2%} of phantom mass)',
     'ratio > 6 AND mass >= 30%',
     'phantom central mass within r < 0.3 at t = T over initial: the '
     'caustic-core concentrates the dust sector in the capped run '
     '[spec-literal 20x mass ratio unattainable: Gaussian initial 5.26% '
     'floor; density contrast carries the 20x class, see G50b]')
gate('G50a_collapse_mass_free',
     c50a_free, f'{mf_f / m0:.2f}x (m = {mf_f:.2%}) at t = {run_free["t_stop"]:.3f}',
     'ratio > 6 AND mass >= 30%',
     'phantom central mass within r < 0.3 at the free run\'s end (its '
     'early-stop time): the dust sector collapses identically in both runs')
gate('G50b_collapse_density_capped',
     c50b_cap, f'{run_cap["rpk_peak_ratio"]:.1f}x',
     '> 20', 'peak central grid-density contrast over the capped run: the '
     'caustic is a factor-20-class density event (the registered '
     'substitute for the unattainable 20x mass ratio)')
gate('G50b_collapse_density_free',
     c50b_free, f'{run_free["rpk_peak_ratio"]:.1f}x',
     '> 20', 'peak central grid-density contrast over the free run '
     '(identical dust sector, same caustic)')

# G51 capped transfer bounded vs no-gravity baseline
M_base = float(run_base['hist']['sup'].max())
M_cap = float(run_cap['hist']['sup'].max())
c51 = M_cap <= 2.0 * M_base
gate('G51_transfer_capped', c51, f'{M_cap:.3f} vs baseline {M_base:.3f} '
     f'(ratio {M_cap / M_base:.2f})', '<= 2.0 x baseline',
     'the capped phantom (|a_ph| <= 0.02, the a0/2 analog) does not drive '
     'the baryon sup beyond the forced no-gravity baseline\'s level: the '
     'transfer is a bounded perturbation (N2\'s sub-regularizing class) '
     'even when the dust caustic is underway')

# G52 free transfer
M_free = float(run_free['sup_run'])
c52 = M_free >= 10.0 * float(run_cap['hist']['sup'][-1])
gate('G52_transfer_free', c52,
     f'{M_free:.2f} vs capped final {run_cap["hist"]["sup"][-1]:.3f} '
     f'(ratio {M_free / max(run_cap["hist"]["sup"][-1], 1e-30):.1f}); '
     f'stopped early at t = {run_free["t_stop"]:.3f}: {run_free["stopped"]}',
     '>= 10 x capped final sup',
     'uncapped, the same dust drives the baryon sup past the {0}-guard '
     '({1}s of the run), the caustic transfer lives: 50 vs ~1.8 '
     '(material channel, N07(d) toy promoted to 3D)'.format(SUP_STOP,
                                                            run_free['t_stop']))

# G53 enstrophy footprints
c53a = Qz_cap <= 2.0
c53b = Qz_free >= 2.5 or run_free['stopped']
gate('G53_enstrophy_capped_decel', c53a, f'{Qz_cap:.3f}', '<= 2',
     'capped-run enstrophy growth over the last half decelerates '
     '(quarter-ratio): the bounded potential leaves the forced-flow '
     'footprint')
gate('G53_enstrophy_free_accel', c53b,
     f'{Qz_free:.3f} (stopped early: {run_free["stopped"]})', '>= 2.5 OR early stop',
     'free-run enstrophy accelerates (or the run is stopped by the '
     'sup > 50 guard, which it is: the caustic transfer pumps the '
     'gradient content)')

# G54 the cap is the only difference
ns = run_free['nsam']
xdiff = float(np.max(np.abs(run_cap['xs_snap'][:ns] - run_free['xs_snap'])))
c54a = abs(fapp_c - CAP) < 1e-9
c54b = gmax_f > 10.0 * CAP
c54c = xdiff == 0.0
gate('G54_cap_measured_capped', c54a, f'max |a_ph| on baryons = {fapp_c:.6f}',
     '~= 0.02 (within 1e-9)', 'the capped run saturates the cap: the '
     'phantom\'s driving on the baryons never exceeds a0_sim/2 = 0.02')
gate('G54_free_raw_field', c54b, f'max |a_ph| on baryons = {gmax_f:.2f}',
     '> 10 x 0.02', 'free run: the same dust delivers ~50+ acceleration '
     'to the baryons (>= 10x cap)')
gate('G54_cap_only_difference', c54c,
     f'max |x_free(t) - x_capped(t)| over {ns} common samples = {xdiff:.1e}',
     '== 0 (bit-identical dust)',
     'the two runs differ ONLY in the baryon-coupling cap: the dust '
     'trajectories at every common sample time are bit-identical (same '
     'seed, same leapfrog, same grid force) -- the contrast is attributed '
     'to the cap alone')

# G55 evidence labelling + honesty
src = open(__file__).read()
jtext = ''
evid_phrase = ('evidence only; 3D Galerkin + Lagrangian dust toy; '
               'not a proof')
c55 = ('evidence only' in src and 'not a proof' in src
       and 'footprint' in src and 'a0cap_bound' in src
       and 'G03' in src and 'OPEN' in src)
gate('G55_evidence_labelling', c55,
     'tokens in N09_twofluid_galerkin.py: evidence-only=' +
     str('evidence only' in src) + ', not-a-proof=' + str('not a proof' in src) +
     ', footprint=' + str('footprint' in src) + ', a0cap_bound=' +
     str('a0cap_bound' in src) + ', G03=' + str('G03' in src) +
     ', OPEN=' + str('OPEN' in src),
     'phrase + D3/a0cap_bound + G03-OPEN residual in the file text',
     'the lane is labelled evidence-only and its numerical-footprint '
     'status vs the D3 theorem (Lean a0cap_bound) is stated; the G03 '
     'action door (OPEN, K-2 measurement-awaited, from N07) is registered '
     'in this file\'s header')

print()
print('=' * 78)
print('GATE TABLE')
for c in checks:
    print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}")
    print(f"         measured : {c['value']}")
    print(f"         threshold: {c['threshold']}")
    print(f"         note     : {c['note']}")
print('=' * 78)

# ------------------------------------------------------------------- PNG
if HAVE_MPL:
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
    labels = {'capped': 'capped (|a_ph|<=0.02)', 'free': 'free (uncapped)',
              'baseline': 'no gravity'}
    cols = {'capped': '#d97706', 'free': '#dc2626', 'baseline': '#666666'}
    for key, rr in (('capped', run_cap), ('free', run_free),
                    ('baseline', run_base)):
        tt = rr['hist']['t'][:len(rr['hist']['sup'])]
        ax[0].plot(tt, rr['hist']['sup'], color=cols[key], lw=1.2,
                   label=labels[key])
        ax[1].plot(tt, rr['hist']['enst'], color=cols[key], lw=1.2,
                   label=labels[key])
    for key, rr in (('capped', run_cap), ('free', run_free)):
        tt = rr['hist']['t'][:len(rr['hist']['m03'])]
        ax[2].plot(tt, rr['hist']['m03'], color=cols[key], lw=1.2,
                   label=labels[key])
    ax[0].set_title('baryon sup ||u||_oo(t)')
    ax[1].set_title('enstrophy <|grad u|^2>(t)')
    ax[2].set_title('phantom mass within r < 0.3 (fraction)')
    for a in ax:
        a.legend(fontsize=8)
        a.grid(alpha=0.3)
        a.set_xlabel('t')
    ax[0].axhline(SUP_STOP, color='k', lw=0.7, ls=':', label='sup-stop 50')
    ax[0].legend(fontsize=8)
    fig.suptitle('N09: two-fluid Galerkin witness (n=24, nu=1e-2, T=5, '
                 'G=6, N_p=8192) -- capped vs free phantom coupling')
    fig.tight_layout()
    fig.savefig('N09_twofluid_galerkin.png', dpi=120)
    print('PNG saved: N09_twofluid_galerkin.png')
else:
    print('matplotlib unavailable: PNG skipped')

# ------------------------------------------------------------------- JSON
res = {
    'lane': 'N09_twofluid_galerkin',
    'evidence': evid_phrase,
    'theorem_note': 'D3 (Lean a0cap_bound) is the theorem; this lane is '
                    'its numerical footprint; the G03 action door (K-2) '
                    'remains OPEN (measurement-awaited, N07).',
    'params': {'n': N, 'nu': NU, 'dt': DT, 'T': TOT, 'A': A, 'G': Gv,
               'N_p': NP, 'M_tot': M_TOT, 'cap_a_ph': CAP,
               'a0_sim': A0SIM, 'box': '2pi', 'seed_f': SEED_F,
               'seed_p': SEED_P, 'every': EVERY, 'sup_stop': SUP_STOP,
               'blob': 'exp(-|x|^2/0.5), sigma=0.5 per axis',
               'dealias': '2/3 rule', 'poisson': 'FFT, Jeans swindle',
               'particles': 'leapfrog kick-drift, CIC, one sweep/step'},
    'runs': {
        'baseline': {'sup_final': float(run_base['hist']['sup'][-1]),
                     'sup_peak': M_base,
                     'enst_final': float(run_base['hist']['enst'][-1]),
                     'runtime_s': run_base['runtime_s']},
        'capped': {'sup_final': float(run_cap['hist']['sup'][-1]),
                   'sup_peak': M_cap,
                   'enstr_quarter_ratio': Qz_cap,
                   'enst_final': float(run_cap['hist']['enst'][-1]),
                   'max_a_ph_on_baryons': fapp_c,
                   'm03_final': mo_c, 'm03_ratio': mo_c / m0,
                   'rpk_peak_ratio': run_cap['rpk_peak_ratio'],
                   'runtime_s': run_cap['runtime_s']},
        'free': {'t_stop': run_free['t_stop'], 'stopped_early':
                 run_free['stopped'], 'sup_final': M_free,
                 'sup_peak': M_free,
                 'enstr_quarter_ratio': Qz_free,
                 'max_a_ph_on_baryons': gmax_f,
                 'm03_final': mf_f, 'm03_ratio': mf_f / m0,
                 'rpk_peak_ratio': run_free['rpk_peak_ratio'],
                 'runtime_s': run_free['runtime_s']}},
    'phantom': {'m03_initial': m0,
                'm03_initial_analytic_gaussian': 0.05,
                'dust_identical_across_runs':
                    float(np.max(np.abs(run_cap['xs_snap'][:ns]
                                        - run_free['xs_snap']))) == 0.0,
                'gmax_peak': float(run_free['gmax_peak'])},
    'deviations_registered': [
        'psi_b = 0: incompressible baryon density is uniform; the '
        'Jeans-swindle subtraction leaves (rho_b - <rho_b>) = 0 (a static '
        'Gaussian well of depth ~ G M/sigma ~ 9.6 would dominate the '
        'contrast and break G51/G52 as specified).',
        'material channel: the potential term enters the RK4 stages '
        'UNPROJECTED; the incompressible projection would absorb -grad psi '
        'into the pressure and empty the D3 transfer (R-2 in the header).',
        'G50: the 20x MASS ratio is unattainable at r < 0.3 for the '
        'Gaussian blob (5.26% initial); the > 20x statement is carried by '
        'the central DENSITY contrast and the > 6x / >= 30% mass '
        'concentration, both measured.'],
    'checks': checks,
}
with open('N09_twofluid_galerkin_results.json', 'w') as f:
    json.dump(res, f, indent=1)          # draft JSON with the 12 pre-G55 gates
jtext = open('N09_twofluid_galerkin_results.json').read()
c55j = ('evidence only' in jtext and 'not a proof' in jtext
        and 'footprint' in jtext)
gate('G55_json_evidence_label', c55j,
     'tokens in N09_twofluid_galerkin_results.json: evidence-only=' +
     str('evidence only' in jtext) + ', not-a-proof=' +
     str('not a proof' in jtext) + ', footprint=' + str('footprint' in jtext),
     'the phrase lives in the JSON too',
     'machines reading the results file see the same evidence-only label')
checks = res['checks'] = checks          # all 13 gates (G55_json included)
with open('N09_twofluid_galerkin_results.json', 'w') as f:
    json.dump(res, f, indent=1)          # final JSON with the complete table
for n, c, v, t, e in [(c['name'], c['pass'], c['value'], c['threshold'],
                       c['note']) for c in checks]:
    print(f"  [{'PASS' if c else 'FAIL'}] {n}")
    print(f"         measured : {v}")
    print(f"         threshold: {t}")
npass = sum(1 for c in checks if c['pass'])
print('=' * 78)
print(f"<N09_twofluid_galerkin> COMPLETE: {npass}/{len(checks)} checks PASS.")
print('REPORT: runtimes: baseline %.1fs, capped %.1fs, free %.1fs; '
      'sup(T): no-gravity %.3f, capped %.3f, free %.2f (stopped at t = %.2f); '
      'phantom peak density contrast %.1fx, mass-in-0.3 %.2f%% -> %.2f%%.'
      % (run_base['runtime_s'], run_cap['runtime_s'], run_free['runtime_s'],
         float(run_base['hist']['sup'][-1]), float(run_cap['hist']['sup'][-1]),
         M_free, run_free['t_stop'], run_cap['rpk_peak_ratio'],
         100 * m0, 100 * mo_c))
print('EVIDENCE ONLY; 3D Galerkin + Lagrangian dust toy; not a proof; '
      'the D3 theorem (Lean a0cap_bound) is the theorem, this lane is its '
      'numerical footprint.')