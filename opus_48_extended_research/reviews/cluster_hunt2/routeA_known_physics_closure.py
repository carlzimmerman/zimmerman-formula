"""
routeA_known_physics_closure.py  (ROUTE A -- the no-new-physics cluster-core closure)

QUESTION (both ways): with the framework's MODIFIED-INERTIA MOND phantom in the cluster
CORE undershooting the lensing+X-ray residual, does ALREADY-KNOWN physics -- WITHOUT a new
particle -- close the gap? Three known pieces, added in the core (<~420 kpc):
  (i)  the MINIMUM neutrino mass that MUST exist (normal-ordering floor Sum m_nu ~0.058-0.06 eV):
       how much of it clusters in the cluster core?  (hot, weakly-clustering -- quantify)
  (ii) missing warm-hot baryons (the cluster baryon-budget gap): how much can sit INSIDE the core?
  (iii) a heavier BCG stellar mass from an IGIMF / bottom-heavy IMF (factor ~1.5-2 on BCG M*).

GATES a valid closure must pass:
  G1 SUFFICIENCY -- closes the core undershoot / ~2.3e14 Msun core target at a0=9.36e-11.
  G2 GALAXY-VETO -- does NOT break SPARC RAR/BTFR (<~0.13 dex).
  G3 NO-NEW-PARTICLE -- uses min-nu that MUST exist + real baryons + real stars, NOT a new species.
  G4 DATA -- survives eRASS1/CLASH/XRISM/Lyman-alpha/X-ray.

BOTH WAYS: hunt as hard for a real closure as to confirm the null; credit a genuine closure
at full weight, concede insufficiency at full weight. Quarantine: a0/Z/kappa never derived.

Framework footing sealed: a0 = 9.36e-11 m/s^2, dS-Unruh nu g_obs = sqrt(gbar^2 + gbar*a0).
"""
import numpy as np
from astropy.io import fits

# ----------------------------- constants (SI) -----------------------------
G    = 6.674e-11
c    = 2.998e8
kB   = 1.381e-23
hbar = 1.055e-34
hP   = 6.626e-34
eV   = 1.602e-19
Msun = 1.989e30
kpc  = 3.086e19
Mpc  = 1000.0*kpc
a0   = 9.36e-11            # framework a0 (eta-worst footing; QUARANTINE not derived)

def g_pred(gbar, a0=a0):
    return np.sqrt(gbar**2 + gbar*a0)
def gN_from_gobs(gobs, a0=a0):
    return (-a0 + np.sqrt(a0**2 + 4.0*gobs**2))/2.0

print("="*96)
print(" ROUTE A -- KNOWN-PHYSICS cluster-core closure (min-nu + missing baryons + IGIMF BCG)")
print(" framework a0 = %.3e m/s^2 (QUARANTINE not derived); dS-Unruh nu" % a0)
print("="*96)

# =========================================================================
# 0. ANCHOR THE CORE TARGET to real eRASS1 (the rich bin) + CLASH cross-check
# =========================================================================
hd = fits.open('real_research/data/erass1cl_primary_v3.2.fits')[1].data
z   = hd['BEST_Z']; M500 = hd['M500']; Mgas = hd['MGAS500']
fg  = hd['FGAS500']; R500 = hd['R500']; kT = hd['KT']
ok  = np.isfinite(M500)&np.isfinite(Mgas)&np.isfinite(z)&(z>0)&(z<1)&(M500>0)&(Mgas>0)&(fg>0.01)&(fg<0.30)
M500=M500[ok]; Mgas=Mgas[ok]; fg=fg[ok]; z=z[ok]; R500=R500[ok]; kT=kT[ok]
# units: catalog M500/Mgas in 1e14 Msun? check magnitude
print("\n[eRASS1] N=%d  median M500=%.3g  median Mgas=%.3g  median fgas=%.3f  median R500=%.3g  median kT=%.2f"
      % (ok.sum(), np.median(M500), np.median(Mgas), np.median(fg), np.median(R500), np.median(kT)))
# rich bin
rich = M500 >= np.percentile(M500, 90)
print("[eRASS1 rich >=90pct] N=%d  median M500=%.3g  median R500=%.3g Mpc(?)  median kT=%.2f keV"
      % (rich.sum(), np.median(M500[rich]), np.median(R500[rich]), np.median(kT[rich])))

# =========================================================================
# 1. THE CORE TARGET -- build the rich CLASH-like cluster (matches banked framework_mi_residual.py)
# =========================================================================
# These match the banked clash_cluster/framework_mi_residual.py rich cluster.
M500_c   = 1.0e15*Msun
R500_c   = 1400.0*kpc
fgas500  = 0.13
beta     = 0.70
rc       = 200.0*kpc
M_BCG0   = 1.0e12*Msun     # fiducial BCG stellar mass (Chabrier/Kroupa IMF)
a_BCG    = 25.0*kpc

