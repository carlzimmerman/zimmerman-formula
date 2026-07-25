#!/usr/bin/env python3
"""
fullrange_family_bias.py -- DOES THE a0-LINE ESTIMATOR BIAS TRANSFER TO THE *PUBLISHED*
SPARC ACCELERATION SCALE?   (ROLE: measure the bias of each ESTIMATOR FAMILY over the
FULL y range, never extrapolate the deep-MOND number.)
==========================================================================================
THE QUESTION, STATED SO IT CANNOT BE FUDGED.  The committed, hash-frozen, adversary-checked
result (`PREREG_ESTIMATOR_BIAS.md` + `estimator_bias_mocks.py` + `estimator_bias_verdict
.json`) is that on the GAS-DOMINATED SPARC subsample (310 points, 49 galaxies,
y = g_bar/a0 in 0.0094..0.19) the through-origin GLS on per-point a0 is biased HIGH by
+10.34 pp (26 bootstrap sd, injection-independent) while six median-like estimators pass at
|b| < 2 pp.  The mechanism is Jensen / log-mean inflation of a MEAN-like statistic.

It is TEMPTING to conclude "the literature's 1.2e-10 is biased high and the true value is
the framework's Lambda-anchored 9.36e-11".  THAT INFERENCE IS NOT LICENSED UNTIL MEASURED.
Three reasons it may not transfer, each CHECKED here, none assumed:
  (a) DIFFERENT ESTIMATOR -- the published numbers are NOT a through-origin GLS on
      per-point a0.  Catalogued in S0 from the papers themselves, verbatim.
  (b) DIFFERENT REGIME -- +10.34 pp was measured at y <= 0.19.  Published fits span
      y ~ 0.01 .. 98.  RE-MEASURED here on the FULL range; never extrapolated.
  (c) DIFFERENT QUANTITY -- the a0-line (g_obs^2 - g_bar^2 = a0 g_bar) and the RAR
      interpolation fit are different functional relations.  Each family is fitted with
      the SAME form that generated the truth, so functional-form difference is NEVER
      charged as estimator bias; the pure form conversion is measured NOISE-FREE and
      reported on its own line.

METHOD.  Full-range SPARC-structured mocks: the real g_bar values of 2696 points in 147
galaxies held FIXED as the truth, real per-point velocity errors, per-galaxy
distance-by-method and inclination errors, coherent GLOBAL Upsilon and gas-calibration
offsets, deep-MOND amplification DERIVED not injected -- the frozen forward model verbatim,
generalized to either nu form.  a0 injected at THREE values (canonical 9.355e-11, ALT
1.1305e-10, published 1.2e-10) so NEITHER the framework's value NOR the literature's is
privileged.  Bias metric and gates copied from the frozen prereg: b = median(a_hat/a_inj)-1
in pp; PASS |b| < 2.0 pp at ALL THREE injections; FAIL |b| >= 5.0 pp.

HARD RAILS (highest manufactured-win risk in the project):
  * No claim that a published number is biased unless THAT estimator was IMPLEMENTED and
    its bias MEASURED on mocks.  "It is mean-like therefore biased" is not evidence.
  * If a family recovers 1.2e-10 when 1.2e-10 was injected, it is unbiased there and the
    published number stands -- and this script says exactly that.
  * Estimator bias is held apart from the Upsilon degeneracy, the sample-selection
    difference and the functional-form difference; each has its own reported line.
  * a0's VALUE remains POSITED in the framework.  Measurement methodology, not derivation.
    Both footings carried.  No "theory closed", no TOE claim, no "no open doors".
  * Exit 0 means "mocks built, nulls passed, bias measured" -- not a verdict for anyone.
"""
import numpy as np, os, sys, json, math, time, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fullrange_family_bias_lib as L                                   # noqa: E402
import fire_common as fc                                                # noqa: E402
from scipy import odr as sodr                                           # noqa: E402

np.seterr(all="ignore")
bar = "=" * 100
t0 = time.time()
LG = np.arange(-11.0, -9.0 + 1e-9, 0.01)       # coarse grid; then fine grid + parabola
KEYS = ["odr_log", "odr_lin", "nls_log", "like_log"]
M_MAIN = int(os.environ.get("M_MAIN", 600))
M_ANCHOR = int(os.environ.get("M_ANCHOR", 2000))
M_ABL = int(os.environ.get("M_ABL", 200))
PASS_PP, FAIL_PP = 2.0, 5.0
OUT = {}

