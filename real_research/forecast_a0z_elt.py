#!/usr/bin/env python3
"""
THE DECISIVE TEST, MADE OBSERVATION-READY: the ELT-class forecast for the Zimmerman a0(z) decline.
The framework's one falsifiable, distinctive prediction is a0(z) = a0 * sqrt(rho_DE(z)/rho_DE0) -- non-monotonic
(+6% bump at z~0.4) then DECLINING (0.86x at z=2, 0.74x at z=3). This script computes, precisely:
  (1) a0(z)/a0(0) for the framework vs the 4 rivals it must beat;
  (2) the SIGNAL size (in dex of a0, and % of V_flat at fixed M_b);
  (3) the SAMPLE SIZE of clean deep-MOND z~3 rotation curves needed for 3sigma/5sigma;
  (4) the SYSTEMATIC FLOOR that actually binds (not N), and the required control;
  (5) which rivals separate at which z.
This is what ELT/HARMONI + ALMA (gas) must deliver. The result decides the physics regardless of the open QG premises.
C. Zimmerman, 2026-06-06. Framework's own equation throughout.
"""
import numpy as np
Om, OmL = 0.315, 0.685
def rhoDE_ratio(z, w0=-0.752, wa=-0.86):   # DESI DR2 CPL -> rho_DE(z)/rho_DE0
    a = 1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def E(z): return np.sqrt(Om*(1+z)**3 + OmL)   # H(z)/H0 (matter-inclusive)

MODELS = {
 "FRAMEWORK (declining sqrt(rho_DE))": lambda z: np.sqrt(rhoDE_ratio(z)),
 "constant a0 (regular MOND)":         lambda z: np.ones_like(np.atleast_1d(z)*1.0),
 "rising-cH (Verlinde)":               lambda z: E(z),
 "assembly (1+z)^0.75 (Xu/SIV/sims)":  lambda z: (1+z)**0.75,
}
zs = np.array([0.4, 1.0, 2.0, 3.0])
print("="*92); print("(1) PREDICTED a0(z)/a0(0)  -- the framework vs the rivals it must beat"); print("="*92)
print(f"  {'z':>4}", *[f"{k.split('(')[0].strip()[:16]:>17}" for k in MODELS])
for z in zs:
    print(f"  {z:>4}", *[f"{MODELS[k](np.array([z]))[0]:>17.3f}" for k in MODELS])

print("\n"+"="*92); print("(2) THE SIGNAL: framework's a0(z) decline vs CONSTANT (the hard, decisive discriminator)"); print("="*92)
print("  deep-MOND identity V_flat^4 = G M_b a0  =>  at FIXED M_b, V_flat ratio = (a0 ratio)^(1/4)")
print(f"  {'z':>4}{'a0/a0(0)':>11}{'signal[dex a0]':>16}{'V_flat shift':>14}{'V_flat %':>10}")
for z in zs:
    r = np.sqrt(rhoDE_ratio(z)); dloga0 = np.log10(r); dV = 0.25*dloga0
    print(f"  {z:>4}{r:>11.3f}{dloga0:>16.3f}{dV:>14.3f}{(10**dV-1)*100:>+9.1f}%")
print("  (the bump at z~0.4 is +6% in a0 = +1.5% in V_flat; the z=3 decline is -26% in a0 = -7% in V_flat)")

print("\n"+"="*92); print("(3)+(4) SAMPLE SIZE and the BINDING SYSTEMATIC FLOOR"); print("="*92)
sig_stat = 0.40       # per-galaxy a0 scatter, dex (RC100 deep-MOND)
sig_sys  = 0.10       # high-z baryon (gas + IMF + pressure-support) systematic floor, dex -- does NOT average down
sigz3 = abs(np.log10(np.sqrt(rhoDE_ratio(3.0))))   # |signal| at z=3
print(f"  signal at z=3 = {sigz3:.3f} dex in a0;  per-galaxy statistical scatter ~{sig_stat} dex;  systematic floor ~{sig_sys} dex")
for nsig in (3,5):
    N = (sig_stat/(sigz3/nsig))**2
    print(f"  N for {nsig}sigma (statistics only) = ({sig_stat}/({sigz3:.3f}/{nsig}))^2 = {N:.0f} clean deep-MOND z~3 rotation curves")
print(f"  *** THE BINDING CONSTRAINT IS THE SYSTEMATIC, NOT N ***")
print(f"      the signal {sigz3:.3f} dex is only {sigz3/sig_sys:.1f}x the ~{sig_sys} dex high-z baryon systematic floor.")
print(f"      a 3sigma detection needs the systematic CONTROLLED to < {sigz3/3:.3f} dex -- i.e. M_b (esp. molecular gas)")
print(f"      to ~{ (10**(sigz3/3)-1)*100:.0f}% per galaxy. That is the real requirement: ALMA gas + careful M_b, not just N.")

print("\n"+"="*92); print("(5) WHICH RIVALS SEPARATE, AND WHEN"); print("="*92)
fw3 = np.log10(np.sqrt(rhoDE_ratio(3.0)))
for k in MODELS:
    if k.startswith("FRAMEWORK"): continue
    d = np.log10(MODELS[k](np.array([3.0]))[0]) - fw3
    n_per = abs(d)/sig_stat
    verdict = ("TRIVIAL to separate (already excluded)" if abs(d)>0.4 else
               "HARD -- the decisive test (systematic-limited)" if abs(d)<0.2 else "moderate")
    print(f"  framework vs {k.split('(')[0].strip():28}: |dlog a0(z=3)| = {abs(d):.2f} dex  ({n_per:.1f}sigma/galaxy)  -> {verdict}")

print("\n"+"="*92); print("OBSERVATIONAL PROGRAM (what delivers it)"); print("="*92)
print("""  TARGET: ~100+ clean deep-MOND (g_bar < a0, flat outer RC) star-forming discs at z=2-3.5, with:
    - resolved kinematics -> V_flat to <~5%   : ELT/HARMONI & MOSAIC (first light ~2028-2030); JWST/NIRSpec now (smaller N)
    - MOLECULAR + atomic gas -> M_b to <~10%   : ALMA (CO/[CII]); SKA (HI) later -- THIS controls the binding systematic
    - selection: rotation-dominated, NOT dispersion-dominated/assembly-active (MUSE intermediate-z discs cannot test it)
  PRE-REGISTERED PREDICTION: a0(z=3) = 0.74 x local (V_flat ~7% low at fixed M_b); +6% bump at z~0.4.
  KILL CONDITIONS: a0(z=3) >= local  -> declining-sqrt(rho_DE) FALSIFIED;  a0 ~ cH(z) rising -> FALSIFIED (already excluded).
  CONFIRM: a0(z) tracks sqrt(rho_DE(z)), inconsistent with constant AND rising at >3sigma, concordant with DESI's rho_DE(z).
  TIMELINE: decidable this decade (ELT+ALMA, ~2030). Independent of the open QG premises (volume-law existence; N-V dictionary).""")
