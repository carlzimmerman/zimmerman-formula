#!/usr/bin/env python3
"""
THIRD CHANNEL: the KiDS weak-lensing RAR -> a0 -> Lambda.
Does the acceleration scale read off LENSING GEOMETRY (Brouwer et al. 2021, A&A 650 A113,
KiDS-1000) land on the same Planck Lambda that rotation DYNAMICS (SPARC) and the
EXPANSION history (SNe/DESI) do?  Closing a dynamics-geometry-expansion triangle.

KEY FACTS (verified from the paper, pdftotext + A&A HTML):
  - lensing RAR spans 1e-15 < g_bar < 5e-12 m/s^2  -> reaches ~5 DECADES below a0,
    ~3 decades deeper than the deepest rotation curve. Ultra-deep MOND.
  - Brouwer ADOPT (not free-fit) g_dagger = a0 = 1.20 +/- 0.26 e-10 (McGaugh 2016) and
    find the lensing data AGREE with the MOND/MG prediction at that a0.
  - >= 6 sigma difference between early- and late-type RARs at fixed M* (early-types show
    EXCESS g_obs; Brouwer suggest circumgalactic gas M_gas ~ M*). A real systematic.
HONEST SCOPE, carried below: (i) a0 is ADOPTED by Brouwer, so this is a CONSISTENCY, and
an independent lensing-only free-fit of a0 is a FORECAST on their public data; (ii) the
6-sigma morphology split strains a single universal a0 (clean case = late-type disks);
(iii) THE DISFORMAL WRINKLE -- in THIS (modified-INERTIA) framework, lensing does NOT
share the matter metric: it runs through the published disformal photon sector
(g~ = g + B uu; lensing no-go DOI 21418816 + the disformal completion). So lensing-a0 =
dynamical-a0 is a PREDICTION of that completion, not automatic (unlike single-metric MG).
This calculation therefore ALSO tests the disformal sector. Both a0 footings.
"""
import numpy as np
c = 2.99792458e8
LAM_PLANCK = 1.089e-52
A0_LENS, A0_LENS_E = 1.20e-10, 0.26e-10   # Brouwer-adopted g_dagger (McGaugh 2016)
A0_CANON = 9.355e-11                       # framework canonical (Lambda=Planck by construction)
A0_ALT   = 1.1305e-10                       # alternative footing (rho_total, cH0)
A0_SPARC, A0_SPARC_LO, A0_SPARC_HI = 1.181e-10, 0.84e-10, 1.36e-10   # a0-line SPARC box
A0_SNE_LO, A0_SNE_HI = 9.17e-11, 9.93e-11  # SNe-demanded a0 (side_by_side.py, H0 67.4->73)

def lam(a0): return 32*np.pi*a0**2/c**4     # Lambda = 32 pi a0^2 / c^4

print("="*76)
print("1. INVERT THE LENSING a0 TO LAMBDA, COMPARE TO PLANCK")
print("="*76)
L = lam(A0_LENS); Llo = lam(A0_LENS-A0_LENS_E); Lhi = lam(A0_LENS+A0_LENS_E)
print(f"  KiDS-adopted a0 = {A0_LENS:.2e} +/- {A0_LENS_E:.2e} m/s^2")
print(f"  Lambda_lensing  = 32 pi a0^2 / c^4 = {L:.3e} [{Llo:.3e}, {Lhi:.3e}] m^-2")
print(f"  Lambda_Planck   = {LAM_PLANCK:.3e} m^-2")
print(f"  ratio Lambda_lens/Lambda_Planck = {L/LAM_PLANCK:.2f}  [{Llo/LAM_PLANCK:.2f}, {Lhi/LAM_PLANCK:.2f}]")
sig = abs(L-LAM_PLANCK)/((Lhi-Llo)/2)
print(f"  Planck Lambda sits {sig:.2f} sigma from the lensing central -> {'CONSISTENT' if sig<2 else 'TENSION'} (factor {L/LAM_PLANCK:.1f}, same 'high-side-of-box' as SPARC)")
# HONEST FRAME NOTE: the sigma above is computed in Lambda-space with a linearized half-width.
# In a0-space (Planck-equivalent a0 = sqrt(Lambda_Planck c^4/32pi)) the same comparison is:
a0_planck = np.sqrt(LAM_PLANCK*c**4/(32*np.pi))
print(f"  [frame check] a0-space: Planck-equiv a0={a0_planck:.3e}; |a0_lens-a0_planck|/sig_a0 = {abs(A0_LENS-a0_planck)/A0_LENS_E:.2f} sigma (also CONSISTENT; Lambda-space gives the smaller number)")
print(f"  --- both footings of a0 (Lambda by construction on canonical) ---")
print(f"  canonical a0={A0_CANON:.3e} -> Lambda={lam(A0_CANON):.3e} = {lam(A0_CANON)/LAM_PLANCK:.2f}x Planck (=Planck by construction)")
print(f"  alt       a0={A0_ALT:.4e} -> Lambda={lam(A0_ALT):.3e} = {lam(A0_ALT)/LAM_PLANCK:.2f}x Planck")