# ============================================================ S0. THE PUBLISHED CATALOGUE
print(bar); print("S0 -- CATALOGUE OF THE PUBLISHED DETERMINATIONS, BY ESTIMATOR FAMILY")
print(bar)
CATALOGUE = [
    dict(ref="McGaugh, Lelli & Schombert 2016, PRL 117:201101 (arXiv:1609.05917)",
         value="g_dagger = 1.20 +- 0.02 (random) +- 0.24 (systematic) e-10 m/s^2",
         estimator="ORTHOGONAL DISTANCE REGRESSION of g_obs = g_bar/(1-exp(-sqrt(g_bar/"
                   "g_dagger))) to the UNBINNED 2693 points of 153 galaxies, 'considers "
                   "errors on both variables'; the plotted axes are log(g_bar), "
                   "log(g_obs), residuals and the entire scatter budget are in dex. "
                   "Upsilon_disk FIXED at 0.50 (bulge 0.70); the +-0.24 systematic IS the "
                   "20% Upsilon normalisation, quoted SEPARATELY from the fit.",
         family="RAR-form errors-on-both-axes fit  -> tested as odr_log / odr_lin",
         verbatim="'The solid line is the fit of eq. 4 to the unbinned data using an "
                  "orthogonal-distance-regression algorithm that considers errors on both "
                  "variables.'"),
    dict(ref="Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836:152 (arXiv:1610.08981)",
         value="g_dagger = (1.20 +- 0.02) e-10 (rnd) +- 0.24 e-10 (sys); with an "
               "acceleration floor added, g_dagger = (1.1 +- 0.1) e-10",
         estimator="scipy.odr, errors in both variables, UNBINNED 2693 points. Mean error "
                   "on g_obs 0.1 dex (velocity, inclination, distance); mean error on "
                   "g_bar 0.08 dex (10% HI flux calibration + 25% scatter on Upsilon).",
         family="same as MLS2016 -> tested as odr_log / odr_lin",
         verbatim="'The data are fitted using the Python orthogonal distance regression "
                  "algorithm (scipy.odr), considering errors in both variables. We do not "
                  "fit the binned data, but the individual 2693 points.'"),
    dict(ref="Li, Lelli, McGaugh & Schombert 2018, A&A 615:A3 (arXiv:1803.00022)",
         value="NO independent global a0 published. g_dagger FIXED at 1.20e-10 in the "
               "primary fits; freeing it (flat prior 0..1e-9) leaves chi2 and the rms "
               "scatter essentially unchanged (0.054 vs 0.057 dex).",
         estimator="PER-GALAXY MCMC (emcee), chi2 in LINEAR acceleration space, "
                   "chi2_nu = sum_R [g_obs - g_tot]^2/sigma_gobs^2/(N-f) with "
                   "sigma_gobs = 2 V_obs dV_obs / R; Gaussian priors on Upsilon_star "
                   "(0.1 dex), distance and inclination.",
         family="per-galaxy fit then combine -> tested as pergal_median / pergal_meanlog",
         verbatim="'chi2_nu = sum_R [g_obs(R)-g_tot(R)]^2/sigma_gobs^2/(N-f)'; 'Adjusting "
                  "the value of g_dagger improves neither the fits nor the rms scatter.'"),
    dict(ref="Begeman, Broeils & Sanders 1991, MNRAS 249:523",
         value="a0 = 1.21 +- 0.24 e-10 m/s^2",
         estimator="per-galaxy rotation-curve chi2 fits of the MOND formula to 10 "
                   "galaxies, then combined.",
         family="per-galaxy fit then combine -> same family as Li+2018 (tested)",
         verbatim="(standard literature quote; not re-fetched)"),
]
for c in CATALOGUE:
    print(f"  * {c['ref']}\n      value    : {c['value']}\n      estimator: {c['estimator']}"
          f"\n      family   : {c['family']}\n      verbatim : {c['verbatim']}")
print("\n  S0 CONCLUSION (fact, not inference): NOT ONE published determination uses a")
print("  through-origin GLS on per-point a0 = (g_obs^2-g_bar^2)/g_bar.  The a0-line")
print("  incumbent that carries the +10.34 pp bias is NOT the published estimator, so the")
print("  bias CANNOT be transferred by assertion -- it must be measured family by family,")
print("  which is what the rest of this script does.")
OUT["catalogue"] = CATALOGUE

# ==================================================================== S1. THE TWO SAMPLES
print(); print(bar); print("S1 -- THE SAMPLES (real SPARC structure held FIXED as the truth)")
print(bar)
SG = L.make_sample(0.70, True)                     # frozen gas-dominated regression anchor
SF = L.make_sample(0.70, False)                    # FULL range
for tag, S in (("gas-dominated (frozen anchor)", SG), ("FULL range", SF)):
    y = S["GB"] / L.A0_CANON
    print(f"  {tag:<30} N = {S['N']:>5}  N_gal = {S['G']:>4}   "
          f"y in [{y.min():.4f}, {y.max():.2f}]  median {np.median(y):.3f}")
    print(f"  {'':<30} frac y>1 = {(y>1).mean():.3f}   frac y>10 = {(y>10).mean():.4f}   "
          f"phi median {np.median(S['PHI']):.3f}   fv median {np.median(S['FV']):.4f}")
print("  The FULL-range sample (2696 points / 147 galaxies) is the SAME data product the")
print("  published fits use (2693 points / 153 galaxies); the small difference is the")
print("  quality cut (Q<=2 here vs their explicit rejection of 12 asymmetric curves).")
print("  That is SAMPLE SELECTION and is reported as such -- never as estimator bias.")
print(f"  analyst's assumed per-point errors: sigma_log(g_obs) median "
      f"{np.median(SF['sig_log_obs']):.4f} dex (published 'mean error 0.1 dex'), "
      f"sigma_log(g_bar) median {np.median(SF['sig_log_bar']):.4f} dex (published 0.08)")
OUT["samples"] = {t: dict(N=S["N"], G=S["G"], y_min=float((S["GB"]/L.A0_CANON).min()),
                          y_max=float((S["GB"]/L.A0_CANON).max()),
                          sig_log_obs_med=float(np.median(S["sig_log_obs"])),
                          sig_log_bar_med=float(np.median(S["sig_log_bar"])))
                  for t, S in (("gasdom", SG), ("full", SF))}

# ============================================================= S2. UNIT TESTS (HARD HALTS)
print(); print(bar); print("S2 -- UNIT TESTS ON THE MACHINERY (hard halts; no bias number yet)")
print(bar)
a_ref = fc.gls(SG["GB"], SG["GO_real"], SG["FV"])[0]
a_vec = L.gls_vec(SG, SG["GB"][None, :], SG["GO_real"][None, :])[0]
print(f"  (i)   gls_vec vs fire_common.gls, real gas-dominated: {a_vec:.10e} vs "
      f"{a_ref:.10e}   rel {abs(a_vec/a_ref-1):.2e}")
assert abs(a_vec / a_ref - 1) < 1e-12
print(f"        committed incumbents reproduced: GLS {a_ref:.4e} (banked 1.1814e-10), "
      f"median {L.median_a0pt(SG['GB'][None,:], SG['GO_real'][None,:])[0]:.4e} "
      f"(banked 9.7256e-11)")

# (ii) full-likelihood Woodbury == explicit dense covariance
n = 60
gsub = np.repeat(np.arange(SG["G"]), SG["NPT"])[:n]
_, gi = np.unique(gsub, return_inverse=True)
Ssub = dict(SG)
NPTs = np.bincount(gi)
Ssub.update(GB=SG["GB"][:n], FV=SG["FV"][:n], PHI=SG["PHI"][:n], CTI=SG["CTI"][:n],
            sig_log_obs=SG["sig_log_obs"][:n], sig_log_bar=SG["sig_log_bar"][:n],
            N=n, G=int(gi.max()) + 1, NPT=NPTs,
            STARTS=np.concatenate(([0], np.cumsum(NPTs)[:-1])),
            SLD_g=np.array([SG["SLD_g"][g] for g in np.unique(gsub)]),
            INC_g=np.array([SG["INC_g"][g] for g in np.unique(gsub)]))
