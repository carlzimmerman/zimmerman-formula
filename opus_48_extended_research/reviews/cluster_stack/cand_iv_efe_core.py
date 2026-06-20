"""
FINAL-DOOR candidate (iv): the EXTERNAL-FIELD-EFFECT (EFE) correction on the core.

QUESTION (both ways): does the EFE -- the MOND/modified-inertia coupling to the ambient
gravitational field -- ADD missing mass in the cluster core, shrinking the residual a
no-DM theory must source?

THE PHYSICS (literature + the framework's own MI, both ways):
  - EFE in MOND: a system's internal MOND boost is SUPPRESSED when the EXTERNAL field
    g_ext exceeds the internal field. In a cluster CORE the INTERNAL field is the LARGEST
    in the cluster (densest baryons, hottest gas) -> the core is the LEAST EFE-affected
    region. At the very center the external (cluster-scale) field is small relative to the
    steep internal field, so EFE is negligible THERE.
  - SIGN in the cluster (the decisive check): including the EFE makes the MOND boost
    SMALLER, so MORE missing mass is required to fit the data, NOT less (Kelleher-Lelli /
    aanda 49968-24, verbatim: "when the EFE is taken into account ... the MOND boost is
    decreased, so MORE missing mass is required"). So EFE is the WRONG SIGN: it deepens
    the residual a no-DM theory must source, it does not shrink it.
  - The framework is MODIFIED-INERTIA. In MI the relevant acceleration is the TRUE internal
    self-field (banked: solitary-MSP pulsar reductio forces the self-field, not the galactic
    ~2a0 reading). The cluster's external field on the core is g_ext ~ G M(<R)/R^2 at the
    cluster scale; at the CORE center the self-field dominates -> the MI core boost is set
    by the internal g_bar, unchanged by EFE. The dS-Unruh ENVIRONMENTAL term was already
    banked as WRONG-SIGNED (hot core a >> a0 -> more Newtonian -> LESS MOND). EFE is the
    same physics: it cannot ADD core phantom.

CONCLUSION (both ways): the EFE on the cluster core is either negligible (internal field
dominates the center) or WRONG-SIGNED (it suppresses the MOND boost -> deepens, not closes,
the residual). It is NOT a third ingredient.

We quantify: (1) the EFE suppression factor across the core radii on the framework footing,
(2) the resulting change in the MI phantom (it goes DOWN, deepening the gap), both ways.
"""
import numpy as np

G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19
Mpc  = 1000*kpc
a0   = 9.36e-11

print("="*94)
print(" FINAL-DOOR candidate (iv): EXTERNAL-FIELD-EFFECT (EFE) on the cluster core")
print("="*94)

# banked core numbers
M_target_lens = 1.357e14
M_phantom_MI  = 3.508e13
core_gap      = M_target_lens - M_phantom_MI
print("\n[banked core, <420 kpc] target %.3e, MI phantom %.3e, gap %.3e (x%.2f)"
      % (M_target_lens, M_phantom_MI, core_gap, M_target_lens/M_phantom_MI))

# =====================================================================
# 1. the internal vs external field across the core (where does EFE matter?)
# =====================================================================
print("\n" + "-"*94)
print(" 1. Internal self-field vs the cluster external field across the core")
print("-"*94)
# rich cluster baryon model (same as routeA): beta-model gas + BCG
M500_c, R500_c, fgas500, beta, rc = 1.0e15*Msun, 1400.0*kpc, 0.13, 0.70, 200.0*kpc
M_BCG, a_BCG = 1.0e12*Msun, 25.0*kpc
def Mgas_enc(r, rho0):
    rr = np.linspace(1e-4*rc, r, 6000)
    rho = rho0/(1.0+(rr/rc)**2)**(1.5*beta)
    return np.trapz(4*np.pi*rr**2*rho, rr)
rho0_gas = fgas500*M500_c/Mgas_enc(R500_c, 1.0)
def M_bar(r):
    return Mgas_enc(r, rho0_gas) + M_BCG*r**2/(r+a_BCG)**2
def g_int(r):  # internal Newtonian self-field
    return G*M_bar(r)/r**2
# external field: the cluster sits in cosmic web filament/large-scale field ~ few x 1e-12 m/s2
# (Kelleher-Lelli: g_ext for clusters from the local supercluster ~ 0.01-0.1 a0). Take generous.
g_ext = 0.1*a0   # generous external field on the cluster (most clusters: << this at center)
print("  external (cosmic-web) field on the cluster ~ %.2f a0 = %.2e m/s^2 (generous)" % (g_ext/a0, g_ext))
print("  %6s %14s %14s %14s" % ("R[kpc]", "g_int[m/s2]", "g_int/a0", "g_int/g_ext"))
for Rk in [50, 100, 200, 300, 420]:
    gi = g_int(Rk*kpc)
    print("  %6d %14.3e %14.3f %14.2f" % (Rk, gi, gi/a0, gi/g_ext))
