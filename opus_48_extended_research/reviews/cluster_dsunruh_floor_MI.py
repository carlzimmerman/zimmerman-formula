#!/usr/bin/env python3
r"""
ROUTE cluster_dsunruh_floor_MI -- the de Sitter (cH)^2 FLOOR in T_eff, the DISTINCTIVE
modified-INERTIA reading, on real eRASS1.  (companion/sharpening of cluster_dsunruh_baryons.py)
=================================================================================================
THE FRAMEWORK'S DISTINCTIVE PHYSICS (not normal MOND):
  Modified INERTIA from the de Sitter-Unruh temperature
        T_eff(a) = (hbar/2pi c kB) sqrt(a^2 + (cH)^2),
  with the inertial response set by Delta T = T(a)-T(0):
        mu_eff(a) = [ sqrt(a^2 + (cH)^2) - cH ] / a,     and the inertia law  mu_eff(a) a = g_bar.
  The (cH) term is the de Sitter FLOOR: the temperature (=> inertia) never drops below the value
  set by the cosmic horizon. In the framework cH = cH_Lambda = Z*a0 = 5.789*a0 (NOT 2 a0).

  This is DISTINCT from the closing-calc algebraic nu (g_obs = nu(y) g_bar, modified GRAVITY).
  Here the relevant acceleration `a` that enters the FLOOR is the particle's TRUE kinematic
  acceleration, and the floor cH sits at 5.8 a0 -- so at R500 where g_obs ~ 0.45 a0 ~ 0.08 cH,
  a particle is DEEP in the floor-dominated regime (a << cH). DERIVE whether the floor changes eta.

WHAT IS PINNED HERE (the brief's angle [desitter_floor_in_clusters]):
  1. Solve the FULL dS-Unruh inertia law mu_eff(a) a = g_bar with the floor at cH=cH_Lambda=Z a0,
     and compare the resulting g_obs to (a) the deep-MOND sqrt(g_bar a0) and (b) the single-scale
     a0=2cH closed form. Show the floor's quantitative effect at the cluster transition regime.
  2. Add the MODIFIED-INERTIA (pressure-supported) virial reading: clusters are sigma-supported,
     and Milgrom proved MI != MG for pressure-supported systems (the virial coefficient). Bracket
     the MI vs MG coefficient and propagate to eta.
  3. Compute eta(R500) on real eRASS1 BOTH WAYS (framework a0=9.36e-11 and regular MOND a0=1.2e-10;
     floor at cH_Lambda=Z a0 vs the naive 2cH single-scale), and compare to the normal-MOND eta~2.15.

HONESTY: a0/Z never asserted derived (quarantine). Grade both ways. Do not manufacture a reduction.
"""
import numpy as np
from astropy.io import fits

# ---------- constants / framework cosmology canon -----------------------------------------------
c, G, Msun, kpc, Mpc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
H0   = 2.184e-18                       # 67.4 km/s/Mpc
Om, OmL = 0.315, 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
RHO_DE0   = OmL*RHO_CRIT0

A0_FRAME = 0.5*c*np.sqrt(G*RHO_DE0)    # framework pure-Lambda a0 = (c/2) sqrt(G rho_DE) = 9.36e-11
A0_MOND  = 1.2e-10                      # regular MOND
Z        = 5.789                        # framework: cH_Lambda = Z a0  (c^2 sqrt(Lambda/3) / a0)

# de Sitter floor acceleration cH_Lambda used in T_eff (framework reading):
cH_FRAME = Z*A0_FRAME                   # = c^2 sqrt(Lambda/3) ~ 5.79 a0_frame
# cross-check: c^2 sqrt(Lambda/3) with Lambda = 3 OmL H0^2/c^2  => c^2 sqrt(OmL) H0 / c = c H0 sqrt(OmL)
cH_check = c*H0*np.sqrt(OmL)
print("="*94)
print("(0) THE TWO SCALES: a0 (the MOND scale) vs cH_Lambda (the dS FLOOR in T_eff)")
print("="*94)
print(f"  a0_FRAME          = {A0_FRAME:.4e} m/s^2     [(c/2) sqrt(G rho_DE), canon 9.36e-11]")
print(f"  cH_Lambda (Z a0)  = {cH_FRAME:.4e} m/s^2     = {cH_FRAME/A0_FRAME:.3f} a0   [the FLOOR]")
print(f"  cH_Lambda direct  = {cH_check:.4e} m/s^2     (= c H0 sqrt(OmL), {cH_check/A0_FRAME:.3f} a0)  <- consistency")
print(f"  naive single-scale 2cH would imply a0 = 2cH; here a0 != 2 cH_Lambda (two-scale framework).")
print(f"  Z = cH_Lambda/a0 = {cH_FRAME/A0_FRAME:.3f}  (asserted, NOT derived -- quarantine).")

