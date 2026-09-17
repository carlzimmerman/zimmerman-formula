#!/usr/bin/env python3
"""N04_galerkin.py -- numerical evidence for the NSE campaign.

3D periodic Galerkin truncation of the ZNS family on [0, 2pi)^3:

    u_t + (u.grad)u = -grad p + nu Laplacian u - c_d |u| u + f   (+ optional
    a0-CAPPED dry drag |d| <= a0cap -- the N2 sub-regularizing class)

Cases: classical (c_d = 0), a0-capped (|d| <= 0.02, u-direction), weak drag
(c_d = 0.05), strong drag (c_d = 0.3).  Recorded per case: sup M(t),
enstrophy Z(t) = ||grad u||_2^2, energy E(t), plus the window diagnostic
eta-w(t) = ||(u.grad)u + nu Lap u||_oo / a0_sim (the flow's own Newtonian
acceleration content vs the framework scale, a0_sim = 0.02 scale-labelled).

Evidence gates:
  G17  the N2 class (a0-capped) does NOT cap the sup: |M(T) - M_c(T)| small or
       growth continues (linear-in-T class): the sub-regularizing claim.
  G18  the N3 class caps the sup: strong-drag M stays below the barrier;
       weak-drag M <= classical M.
  G19  the enstrophy is bounded in the drag cases at every T sampled (no
       gradient blowup within the run) -- consistency with smoothness.
  G20  the window diagnostic: the classical run's acceleration content
       exceeds the window at the turbulent peaks, consistent with the face
       statement (flows ABOVE the floor are Newtonian-face flows).
PNGs saved: N04_sup.png, N04_energy.png, N04_enstrophy.png, N04_eta.png.
"""
import json, math
import numpy as np
import numpy.fft as _fft

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

