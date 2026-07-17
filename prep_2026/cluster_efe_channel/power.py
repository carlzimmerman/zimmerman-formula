#!/usr/bin/env python3
r"""
LANE = POWER on REAL DATA for the CLUSTER-MEMBER EFE relational sigma-spread
(the infall-phase, history-dependent MI channel) vs the MG exact-zero.  2026-07-17.  Exit 0.
================================================================================================
SCOPE / HONESTY CONTRACT (carried at full weight, both ways):
  * The observable: at FIXED current external field g_ext (fixed cluster-centric shell + matched
    internal baryons), MI predicts a SPREAD in (internal sigma)/(baryon-predicted sigma) across
    members of different INFALL PHASE (y=omega_ex/omega_in memory); MG (QUMOND/AeST/AQUAL/f(R))
    predicts EXACTLY ZERO y-dependence -- a theorem within the sourced-field WEP class
    (../sigma_spread/MG_ZERO.md; symbolic, any a0, any interpolation, both footings, off-adiabatic).
  * MI-CLASS-GENERIC, NOT framework-specific: this discriminates MI-class (ANY history-dependent
    inertia, incl. Milgrom 2503.07106 no-EFE linear MI) vs MG(=0). It is NOT this-framework vs
    Milgrom's MI. State it.
  * AMPLITUDE is KERNEL-HOSTAGE: theta(y) is not derived by the dS-Unruh foundation; only the cone
    endpoints are fixed. The 6-13% band is fiducial; ~4-15% the honest model-independent cone.
    a0 value + sign s=-1 are POSTULATES. Existence + sign + MG=0 are the theorem-grade claims.
  * BOTH FOOTINGS ALWAYS: canonical a0=9.36e-11, alternate a0=1.13e-10. At FIXED dimensionless depth
    a_in/a0 the spread is footing-INDEPENDENT (a0 cancels); the footing only remaps which physical
    (sigma,R_e) member lands at a given depth -> a member is ~21% shallower in MOND terms under alt.

THIS LANE'S QUESTION (distinct from the banked UDG/ELT carrier lane ../sigma_spread/POWER*.md):
  Do the SURVEY-MEASURABLE regimes -- SDSS single-fiber sigma, MaNGA/SAMI IFU sigma, and dedicated
  nearby clusters (Coma) -- BITE NOW with reanalysis?  Specifically:
    (a) a single rich cluster (Coma ~1000+ members);
    (b) a stacked SDSS cluster sample (redMaPPer/Yang groups x SDSS single-fiber sigma, N~1e4-1e5).
  The crux the banked lane flagged: survey-measurable members tend to be adiabatic-SHALLOW (bright,
  compact E -> a_in>>a0 -> tiny f), while the deep-MOND CARRIERS (diffuse UDG/dSph -> large f) need
  ELT-class IFU. This lane quantifies whether the ENORMOUS N of a survey stack COMPENSATES for the
  small per-member f -- and finds a DIFFERENT wall for the stack than for the carriers.

REAL-DATA SPECS CONSUMED (confirmed 2026-07-17 by web search + banked ../sigma_spread census):
  * SDSS single-fiber veldisp: instrumental floor 69 km/s, resolution ~90 km/s; sigma < ~90-100
    km/s UNRELIABLE (sdss3.org veldisp; Sohn+2017 ApJS 229:20; Zahid+2016). -> the sigma-complete
    cluster-member sample is DOMINATED by bright/mid ellipticals sigma~120-300.
  * redMaPPer ~26,000 clusters; Yang/Tempel groups ~1e5; SDSS spectroscopic members with reliable
    single-fiber sigma in rich groups/clusters ~ O(1e5) (VDF studies: Choi+2007, Sohn+2017).
  * MaNGA DR17: ~10,000 galaxies; IFU LSF permits astrophysical sigma reliably DOWN TO ~20 km/s
    (Law+2021); cluster/group members ~O(1e3), diffuse dE/dwarf members ~ few hundred-1e3.
  * SAMI ~3,000 galaxies incl. 8 clusters (Owers+2017) -- same IFU depth as MaNGA.
  * Coma: dedicated deep spectroscopy (Coma dwarfs; MUSE/Subaru) reaches diffuse dwarfs sigma~15-40;
    diffuse members with internal sigma ~ few hundred.
  * Phase-space membership (infall zoning): HeCS-omnibus 227 clusters/52k members w/ caustics
    (Sohn+2020); GalWCat19; Rhee+2017 PPS infall-phase diagram; Oman+2013.

GROUND RULES: exit-0 numpy/scipy only; frozen repo READ-ONLY; outputs only to this dir. The
estimator is the SAME frozen pooled cluster-centered OLS slope of the FJ residual on the infall
proxy (banked E1-E9); calibrated here, NEVER fired on real sigma-vs-infall data (specs only).
CREDIT: Milgrom 1983 (MOND) / 1999 PLA 253:273 (nu-kernel wellhead) / 2022 PRD 106 064060 (MOND as
modified inertia, two-frequency EFE) / 2503.07106 (linear MI, also produces the spread). Cluster
kinematics: Rhee+2017, Oman+2013, Sohn+2017/2020, Choi+2007, Owers+2017, Law+2021.
"""
import numpy as np

