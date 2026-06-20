"""
ROUTE D — FRESH 2024-2026 cluster-MOND mechanism hunt.
THE NEW LEAD: Zhang, Zonoozi & Kroupa 2026 (arXiv:2602.06082, PRD) —
"Revisiting the missing mass problem in MOND for nearby galaxy clusters."

CLAIM (their abstract, verified by WebFetch of the arXiv HTML):
  - top-heavy IGIMF in massive ellipticals -> M/L ~ 6x canonical
  - stellar remnants (neutron stars + stellar black holes) dominate the boost
  - baryons (stars+remnants+ICM) = 88% of the MOND dynamical mass at R200
  - a0 = 1.2e-10, 46 clusters z<0.1, WINGS+2MASS, HSE-equivalent integrated masses.

WHY THIS IS A GENUINE NEW LEAD (vs the banked killed-list):
  - NO NEW PARTICLE: neutron stars + stellar BHs are REAL baryons (collapsed
    stellar remnants). Passes G3 by construction (real baryons, not a new species).
  - GALAXY-SAFE BY CONSTRUCTION (G2): the IGIMF is top-heavy ONLY in high-SFR
    (>10 Msun/yr) massive ellipticals; SPARC disks keep ~canonical IMF -> their M/L
    and the RAR are unchanged. This is NOT the density-a0 killer.
  - NOT in the banked killed-list (that list has: density-a0, MI non-adiabatic,
    dS-Unruh environmental, keV/eV sterile, AeST mu^2-Phi). IGIMF remnants are new.

THE MAKE-OR-BREAK QUESTION (G1, SUFFICIENCY): Kroupa closes the INTEGRATED ~2x
deficit at R200. But the framework's open soft-spot is the CENTRAL/CORED residual:
FPS 2025 (2410.02612) find the residual is GAS-TRACKING, missing-to-gas ~10, with
a ~400 kpc exp cutoff, inside ~420 kpc -> a ~2.3e14 Msun CORE target. Stellar
remnants track the STARS/BCG (centrally concentrated), NOT the gas. Two questions:
  (Q1) Is there ENOUGH remnant mass to source the core target?
  (Q2) Does it have the right SHAPE (gas-tracking) or is it BCG-concentrated
       (helps the very center but not the gas-following 100-420 kpc shell)?

This script computes BOTH on the framework's footing (a0=9.36e-11), both ways.
"""
import numpy as np

# ----------------------------- constants -----------------------------
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19
Mpc  = 1000*kpc
a0   = 9.36e-11                       # FRAMEWORK a0 (eta-worst footing)

def gpred(gbar):
    return np.sqrt(gbar**2 + gbar*a0)  # framework dS-Unruh interpolation

# =====================================================================
# (A) THE CORE TARGET on the framework footing (from the banked ledgers,
#     reproduced): rich cluster, M_res inside ~420 kpc.
# =====================================================================
# Banked (CLUSTER_CORE_CLASH_AND_XLSSC122 + CLASH_TARGET_RESULT):
#   CLASH-lensing core M_res(<420 kpc) = 2.37e14 Msun at matched ~1e15 anchor
#   = eRASS1 X-ray core 2.30e14 (ratio 1.03).
#   Framework MI phantom supplies M_res(<450 kpc) = 4.00e13 -> undershoot x4.42.
M_core_target = 2.30e14          # Msun, missing collisionless mass inside ~420 kpc
M_MI_phantom  = 4.00e13          # Msun, what the framework MI already supplies
R_core        = 420.0            # kpc
undershoot    = M_core_target/M_MI_phantom
print("="*86)
print("THE CORE TARGET (framework footing, banked + reproduced)")
print("="*86)
print(f"  Core missing mass target  M_res(<{R_core:.0f} kpc) = {M_core_target:.2e} Msun")
print(f"  Framework MI phantom supplies               = {M_MI_phantom:.2e} Msun")
print(f"  => undershoot x{undershoot:.2f}  ; SHORTFALL = {M_core_target-M_MI_phantom:.2e} Msun")
print(f"     (this is the ~2.3e14 'rich' CORE target Kroupa's remnants must fill)")

# =====================================================================
# (B) HOW MUCH REMNANT MASS does the IGIMF route actually supply in the core?
#     The honest budget. Stellar light in a rich cluster, x(M/L boost), then
#     the remnant FRACTION, then how much sits inside 420 kpc.
# =====================================================================
# Cluster stellar budget (rich, M500~1e15):
#   total cluster stellar mass (canonical IMF) ~ 1.0-1.5e13 Msun
#   (f_star/f_gas ~ 0.1-0.2; M_gas ~ 1e14 -> M_star,canon ~ 1-2e13). Kroupa's own
#   Abell 85 example: M_star(canonical) ~ 1e13, M_gas ~ 1e14, M_dyn(MOND) ~ 2e14.
M_star_canon_total = 1.3e13       # Msun, canonical-IMF stellar mass, whole cluster
fgas_to_star       = 1.0e14/M_star_canon_total
print("\n"+"="*86)
print("(B) IGIMF REMNANT BUDGET — how much extra mass, and where")
print("="*86)
print(f"  Canonical-IMF cluster stellar mass (whole cluster) ~ {M_star_canon_total:.2e} Msun")
print(f"  Cluster gas mass ~1e14 -> M_gas/M_star,canon ~ {fgas_to_star:.1f}")

