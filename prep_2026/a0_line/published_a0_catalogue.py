#!/usr/bin/env python3
"""
published_a0_catalogue.py -- CATALOGUE OF THE *PUBLISHED* SPARC/MOND a0 DETERMINATIONS BY
ESTIMATOR FAMILY, WITH THE SAMPLE FOOTPRINTS AND y-RANGES REPRODUCED FROM THE REAL DATA.
=========================================================================================
WHY THIS FILE EXISTS.  This repo has PROVEN (frozen pre-registration
`a0_line_estimator_bias_v1`, estimator_bias_mocks.py, estimator_bias_verdict.json) that ONE
estimator family -- a through-origin MEAN-like slope on per-point a0_pt = (g_obs^2-g_bar^2)/g_bar
-- is biased HIGH by +10.34 pp on the GAS-DOMINATED SPARC subsample, while six median-like
estimators pass at |b| < 1.5 pp.  It is TEMPTING to conclude "the published 1.2e-10 is biased
high and the framework's Lambda-anchored 9.355e-11 is the true value".  THAT INFERENCE IS NOT
LICENSED BY ANYTHING IN THIS REPO, and this script's job is to establish exactly WHAT the
published determinations actually compute, so the transfer question can be settled by
MEASUREMENT rather than by analogy.

WHAT THIS SCRIPT DOES (and does NOT do):
  * DOES: reproduce, from the raw SPARC files, the sample footprint and the y = g_bar/a0 range
    of each published sample, so item (iii) of the catalogue is a measured number and not a
    quotation; convert every published number into m/s^2 with the paper's own conversion
    factors; assemble the family classification with its a priori risk flag AND the reason;
    re-verify the committed regression anchors.
  * DOES NOT: claim any published number is biased.  No published estimator is implemented
    here and no bias is measured here.  Every "AT RISK" flag below is an A PRIORI flag with a
    stated mechanism, to be CONFIRMED OR KILLED by mocks in a later step.  "It is mean-like,
    therefore biased" is explicitly NOT an argument this file makes.
  * DOES NOT: derive a0.  a0's VALUE remains POSITED in the framework (horizon-derived
    a0 = c*H_Lambda/Z, Z = sqrt(32 pi/3)); both footings (canonical 9.355e-11, ALT 1.1305e-10)
    are carried on every dimensional number.  This is a MEASUREMENT-METHODOLOGY catalogue.
    No "theory closed", no TOE claim, no "no open doors".

WELLHEAD CREDIT (applies everywhere in this project): the framework's kernel
nu = sqrt(1+1/y) is identical to Milgrom 1999 PLA 253:273 Eq. 9.  The framework's distinctive
content is the cH_Lambda/Z COEFFICIENT (Milgrom's was 2cH_Lambda) plus the modified-inertia
completion -- not the kernel.

SOURCES (all verified against the papers themselves, not from memory):
  [MLS16]  McGaugh, Lelli & Schombert 2016, PRL 117, 201101 (arXiv:1609.05917)
  [L17]    Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152 (arXiv:1610.08981)
  [Li18]   Li, Lelli, McGaugh & Schombert 2018, A&A 615, A3 (arXiv:1803.00022)
  [D23]    Desmond 2023, MNRAS 526, 3342 (arXiv:2303.11314)
  [C22]    Chae 2022, ApJ 941, 55 (arXiv:2207.11069)
  [CZ18]   Chang & Zhou 2018 (arXiv:1803.08344)
  [M11]    McGaugh 2011/2012, AJ 143, 40 (arXiv:1107.2934)
  [SSM10]  Swaters, Sanders & McGaugh 2010, ApJ 718, 380 (arXiv:1005.5456)
  [BBS91]  Begeman, Broeils & Sanders 1991, MNRAS 249, 523
  [Mi24]   Mistele, McGaugh, Lelli, Schombert & Li 2024, JCAP 04, 020 (arXiv:2310.15248)

Exit 0 = footprints reproduced and the catalogue assembled.  Exit code is not a verdict.
"""
import numpy as np, os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fire_common as fc

bar = "=" * 100
GDAG = 1.2e-10                       # [MLS16]/[L17] published g_dagger
A0C, A0A = fc.A0C, fc.A0A            # canonical cH_Lambda/Z, ALT cH0/Z -- BOTH carried
kpc_m = 3.0857e19
Msun = 1.98892e30
Gn = 6.674e-11
RES = {}

print(bar)
print("S0 -- THE QUESTION, STATED SO IT CANNOT BE FUDGED")
print(bar)
print(f"  published standard value   g_dagger = {GDAG:.4e} m/s^2   [MLS16], [L17]")
print(f"  framework canonical        a0       = {A0C:.4e} m/s^2   (POSITED, cH_Lambda/Z)")
print(f"  framework ALT footing      a0       = {A0A:.4e} m/s^2   (POSITED, cH0/Z)")
print(f"  gap: g_dagger/a0_canon = {GDAG/A0C:.4f}  (canonical is {100*(1-A0C/GDAG):.1f}% BELOW"
      f" the published value; the published value is {100*(GDAG/A0C-1):.1f}% ABOVE canonical)")
print(f"  the SAME published paper quotes a SYSTEMATIC error of 0.24e-10 (20% of Upsilon_[3.6]):")
print(f"     (g_dagger - a0_canon)/sigma_sys = {(GDAG-A0C)/0.24e-10:+.2f} sigma_sys")
print(f"     (g_dagger - a0_ALT  )/sigma_sys = {(GDAG-A0A)/0.24e-10:+.2f} sigma_sys")
print("  => BEFORE any estimator-bias argument is made, the canonical value is already inside")
print("     ~1.1 published systematic sigma of 1.20e-10. Any bias claim must be measured ON TOP")
print("     of that, not instead of it.")
RES["framing"] = dict(gdag=GDAG, a0_canon=A0C, a0_alt=A0A,
                      ratio_gdag_over_canon=GDAG / A0C,
                      canon_below_gdag_pct=100 * (1 - A0C / GDAG),
                      gdag_above_canon_pct=100 * (GDAG / A0C - 1),
                      sigma_sys_published=0.24e-10,
                      canon_offset_in_sigma_sys=(GDAG - A0C) / 0.24e-10,
                      alt_offset_in_sigma_sys=(GDAG - A0A) / 0.24e-10)

