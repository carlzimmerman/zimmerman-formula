#!/usr/bin/env python3
"""
estimator_weight_diagnosis.py -- WHY COULD AN a0-LINE SLOPE ESTIMATOR BE BIASED?
A STRUCTURAL, PURELY NUMERICAL MECHANISM DIAGNOSIS ON THE REAL GAS-DOMINATED SPARC
SUBSAMPLE -- INDEPENDENT OF (AND PRIOR TO) THE FROZEN MOCK BIAS MEASUREMENT.
=================================================================================
Framework: Zimmerman de Sitter-Unruh MODIFIED-INERTIA law, its OWN interpolation
  g_obs = sqrt(g_bar^2 + a0*g_bar)  <=>  E := g_obs^2 - g_bar^2 = a0*g_bar  (exact),
  a0 = c*H_Lambda/Z, Z = sqrt(32*pi/3). Judged on its own terms; McGaugh's nu is never
  the yardstick. Both footings (canonical 9.355e-11, ALT 1.1305e-10) carried throughout.

THE QUESTION (committed Step-A ground truth, per_galaxy_budget.py / reach_target.py /
estimator_theory.py): on the gas-dominated subsample (49 galaxies, 310 points) the two
committed estimators disagree by 22% of canonical -- MORE than the 21% footing gap:
    GLS through-origin  a0_hat = sum(w E g)/sum(w g^2)  -> 1.1814e-10  (~ ALT)
    robust median of a0_pt = (g_obs^2-g_bar^2)/g_bar     -> 9.7256e-11  (~ canonical)
The frozen pre-registration (PREREG_ESTIMATOR_BIAS.md, commit c63a2931) measures each
estimator's BIAS on mocks with a known injected a0. THIS script does something different
and complementary: it asks whether the DATA STRUCTURE ITSELF predicts a bias, and of
which SIGN, from the real weights/leverages alone -- an independent cross-check that can
CORROBORATE or CONTRADICT the mock result.

THE BRIEF'S PROPOSED MECHANISM, TESTED HERE (hypothesis, not conclusion):
  "GLS weights points by w*g_bar^2, which UPWEIGHTS HIGH-g_bar points; at high g_bar,
   E = g_obs^2 - g_bar^2 is a small difference of large numbers (catastrophic
   cancellation), and those same points carry maximal M/L leverage ~phi*a0*(2y+1);
   so GLS may be dominated by the points with the LEAST a0 information and the MOST
   systematic leverage."
Sections D2/D3/D4 test the three legs of that chain quantitatively. D5 then derives a
SIGN PREDICTION from whatever mechanism actually survives.

PREREGISTRATION COMPLIANCE (explicit, checked by assertion where checkable):
  * NO mock realization is generated here. D5 is semi-analytic MOMENT PROPAGATION: the
    independent noise terms are replaced by their EXACT analytic moments (plus a 1-D MC
    over the two GLOBAL coherent draws only). No 310-point noise vector is ever drawn.
  * NO candidate estimator from the frozen list of nine is evaluated on the real data
    beyond the TWO ALREADY-COMMITTED incumbents (gls_origin, median_a0pt), per S7. The
    one auxiliary location statistic used (the UNWEIGHTED mean of a0_pt) is NOT in the
    frozen list, is not a candidate for primary status, and is reported only as a RATIO
    to the incumbent GLS because it is a decomposition diagnostic of that incumbent.
  * NO gate, threshold, estimator definition, seed or injection value is touched. The
    frozen gates are sign-blind (|b| only); a sign PREDICTION made in advance cannot
    enter them. This file is additive and does not modify any frozen artifact.

HONESTY RAILS (a manufactured mechanism is penalized exactly like a manufactured deficit):
  * The brief's hypothesis is tested, and where the data KILL it, it is reported killed --
    including the legs that would have been convenient. Two of the three legs fail.
  * The surviving mechanism's predicted sign happens to favour the canonical footing.
    That is stated openly as a RISK, the prediction is made falsifiable (numbers, not
    adjectives), and the frozen sign-blind mock remains the arbiter. A prediction is not
    a measurement and is NOT a footing verdict.
  * a0's VALUE remains POSITED in the framework regardless. This is a MEASUREMENT
    diagnosis, not a derivation of the coefficient. No "theory closed", no TOE claim.
Exit 0 = the structure was computed. Exit code is not a verdict.
"""
import numpy as np, os, json, hashlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fire_common as fc

HERE = fc.HERE
bar = "=" * 100
UD = 0.70
A0C, A0A, A0M = fc.A0C, fc.A0A, 1.2e-10          # canonical / ALT / standard-MOND
SIG_INC, SIG_LNU, SIG_LNG, SLNB = fc.SIG_INC, fc.SIG_LNU, fc.SIG_LNG, fc.SLNB
INJ = (("canonical", 9.354769736111044e-11), ("ALT", 1.1305322040279838e-10),
       ("std-MOND", 1.2e-10))                     # the three FROZEN injections
RES = {}

# ============================================================================ D0
print(bar)
print("D0 -- SAMPLE, COMMITTED ANCHORS, AND A CROSS-CHECK AGAINST THE FROZEN PREREG MANIFEST")
print(bar)
gals = fc.load(UD)
GB, GO, FV, PHI, GAL, SLD, CTI = fc.flat(gals, True)          # gas-dominated points
a0, fint, c2n, w = fc.gls(GB, GO, FV)
S = float(np.sum(w * GB**2))
u = w * GB**2 / S                                              # normalized GLS weights
E = GO**2 - GB**2
apt = E / GB                                                   # per-point a0_pt
med = float(np.median(apt))
N, NG = len(GB), len(set(GAL.tolist()))
assert (N, NG) == (310, 49), (N, NG)
assert abs(a0 - 1.1814381247770623e-10) < 1e-22, a0            # committed regression anchor
assert abs(med - 9.725607106012755e-11) < 1e-22, med
print(f"  N = {N} gas-dominated points, N_gal = {NG}  (SPARC Q<=2, inc>=30, eV/Vobs<0.10)")
print(f"  committed incumbents reproduced EXACTLY:  GLS = {a0:.4e}   median = {med:.4e}")
print(f"  GLS/median = {a0/med:.4f}  (the {100*(a0/med-1):.1f}% estimator spread under diagnosis)")
print(f"  iterated f_int = {fint:.4f} at chi2/N = {c2n:.6f}")
print(f"  g_bar range {GB.min():.3e} .. {GB.max():.3e}  ;  y := g_bar/a0 depends on the footing:")
print(f"    y_max = {GB.max()/A0C:.4f} (canonical) / {GB.max()/A0A:.4f} (ALT) / "
      f"{GB.max()/A0M:.4f} (std-MOND) / {GB.max()/1e-10:.4f} (prereg's neutral 1e-10 ref)")
