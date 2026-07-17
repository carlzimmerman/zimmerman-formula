#!/usr/bin/env python3
r"""
POWER-ANALYSIS LANE -- can the STAR-ORBIT-WITHIN-ONE-SYSTEM sigma-spread be detected?  2026-07-17.  Exit 0.
=========================================================================================================
de Sitter-Unruh MODIFIED INERTIA (Zimmerman).  nu(y)=sqrt(1+1/y), y=g_bar/a0, a0=cH_Lambda/Z=9.36e-11.
MI = inertia is a time-NONLOCAL functional of the body's OWN worldline through K(Box_u/a0^2),
tau_mem = 2c/a0 = 2Z/H_Lambda (E10, exact, footing-free).  Milgrom 1983/1999 wellhead credit for the
nu-kernel; distinctive content = the cH_Lambda/Z coefficient + the MI completion.  a0 value + s=-1 postulates.

THE OBSERVABLE (this lane -- DISTINCT from the cluster-member EFE boost of power_analysis.py):
  Individual stars on DIFFERENT orbits inside ONE pressure-supported system (dSph / elliptical / cluster).
  At radius r every star feels the SAME g_bar(r); a LOCAL mu(|a|) gives all the same |a| -> no spread.
  MI's NON-ADIABATIC effect: an eccentric orbit time-samples a VARYING |a| (large at pericenter), so its
  memory-averaged effective inertia differs from a circular orbit at the same energy -- a Jensen gap over
  the curvature of nu.  Different eccentricity FAMILIES at one radius carry different effective inertia
  -> an intrinsic LOS-dispersion SPREAD beyond anisotropy/projection/measurement error.  Sign NEGATIVE
  (eccentric orbits run slightly cooler).  MG (QUMOND/AeST/local-g) = EXACTLY 0 (MG_ZERO.md theorem).

THE HONEST RE-DERIVED MAGNITUDE (mi_spread.py / MI_SPREAD.md, 2026-07-17 -- NOT the banked 6-13%):
  tau_mem = 203 Gyr (canonical) / 168 Gyr (alt) >> every real T_orb (>=22x, Coma) => DEEP ADIABATIC =>
  the memory freezes at the orbit mean, NO resonant amplification.  The effect is the small residual
  adiabatic Jensen gap, potential-shape dependent:
    - FIDUCIAL (cored / real-kernel-matched):  RMS spread 0.20-0.35% in sigma; peak single-orbit ~0.9%.
    - UPPER BOUND (point-mass, no core = sharpest pericenter): RMS up to ~0.7-1.0%; peak ~2.8%.
    - strongly-cored: <0.1%.  ellipticals/dE (y>>1, internally near-Newtonian): essentially 0.
  Maximized by DEEPEST y (diffuse deep-MOND dSph/UDG) x radial-biased orbits.  Both footings <~20%.

WHAT THIS SCRIPT COMPUTES: the S/N to detect that intrinsic fractional-sigma spread f in REAL
pressure-supported systems, given the estimator's fundamental floor and the ORBIT-TAG obstruction.
Frozen estimator + magnitude band are set in this header BEFORE any spec is used.

CREDIT: Milgrom 1983/1999.  dSph kinematics: Walker+2009 (MMFS), Battaglia+2008, Wolf+2010, Walker&Penarrubia
2011, Massari+2018 (Sculptor HST internal PM), Ji+2021 (Antlia II), Caldwell+2017 (Crater II).  Gaia DR3
dSph proper motions (McConnachie&Venn 2020).  Ellipticals: ATLAS3D (Cappellari+2013), MaNGA.  Coma: Cairns+2003.
"""
import numpy as np

rng = np.random.default_rng(20260717)

# ============================================================== (0) FROZEN magnitude band + footings
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10                       # BOTH footings, always
# honest re-derived RMS fractional-sigma spread f (mi_spread.py). f is defined as std(ln sigma across
# orbit families) = the standardized-tag regression slope amplitude.  Both footings identical to <1%
# at fixed deep-MOND depth y (a0 cancels), so we carry ONE band and note the <20% footing shift.
F_FID_LO, F_FID_HI = 0.0020, 0.0035                       # fiducial cored / real-kernel-matched
F_CEIL_LO, F_CEIL_HI = 0.0070, 0.0100                     # point-mass ceiling (sharpest cusp)
F_ELLIP = 0.0008                                          # y>>1 systems: essentially none
FGRID = [("fiducial-lo", 0.0020), ("fiducial-hi", 0.0035),
         ("ceiling-lo", 0.0070), ("ceiling-hi", 0.0100)]