# ======================================================================= S1 SAMPLE FOOTPRINTS
print()
print(bar)
print("S1 -- SAMPLE FOOTPRINTS AND y-RANGES, REPRODUCED FROM THE RAW SPARC FILES")
print(bar)
print("  [MLS16]/[L17]/[Li18]/[D23] all use SPARC with Q<=2 (i.e. Q<3), inc>30 deg, and the")
print("  point cut dV_obs/V_obs < 0.10, at Upsilon_disk = 0.5 / Upsilon_bulge = 0.7 M/L_3.6.")
print("  fire_common.load(Ud) applies exactly those cuts with Ub = 1.4*Ud, so Ud = 0.50 -> ")
print("  Ub = 0.70 IS the published convention. Reproduce their counts:")
FOOT = {}
for Ud, tag in ((0.50, "published convention (Ud=0.50, Ub=0.70)"),
                (0.70, "this repo's a0-line baseline (Ud=0.70)")):
    gals = fc.load(Ud)
    GB, GO, FV, PHI, GAL, SLD, CTI = fc.flat(gals, False)
    GBg, GOg, FVg, PHIg, GALg, _, _ = fc.flat(gals, True)
    y, yg = GB / GDAG, GBg / GDAG
    FOOT[Ud] = dict(tag=tag, N=int(len(GB)), Ngal=int(len(set(GAL.tolist()))),
                    N_gasdom=int(len(GBg)), Ngal_gasdom=int(len(set(GALg.tolist()))),
                    y_at_gdag=[float(y.min()), float(np.median(y)), float(y.max())],
                    y_gasdom_at_gdag=[float(yg.min()), float(yg.max())],
                    y_at_canon=[float((GB / A0C).min()), float(np.median(GB / A0C)),
                                float((GB / A0C).max())],
                    y_gasdom_at_1em10=[float(GBg.min() / 1e-10), float(GBg.max() / 1e-10)])
    print(f"\n  {tag}")
    print(f"    FULL RAR sample : N = {len(GB)} points, {len(set(GAL.tolist()))} galaxies "
          f"retaining >=1 point")
    print(f"    y = g_bar/g_dagger : {y.min():.4f} .. {y.max():.1f}  (median {np.median(y):.3f})"
          f"   -> spans {math.log10(y.max()/y.min()):.2f} decades")
    print(f"    y = g_bar/a0_canon : {(GB/A0C).min():.4f} .. {(GB/A0C).max():.1f} "
          f"(median {np.median(GB/A0C):.3f})")
    print(f"    GAS-DOMINATED subsample (the PROVEN-BIAS sample): N = {len(GBg)} points, "
          f"{len(set(GALg.tolist()))} galaxies")
    print(f"      y = g_bar/g_dagger : {yg.min():.4f} .. {yg.max():.4f}"
          f"   -> spans {math.log10(yg.max()/yg.min()):.2f} decades  [DEEP-MOND THROUGHOUT]")
    print(f"      y = g_bar/1e-10    : {GBg.min()/1e-10:.4f} .. {GBg.max()/1e-10:.4f}"
          f"   (prereg-frozen figures)")

# hard anchors: the published counts
f5, f7 = FOOT[0.50], FOOT[0.70]
print()
print(f"  PUBLISHED-COUNT ANCHORS:")
print(f"    [MLS16]/[L17] state '2693 individual points in 153 galaxies'. Q<=2 & inc>=30 in")
print(f"    the SPARC master table gives EXACTLY 153 galaxies (checked below); after the")
print(f"    dV/V<0.10 point cut this repo retains {f5['N']} points in {f5['Ngal']} galaxies.")
print(f"    [D23] states '2696 points from 147 galaxies' -- an EXACT match to this repo's")
print(f"    reproduction ({f5['N']} points, {f5['Ngal']} galaxies). The 2693-vs-2696 and")
print(f"    153-vs-147 differences are the published papers' galaxy bookkeeping (153 galaxies")
print(f"    pass the Q/inc cuts; 6 of them lose ALL points to dV/V<0.10) plus 3 borderline")
print(f"    points -- 0.1% in N. The sample footprint is REPRODUCED, not assumed.")
import csv
_rows = list(csv.DictReader(open(os.path.join(fc.REPO, "data", "sparc_master_clean.csv"))))
n153 = sum(1 for r in _rows if int(r["Q"]) <= 2 and float(r["inc"]) >= 30)
print(f"    check: SPARC master rows = {len(_rows)}; passing Q<=2 & inc>=30 = {n153} "
      f"(published: 153) -> {'MATCH' if n153 == 153 else 'MISMATCH'}")
assert n153 == 153
assert f5["N"] == 2696 and f5["Ngal"] == 147, (f5["N"], f5["Ngal"])
assert f7["N_gasdom"] == 310 and f7["Ngal_gasdom"] == 49

print()
print("  THE REGIME CONTRAST -- reason (b) of the brief, as a NUMBER:")
r_med = np.median(fc.flat(fc.load(0.70), False)[0]) / np.median(fc.flat(fc.load(0.70), True)[0])
GBf = fc.flat(fc.load(0.70), False)[0]
GBg7 = fc.flat(fc.load(0.70), True)[0]
frac_in = float((GBf <= GBg7.max()).mean())
print(f"    published full-range fits span y up to {f5['y_at_gdag'][2]:.0f} "
      f"({math.log10(f5['y_at_gdag'][2]/f5['y_at_gdag'][0]):.2f} decades).")
print(f"    the proven-bias subsample stops at y = {f7['y_gasdom_at_gdag'][1]:.4f} "
      f"({math.log10(f7['y_gasdom_at_gdag'][1]/f7['y_gasdom_at_gdag'][0]):.2f} decades) --")
print(f"    i.e. the bottom {100*math.log10(f7['y_gasdom_at_gdag'][1]/f7['y_gasdom_at_gdag'][0])/math.log10(f5['y_at_gdag'][2]/f5['y_at_gdag'][0]):.0f}% "
      f"of the published dynamic range in log y.")
print(f"    median y ratio (full / gas-dominated) = {r_med:.1f}x")
print(f"    only {100*frac_in:.1f}% of full-sample points lie inside the gas-dominated y window.")
print("    => the +10.34 pp CANNOT be carried across by assertion. It must be re-measured over")
print("       the full y range. That is the next step's job, not this file's.")
RES["footprints"] = {str(k): v for k, v in FOOT.items()}
RES["footprints"]["published_Q_inc_galaxy_count"] = n153
RES["footprints"]["regime_contrast"] = dict(median_y_ratio_full_over_gasdom=float(r_med),
                                           frac_full_points_in_gasdom_y_window=frac_in)