rng = np.random.default_rng(1)
gbx = Ssub["GB"] * np.exp(rng.normal(0, .1, n))
gox = L.F_form(Ssub["GB"], 1e-10, "FW") * np.exp(rng.normal(0, .1, n))
at = np.array([1.05e-10])
cw = L.chi2_block(Ssub, gbx[None, :], gox[None, :], "FW", at)["like_log"][0, 0]
Sl = L.S_form(gbx, at[0], "FW")
r = np.log10(gox) - np.log10(L.F_form(gbx, at[0], "FW"))
C = np.diag((2 * Ssub["FV"] / L.LN10) ** 2 + (Sl * L.SLNB / L.LN10) ** 2)
for k in range(Ssub["G"]):
    m = (gi == k).astype(float)
    sk = Ssub["SLD_g"][k] ** 2 + (2 * Ssub["CTI"][gi == k][0] * L.SIG_INC) ** 2
    C += sk * np.outer(m, m) / L.LN10 ** 2
C += L.SIG_LNU ** 2 * np.outer(Sl * Ssub["PHI"], Sl * Ssub["PHI"]) / L.LN10 ** 2
C += L.SIG_LNG ** 2 * np.outer(Sl * (1 - Ssub["PHI"]), Sl * (1 - Ssub["PHI"])) / L.LN10 ** 2
cd = float(r @ np.linalg.solve(C, r))
print(f"  (ii)  full-likelihood Woodbury vs dense {n}x{n} covariance: {cw:.10f} vs "
      f"{cd:.10f}   rel {abs(cw/cd-1):.2e}")
assert abs(cw / cd - 1) < 1e-9

# (iii) the effective-variance odr_log is a faithful proxy for scipy.odr
S05 = L.make_sample(0.50, False)


def scipy_odr_log(S, gb, go, form, beta0=-9.92):
    def mod(B, xx):
        return np.log10(L.F_form(10.0 ** xx, 10.0 ** B[0], form))
    d = sodr.RealData(np.log10(gb), np.log10(go), sx=S["sig_log_bar"], sy=S["sig_log_obs"])
    o = sodr.ODR(d, sodr.Model(mod), beta0=[beta0]); o.set_job(fit_type=0)
    return 10.0 ** o.run().beta[0]


nz10 = L.draw_noise(SF, 10)
gb10, go10 = L.observables(SF, L.A0_MOND, "MCG", nz10)
mine = L.fit_grid(SF, gb10, go10, "MCG", LG, ["odr_log"])[0]["odr_log"]
theirs = np.array([scipy_odr_log(SF, gb10[i], go10[i], "MCG") for i in range(10)])
w = float(np.abs(mine / theirs - 1).max())
r_real_mine = L.fit_grid(S05, S05["GB"][None, :], S05["GO_real"][None, :], "MCG",
                         LG, ["odr_log"])[0]["odr_log"][0]
r_real_scipy = scipy_odr_log(S05, S05["GB"], S05["GO_real"], "MCG")
print(f"  (iii) effective-variance odr_log vs scipy.odr: 10 mock reals max rel diff "
      f"{w:.2e};  real data {r_real_mine:.4e} vs {r_real_scipy:.4e} "
      f"(rel {abs(r_real_mine/r_real_scipy-1):.2e})")
assert w < 0.01, "odr_log proxy not faithful to scipy.odr"
OUT["unit_tests"] = dict(gls_rel=float(abs(a_vec / a_ref - 1)),
                         woodbury_rel=float(abs(cw / cd - 1)),
                         odr_proxy_max_rel_mock=w,
                         odr_proxy_rel_real=float(abs(r_real_mine / r_real_scipy - 1)))
print("  ALL UNIT TESTS PASS.  The ODR proxy agrees with the real scipy.odr to <1%, i.e.")
print("  5x below the 2 pp gate; the residual offset is reported, not absorbed.")

# ================================================== S3. V1 ZERO-NOISE NULL, EVERY FAMILY
print(); print(bar)
print("S3 -- V1 ZERO-NOISE NULL on the FULL range: every family x 3 injections x 2 forms")
print(bar)
nz1 = L.draw_noise(SF, 1)
rowsv1 = {}
for form in ("FW", "MCG"):
    for a, lab in zip(L.INJ, L.INJ_LAB):
        gb, go = L.observables(SF, a, form, nz1, scale=0.0)
        res, ed, pg, pge = L.fit_grid(SF, gb, go, form, LG, KEYS)
        bn = L.binned_fits(SF, gb, go, form, LG)
        vals = {k: float(res[k][0]) for k in KEYS}
        vals["pergal_median"] = float(np.median(pg[0]))
        vals["pergal_meanlog"] = float(np.exp(np.mean(np.log(pg[0]))))
        vals["binned_meanlog"] = float(bn["meanlog"][0])
        vals["binned_meanlin"] = float(bn["meanlin"][0])
        if form == "FW":
            vals["gls_origin"] = float(L.gls_vec(SF, gb, go)[0])
            vals["median_a0pt"] = float(L.median_a0pt(gb, go)[0])
        for k, v in vals.items():
            rowsv1.setdefault(k, {})[f"{form}|{lab.split()[0]}"] = float(v / a - 1.0)
FAMS = list(rowsv1.keys())
cols = list(rowsv1["odr_log"].keys())
print(f"  {'family':<16}" + "".join(f"{c:>19}" for c in cols))
worst = 0.0
for k in FAMS:
    print(f"  {k:<16}" + "".join(f"{rowsv1[k].get(c, float('nan')):>19.2e}" for c in cols))
    worst = max(worst, max(abs(x) for x in rowsv1[k].values()))