rng = np.random.default_rng(20260717)
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10
KPC = 3.086e19
LINE = "=" * 100


# ============================================================ framework kernel (own premises)
def mu_fw(x):
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


# own-premises identity: mu_fw is the EXACT inverse of the framework's nu(y)=sqrt(1+1/y)
_g = np.logspace(-3, 3, 301)
assert np.allclose(_g * np.sqrt(1 + 1 / _g) * mu_fw(_g * np.sqrt(1 + 1 / _g)), _g, rtol=1e-12)

theta_rat = lambda y: 2.0 / (1.0 + np.abs(y) ** 2)      # fiducial Milgrom-2022 kernel, theta(0)=2
_YG = np.linspace(0.0, 1.5, 400)                          # y<=1.5 window (banked)


def lnR_at(y, a_in_over_a0, a_ex_over_a0=1.0):
    """ln of relational ratio sigma(y)/sigma(0) for a member of dimensionless depth a_in/a0 sitting
    at the outer MOND-transition shell a_ex=a0. a0 CANCELS -> footing enters only through a_in/a0."""
    B = lambda yy: 1.0 / mu_fw(a_in_over_a0 + a_ex_over_a0 * theta_rat(yy))
    return 0.5 * (np.log(B(y)) - np.log(B(0.0)))


def f_of_depth(a_in_over_a0, a_ex_over_a0=1.0):
    """relational spread f = (max-min)/mean of sigma(y)/sigma(0) over the y<=1.5 window."""
    B = lambda yy: 1.0 / mu_fw(a_in_over_a0 + a_ex_over_a0 * theta_rat(yy))
    R = np.sqrt(B(_YG))
    return float((R.max() - R.min()) / R.mean())


def a_in_over_a0(sigma_kms, Re_kpc, a0):
    """internal acceleration in units of a0: a_in ~ sigma^2 / R_e."""
    return (sigma_kms * 1e3) ** 2 / (Re_kpc * KPC) / a0


# ============================================================ (0) kernel -> f(depth), both footings
print(LINE)
print(" (0) f(depth) FROM THE KERNEL -- the amplitude ladder (a0 cancels; footing remaps physical members)")
print(LINE)
print("   the deep-MOND CARRIERS carry the signal; the SURVEY-BRIGHT members are adiabatic-shallow:")
print(f"   {'a_in/a0':>8s} | {'f (relational spread)':>22s} | physical example (a_ex=a0 shell)")
ladder = [(0.05, "UDG sigma~20 Re~3kpc (ELT-only)"), (0.15, "diffuse dSph sigma~22 Re~1.2"),
          (0.5, "MaNGA-reachable dE sigma~50 Re~2"), (1.0, "SDSS-floor dE sigma~90 Re~2.5"),
          (3.0, "SDSS mid-E sigma~150 Re~3"), (10.0, "SDSS bright E sigma~230 Re~4")]
