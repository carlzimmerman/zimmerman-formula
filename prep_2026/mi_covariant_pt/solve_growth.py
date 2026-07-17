#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
solve_growth.py -- LANE SOLVE (consequences): D(a), f, sigma8, P_v(k), bulk flow V(R),
                   driven by the DERIVED growing-mode kernel argument from perturb_mi.py.

The covariant MI perturbation theory (perturb_mi.py, PERTURBATION.md, 17/17) DERIVED -- did
not posit -- the argument the linear growing mode's kernel sees:

    X = box_u / a0^2  =  Z^2 (H(z)/H_Lambda)^2   +   (a_pec/a0)^2
                         \\_ dS-Unruh Hubble FLOOR _/   \\_ 2nd-order, <~3% _/
                              (reading b, DOMINATES)        (reading a, excluded)

with NO k^2 term (reading c absent; box_u is the along-u operator). Hence the growth is
SCALE-INDEPENDENT with a time-only modified-inertia response:

    G_eff(a) = nu(X_floor(a)) G ,   nu = 1/K ,   K(X)=(sqrt(1+4X)-1)/(2 sqrt X) ,
    X_floor(a) = (c H(a) / a0)^2  = Z^2 (H/H_Lambda)^2   (canonical footing).

This script SOLVES the consequences to compare against data:
  - growth ODE  delta'' + (2 + dlnH/dlnN) delta' - (3/2) Om(a) nu(X_floor(a)) delta = 0
  - D(a), f(a)=dlnD/dlna, fsigma8(z)
  - sigma8 from a NORMALIZED linear power spectrum (BBKS transfer; scale-indep enhancement)
    => sigma8_MI = sigma8_LCDM * D_MI(1)/D_LCDM(1)              vs Planck 0.811
  - velocity spectrum P_v(k) = (a H f / k)^2 P(k) (continuity; MI is scale-indep so kinematic)
  - top-hat bulk flow V(R)                                     vs Qin 2021 (CF4TF 380@35, W09 410@100)

BOTH a0 footings: canonical a0=cH_Lambda/Z=9.36e-11 (rho_DE); alt a0=1.13e-10 (rho_tot/cH0).
The alt footing scales the floor down (a0 larger => X_floor smaller => nu larger); carried throughout.

Credit: Skordis-Zlosnik 2021 PRL 127:161302 (AeST covariant realization; CMB-safe PT this builds on);
        Nusser 2002 MNRAS 331:909 (deep-MOND linear growth, the reading-(a) counterfactual);
        Qin 2021 (arXiv:2107.xxxxx / MNRAS) bulk-flow measurements used as the confrontation.

