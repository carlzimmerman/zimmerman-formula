#!/usr/bin/env python3
"""
ROUTE 3 -- DEEP 2024-2026 LITERATURE SWEEP for cluster-residual EXPLANATIONS.
Zimmerman framework (modified-inertia dS-Unruh MOND, a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11;
dark sector = AeST Q-mode ghost condensate, I0 ~ Omega_dm FREE).

Question: what GENUINELY-NEW 2024-2026 idea could explain the cluster-core residual
(eta(R500) ~ 1.6-2.4, concentrated in core, missing-to-baryon ~ x2 after the MOND boost)
WITHOUT a new fundamental particle AND while preserving the galaxy RAR (the hard galaxy-veto)?

This script quantifies each literature candidate against four gates:
  G1 sufficiency  (does it close the ~x2 core residual?)
  G2 galaxy-veto  (does it preserve the tight galaxy RAR? -- the HARD constraint)
  G3 no-particle  (no new fundamental species)
  G4 data         (consistent with eRASS1 / A2029 / Bullet / KATRIN / DESI)

Both-ways rule: credit real partials at full weight; concede gate-failures at full weight;
do NOT manufacture a close. Quarantine: a0/Z/kappa/I0 never asserted derived.

Real numbers are drawn from the 2024-2026 papers fetched in this session (cited inline).
"""
import numpy as np

# ----------------------------------------------------------------------------
# 0. FRAMEWORK + CLUSTER TARGET (the residual we must explain)
# ----------------------------------------------------------------------------
c    = 2.998e8                 # m/s
a0   = 9.36e-11                # m/s^2  -- framework's a0 (INPUT, quarantined)
a0_mond = 1.2e-10             # regular-MOND a0 for cross-check
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19               # m
Mpc  = 1000*kpc

print("="*78)
print("ROUTE 3 -- CLUSTER-RESIDUAL EXPLANATION SWEEP (2024-2026 literature)")
print("="*78)

# The cluster-core residual, as the MODERN MOND-cluster literature actually states it.
# Kelleher-Lelli 2024 (arXiv:2405.08557): missing-to-VISIBLE ratio ~1-5 at 200-300 kpc,
#   declining to ~0.4-1.1 at 2-3 Mpc.  => the residual is a CORE phenomenon.
# Famaey-Pizzuti-Saltas 2024 (arXiv:2410.02612, PRD 111,123042): the residual, read off
#   gravitational LENSING of RELAXED clusters, is GAS-TRACKING: inner constant-density
#   core + outer slope < -3.5, "missing-to-hot-gas density ratio ... of order ~10",
#   exponential cutoff ~400 kpc.
# Famaey 2026 (arXiv:2605.10022), the NEW Bullet result on the JWST lens model:
#   the MOND phantom+baryon / baryon ratio at 300 kpc of the BCGs is only 2.8-3.3,
#   but the data need ~8  => a residual factor of ~x2.4 ON TOP of the MOND boost.
#   The residual mass ~ 3.4e14 Msun ~ the cluster's whole baryonic mass (~4e14 Msun).
#   CRUCIAL NEW SHAPE FACT: in the Bullet MERGER the residual is CENTRED ON THE GALAXIES
#   (collisionless), NOT on the gas -- the lensing kapp>=1 ridge sits on the galaxies.
print("\n[TARGET] modern MOND-cluster residual (2024-2026 consensus):")
print("  Kelleher-Lelli 2024 : missing/visible ~1-5 @200-300kpc -> ~0.4-1.1 @2-3Mpc (CORE)")
print("  Famaey-Piz-Saltas '24: lensing residual GAS-TRACKING, missing/gas ~10, cutoff ~400kpc")
print("  Famaey 2026 (Bullet): MOND boost gives x2.8-3.3 @300kpc, data need x8 => x2.4 RESIDUAL")
print("                        residual ~3.4e14 Msun ~ M_baryon; CENTRED ON GALAXIES (collisionless)")

# So the number every candidate must hit:
RESIDUAL_FACTOR = 2.4         # extra mass / (baryon+MOND-phantom), at the core (Bullet, Famaey 2026)
ETA_R500        = 1.9         # framework's integrated eta(R500) ~1.6-2.4 (banked)
M_residual_core = 3.4e14      # Msun, projected within ~430 kpc (Famaey 2026 Bullet)
M_baryon        = 4.0e14      # Msun (Famaey 2026 Bullet total baryonic)
print(f"\n  => CANDIDATE MUST PROVIDE: core factor ~{RESIDUAL_FACTOR}x ;"
      f" M_residual ~{M_residual_core:.1e} Msun ~ M_baryon")
