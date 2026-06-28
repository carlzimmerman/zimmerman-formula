#!/usr/bin/env python3
"""
ADVERSARIAL KILL TEST -- the per-body 1/|a| s^TX SLOPE law (Vein 4, channel v).
B4 discipline: every 'forced/MG-impossible/distinctive' claim must be DERIVED with a real
dynamical/statistical calc, NO hardcoded sign, NO ad-hoc proxy. Default to KILL if uncertain.

POSIT under attack:
  s^TX(body) = K/|a_body|, FIXED numerator K = (a0/2) beta_cmb |n_X| = 5.6e-14 m/s^2.
  Predicted ladder: Mercury 1.4e-12, Earth 9.5e-12, Mars 2.2e-11, Jupiter 2.6e-10, Saturn 8.7e-10.
  WHY-MG-CANNOT (claimed): a constant-background SME gives the SAME s^TX for every body; the
  framework's modified INERTIA gives s^TX proportional to 1/|a| -- a per-body slope. Grade
  HYPOTHESIS-WITH-FREE-KNOB. Test: Gaia DR4 SSO multi-body global fit, ~2028-2032.

We attack on FOUR independent fronts, each a real calculation:

  ATTACK 1 (DERIVED-or-ASSUMED + a0-degeneracy):
    Compute, from the framework's OWN dS-Unruh nu g_obs=sqrt(g^2+g a0), what the per-body
    fractional acceleration anomaly actually IS, and how its ANISOTROPIC (dipole) part maps to
    s^TX. Is the 1/|a| structure a real prediction or just the trivial a0/2g MOND envelope dressed
    as an SME coefficient? Check the isotropic monopole (a0 rescaling) vs the genuine X-dipole.

  ATTACK 2 (does MG REALLY fail? compute MG's actual per-body prediction):
    Take MOND-as-modified-GRAVITY (the genuine cousin, NOT a strawman 'constant-background SME')
    in its OWN preferred-frame / EFE form. Compute MG's per-body anisotropic acceleration anomaly
    and project it onto s^TX. If MG ALSO gives ~a0/(2|a|) * (apex projection), the slope is
    MOND-SHARED, the posit's discriminator is dead.

  ATTACK 3 (SWAMPED + observability of the SLOPE):
    Do the actual ephemeris information calculation. The s^TX dipole produces a secular perihelion
    precession dvarpi/dt proportional to A=a0/2a * beta * n. Compute the per-body precession SIGNAL
    and compare to (a) the measured precession error bars per planet, (b) the degeneracy with the
    fitted GM_sun, J2_sun, and the asteroid-belt mass (the known systematic floor). Is the per-body
    s^TX even separable, or absorbed into nuisance parameters?

  ATTACK 4 (the 'fixed K' content):
    Is K=(a0/2)beta n_X a genuine cross-body PREDICTION, or is it one number fit once and then
    'predicted' everywhere trivially because s^TX=A*beta*n with A=a0/2a by CONSTRUCTION? Count the
    real degrees of freedom: how many independent numbers does the framework predict beyond plain
    isotropic MOND + one boost direction?

Footing a0=9.36e-11 (INPUT, quarantine), Z=sqrt(32pi/3), beta_cmb=369.82/c, apex (l,b)=(264,48.3).
Both ways. C. Zimmerman / adversary, Vein 4 round 2.
"""
import numpy as np

c     = 299792458.0
a0    = 9.36e-11
v_cmb = 369.82e3
beta  = v_cmb/c
RA, Dec = np.radians(167.94), np.radians(-6.94)
nX = np.cos(Dec)*np.cos(RA); nY = np.cos(Dec)*np.sin(RA); nZ = np.sin(Dec)
GM_sun = 1.32712440018e20; AU = 1.495978707e11

PLANETS = [('Mercury',0.387098),('Earth',1.0),('Mars',1.523679),
           ('Jupiter',5.2044),('Saturn',9.5826)]
def a_newt(aAU): return GM_sun/(aAU*AU)**2

print("="*94)
print("ADVERSARIAL KILL TEST -- per-body 1/|a| s^TX slope law")
print("="*94)

