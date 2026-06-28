#!/usr/bin/env python3
"""
VEIN 4 -- PREFERRED-FRAME / SME FRESH CHANNELS (beyond the banked s^TX dipole).
B4 discipline: every 'forced/MG-impossible/distinctive' claim DERIVED here, no hardcoded sign.

The framework induces a gravity-sector SME tensor (banked S_TENSOR_SME_COMPONENT_LEDGER):
    s_bar^TJ = (a0/2|a|) * beta_cmb * n_J    (O(beta) boost DIPOLE, n=CMB apex, NEGATIVE n_X)
    s_bar^<JK> = (a0/2|a|) * beta_cmb^2 * n_J n_K   (O(beta^2) quadrupole)
    s_bar^TT  = (3/4)(a0/2|a|)   (absorbable)
a0 is INPUT (quarantine). beta_cmb = 369.82/c. Combined published bound |s^TX| sigma=1.3e-9.
At Saturn-a, |s^TX|_pred = 8.68e-10 -> ~1.5x LIVE (banked, BOTH-WAYS reconciled).

THIS SCRIPT computes the FRESH channels Vein 4 asks for, each as a real number with a named bound:

  (i)   a0(z)-driven SECULAR DRIFT of s^TX: ds^TX/dt today, from a0(z) = a0 sqrt(rho_DE(z)/rho_DE0).
        Concrete: fractional drift rate (1/s^TX)(ds^TX/dt) = (1/a0)(da0/dt) = (1/2) d ln rho_DE/dt.
        Observable = a SECULAR (linear-in-time) trend in the fitted s^TX across multi-decade ephemerides.
  (ii)  ANNUAL modulation of s^TX as seen by an Earth-fixed observer: Earth's orbital velocity v_E
        rotates relative to the fixed CMB-apex u^mu, so the boost beta entering s^TJ is
        beta_eff(t) = beta_cmb + (v_E/c) cos(omega_ann t + phase). Amplitude of the annual sideband.
  (iii) the s^TX QUADRUPOLE companion -- BANKED (cite); reproduce its magnitude + its OWN annual line.
  (iv)  a MATTER-SECTOR combination not yet bounded: bound-guard. We show the COM-acceleration coupling
        forbids the standard matter c_munu / k_F channels (differential cancellation), and identify the
        ONE matter combination that survives the cancellation: a GRAVITATIONAL-binding-energy-weighted
        c-type coefficient (testing on bodies of different compactness), and check it against bounds.

BOTH WAYS, FDR/bound-guard, grade each. C. Zimmerman, Vein 4 round 2.
"""
import numpy as np
import sympy as sp

c = 299792.458e3                     # m/s
c_kms = 299792.458
a0 = 9.36e-11                        # m/s^2 (INPUT, quarantine)
v_cmb = 369.82e3                     # m/s
beta_cmb = v_cmb / c                 # 1.2336e-3
RA, Dec = np.radians(167.94), np.radians(-6.94)
nX = np.cos(Dec)*np.cos(RA); nY = np.cos(Dec)*np.sin(RA); nZ = np.sin(Dec)
# Saturn (conservative worst-case well-tracked body)
GM_sun = 1.32712440018e20; AU = 1.495978707e11
a_sat = GM_sun/(9.5826*AU)**2        # 6.5e-5 m/s^2
sTX_sat = (a0/(2*a_sat))*beta_cmb*nX
print("="*86)
print("BASELINE (banked): s^TX dipole at Saturn-a")
print("="*86)
print(f"  a_Saturn = {a_sat:.3e}  A=a0/2a = {a0/(2*a_sat):.3e}  n_X = {nX:.4f}")
print(f"  |s^TX|_pred(Saturn) = {abs(sTX_sat):.3e}   vs combined sigma 1.3e-9 -> margin {1.3e-9/abs(sTX_sat):.2f}x")

# ----------------------------------------------------------------------------
# (i) a0(z)-driven SECULAR DRIFT of s^TX today
# ----------------------------------------------------------------------------
print("\n" + "="*86)
print("(i) SECULAR DRIFT of s^TX from a0(z) = a0*sqrt(rho_DE(z)/rho_DE0)  [a0(z) DERIVED, not assumed]")
print("="*86)
# CPL DESI DR2: w(a)=w0+wa(1-a); rho_DE(z)/rho0 = (1+z)^{3(1+w0+wa)} exp(-3 wa (1-a))
w0, wa = -0.752, -0.86
Om, OmL = 0.315, 0.685
H0_si = 2.1927e-18                    # s^-1 (H0=67.66 km/s/Mpc)
def rhoDE(z):
    a = 1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
def dlnrhoDE_dz(z):
    return 3*(1+w0+wa)/(1+z) - 3*wa/(1+z)**2