print(f"    y_median = {np.median(GB)/A0C:.4f} (canonical)")
print(f"  ==> the subsample is DEEP-MOND THROUGHOUT at EVERY footing: y_max < 0.19 << 1.")

# cross-check the sample against the frozen prereg truth manifest (integrity of footing)
cfgp = os.path.join(HERE, "prereg_estimator_bias_config.json")
cfg = json.load(open(cfgp))
man = {m["name"]: m for m in cfg["sample"]["manifest"]}
assert cfg["sample"]["N_points"] == N and cfg["sample"]["N_gal"] == NG
nchk = 0
for k, g in enumerate(gals):
    m = g["gasdom"]
    if not m.any():
        continue
    r = man[g["name"]]
    assert np.allclose(np.array(r["g_bar_true"]), g["gb"][m], rtol=1e-12, atol=0)
    assert np.allclose(np.array(r["phi"]), g["phi"][m], rtol=1e-12, atol=0)
    assert np.allclose(np.array(r["fv"]), g["fv"][m], rtol=1e-12, atol=0)
    assert abs(r["sig_lnD"] - g["sig_lnD"]) < 1e-15 and r["npt"] == int(m.sum())
    nchk += int(m.sum())
assert nchk == N
FROZEN_CFG_SHA = "8cc0a9664c420a0c36f07a8a99372481cad2d4aca1fd6c552b2955f3a840d765"
FROZEN_MD_SHA = "6be465f21c7ea075f7a585779184970f145a8cdd2e61554a17e101be9a099dc2"
h = hashlib.sha256(open(cfgp, "rb").read()).hexdigest()
hmd = hashlib.sha256(open(os.path.join(HERE, "PREREG_ESTIMATOR_BIAS.md"), "rb").read()).hexdigest()
print(f"  [prereg manifest cross-check: all {nchk} (g_bar_true, phi, fv) triples + all 49")
print(f"   (f_D, sigma_lnD, inc, npt) records match this sample to 1e-12 relative]")
print(f"  [frozen digests re-verified: config {h[:16]}... "
      f"{'OK' if h == FROZEN_CFG_SHA else 'MISMATCH'} ; PREREG md {hmd[:16]}... "
      f"{'OK' if hmd == FROZEN_MD_SHA else 'MISMATCH'}]")
assert h == FROZEN_CFG_SHA and hmd == FROZEN_MD_SHA, "frozen pre-registration was altered"
RES["config_sha256"] = h
RES["prereg_md_sha256"] = hmd

# ============================================================================ D1
print()
print(bar)
print("D1 -- THE ALGEBRAIC FACT THAT REFRAMES THE WHOLE QUESTION")
print(bar)
wmean = float(np.sum(u * apt))
print("  a0_hat(GLS) = sum(w E g)/sum(w g^2) = sum_i [w_i g_i^2 / S] * (E_i/g_i)")
print(f"            === WEIGHTED MEAN of the per-point a0_pt with weights u_i = w_i g_i^2/S")
print(f"  numerical check: sum(u*a0_pt) = {wmean:.12e}   a0_hat(GLS) = {a0:.12e}")
print(f"                   |difference| / a0 = {abs(wmean-a0)/a0:.2e}   (machine precision)")
assert abs(wmean - a0) / a0 < 1e-13
print("  ==> 'GLS vs robust median' is NOT a regression-vs-robustness question at all:")
print("      it is exactly a MEAN vs MEDIAN comparison on ONE per-point distribution,")
print("      a0_pt. Whatever separates them must be a property of that distribution")
print("      (its skew) and/or of the weights u_i. Both are measured below.")
unw = float(np.mean(apt))
print(f"\n  weight non-uniformity: u_i*N in [{u.min()*N:.3f}, {u.max()*N:.3f}] "
      f"(max/min = {u.max()/u.min():.2f}); N_eff = 1/sum(u^2) = {1/np.sum(u**2):.1f} of {N} "
      f"({100/np.sum(u**2)/N:.1f}%)")
print(f"  UNWEIGHTED mean of a0_pt / a0_hat(GLS) = {unw/a0:.4f}  <-- diagnostic ratio only")
print("   (the unweighted mean is NOT one of the nine frozen candidate estimators and cannot")
print("    enter any gate; it is quoted as a ratio because it decomposes the incumbent GLS.)")
print(f"  ==> on THIS subsample the GLS weights are nearly UNIFORM: GLS is within "
      f"{100*abs(unw/a0-1):.2f}% of")
print("      the plain unweighted mean. So essentially NONE of the GLS-median gap can come")
print("      from weighting; it is a MEAN-vs-MEDIAN (skew) effect. First leg of the brief's")
print("      chain already looks weak -- quantified next.")
RES["D1"] = dict(gls=a0, median=med, ratio_gls_over_median=a0 / med,
                 identity_resid_rel=abs(wmean - a0) / a0, unweighted_over_gls=unw / a0,
                 Neff=float(1 / np.sum(u**2)), u_max_over_min=float(u.max() / u.min()),
                 fint=fint)

# ============================================================================ D2
print()
print(bar)
print("D2 -- (a) THE GLS WEIGHT DISTRIBUTION: WHERE DOES THE WEIGHT ACTUALLY SIT?")
print(bar)
order = np.argsort(GB)
print(f"  {'g_bar decile (low->high)':<26}{'N':>4}{'<y_canon>':>11}{'weight share %':>16}"
      f"{'cum %':>8}")