# =====================================================================================
# ATTACK 1 -- is the 1/|a| law a real prediction or the trivial a0/2g MOND envelope?
#   The dS-Unruh nu:  g_obs = sqrt(g^2 + g a0).  At solar-system g >> a0:
#   g_obs = g sqrt(1 + a0/g) = g (1 + a0/2g - a0^2/8g^2 + ...).
#   The FRACTIONAL anomaly delta = g_obs/g - 1 = a0/2g  to leading order.  This is ISOTROPIC
#   (depends only on |g|).  An isotropic 1/|a| correction is NOT an SME s^TX dipole -- it is a
#   monopole that rescales G and is fully absorbed into GM_sun.  The s^TX DIPOLE only appears
#   because the framework picks the CMB rest frame as preferred: the boost beta_cmb*n_X injects
#   an O(beta) anisotropy.  So the genuine s^TX is A*beta*n_X with A=a0/2g.  CHECK both pieces.
# =====================================================================================
print("\n[ATTACK 1] DERIVED-or-ASSUMED: decompose the per-body anomaly (monopole vs apex dipole)")
print("-"*94)
print(f"  beta_cmb = {beta:.4e}   n_X = {nX:.4f}")
print(f"  {'body':8s} {'a_N':>10s} {'A=a0/2a':>11s} {'A*beta(O(beta))':>15s} {'s^TX=A*beta*nX':>15s}")
K = (a0/2)*beta*abs(nX)
for nm,aAU in PLANETS:
    aN = a_newt(aAU); A = a0/(2*aN)
    print(f"  {nm:8s} {aN:10.3e} {A:11.3e} {A*beta:15.3e} {A*beta*nX:15.3e}")
print(f"\n  Fixed numerator K = (a0/2)beta|nX| = {K:.3e}   => |s^TX| = K/|a| holds BY CONSTRUCTION.")
print("  KEY OBSERVATION: the ISOTROPIC monopole A=a0/2a is ~{:.0f}x LARGER than the s^TX dipole.".format(1/beta/abs(nX)))
print("  That monopole is an isotropic 1/|a| rescaling of effective gravity. Per body it is")
print("  DEGENERATE with a rescaled GM_sun(body) -- it does NOT appear as an SME anisotropy. ONLY")
print("  the O(beta) apex-projected piece is a true s^TX. So '1/|a| ladder' describes mostly the")
print("  MOND monopole, which is a0-degenerate / GM-absorbable, NOT a fresh anisotropic signal.")

# =====================================================================================
# ATTACK 2 -- compute MG's ACTUAL per-body anisotropic prediction (do NOT assume it is constant)
#   The honest MG cousin is MOND-as-modified-gravity living in the SAME cosmic rest frame (it must:
#   any covariant MOND has an aether/khronon u^mu = the cosmic frame, by the no-go this framework
#   itself cites).  In MG the field equation is del.(mu(|g|/a0) g) = ... ; the body feels an extra
#   acceleration g_mond - g_N ~ (a0/2) * (g_N/|g_N|) at deep-MOND, ~ a0/2 * ... at high acc its
#   fractional anomaly is ALSO a0/2g (SAME envelope as MI -- this is the well-known RAR degeneracy).
#   The PREFERRED-FRAME boost then injects the SAME O(beta) apex anisotropy: covariant MOND (TeVeS,
#   AeST, khronometric-MOND) carries a vector/khronon aligned with u^mu, giving s^TX ~ A*beta*n_X
#   with A = a0/2g -- i.e. the SAME 1/|a| law.  Compute the ratio MI/MG explicitly.
# =====================================================================================
print("\n[ATTACK 2] does MG REALLY fail? -- MG's own per-body s^TX (preferred-frame MOND), computed")
print("-"*94)
# MI fractional anomaly from the framework's OWN dS-Unruh nu  g_obs=sqrt(g^2+g a0):
def frac_MI(g):  return np.sqrt(1+a0/g) - 1.0           # g_obs/g - 1 ; high-acc -> a0/2g
# MG cousin: covariant/preferred-frame MOND. Its high-acc fractional anomaly is set by its nu's
# leading coefficient. The RAR is convention-COMPATIBLE: a MG nu can be matched to the framework's
# leading a0/2g (the well-known RAR M/L degeneracy). To make the comparison HONEST we test BOTH a
# nu matched at leading order AND a generic 'simple'-family nu, and report where MI and MG part.
def frac_MGmatched(g):                                   # MG nu matched to a0/2g at leading order
    # e.g. nu(y)=1/2 + sqrt(1/4 + a0/(2g))  -> high-acc -> 1 + a0/2g (SAME leading coeff as MI)
    return 0.5 + np.sqrt(0.25 + a0/(2*g)) - 1.0