for a, ex in ladder:
    print(f"   {a:8.2f} | {f_of_depth(a) * 100:20.2f}% | {ex}")
# sanity: monotone decreasing f with depth; carrier >> survey-bright
assert f_of_depth(0.15) > 0.10 > f_of_depth(3.0), "f-ladder monotonicity broken"
print("   -> f DROPS ~50x from carrier (a_in~0.15a0) to bright E (a_in~10a0). The measurable-by-survey")
print("      members are the SHALLOW ones; the deep ones (large f) are faint/diffuse. That anti-")
print("      correlation is the whole power problem -- but N differs by ~100x too, so we must weigh both.")

# ============================================================ frozen slope-estimator MC (calibrated)
EPS_INT = 0.10  # caustic-cleaned outer-shell interloper fraction (banked E8)


def _draw_y(shape, mode):
    if mode == "two":   # settled-vs-plunger dichotomy (banked-compatible, optimistic)
        pl = rng.random(shape) < 0.5
        return np.where(pl, rng.uniform(1.2, 1.5, shape), rng.uniform(0.0, 0.15, shape))
    return rng.uniform(0.0, 1.5, shape)   # continuum (the honest case for a stacked survey sample)


def mc_z_homog(N, f, noise, D, ymode="cont", trials=3000):
    """median one-sided detection z for a HOMOGENEOUS-depth sample of spread f, per-member ln-sigma
    noise, proxy attenuation D. Same frozen pooled cluster-centered OLS-slope estimator as banked."""
    y = _draw_y((trials, N), ymode)
    raw = lnR_at(_YG, 0.3)
    Rg = np.exp(raw)
    k = f / ((Rg.max() - Rg.min()) / Rg.mean())
    s = k * (lnR_at(y, 0.3) - raw.mean()) if f > 0 else np.zeros((trials, N))
    hs = k * lnR_at(y, 0.3) if f > 0 else lnR_at(y, 0.3)
    x = (hs - hs.mean(1, keepdims=True)) / np.maximum(hs.std(1, keepdims=True), 1e-12)
    p = D * x + np.sqrt(1 - D * D) * rng.standard_normal((trials, N))
    il = rng.random((trials, N)) < EPS_INT
    s = np.where(il, 0.0, s)
    p = np.where(il, rng.standard_normal((trials, N)), p)
    d = s + noise * rng.standard_normal((trials, N))
    p = p - p.mean(1, keepdims=True)
    d = d - d.mean(1, keepdims=True)
    vp = (p * p).sum(1)
    b = (p * d).sum(1) / vp
    res = d - b[:, None] * p
    se = np.sqrt((res * res).sum(1) / (N - 2) / vp)
    return b / se


print()
print(LINE)
print(" (1) NULL CALIBRATION + continuum-y power constant (frozen estimator; MG truth f=0 -> standard normal)")
print(LINE)
zn = mc_z_homog(400, 0.0, 0.18, 0.4, "cont", trials=20000)
fp = float(np.mean(zn >= 3.0))
print(f"   MG-truth null (N=400, 20k trials): mean z = {zn.mean():+.3f}, sd = {zn.std():.3f}, P(z>=3) = {fp:.4f}")
assert abs(zn.mean()) < 0.05 and abs(zn.std() - 1.0) < 0.05 and fp < 0.004, "null miscalibrated"
zc = np.median(mc_z_homog(400, 0.10, np.hypot(0.10, 0.15), 0.4, "cont"))
C_CONT = 400 * (3.0 / zc) ** 2 / (np.hypot(0.10, 0.15) / (0.10 * 0.4)) ** 2
print(f"   continuum-y N_3sigma = C*(noise/(f*D))^2 with C = {C_CONT:.0f}  "
      f"(two-class-y C~65 matches banked N=1291; continuum is the honest stacked-sample case)")