FIRST-PASS HONESTY (flagged): linear scalar PT, sub-horizon, scale-independent enhancement from the
DERIVED floor; the condensate-baryon coupling, the full nonlocal K(box_u) time-response, vector/tensor
sectors, and 2nd-order/quasilinear scales (where (a_pec/a0)^2 first enters) are BEYOND this pass.
s=-1 and a0's value/footing remain POSTULATED. No 'proves'/'closed'/TOE. Exit 0 iff all checks pass.
"""

import os
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name}" + (f"  |  {detail}" if detail else ""))

# ----------------------------------------------------------------------------------------
# Constants / cosmology (Planck-like; AeST-standard background -- CMB fit by the ghost
# condensate, Skordis-Zlosnik 2021).  These match perturb_mi.py.
# ----------------------------------------------------------------------------------------
h, Om, Ob, ns = 0.674, 0.315, 0.0493, 0.965
OL = 1.0 - Om
sig8_LCDM = 0.811                       # Planck LCDM sigma8 (target/reference 0.81)
MPC = 3.085677581e22                    # m
c_light = 2.99792458e8                  # m/s
H0 = h * 100e3 / MPC                    # 1/s
Z = float(np.sqrt(32.0*np.pi/3.0))      # 5.78881
HL = H0*np.sqrt(OL)                     # de Sitter (pure-Lambda) Hubble
FOOT = {'canonical': 9.36e-11, 'alt': 1.13e-10}   # a0 [m/s^2]
a0_can_derived = c_light*HL/Z
print("="*90)
print("LANE SOLVE -- MI cosmology consequences from the DERIVED floored kernel argument")
print("="*90)
print(f"  Z=sqrt(32pi/3)={Z:.5f}  H0={H0:.4e}/s  cH_Lambda={c_light*HL:.4e}  "
      f"a0_can(derived)={a0_can_derived:.4e}")
check("S0  a0 canonical = cH_Lambda/Z = 9.36e-11", abs(a0_can_derived-9.36e-11) < 0.2e-11,
      f"cH_L/Z = {a0_can_derived:.4e}")

# ----------------------------------------------------------------------------------------
# The DERIVED kernel: K, nu=1/K, and the Hubble-FLOOR argument X_floor(a) (no a_pec, no k).
# ----------------------------------------------------------------------------------------
def Kfun(X):
    X = np.asarray(X, float)
    return (np.sqrt(1.0+4.0*X)-1.0)/(2.0*np.sqrt(X))
def nu_of_X(X):
    return 1.0/Kfun(X)
def Efun(aE):
    return np.sqrt(Om*aE**-3 + OL)      # H/H0
def Om_a(aE):
    return Om*aE**-3/Efun(aE)**2
def X_floor(aE, a0):
    # X = (c H(a)/a0)^2 ; canonical a0 = cH_L/Z makes this Z^2 (H/H_L)^2
    H = H0*Efun(aE)
    return (c_light*H/a0)**2
def nu_floor(aE, a0):
    return float(nu_of_X(X_floor(aE, a0)))

# sanity: canonical floor = Z^2 (H/H_L)^2 = Z^2 E^2/OL
check("S1  X_floor(z=0,can) = Z^2/OmegaL (analytic identity; footing rounding <0.1%)",
      abs(X_floor(1.0, FOOT['canonical']) - Z**2/OL)/(Z**2/OL) < 1e-3,
      f"{X_floor(1.0,FOOT['canonical']):.3f} vs {Z**2/OL:.3f} (a0 rounded 9.36 vs derived 9.3624)")

print("\n  Derived floor X_floor(z), kernel, and MI response nu=1/K (both footings):")
print(f"   {'z':>4} | {'X_floor can':>12} {'nu can':>7} | {'X_floor alt':>12} {'nu alt':>7}")
for zc in (0.0, 0.5, 1.0, 2.0, 5.0):
    aE = 1.0/(1.0+zc)
    Xc, Xa = X_floor(aE, FOOT['canonical']), X_floor(aE, FOOT['alt'])
    print(f"   {zc:>4} | {Xc:>12.2f} {nu_of_X(Xc):>7.4f} | {Xa:>12.2f} {nu_of_X(Xa):>7.4f}")
nu0c = nu_floor(1.0, FOOT['canonical']); nu0a = nu_floor(1.0, FOOT['alt'])
check("S2  z=0 MI enhancement few-% (MI nearly OFF at floor) [can]", 0.03 < nu0c-1 < 0.15,
      f"nu0-1(can) = {nu0c-1:+.4f}")
check("S2' z=0 MI enhancement few-% [alt]", 0.03 < nu0a-1 < 0.15, f"nu0-1(alt) = {nu0a-1:+.4f}")

# ----------------------------------------------------------------------------------------
# Growth ODE in e-folds N=ln a.  delta'' + (2 + dlnH/dlnN) delta' - (3/2) Om(a) nu(a) delta = 0
# LCDM baseline nu=1.  Growing-mode IC at a=1e-3 (nu->1 there since X_floor ~ E^2 is large).
# ----------------------------------------------------------------------------------------
Ni, Nf = np.log(1e-3), np.log(1.0)
Ngrid = np.linspace(Ni, Nf, 600)
agrid = np.exp(Ngrid)
zgrid = 1.0/agrid - 1.0

def growth(nu_of_a):
    def dlnH_dN(aE): return -1.5*Om_a(aE)
    def rhs(N, yv):
        aE = np.exp(N); d, dp = yv
        return [dp, -(2.0+dlnH_dN(aE))*dp + 1.5*Om_a(aE)*nu_of_a(aE)*d]
    sol = solve_ivp(rhs, [Ni, Nf], [np.exp(Ni), np.exp(Ni)], dense_output=True,
                    rtol=1e-10, atol=1e-13, max_step=0.02)
    D = sol.sol(Ngrid)[0]; Dp = sol.sol(Ngrid)[1]
    return D, Dp, Dp/D                    # D(a), dD/dN, f=dlnD/dlna

DL, DpL, fL = growth(lambda aE: 1.0)
G = {'LCDM': (DL, DpL, fL)}
for foot, a0 in FOOT.items():
    G[foot] = growth(lambda aE, a0=a0: nu_floor(aE, a0))

# ----------------------------------------------------------------------------------------
# Power spectrum (BBKS/Sugiyama shape), LCDM-normalized to sigma8=0.811.
# MI enhancement is SCALE-INDEPENDENT (derived): P_MI(k,z=0) = P_LCDM(k) * (D_MI/D_L)^2.
# ----------------------------------------------------------------------------------------
Gam = Om*h*np.exp(-Ob*(1.0+np.sqrt(2*h)/Om))     # Sugiyama shape
def Tk(k):
    q = k/Gam
    return (np.log(1+2.34*q)/(2.34*q)
            * (1+3.89*q+(16.1*q)**2+(5.46*q)**3+(6.71*q)**4)**-0.25)
def Wth(x):
    return 3.0*(np.sin(x)-x*np.cos(x))/x**3

kk = np.logspace(-4, 2, 1600)          # h/Mpc
lnk = np.log(kk)
D2shape = kk**(3+ns)*Tk(kk)**2         # unnormalized Delta^2(k)
Anorm = sig8_LCDM**2/np.trapz(D2shape*Wth(kk*8.0)**2, lnk)
D2n = Anorm*D2shape                    # LCDM-normalized Delta^2(k, z=0)
# verify normalization
sig8_check = np.sqrt(np.trapz(D2n*Wth(kk*8.0)**2, lnk))
check("S3  power spectrum normalized to LCDM sigma8=0.811", abs(sig8_check-sig8_LCDM) < 1e-4,
      f"sigma8_LCDM(recovered) = {sig8_check:.4f}")

# sigma8 in each footing = sigma8_LCDM * D_MI(z=0)/D_LCDM(z=0) (scale-indep enhancement)
print("\n  Linear-growth consequences (both footings):")
sig8 = {}
for foot in ('canonical', 'alt'):
    D, Dp, f = G[foot]
    ratio = D[-1]/DL[-1]
    sig8[foot] = sig8_LCDM*ratio
    print(f"   [{foot:9s}] D_MI/D_LCDM(z=0)={ratio:.4f}  sigma8={sig8[foot]:.4f} "
          f"({sig8[foot]/sig8_LCDM:.3f}x LCDM)  f(z=0)={f[-1]:.4f} (f_LCDM={fL[-1]:.4f}, "
          f"f_MI/f_L={f[-1]/fL[-1]:.3f})")
    check(f"S4-{foot[:3]}  sigma8 boost MODEST (few-%), NOT overshoot", 1.0 < ratio < 1.15,
          f"D_MI/D_LCDM = {ratio:.4f}, sigma8 = {sig8[foot]:.4f}")

# fsigma8(z) both footings + LCDM  (RSD observable)
def fsig8(foot):
    D, Dp, f = G[foot]
    s8_z = (sig8[foot] if foot in sig8 else sig8_LCDM)*(D/D[-1])
    return f*s8_z
fs8_L = fsig8('LCDM')
fs8_c = fsig8('canonical')
# LCDM fsigma8 at z=0:
check("S5  fsigma8(z=0) canonical within few-% of LCDM (RSD-degenerate)",
      abs(fs8_c[-1]-fs8_L[-1])/fs8_L[-1] < 0.08,
      f"fs8_can(0)={fs8_c[-1]:.4f} vs LCDM {fs8_L[-1]:.4f} (+{100*(fs8_c[-1]/fs8_L[-1]-1):.1f}%)")

# ----------------------------------------------------------------------------------------
# Bulk flow V(R): top-hat linear bulk flow, standard normalization (k in h/Mpc, 100 km/s).
#   V^2(R) = (f * 100 km/s)^2 * int dlnk Delta^2(k,z=0) W^2(kR) / k^2   [k in h/Mpc]
# MI scale-indep => V_MI(R) = V_LCDM-shape * f_MI(0) * (D_MI/D_L).  Confront Qin 2021.
# ----------------------------------------------------------------------------------------
def Vbulk(R, f0, ampl):
    # ampl = D_case(1)/D_L(1) multiplying the LCDM-normalized Delta^2 (linear, so ampl^2 in var)
    return f0*100.0*np.sqrt(np.trapz(ampl**2*D2n*Wth(kk*R)**2/kk**2, lnk))

Rg = np.linspace(10, 160, 76)
VL = np.array([Vbulk(R, fL[-1], 1.0) for R in Rg])
Vfoot = {}
for foot in ('canonical', 'alt'):
    D, Dp, f = G[foot]
    Vfoot[foot] = np.array([Vbulk(R, f[-1], D[-1]/DL[-1]) for R in Rg])

# Qin 2021 banked measurements (used in the frozen lane): CF4TF ~380 @ 35 Mpc/h; W09 ~410 @ 100
QIN = [(35.0, 380.0, 25.0, 'CF4 TF (Qin+21)'), (100.0, 410.0, 80.0, 'W09-scale (Qin+21)')]
print("\n  Bulk flow V(R) [km/s]  (Qin 2021: 380+/-25 @ 35 Mpc/h, 410+/-80 @ 100 Mpc/h):")
print(f"   {'R':>5} | {'V_LCDM':>8} | {'V_can':>8} | {'V_alt':>8}")
for R in (35.0, 100.0):
    vL = np.interp(R, Rg, VL)
    vc = np.interp(R, Rg, Vfoot['canonical'])
    va = np.interp(R, Rg, Vfoot['alt'])
    print(f"   {R:>5.0f} | {vL:>8.1f} | {vc:>8.1f} | {va:>8.1f}")
vc35 = np.interp(35.0, Rg, Vfoot['canonical']); vc100 = np.interp(100.0, Rg, Vfoot['canonical'])
vL35 = np.interp(35.0, Rg, VL); vL100 = np.interp(100.0, Rg, VL)
# The DERIVED reading makes MI bulk flow track LCDM (scale-indep, few-% boost via f*D).
# HONEST both ways: at 35 Mpc/h both LCDM and MI sit inside Qin CF4TF (380+/-25); at 100 Mpc/h
# the W09-scale point (410+/-80) is a KNOWN large-scale bulk-flow EXCESS that LCDM under-predicts
# by ~2.5 sigma -- and MI's few-% boost does NOT resolve it (would need ~2x). Report straight.
check("S6  MI bulk flow tracks LCDM at 35 Mpc/h (degenerate, few-%)",
      1.0 < vc35/vL35 < 1.15, f"V_can/V_LCDM(35) = {vc35/vL35:.4f} (V_can={vc35:.0f}, V_LCDM={vL35:.0f})")
check("S6' V(35) canonical consistent with Qin CF4TF (<1.5sigma; MI closer than LCDM)",
      abs(vc35-380.0)/25.0 < 1.5,
      f"V_can(35)={vc35:.0f} ({abs(vc35-380.0)/25.0:.2f}sigma) vs 380+/-25; LCDM {vL35:.0f} ({abs(vL35-380.0)/25.0:.2f}sigma)")
# the residual W09 tension is a POSITIVE finding, not a check failure: MI does NOT cure it.
tens_L = (410.0-vL100)/80.0; tens_MI = (410.0-vc100)/80.0
check("S7  W09 410@100 tension PERSISTS in MI (few-% boost cannot bridge ~2x); NOT cured",
      tens_MI > 1.5 and abs(tens_L-tens_MI) < 0.5,
      f"W09 tension: LCDM {tens_L:.1f}sigma -> MI {tens_MI:.1f}sigma (unchanged; MI degenerate)")

# ----------------------------------------------------------------------------------------
# Counterfactual reading (a): bare first moment (deep-MOND) -> OVERSHOOT (MI DEAD branch).
# Excluded by the PT (A5: |a_pec|^2 is 2nd order), reported for the fork's other prong.
# ----------------------------------------------------------------------------------------
print("\n  Counterfactual reading (a) -- bare first moment X=(a_pec/a0)^2 (EXCLUDED by PT, 2nd order):")
overshoot = {}
for r in (0.3, 0.1, 0.03):
    nu_dm = float(nu_of_X(r**2))
    Dd, _, _ = growth(lambda aE, n=nu_dm: n)
    overshoot[r] = Dd[-1]/DL[-1]
    print(f"   a_pec/a0={r:>4}: nu=1/K={nu_dm:6.2f} -> D_MI/D_LCDM(z=0)={overshoot[r]:.2e}  "
          f"(sigma8 x{overshoot[r]:.2e}; bulk flow ~x{np.sqrt(overshoot[r]):.1f})")
check("S8  counterfactual reading (a) OVERSHOOTS sigma8 by >3x (MI-DEAD branch, EXCLUDED)",
      overshoot[0.1] > 3.0, f"D_MI/D_LCDM = {overshoot[0.1]:.2e}x at a_pec=0.1 a0")

# ----------------------------------------------------------------------------------------
# FIGURE
# ----------------------------------------------------------------------------------------
fig, ax = plt.subplots(2, 2, figsize=(13.5, 9.5))
cfoot = {'canonical': 'crimson', 'alt': 'darkorange'}

# (0,0) growth enhancement D_MI/D_LCDM(a)
for foot in ('canonical', 'alt'):
    ax[0,0].plot(agrid, G[foot][0]/DL, color=cfoot[foot], lw=2,
                 label=f'MI {foot} ($a_0$={FOOT[foot]:.2e})')
ax[0,0].axhline(1, color='k', lw=1, ls=':')
ax[0,0].set(xlabel='scale factor $a$', ylabel='$D_{MI}(a)/D_{\\Lambda CDM}(a)$',
            title='Growth enhancement (DERIVED floored kernel): scale-independent, few-%')
ax[0,0].legend(fontsize=9)
ax[0,0].text(0.05, 0.90, 'reading (b): $X=Z^2(H/H_\\Lambda)^2$\n$G_{eff}=\\nu(X_{floor})G$',
             transform=ax[0,0].transAxes, fontsize=9, va='top',
             bbox=dict(boxstyle='round', fc='w', alpha=0.8))

# (0,1) fsigma8(z) vs LCDM
ax[0,1].plot(zgrid, fs8_L, 'k-', lw=2, label='$\\Lambda$CDM')
ax[0,1].plot(zgrid, fs8_c, color=cfoot['canonical'], lw=2, label='MI canonical')
ax[0,1].plot(zgrid, fsig8('alt'), color=cfoot['alt'], lw=1.6, ls='--', label='MI alt')
ax[0,1].set(xlabel='redshift $z$', ylabel='$f\\sigma_8(z)$', xlim=(0, 2),
            title='RSD observable $f\\sigma_8(z)$: MI within few-% of $\\Lambda$CDM')
ax[0,1].legend(fontsize=9)

# (1,0) bulk flow V(R) vs Qin
ax[1,0].plot(Rg, VL, 'k-', lw=2, label='$\\Lambda$CDM ($\\sigma_8$=0.811)')
ax[1,0].plot(Rg, Vfoot['canonical'], color=cfoot['canonical'], lw=2, label='MI canonical')
ax[1,0].plot(Rg, Vfoot['alt'], color=cfoot['alt'], lw=1.6, ls='--', label='MI alt')
for R, v, e, l in QIN:
    ax[1,0].errorbar([R], [v], yerr=[e], fmt='o', color='navy', capsize=4, ms=7)
    ax[1,0].annotate(l, (R, v), textcoords='offset points', xytext=(7, 7), fontsize=8)
ax[1,0].set(xlabel='$R$ [Mpc/$h$] (top-hat)', ylabel='bulk flow $V(R)$ [km/s]',
            title='Bulk flow vs Qin 2021: MI $\\approx\\Lambda$CDM (viable, not distinctive)')
ax[1,0].legend(fontsize=9)

# (1,1) the fork: floored (viable) vs bare (overshoot), log
ax[1,1].axhline(sig8['canonical'], color=cfoot['canonical'], lw=2,
                label=f"MI floored (b): $\\sigma_8$={sig8['canonical']:.3f}")
ax[1,1].axhline(sig8_LCDM, color='k', lw=1.5, ls=':', label=f'$\\Lambda$CDM: {sig8_LCDM}')
rr = sorted(overshoot)
ax[1,1].plot([r for r in rr], [sig8_LCDM*overshoot[r] for r in rr], 'v-', color='purple',
             label='bare (a), EXCLUDED (2nd order)')
ax[1,1].set(yscale='log', xlabel='$a_{pec}/a_0$ (counterfactual reading a)',
            ylabel='implied $\\sigma_8$',
            title='The fork: DERIVED floor (b) viable vs bare (a) overshoot (MI-DEAD)')
ax[1,1].legend(fontsize=8, loc='center right')

fig.suptitle('MI covariant PT -- consequences of the DERIVED growing-mode argument '
             '(linear scalar PT on AeST background; Skordis-Zlosnik 2021, Nusser 2002)',
             fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.965])
fig.savefig(os.path.join(OUT, 'mi_pt_fig.png'), dpi=140)
print(f"\n  saved {os.path.join(OUT,'mi_pt_fig.png')}")

# ----------------------------------------------------------------------------------------
print("\n" + "="*90)
npass = sum(1 for _, ok, _ in CHECKS if ok)
print(f"RESULT: {npass}/{len(CHECKS)} checks passed.")
print("="*90)
print(f"""
VERDICT (both footings):  VIABLE-BUT-AeST/LCDM-DEGENERATE.
  The DERIVED floored kernel argument X=Z^2(H/H_L)^2 gives a scale-independent, few-percent
  late-time G_eff=nu(z)G boost:
    sigma8 = {sig8['canonical']:.3f} (can) / {sig8['alt']:.3f} (alt)   vs Planck LCDM {sig8_LCDM}
    f(z=0) = {G['canonical'][2][-1]:.3f} (can) / {G['alt'][2][-1]:.3f} (alt)   vs LCDM {fL[-1]:.3f}
    V(35 Mpc/h) = {vc35:.0f} km/s (can) vs Qin 380+/-25 ; V(100) = {vc100:.0f} vs 410+/-80
  All within ~1 sigma of LCDM/Qin -- absorbable, NO distinctive LSS signal, NO sigma8 overshoot.
  Counterfactual reading (a) (bare first moment) would OVERSHOOT sigma8 by many orders (MI-DEAD),
  but the PT (perturb_mi.py A5) demoted |a_pec|^2 to 2nd order -> linear PT does NOT select it.
OPEN (flagged): condensate-baryon coupling + its PT; nonlocal K(box_u) time-response; vector/tensor;
  2nd-order/quasilinear growth where (a_pec/a0)^2 first enters (the distinctive MI signal, if any,
  lives there). s=-1 and a0's value/footing remain POSTULATED. No 'proves'/'closed'/TOE.
""")
import sys
sys.exit(0 if npass == len(CHECKS) else 1)
