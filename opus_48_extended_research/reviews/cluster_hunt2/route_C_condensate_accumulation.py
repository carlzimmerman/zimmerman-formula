#!/usr/bin/env python3
"""
ROUTE C -- ghost-condensate ACCUMULATION in deep cluster cores.

The deepest no-particle route: "dark matter is my field, and it piles into clusters."

The framework's dark sector IS a ghost condensate (AeST: K(Q)=mu^2(Q-1)^2; the
Q-mode off the minimum -> w=0 cold a^-3 dust = "Ghost Dark Matter", Furukawa-
Yokoyama-Ichiki-Sugiyama-Mukohyama arXiv:1001.4634, ACLM hep-th/0312099).

THE ROUTE C QUESTION (both ways): does the condensate dust accumulate NONLINEARLY
in deep cluster cores -- supplying the EXTRA core mass (~10x-gas) that smooth
CDM-at-cosmic-share cannot -- WITHOUT breaking galaxies?

Three sub-mechanisms named in the route:
  (i)   chameleon-like / accretion enhancement (condensate response to deep potential)
  (ii)  Q-mode sourced by the strong Y-mode (MOND) gradient
  (iii) ghost-condensate accretion onto massive bodies (ACLM Sec 6 / Mukohyama 2005)

GATES (both-ways, all four):
  G1 SUFFICIENCY  -- closes the ~4.4x core undershoot / ~2.3e14 Msun core target at a0=9.36e-11
  G2 GALAXY-VETO  -- does NOT break SPARC RAR/BTFR (<~0.13 dex scatter)
  G3 NO-NEW-PARTICLE -- framework's OWN field or KNOWN physics, not a new species
  G4 DATA         -- survives eRASS1/CLASH/XRISM/Lyman-alpha/X-ray

LITERATURE PHYSICS (extracted verbatim this session from the primary PDFs):
  * Ghost Dark Matter sound speed (Eq 3.7, 4.7):  c_s^2 = (X-M^4)/(3X-M^4) ~ (X-M^4)/(2 M^4)
    -> near the attractor c_s^2 ~ rho_gdm / (2 Mbar^4), i.e. c_s^2 GROWS WITH DENSITY.
  * Jeans wavenumber (Eq 4.1):  k_J = sqrt(3/2) * aH / c_s
  * k_J,eq = 1 * (Omega_gdm h^2/0.11)^(-5/6) * (M/10eV)^(4/3) Mpc^-1  (Eq 4.2)
  * LSS bound: M >~ 10 eV (else matter power spectrum suppressed below k~1 Mpc^-1).
  * Mukohyama hep-th/0502189: accretion onto a BH is "pressure-less dust", geodesic,
    NEGLIGIBLE late-time dM/dt if the cosmic density is small; NO chameleon enhancement.
  * ACLM hep-th/0312099 Sec 6: pi-response to a static source -> oscillatory potential
    at r > r_c = M_Pl/M^2, onset time t_c = M_Pl^2/M^3; static-source limit valid only
    on tau >~ M r^2.  No density pile-up.

This script computes, with REAL numbers, whether each sub-mechanism supplies the
core target -- and what each does to galaxies.
"""
import numpy as np

print("="*78)
print("ROUTE C -- GHOST-CONDENSATE ACCUMULATION IN CLUSTER CORES")
print("="*78)

# ---------------------------------------------------------------------------
# Constants (SI + convenient astro units)
# ---------------------------------------------------------------------------
G      = 6.674e-11           # m^3 kg^-1 s^-2
c      = 2.998e8            # m/s
hbar   = 1.055e-34          # J s
kB     = 1.381e-23          # J/K
Msun   = 1.989e30          # kg
kpc    = 3.086e19          # m
Mpc    = 3.086e22          # m
eV     = 1.602e-19         # J
eV_kg  = eV / c**2          # kg per eV/c^2
yr     = 3.156e7           # s
Gyr    = 1e9 * yr