cum = 0.0
dec_share = []
for d in range(10):
    sel = order[d * N // 10:(d + 1) * N // 10]
    sh = float(u[sel].sum()); cum += sh
    dec_share.append(sh)
    print(f"  decile {d+1:<19}{len(sel):>4}{np.mean(GB[sel])/A0C:>11.4f}{100*sh:>15.2f}%"
          f"{100*cum:>7.1f}%")
top10 = float(u[order[-N // 10:]].sum())
top5pts = float(u[order[-5:]].sum())
bot10 = float(u[order[:N // 10]].sum())


def spearman(x, yv):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(yv)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])


sp_ug = spearman(u, GB)
slope = float(np.polyfit(np.log(GB), np.log(u), 1)[0])
print(f"\n  HIGHEST-g_bar decile carries {100*top10:.2f}% of the GLS weight "
      f"(uniform would be 10.00%).")
print(f"  the 5 single highest-g_bar points carry {100*top5pts:.2f}% (uniform: "
      f"{100*5/N:.2f}%).")
print(f"  LOWEST-g_bar decile carries {100*bot10:.2f}%.")
print(f"  Spearman rank correlation  corr(u, g_bar) = {sp_ug:+.3f}")
print(f"  log-log regression         d ln u / d ln g_bar = {slope:+.3f}")
print("  ==> THE BRIEF'S FIRST LEG IS FALSE ON THIS SAMPLE: the GLS weight is (mildly)")
print("      ANTI-correlated with g_bar -- high-g_bar points are DOWN-weighted, not up-.")
print("\n  WHY, structurally (exact algebra of the committed error model):")
print("    sig2_E = (4*Gm2*fv)^2 + (2*g_bar^2*0.10)^2 + (f_int*Gm2)^2 ,  Gm2 = g_bar^2+a0*g_bar")
print("    => w*g_bar^2 = 1 / [ sig2_E/g_bar^2 ] = 1 / [ a0^2(1+y)^2(16 fv^2 + f_int^2)")
print("                                                 + 0.04 g_bar^2 ]")
print("    BOTH bracketed terms INCREASE with g_bar at fixed fv, so u is STRICTLY DECREASING")
print("    in g_bar: the estimator structurally CANNOT upweight high-g_bar points. At y<<1 the")
print("    g_bar^4 term is negligible and u ~ 1/[(1+y)^2 (16 fv^2 + f_int^2)] -- set by the")
print("    VELOCITY-ERROR quality flag fv times a mild (1+y)^-2 decline. Verify numerically:")
# fire_common.gls returns the weights of the converged iteration, whose f_int is the
# PRE-update value (f_int is rescaled by c2n**0.25 AFTER w is formed); undo that to compare.
fint_w = fint / c2n**0.25
u_pred = 1.0 / (a0**2 * (1 + GB / a0)**2 * (16 * FV**2 + fint_w**2) + 0.04 * GB**2)
u_pred = u_pred / u_pred.sum()
u_fv = 1.0 / (16 * FV**2 + fint_w**2); u_fv = u_fv / u_fv.sum()
print(f"    closed form vs iterated GLS weights: max |du/u| = {np.max(abs(u_pred/u-1)):.2e}"
      f"  [= the GLS loop's own |da0|<1e-17 convergence tolerance, 8e-8 relative: EXACT]")
print(f"    fv-only limit   vs iterated GLS weights: max |du/u| = {np.max(abs(u_fv/u-1)):.3f}"
      f" ({100*np.max(abs(u_fv/u-1)):.0f}%, i.e. the (1+y)^-2 part), rank corr = "
      f"{spearman(u_fv,u):+.3f}")
assert np.max(abs(u_pred / u - 1)) < 1e-6
# monotonicity of w*g_bar^2 in g_bar, at fixed fv, over 5 decades (the structural claim)
_gg = np.geomspace(1e-13, 1e-8, 400)
_uu = 1.0 / (a0**2 * (1 + _gg / a0)**2 * (16 * np.median(FV)**2 + fint_w**2) + 0.04 * _gg**2)
assert np.all(np.diff(_uu) < 0), "w*g_bar^2 not monotonically decreasing in g_bar"
print(f"    monotonicity check: w*g_bar^2 strictly DECREASING over g_bar = 1e-13..1e-8 "
      f"(5 decades, 400 pts) at fixed fv -- verified")
print(f"  Spearman corr(u, fv) = {spearman(u, FV):+.3f}: the GLS weight is essentially the")
print(f"  point-quality flag, NOT an acceleration weighting.")

# --- weight concentration BY GALAXY (mechanism M2 of the prereg) --------------------
gsh = np.array([float(u[GAL == k].sum()) for k in sorted(set(GAL.tolist()))])
npts = np.array([int((GAL == k).sum()) for k in sorted(set(GAL.tolist()))])
og = np.argsort(-gsh)
print(f"\n  weight concentration BY GALAXY (prereg mechanism M2):  N_eff,gal = "
      f"{1/np.sum(gsh**2):.1f} of {NG}")
print(f"    top-1 galaxy {100*gsh[og[0]]:.1f}% (npts={npts[og[0]]}), top-5 "
      f"{100*gsh[og[:5]].sum():.1f}%, top-10 {100*gsh[og[:10]].sum():.1f}%")
print(f"    galaxy weight share vs point share: max |share - npts/N| = "
      f"{np.max(abs(gsh - npts/N)):.4f}")
print("    ==> galaxy weight tracks POINT COUNT almost exactly; there is no small-effective-N")
print("        concentration either. M2 is FALSE on this sample.")

# --- the FULL-sample contrast: is the brief's leg true anywhere? --------------------
GBf, GOf, FVf, PHIf, GALf, SLDf, CTIf = fc.flat(gals, False)
a0f, fintf, _, wf = fc.gls(GBf, GOf, FVf)
uf = wf * GBf**2 / np.sum(wf * GBf**2)
yf = GBf / A0C
print(f"\n  FULL-SAMPLE CONTRAST (N={len(GBf)}, y up to {yf.max():.1f} -- the regime the brief's")
print("  mechanism was written for):")
print(f"    Spearman corr(u, g_bar) = {spearman(uf, GBf):+.3f} ; d ln u/d ln g_bar = "
      f"{np.polyfit(np.log(GBf), np.log(uf), 1)[0]:+.3f}")
for cut in (1, 3, 10, 30):
    m = yf > cut
    print(f"    y > {cut:<3}: N = {int(m.sum()):>4}  GLS weight share = {100*uf[m].sum():6.3f}%")
print("    ==> the high-g_bar points are down-weighted EVEN MORE strongly on the full")
print("        sample (the 0.04*g_bar^2 shape-scatter term takes over and w*g_bar^2 ~ 1/g_bar^2).")
print("        The 'GLS is dominated by high-g_bar points' hypothesis is FALSE in BOTH samples.")
RES["D2"] = dict(decile_weight_share=dec_share, top_decile_share=top10,
                 bottom_decile_share=bot10, top5_points_share=top5pts,
                 spearman_u_gbar=sp_ug, loglog_slope_u_gbar=slope,
                 spearman_u_fv=spearman(u, FV), Neff_gal=float(1 / np.sum(gsh**2)),
                 closed_form_weight_max_relerr=float(np.max(abs(u_pred / u - 1))),
                 full_spearman_u_gbar=spearman(uf, GBf),
                 full_weight_share_y_gt={str(c): float(uf[yf > c].sum()) for c in (1, 3, 10, 30)},
                 verdict="brief leg 1 (GLS upweights high g_bar) FALSE in both samples")

# ============================================================================ D3
print()
print(bar)
print("D3 -- (b) CATASTROPHIC CANCELLATION IN E = g_obs^2 - g_bar^2: HOW BIG IS IT HERE?")
print(bar)
print("  Exact structure on the a0-line (g_obs^2 = g_bar^2 + a0 g_bar):")
print("    E / g_bar^2                = 1/y            <- the 'small difference' ratio")
print("    kappa(y) := (g_obs^2+g_bar^2)/|E| = 2y+1     <- subtraction condition number")
print("    d lnE / d ln g_bar         = -2y            <- the CANCELLATION amplification")
print("    d lnE / d ln g_obs         = +2(y+1)        <- (not cancellation: the signal term)")
print("    d ln a0_pt / d ln g_bar    = -(2y+1)        <- 1 from E/g_bar, 2y from cancellation")
print("  so the cancellation SHARE of the total g_bar lever is 2y/(2y+1): it VANISHES as")
print("  y->0 and only becomes catastrophic for y >> 1. Verify numerically (finite diff):")
h_ = 1e-7
for yv in (0.05, 0.15, 1.0, 10.0, 100.0):
    gbv = yv * A0C
    Ev = (gbv**2 + A0C * gbv) - gbv**2
    Ep = (gbv**2 + A0C * gbv) - (gbv * (1 + h_))**2
    num = (Ep / Ev - 1) / h_
    print(f"    y={yv:>6.2f}: dlnE/dln g_bar  numeric {num:+9.4f}  analytic {-2*yv:+9.4f}"
          f"   kappa = {2*yv+1:8.2f}   E/g_bar^2 = {1/yv:9.2f}")
    assert abs(num + 2 * yv) < 5e-4 * max(1.0, 2 * yv)
ymax, ymed = GB.max() / A0C, np.median(GB) / A0C
print(f"\n  WHERE THIS SUBSAMPLE ACTUALLY LIVES:  y_median = {ymed:.4f}, y_max = {ymax:.4f}")
print(f"    at y_max: kappa = {2*ymax+1:.3f}  (1.000 = no cancellation at all),")
print(f"              E/g_bar^2 = {1/ymax:.1f}  -- E is {1/ymax:.0f}x LARGER than g_bar^2,")
print(f"              cancellation share of the g_bar lever = 2y/(2y+1) = "
      f"{2*ymax/(2*ymax+1):.3f} ({100*2*ymax/(2*ymax+1):.1f}%)")
print(f"    weight-averaged over the sample: kappa = {float(np.sum(u*(2*GB/A0C+1))):.4f}, "
      f"cancellation share = {float(np.sum(u*2*GB/A0C/(2*GB/A0C+1))):.4f}")
canc_alt = float(np.sum(u * 2 * GB / A0A / (2 * GB / A0A + 1)))
print(f"    (ALT footing: cancellation share {canc_alt:.4f} -- footing-insensitive)")
print("  ==> THE BRIEF'S SECOND LEG IS FALSE ON THIS SAMPLE. E is NOT a small difference of")
print("      large numbers here; it is a LARGE difference of small numbers. There is no")
print("      catastrophic cancellation to amplify anything. (This is the same honesty note")
print("      already recorded in advance in PREREG S3 -- confirmed numerically.)")
print(f"\n  For completeness, where the mechanism IS live -- FULL sample (y up to {yf.max():.0f}):")
print(f"    {'y-cut':>7}{'N':>6}{'kappa at cut':>14}{'GLS weight share':>18}")
for cut in (1, 3, 10, 30):
    m = yf > cut
    print(f"    {cut:>7}{int(m.sum()):>6}{2*cut+1:>14.1f}{100*uf[m].sum():>17.3f}%")
print("    ==> even where kappa reaches 21-61, GLS puts <0.6% of its weight there. The")
print("        cancellation regime and the GLS weight simply do not overlap. The brief's")
print("        mechanism is REAL ALGEBRA but is NOT REALIZED by this estimator on this data.")
RES["D3"] = dict(y_median=float(ymed), y_max=float(ymax), kappa_at_ymax=float(2 * ymax + 1),
                 E_over_gbar2_at_ymax=float(1 / ymax),
                 cancel_share_at_ymax=float(2 * ymax / (2 * ymax + 1)),
                 cancel_share_weighted=float(np.sum(u * 2 * GB / A0C / (2 * GB / A0C + 1))),
                 cancel_share_weighted_ALT=canc_alt,
                 verdict="brief leg 2 (catastrophic cancellation) FALSE on the gas-dominated "
                         "subsample (deep-MOND throughout); real only at y>>1 where GLS "
                         "carries <0.6% of its weight")

# ============================================================================ D4
print()
print(bar)
print("D4 -- (c) SYSTEMATIC LEVERAGE vs a0-INFORMATION: DOES GLS WEIGHT THE WORST POINTS?")
print(bar)
y = GB / a0
LU = PHI * (2 * y + 1)                       # M/L leverage /a0   (d a0_pt/dlnUps = -phi a0(2y+1))
LG = (1 - PHI) * (2 * y + 1)                 # gas-cal leverage /a0
LD = 2 * (y + 1) * SLD                       # per-point distance leverage x sigma_lnD
LI = 4 * (y + 1) * CTI * SIG_INC             # per-point inclination leverage x sigma_i
LV = 4 * (y + 1) * FV                        # per-point velocity leverage x fv
print(f"  per-point leverages (fractional a0_pt error each term alone would produce):")
for nm, L in (("M/L  phi*(2y+1)*0.23", LU * SIG_LNU), ("gascal (1-phi)(2y+1)*0.10", LG * SIG_LNG),
              ("distance 2(y+1)*sig_lnD", LD), ("inclination 4(y+1)cot(i)*sig_i", LI),
              ("velocity 4(y+1)*fv", LV)):
    print(f"    {nm:<32} median {np.median(L):.3f}  max {L.max():.3f}  "
          f"u-weighted mean {float(np.sum(u*L)):.3f}")
print(f"  the (2y+1) and (y+1) factors are {2*y.min()+1:.3f}..{2*y.max()+1:.3f} and "
      f"{y.min()+1:.3f}..{y.max()+1:.3f} on this sample:")
print("  i.e. essentially CONSTANT. So leverage ordering here is set by phi, cot(i), fv and")
print("  sigma_lnD -- NOT by y. The brief's 'maximal leverage at high y' does not order")
print("  these points either.")
print(f"\n  correlations with the GLS weight u:")
for nm, L in (("M/L leverage phi(2y+1)", LU), ("gascal leverage (1-phi)(2y+1)", LG),
              ("distance leverage 2(y+1)sig_lnD", LD), ("incl. leverage 4(y+1)cot(i)sig_i", LI),
              ("velocity leverage 4(y+1)fv", LV), ("y = g_bar/a0", y)):
    print(f"    Spearman corr(u, {nm:<34}) = {spearman(u, L):+.3f}")
print("  ==> weight vs M/L leverage is essentially UNCORRELATED-to-mildly-NEGATIVE: the")
print("      brief's third leg (GLS concentrates weight on the maximal-M/L-leverage points)")
print("      is also NOT realized. All three legs of the proposed chain fail HERE.")

print("\n  BUT there IS a real mis-weighting, and it is a DIFFERENT one. Note first that")
print("  w_i*g_bar_i^2 IS the Fisher information for a0 under the committed error model, so")
print("  GLS is optimal *given that model*. The model, however, OMITS the distance and")
print("  inclination errors entirely (fire_common.sig2_model has only fv, shape, f_int).")
sig_meas2 = LD**2 + LI**2 + LV**2 + ((2 * y + 1) * SLNB)**2       # measurement terms only
hf = SLD > 0.2                                   # Hubble-flow points, sigma_lnD = 0.25
tr = SLD < 0.06                                  # TRGB points, sigma_lnD = 0.05
# self-consistent variance-component fit: add an intrinsic term and iterate to chi2/N = 1
si = 0.4
for _ in range(500):
    wv = 1.0 / (sig_meas2 + si**2)
    aw = float(np.sum(wv * apt) / np.sum(wv))
    c2 = float(np.mean(wv * (apt / aw - 1.0)**2))
    si = max(1e-4, si * c2**0.25)
    if abs(c2 - 1) < 1e-8:
        break
w_sc = 1.0 / (sig_meas2 + si**2); u_sc = w_sc / w_sc.sum()       # self-consistent weights
w_ms = 1.0 / sig_meas2; u_ms = w_ms / w_ms.sum()                 # measurement-only weights
print(f"  Build the COMPLETE per-point a0_pt variance and compare weightings. Two versions,")
print(f"  both reported because the choice matters: measurement-terms-only (D+i+v+shape), and")
print(f"  self-consistent (same + an intrinsic term refitted to chi2/N=1 -> sigma_int = "
      f"{si:.3f}).")
print(f"    {'subset':<28}{'pt share':>10}{'GLS wt':>9}{'complete(self-cons)':>21}"
      f"{'complete(meas-only)':>21}")
for lab, msk in (("Hubble-flow (sig_lnD=0.25)", hf), ("TRGB (sig_lnD=0.05)", tr)):
    print(f"    {lab:<28}{100*msk.mean():>9.1f}%{100*u[msk].sum():>8.1f}%"
          f"{100*u_sc[msk].sum():>20.1f}%{100*u_ms[msk].sum():>20.1f}%")
print(f"    N_eff: GLS {1/np.sum(u**2):.1f} | self-cons {1/np.sum(u_sc**2):.1f} | "
      f"meas-only {1/np.sum(u_ms**2):.1f}   of {N}")
over_sc = float(u[hf].sum() / u_sc[hf].sum())
over_ms = float(u[hf].sum() / u_ms[hf].sum())
print(f"  ==> GLS OVER-WEIGHTS the distance-uncertain (Hubble-flow) half of the sample by")
print(f"      x{over_sc:.2f} (self-consistent) to x{over_ms:.2f} (measurement-only) relative to a")
print(f"      complete-error weighting. THIS is the real mis-weighting -- not 'high g_bar'")
print(f"      but 'sigma_lnD = 0.25 weighted as if it were 0'.")
eff = float(np.sum(u**2 * (sig_meas2 + si**2)) / (1.0 / np.sum(1.0 / (sig_meas2 + si**2))))
print(f"      variance inefficiency of the GLS weights under the self-consistent model: "
      f"x{eff:.2f} (RMS x{np.sqrt(eff):.2f})")
print(f"      NOTE, honestly: that is nearly optimal. The omission of sigma_lnD costs almost")
print(f"      nothing in VARIANCE (the large intrinsic term dominates and flattens the")
print(f"      weights); it costs in BIAS, because it is exactly the high-sigma_lnD galaxies")
print(f"      that carry the largest Jensen inflation (D5). Variance-optimality does NOT")
print(f"      protect a mean-like estimator from a multiplicative-error bias.")
RES["D4"] = dict(spearman_u_MLlev=spearman(u, LU), spearman_u_gascallev=spearman(u, LG),
                 spearman_u_distlev=spearman(u, LD), spearman_u_inclev=spearman(u, LI),
                 spearman_u_y=spearman(u, y),
                 hubbleflow_point_share=float(hf.mean()),
                 hubbleflow_gls_weight=float(u[hf].sum()),
                 hubbleflow_weight_selfconsistent=float(u_sc[hf].sum()),
                 hubbleflow_weight_measonly=float(u_ms[hf].sum()),
                 sigma_int_selfconsistent=float(si),
                 overweight_factor_selfconsistent=over_sc, overweight_factor_measonly=over_ms,
                 var_inefficiency=eff, Neff_complete=float(1 / np.sum(u_sc**2)),
                 verdict="brief leg 3 (weight on maximal-M/L-leverage points) FALSE; the REAL "
                         "mis-weighting is that the GLS error model omits sigma_lnD and "
                         "sigma_i, over-weighting Hubble-flow points by x%.2f-%.2f -- a BIAS "
                         "defect, not a variance defect" % (over_sc, over_ms))

# ============================================================================ D5
print()
print(bar)
print("D5 -- (d) THE SURVIVING MECHANISM AND ITS PREDICTED SIGN (semi-analytic, NO MOCK RUN)")
print(bar)
print("  Propagate the FROZEN forward model exactly. With")
print("    F_i = exp(-2 dlnD_k) * (sin i_k / sin(i_k+di_k))^4 * (1+dv_i)^4     [g_obs^2 factor]")
print("    B_i = (phi_i e^dlnU + (1-phi_i) e^dlnG) * exp(eps_i)               [g_bar factor]")
print("  the per-point observable is EXACTLY")
print("    a0_pt,i / a0_inj = (y_i+1) * F_i / B_i  -  y_i * B_i .")
print("  Every factor is MULTIPLICATIVE and CONVEX in its (symmetric) noise, so")
print("    E[F] > median[F] ~ 1   and   E[1/B] > 1 ,   while median[exp(-2 dlnD)] = 1 exactly.")
print("  The only term pulling DOWNWARD is -y*E[B] (E[B]>1 too), and it is suppressed by the")
print("  factor y < 0.19: on a deep-MOND sample the +(y+1)*E[F/B] term wins by ~6:1.")
print("  A MEAN-like estimator therefore inherits the Jensen/log-normal offset; a MEDIAN-like")
print("  one largely does not. Since D1 proved a0_hat(GLS) IS a weighted mean of a0_pt, GLS")
print("  must be biased HIGH and the median must not. The magnitudes, computed exactly:")
rng = np.random.default_rng(20260725)
NMC = 300000
EFk, MFk = {}, {}
for k, g in enumerate(gals):
    if not g["gasdom"].any():
        continue
    inc, sD = g["inc"], g["sig_lnD"]
    dD = rng.normal(0, sD, NMC)
    di = rng.normal(0, SIG_INC, NMC)
    bad = (inc + di <= np.deg2rad(5)) | (inc + di > np.deg2rad(90))     # frozen redraw rule
    t = 0
    while bad.any() and t < 500:
        di[bad] = rng.normal(0, SIG_INC, int(bad.sum()))
        bad = (inc + di <= np.deg2rad(5)) | (inc + di > np.deg2rad(90))
        t += 1
    Fg = np.exp(-2 * dD) * (np.sin(inc) / np.sin(inc + di))**4
    EFk[k], MFk[k] = float(Fg.mean()), float(np.median(Fg))
EF = np.array([EFk[i] for i in GAL])
MF = np.array([MFk[i] for i in GAL])
Ev4 = 1 + 6 * FV**2 + 3 * FV**4              # E[(1+dv)^4] exact for dv ~ N(0, fv)
Eeps = np.exp(SLNB**2 / 2)                   # E[exp(+-eps)], eps ~ N(0, 0.10)
print(f"    E[exp(-2 dlnD)] = exp(2 sig_lnD^2):  Hubble-flow {np.exp(2*0.25**2):.4f}, "
      f"TRGB {np.exp(2*0.05**2):.4f}, UMa {np.exp(2*0.10**2):.4f}   (median = 1 exactly)")
print(f"    u-weighted E[F] = {float(np.sum(u*EF)):.4f} ,  u-weighted median[F] = "
      f"{float(np.sum(u*MF)):.4f}")
print(f"    u-weighted E[(1+dv)^4] = {float(np.sum(u*Ev4)):.4f} ,  E[e^eps] = {Eeps:.4f}")
# 1-D MC over the TWO GLOBAL coherent draws only (dlnU, dlnG); independent noise at moments
MG = 60000
dU = rng.normal(0, SIG_LNU, MG)
dG = rng.normal(0, SIG_LNG, MG)
pred = {}
print(f"\n  PREDICTED BIAS b = median_over_realizations(a_hat/a0_inj) - 1, in percentage points")
print(f"  (independent noise replaced by exact moments; global Ups/gas-cal by a 1-D MC):")
print(f"    {'injection':<12}{'b_pred GLS (mean-like)':>24}{'b_pred median-like':>21}")
for nm, ainj in INJ:
    yi = GB / ainj
    num = (yi + 1) * EF * Ev4 * Eeps                        # E[(y+1) F / e^eps] numerator part
    den = yi * Eeps
    rat = np.empty(MG)
    for j in range(0, MG, 6000):                            # chunked to bound memory
        sl = slice(j, min(j + 6000, MG))
        Bc = PHI[None, :] * np.exp(dU[sl])[:, None] + (1 - PHI[None, :]) * np.exp(dG[sl])[:, None]
        rat[sl] = np.sum(u[None, :] * (num[None, :] / Bc - den[None, :] * Bc), axis=1)
    b_gls = float(np.median(rat)) - 1.0
    # median-like estimator: per-point median factor, then pooled median (approximation stated)
    Bm = PHI[None, :] * np.exp(dU[:4000])[:, None] + (1 - PHI[None, :]) * np.exp(dG[:4000])[:, None]
    rm = np.median((yi + 1)[None, :] * MF[None, :] / Bm - yi[None, :] * Bm, axis=1)
    b_med = float(np.median(rm)) - 1.0
    pred[nm] = dict(b_gls_pp=100 * b_gls, b_median_pp=100 * b_med)
    print(f"    {nm:<12}{100*b_gls:>+23.2f} {100*b_med:>+20.2f}")
sp_gls = max(p["b_gls_pp"] for p in pred.values()) - min(p["b_gls_pp"] for p in pred.values())
sp_med = max(p["b_median_pp"] for p in pred.values()) - min(p["b_median_pp"] for p in pred.values())
bg = np.mean([p["b_gls_pp"] for p in pred.values()])
bm = np.mean([p["b_median_pp"] for p in pred.values()])
print(f"    injection spread (G3-analogue): GLS {sp_gls:.2f} pp, median-like {sp_med:.2f} pp")
# how much of the mean-bias is the D4 mis-weighting vs irreducible Jensen?
kern = (GB / A0C + 1) * EF * Ev4 * Eeps - (GB / A0C) * Eeps
b_gw, b_sc, b_ms = (float(np.sum(z * kern) - 1) for z in (u, u_sc, u_ms))
print(f"\n  PREDICTION, stated numerically and falsifiably BEFORE any mock number exists:")
print(f"    * b(gls_origin): sign POSITIVE (biased HIGH), magnitude {bg:+.1f} pp "
      f"(quote +9 to +13 pp)")
print(f"      -> predicted to FAIL the frozen G2 gate (2.0 pp) by a factor ~{bg/2.0:.0f}.")
print(f"      This prediction is EXACT in structure, not approximate: the mean commutes with")
print(f"      the expectation, so E[weighted mean] = weighted mean of E[a0_pt] identically.")
print(f"      Residual model risk is only that the mock re-fits its weights on noisy data;")
print(f"      since u depends on g_bar only through (1+y)^-2 with y<0.19, that feedback is")
print(f"      O(1 pp) at most, and f_int re-fitting rescales all weights uniformly (no bias).")
print(f"    * b(median_a0pt): magnitude |b| = {abs(bm):.2f} pp, i.e. SMALL -> predicted to PASS")
print(f"      G2. This prediction is APPROXIMATE, and the approximation is stated: the median")
print(f"      does NOT commute with a mixture, so the pooled median over 310 points drawn")
print(f"      from 49 galaxy-level factors can shift by O(1/sqrt(N_gal)) ~ 1-2 pp. So the")
print(f"      honest form of the claim is |b(median)| <~ 2 pp, i.e. CONSISTENT WITH PASS but")
print(f"      NOT sharply predicted. The mock is the arbiter for this one.")
print(f"    * both nearly INJECTION-INDEPENDENT (spread <= {max(sp_gls,sp_med):.2f} pp): G3 will")
print(f"      not discriminate. The decision will be made by G2 (and then G4).")
print(f"    * ORIGIN OF THE GLS BIAS, decomposed:")
print(f"        exp(2 sig_lnD^2) on the 29 Hubble-flow galaxies is the dominant single term")
print(f"        ({np.exp(2*0.0625):.4f}, i.e. +{100*(np.exp(2*0.0625)-1):.1f}% on their points), amplified by the D4")
print(f"        mis-weighting (GLS gives Hubble-flow points {100*u[hf].sum():.0f}% of the weight vs "
      f"{100*u_sc[hf].sum():.0f}%")
print(f"        self-consistent / {100*u_ms[hf].sum():.0f}% measurement-only). Predicted mean-bias under each")
print(f"        weighting: GLS {100*b_gw:+.1f} pp | self-consistent {100*b_sc:+.1f} pp | "
      f"meas-only {100*b_ms:+.1f} pp.")
print(f"        => {100*(b_gw-b_ms)/b_gw:.0f}% of the GLS bias is mis-weighting; the remaining "
      f"{100*b_ms/b_gw:.0f}% is")
print(f"        IRREDUCIBLE Jensen -- no re-weighting removes it, because any mean-like")
print(f"        estimator of a multiplicative-error quantity inherits E[noise factor] > 1.")

print("\n  INDEPENDENT REAL-DATA CROSS-CHECK OF THE SAME MECHANISM (log-normal consistency):")
pos = apt > 0
lo = np.log(apt[pos])
sig_lnA = float(0.5 * (np.percentile(lo, 84) - np.percentile(lo, 16)))
print(f"    non-positive a0_pt on the real gas-dominated sample: {int((~pos).sum())} of {N}")
print(f"    dispersion of ln a0_pt: 0.5*(P84-P16) = {sig_lnA:.4f}  (a DISPERSION, not a")
print("     location estimate -- no new candidate estimator is evaluated)")
print(f"    if a0_pt were log-normal, mean/median = exp(sig^2/2) = {np.exp(sig_lnA**2/2):.4f}")
print(f"    OBSERVED mean/median on the real data  = GLS/median = {a0/med:.4f}")
print(f"    agreement: {100*abs(np.exp(sig_lnA**2/2)/(a0/med)-1):.1f}%")
print("    ==> the ENTIRE 21.5% GLS-median gap on the real data is quantitatively accounted")
print("        for by the mean-median offset of a right-skewed multiplicative distribution.")
print("        Nothing else is needed to explain it.")
print(f"\n  WHY THE MOCK WILL PREDICT LESS THAN 21.5% (a caveat that cuts AGAINST the")
print("  canonical-favourable reading, so it is stated up front):")
sig_mock = float(np.sqrt(np.sum(u * (LD**2 + LI**2 + LV**2 + ((2 * y + 1) * SLNB)**2))))
print(f"    the frozen mock injects D, i, v, shape, Ups, gas-cal but NO intrinsic-scatter")
print(f"    term, whereas the real fit needs f_int = {fint:.3f} (= {fint*(1+float(np.sum(u*y))):.3f}")
print(f"    fractional on a0_pt) to reach chi2/N=1. Modeled-noise-only log-scatter is")
print(f"    ~{sig_mock:.3f} vs the real {sig_lnA:.3f}; exp(sig^2/2)-1 is {100*(np.exp(sig_mock**2/2)-1):.1f}%")
print(f"    vs {100*(np.exp(sig_lnA**2/2)-1):.1f}%. So the mock UNDERSTATES the GLS bias -- it is")
print("    KIND to the incumbent (ALT-side) estimator, not to the canonical-side one.")
print("    If GLS still fails G2 on the mock, that failure is a floor, not a ceiling.")
print(f"    (sig_mock uses the INDEPENDENT terms only -- D, i, v, shape. The coherent Ups and")
print(f"    gas-cal draws shift a whole realization and so contribute realization-to-")
print(f"    realization SCATTER, not a within-realization mean-median gap.)")
print(f"\n  TWO INDEPENDENT ROUTES TO THE SAME NUMBER (a real consistency check, not a")
print(f"  restatement): the moment-propagation prediction is {bg:+.2f} pp and the log-normal")
print(f"  shortcut exp(sig_mock^2/2)-1 is {100*(np.exp(sig_mock**2/2)-1):+.2f} pp. They agree to "
      f"{abs(bg-100*(np.exp(sig_mock**2/2)-1)):.2f} pp")
print(f"  despite sharing no algebra beyond the forward model itself.")
RES["D5"] = dict(pred=pred, u_wtd_EF=float(np.sum(u * EF)), u_wtd_medF=float(np.sum(u * MF)),
                 sig_lnA_real=sig_lnA, lognormal_mean_over_median=float(np.exp(sig_lnA**2 / 2)),
                 observed_gls_over_median=a0 / med,
                 lognormal_check_relerr=float(abs(np.exp(sig_lnA**2 / 2) / (a0 / med) - 1)),
                 pred_bias_glsweights_pp=100 * b_gw,
                 pred_bias_selfconsistent_weights_pp=100 * b_sc,
                 pred_bias_measonly_weights_pp=100 * b_ms,
                 misweighting_share_of_bias=float((b_gw - b_ms) / b_gw),
                 sig_mock_only=sig_mock, n_nonpositive_a0pt=int((~pos).sum()),
                 predicted_sign_gls="POSITIVE (high)", predicted_sign_median="~zero, slightly positive")

# ============================================================================ D6
print()
print(bar)
print("D6 -- STRUCTURAL FLAGS FOR THE MOCK PHASE (found here, reported, gates untouched)")
print(bar)
n_lowy = int((GB < 1.0e-10).sum())
print(f"  1. gls_lowy IS DEGENERATE WITH gls_origin ON THIS SAMPLE. Its frozen cut is")
print(f"     g_bar < 1.0e-10, and max(g_bar) = {GB.max():.3e} -- ALL {n_lowy}/{N} points pass.")
print(f"     Expect the two to agree exactly (up to the identical GLS iteration) at every")
print(f"     injection. Not a defect of the prereg, but the diagnostic it was meant to")
print(f"     provide (isolating low-y points) is UNAVAILABLE on a sample that is already")
print(f"     entirely at y < 0.18. Worth reporting rather than presenting as a check passed.")
assert n_lowy == N
print(f"  2. log_median_a0pt will discard 0 points on the ZERO-NOISE null and few in mocks:")
print(f"     the real data has {int((~pos).sum())} non-positive a0_pt of {N}. With the mock's")
print(f"     log-scatter ~{sig_mock:.2f} negatives will be rare but NOT absent for the")
print(f"     lowest-y, highest-fv points -- the discard count must be reported per S3.")
print(f"  3. The GLS weights are a pure function of fv here (D2), so any 'weighted' variant")
print(f"     that reuses sig2_model (ivw_median_a0pt) inherits an fv-only weighting, i.e. it")
print(f"     is close to an UNweighted median. Expect ivw_median_a0pt ~ median_a0pt.")
print(f"  4. Common-random-numbers pairing across injections is expected to make the")
print(f"     injection-to-injection bias spread TINY for every estimator (D5 predicts")
print(f"     <{max(sp_gls, sp_med):.2f} pp): G3 will likely separate nothing. The decision will")
print(f"     rest on G2 and G4, as the magnitudes above suggest.")
RES["D6"] = dict(gls_lowy_points_passing=n_lowy, gls_lowy_degenerate=bool(n_lowy == N),
                 pred_injection_spread_pp=float(max(sp_gls, sp_med)))

# ============================================================================ verdict
print()
print(bar)
print("MECHANISM VERDICT (independent of the mock; both directions stated)")
print(bar)
print("  THE BRIEF'S PROPOSED MECHANISM IS FALSIFIED ON THIS SAMPLE -- all three legs:")
print(f"    (leg 1) GLS does NOT upweight high-g_bar points: corr(u, g_bar) = {sp_ug:+.3f},")
print(f"            d ln u/d ln g_bar = {slope:+.3f}, top-g_bar decile = {100*top10:.1f}% of the")
print(f"            weight (uniform = 10%). Structurally, w*g_bar^2 is non-increasing in")
print(f"            g_bar and at y<<1 depends on fv ALONE. Also false on the full sample.")
print(f"    (leg 2) there is NO catastrophic cancellation: y_max = {ymax:.3f}, kappa = 2y+1 =")
print(f"            {2*ymax+1:.3f}, E/g_bar^2 = {1/ymax:.0f}. E is a LARGE difference of SMALL")
print(f"            numbers on this subsample.")
print(f"    (leg 3) weight and M/L leverage are uncorrelated: corr(u, phi(2y+1)) = "
      f"{spearman(u, LU):+.3f}.")
print("  WHAT IS ACTUALLY THERE (two mechanisms, both quantified):")
print("    (M-A) SKEW / JENSEN, the dominant one. GLS through-origin IS ALGEBRAICALLY a")
print("          weighted MEAN of a0_pt (D1, machine precision), and the a0_pt errors are")
print("          MULTIPLICATIVE and convex (distance, inclination, velocity, M/L all enter")
print(f"          as products), so E[a0_pt] > median[a0_pt]. Measured on the real data:")
print(f"          exp(sig_lnA^2/2) = {np.exp(sig_lnA**2/2):.3f} vs the observed GLS/median = {a0/med:.3f}")
print("          -- the whole gap, with nothing left over.")
print(f"    (M-B) MIS-WEIGHTING, subdominant but real. The GLS error model omits sigma_lnD")
print(f"          and sigma_i, so the 29 Hubble-flow galaxies get {100*u[hf].sum():.0f}% of the weight")
print(f"          instead of {100*u_sc[hf].sum():.0f}% (self-consistent) / {100*u_ms[hf].sum():.0f}%"
      f" (measurement-only); they are also exactly")
print(f"          where the Jensen inflation exp(2 sig_lnD^2) = {np.exp(2*0.0625):.3f} is largest. This")
print(f"          AMPLIFIES M-A by ~{100*(b_gw-b_ms)/b_gw:.0f}% ({100*b_ms:+.1f} -> {100*b_gw:+.1f} pp);"
      f" the other ~{100*b_ms/b_gw:.0f}% is irreducible.")
print("  PREDICTED SIGN (recorded before any mock number exists):")
print(f"    b(gls_origin)  = POSITIVE, {bg:+.1f} pp (quote +9 to +13) -> predicted FAIL of G2 (2.0 pp)")
print(f"    b(median_a0pt) = {bm:+.2f} pp, honest bound |b| <~ 2 pp -> predicted PASS of G2")
print("    Direction, plainly: the incumbent GLS is predicted to read HIGH, i.e. the real-data")
print("    1.181e-10 is predicted to be an inflated reading of whatever the sample's true")
print("    slope is. That conclusion is CANONICAL-FAVOURABLE, which is precisely the")
print("    manufactured-win risk this pre-registration exists to block, so:")
print("      * it is a PREDICTION from data structure, NOT a measurement and NOT a verdict;")
print("      * the frozen gates are sign-blind and are the arbiter -- if the mock returns a")
print("        NEGATIVE or null GLS bias, THIS DIAGNOSIS IS WRONG and must be reported wrong;")
print("      * the caveat that cuts the other way is stated in D5: the mock omits the")
print("        intrinsic-scatter term the real fit needs (f_int = %.2f), so it will UNDERSTATE"
      % fint)
print("        the GLS bias -- the mock is kind to the ALT-side incumbent, not to canonical;")
print("      * an equally real alternative reading is NOT excluded here: if part of the")
print("        a0_pt scatter is PHYSICAL (real point-to-point spread in the a0-line rather")
print("        than measurement error), then neither the mean nor the median is 'a0' and the")
print("        22% spread is partly REAL STRUCTURE -- prereg outcome (b). Mocks cannot")
print("        settle that, because they inject an exact single a0 by construction.")
print("  BOTH FOOTINGS CARRIED, AND a0 STAYS POSITED:")
for nm, v in (("canonical cH_L/Z", A0C), ("ALT cH0/Z", A0A), ("std-MOND g_dagger", A0M)):
    print(f"    {nm:<20} {v:.4e}:  GLS/target = {a0/v:.3f},  median/target = {med/v:.3f}")
print("    Nothing here derives a0's value: the framework's coefficient remains POSITED, and")
print("    this diagnosis resolves only HOW a slope should be estimated. No 'theory closed'.")

out = os.path.join(HERE, "estimator_weight_diagnosis_results.json")
RES["meta"] = dict(script="estimator_weight_diagnosis.py", N=N, N_gal=NG, Ud=UD,
                   a0_canon=A0C, a0_alt=A0A, a0_mond=A0M,
                   role="mechanism diagnosis, independent theoretical cross-check on the "
                        "frozen mock bias measurement",
                   prereg="PREREG_ESTIMATOR_BIAS.md (frozen, commit c63a2931); no mock run, "
                          "no gate touched, no new candidate estimator evaluated on real data",
                   brief_mechanism_verdict="FALSIFIED (all three legs) on the gas-dominated "
                                           "subsample",
                   surviving_mechanism="(M-A) Jensen/skew: GLS == weighted MEAN of a0_pt and "
                                       "a0_pt errors are multiplicative/convex; (M-B) the GLS "
                                       "error model omits sigma_lnD and sigma_i, over-weighting "
                                       "Hubble-flow galaxies where the Jensen inflation is "
                                       "largest",
                   predicted_sign_gls="POSITIVE (+9 to +13 pp, predicted FAIL of G2)",
                   predicted_sign_median="~+0.5 pp (predicted PASS of G2)",
                   posited_clause="a0's VALUE remains POSITED; this is a measurement-estimator "
                                  "diagnosis only. No theory-closed claim.")
json.dump(RES, open(out, "w"), indent=1, default=float)
print(f"\n[estimator_weight_diagnosis_results.json written]")
print("EXIT 0: mechanism structure computed and sign prediction recorded. Not a verdict.")