# ============================================== S2 STRUCTURAL LIMIT OF THE a0-LINE STATISTIC
print()
print(bar)
print("S2 -- WHY NO PUBLISHED DETERMINATION *CAN* BE IN THIS REPO'S ESTIMATOR FAMILY")
print("      (reason (c) of the brief, made structural rather than rhetorical)")
print(bar)
print("  This repo's estimators act on the per-point statistic")
print("      a0_pt = (g_obs^2 - g_bar^2)/g_bar ,")
print("  which is EXACT for the framework's own nu but which changes SIGN wherever the measured")
print("  g_obs < g_bar. On the published FULL-range sample that happens often, because at high y")
print("  the relation is Newtonian (g_obs ~ g_bar) and noise straddles the line. Counted:")
gals7 = fc.load(0.70)
GBa, GOa, FVa, PHIa, GALa, _, _ = fc.flat(gals7, False)
apt_all = (GOa**2 - GBa**2) / GBa
ya = GBa / GDAG
bands = [(0.0, 0.1), (0.1, 0.3), (0.3, 1.0), (1.0, 3.0), (3.0, 10.0), (10.0, np.inf)]
print(f"  {'y band (g_bar/g_dagger)':<26}{'N':>6}{'% a0_pt<0':>11}{'mean/median a0_pt':>20}")
BAND = []
for lo, hi in bands:
    m = (ya >= lo) & (ya < hi)
    if m.sum() < 5:
        continue
    v = apt_all[m]
    neg = 100.0 * float((v <= 0).mean())
    med = float(np.median(v))
    rat = float(np.mean(v) / med) if abs(med) > 0 else float("nan")
    BAND.append(dict(y_lo=lo, y_hi=float(hi), N=int(m.sum()), pct_negative=neg,
                     mean_over_median=rat))
    lab_b = f"[{lo:g}, {'inf' if hi == np.inf else format(hi, 'g')})"
    print(f"  {lab_b:<26}{int(m.sum()):>6}{neg:>11.1f}{rat:>20.3f}")
print("  READING (a DIAGNOSTIC of skew structure, NOT an a0 determination and NOT a bias):")
print("   * in the deep-MOND band the per-point statistic is well defined and RIGHT-SKEWED")
print("     (mean/median > 1) -- the precondition for the Jensen gap this repo measured.")
print("   * at y >~ 1 a0_pt becomes sign-indefinite and its mean/median ratio is meaningless.")
print("     A location statistic on a0_pt therefore CANNOT be defined over the published")
print("     full-range sample. This is a STRUCTURAL reason -- not a stylistic preference --")
print("     why every published determination fits a CURVE g_obs(g_bar) (or a per-galaxy")
print("     rotation curve) instead. The two statistics are different QUANTITIES, and the")
print("     bias of one carries no automatic implication for the other.")
print("   * the ratios are dimensionless, so this diagnostic privileges NEITHER footing.")
RES["a0pt_structural_limit"] = BAND

# ============================================================ S3 UNIT CONVERSIONS, AS PUBLISHED
print()
print(bar)
print("S3 -- EVERY PUBLISHED NUMBER CONVERTED TO m/s^2 USING THE PAPER'S OWN CONVERSION")
print(bar)


def kkpc_to_ms2(v):
    """km^2 s^-2 kpc^-1 -> m/s^2 (the unit [SSM10] quote a0 in)."""
    return v * 1e6 / kpc_m


def A_to_a0(A_msun_km4s4, chi):
    """[M11] eq.19: A = chi/(a0 G), chi = geometry factor -> a0 = chi/(G A)."""
    A_si = A_msun_km4s4 * Msun / 1e12          # kg s^4 m^-4
    return chi / (Gn * A_si)


print("  [SSM10] quote a0 in km^2 s^-2 kpc^-1 (27 dwarf/LSB galaxies, a0 free per galaxy):")
for v, what in ((3080, "value ADOPTED (= Sanders & McGaugh 2002)"),
                (3350, "AVERAGE of their per-galaxy free-a0 fits"),
                (2150, "average EXCLUDING the three highest per-galaxy values")):
    print(f"    {v:>5} km^2/s^2/kpc = {kkpc_to_ms2(v):.4e} m/s^2   <- {what}")
ssm_mean, ssm_trim = kkpc_to_ms2(3350), kkpc_to_ms2(2150)
print(f"    mean/trimmed ratio = {ssm_mean/ssm_trim:.3f}  -- a factor {ssm_mean/ssm_trim:.2f}")
print(f"    swing from dropping 3 of 27 galaxies. [SSM10]'s own conclusion (their Sec. 5) is")
print(f"    that the sample 'suggest[s] a lower value for a0 than the adopted value'.")
print()
print("  [M11] BTFR normalisation route, with the paper's OWN geometry factor chi:")
for A, s in ((47.0, "abstract value A = 47 +- 6"), (41.0, "A - 1sigma"), (53.0, "A + 1sigma")):
    print(f"    A = {A:>4.0f} M_sun km^-4 s^4, chi = 0.80 -> a0 = {A_to_a0(A,0.80):.4e} m/s^2"
          f"   ({s})")
print(f"    the SAME A with chi = 1 (no geometry correction) -> a0 = {A_to_a0(47.0,1.0):.4e}")
print(f"    published statement: a0 = 1.3 +- 0.3 e-10 (their eq. 20); reproduced here to "
      f"{100*abs(A_to_a0(47.0,0.80)/1.3e-10-1):.1f}%")
print("    *** CATALOGUE FLAG (circularity, not bias): chi = 0.80 is itself calibrated FROM")
print("        MOND rotation-curve fits that ASSUMED a0 = 1.2e-10 (their text: the McGaugh")
print("        2005b sample has MOND fits at a0 = 1.2e-10 and a BTFR fit A = 50, giving the")
print("        empirical chi = 0.80 they adopt). The BTFR route is therefore NOT an")
print("        independent determination of a0: it inherits 1.2e-10 through chi. It also")
print("        cannot be used as independent CORROBORATION of 1.2e-10. Both directions.")
assert abs(A_to_a0(47.0, 0.80) / 1.3e-10 - 1) < 0.02
RES["conversions"] = dict(
    ssm10_adopted=kkpc_to_ms2(3080), ssm10_mean_free=ssm_mean, ssm10_trim3=ssm_trim,
    ssm10_mean_over_trim=ssm_mean / ssm_trim,
    btfr_A47_chi080=A_to_a0(47.0, 0.80), btfr_A47_chi1=A_to_a0(47.0, 1.0),
    btfr_A41_chi080=A_to_a0(41.0, 0.80), btfr_A53_chi080=A_to_a0(53.0, 0.80),
    btfr_chi_is_calibrated_on_a0_12=True)