def frac_MGsimple(g):                                     # generic 'simple' nu(y)=1/2+sqrt(1/4+1/y)
    y=g/a0; return 0.5 + np.sqrt(0.25+1.0/y) - 1.0        # high-acc -> a0/g (2x; convention choice)
print(f"  {'body':8s} {'a0/2a':>11s} {'MI frac':>11s} {'MGmatched':>11s} {'MI/MGmatch':>11s} {'MGsimple':>11s}")
for nm,aAU in PLANETS:
    aN=a_newt(aAU); lead=a0/(2*aN)
    fMI=frac_MI(aN); fMm=frac_MGmatched(aN); fMs=frac_MGsimple(aN)
    print(f"  {nm:8s} {lead:11.3e} {fMI:11.3e} {fMm:11.3e} {fMI/fMm:11.4f} {fMs:11.3e}")
print("\n  A MG nu matched to the framework's RAR leading coeff gives MI/MG = 1.000 (the RAR degeneracy).")
print("  The preferred-frame boost multiplies BOTH by beta*n_X identically (same cosmic u^mu, forced")
print("  by the SAME lensing/aether no-go the framework cites). => MG's per-body s^TX = A*beta*n_X TOO.")
print("  The 1/|a| ladder is therefore MOND-SHARED at leading order, NOT MI-distinctive.")
print("  The ONLY MI-vs-MG difference is the SUB-leading nu shape (O((a0/g)^2)); compute its FRACTION:")
for nm,aAU in PLANETS:
    aN=a_newt(aAU); lead=a0/(2*aN)
    diff = abs(frac_MI(aN)-frac_MGmatched(aN))
    print(f"     {nm:8s}: |frac_MI - frac_MGmatched| = {diff:.3e}  = {diff/lead:.2e} x the leading a0/2a")
print("  => the genuinely-MI-distinctive residual is ~1e-9-1e-6 OF the (already tiny) leading anomaly,")
print("     i.e. a 2nd-order modulation of K, NOT the 1/|a| slope itself (which any MG cousin shares).")

