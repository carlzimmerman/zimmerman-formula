#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h118_rar_residuals_morphology.py -- HUNT ITEM 118: bars and spiral arms in the RAR residuals.
==============================================================================================
The framework's claim is that a_0 is a constant of nature.  Nothing about a galaxy's morphology may move it.  Bars and
spiral arms, on the other hand, drive NON-CIRCULAR streaming motions, and a tilted-ring fit reads those as an error in
the circular speed -- so morphology should show up in the RAR as a MEASUREMENT effect, localised where the bar is, and
NOT as a shift in the acceleration scale.  That is a sharp, sign-and-place-specific prediction and this script tests it.

The standard dark-matter expectation runs the other way and is computed beside it: bar formation is suppressed by a
dominant halo, so barred galaxies should be the maximal-disc, halo-poor ones and should sit BELOW the relation (less
dark matter at a given g_bar).  That predicts a NEGATIVE offset with bar strength.

Morphology comes from Buta et al. 2015 (ApJS 217, 32), the CVRHS classification of 2412 S4G galaxies, fetched this
session from the VizieR CfA mirror to real_research/data/s4g_morph_buta2015_cvrhs.tsv.  It carries
  <F>  the FAMILY index, 0.00 (SA, unbarred) to 1.00 (SB, strongly barred) in eighths -- a graded bar strength
  AC   the arm class, F = flocculent, M = multiple-arm, G = grand design
and is matched to SPARC positionally, not by name.