print("=" * 104)
print(" (0) HONEST RE-DERIVED MAGNITUDE (mi_spread.py) -- the number this lane must detect")
print("=" * 104)
print(f"  fiducial (cored, real-kernel-matched) RMS sigma-spread : {F_FID_LO*100:.2f}-{F_FID_HI*100:.2f}%")
print(f"  point-mass CEILING (sharpest cusp, hard upper bound)   : {F_CEIL_LO*100:.2f}-{F_CEIL_HI*100:.2f}%")
print(f"  ellipticals/dE (y>>1, near-Newtonian internal)         : ~{F_ELLIP*100:.2f}% (dead)")
print("  Both footings shift f <~20% (a0 cancels at fixed y); N-to-3sig therefore shifts <~44% (N ~ 1/f^2).")

# ============================================================== (1) THE ESTIMATOR + its Fisher floor
print()
print("=" * 104)
print(" (1) ESTIMATOR: regression slope of ln(sigma_local) on the standardized per-star ORBIT tag x")
print("=" * 104)
print("""  Each member i: LOS velocity v_i ~ N(0, sigma_i^2 + e_i^2), with
      ln sigma_i = ln sigma_bar + f * x_i,   x standardized (mean 0, var 1) = its eccentricity/orbit tag.
  EFFICIENT (score / MLE) test.  For v~N(0,sigma^2+e^2), the Fisher info for the slope f is
  I_ff = 2 w^2 * sum x_i^2 = 2 N w^2 (w=sigma^2/(sigma^2+e^2): measurement error down-weights the
  variance-information QUADRATICALLY).  Tag impurity attenuates by D = corr(measured proxy, true
  eccentricity).  Detection z of the one-sided (sign-fixed) slope, at the Fisher floor:

      z = f * w * D * sqrt(2 * N)          (best any estimator can do; MC-validated below via the score)

  => N_3sigma = (3 / (f * w * D))^2 / 2.   No estimator can beat this Fisher floor for this observable.""")


def mc_z(N, f, w, D, trials=4000, rg=rng):
    """Monte-Carlo the EFFICIENT (score-statistic) one-sided detection z. w=sigma^2/(sigma^2+e^2).
    The score test is asymptotically MLE-efficient -> it reaches the Fisher floor z=f w D sqrt(2N)."""
    e2 = 1.0 / w - 1.0                                   # e^2 in units of sigma_bar^2=1
    T0 = 1.0 + e2                                        # null total variance per star
    xt = rng.standard_normal((trials, N))               # TRUE standardized orbit tag
    x = D * xt + np.sqrt(max(1 - D * D, 0.0)) * rng.standard_normal((trials, N))  # measured proxy
    x = x - x.mean(axis=1, keepdims=True)               # centered (profiles out the mean)
    si2 = np.exp(2.0 * f * xt)                           # per-star intrinsic variance carries the signal
    v = rng.standard_normal((trials, N)) * np.sqrt(si2 + e2)
    U = ((v * v / T0 - 1.0) * (w * x)).sum(axis=1)       # score for f at the null
    I = 2.0 * w * w * (x * x).sum(axis=1)                # observed Fisher info (score variance)
    return U / np.sqrt(I)


# validate the analytic Fisher floor z = f*w*D*sqrt(2 N) against the efficient-score MC, + sqrt(N) scaling
w0 = 0.95
for (N, f, D) in [(3000, 0.03, 1.0), (3000, 0.03, 0.5), (8000, 0.02, 0.7)]:
    zpred = f * w0 * D * np.sqrt(2 * N)
    zmc = np.median(mc_z(N, f, w0, D, trials=8000))
    print(f"  validate: N={N:5d} f={f:.3f} D={D:.1f} w={w0} -> analytic z={zpred:.3f}, score-MC median z={zmc:.3f}")
    assert abs(zmc - zpred) < 0.08 + 0.05 * zpred, "analytic Fisher floor disagrees with the efficient-score MC"
z_a = np.median(mc_z(1000, 0.03, w0, 1.0, trials=8000))
z_b = np.median(mc_z(4000, 0.03, w0, 1.0, trials=8000))
print(f"  sqrt(N) scaling: z(4000)/z(1000) = {z_b/z_a:.2f} (expect 2.00)")
assert abs(z_b / z_a - 2.0) < 0.2, "sqrt-N scaling broken"
# null calibration: f=0 -> the score z must be standard normal
zn = mc_z(3000, 0.0, w0, 1.0, trials=20000)
print(f"  null calibration (f=0, 20k trials): mean z = {zn.mean():+.3f}, sd = {zn.std():.3f} (expect 0, 1)")
assert abs(zn.mean()) < 0.04 and abs(zn.std() - 1.0) < 0.04, "score null miscalibrated"


