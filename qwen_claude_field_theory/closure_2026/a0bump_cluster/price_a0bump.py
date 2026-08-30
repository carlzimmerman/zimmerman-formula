#!/usr/bin/env python3
"""PRICE the a0-bump cluster route: enhance a0 at cluster scales to explain the ~2x dynamical residual
(the classic MOND cluster problem), WITHOUT breaking galaxies/solar-system/CMB. Grounded in the repo's
numbers (a0=9.36e-11, g_obs=sqrt(g_bar^2+g_bar a0), residual eta~1.72-2.08 core). sympy + numerics."""
import sympy as sp, math

print("=== 1. what the bump must deliver ===")
# deep MOND g ~ sqrt(g_bar a0). cluster residual eta = g_obs_needed/g_MOND ~ 1.72-2.08 (core, kernel-dep).
# to get eta_g in g via an a0 enhancement: g~sqrt(a0 g_bar) => g doubles when a0 quadruples.
for eta in [1.72, 2.08]:
    a0_boost = eta**2
    print(f"   cluster residual eta_g = {eta} (extra gravity)  => a0 must be BUMPED x{a0_boost:.1f} in clusters")
print("   => a factor ~3-4x a0 enhancement at cluster scales (large, not a small perturbation).")

print("\n=== 2. the trigger problem: clusters and galaxy-outskirts OVERLAP in acceleration ===")
c,G,Msun,Mpc,kpc = 2.998e8,6.674e-11,1.989e30,3.086e22,3.086e19
a0 = 9.36e-11
# cluster core accel: sigma~1000 km/s over ~0.5 Mpc
sig=1e6; Rc=0.5*Mpc; g_cl=sig**2/Rc
# galaxy outskirt accel: v~150 km/s at ~20 kpc
vg=1.5e5; Rg=20*kpc; g_gal=vg**2/Rg
print(f"   cluster core:      g ~ sigma^2/R = {g_cl:.2e} = {g_cl/a0:.2f} a0  (deep MOND)")
print(f"   galaxy outskirt:   g ~ v^2/R     = {g_gal:.2e} = {g_gal/a0:.2f} a0  (deep MOND)")
print("   => BOTH are deep-MOND (g < a0), OVERLAPPING. MOND WORKS in galaxies (RAR 0.108dex) but FAILS")
print("   in clusters at the SAME acceleration. So the residual is NOT an acceleration effect =>")
print("   an acceleration-triggered a0-bump would ALSO fire in galaxies and BREAK the RAR. FORBIDDEN.")
print("   => the bump MUST be triggered by a CLUSTER-SPECIFIC quantity: total mass / potential depth /")
print("   pressure of the dark condensate / a length scale -- NOT the local acceleration (I4 tension).")

print("\n=== 3. the decisive constraint: cluster weak-LENSING (Mistele KiDS) ===")
print("   A genuine a0-bump is ONE effective a0 => boosts DYNAMICS and LENSING EQUALLY (eta_lens=eta_dyn).")
print("   But the repo's confrontation: 'Mistele 34x excluded under all K_B candidates'. The cluster")
print("   weak-lensing mass does NOT match the a0-bump that fixes the dynamical residual -- a dynamics-")
print("   vs-lensing MISMATCH at cluster scales, the SAME disease as single-metric MOND (DC-013/017),")
print("   now at cluster scales. A single-a0 bump gives eta_lens=eta_dyn; the DATA appears to want them")
print("   different => a single effective-a0 bump is 34x off. STRONG negative for the simple version.")

print("\n=== 4. what survives / the second-field escape ===")
print("   To have eta_lens != eta_dyn (or to source the bump cluster-specifically), the bump needs a")
print("   SECOND FIELD (the K(Q) dark condensate / pressure field) carrying independent lensing -- which")
print("   EXITS single-metric (as bimetric does). Repo status: c_T=1 EXACT + no-ghost theorem PASS for")
print("   this sector; BBN forces K_B <~ 0.25; but Mistele 34x-excludes the tested K_B couplings. So the")
print("   second field passes the theory-health gates but FAILS the current cluster-lensing data for the")
print("   couplings tried. The 'live' status = untested K_B corners + the pressure-field construction open.")

print("\n=== PRICE SUMMARY ===")
print("The a0-bump cluster route: enhance a0 x3-4 at cluster scales for the ~2x residual. EXITS single-")
print("metric (needs a cluster-specific trigger + a second field for independent lensing). PASSES the")
print("theory-health gates the single-metric DHOST route failed: c_T=1 exact, no-ghost theorem. PRICE:")
print("(i) trigger cannot be acceleration (galaxy-cluster deep-MOND overlap => would break the RAR) --")
print("    must be mass/potential/pressure/scale, cluster-specific; (ii) BBN caps K_B<~0.25; (iii) DECISIVE:")
print("    cluster weak-lensing (Mistele KiDS) 34x-EXCLUDES the tested K_B bump couplings -- a dynamics-vs-")
print("    lensing mismatch (the DC-013/017 disease resurfacing at cluster scales) unless a second field")
print("    carries independent lensing. DECISIVE OPEN CALC: does a pressure/condensate-sourced a0-bump")
print("    (second field, cluster-triggered) fit BOTH the dynamical residual AND the Mistele weak-lensing")
print("    profile, ghost-free, at some allowed K_B<0.25? Leans CONSTRAINED-PESSIMISTIC (34x is a big miss)")
print("    but NOT excluded (untested couplings + the pressure-field construction remain).")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"PRICE-a0bump-cluster","status":"OPEN-PRICED-CONSTRAINED",
 "certificate":("a0-bump cluster route: enhance a0 x3-4 (eta~1.72-2.08 residual, g~sqrt(a0 g_bar) so 2x g "
   "needs 4x a0) at cluster scales. EXITS single-metric: (i) trigger CANNOT be acceleration -- cluster "
   "cores (~0.5 a0) and galaxy outskirts (~0.5 a0) OVERLAP in deep MOND, so an accel-bump breaks the RAR; "
   "must be cluster-specific (mass/potential/pressure/scale); (ii) needs a SECOND FIELD (K(Q) condensate) "
   "for independent lensing. PASSES the gates single-metric DHOST failed: c_T=1 exact + no-ghost theorem. "
   "PRICE: BBN K_B<~0.25; DECISIVE -- cluster weak-lensing (Mistele KiDS) 34x-EXCLUDES the tested K_B "
   "couplings = a dynamics-vs-lensing mismatch (DC-013/017 disease at cluster scales) unless the 2nd field "
   "carries independent lensing. OPEN CALC: pressure/condensate-sourced cluster-triggered a0-bump fitting "
   "BOTH the dynamical residual AND Mistele weak-lensing, ghost-free, at K_B<0.25? Leans constrained-"
   "pessimistic (34x miss) but not excluded (untested couplings + pressure-field construction open)."),
 "numeric_values":{"a0_boost_needed":"x3-4","cluster_g":"~0.5 a0","galaxy_g":"~0.5 a0 (overlap)","Mistele":"34x excluded (tested K_B)","BBN":"K_B<0.25"}}))