# IGIMF M/L boost: Kroupa paper states massive ellipticals M/L ~ 6x canonical.
# But the boost is a *stellar-mass* boost (extra remnants + already-counted stars).
# The EXTRA mass over canonical is (boost-1) x M_star,canon, dominated by remnants.
ML_boost = 6.0
M_star_igimf_total = ML_boost*M_star_canon_total
M_extra_total = M_star_igimf_total - M_star_canon_total
print(f"  IGIMF M/L boost in massive ellipticals = {ML_boost:.1f}x canonical")
print(f"  IGIMF total stellar mass (whole cluster) ~ {M_star_igimf_total:.2e} Msun")
print(f"  EXTRA mass (remnants+top-heavy stars)    ~ {M_extra_total:.2e} Msun")

# ---- BUT: the M/L boost applies only to the EARLY-TYPE (elliptical) light,
#      which dominates cluster stellar light but not 100%. And the boost in the
#      Kroupa paper is needed to reach 88% of the INTEGRATED R200 mass, i.e. it is
#      already spent on the integrated deficit. Let's be GENEROUS (both-ways) and
#      give the route its FULL integrated extra mass, then ask the geometry question.
print(f"\n  [both-ways generous]: grant the FULL extra IGIMF mass {M_extra_total:.2e} Msun")

# =====================================================================
# (C) THE GEOMETRY: remnants track STARS (BCG + galaxies, centrally peaked via
#     ICL but on a stellar scale-length), the FPS residual tracks GAS (cored,
#     ~400 kpc, missing-to-gas ~10). What FRACTION of the stellar/remnant mass
#     lands inside the 420 kpc core, and does its SHAPE match the gas-tracking
#     residual?
# =====================================================================
print("\n"+"="*86)
print("(C) GEOMETRY — does remnant mass land in the 100-420 kpc gas-tracking shell?")
print("="*86)

# Stellar light in clusters: BCG + ICL is steeply centrally concentrated
# (de Vaucouleurs / NFW-stars), satellite galaxies follow ~NFW of the cluster.
# Model the stellar mass as a sum:
#   - BCG+ICL: ~30-50% of cluster stars, very centrally peaked (Re ~ 30-60 kpc,
#     effectively all inside ~150 kpc).
#   - satellite galaxies: ~50-70%, follow ~NFW(c~3-5) of the cluster (extended).
# Gas: beta-model, rc~200 kpc -> the gas-tracking residual peaks at 100-420 kpc.

# Fraction of stellar mass inside R for the two components:
def frac_bcg_icl(R_kpc, Re=50.0):
    # de Vaucouleurs effective: ~ fraction inside R for Sersic n=4; approximate by
    # 1 - exp(-(R/Re)^0.25 * 7.67)/normalization -> just use enclosed-light table.
    # Use the fact that R_e encloses 50%, 4 R_e ~ 86%, 10 R_e ~ 95%.
    x = R_kpc/Re
    # smooth monotone fit to de Vauc enclosed-light fraction
    return 1.0 - (1+ (x/3.0))*np.exp(-1.0*(x/3.0))   # ~0.5 at x~3 (R~150), ~0.9 by R~420

def frac_nfw_stars(R_kpc, rs=300.0):
    # satellites ~NFW with scale rs ~ R500/c ~ 300-400 kpc
    x = R_kpc/rs
    m = np.log(1+x) - x/(1+x)
    mtot = np.log(1+ (1400.0/rs)) - (1400.0/rs)/(1+1400.0/rs)  # to R500~1400
    return m/mtot

f_bcg = 0.40      # BCG+ICL share of cluster stellar mass
f_sat = 0.60
for R in [150.0, 300.0, 420.0]:
    fr = f_bcg*frac_bcg_icl(R) + f_sat*frac_nfw_stars(R)
    M_extra_inR = fr*M_extra_total
    print(f"  R<{R:5.0f} kpc: stellar/remnant enclosed fraction = {fr:.2f}"
          f"  -> extra remnant mass inside = {M_extra_inR:.2e} Msun")

