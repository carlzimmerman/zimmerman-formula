#!/usr/bin/env python3
"""(B) MI spectra + bulk flow from the self-consistent growth (reads mi_growth.npz).

P(k,z=0)_case = Delta^2_LCDM-norm * (D_case/D_L)^2 (scale-independent enhancement,
first-pass approximation). sigma8 vs Planck 0.811. Velocity from continuity
(kinematic, unmodified by MI): P_v = (a H f / k)^2 P(k). Top-hat bulk flow:
    V^2(R) = (f * 100 km/s)^2 * int dlnk Delta^2(k) W^2(kR) / k^2   [k in h/Mpc]
Confront Qin 2021 banked points (CF4TF ~380 km/s @ 35 Mpc/h; W09-style ~410 @ 100)
and the NAIVE prescription V_naive = V_LCDM * nu(g_R/a0) with g_R the rms peculiar
gravity smoothed on the bulk scale R (the prior workflow's ~10x overshoot: it
evaluates the kernel at the tiny LARGE-SCALE g instead of the element's own
acceleration -- the double-count root cause). Figure -> mi_cosmo_fig.png. Exit 0.
"""
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
d = np.load(os.path.join(OUT, 'mi_growth.npz'))
ag, DL, fL, k, D2n = d['a'], d['DL'], d['fL'], d['k'], d['D2n']
lnk = np.log(k)
sig8L = float(d['sig8L'])
h, Om, OL = 0.674, 0.315, 0.685
MPC = 3.0857e22
H0 = h * 100e3 / MPC
c = 2.998e8
FOOT = {'canonical': 9.36e-11, 'alt': 1.13e-10}

def nu(y):
    return np.sqrt(1.0 + 1.0 / y)

def Wth(x):
    return 3 * (np.sin(x) - x * np.cos(x)) / x**3

def Vbulk(R, f0, ampl2):
    # ampl2 = (D_case(1)/D_L(1))^2 multiplying the LCDM-normalized Delta^2
    return f0 * 100.0 * np.sqrt(np.trapz(ampl2 * D2n * Wth(k * R)**2 / k**2, lnk))

Rg = np.linspace(10, 160, 61)
VL = np.array([Vbulk(R, fL[-1], 1.0) for R in Rg])

# naive prescription: nu at the R-scale smoothed rms peculiar gravity (LCDM field)
k_m = k * h / MPC
gR = np.array([1.5 * Om * H0**2 * np.sqrt(np.trapz(D2n * Wth(k * R)**2 / k_m**2, lnk))
               for R in Rg])

QIN = [(35.0, 380.0, 25.0, 'CF4TF (Qin+21)'), (100.0, 410.0, 80.0, 'W09 (Qin+21)')]

print("=== MI SPECTRA + BULK FLOW ===")
print(f"LCDM: sigma8={sig8L:.3f}  V(35)={np.interp(35,Rg,VL):.0f}  "
      f"V(100)={np.interp(100,Rg,VL):.0f} km/s   [Qin banked: 380@35, 410@100]")
V = {}
for foot, a0 in FOOT.items():
    nuR = nu(gR / a0)
    Vn = VL * nuR
    V[f'{foot}_naive'] = Vn
    print(f"\n--- footing {foot} (a0={a0:.2e}) ---")
    print(f"  naive nu(g_R/a0): nu(35)={np.interp(35,Rg,nuR):.1f} nu(100)={np.interp(100,Rg,nuR):.1f}"
          f" -> V_naive(35)={np.interp(35,Rg,Vn):.0f}, V_naive(100)={np.interp(100,Rg,Vn):.0f} km/s"
          f"  (the banked ~10x overshoot)")
    for case in ('SC', 'floor_a0', 'floor_cH'):
        Dc = d[f'{foot}_{case}_D']
        fc = d[f'{foot}_{case}_f']
        rat = Dc[-1] / DL[-1]
        s8 = sig8L * rat
        Vc = np.array([Vbulk(R, fc[-1], rat**2) for R in Rg])
        V[f'{foot}_{case}'] = Vc
        v35, v100 = np.interp(35, Rg, Vc), np.interp(100, Rg, Vc)
        print(f"  {case:9s}: sigma8={s8:6.3f} ({s8/0.81:5.2f}x Planck)  "
              f"V(35)={v35:6.0f} ({v35/380:4.1f}x Qin)  V(100)={v100:6.0f} ({v100/410:4.1f}x Qin)")

# ---------------- figure ----------------
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
cols = {'SC': 'crimson', 'floor_a0': 'darkorange', 'floor_cH': 'seagreen'}
lab = {'SC': 'MI self-consistent (linear $g_{rms}$)',
       'floor_a0': 'MI, element floor $g\\geq a_0$',
       'floor_cH': 'MI, total-accel floor $g\\geq cH_\\Lambda$'}
for case in cols:
    for foot, ls in [('canonical', '-'), ('alt', '--')]:
        ax[0].plot(ag, d[f'{foot}_{case}_D'] / DL, ls, color=cols[case],
                   label=lab[case] if foot == 'canonical' else None, lw=2 if foot == 'canonical' else 1)
        ax[1].plot(ag, d[f'{foot}_{case}_f'], ls, color=cols[case], lw=2 if foot == 'canonical' else 1)
ax[0].axhline(1, color='k', lw=1)
ax[0].set(xlabel='a', ylabel='$D_{MI}(a)/D_{\\Lambda CDM}(a)$', yscale='log',
          title='growth enhancement (solid=canonical, dashed=alt $a_0$)')
ax[0].legend(fontsize=8, loc='upper left')
ax[1].plot(ag, fL, 'k-', lw=2, label='$\\Lambda$CDM')
ax[1].set(xlabel='a', ylabel='$f = d\\ln D/d\\ln a$', title='growth rate')
ax[1].legend(fontsize=8)
ax[2].plot(Rg, VL, 'k-', lw=2, label='$\\Lambda$CDM (0.81)')
ax[2].plot(Rg, V['canonical_naive'], 'k:', lw=2, label='naive $V_L\\times\\nu(g_R/a_0)$')
for case in cols:
    ax[2].plot(Rg, V[f'canonical_{case}'], color=cols[case], lw=2, label=lab[case])
    ax[2].plot(Rg, V[f'alt_{case}'], '--', color=cols[case], lw=1)
for R, v, e, l in QIN:
    ax[2].errorbar([R], [v], yerr=[e], fmt='o', color='navy', capsize=4)
    ax[2].annotate(l, (R, v), textcoords='offset points', xytext=(6, 6), fontsize=8)
ax[2].set(xlabel='R [Mpc/h] (top-hat)', ylabel='bulk flow V(R) [km/s]', yscale='log',
          title='bulk flow: self-consistent vs naive vs Qin 2021')
ax[2].legend(fontsize=7.5)
fig.suptitle('MI linear cosmology, first pass (Newtonian quasi-linear on AeST background; '
             'Nusser 2002 / Skordis-Zlosnik 2021)', fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(os.path.join(OUT, 'mi_cosmo_fig.png'), dpi=140)
print("\nsaved mi_cosmo_fig.png")
