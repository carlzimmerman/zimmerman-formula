#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG80 -- IS THE ULTRA-FAINT OFFSET LUMINOSITY-ORDERED?   (FROZEN BEFORE THE FIRST RUN; nothing below is tuned after a result.)

QUESTION.  CFG78 noted (untested) that the per-system ultra-faint offsets d_i = log10(sigma_obs/sigma_pred) look luminosity-ordered (Boo I ~ 0; Car II/Hyd I/Leo V
+0.15..+0.28; Ret II/Seg 1/Wil 1 +0.4..+0.65), which would point to a luminosity- or Upsilon_V-dependent systematic instead of a flat offset.  Test that, on
ON-DISK data only (no downloads; nothing in the repository is edited; outputs go to the scratch directory only).
DATA.  real_research/data/dsph/lvd_dwarf_mw.csv (sample (i)); real_research/data/arroyopolonio2026_ufd_binary_corrected.tsv (sample (ii)).
SAMPLE (i) = FG001/CFG28/CFG42/CFG73 selection: rows with M_V > -7.7, a distance (distance_host, else distance_gc), an r_half (rhalf_sph_physical [pc], else
  rhalf_physical), and either vlos_sigma > 0 (RESOLVED, 31) or vlos_sigma_ul (LIMIT, 9; left-censored: true sigma <= limit; the limit's offset is an UPPER
  bound).  Stars only (mass_HI is empty for all 40 anyway), Upsilon_V = 2 (M_b = 2 L_V, L_V = 10^(0.4 (4.83 - M_V))), half the baryons enclosed at r = (4/3) r_half,
  sigma_pred^2 = g r / 3.
SAMPLE (ii) = the 8 scorable Arroyo-Polonio+2026 systems of CFG46/CFG78 (Boo I, Car II, Hyd I, Leo IV, Leo V, Ret II, Seg 1, Wil 1), no censoring; the observed
  sigma is the paper's posterior median at f = 0, f free, f = 0.7; M_V and r_half from the LVD table (as CFG46).
MODELS (offsets, all with the estimator above):
  LAW    bare isolated law, kernel nu(y) = 1/(1 - exp(-sqrt y)) (the RAR kernel, as CFG42/CFG78), a0 = 9.36e-11 (canonical) and 1.13e-10 (alt);
  RULE   the derived sum rule (CFG35/CFG42/CFG46/CFG78): g += G f_ex (1-f_b) M_NFW(<r)/r^2, f_ex = max(0, 1 - M_ph,edge/[(1-f_b) M_coll]), Moster+13 inverted
         on a grid (clamps at 1e9), Dutton-Maccio NFW, x_e = 0.40, own LCDM top-hat solve; both footings;
  LCDM   the Duffy-full comparator of CFG69/CFG73: M_h = Moster inversion floored at 1e9, Duffy-full c = 5.71 (M/(2e12/h))^-0.084, debris (1-f_b) M_NFW(<r), nu = 1,
         stars only, no collapse-mass scan (the central prediction; a scan would only shift the offsets, not their ordering).  Footing-free.
COVARIATES.  (1) M_V.   (2) stellar mass: M_* = Upsilon_V L_V (Upsilon_V = 2) -- a strictly monotone function of M_V, so every rank statistic vs M_* is IDENTICAL to
  that vs M_V with the opposite sign; reported once, as "vs M_V (faint = large M_V; positive = fainter systems more over-dispersed)".  As a separate check, the
  catalogue's own mass_stellar column (log10 M_*; a different, catalogue number) is also used, with its raw sign.  (3) log10 r_half (pc), raw sign.  Note that r_half
  enters the prediction itself, so an offset-r_half trend can be produced by a mis-specified estimator; the MC in (d) has that built in (flat offset, same pred).