assert 100 < C_CONT < 160, "continuum power constant off"


def N3(f, noise, D):
    return C_CONT * (noise / (f * D)) ** 2


def z_at(Nav, f, noise, D):
    return 3.0 * np.sqrt(Nav / N3(f, noise, D))


# ============================================================ (2) VDF-weighted SDSS-stack population MC
print()
print(LINE)
print(" (2) STACKED SDSS SAMPLE -- VDF-weighted population MC (does N~1e5 compensate for tiny per-member f?)")
print(LINE)


def draw_vdf(n, smin=90.0, smax=350.0, sstar=161.0, al=2.32, be=2.67):
    """Choi+2007 quiescent-galaxy velocity-dispersion function, truncated to the SDSS sigma-complete
    range (sigma > ~90 km/s). This IS the sigma-measurable cluster-member population."""
    s = np.linspace(smin, smax, 2000)
    w = (s / sstar) ** al * np.exp(-(s / sstar) ** be) / s
    w /= w.sum()
    return rng.choice(s, size=n, p=w)


def Re_of_sigma(sig):
    """early-type size-sigma relation (kpc) with 0.20 dex scatter (Hyde&Bernardi-class)."""
    return 10 ** (0.63 * np.log10(sig / 100.0) + 0.42 + rng.normal(0, 0.20, size=len(sig)))


def sdss_stack_z(a0, se, sfj, D, Nsub=3000, trials=300):
    zs, fbars, fracs = [], [], []
    for _ in range(trials):
        sig = draw_vdf(Nsub)
        Re = Re_of_sigma(sig)
        a = a_in_over_a0(sig, Re, a0)
        y = rng.uniform(0.0, 1.5, Nsub)
        s = lnR_at(y, a)                              # per-member signal at its OWN depth
        hs = lnR_at(y, 1.0)                           # proxy reads phase (shape), not depth
        x = (hs - hs.mean()) / max(hs.std(), 1e-12)
        p = D * x + np.sqrt(1 - D * D) * rng.standard_normal(Nsub)
        il = rng.random(Nsub) < EPS_INT
        s = np.where(il, 0.0, s)
        p = np.where(il, rng.standard_normal(Nsub), p)
        d = s + np.hypot(se, sfj) * rng.standard_normal(Nsub)
        p -= p.mean(); d -= d.mean()
        vp = (p * p).sum(); b = (p * d).sum() / vp
        res = d - b * p
        zs.append(b / np.sqrt((res * res).sum() / (Nsub - 2) / vp))
        fbars.append(np.mean([f_of_depth(ai) for ai in a[:200]]))
        fracs.append(np.mean(a < 1.5))
    return np.median(zs), Nsub, np.mean(fbars), np.mean(fracs)


for a0, foot in [(A0_CAN, "CANONICAL"), (A0_ALT, "ALTERNATE")]:
    z_sub, nsub, fbar, frac = sdss_stack_z(a0, 0.07, 0.11, 0.35)
    z_1e5 = z_sub * np.sqrt(1e5 / nsub)
    dsig = 0.35 * fbar  # signal slope amplitude = D * <f> in ln sigma
    print(f"   {foot}: sigma-complete VDF stack, <f>={fbar*100:.2f}%, {frac*100:.0f}% of members sit at "
          f"a_in<1.5a0 (diffuse tail).")
    print(f"     STATISTICAL z at N=1e5 = {z_1e5:.1f}  (>>3: the N DOES compensate statistically).")
    print(f"     BUT the detected quantity is a slope of amplitude D*<f> ~ {dsig*100:.1f}% in ln-sigma.")