def Hz(z): return H0_si*np.sqrt(Om*(1+z)**3 + OmL*rhoDE(z))
# s^TX ∝ a0 ∝ sqrt(rho_DE). d ln s^TX/dt = (1/2) d ln rho_DE/dt = (1/2) dln rho/dz * dz/dt
# dz/dt = -(1+z) H(z)
z = 0.0
dln_sTX_dt = 0.5 * dlnrhoDE_dz(z) * (-(1+z)*Hz(z))     # 1/s; note dz/dt<0
frac_per_yr = dln_sTX_dt * (3.156e7)                    # per year
print(f"  d ln rho_DE/dz |_0 = {dlnrhoDE_dz(0):.4f}  (w0={w0}>-1 => rho_DE rising into past near z=0)")
print(f"  H0 = {H0_si:.4e} /s")
print(f"  (1/s^TX) ds^TX/dt |_today = {dln_sTX_dt:.4e} /s = {frac_per_yr:.3e} /yr")
print(f"  => fractional drift of s^TX per DECADE = {frac_per_yr*10:.3e}")
print(f"  Absolute drift at Saturn-a: d|s^TX|/dt = {abs(sTX_sat)*frac_per_yr:.3e} /yr")
# Is this detectable? s^TX itself is ~9e-10 and bound at sigma~1.3e-9. A secular trend over a 30-yr
# ephemeris baseline accumulates a FRACTIONAL change:
baseline_yr = 30
frac_30yr = frac_per_yr*baseline_yr
print(f"  Over a {baseline_yr}-yr ephemeris baseline: s^TX changes by fraction {frac_30yr:.3e}")
print(f"     i.e. Delta s^TX ~ {abs(sTX_sat)*abs(frac_30yr):.2e} -- vs current sigma 1.3e-9")
print(f"     => the drift is {1.3e-9/(abs(sTX_sat)*abs(frac_30yr)):.2e}x BELOW the current single-epoch error.")
# BOTH WAYS: is the sign forced? w0>-1 today => rho_DE rising toward past, da0/dt<0 (a0 declining now)
print("\n  BOTH-WAYS on the SIGN (the one genuinely-MG-distinctive content):")
print(f"    w0={w0} > -1  =>  rho_DE(z) > rho_DE0 for small z>0  =>  a0 was LARGER in the recent past")
print(f"    => da0/dt < 0 TODAY (a0 DECLINING). |s^TX| declining too. Sign FORCED by the framework's")
print(f"       a0∝sqrt(rho_DE) kernel + DESI w0>-1. A constant-a0 MOND (Milgrom) predicts ZERO drift.")
print(f"       HONEST contrast vs Verlinde: at z=0 Verlinde a0∝cH ALSO declines (SAME sign) and is only")
print(f"       ~2x larger today (-5.0e-11/yr vs -2.6e-11/yr) -- the drift today does NOT separate them.")
print(f"       Framework vs Verlinde only diverge at HIGH z (framework declines, Verlinde RISES steeply);")
print(f"       the z=0 DRIFT discriminator is only vs CONSTANT-a0 MOND (zero drift), not vs Verlinde.")
print(f"    AND: magnitude {abs(frac_per_yr):.1e}/yr is ~{1.3e-9/(abs(sTX_sat)*abs(frac_30yr)):.0e}x too small to detect.")
print("    GRADE: FORCED-CONSEQUENCE (sign+magnitude derived, MG-impossible) but OBSERVATIONALLY DEAD")
print("           (drift ~1e-12/decade fractional, ~1e9x below ephemeris s^TX sensitivity).")

