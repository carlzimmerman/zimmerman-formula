#!/usr/bin/env python3
"""
THE CRUX: does the cluster-closure's galaxy-safe component ALSO do the CMB?
(2026-06-19, topic "cluster_component_cmb")

The framework (Zimmerman a0=9.36e-11, MODIFIED INERTIA) does NOT modify the LINEAR
CMB (Bridge-1 order-counting: a0 absent from linear perturbations).  So the CMB
acoustic peaks need a DARK COMPONENT exactly as in LCDM.  Separately, the cluster-
closure calc (CLUSTER_RESIDUAL_CLOSURE_2026-06-19.md) found the framework needs a
galaxy-SAFE collisionless component for clusters: a Tremaine-Gunn-protected eV-keV
fermion, ~0.25-Omega.

QUESTION (both-ways, quarantine held): is the cluster-required component the SAME
species as the CMB dark matter, consistently?  An Omega~0.25 coincidence is NOT a
unification unless the SAME mass m satisfies BOTH:
   (cluster, lower bound) the TG phase-space floor to pack into a cluster core,
   (CMB, lower bound)     the free-streaming floor to be "cold enough" to (i) NOT
                          erase the CMB third peak and (ii) clear Lyman-alpha.
...while ALSO respecting galaxy-safety (which the eV reading buys as an UPPER bound,
the dSph TG floor: an eV fermion is FORBIDDEN from dwarfs, which is why it's galaxy-
safe and why MOND needed it).

We compute TWO independent mass floors and ask: OVERLAP (one species works) or a
GAP (tension / two components)?

TWO BOUNDS:
  BOUND A  (cluster, phase-space / Tremaine-Gunn):
     m_min,TG = [ rho_req / (2.16e2 (sigma/c)^3) ]^(1/4)   [eV]
     (Angus-Famaey-Diaferio 2010 Eq.14 norm; matches repo tremaine_gunn_matter_route.py)
     - cluster core (sigma~1000): m_min ~ a few eV  -> CAN pack
     - dSph (sigma~10):           m_min ~ hundreds eV -> galaxy-safety floor
       (the eV fermion is forbidden from dwarfs = galaxy-safe)

  BOUND B  (CMB / Lyman-alpha, free-streaming):
     - HARD CMB exclusion: an eV-scale thermalized fermion (HOT DM) free-streams
       tens of Mpc -> erases sub-horizon clustering -> CANNOT source the 3rd peak.
       The third peak directly measures the COLD clustering density (CAMB: P3/P2
       rises monotonically with Omega_c h^2; baryon-only/HDM fails by any tuning,
       per SKORDIS_CMB_CLUSTER_DEEPDIVE_LEDGER_2026-06-15.md). HDM mass to be the
       DM is excluded: needs m_WDM >> eV.
     - Lyman-alpha thermal-relic WDM floor: m_WDM >~ 3.5-5.7 keV (2017-2024).
       Below this, too much small-scale power is erased.
     - thermal-relic <-> Dodelson-Widrow sterile mapping (Viel 2005 / Abazajian 2006):
       m_sterile = 4.43 keV (m_WDM/keV)^(4/3) (Omega h^2/0.1225)^(-1/3).

THE TEST: plot m_min,cluster-TG (a few eV) and m_min,galaxy-safe (dSph, ~390 eV)
and m_min,CMB-cold (Lyman-a, >~5 keV thermal / >~ many-keV sterile) on the SAME
mass axis.  The CMB-cold floor sits FAR ABOVE the eV cluster-fix AND above the
galaxy-safety dSph floor.  Where they fall determines one-vs-two.

LITERATURE (real, pulled this session):
 - Tremaine & Gunn 1979, PRL 42, 407 (phase-space bound)
 - Angus, Famaey & Diaferio 2010, MNRAS 402, 395 (arXiv:0906.3322) Eq.14
 - Boyarsky, Ruchayskiy, Iakubovskyi, Macias 2009 (TG for clusters/dwarfs)
 - Bode, Ostriker & Turok 2001, ApJ 556, 93 (WDM free-streaming)
 - Bond & Szalay 1983 (HDM free-streaming ~ tens of Mpc for eV fermion)
 - Viel et al. 2005, PRD 71, 063534; Abazajian 2006 (thermal<->sterile mapping)
 - Lyman-a thermal WDM floor m_WDM>~3.5 keV (Viel 2013), 5.3 keV (Irsic 2017),
   5.7 keV (2024 high-res): conservative >~5 keV.
 - Planck 2018: Omega_cdm h^2 = 0.120, Omega_DM ~ 0.265 (h=0.674).
"""
import numpy as np