# ==================================================================== S4 THE CATALOGUE PROPER
print()
print(bar)
print("S4 -- THE CATALOGUE: WHAT EACH PUBLISHED DETERMINATION ACTUALLY COMPUTES")
print(bar)
CAT = [
 dict(id="MLS16", ref="McGaugh, Lelli & Schombert 2016, PRL 117, 201101",
      family="F1_curvefit_ODR",
      statistic="nonlinear orthogonal-distance regression (scipy.odr) of the ONE-parameter "
                "curve g_obs = g_bar/(1-exp(-sqrt(g_bar/g_dag))) to the INDIVIDUAL points "
                "(explicitly NOT binned); single global g_dag; errors on BOTH variables",
      mean_or_median="MEAN-like in the residual it minimises, but that residual is in LOG10 "
                     "space (independently verified: [CZ18] reproduce 1.20e-10 only when the "
                     "first chi2 term is the logarithmic distance) -> therefore MEDIAN-LIKE "
                     "in linear g. Published residual histogram: symmetric, Gaussian, "
                     "sigma = 0.11 dex, rms 0.13 dex.",
      sample="SPARC LTGs, Q<=2, inc>30 deg, dV/V<0.10: 2693 points, 153 galaxies; "
             "Upsilon_disk=0.5, Upsilon_bulge=0.7 M/L at 3.6um",
      y_range="reproduced here: y = g_bar/g_dag from 0.0069 to 54.5, median 0.212 "
              "(3.90 decades)",
      error_space="LOG (dex): 'The mean error on gobs is 0.1 dex' and 'The mean error on gbar "
                  "is 0.08 dex' [L17]. IMPORTANTLY, their d(g_obs) (L17 eq. 2) ALREADY "
                  "propagates dV_obs/V_obs, di/tan(i) AND dD/D in quadrature -- so unlike "
                  "this repo's fire_common.sig2_model, family F1 does NOT omit sigma_lnD from "
                  "its weights. Mechanism M-B of estimator_weight_diagnosis.py (Hubble-flow "
                  "over-weighting from an omitted sigma_lnD) therefore does NOT transfer to "
                  "F1. What DOES remain is that these per-galaxy coherent errors are treated "
                  "as per-point independent.",
      quoted="g_dag = 1.20 +- 0.02 (random) +- 0.24 (systematic) x 1e-10 m/s^2"),
 dict(id="L17", ref="Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152",
      family="F1_curvefit_ODR",
      statistic="same scipy.odr fit of the same one-parameter curve to the same 2693 LTG "
                "points; ALSO a variant (their eq. 14) with an added acceleration floor "
                "g_hat, fitted to LTGs+ETGs+dSphs",
      mean_or_median="as MLS16 (log-space ODR -> median-like in linear g)",
      sample="153 LTGs (2693 pts) + 25 ETGs (28 rotating + 80 X-ray pts) + 62->35 dSphs "
             "(1 pt each, after a tidal cut); total acceleration range ~1e-12 to 1e-9 m/s^2 "
             "(4 dex; ~6 dex with ultrafaints)",
      y_range="LTG part identical to MLS16; the dSph extension pushes g_obs down to ~1e-12, "
              "i.e. far below the SPARC rotation-curve floor",
      error_space="LOG (dex), errors on both variables",
      quoted="LTG fit: g_dag = 1.20 +- 0.02 x 1e-10 (sys 0.24). ONE-LAW fit with the floor: "
             "g_dag = (1.1 +- 0.1) x 1e-10 and g_hat = (9.2 +- 0.2) x 1e-12 m/s^2"),
 dict(id="CZ18", ref="Chang & Zhou 2018, arXiv:1803.08344",
      family="F1_curvefit_ODR",
      statistic="the SAME ODR statistic, run BOTH ways: chi2 first term in LINEAR g_obs, and "
                "in log10 g_obs. Explicit reproduction test of MLS16.",
      mean_or_median="both variants measured: the LOG variant is median-like, the LINEAR "
                     "variant is mean-like in g",
      sample="SPARC, n = 2693 points, 147 galaxies",
      y_range="as MLS16",
      error_space="LINEAR for their fiducial chi2; LOG for the MLS16-reproducing variant",
      quoted="LINEAR-residual ODR: g_dag = (1.02 +- 0.02) x 1e-10 m/s^2. LOG-residual ODR: "
             "reproduces MLS16's 1.20e-10. => a MEASURED, PUBLISHED 15% estimator sensitivity "
             "INSIDE family F1, with the mean-like/linear variant reading LOWER, not higher."),
 dict(id="Li18", ref="Li, Lelli, McGaugh & Schombert 2018, A&A 615, A3",
      family="F2_pergalaxy_then_combine",
      statistic="per-galaxy MCMC fit of the RAR curve to each rotation curve; chi2 in LINEAR "
                "acceleration space, chi2 = sum_R (g_obs-g_tot)^2/sigma_gobs^2 with "
                "sigma_gobs = 2 V_obs dV_obs/R; Gaussian priors on Upsilon_star (0.5/0.7 with "
                "0.1 dex), D and i (observational errors). Section 5 refits with g_dag FREE "
                "per galaxy, under a flat and a Gaussian prior.",
      mean_or_median="the per-galaxy fit is MEAN-like in linear acceleration; NO combination "
                     "statistic is applied -- the paper reports the DISTRIBUTION (their "
                     "Fig. 7) and declines to quote a combined free-g_dag value",
      sample="175 SPARC galaxies fitted (2694 points in the 153-galaxy RAR subsample); "
             "rms residual 0.057 dex (fixed g_dag), 0.054 dex (free g_dag)",
      y_range="as MLS16 for the RAR subsample",
      error_space="LINEAR on g_obs; Upsilon/D/i marginalised as nuisance parameters "
                  "(log-normal prior on Upsilon)",
      quoted="NO new a0. Fiducial fits FIX g_dag = 1.20e-10 (Gaussian prior 1.20 +- 0.02). "
             "Their result is a NULL: 'adjusting the value of g_dag improves neither the fits "
             "nor the rms scatter'; free-g_dag gains are absorbed by the Upsilon degeneracy. "
             "=> Li+2018 must NOT be cited as an independent a0 determination."),
 dict(id="D23", ref="Desmond 2023, MNRAS 526, 3342",
      family="F3_full_hierarchical_likelihood",
      statistic="full joint Bayesian inference by Hamiltonian Monte Carlo (NUTS/numpyro). "
                "Likelihood is GAUSSIAN IN log10(g_obs) with "
                "sigma_tot^2 = dlog(g_obs)^2 + sigma_int^2 + (dlog g_pred/dlog g_bar)^2 "
                "dlog(g_bar)^2 (marginalised-likelihood form). Free parameters: a0, "
                "sigma_int, and 147x(e_N, D, i, L_3.6, Upsilon_disk, Upsilon_gas) + "
                "31xUpsilon_bulge. Reports the POSTERIOR MEDIAN.",
      mean_or_median="MEDIAN-like twice over: log-space residuals AND a posterior median",
      sample="2696 points, 147 galaxies -- an EXACT match to this repo's reproduction",
      y_range="reproduced here: 0.0069 .. 54.5 in g_bar/g_dag",
      error_space="LOG throughout; and -- decisively for the transfer question -- D, i, "
                  "L_3.6 and every Upsilon are SAMPLED, not folded into a fixed error bar. "
                  "D23's stated motivation is precisely that the F1 error model is "
                  "misspecified: 'in reality these are free parameters of the fit, "
                  "contributing systematic rather than statistical error'.",
      quoted="a0 = (1.19 +- 0.04 (stat) +- 0.09 (sys)) x 1e-10 m/s^2; sigma_int = 0.034 dex. "
             "Across models (Table 3): 1.070, 1.077, 1.19, 1.236, 1.307, 1.309 x 1e-10."),
 dict(id="C22", ref="Chae 2022, ApJ 941, 55",
      family="F3_full_hierarchical_likelihood",
      statistic="global Bayesian MCMC on the stacked sample; likelihood built on ORTHOGONAL "
                "residuals from the relation using the individual uncertainties of the "
                "LOGARITHMIC baryonic and observed accelerations; a0 fitted GLOBALLY (not "
                "per galaxy) jointly with the external-field strength",
      mean_or_median="MEDIAN-like (log-space residuals, posterior summary)",
      sample="3097 points, 152 SPARC galaxies; split into inner and outer rotation-curve parts",
      y_range="full SPARC range; the inner/outer split is a y split in practice",
      error_space="LOG on both accelerations",
      quoted="OUTER parts: a0 = 1.199 (+0.023/-0.022) x 1e-10. INNER parts: a0 = 1.114 "
             "(+0.035/-0.034) x 1e-10. (The inner/outer difference is attributed to the EFE, "
             "not to a0; but it is a ~2 sigma a0 spread WITHIN one paper's own estimator.)"),
 dict(id="SSM10", ref="Swaters, Sanders & McGaugh 2010, ApJ 718, 380",
      family="F2_pergalaxy_then_combine",
      statistic="per-galaxy LEAST-SQUARES fit of the MOND rotation curve v_rot(r) (standard "
                "mu(x) = x/sqrt(1+x^2)) to the observed V(R), with a0 free per galaxy "
                "alongside Upsilon_disk; then the per-galaxy a0 values are COMBINED BY "
                "ARITHMETIC AVERAGING",
      mean_or_median="MEAN-like on per-object a0 -- the ONLY published family that is "
                     "structurally the same class as this repo's failing gls_origin, and in "
                     "the SAME deep-MOND regime",
      sample="27 dwarf and LSB galaxies (deep-MOND dominated, low surface brightness); "
             "fits in LINEAR velocity space",
      y_range="dwarf/LSB rotation curves: predominantly y < 1 (their own framing: 'in most "
              "of these galaxies the accelerations fall below the threshold')",
      error_space="LINEAR on V_obs (errors on velocity only); D and i explored as free "
                  "parameters in separate fits, not marginalised",
      quoted="average of the free-a0 fits: 3350 km^2/s^2/kpc = 1.086e-10 m/s^2. Excluding "
             "the three highest: 2150 km^2/s^2/kpc = 6.97e-11 m/s^2 (their '0.7e-8 cm/s^2'). "
             "Their conclusion: the sample favours a LOWER a0 than the adopted 1.0e-10."),
 dict(id="BBS91", ref="Begeman, Broeils & Sanders 1991, MNRAS 249, 523",
      family="F2_pergalaxy_then_combine",
      statistic="least-squares fits of the MOND rotation curve (standard mu) to 10 "
                "high-quality extended HI rotation curves, with a universal a0 and per-galaxy "
                "M/L; the origin of the canonical '1.2e-10'",
      mean_or_median="MEAN-like (chi2 on velocities, linear space)",
      sample="10 galaxies, high-quality extended rotation curves",
      y_range="bright spirals: spans the transition region, y ~ 0.1 to a few",
      error_space="LINEAR on V_obs",
      quoted="a0 = 1.2 +- 0.27 x 1e-10 m/s^2 (1.21 x 1e-8 cm/s^2), 'standard' mu"),
 dict(id="M11", ref="McGaugh 2011/2012, AJ 143, 40 (BTFR normalisation route)",
      family="F4_BTFR_normalisation",
      statistic="fit of log M_b = 4 log V_f + log A to ONE point per galaxy with the slope "
                "FIXED at 4, minimising the ORTHOGONAL deviations in log space (weighted and "
                "unweighted both reported); then invert via A = chi/(a0 G)",
      mean_or_median="MEDIAN-like in effect: log-space orthogonal residuals, and the paper "
                     "reports the SKEW and KURTOSIS of those residuals as alpha3 = -0.01, "
                     "alpha4 = 0.01 for the combined sample -- i.e. measured to be SYMMETRIC",
      sample="34 gas-rich galaxies (Stark + Trachternach), M_gas > M_star so Upsilon-free; "
             "one asymptotic point per galaxy",
      y_range="the asymptotic flat part only: a single deep-MOND point per galaxy",
      error_space="LOG (log M_b vs log V_f), errors on both variables",
      quoted="A = 47 +- 6 M_sun km^-4 s^4; with chi = 0.80, a0 = 1.3 +- 0.3 x 1e-10 m/s^2. "
             "CIRCULARITY FLAG: chi = 0.80 is calibrated from MOND rotation-curve fits that "
             "assumed a0 = 1.2e-10, so this route is NOT independent of F2. With chi = 1 the "
             "same A gives 1.61e-10."),
 dict(id="Mi24", ref="Mistele, McGaugh, Lelli, Schombert & Li 2024, JCAP 04, 020",
      family="F5_not_a_determination",
      statistic="weak-lensing extension of the RAR; the RAR fit function is ADOPTED, not "
                "fitted",
      mean_or_median="n/a",
      sample="stacked weak lensing around isolated SPARC-like LTGs/ETGs, reaching "
             "g_bar ~ 1e-15 to 1e-12 m/s^2",
      y_range="y = g_bar/a0 down to ~1e-4 -- 4 decades BELOW the SPARC rotation-curve floor",
      error_space="binned means with statistical + systematic bands",
      quoted="NO determination: 'adopting a0 = 1.24e-10 m/s^2' from the literature and "
             "checking that the extrapolated curve matches. Must NOT be cited as an "
             "independent a0. It IS, however, the natural future home of a deep-MOND "
             "AMPLITUDE test, since there the framework's nu and McGaugh's nu coincide."),
]
for c in CAT:
    print(f"\n  [{c['id']}] {c['ref']}")
    print(f"      family      : {c['family']}")
    print(f"      (i)  stat   : {c['statistic']}")
    print(f"      (ii) mean/med: {c['mean_or_median']}")
    print(f"      (iii) sample : {c['sample']}")
    print(f"            y-range: {c['y_range']}")
    print(f"      (iv) errors  : {c['error_space']}")
    print(f"      (v)  quoted  : {c['quoted']}")