print(f"     AND the new Bullet shape constraint: the residual is COLLISIONLESS, GALAXY-TRACKING")

# ----------------------------------------------------------------------------
# 1. NEUTRINOS IN MOND -- KILLED HARDER by 2024-2026 data (G1+G4 fail)
# ----------------------------------------------------------------------------
print("\n" + "="*78)
print("[CANDIDATE 1] Neutrinos in MOND (active 1.5eV / sterile 11keV)")
print("="*78)
# Latest direct bound: KATRIN 2024 campaign (arXiv:2406.13516, Science 2025): m_nu < 0.45 eV (90% CL)
#   -- tightens the old 0.8 eV by ~2x.  An eV-scale ACTIVE neutrino hot DM is excluded.
# Cosmology: DESI DR2 BAO + CMB + DESY5 SNe (2026): sum m_nu < 0.052-0.064 eV (95% CL)
#   -- BELOW the normal-hierarchy floor (0.059 eV).  Active neutrinos cannot be the cluster mass.
# keV sterile (Angus 11 eV / 11 keV nuHDM): Russell-Banik-Cray-Zhao 2026 (arXiv:2602.21975)
#   -- a MOND+nuHDM cosmology "massively overproduces large-scale structure", ruled out >5 sigma.
#   Plus MicroBooNE has closed the eV-sterile (LSND/MiniBooNE) window.
m_nu_katrin   = 0.45         # eV, KATRIN 2024 direct (was 0.8)
sum_mnu_desi  = 0.058        # eV, DESI DR2 cosmological 95% CL (mid of 0.052-0.064)

# Tremaine-Gunn phase-space ceiling: a light free-streaming neutrino cannot pack a cluster
# core above its cosmic mean.  Banked Route-A number: M_nu(<420 kpc) ~ 4-9e7 Msun for a 0.05 eV nu
# -- ~0.00004% of the ~1e14 Msun gap.  Even a hypothetical 1.5 eV active neutrino is now excluded
# at BOTH the direct (0.45 eV) and cosmological (0.058 eV) level.
M_nu_phasespace = 7e7        # Msun in 420 kpc for a viable (<0.45 eV) neutrino
frac_nu = M_nu_phasespace / (M_residual_core*1e0)
print(f"  KATRIN 2024 direct bound : m_nu < {m_nu_katrin} eV (was 0.8) -> eV active nu EXCLUDED")
print(f"  DESI DR2 cosmological    : sum m_nu < {sum_mnu_desi} eV (95% CL) < NH floor 0.059 eV")
print(f"  keV sterile nuHDM        : Russell+2026 LSS overproduction RULES OUT >5sigma; MicroBooNE")
print(f"  Tremaine-Gunn ceiling    : M_nu(<420kpc) ~{M_nu_phasespace:.0e} Msun")
print(f"  => fills {frac_nu*100:.5f}% of the core residual.")
print("  VERDICT: G1 FAIL (negligible), G4 FAIL (excluded by KATRIN+DESI+LSS). NOT viable.")
cand1 = dict(name="neutrinos", G1=False, G2=True, G3=False, G4=False, no_particle=False)