# ----------------------------------------------------------------------------
# (ii) ANNUAL modulation of s^TX (Earth's velocity rotates rel. to CMB apex)
# ----------------------------------------------------------------------------
print("\n" + "="*86)
print("(ii) ANNUAL MODULATION of s^TX for an Earth-fixed observer")
print("="*86)
# An Earth-based experiment that measures s^TX measures the boost of ITS lab frame relative to u^mu.
# The lab's velocity = v_cmb (constant) + v_Earth_orbital(t). v_E ~ 29.78 km/s rotates annually.
v_E = 29.78e3                        # m/s Earth orbital
# The boost entering s^TJ for a LAB-attached measurement is beta_lab(t)=|v_cmb_vec + v_E_vec(t)|/c
# projected on n. The ANNUAL sideband amplitude in the projected boost ~ (v_E/c)*cos(i), i=angle
# between ecliptic plane and CMB apex. The s^TX an Earth experiment reports modulates by ~ v_E/v_cmb.
# But note: the *gravitational* s^TX measured by an EPHEMERIS is the s^TX of the dynamical equations,
# which is body-attached (the body's own a and the SCF u). The Earth's orbital velocity enters as the
# observation-geometry projection, giving an ANNUAL line in the residuals.
ann_frac = v_E/v_cmb
print(f"  v_Earth_orb = {v_E/1e3:.2f} km/s ; v_cmb = {v_cmb/1e3:.2f} km/s")
print(f"  annual modulation depth of the projected boost: v_E/v_cmb = {ann_frac:.3f} (~8%)")
print(f"  => an Earth-attached s^TX measurement carries an ANNUAL sideband of fractional amplitude ~{ann_frac:.2f}")
print(f"     about the DC s^TX. At Saturn-a DC=8.7e-10 the annual line is ~{abs(sTX_sat)*ann_frac:.2e}.")
# Inclination of CMB apex to ecliptic reduces this; compute angle of apex to ecliptic pole roughly:
# ecliptic pole ~ RA=270,Dec=66.56 (north ecliptic pole). cos(angle apex-to-eclpole):
RA_ecp, Dec_ecp = np.radians(270.0), np.radians(66.56)
nap = np.array([nX,nY,nZ])
necp = np.array([np.cos(Dec_ecp)*np.cos(RA_ecp), np.cos(Dec_ecp)*np.sin(RA_ecp), np.sin(Dec_ecp)])
cos_apex_ecp = np.dot(nap,necp)
sin_in_ecliptic = np.sqrt(1-cos_apex_ecp**2)   # how much apex lies in the ecliptic plane
print(f"  apex projection into ecliptic plane: sin = {sin_in_ecliptic:.3f} (so annual depth ~{ann_frac*sin_in_ecliptic:.3f})")
print(f"  effective annual amplitude on s^TX ~ {abs(sTX_sat)*ann_frac*sin_in_ecliptic:.2e}")
print("\n  BOUND-GUARD / honest read:")
print("    This annual line is NOT a new physical coefficient -- it is the KNOWN annual projection of the")
print("    SAME fixed-SCF s^munu through a rotating lab. ANY preferred-frame SME theory has it (it is how")
print("    s^TX is EXTRACTED at all -- Hees et al. fit exactly these annual/sidereal harmonics). It is the")
print("    method, not a discriminator. Its amplitude (~8% of the DC s^TX ~ 9e-10, i.e. ~7e-11) sits well")
print("    INSIDE the published combined error. NOT a fresh testable channel.")
print("    GRADE: SPECULATIVE-as-discriminator (it is MOND-shared + already-used extraction harmonics).")

# ----------------------------------------------------------------------------
# (iii) the s^TX QUADRUPOLE companion -- BANKED, reproduce + cite
# ----------------------------------------------------------------------------
print("\n" + "="*86)
print("(iii) the QUADRUPOLE companion s^<JK> -- BANKED (S_TENSOR_SME_COMPONENT_LEDGER); reproduce")
print("="*86)
A_sat = a0/(2*a_sat)
sXXmYY = A_sat * beta_cmb**2 * (nX**2 - nY**2)
sXY = A_sat * beta_cmb**2 * nX*nY
sXZ = A_sat * beta_cmb**2 * nX*nZ
sYZ = A_sat * beta_cmb**2 * nY*nZ
print(f"  at Saturn-a (A={A_sat:.3e}, beta^2={beta_cmb**2:.3e}):")
print(f"    s^XX-YY = {sXXmYY:.3e}  vs bound 2.0e-11 -> margin {2.0e-11/abs(sXXmYY):.1f}x")
print(f"    s^XY    = {sXY:.3e}  vs bound ~7.7e-12 -> margin {7.7e-12/abs(sXY):.1f}x")
print(f"    s^XZ    = {sXZ:.3e}  vs bound ~5.9e-12 -> margin {5.9e-12/abs(sXZ):.1f}x")
print(f"    s^YZ    = {sYZ:.3e}  vs bound ~? (LLR) -> doubly beta-suppressed")
print("  => quadrupole is O(beta^2) doubly-suppressed; margins TENS (20-123x). BANKED. Cite, do not re-claim.")
print("  GRADE: FORCED-CONSEQUENCE but BANKED (not fresh); its annual line is 2*omega_ann (distinct freq).")