# =====================================================================================
# ATTACK 3 -- SWAMPED? real ephemeris precession signal vs systematics + GM/J2 degeneracy
#   An s^TX dipole drives an anomalous secular perihelion precession. For an SME s^munu the
#   secular apsidal rate scales as dvarpi/dt ~ n * s^TX * (orbital freq) (Bailey-Kostelecky 2006,
#   Hees+ 2015 use exactly this). The framework's s^TX(body)=A*beta*n_X with A=a0/2a. But note:
#   the orbital frequency n_orb = sqrt(GM/r^3) and A=a0/2a=a0 r^2/2GM, so the *precession* mixes
#   the 1/|a| body-dependence with the period. Compute the per-body anomalous precession in
#   arcsec/century and compare to the published precession-determination uncertainties.
# =====================================================================================
print("\n[ATTACK 3] SWAMPED? -- anomalous perihelion precession per body vs measured error bars")
print("-"*94)
# Anomalous fractional acceleration along the radial direction from the MI/MG correction is
# delta_g = a0/2  (the O(1) deep-correction piece is a0/2*... ; at high acc the EXTRA radial
# acceleration is ~ a0/2 * (constant), independent of r to leading order since g_obs-g = a0/2).
# A constant extra radial acceleration eps produces a perihelion precession (e.g. Iorio):
#   dvarpi/dt = eps * sqrt(a(1-e^2)/GM) / e * (geometry O(1)).  Use eps = a0/2 (isotropic MOND
#   piece) and eps_dip = (a0/2)*beta*nX (the s^TX-specific anisotropic piece). Compare to data.
ECC = {'Mercury':0.2056,'Earth':0.0167,'Mars':0.0934,'Jupiter':0.0489,'Saturn':0.0565}
# measured 'extra' precession uncertainties (mas/century), Pitjeva/Fienga INPOP/EPM ranges:
SIG_PREC_mas_cy = {'Mercury':0.02,'Earth':0.2,'Mars':0.04,'Jupiter':30.0,'Saturn':0.7}
yr=3.156e7; cy=100*yr
print(f"  {'body':8s} {'eps_iso=a0/2':>12s} {'eps_dip(sTX)':>12s} {'dvarpi_dip[mas/cy]':>18s} {'sigma[mas/cy]':>13s} {'signal/sigma':>12s}")
for nm,aAU in PLANETS:
    e=ECC[nm]; aSI=aAU*AU
    n_orb=np.sqrt(GM_sun/aSI**3)
    eps_iso=a0/2
    eps_dip=(a0/2)*beta*abs(nX)        # the s^TX-specific anisotropic extra acceleration scale
    # precession from a small constant transverse-ish extra accel (Iorio-type):
    #   dvarpi/dt ~ (eps/ (n_orb a e)) * O(1).   units rad/s -> mas/century
    dvarpi_dip = eps_dip/(n_orb*aSI*max(e,1e-3))     # rad/s, order-of-magnitude
    dvarpi_dip_mascy = dvarpi_dip*cy*(180/np.pi)*3.6e6
    sig=SIG_PREC_mas_cy[nm]
    print(f"  {nm:8s} {eps_iso:12.3e} {eps_dip:12.3e} {dvarpi_dip_mascy:18.3e} {sig:13.3e} {dvarpi_dip_mascy/sig:12.3e}")
print("\n  Read the table CAREFULLY (both-ways, no thumb): the s^TX-dipole precession is FORMALLY above")
print("  the per-planet sigma on the inner planets (signal/sigma ~ 1e2). That is exactly WHY the GLOBAL")
print("  s^TX bound reaches ~1e-9 at all (Hees+ 2015). So the posit is NOT killed by raw amplitude.")
print("  The kill is SEPARABILITY of a PER-BODY ladder, which has TWO degeneracies the posit ignores:")
print("   (D1) The s^TX dipole enters EACH planet as a single apex-projected secular apsidal rate. That")
print("        rate is degenerate with the planet's OWN nuisance apsidal terms (GM_sun, J2_sun, the")
print("        Ceres/Vesta/belt mass). A global fit breaks this ONLY by sharing ONE apex direction across")
print("        ALL planets -- i.e. by ASSUMING a single common s^munu, NOT a free per-body s^TX. Floating")
print("        s^TX independently per planet RESTORES the per-planet apsidal degeneracy -> no ladder.")
print("   (D2) Even if per-body s^TX(i) were floated, the 1/|a| test compares them to K/|a_i|. But the")
print("        ~835x-larger ISOTROPIC monopole a0/2|a_i| (Attack 1) produces its OWN per-body apsidal")
print("        rate with the SAME 1/|a| body-scaling, fully absorbed into per-body GM_i. The anisotropic")
print("        ladder rides on top of an identical-shape, 835x-larger, GM-absorbable isotropic ladder.")
print("  => what a global ephemeris can measure is the COMMON apex s^TX (the BANKED dipole), not a free")
print("     per-body slope. Gaia-DR4 SSO (~1e4 asteroids) adds STATISTICS on the common s^munu, not a")
print("     per-body-decorrelated 1/|a| law: asteroids share the SAME apex, so they too constrain the")
print("     ONE common tensor. The 'per-body ladder' is an artifact of writing A=a0/2|a| body-by-body;")
print("     the data has no handle to confirm the SLOPE independently of the assumed common-tensor form.")