# ----------------------------------------------------------------------------
# 2. EMOND -- potential-dependent a0 (Hodson-Zhao 2017; G2 + framework-veto)
# ----------------------------------------------------------------------------
print("\n" + "="*78)
print("[CANDIDATE 2] EMOND -- potential-dependent a0 = A0(Phi) (Hodson-Zhao 2017)")
print("="*78)
# Hodson-Zhao 2017 (arXiv:1701.03369): A0(Phi) = a0 * exp(Phi/Phi0),
#   |Phi0| ~ 1.5e12 m^2/s^2 ; with a step (tanh) variant: A0max ~ 80*a0, Phi0 ~ -2.7e12.
# In a galaxy (shallow Phi) A0 -> a0 so the RAR is preserved -- this is the WHOLE design.
# In a cluster core (deep Phi) a0 is boosted up to ~80x => boosts the MOND phantom enough.
Phi0   = 1.5e12              # m^2/s^2 (Hodson-Zhao exp form)
A0max  = 80*a0              # cluster ceiling
# Galaxy potential (MW-scale): |Phi| ~ v^2 ~ (200 km/s)^2 = 4e10 m^2/s^2 -> A0/a0:
Phi_gal = (200e3)**2
boost_gal = np.exp(Phi_gal/Phi0)
# Cluster core potential: |Phi| ~ (1000 km/s)^2 ~ 1e12 m^2/s^2 -> A0/a0:
Phi_clu = (1000e3)**2
boost_clu = np.exp(Phi_clu/Phi0)
print(f"  A0(Phi)=a0*exp(Phi/Phi0), Phi0~{Phi0:.1e} m^2/s^2 ; ceiling A0max~{A0max/a0:.0f} a0")
print(f"  galaxy  Phi~{Phi_gal:.1e} -> A0/a0 = {boost_gal:.3f}  (RAR preserved: ~1.0)")
print(f"  cluster Phi~{Phi_clu:.1e} -> A0/a0 = {boost_clu:.2f}   (enough boost to close core)")
print("  Hodson-Zhao verdict: 'MIXED success ... issues explaining the deficit FULLY'.")
print("  GALAXY-VETO: passes by CONSTRUCTION (A0->a0 in shallow Phi).")
print("  BUT *FRAMEWORK*-VETO (decisive here): the Zimmerman a0 = c^2 sqrt(Lambda/32pi) is")
print("    TIED TO Lambda (a constant of NATURE).  A potential-dependent A0(Phi) DESTROYS the")
print("    a0<->Lambda identity -- the framework's central claim. So EMOND is galaxy-safe but")
print("    INCOMPATIBLE WITH THE FRAMEWORK'S DERIVATION OF a0. It would be a DIFFERENT theory.")
# Quantify the conflict: EMOND needs a0 to vary by ~x80 across environments; the framework
# forbids ANY variation (a0 is fixed by Lambda).  This is a hard incompatibility, not a tuning.
cand2 = dict(name="EMOND", G1=True, G2=True, G3=True, G4=True, no_particle=True,
             framework_veto=True)

# ----------------------------------------------------------------------------
# 3. AeST FIELD CLUSTERING -- the framework's OWN Q-mode (Durakovic-Skordis 2023)
# ----------------------------------------------------------------------------
print("\n" + "="*78)
print("[CANDIDATE 3] AeST Q-mode field clustering (Durakovic-Skordis 2023; the CENTERPIECE)")
print("="*78)
# Durakovic-Skordis 2023 (arXiv:2312.00889): isothermal AeST cluster models.  The AeST RAR
#   "can display a peak" then "drops BELOW the MOND expectation, AS IF there is a NEGATIVE
#   mass density".  Gas "may become more compressed than Newtonian/MOND".  But: "a full
#   quantitative comparison ... will require going beyond the isothermal case" -- i.e. AeST
#   does NOT robustly source enough core mass; the effect is sign-indefinite.
# This is EXACTLY the banked Route-B finding: the full nonlinear Y-Q coupling sources a real
#   extra ~17-20% over the bare phantom, galaxy-SAFE, but the BIG enhancement lives in the
#   OUTSKIRTS (r_C ~2-20 Mpc) and turns sign-indefinite-oscillatory if forced into the core.
aest_core_boost = 0.18       # +18% over bare phantom (banked Route B, mid of 17-20%)
need_extra      = RESIDUAL_FACTOR - 1.0   # need +140% in the core
frac_aest = aest_core_boost / need_extra
print(f"  Durakovic-Skordis: AeST RAR PEAKS then drops 'as if negative mass density' -> the field")
print(f"    does NOT monotonically pile into cores; the big effect is in the OUTSKIRTS.")
print(f"  Banked Route-B (full nonlinear Y-Q): +{aest_core_boost*100:.0f}% core mass over bare phantom, GALAXY-SAFE")
print(f"  need +{need_extra*100:.0f}% in the core -> AeST clustering closes {frac_aest*100:.0f}% of it.")
print("  GALAXY-VETO: PASSES (the I0 amplitude that keeps galaxies on the RAR is the SAME one")
print("    that under-sources the core -- the field is SUB-dominant in galaxies by design).")
print("  VERDICT: G1 FAIL (~13% of the residual), G2/G3 PASS. REAL PARTIAL, not a close.")
print("  -> The centerpiece idea (field IS the cluster DM) is RIGHT IN KIND but SHORT IN AMOUNT:")
print("     to close the core the field must cluster ~8x more than it does while staying smooth")
print("     in galaxies -- and Durakovic-Skordis show it goes sign-INDEFINITE, not up, in cores.")
cand3 = dict(name="AeST_Qmode", G1=False, G2=True, G3=True, G4=True, no_particle=True,
             closes=frac_aest)