(a) STATISTICS.  Sample (i) has left-censored values.  PRIMARY statistic: the Kendall tau for censored data of Brown-Hollander-Korwar (1974) / Akritas-Murphy-
  LaValley (1995): S = sum_{i<j} sgn(x_i - x_j) * Sy_ij, where Sy_ij = sgn(y_i - y_j) if the order is determinate and 0 otherwise.  Determinate = both resolved; or
  one resolved (value v) and the other a limit (bound b) with v > b (then the resolved one is larger, since the limit's true value <= b < v); two limits never; ties 0.
  tau_c = S / sqrt(N_x N_y) with N_x = number of x-untied pairs, N_y = number of y-determinate pairs (= Kendall tau-b when nothing is censored).  Its permutation
  p-value permutes the (y, censor-flag) pairs among the systems, x fixed, 10^5 permutations, two-sided, p = (1 + #{|S_perm| >= |S_obs|}) / (1 + N) (the y-order
  matrix is invariant under the permutation, so N_y is fixed).  The trend SLOPE is the Akritas-Theil-Sen estimator: the b for which S(y - b x) = 0 (the same censored
  Kendall statistic on the residuals y - b x, bound - b x for limits; bisection on [-3, 3]); its 68% interval is the 16-84 percentile of 1000 bootstrap resamples of
  the systems.  SPEARMAN cannot be made exact for left-censored data without a model, so it is BRACKETED, all with 10^5-permutation p-values: rho_R = resolved
  only (31; drops the limits), rho_B = all 40 with each limit at its upper bound (biases the faint end UP), rho_L = all 40 with each limit ranked at the bottom (biases
  it DOWN); the censored Kendall is the arbiter, the Spearman rows are reported for completeness.  Sample (ii) has no censoring: Spearman rho and Kendall tau-b,
  EXACT permutation p (all 8! = 40320 permutations enumerated -- stronger than 10^5 random ones, which would only re-sample the same set); slope = ATS
  (uncensored: Theil-Sen-like) with a 1000-resample bootstrap interval.  Each rank row (i) and (ii) is done for LAW canonical, LAW alt, RULE canonical, RULE alt and
  LCDM, vs each covariate; (ii) at f = 0, f free, f = 0.7.
  PASS LINES.  p < 0.01 (two-sided, permutation) = trend DETECTED; 0.01 <= p < 0.05 = SUGGESTIVE only; p >= 0.05 = NO TREND DETECTED (a valid outcome, not a failure).
  PRIMARY FAMILY = LAW canonical on the 40 vs M_V and vs log r_half (censored Kendall), 2 tests, each judged at 0.01.  Every other row is SECONDARY: a secondary
  p < 0.01 is reported as "flagged" and is not called a detection unless p < 0.01/30 = 3.3e-4 (about 30 secondary rows, Bonferroni).  The M_V and M_* rows are the
  same test, not two.  Nothing is claimed about the framework from any row.
(c) WHAT Upsilon_V WOULD REMOVE THE TREND.  For the primary rows (LAW canonical vs M_V and vs log r_half; sample (i)) recompute the censored Kendall S/tau, its
  permutation p (2x10^4 permutations) and the ATS slope with a single constant Upsilon_V on the grid {0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 32, 64, 128}
  (Moster/collapse masses are not used by the law, so Upsilon_V enters only the baryonic mass), and locate by bisection on a finer grid the Upsilon_V (0.1..1000) at
  which the ATS slope is exactly zero, if any.  Lanes' range: 1-4 (CFG28/CFG42/CFG73 floor scans use 1, 2, 4).  PLAUSIBILITY (stated now, not adjusted): an old,
  metal-poor stellar population has Upsilon_V of roughly 1.5-3 (the lanes' 1-4 brackets it); anything above ~4 needs a dark stellar component or a strongly bottom-
  heavy IMF and is called IMPLAUSIBLE here; a required Upsilon_V outside 1-4 is reported as such.  Pre-run expectation (declared): in the deep-MOND regime
  sigma_pred^4 ~ Upsilon_V, which moves every offset almost UNIFORMLY (-0.25 log10 Upsilon_V), so a constant Upsilon_V changes the level, not the slope, and the slope
  is expected to be nearly Upsilon_V-independent; a slope-zero Upsilon_V may not exist.
(d) SELECTION-BIAS MONTE CARLO (sample (i), LAW canonical).  Truth: a FLAT offset a, sigma_true,i = sigma_pred,i 10^a, for a in {0, +0.15, +0.30}.  Each system keeps
  its own sensitivity: s_i = (em_i + ep_i)/2 (the literature dispersion errors) for the 31 resolved, s_i = ul_i/1.645 for the 9 limits (the reported limits read as
  one-sided 95% bounds; the same detection limits).  Draw sigma_hat_i = sigma_true,i + s_i z_i (z ~ N(0,1)).  Reported RESOLVED iff sigma_hat_i > k s_i, with k in
  {1, 1.5 (primary), 2}; else a LIMIT at max(sigma_hat_i, 0) + 1.645 s_i.  Then the same censored Kendall tau_c vs M_V and vs log r_half, its permutation p (500
  fixed random permutations per simulated data set), 1000 simulated data sets per (a, k).  Reported: mean and sd of tau_c, the FALSE-POSITIVE RATE Pr(p < 0.01)
  and Pr(p < 0.05), the number of resolved (vs 31 observed), and the selection-aware MC p-value of the observed tau_c: Pr(|tau_sim| >= |tau_obs|).  Also the
  resolved-only Spearman false-positive rate (to show how the naive statistic behaves).  PASS LINES: the censored-Kendall selection is CLEAN if the false-positive rate
  at p < 0.01 is <= 0.02 in every (a, k) cell (twice nominal); a trend is called SELECTION-ROBUST only if its permutation p < 0.01 AND its MC p < 0.01 in every
  cell with a >= 0.15 (the offset level the data actually show) at k = 1.5.  A flat-offset MC is a null-model check, not a fit; it does not test Upsilon_V.
  For sample (ii) an analogous MC: flat offset a in {0, 0.15, 0.30}, sigma_hat = sigma_true + split-normal noise with the paper's p1/m1 errors (floor 0.05 km/s),
  2000 simulated sets, exact-style permutation p (2000 random permutations), false-positive rate at 0.01 and 0.05.  (The 8 systems are not censored.)
CONTROLS.  C1 (implementation; synthetic): (a) my Spearman == scipy.stats.spearmanr and my tau_c == scipy kendalltau tau-b to 1e-12 on tied data; (b) the
  permutation p of the uncensored Kendall (10^5 permutations) agrees with scipy's asymptotic p within 0.01 (untied, n = 40, tau ~ 0.25); (c) a hand-worked censored
  example: systems (x, y) = (1, 3.0), (2, limit 1.0), (3, 2.0), (4, 4.0): S = +2, tau_c = 2/6; and two limits are indeterminate; (d) INJECTED SLOPE: n = 200 synthetic
  systems, x ~ U(-7, -1), y = 0.1 + 0.08 (x - mean x) + N(0, 0.15), 45 faintest-side systems left-censored (bound = y + |N(0.2, 0.1)|): the censored Kendall p must be
  < 1e-3 (10^5 perms), the ATS slope must recover 0.08 within 0.02, and the ATS slope must move to 0 +- 0.02 when the injection is 0; (e) NULL CALIBRATION: 300 null
  data sets (n = 40, 9 censored) with 2000-permutation p: the fraction with p < 0.05 must lie in [0.02, 0.09]; (f) the injected data set with y randomly permuted among
  systems must give p > 0.01.  C2: the law's closed forms (Newtonian a0 -> 0, deep-MOND a0 -> inf) to 1e-9 / 1e-4; the rule and LCDM predictions reduce to the law/Newtonian
  when the halo is off (structure check); the KM-free arithmetic is not used at all here.
  MUTATE=1: the offsets of each sample are RANDOMLY PERMUTED among the systems (seed fixed), censor flags moving with them.  Requirement: the headline statistics lose
  their trends (primary p >= 0.01) and, as a calibration of the whole pipeline, over 200 further random permutations of the real offsets the fraction with primary
  p < 0.01 must be <= 0.05 (nominal 0.01, binomial slack); the synthetic injection C1(d),(f) is run in both modes as the control that has bite independent of the
  real data (if the real data show no trend the MUTATE run on the real data is uninformative, and that is stated).  Exit code 1 if any control fails, or under MUTATE
  if the real-data primary p < 0.01 survives the permutation; otherwise 0.  The hypotheses themselves are RESULTS, not pass/fail: a null trend is a valid outcome.
PRE-RUN EXPECTATIONS (declared honestly).  With n = 8 a Kendall p < 0.01 needs |tau| >~ 0.79, so sample (ii) has little power; on the 40, if the trend is as
  the eight suggest, a positive tau vs M_V is expected, but the heteroscedastic errors and the positive-definiteness of sigma_hat make a selection-induced positive
  tau at the faint end plausible, which (d) is there to measure.  No expectation is held about the LCDM or rule offsets.
PROGRAMME RULES.  The data are never said to favour the framework; kappa = 1/2 is FITTED; nothing here says the theory is closed; a null trend is valid.
AMENDMENTS (appended AFTER the first run; the frozen text above is unchanged; every number the first run produced is unchanged by them).
  A1 (bug in my control C2, not a tolerance change): the deep-MOND closed form in C2 used sigma^4 = (4/81) G M a0 (the r-independent estimator constant of an
     unused option) instead of the correct value for THIS estimator, sigma^4 = G M a0/18 (g = sqrt(g_N a0), g_N = G M/(2 r^2), sigma^2 = g r/3).  The first run
     failed it at +3.0e-2 = (8/9)^(-1/4) - 1, exactly the constant mismatch; fixed to 1/18, tolerance unchanged (1e-4).  The law's predictions never used the wrong constant.
  A2 (C1e, kept as a DECLARED FAILURE and explained): the first run FAILED C1e (fraction with p < 0.05 = 0.117 against [0.02, 0.09]).  Cause: the null data sets censored
     the 9 LARGEST-x systems with bounds above the truth, so the censoring flag is x-dependent, which breaks the exchangeability the permutation test assumes.  The
     real limits are also concentrated at the faint end, so the censored-Kendall permutation p of sample (i) is ANTI-CONSERVATIVE by this mechanism; part (d)'s MC
     (which builds in the same x-dependent censoring) is the selection-aware answer.  Two clearly-labelled post-hoc controls are added: C1e2 (censoring independent of x:
     the permutation p must then be calibrated, fraction in [0.02, 0.09]) and C1e3 (informational: x-dependent censoring inflates the fraction).  C1e stays FAILED in the
     record and the main-run exit code stays 1 because of it.
Run: python3 cfg80_ufd_luminosity_trend.py   (MUTATE=1 for the control; output to cfg80.out / cfg80_MUTATE.out and *_results.json next to this file).
"""
import os, sys, math, csv, json, itertools, time
import numpy as np
from scipy import stats
from scipy.optimize import brentq
from scipy.integrate import quad

T0 = time.time()
MUTATE = os.environ.get("MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
LVDF = f"{REPO}/real_research/data/dsph/lvd_dwarf_mw.csv"
TSV = f"{REPO}/real_research/data/arroyopolonio2026_ufd_binary_corrected.tsv"
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)
FAILS = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")
    if not ok: FAILS.append(name)
RESULTS = {}

G, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FOOTS = ("canonical", "alt")
FB = 0.02237 / (0.02237 + 0.1200)
H0_KMS = 67.4; HL = 0.674; MPC_M = 3.0857e22
RHO_C = 3 * (H0_KMS * 1e3 / MPC_M) ** 2 / (8 * math.pi * G) / MSUN * MPC_M ** 3   # Msun / Mpc^3
NPERM = 100000

# ------------------------------------------------------------------------------ data
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None
S40 = []
for r in csv.DictReader(open(LVDF)):
    MV = fl(r["M_V"]); rh = fl(r["rhalf_sph_physical"]) or fl(r["rhalf_physical"]); Dh = fl(r["distance_host"]) or fl(r["distance_gc"])
    if MV is None or rh is None or Dh is None or MV <= -7.7: continue
    sig = fl(r["vlos_sigma"]); ul = fl(r["vlos_sigma_ul"])
    d = dict(name=r["name"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=0.0, cat_lms=fl(r["mass_stellar"]))
    if ul is not None:
        d.update(sig=ul, cen=True, em=None, ep=None, s=ul / 1.645)
    elif sig is not None and sig > 0:
        em = fl(r["vlos_sigma_em"]); ep = fl(r["vlos_sigma_ep"])
        d.update(sig=sig, cen=False, em=em, ep=ep, s=0.5 * (em + ep))
    else:
        continue
    S40.append(d)
LVD = {r["name"]: r for r in csv.DictReader(open(LVDF))}
rows = [l.rstrip("\n").split("\t") for l in open(TSV) if l.strip() and not l.startswith("#")]
hdr = rows[0]; TAB = {r[0]: dict(zip(hdr, r)) for r in rows[1:]}
MAP8 = {"Boo I": "Bootes I", "Car II": "Carina II", "Hyd I": "Hydrus I", "Leo IV": "Leo IV", "Leo V": "Leo V", "Ret II": "Reticulum II", "Seg 1": "Segue 1", "Wil 1": "Willman 1"}
S8 = []
for k, lv in MAP8.items():
    r = LVD[lv]; t = TAB[k]
    MV = fl(r["M_V"]); rh = fl(r["rhalf_sph_physical"]) or fl(r["rhalf_physical"])
    d = dict(name=k, MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=0.0, cat_lms=fl(r["mass_stellar"]))
    for kk in ("sig_fz", "sig_f", "sig_f7"):
        d[kk] = float(t[kk]); d[kk + "_p1"] = float(t[kk + "_p1"]); d[kk + "_m1"] = float(t[kk + "_m1"])
    S8.append(d)
P(f"sample (i): {len(S40)} systems, {sum(not d['cen'] for d in S40)} resolved + {sum(d['cen'] for d in S40)} limits; sample (ii): {len(S8)} systems ({', '.join(d['name'] for d in S8)})")

# ------------------------------------------------------------------------------ predictions
def nu(y):
    y = max(float(y), 1e-300)
    return 1.0 / (-math.expm1(-math.sqrt(y)))
def sig_law_kms(g, a0, ups=2.0, deep=False, extra_g=0.0):
    Mb = ups * g["LV"]
    r = (4.0 / 3.0) * g["rh"] * PC
    gN = G * 0.5 * Mb * MSUN / r ** 2
    if deep:
        return (4.0 / 81.0 * G * Mb * MSUN * a0) ** 0.25 / 1e3
    gg = gN * nu(gN / a0) + extra_g
    return math.sqrt(gg * r / 3.0) / 1e3
_LMH = np.linspace(9.0, 15.5, 1301)
def _moster_ms(lmh):
    x = 10 ** (lmh - 11.590)
    return 10 ** lmh * 2 * 0.0351 / (x ** (-1.376) + x ** 0.608)
_LMS = np.log10(_moster_ms(_LMH))
def mcoll(Mstar): return float(10 ** np.interp(math.log10(Mstar), _LMS, _LMH))
def moster_mh_exact(Mstar, floor=1e9):
    f = lambda lm: math.log10(float(_moster_ms(lm))) - math.log10(Mstar)
    if f(math.log10(floor)) >= 0: return floor
    return 10 ** brentq(f, 9.0, 16.0, xtol=1e-13)
def mfun(t): return math.log1p(t) - t / (1 + t)
def R200_kpc(Mh): return (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.0) * 1000.0
def nfw_enc(Mh, r_kpc, kind="dutton_maccio"):
    if kind == "dutton_maccio": c = 10 ** (0.905 - 0.101 * (math.log10(Mh * HL) - 12.0))
    else: c = 5.71 * (Mh / (2e12 / HL)) ** (-0.084)
    x = min(max(r_kpc / R200_kpc(Mh), 1e-4), 5.0)
    return Mh * mfun(c * x) / mfun(c)
OM, HH = 0.3153, 0.6736; OL = 1 - OM
GMPC = 4.30091727e-9; H0M = 100 * HH
RHOM0 = OM * 3 * H0M ** 2 / (8 * math.pi * GMPC)
AGE = 2.0 / (3.0 * H0M * math.sqrt(OL)) * math.asinh(math.sqrt(OL / OM))
def _tta(rta, M=1.0):
    L3 = OL * H0M ** 2
    f = lambda r: 1.0 / math.sqrt(max(2 * GMPC * M * (1 / r - 1 / rta) + L3 * (r * r - rta * rta), 1e-300))
    v, _ = quad(f, 0, rta, limit=400)
    return v
def _one_plus_delta():
    M = 1.0e6
    lr = brentq(lambda lr: _tta(math.exp(lr), M) - AGE, math.log(1e-4), math.log(50.0), xtol=1e-12)
    return M / (4 * math.pi / 3 * math.exp(lr) ** 3) / RHOM0
DELTA_TA = _one_plus_delta()
def edge_phantom(Mb, a0, xe=0.40):
    Mlaw = lambda r: Mb * nu(GMPC * Mb / r ** 2 / (a0 * MPC_M / 1e6))
    fn = lambda lr: math.log(Mlaw(math.exp(lr)) / (4 * math.pi / 3 * math.exp(3 * lr) * RHOM0)) - math.log(DELTA_TA)
    rta = math.exp(brentq(fn, math.log(1e-5), math.log(1e3), xtol=1e-13))
    return Mlaw(xe * rta) - Mb
def sig_rule_kms(g, a0):
    Mb = 2.0 * g["LV"]
    Mh = mcoll(2.0 * g["LV"])
    fex = max(0.0, 1.0 - edge_phantom(Mb, a0) / ((1 - FB) * Mh))
    rhp = (4.0 / 3.0) * g["rh"]; r = rhp * PC
    extra = G * fex * (1 - FB) * nfw_enc(Mh, rhp / 1000.0) * MSUN / r ** 2
    return sig_law_kms(g, a0, extra_g=extra)
def sig_lcdm_kms(g, halo=True):
    Mb = 2.0 * g["LV"]; rhp = (4.0 / 3.0) * g["rh"]; r = rhp * PC
    Mh = moster_mh_exact(2.0 * g["LV"])
    Mn = (1 - FB) * nfw_enc(Mh, rhp / 1000.0, "duffy_full") if halo else 0.0
    return math.sqrt(G * (0.5 * Mb + Mn) * MSUN / r ** 2 * r / 3.0) / 1e3

def pred_table(smp):
    T = {}
    for foot in FOOTS:
        T[("LAW", foot)] = np.array([sig_law_kms(g, A0[foot]) for g in smp])
        T[("RULE", foot)] = np.array([sig_rule_kms(g, A0[foot]) for g in smp])
    T[("LCDM", "-")] = np.array([sig_lcdm_kms(g) for g in smp])
    return T
PRED40 = pred_table(S40); PRED8 = pred_table(S8)
MODELS = [("LAW", "canonical"), ("LAW", "alt"), ("RULE", "canonical"), ("RULE", "alt"), ("LCDM", "-")]

# ------------------------------------------------------------------------------ statistics
def sxmat(x):
    x = np.asarray(x, float); return np.sign(x[:, None] - x[None, :])
def symat(y, cen):
    y = np.asarray(y, float); cen = np.asarray(cen, bool)
    D = y[:, None] - y[None, :]
    res = ~cen
    A = (res[:, None] & res[None, :]) | (res[:, None] & cen[None, :] & (D > 0)) | (cen[:, None] & res[None, :] & (D < 0))
    return np.where(A, np.sign(D), 0.0)
def perms_matrix(n, N, seed):
    rng = np.random.default_rng(seed)
    return np.argsort(rng.random((N, n)), axis=1)
def perm_S(SX, SY, Pm, chunk=1500):
    out = np.empty(len(Pm))
    for a in range(0, len(Pm), chunk):
        Pc = Pm[a:a + chunk]
        out[a:a + chunk] = 0.5 * np.einsum("bij,ij->b", SY[Pc[:, :, None], Pc[:, None, :]], SX)
    return out
def kendall_cens(x, y, cen, Pm):
    SX = sxmat(x); SY = symat(y, cen)
    S0 = 0.5 * float(np.sum(SX * SY))
    Nx = 0.5 * float(np.sum(SX != 0)); Ny = 0.5 * float(np.sum(SY != 0))
    tau = S0 / math.sqrt(Nx * Ny) if Nx * Ny > 0 else 0.0
    Sp = perm_S(SX, SY, Pm)
    p = (1 + np.sum(np.abs(Sp) >= abs(S0) - 1e-9)) / (1 + len(Pm))
    return dict(S=S0, tau=tau, p=float(p), Nx=Nx, Ny=Ny)
def S_of_b(x, y, cen, b, SX=None):
    SX = sxmat(x) if SX is None else SX
    yy = np.asarray(y, float) - b * np.asarray(x, float)
    return 0.5 * float(np.sum(SX * symat(yy, cen)))
def ats_slope(x, y, cen, lo=-3.0, hi=3.0, it=42):
    x = np.asarray(x, float); SX = sxmat(x)
    f = lambda b: S_of_b(x, y, cen, b, SX)
    flo, fhi = f(lo), f(hi)
    if not (flo > 0 and fhi < 0):
        return float("nan")
    for _ in range(it):
        mid = 0.5 * (lo + hi); fm = f(mid)
        if fm > 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)
def ats_boot(x, y, cen, nb=1000, seed=80):
    rng = np.random.default_rng(seed); n = len(x); v = []
    x = np.asarray(x, float); y = np.asarray(y, float); cen = np.asarray(cen, bool)
    for _ in range(nb):
        k = rng.integers(0, n, n)
        b = ats_slope(x[k], y[k], cen[k])
        if np.isfinite(b): v.append(b)
    v = np.array(v)
    return (float(np.percentile(v, 16)), float(np.percentile(v, 84)), len(v)) if len(v) > 50 else (float("nan"), float("nan"), len(v))
def avg_rank(a): return stats.rankdata(a, method="average")
def spearman_perm(x, y, Pm):
    rx = avg_rank(x); ry = avg_rank(y)
    rxc = rx - rx.mean(); nrm = math.sqrt(np.sum(rxc ** 2))
    def cor(ryv):
        ryc = ryv - ryv.mean(); return float(rxc @ ryc / (nrm * math.sqrt(np.sum(ryc ** 2))))
    r0 = cor(ry)
    ryc = ry - ry.mean(); ryn = math.sqrt(np.sum(ryc ** 2))
    rp = (ryc[Pm] @ rxc) / (nrm * ryn)
    p = (1 + np.sum(np.abs(rp) >= abs(r0) - 1e-12)) / (1 + len(Pm))
    return r0, float(p)

# ------------------------------------------------------------------------------ controls
P("\n=== CONTROLS (synthetic / closed form) ===")
rng = np.random.default_rng(8001)
# C1a
xa = np.round(rng.normal(size=40), 1); ya = np.round(0.3 * xa + rng.normal(size=40), 1)
r_mine, _ = spearman_perm(xa, ya, perms_matrix(40, 10, 1))
r_sp = stats.spearmanr(xa, ya)[0]
k_mine = kendall_cens(xa, ya, np.zeros(40, bool), perms_matrix(40, 10, 1))["tau"]; k_sp = stats.kendalltau(xa, ya)[0]
check("C1a my Spearman == scipy.spearmanr and my tau_c == scipy.kendalltau (tau-b) on tied data", abs(r_mine - r_sp) < 1e-12 and abs(k_mine - k_sp) < 1e-12,
      f"rho {r_mine:.12f}/{r_sp:.12f}; tau {k_mine:.12f}/{k_sp:.12f}")
# C1b
xb = rng.normal(size=40); yb = 0.25 * xb + rng.normal(size=40)
while True:
    kb = stats.kendalltau(xb, yb, method="asymptotic")
    if 0.18 < kb[0] < 0.32: break
    xb = rng.normal(size=40); yb = 0.25 * xb + rng.normal(size=40)
mp = kendall_cens(xb, yb, np.zeros(40, bool), perms_matrix(40, NPERM, 2))
check("C1b uncensored Kendall permutation p (1e5) agrees with scipy asymptotic p within 0.01", abs(mp["p"] - kb[1]) < 0.01, f"tau {mp['tau']:.3f}; perm p {mp['p']:.4f} vs scipy {kb[1]:.4f}")
# C1c hand example
xh = np.array([1., 2, 3, 4]); yh = np.array([3.0, 1.0, 2.0, 4.0]); ch = np.array([False, True, False, False])
hh = kendall_cens(xh, yh, ch, perms_matrix(4, 50, 3))
two_lim = symat(np.array([1.0, 2.0]), np.array([True, True]))
check("C1c hand-worked censored example S = +2, tau_c = 2/6; two limits indeterminate", abs(hh["S"] - 2) < 1e-12 and abs(hh["tau"] - 2 / 6) < 1e-12 and np.all(two_lim == 0), f"S {hh['S']}, tau {hh['tau']:.4f}")
# C1d injection
def synth(n, b, ncen, rng, noise=0.15):
    x = rng.uniform(-7, -1, n); y = 0.1 + b * (x - x.mean()) + rng.normal(0, noise, n)
    cen = np.zeros(n, bool); cen[np.argsort(x)[-ncen:]] = True          # faintest side censored (largest x)
    yy = y.copy(); yy[cen] = y[cen] + np.abs(rng.normal(0.2, 0.1, ncen))
    return x, yy, cen
xs_, ys_, cs_ = synth(200, 0.08, 45, np.random.default_rng(8002))
Pm200 = perms_matrix(200, NPERM, 4)
inj = kendall_cens(xs_, ys_, cs_, Pm200); bs_inj = ats_slope(xs_, ys_, cs_)
xs0, ys0, cs0 = synth(200, 0.0, 45, np.random.default_rng(8003)); bs_0 = ats_slope(xs0, ys0, cs0)
check("C1d injected slope +0.08 (n=200, 45 censored): censored-Kendall p < 1e-3, ATS slope within 0.02 of 0.08; zero injection gives slope 0 +- 0.02",
      inj["p"] < 1e-3 and abs(bs_inj - 0.08) < 0.02 and abs(bs_0) < 0.02, f"p {inj['p']:.1e}, tau {inj['tau']:.3f}, ATS {bs_inj:+.4f}; null-injection ATS {bs_0:+.4f}")
# C1e null calibration
rc = np.random.default_rng(8004); P2k = perms_matrix(40, 2000, 5); pv = []
for _ in range(300):
    x, y, c = synth(40, 0.0, 9, rc)
    pv.append(kendall_cens(x, y, c, P2k)["p"])
fr = float(np.mean(np.array(pv) < 0.05))
check("C1e null calibration: fraction of 300 null data sets (n=40, 9 censored) with p < 0.05 lies in [0.02, 0.09]", 0.02 <= fr <= 0.09, f"fraction {fr:.3f}")
# C1e2 / C1e3 (amendment A2, post-hoc)
def synth_indep(n, ncen, rng, noise=0.15):
    x = rng.uniform(-7, -1, n); y = 0.1 + rng.normal(0, noise, n)
    cen = np.zeros(n, bool); cen[rng.choice(n, ncen, replace=False)] = True
    yy = y.copy(); yy[cen] = y[cen] + np.abs(rng.normal(0.2, 0.1, ncen))
    return x, yy, cen
rc2 = np.random.default_rng(8006); pv2 = []
for _ in range(300):
    x, y, c = synth_indep(40, 9, rc2); pv2.append(kendall_cens(x, y, c, P2k)["p"])
fr2 = float(np.mean(np.array(pv2) < 0.05))
check("C1e2 [post-hoc, A2] null calibration with censoring INDEPENDENT of x: fraction with p < 0.05 lies in [0.02, 0.09]", 0.02 <= fr2 <= 0.09, f"fraction {fr2:.3f}")
P(f"  C1e3 [info, A2] x-dependent censoring gave fraction {fr:.3f} (C1e) vs independent censoring {fr2:.3f} (C1e2) at nominal 0.05")
# C1f mutated injection
pm_ = np.random.default_rng(8005).permutation(200)
mut = kendall_cens(xs_, ys_[pm_], cs_[pm_], Pm200)
check("C1f injected data with (y, flag) randomly permuted among systems lose the trend (p > 0.01)", mut["p"] > 0.01, f"p {mut['p']:.3f}, tau {mut['tau']:+.3f}")
# C2 closed forms
g0 = S40[0]
sN = sig_law_kms(g0, 1e-40); cN = math.sqrt(G * 2 * g0["LV"] * MSUN / (6 * (4 / 3) * g0["rh"] * PC)) / 1e3
sD = sig_law_kms(g0, 1e40); cD = (G * 2 * g0["LV"] * MSUN * 1e40 / 18.0) ** 0.25 / 1e3
check("C2 law closed forms: Newtonian (a0 -> 0) to 1e-9, deep-MOND (a0 -> inf) to 1e-4", abs(sN / cN - 1) < 1e-9 and abs(sD / cD - 1) < 1e-4, f"{sN/cN-1:+.1e}, {sD/cD-1:+.1e}")
s0 = np.array([sig_lcdm_kms(g, halo=False) for g in S40])
cf = np.array([math.sqrt(G * 0.5 * 2 * g["LV"] * MSUN / (3 * (4 / 3) * g["rh"] * PC)) / 1e3 for g in S40])
check("C2 LCDM with the halo off is the Newtonian closed form; the halo only adds", np.max(np.abs(s0 / cf - 1)) < 1e-12 and np.all(PRED40[("LCDM", "-")] >= s0), f"{np.max(np.abs(s0/cf-1)):.1e}")
check("C2 rule >= law for every system (the sum rule only adds) and LAW alt >= LAW canonical", bool(np.all(PRED40[("RULE", "canonical")] >= PRED40[("LAW", "canonical")] - 1e-12)) and bool(np.all(PRED40[("LAW", "alt")] >= PRED40[("LAW", "canonical")])), "")

# ------------------------------------------------------------------------------ offsets, covariates
def offsets(smp, key_sig, pred, cens_flags):
    obs = np.array([g[key_sig] for g in smp], float)
    return np.log10(obs / pred), np.array(cens_flags, bool)
COV40 = {"M_V": np.array([g["MV"] for g in S40]), "logrh": np.log10([g["rh"] for g in S40]), "cat_logMs": np.array([g["cat_lms"] for g in S40])}
COV8 = {"M_V": np.array([g["MV"] for g in S8]), "logrh": np.log10([g["rh"] for g in S8]), "cat_logMs": np.array([g["cat_lms"] for g in S8])}
CEN40 = np.array([g["cen"] for g in S40])
PI40 = np.random.default_rng(80001).permutation(len(S40)); PI8 = np.random.default_rng(80002).permutation(len(S8))
def y40(model):
    y, c = offsets(S40, "sig", PRED40[model], CEN40)
    return (y[PI40], c[PI40]) if MUTATE else (y, c)
def y8(model, key):
    y, c = offsets(S8, key, PRED8[model], np.zeros(len(S8), bool))
    return (y[PI8], c[PI8]) if MUTATE else (y, c)

P("\n=== per-system offsets (LAW canonical; sample (i), sorted by M_V) ===" + ("   [MUTATED: offsets permuted among systems]" if MUTATE else ""))
yl, cl = y40(("LAW", "canonical"))
for i in np.argsort(COV40["M_V"]):
    P(f"  {S40[i]['name']:18s} M_V {S40[i]['MV']:6.2f} rh {S40[i]['rh']:7.1f} pc  offset {yl[i]:+.3f}{' (limit, upper bound)' if cl[i] else ''}")

Pm40 = perms_matrix(40, NPERM, 80100)
P8 = np.array(list(itertools.permutations(range(8))))
COVNAMES = [("M_V", "vs M_V (faint = +)"), ("logrh", "vs log10 r_half"), ("cat_logMs", "vs catalogue log M_*")]

# ------------------------------------------------------------------------------ (a),(b) sample (i)
P("\n" + "=" * 118 + "\n(a)/(b) SAMPLE (i): 31 resolved + 9 limits.  censored Kendall (BHK/AML), ATS slope (68% boot), Spearman bracket (R = resolved only, B = limits at bound, L = limits at bottom)\n" + "=" * 118)
TAB_I = {}
for model in MODELS:
    y, c = y40(model)
    for cov, lab in COVNAMES:
        x = COV40[cov]
        k = kendall_cens(x, y, c, Pm40)
        b = ats_slope(x, y, c); lo, hi, nb = ats_boot(x, y, c, 1000, seed=81)
        res = ~c
        rR, pR = spearman_perm(x[res], y[res], perms_matrix(int(res.sum()), NPERM, 82))
        yB = y.copy()
        rB, pB = spearman_perm(x, yB, Pm40)
        yL = y.copy(); yL[c] = y.min() - 1.0
        rL, pL = spearman_perm(x, yL, Pm40)
        TAB_I[(model, cov)] = dict(tau=k["tau"], p=k["p"], S=k["S"], slope=b, lo=lo, hi=hi, rhoR=rR, pR=pR, rhoB=rB, pB=pB, rhoL=rL, pL=pL)
        P(f"  {model[0]:5s}{model[1]:10s} {lab:22s}: tau_c {k['tau']:+.3f} p {k['p']:.4f} | ATS slope {b:+.4f} [{lo:+.4f},{hi:+.4f}] | rho_R {rR:+.3f} (p {pR:.4f}) rho_B {rB:+.3f} (p {pB:.4f}) rho_L {rL:+.3f} (p {pL:.4f})")
RESULTS["sample_i"] = {f"{m[0]}|{m[1]}|{c}": v for (m, c), v in TAB_I.items()}
prim = [(("LAW", "canonical"), "M_V"), (("LAW", "canonical"), "logrh")]
P("\n  PRIMARY FAMILY (LAW canonical, censored Kendall, threshold 0.01): " + "; ".join(f"{c}: p {TAB_I[(m, c)]['p']:.4f} -> {'DETECTED' if TAB_I[(m, c)]['p'] < 0.01 else ('suggestive' if TAB_I[(m, c)]['p'] < 0.05 else 'no trend')}" for m, c in prim))
sec = [(k, v) for k, v in TAB_I.items() if k not in prim and k[1] != "cat_logMs"]
P("  secondary rows flagged (p < 0.01): " + (", ".join(f"{k[0][0]}-{k[0][1]}/{k[1]} p {v['p']:.4f}" for k, v in sec if v["p"] < 0.01) or "none") +
  " ; below Bonferroni 3.3e-4: " + (", ".join(f"{k[0][0]}-{k[0][1]}/{k[1]}" for k, v in sec if v["p"] < 3.3e-4) or "none"))

# ------------------------------------------------------------------------------ (a),(b) sample (ii)
P("\n" + "=" * 118 + "\n(a)/(b) SAMPLE (ii): 8 binary-corrected systems; exact permutation p over all 8! = 40320 permutations\n" + "=" * 118)
TAB_II = {}
KEYS8 = (("sig_fz", "f = 0"), ("sig_f", "f free"), ("sig_f7", "f = 0.7"))
SX8 = {}
for key, kl in KEYS8:
    for model in MODELS:
        y, c = y8(model, key)
        for cov, lab in COVNAMES:
            x = COV8[cov]
            k = kendall_cens(x, y, c, P8)     # exact: all permutations
            b = ats_slope(x, y, c); lo, hi, nb = ats_boot(x, y, c, 1000, seed=83)
            r0, p0 = spearman_perm(x, y, P8)
            TAB_II[(key, model, cov)] = dict(tau=k["tau"], p=k["p"], slope=b, lo=lo, hi=hi, rho=r0, prho=p0)
            P(f"  {kl:8s} {model[0]:5s}{model[1]:10s} {lab:22s}: tau_b {k['tau']:+.3f} p {k['p']:.4f} | rho {r0:+.3f} p {p0:.4f} | ATS slope {b:+.4f} [{lo:+.4f},{hi:+.4f}]")
RESULTS["sample_ii"] = {f"{a}|{m[0]}|{m[1]}|{c}": v for (a, m, c), v in TAB_II.items()}
mn8 = min(v["p"] for v in TAB_II.values())
P(f"\n  sample (ii) smallest exact p over all {len(TAB_II)} rows: {mn8:.4f}; rows with p < 0.05: {sum(v['p'] < 0.05 for v in TAB_II.values())}; with p < 0.01: {sum(v['p'] < 0.01 for v in TAB_II.values())}")
if not MUTATE:
    for key, kl in KEYS8:
        y, c = y8(("LAW", "canonical"), key)
        P(f"  per-system LAW canonical offsets ({kl}), sorted by M_V: " + ", ".join(f"{S8[i]['name']} {y[i]:+.2f}" for i in np.argsort(COV8['M_V'])))

# ------------------------------------------------------------------------------ MUTATE calibration
if MUTATE:
    P("\n=== MUTATE calibration: 200 random permutations of the real offsets; primary rows ===")
    y0, c0 = offsets(S40, "sig", PRED40[("LAW", "canonical")], CEN40)
    rcal = np.random.default_rng(80200); Pm2 = perms_matrix(40, 2000, 80201); ps = {"M_V": [], "logrh": []}
    for _ in range(200):
        pp = rcal.permutation(40)
        for cov in ps:
            ps[cov].append(kendall_cens(COV40[cov], y0[pp], c0[pp], Pm2)["p"])
    for cov in ps:
        fr = float(np.mean(np.array(ps[cov]) < 0.01))
        check(f"MUTATE calibration ({cov}): fraction of 200 permuted real data sets with p < 0.01 is <= 0.05", fr <= 0.05, f"fraction {fr:.3f} (nominal 0.01)")
    lost = all(TAB_I[(m, c)]["p"] >= 0.01 for m, c in prim)
    P(f"  primary rows on the seeded mutated data: " + "; ".join(f"{c} p {TAB_I[(m, c)]['p']:.4f}" for m, c in prim))
    if not lost: FAILS.append("MUTATE: a primary trend survived the permutation")
    P("  (if the un-mutated real data show no trend, this MUTATE run on the real data is uninformative; the synthetic C1d/C1f controls carry the bite.)")

# ------------------------------------------------------------------------------ (c) Upsilon_V
if not MUTATE:
    P("\n" + "=" * 118 + "\n(c) A SINGLE CONSTANT Upsilon_V (LAW canonical, sample (i), censored Kendall + ATS slope)\n" + "=" * 118)
    def y_ups(u):
        pr = np.array([sig_law_kms(g, A0["canonical"], ups=u) for g in S40])
        return np.log10(np.array([g["sig"] for g in S40]) / pr)
    UG = [0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 32, 64, 128]
    Pu = perms_matrix(40, 20000, 80300); CU = {}
    for cov in ("M_V", "logrh"):
        P(f"  covariate {cov}:")
        for u in UG:
            y = y_ups(u); k = kendall_cens(COV40[cov], y, CEN40, Pu); b = ats_slope(COV40[cov], y, CEN40)
            CU[(cov, u)] = (k["tau"], k["p"], b)
            P(f"    Upsilon_V {u:6.2f}: median offset {np.median(y):+.3f}  tau_c {k['tau']:+.3f} p {k['p']:.4f}  ATS slope {b:+.4f}")
    roots = {}
    for cov in ("M_V", "logrh"):
        gridu = np.geomspace(0.1, 1000, 41)
        sl = [ats_slope(COV40[cov], y_ups(u), CEN40) for u in gridu]
        rt = None
        for i in range(len(gridu) - 1):
            if np.isfinite(sl[i]) and np.isfinite(sl[i + 1]) and sl[i] * sl[i + 1] < 0:
                rt = brentq(lambda lu: ats_slope(COV40[cov], y_ups(math.exp(lu)), CEN40), math.log(gridu[i]), math.log(gridu[i + 1]), xtol=1e-6); rt = math.exp(rt); break
        roots[cov] = rt
        P(f"  {cov}: slope range over Upsilon_V 0.1..1000: {np.nanmin(sl):+.4f} .. {np.nanmax(sl):+.4f}; zero-slope Upsilon_V: {('%.2f' % rt) if rt else 'none in 0.1..1000'}"
          + (f" -> {'inside' if 1 <= rt <= 4 else 'OUTSIDE'} the lanes' 1-4 range" if rt else ""))
    RESULTS["upsilon"] = {f"{c}|{u}": v for (c, u), v in CU.items()}; RESULTS["upsilon_root"] = {k: v for k, v in roots.items()}

# ------------------------------------------------------------------------------ (d) MC
if not MUTATE:
    P("\n" + "=" * 118 + "\n(d) SELECTION-BIAS MONTE CARLO: flat true offset a, literature errors, same sensitivities; sample (i) LAW canonical\n" + "=" * 118)
    pred = PRED40[("LAW", "canonical")]; sarr = np.array([g["s"] for g in S40]); NS = 1000
    P500 = perms_matrix(40, 500, 80400); SXc = {c: sxmat(COV40[c]) for c in ("M_V", "logrh")}
    MCR = {}
    for k_thr in (1.0, 1.5, 2.0):
        for a in (0.0, 0.15, 0.30):
            rng = np.random.default_rng(80500 + int(100 * a) + int(10 * k_thr))
            taus = {c: [] for c in SXc}; ps_ = {c: [] for c in SXc}; pspr = []; nres = []
            for _ in range(NS):
                st = pred * 10 ** a; sh = st + sarr * rng.standard_normal(40)
                res = sh > k_thr * sarr
                obs = np.where(res, sh, np.maximum(sh, 0) + 1.645 * sarr)
                yv = np.log10(obs / pred); cn = ~res; nres.append(int(res.sum()))
                SY = symat(yv, cn); Ny = 0.5 * float(np.sum(SY != 0))
                Sp = None
                for c in SXc:
                    S0 = 0.5 * float(np.sum(SXc[c] * SY)); Nx = 0.5 * float(np.sum(SXc[c] != 0))
                    taus[c].append(S0 / math.sqrt(Nx * Ny) if Ny > 0 else 0.0)
                    Sp = 0.5 * np.einsum("bij,ij->b", SY[P500[:, :, None], P500[:, None, :]], SXc[c])
                    ps_[c].append((1 + np.sum(np.abs(Sp) >= abs(S0) - 1e-9)) / 501.0)
                if res.sum() > 4:
                    pspr.append(spearman_perm(COV40["M_V"][res], yv[res], perms_matrix(int(res.sum()), 200, 7))[1])
            row = {}
            for c in SXc:
                t = np.array(taus[c]); p = np.array(ps_[c]); tobs = TAB_I[(("LAW", "canonical"), c)]["tau"]
                row[c] = dict(mean=float(t.mean()), sd=float(t.std()), fp01=float(np.mean(p < 0.01)), fp05=float(np.mean(p < 0.05)), mcp=float(np.mean(np.abs(t) >= abs(tobs) - 1e-12)), nres=float(np.mean(nres)))
            row["spearR_fp01"] = float(np.mean(np.array(pspr) < 0.01)) if pspr else float("nan")
            MCR[(k_thr, a)] = row
            P(f"  k={k_thr:3.1f} a={a:+.2f}: <n_resolved> {np.mean(nres):5.1f} | vs M_V: tau_sim {row['M_V']['mean']:+.3f}+-{row['M_V']['sd']:.3f}, FP(p<.01) {row['M_V']['fp01']:.3f}, FP(p<.05) {row['M_V']['fp05']:.3f}, MC p(obs) {row['M_V']['mcp']:.3f}"
              f" | vs log r_half: tau_sim {row['logrh']['mean']:+.3f}+-{row['logrh']['sd']:.3f}, FP01 {row['logrh']['fp01']:.3f}, MC p(obs) {row['logrh']['mcp']:.3f} | resolved-only Spearman FP01 {row['spearR_fp01']:.3f}")
    RESULTS["mc_i"] = {f"{k}|{a}": v for (k, a), v in MCR.items()}
    clean = all(MCR[k][c]["fp01"] <= 0.02 for k in MCR for c in ("M_V", "logrh"))
    P(f"  selection CLEAN for censored Kendall (every cell FP(p<0.01) <= 0.02)? {clean}")
    for c in ("M_V", "logrh"):
        pobs = TAB_I[(("LAW", "canonical"), c)]["p"]
        robust = pobs < 0.01 and all(MCR[(1.5, a)][c]["mcp"] < 0.01 for a in (0.15, 0.30))
        P(f"  {c}: permutation p {pobs:.4f}; MC p at k=1.5, a=0.15/0.30: {MCR[(1.5,0.15)][c]['mcp']:.3f}/{MCR[(1.5,0.30)][c]['mcp']:.3f} -> SELECTION-ROBUST TREND: {robust}")
    # sample (ii) MC
    P("\n  sample (ii) flat-offset MC (paper errors, 2000 sets, 2000 random permutations each), LAW canonical, f free:")
    pr8 = PRED8[("LAW", "canonical")]
    P2 = perms_matrix(8, 2000, 80600); MC8 = {}
    for a in (0.0, 0.15, 0.30):
        rng = np.random.default_rng(80700 + int(100 * a)); tt = {c: [] for c in ("M_V", "logrh")}; pp_ = {c: [] for c in tt}
        for _ in range(2000):
            z = rng.standard_normal(8)
            sh = np.array([max(pr8[i] * 10 ** a + z[i] * (S8[i]["sig_f_p1"] if z[i] > 0 else S8[i]["sig_f_m1"]), 0.05) for i in range(8)])
            yv = np.log10(sh / pr8); SY = symat(yv, np.zeros(8, bool)); Ny = 0.5 * float(np.sum(SY != 0))
            for c in tt:
                SXx = sxmat(COV8[c]); S0 = 0.5 * float(np.sum(SXx * SY)); Nx = 0.5 * float(np.sum(SXx != 0))
                tt[c].append(S0 / math.sqrt(Nx * Ny)); Sp = 0.5 * np.einsum("bij,ij->b", SY[P2[:, :, None], P2[:, None, :]], SXx)
                pp_[c].append((1 + np.sum(np.abs(Sp) >= abs(S0) - 1e-9)) / 2001.0)
        for c in tt:
            MC8[(a, c)] = dict(mean=float(np.mean(tt[c])), sd=float(np.std(tt[c])), fp01=float(np.mean(np.array(pp_[c]) < 0.01)), fp05=float(np.mean(np.array(pp_[c]) < 0.05)),
                               mcp=float(np.mean(np.abs(tt[c]) >= abs(TAB_II[("sig_f", ("LAW", "canonical"), c)]["tau"]) - 1e-12)))
            P(f"    a={a:+.2f} {c:6s}: tau_sim {MC8[(a,c)]['mean']:+.3f}+-{MC8[(a,c)]['sd']:.3f}, FP(p<.01) {MC8[(a,c)]['fp01']:.3f}, FP(p<.05) {MC8[(a,c)]['fp05']:.3f}, MC p of the observed tau {MC8[(a,c)]['mcp']:.3f}")
    RESULTS["mc_ii"] = {f"{a}|{c}": v for (a, c), v in MC8.items()}

P(f"\nFAILS: {FAILS if FAILS else 'none'}; elapsed {time.time()-T0:.0f} s")
tag = "_MUTATE" if MUTATE else ""
json.dump(dict(mutate=MUTATE, fails=FAILS, results=RESULTS), open(os.path.join(HERE, f"cfg80_results{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg80{tag}.out"), "w").write("\n".join(OUT))
sys.exit(1 if FAILS else 0)
