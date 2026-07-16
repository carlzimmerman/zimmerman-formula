#!/usr/bin/env python3
"""
THE BIG WHEEL as a clean galaxy-scale z=3.25 test of a0(z) evolution.

Deep-MOND BTFR: V_flat^4 = G a0 M_bar  =>  a0_eff = V_circ^4/(G M_bar) reads the
acceleration scale straight off one rotation curve. We confront the Big Wheel
(Nature Astronomy 2025, arXiv:2409.17956) against THREE evolution hypotheses at
z=3.25, on BOTH footings for the local scale (rule 4: run both, print the spread):

  H_RISE   a0(z) = a0_loc * E(z)         (a0 propto cH(z): Verlinde/QI/MDM-rising class)
  H_CONST  a0(z) = a0_loc                (constant Lambda / w=-1: the framework's safe core)
  H_DECL   a0(z) = a0_loc * sqrt(rhoDE(z)/rhoDE0)   (framework's a0 propto sqrt(rho_DE),
                                           DESI evolving DE w0wa -> declines at high z)

Local footings: framework canonical a0 = 9.36e-11 (rho_DE/cH_Lambda) AND the empirical
MOND a0 = 1.20e-10 (SPARC RAR). Monte-Carlo propagates V, M_star, M_gas errors.
Reported straight -- a single galaxy with real M_bar systematics, bounded honestly.
"""
import numpy as np
np.random.seed(20260705)

# ---- constants ----
G   = 6.674e-11
Msun= 1.989e30
kpc = 3.0857e19
c   = 2.998e8

# ---- cosmology (Planck-ish) + DESI DR2 CPL for the declining branch ----
Om, OL = 0.31, 0.69
def E(z): return np.sqrt(Om*(1+z)**3 + OL)
def rhoDE_ratio(z, w0=-0.75, wa=-0.86):
    # rho_DE(z)/rho_DE0 for CPL w(z)=w0+wa z/(1+z)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))

z = 3.25

# ---- Big Wheel data (arXiv:2409.17956) ----
V_rot, V_err   = 280.0, 31.0          # km/s, inclination-corrected max (+32/-31 ~ 31)
sig_int        = 61.0                  # km/s internal dispersion (V/sig=4.5)
Mstar_sed, Mstar_sed_e   = 3.7e11, 1.0e11   # SED (OVERestimated per M_dyn, see below)
Mstar_par, Mstar_par_e   = 1.7e11, 0.6e11   # parametric/dynamical-consistent
Mgas, Mgas_e             = 1.8e11, 0.9e11    # H2 from CO
HE = 1.36                              # helium correction on gas
Reff = 9.6                             # kpc

# dynamical-mass sanity: M_dyn(<Reff) = V^2 R / G  bounds M_bar from above
Mdyn = (V_rot*1e3)**2 * (Reff*kpc)/G/Msun/1e11
print(f"M_dyn(<{Reff} kpc) = {Mdyn:.2f}e11 Msun  => M_bar(<Reff) <= this; SED M_star=3.7e11 alone exceeds it")
print(f"   => SED stellar mass is overestimated; use parametric M_star as the fair central case.\n")

def mc_a0eff(Mstar, Mstar_e, n=400000):
    V   = np.random.normal(V_rot, V_err, n)*1e3
    # asymmetric-drift: V_circ^2 = V_rot^2 + 3.4 sigma^2 (exp disk ~1 Reff); small (V/sig=4.5)
    Vc2 = V**2 + 3.4*(sig_int*1e3)**2
    Ms  = np.clip(np.random.normal(Mstar, Mstar_e, n), 0.05e11, None)
    Mg  = np.clip(np.random.normal(Mgas, Mgas_e, n), 0.05e11, None)
    Mbar= (Ms + HE*Mg)*Msun
    a0  = Vc2**2/(G*Mbar)
    return np.percentile(a0, [16,50,84])