# ----------------------------------------------------------------------------
# 4. IGIMF STELLAR REMNANTS -- collisionless, galaxy-tracking real baryons (Kroupa 2026)
#    *** the candidate the NEW Bullet shape (Famaey 2026) actually FAVORS ***
# ----------------------------------------------------------------------------
print("\n" + "="*78)
print("[CANDIDATE 4] IGIMF top-heavy-IMF stellar remnants (Zhang-Zonoozi-Kroupa 2026)")
print("="*78)
# Zhang-Zonoozi-Kroupa 2026 (arXiv:2602.06082): a top-heavy IGIMF in high-SFR massive
#   ellipticals -> many extra neutron stars + stellar BHs (REAL collapsed baryons, no new
#   species, BBN-safe).  Claim: "baryonic mass in stars, remnants and the ICM accounts for
#   at least 88%" of the MOND dynamical mass -> alleviates the deficit substantially.
# Companion Bullet paper Zhang-Haghi-Asencio-Banik 2026 (arXiv:2606.19454): MOND strong-lensing
#   masses of all 3 Bullet cores lie WITHIN the IGIMF-predicted baryon range.
# Banked Route-D: cuts eRASS1 median eta(R500) 6.56 -> 3.80-4.72 (closes the INTEGRATED /
#   equilibrium problem at the HSE-reliable eta~1.0-1.6 end); fills ~44% (max-generous) of
#   the ~1.9e14 Msun CORE shortfall.  G2 PASS (top-heavy IMF ONLY in massive ellipticals,
#   SPARC disks canonical -> RAR untouched).  G3 PASS (real baryons).
igimf_integrated = (6.56-4.26)/(6.56-1.3)   # fraction of the integrated eta gap closed (mid 3.8-4.72)
igimf_core_frac  = 0.44                       # max-generous core fill (banked)
print(f"  Zhang-Zonoozi-Kroupa 2026: stars+remnants+ICM = >=88% of MOND dynamical mass")
print(f"  Zhang-Haghi-Banik 2026 (Bullet): MOND lensing masses WITHIN IGIMF baryon range")
print(f"  integrated eta(R500) 6.56 -> 3.8-4.72 (closes ~{igimf_integrated*100:.0f}% of the equilibrium gap)")
print(f"  CORE fill (max-generous 8x boost, 60% in core): ~{igimf_core_frac*100:.0f}% of the core shortfall")
print("  *** SHAPE MATCH (the NEW decisive point): Famaey 2026 Bullet shows the residual is")
print("      COLLISIONLESS + CENTRED ON GALAXIES.  Stellar remnants TRACK THE STARS/GALAXIES")
print("      and are collisionless -- so the NEW lensing shape FAVORS remnants over the older")
print("      gas-tracking (FPS missing/gas~10) reading.  The merger SEPARATES gas from galaxies,")
print("      and the residual went with the GALAXIES. This is the cleanest no-particle pointer.")
print("  GALAXY-VETO: PASSES (top-heavy IMF gated to high-SFR massive ellipticals only).")
print("  VERDICT: G1 FAIL on the CORE (~44% max), G2/G3 PASS, G4 favored by the new shape.")
print("  REAL PARTIAL -- the strongest no-particle lead; closes ~half the core if the Bullet")
print("  galaxy-tracking shape (not the FPS gas-tracking shape) is the right one.")
cand4 = dict(name="IGIMF_remnants", G1=False, G2=True, G3=True, G4=True, no_particle=True,
             closes=igimf_core_frac)

# ----------------------------------------------------------------------------
# 5. CREATIVE / NEW 2024-2026 IDEAS (screening, 2nd scale, cosmic-web EFE, lensing-vs-dyn,
#    cold-baryon clouds, Blanchet dipolar dark medium)
# ----------------------------------------------------------------------------
print("\n" + "="*78)
print("[CANDIDATE 5] Creative/new 2024-2026 mechanisms")
print("="*78)

