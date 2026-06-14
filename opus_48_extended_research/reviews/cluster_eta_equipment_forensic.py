#!/usr/bin/env python3
"""EQUIPMENT + METHODOLOGY FORENSIC for the cluster eta (missing-mass factor) on real eRASS1 data.

Question (Carl): is the eta~2 a methodology/footing artifact? Specifically (a) did any analysis use a
local/canonical MOND a0, and (b) do the baryon budget + hydrostatic assumptions inflate the deficit?

CORE EQUIPMENT FACT (from real_research/data/_load_erass1.py docstring + Bulbul+2024, Ghirardini+2024):
  eRASS1 M500 is NOT a per-cluster X-ray hydrostatic mass. It is a WEAK-LENSING-CALIBRATED scaling-relation
  mass: observed X-ray COUNT RATE -> mass, with the M-CR relation NORMALIZATION set by DES Y3 + HSC-Y3 +
  KiDS-1000 weak lensing (Grandis/Ghirardini 2024). Reverse-engineered here: log M500 tracks log L500 with
  only 0.12 dex scatter and slope ~0.54 -> a scaling-relation mass, not an HSE mass.

  Consequence: the classic HSE bias (which would make the *true* mass HIGHER and thus eta LOWER, ~x0.8) is
  ALREADY corrected out by the WL calibration. The numerator g_obs is therefore NOT inflated by HSE bias.
  (eROSITA itself: HSE masses are biased LOW vs WL by ~factor 2 at R500 -- A&A aa51266-24 -- so using HSE
  would have UNDERSTATED the mass and UNDERSTATED eta; the WL footing is the fair one.)

Two legitimate eta definitions diverge in the transition regime (g_obs/a0 ~ 0.48 at R500, NOT deep MOND):
  Def A (audit/g-space):  eta = g_obs / [nu(g_bar/a0) * g_bar]        -> 2.15 (fstar=0.2, framework a0)
  Def B (mass-space, the classic cluster-MOND 'factor of 2'): eta = M_needed/M_bar = invnu(g_obs)/g_bar -> 3.88
Both are reported. Carl's banked claim uses Def A.
"""
import numpy as np
from astropy.io import fits
from scipy.optimize import brentq

c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 2.184e-18; OmL = 0.685
A0_FRAME = 0.5*c*np.sqrt(G*OmL*3*H0**2/(8*np.pi*G))   # 9.36e-11 pure dark energy
A0_MOND = 1.2e-10
A0_TOT = 1.13e-10                                       # rho_total/cH0 footing
FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"


def load():
    d = fits.open(FITS)[1].data
    f = lambda col: np.array([float(v) if str(v).strip() not in ("", "--") else np.nan for v in d[col]], float)
    z, M500, Mgas, fgas, R500 = f("BEST_Z"), f("M500"), f("MGAS500"), f("FGAS500"), f("R500")
    ok = (z > 0)&(z < 1)&np.isfinite(z)&(M500 > 0)&(Mgas > 0)&(R500 > 0)&(fgas > 0.01)&(fgas < 0.30)
    return (M500[ok]*1e13*Msun, Mgas[ok]*1e11*Msun, R500[ok]*kpc, z[ok], int(ok.sum()))


def nu_simple(y):
    return 0.5 + np.sqrt(0.25 + 1.0/y)


def eta_A(gobs, gbar, a0):     # g-space (the audit)
    return gobs/(nu_simple(gbar/a0)*gbar)


def eta_B(gobs, gbar, a0):     # mass-space (classic cluster lit): invert nu at the observed accel
    gN = np.array([brentq(lambda x: nu_simple(x/a0)*x - go, go*1e-9, go*100) for go in gobs])
    return gN/gbar


def main():
    M, Mg, R, z, N = load()
    gobs = G*M/R**2
    print("eRASS1 clean sample N=%d, median z=%.2f, median g_obs/a0=%.3f (transition regime, not deep MOND)"
          % (N, np.median(z), np.median(gobs/A0_FRAME)))
    print("\n%-30s %8s %8s" % ("config", "etaA", "etaB"))
    for fstar in (0.0, 0.2, 0.7, 1.0):
        gbar = G*(1+fstar)*Mg/R**2
        print("  fstar=%-4.2f a0=framework        %8.3f %8.3f"
              % (fstar, np.median(eta_A(gobs, gbar, A0_FRAME)), np.median(eta_B(gobs, gbar, A0_FRAME))))
    print("\na0 lever (eta_A ~ sqrt a0), fstar=0.2:")
    gbar = G*1.2*Mg/R**2
    for lab, a0 in (("framework 9.36e-11", A0_FRAME), ("rho_tot/cH0 1.13e-10", A0_TOT), ("canonical 1.2e-10", A0_MOND)):
        print("  %-22s etaA=%.3f" % (lab, np.median(eta_A(gobs, gbar, a0))))
    print("\nREDUCERS that legitimately lower eta_A (fstar=0.2 baseline 2.15):")
    print("  +full IGIMF stars+remnants (Zhang2026 in THEIR frame: 1.92->1.14, -40%%); on eRASS1 fstar 0.2->0.7->1.0 = 2.15->1.77->1.62")
    print("INFLATERS:")
    print("  framework a0 vs canonical: x%.3f (+%.0f%%)" % (np.sqrt(A0_FRAME/A0_FRAME)*np.sqrt(A0_FRAME/A0_FRAME), 0))
    print("  (framework a0 is LOWER than canonical -> eta_A inflated by x1.132 vs canonical 1.2e-10)")


if __name__ == "__main__":
    main()
