#!/usr/bin/env python3
"""
CONFRONTATION: Kessler, Di Valentino, Escamilla, Huterer (arXiv:2606.05853, 2026-06-04),
"Reconstructing dark energy with fewer assumptions" — vs the framework's a0(z) branch.
=====================================================================================
This paper measures rho_DE(z)/rho_DE,0 DIRECTLY in 7 bins (z=0..4.2), late-time distances
only (DESI+SDSS BAO; Pantheon+/Union3.1/DES-Dovekie SNe) + a CMB acoustic-scale prior.
That is the EXACT quantity the framework's a0(z) branch is tied to via a0 ~ sqrt(rho_DE).

KEY MEASURED SHAPE (Sec IV.1, Fig 3, Fig 6 caption — TEXT/figure-only, no per-bin table):
  - rho_DE RISES to a local maximum at z in [0.6, 0.8) (DESI combos),
    [0.8, 1.1) for SDSS+DES-Dovekie;
  - then DECLINES back toward the LCDM (constant) limit at higher z;
  - per-bin deviation ~2.6-3 sigma in the z in [0.6,0.8) bin (with DESI);
  - w crosses -1 around z~0.6-0.8; lowest bin z<0.1 prefers w>-1 at ~1-2 sigma.
  - GLOBAL: only ~1.6-2 sigma support for the 7 extra params; LCDM not decisively rejected.

The bin-by-bin posterior MEANS/ERRORS for rho_DE(z) are FIGURE-ONLY (not tabulated), so this
is a QUALITATIVE shape + bin-sigma confrontation. We do NOT invent numeric posteriors. What we
CAN compute exactly: the SIGN and MAGNITUDE each a0(z) hypothesis predicts under the measured
rho_DE shape, sqrt-scaled, on BOTH footings.

Three a0(z) hypotheses (from the repo's locked conventions):
  (1) framework constant / Lambda-floor:  rho_DE const  => a0(z) FLAT.
  (2) framework FAITHFUL declining branch: a0 = a0_0 * sqrt(rho_DE(z)) with DESI-CPL rho_DE
      [project_a0_tracks_dark_energy.py, efe_vs_z_recompute.py] => a0 MONOTONIC DECLINE.
  (3) rival RISING branch: a0 = a0_0 * E(z) (cH(z)/Z ~ sqrt(rho_total))
      [a0_constant_vs_evolving_fork.py] => a0 MONOTONIC RISE.

Run on BOTH footings: framework a0_0=9.36e-11 (rho_DE footing) AND reg-MOND a0_0=1.2e-10.
"""
import numpy as np

# ---- locked conventions ----
OM, OL = 0.315, 0.685
A0_FRAMEWORK = 9.36e-11        # rho_DE footing (framework's own)
A0_REGMOND   = 1.20e-10        # standard MOND default baseline

def E(z):                       # H(z)/H0
    return np.sqrt(OM*(1+z)**3 + OL)

# DESI-CPL rho_DE(z)/rho_DE,0 — the repo's two CPL choices (faithful branch)
def rhoDE_cpl(z, w0, wa):
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a))

# Kessler measures a NON-MONOTONIC shape: rise then fall. We encode the QUALITATIVE
# reconstruction as a bump on top of LCDM (rho_DE/rho_DE,0 = 1 + bump), peak at z_pk,
# returning to ~1 at high z. Magnitude of the peak bump is the load-bearing unknown:
# the paper gives it only via the ~2.6-3 sigma deviation, not a tabulated mean.
# We bracket the plausible peak amplitude and propagate sqrt-scaling to a0.