print("\n" + "="*76)
print("2. INTERPOLATION-INDEPENDENCE OF THE a0 EXTRACTION AT g_bar = 1e-15 (ultra-deep MOND)")
print("="*76)
gbar = 1e-15
# framework a0-line: g_obs^2 = g_bar^2 + g_bar a0
g_fw  = np.sqrt(gbar**2 + gbar*A0_LENS)
# Brouwer 'third family': g_obs = g_bar/(1 - exp(-sqrt(g_bar/a0)))
g_b3  = gbar/(1 - np.exp(-np.sqrt(gbar/A0_LENS)))
# pure deep-MOND: g_obs = sqrt(a0 g_bar)
g_dm  = np.sqrt(A0_LENS*gbar)
print(f"  at g_bar={gbar:.0e} (y=g_bar/a0={gbar/A0_LENS:.1e}):")
print(f"    framework nu-kernel  g_obs = {g_fw:.6e}")
print(f"    Brouwer third-family g_obs = {g_b3:.6e}")
print(f"    pure deep-MOND       g_obs = {g_dm:.6e}")
print(f"    max fractional spread = {max(abs(g_fw-g_dm),abs(g_b3-g_dm))/g_dm:.2e}")
print(f"  -> 5 decades deep, ALL kernels agree: a0 = g_obs^2/g_bar is interpolation-FREE here.")
print(f"     (This is the lensing channel's edge: no interpolation-function ambiguity, unlike")
print(f"      rotation curves which live near y~1. a0 = g_obs^2/g_bar recovers {g_dm**2/gbar:.3e}.)")

print("\n" + "="*76)
print("3. THE DYNAMICS-GEOMETRY-EXPANSION TRIANGLE (all a0 in 1e-10 units)")
print("="*76)
print(f"  DYNAMICS  (SPARC a0-line):        {A0_SPARC*1e10:.2f}  box [{A0_SPARC_LO*1e10:.2f},{A0_SPARC_HI*1e10:.2f}]  (kinematics)")
print(f"  GEOMETRY  (KiDS weak lensing):    {A0_LENS*1e10:.2f} +/- {A0_LENS_E*1e10:.2f}          (lensing, g_bar to 1e-15)")
print(f"  EXPANSION (SNe-demanded, H0-dep): {A0_SNE_LO*1e10:.2f}-{A0_SNE_HI*1e10:.2f}                    (Pantheon+ Hubble diagram)")
print(f"  framework canonical (Lambda=Planck): {A0_CANON*1e10:.2f}")
allc = [A0_SPARC, A0_LENS, (A0_SNE_LO+A0_SNE_HI)/2]
print(f"  three-channel spread: {min(allc)*1e10:.2f}-{max(allc)*1e10:.2f} e-10 (~{100*(max(allc)-min(allc))/np.mean(allc):.0f}% wide),")
print(f"  ALL inside the SPARC systematics box and ALL -> Lambda within a factor ~{lam(max(allc))/LAM_PLANCK:.1f} of Planck.")
print(f"  Three observables with ORTHOGONAL systematics (M/L+inclination vs shear+photo-z vs")
print(f"  SNe-standardization) agree on the acceleration scale to ~30%. Not a precision match; a")
print(f"  genuinely-independent third leg on 'the scale is universal at ~sqrt(Lambda)'.")