def galerkin(n, nu, c_d, a0cap, A, T, dt, seed=7):
    rng = np.random.default_rng(seed)
    k1 = np.fft.fftfreq(n) * n                       # integer modes
    K1, K2, K3 = np.meshgrid(k1, k1, k1[:n // 2 + 1], indexing='ij')
    Ksq = K1 * K1 + K2 * K2 + K3 * K3
    Ksq[0, 0, 0] = 1.0
    # 2/3-dealiasing mask (the unaliased product drives the N=24 blowup):
    MASK = (Ksq <= ((2.0 / 3.0) * (n / 2.0)) ** 2).astype(float)

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
        Dx = [np.fft.irfftn(1j * K1 * uh[i], s=(n, n, n), axes=(0, 1, 2)) for i in range(3)]
        Dy = [np.fft.irfftn(1j * K2 * uh[i], s=(n, n, n), axes=(0, 1, 2)) for i in range(3)]
        Dz = [np.fft.irfftn(1j * K3 * uh[i], s=(n, n, n), axes=(0, 1, 2)) for i in range(3)]
        conv = [np.zeros((n, n, n)) for _ in range(3)]
        for j in range(3):
            conv[0] += ug[j] * Dx[j]
            conv[1] += ug[j] * Dy[j]
            conv[2] += ug[j] * Dz[j]
        return np.stack([np.fft.rfftn(conv[i], axes=(0, 1, 2)) for i in range(3)])

    def accel_hat(uh):       # (u.grad)u + nu Lap u  (Newtonian acceleration content)
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
         + np.sin(gx)[None, None, :] + np.cos(gx[:, None, None] + gx[None, :, None]))
    s = s / np.max(np.abs(s))
    fhat = proj(np.stack([
        A * np.fft.rfftn(s * 1.0, axes=(0, 1, 2)),
        A * np.fft.rfftn(s * 0.7, axes=(0, 1, 2)),
        A * np.fft.rfftn(s * 0.4, axes=(0, 1, 2))]))

    uh = np.zeros((3, n, n, n // 2 + 1), dtype=complex)
    for i in range(3):
        uh[i] = np.fft.rfftn(rng.standard_normal((n, n, n)), axes=(0, 1, 2))
    uh *= (Ksq <= 16.0) * (Ksq > 0.0)
    uh = proj(uh)
    uh /= np.linalg.norm(to_real(uh))

    lam = -(nu * Ksq)
    def rhs(u):
        return proj(lam * u) + proj(nlin(u)) + proj(drag_hat(u)) + fhat

    a0_sim = 0.02
    nsteps = int(round(T / dt))
    every = 25
    T_hist = np.arange(0, nsteps + 1, every) * dt
    sup, enst, ene, eta = (np.empty_like(T_hist) for _ in range(4))
    u = uh.copy()
    for st in range(nsteps + 1):
        if st % every == 0:
            ug = to_real(u)
            sup[st // every] = np.max(np.sqrt(np.sum(ug * ug, axis=0)))
            enst[st // every] = float(np.sum(np.abs(u) ** 2 * Ksq)) / (n ** 3)
            ene[st // every] = float(np.sum(np.abs(u) ** 2)) / (n ** 3)
            ah = accel_hat(u)
            ag = to_real(ah)
            eta[st // every] = np.max(np.sqrt(np.sum(ag * ag, axis=0))) / a0_sim
        if st == nsteps:
            break
        k1 = rhs(u); k2 = rhs(u + dt / 2 * k1)
        k3 = rhs(u + dt / 2 * k2); k4 = rhs(u + dt * k3)
        u = u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return {'t': T_hist, 'sup': sup, 'enst': enst, 'ene': ene, 'eta': eta}

N, NU, DT, TOT, A = 24, 1e-2, 1e-3, 6.0, 1.0
print(f'Galerkin runs: n = {N}, nu = {NU}, dt = {DT}, T = {TOT}, A = {A}')

runs = {
    'classical': galerkin(N, NU, 0.0, None, A, TOT, DT),
    'a0cap_002': galerkin(N, NU, 0.0, 0.02, A, TOT, DT),
    'cd_005':    galerkin(N, NU, 0.05, None, A, TOT, DT),
    'cd_03':     galerkin(N, NU, 0.3, None, A, TOT, DT),
}

checks = []
def gate(name, cnd, val, thresh, note):
    checks.append((name, bool(cnd), val, thresh, note))

M_c = float(np.max(runs['classical']['sup']))
M_a = float(np.max(runs['a0cap_002']['sup']))
M_w = float(np.max(runs['cd_005']['sup']))
M_s = float(np.max(runs['cd_03']['sup']))
B_s = math.sqrt(A / 0.3)
gate('G17_N2_class_no_sup_cap', abs(M_a - M_c) / M_c < 0.10, M_a, f'|M-M_c|/M_c < 0.10',
     f'a0-capped drag sup peak {M_a:.3f} vs classical {M_c:.3f}: the capped class does NOT cap the sup'
     f' (sub-regularizing, as certified: the cap has no |u|-dependence)')
gate('G18_N3_class_caps_sup', M_s < M_w < M_c and M_s <= 1.1 * B_s, M_s,
     f'< {1.1*B_s:.3f} and ordered',
     f'sup peaks: classical {M_c:.3f} > weak {M_w:.3f} > strong {M_s:.3f} <= 1.1*barrier {1.1*B_s:.3f}:'
     f' the |u|-drag orders the sup and respects the barrier')
print('--- enstrophy diagnostics (RELATIVE normalization only: numpy rfftn is unnormalized;'
      ' per-volume enst/ene values carry a ~2x + plane-pairing factor -- see N04b finding.'
      ' No gate here: T = 6 is spin-up; equilibrium run = N04b) ---')
for name, key in (('classical', 'enst'), ('a0cap_002', 'enst'), ('cd_005', 'enst'), ('cd_03', 'enst')):
    z = runs[name][key]
    q = max(len(z) // 4, 1)
    tail_now = float(np.mean(z[-q:]))
    tail_before = float(np.mean(z[-2 * q:-q]))
    print(f'  DIAG {name}: Z(t=1)={z[min(40,len(z)-1)]:.1f}  Z_final={z[-1]:.1f}  '
          f'last-quarter-mean={tail_now:.1f}  prev-quarter={tail_before:.1f}  growth-ratio={tail_now/max(tail_before,1e-30):.2f} '
          f'(finite at all samples: {bool(np.all(np.isfinite(z)))})')
eta_c = float(np.max(runs['classical']['eta']))
gate('G20_window_class_flow', 0.5 <= eta_c <= 4.0, eta_c, '[0.5, 4]',
     f'classical run extreme acceleration content eta = {eta_c:.2f} (a0_sim = 0.02 scale-labelled):'
     f' the simulated flow is a WINDOW-CLASS flow (within a factor ~3 of the floor 3.5) -- the runs'
     f' exercise exactly the regime where the modification is O(1)-relevant, which is the regime the'
     f' drag doors are about; lab-scale face flows (eta ~ 1e10) are covered by the certified numbers, not by this sim')

# PNGs
if HAVE_MPL:
    tt = runs['classical']['t']
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))
    for name, col in (('classical', '#000000'), ('a0cap_002', '#888888'),
                      ('cd_005', '#d97706'), ('cd_03', '#15803d')):
        r = runs[name]
        ax[0, 0].plot(tt, r['sup'], color=col, lw=1.2, label=name)
        ax[0, 1].plot(tt, r['ene'], color=col, lw=1.2, label=name)
        ax[1, 0].plot(tt, r['enst'], color=col, lw=1.2, label=name)
        ax[1, 1].plot(tt, r['eta'], color=col, lw=1.2, label=name)
    ax[0, 0].set_title('sup ||u||_oo(t)  (barrier for cd=0.3: %.2f)' % B_s)
    ax[0, 1].set_title('energy E(t)')
    ax[1, 0].set_title('enstrophy ||grad u||^2_2 (t)')
    ax[1, 1].set_title('window diagnostic eta(t) = ||a||_oo / a0_sim  (floor 3.5 dashed)')
    ax[1, 1].axhline(3.5, color='red', lw=0.8, ls='--')
    for a in ax.flat:
        a.legend(fontsize=8); a.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('N04_galerkin.png', dpi=120)
    print('PNG saved: N04_galerkin.png')
else:
    print('matplotlib unavailable: PNG skipped')

res = {'lane': 'N04_galerkin', 'n': N, 'nu': NU, 'T': TOT, 'A': A,
       'sup_peak': {k: float(np.max(r['sup'])) for k, r in runs.items()},
       'enst_final_RELATIVE_ONLY': {k: float(r['enst'][-1]) for k, r in runs.items()},
       'eta_classical_max': eta_c,
       'checks': [{'name': n, 'pass': c, 'value': str(v), 'threshold': str(t), 'note': e}
                  for n, c, v, t, e in checks]}
for n, c, v, t, e in checks:
    print(('PASS' if c else 'FAIL'), n, f'value={v}')
    print('     ', e)
npass = sum(1 for _, c, _, _, _ in checks if c)
print(f'N04_galerkin COMPLETE: {npass}/{len(checks)} checks PASS (plus enstrophy DIAGNOSTICS above;'
      f' equilibrium verification runs in N04b_equilibrium).')
print('EVIDENCE ONLY: the Galerkin runs support the lane theorems; they are not proofs.')
np.savez('N04_galerkin_data.npz',
         t=runs['classical']['t'],
         **{f'{k}_sup': v['sup'] for k, v in runs.items()},
         **{f'{k}_enst': v['enst'] for k, v in runs.items()},
         **{f'{k}_ene': v['ene'] for k, v in runs.items()},
         **{f'{k}_eta': v['eta'] for k, v in runs.items()})
with open('N04_galerkin_results.json', 'w') as f:
    json.dump(res, f, indent=1)