def zdet(N, f, w, D):
    return f * w * D * np.sqrt(2 * N)


def N3(f, w, D):
    return (3.0 / (f * w * D)) ** 2 / 2.0


# ============================================================== (2) dSph single-system specs (cited)
print()
print("=" * 104)
print(" (2) CLASSICAL/DIFFUSE dSph SPECS -- N members, per-star LOS error, deep-MOND depth y")
print("=" * 104)
# (name, N_LOS_members_public, sigma_LOS[km/s], per-star vel error[km/s], distance[kpc], internal-vel[km/s], typ y)
# member counts: Walker+2009 MMFS + DEIMOS/APOGEE/DESI era; per-star err ~2 km/s bright RGB (Walker+2009);
# y = typical g_bar/a0 in the kinematically-sampled body (deep-MOND outskirts of these systems).
DSPH = [
    ("Fornax",     2600, 11.7, 2.0, 147, 11.7, 0.6),
    ("Sculptor",   1500,  9.2, 2.0,  86,  9.2, 0.3),
    ("Draco",       700,  9.1, 2.0,  76,  9.1, 0.25),
    ("Carina",      770,  6.6, 2.0, 105,  6.6, 0.3),
    ("Sextans",     440,  7.9, 2.0,  86,  7.9, 0.2),
    ("Leo I",       370,  9.2, 2.5, 254,  9.2, 0.5),
    ("Ursa Minor",  400,  9.5, 2.0,  76,  9.5, 0.25),
    ("Crater II",   150,  2.7, 2.0, 117,  2.7, 0.08),   # diffuse, DEEPEST MOND -> max f, tiny N
    ("Antlia II",   200,  5.7, 2.0, 132,  5.7, 0.10),   # diffuse, deep MOND
]
print(f"  {'system':12s} {'N':>5s} {'sig':>5s} {'e_v':>4s} {'w':>5s}  {'y':>5s} | perfect-tag z (fid 0.28% | ceil 0.85%)")
N_STACK = 0
w_of = {}
for nm, N, s, ev, D_, vi, y in DSPH:
    w = s * s / (s * s + ev * ev)
    w_of[nm] = w
    N_STACK += N
    zf = zdet(N, 0.0028, w, 1.0)
    zc = zdet(N, 0.0085, w, 1.0)
    print(f"  {nm:12s} {N:5d} {s:5.1f} {ev:4.1f} {w:5.2f}  {y:5.2f} |  z_fid={zf:.2f}   z_ceil={zc:.2f}")
print(f"  -- per-star velocity error (~2 km/s bright RGB) is NOT the wall: w=0.85-0.96 (sigma>>e_v).")
print(f"  -- DEEPEST-MOND systems (Crater II, Antlia II: max f) have the FEWEST stars (150-200): the")
print(f"     amplitude and the count PULL OPPOSITE. Even a PERFECT orbit tag gives z<0.5 in every system.")

# ============================================================== (3) THE ORBIT-TAG OBSTRUCTION (the real wall)
print()
print("=" * 104)
print(" (3) ORBIT-TAG OBSTRUCTION -- can we tag per-star eccentricity? (this sets D, the binding wall)")
print("=" * 104)
print("  The estimator needs a per-star ORBIT tag x_i (eccentricity). Sources of x, and their real D:")
# (a) Gaia per-star internal PM at dSph distance
for nm, D_kpc, vint in [("Sculptor", 86, 9.2), ("Fornax", 147, 11.7), ("Draco", 76, 9.1)]:
    mu_int = vint / (4.74 * D_kpc)                       # internal PM signal, mas/yr
    gaia_err = 0.5                                       # Gaia DR3 per-star PM err, G~19-20.5 RGB, mas/yr
    print(f"    (a) Gaia per-star internal PM {nm:9s}: signal {mu_int*1000:5.1f} uas/yr vs DR3 per-star err "
          f"~{gaia_err*1000:.0f} uas/yr -> S/N {mu_int/gaia_err:.2f} (per-star tangential velocity UNMEASURABLE)")
