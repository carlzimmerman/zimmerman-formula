#!/usr/bin/env python3
"""
bullet_data_table.py  -- topic "bullet_data"
============================================
Compiles the REAL observational parameters of the Bullet Cluster 1E 0657-558
(z = 0.296) from the primary literature, and DERIVES the geometric quantities
(peak-to-peak offsets in kpc) directly from the published J2000 coordinates.

This is a DATA-COMPILATION file: every number is sourced. The only things
COMPUTED here are angular separations -> kpc using the cluster's own plate
scale, and the baryon ratios from the published component masses. No framework
fitting is done here (that is downstream). Quarantine held: a0/kappa/Z untouched.

PRIMARY SOURCES
---------------
[C06]  Clowe, Bradac, Gonzalez, Markevitch, Randall, Jones, Zaritsky 2006,
       ApJL 648, L109 ("A Direct Empirical Proof of the Existence of Dark
       Matter"), arXiv:astro-ph/0608407.  -> Table 2 read VERBATIM below.
[B06]  Bradac, Clowe, Gonzalez, et al. 2006, ApJ 652, 937
       ("Strong & Weak Lensing United III"), arXiv:astro-ph/0608408.
[M02]  Markevitch, Gonzalez, David, Vikhlinin, Murray, Forman, Jones, Tucker
       2002, ApJ 567, L27 (Chandra discovery of the bow shock).
[M06]  Markevitch 2006 (Chandra 500 ks; shock Mach 3.0+-0.4, T=14.1+-0.2 keV).
[C04]  Clowe, Gonzalez, Markevitch 2004, ApJ 604, 596 (first WL, 3 sigma).
[SF07] Springel & Farrar 2007, MNRAS 380, 911, arXiv:astro-ph/0703232
       (the velocity reconciliation: shock != bullet bulk speed).
[LK10] Lee & Komatsu 2010, ApJ 718, 60 (LCDM probability of the velocity).
[Par16]Paraficz, Kneib, Richard, et al. 2016, A&A 594, A121,
       arXiv:1209.0384 ("weighing stars, gas, and dark matter").
"""

import numpy as np

# ----------------------------------------------------------------------------
# 0. GLOBAL CLUSTER PARAMETERS
# ----------------------------------------------------------------------------
Z = 0.296                       # [C06] redshift
# [C06] adopt Om=0.3, OL=0.7, H0=70 -> plate scale:
KPC_PER_ARCSEC = 4.413          # [C06] "4.413 kpc/'' plate-scale" at z=0.296
print("="*78)
print("BULLET CLUSTER 1E 0657-558  --  REAL OBSERVATIONAL PARAMETERS")
print("="*78)
print(f"redshift z                 = {Z}")
print(f"plate scale                = {KPC_PER_ARCSEC} kpc/arcsec  (Om=0.3,OL=0.7,H0=70) [C06]")

# ----------------------------------------------------------------------------
# 1. COMPONENT POSITIONS  --  Clowe 2006 Table 2 (J2000), VERBATIM
#    aperture = 100 kpc radius; M_X, M_* in 1e12 Msun; kbar = mean convergence
# ----------------------------------------------------------------------------
def hms_to_deg(h, m, s):   return 15.0*(h + m/60.0 + s/3600.0)
def dms_to_deg(d, m, s):
    sign = -1.0 if d < 0 or (d == 0 and (m < 0 or s < 0)) else 1.0
    return sign*(abs(d) + m/60.0 + s/3600.0)

# Table 2 rows: (label, RA h,m,s, Dec d,m,s, M_X[1e12], dM_X, M_star[1e12], dM_star, kbar, dkbar)
TABLE2 = [
    ("Main cluster BCG",    (6,58,35.3), (-55,56,56.3), 5.5,0.6, 0.54,0.08, 0.36,0.06),
    ("Main cluster plasma", (6,58,30.2), (-55,56,35.9), 6.6,0.7, 0.23,0.02, 0.05,0.06),
    ("Subcluster BCG",      (6,58,16.0), (-55,56,35.1), 2.7,0.3, 0.58,0.09, 0.20,0.05),
    ("Subcluster plasma",   (6,58,21.2), (-55,56,30.0), 5.8,0.6, 0.12,0.01, 0.02,0.06),
]

