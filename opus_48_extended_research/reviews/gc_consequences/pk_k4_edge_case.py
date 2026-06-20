#!/usr/bin/env python3
"""
pk_k4_edge_case.py -- the BOTH-WAYS crux: at the FORCED edge mu^-1 = 1 Mpc (== M ~ 0.15 eV),
the GC graviton-mass handle and the AeST-mass handle AGREE at k_J ~ 1.5 h/Mpc, which IS inside
the Lyman-alpha / Euclid window. Does that corner give a DETECTABLE, DISTINCTIVE suppression,
or is it (i) self-inconsistent / excluded by galaxies, and (ii) degenerate with neutrino-mass /
WDM suppression already in the LCDM nuisance budget?

We test the edge honestly -- do NOT dismiss it reflexively, do NOT manufacture a signal.
"""
import numpy as np

c=2.99792458e8; G=6.67430e-11; hbar=1.054571817e-34; eV=1.602176634e-19
Mpc=3.0856775814913673e22; h=0.674
M_Pl_eV=2.435e27   # reduced Planck mass eV

print("="*84)
print("SELF-CONSISTENCY of the two handles (do they pick the SAME M?)")
print("="*84)
# Handle 2 says mu^-1 = 1 Mpc -> mu = 1 Mpc^-1.  Convert to graviton-mass eV:
mu_invm = 1.0/Mpc                          # 1/m  (mu = 1 Mpc^-1)
mu_eV   = mu_invm*hbar*c/eV                 # eV
print(f"  mu = 1 Mpc^-1  ->  mu = {mu_eV:.3e} eV")
# Handle 1: mu == m == M^2/(sqrt2 M_Pl) -> invert for M
M_from_mu = np.sqrt(np.sqrt(2)*M_Pl_eV*mu_eV)
print(f"  invert m = M^2/(sqrt2 M_Pl) = mu  ->  M = sqrt(sqrt2 M_Pl mu) = {M_from_mu:.3e} eV = {M_from_mu*1e3:.1f} meV")
print(f"  => the FORCED edge mu^-1=1 Mpc corresponds to M ~ {M_from_mu*1e3:.0f} meV ~ 0.13 eV,")
print(f"     which is EXACTLY the banked clustering-scale M~0.04-1 eV center. The two handles AGREE")
print(f"     (this is the self-consistency point, banked seesaw_two_scales M~0.15 eV <-> mu^-1=1 Mpc).")
print()
k_edge = (1.0/1.0)/h    # mu=1 Mpc^-1 -> h/Mpc
print(f"  At this edge: k_J = mu = 1 Mpc^-1 = {k_edge:.3f} h/Mpc  -- INSIDE the Lya/Euclid window.")
print()

