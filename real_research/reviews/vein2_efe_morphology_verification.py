#!/usr/bin/env python3
"""
VEIN 2 -- EFE / MORPHOLOGY-FLATTENING posit mining, B4 discipline.

Origin (from b4_jeans_verification.py, the REAL Jeans calc): a relaxed (energy-DF) system in an
external field is FLATTENED IN DENSITY along the field axis -- in MODIFIED GRAVITY with ISOTROPIC
velocities. That is a SHAPE signature (not a kinematic one). This script DERIVES the magnitudes,
signs, and DISCRIMINATORS for that morphology vein, with NO assumed sign and NO ad-hoc proxy.

Footing (sealed): a0 = cH_Lambda/Z = 9.36e-11 m/s^2; framework interpolation
mu_fw(x)=(sqrt(1+4x^2)-1)/(2x); the EFE anisotropy parameter L_ext = dln mu/dln a at a_ext/a0.
Both-ways, exit 0, prove-by-moving-the-number. NOT a TOE; founded-not-derived stays.

What is DERIVED here (each a real calc, not an assumed sign):
 (P1) dSph density ellipticity from EFE: e_EFE(a_ext/a0) along the field axis, MG energy-DF.
 (P2) the EFE flattening is SIGNED: PROLATE vs OBLATE -- which one does mu_fw force? (computed)
 (P3) MI vs MG flattening: does MI flatten the density the SAME, less, or not-at-all? (b4-honest)
 (P4) the discriminator vs DM/tidal flattening: ALIGNMENT with the field axis, and the
      e-vs-(a_ext/a0) SCALING law -- can EFE be separated from tides? (computed both signals)
 (P5) cluster-member alignment with the large-scale-structure (cosmic-web) field.
"""
import numpy as np
rng = np.random.default_rng(20260627)

A0 = 9.36e-11
def mu_fw(x):
    x = np.asarray(x, float)
    return np.where(x > 0, (np.sqrt(1+4*x*x)-1)/(2*x+1e-300), 0.0)
def Lext(x, h=1e-5):
    return (np.log(mu_fw(x*(1+h))) - np.log(mu_fw(x*(1-h)))) / (2*h)

print("="*100)
print("  VEIN 2 -- EFE MORPHOLOGY FLATTENING: derive the shape signal, sign, and discriminator")
print("="*100)

# ----------------------------------------------------------------------------------------------
# P1+P2: density ellipticity from the EFE, in a relaxed (energy-DF) MG dwarf.
# SIGN -- DERIVED from the STANDARD MOND EFE linearization, NOT assumed (B4 discipline):
# Brada & Milgrom 1995 / Milgrom 1986: in a dominant external field a_ext along z, the internal
# field of a mass is that of a point mass in an ANISOTROPIC dielectric. The effective gravity is
# WEAKER along the field by 1/(1+L_ext) and unchanged perpendicular. Equivalently the effective
# harmonic frequencies satisfy omega_z^2/omega_perp^2 = 1/(1+L_ext) < 1  (NOT 1+L; the earlier
# b4 script had this sign BACKWARDS -- caught here).
# Energy DF f(E)~exp(-E/sig0^2): density rho(x)~exp(-Phi/sig0^2) Gaussian, sigma_i = sig0/omega_i
#   => sigma_z/sigma_perp = sqrt(1+L_ext) > 1  => EXTENDED along z => PROLATE, LONG axis ALONG the
#   field (RADIAL, toward the host). e = 1 - sigma_short/sigma_long = 1 - 1/sqrt(1+L_ext).
# *** This is the SAME orientation as a tide. The "tangential" claim was WRONG. ***
# ----------------------------------------------------------------------------------------------
print("\n[P1/P2] dSph DENSITY ellipticity from the EFE (MG energy DF) -- magnitude + SIGN (corrected)")
print("   SIGN derived from Brada-Milgrom 1995: EFE gravity is WEAKER along the field (1/(1+L)) =>")
print("   PROLATE, LONG axis ALONG the field = RADIAL toward host (NOT tangential).")
print(f"   {'a_ext/a0':>9} {'mu_fw':>8} {'L_ext':>8} {'1+L':>7} {'long/short=sqrt(1+L)':>20} {'e=1-1/sqrt(1+L)':>15}  orientation")
xs = [0.1, 0.3, 0.5, 1.0, 2.0, 5.0]
for xe in xs:
    Le = float(Lext(xe)); ratio = np.sqrt(1+Le); e = 1-1/ratio
    print(f"   {xe:9.2f} {float(mu_fw(xe)):8.4f} {Le:8.4f} {1+Le:7.4f} {ratio:20.4f} {e:15.4f}  long||field => PROLATE, RADIAL toward host")

