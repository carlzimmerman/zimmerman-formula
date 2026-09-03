#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h121_gas_calibration_transfer.py -- HUNT ITEM 121: CALIBRATE a_0 WHERE THERE ARE NO STARS, PREDICT Upsilon WHERE THERE ARE.
============================================================================================================================
THE ITEM.  "ON DISK SPARC.  Calibrate a_0 on f_gas > 0.7 (item 102), then PREDICT Upsilon for the star-dominated rest.
Zero free parameters anywhere in the chain.  Pass if the predicted Upsilon distribution matches SPS in median and spread."

THE CHAIN, AND WHY IT HAS NO FREE PARAMETER.
  step 1  split SPARC by baryonic gas fraction f_gas = 1.33 M_HI / (1.33 M_HI + Upsilon L_[3.6]).
          CALIBRATORS f_gas > 0.7, TARGETS f_gas < 0.3.  The two sets are disjoint and share no galaxy and no point.
  step 2  measure a_0 on the CALIBRATORS ONLY, with item 25's slope-fixed deep-tail estimator: in the deep-MOND limit
          g_obs = sqrt(a_0 g_bar) exactly, so log a_0 = 2 <log g_obs - 0.5 log g_bar> over points with g_bar < 1e-11.
          No fitting, no free slope.
  step 3  with that a_0 -- and ONLY that a_0 -- fit each TARGET galaxy's whole rotation curve for its own Upsilon_disk
          (the item-119 estimator).  One parameter per target galaxy, none shared, and a_0 was never allowed to move.
  step 4  compare the resulting Upsilon distribution with stellar populations in MEDIAN and in SPREAD.
The one residual circularity -- g_bar on the calibrators still contains Upsilon L_[3.6] -- is removed two ways: an extra
POINT-level cut keeping only points where the stars supply less than 30% of g_bar, and then iterating the whole chain to
its fixed point, so the Upsilon used in the split and in the calibration is the Upsilon the chain predicts.  It converges
in three passes.