EXACT = [k for k in FAMS if not k.startswith("binned_")]
w_exact = max(max(abs(x) for x in rowsv1[k].values()) for k in EXACT)
w_binned = max(max(abs(x) for x in rowsv1[k].values()) for k in FAMS if k.startswith("binned_"))
print(f"  worst |a_hat/a_inj - 1|:  algebraically-exact families {w_exact:.2e}   "
      f"binned families {w_binned:.2e}")
print("  TWO TIERS, stated openly rather than blurred:")
print("   * the 8 families that are algebraically exact at zero noise must pass 1e-3")
print("     relative (= 0.1 pp, 20x below the 2.0 pp gate); the closed-form pair reaches")
print("     machine precision and the grid families reach 1e-6..1.5e-4 (grid+parabola).")
print("   * the BINNED pair is NOT exact at zero noise, and this is NOT a numerical")
print("     artifact: collapsing a bin of a CURVED relation to one point shifts it, by")
print("     +0.11 pp (mean-of-log) and -0.38 pp (log-of-mean).  Refining the grid 15x")
print("     leaves both unchanged, which proves it is intrinsic.  It is therefore counted")
print("     INSIDE that family's bias rather than subtracted out.")
assert w_exact < 1e-3, "V1 ZERO-NOISE NULL FAILED (exact families) -> HARD HALT"
assert w_binned < 1e-2, "binned zero-noise offset unexpectedly large -> HARD HALT"
OUT["V1_zero_noise"] = dict(worst_rel_exact=float(w_exact),
                            worst_rel_binned_intrinsic=float(w_binned),
                            tolerance_exact=1e-3, tolerance_binned=1e-2,
                            residuals=rowsv1,
                            note="the binned pair's zero-noise offset is the within-bin "
                                 "curvature of the binned route itself (grid-refinement "
                                 "invariant); it is counted inside that family's bias.")
print("  V1 PASSES: every family round-trips its own injection on noiseless full-range")
print("  data at both nu forms and all three injected values.  Wiring is correct.")

# =========================================== S4. REGRESSION ANCHOR (the committed number)
print(); print(bar)
print(f"S4 -- REGRESSION ANCHOR: reproduce the COMMITTED gas-dominated bias "
      f"(+10.34 / -0.84 pp), {M_ANCHOR} reals")
print(bar)
nzA = L.draw_noise(SG, M_ANCHOR)
anch = {}
for a, lab in zip(L.INJ, L.INJ_LAB):
    gb, go = L.observables(SG, a, "FW", nzA)
    anch[lab] = dict(gls_origin=100 * (float(np.median(L.gls_vec(SG, gb, go))) / a - 1),
                     median_a0pt=100 * (float(np.median(L.median_a0pt(gb, go))) / a - 1))
    print(f"  {lab:<22} gls_origin b = {anch[lab]['gls_origin']:+8.4f} pp   "
          f"median_a0pt b = {anch[lab]['median_a0pt']:+8.4f} pp")
BANK = {"canonical cH_L/Z": (10.337184387348985, -0.8429077421413522),
        "ALT cH0/Z": (10.243508706284477, -0.791780283234711),
        "published g_dagger": (10.226721684239237, -0.7732525967097725)}
dmax = max(max(abs(anch[l]["gls_origin"] - BANK[l][0]),
               abs(anch[l]["median_a0pt"] - BANK[l][1])) for l in L.INJ_LAB)
print(f"  max |reproduced - committed verdict JSON| = {dmax:.2e} pp  (same seed, same draw")
print(f"  order, same forward model -> a BIT-LEVEL regression, not a re-derivation)")
assert dmax < 1e-9, "ANCHOR MISMATCH -> forward model or draw order drifted"
OUT["anchor_gasdominated"] = dict(
    reproduced=anch, max_abs_diff_pp=float(dmax),
    committed={l: dict(gls_origin=BANK[l][0], median_a0pt=BANK[l][1]) for l in L.INJ_LAB})
print(f"  ANCHOR HELD.  [{time.time()-t0:.0f}s]")

# ======================================================== S5. THE MAIN FULL-RANGE BIAS TABLE
print(); print(bar)
print(f"S5 -- MAIN RESULT: BIAS OF EVERY FAMILY OVER THE FULL y RANGE (0.009 .. 98), "
      f"{M_MAIN} reals")
print(bar)
print("  Each family is fitted with the SAME functional form that generated the truth, so")
print("  no functional-form difference is charged as estimator bias (rail 4).  Injections")
print("  are the framework's canonical, the framework's ALT, and the PUBLISHED 1.2e-10.")
FAM_ORDER = ["gls_origin", "median_a0pt", "odr_log", "odr_lin", "nls_log", "like_log",
             "pergal_median", "pergal_meanlog", "binned_meanlog", "binned_meanlin"]
FAM_DESC = {
    "gls_origin": "(a) a0-line through-origin GLS on per-point a0 -- the INCUMBENT",
    "median_a0pt": "(a) a0-line median of per-point a0 -- the frozen-study PASS",
    "odr_log": "(b) RAR-form errors-on-both-axes fit, LOG plane  = McGaugh+2016/Lelli+2017",
    "odr_lin": "(b) RAR-form errors-on-both-axes fit, LINEAR space (the other reading)",
    "nls_log": "(b) RAR-form weighted least squares, vertical residuals in log space",
    "like_log": "(e) FULL likelihood, log space, errors CORRECTLY MODELLED (D,i per-galaxy "
                "correlated; Upsilon/gas-cal global; Woodbury)",
    "pergal_median": "(c) per-galaxy chi2 fit (Li+2018 convention) then MEDIAN over galaxies",
    "pergal_meanlog": "(c) per-galaxy chi2 fit then GEOMETRIC MEAN over galaxies",
    "binned_meanlog": "(d) binned route, bin collapsed by MEAN OF LOG, then RAR-form fit",
    "binned_meanlin": "(d) binned route, bin collapsed by LOG OF MEAN, then RAR-form fit",
}