# Cosmology / framework
H0     = 2.20e-18          # s^-1  (67.7 km/s/Mpc)
h      = 0.677
Om     = 0.31
OL     = 0.69
Odm    = 0.266
Ob     = 0.049
a0_fw  = 9.36e-11          # m/s^2  framework a0 = c^2 sqrt(Lambda/32pi)
M_Pl   = np.sqrt(hbar*c/(8*np.pi*G))   # reduced Planck mass in kg... careful: use energy
# Reduced Planck ENERGY:
E_Pl   = np.sqrt(hbar*c**5/(8*np.pi*G)) / eV   # in eV
print(f"\nReduced Planck energy M_Pl = {E_Pl:.3e} eV = {E_Pl/1e9:.3e} GeV")

# ---------------------------------------------------------------------------
# THE TARGET (banked, from eRASS1 + CLASH/FPS)
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("THE CORE TARGET (banked eRASS1/CLASH)")
print("-"*78)
M_core_target = 2.3e14      # Msun missing inside ~420 kpc (rich cluster)
R_core        = 420.0       # kpc
M_phantom_MI  = 4.0e13      # Msun the framework MI phantom supplies inside ~450 kpc (CLASH script)
# Banked CLASH core-avg undershoot = 4.42x (100-450 kpc integral, CLASH_TARGET_RESULT);
# the simple 1.47e14/4.0e13 = 3.67x is the matched-anchor ratio. Report the banked 4.42x.
undershoot    = 4.42        # core-avg, banked (CLASH 1.47e14 vs MI 4.0e13 over 100-450 kpc)
print(f"Core missing mass target (<420 kpc, rich) : {M_core_target:.2e} Msun")
print(f"Framework MI phantom supplies (<450 kpc)   : {M_phantom_MI:.2e} Msun")
print(f"Core-avg undershoot factor (banked CLASH)  : ~{undershoot:.2f}x")
print(f"EXTRA mass Route C must supply              : ~{M_core_target - 0.4e14:.2e} Msun")
print("FPS residual: rho_dM = eta * rho_gas * exp(-lambda r/r0), eta~10, r0~450 kpc")
print("  -> the residual TRACKS THE GAS (cored, gas-shaped), NOT a smooth NFW halo.")

# ---------------------------------------------------------------------------
# MECHANISM (iii) + (i):  ACCRETION / CHAMELEON enhancement in the core
#   Does the condensate energy density pile up in a deep potential?
# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("MECHANISM (i)+(iii):  does the condensate DENSITY pile up in the core?")
print("="*78)
print("""
Mukohyama (hep-th/0502189): the condensate accretes onto a massive body LIKE
PRESSURE-LESS DUST, following geodesics; the late-time dM/dt is NEGLIGIBLE if the
cosmic density is small.  There is NO chameleon/screening enhancement: the field
has a SHIFT symmetry (no potential V(phi)), so there is no density-dependent
effective mass to drive a chameleon overdensity.  The only "response" to a source
is the ACLM oscillatory pi-wake at r > r_c = M_Pl/M^2, onset t_c = M_Pl^2/M^3.
""")

# accretion enhancement: the dust accretes onto the cluster GRAVITATIONALLY, exactly
# like CDM -- there is no EXTRA chameleon boost. So the question reduces to: does it
# cluster like CDM (mechanism via gravity), bounded by the Jeans/sound-speed scale.

# r_c and t_c at the framework's clustering scale M (set by mu^-1 ~ 1 Mpc <-> M~0.15 eV)
# but Ghost-DM LSS demands M >~ 10 eV.  Compute both.
def rc_tc(M_eV):
    M4 = M_eV  # eV
    r_c = (E_Pl / M_eV**2)            # in units where length ~ 1/energy; convert
    # r_c = M_Pl/M^2 as a LENGTH = hbar c /(M^2/M_Pl) ... do it in SI:
    M_J  = M_eV * eV                  # J
    MPl_J= E_Pl * eV                  # J
    r_c_m = hbar*c * MPl_J / M_J**2   # m   (= M_Pl/M^2 in natural units, restored)
    t_c_s = hbar * MPl_J**2 / M_J**3  # s
    return r_c_m/kpc, t_c_s/Gyr

for M_eV in [0.15, 10.0, 1e3]:
    r_c_kpc, t_c_Gyr = rc_tc(M_eV)
    print(f"  M={M_eV:>8.2f} eV :  r_c (osc. onset) = {r_c_kpc:.2e} kpc ,  t_c = {t_c_Gyr:.2e} Gyr")