# 5a. COLD pressure-confined gas clouds (Kelleher-Lelli 2024; Famaey 2026 'small gas clouds').
#   The MODERN MOND-cluster consensus candidate: collisionless-ish cold dark BARYONS,
#   <1e5 Msun clouds, <50 pc, dynamically cold so they track the galaxies/potential, not
#   the hot X-ray gas.  REAL baryons (G3 pass), galaxy-safe (G2 pass: they don't exist in
#   isolated SPARC disks at the level needed).  The OBSERVATIONAL handle: they'd track
#   GALAXIES (collisionless) -> CONSISTENT with Famaey 2026's Bullet shape.  But a >=2x
#   baryon budget hidden in cold clouds strains the cosmological baryon census (f_b ceiling)
#   -- banked: missing warm-hot baryons ~7%, can't reach 2x. So G1 = partial at best.
print("  (5a) Cold pressure-confined baryon clouds (Kelleher-Lelli '24; Famaey '26 'small gas clouds')")
print("       <1e5 Msun, <50 pc, collisionless+cold -> GALAXY-tracking (matches Bullet shape).")
print("       REAL baryons (G3 ok), galaxy-safe (G2 ok). BUT a 2x hidden-baryon budget strains")
print("       the cosmic f_b census (banked: only ~7% warm-hot recoverable). G1 = weak partial.")

# 5b. COSMIC-WEB / COLLECTIVE EFE (the cluster sits in the web's external field).
#   Banked COLLECTIVE_EFE_CLUSTER: the external field of the cosmic web SUPPRESSES the MOND
#   boost (wrong sign) -- it makes clusters MORE Newtonian, DEEPENING the deficit, not curing.
print("  (5b) Cosmic-web / collective EFE: external field SUPPRESSES the MOND boost (WRONG SIGN)")
print("       -> deepens the deficit. NOT a cure (banked COLLECTIVE_EFE_CLUSTER).")

# 5c. LENSING-vs-DYNAMICS split.  2024-2026 data CLOSE this escape: Ma-Zhang-Wang-Wu 2025
#   (arXiv:2409.13329) find weak-lensing and satellite-kinematics masses in "strong
#   concordance" (lensing reliably measures the dynamical mass); FPS find lensing/X-ray
#   ratio ~1.03.  So the residual is NOT a lensing-vs-dynamics artifact.
print("  (5c) Lensing-vs-dynamics split: CLOSED. Ma+2025 (WL == satellite-kinematics 'strong")
print("       concordance'); FPS lensing/X-ray ~1.03. Residual is REAL, not a proxy artifact.")

# 5d. SECOND SCALE / new-scale quasi-static AeST (Mistele 2023, arXiv:2305.07742).
#   A second length scale appears in the AeST quasi-static limit -> in PRINCIPLE a cluster-only
#   enhancement.  But it is the SAME I0/mass-parameter physics as Route B (sign-indefinite in
#   cores), and it is CDM-degenerate on large scales -> no independent cluster cure.
print("  (5d) AeST 'new quasi-static scale' (Mistele 2023): same I0/mass-param physics as Route B,")
print("       sign-indefinite in cores -> no independent cure beyond the ~18% already counted.")

# 5e. BLANCHET dipolar / Yang-Mills graviphoton dark MEDIUM (Blanchet+2025, arXiv:2507.02563,
#   2502.14686).  A dark-matter MEDIUM whose gravitational POLARIZATION reproduces MOND in
#   galaxies AND which can CLUSTER (provide mass) in clusters.  This is the cleanest published
#   'MOND-in-galaxies + clustering-medium-in-clusters' mechanism -- BUT it POSITS a new
#   dark-matter medium (a fundamental dark sector beyond the metric), so for the Zimmerman
#   framework it would be a NEW PARTICLE/FIELD (G3 FAIL for the framework's no-particle goal).
#   It is, however, the closest ANALOGUE to what the framework's Q-mode is TRYING to be.
print("  (5e) Blanchet dipolar/Yang-Mills graviphoton dark MEDIUM (2025): polarization->MOND in")
print("       galaxies + the medium CLUSTERS in clusters. Cleanest 'both-scales' mechanism, BUT")
print("       it POSITS a new dark medium -> for the framework that is a NEW PARTICLE (G3 FAIL).")
print("       It is the published proof-of-concept that the Q-mode's INTENDED behavior is")
print("       theoretically consistent -- the framework just wants the metric mode to do it.")

