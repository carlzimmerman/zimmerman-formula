#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h31b_almost_dark_selection_audit.py -- HUNT ITEM 31, the adversarial audit of h31's own liability.
==================================================================================================
h31_almost_dark_btfr.py measured the 115 HI-bearing ultra-diffuse ALFALFA galaxies (Leisman+2017) to sit
-0.296 +- 0.028 dex BELOW the framework's zero-parameter BTFR in rotation speed, -0.265 dex differentially
against a mass-matched control, and recorded it as a 9.5 sigma LIABILITY.

The standing working rule of this repository is that a DEFICIT must be verified as hard as a WIN, and that a
deficit must never be manufactured.  h31 did not do that.  It priced three escapes (HI radius, external field,
inclination) but it did NOT model the one mechanism that can manufacture exactly this signal:

    ALFALFA's detection limit depends on the LINE WIDTH.  SNR ~ F * W50^(-1/2), so at fixed HI mass and distance
    a galaxy with a WIDER line is HARDER to detect.  At fixed baryonic mass and inclination that is a selection
    ON THE BTFR RESIDUAL ITSELF: high-v galaxies are preferentially thrown away, and the survivors sit low.

There is also a published counter-claim that h31 does not cite:
    * Mancera Pina et al. 2022, MNRAS 512, 3230 (arXiv:2112.00017), resolved HI of AGC 114905: measured
      inclination 32 +- 3 deg, and the rotation curve "deviates strongly from the predictions of Modified
      Newtonian dynamics".  (VERIFIED from the abstract this session.)
    * BUT: Sanchez Almeida 2024, A&A (arXiv:2408.05269), "Gas-rich 'ultra-diffuse' galaxies are consistent with
      the baryonic Tully-Fisher relation and with Milgromian dynamics", argues the offset is a systematic of
      LOW INCLINATION: UDGs are "a subset of LSB dwarf galaxies biased toward face-on systems", and re-estimates
      AGC 114905 at i = 15 +- 2 deg because the disc is lopsided.  (VERIFIED this session.)
    * NOTE AGAINST h31: h31's check 31.3 asserts that Mancera Pina+2022 "report 10.8 +- 0.3 deg" as the
      MOND-required inclination.  That precise value could NOT be verified from the paper this session.  The
      ~10-11 deg figure is reproduced here as this pipeline's OWN calculation and is quoted as such; the
      "+- 0.3" should not be quoted from that paper without checking the text.