# ---------------- constants ----------------
c    = 2.998e8          # m/s
G    = 6.674e-11
Msun = 1.989e30
pc   = 3.086e16
kpc  = 1e3*pc; Mpc = 1e6*pc
km   = 1e3
eV   = 1.602e-19
Msun_pc3 = Msun/pc**3

a0_FW = 9.36e-11

print("="*84)
print("CLUSTER-COMPONENT-CMB CRUX: does the SAME galaxy-safe species do clusters AND the CMB?")
print("="*84)

# ===========================================================================
# BOUND A  —  TREMAINE-GUNN phase-space floor (CLUSTER fill + GALAXY safety)
#   (exactly the repo tremaine_gunn_matter_route.py norm; reproduced here)
# ===========================================================================
def rho_max_TG_Msunpc3(m_eV, sigma_ms, g=2.0):
    """AFD-2010 Eq.14 norm: rho_max = 2.16e2 (m/eV)^4 (sigma/c)^3 [Msun/pc^3], g=2."""
    return 2.16e2 * m_eV**4 * (sigma_ms/c)**3 * (g/2.0)

def rho_iso_core(sigma_ms, r_core_m):
    """Isothermal-core dynamical density rho = 9 sigma^2/(4 pi G r_c^2)."""
    return 9*sigma_ms**2/(4*np.pi*G*r_core_m**2)   # kg/m^3

def m_min_TG_eV(sigma_ms, rho_req_Msunpc3):
    """Min fermion mass (eV) for TG to ALLOW it to be the DM of (sigma, rho_req)."""
    m4 = rho_req_Msunpc3 / (2.16e2*(sigma_ms/c)**3)
    return m4**0.25

# the systems (same as repo); rho_req = isothermal-core dyn density
systems = [
    ("Rich cluster core (Coma)", 1000*km, 250*kpc),
    ("Group / poor cluster",      500*km, 150*kpc),
    ("L* spiral (Milky Way)",     100*km,   3*kpc),
    ("SPARC dwarf disk",           40*km,   1*kpc),
    ("dSph (Fornax-like)",         10*km, 0.3*kpc),
]
print("\n--- BOUND A: Tremaine-Gunn minimum fermion mass to be the DM of each system ---")
print(f"{'system':27s} {'sigma[km/s]':>11s} {'rho_req[Msun/pc3]':>17s} {'m_min,TG[eV]':>12s}")
TG = {}
for nm, sig, rc in systems:
    rho_req = rho_iso_core(sig, rc)/Msun_pc3
    mmin = m_min_TG_eV(sig, rho_req)
    TG[nm] = mmin
    print(f"{nm:27s} {sig/km:11.0f} {rho_req:17.3e} {mmin:12.1f}")

m_TG_cluster = TG["Rich cluster core (Coma)"]   # cluster FILL floor (lower bound to pack)
m_TG_dSph    = TG["dSph (Fornax-like)"]         # GALAXY-SAFETY floor (eV reading: m<this => dwarf-excluded)
m_TG_spiral  = TG["L* spiral (Milky Way)"]
print(f"""
  CLUSTER FILL floor (lower bound to pack a cluster core): m_TG,cluster = {m_TG_cluster:.1f} eV
  GALAXY-SAFETY floor (dSph TG): an eV fermion below ~{m_TG_dSph:.0f} eV is FORBIDDEN from
  dwarfs -> galaxy-safe (this is WHY the eV cluster-fix never spoiled rotation curves).
  L* spiral TG floor: {m_TG_spiral:.0f} eV.
  => the eV cluster-fix lives in the WINDOW {m_TG_cluster:.0f} eV < m < {m_TG_dSph:.0f} eV (cluster-ON, galaxy-OFF).
""")