print("\n--- Clowe 2006 Table 2 (J2000, 100 kpc aperture) -------------------------")
print(f"{'component':22s} {'RA(deg)':>10s} {'Dec(deg)':>10s} {'M_X':>6s} {'M_*':>6s} {'kbar':>6s}")
pos = {}
for lab,(rh,rm,rs),(dd,dm,ds),mx,dmx,mstar,dmstar,kb,dkb in TABLE2:
    ra  = hms_to_deg(rh,rm,rs)
    dec = dms_to_deg(dd,dm,ds)
    pos[lab] = (ra, dec, mx, mstar, kb)
    print(f"{lab:22s} {ra:10.5f} {dec:10.5f} {mx:5.1f}  {mstar:5.2f}  {kb:5.2f}")

# angular separation (small-angle, with cos(dec)) -> arcsec -> kpc
def sep_kpc(a, b):
    ra1,dec1 = pos[a][0], pos[a][1]
    ra2,dec2 = pos[b][0], pos[b][1]
    dec0 = np.radians(0.5*(dec1+dec2))
    dra  = (ra1-ra2)*np.cos(dec0)*3600.0      # arcsec
    ddec = (dec1-dec2)*3600.0                 # arcsec
    arc  = np.hypot(dra, ddec)
    return arc, arc*KPC_PER_ARCSEC

# ----------------------------------------------------------------------------
# 2. THE OFFSETS  (kappa peak ~ BCG/galaxies vs the plasma)  -- DERIVED from Table 2
#    [C06]: kappa peaks coincide with the BCGs/galaxies, NOT the plasma.
# ----------------------------------------------------------------------------
print("\n--- DERIVED peak-to-peak offsets (from Table 2 coords) --------------------")
arc_main, kpc_main = sep_kpc("Main cluster BCG", "Main cluster plasma")
arc_sub,  kpc_sub  = sep_kpc("Subcluster BCG",  "Subcluster plasma")
print(f"MAIN:  BCG/kappa-peak  <->  plasma   = {arc_main:5.1f}''  = {kpc_main:6.1f} kpc")
print(f"SUB :  BCG/kappa-peak  <->  plasma   = {arc_sub:5.1f}''  = {kpc_sub:6.1f} kpc")

# subcluster<->main projected separation: [C06] state 0.72 Mpc 'on the sky'.
arc_bcg, kpc_bcg = sep_kpc("Main cluster BCG", "Subcluster BCG")
print(f"BCG<->BCG (galaxy concentrations)    = {arc_bcg:5.1f}''  = {kpc_bcg:6.1f} kpc")
print(f"  [C06 quote the projected subcluster separation as 0.72 Mpc 'on the sky']")

# ----------------------------------------------------------------------------
# 3. OFFSET SIGNIFICANCE  -- quoted, not re-derived
# ----------------------------------------------------------------------------
print("\n--- Offset SIGNIFICANCE (quoted) -----------------------------------------")
print("  Each kappa peak offset from its OWN plasma cloud  : ~8 sigma   [C06]")
print("  Main-cluster kappa peak detection significance     : 8 sigma   [C06]")
print("  Subcluster   kappa peak detection significance     : 12 sigma  [C06]")
print("  (kappa peaks lie ~2'' from their BCGs, within 1 sigma of the galaxies)")
print("  Main kappa peak vs X-ray, C04 earlier value        : 3.4 sigma [C04]")

# ----------------------------------------------------------------------------
# 4. MASSES & BARYON BUDGET
# ----------------------------------------------------------------------------
print("\n--- Component masses (100 kpc aperture, 1e12 Msun) [C06 Table 2] ----------")
MX_main_bcg, Mstar_main_bcg = 5.5, 0.54
MX_main_pla, Mstar_main_pla = 6.6, 0.23
MX_sub_bcg,  Mstar_sub_bcg  = 2.7, 0.58
MX_sub_pla,  Mstar_sub_pla  = 5.8, 0.12
# Note: M_X here is the PLASMA (gas) mass in the aperture; M_* the stellar mass.
gas_tot_4ap  = MX_main_bcg+MX_main_pla+MX_sub_bcg+MX_sub_pla
star_tot_4ap = Mstar_main_bcg+Mstar_main_pla+Mstar_sub_bcg+Mstar_sub_pla
print(f"  sum of the 4 plasma-mass apertures (M_X) = {gas_tot_4ap:.1f}e12 Msun")
print(f"  sum of the 4 stellar-mass apertures(M_*) = {star_tot_4ap:.2f}e12 Msun")
print(f"  aperture gas/stars (C06 apertures)       = {gas_tot_4ap/star_tot_4ap:.1f}")
print("   -> [C06]: plasma is the DOMINANT baryon; stars are ~1-2% of total mass,")
print("      plasma ~5-15% of total mass  (Allen+2002; Vikhlinin+2006; Kochanek+2003)")

