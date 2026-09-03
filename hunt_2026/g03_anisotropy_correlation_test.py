#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g03_anisotropy_correlation_test.py -- DOES THE PRESSURE-SUPPORTED DEFICIT TRACK MEASURED ORBITAL ANISOTROPY?
============================================================================================================
THE QUESTION.  f09 found a BETWEEN-population contrast: rotating systems sit on the framework's kernel,
pressure-supported ones sit above it, +0.215 dex at 1.73 sigma on the only eight classical dwarf spheroidals
that exist.  That contrast cannot separate "orbital coherence" from "dark-matter fraction", because in the real
universe the two are correlated.  Modified INERTIA makes a sharper, WITHIN-population claim: the modification
attaches to the TRAJECTORY, so at fixed mass the deficit should track ORBIT SHAPE -- the velocity-anisotropy
parameter beta.  Dark matter predicts no correlation with beta at fixed mass, because beta is a property of the
TRACERS and not of the halo.  That is a dark-matter-blind test, and it is the one this file runs.

WHAT IS ACTUALLY BEING TESTED, STATED HONESTLY BEFORE ANY NUMBER IS COMPUTED:
  * The residual currency is f09's, verbatim: log10( g_obs / g_pred ) with g_obs = 3 sigma^2 / R_half and
    g_pred = max(isolated deep-MOND, external-field value), the choice that FAVOURS the framework.
  * The anisotropy is the only homogeneous published set that exists for these eight objects: the axisymmetric
    Jeans fits of Hayashi, Chiba & Ishiyama 2020, ApJ 904, 45 (arXiv:2007.13780), their Table 2 column
    -log10(1 - beta_z), converted to beta_z = 1 - 10^(-x).  Every value is quoted inline below.
  * MODIFIED INERTIA DOES NOT PREDICT THE SIGN.  It is a CLASS, not a theory, and Milgrom's deep-MOND virial
    relation (Milgrom 1994, Ann. Phys. 229, 384; Milgrom 1997, Phys. Rev. E 56, 1148) holds in BOTH arms, so a
    GLOBAL dispersion-based residual is precisely the observable for which modified inertia and modified gravity
    are proven to agree in the deep-MOND limit.  The test is therefore two-sided and second-order.  Check A13.
  * A uniform multiplicative error in the mass estimator (3 sigma^2/R with a projected rather than a 3D
    half-light radius, i.e. the Wolf+2010 factor 4/3) shifts every residual by the SAME number of dex and
    therefore cannot move a correlation.  Check A4 re-runs everything on an independent structural compilation
    that uses a circularised 3D half-light radius, and the two residual vectors agree at r = +0.96.

THE CIRCULARITY RISK, WHICH THE BRIEF FLAGGED AND WHICH TURNS OUT TO BE THE ANSWER.  Published beta values are
fitted JOINTLY with a dark-matter halo.  This file measures how big that problem is instead of asserting it,
using three independent published re-analyses of the SAME two galaxies (checks A8-A11).  Its verdict is not
"underpowered"; it is that the INPUT VARIABLE IS NOT MEASURED to the precision this test needs.

DATA NOT ASSEMBLED, AND WHY -- marked not-run rather than guessed, per the working rules:
  * Early-type galaxies (ATLAS3D / SLUGGS).  The repository holds atlas3d_fj_table.tsv (sigma_e, R_e, M/L) but
    NOT a per-galaxy anisotropy column, and the ATLAS3D JAM anisotropy beta_z is not in VizieR (the catalogue
    J/MNRAS/432/1709 does not resolve).  No value is invented; this population is NOT RUN.
  * Outer-halo globular clusters.  The two that appear in the liability table (Pal 4, Pal 14) have no published
    internal proper-motion anisotropy -- their stars are too faint and too few.  NOT RUN.
  * Galaxy clusters.  Published beta(r) for cluster galaxies comes from MAMPOSSt/caustic modelling that assumes
    an NFW halo, i.e. maximal circularity for a non-NFW theory.  NOT RUN.
