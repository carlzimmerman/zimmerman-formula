#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g03v_anisotropy_confound_verification.py -- ADVERSARIAL VERIFICATION OF g03's ANISOTROPY CORRELATION
====================================================================================================
THE CLAIM UNDER TEST (g03_anisotropy_correlation_test.py): within the eight classical dwarf spheroidals the
framework's residual correlates positively with published velocity anisotropy (Spearman rho = +0.667,
permutation p = 0.082, 1.74 sigma, both footings) "in the sense a trajectory-dependent (modified-inertia)
modification would suggest".

THIS FILE DOES NOT DISPUTE THE NUMBER.  It reproduces rho = +0.667 independently and computes the EXACT
permutation p over all 8! = 40320 orderings.  What it disputes is the INFERENCE, on four grounds, each a
numbered check that can fail:

  V1  The residual carries almost no rank information beyond stellar mass:  Spearman(resid, -log M*) = +0.95.
  V2  THE MUTATION g03 DID NOT RUN.  Freeze every velocity dispersion to the sample mean -- delete every scrap
      of KINEMATIC information from the residual, leaving only M*, R_half and Galactocentric distance -- and the
      correlation with beta does not weaken.  Freeze the stellar masses instead, keeping the kinematics, and it
      collapses.  A trajectory-dependent modification cannot live in a residual whose trajectories have been
      deleted without loss.
  V3  g03's confound check A5 is computed in the WRONG CURRENCY.  Its headline statistic is Spearman; its
      partial() is a PEARSON partial on the raw variables.  Redone on ranks, to match the headline statistic,
      partial(resid, beta | log M*) falls from +0.717 to +0.17 with exact p = 0.70.  g03's verdict sentence
      "Controlling for stellar mass does NOT weaken it" is an artefact of that mismatch.
  V4  ALGEBRA.  On the isolated branch (6 of the 8 objects) R_half cancels identically and the residual is
      exactly  2 log(sigma) - 0.5 log(M*) + const  -- the deep-MOND Faber-Jackson residual.  The 0.5 log(M*)
      term spans 1.09 dex against 0.50 dex for 2 log(sigma), so the residual is dominated better than 2:1 by
      stellar mass BY CONSTRUCTION.  The two objects on the other branch (Fornax, Leo I) are exactly the two
      most massive, so the prescription branch is itself a stellar-mass indicator.

WHY THIS REFUTES IT AS A DISCRIMINANT.  In rank terms the claim reduces to "Hayashi+2020's beta_z anticorrelates
with dwarf stellar mass" (Kendall tau = +0.54).  That is a statement about the tracer population and about the
modelling, not about gravity.  Hayashi, Chiba & Ishiyama 2020 (ApJ 904, 45) fit beta_z jointly with the halo axis
ratio Q and the inclination and report the Q-beta_z degeneracy themselves (their Sec. IV.1); fainter dwarfs have
fewer member velocities, so their beta_z drifts toward whatever that degeneracy favours.  Ordinary cold dark
matter reproduces a mass-anisotropy trend among the classical dwarfs with no new physics at all.