def Mgas_enc(r, rho0):
    rr = np.linspace(1e-4*rc, r, 8000)
    rho = rho0/(1.0+(rr/rc)**2)**(1.5*beta)
    return np.trapz(4.0*np.pi*rr**2*rho, rr)
unit = Mgas_enc(R500_c, 1.0)
rho0_gas = fgas500*M500_c/unit
def rho_gas(r):  return rho0_gas/(1.0+(r/rc)**2)**(1.5*beta)
def M_gas(r):    return Mgas_enc(r, rho0_gas)
def M_stars(r, M_BCG=M_BCG0): return M_BCG*r**2/(r+a_BCG)**2
def M_bar(r, M_BCG=M_BCG0):   return M_gas(r) + M_stars(r, M_BCG)

# framework MI phantom (mean = quasi-static MOND, scale-inv pinned, banked)
def M_phantom_MI(r, M_BCG=M_BCG0):
    gb = G*M_bar(r, M_BCG)/r**2
    return g_pred(gb)*r**2/G - M_bar(r, M_BCG)

# THE CORE TARGET: CLASH-lensing residual (FPS), 10x-gas, 450 kpc cutoff
eta_dg, r0_cut = 10.0, 450.0*kpc
def M_res_clash(r):
    rr = np.linspace(1e-4*rc, r, 8000)
    return np.trapz(4.0*np.pi*rr**2*(eta_dg*rho_gas(rr)*np.exp(-rr/r0_cut)), rr)

R_core = 420.0*kpc
print("\n" + "-"*96)
print(" THE CORE TARGET (r < 420 kpc), rich cluster M500=1e15:")
print("-"*96)
Mph   = M_phantom_MI(R_core)/Msun
Mcl   = M_res_clash(R_core)/Msun
Mbar  = M_bar(R_core)/Msun
Mgas_core = M_gas(R_core)/Msun
print("  M_bar(<420 kpc)        = %.3e Msun  (gas %.3e + BCG %.3e)" % (Mbar, Mgas_core, M_stars(R_core)/Msun))
print("  M_phantom_MI(<420 kpc) = %.3e Msun  (the framework supplies this)" % Mph)
print("  M_res_CLASH(<420 kpc)  = %.3e Msun  (the lensing+Xray target, ratio 1.03 agree)" % Mcl)
GAP = Mcl - Mph
print("  ==> CORE GAP to fill    = %.3e Msun   (undershoot x%.2f)" % (GAP, Mcl/Mph))

# =========================================================================
# 2. POST-XRISM EQUILIBRIUM: is the CORE target itself inflated? (both ways)
# =========================================================================
# The banked eta(R500) bracket [~1.0 HSE, ~2.33 WL] is an R500-integrated statement: the
# WL-vs-HSE gap is ~1.6x and lives at R500 (the outskirts). In the CORE the two probes AGREE
# (CLASH lensing 2.37e14 = eRASS1 Xray 2.30e14, ratio 1.03) -- the core is RELAXED, lensing is
# NOT disequilibrium-sensitive there, and HSE is reliable in a relaxed core. So the CORE target
# is NOT WL-inflated; it is the robust ~2.3e14. Quantify how much the post-XRISM relaxation
# could deflate the CORE specifically.
print("\n" + "-"*96)
print(" POST-XRISM equilibrium check -- is the CORE target itself deflatable? (both ways)")
print("-"*96)
print("  Two-probe core agreement: CLASH-lensing 2.37e14 vs eRASS1-Xray 2.30e14 (ratio 1.03).")
print("  Lensing is NOT HSE-dependent; the WL-vs-HSE 1.6x gap lives at R500 (outskirts), not core.")
print("  XRISM A2029: nonthermal P<=2%, HSE bias ~2% -> a CORE deflation of at most ~2-5%, NOT 1.6x.")
# best-case core deflation: take the XRISM ~2% nonthermal + a generous 10% relaxed-core correction
core_deflate = 0.90   # generous: shave 10% off the core target for residual disequilibrium
Mcl_eq = Mcl*core_deflate
GAP_eq = Mcl_eq - Mph
print("  Even a GENEROUS 10%% core deflation -> target %.3e, GAP %.3e (still x%.2f undershoot)."
      % (Mcl_eq, GAP_eq, Mcl_eq/Mph))
print("  ==> The CORE residual is robust; the [1.0,2.33] bracket is an R500 statement, NOT a core escape.")