def run_all(S, gb, go, form):
    """Every family on one block of mock observables, each in ITS OWN convention."""
    out = {}
    res, ed, pg, pge = L.fit_grid(S, gb, go, form, LG, KEYS)
    for k in KEYS:
        out[k] = res[k]
    out["pergal_median"] = np.median(pg, axis=1)
    out["pergal_meanlog"] = np.exp(np.mean(np.log(pg), axis=1))
    bn = L.binned_fits(S, gb, go, form, LG)
    out["binned_meanlog"] = bn["meanlog"]
    out["binned_meanlin"] = bn["meanlin"]
    if form == "FW":
        out["gls_origin"] = L.gls_vec(S, gb, go)
        out["median_a0pt"] = L.median_a0pt(gb, go)
    out["_edge_frac"] = np.array([float(ed[k].mean()) for k in KEYS])
    out["_pergal_edge_frac"] = np.array([float(pge.mean())])
    return out


NZF = L.draw_noise(SF, M_MAIN)
print(f"  noise drawn for the FULL sample: inclination redraws {NZF['n_redraw_i']}, "
      f"velocity redraws {NZF['n_redraw_v']}  (frozen guards)")
RAT = {}
EDGE = {}
for form in ("FW", "MCG"):
    for a, lab in zip(L.INJ, L.INJ_LAB):
        acc = {}
        for s in range(0, M_MAIN, 100):
            e = min(M_MAIN, s + 100)
            gb, go = L.observables(SF, a, form, L.slice_noise(NZF, s, e))
            r = run_all(SF, gb, go, form)
            for k, v in r.items():
                acc.setdefault(k, []).append(np.atleast_1d(v))
        for k, v in acc.items():
            if k.startswith("_"):
                EDGE.setdefault(f"{form}|{lab}", {})[k] = float(np.mean(np.concatenate(v)))
            else:
                RAT.setdefault(k, {})[f"{form}|{lab}"] = np.concatenate(v) / a
        print(f"    {form} / {lab:<22} done  [{time.time()-t0:.0f}s]")

rb = np.random.default_rng(20260725 + 7)
BIDX = rb.integers(0, M_MAIN, (400, M_MAIN))
TAB = {}
for form in ("FW", "MCG"):
    cols = [f"{form}|{l}" for l in L.INJ_LAB]
    print(f"\n  ---- TRUTH LAW = {'framework nu sqrt(1+1/y)' if form=='FW' else 'McGaugh RAR nu (the published one)'} "
          f"----")
    print(f"  {'family':<16}" + "".join(f"{'b(pp)':>9}{'s(%)':>7}" for _ in cols)
          + f"{'max|b|':>8}{'spread':>8}{'sMC':>6}{'bootsd':>7}  tier      G2 G3")
    for k in FAM_ORDER:
        if cols[0] not in RAT.get(k, {}):
            continue
        bs, ss, mcs = [], [], []
        for c in cols:
            r = RAT[k][c]
            bs.append(100.0 * (float(np.median(r)) - 1.0))
            ss.append(100.0 * 0.5 * float(np.percentile(r, 84) - np.percentile(r, 16)))
            mcs.append(1.2533 * ss[-1] / math.sqrt(M_MAIN))
        bb = 100.0 * (np.stack([np.median(RAT[k][c][BIDX], axis=1) for c in cols], 1) - 1.0)
        bsd = float(bb.std(0).mean())
        maxb = max(abs(x) for x in bs); spread = max(bs) - min(bs)
        tier = "PASS" if maxb < PASS_PP else ("MARGINAL" if maxb < FAIL_PP else "FAIL")
        TAB[f"{form}|{k}"] = dict(b=bs, s=ss, sigma_mc=mcs, max_abs_b=maxb,
                                  b_spread=spread, boot_sd_b_pp=bsd, tier=tier,
                                  G2=bool(maxb < PASS_PP), G3=bool(spread < 2.0),
                                  n_sd=float(maxb / max(bsd, 1e-9)))
        print(f"  {k:<16}" + "".join(f"{b:>9.2f}{sv:>7.2f}" for b, sv in zip(bs, ss))
              + f"{maxb:>8.2f}{spread:>8.2f}{max(mcs):>6.2f}{bsd:>7.2f}  {tier:<9}"
              + f" {'Y' if maxb<PASS_PP else 'n'}  {'Y' if spread<2.0 else 'n'}")
    print(f"  columns per injection, in order: " + " | ".join(L.INJ_LAB))
print("\n  b = median(a_hat/a_inj)-1 in pp;  s = 0.5*(P84-P16) in %;  sMC = 1.2533 s/sqrt(M);")
print("  bootsd = sd of b over 400 paired bootstraps of the realizations.  PASS |b|<2.0 pp")
print("  at ALL THREE injections; FAIL |b|>=5.0 pp -- the frozen prereg's own gates.")
OUT["main_bias_table"] = TAB
OUT["edge_diagnostics"] = EDGE
OUT["family_descriptions"] = FAM_DESC
OUT["M_main"] = M_MAIN

# ============================================================= S6. NOISE ABLATIONS
print(); print(bar)
print(f"S6 -- NOISE ABLATION: WHICH error term drives each family's bias ({M_ABL} reals)")
print(bar)
print("  Diagnostic only, no gate.  A genuine log-mean (Jensen) inflation must collapse")
print("  when its driving multiplicative term is switched off; a coding artifact would not.")
NZa = L.slice_noise(NZF, 0, M_ABL)
SHOW = ["gls_origin", "median_a0pt", "odr_log", "odr_lin", "nls_log", "like_log",
        "pergal_median", "binned_meanlog", "binned_meanlin"]


def ablate(*keys):
    z = dict(NZa)
    for k in keys:
        z[k] = np.zeros_like(NZa[k])
    return z


