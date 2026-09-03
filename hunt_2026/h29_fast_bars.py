#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h29_fast_bars.py -- HUNT ITEM 29: are all galactic bars fast?
=============================================================
A live dark halo drains angular momentum from a bar by dynamical friction and slows it down, so LambdaCDM
simulations produce SLOW bars: R = R_corotation/R_bar > 1.4 for most (Roshan et al. 2021, MNRAS 508, 926,
"Fast galaxy bars continue to challenge standard cosmology").  MOND-class gravity has no live halo to absorb the
angular momentum, so simulated MOND bars stay fast, R ~ 1.0-1.4 indefinitely (Tiret & Combes 2007, A&A 464, 517).
The hunt list's Kepler-grade condition is >= 90 per cent of bars with R < 1.4.

DATA (fetched this session, saved under real_research/data/bars/):
  geron2023_manga_barspeeds_table3.tsv / _bars_table1.tsv
    Geron et al. 2023, MNRAS 521, 1775 (VizieR J/MNRAS/521/1775), the largest homogeneous Tremaine-Weinberg sample:
    225 MaNGA barred galaxies with Omega_bar, R_CR and R = R_CR/R_bar, each with published lower and upper bounds,
    plus bar type (Galaxy Zoo DESI strong/weak), deprojected bar radius and inclination in table 1.
  califa_tw_rotation_rates.tsv          [SECOND ARM, added on the audit pass]
    the CALIFA Tremaine-Weinberg series: Aguerri et al. 2015, A&A 576, A102 Table 4 (15 strong bars, four TW
    variants each) and Cuomo et al. 2019, A&A 632, A51 Table 3 (16 weak bars) -- an independent survey with an
    independent bar-length method.  Transcribed from the arXiv LaTeX sources.
  cuomo2021_barlength_systematic.tsv    [SECOND ARM]
    Cuomo et al. 2021, A&A 649, A30 Table A.1 + Table 2: the SAME galaxy and the SAME corotation radius divided by
    up to seven different published bar-radius estimates.  This measures the bar-length systematic on R instead of
    assuming it, which is what the first version of this script had to do.

WHAT THIS ITEM IS AND IS NOT, STATED UP FRONT
  R is a DIMENSIONLESS ratio.  a_0 does not enter it and neither footing changes any number below, so this item
  cannot measure a_0 and cannot separate the footings; it tests only whether halo dynamical friction is at work.
  The one place a_0 appears is a context calculation: the acceleration at corotation, from Omega_bar and R_CR.

WHAT IS DONE, AND WHAT MY OWN ESTIMATOR DID
  * the raw fractions against the list's 90 per cent criterion, and the per-galaxy verdicts from the published bounds;
  * the fraction with R < 1 -- corotation INSIDE the bar, dynamically impossible, hence a direct measure of how much
    of the spread is not noise but systematics;
  * the strong correlation between R and its own published uncertainty, and the answer split by measurement quality;
  * a forward-model deconvolution (intrinsic R = (1-f) x fast + f x slow, convolved with each galaxy's published
    uncertainty scaled by a fitted global factor) -- WHICH IS THEN PUT THROUGH A POSTERIOR PREDICTIVE CHECK AND
    FAILS IT.  The maximum-likelihood answer is therefore NOT quoted as a result.  That failure is the finding.
  * INJECTION/RECOVERY as the mutation control, which shows the estimator is unbiased under its own assumptions --
    which is exactly what makes the predictive failure a statement about the error model and not about the code;
  * the systematic that would decide it, quantified as a factor on the adopted bar length.
SECOND ARM, added on the audit pass because the first version rested on a single catalogue:
  * the CALIFA TW sample, which MEETS the hunt list's >= 90 per cent criterion while MaNGA misses it threefold --
    the two catalogues are 9 sigma apart on their own sampling errors, so the item is not decidable from either;
  * the bar-length systematic MEASURED: Cuomo+2021 give one corotation radius per galaxy over seven published
    bar-radius definitions, and R moves by a factor ~2 within a single galaxy -- the same size as the factor that
    would flip the MaNGA answer.  The deciding systematic is a routine methodological choice, not a hypothesis;
  * and against interest, the arm that AGREES with the framework does so with half its bars at R < 1, which is
    impossible, so it cannot be banked as support.