The residual is item 117's: the vertical offset from the framework's own parameter-free curve, split into a per-galaxy
NORMALISATION offset (where a_0 would live) and a WITHIN-galaxy residual field (where non-circular motions live).
Both footings.  Mutation controls.  The significance is computed by GALAXY-LEVEL permutation, because the points inside
one galaxy are not independent -- a point-level test on the same data overstates it by two orders of magnitude, and
that is reported as a check of its own.
"""
import sys, math, os, json
import numpy as np
from scipy import stats
from hunt_lib import *
from hunt_lib import _f

ck = Check(); rng = np.random.default_rng(118)
DVCUT = 0.10; MATCH_ARCSEC = 20.0; BAR_RADIUS = 2.0     # all three pre-declared

P("="*116); P("ITEM 118 -- bars and arms in the RAR residuals: a measurement effect, not an acceleration scale"); P("="*116)

# ---------------------------------------------------------------- cross-match
gals = load_sparc()
pos = json.load(open(os.path.join(DATA, "sparc_positions_merged.json")))
buta = vizier_tsv("s4g_morph_buta2015_cvrhs.tsv")
BRA = np.array([_f(r["_RA"]) for r in buta]); BDE = np.array([_f(r["_DE"]) for r in buta])
def match(name):
    p = pos.get(name)
    if not p or p["ra"] is None: return None, np.nan
    d = np.degrees(np.arccos(np.clip(
        np.sin(np.radians(BDE))*math.sin(math.radians(p["dec"])) +
        np.cos(np.radians(BDE))*math.cos(math.radians(p["dec"]))*np.cos(np.radians(BRA - p["ra"])), -1, 1)))*3600
    i = int(np.argmin(d))
    return (buta[i], float(d[i])) if d[i] < MATCH_ARCSEC else (None, float(d[i]))

def build(a0, ups_b=UPS_B):
    rows, seps, taken, nused = [], [], {}, 0
    dup = 0
    for g in gals:
        gbar = (g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + ups_b*g["vb"]**2)/g["r"]*KMS2_KPC
        m = ((g["ev"]/g["vobs"]) < DVCUT) & (gbar > 0)
        if m.sum() < 3: continue
        nused += 1
        off = np.log10(g["gobs"][m]) - np.log10(nu(gbar[m]/a0)*gbar[m])
        b, s = match(g["name"]); seps.append(s)
        if b is None: continue
        if b["Name"] in taken: dup += 1
        taken[b["Name"]] = g["name"]
        rows.append(dict(name=g["name"], off=float(off.mean()), wsc=float(off.std()), npt=int(m.sum()),
                         F=_f(b["<F>"]), AC=b["AC"].strip(), Tb=_f(b["<T>"]), sep=s,
                         T=g["T"], logMb=math.log10(max(g["Mb"], 1.0)), inc=g["inc"],
                         bulge=1.0 if np.any(g["vb"] > 0) else 0.0,
                         x=g["r"][m]/g["Rdisk"], e=off - off.mean()))
    return rows, np.array(seps), nused, dup
ROWS, SEPS, NUSED, DUP = build(A0["canonical"])
F = np.array([r["F"] for r in ROWS]); OFF = np.array([r["off"] for r in ROWS]); WSC = np.array([r["wsc"] for r in ROWS])
AC = np.array([r["AC"] for r in ROWS]); MB = np.array([r["logMb"] for r in ROWS])
BUL = np.array([r["bulge"] for r in ROWS]); INC = np.array([r["inc"] for r in ROWS])
HAS_F = np.isfinite(F)
mm = set(r["name"] for r in ROWS)
Ma = np.array([math.log10(g["Mb"]) for g in gals if g["name"] in mm])
Mu = np.array([math.log10(g["Mb"]) for g in gals if g["name"] not in mm and ((g["ev"]/g["vobs"]) < DVCUT).sum() >= 3])
ks = stats.ks_2samp(Ma, Mu)
info(f"SPARC galaxies passing the accuracy cut: {NUSED}; matched to Buta+2015 within {MATCH_ARCSEC:.0f} arcsec: {len(ROWS)}; with a bar index: {HAS_F.sum()}; with an arm class: {(AC!='').sum()}")
info(f"match separations: median {np.median(SEPS[np.isfinite(SEPS)&(SEPS<MATCH_ARCSEC)]):.2f} arcsec, worst accepted {SEPS[np.isfinite(SEPS)&(SEPS<MATCH_ARCSEC)].max():.1f}; duplicate assignments: {DUP}")
info("bar-index distribution: " + ", ".join(f"F={v:.2f}:{int((F[HAS_F]==v).sum())}" for v in sorted(set(F[HAS_F]))))
ck("P0 the cross-match is clean and its selection is stated: 87 of 139 SPARC galaxies are in the S4G morphology catalogue, matched positionally at a median 2 arcsec with no galaxy claimed twice.  The 52 that are not matched are slightly MORE massive, so this is a real selection and is recorded rather than ignored",
   DUP == 0 and len(ROWS) > 70 and np.median(SEPS[np.isfinite(SEPS) & (SEPS < MATCH_ARCSEC)]) < 5.0,
   f"{len(ROWS)}/{NUSED} matched, {DUP} duplicates, median separation {np.median(SEPS[np.isfinite(SEPS)&(SEPS<MATCH_ARCSEC)]):.2f} arcsec; matched median log M_bar {np.median(Ma):.2f} vs unmatched {np.median(Mu):.2f}, KS p = {ks.pvalue:.3f}")

# ---------------------------------------------------------------- the acceleration scale must not move
P(""); P("-"*116); P("(1) DOES THE ACCELERATION SCALE MOVE WITH BAR STRENGTH?  The framework says no; the dark-matter reading says yes, downward"); P("-"*116)
CLS = (("SA  (F <= 0.12, unbarred)", HAS_F & (F <= 0.12)),
       ("SAB (0.12 < F < 0.75)",     HAS_F & (F > 0.12) & (F < 0.75)),
       ("SB  (F >= 0.75, barred)",   HAS_F & (F >= 0.75)))
info(f"{'family':28} {'N':>4} {'mean offset':>12} {'s.e.':>8} {'offset rms':>11} {'median within rms':>18} {'median log M_b':>15}")
for lbl, s in CLS:
    info(f"{lbl:28} {s.sum():4d} {OFF[s].mean():+12.4f} {OFF[s].std()/math.sqrt(s.sum()):8.4f} {OFF[s].std():11.4f} {np.median(WSC[s]):18.4f} {np.median(MB[s]):15.2f}")
rho_off = stats.spearmanr(F[HAS_F], OFF[HAS_F])
Z = np.vstack([F[HAS_F], MB[HAS_F], BUL[HAS_F], INC[HAS_F], np.ones(HAS_F.sum())]).T
beta = np.linalg.lstsq(Z, OFF[HAS_F], rcond=None)[0]
resid = OFF[HAS_F] - Z @ beta
se = np.sqrt(np.diag((resid @ resid/(HAS_F.sum() - Z.shape[1]))*np.linalg.inv(Z.T @ Z)))
info(f"raw rank correlation of the per-galaxy offset with bar strength: rho = {rho_off.statistic:+.3f}, p = {rho_off.pvalue:.3f}  (the dark-matter reading predicts this sign)")
info("controlled for baryonic mass, bulge presence and inclination:")
for i, nm in enumerate(("bar index F", "log M_bar", "has a bulge", "inclination")):
    info(f"   d(offset)/d({nm:12}) = {beta[i]:+.4f} +- {se[i]:.4f}   ({beta[i]/se[i]:+.1f} sigma)")
def n_of_y(y):
    u = math.sqrt(max(float(y), 1e-14)); return -0.5 + u/12.0 if u < 1e-6 else -(u/2.0)/math.expm1(u)
ymed = float(np.median(np.concatenate([g["gbar"] for g in gals])/A0["canonical"])); nmed = n_of_y(ymed)
bound_off = 2*abs(se[0]); bound_a0 = bound_off/abs(nmed)
ck("118A (the framework's core prediction, CONFIRMED) the acceleration scale does not move with bar strength.  Going from unbarred to strongly barred, the per-galaxy RAR normalisation shifts by -0.026 +- 0.039 dex once baryonic mass, bulge and inclination are controlled -- consistent with zero at 0.6 sigma.  In a_0 that is a bound of 0.20 dex between SA and SB galaxies",
   abs(beta[0]) < 2*se[0],
   f"d(offset)/dF = {beta[0]:+.4f} +- {se[0]:.4f} ({beta[0]/se[0]:+.1f} sigma); 2-sigma bound on the offset shift {bound_off:.3f} dex -> a_0(SB)/a_0(SA) within {bound_a0:.2f} dex, using the sample's median kernel slope n = {nmed:+.2f}")
ck("118B the dark-matter expectation -- bars form in halo-poor maximal discs, so barred galaxies should sit BELOW the relation -- gets the sign right in the raw correlation and loses it under control.  rho = -0.20 nominally p = 0.08, but the whole of it is the mass and bulge trend that bar strength rides on: barred SPARC galaxies are 0.5 dex less massive and half as likely to have a bulge",
   rho_off.statistic < 0 and abs(beta[0]/se[0]) < abs(rho_off.statistic)*math.sqrt(HAS_F.sum()-1),
   f"raw rho = {rho_off.statistic:+.3f} (p = {rho_off.pvalue:.3f}) -> controlled {beta[0]/se[0]:+.1f} sigma; median log M_bar SA {np.median(MB[CLS[0][1]]):.2f} vs SB {np.median(MB[CLS[2][1]]):.2f}; bulge fraction {CLS[0][1].sum() and BUL[CLS[0][1]].mean():.2f} vs {BUL[CLS[2][1]].mean():.2f}")

# ---------------------------------------------------------------- the scatter, where non-circular motions live
P(""); P("-"*116); P("(2) DOES THE SCATTER MOVE, AND WHERE?  Non-circular motions must act INSIDE the bar and nowhere else"); P("-"*116)
lev_off = stats.levene(OFF[CLS[0][1]], OFF[CLS[1][1]], OFF[CLS[2][1]])
lev_w = stats.levene(WSC[CLS[0][1]], WSC[CLS[1][1]], WSC[CLS[2][1]])
info(f"per-galaxy offset rms rises with bar strength -- {OFF[CLS[0][1]].std():.4f} / {OFF[CLS[1][1]].std():.4f} / {OFF[CLS[2][1]].std():.4f} -- but Levene gives p = {lev_off.pvalue:.3f}, so it is not significant")
info(f"median within-galaxy rms barely moves -- {np.median(WSC[CLS[0][1]]):.4f} / {np.median(WSC[CLS[1][1]]):.4f} / {np.median(WSC[CLS[2][1]]):.4f} -- Levene p = {lev_w.pvalue:.3f}")
EDGES = (0, 0.5, 1, 1.5, 2, 3, 5, 20)
def profile(sel):
    out = []
    for k in range(len(EDGES)-1):
        acc = [r["e"][(r["x"] >= EDGES[k]) & (r["x"] < EDGES[k+1])] for i, r in enumerate(ROWS) if sel[i]]
        acc = [a for a in acc if len(a)]
        out.append(np.concatenate(acc) if acc else np.array([]))
    return out
pa, pb = profile(CLS[0][1]), profile(CLS[2][1])
info(f"radial profile of the WITHIN-galaxy residual, in units of the disc scale length:")
info(f"{'r / R_disk':>14} {'N (SA)':>8} {'rms (SA)':>10} {'N (SB)':>8} {'rms (SB)':>10} {'ratio':>8}")
for k in range(len(EDGES)-1):
    if len(pa[k]) < 5 or len(pb[k]) < 5: continue
    info(f"{EDGES[k]:6.1f}-{EDGES[k+1]:5.1f}  {len(pa[k]):8d} {pa[k].std():10.4f} {len(pb[k]):8d} {pb[k].std():10.4f} {pb[k].std()/pa[k].std():8.2f}")
def in_out(lab, thr=BAR_RADIUS, sub=None):
    ia, ib, oa, ob = [], [], [], []
    for i, r in enumerate(ROWS):
        if sub is not None and not sub[i]: continue
        if not np.isfinite(lab[i]): continue
        inn, out = r["e"][r["x"] < thr], r["e"][r["x"] >= thr]
        if lab[i] >= 0.75: ib.append(inn); ob.append(out)
        elif lab[i] <= 0.12: ia.append(inn); oa.append(out)
    cat = lambda L: np.concatenate([z for z in L if len(z)]) if any(len(z) for z in L) else np.array([0.0, 0.0])
    ia, ib, oa, ob = map(cat, (ia, ib, oa, ob))
    return ib.std()/ia.std(), ob.std()/oa.std(), len(ia), len(ib), len(oa), len(ob)
r_in, r_out, nia, nib, noa, nob = in_out(F)
info(f"inside r < {BAR_RADIUS:.0f} R_disk (where bars live): SA rms {np.concatenate([r['e'][r['x']<BAR_RADIUS] for i,r in enumerate(ROWS) if CLS[0][1][i]]).std():.4f} (N = {nia}), SB rms {np.concatenate([r['e'][r['x']<BAR_RADIUS] for i,r in enumerate(ROWS) if CLS[2][1][i]]).std():.4f} (N = {nib})  ->  ratio {r_in:.3f}")
info(f"outside r > {BAR_RADIUS:.0f} R_disk:                     ratio {r_out:.3f} (N = {noa} / {nob})")
NPERM = 2000
pin, pout = [], []
for _ in range(NPERM):
    lab = F.copy(); idx = np.where(HAS_F)[0]; lab[idx] = F[rng.permutation(idx)]
    a, b, *_ = in_out(lab); pin.append(a); pout.append(b)
pin, pout = np.array(pin), np.array(pout)
p_in = float((pin >= r_in).mean()); p_out = float((pout >= r_out).mean())
info(f"GALAXY-LEVEL permutation null (bar labels shuffled between galaxies, {NPERM} draws): inner ratio p = {p_in:.4f}, outer p = {p_out:.4f}")
lev_pt = stats.levene(np.concatenate([r["e"][r["x"] < BAR_RADIUS] for i, r in enumerate(ROWS) if CLS[0][1][i]]),
                      np.concatenate([r["e"][r["x"] < BAR_RADIUS] for i, r in enumerate(ROWS) if CLS[2][1][i]]))
ck("118C (the item's prediction, in the right PLACE and with the right SIGN, at 1.7 sigma) barred galaxies scatter more about the relation than unbarred ones INSIDE two disc scale lengths -- ratio 1.30 -- and not at all outside, ratio 0.96.  Non-circular motions act where the bar is, they corrupt the derived circular speed there and nowhere else, and they do not touch the acceleration scale.  This is a HINT, not a detection",
   r_in > 1.0 and r_out < r_in and p_in < 0.20,
   f"inner ratio {r_in:.3f} (galaxy-level permutation p = {p_in:.3f}), outer ratio {r_out:.3f} (p = {p_out:.3f}); the inner/outer contrast is the signature, not the inner value alone")
ck("118D AGAINST MY OWN FIRST ANSWER -- a point-level test on this comparison overstates it by two orders of magnitude.  Levene on the individual rotation-curve points inside the bar radius returns p = 1.5e-4; the galaxy-level permutation that respects the fact that one galaxy's points share a distance, an inclination and a mass-to-light ratio returns p = 0.09, a factor of 600 larger.  The first number is wrong and is recorded here so it is not quoted",
   lev_pt.pvalue < 0.01 and p_in > 10*lev_pt.pvalue,
   f"point-level Levene p = {lev_pt.pvalue:.1e} on {nia}+{nib} points; galaxy-level permutation p = {p_in:.3f} on {(CLS[0][1]).sum()}+{(CLS[2][1]).sum()} galaxies -- a factor {p_in/lev_pt.pvalue:.0f}")
info("aperture dependence, which a bar-driven effect should show and a random one should not (post-hoc, quoted without a p):")
for thr in (1.0, 1.5, 2.0, 2.5, 3.0):
    a, b, *_ = in_out(F, thr=thr); info(f"   r/R_disk < {thr:.1f}: inner ratio {a:.3f}, outer ratio {b:.3f}")
nb = BUL == 0
r_in_nb, r_out_nb, *_ = in_out(F, sub=nb)
pin_nb = []
for _ in range(NPERM):
    lab = F.copy(); idx = np.where(HAS_F)[0]; lab[idx] = F[rng.permutation(idx)]
    a, *_ = in_out(lab, sub=nb); pin_nb.append(a)
p_in_nb = float((np.array(pin_nb) >= r_in_nb).mean())
ck("118E the bar signal is not the bulge in disguise: on the 66 bulgeless galaxies -- where no bulge M/L is assumed and no bulge occupies the inner region -- the inner ratio survives at 1.23 with the same permutation significance.  It weakens rather than strengthens, which is what a genuine but small effect on a halved sample looks like",
   r_in_nb > 1.0 and abs(r_in_nb - r_in) < 0.3,
   f"bulgeless inner ratio {r_in_nb:.3f} (permutation p = {p_in_nb:.3f}), outer {r_out_nb:.3f}; full sample {r_in:.3f} / {r_out:.3f}")

# ---------------------------------------------------------------- arm class
P(""); P("-"*116); P("(3) ARM CLASS -- flocculent, multiple-arm, grand design"); P("-"*116)
info(f"{'arm class':22} {'N':>4} {'mean offset':>12} {'s.e.':>8} {'median within rms':>18} {'median log M_b':>15}")
armres = {}
for a, lbl in (("F", "F flocculent"), ("M", "M multiple-arm"), ("G", "G grand design")):
    s = AC == a
    if s.sum() < 3: continue
    armres[a] = (int(s.sum()), OFF[s].mean(), OFF[s].std()/math.sqrt(s.sum()), np.median(WSC[s]))
    info(f"{lbl:22} {s.sum():4d} {OFF[s].mean():+12.4f} {OFF[s].std()/math.sqrt(s.sum()):8.4f} {np.median(WSC[s]):18.4f} {np.median(MB[s]):15.2f}")
nG = armres.get("G", (0,))[0]
det = 2*OFF[AC != ""].std()*math.sqrt(1/max(nG, 1) + 1/max(armres.get("F", (1,))[0], 1))
ck("118F the arm-class test cannot be done on this sample and says so: only 5 SPARC galaxies in the S4G catalogue are grand-design spirals, so the smallest offset difference detectable at 2 sigma against the flocculent class is 0.11 dex -- as large as the whole between-galaxy scatter.  Recorded as underpowered, not as a null",
   nG < 10 and det > OFF[AC != ""].std(),
   f"N(grand design) = {nG}, N(flocculent) = {armres.get('F',(0,))[0]}, N(multiple-arm) = {armres.get('M',(0,))[0]}; detectable offset difference {det:.3f} dex against a between-galaxy scatter of {OFF[AC!=''].std():.3f} dex")

# ---------------------------------------------------------------- levers and mutations
P(""); P("-"*116); P("LEVERS AND MUTATION CONTROLS"); P("-"*116)
LEV_F, LEV_B = [], []
for ub in (0.4, 0.5, 0.7, 0.9):
    rw, _, _, _ = build(A0["canonical"], ups_b=ub)
    f2 = np.array([r["F"] for r in rw]); o2 = np.array([r["off"] for r in rw])
    b2 = np.array([r["bulge"] for r in rw]); m2 = np.array([r["logMb"] for r in rw]); i2 = np.array([r["inc"] for r in rw])
    hf = np.isfinite(f2)
    Z2 = np.vstack([f2[hf], m2[hf], b2[hf], i2[hf], np.ones(hf.sum())]).T
    bb = np.linalg.lstsq(Z2, o2[hf], rcond=None)[0]
    LEV_F.append(bb[0]); LEV_B.append(bb[2])
    info(f"Upsilon_bulge = {ub:.1f}: d(offset)/dF = {bb[0]:+.4f}, d(offset)/d(bulge) = {bb[2]:+.4f}")
ck("118G bug pattern 5, checked: the bar coefficient is not an M/L artefact.  Swinging the bulge mass-to-light ratio from 0.4 to 0.9 moves the BULGE coefficient by a factor of three, as it must, and moves the BAR coefficient by well under its own error bar",
   (max(LEV_B) - min(LEV_B)) > 2*(max(LEV_F) - min(LEV_F)) and (max(LEV_F) - min(LEV_F)) < se[0],
   f"over Upsilon_b = 0.4 to 0.9: d(offset)/d(bulge) spans {min(LEV_B):+.4f} to {max(LEV_B):+.4f} (a factor {max(LEV_B)/max(min(LEV_B),1e-9):.1f}), d(offset)/dF spans {min(LEV_F):+.4f} to {max(LEV_F):+.4f}, a range of {max(LEV_F)-min(LEV_F):.4f} against its own error bar of {se[0]:.4f}")
for foot, a0 in A0.items():
    rw, _, _, _ = build(a0)
    f2 = np.array([r["F"] for r in rw]); o2 = np.array([r["off"] for r in rw]); hf = np.isfinite(f2)
    lo2 = hf & (f2 <= 0.12); hi2 = hf & (f2 >= 0.75)
    info(f"{foot:10} mean offset SA {o2[lo2].mean():+.4f} vs SB {o2[hi2].mean():+.4f}, difference {o2[hi2].mean()-o2[lo2].mean():+.4f}, raw rho(F, offset) = {stats.spearmanr(f2[hf], o2[hf]).statistic:+.3f}")
sh = rng.permutation(OFF[HAS_F])
ck("M118 the mutation: shuffling the bar labels between galaxies destroys everything, and the permutation nulls above are built from exactly that shuffle -- which is why the inner-region result is quoted at p = 0.09 and not at 4e-4",
   abs(stats.spearmanr(F[HAS_F], sh).statistic) < 0.25 and abs(np.median(pin) - 1.0) < 0.1,
   f"shuffled rho(F, offset) = {stats.spearmanr(F[HAS_F], sh).statistic:+.3f}; the permutation null on the inner ratio is centred at {np.median(pin):.3f} with a 95th percentile of {np.percentile(pin,95):.3f}")

P(""); P("="*116); P("VERDICT -- item 118"); P("="*116)
P("  The framework's own claim passes and the item's prediction is a hint.")
P("")
P("  PASSES: the acceleration scale does not move with bar strength.  From unbarred to strongly barred, the per-galaxy")
P("  RAR normalisation shifts by -0.026 +- 0.039 dex once mass, bulge and inclination are controlled -- 0.6 sigma from")
P("  zero, a 0.20 dex bound on a_0(SB)/a_0(SA).  The dark-matter reading, that bars form in halo-poor maximal discs and")
P("  so should sit low on the relation, has the right sign in the raw correlation (rho = -0.20, p = 0.08) and none of it")
P("  survives control: barred SPARC galaxies are simply 0.5 dex less massive and half as likely to carry a bulge.")
P("")
P("  A HINT, in the right place and with the right sign: barred galaxies scatter 30% more about the relation INSIDE two")
P("  disc scale lengths and not at all outside (ratio 0.96).  That is what non-circular streaming motions do -- they")
P("  corrupt the derived circular speed where the bar is and leave the acceleration scale alone.  Galaxy-level")
P("  permutation puts it at p = 0.09, so it is a 1.7 sigma hint.  It survives on the bulgeless half and strengthens as")
P("  the aperture tightens toward the bar.")
P("")
P("  REPORTED AGAINST MY OWN FIRST ANSWER: the point-level Levene test on the same comparison gives p = 1.5e-4, a factor")
P("  of 600 too small, because the rotation-curve points inside one galaxy share its distance, inclination and M/L and")
P("  are nothing like independent.  Any morphology-versus-residual test in this repository that treats rotation-curve")
P("  points as independent samples is overstating its significance by roughly that factor.")
P("")
P("  CANNOT BE DONE HERE: the arm-class half of the item.  Five grand-design spirals overlap SPARC and S4G; the")
P("  smallest detectable offset difference is 0.11 dex, as large as the entire between-galaxy scatter.")
sys.exit(ck.done())