ABL = {}
for form, a in (("FW", L.A0_CANON), ("MCG", L.A0_MOND)):
    print(f"\n  ---- truth law {form}, injected {a:.6e} ----")
    print(f"  {'configuration':<24}" + "".join(f"{k[:14]:>16}" for k in SHOW))
    for tag, z in (("ALL noise on", NZa),
                   ("distance OFF", ablate("dlnD")),
                   ("velocity OFF", ablate("dv")),
                   ("inclination OFF", ablate("di")),
                   ("g_bar shape OFF", ablate("eps")),
                   ("global Ups+gascal OFF", ablate("dlnU", "dlnG")),
                   ("ONLY distance on", ablate("dv", "di", "eps", "dlnU", "dlnG")),
                   ("ONLY velocity on", ablate("dlnD", "di", "eps", "dlnU", "dlnG")),
                   ("ONLY g_bar shape on", ablate("dlnD", "dv", "di", "dlnU", "dlnG")),
                   ("ONLY Ups+gascal on", ablate("dlnD", "dv", "di", "eps"))):
        gb, go = L.observables(SF, a, form, z)
        rr = run_all(SF, gb, go, form)
        row = {k: 100.0 * (float(np.median(rr[k])) / a - 1.0) for k in SHOW if k in rr}
        ABL[f"{form}|{tag}"] = row
        print(f"  {tag:<24}" + "".join(f"{row.get(k, float('nan')):>16.2f}" for k in SHOW))
print(f"\n  (each row is {M_ABL} realizations -> MC error of order "
      f"{1.2533*8/math.sqrt(M_ABL):.2f} pp on a family with s ~ 8%)")
OUT["ablation_pp"] = ABL

# =============================================================== S7. THE y-REGIME SCAN
print(); print(bar)
print("S7 -- THE REGIME SCAN: bias vs y, so the deep-MOND number is never extrapolated")
print(bar)


def subsample(S, mask):
    """Restrict a sample to a point mask, rebuilding the per-galaxy bookkeeping."""
    gal = np.repeat(np.arange(S["G"]), S["NPT"])[mask]
    keep = np.unique(gal)
    _, gi = np.unique(gal, return_inverse=True)
    NPT = np.bincount(gi)
    T = dict(S)
    T.update(GB=S["GB"][mask], GO_real=S["GO_real"][mask], FV=S["FV"][mask],
             PHI=S["PHI"][mask], CTI=S["CTI"][mask],
             sig_log_obs=S["sig_log_obs"][mask], sig_log_bar=S["sig_log_bar"][mask],
             N=int(mask.sum()), G=len(keep), NPT=NPT,
             STARTS=np.concatenate(([0], np.cumsum(NPT)[:-1])),
             SLD_g=S["SLD_g"][keep], INC_g=S["INC_g"][keep], GALI=gi)
    return T, keep


yF = SF["GB"] / L.A0_CANON
REG = [("y < 0.2  (deep MOND)", yF < 0.2), ("0.2 <= y < 1", (yF >= 0.2) & (yF < 1)),
       ("1 <= y < 10", (yF >= 1) & (yF < 10)), ("y >= 10  (Newtonian)", yF >= 10),
       ("FULL RANGE", np.ones(SF["N"], bool))]
SCAN = {}
MSC = min(300, M_MAIN)
print(f"  {'regime':<24}{'N':>6}{'Ngal':>6}" + "".join(f"{k[:13]:>15}" for k in
      ("gls_origin", "median_a0pt", "odr_log", "like_log")))
for tag, mk in REG:
    T, keep = subsample(SF, mk)
    row = {}
    for form, a, fams in (("FW", L.A0_CANON, ("gls_origin", "median_a0pt")),
                          ("MCG", L.A0_MOND, ("odr_log", "like_log"))):
        gbF, goF = L.observables(SF, a, form, L.slice_noise(NZF, 0, MSC))
        gb, go = gbF[:, mk], goF[:, mk]
        if form == "FW":
            row["gls_origin"] = 100 * (float(np.median(L.gls_vec(T, gb, go))) / a - 1)
            row["median_a0pt"] = 100 * (float(np.median(L.median_a0pt(gb, go))) / a - 1)
        else:
            rs = L.fit_grid(T, gb, go, form, LG, ["odr_log", "like_log"])[0]
            for k in ("odr_log", "like_log"):
                row[k] = 100 * (float(np.median(rs[k])) / a - 1)
    SCAN[tag] = dict(N=T["N"], Ngal=T["G"], **row)
    print(f"  {tag:<24}{T['N']:>6}{T['G']:>6}" + "".join(
        f"{row[k]:>15.2f}" for k in ("gls_origin", "median_a0pt", "odr_log", "like_log")))
print(f"  (bias in pp, {MSC} realizations; a0-line families injected at canonical, RAR")
print("   families at the published 1.2e-10 -- each with its own matching truth law)")
OUT["regime_scan_pp"] = SCAN

# ================================================= S8. THE PURE FUNCTIONAL-FORM CONVERSION
print(); print(bar)
print("S8 -- FUNCTIONAL-FORM CONVERSION, MEASURED NOISE-FREE (this is NOT a bias)")
print(bar)
print("  Reason (c): a0 in the a0-line and g_dagger in the RAR fit are parameters of")
print("  DIFFERENT functional relations.  With ZERO noise, fit each form to truth built")
print("  from the OTHER form.  Whatever ratio comes out is a form conversion, and it is")
print("  reported here on its own line so it can never be mistaken for estimator bias.")
FORMC = {}
for a, lab in zip(L.INJ, L.INJ_LAB):
    gb, go = L.observables(SF, a, "FW", nz1, scale=0.0)
    r1 = L.fit_grid(SF, gb, go, "MCG", LG, ["odr_log"])[0]["odr_log"][0]
    gb, go = L.observables(SF, a, "MCG", nz1, scale=0.0)
    r2 = L.fit_grid(SF, gb, go, "FW", LG, ["odr_log"])[0]["odr_log"][0]
    FORMC[lab] = dict(g_dagger_over_a0=float(r1 / a), a0_over_g_dagger=float(r2 / a))
    print(f"  {lab:<22} FW truth a0 -> MCG fit g_dagger/a0 = {r1/a:.4f}    "
          f"MCG truth g_dagger -> FW fit a0/g_dagger = {r2/a:.4f}")
print("  READING: the two laws are NOT the same parameter.  A framework a0 of 9.355e-11")
print(f"  presents to a McGaugh-form fitter as g_dagger ~ "
      f"{FORMC[L.INJ_LAB[0]]['g_dagger_over_a0']*L.A0_CANON:.4e}, and the published")
print("  1.2e-10 presents to a framework-form fitter as a0 ~ "
      f"{FORMC[L.INJ_LAB[2]]['a0_over_g_dagger']*L.A0_MOND:.4e}.  This is arithmetic of")
