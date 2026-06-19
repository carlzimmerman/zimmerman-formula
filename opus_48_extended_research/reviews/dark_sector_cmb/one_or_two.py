#!/usr/bin/env python3
"""
ONE COMPONENT, TWO, OR A TENSION? — the framework's dark-sector accounting
(2026-06-19, topic "one_or_two")

THE SHARP QUESTION
------------------
The framework (Zimmerman) is modified-INERTIA MOND with a0 = 9.36e-11 m/s^2 from
de Sitter-Unruh.  Two banked, independent results force a particle/fluid dark sector:

  (A) CLUSTERS: MOND/MI leaves a CENTRAL residual eta(R500) ~ 1.3-2.33 (post-XRISM
      bracket).  The ONLY galaxy-veto-surviving closure is a Tremaine-Gunn-protected
      collisionless fermion on cluster galaxies (sterile-nu-like), ~0.25-Omega.
      (CLUSTER_RESIDUAL_CLOSURE_2026-06-19.md, tremaine_gunn_matter_route.py.)

  (B) CMB: a0 is ABSENT from linear perturbations (Bridge-1 order-counting theorem),
      so the framework does NOT modify the linear CMB; the acoustic peaks (esp. the
      THIRD peak) need a pressureless, CLUSTERING, cold dark component exactly as in
      LCDM -- supplied either by the AeST K(Q) a^-3 dust FLUID (amplitude = free I0)
      or by a literal cold particle.  (SKORDIS_CMB_CLUSTER_DEEPDIVE_LEDGER, ROUTE2_CMB.)

Omega_cluster ~ 0.25 is suspiciously close to Omega_DM(LCDM) ~ 0.26.  Is it the SAME
species doing BOTH -- one component -- or are the cluster-fix (wants HOT/light, phase-
space-thin, galaxy-excluded) and the CMB-fix (wants COLD/heavy, third peak) in TENSION,
forcing TWO components?

This script resolves it on the framework's own footing, BOTH WAYS, by overlaying the
two independent floors as a function of a SINGLE particle mass m:
  - TG cluster floor   : m > m_TG_cluster  (so it can pack the cluster core)
  - TG galaxy-SAFETY   : the relevant statement is the galaxy thresholds -- a species
                         BELOW the dSph floor is galaxy-excluded ("hot escape"); a
                         species ABOVE all galaxy floors is galaxy-ALLOWED (it is then
                         just CDM-in-galaxies, the nuLCDM reading)
  - FREE-STREAMING/CMB : m_thermal > ~3.1-5.7 keV (Lyman-alpha WDM floor) for the
                         small-scale power / cold-enough-for-structure requirement;
                         the third peak itself needs only "clusters like dust" which a
                         keV+ species does.

QUARANTINE: a0/Z/kappa NOT derived.  An Omega ~ 0.25 coincidence is NOT a unification
unless the SAME m satisfies BOTH floors.  Credit a real single-species thread; kill a
manufactured one.  If a single keV species works, the dark sector is 'nuLCDM-like'
(relocated, not eliminated, DM) -- state it honestly.

LITERATURE FLOORS USED (real, sourced 2026-06-19):
  - WDM thermal-relic free-streaming (Lyman-alpha): m_WDM > 3.1 keV (Villasenor+2023,
    arXiv:2209.14220) to 5.7 keV (Irsic+2024, PhysRevD.109.043511, z=4.2-5.0 HIRES/UVES).
  - TG dSph fermion floor: ~100-200 eV (Alvey+2018 arXiv:1704.06644 Segue1 ~100 eV,
    TriII ~127 eV; Di Paolo+2018; classical dSphs push toward ~few hundred eV).  The
    closure file used a conservative 390 eV from its isothermal-core estimate; we carry
    BOTH (100 eV "loose", 390 eV "strict") and show the verdict is the same.
  - TG cluster floor: ~1.5-6.6 eV (this repo's tremaine_gunn_matter_route.py; AFD-2010).
  - sterile-nu->thermal-relic mass map: m_WDM ~ 0.8-3 keV equiv per m_s ~ 7 keV depending
    on production (DW hot vs Shi-Fuller resonant cold).  DW excluded as 100% DM (X-ray +
    Lyman-alpha, Boyarsky/XRISM).  Resonant (Shi-Fuller) 7 keV evades Lyman-alpha only
    marginally; full X-ray+Lyman-alpha window needs m_s >~ 20 keV (recent refinements).
"""
import numpy as np