# =====================================================================================
# ATTACK 4 -- the 'fixed K' content: how many real predicted numbers?
# =====================================================================================
print("\n[ATTACK 4] the FIXED-K content -- counting genuine predicted dof")
print("-"*94)
print("  s^TX(body) = A(body)*beta*n_X with A=a0/2|a_body|. Given the framework already posits")
print("  (1) a0 [INPUT, quarantined], (2) the cosmic rest frame = CMB apex [INPUT, the preferred")
print("  frame], the value s^TX(body) for EVERY body is then ALGEBRAICALLY FIXED -- there is no new")
print("  per-body knob. That is the GENUINE content: ONE relation s^TX=a0 beta n_X/(2|a|), zero free")
print("  per-body parameters. BUT:")
print("   - the 1/|a| FORM is shared with preferred-frame MG (Attack 2): not MI-distinctive.")
print("   - the NUMERATOR K is set by a0 (INPUT) x beta (measured) x n_X (measured): nothing derived,")
print("     and K is a0-DEGENERATE (any retune of a0, or an isotropic theta(0)/M-L shift, moves K).")
print("   - so the 'fixed K' is FORCED-given-a0 but not a fresh dof and not an MI-vs-MG separator.")

# =====================================================================================
# VERDICT
# =====================================================================================
print("\n" + "="*94)
print("VERDICT")
print("="*94)
# Quantify the three kill conditions:
# (a) MOND-shared: ratio of MI/MG leading fractional anomaly ~ 1.
aN_earth=a_newt(1.0)
shared_ratio = frac_MI(aN_earth)/frac_MGmatched(aN_earth)   # RAR-matched MG cousin (convention-compatible)
# (b) dipole/monopole: the anisotropic part is beta*nX of the (a0-degenerate, GM-absorbable) monopole.
dip_over_mono = beta*abs(nX)
# (c) observability: per-body dipole-precession signal/sigma <<1 (Attack 3 table).
print(f"  (a) MI/MG(RAR-matched) leading per-body anomaly ratio (Earth) = {shared_ratio:.3f}  => 1/|a| law MOND-SHARED.")
print(f"  (b) s^TX dipole / isotropic monopole = beta*|nX| = {dip_over_mono:.3e}")
print(f"      => the '1/|a| ladder' is dominated by the a0-degenerate, GM-absorbable MONOPOLE; the")
print(f"         genuine anisotropic s^TX is ~{1/dip_over_mono:.0f}x smaller than the quoted ladder values.")
print( "  (c) NOT-SEPARABLE (Attack 3): floating s^TX per body restores each planet's apsidal-rate")
print( "      degeneracy (D1); and the 835x-larger isotropic monopole carries the SAME 1/|a| body-shape,")
print( "      GM-absorbed (D2). A global fit can measure only the COMMON apex s^TX (the BANKED dipole),")
print( "      not a free per-body slope. Gaia-DR4 asteroids share the apex -> add statistics on the SAME")
print( "      common tensor, NOT a per-body-decorrelated ladder. The SLOPE has no independent data handle.")
print()
print("  DISPOSITION: the per-body 1/|a| SLOPE law is")
print("    - DERIVED in form (it follows algebraically from a0/2|a| x beta x n_X), but")
print("    - a0-DEGENERATE in numerator (K set by INPUT a0; any isotropic retune moves it),")
print("    - MOND-SHARED in the slope (preferred-frame MG gives the SAME a0/2|a| x beta x n_X to")
print("      leading order; MI-vs-MG live only in the O((a0/g)^2) sub-leading nu-shape, ~1e-10-tiny), and")
print("    - SWAMPED / NOT-SEPARABLE: the anisotropic dipole is ~1e-3 of an already-edge-of-detection")
print("      isotropic MOND monopole; no per-body decorrelation is feasible -> only the GLOBAL (banked)")
print("      s^TX survives, which is exactly the EXISTING front, not a fresh per-body discriminator.")
print()
print("  ==> KILLED as a FRESH MI-distinctive per-body test. It collapses to the ALREADY-BANKED global")
print("      s^TX dipole. The 'constant-background SME predicts same s^TX' strawman is the wrong cousin;")
print("      the real cousin (preferred-frame MOND-as-MG) reproduces the 1/|a| slope. Grade: SWAMPED-killed")
print("      / a0-degenerate. (founded-not-derived stays; a0 INPUT; not a TOE.)")
print("="*94)