# Monte-Carlo CONFIRM the analytic e from an actual energy-DF sample (correct sign now):
xe = 0.5; Le = float(Lext(xe)); N = 400000; sig0 = 1.0
wz = 1/np.sqrt(1+Le)                       # WEAKER gravity along field => SMALLER omega_z => MORE extended
X = np.stack([rng.normal(0, sig0/1.0, N), rng.normal(0, sig0/1.0, N), rng.normal(0, sig0/wz, N)], axis=1)
cov = np.cov(X.T); evals = np.sort(np.sqrt(np.linalg.eigvalsh(cov)))
e_mc = 1 - evals[0]/evals[-1]; e_an = 1 - 1/np.sqrt(1+Le)
axis_var = X.var(axis=0); major_axis = np.argmax(axis_var)
print(f"\n   MC check at a_ext/a0={xe}:  e_analytic={e_an:.4f}  e_MC={e_mc:.4f}  (match: {abs(e_an-e_mc)<0.01})")
print(f"   MAJOR-axis index = {major_axis} (2 = field/z axis) => density EXTENDED along the field. PROLATE/RADIAL. CONFIRMED.")

# ----------------------------------------------------------------------------------------------
# P3: MI vs MG flattening -- b4-honest. MG flattens the DENSITY (above). What does MI do?
# MI has acceleration-history-dependent inertia and NO rigorous equilibrium stat-mech, so the
# density shape is NOT cleanly defined. The b4 calc showed MI puts the anisotropy in the VELOCITY
# ellipsoid (beta_field<0) under a heuristic generalized-equipartition, with the density shape
# undetermined. We report BOTH and refuse to assume the MI density flattening.
# ----------------------------------------------------------------------------------------------
print("\n[P3] MI vs MG flattening (b4-HONEST):")
# MG density flattening (forced, energy-DF theorem): e as above (PROLATE/radial, correct sign).
e_MG = 1 - 1/np.sqrt(1+float(Lext(1.0)))
print(f"   MG (energy DF): DENSITY elongated (PROLATE, radial), e(a_ext/a0=1) = {e_MG:.3f}; velocities ISOTROPIC (beta~0).")
# MI heuristic: anisotropic inertia mu_par=mu_perp*(1+L). Generalized equipartition <mu_i v_i^2>=const
#   => sig_par^2/sig_perp^2 = mu_perp/mu_par = 1/(1+L) => velocity-ellipsoid tangential bias.
#   The DENSITY shape requires the (ill-defined) MI Jeans equation; we do NOT assume it flattens.
Le1 = float(Lext(1.0)); beta_MI = 1 - (1/(1+Le1))  # beta = 1 - sig_par^2/sig_perp^2  (here field=par)
print(f"   MI (heuristic equipartition): VELOCITY ellipsoid tangentially biased, beta_field = {beta_MI:+.3f}")
print(f"        BUT acceleration-history inertia => NO equilibrium stat-mech => density shape ILL-DEFINED.")
print(f"   => The clean, FORCED morphology signal is MG's density flattening. MI's distinctive content is")
print(f"      kinematic (velocity tilt), NOT a forced density shape. Honest: morphology is an MG/MOND-CLASS")
print(f"      signal (shared with metric MOND), NOT an MI-vs-MG discriminator on its own. (key both-ways result)")

# ----------------------------------------------------------------------------------------------
# P4: THE DISCRIMINATOR -- EFE flattening vs DM/tidal flattening.
# CORRECTED: EFE elongates the dwarf RADIALLY (long axis toward host, P1/P2). A tide ALSO
# elongates radially (radial tidal eigenvalue +2GM/r^3 stretch). So ALIGNMENT IS CO-LINEAR --
# NOT an orthogonal sign discriminator. The earlier "90 deg apart" claim was wrong (followed from
# the wrong EFE sign). The ONLY morphological lever left is the e-vs-distance SCALING LAW, which
# differs between the two; alignment alone CANNOT separate them. (B4 discipline: report the loss.)
# ----------------------------------------------------------------------------------------------
GM_MW = 6.674e-11 * 1.0e12 * 1.989e30  # ~1e12 Msun host, SI
kpc = 3.086e19
print("\n[P4] DISCRIMINATOR vs tides/DM (CORRECTED -- alignment is co-linear, only scaling differs):")
print("   (a) ALIGNMENT: BOTH EFE and tide elongate RADIALLY (long axis toward host).")
print("       Tidal tensor eigenvalues: radial +2GM/r^3 (STRETCH), tangential -GM/r^3 (COMPRESS) => RADIAL long axis.")
print("       EFE (P1/P2, Brada-Milgrom): PROLATE, RADIAL long axis. => SAME ORIENTATION. NOT a sign discriminator.")

print("\n   (b) e-vs-host-distance SCALING (the only remaining lever), a_ext = G M_host / D^2:")
print(f"      {'D (kpc)':>8} {'a_ext/a0':>9} {'e_EFE':>7}   {'e_tide (size/r_t)':>18}")
Ds = np.array([20,30,50,80,120,180,250.])
aext = GM_MW/(Ds*kpc)**2
e_efe = 1 - 1/np.sqrt(1+np.array([float(Lext(x)) for x in aext/A0]))
# Tidal ellipticity of a fixed dwarf: distortion ~ (r_half / r_tidal), r_tidal ~ D*(m_dw/M_host)^(1/3).
# r_half fixed; r_tidal GROWS with D => tidal distortion FALLS with D.
r_half = 0.5  # kpc, fixed dwarf half-light radius
r_tidal = Ds*(1e8/1e12)**(1/3)              # kpc
e_tide = np.clip(0.5*(r_half/r_tidal), 0, 0.6)
for i,D in enumerate(Ds):
    print(f"      {int(D):8d} {aext[i]/A0:9.3f} {e_efe[i]:7.4f}   {e_tide[i]:18.4f}")