# ---------- constants ----------
G   = 6.674e-11; c = 2.998e8; Msun = 1.989e30; pc = 3.086e16
kpc = 1e3*pc;    Mpc = 1e6*pc; km = 1e3
Msun_pc3 = Msun/pc**3

# ---------- TG max density (this repo's verified norm; matches AFD-2010 Eq.14 to 0.3%) ----------
def rho_max_TG_Msunpc3(m_eV, sigma_1d_ms, g_nu=2.0):
    """rho_max = 2.16e2 (m/eV)^4 (sigma/c)^3  [Msun/pc^3], g=2 (Tremaine-Gunn 1979)."""
    return 2.16e2 * (m_eV)**4 * (sigma_1d_ms/c)**3 * (g_nu/2.0)

def rho_iso_core(sigma_1d_ms, r_core_m):
    return 9*sigma_1d_ms**2/(4*np.pi*G*r_core_m**2)        # kg/m^3

def m_min_TG_eV(sigma_1d_ms, r_core_m):
    rho_req = rho_iso_core(sigma_1d_ms, r_core_m)/Msun_pc3
    m4 = rho_req / (2.16e2 * (sigma_1d_ms/c)**3)
    return m4**0.25

print("="*84)
print("ONE / TWO / TENSION — overlay of the cluster TG floor and the CMB free-streaming floor")
print("="*84)

# ----------------------------------------------------------------------------
# 1. THE THREE TG FLOORS (cluster, spiral, dSph) — reproduced on this repo's footing
# ----------------------------------------------------------------------------
floors = [
    ("rich cluster core", 1000*km, 250*kpc),
    ("group/poor cluster", 500*km, 150*kpc),
    ("L* spiral (MW)",      100*km,   3*kpc),
    ("dwarf disk",           40*km,   1*kpc),
    ("dSph (Fornax-like)",   10*km, 0.3*kpc),
]
print("\nTG MINIMUM fermion mass to be the DOMINANT DM of each system (this repo's norm):")
print(f"  {'system':22s} {'sigma[km/s]':>11s} {'r_core[kpc]':>11s} {'m_min[eV]':>10s}")
m_cluster_floor = None; m_dSph_floor = None; m_spiral_floor = None
for nm, sg, rc in floors:
    mm = m_min_TG_eV(sg, rc)
    print(f"  {nm:22s} {sg/km:11.0f} {rc/kpc:11.1f} {mm:10.1f}")
    if "cluster core" in nm: m_cluster_floor = mm
    if "dSph" in nm:         m_dSph_floor = mm
    if "spiral" in nm:       m_spiral_floor = mm

# Literature dSph floors (independent of our isothermal estimate)
m_dSph_lit_loose  = 100.0   # eV, Segue1 (Alvey+2018)
m_dSph_lit_strict = 390.0   # eV, the closure-file conservative number

# ----------------------------------------------------------------------------
# 2. THE CMB / FREE-STREAMING FLOOR (Lyman-alpha WDM), as a particle mass
# ----------------------------------------------------------------------------
# Lyman-alpha thermal-relic floor (95% CL)
m_WDM_thermal_loose  = 3.1   # keV (Villasenor+2023)
m_WDM_thermal_strict = 5.7   # keV (Irsic+2024)

# Map thermal-relic WDM mass -> sterile-neutrino mass (production-dependent).
# DW (non-resonant, hot): m_s ~ 2.5-4.5 x m_WDM (a 3 keV WDM ~ 7-15 keV DW-sterile),
#   BUT DW is X-ray excluded as 100% DM for all masses.
# Shi-Fuller (resonant, COLDER): a given m_s maps to a LARGER effective m_WDM (colder),
#   i.e. resonant sterile at fixed m_s evades Lyman-alpha better; full X-ray+Lya window
#   needs m_s >~ 20 keV (recent refinements).
# We work in thermal-relic-equivalent keV throughout; the sterile mass is >= this.
def m_s_from_m_WDM_DW(m_WDM_keV):
    """Approx Viel/Bode-Ostriker-Turok scaling for non-resonant (DW) sterile:
       m_s ~ 4.43 keV (m_WDM/1keV)^(4/3) (Omega_dm h^2/0.1225)^(-1/3); take Omega h^2~0.12."""
    return 4.43 * (m_WDM_keV)**(4.0/3.0)

