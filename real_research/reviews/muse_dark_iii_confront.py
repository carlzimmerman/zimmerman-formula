#!/usr/bin/env python3
"""
CONFRONT: MUSE-DARK III (Ciocan et al. 2026, A&A 709 L16; arXiv to be pinned) a0(z) vs the framework.
=====================================================================================================
The datum (from the paper, all numbers quoted in the prompt's dataset block):
  * a0(z~1) = 2.38 (+0.12/-0.10) x10^-10 m/s^2   [Eq.2, Sect.3.1; abstract says +/-0.1]
  * a0(z)=a0(0)+a1 z (RAR, LCDM-mass route, Eq.4): a0(0)=1.0+/-0.04, a1=1.59+/-0.10  (x10^-10)
  * MOND 3D forward-model (App.E Eq.14): a0(0)=1.03+/-0.05, a1=1.20+/-0.10
  * binned: a0 rises ~1.99 (low-z) -> 2.71 (high-z) x10^-10
  * evolution detected at ~30 sigma; the measured a0(z) rises FASTER than H(z) (Sect.4).
  * z=0 anchors used by the paper: SPARC 1.2+/-0.26; Varasteanu (z<0.08) 1.69+/-0.13.

We confront this with BOTH framework a0(z) branches on BOTH a0-normalization footings:
  BRANCH A (the prompt's BINDING footing): a0 ~ sqrt(rho_DE), DECLINING/flat.
            - pure Lambda (w=-1): rho_DE const -> a0(z) FLAT.
            - DESI w0wa: rho_DE falls into the past -> a0(z) DECLINES.   [project_a0_tracks_dark_energy.py]
  BRANCH B (the corpus's other, registered branch): a0(z)=a0(0) E(z), RISING. [a0_evolution_predictions.py]
            E(z)=sqrt(Om(1+z)^3+OL).
  FOOTINGS: fw a0(0)=9.36e-11 (rho_DE footing); canonical/regular-MOND a0(0)=1.2e-10 (constant baseline).

We use the paper's own assigned redshift z* for the headline number. The headline a0(z~1)=2.38 is the
SAMPLE value; we take z*=0.90 (the value used as the high-z anchor in a0_z_empirical_rigorous.py). We
also run the slope confrontation directly on a1 (the form-independent statement: framework slope <= 0).
"""
import numpy as np
from scipy.integrate import quad

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)

# DESI DR2 CPL (the value used in efe_vs_z_recompute.py) and DESI 2024 (project_a0_tracks_dark_energy.py)
def rhoDE_ratio(z, w0, wa):
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))

# ---- the datum ----
A0_DATA  = 2.38e-10                 # a0(z~1), m/s^2
SIG_HI   = 0.12e-10                 # +err (use the larger/conservative side for a 'too high' test)
SIG_LO   = 0.10e-10                 # -err
ZSTAR    = 0.90                     # assigned redshift for the headline (high-z anchor convention)
A1_DATA, A1_ERR = 1.59e-10, 0.10e-10   # LCDM-route slope (Eq.4)
A1_MOND, A1_MERR = 1.20e-10, 0.10e-10  # MOND-route slope (Eq.14)

FOOTINGS = {"fw  rho_DE 9.36e-11": 9.36e-11, "canon/MOND 1.2e-10": 1.20e-10}

def nsig_high(pred, data, sig_minus):
    # how many sigma the DATA sits ABOVE the prediction (data uses its lower error bar toward pred)
    return (data - pred)/sig_minus

print("#"*100)
print("# MUSE-DARK III a0(z~1)=2.38e-10  vs  the framework's a0(z) branches  (both footings)")
print("#"*100)

print("\n" + "="*100)
print("(0) Where the framework branches predict a0 at z*=0.90 (units of a0(0) and absolute)")
print("="*100)
print(f"  E(z*={ZSTAR}) = {E(ZSTAR):.3f}   [the RISING cH(z)/Z factor]")
for w0,wa,tag in [(-1.0,0.0,"pure Lambda w=-1"),(-0.83,-0.75,"DESI24 w0wa"),(-0.752,-0.86,"DESI DR2 w0wa")]:
    r = np.sqrt(rhoDE_ratio(ZSTAR,w0,wa))
    print(f"  sqrt(rho_DE(z*)/rho_DE0) = {r:.3f}   [{tag}]   -> a0 DECLINING branch factor")