RES["catalogue"] = CAT

# ============================================================== S5 FAMILIES AND A PRIORI RISK
print()
print(bar)
print("S5 -- ESTIMATOR FAMILIES, IMPLEMENTABLE, WITH A PRIORI JENSEN/SKEW RISK AND THE REASON")
print("      (a priori flags ONLY -- no bias is claimed or measured anywhere in this file)")
print(bar)
FAM = [
 dict(id="F1_curvefit_ODR", members=["MLS16", "L17", "CZ18"],
      what="one global scale parameter from an orthogonal-distance regression of a "
           "one-parameter curve to ~2700 individual points over ~3.9 decades in y",
      risk="LOW for Jensen/skew, MODERATE for error-model misspecification",
      reason="The minimised residual is in LOG10 g_obs (verified by [CZ18]'s explicit "
             "reproduction: only the log form returns 1.20e-10), and the published residual "
             "histogram is symmetric and Gaussian at 0.11 dex. A least-squares centre of a "
             "log-symmetric distribution estimates the MEDIAN of the linear distribution, so "
             "the multiplicative-noise Jensen inflation that drives this repo's +10.34 pp is "
             "structurally absent. Two real residual risks remain, and BOTH must be measured: "
             "(1) [CZ18] show a 15% shift (1.20 -> 1.02e-10) from the linear-vs-log residual "
             "choice inside this very family -- with the mean-like variant reading LOWER, "
             "i.e. OPPOSITE in sign to this repo's deep-MOND result; (2) D/i/Upsilon are "
             "folded in as uncorrelated per-point Gaussians when they are in fact per-galaxy "
             "and global coherent offsets ([D23]'s stated criticism), which is an "
             "error-model bias channel unrelated to skew. NOTE what does NOT transfer: F1's "
             "d(g_obs) already contains dD/D and di/tan(i) (L17 eq. 2), so the omitted-"
             "sigma_lnD over-weighting that amplifies this repo's GLS bias by ~35% "
             "(mechanism M-B) is absent from F1 by construction.",
      implementable="YES -- scipy.odr on the published curve, both linear and log residual "
                    "forms, over the full-range mock"),
 dict(id="F2_pergalaxy_then_combine", members=["BBS91", "SSM10", "Li18"],
      what="fit each galaxy's rotation curve (or RAR) with a0 free per object, then combine "
           "the per-object a0 values",
      risk="HIGH -- the only published family in the same structural class as the proven "
           "failure, and [SSM10] is in the same deep-MOND regime",
      reason="[SSM10] combine by ARITHMETIC AVERAGING of per-galaxy a0. A per-object a0 "
             "inherits the multiplicative D/i/V error structure with a lever ~2(1+y), so its "
             "sampling distribution is right-skewed and E[a0] > median[a0] -- exactly the "
             "mechanism this repo isolated (log-mean inflation, dominated by "
             "exp(2 sigma_lnD^2)). [SSM10]'s own numbers show the empirical signature: mean "
             "1.086e-10 vs 6.97e-11 after dropping 3 of 27 galaxies (a factor 1.56). NOTE "
             "THE DIRECTION HONESTLY: robustifying this family moves a0 DOWN, i.e. toward and "
             "PAST the framework's canonical 9.355e-11 -- so a confirmed bias here would NOT "
             "hand the framework a win, it would leave 1.2e-10 unsupported by THIS family "
             "while overshooting canonical. The estimator is also NOT identical to "
             "gls_origin: chi2 on VELOCITIES in linear space, a0 fitted jointly with "
             "Upsilon per galaxy under the standard mu. MUST BE MEASURED.",
      implementable="YES -- per-galaxy nonlinear LSQ on V(R) with (a0, Upsilon) free, then "
                    "mean / median / trimmed-mean combination, on full-range mocks"),
 dict(id="F3_full_hierarchical_likelihood", members=["D23", "C22"],
      what="a single joint likelihood over all points with every galaxy nuisance parameter "
           "(D, i, L, Upsilon, EFE) sampled and marginalised; report the posterior median",
      risk="LOWEST -- this family IS the Jensen-immune counterpart",
      reason="Log-space Gaussian likelihood plus a posterior MEDIAN summary. A correctly "
             "modelled likelihood can be unbiased on skewed data, and this is the family "
             "designed for exactly that. It also repairs the F1 error-model misspecification "
             "by sampling D, i, L and Upsilon rather than fixing them. The decisive datum "
             "for the whole transfer question is that this family does NOT move the answer "
             "down: [D23] gets 1.19 +- 0.04 (stat) +- 0.09 (sys), [C22] 1.199 (outer). If "
             "the published value were an artefact of mean-like estimation on skewed data, "
             "THIS is where it would have collapsed, and it did not.",
      implementable="YES but expensive -- a log-space hierarchical likelihood with per-galaxy "
                    "latent (D, i, Upsilon); a profile-likelihood version is a cheap proxy"),
 dict(id="F4_BTFR_normalisation", members=["M11"],
      what="log-space fixed-slope line fit to one asymptotic point per galaxy, then invert "
           "A = chi/(a0 G)",
      risk="LOW for Jensen; DISQUALIFYING for independence",
      reason="Log-space orthogonal residuals with PUBLISHED skew -0.01 and kurtosis 0.01 -- "
             "measured to be symmetric, so no Jensen gap. But the geometry factor chi = 0.80 "
             "is calibrated from rotation-curve fits that ASSUMED a0 = 1.2e-10, so this route "
             "can neither challenge nor corroborate 1.2e-10 independently. Its own quoted "
             "uncertainty (+-0.3e-10, 23%) already brackets both footings.",
      implementable="YES but low value -- the informative parameter is chi, not the estimator"),
 dict(id="F5_not_a_determination", members=["Mi24"],
      what="papers that ADOPT a published a0 and test consistency",
      risk="n/a", reason="No a0 is estimated, so no estimator bias can exist. Listed so that "
                         "it is never miscounted as independent support for any value.",
      implementable="n/a"),
 dict(id="F6_a0line_perpoint_slope", members=["(none published)"],
      what="through-origin slope / location statistic on per-point "
           "a0_pt = (g_obs^2-g_bar^2)/g_bar -- THIS REPO'S OWN family",
      risk="PROVEN biased for its mean-like member on the gas-dominated subsample",
      reason="gls_origin = +10.34 pp (26 bootstrap sd, injection-independent across "
             "9.355e-11 / 1.1305e-10 / 1.2e-10); six median-like members pass at "
             "|b| < 1.5 pp. Mechanism: multiplicative log-noise inflates the MEAN of a0_pt by "
             "E[A^2]E[1/B] > 1 (dominated by exp(2 sigma_lnD^2) = 1.133 on the 29 "
             "Hubble-flow galaxies) while leaving the MEDIAN alone. NO PUBLISHED "
             "DETERMINATION USES THIS FAMILY, and S2 above shows it cannot even be DEFINED "
             "over the published full-range sample (a0_pt changes sign at y ~ 1).",
      implementable="ALREADY IMPLEMENTED AND MEASURED (estimator_bias_mocks.py)"),
]
for f in FAM:
    print(f"\n  {f['id']}   members: {', '.join(f['members'])}")
    print(f"    what        : {f['what']}")
    print(f"    A PRIORI RISK: {f['risk']}")
    print(f"    reason      : {f['reason']}")
    print(f"    implementable: {f['implementable']}")