print("""
READ: at the AeST clustering scale (M~0.15 eV) r_c ~ Mpc and t_c >> age, so the
oscillatory pi-wake is pushed to cluster-OUTSKIRTS / never-onset -- the SAME banked
result (antigravity beyond galaxies).  At the LSS-required M>~10 eV the onset is at
r_c << kpc but t_c is still cosmological -- accretion stays dust-like.
NEITHER gives a density ENHANCEMENT in the core.  Mechanism (i)+(iii) = NULL
(benign, no pile-up beyond ordinary gravitational infall).  Matches banked.
""")

# ---------------------------------------------------------------------------
# MECHANISM (via gravity):  the dust clusters like CDM -- bounded by the Jeans scale.
#   c_s^2 GROWS WITH DENSITY -> the LOCAL Jeans scale GROWS in the core.
# ---------------------------------------------------------------------------
print("="*78)
print("THE DUST CLUSTERS LIKE CDM -- but the SOUND SPEED grows with density")
print("="*78)
print("""
Ghost Dark Matter (Furukawa+ 1001.4634): the w=0 dust clusters gravitationally like
CDM ABOVE the Jeans scale; below it the sound speed suppresses collapse.
Crucially  c_s^2 ~ rho_gdm/(2 Mbar^4)  -- the sound speed GROWS with local density.
So in a DEEP, DENSE cluster core the local Jeans scale is LARGER, not smaller:
the field RESISTS piling into the core.  This is the OPPOSITE of a chameleon.
""")

# Jeans wavenumber at equality (Eq 4.2): k_J,eq = 1 * (Om_gdm h^2/0.11)^(-5/6) (M/10eV)^(4/3) Mpc^-1
def kJ_eq(M_eV, Omgdm_h2=Odm*h**2):
    return 1.0 * (Omgdm_h2/0.11)**(-5/6) * (M_eV/10.0)**(4/3)   # Mpc^-1

print("Jeans wavenumber at matter-radiation equality (largest comoving Jeans scale):")
for M_eV in [0.15, 1.0, 10.0, 100.0, 1e3]:
    kJ = kJ_eq(M_eV)
    lamJ = 1.0/kJ  # Mpc comoving
    print(f"  M={M_eV:>8.2f} eV :  k_J,eq = {kJ:.3e} Mpc^-1 ,  lambda_J,eq = {lamJ:.3e} Mpc (comoving)")

print("""
The LSS bound M >~ 10 eV is EXACTLY the statement that k_J,eq must be >~ 1 Mpc^-1
so the matter power spectrum is unsuppressed (CDM-like) down to k~1 Mpc^-1.
For M >~ 10 eV the dust clusters like CDM on ALL scales relevant to clusters
(k_J,eq >~ 1 Mpc^-1 -> sub-Mpc cores are well above the Jeans scale, CDM-like).
""")

# ---------------------------------------------------------------------------
# So: WITH M >~ 10 eV (forced by LSS), the dust clusters EXACTLY like CDM.
#   Then Route C reduces to:  can a CDM-like component (the framework's own field)
#   supply the core target WITHOUT breaking galaxies?
#   The amount I0 is FREE -> set it to whatever clusters need.  The catch = G2.
# ---------------------------------------------------------------------------
print("="*78)
print("THE CRUX:  a CDM-like field that closes clusters also makes GALAXY halos")
print("="*78)
print("""
With M>~10 eV the Q-mode dust IS dynamically identical to CDM (zero c_s on cluster
scales, w=0, clusters via gravity).  Its amount I0 ~ Omega_dm is a FREE shift charge
(banked: d rho_dust/d Lambda = 0; pinned only by initial conditions) -- so one is
FREE to set the cluster-core abundance to the target.  Route C's hope: put the
field where clusters need it.

But a CDM-like field clusters by the SAME gravitational instability everywhere.
The reason MOND/AeST fits SPARC galaxies WITHOUT a halo is that there is NO
clustered cold component in galaxies.  If the framework's own field clusters like
CDM into cluster cores, the SAME field clusters into GALAXY halos -- and that is
exactly the CDM halo MOND was built to avoid.  This is the G2 galaxy veto.
""")