# ===========================================================================
# BOUND B  —  CMB / Lyman-alpha free-streaming floor (COLD-enough)
# ===========================================================================
# (B1) HOT-DM free-streaming length for a thermalized fermion of mass m (eV):
#   Bond & Szalay 1983 / classic HDM: a relativistic-decoupled thermal fermion
#   free-streams lambda_FS ~ 40 Mpc (30 eV / m)*(<p/T>/3.15) comoving.
#   <p/T>=3.15 for a Fermi-Dirac fermion -> lambda_FS ~ 1.2 Mpc (keV/m)*... at keV.
def lambda_FS_HDM_Mpc(m_eV, pT=3.15):
    """Free-streaming length [Mpc] of a relativistic-decoupled thermal fermion mass m.
       Bond-Szalay/Bardeen form: lambda_FS ~ 40 Mpc (30 eV/m)(<p/T>/3.15)."""
    return 40.0 * (30.0/m_eV) * (pT/3.15)

# (B2) Thermal-relic WDM free-streaming (Bode-Ostriker-Turok 2001 empirical):
#   lambda_FS ~ 0.049 (m_th/keV)^(-1.11) Mpc/h  (half-mode-ish; small-scale cutoff)
def lambda_FS_WDM_Mpc(m_keV, h=0.674):
    return 0.049 * (m_keV)**(-1.11) / h   # Mpc (physical-ish; /h folded out approx)

# (B3) thermal-relic <-> Dodelson-Widrow sterile mapping (Viel 2005):
#   m_sterile = 4.43 keV (m_th/keV)^(4/3) (Omega_DM h^2/0.1225)^(-1/3)
def m_sterile_from_thermal_keV(m_th_keV, Omega_h2=0.120):
    return 4.43 * (m_th_keV)**(4.0/3.0) * (Omega_h2/0.1225)**(-1.0/3.0)

# Lyman-alpha thermal-relic WDM floor (conservative .. strong)
m_WDM_floor_keV = {"Viel2013 (3.3 keV)":3.3, "conservative (3.5)":3.5,
                   "Irsic2017 (5.3)":5.3, "2024 high-res (5.7)":5.7}

print("--- BOUND B: free-streaming length vs mass (HOT eV reading vs WARM keV reading) ---")
print("\n (B1) HOT-DM free-streaming of a thermalized eV-keV fermion (Bond-Szalay):")
print(f"   {'m':>8s}   {'lambda_FS [Mpc]':>16s}    note")
for m_eV, note in [(2.0,"active-nu (Sanders)"),(11.0,"AFD sterile (cluster fix)"),
                   (100.0,""),(390.0,"dSph TG floor"),(1000.0,"1 keV"),(5000.0,"5 keV"),(7000.0,"7 keV (3.5keV-line)")]:
    print(f"   {m_eV:7.0f}eV  {lambda_FS_HDM_Mpc(m_eV):16.3f}    {note}")