print("\n" + "-"*84)
print("CMB / SMALL-SCALE FREE-STREAMING FLOOR (Lyman-alpha WDM, 95% CL):")
print(f"  thermal-relic WDM mass  m_WDM > {m_WDM_thermal_loose:.1f} keV (loose, Villasenor+2023)")
print(f"                          m_WDM > {m_WDM_thermal_strict:.1f} keV (strict, Irsic+2024)")
print(f"  -> non-resonant (DW) sterile-equiv: m_s ~ {m_s_from_m_WDM_DW(m_WDM_thermal_loose):.1f}"
      f"-{m_s_from_m_WDM_DW(m_WDM_thermal_strict):.1f} keV (but DW is X-ray EXCLUDED as 100% DM)")
print( "  -> resonant (Shi-Fuller) sterile: colder at fixed m_s; full X-ray+Lya window m_s >~ 20 keV")
print( "  NOTE: the THIRD PEAK per se needs only 'clusters like a^-3 dust' -> any keV+ cold")
print( "        species (or the AeST K(Q) FLUID) supplies it; the binding CMB-side number for")
print( "        a PARTICLE is the small-scale (Lyman-alpha) free-streaming floor, ~3-6 keV.")

# ----------------------------------------------------------------------------
# 3. THE OVERLAY — is there a SINGLE mass m that threads both?
# ----------------------------------------------------------------------------
print("\n" + "="*84)
print("THE OVERLAY: a single particle mass m on the number line (eV)")
print("="*84)
print(f"""
  cluster TG floor (can pack a cluster core)   m > {m_cluster_floor:8.1f} eV  = {m_cluster_floor/1e3:.4f} keV
  L* spiral TG floor                           m > {m_spiral_floor:8.1f} eV  = {m_spiral_floor/1e3:.4f} keV
  dSph TG floor (this repo iso)                m > {m_dSph_floor:8.1f} eV  = {m_dSph_floor/1e3:.4f} keV
  dSph TG floor (literature loose/strict)      m > {m_dSph_lit_loose:.0f}-{m_dSph_lit_strict:.0f} eV
  ------------------------------------------------------------------------------
  CMB free-streaming floor (Lyman-alpha)       m > {m_WDM_thermal_loose*1e3:8.0f} eV  = {m_WDM_thermal_loose:.1f} keV (loose)
                                               m > {m_WDM_thermal_strict*1e3:8.0f} eV  = {m_WDM_thermal_strict:.1f} keV (strict)
""")

# The decisive ordering:
print("DECISIVE ORDERING (eV), low -> high:")
order = sorted([
    ("cluster TG floor",        m_cluster_floor),
    ("spiral TG floor",         m_spiral_floor),
    ("dSph TG floor (iso)",     m_dSph_floor),
    ("dSph TG floor (lit loose)", m_dSph_lit_loose),
    ("dSph TG floor (lit strict)",m_dSph_lit_strict),
    ("CMB free-stream (loose)", m_WDM_thermal_loose*1e3),
    ("CMB free-stream (strict)",m_WDM_thermal_strict*1e3),
], key=lambda x: x[1])
for nm, v in order:
    bar = "#"*int(np.clip(np.log10(max(v,1))*6, 0, 60))
    print(f"  {v:9.1f} eV  {nm:28s} {bar}")

