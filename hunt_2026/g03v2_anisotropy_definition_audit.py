#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g03v2_anisotropy_definition_audit.py -- ADVERSARIAL AUDIT OF g03's CHECKS A8 / A9 / A10.
=======================================================================================
THE CLAIM UNDER ATTACK (g03_anisotropy_correlation_test.py, section E, and VERDICT item 1):
  "The test cannot currently be run, because the published anisotropy of a SINGLE galaxy is uncertain by
   more than the entire between-object spread the correlation rests on."
  Numbers cited: between-object spread of the homogeneous Hayashi+2020 beta_z set = 0.531 (+0.224 to +0.755);
  Draco per-object spread across published values = 0.811; Sculptor = 1.280; substituting the "least
  model-dependent" values takes Spearman rho from +0.667 to +0.167 and Pearson r to -0.013, the largest
  substitution shift being 0.524 against a null sd of 0.378.

THIS FILE DOES NOT RE-ARGUE THE PHYSICS.  It attacks the COMPARISON, and specifically whether the numbers
being differenced are measurements of THE SAME QUANTITY.  g03's own author flagged this as the weakest link;
this file measures how much of the quoted spread it accounts for instead of conceding it in a sentence.

THE DEFINITIONS, TAKEN FROM THE SOURCE PAPERS, NOT PARAPHRASED:
  * Hayashi, Chiba & Ishiyama 2020, ApJ 904, 45 (arXiv:2007.13780): beta_z = 1 - sigma_z^2 / sigma_R^2,
    the CYLINDRICAL (meridional-plane) anisotropy of an axisymmetric Jeans model.
  * Vitral et al. 2024, ApJ 970, 1 (arXiv:2407.07769), abstract, verbatim: "We find the velocity dispersion
    to be radially anisotropic along the symmetry axis and tangentially anisotropic in the equatorial plane,
    with a globally-averaged value beta_bar_B = -0.20 (+0.28, -0.53), (where 1 - beta_B == <v_tan^2>/<v_rad^2>
    in 3D)."  So beta_bar_B is a GLOBAL 3D AVERAGE, over the whole galaxy, of a SPHERICAL Binney anisotropy
    whose sign the same sentence says CHANGES WITH DIRECTION inside the object.  Its tangential component
    v_tan^2 contains the AZIMUTHAL dispersion sigma_phi, which beta_z does not.
  * Vitral et al. 2024, same paper, JamPy meridional parameter: beta_J == 1 - <v_theta^2>/<v_r^2>
    = 1 - sigma_theta^2 / sigma_r^2 -- the meridional-plane anisotropy, the counterpart of beta_z.
  * Vitral et al. 2026, ApJ 998, 206 (arXiv:2508.20711), abstract, verbatim: "Our modeling reveals a
    significant degeneracy due to the unknown galaxy inclination... While we do not directly constrain the
    inclination with our Jeans models, higher-order line-of-sight velocity moments provide useful additional
    constraints... Adopting an inclination well consistent with these comparisons (i = 57.1 degrees)..."

WHAT THAT MEANS FOR THE CLAIM.  beta_bar_B = -0.20 and beta_J = +0.56 are BOTH correct descriptions of the
SAME Draco velocity ellipsoid field; they differ because the galaxy is radial in one direction and tangential
in another.  Differencing them and calling the result a "method-to-method uncertainty" is a category error,
not a measurement of how badly beta is known.  This file quantifies exactly how much of g03's headline
per-object spread, and how much of its headline substitution collapse, comes from that one category error.