print("        => Gaia gives the ~N-averaged BULK systemic PM only, NOT a per-star eccentricity tag. D_Gaia ~ 0.")
print("    (b) LOS-only DF inference: a single LOS velocity + position does NOT determine an orbit's")
print("        eccentricity (the DF is E,L-degenerate); statistical deprojection reaches D ~ 0.1-0.2 AT BEST,")
print("        and that IS the anisotropy-beta channel MG mimics (MG_ZERO.md Jeans) -> confound-limited, not clean.")
print("    (c) HST/JWST multi-epoch INTERNAL PM (Sculptor Massari+2018; Draco): reaches ~few km/s per-star 3D")
print("        for a FEW HUNDRED bright stars in 2-3 systems over ~10 yr -> a genuine per-star tag, D ~ 0.3-0.4,")
print("        but N ~ 300-500 and only where the effect is NOT deepest.  This is the only real per-star route.")
print("    (d) tag-FREE route (excess LOSVD kurtosis): the orbit-family variance enters the 4th moment as ~f^2")
print(f"        ~ {0.0028**2:.1e} -- utterly unmeasurable; and degenerate with beta/triaxiality/binaries. Hopeless.")

# ============================================================== (4) N-to-3sigma grid, both footings, realistic D
print()
print("=" * 104)
print(" (4) N-to-3sigma GRID -- clean per-star LOS velocities needed, by tag quality D (w=0.95)")
print("=" * 104)
print("  (both footings folded into the f-band: f shifts <20% -> the four f columns bracket both a0.)")
print(f"  {'D (tag quality)':28s} | {'f=0.20%':>9s} {'f=0.35%':>9s} {'f=0.70%':>9s} {'f=1.00%':>9s}")
for Dlab, D in [("D=1.0  PERFECT tag (ceiling)", 1.0),
                ("D=0.35 HST/JWST 3D (best real)", 0.35),
                ("D=0.15 LOS-DF (confound-limited)", 0.15)]:
    row = " ".join(f"{N3(f, 0.95, D):9.3g}" for _, f in FGRID)
    print(f"  {Dlab:28s} | {row}")
print("  perfect-tag floor: even D=1 needs ~4.7e4 (ceiling 1%) to ~1.2e6 (fiducial 0.2%) clean member velocities")
print("  in a SINGLE deep-MOND system, split by a per-star eccentricity tag.  Realistic D shrinks it x8-45.")

# ============================================================== (5) stacked classical dSph ensemble
print()
print("=" * 104)
print(" (5) STACKED classical+diffuse dSph ensemble -- the entire in-hand LOS reservoir")
print("=" * 104)
w_ens = 0.93
print(f"  total public dSph LOS members (Walker+2009 + DEIMOS/APOGEE/DESI era): ~{N_STACK:,d}")
for flab, f in FGRID:
    zP = zdet(N_STACK, f, w_ens, 1.0)                    # perfect tag ceiling
    zH = zdet(N_STACK, f, w_ens, 0.35)                   # realistic HST-3D tag
    print(f"  {flab:12s} f={f*100:.2f}% : perfect-tag stacked z = {zP:.2f} | realistic (D=0.35) z = {zH:.3f}")
print(f"  => EVEN the perfect-tag stack of ALL ~{N_STACK//1000}k dSph stars stays z<{zdet(N_STACK,0.01,w_ens,1.0):.1f}")
print("     at the point-mass CEILING and z<0.5 at the fiducial magnitude.  With a REAL tag (D<=0.35): z<0.5.")
assert zdet(N_STACK, 0.01, w_ens, 1.0) < 3.0, "even the ceiling perfect-tag stack must be sub-3sigma (it is)"

# ============================================================== (6) ellipticals + clusters (other venues)
print()
print("=" * 104)
print(" (6) ELLIPTICALS (IFU sigma+h4) and CLUSTERS (member galaxies) -- both weak for THIS observable")
print("=" * 104)
print(f"  ELLIPTICALS: MaNGA (~10^4 galaxies) / ATLAS3D (260) give binned sigma-profiles + h4, NOT per-star")
print(f"    velocities, and internally y>>1 (near-Newtonian) -> f~{F_ELLIP*100:.2f}%.  N-to-3sig at f={F_ELLIP*100:.2f}%,")
print(f"    perfect tag: {N3(F_ELLIP,0.95,1.0):.2g} tracers -- and there is no per-star orbit tag in an IFU bin. DEAD.")
# clusters: Coma member galaxies (Cairns+2003), the star-orbit analog uses member galaxies as tracers
N_COMA, e_cz_coma, sig_coma = 1000, 39.0, 1042.0         # Cairns+2003 (caustic members ~1e3; field cat 4160)
w_coma = sig_coma ** 2 / (sig_coma ** 2 + e_cz_coma ** 2)
print(f"  CLUSTERS: Coma ~{N_COMA} caustic-member galaxies, e_cz~{e_cz_coma:.0f} km/s, sigma_cl~{sig_coma:.0f} (w={w_coma:.2f}).")
print(f"    tau_mem/T_orb ~22 (LEAST adiabatic) but still deep-adiabatic -> same f-band. Perfect-tag z at f=0.35%:")
print(f"    {zdet(N_COMA,0.0035,w_coma,1.0):.2f}; N-to-3sig {N3(0.0035,w_coma,1.0):.2g} member galaxies.  BUT: the")
print(f"    star-orbit tag for a galaxy is its 3D cluster orbit -- unavailable (D~0.1-0.2 from projected phase space).")
print("    NOTE: the member-galaxy INTERNAL-dispersion-vs-infall-phase observable (banked f=6-13%, power_analysis.py)")
print("    is the DISTINCT, ~30x-larger EFE channel at cluster scale -- that is the powerable cluster route, not this one.")