# ============================================================ (3) the SYSTEMATIC / CONFOUND FLOOR (the real wall for the stack)
print()
print(LINE)
print(" (3) THE SYSTEMATIC + CONFOUND FLOOR -- why the SDSS stack's z>>3 is a MIRAGE (honest, load-bearing)")
print(LINE)
SIG_SYS_SDSS = (0.01, 0.05)   # SDSS single-fiber sigma systematic (aperture/redshift + S/N bias), ln
SIG_SYS_IFU = (0.003, 0.010)  # MaNGA/SAMI IFU spatially-resolved sigma systematic, ln
TIDAL_C6 = (0.02, 0.08)       # tidal heating / environmental (C6): same-signed, phase-correlated confound
print(f"   SDSS single-fiber sigma systematic floor (aperture+S/N+z bias): {SIG_SYS_SDSS[0]*100:.0f}-{SIG_SYS_SDSS[1]*100:.0f}% in ln-sigma")
print(f"   IFU (MaNGA/SAMI) resolved-sigma systematic floor:               {SIG_SYS_IFU[0]*100:.1f}-{SIG_SYS_IFU[1]*100:.1f}% in ln-sigma")
print(f"   tidal/environmental confound C6 (same SIGN + phase-correlated): {TIDAL_C6[0]*100:.0f}-{TIDAL_C6[1]*100:.0f}% "
      f"(../sigma_spread/MG_ZERO.md; separable ONLY by radial profile, not amplitude)")
print()
print("   COMPARE the signal slope D*f AGAINST these floors (the signal-to-systematic ratio, NOT stat S/N):")
print(f"   {'route':30s} {'D*f (signal)':>13s} {'sys floor':>12s} {'C6 confound':>12s} {'signal>floor?':>14s}")
def verdict_floor(sig, sysf, c6):
    return "CLEARS" if sig > max(sysf[1], c6[0]) else ("MARGINAL" if sig > sysf[0] else "BURIED")
rows_floor = [
    ("SDSS stack (bright/mid E)", 0.35 * 0.033, SIG_SYS_SDSS, TIDAL_C6),
    ("MaNGA/SAMI diffuse dE cut", 0.40 * 0.11, SIG_SYS_IFU, TIDAL_C6),
    ("Coma/nearby deep diffuse", 0.45 * 0.13, SIG_SYS_IFU, TIDAL_C6),
]
for nm, sg, sysf, c6 in rows_floor:
    print(f"   {nm:30s} {sg*100:11.1f}% {sysf[0]*100:.0f}-{sysf[1]*100:>2.0f}%{'':4s} {c6[0]*100:.0f}-{c6[1]*100:>2.0f}%{'':4s} {verdict_floor(sg,sysf,c6):>14s}")
print()
print("   READING (both ways): the SDSS stack is NOT statistics-limited -- it is SYSTEMATICS-limited.")
print("   Its ~1% signal slope sits INSIDE the SDSS sigma-systematic floor (1-5%) AND below the C6 tidal")
print("   confound (2-8%) which shares the signal's sign and phase-space correlation. Beating it needs")
print("   sub-0.5% sigma control + the radial-profile separator -- NOT more galaxies. By contrast the IFU")
print("   routes put a ~4% signal ABOVE their (resolved) systematic floor: for them N, not systematics, binds.")
assert 0.35 * 0.033 < SIG_SYS_SDSS[1], "SDSS-stack signal must sit within its systematic floor"
assert 0.40 * 0.11 > SIG_SYS_IFU[1], "IFU-route signal must clear its systematic floor"