# --- BOTH-WAYS CORRECTION on the "third peak" claim (do NOT manufacture the tension) ---
# Angus 2009 (MNRAS 394, 527) EXPLICITLY fits the first THREE acoustic peaks with a
# single 11-eV sterile, BECAUSE Omega_nu(11eV)~0.25~Omega_cdm and the acoustic peaks
# (l~200-800) probe LARGE comoving scales near the sound horizon r_s~147 Mpc -- LARGER
# than the 11-eV free-streaming scale at z~1100 (the FS scale grows to ~tens-of-Mpc
# only at LOW z; at recombination the relevant k are still inside the horizon).  So the
# honest statement is NOT "11 eV can't do the third peak."  The real 11-eV exclusion is:
#   (1) the SMALL-SCALE matter power spectrum / Lyman-alpha forest (FS suppresses P(k)
#       below ~tens of Mpc -> Lyman-a needs m_WDM>~5 keV, fatal to 11 eV as the DM);
#   (2) LAB + cosmology: KATRIN (active nu<0.45 eV; 259-day sterile search 2025 squeezes
#       eV mixing), DESI+CMB Sum m_nu<0.072 eV (active), N_eff=3.0+-0.2 (thermalized eV
#       sterile adds DeltaN_eff~1, disfavored).
# So 11-eV is excluded as the DOMINANT DM by SMALL-SCALE structure + lab, NOT by the
# acoustic peaks per se.  We keep both readings explicit below.
r_s_comov = 147.0   # Mpc, sound horizon at recombination (Planck)
print(f"""
   READ (both ways, corrected): the 11-eV fermion has a LATE-time free-streaming
   scale ~ {lambda_FS_HDM_Mpc(11.0):.0f} Mpc (this number is the z~0 comoving FS length, the
   galaxy/cluster-suppression scale).  At RECOMBINATION the acoustic peaks probe
   k near the sound horizon r_s~{r_s_comov:.0f} Mpc; Angus 2009 (MNRAS 394,527) shows a single
   11-eV sterile with Omega_nu~0.25 DOES fit the FIRST THREE peaks (its density ~
   Omega_cdm, and it clusters at the large acoustic scales).  So the honest claim is
   NOT 'it fails the third peak.'  The 11-eV EXCLUSION is:
     (1) SMALL-SCALE matter power / Lyman-alpha: FS suppresses P(k) below ~tens of Mpc;
         Lyman-a demands m_WDM>~5 keV -> 11 eV fatally over-erases small-scale structure;
     (2) LAB+cosmo: KATRIN, DESI+CMB Sum m_nu<0.072 eV, N_eff -- squeeze a thermalized
         eV sterile (DeltaN_eff~1).
   => the eV reading dies on Lyman-a + lab, NOT on the third peak.  The CMB-COLD floor
   that bites is the Lyman-alpha small-scale-power floor m_WDM>~5 keV.
""")

print(" (B2) WARM-DM free-streaming (thermal relic, Bode-Ostriker-Turok):")
print(f"   {'m_th [keV]':>10s}   {'lambda_FS [Mpc]':>16s}   {'m_sterile(DW) [keV]':>20s}")
for m_keV in [0.4, 1.0, 3.0, 3.5, 5.0, 5.7, 7.0]:
    print(f"   {m_keV:10.1f}   {lambda_FS_WDM_Mpc(m_keV):16.4f}   {m_sterile_from_thermal_keV(m_keV):20.2f}")

print("\n (B3) Lyman-alpha THERMAL-RELIC WDM mass floor (the CMB-cold/structure floor):")
for k,v in m_WDM_floor_keV.items():
    print(f"   {k:24s}: m_WDM >= {v:.1f} keV  <->  m_sterile(DW) >= {m_sterile_from_thermal_keV(v):.1f} keV")
m_WDM_cons = 5.0
m_sterile_cons = m_sterile_from_thermal_keV(m_WDM_cons)
print(f"""
   CMB-COLD / structure floor (conservative): m_WDM >= ~{m_WDM_cons:.0f} keV (thermal)
   == m_sterile(DW) >= ~{m_sterile_cons:.0f} keV.  Below this the small-scale power
   (Lyman-a forest) is over-erased; an HDM eV fermion is excluded outright.
""")

# ===========================================================================
# THE CRUX — put BOTH floors on the SAME mass axis; OVERLAP or GAP?
# ===========================================================================
print("="*84)
print("THE CRUX — both floors on the SAME mass axis")
print("="*84)
# Convert the CMB-cold floor to the units BOUND A uses (a particle MASS).
# The cluster TG floor and galaxy-safety floor are particle masses in eV.
# The CMB-cold floor is a particle mass in keV (thermal) or sterile-keV.
# To compare apples-to-apples, express all as the PARTICLE mass in eV.
m_TG_cluster_eV   = m_TG_cluster
m_TG_dSph_eV      = m_TG_dSph
# the CMB-cold floor as a thermal-relic particle mass and as a DW-sterile mass:
m_CMB_thermal_eV  = m_WDM_cons*1e3        # ~5000 eV thermal relic
m_CMB_sterile_eV  = m_sterile_cons*1e3    # ~ (DW sterile) eV