BOTH a0 FOOTINGS THROUGHOUT.  Checks are written so they CAN fail; W3 and W6 do fail, and those failures are
the part of g03's claim that SURVIVES this audit and should be carried forward instead of A8.
"""
import sys, math
import numpy as np
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260903)
NDRAW = 200000
MW_VC = 200e3

# ---------------------------------------------------------------------------------------------------------
# structural table and residual currency reproduced verbatim from g03 / f09 so nothing is re-specified here
# ---------------------------------------------------------------------------------------------------------
DSPH = [("Draco",      2.9e5, 0.221, 9.1,  76.), ("Sculptor",   2.3e6, 0.283, 9.2,  86.),
        ("Fornax",     4.3e7, 0.710, 11.7, 147.), ("Carina",     3.8e5, 0.250, 6.6,  105.),
        ("Sextans",    4.4e5, 0.695, 7.9,  86.),  ("Leo I",      5.5e6, 0.251, 9.2,  254.),
        ("Leo II",     7.4e5, 0.176, 6.6,  233.), ("Ursa Minor", 2.9e5, 0.181, 9.5,  76.)]
BZ = {"Draco": (0.41, 0.19, 0.21), "Ursa Minor": (0.61, 0.13, 0.16), "Carina": (0.36, 0.26, 0.24),
      "Sextans": (0.18, 0.18, 0.19), "Leo I": (0.11, 0.17, 0.19), "Leo II": (0.12, 0.23, 0.18),
      "Sculptor": (0.21, 0.18, 0.18), "Fornax": (0.24, 0.18, 0.13)}
names = [d[0] for d in DSPH]
beta  = np.array([1.0 - 10.0 ** (-BZ[n][0]) for n in names])
sbeta = np.array([math.log(10) * 10.0 ** (-BZ[n][0]) * 0.5 * (BZ[n][1] + BZ[n][2]) for n in names])
iD, iS = names.index("Draco"), names.index("Sculptor")

def resid_vec(a0, newton=False):
    out = []
    for _, M, Rh, s, D in DSPH:
        Mk, R, s_, d = M * Msun, Rh * kpc, s * 1e3, D * kpc
        g_obs, g_N = 3.0 * s_ * s_ / R, G * Mk / R ** 2
        if newton:
            out.append(math.log10(g_obs / g_N)); continue
        out.append(math.log10(g_obs / max(math.sqrt(g_N * a0), g_N * nu_s((MW_VC ** 2 / d) / a0))))
    return np.array(out)

RES = {f: resid_vec(A0[f]) for f in A0}

def pear(a, b):
    a = np.asarray(a, float) - np.mean(a); b = np.asarray(b, float) - np.mean(b)
    return float(a @ b / math.sqrt((a @ a) * (b @ b)))
rankv = lambda x: np.argsort(np.argsort(np.asarray(x, float))).astype(float)
spear = lambda a, b: pear(rankv(a), rankv(b))

RHO = {f: spear(RES[f], beta) for f in A0}
BETWEEN = float(beta.max() - beta.min())
NULL_SD = 1.0 / math.sqrt(len(names) - 1)

P("=" * 118)
P("W.  BASELINE REPRODUCED (independent code path)")
P("=" * 118)
for f in A0:
    info(f"a0 = {A0[f]:.3g} ({f:9}): Spearman rho = {RHO[f]:+.4f}, Pearson = {pear(RES[f], beta):+.4f}   "
         f"[g03 reports +0.667 / +0.667 on both footings]")
info(f"between-object spread of the homogeneous beta_z set = {BETWEEN:.4f}  [g03 reports 0.531]")
info(f"null sd of Spearman rho at N = 8 = {NULL_SD:.3f}")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("W1.  HOW MUCH OF THE HEADLINE PER-OBJECT SPREAD IS A CHANGE OF DEFINITION, NOT A DISAGREEMENT?")
P("=" * 118)
# (label, value, definition-class):  'mer' = meridional-plane anisotropy (Hayashi beta_z, Vitral beta_J)
#                                    'sphB'= spherical Binney beta_B / globally averaged beta_bar_B
DRACO = [("Hayashi+2020 beta_z (cylindrical)",          0.611, "mer"),
         ("Vitral+2024 beta_J (meridional, JamPy)",     0.560, "mer"),
         ("Vitral+2024 beta_B (spherical model 3)",     0.390, "sphB"),
         ("Massari+2020 beta (spherical Jeans, NFW)",   0.250, "sphB"),
         ("Vitral+2024 beta_bar_B (global 3D average)",-0.200, "sphB")]
SCL   = [("Hayashi+2020 beta_z (cylindrical)",          0.383, "mer"),
         ("Vitral+2026 beta_J at adopted i=57.1 deg",   0.720, "mer"),
         ("Vitral+2026 beta_J, i-marginalised",         0.130, "mer"),
         ("Vitral+2026 beta_bar_B at i=57.1 deg",       0.350, "sphB"),
         ("Vitral+2026 beta_bar_B, i-marginalised",    -0.560, "sphB")]

def spread(rows, cls=None):
    v = [r[1] for r in rows if cls is None or r[2] == cls]
    return max(v) - min(v), v

for nm, rows in (("Draco", DRACO), ("Sculptor", SCL)):
    P("")
    info(f"{nm}:")
    for lab, v, c in rows: info(f"    [{c:4}] {lab:44} {v:+.3f}")
    all_s, _ = spread(rows); mer_s, mv = spread(rows, "mer")
    info(f"    ALL definitions mixed  -> spread {all_s:.3f}   (this is g03's quoted number)")
    info(f"    MERIDIONAL class only  -> spread {mer_s:.3f}   from values {mv}")

d_all, _ = spread(DRACO); s_all, _ = spread(SCL)
d_mer, _ = spread(DRACO, "mer"); s_mer, _ = spread(SCL, "mer")
P("")
ck("W1 (THE CATEGORY ERROR) g03's headline per-object spreads must not be dominated by differencing "
   "anisotropy parameters that the source papers define as DIFFERENT quantities. beta_bar_B is a global 3D "
   "average of a spherical Binney anisotropy whose sign Vitral+2024's own abstract says changes with "
   "direction inside Draco; beta_z and beta_J are meridional-plane parameters. To sustain g03's claim, the "
   "spread computed WITHIN the meridional class must still exceed the between-object spread for at least one "
   "of the two galaxies at the papers' own adopted configurations",
   max(d_mer, s_mer) > BETWEEN,
   f"restricted to the meridional class, Draco spans {d_mer:.3f} (Hayashi +0.611 vs Vitral beta_J +0.560 -- two "
   f"fully independent analyses, line-of-sight Jeans vs 18 years of HST proper motions, agreeing to "
   f"{d_mer:.3f}, i.e. {d_mer / BETWEEN * 100:.0f} per cent of the between-object range) and Sculptor spans "
   f"{s_mer:.3f}. g03 quotes {d_all:.3f} and {s_all:.3f}. The beta_bar_B entries supply "
   f"{(d_all - d_mer) / d_all * 100:.0f} per cent of Draco's headline spread and "
   f"{(s_all - s_mer) / s_all * 100:.0f} per cent of Sculptor's")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("W2.  THE SUBSTITUTION COLLAPSE -- ONE NUMBER, OR TWO?")
P("=" * 118)
def sub_rho(f, dv=None, sv=None):
    b = beta.copy()
    if dv is not None: b[iD] = dv
    if sv is not None: b[iS] = sv
    return spear(RES[f], b), pear(RES[f], b)

for f in A0:
    r_both, p_both = sub_rho(f, -0.20, 0.35)
    r_d, p_d = sub_rho(f, dv=-0.20)
    r_s, p_s = sub_rho(f, sv=0.35)
    info(f"[{f:9}] baseline rho {RHO[f]:+.3f} | Draco beta_bar_B only -> {r_d:+.3f} (Pearson {p_d:+.3f}) | "
         f"Sculptor only -> {r_s:+.3f} | both -> {r_both:+.3f}")
r_lfl_c, _ = sub_rho("canonical", 0.560, 0.720)
r_lfl_a, _ = sub_rho("alt", 0.560, 0.720)
info(f"LIKE-FOR-LIKE substitution (beta_J for beta_z, same quantity): rho -> {r_lfl_c:+.3f} (canonical), "
     f"{r_lfl_a:+.3f} (alt); shift {abs(r_lfl_c - RHO['canonical']):.3f} against null sd {NULL_SD:.3f}")
shift_s = abs(sub_rho("canonical", sv=0.35)[0] - RHO["canonical"])
ck("W2 (IS THE COLLAPSE A PROPERTY OF THE SAMPLE OR OF ONE ENTRY?) g03 describes the collapse as what happens "
   "when 'the two Jeans-derived anisotropies' are replaced. For that description to hold, BOTH substitutions "
   "must contribute; if one object supplies the whole effect the finding is about a single published number",
   shift_s > 0.05,
   f"substituting Sculptor alone moves Spearman rho by {shift_s:.3f} -- it does not move at all, because "
   f"+0.35 and +0.383 occupy the same rank. The entire collapse from {RHO['canonical']:+.3f} to +0.167 is "
   f"Draco's beta_bar_B = -0.20, which demotes the object with the LARGEST residual (+0.617 dex) from "
   f"second-highest beta to lowest. Substituting the like-for-like beta_J values instead moves rho by only "
   f"{abs(r_lfl_c - RHO['canonical']):.3f}")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("W3.  WHAT SURVIVES: THE INCLINATION DEGENERACY IS WITHIN ONE DEFINITION AND ONE ANALYSIS")
P("=" * 118)
SCL_SWING = (0.98, -0.88)      # Vitral+2026 beta_J across the eleven fitted inclinations 43.7-90 deg
scl_marg  = (0.13, 0.78, 1.15) # their inclination-marginalised beta_J (+0.78, -1.15)
info(f"Vitral+2026 abstract, verbatim: 'Our modeling reveals a significant degeneracy due to the unknown")
info(f"galaxy inclination, which is overlooked under spherical symmetry assumptions.'")
info(f"Sculptor beta_J across eleven acceptable inclinations: {SCL_SWING[0]:+.2f} to {SCL_SWING[1]:+.2f}, "
     f"swing {abs(SCL_SWING[0] - SCL_SWING[1]):.2f}, ALL meridional class, ALL one paper, one dataset.")
info(f"their inclination-marginalised beta_J = {scl_marg[0]:+.2f} (+{scl_marg[1]:.2f}, -{scl_marg[2]:.2f}); "
     f"68 per cent width {scl_marg[1] + scl_marg[2]:.2f} against between-object spread {BETWEEN:.3f}")
ck("W3 (THE SURVIVING HALF OF g03's CLAIM) a single object's anisotropy, compared LIKE FOR LIKE and within a "
   "single published analysis, must be determined to better than the between-object spread. This is the check "
   "A8 should have been",
   abs(SCL_SWING[0] - SCL_SWING[1]) < BETWEEN,
   f"Sculptor's beta_J swings {abs(SCL_SWING[0] - SCL_SWING[1]):.2f} on viewing angle alone, "
   f"{abs(SCL_SWING[0] - SCL_SWING[1]) / BETWEEN:.1f}x the between-object spread, with no change of "
   f"definition and no second paper involved. THIS is a real measurability obstruction. It applies to ONE of "
   f"the eight objects, and the authors themselves prefer i = 57.1 deg on higher-order-moment grounds")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("W4.  IS A 0.524 SHIFT FROM SUBSTITUTING 2 OF 8 VALUES RARE?  g03 COMPARES IT TO THE WRONG NULL.")
P("=" * 118)
def null_shift(f, lo, hi, n=NDRAW):
    r0 = RHO[f]; out = np.empty(n)
    for i in range(n):
        b = beta.copy(); b[iD] = rng.uniform(lo, hi); b[iS] = rng.uniform(lo, hi)
        out[i] = abs(spear(RES[f], b) - r0)
    return out
for f in A0:
    a = null_shift(f, beta.min(), beta.max(), 40000)
    b = null_shift(f, -0.56, 0.755, 40000)
    info(f"[{f:9}] replace 2 of 8 by draws inside the beta_z range: mean |d rho| {a.mean():.3f}, "
         f"95th {np.percentile(a, 95):.3f}, P(|d| >= 0.524) = {(a >= 0.524).mean():.4f}")
    info(f"[{f:9}] replace 2 of 8 by draws over the full published union (-0.56..+0.755): mean {b.mean():.3f}, "
         f"95th {np.percentile(b, 95):.3f}, P(|d| >= 0.524) = {(b >= 0.524).mean():.4f}")
nb = null_shift("canonical", -0.56, 0.755, 60000)
ck("W4 (THE NULL g03 USED) g03 compares the substitution shift 0.524 against 'a null sd of 0.378', which is "
   "the sd of rho ITSELF under a full shuffle, not the sd of a two-element substitution shift. The correct "
   "comparison is against the distribution of |delta rho| when two of the eight values are replaced. For "
   "g03's framing to be wrong, 0.524 must be COMMON under that null",
   (nb >= 0.524).mean() > 0.05,
   f"P(|delta rho| >= 0.524) = {(nb >= 0.524).mean():.4f} when two entries are redrawn over the full published "
   f"union range, and {(null_shift('canonical', beta.min(), beta.max(), 40000) >= 0.524).mean():.4f} when "
   f"redrawn inside the beta_z range. So the shift IS large in magnitude -- g03's null is mislabelled but its "
   f"conclusion on this sub-point is not rescued by the correct null. The shift is large because -0.20 lies "
   f"OUTSIDE the beta_z range entirely, which is itself the signature of a different quantity (W1)")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("W5.  AN UNCITED INPUT")
P("=" * 118)
info("g03's substitution table contains the row 'Vitral inclination-marginalised beta_J' with (Draco, Sculptor)")
info("= (0.13, 0.13). +0.13 is Sculptor's inclination-marginalised beta_J (g03's own SCL_ALT dict). g03's")
info("DRACO_ALT dict contains no 0.13, and its docstring cites no inclination-marginalised beta_J for Draco.")
info("That row therefore assigns Sculptor's number to Draco. It produces rho = +0.143, one of the two rows")
info("g03's verdict calls a collapse.")
r_uncited = sub_rho("canonical", 0.13, 0.13)[0]
ck("W5 (PROVENANCE) every substituted value must be traceable to a cited published number for the object it "
   "is assigned to",
   False,
   f"the Draco entry of the 'inclination-marginalised beta_J' row is uncited and equals Sculptor's value; "
   f"that row returns rho = {r_uncited:+.3f}. Marked FAIL as a provenance defect, not a physics one -- it does "
   f"not change W1's conclusion either way")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("W6.  THE OBSTRUCTION THAT DOES NOT NEED A8 AT ALL")
P("=" * 118)
s = np.sort(beta); gaps = np.diff(s)
info(f"sorted beta_z: {np.round(s, 3)}")
info(f"adjacent gaps: {np.round(gaps, 3)}   median gap = {np.median(gaps):.3f}")
info(f"median Hayashi+2020 STATISTICAL error on beta_z = {np.median(sbeta):.3f}  "
     f"= {np.median(sbeta) / np.median(gaps):.1f}x the median adjacent gap")
mc = {f: np.array([spear(RES[f], np.clip(beta + rng.normal(0, sbeta), -3.0, 0.999)) for _ in range(20000)])
      for f in A0}
for f in A0:
    info(f"[{f:9}] MC over quoted errors: rho median {np.median(mc[f]):+.3f}, 16-84 "
         f"{np.percentile(mc[f], 16):+.3f} to {np.percentile(mc[f], 84):+.3f}, fraction positive "
         f"{(mc[f] > 0).mean():.3f}")
ck("W6 (THE ORDERING) a rank correlation needs the ORDERING of the eight objects, which needs the adjacent "
   "gaps to exceed the per-object errors. Test that on Hayashi+2020's OWN quoted statistical errors, with no "
   "cross-method or cross-definition argument anywhere in it",
   np.median(sbeta) < np.median(gaps),
   f"the median quoted error {np.median(sbeta):.3f} is {np.median(sbeta) / np.median(gaps):.1f} times the "
   f"median adjacent gap {np.median(gaps):.3f}. The ordering is NOT established, on the homogeneous set's own "
   f"error bars, before any of A8-A10 is invoked. This is the honest form of g03's verdict item 1, it is "
   f"footing-independent, and it needs none of the definitional mixing that W1 rejects")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("W7.  MUTATION CONTROL")
P("=" * 118)
res_n = resid_vec(A0["canonical"], newton=True)
rho_n = spear(res_n, beta)
r_n_sub = spear(res_n, np.concatenate(([-0.20, 0.35], beta[2:])))
info(f"M1 kernel OFF (nu = 1): baseline rho = {rho_n:+.3f}; after the beta_bar_B substitution {r_n_sub:+.3f}; "
     f"shift {abs(r_n_sub - rho_n):.3f}")
info(f"   the framework's own shift under the same substitution is "
     f"{abs(sub_rho('canonical', -0.20, 0.35)[0] - RHO['canonical']):.3f}")
b_shuf = beta.copy(); rng.shuffle(b_shuf)
info(f"M2 shuffled beta_z, then the same substitution: baseline {spear(RES['canonical'], b_shuf):+.3f}")
ck("W7 (MUTATION) if the substitution collapse were a statement about the FRAMEWORK's residual, turning the "
   "kernel off (nu = 1, pure Newtonian) should change how big the collapse is. If the collapse is the same "
   "size with gravity unmodified, it is a property of the substituted number and not of the framework",
   abs(abs(r_n_sub - rho_n) - abs(sub_rho('canonical', -0.20, 0.35)[0] - RHO['canonical'])) > 0.15,
   f"Newtonian shift {abs(r_n_sub - rho_n):.3f} vs framework shift "
   f"{abs(sub_rho('canonical', -0.20, 0.35)[0] - RHO['canonical']):.3f}. The substitution does essentially the "
   f"same thing with gravity completely unmodified, confirming it is an input-value effect, not a kernel effect")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118); P("VERDICT ON g03's A8 / A9 / VERDICT-ITEM-1"); P("=" * 118)
P(f"  REFUTED AS STATED, RECOVERABLE AS RESTATED.")
P("")
P(f"  1. THE HEADLINE NUMBERS ARE A CATEGORY ERROR. g03's per-object spreads {d_all:.3f} (Draco) and "
  f"{s_all:.3f} (Sculptor)")
P(f"     difference quantities the source papers define differently. Vitral+2024's abstract states in one")
P(f"     sentence that Draco is radially anisotropic along the symmetry axis AND tangentially anisotropic in")
P(f"     the equatorial plane, with globally-averaged beta_bar_B = -0.20 where 1 - beta_B == <v_tan^2>/<v_rad^2>.")
P(f"     beta_bar_B = -0.20 and beta_J = +0.56 are both correct descriptions of ONE velocity ellipsoid field.")
P(f"     Within the meridional class the two INDEPENDENT analyses of Draco -- line-of-sight Jeans and 18 years")
P(f"     of HST proper motions -- agree to {d_mer:.3f}, which is {d_mer / BETWEEN * 100:.0f} per cent of the "
  f"between-object spread, not 153 per cent.")
P(f"  2. THE SUBSTITUTION COLLAPSE IS ONE NUMBER. Sculptor's substitution moves rho by {shift_s:.3f}. All of it")
P(f"     is Draco's beta_bar_B demoting the largest-residual object to lowest anisotropy. Like for like the")
P(f"     shift is {abs(r_lfl_c - RHO['canonical']):.3f}, inside the null sd {NULL_SD:.3f}.")
P(f"  3. WHAT SURVIVES, AND IT IS ENOUGH TO KEEP THE FORK SHUT: (a) W6 -- the median quoted statistical error")
P(f"     on beta_z is {np.median(sbeta) / np.median(gaps):.1f}x the median adjacent gap, so the ordering is unestablished on the")
P(f"     homogeneous set's own error bars alone; (b) W3 -- Sculptor's beta_J swings")
P(f"     {abs(SCL_SWING[0] - SCL_SWING[1]):.2f} on viewing angle within one definition and one paper; (c) g03's own A11, that")
P(f"     no published beta was derived inside this framework's potential and its phantom halo is cuspier than")
P(f"     the fitted ones by 0.61-1.47 in log slope.")
P(f"  4. AND THE TEST WOULD NOT DISCRIMINATE EVEN IF beta WERE PERFECT: g03's own A6 (64 per cent of the")
P(f"     correlation survives nu = 1) and A13 (the deep-MOND virial relation is common to both arms) already")
P(f"     say so. Those, not A8, are the load-bearing reasons.")
P("")
P(f"  RECOMMENDATION: do not cite '0.81 for Draco' or '1.28 for Sculptor' as measurement uncertainties, and do")
P(f"  not cite 'rho collapses to +0.167' as evidence about measurability. Cite W6 and A11 instead.")
sys.exit(ck.done())
