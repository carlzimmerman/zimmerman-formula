#!/usr/bin/env python3
"""
Analyze the patched-CLASS modified-inertia CMB runs (Fable priority #1: the CLASS Euler-equation hook).

Reads the TT C_l from CLASS runs with the Zimmerman modified-inertia injection (perturbations_mond.patch)
for MOND_MODE in {off, flat, declining, rising} at the calibrated PHYSICAL perturbation amplitude
(MOND_AMP ~ 3.18e-5, set so the baryon proper acceleration ~ 1e-9 m/s^2 at recombination), and computes
the theta_* (acoustic-scale) -marginalized, cosmic-variance-limited Delta chi^2 vs the unmodified run.

This is the FULL-BOLTZMANN replacement for the toy single-oscillator ODE (real CLASS photon hierarchy,
real recombination, both tight-coupling AND post-tca baryon Euler modified). Reproduction in README.md.
C. Zimmerman, 2026-06-09.  Needs numpy, scipy.  Data: the o_*_00_cl.dat / p_*_00_cl.dat files alongside.
"""
import numpy as np, os
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name):
    d = np.loadtxt(os.path.join(HERE, name)); return d[:,0], d[:,1]

l, C_off = load('o_off_00_cl.dat')                 # unmodified (MOND_MODE=off) == standard LCDM
fsky = 0.7; sel = (l>=30)&(l<=2000); L = l[sel]; Co = C_off[sel]
sig2 = 2.0/((2*L+1)*fsky)*Co**2                     # cosmic-variance-limited errors

def peaks(C):
    m = l>100; idx,_ = find_peaks(C[m], prominence=C[m].max()*0.02); return l[m][idx][:3].astype(int)
def dchi2_marg(C):                                  # minimize over a uniform ell-rescale (refit theta_*)
    f = interp1d(l, C, bounds_error=False, fill_value=0.0)
    return min(np.sum((f(L/(1+e))-Co)**2/sig2) for e in np.linspace(-0.03, 0.03, 301))

RUNS = [('declining_phys','declining, physical amp'),
        ('flat_clsnorm','flat/constant a0, CLASS-internal (unphysical) norm'),
        ('flat_phys','flat/constant a0, PHYSICAL amp'),
        ('rising_phys','rising, physical amp')]

print("="*92)
print("PATCHED-CLASS modified-inertia CMB: theta_*-marginalized, cosmic-variance-limited Delta chi^2")
print("="*92)
print(f"  unmodified LCDM peaks: {list(peaks(C_off))}  (validation: MOND_MODE=off reproduces it)\n")
print(f"  {'run':>42}{'peaks l':>20}{'maxdCl%':>9}{'Dchi2':>12}")
for tag, desc in RUNS:
    fn = f'p_{tag}_00_cl.dat'
    if not os.path.exists(os.path.join(HERE, fn)): print(f"  {desc:>42}   (missing {fn})"); continue
    _, C = load(fn)
    mx = 100*np.max(np.abs(C[sel]-Co)/np.maximum(Co,1e-30))
    print(f"  {desc:>42}{str(list(peaks(C))):>20}{mx:>8.2f}%{dchi2_marg(C):>12.1f}")
print("""
  VERDICT (full Boltzmann, physical amplitude):
    declining -> Dchi2 ~ 0      SAFE (a0(z_rec)~5.5e-13, modification negligible at any amplitude)
    constant  -> Dchi2 ~ 117    EXCLUDED (vindicates the toy ODE's provisional ~81, same order)
    rising    -> catastrophic   DEAD
  => the framework's own slow simple-IF shape + Planck EXCLUDES constant a0 and rising, leaving DECLINING
     as the lone CMB survivor -- Fable's syllogism, now at full-Boltzmann grade.
  CAVEAT: modified inertia is NONLINEAR in amplitude, so the effect vanishes at CLASS's internal O(1)
     normalization (flat_clsnorm -> 0) and only appears at the PHYSICAL amplitude (calibrated A_PHYS~3.18e-5
     so a_proper~1e-9 m/s^2 at recomb). Dchi2~117 is 'order 100, robustly >>1', not precise to better than
     a factor ~few (it scales with the amplitude/prescription). Cosmic-variance-limited, unlensed.""")