Data and residual definition are taken VERBATIM from g03/f09 so the comparison is like for like.
Both a_0 footings throughout.  Checks are written so they CAN fail; V5 is the mutation control.
"""
import sys, math, itertools, os, csv
import numpy as np
from hunt_lib import *

ck = Check()
MW_VC = 200e3

# ---- inputs, verbatim from f09_orbital_coherence_fork.py / g03_anisotropy_correlation_test.py -------------
DSPH = [("Draco", 2.9e5, 0.221, 9.1, 76.), ("Sculptor", 2.3e6, 0.283, 9.2, 86.),
        ("Fornax", 4.3e7, 0.710, 11.7, 147.), ("Carina", 3.8e5, 0.250, 6.6, 105.),
        ("Sextans", 4.4e5, 0.695, 7.9, 86.), ("Leo I", 5.5e6, 0.251, 9.2, 254.),
        ("Leo II", 7.4e5, 0.176, 6.6, 233.), ("Ursa Minor", 2.9e5, 0.181, 9.5, 76.)]
# Hayashi, Chiba & Ishiyama 2020, ApJ 904, 45 (arXiv:2007.13780) Table 2, column -log10(1-beta_z).
BZ = {"Draco": 0.41, "Ursa Minor": 0.61, "Carina": 0.36, "Sextans": 0.18,
      "Leo I": 0.11, "Leo II": 0.12, "Sculptor": 0.21, "Fornax": 0.24}
names = [d[0] for d in DSPH]
beta = np.array([1.0 - 10.0 ** (-BZ[n]) for n in names])
logM = np.log10(np.array([d[1] for d in DSPH]))
sig = np.array([d[3] for d in DSPH])

def resid(M, Rh, s, D, a0):
    Mk, R, sv, d = M * Msun, Rh * kpc, s * 1e3, D * kpc
    gN = G * Mk / R ** 2
    gi = math.sqrt(gN * a0); ge = gN * nu_s((MW_VC ** 2 / d) / a0)
    return math.log10(3.0 * sv * sv / R / max(gi, ge)), ("isolated" if gi >= ge else "EFE")

def resids(tab, a0): return np.array([resid(*t[1:], a0)[0] for t in tab])

RES = {f: resids(DSPH, A0[f]) for f in A0}
BRANCH = [resid(*d[1:], A0["canonical"])[1] for d in DSPH]

# ---- statistics, written out ------------------------------------------------------------------------------
def pear(a, b):
    a = np.asarray(a, float) - np.mean(a); b = np.asarray(b, float) - np.mean(b)
    dn = math.sqrt((a @ a) * (b @ b))
    return float(a @ b / dn) if dn > 0 else 0.0
def rk(x): return np.argsort(np.argsort(np.asarray(x, float))).astype(float)
def sp(a, b): return pear(rk(a), rk(b))
def part(x, y, z):
    rxy, rxz, ryz = pear(x, y), pear(x, z), pear(y, z)
    return (rxy - rxz * ryz) / math.sqrt(max((1 - rxz ** 2) * (1 - ryz ** 2), 1e-15))
def exact_p(stat, y):
    """EXACT two-sided permutation p over all 8! = 40320 relabelings -- no Monte Carlo error."""
    obs = stat(y); hits = sum(1 for p in itertools.permutations(range(len(y)))
                              if abs(stat(y[list(p)])) >= abs(obs) - 1e-12)
    return obs, hits / math.factorial(len(y))
def p_to_sigma(p):
    p = min(max(p, 1e-12), 1.0); lo, hi = 0.0, 12.0
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if math.erfc(m / math.sqrt(2.0)) > p: lo = m
        else: hi = m
    return 0.5 * (lo + hi)
NULL_SD = 1.0 / math.sqrt(len(names) - 1)

P("=" * 118); P("A.  REPRODUCTION: the number itself is not in dispute"); P("=" * 118)
rho_can, p_can = exact_p(lambda b: sp(RES["canonical"], b), beta)
rho_alt, p_alt = exact_p(lambda b: sp(RES["alt"], b), beta)
info(f"canonical a0 = {A0['canonical']:.3g}: Spearman rho = {rho_can:+.4f}, Pearson r = {pear(RES['canonical'], beta):+.4f}, "
     f"EXACT permutation p = {p_can:.4f} ({p_to_sigma(p_can):.2f} sigma)")
info(f"alt       a0 = {A0['alt']:.3g}: Spearman rho = {rho_alt:+.4f}, Pearson r = {pear(RES['alt'], beta):+.4f}, "
     f"EXACT permutation p = {p_alt:.4f} ({p_to_sigma(p_alt):.2f} sigma)")
ck("V0 (REPRODUCTION) g03's headline rho = +0.667 at p = 0.082 must reproduce independently, on both footings, "
   "with the p-value computed EXACTLY over all 40320 orderings rather than by Monte Carlo",
   abs(rho_can - 0.667) < 0.005 and abs(rho_alt - 0.667) < 0.005 and abs(p_can - 0.082) < 0.005,
   f"rho = {rho_can:+.4f} / {rho_alt:+.4f}, exact p = {p_can:.4f} / {p_alt:.4f} against g03's 50000-permutation "
   f"0.0820 / 0.0822. The arithmetic is correct. Everything below is about the INFERENCE, not the number")

P(""); P("=" * 118); P("B.  WHAT THE RESIDUAL ACTUALLY IS"); P("=" * 118)
info(f"{'system':13} {'branch':>9} {'log M*':>7} {'sigma':>6} {'resid':>8} "
     f"{'rank(resid)':>12} {'rank(-logM*)':>13} {'rank(beta)':>11}")
for i, n in enumerate(names):
    info(f"{n:13} {BRANCH[i]:>9} {logM[i]:7.2f} {sig[i]:6.1f} {RES['canonical'][i]:+8.3f} "
         f"{rk(RES['canonical'])[i]:12.0f} {rk(-logM)[i]:13.0f} {rk(beta)[i]:11.0f}")
P("")
info(f"Spearman(resid, -log M*)  = {sp(RES['canonical'], -logM):+.4f}   <-- the residual is a stellar-mass rank order")
info(f"Spearman(-log M*, beta)   = {sp(-logM, beta):+.4f}   <-- and THIS is the claimed correlation, without gravity")
info(f"Spearman(resid, beta)     = {sp(RES['canonical'], beta):+.4f}")
tau = sum(np.sign((-logM[i] + logM[j]) * (beta[i] - beta[j])) for i, j in itertools.combinations(range(8), 2)) / 28
info(f"Kendall tau(-log M*, beta) = {tau:+.3f}  -- the whole test, restated: Hayashi's beta_z anticorrelates with M*")
ck("V1 (THE RESIDUAL IS A MASS ORDERING) for the correlation to be about orbits, the residual must carry rank "
   "information that stellar mass does not already carry. Spearman(resid, -log M*) must be below 0.9",
   abs(sp(RES["canonical"], -logM)) < 0.90,
   f"Spearman(resid, -log M*) = {sp(RES['canonical'], -logM):+.4f}: seven of the eight objects are in the same "
   f"rank position in the residual as in inverse stellar mass. And Spearman(-log M*, beta) = {sp(-logM, beta):+.4f} "
   f"is LARGER than the claimed {rho_can:+.4f}, so stellar mass alone outperforms the framework's residual")

# ---- the algebra ------------------------------------------------------------------------------------------
P(""); P("=" * 118); P("C.  THE ALGEBRA: R_half cancels, and the residual is 2 log(sigma) - 0.5 log(M*)"); P("=" * 118)
free = np.array([math.log10(3 * (d[3] * 1e3) ** 2 / math.sqrt(G * d[1] * Msun * A0["canonical"])) for d in DSPH])
iso = np.array([b == "isolated" for b in BRANCH])
info("isolated branch: g_pred = sqrt(G M a0)/R and g_obs = 3 sigma^2/R, so R_half cancels IDENTICALLY:")
for i, n in enumerate(names):
    tag = "EXACT" if abs(RES["canonical"][i] - free[i]) < 1e-9 else "(EFE branch, differs)"
    info(f"    {n:13} resid = {RES['canonical'][i]:+.4f}   log10(3 sigma^2/sqrt(G M a0)) = {free[i]:+.4f}   {tag}")
info(f"spread of 2*log10(sigma) = {2 * np.ptp(np.log10(sig)):.3f} dex; of 0.5*log10(M*) = {0.5 * np.ptp(logM):.3f} dex "
     f"-- ratio {0.5 * np.ptp(logM) / (2 * np.ptp(np.log10(sig))):.2f}")
info(f"the two EFE-branch objects are {[names[i] for i in range(8) if not iso[i]]}, which are the two most massive, "
     f"so the branch choice is itself a stellar-mass indicator")
ck("V2 (VARIANCE BUDGET) for the residual to be a dynamical statistic, the kinematic term 2 log(sigma) must "
   "contribute at least as much spread as the photometric term 0.5 log(M*)",
   2 * np.ptp(np.log10(sig)) >= 0.5 * np.ptp(logM),
   f"2*log10(sigma) spans {2 * np.ptp(np.log10(sig)):.3f} dex, 0.5*log10(M*) spans {0.5 * np.ptp(logM):.3f} dex. On the "
   f"six isolated-branch objects the residual is EXACTLY the deep-MOND Faber-Jackson residual and is dominated "
   f"{0.5 * np.ptp(logM) / (2 * np.ptp(np.log10(sig))):.1f}:1 by stellar mass by construction")

# ---- THE MUTATION CONTROL g03 DID NOT RUN -----------------------------------------------------------------
P(""); P("=" * 118); P("D.  MUTATION CONTROLS: which input carries the correlation?"); P("=" * 118)
FROZ_S = [(names[i], DSPH[i][1], DSPH[i][2], float(sig.mean()), DSPH[i][4]) for i in range(8)]
FROZ_M = [(names[i], 10 ** logM.mean(), DSPH[i][2], DSPH[i][3], DSPH[i][4]) for i in range(8)]
out = {}
for lab, tab in [("dispersions frozen to the sample mean (NO kinematics)", FROZ_S),
                 ("stellar masses frozen to the sample mean (kinematics kept)", FROZ_M)]:
    for f in A0:
        out[(lab, f)] = sp(resids(tab, A0[f]), beta)
    info(f"M-{lab:60} rho = {out[(lab, 'canonical')]:+.4f} (canonical), {out[(lab, 'alt')]:+.4f} (alt)")
info(f"M-baseline, nothing frozen                                       rho = {rho_can:+.4f} (canonical), {rho_alt:+.4f} (alt)")
rho_nokin = out[("dispersions frozen to the sample mean (NO kinematics)", "canonical")]
rho_nomass = out[("stellar masses frozen to the sample mean (kinematics kept)", "canonical")]
ck("V3 (THE MUTATION THAT DECIDES IT) a trajectory-dependent modification expresses itself through the KINEMATICS. "
   "So deleting the kinematics -- setting every velocity dispersion to the sample mean and leaving only M*, "
   "R_half and Galactocentric distance -- must DESTROY the correlation with anisotropy",
   abs(rho_nokin) < 0.5 * abs(rho_can),
   f"with every dispersion frozen the correlation is rho = {rho_nokin:+.4f}, i.e. LARGER than the baseline "
   f"{rho_can:+.4f}. Freezing the stellar masses instead and keeping the kinematics collapses it to "
   f"{rho_nomass:+.4f}. The correlation lives entirely in the stellar masses; the dynamics can be removed "
   f"without loss. Whatever this measures, it is not a property of the orbits")

# ---- the currency error in g03's own confound check -------------------------------------------------------
P(""); P("=" * 118); P("E.  g03's CONFOUND CHECK A5 IS COMPUTED IN THE WRONG CURRENCY"); P("=" * 118)
pp_can, pp_alt = part(RES["canonical"], beta, logM), part(RES["alt"], beta, logM)
sp_can, sp_alt = part(rk(RES["canonical"]), rk(beta), rk(logM)), part(rk(RES["alt"]), rk(beta), rk(logM))
_, p_sp = exact_p(lambda b: part(rk(RES["canonical"]), rk(b), rk(logM)), beta)
_, p_pp = exact_p(lambda b: part(RES["canonical"], b, logM), beta)
info(f"PEARSON partial(resid, beta | log M*) -- what g03 reports as A5: {pp_can:+.4f} (canonical), {pp_alt:+.4f} (alt), "
     f"exact p = {p_pp:.4f}")
info(f"SPEARMAN partial, same variables on ranks -- matching the headline statistic: {sp_can:+.4f} (canonical), "
     f"{sp_alt:+.4f} (alt), exact p = {p_sp:.4f} ({p_to_sigma(p_sp):.2f} sigma)")
info("g03's headline statistic is Spearman rho and its own stated weakest link is that 'the rank ordering is what")
info("the statistic uses'. Its partial() is nevertheless a Pearson partial on the raw variables. The two disagree")
info("by more than the null sd, so the sign of A5's verdict is a choice of statistic, at N = 8.")
ck("V4 (CURRENCY) the confound check must be computed in the same currency as the headline statistic. A Spearman "
   "headline requires a Spearman partial. The two must agree to within the null sd",
   abs(pp_can - sp_can) < NULL_SD,
   f"Pearson partial {pp_can:+.4f} against Spearman partial {sp_can:+.4f}, a difference of {abs(pp_can - sp_can):.3f} "
   f"against a null sd of {NULL_SD:.3f}. In the claim's OWN currency, controlling for stellar mass takes the "
   f"correlation to {sp_can:+.4f} at exact p = {p_sp:.3f} = {p_to_sigma(p_sp):.2f} sigma -- consistent with zero. "
   f"g03's verdict line 'Controlling for stellar mass does NOT weaken it (+0.717)' does not survive this")

# ---- independent structural compilation, same two tests ---------------------------------------------------
LVD = os.path.join(DATA, "dsph", "lvd_dwarf_mw.csv")
lvd = {r["name"]: r for r in csv.DictReader(open(LVD))}
DL = [(n, 10 ** float(lvd[n]["mass_stellar"]), float(lvd[n]["rhalf_sph_physical"]) / 1000.0,
       float(lvd[n]["vlos_sigma"]), float(lvd[n]["distance_gc"])) for n in names]
rl = resids(DL, A0["canonical"]); lM = np.array([math.log10(d[1]) for d in DL])
info("")
info(f"Local Volume Database compilation, same three statistics: Spearman(resid, beta) = {sp(rl, beta):+.4f}, "
     f"Spearman(resid, -log M*) = {sp(rl, -lM):+.4f}, Spearman partial | log M* = "
     f"{part(rk(rl), rk(beta), rk(lM)):+.4f}")
FS_L = [(names[i], DL[i][1], DL[i][2], float(np.array([d[3] for d in DL]).mean()), DL[i][4]) for i in range(8)]
FM_L = [(names[i], 10 ** lM.mean(), DL[i][2], DL[i][3], DL[i][4]) for i in range(8)]
info("")
info("AGAINST INTEREST -- the same two mutations on the Local Volume Database compilation are NOT as clean:")
info(f"    baseline {sp(rl, beta):+.4f};  dispersions frozen {sp(resids(FS_L, A0['canonical']), beta):+.4f};  "
     f"stellar masses frozen {sp(resids(FM_L, A0['canonical']), beta):+.4f}")
info("    On that compilation the kinematics carry about as much as the masses, so the 'photometry carries all of")
info("    it' statement is specific to f09's hand-entered table. What is compilation-INDEPENDENT is the near-")
info("    degeneracy of the residual with stellar mass and the fact that the rank partial is consistent with zero.")

ck("V5 (INDEPENDENT COMPILATION) the same diagnosis must hold on the Local Volume Database numbers, otherwise it "
   "is an artefact of f09's hand-entered table. The rank-partial on that compilation must also be consistent "
   "with zero for the diagnosis to stand",
   abs(part(rk(rl), rk(beta), rk(lM))) < 2 * NULL_SD, 
   f"Local Volume Database: raw rho = {sp(rl, beta):+.4f}, resid-vs-mass rank correlation {sp(rl, -lM):+.4f}, "
   f"Spearman partial controlling stellar mass = {part(rk(rl), rk(beta), rk(lM)):+.4f}. Same diagnosis, "
   f"independent structural data. NOTE this check PASSING is a point AGAINST the claim, not for it")

P(""); P("=" * 118); P("VERDICT"); P("=" * 118)
P(f"  THE NUMBER REPRODUCES AND THE INFERENCE DOES NOT. rho = {rho_can:+.3f}, exact p = {p_can:.4f}, {p_to_sigma(p_can):.2f} sigma,")
P(f"  identical on both footings. But in rank terms the residual IS the stellar-mass ordering")
P(f"  (Spearman = {sp(RES['canonical'], -logM):+.3f}), and stellar mass alone correlates with Hayashi's beta_z at")
P(f"  {sp(-logM, beta):+.3f} -- BETTER than the framework's residual does. Deleting every velocity dispersion from the")
P(f"  residual leaves the correlation at {rho_nokin:+.3f}; deleting the stellar masses instead collapses it to {rho_nomass:+.3f}.")
P("  The correlation is carried by the photometry, not the dynamics, so it cannot be a fingerprint of a")
P("  modification that attaches to trajectories.")
P("")
P(f"  AND g03's OWN CONFOUND CHECK REVERSES. A5 reports a Pearson partial (+{pp_can:.3f}) while the headline is Spearman;")
P(f"  the matching Spearman partial is {sp_can:+.3f} at exact p = {p_sp:.2f}. 'Controlling for stellar mass does NOT")
P("  weaken it' is a currency mismatch, and the verdict line built on it should be withdrawn.")
P("")
P("  ORDINARY COLD DARK MATTER PRODUCES THIS SIGNATURE. A mass-anisotropy trend among the classical dwarfs is a")
P("  statement about the tracers and the modelling. Hayashi+2020 fit beta_z jointly with the halo axis ratio Q and")
P("  the inclination and report the Q-beta_z degeneracy themselves; fainter dwarfs have fewer member velocities and")
P("  their beta_z drifts toward whatever that degeneracy favours. No gravity theory is being discriminated.")
P("")
P("  WHAT SURVIVES: nothing that g03 did not already concede. Its A6 (Newtonian mutation keeps 64 per cent), A7")
P("  (below the shuffle's own 95th percentile), A8-A11 (the input variable is not measured) and A13 (the arms")
P("  agree on this observable) all stand and are correct. This file adds that the ONE thing g03 counted in the")
P("  claim's favour -- that mass does not explain it -- is the opposite of true.")
sys.exit(ck.done())