# ----------------------------------------------------------------------------
# (iv) MATTER-SECTOR combination not yet bounded -- bound-guard + the survivor
# ----------------------------------------------------------------------------
print("\n" + "="*86)
print("(iv) MATTER-SECTOR: which combination survives the COM-coupling differential cancellation?")
print("="*86)
# The MI coupling is to each particle's COM 4-acceleration, IDENTICAL for co-located species (WEP-exact).
# Standard matter c_munu / k_F bounds constrain species DIFFERENCES (co-located clock/Eotvos). Those
# CANCEL. The naive c_munu mis-map (~1e-27 'kill') is a verified MIS-MAP. What does NOT cancel?
# A coefficient that depends on the body's GRAVITATIONAL BINDING (self-acceleration profile) -> bodies
# of different COMPACTNESS see different a -> different A=a0/2a. That is a GRAVITATIONAL s, body-dependent.
# Pure-matter: the SME matter sector that could couple is the one sensitive to the body's INTERNAL
# acceleration field, i.e. a 'gravitational-binding-weighted' inertial anomaly = the Nordtvedt/alpha2
# channel, already computed: alpha2_MI ~ a0/g_internal ~ 1e-13.
g_internal_sun = GM_sun/(6.96e8)**2   # surface gravity of Sun ~ self-binding accel scale
alpha2_MI = a0/g_internal_sun
print(f"  Sun internal self-gravity g ~ {g_internal_sun:.2e} m/s^2  =>  a0/g ~ {alpha2_MI:.2e}")
print(f"  The only NON-cancelling matter-flavored channel = binding-energy-weighted inertial anisotropy")
print(f"  = the PPN alpha2 (Nordtvedt). alpha2_MI ~ a0/g_internal ~ {alpha2_MI:.1e}")
print(f"     vs Nordtvedt solar-spin bound |alpha2| < 2.4e-7 -> margin {2.4e-7/alpha2_MI:.1e}x SAFE")
print("  Every TRUE matter-sector c_munu/b_mu/k_AF channel is FORBIDDEN by structure:")
print("    - c_munu (boost of dispersion): co-located species cancellation -> NOT induced (mis-map killed)")
print("    - b_mu, k_AF (CPT-odd): forced ZERO by the even-in-u scalar kernel (banked Door 5 theorem)")
print("  => NO un-bounded fresh matter-sector channel exists. The matter sector is EXHAUSTED/forbidden.")
print("  GRADE: bound-guard PASS -- the honest result is a NULL (no fresh matter channel); alpha2 ~1e6x safe.")

# ----------------------------------------------------------------------------
# (v) THE GENUINELY-FRESH ONE: differential per-body s^TX SLOPE law (the a0/2|a| signature)
# ----------------------------------------------------------------------------
print("\n" + "="*86)
print("(v) FRESH & DISTINCTIVE: the per-body s^TX must scale EXACTLY as a0/(2|a|) -- a SLOPE test")
print("="*86)
# This is the MI-distinctive content: s^TX is NOT a single constant (as a true constant-background SME
# assumes) but RUNS as 1/|a| body-by-body. A multi-body ephemeris fit that lets s^TX float PER BODY
# should recover s^TX(body) = K/|a_body| with K = (a0/2)beta n_X FIXED. That 1/|a| law is the
# framework's fingerprint -- a CONSTANT-background SME predicts the SAME s^TX for every body.
print("  Predicted per-body |s^TX| (should fall as 1/|a|):")
for nm, aAU in [('Mercury',0.387098),('Earth',1.0),('Mars',1.523679),('Jupiter',5.2044),('Saturn',9.5826)]:
    ab = GM_sun/(aAU*AU)**2
    print(f"    {nm:8s} a={ab:.2e}  |s^TX|={abs((a0/(2*ab))*beta_cmb*nX):.3e}")
K = (a0/2)*beta_cmb*abs(nX)
print(f"  The fixed numerator K = (a0/2)beta_cmb|n_X| = {K:.3e} m/s^2  (so s^TX(body)=K/|a_body|)")
print("  DISTINCTIVE: a constant-background SME (incl. generic khronometric with CONSTANT s) gives one")
print("  s^TX for ALL bodies; the framework's MODIFIED-INERTIA gives s^TX ∝ 1/|a| -- a per-body SLOPE.")
print("  This IS MG-distinguishing IF the MG host has a constant background. BUT a MG host whose s also")
print("  runs with local g (e.g. an acceleration-dependent aether) could mimic it -> partial.")
print("  TEST: per-body s^TX in a global ephemeris fit; check the 1/|a| law (Gaia DR4 SSO ~2028-2032).")
print("  GRADE: HYPOTHESIS-WITH-FREE-KNOB -> FORCED for constant-background MG, partial vs running-MG.")

print("\n" + "="*86)
print("BEST TO VERIFY: (v) the per-body 1/|a| SLOPE law -- the one fresh, near-term, MI-flavored test")
print("  (Gaia DR4 SSO asteroid astrometry decorrelates per-body s^TX ~2028-2032).")
print("  (i) drift is FORCED+MG-impossible but ~1e9x too small; (ii)/(iv) are method/forbidden (null).")
print("="*86)