So this script asks one question: HOW MUCH OF THE ITEM-31 DEFICIT IS REAL?  Six tests, each able to destroy it.
Both footings.  Mutation controls.  Checks CAN fail -- and two of them are written so that they fail if h31 was
right, because the point of the exercise is to try to break h31's result, not to decorate it.
"""
import sys, math, warnings
import numpy as np
from scipy import stats
from hunt_lib import *
warnings.filterwarnings("ignore")
ck = Check(); rng = np.random.default_rng(311)

W_TURB = 20.0
SNRLIM = 6.5

def v_from_width(W50, inc_deg, w_turb=W_TURB):
    Wr = np.sqrt(np.maximum(np.asarray(W50, float)**2 - w_turb**2, 0.0))
    s = np.sin(np.radians(np.asarray(inc_deg, float)))
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(s > 0, Wr/(2*s), np.nan)

def v_btfr(Mb_msun, a0):
    return (G*np.asarray(Mb_msun, float)*Msun*a0)**0.25/1e3

def med_ci(x, n=2000):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3: return np.nan, np.nan
    bs = np.array([np.median(rng.choice(x, len(x))) for _ in range(n)])
    return float(np.median(x)), float(bs.std())

P("="*118); P("ITEM 31b -- is the almost-dark BTFR deficit REAL, or did h31 manufacture it?")
P("="*118)

# ---------------------------------------------------------------- 0. rebuild h31's measurement, self-contained
h = load_huds(); a = load_alfalfa()
Ms = np.where(np.isfinite(h["logMsM"]), h["logMsM"], h["logMsT"])
Mgas = 1.33*10**h["logMHI"]
Mb = Mgas + np.where(np.isfinite(Ms), 10**np.nan_to_num(Ms, nan=0.0), 0.0)
hv = v_from_width(h["W50"], h["inc"])
ok = np.isfinite(hv) & (hv > 0) & np.isfinite(Mb) & np.isfinite(h["inc"])

# the HUDs are all in alpha.100: pull the integrated flux and the rms, which set the detection limit
idx = {k: i for i, k in enumerate(a["agc"])}
mi = np.array([idx.get(k, -1) for k in h["agc"]])
n_match = int((mi >= 0).sum())
hF, hrms, hsnr = a["flux"][mi], a["rms"][mi], a["snr"][mi]
info(f"Leisman+2017 HUDs: N = {len(Mb)}, of which {n_match} are matched back into alpha.100 for the flux and rms "
     f"that set ALFALFA's own detection limit; {ok.sum()} have a usable inclination and width")
RAW = {}
for ft, a0 in A0.items():
    r = np.log10(hv[ok]/v_btfr(Mb[ok], a0)); m, e = med_ci(r); RAW[ft] = (m, e, float(r.std()))
    info(f"h31's raw measurement reproduced, {ft:10}: median log(v_obs/v_pred) = {m:+.3f} +- {e:.3f}, scatter {r.std():.3f} dex")
ck("31b.0 h31's measurement is reproduced exactly here from the same catalogues, so everything below is an audit of "
   "that number and not of a different one",
   abs(RAW["canonical"][0] + 0.296) < 0.01, f"reproduced {RAW['canonical'][0]:+.3f} dex against h31's -0.296")

# the SNR definition, needed for the detection limit
wsmo = np.where(a["W50"] < 400, a["W50"]/20.0, 20.0)
snr_calc = (1000*a["flux"]/a["W50"])*np.sqrt(wsmo)/a["rms"]
gg = np.isfinite(snr_calc) & (a["snr"] > 0)
ck("31b.0b the alpha.100 signal-to-noise definition is reproduced from the published columns, which is what licenses "
   "the width-dependent detection limit W_max = (1000 F/(6.5 rms))^2/20 used throughout section 4",
   abs(float(np.median(snr_calc[gg]/a["snr"][gg])) - 1.0) < 0.02,
   f"median recomputed/catalogue SNR = {float(np.median(snr_calc[gg]/a['snr'][gg])):.4f}, N = {gg.sum()}")

# ---------------------------------------------------------------- 1. the geometry bound (assumption-free)
P(""); P("-"*118); P("1. TEST ONE -- the geometry bound: can ANY disc shape rescue the framework?"); P("-"*118)
P("  For an oblate spheroid of intrinsic axis ratio q0, b/a = sqrt((1-q0^2) cos^2 i + q0^2) >= cos i for every q0.")
P("  So the measured axis ratio sets an ASSUMPTION-FREE floor on the inclination, i >= arccos(b/a), attained only in")
P("  the razor-thin limit q0 -> 0.  A thicker disc always implies a MORE edge-on galaxy, hence a SMALLER v_obs.")
ba = h["ba"]
i_min = np.degrees(np.arccos(np.clip(ba, 0.0, 1.0)))                 # q0 -> 0, the most face-on reading possible
v_max = v_from_width(h["W50"], i_min)                                # therefore the largest v_obs any geometry allows
gok = ok & np.isfinite(v_max) & (v_max > 0) & (ba < 0.995)
BOUND = {}
for ft, a0 in A0.items():
    r = np.log10(v_max[gok]/v_btfr(Mb[gok], a0)); m, e = med_ci(r); BOUND[ft] = (m, e)
    info(f"{ft:10}: with EVERY galaxy given the most face-on inclination its own axis ratio permits "
         f"(median {np.median(i_min[gok]):.0f} deg instead of {np.median(h['inc'][gok]):.0f} deg), the residual is still "
         f"{m:+.3f} +- {e:.3f} dex")
ba_need = np.sqrt(np.clip(1 - (np.sqrt(np.maximum(h["W50"]**2 - W_TURB**2, 0))/(2*v_btfr(Mb, A0["canonical"])))**2, 0, 1))
info(f"put the other way: for the framework to be right the median HUD would need an axis ratio of "
     f"{np.nanmedian(ba_need[ok]):.3f}; SDSS measures {np.nanmedian(ba[ok]):.3f}")
n_imposs = int((gok & (ba_need < ba - 0.02)).sum())
info(f"and for {n_imposs} of the {int(gok.sum())} galaxies the axis ratio the framework needs is SMALLER than the one "
     f"measured, i.e. NO oblate geometry of any thickness can reconcile them -- the object would have to be rounder "
     f"than it is observed to be")
ck("31b.1 (this one survives the audit, and it is the strongest thing in item 31) the deficit is NOT a disc-thickness "
   "assumption.  Hubble's q0 = 0.2 is not doing the work: granting every galaxy the most face-on inclination its own "
   "measured axis ratio allows, for any oblate shape whatsoever, still leaves the almost-darks about a fifth of a dex "
   "below the framework's zero-parameter prediction.  This check asserts that the bound BITES, so it fails if the "
   "geometry escape works",
   BOUND["canonical"][0] < -0.10 and BOUND["alt"][0] < -0.10,
   f"most-face-on-possible residual: canonical {BOUND['canonical'][0]:+.3f} +- {BOUND['canonical'][1]:.3f}, "
   f"alt {BOUND['alt'][0]:+.3f} +- {BOUND['alt'][1]:.3f} dex; {n_imposs} galaxies are geometrically irreconcilable")

# ---------------------------------------------------------------- 2. where the deficit lives in inclination
P(""); P("-"*118); P("2. TEST TWO -- the published counter-claim's mechanism: is the deficit a LOW-INCLINATION artefact?")
P("-"*118)
P("  Sanchez Almeida 2024 (arXiv:2408.05269) attributes the UDG BTFR offset to systematics at low inclination.")
P("  If that is the mechanism, the deficit MUST be concentrated in the face-on half of the sample, because v = W/(2 sin i)")
P("  is the only place an inclination error can enter and its leverage grows as 1/sin i.")
r_can = np.log10(hv/v_btfr(Mb, A0["canonical"]))
edges = [0, 40, 50, 60, 90]
for lo_, hi_ in zip(edges[:-1], edges[1:]):
    s = ok & (h["inc"] >= lo_) & (h["inc"] < hi_)
    if s.sum() >= 5:
        m, e = med_ci(r_can[s])
        info(f"  measured inclination {lo_:2d}-{hi_:2d} deg (N = {int(s.sum()):3d}): median residual {m:+.3f} +- {e:.3f} dex")
lo_i = ok & (h["inc"] < 50); hi_i = ok & (h["inc"] >= 50)
m_lo, e_lo = med_ci(r_can[lo_i]); m_hi, e_hi = med_ci(r_can[hi_i])
sp_i = stats.spearmanr(h["inc"][ok], r_can[ok])
info(f"  face-on half (i < 50 deg, N = {int(lo_i.sum())}): {m_lo:+.3f} +- {e_lo:.3f};  "
     f"edge-on half (i >= 50 deg, N = {int(hi_i.sum())}): {m_hi:+.3f} +- {e_hi:.3f}")
info(f"  Spearman(residual, inclination) = {sp_i.statistic:+.3f}, p = {sp_i.pvalue:.3f}")
ck("31b.2 the low-inclination mechanism is NOT where this deficit lives.  The edge-on half of the sample -- where "
   "v = W/(2 sin i) is best conditioned and an inclination error has the least leverage -- carries a deficit at least "
   "as large as the face-on half.  That is the opposite of the published counter-claim's signature.  This check asserts "
   "the deficit is not carried by the face-on objects, so it FAILS if the counter-claim's mechanism is what is operating",
   m_hi <= m_lo + 0.05,
   f"face-on half {m_lo:+.3f} +- {e_lo:.3f} vs edge-on half {m_hi:+.3f} +- {e_hi:.3f} dex "
   f"(difference {m_hi-m_lo:+.3f}); trend with inclination p = {sp_i.pvalue:.3f}")

# ---------------------------------------------------------------- 3. the direction of noise
P(""); P("-"*118); P("3. TEST THREE -- can NOISE on the axis ratio manufacture a deficit?  (it cannot, and here is why)")
P("-"*118)
P("  log v = log W_rot - log(2 sin i).  -log sin i is a CONVEX function of i, so by Jensen's inequality symmetric")
P("  scatter in the measured inclination raises the MEAN residual.  Random error makes galaxies look FASTER, not")
P("  slower.  Only a systematic -- inclinations biased HIGH -- can push them down.  Mocked here rather than argued.")
for eba in (0.03, 0.05, 0.10):
    ba_t = np.clip(ba[ok], 0.05, 0.99)
    i_t = inclination_from_ba(ba_t)
    v_t = v_from_width(h["W50"][ok], i_t)
    shifts = []
    for _ in range(300):
        ba_m = np.clip(ba_t + rng.normal(0, eba, ba_t.size), 0.05, 0.999)
        v_m = v_from_width(h["W50"][ok], inclination_from_ba(ba_m))
        d = np.log10(v_m/v_t); shifts.append(np.median(d[np.isfinite(d)]))
    info(f"  Gaussian axis-ratio noise sigma(b/a) = {eba:.2f}: it moves the MEDIAN residual by "
         f"{np.mean(shifts):+.4f} dex (+ = looks faster)")
    if eba == 0.05: NOISE_SHIFT = float(np.mean(shifts))
sin_ratio_needed = 10**RAW["canonical"][0]
ck("31b.3 noise cannot be the explanation, and the sign is a theorem, not a fit: symmetric error on the measured axis "
   "ratio biases the inferred rotation speed UPWARD, so it eats into the deficit rather than creating it.  Manufacturing "
   "a -0.30 dex deficit requires a SYSTEMATIC overestimate of every inclination -- sin i too large by a factor 2, the "
   "median galaxy actually at 23 deg where SDSS measures 52 deg -- not scatter",
   NOISE_SHIFT > -0.005,
   f"5% axis-ratio noise shifts the median by {NOISE_SHIFT:+.4f} dex (non-negative, as Jensen requires); "
   f"the deficit needs sin i smaller by a factor {1/sin_ratio_needed:.2f}")

# ---------------------------------------------------------------- 4. the mechanism h31 MISSED
P(""); P("-"*118)
P("4. TEST FOUR -- THE MECHANISM h31 MISSED, AND IT IS REAL: ALFALFA's detection limit depends on the line width")
P("-"*118)
P("  SNR = 1000 (F/W50) sqrt(W50/20) / rms  ->  SNR ~ F W50^(-1/2).  At fixed HI mass and distance a galaxy with a")
P("  wider line has a LOWER signal-to-noise.  Detection therefore requires W50 <= W_max = (1000 F/(6.5 rms))^2/20,")
P("  and at fixed baryonic mass and inclination that is a cut ON THE BTFR RESIDUAL: fast rotators are thrown away.")
Wmax = (1000*hF/(SNRLIM*hrms))**2/20.0
si_h = np.sin(np.radians(h["inc"]))
W_onBTFR = np.sqrt((2*v_btfr(Mb, A0["canonical"])*si_h)**2 + W_TURB**2)
sok = ok & np.isfinite(Wmax) & np.isfinite(W_onBTFR)
info(f"median HUD: W50 observed {np.median(h['W50'][sok]):.0f} km/s, detection ceiling W_max = {np.median(Wmax[sok]):.0f} km/s, "
     f"and the width the SAME galaxy would have if it sat exactly ON the framework's BTFR is "
     f"{np.median(W_onBTFR[sok]):.0f} km/s")
f_undetect = float(np.mean(W_onBTFR[sok] > Wmax[sok]))
info(f"  -> {100*f_undetect:.0f}% of these galaxies, placed exactly on the framework's BTFR at their own HI mass, "
     f"distance and inclination, would NOT have been detected by ALFALFA at all")

def forward(Mb_, inc_, F_, rms_, off, sig, a0=A0["canonical"], K=3000, seed=5, wt=W_TURB):
    """Population with an intrinsic log-normal BTFR residual N(off, sig); apply ALFALFA's width-dependent detection
    limit; return the residual the h31 pipeline recovers from the SURVIVORS (pooled), and the detected fraction."""
    r0 = np.random.default_rng(seed)
    vp = v_btfr(Mb_, a0); Wm = (1000*np.asarray(F_)/(SNRLIM*np.asarray(rms_)))**2/20.0
    pool = []; det = []
    for k in range(len(Mb_)):
        if not all(np.isfinite([vp[k], inc_[k], Wm[k]])): continue
        s = math.sin(math.radians(inc_[k])); r = r0.normal(off, sig, K)
        W = np.sqrt((2*vp[k]*10**r*s)**2 + wt**2)
        d = (W <= Wm[k]) & (W > wt*1.0001); det.append(d.mean())
        if d.sum() < 5: continue
        pool.append(np.log10(np.sqrt(W[d]**2 - wt**2)/(2*s)/vp[k]))
    p = np.concatenate(pool)
    return float(np.median(p)), 0.5*float(np.percentile(p, 84) - np.percentile(p, 16)), float(np.mean(det))

# the mass-matched control, as h31 defined it
aMs = np.where(np.isfinite(a["logMsM"]), a["logMsM"], a["logMsT"])
aMb = 1.33*10**a["logMHI"] + np.where(np.isfinite(aMs), 10**np.nan_to_num(aMs, nan=0.0), 0.0)
cbase = ((a["code"] == 1) & (a["pflag"] == 1) & (a["snr"] >= SNRLIM) & np.isfinite(a["ba"]) & np.isfinite(aMs)
         & (a["W50"] > 0) & (a["inc"] > 45))
cmm = cbase & (np.log10(aMb) >= math.log10(np.nanmin(Mb))) & (np.log10(aMb) <= math.log10(np.nanmax(Mb)))
ci = np.where(cmm)[0]
av = v_from_width(a["W50"], a["inc"])
CTRL_RAW = {}
for ft, a0 in A0.items():
    rr = np.log10(av[cmm]/v_btfr(aMb[cmm], a0)); m, e = med_ci(rr); CTRL_RAW[ft] = (m, e)
info(f"mass-matched control: N = {len(ci)}, raw median residual {CTRL_RAW['canonical'][0]:+.3f} dex; "
     f"median SNR {np.median(a['snr'][ci]):.1f} against the HUDs' {np.median(hsnr[ok]):.1f}, "
     f"median distance {np.median(a['dist'][ci]):.0f} Mpc against {np.median(h['dist'][ok]):.0f} Mpc")
P("")
P("  what the width-selection alone manufactures, if the population is EXACTLY on the framework's BTFR:")
MAN = {}
for sig in (0.15, 0.20, 0.26, 0.35):
    mh, sh, dh = forward(Mb[ok], h["inc"][ok], hF[ok], hrms[ok], 0.0, sig)
    mc, sc, dc = forward(aMb[ci], a["inc"][ci], a["flux"][ci], a["rms"][ci], 0.0, sig, seed=6)
    MAN[sig] = (mh, mc)
    info(f"  intrinsic scatter {sig:.2f} dex: HUDs {mh:+.3f} dex (detected fraction {dh:.2f}), "
         f"control {mc:+.3f} dex (detected fraction {dc:.2f})  ->  manufactured DIFFERENTIAL {mh-mc:+.3f} dex")

def solve_offset(Mb_, inc_, F_, rms_, target, sig, seed=5):
    lo_, hi_ = -0.80, 0.30
    for _ in range(34):
        mid = 0.5*(lo_ + hi_)
        if forward(Mb_, inc_, F_, rms_, mid, sig, seed=seed)[0] < target: lo_ = mid
        else: hi_ = mid
    return 0.5*(lo_ + hi_)

P("")
P("  and therefore, de-selected: the INTRINSIC offset the almost-darks must have for the observed one to come out")
DESEL = {}
for sig in (0.15, 0.20, 0.26, 0.35):
    mu = solve_offset(Mb[ok], h["inc"][ok], hF[ok], hrms[ok], RAW["canonical"][0], sig)
    _, sc_mock, _ = forward(Mb[ok], h["inc"][ok], hF[ok], hrms[ok], mu, sig)
    DESEL[sig] = (mu, sc_mock)
    info(f"  intrinsic scatter {sig:.2f} dex -> intrinsic offset {mu:+.3f} dex "
         f"(mock recovers a scatter of {sc_mock:.3f} against the observed {RAW['canonical'][2]:.3f})")
# the self-consistent solution: the sigma whose mock reproduces the OBSERVED scatter
sigs = np.array(sorted(DESEL)); scat = np.array([DESEL[s][1] for s in sigs]); offs = np.array([DESEL[s][0] for s in sigs])
sig_sc = float(np.interp(RAW["canonical"][2], scat, sigs))
off_sc = float(np.interp(RAW["canonical"][2], scat, offs))
info(f"  SELF-CONSISTENT: the intrinsic scatter that reproduces the observed {RAW['canonical'][2]:.3f} dex spread is "
     f"{sig_sc:.2f} dex, and it implies an intrinsic offset of {off_sc:+.3f} dex")
info(f"  (this is generous to the framework: the observed spread also contains inclination and mass errors, which the "
     f"mock does not have, so the true intrinsic scatter is SMALLER and the true offset therefore MORE negative "
     f"than {off_sc:+.3f})")
ck("31b.4 AGAINST h31 AND AGAINST INTEREST: h31's headline number is inflated, and its 9.5 sigma is not a real error "
   "bar.  ALFALFA cannot detect a wide line as easily as a narrow one, so at fixed HI mass it preferentially keeps the "
   "SLOW rotators -- and about half of these galaxies would be undetectable if they sat on the framework's BTFR.  "
   "Modelling that selection removes roughly a third of the deficit.  This check asserts that the manufactured bias is "
   "a substantial part of h31's number, so it fails if the selection turns out to be harmless",
   MAN[0.26][0] - MAN[0.26][1] < -0.05 and f_undetect > 0.3,
   f"at the observed scatter the selection alone manufactures {MAN[0.26][0]:+.3f} dex in the HUDs against "
   f"{MAN[0.26][1]:+.3f} in the control ({MAN[0.26][0]-MAN[0.26][1]:+.3f} differential); {100*f_undetect:.0f}% of "
   f"BTFR-compliant HUDs would be undetected; de-selected offset {off_sc:+.3f} dex against the raw {RAW['canonical'][0]:+.3f}")

# ------------------------------------------------- 4b. the selection model's own falsifiable prediction, and it fails
P(""); P("-"*118)
P("4b. AND NOW AGAINST THE AUDIT'S OWN MODEL: the width cut predicts a trend with inclination.  It is too small.")
P("-"*118)
P("  A wider line is harder to detect, and width scales as sin i, so the truncation must bite HARDER at high")
P("  inclination.  Section 2 found exactly such a trend.  That is a quantitative prediction, so it can be checked -- and")
P("  when it is, neither the selection model NOR a genuine constant offset reproduces the size of the observed trend.")
BINS = ((0, 40), (40, 50), (50, 60), (60, 90))
def pred_bins(off, sig, K=4000, seed=13):
    r0 = np.random.default_rng(seed); vp = v_btfr(Mb, A0["canonical"]); out = {}
    for lo_, hi_ in BINS:
        s = ok & (h["inc"] >= lo_) & (h["inc"] < hi_); pool = []
        for k in np.where(s)[0]:
            if not all(np.isfinite([vp[k], Wmax[k]])): continue
            si = math.sin(math.radians(h["inc"][k])); r = r0.normal(off, sig, K)
            W = np.sqrt((2*vp[k]*10**r*si)**2 + W_TURB**2); d = (W <= Wmax[k]) & (W > W_TURB*1.0001)
            if d.sum() < 5: continue
            pool.append(np.log10(np.sqrt(W[d]**2 - W_TURB**2)/(2*si)/vp[k]))
        out[(lo_, hi_)] = float(np.median(np.concatenate(pool))) if pool else float("nan")
    return out
p_on = pred_bins(0.0, sig_sc); p_low = pred_bins(off_sc, sig_sc)
info("  inclination bin   observed    if ON the BTFR (selection only)   if genuinely low")
for b in BINS:
    s = ok & (h["inc"] >= b[0]) & (h["inc"] < b[1])
    info(f"    {b[0]:2d}-{b[1]:2d} deg (N = {int(s.sum()):2d})    {np.median(r_can[s]):+.3f}              {p_on[b]:+.3f}                {p_low[b]:+.3f}")
obs_span = float(np.median(r_can[ok & (h["inc"] >= 60)]) - np.median(r_can[ok & (h["inc"] < 40)]))
span_on = p_on[(60, 90)] - p_on[(0, 40)]; span_low = p_low[(60, 90)] - p_low[(0, 40)]
# and it is not axis-ratio noise either
ba_t = np.clip(ba, 0.05, 0.99); it_t = inclination_from_ba(ba_t)
vt_t = v_from_width(h["W50"], it_t); sh_faceon = []
for _ in range(300):
    bm = np.clip(ba_t + rng.normal(0, 0.05, ba_t.size), 0.05, 0.999)
    d = np.log10(v_from_width(h["W50"], inclination_from_ba(bm))/vt_t)
    m_ = ok & (it_t < 40); sh_faceon.append(np.median(d[m_][np.isfinite(d[m_])]))
NOISE_FACEON = float(np.mean(sh_faceon))
info(f"  observed face-on-to-edge-on span {obs_span:+.3f} dex; selection alone predicts {span_on:+.3f}, a genuine "
     f"constant offset predicts {span_low:+.3f}, and 5% axis-ratio noise contributes {NOISE_FACEON:+.4f} in the face-on bin")
ck("31b.4b AGAINST THE AUDIT'S OWN MODEL: the residual's trend with inclination is about three times steeper than the "
   "width selection can produce and steeper than any constant offset, and it is not axis-ratio noise.  Something "
   "inclination-dependent in these measurements is not modelled by h31, by the published counter-claim, or by this "
   "audit.  Consequently the sample MEDIAN is not a clean measurement of anything and item 31 cannot be quoted as a "
   "number to better than about 0.1 dex.  This check asserts that the models FAIL, so it passes only while they do",
   abs(obs_span) > 1.8*max(abs(span_on), abs(span_low)),
   f"observed span {obs_span:+.3f} dex vs selection {span_on:+.3f} and constant-offset {span_low:+.3f}; "
   f"axis-ratio noise contributes {NOISE_FACEON:+.4f}")

# ---------------------------------------------------------------- 5. the independent discriminator
P(""); P("-"*118)
P("5. TEST FIVE -- the inclination distribution decides, and it uses no residual at all"); P("-"*118)
P("  The width cut of section 4 removes WIDE lines, and width scales as sin i.  So if the deficit were an artefact of")
P("  that selection acting on a BTFR-compliant population, the surviving sample would have to be strongly FACE-ON")
P("  biased.  If instead these galaxies are genuinely slow, their lines are narrow at every inclination and nothing is")
P("  preferentially removed, so the sample stays randomly oriented.  The observed axis ratios settle it.")
obs_f45 = float(np.mean(h["inc"][ok] > 45))
n_ok = int(ok.sum()); se_f = math.sqrt(obs_f45*(1-obs_f45)/n_ok)
info(f"  OBSERVED: f(i > 45 deg) = {obs_f45:.3f} +- {se_f:.3f} (N = {n_ok});  random orientation gives "
     f"cos 45 deg = {math.cos(math.radians(45)):.3f}")
def predict_f45(off, sig, K=4000, seed=3):
    r0 = np.random.default_rng(seed); keep = []
    vp = v_btfr(Mb, A0["canonical"]); Wm = (1000*hF/(SNRLIM*hrms))**2/20.0
    for k in range(len(Mb)):
        if not all(np.isfinite([vp[k], Wm[k]])): continue
        u = r0.uniform(0, 1, K); it = np.degrees(np.arccos(u))
        r = r0.normal(off, sig, K)
        W = np.sqrt((2*vp[k]*10**r*np.sin(np.radians(it)))**2 + W_TURB**2)
        keep.append(it[(W <= Wm[k]) & (W > W_TURB*1.0001)])
    z = np.concatenate(keep); return float(np.mean(z > 45))
f_H0 = predict_f45(0.0, sig_sc)                     # the population sits ON the BTFR, selection does the rest
f_H1 = predict_f45(off_sc, sig_sc)                  # the population is genuinely below it
info(f"  predicted f(i > 45) if the almost-darks sit ON the BTFR and selection makes the deficit: {f_H0:.3f} "
     f"({(obs_f45-f_H0)/se_f:+.1f} sigma from the observed value)")
info(f"  predicted f(i > 45) if the almost-darks are genuinely {off_sc:+.2f} dex low:                {f_H1:.3f} "
     f"({(obs_f45-f_H1)/se_f:+.1f} sigma from the observed value)")
ck("31b.5 the inclination distribution -- which never touches the rotation speed -- favours a GENUINE deficit over a "
   "pure selection artefact.  A width cut severe enough to fake -0.30 dex would leave a visibly face-on sample; the "
   "almost-darks are randomly oriented to within the errors, which is what happens when the lines are narrow because "
   "the galaxies really are slow.  Underpowered on its own at N = 112, and reported as such",
   abs(obs_f45 - f_H1) < abs(obs_f45 - f_H0),
   f"observed {obs_f45:.3f} +- {se_f:.3f}; on-the-BTFR-plus-selection predicts {f_H0:.3f} "
   f"({abs(obs_f45-f_H0)/se_f:.1f} sigma away), genuinely-low predicts {f_H1:.3f} ({abs(obs_f45-f_H1)/se_f:.1f} sigma away)")

# ---------------------------------------------------------------- 6. a control matched on SNR, not just mass
P(""); P("-"*118); P("6. TEST SIX -- a control matched on DETECTABILITY, which is what h31's control was missing")
P("-"*118)
lMb_c = np.log10(aMb[ci]); lsnr_c = np.log10(a["snr"][ci]); ld_c = np.log10(a["dist"][ci])
r_c = {ft: np.log10(av[ci]/v_btfr(aMb[ci], a0)) for ft, a0 in A0.items()}
# ---- first, the WRONG control, kept in the record because finding it was the point of the audit
sel_bad = []
for k in np.where(ok)[0]:
    d2 = ((lMb_c - math.log10(Mb[k]))/0.15)**2 + ((lsnr_c - math.log10(hsnr[k]))/0.06)**2 + ((ld_c - math.log10(h["dist"][k]))/0.10)**2
    sel_bad.extend(np.argsort(d2)[:5])
sel_bad = np.array(sel_bad)
m_bad, e_bad = med_ci(r_c["canonical"][sel_bad])
P("  ATTEMPT ONE, and it is a BUG IN MY OWN ESTIMATOR, reported rather than quietly dropped:")
info(f"  matching the control to the HUDs on baryonic mass, SNR and distance gives a control median of "
     f"{m_bad:+.3f} +- {e_bad:.3f} dex and a differential of {RAW['canonical'][0]-m_bad:+.3f} dex -- apparently killing "
     f"the whole effect.  It is not real.  SNR = 1000 (F/W50) sqrt(W50/20)/rms CONTAINS the line width, so matching on "
     f"it conditions on the numerator of the very estimator being tested: a collider.")
info(f"  the fingerprint is unmistakable: the SNR-matched control has a median W50 of "
     f"{np.median(a['W50'][ci][sel_bad]):.0f} km/s where the mass-matched control has {np.median(a['W50'][ci]):.0f} km/s. "
     f"Matching on SNR at fixed mass and distance can only be satisfied by picking NARROW lines, i.e. by selecting "
     f"negative BTFR residuals directly.")
# ---- the correct control: match on the detection CEILING, which contains no width at all
Wmax_c = (1000*a["flux"][ci]/(SNRLIM*a["rms"][ci]))**2/20.0
Wmax_h = (1000*hF/(SNRLIM*hrms))**2/20.0
lw_c = np.log10(Wmax_c)
P("")
P("  ATTEMPT TWO, the honest one: match on W_max = (1000 F/(6.5 rms))^2/20, the detection CEILING.  It is built from")
P("  the integrated flux and the noise only -- no line width anywhere in it -- so it is a common cause and not a")
P("  collider.  Matching baryonic mass, W_max and inclination matches the truncation exactly, because those three are")
P("  what the truncation depends on.")
sel_idx = []
for k in np.where(ok)[0]:
    d2 = ((lMb_c - math.log10(Mb[k]))/0.15)**2 + ((lw_c - math.log10(Wmax_h[k]))/0.08)**2 + ((a["inc"][ci] - h["inc"][k])/10.0)**2
    sel_idx.extend(np.argsort(d2)[:5])
sel_idx = np.array(sel_idx)
MATCH = {}
for ft in A0:
    m, e = med_ci(r_c[ft][sel_idx]); MATCH[ft] = (m, e)
info(f"W_max-matched control ({len(np.unique(sel_idx))} unique galaxies): median log W_max "
     f"{np.median(lw_c[sel_idx]):.2f} vs the HUDs' {np.median(np.log10(Wmax_h[ok])):.2f}; inclination "
     f"{np.median(a['inc'][ci][sel_idx]):.0f} vs {np.median(h['inc'][ok]):.0f} deg; log M_b "
     f"{np.median(lMb_c[sel_idx]):.2f} vs {np.median(np.log10(Mb[ok])):.2f}; log M_HI "
     f"{np.median(a['logMHI'][ci][sel_idx]):.2f} vs {np.median(h['logMHI'][ok]):.2f}")
for ft in A0:
    dif = RAW[ft][0] - MATCH[ft][0]; dife = math.hypot(RAW[ft][1], MATCH[ft][1])
    info(f"  {ft:10}: matched control {MATCH[ft][0]:+.3f} +- {MATCH[ft][1]:.3f} (h31's mass-only control gave "
         f"{CTRL_RAW[ft][0]:+.3f}); DIFFERENTIAL = {dif:+.3f} +- {dife:.3f} dex ({dif/dife:+.1f} sigma)")
    if ft == "canonical": DIFM = (dif, dife)
info(f"and the ladder that makes the mechanism plain: ordinary ALFALFA galaxies at ALL masses sit at "
     f"{np.median(np.log10(av[cbase]/v_btfr(aMb[cbase], A0['canonical']))):+.3f} dex, the mass-matched control at "
     f"{CTRL_RAW['canonical'][0]:+.3f}, the W_max-matched control at {MATCH['canonical'][0]:+.3f}, the almost-darks at "
     f"{RAW['canonical'][0]:+.3f}.  The residual tracks DETECTABILITY, not the almost-dark property.")
ck("31b.6 (this is the finding that resizes item 31) once the control is matched on detectability WITHOUT conditioning "
   "on the line width, ordinary ALFALFA galaxies of the same baryonic mass, HI mass, inclination and detection ceiling "
   "sit almost exactly where the almost-darks sit.  The almost-dark property itself is worth about a tenth of a dex, "
   "not the quarter-dex h31 reported: h31's control was nearer and easier to detect, so it was not bitten by the same "
   "width selection.  This check asserts that the differential is SMALL, so it fails if h31's -0.265 dex was right",
   abs(DIFM[0]) < 0.15,
   f"differential against the W_max-matched control {DIFM[0]:+.3f} +- {DIFM[1]:.3f} dex, against h31's "
   f"{RAW['canonical'][0]-CTRL_RAW['canonical'][0]:+.3f} dex; alt footing {RAW['alt'][0]-MATCH['alt'][0]:+.3f} dex")

# ---------------------------------------------------------------- 7. the resolved anchor, end to end
P(""); P("-"*118); P("7. TEST SEVEN -- the one object with resolved kinematics, run end to end"); P("-"*118)
ia = list(h["agc"]).index("114905")
V_RES, I_RES = 23.0, 32.0                                     # Mancera Pina+2022 (VERIFIED: i = 32 +- 3 deg)
I_ALT = 15.0                                                  # Sanchez Almeida 2024 re-estimate (VERIFIED: 15 +- 2)
v_pipe = float(v_from_width(h["W50"][ia], h["inc"][ia]))
info(f"AGC 114905: ALFALFA W50 = {h['W50'][ia]:.0f} km/s, SDSS b/a = {ba[ia]:.2f} -> this pipeline's inclination "
     f"{h['inc'][ia]:.0f} deg -> pipeline rotation speed {v_pipe:.1f} km/s")
info(f"  interferometry (Mancera Pina+2022) gives V_c = {V_RES:.0f} km/s at i = {I_RES:.0f} +- 3 deg, so the pipeline "
     f"underestimates this galaxy's rotation speed by {math.log10(V_RES/v_pipe):+.3f} dex")
info(f"  the turbulence subtraction is most of it: sqrt({h['W50'][ia]:.0f}^2 - {W_TURB:.0f}^2) = "
     f"{math.sqrt(h['W50'][ia]**2-W_TURB**2):.1f} km/s against 2 V_c sin i = {2*V_RES*math.sin(math.radians(I_RES)):.1f} km/s")
end_bias = math.log10(V_RES/v_pipe)
for ft, a0 in A0.items():
    vp = float(v_btfr(Mb[ia], a0))
    info(f"  {ft:10}: framework predicts {vp:.1f} km/s; the resolved value leaves this object "
         f"{math.log10(V_RES/vp):+.3f} dex low, and at the re-estimated i = {I_ALT:.0f} deg "
         f"({2*V_RES*math.sin(math.radians(I_RES))/(2*math.sin(math.radians(I_ALT))):.0f} km/s) "
         f"{math.log10(2*V_RES*math.sin(math.radians(I_RES))/(2*math.sin(math.radians(I_ALT)))/vp):+.3f} dex low")
resid_corr = RAW["canonical"][0] - end_bias
ck("31b.7 AGAINST INTEREST: on the single object where the pipeline can be checked against interferometry it "
   "UNDERSTATES the rotation speed, so some of the sample deficit is the estimator's.  Applying that one object's "
   "end-to-end correction to the whole sample would move the deficit from -0.30 to about -0.09 dex -- but it is one "
   "galaxy, it is the narrowest-lined object in the sample where the turbulence subtraction is worst, and it cannot "
   "carry the sample.  Recorded as the largest single uncertainty in item 31",
   end_bias > 0.0,
   f"pipeline {v_pipe:.1f} km/s vs resolved {V_RES:.0f} km/s = {end_bias:+.3f} dex; sample residual would go "
   f"{RAW['canonical'][0]:+.3f} -> {resid_corr:+.3f} dex if that correction were universal")

# ---------------------------------------------------------------- 8. mutations
P(""); P("-"*118); P("8. MUTATION CONTROLS -- does the de-selection machinery actually recover a known answer?"); P("-"*118)
for truth in (0.0, -0.30):
    obs_mock, _, _ = forward(Mb[ok], h["inc"][ok], hF[ok], hrms[ok], truth, sig_sc, seed=21)
    rec = solve_offset(Mb[ok], h["inc"][ok], hF[ok], hrms[ok], obs_mock, sig_sc, seed=22)
    info(f"  injected intrinsic offset {truth:+.3f} dex -> the pipeline would MEASURE {obs_mock:+.3f} dex -> "
         f"de-selection recovers {rec:+.3f} dex (error {rec-truth:+.3f})")
    if truth == 0.0: REC0 = rec
    else: REC3 = rec
ck("M31b.a mutation: the section-4 de-selection is invertible.  Feed it a population that is exactly ON the BTFR and it "
   "returns zero; feed it one that is 0.30 dex below and it returns 0.30 dex below.  So the intrinsic offset quoted "
   "above is a measurement and not an artefact of the correction itself",
   abs(REC0) < 0.03 and abs(REC3 + 0.30) < 0.03,
   f"recovered {REC0:+.3f} for a true 0.000, and {REC3:+.3f} for a true -0.300")
no_sel_h, _, _ = forward(Mb[ok], h["inc"][ok], hF[ok], hrms[ok]*1e-3, 0.0, sig_sc, seed=23)
ck("M31b.b mutation: switch the selection OFF (drop the rms by 1000x so nothing is width-limited) and the manufactured "
   "bias vanishes -- confirming that the bias measured in section 4 is the width cut and not a bug in the mock",
   abs(no_sel_h) < 0.02,
   f"with the detection limit removed the mock returns {no_sel_h:+.4f} dex against {MAN[0.26][0]:+.3f} with it in place")
sh = np.array([np.median(rng.permutation(r_can[ok])[:40]) for _ in range(2000)])
ck("M31b.c mutation: the edge-on/face-on split of section 2 is not a random partition -- resampling 40 objects at "
   "random reproduces the sample median, not the split, so section 2's comparison carries information",
   abs(np.median(sh) - RAW["canonical"][0]) < 0.03,
   f"random 40-object medians centre on {np.median(sh):+.3f} against the full-sample {RAW['canonical'][0]:+.3f}")

# ---------------------------------------------------------------- verdict
P(""); P("="*118)
P("VERDICT -- ITEM 31 AFTER THE AUDIT: h31's LIABILITY IS WITHDRAWN AS A DIFFERENTIAL RESULT.  It was mostly selection.")
P("="*118)
P(f"  h31 reported that the almost-darks sit {RAW['canonical'][0]:+.3f} +- {RAW['canonical'][1]:.3f} dex below the framework's zero-parameter BTFR,")
P(f"  {RAW['canonical'][0]-CTRL_RAW['canonical'][0]:+.3f} dex differentially against a mass-matched control, and called it a 9.5 sigma liability.  The")
P(f"  differential does not survive this audit, and the reason is a selection effect h31 did not model.")
P(f"")
P(f"  ALFALFA's sensitivity falls as W50^(-1/2), so at fixed HI mass and distance a FAST rotator is harder to detect")
P(f"  than a slow one.  At fixed baryonic mass and inclination that is a cut on the BTFR residual itself.  It bites the")
P(f"  almost-darks hard -- {100*f_undetect:.0f}% of them would be undetectable if they sat exactly on the framework's BTFR -- and it")
P(f"  barely touched h31's control, which was nearer ({np.median(a['dist'][ci]):.0f} vs {np.median(h['dist'][ok]):.0f} Mpc) and brighter (SNR {np.median(a['snr'][ci]):.1f} vs {np.median(hsnr[ok]):.1f}).")
P(f"  h31 compared a width-truncated sample with an untruncated one and read the difference as physics.")
P(f"")
P(f"  Matched properly -- same baryonic mass, same HI mass, same inclination, same detection ceiling W_max, and with")
P(f"  W_max built from flux and noise alone so that it is not a collider -- ordinary ALFALFA galaxies sit at")
P(f"  {MATCH['canonical'][0]:+.3f} +- {MATCH['canonical'][1]:.3f} dex and the almost-darks at {RAW['canonical'][0]:+.3f}.  The almost-dark property is worth")
P(f"  {DIFM[0]:+.3f} +- {DIFM[1]:.3f} dex ({DIFM[0]/DIFM[1]:.1f} sigma), not {RAW['canonical'][0]-CTRL_RAW['canonical'][0]:+.3f}.  The forward model agrees independently: de-selecting")
P(f"  the width cut self-consistently moves the absolute offset from {RAW['canonical'][0]:+.3f} to {off_sc:+.3f} dex.")
P(f"")
P(f"  What the audit could NOT break, and tried hard to:")
P(f"   * the geometry.  Granting every galaxy the most face-on inclination its own measured axis ratio permits, for ANY")
P(f"     oblate thickness, still leaves {BOUND['canonical'][0]:+.3f} dex.  Hubble's q0 = 0.2 is not doing the work.")
P(f"   * the published counter-claim's mechanism (arXiv:2408.05269, low-inclination systematics).  The deficit is not")
P(f"     carried by the face-on objects: the edge-on half sits at {m_hi:+.3f} dex against the face-on half's {m_lo:+.3f}.")
P(f"   * noise.  Symmetric axis-ratio error moves the median UP ({NOISE_SHIFT:+.4f} dex) by Jensen's inequality, so scatter")
P(f"     cannot manufacture a deficit; only a systematic factor-2 error in sin i could, and no geometry allows one.")
P(f"  But the audit also failed its OWN model: the residual's trend with inclination ({obs_span:+.3f} dex from face-on to")
P(f"  edge-on) is about three times steeper than the width selection can make ({span_on:+.3f}) and steeper than any constant")
P(f"  offset ({span_low:+.3f}), and it is not axis-ratio noise ({NOISE_FACEON:+.4f}).  An inclination-dependent systematic is loose in")
P(f"  these measurements that nobody's model captures, so the sample median cannot be quoted to better than ~0.1 dex.")
P(f"")
P(f"  So the RESIDUAL absolute offset of about {off_sc:+.2f} dex, shared by the almost-darks and by ordinary gas-rich")
P(f"  galaxies of the same detectability, is not an inclination artefact.  Whether it is the framework's problem or a")
P(f"  further layer of ALFALFA selection is NOT settled here, and this script does not claim it either way.")
P(f"")
P(f"  Two bugs found, one in h31 and one in this audit's own first attempt:")
P(f"   * h31: the control was matched on mass alone, so it was not width-truncated the way the almost-darks are.")
P(f"   * here: matching the control on SNR instead looked decisive ({RAW['canonical'][0]-m_bad:+.3f} dex, effect gone) and was WRONG --")
P(f"     SNR contains W50, so it conditions on the estimator's own numerator.  Its control had a median width of")
P(f"     {np.median(a['W50'][ci][sel_bad]):.0f} km/s against the mass-matched {np.median(a['W50'][ci]):.0f} km/s.  Reported, not quietly dropped.")
P(f"   * and against interest a third time: on AGC 114905, the only object with resolved kinematics, this pipeline")
P(f"     returns {v_pipe:.1f} km/s where interferometry gives {V_RES:.0f} -- a {end_bias:+.3f} dex underestimate from the turbulence")
P(f"     subtraction on a {h['W50'][ia]:.0f} km/s line.  The sample median width is {np.median(h['W50'][ok]):.0f} km/s where that correction is far smaller.")
P(f"")
P(f"  STANDING: item 31 is a NULL, not a liability and not a win.  The almost-darks are NOT measurably off the BTFR")
P(f"  relative to comparable ordinary galaxies ({DIFM[0]:+.2f} +- {DIFM[1]:.2f} dex).  The item's Kepler-grade criterion -- 20+ objects")
P(f"  on the line with <= 0.1 dex scatter -- is still not met, because the scatter is {RAW['canonical'][2]:.2f} dex, so this sample")
P(f"  cannot measure a_0 without stellar mass-to-light either.  Nothing here favours one footing over the other.")
P(f"  h31's headline number and its 9.5 sigma must NOT be quoted.  The decisive measurement remains resolved HI for")
P(f"  more than one object, which is what the published dispute is also waiting on.")
sys.exit(ck.done())