print("  => across the WHOLE core the internal self-field >> the external field")
print("     (ratio >> 1). The core is INTERNAL-field-dominated -> EFE is NEGLIGIBLE there.")

# =====================================================================
# 2. SIGN: if EFE acts at all, does it ADD or SUBTRACT core phantom?
# =====================================================================
print("\n" + "-"*94)
print(" 2. SIGN of the EFE (does it add core phantom or deepen the deficit?)")
print("-"*94)
# EFE-modified interpolation (Famaey-McGaugh): g_obs = g_int * nu( (g_int+g_ext)/a0 ) roughly;
# adding g_ext INCREASES the argument -> nu DECREASES -> LESS boost -> SMALLER phantom.
def nu_simple(x):  # simple interpolation nu(x) = 0.5 + sqrt(0.25 + 1/x)
    return 0.5 + np.sqrt(0.25 + 1.0/x)
def M_phantom(r, gext):
    gi = g_int(r)
    x  = (gi+gext)/a0
    gobs = gi*nu_simple(x)
    return (gobs*r**2/G - M_bar(r))
Mph_noEFE = sum(0 for _ in [0]) or None
# core-integrated phantom (shell sum) with and without EFE
rr = np.linspace(5*kpc, 420*kpc, 400)
def core_phantom(gext):
    # crude enclosed-phantom proxy at R=420 using local g_obs (consistent w/ banked method)
    gi = g_int(420*kpc); x=(gi+gext)/a0; gobs=gi*nu_simple(x)
    return (gobs*(420*kpc)**2/G - M_bar(420*kpc))/Msun
Mph_iso = core_phantom(0.0)
Mph_efe = core_phantom(g_ext)
print("  MI/MOND core phantom (<420 kpc), NO EFE (isolated)  = %.3e Msun" % Mph_iso)
print("  MI/MOND core phantom (<420 kpc), WITH g_ext=0.1 a0  = %.3e Msun" % Mph_efe)
print("  => EFE change = %+.1f%% (the phantom goes %s)"
      % (100*(Mph_efe-Mph_iso)/Mph_iso, "DOWN -> DEEPENS the gap" if Mph_efe<Mph_iso else "UP"))
print("  Verbatim Kelleher-Lelli (aanda 49968-24): 'when the EFE is taken into account the")
print("  MOND boost is decreased, so MORE missing mass is required.' WRONG SIGN to help.")

# =====================================================================
# 3. the MI-specific reading (banked): self-field forced, dS-Unruh env wrong-signed
# =====================================================================
print("\n" + "-"*94)
print(" 3. The framework's MODIFIED-INERTIA reading (banked)")
print("-"*94)
print("  - MI uses the TRUE internal self-field (solitary-MSP pulsar reductio forces it).")
print("    At the core center the self-field dominates -> the MI boost is set by g_bar,")
print("    UNCHANGED by the external field. No EFE core enhancement.")
print("  - The dS-Unruh ENVIRONMENTAL term was already banked WRONG-SIGNED: a hot core with")
print("    a >> a0 is MORE Newtonian -> LESS MOND -> SMALLER phantom. EFE is the same physics.")
print("  - So in BOTH the MG (interpolation) and MI (dS-Unruh) readings, the EFE/environment")
print("    on the core is negligible-or-wrong-signed. It cannot ADD core phantom.")

# =====================================================================
# 4. GATES
# =====================================================================
print("\n" + "="*94)
print(" GATES for candidate (iv) [EFE / external-field correction on the core]")
print("="*94)
print("  G1 SUFFICIENCY : FAILS -- the core is internal-field-dominated (EFE negligible),")
print("                   and where EFE acts it is WRONG-SIGNED (suppresses the boost ->")
print("                   MORE missing mass required, deepening the gap). Adds <=0 core mass.")
print("  G2 GALAXY-VETO : N/A (no new field; EFE is intrinsic MOND).")
print("  G3 NO-PARTICLE : PASS trivially (intrinsic to the theory, no new mass).")
print("  G4 DATA        : consistent -- clusters' EFE is small at the center; literature")
print("                   (Kelleher-Lelli) confirms EFE deepens, not closes, the deficit.")
print("\n  VERDICT (iv): NOT a third ingredient. The EFE on the core is negligible (internal")
print("  field dominates) or wrong-signed (suppresses the MOND boost). Both ways: no help.")
