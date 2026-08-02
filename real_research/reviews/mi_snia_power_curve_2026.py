#!/usr/bin/env python3
r"""mi_snia_power_curve_2026.py -- THE SN-Ia HOST-STEP LEVER IS UNDERPOWERED, NOT NULL. Injecting the
framework's OWN generating model into the real Pantheon+ arrays and re-running the shipped estimator shows it
recovers a true a0-threshold step only ~1 time in 5.

WHAT WAS BANKED. snia_hoststep_sizextmatch.py (N=449 SDSS-sized hosts) and snia_hoststep_localSB.py (N=450)
both concluded "NULL for the framework-distinctive claim": once host mass is controlled, host acceleration
g_bar = G M*/R_e^2 adds essentially nothing (partial ~ -0.04 against mass ~ -0.20), so the a0 step-LOCATION
coincidence "stands but is NECESSARY-not-SUFFICIENT". STANDING.md and the project memory carry this as
"decisive tests NULL, lever CLOSED".

WHAT WAS NEVER COMPUTED: THE POWER. A null is only a closure if the test could have SEEN the effect. The
shipped statistic is a partial correlation, whose Fisher standard error at N = 449 is 1/sqrt(N-3) = 0.047 --
and the verdict gate is a hard-coded |partial| > 0.10, i.e. 2.1 SE. If the framework's own step model
generates a partial of comparable size, the test is a coin flip and "null" means nothing.

METHOD. Take the REAL de-trended residuals, masses and log(g_bar/a0) from the shipped pipeline. Inject a
step of amplitude D at the framework's own threshold (g_bar = a0, i.e. lg > 0), with NO intrinsic mass term
-- the framework's generating hypothesis. Resample the data's own residual noise. Re-run the SHIPPED
estimator unchanged. Repeat, and count how often it fires. Then invert for the amplitude and the sample size
that would give 80% power. Both a0 footings (a0 sets the threshold location).

  Q1  the estimator's own noise floor vs the signal it is asked to detect
  Q2  THE POWER CURVE -- injection-recovery at D = 0.02-0.20 mag, plus a null control that must NOT fire
  Q3  minimum detectable amplitude and required N at 80% power; both footings
  Q4  what the corpus should say instead of "NULL"

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import csv
import math
import os
import sys

import numpy as np

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 106)
    print(f"  {t}")
    print("=" * 106)


G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0856775814913673e19
A0 = {"canonical 9.36e-11": 9.36e-11, "alt 1.13e-10": 1.13e-10}
DAT = "real_research/data_cache/PantheonPlusSH0ES.dat"
CACHE = "real_research/data_cache/pantheon_sdss_sizes.csv"
GATE = 0.10                      # the shipped verdict gate on |partial|
NSIM = 1500                      # injections per amplitude (bootstrapped SE inside is the slow part)


# ------------------------------------------------------------------ load exactly as the shipped script does
def load():
    from astropy.cosmology import FlatLambdaCDM
    import astropy.units as u
    cosmo = FlatLambdaCDM(H0=73.04, Om0=0.3)
    hdr = open(DAT).readline().split()
    col = {n: i for i, n in enumerate(hdr)}
    rows = [l.split() for l in open(DAT).read().splitlines()[1:]]
    P = {k: np.array([float(r[col[k]]) for r in rows]) for k in
         ['zHD', 'mB', 'x1', 'c', 'RA', 'DEC', 'HOST_LOGMASS', 'IS_CALIBRATOR', 'MU_SH0ES_ERR_DIAG']}
    sel = ((P['IS_CALIBRATOR'] == 0) & (P['zHD'] > 0.01) & (P['zHD'] < 0.25) & (P['HOST_LOGMASS'] > 6)
           & (P['HOST_LOGMASS'] < 13) & (P['MU_SH0ES_ERR_DIAG'] > 0) & (P['MU_SH0ES_ERR_DIAG'] < 1)
           & (P['DEC'] > -11))
    idx = np.where(sel)[0]
    R50 = {}
    for row in csv.DictReader(open(CACHE)):
        try:
            R50[int(row['row'])] = float(row['petroR50_r'])
        except Exception:
            pass
    r50 = np.array([R50.get(int(i), np.nan) for i in idx])
    z, mB, x1, c = P['zHD'][idx], P['mB'][idx], P['x1'][idx], P['c'][idx]
    lm, err = P['HOST_LOGMASS'][idx], P['MU_SH0ES_ERR_DIAG'][idx]
    HR = (mB + 0.148 * x1 - 3.09 * c) - cosmo.distmod(z).value
    DA = cosmo.angular_diameter_distance(z).to(u.kpc).value
    Re = (r50 / 206265.0) * DA
    gbar = G * (10 ** lm * MSUN) / (Re * KPC) ** 2
    good = (np.isfinite(r50) & (r50 > 0.5) & np.isfinite(Re) & (Re > 0.3) & (Re < 40)
            & np.isfinite(gbar) & (lm > 8.5))
    z, lm, err, HR, gbar = z[good], lm[good], err[good], HR[good], gbar[good]
    w = 1.0 / err ** 2
    A = np.column_stack([np.ones_like(z), z])
    Wr = np.sqrt(w)
    beta, *_ = np.linalg.lstsq(A * Wr[:, None], HR * Wr, rcond=None)
    return dict(HRd=HR - A @ beta, lm=lm, w=w, gbar=gbar, z=z)


if not (os.path.exists(DAT) and os.path.exists(CACHE)):
    print(f"  MISSING DATA: {DAT} / {CACHE} -- cannot run.")
    sys.exit(1)
D = load()
HRd, LM, W, GBAR = D["HRd"], D["lm"], D["w"], D["gbar"]
N = len(HRd)


def presid(y, x):
    Xc = np.column_stack([np.ones_like(x), x])
    b, *_ = np.linalg.lstsq(Xc, y, rcond=None)
    return y - Xc @ b


def estimator(hr, lg):
    """the SHIPPED statistic, unchanged: the two partial correlations and the verdict gate."""
    pGM = np.corrcoef(presid(hr, LM), presid(lg, LM))[0, 1]
    pMG = np.corrcoef(presid(hr, lg), presid(LM, lg))[0, 1]
    fires = (abs(pGM) > abs(pMG)) and abs(pGM) > GATE
    return pGM, pMG, fires


banner("Q1  THE ESTIMATOR'S NOISE FLOOR vs THE SIGNAL IT IS ASKED TO DETECT")

print(f"  loaded {N} SDSS-sized Pantheon+ hosts from the shipped pipeline (de-trended in z, as shipped)")
fisher_se = 1.0 / math.sqrt(N - 3)
print(f"  Fisher SE on a partial correlation at N = {N}:  1/sqrt(N-3) = {fisher_se:.4f}")
print(f"  the shipped verdict gate is |partial| > {GATE}  =  {GATE/fisher_se:.2f} SE")
check(1.5 < GATE / fisher_se < 3.0,
      f"Q1a the hard-coded gate {GATE} is {GATE/fisher_se:.2f} Fisher SE -- i.e. it is a ~2 sigma line, not "
      f"an arbitrary threshold. So the gate itself is defensible; the question is whether the framework's "
      f"own signal clears a 2 sigma line at this N")

for fname, a0 in A0.items():
    lg = np.log10(GBAR / a0)
    pGM, pMG, fires = estimator(HRd, lg)
    above = (lg > 0).sum()
    print(f"  REAL DATA, {fname:<20} N(g>a0) = {above:3d}/{N}  partial(HR,g|M) = {pGM:+.4f}  "
          f"partial(HR,M|g) = {pMG:+.4f}  gate fires: {fires}")
check(not estimator(HRd, np.log10(GBAR / A0["canonical 9.36e-11"]))[2],
      "Q1b the shipped verdict on the real data reproduces: the gate does NOT fire, which is the 'NULL' the "
      "corpus banked. Everything below asks whether it COULD have")
pc = estimator(HRd, np.log10(GBAR / A0["canonical 9.36e-11"]))
pa = estimator(HRd, np.log10(GBAR / A0["alt 1.13e-10"]))
check(abs(pc[0] - pa[0]) < 1e-12 and abs(pc[1] - pa[1]) < 1e-12,
      f"Q1c *** THE SHIPPED STATISTIC IS EXACTLY FOOTING-BLIND. *** Changing a0 shifts lg by a CONSTANT, and "
      f"a partial correlation is invariant under affine transformations of its regressor, so both footings "
      f"give bit-identical partials ({pc[0]:+.4f}, {pc[1]:+.4f}). Useful: this front's headline cannot be an "
      f"a0-convention artefact. Also limiting: the statistic carries no information about WHERE a0 is -- only "
      f"the step-LOCATION test does, and that is the one with the coincidence in it")
check(pc[0] > 0,
      f"Q1d AGAINST INTEREST, and the corpus should state it: the real partial(HR,g|M) is {pc[0]:+.4f} -- "
      f"POSITIVE, i.e. OPPOSITE in sign to what the framework's own step model produces (negative, see Q2). "
      f"It is only {abs(pc[0])/fisher_se:.2f} Fisher SE from zero, so it is statistically nothing, but the "
      f"data do not merely fail to support the framework here; they lean very slightly the wrong way")


banner("Q2  THE POWER CURVE -- inject the framework's own step, re-run the shipped estimator")

print(f"""  Generating model = the framework's own hypothesis: HR = -D * 1[g_bar > a0] + noise, with NO
  intrinsic mass term. Noise is the data's OWN de-trended residual, resampled (so its variance, and any
  non-Gaussianity, are real). {NSIM} injections per amplitude. 'fires' = the shipped verdict flips to
  'ACCEL wins'; 'crosses' = |partial(HR,g|M)| alone clears the {GATE} gate regardless of the mass comparison.\n""")
rng = np.random.default_rng(20260802)
AMPS = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.20, 0.25, 0.30, 0.40]
resid_pool = HRd - HRd.mean()
power = {}
for fname, a0 in A0.items():
    lg = np.log10(GBAR / a0)
    hi = lg > 0.0
    print(f"  --- {fname}  (N above threshold = {hi.sum()}) ---")
    print(f"  {'D [mag]':>9}{'fires':>9}{'crosses':>10}{'mean pGM':>11}{'mean pMG':>11}")
    power[fname] = {}
    for Damp in AMPS:
        nf = nc = 0
        pg = pm = 0.0
        for _ in range(NSIM):
            noise = resid_pool[rng.integers(0, N, N)]
            hr = -Damp * hi.astype(float) + noise
            a, b, f = estimator(hr, lg)
            nf += f
            nc += abs(a) > GATE
            pg += a
            pm += b
        power[fname][Damp] = (nf / NSIM, nc / NSIM)
        print(f"  {Damp:>9.2f}{nf/NSIM:>9.3f}{nc/NSIM:>10.3f}{pg/NSIM:>+11.4f}{pm/NSIM:>+11.4f}")

can = "canonical 9.36e-11"
p06 = power[can][0.06]
check(0.05 < p06[0] < 0.60,
      f"Q2a *** AT THE AMPLITUDE THE DATA ACTUALLY SHOW (D = 0.06 mag, the measured host step) THE SHIPPED "
      f"TEST FIRES ONLY {100*p06[0]:.0f}% OF THE TIME *** ({100*p06[1]:.0f}% for the partial alone). A test "
      f"that recovers a true signal one time in {1/max(p06[0],1e-9):.0f} cannot convert a non-detection into "
      f"a closure. This is the whole finding")

# NULL CONTROL: a pure-MASS truth must NOT fire. If it does, the machinery is broken and Q2a means nothing.
nf_null = 0
lg_c = np.log10(GBAR / A0[can])
hi_m = LM > 10.0
pg_null = 0.0
for _ in range(NSIM):
    noise = resid_pool[rng.integers(0, N, N)]
    hr = -0.06 * hi_m.astype(float) + noise
    a, b, f = estimator(hr, lg_c)
    nf_null += f
    pg_null += a
check(nf_null / NSIM < 0.10,
      f"Q2-CONTROL with a PURE-MASS truth injected at the same 0.06 mag the estimator fires only "
      f"{100*nf_null/NSIM:.1f}% of the time and returns mean partial(HR,g|M) = {pg_null/NSIM:+.4f} ~ 0. So the "
      f"estimator is NOT broken and NOT biased toward the framework -- it correctly rejects a mass-only "
      f"world. The low power in Q2a is a sample-size problem, not an estimator problem")

mono = all(power[can][AMPS[i]][0] <= power[can][AMPS[i + 1]][0] + 0.05 for i in range(len(AMPS) - 1))
check(mono,
      "Q2b the power curve is monotone in amplitude (to Monte-Carlo noise), as it must be -- a sanity check "
      "that the injection is entering the estimator the way it is meant to")


banner("Q3  MINIMUM DETECTABLE AMPLITUDE AND REQUIRED N AT 80% POWER")


def interp80(fname, which):
    """amplitude at which criterion `which` (0 = verdict fires, 1 = |pGM| crosses the gate) hits 80%."""
    xs, ys = AMPS, [power[fname][a][which] for a in AMPS]
    for i in range(len(xs) - 1):
        if ys[i] < 0.80 <= ys[i + 1]:
            t = (0.80 - ys[i]) / (ys[i + 1] - ys[i])
            return xs[i] + t * (xs[i + 1] - xs[i])
    return float("nan")


print("  TWO criteria, because they behave differently:")
print("    'verdict'  = the shipped gate, |pGM| > |pMG| AND |pGM| > 0.10")
print("    'crossing' = |pGM| > 0.10 alone\n")
print(f"  {'footing':<22}{'verdict ceiling':>17}{'D80 verdict':>13}{'D80 crossing':>14}"
      f"{'N for 80% @0.06':>18}")
print("  " + "-" * 84)
req = {}
for fname in A0:
    ceil = max(power[fname][a][0] for a in AMPS)
    dv, dc = interp80(fname, 0), interp80(fname, 1)
    nreq = N * (dc / 0.06) ** 2 if np.isfinite(dc) else float("nan")
    req[fname] = (ceil, dv, dc, nreq)
    print(f"  {fname:<22}{ceil:>17.3f}{dv:>13.3f}{dc:>14.3f}{nreq:>18.0f}")

check(req[can][1] > req[can][2] * 1.2,
      f"Q3a *** THE GATE'S COLLINEARITY CLAUSE COSTS A FURTHER FACTOR {req[can][1]/req[can][2]:.1f} IN REQUIRED "
      f"AMPLITUDE. *** The verdict gate reaches 80% power only at D = {req[can][1]:.3f} mag "
      f"({req[can][1]/0.06:.1f}x the real step), against D = {req[can][2]:.3f} mag ({req[can][2]/0.06:.1f}x) for the "
      f"crossing criterion alone. Structural reason: g_bar = G M*/R_e^2 is built FROM the mass, so injecting a "
      f"pure acceleration step necessarily induces a spurious mass partial too, and |pGM| > |pMG| eats the "
      f"margin. (It does clear 80% eventually -- ceiling {req[can][0]:.2f} -- so this is a cost, not a wall; my "
      f"first reading of this as a hard ceiling was an artefact of too short an amplitude grid.)")
check(np.isfinite(req[can][2]) and req[can][2] > 0.06,
      f"Q3b on the crossing criterion, which is not capped, 80% power needs D = {req[can][2]:.3f} mag "
      f"({req[can][2]/0.06:.1f}x the real 0.06 step), i.e. N ~ {req[can][3]:.0f} sized hosts against the {N} in "
      f"hand -- a factor {req[can][3]/N:.1f}. That is the honest data-volume statement for this front")

# verify the sqrt(N) extrapolation rather than trusting it: sub-sample to N/2 and check power drops as expected
half = N // 2
nf_h = 0
for _ in range(NSIM):
    sub = rng.integers(0, N, half)
    noise = resid_pool[rng.integers(0, N, half)]
    lgh, lmh = lg_c[sub], LM[sub]
    hih = lgh > 0.0
    hr = -0.12 * hih.astype(float) + noise

    def pres(y, x):
        Xc = np.column_stack([np.ones_like(x), x])
        b, *_ = np.linalg.lstsq(Xc, y, rcond=None)
        return y - Xc @ b
    a = np.corrcoef(pres(hr, lmh), pres(lgh, lmh))[0, 1]
    b2 = np.corrcoef(pres(hr, lgh), pres(lmh, lgh))[0, 1]
    nf_h += (abs(a) > abs(b2)) and abs(a) > GATE
p_full_012 = power[can][0.12][0]
print(f"\n  SCALING CHECK: at D = 0.12 mag, power is {p_full_012:.3f} at N = {N} and {nf_h/NSIM:.3f} at "
      f"N = {half}")
check(nf_h / NSIM < p_full_012 + 0.05,
      f"Q3-SCALING halving the sample does not increase the power ({nf_h/NSIM:.3f} vs {p_full_012:.3f}), "
      f"confirming the power is genuinely N-limited and the D*sqrt(N) extrapolation in Q3b is the right "
      f"direction. (Quoted as a direction check, not a calibration -- the N_req figures are order-of-"
      f"magnitude.)")


banner("Q4  WHAT THE CORPUS SHOULD SAY INSTEAD OF 'NULL'")

print(f"""  *** THE LEVER IS UNDERPOWERED, NOT CLOSED. *** On the framework's own generating model, at the
  amplitude the data actually show, the shipped test recovers the signal {100*p06[0]:.0f}% of the time. Its noise
  floor (Fisher SE {fisher_se:.3f}) is comparable to the signal the hypothesis produces, and its own verdict gate
  sits at {GATE/fisher_se:.1f} SE. A non-detection from a test with {100*p06[0]:.0f}% power is not evidence of absence.

  THE REPLACEMENT WORDING, for STANDING.md and the project memory:
    was:  "decisive tests NULL, lever CLOSED -- global (N=449) AND local-SB (N=450) both show accel adds
           ~0 beyond mass; the step is an AGE/metallicity effect not an a0 acceleration effect"
    ->    "mass is PREFERRED over acceleration, but the test is UNDERPOWERED and its verdict gate is
           PENALISED BY COLLINEARITY: {100*p06[0]:.0f}% power against the framework's own model at the observed
           0.06 mag amplitude. 80% power needs D = {req[can][2]:.2f} mag ({req[can][2]/0.06:.1f}x the real step) on the crossing
           criterion, or D = {req[can][1]:.2f} mag ({req[can][1]/0.06:.1f}x) on the shipped verdict gate, whose |pGM| > |pMG|
           clause costs a further {req[can][1]/req[can][2]:.1f}x because g_bar is built from the mass. In sample terms,
           N ~ {req[can][3]:.0f} sized hosts against the {N} in hand ({req[can][3]/N:.1f}x).
           An a0-threshold component is DISFAVOURED, NOT EXCLUDED. Lever OPEN pending a larger sized-host
           sample AND a non-collinear estimator; the a0 step-LOCATION coincidence remains
           necessary-not-sufficient either way. The partial-correlation statistic is exactly a0-footing-blind."

  WHAT THIS DOES NOT DO -- and these matter, because the mirror error is as bad:
   * It does NOT revive the framework's claim. Mass still wins on the real data on both footings (Q1), the
     measured acceleration partial has the WRONG SIGN for the framework (+{pc[0]:.4f} where the model gives
     negative, Q1d), and nothing here shows acceleration is the carrier. The finding is about RESOLUTION.
   * It does NOT show the estimator is faulty. Q2-CONTROL fires {100*nf_null/NSIM:.1f}% on a pure-mass truth with mean
     partial ~ {pg_null/NSIM:+.3f}: the statistic is well-behaved and unbiased. The gate at {GATE} is a defensible
     ~2 sigma line (Q1a), not a rigged threshold.
   * It does NOT fix the deeper problem with the statistic. g_bar = G M*/R_e^2 is built FROM the mass, so the
     two regressors are collinear by construction and a partial correlation is a poor separator regardless of
     N. A joint fit with both terms free is the better estimator and is NOT run here -- that is the next
     script, and it is what would turn "disfavoured" into a quantitative upper limit on the a0 component.
   * The N_req numbers are order-of-magnitude. They come from a D*sqrt(N) scaling whose DIRECTION is verified
     (Q3-SCALING) but whose normalisation is not calibrated against a real larger sample.
   * Both footings give the same verdict, so this does not turn on the a0 convention.""")

banner("RESULT")
n = sum(1 for x, _ in ok if x)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print(f"  Exit 0: power at the real amplitude is {100*p06[0]:.0f}%; the lever is underpowered, not closed.")