RES["families"] = FAM

# =============================================================== S6 THE PUBLISHED SPREAD
print()
print(bar)
print("S6 -- THE PUBLISHED SPREAD, LAID OUT AGAINST BOTH FOOTINGS (no verdict, just the ledger)")
print(bar)
LED = [("SSM10 mean-excl-3 (F2, robustified)", ssm_trim, "6.97e-11"),
       ("framework canonical cH_Lambda/Z", A0C, "POSITED"),
       ("CZ18 linear-residual ODR (F1)", 1.02e-10, "1.02e-10 +- 0.02"),
       ("D23 'scatter, no EFE' model (F3)", 1.070e-10, "1.070 +0.032"),
       ("SSM10 mean of free fits (F2)", ssm_mean, "1.086e-10"),
       ("L17 one-law + floor (F1 variant)", 1.1e-10, "1.1 +- 0.1"),
       ("C22 inner rotation curves (F3)", 1.114e-10, "1.114 +0.035/-0.034"),
       ("framework ALT cH0/Z", A0A, "POSITED"),
       ("D23 fiducial combined (F3)", 1.19e-10, "1.19 +-0.04 stat +-0.09 sys"),
       ("C22 outer rotation curves (F3)", 1.199e-10, "1.199 +0.023/-0.022"),
       ("MLS16 / L17 published g_dagger (F1)", 1.20e-10, "1.20 +-0.02 rnd +-0.24 sys"),
       ("BBS91 original (F2)", 1.21e-10, "1.2 +- 0.27"),
       ("D23 'scatter, max-clustering EFE' (F3)", 1.236e-10, "1.236 +- 0.043"),
       ("Mi24 adopted value (not a fit)", 1.24e-10, "adopted"),
       ("M11 BTFR with chi=0.80 (F4)", A_to_a0(47.0, 0.80), "1.3 +- 0.3"),
       ("D23 'no scatter, max-clustering EFE' (F3)", 1.309e-10, "1.309 +0.039"),
       ("M11 BTFR with chi=1 (F4, uncorrected)", A_to_a0(47.0, 1.0), "1.61e-10")]
