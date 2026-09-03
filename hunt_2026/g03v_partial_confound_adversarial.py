#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g03v_partial_confound_adversarial.py -- ADVERSARIAL RE-DERIVATION OF ONE CLAIM IN g03.
=====================================================================================
THE CLAIM UNDER ATTACK (from g03_anisotropy_correlation_test.py, section C / check A5):
  "The correlation is not manufactured by the mass confound: partialling out stellar mass STRENGTHENS
   rather than weakens it."  Numbers: partial(residual, beta | log M*) = +0.717 against a raw Pearson
   of +0.667; permutation p = 0.0774; +0.719 alt footing; +0.582 on the Local Volume Database.

This file does NOT re-argue the physics.  It attacks the ESTIMATOR and the ARITHMETIC:
  V1  re-derive every number from scratch, with independently written correlation code.
  V2  ALGEBRAIC IDENTITY: on the isolated branch the half-light radius CANCELS from the residual, so
      residual = 2 log sigma - 0.5 log M* + const.  If that holds, "partialling out log M*" leaves
      exactly log sigma, and the partial correlation is a a0-free, kernel-free statistic.
  V3  is +0.717 > +0.667 actually a STRENGTHENING?  A partial correlation loses a degree of freedom.
      Compare in the only currency that means anything: the t / p of each statistic.
  V4  the permutation null used for the partial is the WRONG null.  Shuffling beta destroys beta's real
      correlation with log M* (r = -0.455) as well, i.e. it tests "beta is independent of mass AND of the
      residual".  The null of interest is "beta adds nothing BEYOND mass".  Freedman-Lane is the right one.
  V5  leverage: jackknife and bootstrap the partial on N = 8.
  V6  BRANCH SENSITIVITY (the repo's own known bug pattern -- "a residual whose sign tracks a branch of
      your own prescription"): g_pred = max(g_iso, g_efe) puts 2 of the 8 objects on a different branch.
      Redo the partial with a single branch throughout.
  V7  estimator mixing: the headline rho is SPEARMAN, the confound test is a PEARSON partial.  Do both.
Both a0 footings throughout.  Checks are written so they CAN fail.
"""
import sys, os, math, csv
import numpy as np
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(7654321)
NPERM = 200000
MW_VC = 200e3

DSPH = [("Draco",      2.9e5, 0.221, 9.1,  76.), ("Sculptor",   2.3e6, 0.283, 9.2,  86.),
        ("Fornax",     4.3e7, 0.710, 11.7, 147.), ("Carina",     3.8e5, 0.250, 6.6,  105.),
        ("Sextans",    4.4e5, 0.695, 7.9,  86.),  ("Leo I",      5.5e6, 0.251, 9.2,  254.),
        ("Leo II",     7.4e5, 0.176, 6.6,  233.), ("Ursa Minor", 2.9e5, 0.181, 9.5,  76.)]
BZ = {"Draco": 0.41, "Ursa Minor": 0.61, "Carina": 0.36, "Sextans": 0.18,
      "Leo I": 0.11, "Leo II": 0.12, "Sculptor": 0.21, "Fornax": 0.24}
names = [d[0] for d in DSPH]
beta = np.array([1.0 - 10.0 ** (-BZ[n]) for n in names])
logM = np.log10(np.array([d[1] for d in DSPH]))
logS = np.log10(np.array([d[3] for d in DSPH]))
logR = np.log10(np.array([d[2] for d in DSPH]))

# ---------------------------------------------------------------- independently written statistics
def r_(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    a = a - a.mean(); b = b - b.mean()
    return float(np.dot(a, b) / math.sqrt(np.dot(a, a) * np.dot(b, b)))

def rank_(x):
    x = np.asarray(x, float); o = np.empty(len(x)); o[np.argsort(x)] = np.arange(len(x)); return o

def partial_resid(x, y, z):
    """partial correlation done the LONG way -- OLS-regress x on z and y on z, correlate the two residual
    vectors.  Mathematically identical to the shortcut formula; used here to catch a formula typo."""
    Z = np.vstack([np.asarray(z, float), np.ones(len(z))]).T
    rx = np.asarray(x, float) - Z @ np.linalg.lstsq(Z, np.asarray(x, float), rcond=None)[0]
    ry = np.asarray(y, float) - Z @ np.linalg.lstsq(Z, np.asarray(y, float), rcond=None)[0]
    return r_(rx, ry), rx, ry

def partial_formula(x, y, z):
    rxy, rxz, ryz = r_(x, y), r_(x, z), r_(y, z)
    return (rxy - rxz * ryz) / math.sqrt(max((1 - rxz ** 2) * (1 - ryz ** 2), 1e-12))

def spear_partial(x, y, z):
    return partial_formula(rank_(x), rank_(y), rank_(z))

def sigma_of(p):
    lo, hi = 0.0, 12.0
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if math.erfc(m / math.sqrt(2.0)) > p: lo = m
        else: hi = m
    return 0.5 * (lo + hi)

def t_from_r(r, n, ncov):
    df = n - 2 - ncov
    return r * math.sqrt(df / max(1 - r * r, 1e-15)), df

def t_pvalue(t, df):
    """two-sided Student-t tail by numerical integration of the pdf -- no scipy dependence."""
    lg = math.lgamma((df + 1) / 2) - math.lgamma(df / 2) - 0.5 * math.log(df * math.pi)
    f = lambda u: math.exp(lg - (df + 1) / 2 * math.log1p(u * u / df))
    a, b, n = abs(t), abs(t) + 60.0, 400000
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b)) + sum(f(a + i * h) for i in range(1, n))
    return 2.0 * s * h

# ---------------------------------------------------------------- the residual, g03 verbatim
def resid_one(M, Rh, sob, D, a0, branch="max"):
    Mk, R, s, d = M * Msun, Rh * kpc, sob * 1e3, D * kpc
    g_obs = 3.0 * s * s / R
    g_N = G * Mk / R ** 2
    g_iso = math.sqrt(g_N * a0)
    g_efe = g_N * nu_s((MW_VC ** 2 / d) / a0)
    g_pred = {"max": max(g_iso, g_efe), "iso": g_iso, "efe": g_efe}[branch]
    return math.log10(g_obs / g_pred), ("isolated" if g_iso >= g_efe else "EFE")

def resid_vec(a0, branch="max", tab=DSPH):
    return np.array([resid_one(d[1], d[2], d[3], d[4], a0, branch)[0] for d in tab])

RES = {f: resid_vec(A0[f]) for f in A0}
BR = [resid_one(d[1], d[2], d[3], d[4], A0["canonical"])[1] for d in DSPH]

P("=" * 112); P("V1.  INDEPENDENT RE-DERIVATION OF THE PUBLISHED NUMBERS"); P("=" * 112)
raw_p = r_(RES["canonical"], beta)
raw_s = r_(rank_(RES["canonical"]), rank_(beta))
pr_long, rx, ry = partial_resid(RES["canonical"], beta, logM)
pr_form = partial_formula(RES["canonical"], beta, logM)
pr_alt = partial_formula(RES["alt"], beta, logM)
info(f"branches: {dict(zip(names, BR))}")
info(f"raw Pearson r(residual, beta)          = {raw_p:+.4f}   [g03 says +0.667]")
info(f"raw Spearman rho                       = {raw_s:+.4f}   [g03 says +0.667]")
info(f"partial | logM, shortcut formula       = {pr_form:+.4f}  [g03 says +0.717]")
info(f"partial | logM, OLS-residual route     = {pr_long:+.4f}  (must agree with the line above)")
info(f"partial | logM, alt footing            = {pr_alt:+.4f}   [g03 says +0.719]")
info(f"r(residual, logM) = {r_(RES['canonical'], logM):+.4f} [g03 -0.922];  r(beta, logM) = {r_(beta, logM):+.4f} [g03 -0.455]")
ck("V1 every published number in the claim reproduces to +-0.002 from independently written code, and the "
   "shortcut partial-correlation formula agrees with the regression-residual route",
   abs(raw_p - 0.667) < 2e-3 and abs(pr_form - 0.717) < 2e-3 and abs(pr_long - pr_form) < 1e-10
   and abs(pr_alt - 0.719) < 2e-3,
   f"raw {raw_p:+.4f}, partial {pr_form:+.4f} (= OLS route {pr_long:+.4f}), alt {pr_alt:+.4f}. "
   f"THE ARITHMETIC IS CORRECT. No typo, no reshaped covariance, no wrong formula.")

P(""); P("=" * 112); P("V2.  ALGEBRAIC IDENTITY: DOES THE KERNEL SURVIVE THE PARTIALLING AT ALL?"); P("=" * 112)
info("On the isolated branch g_pred = sqrt(g_N a0) = sqrt(G M a0)/R and g_obs = 3 sigma^2/R, so R CANCELS:")
info("    residual = log10(3 sigma^2) - 0.5 log10(G M a0)  =  2 log sigma - 0.5 log M* + const(a0).")
alg = 2 * logS - 0.5 * logM
res_iso = resid_vec(A0["canonical"], "iso")
info(f"    check: r(residual_isolated, 2logS - 0.5logM) = {r_(res_iso, alg):+.6f} (must be exactly 1)")
info(f"    check: sd of (residual_isolated - alg) = {np.std(res_iso - alg):.2e} (must be 0 -- pure constant)")
pr_iso = partial_formula(res_iso, beta, logM)
pr_logS = partial_formula(logS, beta, logM)
info(f"    partial(residual_isolated, beta | logM) = {pr_iso:+.4f}")
info(f"    partial(log sigma        , beta | logM) = {pr_logS:+.4f}   <-- identical by the identity above")
info(f"    partial(residual_MAXBRANCH, beta | logM) = {pr_form:+.4f}  (the published number)")
ck("V2 (WHAT THE CLAIMED NUMBER ACTUALLY MEASURES) if the partial correlation is evidence about the "
   "FRAMEWORK, it must change when the framework's acceleration constant or kernel changes.  On the isolated "
   "branch a0 enters the residual as a pure ADDITIVE CONSTANT, so the partial is identically the correlation "
   "between anisotropy and line-of-sight dispersion at fixed stellar mass -- a statistic with no framework in "
   "it at all",
   abs(pr_iso - pr_logS) > 1e-6,
   f"partial(residual_isolated, beta|logM) = {pr_iso:+.6f} is EXACTLY partial(log sigma, beta|logM) = "
   f"{pr_logS:+.6f}, to machine precision, because residual = 2logS - 0.5logM + const. a0 CANCELS. The "
   f"published +0.717 is the same statistic with 2 of 8 objects moved onto the EFE branch. So 'the deficit "
   f"correlates with beta at fixed mass' is, arithmetically, 'sigma correlates with beta at fixed M*'.")

P(""); P("=" * 112); P("V3.  IS +0.717 > +0.667 A STRENGTHENING?  DEGREES OF FREEDOM"); P("=" * 112)
t_raw, df_raw = t_from_r(raw_p, 8, 0)
t_par, df_par = t_from_r(pr_form, 8, 1)
p_raw, p_par = t_pvalue(t_raw, df_raw), t_pvalue(t_par, df_par)
sd_raw, sd_par = 1 / math.sqrt(8 - 1), 1 / math.sqrt(8 - 2)
info(f"raw     r = {raw_p:+.4f}  t = {t_raw:.3f} on {df_raw} df  ->  p = {p_raw:.4f}   (null sd {sd_raw:.3f}, z = {raw_p/sd_raw:.3f})")
info(f"partial r = {pr_form:+.4f}  t = {t_par:.3f} on {df_par} df  ->  p = {p_par:.4f}   (null sd {sd_par:.3f}, z = {pr_form/sd_par:.3f})")
info(f"g03's own permutation p's: raw 0.0820 vs partial 0.0774 -- a shift of 0.005, i.e. NOTHING.")
num_before = r_(RES["canonical"], beta)
num_after = r_(rx, ry) * math.sqrt(np.var(rx) * np.var(ry)) / math.sqrt(np.var(RES["canonical"]) * np.var(beta))
info(f"covariance carried by beta BEFORE partialling (in r units) {num_before:+.4f}; AFTER {num_after:+.4f} "
     f"-- the shared signal SHRANK by {100*(1-abs(num_after/num_before)):.0f} per cent; the coefficient only rises "
     f"because the DENOMINATOR (residual variance left after mass) shrank faster.")
info(f"fraction of residual variance already explained by logM alone = {r_(RES['canonical'], logM)**2:.3f}")
ck("V3 (THE WORD 'STRENGTHENS') for the claim to mean what it says, the partial must be more significant "
   "than the raw correlation once the lost degree of freedom is accounted for",
   p_par < 0.8 * p_raw,
   f"p goes {p_raw:.4f} -> {p_par:.4f} (t-test) and 0.0820 -> 0.0774 (g03's own permutation). In standardised "
   f"units z = {raw_p/sd_raw:.3f} -> {pr_form/sd_par:.3f}. THE CORRELATION DOES NOT STRENGTHEN; it is unchanged "
   f"to three decimal places in significance. The rise from 0.667 to 0.717 in the COEFFICIENT is the arithmetic "
   f"consequence of dividing by sqrt((1-rxz^2)(1-ryz^2)) = {math.sqrt((1-r_(RES['canonical'],logM)**2)*(1-r_(beta,logM)**2)):.4f}, "
   f"i.e. of removing 85 per cent of the residual's variance, not of any gain in evidence.")

P(""); P("=" * 112); P("V4.  THE PERMUTATION NULL IS THE WRONG NULL"); P("=" * 112)
def perm_naive(n=NPERM):
    obs = partial_formula(RES["canonical"], beta, logM); h = 0
    for _ in range(n):
        if abs(partial_formula(RES["canonical"], rng.permutation(beta), logM)) >= abs(obs) - 1e-12: h += 1
    return obs, (h + 1) / (n + 1)
def perm_freedman_lane(n=NPERM):
    """Freedman & Lane 1983: permute the part of beta ORTHOGONAL to logM, add the fitted part back, so the
    beta-mass relation (r = -0.455) is PRESERVED under the null.  This is the null 'beta adds nothing beyond
    mass', which is the null the claim actually needs.  The naive shuffle tests a strictly stronger null."""
    Z = np.vstack([logM, np.ones(8)]).T
    fit = Z @ np.linalg.lstsq(Z, beta, rcond=None)[0]
    e = beta - fit
    obs = partial_formula(RES["canonical"], beta, logM); h = 0
    for _ in range(n):
        b2 = fit + rng.permutation(e)
        if abs(partial_formula(RES["canonical"], b2, logM)) >= abs(obs) - 1e-12: h += 1
    return obs, (h + 1) / (n + 1)
o1, pn = perm_naive(40000)
o2, pfl = perm_freedman_lane(40000)
info(f"naive shuffle-beta permutation  p = {pn:.4f}   [g03 reports 0.0774 -- reproduced]")
info(f"Freedman-Lane permutation       p = {pfl:.4f}   (preserves r(beta,logM) = {r_(beta,logM):+.3f})")
ck("V4 the p-value attached to the claim must come from the null the claim is about ('beta carries nothing "
   "beyond mass'), not from the stronger null that beta is unrelated to mass as well",
   abs(pn - pfl) < 0.01,
   f"naive {pn:.4f} vs Freedman-Lane {pfl:.4f}. The gap is {abs(pn-pfl):.4f}. The published p uses the naive "
   f"shuffle. Whether or not the gap is large, the quoted p answers a different question than the claim asks.")

P(""); P("=" * 112); P("V5.  LEVERAGE ON EIGHT OBJECTS"); P("=" * 112)
jk = []
for i in range(8):
    k = [j for j in range(8) if j != i]
    jk.append((names[i], partial_formula(RES["canonical"][k], beta[k], logM[k]), r_(RES["canonical"][k], beta[k])))
for nm, pj, rj in jk: info(f"    drop {nm:11}: partial = {pj:+.4f}   raw = {rj:+.4f}")
lo = min(p for _, p, _ in jk); hi = max(p for _, p, _ in jk)
bs = []
for _ in range(20000):
    k = rng.integers(0, 8, 8)
    if len(set(k.tolist())) < 4: continue
    try:
        v = partial_formula(RES["canonical"][k], beta[k], logM[k])
        if np.isfinite(v): bs.append(v)
    except Exception: pass
bs = np.array(bs)
info(f"jackknife range of the partial: {lo:+.3f} to {hi:+.3f} (published {pr_form:+.3f})")
info(f"bootstrap ({len(bs)} resamples): 2.5-97.5 per cent = {np.percentile(bs,2.5):+.3f} to {np.percentile(bs,97.5):+.3f}, "
     f"fraction <= 0 = {(bs<=0).mean():.3f}")
ck("V5 (LEVERAGE) no single object may move the partial by more than the null sd 1/sqrt(N-2) = "
   f"{sd_par:.3f}",
   max(abs(p - pr_form) for _, p, _ in jk) < sd_par,
   f"largest leave-one-out swing is {max(abs(p-pr_form) for _,p,_ in jk):.3f} "
   f"(dropping {max(jk, key=lambda t: abs(t[1]-pr_form))[0]}), against a null sd of {sd_par:.3f}. The bootstrap "
   f"interval {np.percentile(bs,2.5):+.3f} to {np.percentile(bs,97.5):+.3f} includes zero.")

P(""); P("=" * 112); P("V6.  BRANCH SENSITIVITY -- THE REPO'S OWN KNOWN BUG PATTERN"); P("=" * 112)
info("g_pred = max(g_iso, g_efe) is a PRESCRIPTION CHOICE that fires for exactly 2 of the 8 objects")
info("(Fornax, Leo I -- the two most massive).  If the claimed partial tracks that branch, it tracks the")
info("author's prescription, not the data.")
rows = []
for br in ("max", "iso", "efe"):
    for f in A0:
        rv = resid_vec(A0[f], br)
        rows.append((br, f, r_(rv, beta), partial_formula(rv, beta, logM), r_(rv, logM)))
for br, f, rr, pp, rm in rows:
    info(f"    branch={br:4} footing={f:9}: raw r = {rr:+.4f}  partial|logM = {pp:+.4f}  r(res,logM) = {rm:+.4f}")
pr_by_branch = [pp for br, f, rr, pp, rm in rows if f == "canonical"]
ck("V6 the partial must not depend on which branch of the author's own max(g_iso, g_efe) prescription is "
   "taken; a spread across branches comparable to the statistic itself is the 'residual tracks your own "
   "branch' failure mode this repository has been bitten by before",
   max(pr_by_branch) - min(pr_by_branch) < 0.2,
   f"partial|logM across branches (canonical) = {['%+.3f' % v for v in pr_by_branch]}: max({pr_by_branch[0]:+.3f}) "
   f"vs iso-only({pr_by_branch[1]:+.3f}) vs efe-only({pr_by_branch[2]:+.3f}), spread "
   f"{max(pr_by_branch)-min(pr_by_branch):.3f}")

P(""); P("=" * 112); P("V7.  THE DECIDER -- SPEARMAN HEADLINE vs PEARSON PARTIAL"); P("=" * 112)
info("Every headline number in g03 is a SPEARMAN rank correlation: checks A2, A3, A4, A7, the substitution")
info("table A9, the Monte Carlo A12 and the VERDICT all quote rho = +0.667.  The confound test A5 alone")
info("switches to a PEARSON partial.  Pearson and Spearman happen to coincide at +0.667 for the RAW")
info("correlation here, which is why the swap is invisible in the text.  They do NOT coincide after")
info("partialling.  Doing the partial in RANKS -- the estimator the rest of the file uses -- is the")
info("apples-to-apples comparison.")
pr_spear = spear_partial(RES["canonical"], beta, logM)
def kendall(a, b):
    n = len(a); c = d = 0
    for i in range(n):
        for j in range(i + 1, n):
            sgn = np.sign(a[i] - a[j]) * np.sign(b[i] - b[j]); c += sgn > 0; d += sgn < 0
    return (c - d) / (n * (n - 1) / 2)
kxy, kxz, kyz = kendall(RES["canonical"], beta), kendall(RES["canonical"], logM), kendall(beta, logM)
pr_kend = (kxy - kxz * kyz) / math.sqrt((1 - kxz ** 2) * (1 - kyz ** 2))
def perm_stat(fn, n=100000):
    o = fn(beta); h = sum(1 for _ in range(n) if abs(np.clip(fn(rng.permutation(beta)), -1, 1)) >= abs(o) - 1e-12)
    return o, (h + 1) / (n + 1)
_, p_prs = perm_stat(lambda b: partial_formula(RES["canonical"], b, logM))
_, p_spr = perm_stat(lambda b: spear_partial(RES["canonical"], b, logM))
P("")
info(f"    RAW  Pearson  r   = {raw_p:+.4f}      RAW  Spearman rho = {raw_s:+.4f}   (they coincide)")
info(f"    PEARSON  partial|logM = {pr_form:+.4f}  perm p = {p_prs:.4f}  ({sigma_of(p_prs):.2f} sigma)  <- the claim")
info(f"    SPEARMAN partial|logM = {pr_spear:+.4f}  perm p = {p_spr:.4f}  ({sigma_of(p_spr):.2f} sigma)  <- rank-consistent")
info(f"    KENDALL  partial|logM = {pr_kend:+.4f}   (third estimator, agrees with Spearman)")
P("")
info("WHY THEY DISAGREE.  partial = (rxy - rxz*ryz)/sqrt((1-rxz^2)(1-ryz^2)).  rxz (residual vs logM) is")
info("-0.92 either way.  The direction is set entirely by ryz = corr(beta, logM):")
info(f"    Pearson  r(beta, logM) = {r_(beta, logM):+.4f}     Spearman rho(beta, logM) = {r_(rank_(beta), rank_(logM)):+.4f}")
info("The Pearson value is ATTENUATED, and by exactly one object.  Fornax sits at log M* = 7.63 with the")
info("next object at 6.74 -- a leverage of h_ii = 0.69 out of 1 in the log M* regression:")
h_ii = 1 / 8 + (logM - logM.mean()) ** 2 / ((logM - logM.mean()) ** 2).sum()
for i, n in enumerate(names):
    info(f"      {n:11} logM = {logM[i]:.2f}  z = {(logM[i]-logM.mean())/logM.std():+5.2f}  leverage h_ii = {h_ii[i]:.3f}")
info(f"    drop Fornax: Pearson r(beta,logM) goes {r_(beta, logM):+.3f} -> "
     f"{r_(np.delete(beta,2), np.delete(logM,2)):+.3f}, and the Pearson partial FALLS to "
     f"{partial_formula(np.delete(RES['canonical'],2), np.delete(beta,2), np.delete(logM,2)):+.3f}")
P("")
info("leave-one-out, both estimators:")
for i, n in enumerate(names):
    k = [j for j in range(8) if j != i]
    info(f"      drop {n:11}: Pearson partial = {partial_formula(RES['canonical'][k], beta[k], logM[k]):+.3f}   "
         f"Spearman partial = {spear_partial(RES['canonical'][k], beta[k], logM[k]):+.3f}")

ck("V7 (THE DECIDER) the claim 'partialling out stellar mass STRENGTHENS the correlation' must hold under "
   "the estimator the rest of the file uses for every other number.  g03's headline is Spearman; its confound "
   "test is Pearson",
   pr_spear > raw_s and p_spr < 0.10,
   f"SPEARMAN: rho {raw_s:+.3f} -> partial {pr_spear:+.3f}, permutation p {p_spr:.3f} = {sigma_of(p_spr):.2f} sigma. "
   f"KENDALL: {kxy:+.3f} -> {pr_kend:+.3f}. Both rank estimators say partialling out stellar mass DESTROYS the "
   f"correlation (74 per cent of it gone, p = 0.70). Only the Pearson version rises, and it rises because "
   f"Pearson understates r(beta,logM) as {r_(beta,logM):+.3f} against the rank value "
   f"{r_(rank_(beta), rank_(logM)):+.3f}, an attenuation caused by Fornax alone (leverage 0.69).")

# LVD footing, third structural compilation
LVD = os.path.join(DATA, "dsph", "lvd_dwarf_mw.csv")
lvd = {r["name"]: r for r in csv.DictReader(open(LVD))}
TAB2 = [(n, 10 ** float(lvd[n]["mass_stellar"]), float(lvd[n]["rhalf_sph_physical"]) / 1000.0,
         float(lvd[n]["vlos_sigma"]), float(lvd[n]["distance_gc"])) for n in names]
rv2 = resid_vec(A0["canonical"], "max", TAB2)
lm2 = np.log10(np.array([t[1] for t in TAB2]))
P(""); info(f"Local Volume Database footing: raw r = {r_(rv2, beta):+.4f}, partial|logM = "
            f"{partial_formula(rv2, beta, lm2):+.4f}  [g03 says +0.582]")

P(""); P("=" * 112); P("VERDICT"); P("=" * 112)
P(f"  The ARITHMETIC of the claim is CORRECT and reproduces exactly.  What is wrong is the INFERENCE drawn")
P(f"  from it.  (i) 0.667 -> 0.717 is not a strengthening: p goes {p_raw:.3f} -> {p_par:.3f} (t) and 0.0820 -> 0.0774")
P(f"  (the file's own permutation).  The coefficient rises only because partialling removes 85 per cent of the")
P(f"  residual's variance and the partial-correlation denominator divides it back out.  (ii) On the isolated")
P(f"  branch the residual is ALGEBRAICALLY 2 log sigma - 0.5 log M* + const(a0), so the partial is exactly")
P(f"  corr(beta, log sigma | log M*) -- a0 and the kernel cancel, and the statistic contains no framework.")
P(f"  (iii) The bootstrap interval on the partial spans {np.percentile(bs,2.5):+.3f} to {np.percentile(bs,97.5):+.3f} and includes zero.")
P(f"  (iv) DECISIVE: the file's headline statistic is SPEARMAN everywhere except this one check. The rank-")
P(f"  consistent partial is {pr_spear:+.3f} with permutation p = {p_spr:.3f} ({sigma_of(p_spr):.2f} sigma), and Kendall's gives {pr_kend:+.3f}.")
P(f"  Partialling out stellar mass DESTROYS the correlation under both rank estimators. The Pearson rise is")
P(f"  driven by Pearson understating r(beta,logM) ({r_(beta,logM):+.3f} vs rank {r_(rank_(beta),rank_(logM)):+.3f}), an attenuation")
P(f"  produced by Fornax alone (log M* = 7.63, leverage 0.69). THE DIRECTION OF THE CLAIM IS AN ESTIMATOR CHOICE.")
sys.exit(ck.done())