# ---------------------------------------------------------------------------
# G2 quantitative:  if the field supplies the cluster core target as a CDM-like
#   component, what does the SAME cosmological abundance do to a SPARC galaxy?
# ---------------------------------------------------------------------------
print("-"*78)
print("G2 GALAXY VETO -- the field-as-CDM on SPARC galaxies (quantitative)")
print("-"*78)

# The cluster core needs missing/baryon ~ 10 (FPS eta~10, gas-tracking).
# A CDM-like field that supplies ratio ~10 in cluster cores: what halo:disk ratio
# does the SAME physics give on a galaxy?  CDM-like clustering does NOT key on
# acceleration -- it keys on the cosmic baryon:DM ratio Omega_dm/Omega_b ~ 5.4 and
# the collapse/concentration.  On galaxies the observed RAR has NO room for a
# clustered cold component: the SPARC baryons ALONE (via MOND) fit the curves.

ratio_cosmic = Odm/Ob
print(f"Cosmic Omega_dm/Omega_b = {ratio_cosmic:.2f}  (a CDM-like field tracks this on collapsed scales)")
print(f"Cluster FPS missing/gas  ~ 10            (the field would need to OVER-concentrate ~2x cosmic in cores)")
print("""
A CDM-like field at the cosmic abundance Omega_dm=0.266 produces, on a galaxy, the
SAME dark-to-baryon ratio that LCDM does (~5-10x within the optical radius after
collapse/concentration).  But the SPARC RAR is fit by the BARYONS ALONE through
MOND with ZERO clustered dark component -- adding a CDM-like halo of the field at
even a fraction of the cosmic share DOUBLE-COUNTS: MOND already boosts g, and an
extra cold halo adds MORE.  This is the textbook MOND+CDM incompatibility.
""")

# Quantify the RAR damage: a CDM-like field halo adds g_halo on top of the MOND g.
# Use a representative SPARC galaxy and the standard NFW-at-cosmic-share to show the
# RAR blows up.  (The banked density-a0 route blew RAR 0.145->0.379 dex; here the
# damage is a DIFFERENT mechanism -- an additive cold halo -- but same fatal end.)
print("Representative estimate (additive cold-field halo at cosmic share on an L* disk):")
# At the optical radius of an L* spiral, MOND already gives the observed v_flat.
# Adding even 10% of the LCDM halo mass inside R_opt adds in quadrature to g_obs:
# the RAR is a TIGHT relation (0.13 dex). Any cold component that helps clusters
# (needs ~Omega_dm worth, concentrating like CDM) adds >>0.13 dex on galaxies.
for f_halo in [1.0, 0.3, 0.1]:
    # additive halo accel as a fraction of the baryonic MOND accel at R_opt:
    # if the field has cosmic share and concentrates like CDM, g_halo/g_bar ~ ratio_cosmic*f
    # (order-of-magnitude; the point is it is >> the 0.13 dex RAR width once f is O(0.1-1))
    boost = np.sqrt(1 + ratio_cosmic*f_halo)   # crude quadrature on v
    dex = np.log10(boost**2)                     # extra on g_obs in dex
    print(f"  field-halo fraction f={f_halo:>4.2f} of cosmic CDM -> +{dex:.2f} dex on g_obs (RAR width is 0.13 dex)")

print("""
VERDICT G2: a field that clusters like CDM enough to supply the cluster core
(needs ~Omega_dm-share, CDM-like concentration) adds >>0.13 dex to the SPARC RAR
on galaxies.  The ONLY escape is a component that clusters in clusters but NOT in
galaxies -- which requires an ACCELERATION-keyed or PHASE-SPACE-keyed switch.
The condensate's clustering is keyed on NEITHER: above M~10 eV it is pure CDM
(scale-free gravity); below, the Jeans cut is keyed on the COSMIC k, not on the
local acceleration -- and the sound speed GROWS with density, so cores are HARDER
to fill, not easier.  No cluster-ON/galaxy-OFF switch exists in the field.
""")