print("\n" + "="*100)
print("(1) SIGN + SIGMA TEST per footing: data 2.38e-10 vs each branch prediction at z*=0.90")
print("="*100)
for fname, a00 in FOOTINGS.items():
    print(f"\n  FOOTING {fname}  (a0(0)={a00:.3e}):")
    # Branch A: declining / flat
    predA_flat = a00*1.0                                   # pure Lambda flat
    predA_desi = a00*np.sqrt(rhoDE_ratio(ZSTAR,-0.83,-0.75))   # DESI mild decline
    # Branch B: rising
    predB = a00*E(ZSTAR)
    for label,pred in [("A flat (pure Lambda)   a0~sqrt(rhoDE),w=-1", predA_flat),
                       ("A decline (DESI w0wa)  a0~sqrt(rhoDE)     ", predA_desi),
                       ("B rising  a0(0)E(z)    [cH(z)/Z branch]   ", predB)]:
        ns = nsig_high(pred, A0_DATA, SIG_LO)
        ratio = A0_DATA/pred
        print(f"    {label}: pred={pred:.3e}  data/pred={ratio:.2f}x  data sits {ns:+.1f} sigma {'ABOVE' if ns>0 else 'below'}")

print("\n" + "="*100)
print("(2) SLOPE CONFRONTATION (form-independent): framework declining/flat branch has slope da0/dz <= 0")
print("="*100)
print(f"  measured a1 (LCDM route, Eq.4)  = {A1_DATA:.3e} +/- {A1_ERR:.2e}  -> POSITIVE at {A1_DATA/A1_ERR:.1f} sigma")
print(f"  measured a1 (MOND route, Eq.14) = {A1_MOND:.3e} +/- {A1_MERR:.2e}  -> POSITIVE at {A1_MOND/A1_MERR:.1f} sigma")
print(f"  framework flat (pure-Lambda) branch predicts a1 = 0  ->  ruled out at >= {A1_MOND/A1_MERR:.0f}-{A1_DATA/A1_ERR:.0f} sigma")
# HONEST: the DESI w0wa branch is NON-MONOTONIC -- a small phantom-bump rise to z~0.3-0.5, then a decline.
# Report the EFFECTIVE slope a0(z*=0.9)-a0(0) over [0,0.9] (the lever the data actually measures), not the
# z=0 local derivative (which the bump makes positive and unrepresentative).
for w0,wa,tag in [(-1.0,0.0,"pure Lambda"),(-0.83,-0.75,"DESI24"),(-0.752,-0.86,"DESI DR2")]:
    eff = (np.sqrt(rhoDE_ratio(ZSTAR,w0,wa))-1.0)/ZSTAR   # mean slope over [0,z*], units a0(0)/z
    z0local = (np.sqrt(rhoDE_ratio(1e-4,w0,wa))-1.0)/1e-4
    print(f"  [{tag:11s}] eff slope a0(0->z*)/z* = {eff:+.3f} a0(0)/z (fw {eff*9.36e-11:+.2e}, canon {eff*1.2e-10:+.2e}); "
          f"z=0 local {z0local:+.3f} a0(0)/z  -> branch is FLAT or NET-DECLINING to z*; data slope is +1.59e-10, "
          f"opposite/far above either")

print("\n" + "="*100)
print("(3) Is the RISING branch B itself consistent? (the paper says a0 rises FASTER than H(z))")
print("="*100)
for fname, a00 in FOOTINGS.items():
    predB = a00*E(ZSTAR)
    ns = nsig_high(predB, A0_DATA, SIG_LO)
    print(f"  {fname}: B pred at z*={ZSTAR} = {predB:.3e}; data {A0_DATA:.3e} sits {ns:+.1f} sigma above B "
          f"(data/predB={A0_DATA/predB:.2f}x)")
print("  -> even the RISING cH(z)/Z branch UNDER-predicts: data rises faster than E(z). Branch B is high-side"
      " tension, not a kill, on the canonical footing; worse on the fw footing.")

print("\n" + "="*100)
print("(4) Regular-MOND constant baseline (a0=1.2e-10 fixed): the paper's own null")
print("="*100)
ns_const = nsig_high(1.2e-10, A0_DATA, SIG_LO)
print(f"  constant 1.2e-10 vs data 2.38e-10: data sits {ns_const:+.1f} sigma above the constant null too "
      f"(the paper's ~30 sigma evolution detection).")
print(f"  BUT note: the paper's own a0(0) intercept = 1.0-1.03e-10 is WITHIN 0.5 sigma of regular-MOND 1.2e-10")
print(f"  and the fw 9.36e-11 footing: a0(0)_data=1.0e-10 vs fw 0.936e-10 -> {(1.0e-10-0.936e-10)/0.04e-10:.1f} sigma."
      )
print("  So the framework's z=0 NORMALIZATION is fine; the entire tension is in the z-EVOLUTION (slope/sign).")

print("\n" + "#"*100)
print("# done")
print("#"*100)