print("\n" + "="*76)
print("4. WHY THIS IS A CONSISTENCY, NOT A FREE-FIT (figure-digitization reality + forecast)")
print("="*76)
# In deep MOND (all Brouwer bins have g_bar << a0), log g_obs = 0.5(log g_bar + log a0),
# so a0 = g_obs^2/g_bar and log a0 = 2 log g_obs - log g_bar. Reading Fig. 4 by eye:
print("  Fig. 4 is deep-MOND throughout -> a slope-1/2 line -> a0 = g_obs^2/g_bar (interp-free).")
print("  By-eye digitization of the two lensing samples:")
print("   - KiDS-bright (black, tight bars): PHOTO-Z SELECTION-BIASED HIGH (Brouwer's own caveat)")
print("     -> reads a0 ~ 1-3e-10 (an artifact of the bias + ~0.1-dex reading error), NOT a measurement.")
print("   - GAMA (blue, spectroscopic, RELIABLE): tracks MOND (a0 ~ 1.2e-10) but ~0.2-0.4 dex/point")
print("     intrinsic scatter -> a0 good only to a FACTOR ~2 even with perfect reading.")
print("  => a free-fit from the FIGURE is reading- and scatter-limited; not a precision number.")
print("     (This is exactly why Brouwer FIXED a0 and tested consistency rather than free-fitting.)")
# forecast: what a tabulated per-point free-fit would deliver.
# deep-MOND: log g_obs = 1/2(log a0 + log g_bar) -> the slope-1/2 intercept has sensitivity
# d(log g_obs)/d(log a0)=1/2 -> sigma(log a0) = sigma_point/(1/2 sqrt(N)) = 2 sigma_point/sqrt(N).
# (a0 = g_obs^2/g_bar carries a FACTOR-2 error AMPLIFICATION, not a suppression.)
for tag, sig in [("KiDS-bright per-point ~0.10 dex", 0.10), ("GAMA reliable per-point ~0.30 dex", 0.30)]:
    N=15; stat = 2*sig/np.sqrt(N)       # log a0 statistical error (slope-1/2 intercept; 2x from a0=g_obs^2/g_bar)
    print(f"  FORECAST [{tag}]: 15 bins -> statistical log a0 ~ {stat:.3f} dex -> a0 to ~{100*(10**stat-1):.0f}% statistical")
print("  So statistical alone is ~13% (bright, but photo-z BIASED-HIGH) to ~43% (GAMA reliable/clean).")
print("  The SYSTEMATIC floor (>=6-sigma early/late split + baryonic-mass/deprojection model) is ~15-25%,")
print("  so stat and systematic are COMPARABLE -- neither dominates. A realistic tabulated free-fit reaches")
print("  ~20-28% (biased bright) and ~45-50% (clean late-type/reliable): the gain over the figure's factor~2")
print("  is REAL but MODEST for the clean case (mostly from removing reading error + a late-type selection)")
print("  -- worth doing WHEN the per-point")
print("  table is public (it is not: VizieR has no entry; the portal has only raw ESD profiles).")

print("\n" + "="*76)
print("VERDICT (both ways)")
print("="*76)
print("  WIN-SIDE: lensing geometry -- systematics orthogonal to kinematics, 5 decades below a0")
print("    where NO interpolation ambiguity and NO baryonic effect can mimic -- is CONSISTENT")
print("    with the SAME universal a0 ~ 1.2e-10 -> Lambda within ~1sigma/factor~1.6 of Planck. Third leg.")
print("  CAVEATS (do not skip): (i) Brouwer ADOPTED a0, did not free-fit it -> this is CONSISTENCY;")
print("    the clean independent lensing-a0 fit is a FORECAST on the public KiDS data. (ii) the")
print("    >=6sigma early/late RAR split strains a single a0 (clean case = late-type disks).")
print("    (iii) DISFORMAL WRINKLE: in modified INERTIA lensing runs through the disformal photon")
print("    sector, so lensing-a0 = dynamical-a0 is a PREDICTION of that completion, not automatic;")
print("    the KiDS agreement is CONSISTENT with the disformal sector (a bonus test), NOT independent")
print("    of it. a0's value + Z remain POSITED; the triangle tests universality+scale, not the value.")
print("EXIT 0")