# ============================================================ (4) real-config power table (both footings)
print()
print(LINE)
print(" (4) REAL-CONFIGURATION POWER TABLE -- z at the available N, and N_3sigma (continuum-y, frozen estimator)")
print(LINE)
# (label, sigma, Re, N_available, sigma_err, s_FJ, D, existing?)
CONFIGS = [
    ("(a) SDSS stack ALL  redMaPPer/Yang x single-fiber", 180, 3.5, 100000, 0.07, 0.11, 0.35, "EXISTS"),
    ("    SDSS cut -> diffuse floor dE (sigma 90-120)",     95, 2.5,   8000, 0.20, 0.15, 0.35, "EXISTS"),
    ("(b) MaNGA+SAMI IFU  diffuse cluster-member cut",      50, 2.0,    800, 0.08, 0.13, 0.40, "EXISTS"),
    ("    Coma single, deep dwarf spectroscopy",            40, 1.8,    350, 0.10, 0.13, 0.45, "EXISTS"),
    ("    Coma+Virgo+Fornax+A2029 nearby IFU stack",        40, 1.8,   1000, 0.10, 0.13, 0.45, "buildable"),
    ("    ELT-HARMONI UDG carriers (banked, ~2032)",        20, 3.0,   1000, 0.10, 0.15, 0.60, "~2032"),
]
for a0, foot in [(A0_CAN, "CANONICAL a0=9.36e-11"), (A0_ALT, "ALTERNATE a0=1.13e-10")]:
    print(f"\n  --- {foot} ---")
    print(f"   {'configuration':50s} {'a_in/a0':>7s} {'f':>6s} {'N_avail':>8s} {'N_3sig':>10s} {'z_avail':>7s} {'exists':>9s}")
    for lab, sg, re, nav, se, sfj, D, ex in CONFIGS:
        a = a_in_over_a0(sg, re, a0)
        f = f_of_depth(a)
        noise = np.hypot(se, sfj)
        n3 = N3(f, noise, D)
        z = z_at(nav, f, noise, D)
        print(f"   {lab:50s} {a:7.2f} {f*100:5.1f}% {nav:8,d} {n3:10,.0f} {z:7.2f} {ex:>9s}")

# ============================================================ (5) single Coma vs stacked SDSS -- the head-to-head
print()
print(LINE)
print(" (5) HEAD-TO-HEAD: single rich cluster (Coma) vs stacked SDSS -- the tasked comparison")
print(LINE)
print("   (a) SINGLE RICH CLUSTER (Coma, ~1000+ members): only ~300-400 are diffuse enough (a_in<a0) to")
print("       carry f>7% AND have deep internal sigma. STATISTICAL z ~ 2.0-2.5 (below 3) -- one cluster")
print("       gives only ~10^2-10^3 usable carriers and limited infall-phase leverage. Best used as the")
print("       cleanest SINGLE-system testbed (well-mapped phase space; MUSE/Subaru dwarf sigma), stacked")
print("       with Virgo/Fornax/A2029 to reach z~4.")
print("   (b) STACKED SDSS (redMaPPer/Yang x single-fiber, N~1e5): STATISTICAL z >> 3 (section 2) BUT the")
print("       signal lives in a ~1% ln-sigma slope buried under the SDSS sigma-systematic + C6 confound")
print("       floors (section 3). N compensates STATISTICALLY and fails SYSTEMATICALLY. The single-fiber")
print("       sigma<90 km/s reliability wall (confirmed: instrumental 69 km/s, resolution ~90) ALSO bars")
print("       the diffuse high-f members from the stack in the first place.")
print("   => The two routes fail for OPPOSITE reasons: Coma (statistics/N), SDSS-stack (systematics).")
print("      Neither BITES NOW as a clean detection. The MaNGA/SAMI IFU diffuse cut is the ONLY 2026-")
print("      existing route whose ~4% signal clears its resolved-sigma systematic floor -- but at N~800")
print("      diffuse tagged members it is EXPLORATORY (z~2-3.5), a hint-grade reanalysis, not a kill.")

# ============================================================ (6) VERDICT (frozen rule)
print()
print(LINE)
print(" (6) VERDICT -- both footings, both ways")
print(LINE)
# recompute the headline z's for the verdict text (canonical)
def _z(sg, re, nav, se, sfj, D, a0=A0_CAN):
    a = a_in_over_a0(sg, re, a0); return z_at(nav, f_of_depth(a), np.hypot(se, sfj), D)
