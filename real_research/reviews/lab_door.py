#!/usr/bin/env python3
"""
FRONT 4 — LAB / fundamental-tests door for the modified-INERTIA framework.

QUESTION (Carl, 'more doors'): can the framework's distinctive physics be tested in a LAB?
Two distinct lab signatures, computed quantitatively, both ways:

  (A) the MOND (modified-inertia) signature  -> needs a < a0 = 9.36e-11 m/s^2.
      The framework is modified INERTIA at LOW a. A ground lab is EFE-dominated by the
      external field of Earth/Sun/Galaxy >> a0 -> NO deep-MOND regime reachable. Quantify
      a_ext/a0 for every realistic lab external field, and the residual mu_fw(g)-1 boost.

  (B) the PREFERRED-FRAME (CPT-even SME) signature -> the induced gravity-sector s_bar^TX
      boost dipole (banked S_TENSOR_SME_COMPONENT_LEDGER, w5k0n9hd0). This DOES exist at
      high a, but its lab amplitude scales as A = a0/(2|a|): a ground lab sits at |a|=g,
      the HIGHEST acceleration -> the SMALLEST A -> the WEAKEST signal. Confront the lab
      prediction against the tightest LAB bounds (superconducting gravimeters, atom
      interferometry) -> quantify the margin.

  (C) the WEP / EP tests (MICROSCOPE) -> the framework couples to each particle's COM
      4-acceleration, identical for co-located species (UFF/WEP-exact) -> NULL by construction.

FOOTING (locked): a0 = 9.36e-11 m/s^2 (framework's OWN value, INPUT, quarantine: NOT derived),
c_T = 1, CPT-even, apex = CMB rest frame, beta_cmb = 369.82/c.

dS-Unruh interpolation (framework's OWN, NOT McGaugh's nu):
    g_obs = sqrt(g_bar^2 + g_bar*a0)    ->   mu_fw(g_obs) = g_bar/g_obs  (the inertia factor)
We use it to compute the residual modified-inertia boost at lab/EFE accelerations.

EVERY magnitude below is COMPUTED here. Real bounds from WebSearch this session:
  - Superconducting gravimeters (Flowers, Goodge, Tasson, PRL 119, 201101, 2017; arXiv:1612.08495):
        s_bar^(JK) spatial ~ 1e-10 ;  s_bar^(TX) ~ 3e-7   (GROUND, |a|=g)
  - Atom-interferometry isotropy of post-Newtonian gravity (Chung, Chiow, Herrmann, Chu,
        Mueller, PRL 100, 031101): 4 anisotropic SME coeffs at ppb (1e-9), 3 at 1e-5 (GROUND)
  - MICROSCOPE WEP (Touboul et al 2022): eta_Eotvos < 2e-14  (framework -> WEP-exact, null)
"""
import mpmath as mp
mp.mp.dps = 30

a0     = mp.mpf('9.36e-11')          # framework a0 (INPUT)
c_ms   = mp.mpf('299792458')
c_kms  = mp.mpf('299792.458')
v_cmb  = mp.mpf('369.82')            # km/s, Planck 2018 CMB dipole
beta   = v_cmb / c_kms               # 1.2336e-3
RA     = mp.radians(167.9); Dec = mp.radians(-6.9)
nX     = mp.cos(Dec)*mp.cos(RA)      # ~ -0.97 (dominant component)

def mu_fw(g_bar):
    """framework's OWN dS-Unruh inertia factor mu = g_bar/g_obs, g_obs=sqrt(g^2+g*a0)."""
    g_obs = mp.sqrt(g_bar**2 + g_bar*a0)
    return g_bar/g_obs

print("="*94)
print("FRONT 4 — LAB DOOR for the modified-INERTIA + preferred-frame framework")
print("footing: a0 = %s m/s^2 (INPUT), beta_cmb = %s, n_X = %s" %
      (mp.nstr(a0,3), mp.nstr(beta,5), mp.nstr(nX,3)))
print("="*94)

