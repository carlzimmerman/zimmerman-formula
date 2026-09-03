#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g03v_adversarial_efe_branch_refutation.py -- ADVERSARIAL VERIFICATION OF g03_anisotropy_correlation_test.py
===========================================================================================================
THE CLAIM UNDER TEST (as handed to the verifier):
  "Within the eight classical dwarf spheroidals, the framework's residual correlates positively with published
   velocity anisotropy, in the sense a trajectory-dependent (modified-inertia) modification would suggest."
  Numbers: Spearman rho = +0.667, permutation p = 0.0820 (canonical), +0.667 / 0.0822 (alt); 1.74 sigma.
  Support cited: an independent structural compilation (Local Volume Database) giving rho = +0.548.

WHAT THIS FILE DOES.  It reproduces g03's number independently, then attacks the PHYSICS of the residual, not
the statistics.  Three lines of attack, each a numbered check that can fail:

  V1-V3  THE EXTERNAL-FIELD BRANCH.  g03 sets g_pred = max(g_iso, g_efe) with g_iso = sqrt(g_N a0) the ISOLATED
         deep-MOND asymptote and g_efe = g_N nu(g_ext/a0) the quasi-Newtonian external-field value, describing
         the max() as "the choice that favours the framework".  max() is not a physical criterion: it selects
         whichever formula returns the larger number.  The physical criterion is whether the external field
         dominates the internal one.  For Milky Way classical dwarf spheroidals the external field is NOT
         optional, and this file shows the headline correlation is created by omitting it.

  V4-V5  THE OBSERVABLE.  The residual is a global 3 sigma^2 / R_half virial quantity.  Milgrom's deep-MOND
         virial relation has the SAME form in modified-inertia and in AQUAL/QUMOND (Milgrom 1994, Ann. Phys.
         229, 384; Milgrom 1997, Phys. Rev. E 56, 1148; Milgrom 2012, MNRAS 426, 673 for the modified-gravity
         side), irrespective of the internal mass distribution.  g03's own check A13 says exactly this and marks
         it FAIL.  So the arms agree at leading order on this observable and modified inertia -- a class, not a
         theory -- predicts neither the sign nor the size of any residual anisotropy dependence.  The claim's
         clause "in the sense a modified-inertia modification would suggest" therefore has no content: a
         NEGATIVE rho would have been equally compatible, which is why g03 correctly ran a TWO-SIDED test.

  V6     THE VARIABLE IS NOT AN ORBIT-SHAPE VARIABLE.  Verified against the source: Hayashi, Chiba & Ishiyama
         2020 (ApJ 904, 45; arXiv:2007.13780) define beta_z = 1 - <u_z^2>/<u_R^2> in CYLINDRICAL (R, z)
         coordinates, and state "there are obvious degeneracies between b_halo-rho_0 and Q-beta_z" (Q = halo
         axis ratio).  beta_z measures the flattening of the velocity ellipsoid in the meridional plane and is
         degenerate with a halo SHAPE parameter.  The trajectory-shape quantity a modified-inertia argument
         keys on is the spherical radial anisotropy beta_r = 1 - sigma_t^2/sigma_r^2 (circular vs eccentric
         orbits).  There is no monotone map from beta_z to orbit eccentricity: tangential orbits confined near
         a plane raise beta_z exactly as in-plane radial orbits do.  This also means g03's substitution test A9
         is not like-for-like -- Vitral+2024's beta_B is a SPHERICAL radial anisotropy, a different quantity
         from the beta_z baseline it replaces.

  V7     THE CITED CORROBORATION IS NOT INDEPENDENT.  g03's own A4 reports the two residual vectors correlate
         at r = +0.955.  The Local Volume Database rerun is the same eight objects with slightly different
         structural inputs, not an independent measurement, and its rho = +0.548 is 1.37 sigma, not 1.74.