# ---------------------------------------------------------------------------
# MECHANISM (ii):  Q-mode sourced by the strong Y-mode (MOND) gradient
# ---------------------------------------------------------------------------
print("="*78)
print("MECHANISM (ii):  is the Q-mode (dust) SOURCED by the strong Y-mode gradient?")
print("="*78)
print("""
In AeST the action splits as J(Y) (the spatial-gradient MOND function, carries a0)
+ K(Q) (the temporal mode -> dust).  The route asks: does a strong Y-mode (deep
MOND regime, large |grad phi|) SOURCE extra Q-mode dust in the core?

Structural answer (sympy-checkable): Y and Q are DIFFERENT scalar invariants of the
SAME field (Y ~ spatial gradient^2 of the shift-charge potential; Q ~ temporal).
The shift symmetry phi -> phi + const protects the Q first integral a^3 K'(Q) = I0:
the dust amplitude I0 is a CONSERVED shift charge.  A spatial Y-gradient does NOT
source the temporal shift charge -- d I0 / d(grad phi) = 0 by the shift Ward identity
(the conserved current is J^mu = a^3 K' u^mu; its time component I0 is set by IC, not
by spatial gradients).  So the Y-mode (MOND) does NOT pump the Q-mode (dust).
""")

# Show this is the banked d rho_dust/d a0 = 0 orthogonality:
print("This is the banked orthogonality:  d rho_dust/d a0 = 0  and  d rho_dust/d Lambda = 0.")
print("The Y-mode (a0) and Q-mode (I0) are orthogonal flat directions -> NO sourcing.")
print("Mechanism (ii) = NULL by the shift Ward identity.")

# ---------------------------------------------------------------------------
# SUMMARY against the four gates
# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("ROUTE C -- VERDICT AGAINST THE FOUR GATES")
print("="*78)
print(f"""
G1 SUFFICIENCY:  The field CAN supply the core mass ONLY by setting the free I0 to
   ~Omega_dm-share AND letting it cluster like CDM (M>~10 eV).  But then it is just
   CDM-in-disguise concentrated by gravity -- it does NOT preferentially fill the
   ~10x-gas cored profile (FPS residual TRACKS GAS, a CDM halo is NFW-cuspy, wrong
   shape) and supplies the core target only at the cost of G2.  PARTIAL-but-FORFEITS.

G2 GALAXY-VETO:  FAILS.  A field that clusters like CDM enough to fill cluster cores
   makes CDM-like halos on galaxies (+0.3 to +1 dex on the SPARC RAR vs the 0.13 dex
   width).  The condensate has NO acceleration-keyed or phase-space switch to be
   cluster-ON/galaxy-OFF; above M~10 eV it is scale-free CDM, and its sound speed
   GROWS with density (cores HARDER to fill, the opposite of a chameleon).

G3 NO-NEW-PARTICLE:  PASSES in letter (it IS the framework's own field, no new
   species) -- but the win is hollow: to close clusters the field must become
   dynamically identical to CDM, so "no dark matter PARTICLE" is preserved in name
   while the dark sector becomes a cold clustering component = CDM by another name,
   and it STILL breaks galaxies (G2).

G4 DATA:  The LSS/Lyman-alpha bound M>~10 eV (matter power spectrum unsuppressed to
   k~1 Mpc^-1) FORCES the dust to be CDM-like -- which is exactly what makes G2 fail.
   The cored, gas-tracking FPS residual is NOT reproduced by a CDM-like field (wrong
   shape).  No data window for a cluster-ON/galaxy-OFF condensate clustering.

NET:  Route C is the SMOOTH-CDM-LIKE NULL, sharpened.  The condensate's own field
does NOT accumulate NONLINEARLY beyond gravitational CDM-like infall (no chameleon,
no Y->Q sourcing, accretion benign).  Forced to M>~10 eV by LSS, it clusters like
CDM -- which can be DIALED (free I0) to supply the cluster core, but then it breaks
galaxies exactly as a CDM halo would (G2), and its sound-speed-grows-with-density
makes cores HARDER not easier to fill.  No-particle field closure: FAILS G2 (and
forfeits the spirit of G3).  Banked smooth-CDM null CONFIRMED, with the new
both-ways content that the failure mode is specifically the missing cluster-ON/
galaxy-OFF switch + the wrong (gas-tracking vs NFW) core shape.
""")
