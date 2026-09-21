"""L310 -- THE INSTRUMENT SWEEP: every observational instrument, the frame's committed prediction vs LCDM,
the discriminator and the recipe.  All numbers are the committed lanes (no new physics: the mapping of the
closed linear cosmology onto the instruments).  The synthesis row: the three-instrument cluster test
(X-ray / lensing / SZ) with the frame's bias direction and magnitude."""
import json, os
ROWS = [
    # instrument | frame (lane) | LCDM | discriminator | recipe
    ("rotation curves (HI/CO/optical, outer halo)", "198/205/216 km/s at 30-100 kpc vs the 165 MOND-flat; d ln v/d ln r = +0.10..0.15 over 20-60 kpc (L305)", "flat-to-declining CDM halos", "SIGN and SIZE of the outer slope", "Gaia-RVS + blue-HB halo stars at 20-100 kpc"),
    ("weak lensing, galaxy halo", "outer slope steepening -2.0 -> -2.5; inner active cusp -1.71 MW class (L304/L309)", "-2.00 envelope / NFW -1.5 flat", "the outer-halo lensing slope", "stacked weak-lensing profiles (DECaPS/CFHT), 30-100 kpc bins"),
    ("the RAR (stacked dynamics)", "a0 = 9.3619e-11 with kappa = 1/2, NOT a fit (PD08); scatter = bias 1 by construction", "a0 fitted, scatter from halo variance", "the intercept's curvature at g_N -> 0", "the SPARC + stacked samples at g_N < 0.1 a0"),
    ("strong lensing (Einstein radii)", "interior active fraction ~0.5 x M_b at 5-20 kpc -> theta_E shrinks by ~0.8 (L304 profiles)", "NFW-halo theta_E (mass-concentration-sensitive)", "the lens-ellipticity distortion", "SLACS/LENSCOLD lenses with resolved velocity profiles"),
    ("clusters: X-ray hydrostatic vs lensing", "M_lens/M_X ~ 1.18 (L309: 4.9 vs 4.14x at delta_b = 70)", "M_X < M_lens (HSE bias) by ~10-20%", "the bias MAGNITUDE at fixed gas T", "X-ray (Chandra/XMM) + stacked lensing on the same R500-interior"),
    ("clusters: SZ", "the carrier's cold gas arrives at Mach 9.5 (L294): the kinetic-SZ of the infall adds to the thermal", "thermal-only SZ", "the SZ signal outside the virialized core", "SZ imaging (SPT/ACT) with the infall-region masks"),
    ("clusters: caustic stacks (g04a)", "-1.87 band slope; mass-dependent (MW -1.71, cluster -1.55 active faces) (L294/L298/L309)", "-1.5 at every mass (NFW)", "the rise of cuspiness with mass", "caustic stacks vs weak-lensing halo mass"),
    ("CMB peaks", "peak-window ratio 0.314 vs LCDM 0.315, FLAT across c_s^2 in {1e-11..1e-9} (L308b); the full face 0.991 vs 0.992 (L292)", "0.992 (measured)", "the third-peak flatness of the carrier's sound window", "Planck TT"),
    ("CMB - recombination epoch", "baryons-only face 1.192 vs 0.992: the third peak EXCLUDES the framework's baryons-only face at ~20-sigma (L295): the answer is the baryon-seeded dust (L307: R = 1.0000, alpha = 0)", "n/a", "the peak budget", "Planck TT (committed falsifier)"),
    ("LSS P(k) / BAO", "P/P_LCDM = 0.973/0.967/0.963 (z = 3), 0.987/0.983/0.974 (z = 0) (L292); BAO phase identical (adiabatic seeding)", "1.00", "the BAO phase at fixed amplitude", "BOSS/DESI LRGs"),
    ("LSS growth / f-sigma8", "sigma8 ratio 1.000000 with the sound-term error < 1e-4 at the LSS cells (L306/L308)", "1.00", "the growth budget slope", "RSD (BOSS/DESI)"),
    ("LSS - the forest", "c_s(z = 3) = 6.7 km/s <= 9.5 (L290): the carrier identical to CDM at the forest scales with the cold kinematic floor", "CDM (c_s = 0)", "the small-scale cutoff", "Ly-alpha forest P(k), k = 5 h/Mpc"),
    ("dwarf satellites (L166)", "c_s(alpha = 0.315) = 251 km/s: retained fraction 1.1e-4 <= 0.105 (L290-V6)", "CDM halos (retain everything)", "the dwarf-mass dependence of retention", "the Classical dSphs' phase space (Gaia DR3 proper motions)"),
    ("galaxy dynamics vs lensing (the slip)", "Psi = Phi to leading order, slip 4e-7; G_N = G/(1 - c14/2) (L279, Lean)", "1.000 GR", "the slip at the 1e-6 level", "resolved stellar kinematics vs lensing in the same galaxies"),
    ("wide binaries", "gamma_v = 1.000 (Amend 11)", "1.000 (GR)", "gamma_v at the 1e-3 level", "Gaia wide-binary astrometry"),
    ("the binary-pulsar strong field", "c_T = c, GW170817-consistent; PPN gamma = beta = 1 in the strong field (L280)", "1.000 GR", "the dipole radiation absence", "double-neutron-star timing (PSR J0737)"),
    ("the solar system (PPN)", "alpha_2 passes at c14 <= 8e-7 or the equal-speed locus c2 = c14/(1 - 2 c14) (L280, Lean); Cassini-consistent", "GR", "alpha_2 at 1e-7", "LAGEOS/GP-B frame-dragging, Cassini"),
    ("the S8 tension", "sigma8(carrier)/sigma8(LCDM) = 1.000000: the frame does NOT reproduce the S8 tension: it predicts the LCDM value (L306) -- a statement, not a cure", "the observed S8 ~ 0.76-0.83 (tension with Planck)", "the growth budget", "all RSD+lensing combinations"),
]
print("L310 -- THE INSTRUMENT SWEEP (all numbers committed):\n")
for i, (inst, fr, lcdm, disc, rec) in enumerate(ROWS, 1):
    print(f"  {i:2d}. {inst}\n      frame: {fr}\n      LCDM:  {lcdm}\n      discriminator: {disc}\n      recipe: {rec}\n")
n = len(ROWS)
synthesis = ("THE THREE-INSTRUMENT CLUSTER TEST: the frame predicts M_lens/M_X ~ 1.18 at fixed gas temperature "
             "(4.9 vs 4.14x, L309), the SZ to carry the infall's kinetic signature outside the virialized core "
             "(Mach 9.5, L294), and the caustic slope to rise with mass (-1.71 MW -> -1.55 cluster active faces). "
             "LCDM predicts M_X < M_lens (the HSE bias), thermal-only SZ, and a mass-FLAT -1.5 cusp.  Three "
             "instruments, three directional differences, one model.")
print("SYNTHESIS: " + synthesis)
json.dump(dict(rows=ROWS, synthesis=synthesis, n=n),
          open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1)
print(f"\nL310 COMPLETE: {n} instrument rows committed")
import sys; sys.exit(0)