# =================================================================================================
# (1) THE dS-Unruh MODIFIED-INERTIA LAW WITH THE FLOOR  -- closed form & the floor's effect
# =================================================================================================
# Inertia law: mu_eff(a) a = g_bar,  mu_eff(a)=[sqrt(a^2+cH^2)-cH]/a
#   => sqrt(a^2+cH^2) - cH = g_bar  => a = sqrt(g_bar^2 + 2 g_bar cH)   (EXACT closed form)
# The OBSERVED gravity g_obs (what a dynamical-mass analysis infers as G M_dyn / r^2) is the
# acceleration `a` the particle actually undergoes, i.e. g_obs = a = sqrt(g_bar^2 + 2 g_bar cH).
def g_obs_floor(g_bar, cH):
    return np.sqrt(g_bar**2 + 2.0*g_bar*cH)
def g_obs_deepMOND(g_bar, a0):
    return np.sqrt(g_bar*a0)                 # deep-MOND, the "what MOND really predicts" limit
def g_obs_simple_nu(g_bar, a0):
    # the closing-calc / framework "simple" algebraic relation g_obs=sqrt(gb^2+gb a0) (a0, not 2cH)
    return np.sqrt(g_bar**2 + g_bar*a0)

print()
print("="*94)
print("(1) THE FLOOR vs DEEP-MOND: g_obs/g_bar at the cluster transition regime (g_bar/a0 ~ 0.06)")
print("="*94)
print("  dS-Unruh inertia law with FLOOR cH:  g_obs = sqrt(g_bar^2 + 2 g_bar cH)")
print("  In the floor-dominated regime g_bar << cH:  g_obs -> sqrt(2 cH g_bar) = sqrt((2cH) g_bar)")
print("  => the EFFECTIVE deep-MOND a0 of the floor reading is a0_eff = 2 cH = 2 Z a0 = 11.6 a0 !!")
print()
print(f"  {'g_bar/a0':>9}{'g_obs/g_bar FLOOR(cH=Za0)':>26}{'FLOOR(2cH naive=2a0)':>22}{'simple nu(a0)':>15}{'deepMOND sqrt':>15}")
for y in (0.03, 0.06, 0.1, 0.3, 1.0, 3.0):
    gb = y*A0_FRAME
    bF  = g_obs_floor(gb, cH_FRAME)/gb              # framework floor cH=Z a0
    bN  = g_obs_floor(gb, A0_FRAME)/gb              # naive single-scale 2cH with cH=a0 (i.e. a0_eff=2a0)
    bS  = g_obs_simple_nu(gb, A0_FRAME)/gb          # simple nu at a0
    bD  = g_obs_deepMOND(gb, A0_FRAME)/gb           # deep-MOND sqrt at a0
    print(f"  {y:>9.3f}{bF:>26.3f}{bN:>22.3f}{bS:>15.3f}{bD:>15.3f}")
print("""
  READING: the dS-Unruh floor at cH=Z a0 = 5.8 a0 makes the deep limit a0_eff = 2cH = 11.6 a0.
  At the cluster regime (g_bar/a0 ~ 0.06) the floor reading gives a MUCH STRONGER boost than the
  simple-nu(a0) form -- because the floor sits ~12x higher than a0. THIS is the distinctive effect:
  the de Sitter floor, taken literally in T_eff with cH=cH_Lambda, raises the effective MOND scale
  by 2Z ~ 11.6, which (deep-MOND eta ~ 1/sqrt(a0_eff)) would shrink the deficit by sqrt(11.6/1)~3.4x.
  *** This is the both-ways crux: is cH in T_eff really Z a0 (=> a0_eff=2Z a0), or is the framework's
      a0=9.36e-11 ALREADY the 2cH of a consistent single-scale reading (=> floor adds nothing new)? ***""")

# =================================================================================================
# (2) ETA(R500) ON REAL eRASS1  -- the four readings, both a0 values
# =================================================================================================
FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"
d = fits.open(FITS)[1].data
def col(name):
    return np.array([float(v) if str(v).strip() not in ("","--") else np.nan for v in d[name]], float)