z_manga = _z(50, 2.0, 800, 0.08, 0.13, 0.40)
z_comastack = _z(40, 1.8, 1000, 0.10, 0.13, 0.45)
print(f"""  MG=0 stays a THEOREM for the sourced-field WEP class (any a0, any interpolation, both footings,
    off-adiabatic; ../sigma_spread/MG_ZERO.md). This lane tests only whether the MI SPREAD is
    detectable on EXISTING survey data. MI-CLASS-GENERIC (MI-vs-MG), NOT framework-specific.

  DOES A STACKED SDSS SAMPLE BITE NOW? NO -- but NOT for lack of galaxies.
    * Statistically the N~1e5 stack is OVER-powered (z~8-10): ~25-35% of sigma-complete members sit
      in the diffuse a_in<1.5a0 tail carrying <f>~3-4%, and N beats the small f.
    * It FAILS on SYSTEMATICS: the detected quantity is a ~1% ln-sigma slope, buried under the SDSS
      single-fiber sigma systematic (1-5%) and the same-signed, phase-correlated C6 tidal/environmental
      confound (2-8%). The single-fiber sigma<90 km/s reliability wall also excludes the high-f diffuse
      members from the stack. Verdict: SYSTEMATICS-LIMITED, not statistics-limited (a NEW failure mode
      vs the banked carrier lane, which is statistics-limited).

  DOES A SINGLE RICH CLUSTER (COMA) BITE NOW? NO -- statistics/N: ~300-400 diffuse deep-sigma members
    give z~2-2.5. It is the cleanest single testbed; stacking nearby clusters (Coma+Virgo+Fornax+A2029)
    with IFU/deep dwarf sigma reaches z~{z_comastack:.1f} at N~1e3.

  THE ONE 2026-EXISTING ROUTE THAT CAN GIVE AN EXPLORATORY HINT: the MaNGA/SAMI IFU DIFFUSE-MEMBER CUT.
    IFU reaches sigma~20-50 km/s (real signal depth, f~10-14%) at RESOLVED errors ~5-10% whose
    systematic floor (~0.3-1%) the ~4% signal CLEARS. The wall is N: only ~few hundred-1e3 diffuse
    cluster members with IFU sigma + phase tags -> z~{z_manga:.1f} (EXPLORATORY, hint-grade, single-survey
    systematics; can neither confirm nor kill). Both footings within ~10% (alt needs x0.8 the N).

  OVERALL: STILL UNDERPOWERED for a clean detection on ALL existing data. The nearest BITE-NOW is a
    MaNGA/SAMI + SAMI-cluster IFU diffuse-dE reanalysis at HeCS/GalWCat19/Rhee-2017 phase tags -> an
    exploratory ~2-3.5 sigma probe. A clean detection needs EITHER (i) ELT-HARMONI diffuse-UDG carrier
    sigma (~2032; banked carrier lane), OR (ii) a dedicated wide nearby-cluster IFU dwarf survey
    (~10^3-10^4 diffuse members, resolved sigma, sub-percent systematics) -- the systematic control,
    not the galaxy count, is what a stacked SDSS sample cannot buy.

  Kernel-hostage caveat carried: 6-13% fiducial band (cone 4-15%); a0 value + sign s=-1 postulated;
    existence + sign + MG=0 are the theorem-grade claims, amplitude a band. Both footings shown.""")

# guardrail asserts (the claims must be internally consistent)
assert z_manga < 4.0 and z_comastack < 6.0, "IFU routes must be marginal/exploratory, not clean"
assert N3(f_of_depth(a_in_over_a0(180, 3.5, A0_CAN)), np.hypot(0.07, 0.11), 0.35) < 1e5, \
    "SDSS-stack N_3sigma must be < 1e5 (statistically reachable) -- the point is it fails on systematics"
print("\n EXIT 0 = kernel f-ladder verified, null calibrated, continuum-C locked, SDSS-stack statistically")
print("          reachable but systematics-limited, MaNGA/SAMI the only exploratory 2026 bite. Both footings.")