print("="*84)
print("BOTH WAYS at the edge -- is k_J ~ 1.5 h/Mpc a DETECTABLE distinctive feature?")
print("="*84)
print("""
ARGUMENT IT *COULD* BE A SIGNAL (steelman, full weight):
  - At mu^-1 = 1 Mpc (the FORCED edge), k_J = mu = 1.48 h/Mpc IS inside the Lyman-alpha forest
    window (k ~ 0.3-10 h/Mpc) and the high-k Euclid weak-lensing window. A Jeans/mass cutoff at
    k_J would SUPPRESS small-scale power -- a genuine sub-Mpc P(k) modification, in principle
    measurable by Lya (the tightest small-scale P(k) probe, sensitive to ~few-% suppression).

WHY IT IS NOT A CLEAN NEW FRONT (rebuttals, full weight):
  1. EXCLUDED-BY-GALAXIES at exactly that edge. mu^-1 = 1 Mpc is the ABSOLUTE lower bound; VSB24
     show the oscillation onset r_C = 156 kpc at mu=1/Mpc, which sits INSIDE galaxy/cluster outskirts
     and is squeezed by galaxy weak-lensing data toward mu^-1 = tens of Mpc (k_J -> 0.01-0.05 h/Mpc,
     OUT of the Lya window). So the only corner where k_J reaches the Lya window is the corner most
     disfavored by the galaxy data the framework must fit. You cannot have the Lya feature AND the
     galaxy MOND fits.
  2. DEGENERATE with a known LCDM nuisance: a Jeans/mass SUPPRESSION at k~1 h/Mpc is the SAME shape
     as (a) massive-neutrino free-streaming suppression and (b) warm-dark-matter / thermal cutoff,
     both already marginalized in every Lya/Euclid LCDM analysis. A single suppression scale with a
     free amplitude (mu is free) is absorbed by sum-m_nu + the Lya thermal/pressure-smoothing
     nuisance parameters -- not a distinctive oscillation, no node structure, no phase.
  3. NOT PARAMETER-FREE: k_J = mu is a FREE parameter (banked: mu squeezed in opposite directions by
     galaxy-WL vs clusters = the signature of a free constant). a0 = c^2 sqrt(Lambda/32pi) does NOT
     set mu (d rho_dust/d a0 = 0; the Y-sector a0 and the Q/mu-sector are orthogonal). So even a
     detected cutoff would not be a PREDICTION -- mu would just be fit, like sum-m_nu.
  4. SZ21 ALREADY put mu in this range for their CMB+P(k) fit and the linear P(k) came out a
     few-% TUNED mimic of LCDM (function-dependent residual, per-model bias b). Empirically the
     edge does NOT produce a standout feature in their own computed P(k).
""")

print("="*84)
print("Lya sensitivity sanity check")
print("="*84)
# Lya 1D flux power probes k ~ 0.5-20 h/Mpc (3D ~ 0.1-few h/Mpc); sensitive to suppressions
# at the ~few-% level. A WDM-like cutoff with k_J ~ 1 h/Mpc would be a ~O(1) suppression at
# k > k_J -- i.e. a LARGE effect, which is exactly why mu^-1=1 Mpc is DISFAVORED, not a discovery.
print("""
  Lya 1D flux power is sensitive to P(k) suppressions of a few % at k ~ 1-10 h/Mpc, and currently
  BOUNDS WDM to m_WDM > ~5 keV (cutoff k > ~20-50 h/Mpc) and sum-m_nu < ~0.1 eV. A GC Jeans cutoff
  at k_J = 1.5 h/Mpc would be a GROSS (order-unity) suppression of small-scale power -- already
  RULED OUT by Lya for a sharp cutoff, and only allowed if mu^-1 >> 1 Mpc (k_J << 1 h/Mpc, OUT of
  the window). So the edge is not a 'new detectable front': it is either (a) excluded if sharp at
  k~1 h/Mpc, or (b) pushed below the window (k_J<0.05 h/Mpc) where it is degenerate with b/A_s and
  cosmic-variance-limited. EITHER WAY: no clean distinctive P(k) signal. HONEST NULL.
""")

print("="*84)
print("EDGE-CASE VERDICT")
print("="*84)
print("""
The two handles agree (M~0.13 eV <-> mu^-1=1 Mpc <-> k_J~1.5 h/Mpc), so there IS a corner where
the GC Jeans scale lands in the Lya/Euclid window -- credited at full weight. But that corner is
(i) the most galaxy-DISFAVORED edge of the forced mu^-1>~1 Mpc band, (ii) a single SUPPRESSION
scale degenerate with sum-m_nu and WDM/thermal nuisances already marginalized, (iii) set by the
FREE parameter mu (not by a0/Lambda), and (iv) a sharp cutoff at k~1 h/Mpc is already in tension
with Lya WDM bounds. Pushed to the galaxy-FAVORED region (mu^-1 = tens of Mpc) the feature exits
the window (k_J < 0.05 h/Mpc) and becomes cosmic-variance/bias-degenerate. NET: the edge does not
rescue a distinctive front -- it is an EXCLUDED-or-DEGENERATE null, both ways.
""")