z, M500, Mgas, fgas, R500 = col("BEST_Z"), col("M500"), col("MGAS500"), col("FGAS500"), col("R500")
fstar = 0.20
ok = (z>0)&(z<1)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>0.01)&(fgas<0.30)
M500_kg = M500[ok]*1e13*Msun
Mbar_kg = (1+fstar)*Mgas[ok]*1e11*Msun
R_m = R500[ok]*kpc
gobs = G*M500_kg/R_m**2                 # the "needed" gravity = G M_dyn / R500^2
gbar = G*Mbar_kg/R_m**2
N = int(ok.sum())

print()
print("="*94)
print("(2) ETA = M_dyn/M_pred ON REAL eRASS1  (median [IQR]) -- residual missing-mass factor at R500")
print("="*94)
print(f"  N = {N} clean eRASS1 clusters; z_med={np.median(z[ok]):.3f}")
print(f"  g_bar/a0_FRAME median = {np.median(gbar)/A0_FRAME:.3f}  (DEEP MOND at R500; g_bar/cH_Lambda = {np.median(gbar)/cH_FRAME:.3f})")
print(f"  g_obs/a0_FRAME median = {np.median(gobs)/A0_FRAME:.3f}  (so g_obs ~ {np.median(gobs)/cH_FRAME:.3f} cH_Lambda -- deep in the floor)\n")

def eta_pred(gpred):  # eta = g_obs(needed) / g_pred(model)
    return gobs/gpred
readings = [
    ("dS-Unruh FLOOR  cH=Z a0 (a0_eff=2Z a0=11.6a0)", lambda a0: g_obs_floor(gbar, Z*a0),   ),
    ("dS-Unruh FLOOR  naive 2cH (cH=a0, a0_eff=2a0)", lambda a0: g_obs_floor(gbar, a0),      ),
    ("simple nu   g_obs=sqrt(gb^2+gb a0)",            lambda a0: g_obs_simple_nu(gbar, a0),  ),
    ("deep-MOND   g_obs=sqrt(gb a0)",                 lambda a0: g_obs_deepMOND(gbar, a0),   ),
]
print(f"  {'reading':>48}{'eta(a0=9.36e-11)':>20}{'eta(a0=1.2e-10)':>18}")
results = {}
for name, gp in readings:
    eF = eta_pred(gp(A0_FRAME)); eM = eta_pred(gp(A0_MOND))
    results[name] = (np.median(eF), np.percentile(eF,[25,75]), np.median(eM))
    print(f"  {name:>48}{np.median(eF):>11.3f} {str(np.percentile(eF,[25,75]).round(2)):>8}"
          f"{np.median(eM):>11.3f}")
print(f"""
  NORMAL-MOND BASELINE for comparison: the AeST/standard-nu closing calcs give eta(R500) ~ 2.15.
  The deep-MOND row (a0=9.36e-11) reproduces eta ~ {results['deep-MOND   g_obs=sqrt(gb a0)'][0]:.2f}: that IS the normal-MOND number
  (interpolation-independent at R500, since g_bar/a0~0.06 is deep). The simple-nu row matches it.""")

# =================================================================================================
# (3) MODIFIED-INERTIA vs MODIFIED-GRAVITY for PRESSURE-SUPPORTED systems: the virial coefficient
# =================================================================================================
print()
print("="*94)
print("(3) MODIFIED INERTIA != MODIFIED GRAVITY for pressure-supported clusters (the virial test)")
print("="*94)
print("""  Milgrom (1994 Ann.Phys.229,384; 2012 PhRvL): for a PRESSURE-supported system in deep MOND,
  ALL modified-INERTIA formulations predict the virial relation
        (sigma^2)^2  ==  <v^2>^2  =  (4/9) G M a0            [MI deep-MOND virial, universal]
  Modified GRAVITY (AQUAL) gives the SAME 4/9 leading coefficient for the GLOBAL virial of a
  deep-MOND isothermal sphere (Milgrom 1984; the global virial coincides). The MI/MG DIVERGENCE
  for pressure systems is NOT in the global mass-sigma coefficient -- it is in the LOCAL dynamics
  (no acceleration field in MI; orbit-dependence). For the integrated M(<R500)-from-g_obs(R500)
  deficit eta that eRASS1 measures, the relevant object is the LOCAL g_obs(R500), governed by the
  interpolation/floor of Part 1-2, NOT a distinct virial coefficient.""")