DATA.  Structural table and anisotropies taken verbatim from g03 so the currency is identical.  Hayashi+2020
Table 2 values re-verified against the published paper this session; all eight match to the quoted digit,
including the asymmetric 68 per cent intervals.  Both a0 footings throughout.

NOT RUN, AND WHY.  No attempt is made here to decide whether the framework fits or misses these dwarfs.  The
self-consistent external-field prescription used below makes the framework's dwarf-spheroidal residuals much
LARGER (up to +1.28 dex), but that is a separate question from the one under test and is not adjudicated here;
this file's only claim is about what the CORRELATION does.  Verifying a deficit as hard as a win: the sweep in
section C runs SIX prescriptions, and reports every one, including the three that keep rho at +0.667.
"""
import sys, math, itertools, os, csv
import numpy as np
from hunt_lib import *

ck = Check()
MW_VC = 200e3

# ---------------------------------------------------------------------------------------------------------
# Sample -- verbatim from g03_anisotropy_correlation_test.py
# ---------------------------------------------------------------------------------------------------------
DSPH = [("Draco",      2.9e5, 0.221, 9.1,  76.), ("Sculptor",   2.3e6, 0.283, 9.2,  86.),
        ("Fornax",     4.3e7, 0.710, 11.7, 147.), ("Carina",     3.8e5, 0.250, 6.6,  105.),
        ("Sextans",    4.4e5, 0.695, 7.9,  86.),  ("Leo I",      5.5e6, 0.251, 9.2,  254.),
        ("Leo II",     7.4e5, 0.176, 6.6,  233.), ("Ursa Minor", 2.9e5, 0.181, 9.5,  76.)]
# Hayashi, Chiba & Ishiyama 2020, ApJ 904, 45 (arXiv:2007.13780) Table 2, column -log10(1 - beta_z).
# RE-VERIFIED against the published paper this session: all eight values and both error bars reproduce.
# Their definition, quoted: beta_z = 1 - <u_z^2>/<u_R^2>, CYLINDRICAL (R, z).  Their stated degeneracy,
# quoted: "there are obvious degeneracies between b_halo-rho_0 and Q-beta_z".
BZ = {"Draco": 0.41, "Ursa Minor": 0.61, "Carina": 0.36, "Sextans": 0.18,
      "Leo I": 0.11, "Leo II": 0.12, "Sculptor": 0.21, "Fornax": 0.24}

names = [d[0] for d in DSPH]
beta = np.array([1.0 - 10.0 ** (-BZ[n]) for n in names])
logM = np.log10(np.array([d[1] for d in DSPH]))

def pear(a, b):
    a = np.asarray(a, float) - np.mean(a); b = np.asarray(b, float) - np.mean(b)
    return float(a @ b / math.sqrt((a @ a) * (b @ b)))
def rankv(x): return np.argsort(np.argsort(np.asarray(x, float))).astype(float)
def spear(a, b): return pear(rankv(a), rankv(b))
def partial(x, y, z):
    rxy, rxz, ryz = pear(x, y), pear(x, z), pear(y, z)
    return (rxy - rxz * ryz) / math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))

# EXACT permutation null at N=8 (8! = 40320 orderings) -- no Monte Carlo error at all
_r = np.arange(8.0); _rc = _r - _r.mean(); _den = _rc @ _rc
NULL = np.array([float(_rc @ (np.array(p, float) - 3.5) / _den) for p in itertools.permutations(range(8))])
def exact_p(rho): return float((np.abs(NULL) >= abs(rho) - 1e-9).mean())
def p_to_sigma(p):
    p = min(max(p, 1e-12), 1.0); lo, hi = 0.0, 12.0
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if math.erfc(m / math.sqrt(2.0)) > p: lo = m
        else: hi = m
    return 0.5 * (lo + hi)
NULL_SD = 1.0 / math.sqrt(len(names) - 1)

# ---------------------------------------------------------------------------------------------------------
# (A) THE FIELD-STRENGTH AUDIT -- is the isolated deep-MOND branch legitimate for these satellites?
# ---------------------------------------------------------------------------------------------------------
P("=" * 118)
P("A.  IS THE ISOLATED BRANCH LEGITIMATE?  external field vs internal field, satellite by satellite")
P("=" * 118)
info("MOND's external-field effect is not optional: the isolated deep-MOND relation g = sqrt(g_N a0) holds only")
info("where the system's OWN field dominates the field it is falling in.  The physical criterion is")
info("g_ext vs g_int, not 'whichever formula returns the larger number'.  Milky Way field taken as v_c^2/d with")
info("v_c = 200 km/s, exactly as g03 and f09 do.")
P("")
info(f"{'system':12}{'g_N/a0':>9}{'g_int/a0':>10}{'g_ext/a0':>10}{'g_ext/g_int':>12}   {'regime':>20}   {'g03 branch':>11}")
a0c = A0["canonical"]
n_ext_dom = 0
for nm, M, Rh, s, d in DSPH:
    gN = G * M * Msun / (Rh * kpc) ** 2
    gint = math.sqrt(gN * a0c)                       # isolated MOND internal field
    gext = MW_VC ** 2 / (d * kpc)
    gefe = gN * nu_s(gext / a0c)
    branch = "EFE" if gefe > gint else "isolated"
    reg = "EXTERNAL-dominated" if gext > gint else "internal-dominated"
    if gext > gint: n_ext_dom += 1
    info(f"{nm:12}{gN/a0c:9.4f}{gint/a0c:10.4f}{gext/a0c:10.4f}{gext/gint:12.2f}   {reg:>20}   {branch:>11}")

ck("V1 (THE BRANCH CRITERION IS NOT PHYSICAL) g03 assigns the external-field branch by max(g_iso, g_efe). If "
   "that rule tracked the physics, the objects it labels 'EFE' would be the externally dominated ones. It must "
   "agree with the physical criterion g_ext > g_int on all eight objects",
   False,
   "it agrees on NONE of the four externally dominated objects and is inverted on the two it does flag. Draco, "
   "Carina, Sextans and Ursa Minor sit in an external field 1.4 to 4.4 times their own internal MOND field and "
   "are given the ISOLATED branch; Fornax and Leo I, the two LEAST externally dominated objects "
   "(g_ext/g_int = 0.26 and 0.15), are the only two given the EFE branch. max() picks the larger number, and "
   "for high-g_N objects the quasi-Newtonian formula beats the deep-MOND asymptote for reasons that have "
   "nothing to do with the external field")

ck("V2 (HOW MANY OBJECTS ARE MISTREATED) at most one or two of the eight may be externally dominated for the "
   "isolated deep-MOND asymptote to be a defensible default across the sample",
   n_ext_dom <= 2,
   f"{n_ext_dom} of 8 are externally dominated (g_ext > g_int), and every one of them is put on the isolated "
   f"branch. Sextans is the extreme case at g_ext/g_int = 4.37")

# ---------------------------------------------------------------------------------------------------------
# (B) INDEPENDENT REPRODUCTION OF THE HEADLINE NUMBER
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("B.  INDEPENDENT REPRODUCTION of g03's headline number, with the EXACT permutation null (all 8! orderings)")
P("=" * 118)

def residuals(a0, mode, fM=1.0, vc=MW_VC):
    """mode selects the prediction for the internal dynamical acceleration.
       max        : g03's rule, max(isolated deep-MOND asymptote, quasi-Newtonian EFE)
       iso        : isolated deep-MOND asymptote for every object, no external field anywhere
       kernel     : the framework's OWN kernel isolated, nu(g_N/a0) g_N (not the asymptote)
       efe        : quasi-Newtonian external-field value for every object
       sum        : smooth, nu((g_N + g_ext)/a0) (g_N + g_ext) - nothing subtracted
       qumond     : self-consistent QUMOND: g_int = nu((gNi+gNe)/a0)(gNi+gNe) - nu(gNe/a0) gNe,
                    with the Newtonian external field recovered from the deep-MOND MW field, gNe = g_ext^2/a0
       newton     : MUTATION CONTROL, nu = 1, pure Newtonian mass discrepancy"""
    out = []
    for nm, M, Rh, s, d in DSPH:
        R = Rh * kpc
        gobs = 3.0 * (s * 1e3) ** 2 / R
        gNi = G * fM * M * Msun / R ** 2
        gext = vc ** 2 / (d * kpc)
        gNe = gext * gext / a0                      # deep-MOND inversion of the MW field
        giso, gefe = math.sqrt(gNi * a0), gNi * nu_s(gext / a0)
        gp = {"max": max(giso, gefe), "iso": giso, "kernel": nu_s(gNi / a0) * gNi, "efe": gefe,
              "sum": nu_s((gNi + gext) / a0) * (gNi + gext),
              "qumond": nu_s((gNi + gNe) / a0) * (gNi + gNe) - nu_s(gNe / a0) * gNe,
              "newton": gNi}[mode]
        out.append(math.log10(gobs / gp))
    return np.array(out)

rho_max = {f: spear(residuals(A0[f], "max"), beta) for f in A0}
for f in A0:
    r = residuals(A0[f], "max")
    p = exact_p(spear(r, beta))
    info(f"{f:10} a0 = {A0[f]:.3g}: Spearman rho = {spear(r, beta):+.4f}, Pearson = {pear(r, beta):+.4f}, "
         f"EXACT two-sided p = {p:.4f} ({p_to_sigma(p):.2f} sigma)")
info(f"g03 reported rho = +0.667 / p = 0.0820 (canonical) and +0.667 / 0.0822 (alt) from 50000 permutations.")
info(f"The exact null gives p = {exact_p(2/3):.4f}; g03's Monte Carlo p is correct to its own precision.")
info(f"Achievable rho values at N=8 near the observed one: {sorted(set(np.round(NULL[np.abs(NULL-2/3)<0.08],4)))}")

ck("V3 (ARITHMETIC REPRODUCTION) g03's headline rho and p must reproduce independently on both footings",
   abs(rho_max["canonical"] - 2/3) < 1e-6 and abs(rho_max["alt"] - 2/3) < 1e-6
   and abs(exact_p(2/3) - 0.0820) < 0.02,
   f"rho = {rho_max['canonical']:+.4f} (canonical) and {rho_max['alt']:+.4f} (alt), exact p = {exact_p(2/3):.4f} "
   f"= {p_to_sigma(exact_p(2/3)):.2f} sigma. The arithmetic in g03 is sound and the 1.74 sigma is honest. Note "
   f"the two footings return rho identical to 12 decimal places: a rank statistic is nearly a0-blind here by "
   f"construction, so 'confirmed on both footings' carries no independent information")

# ---------------------------------------------------------------------------------------------------------
# (C) THE ATTACK: sweep the prescription
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("C.  THE ATTACK: does the correlation survive treating the external field consistently?")
P("=" * 118)
MODES = [("max      (g03's rule)",           "max"),   ("iso      (no external field at all)", "iso"),
         ("kernel   (framework nu, isolated)", "kernel"), ("efe      (quasi-Newtonian, all)",  "efe"),
         ("sum      (smooth g_N + g_ext)",    "sum"),   ("qumond   (self-consistent EFE)",     "qumond"),
         ("newton   (MUTATION: nu = 1)",      "newton")]
sweep = {}
info(f"{'prescription':38}{'footing':11}{'rho':>8}{'exact p':>10}{'sigma':>7}{'Pearson':>9}{'partial|logM':>14}")
for lab, m in MODES:
    for f in A0:
        r = residuals(A0[f], m)
        rho = spear(r, beta); p = exact_p(rho)
        sweep[(m, f)] = rho
        info(f"{lab:38}{f:11}{rho:+8.3f}{p:10.4f}{p_to_sigma(p):7.2f}{pear(r, beta):+9.3f}"
             f"{partial(r, beta, logM):+14.3f}")
P("")
info("residuals under the two prescriptions, dex:")
info(f"  {'':12}" + "".join(f"{n[:9]:>10}" for n in names))
for lab, m in [("g03 max()", "max"), ("self-consistent", "qumond"), ("newton", "newton")]:
    info(f"  {lab:14}" + "".join(f"{v:+10.2f}" for v in residuals(a0c, m)))

rho_q = sweep[("qumond", "canonical")]
rho_n = sweep[("newton", "canonical")]
ck("V4 (THE REFUTATION) the correlation must not depend on a non-physical branch rule. Treating the external "
   "field consistently for every satellite -- by any of the three prescriptions that do so -- must leave the "
   "correlation materially above the script's own Newtonian mutation control",
   abs(rho_q - rho_n) > 0.1,
   f"self-consistent QUMOND external field gives rho = {rho_q:+.3f}, exact p = {exact_p(rho_q):.3f} = "
   f"{p_to_sigma(exact_p(rho_q)):.2f} sigma, landing EXACTLY on g03's own Newtonian mutation control "
   f"({rho_n:+.3f}), which g03's check A6 already marks FAIL. The pure quasi-Newtonian prescription gives the "
   f"same {sweep[('efe','canonical')]:+.3f} and the smooth (g_N+g_ext) one gives {sweep[('sum','canonical')]:+.3f}, "
   f"i.e. every external-field-consistent prescription lands AT OR BELOW the Newtonian control. "
   f"The headline +0.667 appears only in "
   f"the three prescriptions that apply the isolated deep-MOND form to externally dominated satellites. "
   f"Sextans' residual moves by {residuals(a0c,'qumond')[4]-residuals(a0c,'max')[4]:+.2f} dex, Draco's by "
   f"{residuals(a0c,'qumond')[0]-residuals(a0c,'max')[0]:+.2f} dex -- these are not rounding corrections")

ck("V5 (IS THE DIFFERENCE ITSELF SIGNIFICANT?) verifying the refutation as hard as the claim: the drop from "
   "+0.667 to +0.429 must itself be larger than the noise floor at N=8, or neither number means anything",
   abs(2/3 - rho_q) > NULL_SD,
   f"the drop is {abs(2/3 - rho_q):.3f} against a null sd of {NULL_SD:.3f} at N=8, i.e. {abs(2/3-rho_q)/NULL_SD:.2f} "
   f"sd. It is NOT resolvable. This cuts BOTH ways and is the honest reading: +0.667 and +0.429 are the same "
   f"number at this sample size, so the claim is not that the correlation is refuted to be zero -- it is that "
   f"NO prescription in the sweep produces a correlation distinguishable from the null, and the one that was "
   f"quoted is the most favourable member of a family whose spread exceeds its own signal")

# ---------------------------------------------------------------------------------------------------------
# (D) THE OBSERVABLE AND THE VARIABLE
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("D.  THE PHYSICS OF THE OBSERVABLE AND OF THE VARIABLE")
P("=" * 118)
GN = np.array([G * d[1] * Msun / (d[2] * kpc) ** 2 / a0c for d in DSPH])
info(f"all eight sit at g_N/a0 = {GN.min():.4f} to {GN.max():.4f}: deep-MOND, where Milgrom's virial relation")
info("has the SAME form in modified inertia and in AQUAL/QUMOND, irrespective of the mass distribution.")
info("g03's own check A13 states this and marks it FAIL. It is correct, and it is fatal to the claim's clause.")
ck("V6 (THE CLAIM'S INTERPRETIVE CLAUSE HAS NO CONTENT) for the phrase 'in the sense a trajectory-dependent "
   "modification would suggest' to be meaningful, modified inertia must predict the SIGN of this correlation. "
   "Modified inertia is a class with no unique prediction, and on a global deep-MOND virial observable the two "
   "arms are proven to agree at leading order",
   False,
   "no sign is predicted, which is why g03 correctly used a TWO-SIDED permutation test -- a two-sided test is "
   "the formal admission that rho = -0.667 would have been equally 'the sense modified inertia suggests'. The "
   "sign clause is post-hoc. g03's own docstring says 'MODIFIED INERTIA DOES NOT PREDICT THE SIGN', and its "
   "VERDICT block then says 'the sign is the one a trajectory-dependent modification would suggest'. Those two "
   "sentences are in the same file and cannot both stand; the claim as handed to the verifier inherits the "
   "second")

ck("V7 (WRONG ANISOTROPY) the correlating variable must be the orbit-shape quantity a trajectory-dependent "
   "modification keys on, namely the radial anisotropy beta_r = 1 - sigma_t^2/sigma_r^2 that distinguishes "
   "circular from eccentric orbits",
   False,
   "it is not. Hayashi+2020 define beta_z = 1 - <u_z^2>/<u_R^2> in CYLINDRICAL coordinates (verified against "
   "the paper), which measures the flattening of the velocity ellipsoid in the meridional plane, and they state "
   "'there are obvious degeneracies between b_halo-rho_0 and Q-beta_z' where Q is the halo AXIS RATIO. beta_z "
   "is entangled with a shape parameter of the system, and there is no monotone map from beta_z to orbital "
   "eccentricity: tangential orbits confined near a plane raise beta_z exactly as in-plane radial orbits do. "
   "This also breaks g03's substitution test A9, which swaps in Vitral+2024's beta_B -- a SPHERICAL radial "
   "anisotropy, a different physical quantity from the beta_z it replaces")

# ---------------------------------------------------------------------------------------------------------
# (E) THE CITED CORROBORATION
# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118)
P("E.  THE CITED INDEPENDENT CORROBORATION")
P("=" * 118)
LVD = os.path.join(DATA, "dsph", "lvd_dwarf_mw.csv")
lvd = {r["name"]: r for r in csv.DictReader(open(LVD))}
DL = [(n, 10 ** float(lvd[n]["mass_stellar"]), float(lvd[n]["rhalf_sph_physical"]) / 1000.0,
       float(lvd[n]["vlos_sigma"]), float(lvd[n]["distance_gc"])) for n in names]
def res_tab(a0, tab, mode="max"):
    out = []
    for nm, M, Rh, s, d in tab:
        R = Rh * kpc; gobs = 3.0 * (s * 1e3) ** 2 / R; gNi = G * M * Msun / R ** 2
        gext = MW_VC ** 2 / (d * kpc); gNe = gext * gext / a0
        gp = {"max": max(math.sqrt(gNi * a0), gNi * nu_s(gext / a0)),
              "qumond": nu_s((gNi + gNe) / a0) * (gNi + gNe) - nu_s(gNe / a0) * gNe}[mode]
        out.append(math.log10(gobs / gp))
    return np.array(out)
for f in A0:
    rl = res_tab(A0[f], DL, "max"); rq = res_tab(A0[f], DL, "qumond")
    info(f"{f:10} LVD max()  rho = {spear(rl, beta):+.3f}, exact p = {exact_p(spear(rl, beta)):.4f} "
         f"({p_to_sigma(exact_p(spear(rl, beta))):.2f} sigma);  LVD self-consistent rho = {spear(rq, beta):+.3f}"
         f" ({p_to_sigma(exact_p(spear(rq, beta))):.2f} sigma);  r(LVD, g03) = "
         f"{pear(rl, residuals(A0[f], 'max')):+.3f}")
rl = res_tab(a0c, DL, "max")
ck("V8 (THE CORROBORATION IS NOT INDEPENDENT AND IS WEAKER THAN QUOTED) the Local Volume Database rerun is "
   "offered as independent support at rho = +0.548. It must be an independent measurement and must reach the "
   "claimed strength",
   pear(rl, residuals(a0c, "max")) < 0.8 and exact_p(spear(rl, beta)) < 0.09,
   f"the two residual vectors correlate at r = {pear(rl, residuals(a0c,'max')):+.3f} (g03's own A4 reports "
   f"+0.955): it is the same eight objects with slightly different structural inputs and the SAME eight "
   f"anisotropies, so it re-tests the structural table and nothing else. Its rho = {spear(rl, beta):+.3f} is "
   f"exact p = {exact_p(spear(rl, beta)):.3f} = {p_to_sigma(exact_p(spear(rl, beta))):.2f} sigma, not 1.74")

# ---------------------------------------------------------------------------------------------------------
P(""); P("=" * 118); P("VERDICT OF THE ADVERSARIAL VERIFICATION"); P("=" * 118)
P("  THE ARITHMETIC IS SOUND.  rho = +0.667 and p = 0.082 reproduce independently on both footings, and the")
P(f"  exact 8! permutation null confirms p = {exact_p(2/3):.4f} = {p_to_sigma(exact_p(2/3)):.2f} sigma. The literature values were checked")
P("  against Hayashi+2020 and all eight match, error bars included. g03 is an honest file: 10 of its 13 checks")
P("  FAIL and its own A6, A7, A8, A9 and A13 already say most of what follows.")
P("")
P("  THE CLAIM IS REFUTED ON THE PHYSICS, IN THREE PLACES:")
P("  1. THE EXTERNAL FIELD.  g_pred = max(g_iso, g_efe) is not a physical criterion. Four of the eight dwarfs")
P("     sit in a Milky Way field 1.4 to 4.4 times their own internal MOND field, and all four are given the")
P("     ISOLATED deep-MOND asymptote; the only two given the external-field branch are the two LEAST externally")
P(f"     dominated. Treating the external field consistently drops rho to {rho_q:+.3f} -- exactly g03's own")
P(f"     Newtonian mutation control ({rho_n:+.3f}), which A6 already marks FAIL. The excess of the headline number")
P("     over the null control is produced by the branch rule, not by the data. This is the repository's own")
P("     listed bug pattern: a residual whose value tracks a branch of one's own prescription.")
P("  2. THE OBSERVABLE.  A global 3 sigma^2/R virial residual is the one observable on which Milgrom proved the")
P("     two arms AGREE in the deep-MOND limit, and all eight dwarfs are deep-MOND. Modified inertia is a class")
P("     and predicts no sign, so 'in the sense modified inertia would suggest' is post-hoc -- the two-sided test")
P("     g03 correctly ran is the formal admission that rho = -0.667 would have read the same way.")
P("  3. THE VARIABLE.  beta_z is a CYLINDRICAL vertical-to-radial ellipsoid ratio degenerate with the halo axis")
P("     ratio Q, not the radial anisotropy that distinguishes circular from eccentric orbits. It is a shape")
P("     parameter of the fit, not a trajectory parameter.")
P("")
P("  AND HONESTLY, AGAINST MY OWN ATTACK: the drop from +0.667 to +0.429 is 0.63 null-sd and is NOT itself")
P("  resolvable at N = 8. The correct statement is not 'the correlation is zero'. It is that every member of")
P("  the prescription family lies inside the null, the family's spread exceeds its own signal, and the number")
P("  that was quoted is the most favourable member. Nothing here says the framework fails these dwarfs; the")
P("  self-consistent prescription that kills the correlation also enlarges the residuals, and that is a")
P("  different question this file does not adjudicate.")
P("")
P("  WHAT WOULD MAKE THE TEST REAL, beyond g03's own list: the residual must be recomputed with the external")
P("  field treated self-consistently for every satellite, and the anisotropy must be a RADIAL beta_r rather")
P("  than a cylindrical beta_z -- and an actual modified-inertia theory must be named that predicts a sign.")
sys.exit(ck.done())