# ----------------------------------------------------------------------------
# 4. THE TWO READINGS OF "GALAXY-SAFETY"
# ----------------------------------------------------------------------------
print("\n" + "="*84)
print("THE CRUX: 'galaxy-safety' has TWO inequivalent meanings -> two scenarios")
print("="*84)
print(f"""
  READING (I) -- "HOT ESCAPE" (the Sanders/Angus cluster-only fix, m ~ eV):
     m must be BELOW the dSph/spiral TG floor so it is PHASE-SPACE-EXCLUDED from galaxies
     -> leaves the SPARC RAR untouched by construction.  Requires:
         {m_cluster_floor:.1f} eV  <  m  <  {m_dSph_lit_loose:.0f} eV   (cluster-on, galaxy-off)
     This is an eV-scale, HOT species.  It is FAR below the CMB free-streaming floor of
     ~{m_WDM_thermal_loose*1e3:.0f} eV by a factor ~{m_WDM_thermal_loose*1e3/30:.0f}-{m_WDM_thermal_strict*1e3/30:.0f}x.
     => This species is too HOT to be the CMB dark matter (fails the third-peak/clustering
        free-streaming requirement).  Reading (I) needs a SECOND, colder CMB component.

  READING (II) -- "nuLCDM / cold species clears EVERYTHING" (m ~ keV):
     m ABOVE the CMB free-streaming floor (~3-6 keV) is automatically ABOVE every TG
     galaxy floor (cluster 4 eV, spiral 69 eV, dSph 100-390 eV) by >~1-3 dex.  So a keV
     species is TG-ALLOWED in galaxies -- it does NOT free-stream out; it sits in galaxy
     halos as ordinary (warm) CDM.  Then galaxy-safety is NOT phase-space exclusion; it
     is the standard MOND-with-some-CDM problem: any CDM in a galaxy ADDS rotation-curve
     mass and would spoil the pure-MOND RAR unless its galactic abundance is small.
""")

# Quantify reading (II): does a keV species, present at Omega~0.25 cosmically, over-fill galaxies?
print("-"*84)
print("READING (II) galaxy-veto NUMBER: does keV CDM at Omega~0.25 spoil the SPARC RAR?")
print("-"*84)
# A keV WDM with Omega~0.25 behaves like CDM on galaxy scales EXCEPT it free-streams out
# of the smallest halos (its half-mode mass). For m_WDM~3-6 keV the half-mode mass is
# ~1e8-1e9 Msun -- BELOW typical SPARC disks (>1e9 Msun). So in an L* spiral a 3-6 keV
# species clusters like CDM and contributes ~ the cosmic DM fraction.
# => it would supply a near-LCDM halo in each galaxy -> the galaxy is then LCDM-like, NOT
#    pure-MOND. The framework's RAR success (which assumes NO halo) is then DOUBLE-COUNTING
#    unless the keV abundance INSIDE galaxies is suppressed.
def half_mode_mass_Msun(m_WDM_keV):
    """Approx half-mode halo mass for thermal WDM (Schneider+2012 / Lovell+2014 scaling):
       M_hm ~ 3.0e8 (m_WDM/3keV)^(-10/3) Msun (order-of-magnitude)."""
    return 3.0e8 * (m_WDM_keV/3.0)**(-10.0/3.0)
for mW in [3.0, 5.7, 10.0, 20.0]:
    print(f"   m_WDM={mW:5.1f} keV -> half-mode halo mass ~ {half_mode_mass_Msun(mW):.2e} Msun"
          f"  ({'BELOW' if half_mode_mass_Msun(mW)<1e9 else 'NEAR/ABOVE'} SPARC disk ~1e9-1e11)")
print("""
  READ: a 3-6 keV species free-streams out ONLY of <~1e8-1e9 Msun halos. Typical SPARC
  disks (1e9-1e11 Msun) are ABOVE the half-mode mass -> a keV species DOES cluster in
  them as warm CDM. So reading (II) is literally LCDM-in-galaxies (plus MOND on top):
  the rotation curves would get a CDM halo AND the MOND boost -> OVER-predict unless the
  MOND boost is dropped (i.e. you are back to LCDM, not the framework).  A keV species
  that is cold enough for the CMB is NOT phase-space-excluded from galaxies.
""")