# Quantify: deep-MOND mass-sigma, MI coefficient 4/9, the implied dynamical mass vs the integrated one.
# eRASS1 gives M500 (lensing+X-ray), not sigma. So the virial coefficient does NOT enter eta(R500)
# directly. The honest statement: the MI/MG difference for pressure systems is a LOCAL-dynamics /
# orbit-shape effect, O(1) and profile-dependent, NOT a clean multiplicative rescue of eta.
sigma_kms = 1000.0
M_from_sigma_MI = (sigma_kms*1e3)**4 / ((4.0/9.0)*G*A0_FRAME)   # MI: M = sigma^4 / ((4/9) G a0)
print(f"\n  Worked number: a sigma=1000 km/s cluster, MI virial M = sigma^4/((4/9) G a0_FRAME)")
print(f"     => M_dyn(MI) = {M_from_sigma_MI/Msun:.3e} Msun  (the MI mass-sigma prediction).")
print(f"  The MG isothermal-sphere virial gives the SAME 4/9 to leading order => no clean eta rescue")
print(f"  from the coefficient. The genuine MI!=MG effect is local/orbit-shape (O(1), profile-set).")

# =================================================================================================
# (4) BOTH WAYS: is the FLOOR rescue real, or an artifact of the cH=Z a0 double-count?
# =================================================================================================
print()
print("="*94)
print("(4) BOTH WAYS -- is the floor's eta-reduction REAL, or a scale double-count?")
print("="*94)
e_floorZ  = results['dS-Unruh FLOOR  cH=Z a0 (a0_eff=2Z a0=11.6a0)'][0]
e_deep    = results['deep-MOND   g_obs=sqrt(gb a0)'][0]
print(f"""  WAY 1 (floor is physical & cH=cH_Lambda=Z a0): a0_eff=2cH=2Z a0=11.6 a0. The deep-MOND eta
        scales as 1/sqrt(a0_eff), so eta -> {e_deep:.2f}/sqrt(2Z) = {e_deep/np.sqrt(2*Z):.2f}, i.e. eRASS1 eta(floor)={e_floorZ:.2f}.
        *** If literally true, the dS FLOOR REDUCES the cluster deficit from ~2.1 to ~{e_floorZ:.2f}. ***

  WAY 2 (the floor scale IS already a0 -- no new scale): the framework FITS galaxies (SPARC, 0.105
        dex) with a0=9.36e-11 used as the MOND scale in g_obs=sqrt(gb^2+gb a0). In that fit the deep
        limit is sqrt(gb a0) with a0=9.36e-11 -- i.e. galaxies ALREADY pin the effective 2cH = a0.
        If you ALSO put cH=Z a0 into the SAME law you DOUBLE-COUNT: the galaxy RAR would then predict
        a0_eff = 2 Z a0 = 11.6 a0 = 1.08e-9, which OVER-predicts galaxy rotation by sqrt(11.6)=3.4x --
        GROSSLY falsified by SPARC. So WAY 1's floor-rescue, applied consistently, BREAKS GALAXIES.""")
# Make the galaxy-consistency check explicit: deep-MOND BTFR normalization.
v_btfr_a0   = (G*1e11*Msun*A0_FRAME)**0.25
v_btfr_2cH  = (G*1e11*Msun*2*cH_FRAME)**0.25
print(f"\n  GALAXY CONSISTENCY (BTFR v_flat=(G M a0_eff)^1/4 for M=1e11 Msun):")
print(f"     a0_eff=a0=9.36e-11 :  v_flat = {v_btfr_a0/1e3:.0f} km/s   (the SPARC-fit value)")
print(f"     a0_eff=2cH=11.6 a0 :  v_flat = {v_btfr_2cH/1e3:.0f} km/s   ({v_btfr_2cH/v_btfr_a0:.2f}x too high -- SPARC-EXCLUDED)")
print(f"  => the floor-as-extra-scale (cH=Z a0 on TOP of a0) is falsified by galaxies. The dS-Unruh law")
print(f"     is SELF-CONSISTENT ONLY as a SINGLE scale, where 2cH IS the fitted a0 -- and then the floor")
print(f"     adds NOTHING new at clusters beyond the standard simple-nu, giving eta = {results['simple nu   g_obs=sqrt(gb^2+gb a0)'][0]:.2f} ~ normal MOND.")
# THE SELF-CONSISTENT NUMBER (companion sparc_floor_check.py): fitting the FLOOR law itself to the
# 175 SPARC curves picks cH_best = 8.9e-11 (scatter 0.105 dex), i.e. a0_eff=2cH=1.78e-10=1.90 a0_FRAME;
# forcing cH=Z a0 costs +0.242 dex (0.105 -> 0.347, 3.3x worse) -- the floor-rescue is SPARC-EXCLUDED
# not by a convention choice but by the real data. Using that galaxy-pinned cH=8.9e-11 in the SAME law
# at eRASS1 clusters gives eta(R500) = 1.71 [IQR 1.58-2.00]:
cH_sparc = 8.905e-11
eta_selfcons = np.median(gobs/g_obs_floor(gbar, cH_sparc))
print(f"\n  SELF-CONSISTENT (galaxy-pinned) dS-Unruh FLOOR law, cH=8.9e-11 from SPARC, at eRASS1:")
print(f"     eta(R500) = {eta_selfcons:.2f} [IQR {np.percentile(gobs/g_obs_floor(gbar,cH_sparc),25):.2f}-{np.percentile(gobs/g_obs_floor(gbar,cH_sparc),75):.2f}]"
      f"  -- MODESTLY below normal-MOND 2.15, because SPARC prefers a0_eff~1.9 a0; still 71% excess, NO closure.")