# ============================================================================
# (A) THE EFE OBSTRUCTION — is the deep-MOND (a<a0) regime reachable in a lab?
# ============================================================================
print("\n(A) EFE OBSTRUCTION: every realistic lab external field vs a0")
print("-"*94)
ext_fields = [
    ("Earth surface gravity g",            mp.mpf('9.80665')),
    ("Sun's tidal/grav field at Earth",    mp.mpf('5.93e-3')),   # GM_sun/(1AU)^2
    ("Galactic field at Sun (~1.8 a0)",    mp.mpf('1.8')*a0),    # the Milky Way's pull on the Sun
    ("Earth's pull on a LEO satellite",    mp.mpf('8.7')),
    ("drag-free sat residual (LISA-class)",mp.mpf('1e-9')),      # best achieved free-fall residual
    ("torsion-balance residual accel",     mp.mpf('1e-12')),     # ~fm/s^2-class differential, optimistic
]
print(f"{'external field':36s} {'a_ext (m/s^2)':>15s} {'a_ext/a0':>14s} {'regime':>16s}")
for name, a_ext in ext_fields:
    ratio = a_ext/a0
    regime = "deep-MOND (a<a0)" if ratio < 1 else ("transition" if ratio < 10 else "Newtonian/EFE")
    print(f"{name:36s} {mp.nstr(a_ext,4):>15s} {mp.nstr(ratio,4):>14s} {regime:>16s}")
print("-"*94)
print("VERDICT (A): every GROUND/orbital lab external field is >> a0. Earth's g alone is")
print("   a_ext/a0 = %s -> %s orders above the MOND scale. The deep-MOND regime is" %
      (mp.nstr(mp.mpf('9.80665')/a0,4), mp.nstr(mp.log10(mp.mpf('9.80665')/a0),3)))
print("   EFE-SWAMPED on Earth. The ONLY environment at a<a0 is a drag-free satellite whose")
print("   residual self/Earth field is pushed below 9.36e-11 — but Earth's pull in LEO is ~8.7,")
print("   so reaching a<a0 needs a residual < 1e-10: ~2 orders below LISA-class free fall.")

# residual modified-inertia boost mu_fw(g)-1 at each lab field (the *intrinsic* MI signal)
print("\n   Residual modified-inertia boost |mu_fw(g)-1| (the deviation from Newton the lab could see):")
print(f"   {'external field':36s} {'a_ext/a0':>12s} {'|1-mu_fw|':>14s}")
for name, a_ext in ext_fields:
    boost = abs(1 - mu_fw(a_ext))
    print(f"   {name:36s} {mp.nstr(a_ext/a0,4):>12s} {mp.nstr(boost,4):>14s}")
print("   => at Earth's g the intrinsic MI deviation from Newton is %s (a0/2g),"
      % mp.nstr(abs(1-mu_fw(mp.mpf('9.80665'))),3))
print("      ~%s -- utterly below ANY gravimeter/EP floor. MI is NULL in a ground lab."
      % mp.nstr(abs(1-mu_fw(mp.mpf('9.80665'))),2))

# ============================================================================
# (B) PREFERRED-FRAME s_bar^TX in a lab -- the door that COULD survive EFE
# ============================================================================
print("\n" + "="*94)
print("(B) PREFERRED-FRAME s_bar^TX BOOST DIPOLE in a lab (exists at HIGH a, A=a0/2|a|)")
print("-"*94)
def sTX(a):
    return (a0/(2*a)) * beta * abs(nX)     # leading order; gamma^2~1 at beta_cmb

# lab / experiment accelerations
g_lab  = mp.mpf('9.80665')
labs = [
    ("Superconducting gravimeter (ground)", g_lab,         mp.mpf('3e-7'),  "s_bar^TX, Flowers17"),
    ("  '' spatial channel s_bar^JK",        g_lab,         mp.mpf('1e-10'), "s_bar^JK, Flowers17"),
    ("Atom interferometer (ground)",         g_lab,         mp.mpf('1e-9'),  "anisotropy, Chung09"),
    ("Atom interferom. (weak chan)",         g_lab,         mp.mpf('1e-5'),  "anisotropy, Chung09"),
]
print(f"{'lab experiment':40s} {'|a|':>9s} {'|s_TX|pred':>12s} {'bound':>10s} {'margin':>10s}")
A_lab = a0/(2*g_lab)
print("  (lab prefactor A = a0/2g = %s -- the SMALLEST A of any arena)" % mp.nstr(A_lab,4))
for name, a, bound, chan in labs:
    s = sTX(a)
    margin = bound/s
    print(f"{name:40s} {mp.nstr(a,3):>9s} {mp.nstr(s,4):>12s} {mp.nstr(bound,3):>10s} {mp.nstr(margin,4):>10s}")
