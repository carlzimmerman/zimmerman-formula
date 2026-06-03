#!/usr/bin/env python3
"""
The decisive test of a0=(c/2)sqrt(G rho): the SPARC radial-acceleration relation.
================================================================================
The density law that fixes clusters predicts a0 ~ sqrt(rho_ambient). So a0 must
VARY between galaxies as half the variation in their ambient density. The galaxy
RAR is one of the tightest relations in astrophysics -- that tightness is a hard
budget. The crux: the SAME smoothing scale that makes a cluster dense enough to
need a0~13x ALSO makes field galaxies' densities vary a lot -> too much a0 scatter.
Is there ANY smoothing scale that threads both needles?

PART 1: fit a0 per SPARC galaxy from the repo data, measure the observed scatter.
PART 2: density-law prediction vs smoothing scale R -- cluster boost AND field a0
        scatter -- and check for an overlap window. Needs numpy + the SPARC files.
"""
import numpy as np, glob, os

c, G, kpc, Mpc, Msun = 2.99792458e8, 6.674e-11, 3.0857e19, 3.0857e22, 1.989e30
A0 = 1.2e-10
ML_D, ML_B = 0.5, 0.7                      # SPARC 3.6um stellar M/L (standard)
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")


# ---------- PART 1: per-galaxy a0 from SPARC rotation curves ----------------
def fit_sparc_a0():
    a0s = []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[0] < 3 or d.shape[1] < 6:
            continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        R_m = R*kpc
        Vbar2 = np.sign(Vgas)*Vgas**2 + ML_D*Vdisk**2 + ML_B*Vbul**2     # (km/s)^2
        gbar = Vbar2*1e6/R_m                                              # m/s^2
        gobs = (Vobs*1e3)**2/R_m
        deep = (gbar > 0) & (gobs > 0) & (gbar < 0.3*A0)                  # deep-MOND pts
        if deep.sum() < 2:
            continue
        a0_est = gobs[deep]**2/gbar[deep]                                 # gobs^2 = gbar a0
        a0s.append(np.median(a0_est))
    a0s = np.array(a0s)
    lg = np.log10(a0s[(a0s > 1e-11) & (a0s < 1e-8)])
    print("="*80); print("PART 1 -- a0 fitted per SPARC galaxy (deep-MOND points, M/L=0.5)"); print("="*80)
    print(f"  galaxies fit            : {lg.size}")
    print(f"  median a0               : {10**np.median(lg):.2e} m/s^2  (canonical 1.2e-10)")
    print(f"  raw scatter sigma(log10 a0) : {np.std(lg):.3f} dex  <-- METHOD-DOMINATED upper bound")
    print(f"     (fixed M/L=0.5, no distance/inclination/M-L deconvolution, crude estimator;")
    print(f"      this is NOT the intrinsic scatter -- it is inflated by my measurement noise)")
    print(f"  Lelli+2017 (proper deconvolution): RAR scatter 0.13 dex TOTAL, <=0.06 dex INTRINSIC")
    print(f"     -> the intrinsic value is the operative budget for an environmental a0.")
    return np.std(lg)


# ---------- PART 2: density-law prediction vs smoothing scale ---------------
def sigma_density(R_Mpc):
    """rms linear density contrast smoothed on top-hat R (sigma8=0.81 @ 8 h^-1Mpc)."""
    return 0.81*(R_Mpc/(8/0.7))**(-0.55)            # approx LCDM slope on these scales

def a0_scatter_dex(R_Mpc):
    s = sigma_density(R_Mpc)
    return 0.5*np.sqrt(np.log(1+s**2))/np.log(10)   # a0 ~ sqrt(rho); lognormal density

def cluster_boost(R_Mpc):
    """sqrt(ambient density / mean) for a massive cluster smoothed on R."""
    # representative M(<R) for a cluster embedded in a supercluster [Msun]:
    Rs  = np.array([1, 2, 4, 8, 16, 30, 50])
    Ms  = np.array([6e14, 1e15, 1.5e15, 2.5e15, 5e15, 1.2e16, 3e16])
    M   = np.interp(R_Mpc, Rs, Ms)
    rho_amb = M/((4/3)*np.pi*R_Mpc**3)              # Msun/Mpc^3
    rho_bar = 0.315*1.4e11                          # Omega_m * rho_crit  [Msun/Mpc^3]
    return np.sqrt(rho_amb/rho_bar)


def main():
    obs = fit_sparc_a0()
    print("\n"+"="*80)
    print("PART 2 -- can ANY smoothing scale fix clusters AND keep the RAR tight?")
    print("="*80)
    print(f"  density law: a0 ~ sqrt(rho_ambient).  Cluster needs a0 ~ 13x. Budget for an")
    print(f"  environmental a0 = the INTRINSIC RAR scatter <=0.06 dex (Lelli+2017; total 0.13).")
    print(f"  (My crude fit gave {obs:.2f} dex but that is method-dominated, not the budget.)\n")
    print(f"  {'R[Mpc]':>7}{'sigma_dens':>11}{'pred a0 scatter[dex]':>22}{'cluster a0 boost':>18}")
    print("  " + "-"*56)
    for R in (2, 3, 4, 6, 8, 12, 20, 30, 50):
        print(f"  {R:>7}{sigma_density(R):>11.2f}{a0_scatter_dex(R):>22.3f}{cluster_boost(R):>16.1f}x")
    print(f"""
  READING IT:
   - To get the cluster boost up to ~13x you need R ~ 3-4 Mpc. There the predicted
     field-galaxy a0 scatter is ~0.23-0.27 dex -- ~4x the observed intrinsic RAR
     scatter (0.06) and ~2x the total (0.13). EXCLUDED by the RAR.
   - To get the a0 scatter down to the observed ~0.06-0.13 dex you need R >~ 30-50
     Mpc. There the cluster boost is only ~1.4-2x -- it does NOT fix clusters.
   - The two requirements pull the smoothing scale in OPPOSITE directions by ~15x.
     There is NO single scale that fixes clusters and keeps the RAR tight.""")
    print("\n"+"="*80); print("VERDICT -- the density law is caught between clusters and galaxies"); print("="*80)
    print(f"""  The elegant single formula a0=(c/2)sqrt(G rho) CANNOT have it both ways:
    * COSMIC-only rho (rho = rho_bar(z)):  tight RAR preserved (a0 universal), but
      clusters get NO boost -> the cluster residual stays (my earlier finding).
    * LOCAL-ambient rho (Mpc-smoothed):    fixes clusters (a0~13x), but predicts
      ~0.24 dex of a0 scatter across field galaxies -- vs the RAR intrinsic scatter
      <=0.06 dex (excluded ~4x) and even the 0.13 dex total (excluded ~2x).
  So the cluster 'success' I found and the tight galaxy RAR are MUTUALLY EXCLUSIVE
  under one density law. This is the decisive constraint, and it lands AGAINST the
  environmental reading. The density law survives only in its cosmic form (the
  a0(z) evolution) -- which is exactly the part that does NOT fix clusters.

  Honest bottom line: a0=(c/2)sqrt(G rho) is beautiful and gets the cosmic value +
  the cluster value in isolation, but no single coarse-graining makes it fit
  galaxies AND clusters together. That is a real, falsifiable result -- and it is
  the sharpest thing we have learned about the formula.""")
    print("="*80)


if __name__ == "__main__":
    main()