print("\n--- System-level masses (literature) -------------------------------------")
print("  Main cluster total       ~ 2.8e14 Msun        [M02/Markevitch]")
print("  Subcluster (bullet) total~ 2.3e14 Msun        [M02/Markevitch]")
print("  M200 main  ~1.5e15 ; M200 bullet ~1.5e14       [Springel&Farrar/sims]")
print("  Strong-lensing M(<250kpc): main 2.5+-0.1e14, sub 2.0+-0.2e14 [Par16]")
print("  Global baryon split: gas (plasma) ~10-15% of total, stars ~1-2% of total")
print("   => GLOBAL gas/stars ~ 5-10  (plasma dominates baryons by ~order of mag)")

print("\n--- The MOND/no-DM mass-ratio demand [C06 discussion] --------------------")
print("  kappa(DM+gal) : kappa(plasma) ~ 7:1 needed at the peaks;")
print("  for a pure constant-acceleration (deep-MOND) law the required TRUE mass")
print("  ratio is as high as 49:1  -> residual collisionless mass on the galaxies.")

# ----------------------------------------------------------------------------
# 5. VELOCITY  -- the shock-vs-bulk distinction (the load-bearing correction)
# ----------------------------------------------------------------------------
print("\n--- COLLISION / INFALL VELOCITY -----------------------------------------")
print("  Bow-shock velocity (gas)      : 4740 +710/-550 km/s   [M06; Mach 3.0+-0.4, T_u~9keV]")
print("  (older quote 'v ~ 4500 km/s', 'v~4700 km/s' [M02/C06])")
print("  Gas-'bullet' bulk speed       : ~2700 km/s            [SF07]")
print("  Subcluster (DM) bulk speed    : ~2700 km/s in main rest frame [SF07]")
print("  Pre-shock gas inflow          : ~1100 km/s (lowers needed bulk) [SF07]")
print("  Shock-ahead-of-bullet lag     : ~700 km/s             [SF07]")
print("  Initial infall (virial touch) : ~1870 km/s (CM frame) [SF07]")
print("  LOS velocity diff components  : ~600 km/s (~4700 plane-of-sky) [Barrena+02/C06]")
print("  Projected centroid separation : ~720 kpc at best match[SF07] (cf BCG-BCG above)")
print("  Cores passed through each other ~ 100 Myr ago         [C06]")
print("  LCDM probability of v_shock~4500: P ~ 3.3e-11 .. 3.6e-9 (Lee&Komatsu 2010);")
print("    bulk-speed reconciliation (SF07) SOFTENS this -- still a ding, not a kill.")

print("\n" + "="*78)
print("SUMMARY ROW (the headline numbers):")
print("="*78)
print(f"  z=0.296 | scale 4.413 kpc/'' | subcluster sep ~0.72 Mpc")
print(f"  MAIN offset (kappa~galaxies vs plasma) = {kpc_main:.0f} kpc ; SUB = {kpc_sub:.0f} kpc")
print(f"  offset significance ~8 sigma ; kappa peaks 8 sigma (main) / 12 sigma (sub)")
print(f"  kappa_bar: main BCG 0.36+-0.06, sub BCG 0.20+-0.05 (plasma ~0.02-0.05)")
print(f"  gas dominates baryons (gas~10-15%, stars~1-2% of total; global gas/stars ~5-10)")
print(f"  v_shock 4740 +710/-550 km/s ; v_bulk ~2700 km/s (SF07); LCDM P~1e-9..1e-11")
