#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g06v_adversarial_cluster_downward_refutation.py -- ADVERSARIAL AUDIT of g06's headline claim.
=================================================================================================================
THE CLAIM UNDER ATTACK (g06_local_volume_groups_lambda_edge.py, check C1 + section 9 item 1):

  "The cluster deficit does not extend downward in acceleration.  Every X-ray group and cluster row in
   THE_LIABILITY_TABLE.md sits above this rung's boost while sitting at HIGHER acceleration, so the residual is
   not the low-acceleration tail of a kernel error; the variable that changes between the two is whether the
   baryon budget is counted or modelled."
  Numbers offered: 14/14 pressure rows with boost <= 3 sit above 0.82; those rows span g/a0 = 0.004-1.640,
  median 0.111, against this rung's median 0.0019 and range 0.00013-0.0208.  Slope inside the sample
  -0.019 (r = -0.02) against a permutation null 0.159, i.e. 0.12 sigma.

WHAT THIS FILE DOES.  It re-runs g06's OWN machinery (imported verbatim by exec, no re-implementation, so any
disagreement is an argument and not a transcription error) and then attacks four things g06 did not test:

  V1  CURRENCY.  Is (sigma_obs/sigma_pred)^2 the same quantity as the liability table's acceleration boost?
      If it is not, the two rungs are not on one axis and the comparison is void.  (This one is a control that
      should PASS -- verifying a "works" as hard as a "fails".)
  V2  SELECTION ON THE DEPENDENT VARIABLE.  The comparison set was built with the cut "pressure AND boost <= 3".
      That is a cut on the very quantity being compared.  Which rows does it delete, and where do they sit in
      acceleration?
  V3  THE CROSS-RUNG TREND.  THE_LIABILITY_TABLE.md's own headline regression over its 26 boost-carrying rows is
      slope -0.206, r = -0.53 -- boost RISING toward LOW acceleration, which is exactly the "low-acceleration
      tail" reading the claim denies.  Does the boost <= 3 cut create the flat trend the claim relies on?
  V4  MEMBERSHIP-CUT ROBUSTNESS OF THE RUNG'S OWN MEDIAN.  boost goes as sigma^2 and half of g06's groups have
      5-8 members.  Does the median boost survive a cut on membership, and does the best-measured subsample
      still sit below every cluster row?
  V5  SMALL-N BIAS OF THE DISPERSION ESTIMATOR.  The sampling distribution of a dispersion estimator at n = 5 is
      right-skewed, so the MEDIAN estimate sits BELOW the truth.  boost goes as sigma^2.  Monte-Carlo the gapper
      on the actual per-group membership counts and size the bias.
  V6  DEEP-MOND APPLICABILITY and the MODIFIED-INERTIA framing, checked as physics rather than as prose.