# ============================================================== (7) VERDICT
print()
print("=" * 104)
print(" (7) VERDICT")
print("=" * 104)
Nfid_perf = N3(0.0028, 0.95, 1.0)
Nceil_perf = N3(0.0085, 0.95, 1.0)
Nfid_hst = N3(0.0028, 0.95, 0.35)
Nceil_hst = N3(0.0085, 0.95, 0.35)
print(f"""  MAGNITUDE (honest, re-derived): star-orbit sigma-spread f = {F_FID_LO*100:.2f}-{F_FID_HI*100:.2f}% fiducial,
    up to {F_CEIL_LO*100:.2f}-{F_CEIL_HI*100:.2f}% point-mass ceiling; ~{F_ELLIP*100:.2f}% in ellipticals. Both footings <20%.
  MG = EXACTLY 0 (airtight theorem, MG_ZERO.md) -- so a clean detection would be MG-impossible, IF detectable.

  POWERED NOW?  NO. Two independent walls, either alone fatal:
    (W1 COUNT)  the estimator's Fisher floor needs N ~ {Nceil_perf:.2g} (ceiling {F_CEIL_HI*100:.1f}%) to ~{Nfid_perf:.2g}
                (fiducial {F_FID_LO*100:.2f}%) CLEAN per-star velocities in a SINGLE deep-MOND system, EVEN WITH a
                perfect orbit tag. Biggest dSph = {DSPH[0][1]:,d}; the entire stacked dSph reservoir ~{N_STACK:,d}
                gives perfect-tag z<{zdet(N_STACK,0.01,0.93,1.0):.1f} at the ceiling, <0.5 at fiducial. Gap x{Nfid_perf/N_STACK:.0g}-{Nceil_perf/N_STACK:.0g}.
    (W2 TAG)    per-star eccentricity is NOT measurable where the count is: Gaia per-star internal PM S/N~0.05
                at dSph distances (bulk PM only, D~0); LOS-only DF gives D<=0.2 and IS the beta-anisotropy channel
                MG mimics; only HST/JWST 3D reaches D~0.3-0.4, for ~300-500 stars in 2-3 systems -> best real
                single-system z ~ {zdet(500,0.005,0.95,0.35):.2f}. Realistic-D N-to-3sig: {Nceil_hst:.2g} (ceiling) to {Nfid_hst:.2g} (fiducial).
  EXISTING DATA THAT BITES?  NONE. Walker+2009 / Gaia DR3 / MaNGA / ATLAS3D / Coma all fall x10^2-10^6 short:
    ellipticals dead (y>>1, no per-star tag), clusters give only the DISTINCT EFE channel (power_analysis.py).

  UNDERPOWERED -- NEEDS: (i) ~10^4.5-10^5.5 CLEAN per-star LOS velocities in a single deep-MOND diffuse
    dSph/UDG (only the point-mass ceiling corner ~1% is within ~1-2 orders of a plausible 30m-class campaign;
    the fiducial 0.2-0.35% needs ~10^5.5-10^6 and is out of reach), AND (ii) a per-star 3D orbit/eccentricity
    tag at dSph distances (post-Gaia astrometry + multi-epoch space PM; Gaia cannot do it per-star). BOTH are
    required; today neither exists. This observable is a clean MG-impossible discriminator but is
    STRUCTURALLY UNPOWERED at its honest magnitude -- not merely short of data, short of a per-star orbit tag.
  Both footings: f shifts <20% -> all N shift <44%; the discriminator is NOT footing-hostage, it is magnitude-
    and tag-hostage. No 'proves' for the framework value/sign; MG=0 is the only theorem-grade claim.""")

print()
print(" EXIT 0 = Fisher floor MC-validated (analytic z matches MC, sqrt-N verified); verdict UNDERPOWERED-NEEDS-X.")