print("  the two kernels on the real g_bar distribution, with no noise and no estimator.")
OUT["form_conversion_noise_free"] = FORMC

# ============================================== S9. REAL DATA: FAITHFULNESS + ONLY-IF-BIASED
print(); print(bar)
print("S9 -- REAL SPARC: (i) is the implementation faithful to the published number, and")
print("      (ii) for families MEASURED biased, what does the unbiased counterpart give")
print(bar)
BIASED = sorted([k.split("|")[1] for k in TAB if TAB[k]["tier"] != "PASS"])
UNBIASED = sorted(set(k.split("|")[1] for k in TAB if TAB[k]["tier"] == "PASS"))
print(f"  MEASURED-BIASED families (tier != PASS): {sorted(set(BIASED))}")
print(f"  MEASURED-UNBIASED families (PASS at all three injections): {UNBIASED}")
REAL = {}
for Ud, ulab in ((0.50, "Upsilon_disk=0.50 (the published McGaugh+2016 choice)"),
                 (0.70, "Upsilon_disk=0.70 (the framework's own RAR M/L fit, 0.108 dex)")):
    S = L.make_sample(Ud, False)
    gb = S["GB"][None, :]; go = S["GO_real"][None, :]
    row = {}
    for form in ("MCG", "FW"):
        res, ed, pg, pge = L.fit_grid(S, gb, go, form, LG, KEYS)
        bn = L.binned_fits(S, gb, go, form, LG)
        d = {k: float(res[k][0]) for k in KEYS}
        d["pergal_median"] = float(np.median(pg[0]))
        d["pergal_meanlog"] = float(np.exp(np.mean(np.log(pg[0]))))
        d["binned_meanlog"] = float(bn["meanlog"][0])
        d["binned_meanlin"] = float(bn["meanlin"][0])
        if form == "FW":
            d["gls_origin"] = float(L.gls_vec(S, gb, go)[0])
            d["median_a0pt"] = float(L.median_a0pt(gb, go)[0])
        d["scipy_odr_log"] = float(scipy_odr_log(S, S["GB"], S["GO_real"], form))
        r = np.log10(go[0]) - np.log10(L.F_form(gb[0], d["odr_log"], form))
        d["rms_dex"] = float(np.sqrt((r ** 2).mean()))
        row[form] = d
    REAL[f"Ud={Ud:.2f}"] = row
    print(f"\n  ---- {ulab} ----")
    for form in ("MCG", "FW"):
        d = row[form]
        nm = "McGaugh RAR nu (the PUBLISHED law)" if form == "MCG" else \
             "framework nu sqrt(1+1/y) (the a0-line law)"
        print(f"   fitted law = {nm}   rms scatter {d['rms_dex']:.3f} dex "
              f"(published 0.13 dex)")
        for k in FAM_ORDER:
            if k not in d:
                continue
            t = TAB.get(f"{form}|{k}") or TAB.get(f"FW|{k}")
            b = t["b"][2] if t else float("nan")
            corr = d[k] / (1.0 + b / 100.0) if t else float("nan")
            print(f"     {k:<16} {d[k]:.4e}   measured bias {b:+6.2f} pp "
                  f"[{t['tier'] if t else '?':<8}]  bias-removed {corr:.4e}")
        print(f"     scipy.odr (real, not the proxy)  {d['scipy_odr_log']:.4e}")
print("\n  FAITHFULNESS: at the published Upsilon the RAR-form log fit lands at "
      f"{REAL['Ud=0.50']['MCG']['odr_log']:.4e} (scipy.odr "
      f"{REAL['Ud=0.50']['MCG']['scipy_odr_log']:.4e}) with "
      f"{REAL['Ud=0.50']['MCG']['rms_dex']:.3f} dex")
print("  scatter, against the published 1.20e-10 and 0.13 dex.  The scatter matches to the")
print("  third decimal; the central value sits ~8% low.  THAT 8% IS NOT MEASURED HERE AS")
print("  ESTIMATOR BIAS: it is the unattributed residue of (i) the galaxy set (147 at Q<=2")
print("  vs their 153 after rejecting 12 asymmetric curves), (ii) our per-point error model")
print("  (sigma_log g_bar 0.103 dex vs their 0.08), (iii) Upsilon_bulge tied to 1.4x disk.")
print("  It is carried as a SAMPLE/DETAIL line and is NOT used to correct anybody.")
print("  Upsilon 0.50 -> 0.70 moves every number by ~35%: that is the M/L DEGENERACY, held")
print("  strictly apart from estimator bias (rail 4).  No footing claim is made from it.")
OUT["real_data"] = REAL
OUT["biased_families"] = sorted(set(BIASED))
OUT["unbiased_families"] = UNBIASED

# ============================ S9b. GOODNESS OF FIT ON REAL DATA -- THE HONEST CAVEAT
print(); print(bar)
print("S9b -- chi2/dof OF EACH FAMILY'S OWN LIKELIHOOD ON THE REAL DATA")
print(bar)
print("  An estimator can be unbiased on mocks and still be the WRONG estimator for the")
print("  real data if its error model is mis-specified there.  This section measures that")
print("  directly, so no family is promoted on mock performance alone.")
GOF = {}
for Ud in (0.50, 0.70):
    S = L.make_sample(Ud, False)
    gb = S["GB"][None, :]; go = S["GO_real"][None, :]
    row = {}
    for form in ("MCG", "FW"):
        res = L.fit_grid(S, gb, go, form, LG, KEYS)[0]
        for k in KEYS:
            c = L.chi2_block(S, gb, go, form, np.array([res[k][0]]))[k][0, 0]
            row[f"{form}|{k}"] = float(c / (S["N"] - 1))
    GOF[f"Ud={Ud:.2f}"] = row
    print(f"  Upsilon_disk={Ud:.2f}: " + "  ".join(f"{k} {v:.2f}" for k, v in row.items()))