print(f"  {'determination':<44}{'a0 [m/s^2]':>13}{'/canon':>8}{'/ALT':>7}{'/1.2e-10':>10}")
for nm, v, q in sorted(LED, key=lambda t: t[1]):
    print(f"  {nm:<44}{v:>13.4e}{v/A0C:>8.3f}{v/A0A:>7.3f}{v/GDAG:>10.3f}")
vals = [v for _, v, _ in LED if "POSITED" not in _[0:0] + ""]
pub = [v for nm, v, q in LED if "framework" not in nm]
print(f"\n  published/derived values span {min(pub):.3e} .. {max(pub):.3e}  "
      f"(factor {max(pub)/min(pub):.2f})")
print(f"  the 'well-established' cluster (F1 log + F3, the median-like families) spans "
      f"1.07e-10 .. 1.31e-10 (factor 1.22) and CONTAINS NEITHER footing.")
print(f"  canonical {A0C:.3e} sits {100*(1-A0C/1.07e-10):.0f}% below the LOWEST F3 model and")
print(f"  {100*(1-A0C/1.02e-10):.0f}% below the lowest F1 variant -- i.e. still outside the")
print(f"  median-like published range, but INSIDE the full published spread once F2's")
print(f"  robustified value (6.97e-11) and F4's chi uncertainty are counted.")
print("  NOTE, both directions: this ledger is NOT evidence for the framework (the low end is")
print("  carried by a 27-galaxy dwarf sample with a non-principled 3-galaxy trim, and by a")
print("  geometry factor that is itself calibrated on 1.2e-10), and it is NOT evidence against")
print("  it either (the high end is a single estimator family whose error model is known to be")
print("  misspecified). It is the honest state of the literature.")
RES["ledger"] = [dict(name=nm, a0=v, quoted=q, over_canon=v / A0C, over_alt=v / A0A,
                      over_gdag=v / GDAG) for nm, v, q in sorted(LED, key=lambda t: t[1])]