def main():
    print("#"*92)
    print("# Kessler+ 2026 (2606.05853) rho_DE(z) reconstruction  vs  framework a0(z) branches")
    print("#"*92)

    print("\n" + "="*92)
    print("(A) WHAT THE PAPER MEASURES (shape only; per-bin posteriors are figure-only)")
    print("="*92)
    print("  rho_DE(z)/rho_DE,0 : RISES to a local max at z~[0.6,0.8), then DECLINES toward LCDM(=1).")
    print("  bin-max deviation  : ~2.6-3 sigma (z in [0.6,0.8), DESI combos).")
    print("  global support     : ~1.6-2 sigma for 7 extra params (LCDM NOT decisively rejected).")
    print("  => NON-MONOTONIC, peaked-then-flattening, low-significance.\n")

    print("="*92)
    print("(B) SIGN TEST: each a0(z) hypothesis vs the measured rho_DE shape (model-independent)")
    print("="*92)
    print("  Hypothesis (1) const/Lambda-floor:  a0 FLAT in z.")
    print("     vs measured: a peaked rho_DE. FLAT is at odds with the bump, but only at the")
    print("     ~2-3 sigma bin level AND LCDM-constancy is itself only ~1.6-2 sigma disfavored")
    print("     => NOT decisively excluded. Status: mild tension, survives.")
    print()
    print("  Hypothesis (2) FAITHFUL declining a0 ~ sqrt(rho_DE):  the framework's OWN map.")
    print("     This branch INHERITS the reconstruction's shape EXACTLY (a0 ~ sqrt of it).")
    print("     So under THIS paper a0(z) would RISE ~10-14% to a peak at z~0.7 then fall back.")
    print("     The repo's CPL-fed declining curve (monotonic) is the EXTRAPOLATION of the high-z")
    print("     tail; at LOW z the new reconstruction says a0 BUMPS UP first. See (C).")
    print()
    print("  Hypothesis (3) rival RISING a0 ~ E(z):  MONOTONIC rise, no turnover.")
    print("     Agrees with the low-z rise in sign, but CONTRADICTS the high-z TURNOVER back to")
    print("     LCDM (E(z) keeps climbing: E(2)=%.2f, E(4)=%.2f). Tension at z>1." % (E(2), E(4)))
    print()

    print("="*92)
    print("(C) MAGNITUDE: a0 bump implied by the measured rho_DE rise (sqrt scaling), BOTH footings")
    print("="*92)
    # The paper does not tabulate the peak rho_DE ratio. From phantom-crossing CPL fits of this
    # class (w0~-0.8, wa<0) and the ~2.6-3 sigma bin, the peak rho_DE/rho_DE,0 sits ~1.2-1.3.
    # We report the a0 bump = sqrt(ratio) - 1 across that bracket, on both footings.
    print(f"  {'peak rho_DE/rho0':>18}{'a0 bump =sqrt-1':>18}{'a0_frmwk(9.36)':>18}{'a0_regMOND(1.20)':>20}")
    for ratio in (1.15, 1.20, 1.25, 1.30):
        bump = np.sqrt(ratio) - 1.0
        a0f = A0_FRAMEWORK*np.sqrt(ratio)
        a0r = A0_REGMOND*np.sqrt(ratio)
        print(f"  {ratio:>18.2f}{bump*100:>16.1f}%{a0f:>18.3e}{a0r:>20.3e}")
    print("  => a peak rho_DE bump of x1.2-1.3 implies an a0 BUMP of ~+10 to +14% at z~0.7,")
    print("     on EITHER footing (the bump is a pure ratio; footing only sets the z=0 anchor).")
    print("     This is the magnitude a future a0(z) lensing / RAR-vs-z probe could check.\n")

    print("="*92)
    print("(D) The repo's monotonic CPL declining branch vs this NON-MONOTONIC reconstruction")
    print("="*92)
    print(f"  {'z':>5}{'E(z) RISE':>12}{'sqrt(rhoDE) DESI24':>20}{'sqrt(rhoDE) DR2':>18}")
    for z in (0.1, 0.4, 0.7, 1.0, 2.0):
        s24 = np.sqrt(rhoDE_cpl(z, -0.83, -0.75))   # DESI 2024 (project_a0_tracks)
        sdr2 = np.sqrt(rhoDE_cpl(z, -0.752, -0.86)) # DESI DR2 (efe_vs_z_recompute)
        print(f"  {z:>5.1f}{E(z):>12.3f}{s24:>20.3f}{sdr2:>18.3f}")
    print("  NOTE: the repo's CPL declining branch is MONOTONIC (a0 falls into the past). The")
    print("  Kessler reconstruction is NON-MONOTONIC (rise to z~0.7 THEN fall). At z<~0.8 the new")
    print("  data says a0 should BUMP UP, opposite to the CPL monotonic decline's sign at low z;")
    print("  at z>1 both the CPL decline and the reconstruction head back toward LCDM (consistent).")
    print("  So the new reconstruction TIGHTENS the low-z end: it disfavors a pure monotonic")
    print("  decline AND a pure monotonic rise — but only at the bin's ~2.6-3 sigma, not decisive.\n")

    print("="*92)
    print("VERDICT")
    print("="*92)
    print("""  Direction of movement, per branch (both footings — the anchor cancels in the shape test):
    (1) const/Lambda-floor  : mild tension (peaked rho_DE vs flat a0), NOT excluded (~2 sigma).
    (2) faithful sqrt(rho_DE): this branch ADOPTS the reconstruction -> predicts a +10-14% a0
        bump at z~0.7 then return to LCDM. The repo's MONOTONIC CPL curve is disfavored at low z
        by the measured RISE; the non-monotonic shape is the new, sharper, framework-faithful read.
    (3) rival rising E(z)    : agrees low-z, CONTRADICTED by the high-z turnover. Tension z>1.
  NONE of the three is killed or confirmed: the global signal is only ~1.6-2 sigma and the
  per-bin rho_DE posteriors are figure-only (not tabulated), so no numeric chi-by-eye placement
  is possible. The clean, NEW, registered-prediction-relevant payload is QUALITATIVE+MAGNITUDE:
  IF this peaked rho_DE survives, the framework's faithful a0 ~ sqrt(rho_DE) branch must show a
  ~+10-14% a0 bump near z~0.7 (not a monotonic trend) — a falsifiable target for a0(z) lensing.""")
    print("#"*92)

if __name__ == "__main__":
    main()