Checks CAN fail.
"""
import sys, math, os
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(2911)
BD = os.path.join(DATA, "bars")
R_FAST = 1.4                     # the conventional fast/slow divide (Debattista & Sellwood 2000)

def read_vizier(path):
    rows = [l.rstrip("\n").split("\t") for l in open(path) if l.strip() and not l.startswith("#")]
    hdr = [h.strip() for h in rows[0]]
    return {h: i for i, h in enumerate(hdr)}, rows[3:]

def f(v):
    try: return float(v)
    except Exception: return float("nan")

P("="*118); P("ITEM 29 -- fast bars: R = R_corotation/R_bar in TWO independent Tremaine-Weinberg samples (MaNGA, then CALIFA)"); P("="*118)
col3, d3 = read_vizier(os.path.join(BD, "geron2023_manga_barspeeds_table3.tsv"))
col1, d1 = read_vizier(os.path.join(BD, "geron2023_manga_bars_table1.tsv"))
t1 = {r[col1["MANGA"]].strip(): r for r in d1}
rec = []
for r in d3:
    nm = r[col3["MANGA"]].strip()
    R, Rl, Ru = f(r[col3["R"]]), f(r[col3["e_R"]]), f(r[col3["E_R"]])
    if not all(np.isfinite([R, Rl, Ru])) or Rl <= 0: continue
    e = t1.get(nm)
    rec.append(dict(name=nm, R=R, Rl=Rl, Ru=Ru, Om=f(r[col3["Omph"]]), Rcr=f(r[col3["Rcrph"]]),
                    typ=(e[col1["BarType"]].strip() if e else ""), Rbar=(f(e[col1["Rbardp"]]) if e else float("nan"))))
info(f"Geron+2023 table 3: {len(d3)} rows, {len(rec)} with a finite R and positive published bounds; "
     f"{sum(1 for x in rec if x['typ']=='Strong bar')} strong bars, {sum(1 for x in rec if x['typ']=='Weak bar')} weak")
R = np.array([x["R"] for x in rec]); Rl = np.array([x["Rl"] for x in rec]); Ru = np.array([x["Ru"] for x in rec])
sig = (Ru - Rl)/2.0
info(f"R: median {np.median(R):.3f}, 16-84% [{np.percentile(R,16):.3f}, {np.percentile(R,84):.3f}], max {R.max():.2f}; "
     f"published half-width: median {np.median(sig):.3f} (16-84%: {np.percentile(sig,16):.3f} - {np.percentile(sig,84):.3f})")

# ---------------------------------------------------------------- the raw answer, against the list's own criterion
frac_fast = float(np.mean(R < R_FAST)); frac_ultra = float(np.mean(R < 1.0))
eb = math.sqrt(frac_fast*(1 - frac_fast)/len(R))
n_slow = int((Rl > R_FAST).sum()); n_fast = int((Ru < R_FAST).sum()); n_amb = len(R) - n_slow - n_fast
info(f"raw: {100*frac_fast:.1f} +- {100*eb:.1f} per cent of bars have R < {R_FAST} (the list's criterion is >= 90 per cent); "
     f"{100*frac_ultra:.1f} per cent have R < 1, which is dynamically impossible")
info(f"per-galaxy verdicts from the published bounds: {n_slow} individually SLOW (lower bound above 1.4), "
     f"{n_fast} individually FAST (upper bound below 1.4), {n_amb} undecided")
for t in ("Strong bar", "Weak bar"):
    s = np.array([x["R"] for x in rec if x["typ"] == t])
    if len(s) > 10:
        info(f"   {t:11}: N = {len(s):3d}, median R = {np.median(s):.3f}, {100*np.mean(s < R_FAST):.0f} per cent fast")

# ---------------------------------------------------------------- the answer depends on measurement quality
cRs = float(np.corrcoef(R, sig)[0, 1])
info(f"R is strongly correlated with its OWN published uncertainty: corr(R, sigma) = {cRs:+.3f}, median sigma/R = {np.median(sig/R):.3f}")
info(f"{'error bin':12} {'N':>4} {'median R':>9} {'frac R<1.4':>11} {'frac R<1 (impossible)':>22}")
qbins = [(0.0, 0.2), (0.2, 0.5), (0.5, 1.5), (1.5, 1e9)]
qsum = []
for lo, hi in qbins:
    m = (sig >= lo) & (sig < hi)
    if m.sum() < 5: continue
    qsum.append((lo, hi, int(m.sum()), float(np.median(R[m])), float(np.mean(R[m] < R_FAST)), float(np.mean(R[m] < 1))))
    info(f"{f'{lo:g}-{hi:g}' if hi < 1e8 else f'>{lo:g}':12} {m.sum():4d} {np.median(R[m]):9.3f} {np.mean(R[m]<R_FAST):11.2f} {np.mean(R[m]<1):22.2f}")
best_med, worst_med = qsum[0][3], qsum[-1][3]
best_imp = qsum[0][5]
info(f"the best-measured {qsum[0][2]} bars have a median R of {best_med:.2f} and {100*best_imp:.0f} per cent of them are "
     f"DYNAMICALLY IMPOSSIBLE; the worst-measured {qsum[-1][2]} have a median R of {worst_med:.2f}.  The two ends of the")
info(f"same catalogue give opposite answers, and the end with the smallest error bars is the one that is unphysical.")

# ---------------------------------------------------------------- forward-model deconvolution (and its own audit)
GR = np.linspace(0.2, 8.0, 800); dGR = GR[1] - GR[0]
FAST_LO, FAST_HI, SLOW_HI = 1.0, R_FAST, 6.0
P_FAST = np.where((GR >= FAST_LO) & (GR < FAST_HI), 1.0/(FAST_HI - FAST_LO), 0.0)
P_SLOW = np.where((GR >= FAST_HI) & (GR <= SLOW_HI), 1.0/(SLOW_HI - FAST_HI), 0.0)
def fit(Robs, sg):
    """the prior is linear in f, so per error-scale s the two component likelihoods are built once and f scanned free."""
    fs = np.linspace(0.0, 1.0, 101); ss = np.geomspace(0.1, 3.0, 40)
    LL = np.empty((len(fs), len(ss)))
    with np.errstate(all="ignore"):
        for j, s in enumerate(ss):
            sgm = np.maximum(s*sg, 1e-3)[:, None]
            K = np.exp(-0.5*((Robs[:, None] - GR[None, :])/sgm)**2)/(math.sqrt(2*math.pi)*sgm)
            A = K @ P_FAST*dGR; B = K @ P_SLOW*dGR
            for i, a in enumerate(fs):
                LL[i, j] = float(np.sum(np.log(np.maximum((1 - a)*A + a*B, 1e-300))))
    i, j = np.unravel_index(np.nanargmax(LL), LL.shape)
    prof = np.nanmax(LL, axis=1); prof -= prof.max()
    lo = fs[np.argmax(prof > -0.5)]; hi = fs[len(fs) - 1 - np.argmax(prof[::-1] > -0.5)]
    return fs[i], ss[j], lo, hi, prof, fs
fhat, shat, flo, fhi, prof, fs = fit(R, sig)
info(f"maximum likelihood: intrinsic slow fraction f = {fhat:.2f} (profile 1-sigma [{flo:.2f}, {fhi:.2f}]) with a global "
     f"error-scale factor s = {shat:.2f}; f = 1 is disfavoured by Delta log L = {prof[-1]:.0f}")

# --- posterior predictive check on that same best fit: does it reproduce the data it was fitted to?
def ppc(ftrue, s, n=400):
    p = (1 - ftrue)*P_FAST + ftrue*P_SLOW; p = p/p.sum()
    o1, o14, om = [], [], []
    for _ in range(n):
        Rt = rng.choice(GR, size=len(sig), p=p); Ro = Rt + rng.normal(0, s*sig)
        o1.append(np.mean(Ro < 1)); o14.append(np.mean(Ro < R_FAST)); om.append(np.median(Ro))
    return (np.mean(o1), np.std(o1)), (np.mean(o14), np.std(o14)), (np.mean(om), np.std(om))
(a1, e1), (a14, e14), (am, em) = ppc(fhat, shat)
z1 = (frac_ultra - a1)/max(e1, 1e-6); zm = (np.median(R) - am)/max(em, 1e-6)
info(f"POSTERIOR PREDICTIVE CHECK of that best fit: it predicts {100*a1:.1f} +- {100*e1:.1f} per cent unphysical R < 1 against "
     f"the observed {100*frac_ultra:.1f} ({z1:+.1f} sigma), and a median R of {am:.2f} +- {em:.2f} against the observed "
     f"{np.median(R):.2f} ({zm:+.1f} sigma)")
ppc_ok = abs(z1) < 3 and abs(zm) < 3
info("so the Gaussian-error deconvolution does NOT reproduce the data it was fitted to.  Its maximum-likelihood f is an")
info("artefact of the R-sigma correlation -- objects with large R also carry large error bars, so the fit is free to call")
info("them badly-measured fast bars, while paying nothing for the unphysical tail it then predicts and the data do not show.")
info("The ML value is recorded but MUST NOT be quoted as the intrinsic slow fraction.")

# ---------------------------------------------------------------- mutation control: injection and recovery
def synth(ftrue, sg, s_true):
    p = (1 - ftrue)*P_FAST + ftrue*P_SLOW; p = p/p.sum()
    return rng.choice(GR, size=len(sg), p=p) + rng.normal(0, s_true*sg)
inj = []
for ftrue in (0.0, 0.3, 0.7):
    got = [fit(synth(ftrue, sig, shat), sig)[0] for _ in range(10)]
    inj.append((ftrue, float(np.mean(got)), float(np.std(got))))
    info(f"INJECTION f_true = {ftrue:.1f} -> recovered {np.mean(got):.2f} +- {np.std(got):.2f} over 10 synthetic samples")
ck("29a MUTATION CONTROL (injection/recovery): the deconvolution is unbiased under its own assumptions -- synthetic samples "
   "with a known slow fraction, built with the real per-galaxy uncertainties, come back with that fraction.  The estimator is "
   "therefore not the thing that is broken, which is what makes its predictive failure above a statement about the published "
   "error model",
   all(abs(a - b) < 0.2 for a, b, _ in inj),
   "; ".join(f"f_true {a:.1f} -> {b:.2f} +- {c:.2f}" for a, b, c in inj))

# ---------------------------------------------------------------- the systematic that decides it
k90 = float(np.percentile(R, 90)/R_FAST); k50 = float(np.median(R)/R_FAST)
info(f"the one systematic that moves every point the same way is the adopted bar length, since R scales as 1/R_bar: for 90 per "
     f"cent of this sample to be fast, bar radii would have to be UNDERestimated by a factor {k90:.2f}; for the median bar, "
     f"by {k50:.2f}.  Conversely the {100*frac_ultra:.0f} per cent with R < 1 require bar radii OVERestimated for those objects.")
info("Cuomo et al. (2021, A&A 649, A30) reached the same conclusion for the 'ultrafast' bars in the CALIFA Tremaine-Weinberg")
info("samples: they are a bar-length measurement problem.  The same systematic is free to move the slow tail the other way.")

# ================================================================================================================
# SECOND ARM, added on the audit pass: an INDEPENDENT catalogue, and the bar-length systematic MEASURED not assumed
# ================================================================================================================
# The first version of this script rested on one catalogue with one bar-length definition and said so in check 29d.
# Two public tables fix that, both transcribed from the arXiv LaTeX sources into real_research/data/bars/:
#   * the CALIFA Tremaine-Weinberg series (Aguerri+2015 Table 4, 15 strong bars x 4 TW variants; Cuomo+2019
#     Table 3, 16 weak bars) -- a different survey, different instrument, different bar-length method;
#   * Cuomo+2021 Table A.1 -- the SAME galaxy and the SAME corotation radius divided by SEVEN different published
#     bar-radius estimates, which turns "the bar length could be wrong by a factor k" from an assumption into a
#     measurement of how much k actually varies between the definitions people use.
info("")
info("-"*114)
info("SECOND ARM: an independent catalogue (CALIFA TW) and the bar-length systematic measured on real galaxies")
info("-"*114)
cal = [l.rstrip("\n").split("\t") for l in open(os.path.join(BD, "califa_tw_rotation_rates.tsv")) if l.strip() and not l.startswith("#")]
ch = {h.strip(): i for i, h in enumerate(cal[0])}
crow = [dict(paper=r[ch["paper"]], gal=r[ch["galaxy"]], typ=r[ch["bartype"]], var=r[ch["R_variant"]],
             R=f(r[ch["R"]]), lo=f(r[ch["eR_lo"]]), hi=f(r[ch["eR_hi"]])) for r in cal[1:]]
# one number per GALAXY: the median over the TW variants a paper publishes for it (papers 1 and 2 both give R directly)
cg = {}
for r in crow: cg.setdefault(r["gal"], []).append(r)
Rc = np.array([np.median([x["R"] for x in v]) for v in cg.values()])
sc = np.array([np.median([0.5*(x["lo"] + x["hi"]) for x in v]) for v in cg.values()])
n_sb = sum(1 for v in cg.values() if v[0]["typ"] == "SB")
info(f"CALIFA TW: {len(cg)} galaxies ({n_sb} strong bars from Aguerri+2015, {len(cg)-n_sb} weak bars from Cuomo+2019), "
     f"median R = {np.median(Rc):.3f}, 16-84% [{np.percentile(Rc,16):.2f}, {np.percentile(Rc,84):.2f}]")
fc = float(np.mean(Rc < R_FAST)); fc1 = float(np.mean(Rc < 1.0))
ec = math.sqrt(fc*(1 - fc)/len(Rc))
info(f"CALIFA: {100*fc:.1f} +- {100*ec:.1f} per cent have R < {R_FAST} -- the hunt list's >= 90 per cent criterion is MET here; "
     f"{100*fc1:.0f} per cent have R < 1, which is again dynamically impossible")
info(f"MaNGA  : {100*frac_fast:.1f} +- {100*eb:.1f} per cent (N = {len(R)}); CALIFA: {100*fc:.1f} +- {100*ec:.1f} per cent (N = {len(Rc)})")
zcat = (fc - frac_fast)/math.sqrt(ec**2 + eb**2)
info(f"the two catalogues differ in fast fraction by {100*(fc-frac_fast):+.0f} percentage points, i.e. {zcat:+.1f} sigma on "
     f"their own sampling errors alone.  They cannot both be measuring the same population with the same estimator.")
info(f"and the same quality trend appears INSIDE CALIFA, independently: Aguerri+2015 print <R> = 1.2 (+0.7/-0.5) for their "
     f"full 32-galaxy TW compilation and <R> = 1.0 (+0.3/-0.3) for the 23 with uncertainties under 30 per cent -- better "
     f"measurements again give SMALLER R, the same direction as the MaNGA error-bin table above.")

# --- the bar-length systematic, measured: one corotation radius, seven published bar radii
cu = [l.rstrip("\n").split("\t") for l in open(os.path.join(BD, "cuomo2021_barlength_systematic.tsv")) if l.strip() and not l.startswith("#")]
uh = {h.strip(): i for i, h in enumerate(cu[0])}
cols = [f"R{i}" for i in range(1, 8)]
spread, per_gal = [], []
for r in cu[1:]:
    v = np.array([f(r[uh[c]]) for c in cols]); v = v[np.isfinite(v)]
    if len(v) >= 3:
        spread.append(v.max()/v.min()); per_gal.append((r[uh["galaxy"]], len(v), float(v.min()), float(v.max())))
spread = np.array(spread)
allR = np.concatenate([[f(r[uh[c]]) for c in cols] for r in cu[1:]]); allR = allR[np.isfinite(allR)]
between = np.array([np.nanmedian([f(r[uh[c]]) for c in cols]) for r in cu[1:]])
w_dex = float(np.mean([np.std(np.log10(np.array([f(r[uh[c]]) for c in cols])[np.isfinite([f(r[uh[c]]) for c in cols])]), ddof=1)
                       for r in cu[1:]]))
b_dex = float(np.std(np.log10(between), ddof=1))
info("")
info(f"Cuomo+2021 Table A.1 + Table 2: {len(per_gal)} galaxies, each with ONE TW corotation radius divided by up to seven "
     f"published bar radii.  Within a single galaxy, R spans a factor of {np.median(spread):.2f} in the median "
     f"(16-84%: {np.percentile(spread,16):.2f} - {np.percentile(spread,84):.2f}, max {spread.max():.2f}).")
info(f"  WITHIN-galaxy scatter from the bar-length definition alone: {w_dex:.3f} dex.  BETWEEN-galaxy scatter of the same "
     f"galaxies' median R: {b_dex:.3f} dex.  The definitional systematic is {w_dex/b_dex:.1f}x the real galaxy-to-galaxy "
     f"signal, so at this precision the bar-length choice, not the galaxy, sets R.")
info(f"  and for scale: making 90 per cent of the MaNGA sample fast needs the bar radii there to be low by a factor "
     f"{k90:.2f} -- INSIDE the factor {np.median(spread):.2f} that the published definitions already disagree by on the "
     f"same galaxies.  The systematic that would flip the item is not hypothetical; it is the size of a routine "
     f"methodological choice.")
ck("29e SECOND ARM, and it does not rescue the item -- it dissolves it.  An independent Tremaine-Weinberg catalogue (CALIFA) "
   "MEETS the hunt list's >= 90 per cent criterion while MaNGA misses it by a factor of three, a difference far larger than "
   "either sample's own error, and Cuomo+2021 show that one galaxy's R moves by about a factor of two depending only on which "
   "published bar-radius definition is used -- as large as the factor that would flip the MaNGA answer",
   abs(zcat) < 3.0,
   f"CALIFA {100*fc:.0f} per cent fast (N = {len(Rc)}) vs MaNGA {100*frac_fast:.0f} per cent (N = {len(R)}), {zcat:+.1f} sigma "
   f"apart; within-galaxy bar-length spread in R = x{np.median(spread):.2f} ({w_dex:.3f} dex) against a between-galaxy "
   f"{b_dex:.3f} dex; the flip factor is x{k90:.2f}")
ck("29f AGAINST INTEREST, and this is the one that stops the CALIFA arm being banked as a win: the catalogue that DOES satisfy "
   "the framework's criterion satisfies it partly by putting a large share of its bars at R < 1, i.e. corotation inside the "
   "bar, which is not a fast bar but an impossible one.  A framework cannot claim credit for agreement produced by "
   "measurements that are themselves unphysical",
   fc1 < 0.10,
   f"CALIFA: {100*fc1:.0f} per cent of {len(Rc)} galaxies have R < 1 (MaNGA: {100*frac_ultra:.0f} per cent); Cuomo+2021 was "
   f"written specifically to explain those objects and concluded they are a bar-length measurement problem, which is the "
   f"same systematic that would be needed to move MaNGA's slow tail")

# ---------------------------------------------------------------- context: where bars sit in acceleration
om = np.array([x["Om"] for x in rec]); rcr = np.array([x["Rcr"] for x in rec])
m = np.isfinite(om) & np.isfinite(rcr) & (rcr > 0)
gcr = (om[m]*1e3/kpc)**2*(rcr[m]*kpc)                     # Omega^2 R = v_c^2/R at corotation, SI
for foot in ("canonical", "alt"):
    info(f"context [{foot}]: the acceleration at corotation is {np.median(gcr)/A0[foot]:.2f} a_0 "
         f"(16-84%: {np.percentile(gcr,16)/A0[foot]:.2f} - {np.percentile(gcr,84)/A0[foot]:.2f}) -- bars sit right at the "
         f"transition, but R is dimensionless and no a_0 enters it")

# ---------------------------------------------------------------- verdicts
ck("29 (NOT DECIDABLE ON THIS CATALOGUE, and reported that way rather than as a kill) at face value the Kepler-grade condition "
   "FAILS badly -- only a third of MaNGA bars have R < 1.4 and 79 are individually slow at their published bounds -- but the "
   "same catalogue puts its BEST-MEASURED bars at a median R of 0.99 with half of them dynamically impossible.  The answer "
   "flips with measurement quality, so the sample cannot settle the item either way",
   frac_fast >= 0.90,
   f"{100*frac_fast:.1f} +- {100*eb:.1f} per cent fast (N = {len(R)}), median R = {np.median(R):.3f}; best-measured "
   f"{qsum[0][2]} bars median {best_med:.2f} ({100*best_imp:.0f} per cent impossible), worst-measured {qsum[-1][2]} median "
   f"{worst_med:.2f}; corr(R, sigma) = {cRs:+.2f}")
ck("29b MY OWN DECONVOLUTION FAILED ITS OWN PREDICTIVE CHECK and is withdrawn, not quoted: the maximum-likelihood fit prefers "
   "all bars intrinsically fast, but when that best fit is asked to regenerate the data it predicts a large unphysical tail "
   "that is not there and a median R far below the observed one",
   ppc_ok,
   f"ML f = {fhat:.2f}, s = {shat:.2f}; predicted unphysical fraction {100*a1:.1f} +- {100*e1:.1f} per cent vs observed "
   f"{100*frac_ultra:.1f} ({z1:+.1f} sigma); predicted median {am:.2f} vs observed {np.median(R):.2f} ({zm:+.1f} sigma)")
ck("29c AGAINST INTEREST, the internal inconsistency that dominates everything: {:.0f} per cent of the whole sample, and "
   "{:.0f} per cent of the twenty best-measured bars, have corotation INSIDE the bar, which cannot happen.  A catalogue whose "
   "cleanest measurements are unphysical cannot be used to count how many bars are slow, and this is stated rather than "
   "trimmed away".format(100*frac_ultra, 100*best_imp),
   True,
   f"{100*frac_ultra:.1f} per cent of {len(R)} have R < 1; among the {qsum[0][2]} with sigma < 0.2 it is {100*best_imp:.0f} per cent")
ck("29d AGAINST INTEREST, the item's own limitation, which no amount of extra data removes: R is dimensionless, a_0 never "
   "enters and both footings give identical numbers, so this item can never measure a_0 or separate the footings -- it can "
   "only test halo dynamical friction, and it does that through a quantity whose value is set by a bar-length convention",
   True,
   f"bar radii would need to be low by x{k90:.2f} for 90 per cent fast, x{k50:.2f} for the median; corotation sits at "
   f"{np.median(gcr)/A0['canonical']:.2f} a_0 (canonical) / {np.median(gcr)/A0['alt']:.2f} a_0 (alt); "
   f"every number above is identical on both footings")
sys.exit(ck.done())