print(f"""
 On a single particle-mass axis (eV):

   cluster TG FILL floor (pack a cluster core)   m >~ {m_TG_cluster_eV:6.1f} eV   [LOWER bound]
   galaxy-SAFETY floor   (eV-reading, dSph TG)   m <~ {m_TG_dSph_eV:6.0f} eV   [UPPER bound, for galaxy-OFF]
   ------------------------------------------------------------------
   CMB-COLD floor (thermal relic, Lyman-a)       m >~ {m_CMB_thermal_eV:6.0f} eV   [LOWER bound]
   CMB-COLD floor (Dodelson-Widrow sterile)      m >~ {m_CMB_sterile_eV:6.0f} eV   [LOWER bound]
""")

# The eV cluster-fix window (cluster-ON & galaxy-OFF) vs the CMB-cold floor:
window_lo, window_hi = m_TG_cluster_eV, m_TG_dSph_eV
print(f" The eV cluster-fix (Angus) lives in the TG window  [{window_lo:.0f}, {window_hi:.0f}] eV (cluster-ON, galaxy-OFF).")
print(f" The CMB-cold floor demands m >~ {m_CMB_thermal_eV:.0f} eV (thermal) / {m_CMB_sterile_eV:.0f} eV (DW sterile).")
gap_factor = m_CMB_thermal_eV/window_hi
print(f"""
 => The CMB-COLD (Lyman-alpha small-scale-power) floor ({m_CMB_thermal_eV:.0f} eV thermal) sits ABOVE the
    TOP of the eV cluster-fix window ({window_hi:.0f} eV) by a factor ~{gap_factor:.0f}x.  The eV reading that
    buys cluster-fill + phase-space galaxy-safety is FAR TOO HOT for SMALL-SCALE
    structure (Lyman-a).  >>> There is a GAP, not an overlap, for the eV reading:
    the 11-eV/active cluster-fix CAN assist the acoustic PEAKS (Angus 2009) but is
    excluded as the dominant DM by the Lyman-a small-scale matter power + KATRIN/DESI/
    N_eff lab bounds.  The GAP is between phase-space-galaxy-safety (eV) and small-scale-
    coldness (keV), NOT at the acoustic third peak.
""")

# ---- Now the keV reading: does a SINGLE keV sterile thread BOTH? ----
print("-"*84)
print("THE keV READING — does a single keV sterile thread cluster-TG AND galaxy-safety AND CMB-cold?")
print("-"*84)
# A keV sterile (~3.9-7 keV DW) is the cluster_closure 'next calc'. Check all three:
m_test_sterile_keV = [3.9, 5.0, 7.0]   # DW-sterile masses, keV
for m_s_keV in m_test_sterile_keV:
    m_s_eV = m_s_keV*1e3
    # (i) cluster TG: trivially OK (m >> few eV); (ii) galaxy-safety dSph:
    #     a keV sterile is ABOVE the dSph TG floor (390 eV) -> it CAN sit in dwarfs.
    galaxy_excluded = m_s_eV < m_TG_dSph_eV
    # but TG-allowed in dwarfs does NOT mean it ruins RC: it just means it's a viable
    # *galaxy DM* too (warm DM galaxy). The cluster_closure veto is RAR-scatter, separate.
    # (iii) CMB-cold: compare to the DW-sterile Lyman-a floor.
    cmb_cold = m_s_keV >= m_sterile_cons
    print(f"  m_sterile={m_s_keV:4.1f} keV (DW): cluster-TG pack? YES (>>{m_TG_cluster:.0f}eV) | "
          f"dSph-TG: {'galaxy-EXCLUDED' if galaxy_excluded else 'galaxy-ALLOWED (could be galaxy DM)'} | "
          f"CMB/Lya cold? {'YES' if cmb_cold else 'NO (warm, below '+f'{m_sterile_cons:.1f}'+'keV floor)'}")