print(f"     (the floor's transition shape pulls a0_eff slightly above a0=9.36e-11 -- a real, mild,")
print(f"      galaxy-pinned distinctive effect: eta 2.15 -> ~1.7, NOT 2.15 -> 0.7 and NOT 2.15 -> parity.)")

# =================================================================================================
# (5) SYNTHESIS
# =================================================================================================
print()
print("="*94)
print("(5) SYNTHESIS -- does the framework's OWN dS-Unruh / modified-inertia physics change clusters?")
print("="*94)
eta_consistent = results['simple nu   g_obs=sqrt(gb^2+gb a0)'][0]
eta_floor_naive = results['dS-Unruh FLOOR  cH=Z a0 (a0_eff=2Z a0=11.6a0)'][0]
print(f"""  (a) THE FLOOR, taken literally with cH=cH_Lambda=Z a0, WOULD reduce eRASS1 eta from ~2.1 to
      ~{eta_floor_naive:.2f} (a0_eff=2cH=11.6 a0). That is the *naive* distinctive prediction -- and it is WRONG:
      applied consistently it over-predicts galaxy rotation by 3.4x (SPARC-falsified, Part 4).
  (b) SELF-CONSISTENTLY, the dS-Unruh inertia law is a SINGLE-scale law whose floor scale is fixed by
      galaxies: fitting the FLOOR law to 175 SPARC picks cH=8.9e-11 (0.105 dex; cH=Z a0 costs +0.242 dex
      = 3.3x worse, EXCLUDED). Using that galaxy-pinned cH at eRASS1 gives eta(R500) = {eta_selfcons:.2f} [IQR 1.58-2.00]
      -- MODESTLY below normal-MOND's 2.15 (the floor's shape prefers a0_eff~1.9 a0), but still a 71%
      excess: NO closure, ~same order as the shared MOND ~2x. (the algebraic simple-nu at the canonical
      a0=9.36e-11 gives {eta_consistent:.2f}; the galaxy-pinned floor law gives {eta_selfcons:.2f} -- both ~2x, neither closes.)
  (c) MODIFIED INERTIA != MODIFIED GRAVITY for pressure systems is REAL (no acceleration field, orbit
      dependence) but it is a LOCAL/orbit-shape O(1) effect; the eRASS1 eta(R500) is governed by the
      LOCAL interpolation at g_bar/a0~0.06 (deep MOND), where MI and MG converge -- so it does NOT
      supply a clean multiplicative rescue of the integrated deficit.
  VERDICT: the framework's distinctive dS-Unruh/modified-inertia physics does NOT reduce the cluster
  deficit. The floor that *could* help is the same scale that fits galaxies, so using it twice breaks
  galaxies; used once it gives normal-MOND eta ~ 2.0-2.1. Clusters remain the shared ~2x MOND liability.
  GATING: even the (refuted) floor-rescue would be UNGATED -- modified inertia has NO covariant
  completion (the trilemma/X2: 'no covariant completion exists'), so any MI cluster claim is not
  covariantly realized. The honest result here is a clean NEGATIVE that needs no gating caveat.""")
print("="*94)