print("-"*94)
print("VERDICT (B): the lab s_bar^TX prediction is %s (at |a|=g)." % mp.nstr(sTX(g_lab),4))
print("   The tightest LAB bound is the superconducting-gravimeter spatial channel ~1e-10,")
print("   giving margin ~%s. The s_bar^TX channel itself is bounded at ~3e-7 -> margin ~%s."
      % (mp.nstr(mp.mpf('1e-10')/sTX(g_lab),3), mp.nstr(mp.mpf('3e-7')/sTX(g_lab),3)))
print("   => the LAB s_bar floor is ~4-7 ORDERS too coarse: a ground lab sits at the HIGHEST")
print("      acceleration g, which gives the SMALLEST A=a0/2g and hence the WEAKEST signal.")

# the contrast: the SAME dipole at the lowest-accel SPACE body is the live test, NOT a lab
a_saturn = mp.mpf('6.5e-5')
print("\n   CONTRAST (why this is a SPACE test, not a lab test): the SAME dipole at Saturn's")
print("   orbital accel a=%s gives |s_TX|=%s (A is %sx larger than the lab),"
      % (mp.nstr(a_saturn,2), mp.nstr(sTX(a_saturn),4), mp.nstr(g_lab/a_saturn,4)))
print("   confronted by INPOP/Cassini ~8.3e-9 -> ~9.6x (the banked live front). The lab is")
print("   the WRONG arena for s_TX by the ratio (g/a_Saturn) = %s." % mp.nstr(g_lab/a_saturn,4))

# ============================================================================
# (C) WEP / MICROSCOPE -- null by construction
# ============================================================================
print("\n" + "="*94)
print("(C) WEP / EP (MICROSCOPE eta<2e-14): NULL by construction")
print("-"*94)
print("   The MI coupling is to each particle's COM 4-acceleration, IDENTICAL for co-located")
print("   species (universal, mass-proportional, CPT-even) -> Eotvos eta = 0 EXACTLY (the")
print("   differential cancellation, banked ledger). MICROSCOPE tests species DIFFERENCES;")
print("   the framework predicts NONE. Predicted eta = 0 vs bound 2e-14 -> NULL, not a door.")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*94)
print("FRONT-4 LAB DOOR SUMMARY")
print("="*94)
print("(A) MOND/MI signature: EFE-SWAMPED. Earth g is %s x a0 (~%s orders); the intrinsic"
      % (mp.nstr(g_lab/a0,3), mp.nstr(mp.log10(g_lab/a0),2)))
print("    MI boost in a ground lab is ~%s. No deep-MOND regime reachable on the ground;"
      % mp.nstr(abs(1-mu_fw(g_lab)),2))
print("    a<a0 needs a drag-free residual <1e-10 (~2 orders below LISA-class). BELOW-FLOOR.")
print("(B) s_bar^TX preferred-frame dipole: EXISTS in a lab (=%s) but the lab acceleration g"
      % mp.nstr(sTX(g_lab),3))
print("    gives the SMALLEST A=a0/2g; tightest lab bound ~1e-10 is ~%sx too coarse."
      % mp.nstr(mp.mpf('1e-10')/sTX(g_lab),2))
print("    The s_TX live test is SPACE (Saturn/INPOP-Cassini ~9.6x), NOT a lab. ALREADY-COVERED.")
print("(C) WEP/MICROSCOPE: NULL by construction (WEP-exact, differential cancellation).")
print("-"*94)
print("NET: NO fresh lab door. The MOND signature is EFE-swamped/below-floor on the ground;")
print("     the preferred-frame s_bar^TX exists in a lab but is 4-7 orders below the lab floor")
print("     and its real near-term test is the SPACE s_TX dipole (banked, already-covered);")
print("     the WEP channel is null by construction. The obstruction is QUANTITATIVELY confirmed.")
print("="*94)