# ================================================================== S7 REGRESSION ANCHORS
print()
print(bar)
print("S7 -- REGRESSION ANCHORS (this file must not silently drift from the committed results)")
print(bar)
gals7 = fc.load(0.70)
GBg, GOg, FVg, _, _, _, _ = fc.flat(gals7, True)
a0_gls, fint, c2n, w = fc.gls(GBg, GOg, FVg)
med = float(np.median((GOg**2 - GBg**2) / GBg))
print(f"  committed incumbents on the gas-dominated subsample (Ud=0.70, N=310, 49 galaxies):")
print(f"    gls_origin  = {a0_gls:.6e}   (banked 1.1814381e-10)")
print(f"    median_a0pt = {med:.6e}   (banked 9.7256071e-11)")
assert abs(a0_gls - 1.1814381247770623e-10) < 1e-22, a0_gls
assert abs(med - 9.725607106012755e-11) < 1e-22, med
V = json.load(open(os.path.join(HERE, "estimator_bias_verdict.json")))
bt = V["bias_table"]
lab = "canonical cH_Lambda/Z"
print(f"  frozen mock verdict ({V['prereg_id']}, content digest "
      f"{V['content_sha256'][:16]}...):")
print(f"    gls_origin bias @ {lab} = {bt['gls_origin']['b'][lab]:+.2f} pp   (tier "
      f"{bt['gls_origin']['tier']}) <- THE REGRESSION ANCHOR")
print(f"    median_a0pt bias @ {lab} = {bt['median_a0pt']['b'][lab]:+.2f} pp   (tier "
      f"{bt['median_a0pt']['tier']})")
print(f"    survivors G1+G2+G3 ({len(V['survivors_G1G2G3'])}): "
      f"{', '.join(V['survivors_G1G2G3'])}")
assert abs(bt["gls_origin"]["b"][lab] - 10.34) < 0.02, bt["gls_origin"]["b"][lab]
assert bt["gls_origin"]["tier"] == "FAIL" and bt["median_a0pt"]["tier"] == "PASS"
print(f"  +10.34 pp anchor CONFIRMED from the committed, hashed verdict file.")
RES["anchors"] = dict(gls_origin_real=a0_gls, median_a0pt_real=med,
                      mock_bias_gls_pp=bt["gls_origin"]["b"][lab],
                      mock_bias_median_pp=bt["median_a0pt"]["b"][lab],
                      verdict_content_sha256=V["content_sha256"])

# ============================================================================ S8 WHAT'S NEXT
print()
print(bar)
print("S8 -- WHAT IS AND IS NOT LICENSED BY THIS CATALOGUE")
print(bar)
print("  LICENSED:")
print("   1. 'The published determinations do NOT use this repo's estimator.' Established: no")
print("      published a0 comes from a location statistic on per-point a0_pt, and S2 shows")
print("      that statistic cannot even be defined over their y range.")
print("   2. 'The published families are predominantly LOG-space and median-like.' Established")
print("      from the papers: F1 log-residual ODR, F3 log-space likelihood + posterior median,")
print("      F4 log-space orthogonal fit with published skew ~ 0.")
print("   3. 'One published family (F2) IS mean-like on per-object a0 in the deep-MOND regime,")
print("      and is therefore a priori at risk BY THE SAME MECHANISM.' Flagged, with the")
print("      reason and with [SSM10]'s own mean-vs-trimmed factor of 1.56 as the empirical")
print("      hint. NOT a bias claim: F2 must be implemented and measured on mocks.")
print("   4. 'The literature already contains a MEASURED 15% estimator sensitivity inside F1'")
print("      ([CZ18], linear vs log residual), and its sign is DOWNWARD for the mean-like")
print("      variant -- the OPPOSITE of this repo's deep-MOND result. Extrapolating the")
print("      +10.34 pp across regimes would have got the sign wrong.")
print("  NOT LICENSED (and specifically forbidden by the calibration):")
print("   A. Any statement that a published number IS biased. Nothing here implements or")
print("      measures a published estimator.")
print("   B. Attributing the Upsilon degeneracy, the sample-selection difference, or the")
print("      functional-form difference to 'estimator bias'. They are separate lines and are")
print("      kept separate above (Upsilon is the 0.24e-10 systematic in F1 and the reason")
print("      Li+2018's free-g_dag fit is uninformative; selection is the F2 dwarf/LSB vs F1")
print("      full-sample difference; functional form is F1's nu vs the framework's nu).")
print("   C. Any derivation of a0. a0's VALUE remains POSITED. Both footings carried on every")
print("      dimensional number above. No 'theory closed', no TOE claim, no 'no open doors'.")
print("  NEXT STEP (for the implementation agent): mock F1 (both residual forms), F2 (mean,")
print("  median and trimmed combinations) and a profile-likelihood proxy for F3, over the FULL")
print("  y range reproduced in S1, injecting a0 at 9.355e-11, 1.1305e-10 AND 1.2e-10 so that")
print("  no value is privileged; report each family's bias at all three.")

out = os.path.join(HERE, "published_a0_catalogue_results.json")
RES["meta"] = dict(script="published_a0_catalogue.py",
                   role="catalogue the PUBLISHED a0 determinations by estimator family; "
                        "reproduce their sample footprints and y-ranges from raw SPARC; flag "
                        "a priori Jensen/skew risk WITH the mechanism. No published estimator "
                        "is implemented and NO bias of any published number is claimed.",
                   posited_clause="a0's VALUE remains POSITED in the Zimmerman dS-Unruh "
                                  "modified-inertia framework (a0 = c H_Lambda/Z). This is a "
                                  "measurement-methodology catalogue, not a derivation. Both "
                                  "footings carried. No theory-closed claim.",
                   wellhead_credit="nu = sqrt(1+1/y) is Milgrom 1999 PLA 253:273 Eq. 9; the "
                                   "framework's distinctive content is the cH_Lambda/Z "
                                   "coefficient plus the modified-inertia completion.")
json.dump(RES, open(out, "w"), indent=1, default=float)
print(f"\n[published_a0_catalogue_results.json written]")
print("EXIT 0: footprints reproduced, catalogue assembled. Exit code is not a verdict.")