# ----------------------------------------------------------------------------
# 4b. THE 11 eV ANGUS COUNTEREXAMPLE — both-ways: does the third peak REALLY need keV?
# ----------------------------------------------------------------------------
print("-"*84)
print("BOTH-WAYS: the Angus-2009 11 eV sterile DID fit the 2009 CMB third peak — re-examine")
print("-"*84)
print("""
  CREDIT (do not overstate the CMB floor): Angus 2009 (MNRAS 394, 527) showed a SINGLE
  11 eV sterile neutrino reproduces the CMB power spectrum INCLUDING the third peak (mass
  within ~10% of 11 eV).  Why: at recombination an 11 eV sterile is non-relativistic and
  Omega_nu_s h^2 ~ 0.117 ~ Omega_CDM -> it clusters enough to lift the third peak.  By
  CONTRAST 3x(1-2 eV) active neutrinos suppress the third peak ~25% (too hot, TG free-
  streaming).  So the THIRD-PEAK floor is NOT strictly 3 keV; an 11 eV single sterile can
  pass the *acoustic-peak* test.  This is the honest counter to 'CMB needs keV'.

  BUT the 11 eV scenario is killed by the OTHER CMB-era + late-time data, NOT the peak:
   - 11 eV at Omega_nu h^2~0.117 means a FULLY-thermalized species -> DeltaN_eff ~ 1,
     vs Planck+DESI N_eff = 3.0 +- ~0.2 (excludes a thermalized ~eV sterile).
   - DESI+Planck Sum m_nu / sterile m_eff ~ 0.5 eV (arXiv:2501.10785) -> an 11 eV
     thermal sterile is excluded by ~20x on the cosmological mass.
   - small-scale POWER: an 11 eV species free-streams ~10s of Mpc (HOT) -> wipes out the
     Lyman-alpha small-scale power (m_WDM-equiv << 3 keV) -> excluded by the same Lyman-
     alpha data that sets the 3-6 keV floor.
  NET both-ways: the third PEAK alone tolerates 11 eV, so 'CMB strictly needs keV' is an
  OVERSTATEMENT at the peak level — BUT the FULL modern CMB+LSS package (N_eff, DESI mass,
  Lyman-alpha small-scale power) DOES force keV-cold, and rules out the 11 eV hot fix.  The
  eV-hot vs keV-cold tension therefore STANDS once 2024 data is used, even though it is the
  N_eff/Lyman-alpha axis (not the bare third-peak height) that bites the eV species.
""")

# ----------------------------------------------------------------------------
# 5. THE VERDICT TABLE — one mass cannot be both eV-hot-and-galaxy-excluded AND keV-cold
# ----------------------------------------------------------------------------
print("="*84)
print("VERDICT: is there a SINGLE mass window that threads BOTH floors?")
print("="*84)
# The window for "cluster-on, galaxy-off AND CMB-cold" requires simultaneously:
#   m > cluster TG floor      (~4 eV)        [cluster fill]
#   m < dSph TG floor         (~100-390 eV)  [galaxy phase-space exclusion, hot escape]
#   m > CMB free-stream floor (~3100-5700 eV)[cold enough for CMB]
# (2nd) and (3rd) are MUTUALLY EXCLUSIVE: m < 390 eV AND m > 3100 eV is EMPTY.
lo_gal_excl = m_dSph_lit_strict       # must be below this to be galaxy-EXCLUDED (hot escape)
hi_cmb      = m_WDM_thermal_loose*1e3  # must be above this to be CMB-cold
print(f"""
  To be the SAME species doing BOTH the cluster-only HOT fix AND the cold CMB:
     need  m < {lo_gal_excl:.0f} eV   (galaxy phase-space exclusion -- the 'hot escape')
     AND   m > {hi_cmb:.0f} eV   (CMB free-streaming / small-scale power)
     -> {lo_gal_excl:.0f} eV < ... > {hi_cmb:.0f} eV  =>  EMPTY (gap factor {hi_cmb/lo_gal_excl:.1f}x).

  THE HOT-ESCAPE READING AND THE COLD-CMB READING CANNOT BE THE SAME PARTICLE.

  The ONLY way ONE particle does both is reading (II): a keV+ species that is cold enough
  for the CMB and is ALSO TG-allowed in galaxies.  But then it is NOT phase-space-excluded
  from galaxies -- it is literally warm CDM in galaxies = 'nuLCDM'.  Galaxy-safety then
  requires the MOND boost to NOT be double-counted, i.e. the galaxy dynamics are CDM-like,
  which is the OPPOSITE of the framework's pure-MOND RAR claim.

  ====> RESULT: 'one_or_two' = TWO-NEEDED (in the strict/honest reading), OR equivalently a
        keV single species that makes the dark sector nuLCDM-LIKE (relocated DM), NOT a
        MOND-replaces-galaxy-DM unification.
""")