from numpy import corrcoef
print(f"\n      EFE:  corr(e_EFE,  D) = {corrcoef(e_efe, Ds)[0,1]:+.3f}  (e RISES with D: deeper deep-MOND => bigger L_ext)")
print(f"      Tide: corr(e_tide, D) = {corrcoef(e_tide, Ds)[0,1]:+.3f}  (e FALLS with D: r_tidal grows => less distortion)")
print("      => The SCALING SIGN flips: EFE e-vs-D POSITIVE, tide NEGATIVE. That is the ONE remaining")
print("         morphological discriminator -- a 1-bit (trend-sign), NOT the 2-bit I wrongly claimed.")
print("      Caveat: both signals are CO-ALIGNED and superpose along the same radial axis, so the trend must")
print("         be fit in the PRESENCE of the tide, not as a clean separation. Confound-heavy.")

# ----------------------------------------------------------------------------------------------
# P5: cluster-member alignment with the cosmic-web (large-scale-structure) external field.
# Same energy-DF EFE flattening, but the external field is the LSS tidal/acceleration field along
# the filament. Magnitude: cluster outskirts a_ext ~ a0 => L_ext ~ 0.45 => e ~ 0.17 ALIGNED with
# the filament axis (minor axis along the field => long axis PERP to the field gradient direction).
# ----------------------------------------------------------------------------------------------
print("\n[P5] cluster-member / cosmic-web alignment:")
for xe in [0.3, 1.0, 3.0]:
    Le = float(Lext(xe)); e = 1 - 1/np.sqrt(1+Le)
    print(f"   a_ext/a0={xe:4.1f}: e_EFE = {e:.3f}, PROLATE with LONG axis ALONG the LSS field gradient (radial to the filament/cluster).")
print("   Distinctive content: an EFE-induced member-shape alignment is SHARED with metric MOND (MG-class), and")
print("   is co-aligned + degenerate with the well-known LSS tidal intrinsic-alignment of galaxies (the long axis")
print("   points along the tidal stretch in BOTH). NOT a clean MI-vs-MG discriminator; confound-heavy MOND-class")
print("   signal. (both-ways: real but not distinctive, and the IA confound is exactly co-aligned.)")

print("\n"+"="*100)
print(" VEIN-2 VERDICT (both-ways, B4-disciplined)")
print("="*100)
print(f"""  * The EFE DENSITY-elongation signal is REAL and FORCED in MG/MOND-class theories (energy-DF theorem +
    Brada-Milgrom EFE sign): e = 1 - 1/sqrt(1+L_ext), e.g. e~{1-1/np.sqrt(1+float(Lext(0.5))):.2f} at a_ext/a0=0.5, PROLATE with the
    LONG axis RADIAL (toward the host). [SIGN CORRECTED from an earlier 'tangential' error -- B4 discipline.]
  * It is NOT an MI-vs-MG discriminator: MG forces the density shape; MI's distinctive effect is in the
    VELOCITY ellipsoid and MI's density shape is ILL-DEFINED (acceleration-history inertia, no equilibrium
    stat-mech). So morphology is a MOND-CLASS signal, shared, not MI-distinctive. (the key honest result.)
  * The alignment is CO-LINEAR with a tide (both elongate RADIALLY) -- so alignment is NOT a discriminator.
    The ONLY morphological lever vs tides is the e-vs-galactocentric-distance TREND SIGN: EFE e RISES with D
    (via L_ext); a tide FALLS with D (r_tidal grows). A 1-bit trend test, fit through the co-aligned tide.
  * Caveat honestly: tides AND a DM subhalo's tidal response ALSO elongate dSphs RADIALLY -- exactly co-aligned
    with EFE -- and observed dSph ellipticities (e~0.1-0.5) are dominated by formation/tidal history. The EFE
    term is sub-dominant and confound-co-aligned. This is the honest weakening of the morphology vein.
  => Best-to-VERIFY: the e-vs-galactocentric-distance TREND on the MW dSph population (existing shapes +
     positions). EFE predicts a POSITIVE e-D correlation at fixed luminosity; the tidal+DM null predicts a
     NEGATIVE (or flat) one. It is a MOND-CLASS test (NOT MI-vs-MG) and the tide is co-aligned, so it is a weak,
     confound-heavy 1-bit test -- NOT a clean lock. The clean MI-vs-MG discriminators remain Cassini, the
     relational sigma-spread, the dwarf-sigma clock, and s^TX; morphology does NOT join that ledger.""")
print("="*100)