# =========================================================================
# 3. KNOWN-PHYSICS PIECE (i): MINIMUM neutrino mass clustering in the core
# =========================================================================
# Normal-ordering floor: Sum m_nu ~ 0.058-0.06 eV (one ~0.05 eV + one ~0.0087 eV + ~0 eV).
# The cosmic neutrino background number density n_nu = 336 /cm^3 (3 flavors, 112/cm^3 each).
# Neutrinos cluster gravitationally but are HOT: free-streaming sets a maximum overdensity.
# The linear-response clustering of relic nu in a cluster potential (Ringwald-Wong 2004,
# astro-ph/0408192; Villaescusa-Navarro+2011): for m_nu ~ 0.05 eV the OVERDENSITY in a rich
# cluster is delta_nu ~ a few (NOT thousands) -- the nu cannot pack into the core.
print("\n" + "="*96)
print(" PIECE (i): MINIMUM neutrino mass clustering in the core (Sum m_nu = 0.058 eV floor)")
print("="*96)
Sum_mnu = 0.058           # eV, normal-ordering floor (MUST exist)
# heaviest eigenstate ~ sqrt(dm31^2) ~ 0.05 eV does the clustering
m_heavy = 0.0497          # eV
n_cnb = 336e6             # /m^3 total (all flavors), mean cosmic
# but only the species with mass ~m_heavy clusters; ~1 species worth ~112/cm^3
n_one = 112e6            # /m^3 for one species
rho_nu_mean = (n_one * m_heavy*eV/c**2)   # kg/m^3, mean density of the clustering eigenstate
Omega_m_rho_c = 9.47e-27  # kg/m^3 (critical density ~ rho_c) * for scale
print("  Sum m_nu (NO floor) = %.3f eV; clustering eigenstate m ~ %.4f eV." % (Sum_mnu, m_heavy))
print("  mean CNB density (one species) rho_nu_mean = %.3e kg/m^3" % rho_nu_mean)

# Maximum nu phase-space packing (Tremaine-Gunn) in a cluster with sigma ~ 1000 km/s.
# The max nu mass density allowed by phase space: rho_max = (4 pi/3)*... but the relevant
# bound for the ACHIEVED overdensity is the linear-theory clustering factor.
# Ringwald-Wong 2004: for a 1e15 Msun cluster and m_nu=0.05 eV the nu overdensity at the
# center is delta_nu = rho_nu/rho_nu_mean ~ O(1-10). Take the OPTIMISTIC end delta_nu ~ 10.
# (For m_nu=0.6 eV they get ~100-1000; for 0.05 eV it is ~1-10, free-streaming-limited.)
for delta_nu, label in [(1.0,"no clustering"), (10.0,"optimistic delta_nu=10 (RW04 m=0.05eV)"),
                         (50.0,"very optimistic delta_nu=50")]:
    rho_nu_core = delta_nu*rho_nu_mean
    Vcore = (4.0/3.0)*np.pi*R_core**3
    M_nu_core = rho_nu_core*Vcore/Msun
    print("    delta_nu=%5.1f (%s):  M_nu(<420 kpc) = %.3e Msun  (%.4f%% of gap)"
          % (delta_nu, label, M_nu_core, 100*M_nu_core/GAP))

# =========================================================================
# 4. KNOWN-PHYSICS PIECE (ii): missing warm-hot baryons INSIDE the core
# =========================================================================
print("\n" + "="*96)
print(" PIECE (ii): missing warm-hot baryons that can sit INSIDE the core (<420 kpc)")
print("="*96)
# Baryon forensic (banked): the missing baryons are EXPELLED to >R500 by AGN feedback
# (Siegel+2025, Popesso+2024). In the CORE (<420 kpc) the gas is the densest, hottest, most
# X-ray-complete part of the cluster -- there is NO undetected reservoir there. The cosmic
# ceiling: cram ALL cosmic baryons that "belong" to the core mass inside the core.
fb_cosmic = 0.157
# total mass enclosed in core if MOND/CLASH were right (baryons + residual):
M_tot_core_target = (Mbar + Mcl)*Msun   # what the lensing implies is enclosed
# but baryons cannot exceed fb_cosmic of the TRUE enclosed mass. In MOND there's no DM, so the
# "true" enclosed Newtonian-equivalent mass is M_bar + M_phantom. The missing-baryon ceiling:
# the maximum extra baryons = fb_cosmic*M_dyn - M_bar_observed, but only if they're INSIDE core.
# Most generous: gas could be ~15% denser than measured (eRASS1 ~2x low vs sims at GROUP scale,
# but rich-cluster cores are X-ray-bright and complete). Take a generous +30% core gas.
for gas_boost, label in [(1.15,"+15% undetected core gas"), (1.30,"+30% (very generous)"),
                          (2.00,"+100% (eRASS1-vs-FLAMINGO max, NOT in rich cores)")]:
    extra_gas = (gas_boost-1.0)*Mgas_core
    print("    %s: extra baryons in core = %.3e Msun  (%.4f%% of gap)"
          % (label, extra_gas, 100*extra_gas/GAP))