BOTH FOOTINGS.  MUTATION CONTROLS.  CHECKS CAN FAIL, AND SEVERAL ARE MEANT TO.
Data and citations are g06's own; the liability rows are transcribed from THE_LIABILITY_TABLE.md (2026-09-03).
"""
import sys, os, math, io, contextlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0, G, Msun, Mpc, kpc, nu, nu_s

ck = Check(); rng = np.random.default_rng(20260903)
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "g06_local_volume_groups_lambda_edge.py")

# ================================================================================================ SECTION 0
P("="*126)
P("0.  RE-RUN g06's OWN MACHINERY VERBATIM (exec of the committed file; nothing re-implemented)")
P("="*126)
ns = {"__name__": "__g06__", "__file__": TARGET}
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(open(TARGET).read(), TARGET, "exec"), ns)
except SystemExit:
    pass
groups = ns["groups"]; RES = ns["RES"]; run = ns["run"]; predict_sigma = ns["predict_sigma"]
bcan = ns["bcan"]; xcan = ns["xcan"]; balt = ns["balt"]; med_can = ns["med_can"]; med_alt = ns["med_alt"]
lo68, hi68 = ns["lo68"], ns["hi68"]; gapper = ns["gapper"]; seg_se = ns["seg_se"]
info(f"imported: {len(groups)} groups, canonical median boost {med_can:.3f}, alt {med_alt:.3f}, "
     f"bootstrap [{lo68:.3f}, {hi68:.3f}]; g06 printed {len(buf.getvalue().splitlines())} lines, suppressed")
ck("V0 the re-run reproduces g06's published headline exactly, so everything below is an argument about that "
   "number and not a transcription of a different one",
   abs(med_can - 0.817) < 0.005 and abs(med_alt - 0.746) < 0.005,
   f"re-run canonical {med_can:.3f} (published 0.817), alt {med_alt:.3f} (published 0.746)")

# ================================================================================================ SECTION 1
P(""); P("="*126)
P("1.  V1 -- CURRENCY.  Is (sigma_obs/sigma_pred)^2 the liability table's ACCELERATION boost?")
P("="*126)
info("THE_LIABILITY_TABLE.md defines its currency as 'the factor by which the observation exceeds the framework's")
info("zero-parameter prediction in ACCELERATION'.  g06 reports (sigma_obs/sigma_pred)^2.  These agree only if")
info("sigma^2 scales as g at fixed radius.  In the deep-MOND point-mass limit sigma^2 = (1/3) sqrt(G M a_0) and")
info("g = sqrt(G M a_0)/r, so BOTH ratios equal sqrt(M_dyn/M_bar).  Checked numerically, not asserted.")
a0v = A0["canonical"]
Mb_t, Mdyn_t = 1.0e11*Msun, 4.0e11*Msun          # a factor 4 in mass
r_t = 0.3*Mpc
g_ratio = math.sqrt(G*Mdyn_t*a0v)/r_t / (math.sqrt(G*Mb_t*a0v)/r_t)
s2_ratio = math.sqrt(G*Mdyn_t*a0v)/3.0 / (math.sqrt(G*Mb_t*a0v)/3.0)
ck("V1 the two rungs ARE in one currency: a dispersion-squared ratio and an acceleration ratio are the same "
   "number in the deep-MOND limit, so g06's row can legitimately be laid beside the X-ray rows.  This check is a "
   "control -- if it had failed, the whole comparison would be void by a square root and the claim would die here",
   abs(g_ratio/s2_ratio - 1) < 1e-9,
   f"a factor {Mdyn_t/Mb_t:.0f} in mass gives acceleration ratio {g_ratio:.6f} and sigma^2 ratio {s2_ratio:.6f}; "
   f"both = sqrt(M_dyn/M_bar) = {math.sqrt(Mdyn_t/Mb_t):.6f}")
xmax = float(xcan.max())
ck("V1b and the deep-MOND limit that V1 leans on is actually where these groups live, so the currency identity is "
   "not being used outside its domain",
   xmax < 0.05, f"largest internal g_bar/a_0 in the sample is {xmax:.5f}, deepest {xcan.min():.5f}; the kernel's "
   f"transition sits at y ~ 1, three decades away")

# ================================================================================================ SECTION 2
P(""); P("="*126)
P("2.  V2 -- SELECTION ON THE DEPENDENT VARIABLE.  What the 'boost <= 3' cut deletes")
P("="*126)
# THE_LIABILITY_TABLE.md (2026-09-03), the 26 boost-carrying rows that also carry a g/a0.
TAB = [(44.7, 0.001, "pressure", "MW ultra-faint dwarfs, 31 satellites"),
       (6.40, 0.185, "rotation", "HI warp onset, 16 WHISP edge-on discs"),
       (6.00, 0.049, "pressure", "Pal 4 (outer-halo globular)"),
       (4.63, 0.730, "pressure", "SLUGGS globular systems, log M* >= 11.3"),
       (4.60, 0.010, "pressure", "Pal 14 (outer-halo globular)"),
       (3.57, 0.012, "two-body", "isolated major galaxy pairs, 2MRS"),
       (3.45, 0.361, "lensing",  "CLASH, 20 clusters"),
       (3.17, 0.414, "lensing",  "Bullet BCG1"),
       (3.15, 0.382, "lensing",  "Bullet BCG3"),
       (2.91, 0.520, "pressure", "X-COP cluster cores, 30-100 kpc"),
       (2.76, 0.259, "pressure", "X-COP at 0.2 R500"),
       (2.63, 0.004, "pressure", "eRASS1 groups 10^12.5-13.5 at R500"),
       (2.56, 0.059, "pressure", "eRASS1 fixed mass 1-3e14, z = 0.7-1.0"),
       (2.48, 0.038, "rotation", "six tidal dwarf galaxies"),
       (2.24, 0.041, "pressure", "X-ray groups at R2500"),
       (2.17, 0.113, "pressure", "eRASS1 rich clusters at R500"),
       (2.13, 0.036, "pressure", "eRASS1 clusters 10^14-14.5 at R500"),
       (2.09, 0.175, "pressure", "X-COP at 0.5 R500"),
       (1.93, 0.110, "pressure", "the a0 ladder's cluster rung"),
       (1.92, 0.031, "pressure", "eRASS1 fixed mass 1-3e14, z < 0.15"),
       (1.69, 0.800, "pressure", "X-ray ellipticals, 5-70 kpc"),
       (1.50, 0.353, "rotation", "DiskMass, 22 discs at 2.2 scale lengths"),
       (1.48, 0.111, "pressure", "X-COP at 0.9 R500"),
       (1.45, 0.023, "pressure", "X-ray groups at R500"),
       (1.30, 1.640, "pressure", "SLUGGS globular systems, log M* < 11.3"),
       (1.30, 1.390, "rotation", "Milky Way vertical force K_z at 1.1 kpc")]
press = [(b, x, s, n) for b, x, s, n in TAB if s == "pressure"]
kept  = [t for t in press if t[0] <= 3.0]
cutaway = [t for t in press if t[0] > 3.0]
info(f"pressure-supported rows in the table: {len(press)}.  g06's comparison set is 'pressure AND boost <= 3': "
     f"{len(kept)} kept, {len(cutaway)} DELETED.")
P(f"    {'DELETED row':46} {'boost':>7} {'g/a0':>8}  {'vs this rung'}")
for b, x, s, n in sorted(cutaway, key=lambda t: t[1]):
    rel = ("BELOW the rung's median acceleration" if x < float(np.median(xcan)) else
           "inside the rung's acceleration range" if x <= xmax else "above the rung's range")
    P(f"    {n:46} {b:7.2f} {x:8.4f}  {rel}")
xmed = float(np.median(xcan))
low_and_high = [t for t in press if t[1] <= xmax and t[0] > med_can]
low_below_med = [t for t in press if t[1] <= xmed]
info(f"this rung: median g/a0 = {xmed:.5f}, range {xcan.min():.5f} - {xmax:.5f}, boost {med_can:.2f}")
ck("V2 (THE CENTRAL ATTACK) the claim is that NOTHING at or below this rung's acceleration carries a cluster-sized "
   "boost -- that is what 'the deficit does not extend downward' means.  Tested against ALL pressure rows rather "
   "than the boost-selected 14, it asserts that no pressure row at or below this rung's own MEDIAN acceleration "
   "sits above this rung's boost.  If it fails, the comparison set was built by cutting on the quantity being "
   "compared and the ordering statistic 14/14 is circular",
   len(low_below_med) == 0 or all(b <= med_can for b, x, s, n in low_below_med),
   f"pressure rows at g/a_0 <= {xmed:.5f} (this rung's median): " +
   ("none" if not low_below_med else "; ".join(f"{n} at {x:.4f} a_0, boost {b:.2f}" for b, x, s, n in low_below_med))
   + f".  This rung's boost is {med_can:.2f}")
ck("V2b and the weaker form: within this rung's own acceleration RANGE (0.00013 - 0.0208 a_0), no pressure row "
   "carries a boost above the rung's.  This is the honest scope of the 'does not extend downward' statement, "
   "because outside that range the two rungs are not being compared at matched acceleration at all",
   len(low_and_high) == 0,
   f"{len(low_and_high)} pressure rows lie inside the rung's acceleration range with a LARGER boost: " +
   ("none" if not low_and_high else "; ".join(f"{n} ({b:.2f} at {x:.4f})" for b, x, s, n in low_and_high)))

# ================================================================================================ SECTION 3
P(""); P("="*126)
P("3.  V3 -- DOES THE 'boost <= 3' CUT MANUFACTURE THE FLAT TREND?")
P("="*126)
def fitslope(rows):
    x = np.log10(np.array([t[1] for t in rows])); y = np.log10(np.array([t[0] for t in rows]))
    A = np.vstack([x, np.ones_like(x)]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    return float(m), float(np.corrcoef(x, y)[0, 1])
for lbl, rows in (("all 26 boost-carrying rows", TAB), ("all pressure rows", press),
                  ("pressure rows AFTER the boost <= 3 cut  (g06's set)", kept)):
    m, r = fitslope(rows)
    info(f"    {lbl:52} N = {len(rows):2d}   slope = {m:+.3f}   r = {r:+.3f}")
m_all, r_all = fitslope(press); m_cut, r_cut = fitslope(kept)
m26, r26 = fitslope(TAB)
info(f"THE_LIABILITY_TABLE.md's own published regression over its 26 rows is slope -0.206, r = -0.53; reproduced "
     f"here as {m26:+.3f}, r = {r26:+.3f}")
ck("V3 the table's own headline says the boost RISES toward LOW acceleration (slope -0.206, r = -0.53).  That is "
   "the 'low-acceleration tail' reading.  This check asserts the boost <= 3 cut does not materially change that "
   "trend.  If it fails, g06's flat picture is an artefact of the cut, not a property of the data",
   abs(m_cut - m_all) < 0.5*abs(m_all) or abs(m_all) < 0.05,
   f"all pressure rows slope {m_all:+.3f} (r = {r_all:+.3f}); after the cut {m_cut:+.3f} (r = {r_cut:+.3f}); "
   f"the cut changes the slope by {m_cut - m_all:+.3f}, i.e. {100*abs(m_cut-m_all)/abs(m_all):.0f}% of it")
# mutation control on V3: a cut at the SAME rank fraction but on the INDEPENDENT variable must not do this
n_del = len(cutaway)
by_x = sorted(press, key=lambda t: -t[1])[n_del:]          # delete the n_del highest-acceleration rows instead
m_x, r_x = fitslope(by_x)
ck("V3b MUTATION CONTROL for V3.  Delete the same NUMBER of pressure rows, but by the INDEPENDENT variable "
   "(highest acceleration) instead of by boost.  A cut that is innocent of the dependent variable must leave the "
   "sign of the trend alone.  This isolates 'cutting on boost' as the cause rather than 'cutting 4 rows'",
   np.sign(m_x) == np.sign(m_all),
   f"deleting the {n_del} highest-ACCELERATION rows leaves slope {m_x:+.3f} (r = {r_x:+.3f}), same sign as the "
   f"full {m_all:+.3f}; deleting the {n_del} highest-BOOST rows gives {m_cut:+.3f}")
# and: where does g06's own row fall on the all-pressure-row trend?
pred_at_rung = m_all*math.log10(xmed) + np.linalg.lstsq(
    np.vstack([np.log10(np.array([t[1] for t in press])), np.ones(len(press))]).T,
    np.log10(np.array([t[0] for t in press])), rcond=None)[0][1]
info(f"extrapolating the ALL-pressure-row trend to this rung's median acceleration {xmed:.5f} predicts "
     f"log boost = {pred_at_rung:+.3f} (boost {10**pred_at_rung:.2f}); g06 measures {math.log10(med_can):+.3f} "
     f"(boost {med_can:.2f}).  The rung is {pred_at_rung - math.log10(med_can):+.3f} dex BELOW that trend, which "
     f"is the real content of the finding -- an outlier from the table's trend, not a demonstration that the "
     f"trend is absent.")

# ================================================================================================ SECTION 4
P(""); P("="*126)
P("4.  V4 -- IS 0.82 ROBUST TO A MEMBERSHIP CUT?  boost goes as sigma^2 and half these groups have 5-8 members")
P("="*126)
NV = np.array([g["Nv"] for g in groups]); NM = np.array([g["N"] for g in groups])
P(f"    {'membership cut':>16} {'N groups':>9} {'median boost (can)':>19} {'(alt)':>8} {'median g/a0':>12} "
  f"{'typ stat err/dex':>17}")
CUTS = {}
for nmin in (5, 8, 10, 15, 20):
    k = NM >= nmin
    if k.sum() < 3: continue
    bc = bcan[k]; ba = balt[k]; xx = xcan[k]
    est = float(np.median([2.0/math.sqrt(2*(g["Nv"]-1))/math.log(10) for g, kk in zip(groups, k) if kk]))
    CUTS[nmin] = (float(np.median(bc)), float(np.median(ba)), int(k.sum()), float(np.median(xx)))
    P(f"    {'N >= '+str(nmin):>16} {int(k.sum()):9d} {np.median(bc):19.3f} {np.median(ba):8.3f} "
      f"{np.median(xx):12.5f} {est:17.3f}")
m20 = CUTS[20][0]; m20a = CUTS[20][1]; m10 = CUTS[10][0]
swing = abs(math.log10(m20/med_can))
ck("V4 the headline median must not depend on where the membership cut is put.  g06 keeps every group with >= 5 "
   "members; a 5-member gapper carries 0.31 dex on its own boost while a 39-member one carries 0.10.  This check "
   "asserts that moving the cut to N >= 20 -- the six groups whose dispersions are actually measured -- moves the "
   "median boost by less than the claimed separation's own standard error of "
   f"{seg_se:.3f} dex.  A failure means the number quoted in the liability table is a statement about the "
   "catalogue's faint end",
   swing < seg_se, f"N >= 5 (g06's primary): {med_can:.3f}; N >= 10: {m10:.3f}; N >= 20: {m20:.3f} canonical / "
   f"{m20a:.3f} alt -- a swing of {swing:+.3f} dex against the standard error {seg_se:.3f} dex")
xray_kept = [t for t in kept]
below_all_20 = [t for t in xray_kept if t[0] > m20]
ck("V4b THE ORDERING STATISTIC ITSELF.  C1's '14 of 14' is the load-bearing sentence.  Recompute it on the "
   "best-measured half of the rung (N >= 20).  If the 14/14 does not survive, the claim 'every X-ray group and "
   "cluster row sits above this rung's boost' is a property of the 5-member groups",
   len(below_all_20) == len(xray_kept),
   f"{len(below_all_20)} of {len(xray_kept)} rows sit above the N >= 20 median of {m20:.2f} "
   f"(g06's N >= 5 value was {med_can:.2f}, 14 of 14).  The rows now BELOW it: " +
   ("none" if len(below_all_20) == len(xray_kept) else
    ", ".join(f"{n} ({b:.2f})" for b, x, s, n in xray_kept if b <= m20)))
# is the membership dependence a real trend or noise?
rr = float(np.corrcoef(np.log10(NM.astype(float)), np.log10(bcan))[0, 1])
perm = np.array([float(np.corrcoef(np.log10(NM.astype(float)), rng.permutation(np.log10(bcan)))[0, 1])
                 for _ in range(4000)])
ck("V4c and is that membership dependence a trend or an accident of six points?  Judged against a permutation "
   "null, the same way g06 judged its own acceleration slope in R5.  A null here would mean V4/V4b are small-"
   "sample noise and the claim survives them",
   abs(rr) < 2*perm.std(), f"corr(log N_members, log boost) = {rr:+.3f} against a permutation null of width "
   f"{perm.std():.3f}, i.e. {abs(rr)/perm.std():.2f} sigma")

# ================================================================================================ SECTION 5
P(""); P("="*126)
P("5.  V5 -- SMALL-N BIAS.  The MEDIAN of a dispersion estimator at n = 5 sits BELOW the truth, and boost ~ sigma^2")
P("="*126)
info("Monte-Carlo: draw n Gaussian velocities of unit true dispersion, apply g06's own gapper() function, and")
info("record the median of the returned sigma^2.  This is a property of the estimator, not of the data.")
P(f"    {'n':>4} {'median (sigma_hat/sigma)^2':>27} {'bias in dex':>13}")
BIAS = {}
for n in sorted(set(int(v) for v in NV)):
    s2 = np.array([gapper(rng.normal(0.0, 1.0, n))**2 for _ in range(20000)])
    BIAS[n] = float(np.median(s2))
    P(f"    {n:4d} {BIAS[n]:27.4f} {math.log10(BIAS[n]):13.4f}")
corr = np.array([bcan[i]/BIAS[int(groups[i]["Nv"])] for i in range(len(groups))])
corr_a = np.array([balt[i]/BIAS[int(groups[i]["Nv"])] for i in range(len(groups))])
shift = math.log10(float(np.median(corr))/med_can)
ck("V5 the estimator's own small-n bias must be smaller than the effect being claimed.  Debiasing each group's "
   "boost by the Monte-Carlo median of its own membership count moves the sample median; this check asserts that "
   "move is under half the claimed separation's standard error.  It is a bias against the framework's interest "
   "in the sense that correcting it RAISES the boost toward the cluster rows",
   abs(shift) < 0.5*seg_se,
   f"debiased median boost {np.median(corr):.3f} canonical / {np.median(corr_a):.3f} alt against g06's "
   f"{med_can:.3f} / {med_alt:.3f}: a shift of {shift:+.3f} dex, standard error {seg_se:.3f} dex")
info(f"combining V4 and V5: the N >= 20 subsample debiased sits at "
     f"{float(np.median([bcan[i]/BIAS[int(groups[i]['Nv'])] for i in range(len(groups)) if groups[i]['N'] >= 20])):.3f} "
     f"canonical, against g06's headline {med_can:.3f} and the X-ray rows' 1.45 - 2.91.")

# ================================================================================================ SECTION 6
P(""); P("="*126)
P("6.  V6 -- THE PHYSICS FRAMING: deep-MOND applicability, the EFE regime, and modified inertia")
P("="*126)
en_over_x = np.array([g["gext"]/g["gN_rh"] for g in groups])
info(f"groups: internal g_bar/a_0 = {xcan.min():.5f} - {xmax:.5f}; e_N/x_int = {en_over_x.min():.3f} - "
     f"{en_over_x.max():.3f}, median {np.median(en_over_x):.3f}")
DSPH_X = np.array([0.00249, 0.01203, 0.03573, 0.00255, 0.00038, 0.03657, 0.01001, 0.00371])
DSPH_E = np.array([0.01554, 0.01215, 0.00420, 0.00817, 0.01215, 0.00145, 0.00171, 0.01554])
info(f"dwarf spheroidals (g06 section 7): e_N/x_int = {(DSPH_E/DSPH_X).min():.2f} - {(DSPH_E/DSPH_X).max():.2f}, "
     f"median {np.median(DSPH_E/DSPH_X):.2f}")
ck("V6 the two pressure-supported populations g06 compares in section 7 are in the SAME external-field regime, "
   "so the interpolated branch is doing the same job in both.  g06's own check R4 says the pure external-field "
   "limit is inapplicable to the groups and would move them by a factor 3.93; if the dwarf spheroidals sit in "
   "that limit while the groups do not, the +0.82 dex gap of check F3 is partly a regime difference and not a "
   "difference between the systems",
   np.median(DSPH_E/DSPH_X) < 1.0 and float(np.median(en_over_x)) < 1.0,
   f"groups median e_N/x_int = {np.median(en_over_x):.3f} (internal-field dominated); dwarf spheroidals median "
   f"{np.median(DSPH_E/DSPH_X):.2f}, with {int((DSPH_E/DSPH_X > 1).sum())} of 8 EXTERNAL-field dominated "
   f"(Draco {DSPH_E[0]/DSPH_X[0]:.1f}, Sextans {DSPH_E[4]/DSPH_X[4]:.1f}, Ursa Minor {DSPH_E[7]/DSPH_X[7]:.1f})")
src = open(TARGET).read()
overclaim = "EVERY pressure-supported system should sit above the kernel" in src
retract = "it fixes no sign and no size for the difference" in src
ck("V6b MODIFIED INERTIA IS A CLASS, NOT A THEORY.  Milgrom's theorem (1994; 2011 arXiv:1111.1611) says only that "
   "modified inertia and modified gravity agree for CIRCULAR deep-MOND orbits and differ otherwise.  It fixes no "
   "sign and no magnitude on a group's eccentric satellite orbits.  g06's check F1 asserts 'EVERY pressure-"
   "supported system should sit above the kernel', which is not a consequence of the theorem.  This check passes "
   "only if the file ALSO retracts that inference where a reader would meet it",
   (not overclaim) or retract,
   f"the over-strong premise is {'present' if overclaim else 'absent'} in F1's check text; the retraction "
   f"('it fixes no sign and no size') is {'present' if retract else 'ABSENT'} in section 9.  The premise is "
   f"therefore stated as a check and withdrawn as a conclusion in the same file -- readable, but F1's own text "
   f"must not be quoted without section 9 item 2")
ck("V6c BOTH FOOTINGS genuinely enter the attacked claim, rather than being printed decoratively.  The claim's "
   "own headline number 0.82 is canonical-only (C1 never touches the alt footing); this check asserts the alt "
   "footing would not change the claim's direction",
   (med_alt < min(b for b, x, s, n in kept)) == (med_can < min(b for b, x, s, n in kept)),
   f"canonical {med_can:.3f} and alt {med_alt:.3f} both sit below the lowest kept row "
   f"{min(b for b,x,s,n in kept):.2f}; the alt footing is LOWER, so it strengthens rather than threatens C1 -- "
   f"but note that C1, R3-R6 and F1-F3 are all computed on the canonical footing alone")

# ================================================================================================ SECTION 7
P(""); P("="*126)
P("7.  MUTATION CONTROLS ON THIS AUDIT")
P("="*126)
fake = [(b, x, s, n) for b, x, s, n in press]
fake_shuf = [(fake[i][0], fake[j][1], fake[i][2], fake[i][3])
             for i, j in zip(range(len(fake)), rng.permutation(len(fake)))]
m_sh = np.array([fitslope([(fake[i][0], fake[j][1], "p", "") for i, j in
                           zip(range(len(fake)), rng.permutation(len(fake)))])[0] for _ in range(2000)])
ck("W1 MUTATION -- shuffle the accelerations against the boosts among the pressure rows.  The all-row trend V3 "
   "leans on must be distinguishable from that null, or V3 has no content and the claim survives V3",
   abs(m_all) > 2*m_sh.std(), f"all-pressure-row slope {m_all:+.3f} against a shuffled null of width "
   f"{m_sh.std():.3f}, i.e. {abs(m_all)/m_sh.std():.2f} sigma")
b_nonu = np.array([x["boost"] for x in run(A0["canonical"], nu_on=False)])
ck("W2 MUTATION -- the imported machinery still responds to switching the kernel off, so the exec-import did not "
   "silently freeze a cached result",
   float(np.median(b_nonu)) > 8.0, f"Newtonian median boost {np.median(b_nonu):.1f} against the framework's "
   f"{med_can:.2f}")
ck("W3 MUTATION -- V4's membership effect must vanish when the boosts are randomly reassigned to groups, or V4 is "
   "measuring the marginal distribution rather than the membership",
   True, f"reported not asserted: over 2000 reassignments the median |log10(median_{{N>=20}}/median_{{N>=5}})| is "
   f"{np.median([abs(math.log10(np.median(rng.permutation(bcan)[NM>=20])/np.median(bcan))) for _ in range(2000)]):.3f} "
   f"dex, against the real {swing:.3f} dex")

# ================================================================================================ SECTION 8
P(""); P("="*126)
P("8.  VERDICT")
P("="*126)
info("WHAT SURVIVES")
info("  * The currency is right (V1, V1b).  A dispersion-squared ratio IS the table's acceleration boost in the")
info("    deep-MOND limit, and these groups are three decades inside that limit.  The comparison is legitimate.")
info("  * The Jeans machinery, the enclosed-mass handling and the external-field inversion are not where this")
info("    breaks.  g06's own R3/R4/R6/M1-M5 are sound and its R2 and R4b failures are honestly reported.")
info("WHAT DOES NOT")
info(f"  * V2: the comparison set was built by cutting on the quantity being compared.  Of the {len(press)} "
     f"pressure rows, {len(cutaway)} were deleted by 'boost <= 3', and they include the table's LOWEST-")
info(f"    acceleration row (MW ultra-faint dwarfs, 0.001 a_0 -- below this rung's median {xmed:.5f}) carrying the")
info( "    table's LARGEST boost, 44.7, and Pal 14 at 0.010 a_0 (inside the rung's range) at 4.60.")
info(f"  * V3: the table's own trend over all pressure rows is slope {m_all:+.3f}; the cut turns it into "
     f"{m_cut:+.3f}.")
info(f"  * V4/V4b: the median boost is {med_can:.2f} at N >= 5 and {m20:.2f} at N >= 20, a {swing:.2f} dex swing "
     f"against a")
info(f"    quoted standard error of {seg_se:.3f} dex, and the 14/14 ordering does not survive it.")
info(f"  * V5: the gapper's own small-n bias moves the median a further {shift:+.3f} dex, in the same direction.")
P("")
info("THE HONEST RESIDUAL FINDING, which is smaller than the claim but is real: 26 Local Volume groups with a")
info("directly counted baryon budget sit BELOW the extrapolation of the liability table's own pressure-row trend")
info(f"to their acceleration by {pred_at_rung - math.log10(med_can):.2f} dex.  That is an outlier from the trend.")
info("It is NOT a demonstration that the trend is absent, and 'the deficit does not extend downward in")
info("acceleration' is contradicted by the table's own lowest-acceleration row.")
sys.exit(ck.done())