So N = 8, exactly the eight classical dwarf spheroidals, and that is stated as a limit, not hidden.
"""
import sys, math, os, csv
import numpy as np
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260903)
NPERM = 50000
MW_VC = 200e3      # Milky Way circular speed, m/s, for the external field on satellites (as in f09)

# ---------------------------------------------------------------------------------------------------------
# (a) THE SAMPLE
# ---------------------------------------------------------------------------------------------------------
P("=" * 118)
P("A.  THE SAMPLE: every pressure-supported system with a published velocity anisotropy AND the structural data")
P("=" * 118)

# Structural data: taken verbatim from f09_orbital_coherence_fork.py so the currency is identical.
# (name, M_star [Msun], R_half [kpc], sigma_los [km/s], Galactocentric distance [kpc])
DSPH = [("Draco",      2.9e5, 0.221, 9.1,  76.), ("Sculptor",   2.3e6, 0.283, 9.2,  86.),
        ("Fornax",     4.3e7, 0.710, 11.7, 147.), ("Carina",     3.8e5, 0.250, 6.6,  105.),
        ("Sextans",    4.4e5, 0.695, 7.9,  86.),  ("Leo I",      5.5e6, 0.251, 9.2,  254.),
        ("Leo II",     7.4e5, 0.176, 6.6,  233.), ("Ursa Minor", 2.9e5, 0.181, 9.5,  76.)]

# ANISOTROPY -- the ONLY homogeneous published set for all eight, one analysis, one code, one halo family.
# Hayashi, Chiba & Ishiyama 2020, ApJ 904, 45 (arXiv:2007.13780), Table 2, column -log10(1 - beta_z),
# with their 68 per cent credible intervals (-err, +err).  beta_z = 1 - sigma_z^2/sigma_R^2 (cylindrical),
# fitted simultaneously with a generalised-Hernquist dark halo (rho_0, b_halo, alpha, beta, gamma), the halo
# axis ratio Q and the inclination i.  The paper itself reports a Q-beta_z degeneracy: their Section IV.1.
BZ_HAYASHI = {"Draco": (0.41, 0.19, 0.21), "Ursa Minor": (0.61, 0.13, 0.16), "Carina": (0.36, 0.26, 0.24),
              "Sextans": (0.18, 0.18, 0.19), "Leo I": (0.11, 0.17, 0.19), "Leo II": (0.12, 0.23, 0.18),
              "Sculptor": (0.21, 0.18, 0.18), "Fornax": (0.24, 0.18, 0.13)}

# INDEPENDENT re-analyses of the two dwarfs that have resolved internal PROPER MOTIONS.  These are the least
# model-dependent anisotropies in existence for any dwarf spheroidal, and they are used in checks A8-A10.
#   Draco   -- Vitral et al. 2024, ApJ 970, 1 (arXiv:2407.07769), HSTPROMO I:
#              axisymmetric, inclination-marginalised   beta_bar_B = -0.20 (+0.28, -0.53)
#              same data, meridional JAM parameter      beta_J     = +0.56 (+0.25, -0.42)
#              same data, SPHERICAL model (their model 3) beta_B   = +0.39 (+0.13, -0.14)
#              measured plane-of-sky ratio  <sigma_POSt>/<sigma_POSr> = 0.80 +/- 0.08
#   Draco   -- Massari et al. 2020, A&A 633, A36 (arXiv:1904.04037), spherical Jeans + NFW:
#                                                       beta        = +0.25 (+0.47, -1.38)
#   Sculptor-- Vitral et al. 2026, ApJ 998, 206 (arXiv:2508.20711), HSTPROMO II, their Table (axisymmetric):
#              at the adopted i = 57.1 deg              beta_J = +0.72 (+0.07, -0.12), beta_bar_B = +0.35 (+0.17, -0.39)
#              inclination-marginalised                 beta_J = +0.13 (+0.78, -1.15), beta_bar_B = -0.56 (+1.33, -2.00)
#              full swing of beta_J across the unconstrained inclination 43.7-90 deg: +0.98 down to -0.88
#              measured plane-of-sky ratio  <sigma_POSt>/<sigma_POSr> = 1.19 +/- 0.19
DRACO_ALT = {"Vitral+24 axisym beta_bar_B": -0.20, "Vitral+24 JAM beta_J": 0.56,
             "Vitral+24 spherical beta_B": 0.39, "Massari+20 spherical NFW beta": 0.25}
SCL_ALT   = {"Vitral+26 i=57.1 beta_J": 0.72, "Vitral+26 i=57.1 beta_bar_B": 0.35,
             "Vitral+26 i-marginalised beta_J": 0.13, "Vitral+26 i-marginalised beta_bar_B": -0.56}
SCL_INC_SWING = (0.98, -0.88)   # beta_J at i = 43.7 deg and i = 85.3 deg, Vitral+26 Table 4

names = [d[0] for d in DSPH]
beta = np.array([1.0 - 10.0 ** (-BZ_HAYASHI[n][0]) for n in names])
sbeta = np.array([math.log(10) * 10.0 ** (-BZ_HAYASHI[n][0]) * 0.5 * (BZ_HAYASHI[n][1] + BZ_HAYASHI[n][2])
                  for n in names])
logM = np.log10(np.array([d[1] for d in DSPH]))

info("N = 8.  These are ALL of the classical dwarf spheroidals; three other populations were considered and are")
info("marked NOT RUN in this file's docstring because no usable published anisotropy exists for them.")
info("The brief's own bar was 'if it is under 8 the test is underpowered'.  It is exactly 8, which is the floor.")

# ---------------------------------------------------------------------------------------------------------
# (b) THE RESIDUAL -- f09's currency, verbatim
# ---------------------------------------------------------------------------------------------------------
def dsph_resid(M, Rh, sob, D, a0, newton=False):
    """f09_orbital_coherence_fork.py, function dsph_resid, reproduced unchanged (newton= adds the mutation).
    log10 of observed over framework-predicted dynamical acceleration for a pressure-supported satellite."""
    Mk, R, s, d = M * Msun, Rh * kpc, sob * 1e3, D * kpc
    g_obs = 3.0 * s * s / R                      # isotropic estimator: 3 sigma^2 / R_half
    g_N = G * Mk / R ** 2
    if newton:
        return math.log10(g_obs / g_N), g_N / a0, "newtonian"
    g_iso = math.sqrt(g_N * a0)                  # isolated deep-MOND
    g_ext = MW_VC ** 2 / d                       # Milky Way external field at the satellite
    g_efe = g_N * nu_s(g_ext / a0)               # quasi-Newtonian boost when the external field dominates
    g_pred = max(g_iso, g_efe)                   # the choice that favours the framework
    return math.log10(g_obs / g_pred), g_N / a0, ("isolated" if g_iso >= g_efe else "EFE")

def residuals(a0, newton=False, table=DSPH):
    return np.array([dsph_resid(d[1], d[2], d[3], d[4], a0, newton)[0] for d in table])

RES = {f: residuals(A0[f]) for f in A0}
REG = [dsph_resid(d[1], d[2], d[3], d[4], A0["canonical"])[2] for d in DSPH]
GN = np.array([dsph_resid(d[1], d[2], d[3], d[4], A0["canonical"])[1] for d in DSPH])

P("")
info(f"{'system':13} {'M*/Msun':>9} {'g_N/a0':>8} {'branch':>9} {'beta_z':>8} {'+-':>6} {'residual dex':>13}")
for i, n in enumerate(names):
    info(f"{n:13} {DSPH[i][1]:9.2e} {GN[i]:8.4f} {REG[i]:>9} {beta[i]:+8.3f} {sbeta[i]:6.3f} "
         f"{RES['canonical'][i]:+13.3f}")

# ---------------------------------------------------------------------------------------------------------
# statistics helpers -- written out so nothing hides in a library
# ---------------------------------------------------------------------------------------------------------
def pear(a, b):
    a = np.asarray(a, float) - np.mean(a); b = np.asarray(b, float) - np.mean(b)
    return float(a @ b / math.sqrt((a @ a) * (b @ b)))

def rankv(x):
    return np.argsort(np.argsort(np.asarray(x, float))).astype(float)

def spear(a, b):
    return pear(rankv(a), rankv(b))

def partial(x, y, z):
    """partial correlation of x and y controlling for z."""
    rxy, rxz, ryz = pear(x, y), pear(x, z), pear(y, z)
    return (rxy - rxz * ryz) / math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))

def perm_p(stat, y, n=NPERM):
    """two-sided permutation p-value: shuffle the anisotropy vector, which is the null 'beta carries nothing'."""
    obs = stat(y); hits = 0
    for _ in range(n):
        if abs(stat(rng.permutation(y))) >= abs(obs) - 1e-12:
            hits += 1
    return obs, (hits + 1) / (n + 1)

def p_to_sigma(p):
    """two-sided p to an equivalent gaussian sigma, by bisection on erfc."""
    p = min(max(p, 1e-12), 1.0)
    lo, hi = 0.0, 12.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if math.erfc(mid / math.sqrt(2.0)) > p: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

NULL_SD = 1.0 / math.sqrt(len(names) - 1)   # sd of Spearman rho under the null at N=8 -> 0.378

# ---------------------------------------------------------------------------------------------------------
# (c) THE CORRELATION
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("B.  THE CORRELATION: residual against measured anisotropy, permutation-tested")
P("=" * 118)

rho_can, p_can = perm_p(lambda b: spear(RES["canonical"], b), beta)
rho_alt, p_alt = perm_p(lambda b: spear(RES["alt"], b), beta)
pe_can = pear(RES["canonical"], beta)
info(f"canonical a0 = {A0['canonical']:.3g}:  Spearman rho = {rho_can:+.3f}, Pearson r = {pe_can:+.3f}, "
     f"permutation p = {p_can:.4f}  ({p_to_sigma(p_can):.2f} sigma)")
info(f"alt       a0 = {A0['alt']:.3g}:  Spearman rho = {rho_alt:+.3f}, Pearson r = {pear(RES['alt'], beta):+.3f}, "
     f"permutation p = {p_alt:.4f}  ({p_to_sigma(p_alt):.2f} sigma)")
info(f"{NPERM} permutations per p-value; null sd of Spearman rho at N=8 is 1/sqrt(N-1) = {NULL_SD:.3f}")

# how large a sample would the OBSERVED effect need to reach 3 sigma?
def n_for_3sigma(r):
    for N in range(8, 400):
        t = abs(r) * math.sqrt((N - 2) / max(1 - r * r, 1e-9))
        if t > 3.0: return N
    return None
N3 = n_for_3sigma(rho_can)

ck("A1 (SAMPLE SIZE, AND IT FAILS BY CONSTRUCTION) the within-population anisotropy test needs a sample large "
   "enough that the effect it finds could reach three sigma.  Only eight classical dwarf spheroidals exist, and "
   "they are the ONLY pressure-supported systems in the sky with a homogeneous published anisotropy and the "
   "structural data the framework's kernel needs.  Three further populations were considered and none supplies "
   "a usable anisotropy",
   len(names) >= N3,
   f"N = {len(names)}; at the measured rho = {rho_can:+.3f} a three-sigma detection would need N = {N3}. "
   f"Early-type galaxies NOT RUN (no per-galaxy anisotropy in the repository and the ATLAS3D JAM catalogue does "
   f"not resolve in VizieR); outer-halo globulars Pal 4 / Pal 14 NOT RUN (no published internal anisotropy); "
   f"galaxy clusters NOT RUN (published beta comes from NFW-based MAMPOSSt modelling, maximal circularity)")

ck("A2 (THE TEST ITSELF) the deficit correlates with measured anisotropy at three sigma, in the sense modified "
   "inertia would suggest -- more radially biased orbits sitting further above the framework's kernel",
   p_can < 0.0027,
   f"Spearman rho = {rho_can:+.3f}, permutation p = {p_can:.4f}, i.e. {p_to_sigma(p_can):.2f} sigma. The sign IS "
   f"positive and IS the direction a trajectory-dependent modification would suggest, but this is a HINT at the "
   f"same strength as f09's 1.7 sigma and must never be quoted higher")

ck("A3 the correlation is a property of the data and not of the acceleration constant: it must be the same on "
   "both footings of a0",
   abs(rho_can - rho_alt) < 0.05 and rho_can * rho_alt > 0,
   f"canonical rho = {rho_can:+.3f}, alt rho = {rho_alt:+.3f}; the residuals shift with a0 but their ORDERING "
   f"does not, so the rank correlation is footing-independent")

# independent structural compilation -- Local Volume Database (Pace 2024), already in the repository
LVD = os.path.join(DATA, "dsph", "lvd_dwarf_mw.csv")
lvd = {r["name"]: r for r in csv.DictReader(open(LVD))}
DSPH_LVD = [(n, 10 ** float(lvd[n]["mass_stellar"]), float(lvd[n]["rhalf_sph_physical"]) / 1000.0,
             float(lvd[n]["vlos_sigma"]), float(lvd[n]["distance_gc"])) for n in names]
res_lvd = residuals(A0["canonical"], table=DSPH_LVD)
logM_lvd = np.array([math.log10(d[1]) for d in DSPH_LVD])
rho_lvd = spear(res_lvd, beta)
ck("A4 (STRUCTURAL ROBUSTNESS) the correlation must not depend on which compilation of stellar masses, half-light "
   "radii, dispersions and Galactocentric distances is used.  Recomputed from the Local Volume Database already "
   "in this repository (real_research/data/dsph/lvd_dwarf_mw.csv), independent of f09's hand-entered table",
   rho_lvd * rho_can > 0 and abs(rho_lvd - rho_can) < NULL_SD,
   f"f09 compilation rho = {rho_can:+.3f}; Local Volume Database rho = {rho_lvd:+.3f}; the two residual vectors "
   f"correlate at r = {pear(res_lvd, RES['canonical']):+.3f}. Difference {abs(rho_lvd - rho_can):.3f} is inside "
   f"the null sd {NULL_SD:.3f}, so the structural compilation is not driving anything")

# ---------------------------------------------------------------------------------------------------------
# (d) THE CONFOUND: mass
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("C.  THE CONFOUND: beta correlates with system type and mass, so mass must be partialled out")
P("=" * 118)
r_res_M = pear(RES["canonical"], logM)
r_beta_M = pear(beta, logM)
pr, p_pr = perm_p(lambda b: partial(RES["canonical"], b, logM), beta)
pr_alt = partial(RES["alt"], beta, logM)
pr_lvd = partial(res_lvd, beta, logM_lvd)
info(f"residual vs log M*      : r = {r_res_M:+.3f}   <-- the residual is very nearly a stellar-mass relation")
info(f"anisotropy vs log M*    : r = {r_beta_M:+.3f}")
info(f"partial(residual, beta | log M*) = {pr:+.3f}, permutation p = {p_pr:.4f} ({p_to_sigma(p_pr):.2f} sigma)")
info(f"same on the alt footing = {pr_alt:+.3f};  same on the Local Volume Database = {pr_lvd:+.3f}")
for lab, ctrl in [("log g_N/a0", np.log10(GN)), ("log R_half", np.log10([d[2] for d in DSPH])),
                  ("log sigma", np.log10([d[3] for d in DSPH]))]:
    info(f"partial controlling {lab:12}: {partial(RES['canonical'], beta, ctrl):+.3f}")

ck("A5 (THE CONFOUND CHECK, AND IT DOES NOT CLEAR ITS BAR) partialling out stellar mass must leave the "
   "anisotropy correlation significant at the five per cent level, otherwise the correlation cannot be "
   "distinguished from the mass trend that dark matter also predicts",
   p_pr < 0.05,
   f"partial r = {pr:+.3f} (it goes UP from the raw {pe_can:+.3f}, i.e. mass is not manufacturing it), but "
   f"permutation p = {p_pr:.4f} = {p_to_sigma(p_pr):.2f} sigma, short of the bar. AND NOTE THE WARNING: the "
   f"residual correlates with log M* at r = {r_res_M:+.3f}, so the currency is very nearly a stellar-mass "
   f"relation on its own and partialling it out removes most of the variance in a sample of eight")

# ---------------------------------------------------------------------------------------------------------
# (e) MUTATION CONTROLS
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("D.  MUTATION CONTROLS")
P("=" * 118)
res_newt = residuals(A0["canonical"], newton=True)
rho_newt = spear(res_newt, beta)
pr_newt = partial(res_newt, beta, logM)
info(f"M1 kernel OFF (nu = 1, pure Newtonian residual log10(g_obs/g_N)): rho = {rho_newt:+.3f}, "
     f"partial|logM = {pr_newt:+.3f}")
shuf = np.array([abs(spear(RES["canonical"], rng.permutation(beta))) for _ in range(NPERM // 5)])
info(f"M2 shuffled anisotropy, {len(shuf)} draws: 95th percentile |rho| = {np.percentile(shuf, 95):.3f}, "
     f"observed |rho| = {abs(rho_can):.3f}")
fake = rng.uniform(beta.min(), beta.max(), size=(2000, len(beta)))
rf = np.array([abs(spear(RES["canonical"], f)) for f in fake])
info(f"M3 anisotropy replaced by uniform draws over the same range: mean |rho| = {rf.mean():.3f}, "
     f"fraction exceeding the observed = {(rf >= abs(rho_can)).mean():.3f}")

ck("A6 (THE MUTATION THAT MATTERS, AND IT FAILS) if the correlation is about the framework's kernel, then "
   "turning the kernel OFF must destroy it.  Replacing nu by 1 -- pure Newtonian gravity, no modification of "
   "any kind -- and correlating the resulting mass discrepancy against the same anisotropies must leave a much "
   "weaker correlation",
   abs(rho_newt) < 0.30,
   f"Newtonian mutation still gives rho = {rho_newt:+.3f} against the framework's {rho_can:+.3f}, i.e. about "
   f"{abs(rho_newt / rho_can) * 100:.0f} per cent of the signal survives with gravity completely unmodified. So "
   f"most of what is being measured is a mass-discrepancy/anisotropy relation among dwarf spheroidals, which "
   f"dark matter produces too, not a fingerprint of a trajectory-dependent modification")

ck("A7 (SHUFFLE MUTATION) the observed correlation must exceed the 95th percentile of the shuffled-anisotropy "
   "null, which is the same bar f08's withdrawn result failed",
   abs(rho_can) > np.percentile(shuf, 95),
   f"observed |rho| = {abs(rho_can):.3f} against a 95th percentile of {np.percentile(shuf, 95):.3f}; with eight "
   f"objects a rank correlation of 0.67 is simply not rare under the null")

# ---------------------------------------------------------------------------------------------------------
# (f) THE CIRCULARITY AUDIT -- the part that decides this file
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("E.  THE CIRCULARITY AUDIT: are these anisotropies usable to test a theory with no dark-matter halo?")
P("=" * 118)
info("Every published beta for a dwarf spheroidal is fitted JOINTLY with a dark-matter halo.  That is the")
info("mass-anisotropy degeneracy.  The question is not whether it exists but HOW BIG it is compared with the")
info("signal, and the two galaxies with resolved internal proper motions answer it directly.")

between = float(beta.max() - beta.min())
draco_vals = [beta[names.index("Draco")]] + list(DRACO_ALT.values())
scl_vals = [beta[names.index("Sculptor")]] + list(SCL_ALT.values())
draco_spread = max(draco_vals) - min(draco_vals)
scl_spread = max(scl_vals) - min(scl_vals)
P("")
info(f"between-object spread of the homogeneous set (Hayashi+2020, 8 objects): {beta.min():+.3f} to "
     f"{beta.max():+.3f}  =  {between:.3f}   <-- the entire signal lives inside this")
info("Draco, published anisotropies, all from proper-motion or line-of-sight data on the same galaxy:")
info(f"    Hayashi+2020 beta_z (axisym Jeans, gen-Hernquist halo)      {beta[names.index('Draco')]:+.3f}")
for k, v in DRACO_ALT.items(): info(f"    {k:56} {v:+.3f}")
info(f"    -> spread for ONE galaxy: {draco_spread:.3f}")
info("Sculptor, same:")
info(f"    Hayashi+2020 beta_z (axisym Jeans, gen-Hernquist halo)      {beta[names.index('Sculptor')]:+.3f}")
for k, v in SCL_ALT.items(): info(f"    {k:56} {v:+.3f}")
info(f"    -> spread for ONE galaxy: {scl_spread:.3f}")

ck("A8 (THE DECISIVE ONE) the per-object spread across published re-analyses must be SMALLER than the "
   "between-object spread the correlation is built from.  If one galaxy's anisotropy is less well known than the "
   "difference between galaxies, the ordering that the rank correlation depends on is not measured",
   max(draco_spread, scl_spread) < between,
   f"Draco spans {draco_spread:.3f} and Sculptor spans {scl_spread:.3f} across published values, against a "
   f"between-object spread of only {between:.3f}. The two BEST-measured dwarf spheroidals in the sky each carry "
   f"a method-to-method uncertainty LARGER than the whole dynamic range of the test")

# substitution test
P("")
info("SUBSTITUTION TEST -- swap the two Jeans-derived values for the direct proper-motion-based ones and rerun:")
subs = [("Hayashi+2020 throughout (the baseline)", beta[names.index("Draco")], beta[names.index("Sculptor")]),
        ("Vitral axisymmetric beta_bar_B (the least model-dependent)", -0.20, 0.35),
        ("Vitral meridional beta_J", 0.56, 0.72),
        ("Vitral inclination-marginalised beta_J", 0.13, 0.13),
        ("Massari+20 Draco / Vitral i=57.1 Sculptor", 0.25, 0.72)]
sub_rhos = []
for lab, dv, sv in subs:
    b2 = beta.copy(); b2[names.index("Draco")] = dv; b2[names.index("Sculptor")] = sv
    r_, pr_ = spear(RES["canonical"], b2), partial(RES["canonical"], b2, logM)
    sub_rhos.append(r_)
    info(f"    {lab:58} rho = {r_:+.3f}   partial|logM = {pr_:+.3f}   Pearson = {pear(RES['canonical'], b2):+.3f}")
worst = max(abs(r - rho_can) for r in sub_rhos)
ck("A9 (SUBSTITUTION) the correlation must survive replacing the two Jeans-derived anisotropies with the "
   "proper-motion-based ones measured by the same technique on the same galaxies.  Those are the only two "
   "anisotropies in the sample that are constrained by data rather than by a halo prior",
   worst < NULL_SD,
   f"largest change in Spearman rho under substitution is {worst:.3f}, against a null sd of {NULL_SD:.3f}. "
   f"Substituting the least model-dependent values (Vitral axisymmetric) collapses the correlation from "
   f"{rho_can:+.3f} to {sub_rhos[1]:+.3f} and the Pearson coefficient to essentially zero. The result depends "
   f"entirely on which published anisotropy is adopted for two of the eight objects")

ck("A10 (THE NUISANCE PARAMETER) the published anisotropy of a single galaxy must not swing across the whole "
   "physical range when one unconstrained nuisance parameter is varied.  Vitral+2026 fit Sculptor at eleven "
   "inclinations from 43.7 to 90 degrees, all giving acceptable fits, because their Jeans models do not "
   "constrain the inclination at all",
   abs(SCL_INC_SWING[0] - SCL_INC_SWING[1]) < between,
   f"Sculptor's beta_J runs from {SCL_INC_SWING[0]:+.2f} to {SCL_INC_SWING[1]:+.2f}, a swing of "
   f"{abs(SCL_INC_SWING[0] - SCL_INC_SWING[1]):.2f}, driven by NOTHING but the assumed viewing angle, against a "
   f"between-object spread of {between:.3f}. Their inclination-marginalised value is beta_J = +0.13 (+0.78,-1.15)")

# transportability: is the framework's own phantom profile close enough to the fitted haloes that a published
# beta can be carried across?
def phantom_logslope(Mb_Msun, b_pc, r_lo_pc, r_hi_pc, a0):
    """log slope of the framework's PHANTOM dark-matter density for a Plummer sphere, isolated branch.
    QUMOND: M_dyn(r) = nu(g_N/a0) M(r), so M_phantom(r) = (nu - 1) M(r) and rho_ph = dM_ph/dr / (4 pi r^2)."""
    b = b_pc * kpc / 1000.0
    def Mph(r):
        M = Mb_Msun * Msun * r ** 3 / (r * r + b * b) ** 1.5
        return (nu_s(G * M / r ** 2 / a0) - 1.0) * M
    def rho(r):
        h = r * 1e-4
        return (Mph(r + h) - Mph(r - h)) / (2 * h) / (4 * math.pi * r * r)
    r1, r2 = r_lo_pc * kpc / 1000.0, r_hi_pc * kpc / 1000.0
    return (math.log(rho(r2)) - math.log(rho(r1))) / (math.log(r2) - math.log(r1))

P("")
info("TRANSPORTABILITY.  A beta fitted inside a dark halo can only be reused to test the framework if the")
info("framework's own mass profile is close to that halo.  Plummer scale lengths from Hayashi+2020 Table 1;")
info("published slopes Gamma_dark over the same radii from Vitral+2024 (Draco) and Vitral+2026 (Sculptor).")
TRANS = [("Draco", 2.9e5, 214.0, -0.83), ("Sculptor", 2.3e6, 280.0, +0.29)]
gaps = []
for nm, Mb, bpc, gam in TRANS:
    s_can = phantom_logslope(Mb, bpc, 120.0, 240.0, A0["canonical"])
    s_alt = phantom_logslope(Mb, bpc, 120.0, 240.0, A0["alt"])
    gaps.append(abs(s_can - gam))
    info(f"    {nm:9} framework phantom dln(rho)/dln(r) over 120-240 pc = {s_can:+.3f} (canonical), "
         f"{s_alt:+.3f} (alt);  published fitted halo Gamma_dark = {gam:+.3f};  gap {abs(s_can - gam):.2f}")
ck("A11 (TRANSPORTABILITY / CIRCULARITY) the framework's own phantom mass profile must be close to the halo "
   "inside which the published anisotropies were fitted, otherwise those anisotropies cannot be carried across. "
   "Vitral+2024 state the degeneracy explicitly -- models with a core require more radial anisotropy -- so a "
   "different assumed profile moves beta by a non-negligible amount, in a way that differs object by object",
   max(gaps) < 0.5,
   f"the framework's phantom halo is CUSPIER than the fitted haloes by {gaps[0]:.2f} (Draco) and {gaps[1]:.2f} "
   f"(Sculptor) in log slope. By the published degeneracy that pushes the inferred beta TANGENTIAL relative to "
   f"the quoted values, by an object-dependent amount comparable to the whole between-object spread. Nobody has "
   f"re-derived beta inside this framework's potential, so no published beta is transportable into it")

# ---------------------------------------------------------------------------------------------------------
# (g) ERROR PROPAGATION AND THE THEORY LIMIT
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("F.  ERROR PROPAGATION, AND THE LIMIT THE THEORY ITSELF PUTS ON THIS OBSERVABLE")
P("=" * 118)
mc = np.array([spear(RES["canonical"], np.clip(beta + rng.normal(0, sbeta), -3.0, 0.999))
               for _ in range(20000)])
info(f"Monte Carlo over the published 68 per cent intervals ({len(mc)} draws): rho median {np.median(mc):+.3f}, "
     f"16-84 range {np.percentile(mc, 16):+.3f} to {np.percentile(mc, 84):+.3f}, "
     f"fraction positive {(mc > 0).mean():.3f}")
info(f"median published uncertainty on beta is {np.median(sbeta):.3f}, against a between-object spread of "
     f"{between:.3f} -- the error bars are half the whole dynamic range before any method systematic is added")
ck("A12 (ERROR PROPAGATION) propagating only the quoted statistical uncertainties, the SIGN of the correlation "
   "should be robust in at least 90 per cent of draws",
   (mc > 0).mean() > 0.90,
   f"{(mc > 0).mean() * 100:.1f} per cent of draws are positive. This is the ONE thing in this file that passes "
   f"cleanly, and it is worth almost nothing, because the quoted statistical errors are far smaller than the "
   f"method-to-method spread measured in A8-A10, which the Monte Carlo does not include")

ck("A13 (THE THEORY LIMIT ON THE OBSERVABLE ITSELF) the observable used here must be one for which modified "
   "inertia and modified gravity actually differ.  The deep-MOND virial relation -- which is what a global "
   "sigma^2/R residual measures -- is a theorem in modified-gravity formulations AND was derived for "
   "modified-inertia formulations by Milgrom 1994 (Ann. Phys. 229, 384; see also Milgrom 1997, Phys. Rev. E 56, "
   "1148). So the arms are proven to AGREE on this observable in the deep-MOND limit",
   False,
   f"all eight dwarfs sit at g_N/a0 = {GN.min():.4f} to {GN.max():.4f}, i.e. deep in the MOND regime where the "
   f"virial relation is common to both arms. Any anisotropy dependence is therefore a SECOND-ORDER effect, and "
   f"modified inertia -- being a class rather than a theory -- predicts NEITHER its sign NOR its size. That "
   f"forces a two-sided test, halves the power, and means even a clean correlation would not by itself select "
   f"an arm. Marked as a FAIL because it is a structural limit on the test, not on the data")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118); P("VERDICT"); P("=" * 118)
P(f"  THE CORRELATION EXISTS AND IS NOT A RESULT.  Spearman rho = {rho_can:+.3f} (canonical), {rho_alt:+.3f} (alt),")
P(f"  permutation p = {p_can:.3f} = {p_to_sigma(p_can):.2f} sigma on eight objects. Controlling for stellar mass does NOT")
P(f"  weaken it ({pr:+.3f}, p = {p_pr:.3f}), so it is not obviously the mass trend dark matter also predicts, and the")
P(f"  sign is the one a trajectory-dependent modification would suggest. Quote it at 1.7 sigma or not at all.")
P("")
P("  THREE THINGS KILL IT, AND THEY ARE THE POINT OF THIS FILE:")
P(f"  1. THE INPUT VARIABLE IS NOT MEASURED WELL ENOUGH FOR THE TEST TO BE RUN. Published anisotropies for a")
P(f"     SINGLE galaxy span {draco_spread:.2f} (Draco) and {scl_spread:.2f} (Sculptor); the between-object spread the whole")
P(f"     correlation rests on is {between:.2f}. Varying nothing but Sculptor's unconstrained inclination moves its beta")
P("     from +0.98 to -0.88. The ORDERING of the eight objects in anisotropy is simply not established.")
P(f"  2. SUBSTITUTING THE BEST-MEASURED VALUES COLLAPSES IT. Using the proper-motion-based axisymmetric")
P(f"     anisotropies for Draco and Sculptor takes rho from {rho_can:+.3f} to {sub_rhos[1]:+.3f} and Pearson r to zero.")
P(f"  3. IT PARTLY SURVIVES TURNING GRAVITY BACK TO NEWTON. The same correlation computed with nu = 1 gives")
P(f"     rho = {rho_newt:+.3f}, so roughly {abs(rho_newt / rho_can) * 100:.0f} per cent of it is a mass-discrepancy/anisotropy relation among")
P("     dwarf spheroidals that dark matter produces as readily as any modification.")
P("")
P("  AND THE CIRCULARITY IS WORSE THAN A CAVEAT: the framework's own phantom halo is CUSPIER than the haloes")
P("  inside which these anisotropies were fitted, and the published mass-anisotropy degeneracy (core <-> radial)")
P("  then shifts beta by an object-dependent amount of order the entire signal. No published beta is")
P("  transportable into a theory with no dark-matter halo without redoing the modelling, which nobody has done.")
P("")
P("  WHAT WOULD MAKE THIS TEST REAL, and it is cheap to state: resolved internal proper motions for six more")
P(f"  classical dwarf spheroidals (N = {N3} would carry the measured effect to three sigma), each analysed")
P("  axisymmetrically with the inclination constrained by higher-order moments as Vitral+2024/2026 do -- and,")
P("  separately, the anisotropy re-derived inside the framework's own potential so the input is not borrowed")
P("  from a dark-matter fit. Until then this is a hint on top of a hint, and the fork stays open.")
P("")
P("  NOTHING HERE RESCUES CLUSTERS and nothing here reopens the excluded modified-inertia action; f09's four")
P("  honest limits all still apply, and dark matter explains this pattern exactly as well.")
sys.exit(ck.done())