print("  NOTE (banked baryon forensic): the missing baryons are MEASURED at >R500 (AGN-expelled),")
print("  not in the core; rich-cluster cores are X-ray-complete (X-COP even gas-RICH). So the")
print("  realistic core extra is ~0-15%, the +100% is a non-core group-scale number shown for ceiling.")

# =========================================================================
# 5. KNOWN-PHYSICS PIECE (iii): heavier BCG from IGIMF / bottom-heavy IMF
# =========================================================================
print("\n" + "="*96)
print(" PIECE (iii): heavier BCG stellar mass from IGIMF / bottom-heavy IMF (factor 1.5-2)")
print("="*96)
# A bottom-heavy IMF in BCGs (van Dokkum-Conroy 2010; ETG cores) gives M*/L up to ~2x Salpeter.
# Boost the BCG from 1e12 to up to 2e12 Msun. But note: this CHANGES the baryon distribution,
# which RAISES g_bar in the core, which CHANGES the MI phantom. Recompute self-consistently.
for M_BCG, label in [(1.0e12*Msun,"fiducial 1e12"), (1.5e12*Msun,"IGIMF x1.5"), (2.0e12*Msun,"bottom-heavy x2")]:
    extra_star = (M_BCG - M_BCG0)/Msun * (R_core**2/(R_core+a_BCG)**2)  # enclosed extra in core
    # self-consistent: heavier BCG -> higher g_bar -> higher MI phantom too
    Mph_new = M_phantom_MI(R_core, M_BCG)/Msun
    Mbar_new = M_bar(R_core, M_BCG)/Msun
    total_supplied = Mph_new + Mbar_new
    print("    BCG=%s (%s): extra M* in core=%.3e, new MI phantom=%.3e (was %.3e)"
          % (("%.1e"%(M_BCG/Msun)), label, extra_star, Mph_new, Mph))

# =========================================================================
# 6. STACK ALL THREE -- best-case known-physics sum vs the core gap
# =========================================================================
print("\n" + "="*96)
print(" STACK: best-case (optimistic) known-physics sum vs the CORE gap")
print("="*96)
# optimistic best-case:
M_nu_best   = 10.0*rho_nu_mean*((4.0/3.0)*np.pi*R_core**3)/Msun       # delta_nu=10
extra_gas_best = 0.30*Mgas_core                                       # +30% core gas (generous)
# IGIMF BCG x2 -> extra stars in core, PLUS its self-consistent MI boost
M_BCG2 = 2.0e12*Msun
extra_star_best = (M_BCG2 - M_BCG0)/Msun * (R_core**2/(R_core+a_BCG)**2)
Mph_bcg2 = M_phantom_MI(R_core, M_BCG2)/Msun
mi_boost_from_bcg = Mph_bcg2 - Mph
print("  (i)   min-nu (delta_nu=10):           %.3e Msun" % M_nu_best)
print("  (ii)  missing baryons (+30%% gas):     %.3e Msun" % extra_gas_best)
print("  (iii) IGIMF BCG x2 extra stars:        %.3e Msun" % extra_star_best)
print("  (iii') + its self-consistent MI boost: %.3e Msun" % mi_boost_from_bcg)
total_known = M_nu_best + extra_gas_best + extra_star_best + mi_boost_from_bcg
print("  ---------------------------------------------------------")
print("  TOTAL known-physics (optimistic):      %.3e Msun" % total_known)
print("  CORE GAP to fill:                      %.3e Msun" % GAP)
print("  ==> known physics closes %.1f%% of the core gap (optimistic best-case)" % (100*total_known/GAP))
frac = total_known/GAP
print()
if frac >= 1.0:
    print("  G1 SUFFICIENCY: *** CLOSES *** (optimistic best-case reaches the core target)")
elif frac >= 0.5:
    print("  G1 SUFFICIENCY: PARTIAL (closes ~half; remainder needs the field or a particle)")
else:
    print("  G1 SUFFICIENCY: INSUFFICIENT (known physics closes <%.0f%% of the core gap)" % (100*frac))

# what residual gap remains, and what a0 / extra mass it would need
print("\n  Residual core gap after known physics: %.3e Msun" % (GAP - total_known))
# how much would a0 have to rise to supply this? deep-MOND M_ph ~ sqrt(gbar*a0)*r^2/G ~ sqrt(a0)
# so to multiply the phantom by (Mcl/(Mph+...)) needs a0 -> a0*(factor)^2
needed_factor = (Mcl)/(Mph + total_known)
print("  To close the rest via the framework's own MOND would need a0 x%.2f = %.2e (deep-MOND ~a0^0.5 scaling: ~%.1fx in a0)"
      % (needed_factor, needed_factor*a0, needed_factor**2))