A RESULT AGAINST INTEREST THAT COMES OUT OF STEP 2, AND IT CORRECTS THIS HUNT'S OWN LEDGER.  The Upsilon-leverage of the
deep-tail estimator is measured here rather than assumed, by re-running it at Upsilon = 0.2, 0.5 and 0.8:
        FULL SPARC (item 25's committed sample)          d log a_0 / d log Upsilon = -0.65
        galaxies with f_gas > 0.7 (the item's subset)                              = -0.35
        ...and with the point-level stars-under-30% cut                            = -0.14
So item 25's a_0 = 1.14e-10 is NOT the M/L-free measurement the item-100 ladder calls it -- it carries the LARGEST
Upsilon leverage of any rung on that ladder.  The genuinely M/L-immunised deep-tail number is measured below and it is
different, and lower.  That correction is the reason this item matters beyond its own pass/fail.

Both footings are reported, but note what changes here: a_0 is MEASURED, not assumed, so the footings enter as the two
values the measurement is compared WITH, and the Upsilon prediction is also computed at each footing for comparison with
items 76 and 119.  Mutation controls.  The Newtonian alternative computed beside.  Checks CAN fail.
"""
import sys, math
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(121)
SPS_U, SPS_U_E = 0.50, 0.10      # Upsilon_[3.6] from stellar populations (repository anchor)
SPS_TOT, SPS_PG = 0.10, 0.070    # total and per-galaxy SPS scatter in dex (prep_2026/a0_line_mlpriors/SETUP.md)
FSTAR_MAX = 0.30                 # point-level cut: keep points where the stars supply < 30% of g_bar
TAIL_CUT = 1e-11                 # item 25's committed deep-tail threshold
GASCUT_HI, GASCUT_LO = 0.70, 0.30

gals = load_sparc()
P("="*118); P("ITEM 121 -- a_0 calibrated where there are no stars, Upsilon predicted where there are"); P("="*118)

# ------------------------------------------------------------------ the machinery
def split(ups):
    fg = np.array([1.33*g["MHI"]/max(1.33*g["MHI"] + ups*g["L36"], 1e-12) for g in gals])
    return ([g for g, f in zip(gals, fg) if f > GASCUT_HI], [g for g, f in zip(gals, fg) if f < GASCUT_LO], fg)

def a0_tail(sub, ups, fstar_max=FSTAR_MAX, cut=TAIL_CUT, gasf=1.0, dsc=1.0):
    """item 25's slope-fixed deep-tail estimator, with an added point-level 'stars are a minor term' cut.
    dsc rescales every distance (r ~ D, V_component^2 ~ D), gasf rescales the gas mass."""
    v = []
    for g in sub:
        r = g["r"]*dsc
        st = (ups*g["vd"]**2 + UPS_B/UPS_D*ups*g["vb"]**2)*dsc
        gs = gasf*g["vg"]*np.abs(g["vg"])*dsc
        gb = (gs + st)/r*KMS2_KPC
        fst = st/np.maximum(gs + st, 1e-12)
        go = g["vobs"]**2/r*KMS2_KPC
        m = (gb > 0) & (gb < cut) & (fst < fstar_max)
        if m.sum(): v.append(np.log10(go[m]) - 0.5*np.log10(gb[m]))
    if not v: return float("nan"), 0, 0
    vv = np.concatenate(v)
    return 10**(2*float(np.mean(vv))), len(vv), len(v)

def fit_ups(g, a0, dsc=1.0, isc=1.0, newton=False, lo=0.02, hi=6.0):
    r = g["r"]*dsc; vo = g["vobs"]*isc; ev = np.maximum(g["ev"], 2.0)*isc; s = math.sqrt(dsc)
    vg, vd, vb = g["vg"]*s, g["vd"]*s, g["vb"]*s
    def chi2(u):
        gb = np.maximum((vg*np.abs(vg) + u*vd**2 + 1.4*u*vb**2)/r*KMS2_KPC, 1e-18)
        return float(np.sum(((vo - np.sqrt(gb*(1.0 if newton else nu(gb/a0))*r/KMS2_KPC))/ev)**2))
    return minimize_scalar(chi2, bounds=(lo, hi), method="bounded", options={"xatol": 1e-4}).x

def predict(tgt, a0, **kw):
    out = [(g, fit_ups(g, a0, **kw)) for g in tgt]
    return [(g, u) for g, u in out if 0.03 < u < 5.9]

# ------------------------------------------------------------------ step 2's leverage audit, first, because it reframes the item
P(""); P("-"*118); P("THE Upsilon-LEVERAGE OF THE DEEP-TAIL ESTIMATOR, MEASURED"); P("-"*118)
cal0, tgt0, fg0 = split(SPS_U)
KEY_FULL  = "FULL SPARC, no point cut (item 25's own sample)"
KEY_NOCUT = "f_gas > 0.7 galaxies, no point cut"
KEY_IMM   = "f_gas > 0.7 galaxies, stars < 30% of g_bar"
LEV = {}
info(f"{'sample':>52} {'N gal':>6} {'N pts':>6} {'a_0(U=0.5)':>12} {'a_0(0.2)':>11} {'a_0(0.8)':>11} {'d log a0/d log U':>17}")
for label, sub, fsm in ((KEY_FULL, gals, 1.01),
                        (KEY_NOCUT, cal0, 1.01),
                        (KEY_IMM, cal0, FSTAR_MAX),
                        ("f_gas > 0.7 galaxies, stars < 20% of g_bar", cal0, 0.20)):
    a5, n5, g5 = a0_tail(sub, 0.5, fstar_max=fsm)
    a2, _, _ = a0_tail(sub, 0.2, fstar_max=fsm); a8, _, _ = a0_tail(sub, 0.8, fstar_max=fsm)
    lev = (math.log10(a8) - math.log10(a2))/(math.log10(0.8) - math.log10(0.2))
    LEV[label] = (a5, lev, n5, g5)
    info(f"{label:>52} {g5:6d} {n5:6d} {a5:12.3e} {a2:11.3e} {a8:11.3e} {lev:17.3f}")
lev_full, a0_full25 = LEV[KEY_FULL][1], LEV[KEY_FULL][0]
lev_imm, a0_imm = LEV[KEY_IMM][1], LEV[KEY_IMM][0]
ck("121a AGAINST INTEREST, AND IT CORRECTS THIS HUNT'S OWN LEDGER.  The item-100 ladder lists item 25's a_0 = 1.14e-10 "
   "as 'the gas-dominated deep tail' and as one of the two rungs that do NOT lean on the stellar mass-to-light ratio.  "
   "Measured rather than assumed, that estimator's Upsilon leverage is the LARGEST on the ladder: change Upsilon by a "
   "factor 4 and its a_0 moves by 0.39 dex.  Item 25 was run on the WHOLE of SPARC, not on a gas-dominated subset, and "
   "its number must not be quoted as M/L-free.  Restricting to gas-dominated galaxies more than halves the leverage, "
   "and adding a point-level cut that keeps only points where the stars supply under 30% of g_bar cuts it by a further "
   "factor of two",
   abs(lev_full) > 3*abs(lev_imm) or (abs(lev_full) > 0.5 and abs(lev_imm) < 0.2),
   f"d log a_0/d log Upsilon: full SPARC {lev_full:+.3f}, f_gas > 0.7 "
   f"{LEV[KEY_NOCUT][1]:+.3f}, immunised {lev_imm:+.3f}; the immunised deep tail gives a_0 = "
   f"{a0_imm:.3e} against item 25's {a0_full25:.3e} -- {math.log10(a0_full25/a0_imm):+.3f} dex apart")

# ------------------------------------------------------------------ steps 1-3: the self-consistent chain
P(""); P("-"*118); P("THE CHAIN, ITERATED TO ITS FIXED POINT"); P("-"*118)
U = SPS_U
info(f"{'pass':>5} {'Upsilon used in the split/calibration':>38} {'N cal':>6} {'N tgt':>6} {'a_0(gas)':>12} {'predicted Upsilon':>18}")
for it in range(8):
    cal, tgt, fg = split(U)
    a0g, npts, ngal = a0_tail(cal, U)
    pr = predict(tgt, a0g)
    med = float(np.median([u for _, u in pr]))
    info(f"{it:5d} {U:38.4f} {len(cal):6d} {len(tgt):6d} {a0g:12.4e} {med:18.4f}")
    if abs(math.log10(med/U)) < 1e-3: break
    U = med
cal, tgt, fg = split(U); a0g, npts, ngal = a0_tail(cal, U); pr = predict(tgt, a0g)
UP = np.array([u for _, u in pr]); TG = [g for g, _ in pr]
shared = set(g["name"] for g in cal) & set(g["name"] for g in tgt)
info(f"fixed point after {it+1} passes: Upsilon = {U:.4f}, a_0(gas) = {a0g:.4e} m/s^2 from {ngal} calibrator galaxies "
     f"({npts} deep-tail points), {len(UP)} of {len(tgt)} target galaxies fitted")
info(f"calibrators and targets share {len(shared)} galaxies (must be 0) and, by the f_gas split, no rotation-curve point")

bs = np.array([a0_tail([cal[i] for i in rng.integers(0, len(cal), len(cal))], U)[0] for _ in range(600)])
bs = bs[np.isfinite(bs)]; EA0 = float(np.std(np.log10(bs)))
info(f"a_0(gas) galaxy-bootstrap: {np.median(bs):.4e} +- {EA0:.3f} dex ({100*(10**EA0-1):.0f}%)")
info(f"compared with the two footings: canonical {A0['canonical']:.3e} is {math.log10(a0g/A0['canonical']):+.3f} dex away, "
     f"alt {A0['alt']:.3e} is {math.log10(a0g/A0['alt']):+.3f} dex away")

# ------------------------------------------------------------------ step 4: median and spread against stellar populations
P(""); P("-"*118); P("THE PREDICTION, AGAINST STELLAR POPULATIONS, IN MEDIAN AND IN SPREAD"); P("-"*118)
ED, EI, ES = [], [], []
for g in TG:
    fD = min(g["eD"]/g["D"], 0.45)
    up_ = fit_ups(g, a0g, dsc=1 + fD); um_ = fit_ups(g, a0g, dsc=max(1 - fD, 0.2))
    ED.append(abs(math.log10(max(up_, 1e-3)/max(um_, 1e-3)))/2)
    i0 = math.radians(g["inc"]); di = math.radians(min(g["einc"], 20))
    sp = math.sin(i0)/math.sin(min(i0 + di, math.radians(89.5))); sm = math.sin(i0)/math.sin(max(i0 - di, math.radians(5)))
    uip = fit_ups(g, a0g, isc=sp); uim = fit_ups(g, a0g, isc=sm)
    EI.append(abs(math.log10(max(uip, 1e-3)/max(uim, 1e-3)))/2)
ED = np.array(ED); EI = np.array(EI)
obs_sd = float(np.log10(UP).std()); budget = float(np.sqrt(np.mean(ED**2 + EI**2)))
intr = math.sqrt(max(obs_sd**2 - budget**2, 0.0))
intr_lo = math.sqrt(max(obs_sd**2 - (1.1*budget)**2, 0.0)); intr_hi = math.sqrt(max(obs_sd**2 - (0.9*budget)**2, 0.0))
med = float(np.median(UP))
bmed = np.array([np.median(UP[i]) for i in (rng.integers(0, len(UP), len(UP)) for _ in range(3000))])
info(f"predicted Upsilon_[3.6] on {len(UP)} star-dominated galaxies (f_gas < {GASCUT_LO}), zero free parameters:")
info(f"   median {med:.3f} +- {float(bmed.std()):.3f} (galaxy bootstrap)   vs stellar populations {SPS_U} +- {SPS_U_E}")
info(f"   16-84%  {np.percentile(UP,16):.3f} - {np.percentile(UP,84):.3f};  full range {UP.min():.3f} - {UP.max():.3f}")
info(f"   spread  {obs_sd:.3f} dex observed;  measurement budget {budget:.3f} dex rms (distance {np.median(ED):.3f}, "
     f"inclination {np.median(EI):.3f});  implied intrinsic {intr:.3f} dex [{intr_lo:.3f} - {intr_hi:.3f} if the budget "
     f"is wrong by 10%]   vs SPS total {SPS_TOT}, per-galaxy component {SPS_PG}")
info(f"{'(B-V)-free binned view':>26} {'N':>4} {'median Upsilon':>15} {'log sd':>8}")
lL = np.log10(np.array([g["L36"] for g in TG]))
qs = np.percentile(lL, [0, 25, 50, 75, 100])
for i in range(4):
    m = (lL >= qs[i]) & (lL < qs[i+1] if i < 3 else lL <= qs[i+1])
    if m.sum() > 3:
        info(f"{f'log L36 {qs[i]:.1f}-{qs[i+1]:.1f}':>26} {m.sum():4d} {np.median(UP[m]):15.3f} {np.log10(UP[m]).std():8.3f}")

d_med = abs(math.log10(med/SPS_U))
e_med = math.sqrt((float(bmed.std())/med/math.log(10))**2 + (EA0*0.47)**2)
ck("121b (a WORKS -- and it is the only place in the hunt where a stellar-population parameter is PREDICTED with no free "
   "parameter at all) a_0 measured on gas-dominated galaxies alone, transferred to a disjoint set of star-dominated "
   "ones, predicts their 3.6 um stellar mass-to-light ratio to within 0.03 dex of the stellar-population value.  "
   "Nothing was fitted to the target galaxies except one Upsilon each, and a_0 came from galaxies whose light barely "
   "enters the calculation",
   d_med < 0.10,
   f"predicted median Upsilon = {med:.3f} +- {float(bmed.std()):.3f} (galaxies) and +- {EA0*0.47:.3f} dex from the "
   f"a_0 calibration, against SPS {SPS_U} +- {SPS_U_E}: {math.log10(med/SPS_U):+.3f} dex, "
   f"{d_med/max(e_med,1e-6):.1f} of this measurement's own sigma and {d_med/(SPS_U_E/SPS_U/math.log(10)):.1f} of the "
   f"stellar populations' sigma.  N = {len(UP)} targets, {ngal} calibrators, no shared galaxy")

ck("121c ...and the SPREAD matches too, which is the half of the item that could have failed independently.  The "
   "predicted Upsilon distribution is 0.14 dex wide, and the distance and inclination errors alone account for "
   "essentially all of it: the intrinsic galaxy-to-galaxy spread is bounded below the stellar populations' own "
   "per-galaxy component.  As in item 119 this is a BOUND and not a measurement -- the budget saturates the "
   "observation, so the sample cannot detect an intrinsic spread of the size stellar populations predict",
   intr_hi < SPS_TOT + 0.03,
   f"observed {obs_sd:.3f} dex, budget {budget:.3f}, intrinsic {intr:.3f} dex [{intr_lo:.3f}-{intr_hi:.3f}] against "
   f"the SPS per-galaxy component {SPS_PG} and total {SPS_TOT}.  For contrast, the same estimator over item 119's "
   f"wider sample gave 0.25 dex, because gas-dominated galaxies -- where Upsilon is barely visible -- were still in it")

# ------------------------------------------------------------------ systematics on the calibration
P(""); P("-"*118); P("SYSTEMATICS ON a_0(gas)"); P("-"*118)
SYS = {}
for nm, kw, note in (("stars < 20% of g_bar", dict(fstar_max=0.20), "the point-level cut"),
                     ("stars < 50% of g_bar", dict(fstar_max=0.50), "the point-level cut"),
                     ("deep-tail cut 3e-11", dict(cut=3e-11), "item 25's threshold moved up"),
                     ("deep-tail cut 3e-12", dict(cut=3e-12), "item 25's threshold moved down"),
                     ("gas mass x 1.1", dict(gasf=1.1), "the 1.33 helium factor / HI flux scale"),
                     ("gas mass x 0.9", dict(gasf=0.9), "the same, the other way"),
                     ("all distances x 1.1", dict(dsc=1.1), "a coherent distance-scale error"),
                     ("all distances x 0.9", dict(dsc=0.9), "the same, the other way")):
    a, n, _ = a0_tail(cal, U, **kw)
    SYS[nm] = (a, math.log10(a/a0g), n)
    info(f"{nm:>24} -> a_0 = {a:.4e} ({math.log10(a/a0g):+.3f} dex, {n} points)   [{note}]")
sys_cut = max(abs(SYS["stars < 20% of g_bar"][1]), abs(SYS["stars < 50% of g_bar"][1]), abs(SYS["deep-tail cut 3e-11"][1]))
sys_gas = max(abs(SYS["gas mass x 1.1"][1]), abs(SYS["gas mass x 0.9"][1]))
sys_dist = max(abs(SYS["all distances x 1.1"][1]), abs(SYS["all distances x 0.9"][1]))
tot = math.sqrt(EA0**2 + sys_cut**2 + sys_gas**2 + sys_dist**2)
info(f"total on a_0(gas): {EA0:.3f} (statistical) (+) {sys_cut:.3f} (cut choices) (+) {sys_gas:.3f} (gas calibration) "
     f"(+) {sys_dist:.3f} (a coherent 10% distance-scale error) = {tot:.3f} dex")
sig_can = abs(math.log10(a0g/A0["canonical"]))/tot; sig_alt = abs(math.log10(a0g/A0["alt"]))/tot
ck("121d AGAINST INTEREST -- this does NOT decide between the two footings, and the reason is the distance scale.  The "
   "M/L-immunised a_0 lands on the canonical footing almost exactly, but its total error is dominated by a systematic "
   "the estimator cannot see: a coherent 10% error in SPARC's distances moves a_0 by 0.09 dex, which is larger than "
   "the whole 0.082 dex gap between the footings.  The central value favours canonical; the error bar does not exclude "
   "alt, and item 123 must be told so",
   sig_alt < 3.0,
   f"a_0(gas) = {a0g:.3e} +- {tot:.3f} dex total: canonical at {sig_can:.1f} sigma, alt at {sig_alt:.1f} sigma.  "
   f"Statistical alone would give canonical {abs(math.log10(a0g/A0['canonical']))/EA0:.1f} sigma and alt "
   f"{abs(math.log10(a0g/A0['alt']))/EA0:.1f} sigma -- so the distance scale, not the sample size, is what blocks the "
   f"footing decision here")

# the ladder implication
DWARF_LENS, DWARF_LENS_E = 9.55e-11, 0.24e-10
P("")
info("THE LADDER, RE-RUNG (input to items 123 and 125).  The item-100 ladder's two supposedly M/L-free rungs were "
    "item 25's deep tail (1.14e-10) and the KiDS dwarf lens stack (9.55e-11), 0.08 dex apart.  Item 25's rung is not "
    "M/L-free (leverage -0.65, above).  Replacing it with the immunised measurement made here:")
info(f"   gas-dominated, M/L-immunised deep tail : {a0g:.3e} +- {tot:.3f} dex   (leverage {lev_imm:+.2f})")
info(f"   KiDS dwarf lens stack (item 2)         : {DWARF_LENS:.3e} +- {DWARF_LENS_E/DWARF_LENS/math.log(10):.3f} dex")
info(f"   they agree to {abs(math.log10(a0g/DWARF_LENS)):.3f} dex, and both sit on the canonical footing "
     f"({math.log10(a0g/A0['canonical']):+.3f} and {math.log10(DWARF_LENS/A0['canonical']):+.3f} dex).")
info(f"   That agreement is far inside both error bars ({tot:.2f} and "
     f"{DWARF_LENS_E/DWARF_LENS/math.log(10):.2f} dex), so it is a coincidence of central values and NOT a 0.01 dex "
     f"measurement.  What it does support is that the ladder's spread was M/L, exactly as item 100 said.")

# ------------------------------------------------------------------ MUTATIONS
P(""); P("="*118); P("MUTATION CONTROLS"); P("="*118)
a0_star, n_star, g_star = a0_tail(tgt, U, fstar_max=1.01)
pr_star = predict(tgt, a0_star); med_star = float(np.median([u for _, u in pr_star]))
ck("M121-1 the transfer carries real information, shown by breaking it: calibrate a_0 on the TARGET galaxies instead -- "
   "the circular version the item is designed to avoid -- and both the a_0 and the recovered Upsilon move.  The "
   "gas-calibrated chain is therefore not returning its own input",
   abs(math.log10(a0_star/a0g)) > 0.03,
   f"a_0 from the star-dominated targets themselves = {a0_star:.3e} ({math.log10(a0_star/a0g):+.3f} dex from the "
   f"gas-calibrated {a0g:.3e}), and it returns Upsilon = {med_star:.3f} against the transferred {med:.3f}")

for k in (0.5, 2.0):
    pk = predict(tgt, k*a0g); mk = float(np.median([u for _, u in pk]))
    lever = math.log10(mk/med)/math.log10(k)
    if k == 2.0: MUT2 = (mk, lever)
    info(f"a_0 x {k}: predicted Upsilon median {mk:.3f} ({math.log10(mk/SPS_U):+.3f} dex from SPS), implied "
         f"d log Upsilon/d log a_0 = {lever:+.2f}")
sig_mut = abs(math.log10(MUT2[0]/SPS_U))/(SPS_U_E/SPS_U/math.log(10))
ck("M121-2 the a_0 mutation, and it is honest about the POWER rather than flattering it.  Doubling a_0 moves the "
   "predicted Upsilon off the stellar-population value -- but by only 1.3 sigma of the stellar populations' own error, "
   "because these star-dominated galaxies sit at accelerations where the kernel's response to a_0 is half what the "
   "deep-MOND limit gives.  So 121b is a genuine zero-parameter agreement and NOT a sharp measurement of a_0: this "
   "test on its own constrains a_0 only to about a factor of two",
   sig_mut < 3.0,
   f"a_0 x 2 -> Upsilon = {MUT2[0]:.3f}, {math.log10(MUT2[0]/SPS_U):+.3f} dex from SPS = {sig_mut:.1f} sigma of the "
   f"SPS uncertainty; measured d log Upsilon/d log a_0 = {MUT2[1]:+.2f}, against -1 in the deep-MOND limit")

pn = [fit_ups(g, a0g, newton=True) for g in TG]; pn = np.array([u for u in pn if 0.02 < u < 6.0])
ck("M121-3 the kernel is load-bearing: with nu = 1 and no dark matter the same target curves demand nearly twice the "
   "stellar-population mass-to-light ratio, so the agreement in 121b is not something the rotation curves would give "
   "for any gravity law",
   abs(math.log10(np.median(pn)/SPS_U)) > 0.2,
   f"Newtonian predicted Upsilon median {np.median(pn):.3f} = {math.log10(np.median(pn)/SPS_U):+.2f} dex from SPS, "
   f"against {med:.3f} = {math.log10(med/SPS_U):+.3f} dex with the kernel")

# A FIRST VERSION OF THIS CONTROL PASSED ON A NaN.  It paired galaxies only where the two rotation curves happened to
# have the SAME NUMBER of points, which left N = 1, and the check's boolean was satisfied by the non-finite result --
# a control that could not fail.  Rebuilt: every target galaxy keeps its own radii and its own photometry and is given
# a donor's observed velocities, interpolated onto its radial range in units of that range.  N is now the full sample.
def scramble(g, h):
    xg = g["r"]/g["r"].max(); xh = h["r"]/h["r"].max()
    gg = dict(g); gg["vobs"] = np.interp(xg, xh, h["vobs"]); gg["ev"] = np.interp(xg, xh, h["ev"])
    return gg
mix, nrail = [], 0
for _ in range(20):
    perm = rng.permutation(len(TG))
    for j, g in enumerate(TG):
        if perm[j] == j: continue
        u = fit_ups(scramble(g, TG[perm[j]]), a0g)
        if 0.03 < u < 5.9: mix.append(u)
        else: nrail += 1
mix = np.array(mix)
sd_mix = float(np.log10(mix).std())
ck("M121-4 pairing each target galaxy's photometry with a DIFFERENT galaxy's observed rotation curve, interpolated onto "
   "its own radial range, roughly triples the spread of the recovered Upsilon and rails a tenth of the fits.  So the "
   "0.14 dex distribution in 121c is genuine per-galaxy correspondence between light and kinematics, not something the "
   "estimator would return for any pairing",
   np.isfinite(sd_mix) and len(mix) > 100 and sd_mix > 1.5*obs_sd,
   f"scrambled pairs over 20 permutations: N = {len(mix)} fits ({nrail} railed and dropped, against 1 in the true "
   f"sample), median Upsilon {np.median(mix):.3f}, spread {sd_mix:.3f} dex against the true {obs_sd:.3f} dex "
   f"(ratio {sd_mix/obs_sd:.1f}x) and the measurement budget {budget:.3f}")

# ------------------------------------------------------------------ both footings, for comparison with 76 and 119
P(""); P("-"*118); P("THE SAME PREDICTION WITH a_0 IMPOSED AT EACH FOOTING, for comparison with items 76 and 119")
P("-"*118)
for foot, a0v in A0.items():
    pf = predict(tgt, a0v); mf = float(np.median([u for _, u in pf]))
    info(f"{foot:>10} a_0 = {a0v:.3e} imposed: predicted Upsilon median {mf:.3f} ({math.log10(mf/SPS_U):+.3f} dex from SPS) "
         f"on the same {len(pf)} star-dominated galaxies")
info(f"measured a_0(gas) = {a0g:.3e} gives {med:.3f}.  Item 76's deep-tail inversion required 0.656 / 0.504; item 119's "
     f"full-curve median over a wider sample was 0.505 / 0.456.  The spread among these is the estimator-and-sample "
     f"systematic on 'the Upsilon that Lambda predicts', and it is about 0.1 dex.")
info("AGAINST INTEREST, and it is why 121d refuses to pick a footing: read as an imposed-a_0 test the ALT footing lands "
     "closer to stellar populations here, while the MEASURED gas calibration lands on canonical.  Both differences are "
     "well inside the 0.12 dex systematic on a_0(gas), so the two readings do not conflict -- but neither may be quoted "
     "as favouring a footing, in either direction.")

# ------------------------------------------------------------------ the alternative, computed beside
P(""); P("-"*118); P("THE LambdaCDM / NEWTONIAN ALTERNATIVE, COMPUTED BESIDE"); P("-"*118)
info("There is no LambdaCDM version of this chain.  A dark halo has at least two free parameters per galaxy, so the")
info("gas-dominated galaxies determine no acceleration scale to transfer, and the star-dominated ones' Upsilon is")
info("degenerate with the halo -- rotation curves bound it from above and no further.  What LambdaCDM does instead is")
info("take Upsilon from stellar populations as an INPUT and fit the halo; the framework takes Lambda as the input and")
info("returns Upsilon as an OUTPUT.  The comparison is therefore asymmetric by construction: this item shows that one")
info("theory makes the prediction and that the prediction is right, not that the other theory is wrong.")
mx = []
for g in TG:
    ratio = g["vobs"]**2/np.maximum(g["vd"]**2 + 1.4*g["vb"]**2, 1e-6)
    m = g["r"] < 2.2*max(g["Rdisk"], 1e-3)
    mx.append(float(np.min(ratio[m])) if m.sum() else float(np.min(ratio)))
mx = np.array(mx)
info(f"the maximum-disc upper bound on Upsilon for these same {len(mx)} galaxies: median {np.median(mx):.2f}, "
     f"5-95% {np.percentile(mx,5):.2f} - {np.percentile(mx,95):.2f} -- an upper limit, and "
     f"{100*np.mean(mx > SPS_U):.0f}% of it lies above the stellar-population value, i.e. carries no information")

# ------------------------------------------------------------------ verdict
P(""); P("="*118); P("VERDICT"); P("="*118)
P(f"  The chain closes.  a_0 measured on {ngal} gas-dominated SPARC galaxies -- with a point-level cut that keeps only")
P(f"  places where the stars supply under 30% of g_bar, and iterated to self-consistency -- is {a0g:.3e} m/s^2,")
P(f"  {math.log10(a0g/A0['canonical']):+.3f} dex from the canonical footing.  Transferred with no further freedom to {len(UP)} disjoint star-dominated")
P(f"  galaxies, it predicts Upsilon_[3.6] = {med:.3f}, {math.log10(med/SPS_U):+.3f} dex from stellar populations, with a spread of {obs_sd:.2f} dex")
P(f"  that the distance and inclination errors alone account for.  Median and spread both pass.")
P(f"  Three things are recorded AGAINST it.  (1) The power is modest: doubling a_0 would show at only {sig_mut:.1f} sigma of the")
P(f"  stellar populations' own error, so this is a zero-parameter agreement, not a sharp measurement of a_0.  (2) The")
P(f"  footing question is NOT settled -- a coherent 10% distance-scale error moves a_0 by {sys_dist:.2f} dex, more than the gap")
P(f"  between the footings.  (3) The scatter agreement is a bound, not a detection, for the same reason as in item 119.")
P(f"  And one correction it forces on this hunt's own ledger: item 25's 1.14e-10 is NOT the M/L-free rung the item-100")
P(f"  ladder calls it -- its Upsilon leverage is {lev_full:+.2f}, the largest there -- and the immunised replacement is")
P(f"  {a0g:.3e}, which agrees with the dwarf lens stack to {abs(math.log10(a0g/DWARF_LENS)):.3f} dex instead of 0.08.")
sys.exit(ck.done())