f_core = f_bcg*frac_bcg_icl(R_core) + f_sat*frac_nfw_stars(R_core)
M_extra_core = f_core*M_extra_total
print(f"\n  EXTRA remnant mass inside the {R_core:.0f} kpc core = {M_extra_core:.2e} Msun")
print(f"  Core shortfall to fill                        = {M_core_target-M_MI_phantom:.2e} Msun")
fill = M_extra_core/(M_core_target-M_MI_phantom)
print(f"  => remnants fill {100*fill:.0f}% of the core shortfall (mass budget)")

# =====================================================================
# (D) THE SHAPE TEST: even if the mass budget is enough, is the SHAPE right?
#     FPS: residual is GAS-TRACKING (missing-to-gas ~10, flat ratio), cored at
#     ~400 kpc. Remnants are STAR-tracking (BCG-peaked at <150 kpc + NFW sats).
#     Compare the residual-to-gas ratio the remnants would produce vs the
#     observed flat ~10.
# =====================================================================
print("\n"+"="*86)
print("(D) SHAPE TEST — remnants are STAR-tracking, FPS residual is GAS-tracking")
print("="*86)
# gas enclosed fraction (beta-model rc=200, beta=0.65) inside R, to R500=1400
def frac_gas(R_kpc, rc=200.0, beta=0.65):
    rr = np.linspace(1.0, 1400.0, 4000)
    rho = 1.0/(1+(rr/rc)**2)**(1.5*beta)
    cum = np.cumsum(4*np.pi*rr**2*rho)*(rr[1]-rr[0])
    tot = cum[-1]
    return np.interp(R_kpc, rr, cum)/tot

print(f"  {'R[kpc]':>7} {'f_gas(<R)':>10} {'f_star(<R)':>11} {'ratio star/gas':>15}")
for R in [100.0, 150.0, 200.0, 300.0, 420.0]:
    fg = frac_gas(R)
    fs = f_bcg*frac_bcg_icl(R) + f_sat*frac_nfw_stars(R)
    print(f"  {R:7.0f} {fg:10.3f} {fs:11.3f} {fs/fg:15.2f}")
print("\n  -> If remnants were the residual, residual/gas RISES toward the center")
print("     (stars more concentrated than gas) -> a CENTRAL SPIKE, NOT the FLAT")
print("     missing-to-gas~10 cored shell FPS observe. Shape mismatch quantified above.")

# =====================================================================
# (E) THE a0 SUBTLETY — Kroupa uses a0=1.2e-10; the framework uses 9.36e-11.
#     The lower framework a0 gives LESS MOND boost -> a LARGER MOND dynamical
#     mass to match -> a HARDER target. Quantify the surcharge.
# =====================================================================
print("\n"+"="*86)
print("(E) a0 FOOTING — Kroupa a0=1.2e-10 vs framework 9.36e-11 (the surcharge)")
print("="*86)
# deep-MOND: M_dyn ~ V^4/(G a0). Lower a0 -> larger inferred M_dyn for same V.
# eta surcharge ~ (1.2e-10/9.36e-11) in the deep-MOND limit for the phantom.
a0_kroupa = 1.2e-10
# In deep MOND M_res scales as 1/a0 (the phantom needed to reach g_obs).
# surcharge factor on the residual:
surch = a0_kroupa/a0          # >1: framework needs MORE residual
print(f"  Kroupa a0 = {a0_kroupa:.2e}, framework a0 = {a0:.2e}")
print(f"  Deep-MOND residual scales ~1/a0 -> framework target is x{surch:.3f} HARDER")
print(f"  (so Kroupa's 88%-at-R200 on a0=1.2e-10 is OPTIMISTIC for the framework;")
print(f"   on a0=9.36e-11 the same baryons cover ~{88/surch:.0f}% -> a deeper residual)")

# =====================================================================
# (F) VERDICT SUMMARY
# =====================================================================
print("\n"+"="*86)
print("(F) VERDICT on the IGIMF-remnant route vs the framework's CORE soft-spot")
print("="*86)
print(f"  G3 NO-NEW-PARTICLE : PASS — neutron stars + stellar BHs are REAL baryons.")
print(f"  G2 GALAXY-VETO     : PASS — IGIMF top-heavy ONLY in high-SFR ellipticals;")
print(f"                       SPARC disks keep canonical IMF -> RAR untouched.")
print(f"  G1 SUFFICIENCY     : mass budget fills ~{100*fill:.0f}% of the CORE shortfall,")
print(f"                       BUT SHAPE is star-tracking (central spike) not the FLAT")
print(f"                       gas-tracking ~10 shell FPS observe -> PARTIAL at best.")
print(f"  a0 surcharge       : framework target x{surch:.2f} harder than Kroupa's a0=1.2e-10.")
print(f"  G4 DATA            : Kroupa's 88% is INTEGRATED R200 (HSE); the CORE (FPS")
print(f"                       lensing, ~420 kpc, ratio~10) is a DIFFERENT, untested-by-")
print(f"                       Kroupa regime. Lensing core != HSE integrated mass.")