print(f"""
  KEY STRUCTURAL POINT (both ways):
  - A keV sterile is COLD ENOUGH for the CMB only if m_sterile(DW) >~ {m_sterile_cons:.0f} keV
    (== m_WDM,thermal >~ {m_WDM_cons:.0f} keV), per Lyman-alpha.  3.9 keV (the dSph-floor 'next calc'
    seed) is BELOW this and is WARM, in tension with Lyman-a; ~38 keV DW (==5 keV thermal)
    is the comfortable CMB-cold NON-RESONANT mass.
    BOTH-WAYS CAVEAT (do NOT overstate against keV): a RESONANTLY-produced (Shi-Fuller)
    sterile is COLDER than DW at the same mass, so a ~7 keV resonant sterile (the 3.5-keV-
    line candidate) can clear Lyman-alpha at a MUCH lower mass than the 38 keV DW number.
    So the CMB-cold WDM option is comfortably realizable at ~7 keV (resonant), NOT 38 keV.
    The point is unchanged: ~7 keV >> the dSph TG floor ({m_TG_dSph:.0f} eV) -> still NOT phase-space-
    galaxy-safe; CMB-coldness and eV-phase-space-galaxy-safety remain mutually exclusive.
  - BUT a keV sterile is FAR ABOVE the dSph TG floor ({m_TG_dSph:.0f} eV): TG NO LONGER excludes it
    from galaxies.  The galaxy-safety the eV cluster-fix bought from PHASE SPACE is LOST at
    keV.  A keV sterile is just standard (warm) CDM-like dark matter: it falls into galaxies
    like LCDM's DM.  It is galaxy-safe for MODIFIED-INERTIA only if its ABUNDANCE in galaxy
    halos is small AND its warm free-streaming keeps it diffuse -- i.e. it behaves like
    LCDM sub-dominant WDM, NOT like a phase-space-excluded eV species.
""")

# ===========================================================================
# SUMMARY TABLE — the two readings
# ===========================================================================
print("="*84)
print("SUMMARY — the eV reading vs the keV reading")
print("="*84)
print(f"""
                          | eV reading (Angus 11 eV)      | keV reading (~14 keV DW sterile)
  ------------------------+-------------------------------+--------------------------------
  cluster TG pack (>{m_TG_cluster:.0f}eV)  | YES                           | YES
  galaxy-safe via TG      | YES (phase-space excluded      | NO -- TG no longer excludes it
   (dSph floor ~{m_TG_dSph:.0f}eV)      |  from dwarfs, m<{m_TG_dSph:.0f}eV)         |  from galaxies (m>>{m_TG_dSph:.0f}eV)
  CMB acoustic peaks      | OK at the peaks (Angus2009     | YES (cold, clusters like CDM)
                          |  fits 1st-3rd; Omega~Omega_cdm)|
  small-scale P(k)/Lyman-a| NO -- FS over-erases P(k);     | YES (if >~14 keV DW == 5 keV
   (>~5 keV thermal)      |  Lya needs m_WDM>~5keV; +KATRIN/|  thermal; clears Lyman-a)
                          |  DESI/N_eff kill thermalized eV|
  ------------------------+-------------------------------+--------------------------------
  => one species does     | clusters + galaxy-safety +     | CMB(peaks+small-scale) +
     ...                   |  CMB PEAKS, but NOT small-scale|  clusters (LCDM-like WDM), but
                          |  P(k)/Lyman-a (and lab kills)  |  NOT phase-space galaxy-safe

  VERDICT: NO single mass threads all three of {{cluster-TG-pack, eV-phase-space-galaxy-
  -safety, CMB-cold}}.  The cluster-closure's galaxy-SAFETY mechanism (phase-space
  exclusion at eV) and the CMB-coldness requirement (keV) are at OPPOSITE ends of the
  mass axis, separated by ~{m_CMB_thermal_eV/window_hi:.0f}-{m_CMB_sterile_eV/window_hi:.0f}x.

  - If you pick the eV species (Angus cluster-fix): clusters + galaxy-safety YES, CMB NO.
  - If you pick the keV species (CMB-cold WDM):     CMB + clusters YES, but galaxy-safety
    is NO LONGER from phase space -- it is just LCDM-like (warm) dark matter that DOES
    fall into galaxies; the framework's "MOND replaces galaxy DM" then coexists with a
    keV WDM that is also present in galaxies (sub-dominant, warm), i.e. nuLCDM-like.

  => The honest reading is NOT "one Omega~0.25 species unifies clusters+CMB by phase
     space."  It is: the framework needs ~LCDM-amount of (galaxy-safe-by-abundance, keV
     warm) dark matter for CMB+clusters, RELOCATING not eliminating the dark sector --
     OR two components (eV-cluster + cold-CMB).  An Omega coincidence is NOT a unification.
""")