lo_sed, med_sed, hi_sed = mc_a0eff(Mstar_sed, Mstar_sed_e)
lo_par, med_par, hi_par = mc_a0eff(Mstar_par, Mstar_par_e)
# gas-only floor on M_bar => hard UPPER bound on a0_eff
Vc2_c = (V_rot*1e3)**2 + 3.4*(sig_int*1e3)**2
a0_gasceil = Vc2_c**2/(G*(HE*Mgas*Msun))
print("MEASURED a0_eff = V_circ^4/(G M_bar):")
print(f"  SED  M_star=3.7e11 :  {med_sed*1e10:.2f}  (+{(hi_sed-med_sed)*1e10:.2f}/-{(med_sed-lo_sed)*1e10:.2f}) e-10")
print(f"  PARAM M_star=1.7e11:  {med_par*1e10:.2f}  (+{(hi_par-med_par)*1e10:.2f}/-{(med_par-lo_par)*1e10:.2f}) e-10   <-- fair central")
print(f"  gas-only HARD UPPER bound (no stars): {a0_gasceil*1e10:.2f} e-10\n")

# ---- predictions on both footings ----
for name, a0loc in [("FRAMEWORK canonical (rho_DE)", 9.36e-11), ("empirical MOND (SPARC RAR)", 1.20e-10)]:
    aR = a0loc*E(z)
    aC = a0loc
    aD = a0loc*np.sqrt(rhoDE_ratio(z))
    print(f"[{name}]  local a0={a0loc*1e10:.2f}e-10, E({z})={E(z):.2f}, sqrt(rhoDE ratio)={np.sqrt(rhoDE_ratio(z)):.2f}")
    print(f"   H_RISE  a0({z}) = {aR*1e10:.2f}e-10   H_CONST = {aC*1e10:.2f}e-10   H_DECL = {aD*1e10:.2f}e-10")
    # velocity each hypothesis predicts for the PARAM-mass Big Wheel (fair central M_bar)
    Mbar_c = (Mstar_par + HE*Mgas)*Msun
    for tag, a0h in [("RISE",aR),("CONST",aC),("DECL",aD)]:
        Vpred = (G*a0h*Mbar_c)**0.25/1e3     # deep-MOND V_flat
        print(f"      V_pred[{tag}] = {Vpred:6.1f} km/s   (measured max {V_rot:.0f}+/-{V_err:.0f})")
    print()

# ---- significance of disfavouring the RISE branch (footing-robust, HONEST) ----
# a0_eff has a heavy UPPER tail, so a naive (aR-med)/upper_sigma ratio over-counts.
# The honest, transformation-invariant measure is the TAIL PROBABILITY P(a0_eff>=a0_rise),
# converted to an equivalent one-tailed Gaussian sigma via the inverse survival function.
from scipy.stats import norm
print("DISFAVOURING of the rising branch (a0 propto E(z)) -- tail probability, the honest measure:")
for name, a0loc in [("framework", 9.36e-11), ("empirical", 1.20e-10)]:
    aR = a0loc*E(z)
    V = np.random.normal(V_rot, V_err, 400000)*1e3
    Vc2 = V**2 + 3.4*(sig_int*1e3)**2
    Ms = np.clip(np.random.normal(Mstar_par, Mstar_par_e, 400000),0.05e11,None)
    Mg = np.clip(np.random.normal(Mgas, Mgas_e, 400000),0.05e11,None)
    a0 = Vc2**2/(G*(Ms+HE*Mg)*Msun)
    frac_above = np.mean(a0 >= aR)
    sig_tail = norm.isf(frac_above) if frac_above > 0 else np.inf
    med = np.percentile(a0,50); hi = np.percentile(a0,84)
    nsig_naive = (aR-med)/(hi-med)   # the INFLATED ratio, printed for contrast only
    print(f"  {name}: a0_RISE={aR*1e10:.2f}e-10 vs measured median {med*1e10:.2f}e-10  "
          f"P(a0_eff>=rise)={frac_above:.2e} -> {sig_tail:.1f} sigma (honest); "
          f"naive median/sigma ratio would read {nsig_naive:.1f} sigma (tail-inflated)")
    a0_gas = Vc2**2/(G*(HE*Mg)*Msun)   # gas-only ceiling: rise only ~1 sigma, NOT excluded
    fg = np.mean(a0_gas >= aR)
    print(f"     gas-only ceiling: P(>=rise)={fg:.2f} -> only ~{norm.isf(fg):.1f} sigma; NOT excluded there.")
print()
print("SUMMARY: a0_eff ~ 1.0-1.6e-10 (LOCAL, gas ceiling 2.55e-10); rising x5 DISFAVOURED ~2 sigma "
      "(P~1-3%) both footings, NOT excluded in the gas-only extreme; constant matches; "
      "DESI-declining (0.67e-10 framework / 0.86e-10 empirical) mildly low but consistent, undetected.")