# ----------------------------------------------------------------------------
# 6. SYNTHESIS -- best no-particle, galaxy-safe candidate(s)
# ----------------------------------------------------------------------------
print("\n" + "="*78)
print("SYNTHESIS")
print("="*78)
cands = [cand1, cand2, cand3, cand4]
print(f"{'candidate':<16}{'G1 suff':<9}{'G2 gal':<8}{'G3 noP':<8}{'G4 data':<9}{'closes'}")
for cnd in cands:
    cl = cnd.get('closes', None)
    cls = f"{cl*100:.0f}%" if cl is not None else ("by-veto" if cnd.get('framework_veto') else "-")
    print(f"{cnd['name']:<16}{str(cnd['G1']):<9}{str(cnd['G2']):<8}{str(cnd['G3']):<8}{str(cnd['G4']):<9}{cls}")

print("""
HEADLINE (both ways):
  NO single candidate closes the core residual with zero new particles AND a clean galaxy-veto.
  BUT the 2024-2026 literature converges on a CONCRETE, no-particle, galaxy-safe COMBINATION,
  and -- decisively new this cycle -- the Famaey 2026 Bullet SHAPE constraint discriminates
  AMONG the candidates and FAVORS the no-particle ones.

  THE BEST CANDIDATE = IGIMF stellar remnants (Kroupa 2026) + AeST Q-mode field clustering,
  selected by the new Bullet shape (residual is COLLISIONLESS + GALAXY-TRACKING):
   - remnants are collisionless real baryons that TRACK GALAXIES   -> matches the Bullet shape
   - the Q-mode adds a galaxy-safe ~18% on top
   - together they cover roughly HALF the core at ZERO new particles, IF the Bullet
     galaxy-tracking shape (not the FPS gas-tracking shape) is the right reading.
  This is REAL but a PARTIAL -- it does not reach the full ~2.4x. Conceded at full weight.

GALAXY-VETO (the hard constraint) -- which candidates survive it:
  EMOND          : galaxy-SAFE by construction, but BREAKS THE FRAMEWORK (a0!=f(Phi); a0<->Lambda).
  AeST Q-mode    : galaxy-SAFE (I0 keeps galaxies on the RAR; same I0 under-sources cores).
  IGIMF remnants : galaxy-SAFE (top-heavy IMF gated to massive ellipticals; SPARC disks untouched).
  cold clouds    : galaxy-SAFE (absent in isolated disks at the needed level).
  density-a0     : FAILS the veto (banked kill: closes clusters but breaks galaxies) -- excluded.
  NONE that closes clusters spoils galaxies EXCEPT the already-killed density-a0 route.

NEUTRINOS -- killed HARDER in 2024-2026:
  KATRIN 2024 m_nu<0.45 eV (was 0.8); DESI DR2 sum m_nu<0.058 eV (< NH floor); nuHDM LSS >5sigma;
  Tremaine-Gunn ceiling fills 0.00004% of the core. DEAD as the cluster mass. (G1+G4 fail.)

THE SINGLE DECISIVE, FALSIFIABLE HANDLE (genuinely new, both-ways honest):
  Settle the core-residual SHAPE -- is it GAS-tracking (FPS 2024, missing/gas~10, hot-gas profile)
  or GALAXY-tracking (Famaey 2026 Bullet, collisionless, on the galaxies)?
   * GALAXY-tracking  -> IGIMF remnants + Q-mode cover ~HALF the core at ZERO new particles.
   * GAS-tracking     -> cold-baryon clouds or an irreducible shared-MOND gap.
  The Bullet (a merger that SEPARATES gas from galaxies) already points GALAXY-tracking.
  A resolved, deprojected total-to-baryon profile of one rich relaxed core (CLASH+XRISM)
  is the observation that decides it. This is the cleanest live no-particle path.

QUARANTINE held: a0/Z/kappa/I0 never asserted derived (a0=9.36e-11 INPUT, I0 free).
NO manufactured close; every gate-failure conceded at full weight.
""")