# ----------------------------------------------------------------------------
# 6. THE AeST K(Q) FLUID ESCAPE (the framework's ACTUAL banked CMB-fix) — note it honestly
# ----------------------------------------------------------------------------
print("="*84)
print("THE FLUID ESCAPE (AeST K(Q)) — why the framework is not forced into the keV particle")
print("="*84)
print("""
  The framework's BANKED CMB-fix is NOT a thermal particle: it is the AeST K(Q) scalar's
  a^-3 'dust' mode (Skordis-Zlosnik 2021), a FLUID with EXACTLY a^-3 scaling -> ZERO
  free-streaming (cold by construction, no Tremaine-Gunn, no Lyman-alpha cutoff).  Its
  amplitude is the FREE integration constant I0 ~ Omega_dm ~ 0.26, orthogonal to a0=Lambda.

  CONSEQUENCE FOR 'one_or_two':
   - If the CMB clustering is the K(Q) FLUID and the cluster residual is a TG particle,
     that is TWO distinct dark sectors (a fluid + a particle) -> NOT one component.
   - If BOTH the CMB and clusters are the SAME K(Q) fluid, the fluid must also CLUSTER on
     cluster scales without spoiling galaxies -- which is the literature-OPEN AeST question
     (ROUTE2/SKORDIS ledger: 'remains to be seen'); and the fluid carries NO phase-space
     galaxy-exclusion, so it would also cluster in galaxies (same nuLCDM tension).
   - Either way the amplitude is a SEPARATE ~0.25-Omega number (I0), not from a0=Lambda.

  So the FLUID escape removes the eV/keV TENSION (a fluid is cold and not TG-bound) but it
  does NOT remove the COST: a second ~0.25-Omega dark component whose amplitude is a free
  number.  The Omega~0.25 'coincidence' is NOT a unification -- it is the same I0~Omega_dm
  that LCDM also free-fits.
""")

# ----------------------------------------------------------------------------
# 7. ALLOWED MASS WINDOW SUMMARY
# ----------------------------------------------------------------------------
print("="*84)
print("ALLOWED MASS WINDOW (if any) — final accounting")
print("="*84)
print(f"""
  (a) SINGLE eV species, cluster-only HOT fix (galaxy phase-space excluded):
        window  ~ {m_cluster_floor:.1f} - {m_dSph_lit_loose:.0f} eV   (EXISTS, but CMB-TOO-HOT)
        -> needs a SEPARATE cold CMB component => TWO components.

  (b) SINGLE keV species threading cluster + galaxy + CMB:
        window  m > {m_WDM_thermal_strict:.1f} keV  (Lyman-alpha strict) — and for a sterile
        neutrino the X-ray+Lyman-alpha joint window needs m_s >~ 20 keV (resonant).
        This species IS cold enough for the CMB and CAN pack clusters, BUT it is
        TG-ALLOWED in galaxies (above all galaxy floors) -> it clusters in galaxies as
        warm CDM.  => the dark sector is nuLCDM-LIKE (relocated DM); galaxy-safety now
        rests on the MOND-vs-CDM degeneracy, NOT phase-space exclusion.  This is ONE
        component, but it is CDM-by-another-name, not a MOND elimination of galaxy DM.

  (c) The framework's actual banked fix (AeST K(Q) FLUID): cold, not TG-bound, fits the
        CMB; amplitude = free I0 ~ 0.26.  Removes the eV/keV tension but is a SEPARATE
        ~0.25-Omega number, not from a0=Lambda; for clusters it is the literature-OPEN
        question.  => still NOT a one-number unification.

  BOTTOM LINE (both ways):
   * The eV cluster-fix (hot, galaxy-excluded) and the keV CMB-fix (cold, third peak) are
     in genuine TENSION as a SINGLE PARTICLE: the windows are disjoint by ~{hi_cmb/lo_gal_excl:.0f}x.
   * A single ~keV+ (or fluid) species CAN do both numerically, but ONLY by being cold
     CDM that clusters in galaxies too -> 'nuLCDM-like': DM is RELOCATED, not eliminated.
   * The Omega~0.25 closeness is NOT a unification: it is a free amplitude (I0 / sterile
     abundance) that LCDM also fits; the framework REPLACES galaxy-scale DM with MOND but
     STILL NEEDS ~LCDM-amount of (cold) DM for clusters+CMB.  Say so honestly.
""")
print("DONE.")