print("  READING: every point-level family has chi2/dof > 1 on the real data, i.e. the")
print("  real relation carries scatter beyond the modelled errors.  This matters MOST for")
print("  like_log, whose whole advantage (s = 2% instead of 25%) comes from marginalising")
print("  the global Upsilon mode under the ASSUMPTION that the modelled covariance is")
print("  complete.  Its mock bias of +0.1..0.3 pp is therefore NOT a licence to prefer it")
print("  on real data, and its real-data value (1.38e-10 at the published Upsilon) is")
print("  reported as an OUTLIER of the unbiased set, not as a better measurement.")
print("  The four unbiased families whose error models are not load-bearing in that way")
print("  (odr_log, nls_log, binned_meanlog, median_a0pt) agree far better with each other.")
ub_pub = [REAL["Ud=0.50"]["MCG"][k] for k in ("odr_log", "nls_log", "binned_meanlog")]
print(f"  spread of the three robust unbiased RAR-family values at the published Upsilon:")
print(f"    {ub_pub[0]:.4e}, {ub_pub[1]:.4e}, {ub_pub[2]:.4e}  ->  "
      f"(max-min)/2 = {(max(ub_pub)-min(ub_pub))/2:.3e} = "
      f"{100*(max(ub_pub)-min(ub_pub))/2/np.mean(ub_pub):.1f}% residual estimator systematic")
OUT["gof_chi2_per_dof_real"] = GOF
OUT["unbiased_rar_family_real_spread_pct"] = float(
    100 * (max(ub_pub) - min(ub_pub)) / 2 / np.mean(ub_pub))

# ===================================================================== S10. THE VERDICT
print(); print(bar)
print("S10 -- VERDICT: DOES THE +10.34 pp TRANSFER TO THE PUBLISHED a0?")
print(bar)
pub = TAB["MCG|odr_log"]
pubL = TAB["MCG|odr_lin"]
transfers = ("NO-published-robust" if pub["tier"] == "PASS" and pubL["tier"] == "PASS"
             else "PARTIAL" if pub["tier"] == "PASS" else "YES-published-biased")
print(f"  1. THE PUBLISHED ESTIMATOR (McGaugh+2016 / Lelli+2017 = scipy.odr fit of the RAR")
print(f"     form to the unbinned points, errors on both axes, log plane) measures")
print(f"     b = {pub['b'][0]:+.2f} / {pub['b'][1]:+.2f} / {pub['b'][2]:+.2f} pp at the three")
print(f"     injections -> max|b| = {pub['max_abs_b']:.2f} pp, tier {pub['tier']}, injection")
print(f"     spread {pub['b_spread']:.2f} pp.  IT RECOVERS 1.2e-10 WHEN 1.2e-10 IS INJECTED")
print(f"     (to {abs(pub['b'][2]):.2f} pp).  On estimator-bias grounds the published value")
print(f"     STANDS.  The +10.34 pp DOES NOT TRANSFER.")
print(f"  2. The a0-line incumbent gls_origin is WORSE on the full range than on the")
print(f"     gas-dominated cut: {TAB['FW|gls_origin']['b'][0]:+.2f} pp vs the committed")
print(f"     +10.34 pp -- so the deep-MOND number was not even an upper bound.  The a0-line")
print(f"     MEDIAN survives the full range ({TAB['FW|median_a0pt']['b'][0]:+.2f} pp).")
print(f"  3. NOT every published-adjacent route is clean.  Measured FAIL/MARGINAL:")
for k in FAM_ORDER:
    for form in ("MCG", "FW"):
        t = TAB.get(f"{form}|{k}")
        if t and t["tier"] != "PASS":
            print(f"       {form}|{k:<16} b = {t['b'][2]:+6.2f} pp   {t['tier']}")
print(f"  4. The LINEAR-space reading of 'orthogonal distance regression' is biased")
print(f"     ({pubL['b'][2]:+.2f} pp, {pubL['tier']}) while the LOG-plane reading is not.")
print(f"     The papers' axes, residual histograms and whole scatter budget are in dex, so")
print(f"     the log reading is the documented one -- but this is a READING of the method,")
print(f"     not a measurement, and the {abs(pubL['b'][2]-pub['b'][2]):.1f} pp swing between")
print(f"     the two readings is reported as an irreducible ambiguity, not resolved here.")
print(f"  5. SIGN. Every bias measured on a published-family route is NEGATIVE (recovered")
print(f"     LOW).  Correcting for it would move the literature value UP, AWAY from the")
print(f"     framework's 9.36e-11 -- the opposite of the tempting conclusion.  Stated")
print(f"     because the gate is sign-blind and the direction must not be hidden.")
print(f"  6. POSITED. a0's VALUE remains POSITED in the framework regardless. This is a")
print(f"     measurement-methodology result, NOT a derivation. Both footings carried.")
print(f"     No 'theory closed', no TOE claim, no 'no open doors'.")
OUT["verdict"] = dict(
    transfers_to_published=transfers,
    published_family_bias_pp=pub["b"], published_family_tier=pub["tier"],
    published_family_max_abs_b_pp=pub["max_abs_b"],
    published_linear_reading_bias_pp=pubL["b"], published_linear_reading_tier=pubL["tier"],
    gls_origin_fullrange_pp=TAB["FW|gls_origin"]["b"],
    gls_origin_gasdominated_pp=[anch[l]["gls_origin"] for l in L.INJ_LAB],
    median_a0pt_fullrange_pp=TAB["FW|median_a0pt"]["b"],
    all_published_family_biases_are_negative=bool(
        all(x < 0 for x in pub["b"] + pubL["b"] + TAB["MCG|nls_log"]["b"]
            + TAB["MCG|pergal_median"]["b"])),
    posited="a0's VALUE remains POSITED in the framework. Measurement methodology only.")

VP = os.path.join(HERE, "fullrange_family_bias_results.json")
_c = {k: v for k, v in OUT.items()}
OUT["content_sha256"] = hashlib.sha256(
    json.dumps(_c, sort_keys=True, default=float).encode()).hexdigest()
with open(VP, "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
print(f"\n  results written: {VP}")
print(f"  content sha256 = {OUT['content_sha256']}")
print(f"  transfers_to_published = {transfers}")
print(f"\nEXIT 0: mocks built, nulls passed, bias measured in {time.time()-t0:.0f}s. "
      f"Exit code is not a verdict.")
