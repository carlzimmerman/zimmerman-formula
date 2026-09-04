#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
f21_two_kernels_and_the_phantom_maximum.py -- distinct kernels and a fixed-footing binned diagnostic.
=======================================================================================================================
NOTE 2026-09-04 (see f23_kernel_transcription_audit.py): the 'field-theory kernel' named below is the CLOSURE PROGRAM's
frozen kernel (FRIED_CHICKEN_SPEC item 12; mond_compiler_2026 'FROZEN NON-NEGOTIABLES'), mu_exp(x) = 1 - e^{-x} in the
AQUAL variable.  THE_COMPLETION.md's own MOND sector is the parametric pair mu(u) = 1 - e^{-u}, u = sqrt(g_bar/a_0),
which is nu_RAR EXACTLY. The fixed-input comparison below concerns mu_exp(x), i.e. what the closure program ran,
not the parametric field-theory document. f23 adds mu_10 diagnostics and the RAR kernel's QUMOND quadrupole.
Two kernels are in play.  The EMPIRICAL one, fitted to SPARC (McGaugh, Lelli & Schombert 2016) and used in every
phenomenological script here:
        nu_RAR(y) = 1 / (1 - e^{-sqrt(y)}),     y = g_bar/a_0,     g_obs = nu_RAR(y) g_bar.
The FIELD-THEORY one, gate 12 of the completion spec, called 'exact exponential AQUAL' and used by CDE-L4C, HPI-Delta,
the regular-center theorem and the alpha_1 drag coefficient:
        mu_exp(x) = 1 - e^{-x},     x = g/a_0,     g_bar = mu_exp(x) g.
These agree as y -> 0 (both give g = sqrt(g_bar a_0)) and as y -> infinity (both give g = g_bar).  They are NOT the same
relation in between: inverting mu_exp gives a nu_mu(y) that differs from nu_RAR(y) in the transition.  This file
(1) quantifies the difference, (2) asks SPARC which one it follows, and (3) states the phantom-acceleration maximum
-- the 'dark' acceleration g_obs - g_bar never exceeds a fixed multiple of a_0 -- for the kernel the data follow.
S2 is a fixed-parameter, diagonal-bin diagnostic, not a calibrated model-rejection significance.
Galaxy resampling is independent between bins; distance, inclination, M/L and a0 are not fitted.
See closure_2026/two_kernel_orbit_shape_2026/kernel_comparison.py for a paired whole-galaxy
audit with a0 profiled in both laws. Neither script solves the non-spherical AQUAL disk equation.
"""
import sys, math
import numpy as np
from hunt_lib import *
ck = Check()
def nu_rar(y): y = np.maximum(np.asarray(y, float), 1e-12); return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def g_of_gbar_muexp(gbar, a0):
    yy = gbar/a0; g = a0*np.maximum(np.sqrt(yy), yy)
    for _ in range(80): g = g - (g*(1 - np.exp(-g/a0)) - gbar)/((1 - np.exp(-g/a0)) + (g/a0)*np.exp(-g/a0))
    return g
def nu_muexp(y, a0=1.0): return g_of_gbar_muexp(np.asarray(y, float)*a0, a0)/(np.asarray(y, float)*a0)

P("="*116); P("1.  the two kernels, side by side"); P("="*116)
yg = np.logspace(-3, 3, 601); dl = np.log10(nu_rar(yg)) - np.log10(nu_muexp(yg))
info(f"{'y = g_bar/a0':>12} {'nu_RAR':>8} {'nu_muexp':>9} {'dlog g_obs':>11}")
for yv in (0.01, 0.1, 0.3, 0.63, 1.0, 2.0, 4.0, 10.0, 100.0):
    info(f"{yv:12.2f} {float(nu_rar(yv)):8.3f} {float(nu_muexp(yv)):9.3f} {math.log10(float(nu_rar(yv)))-math.log10(float(nu_muexp(yv))):+11.3f}")
imax = int(np.argmax(np.abs(dl)))
ck("K1 the two kernels are different functions: they coincide in the deep-MOND and Newtonian limits and differ by up to ~0.08 dex in predicted g_obs in the transition, more than the radial acceleration relation's 0.06 dex scatter",
   np.abs(dl).max() > 0.05 and abs(dl[0]) < 0.01 and abs(dl[-1]) < 0.01, f"max |dlog g_obs| = {np.abs(dl).max():.3f} dex at y = {yg[imax]:.2f}; at y = 0.001: {dl[0]:+.4f}, at y = 1000: {dl[-1]:+.4f}")

P(""); P("="*116); P("2.  SPARC: which kernel do the data follow?"); P("="*116)
gals = load_sparc()
gb = np.concatenate([g["gbar"] for g in gals]); go = np.concatenate([g["gobs"] for g in gals])
ev = np.concatenate([2*g["ev"]/np.maximum(g["vobs"], 1)/math.log(10) for g in gals]); gid = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(gals)])
m = (gb > 0) & (go > 0); gb, go, ev, gid = gb[m], go[m], ev[m], gid[m]
lo = np.log10(go)
RES = {}
for foot, a0 in A0.items():
    ly = np.log10(gb/a0); edges = np.linspace(-2.6, 1.6, 22); cen = 0.5*(edges[1:]+edges[:-1])
    rows = []
    for i in range(len(cen)):
        k = (ly >= edges[i]) & (ly < edges[i+1])
        if k.sum() < 15: continue
        rng = np.random.default_rng(i); gl = np.unique(gid[k]); bb = []
        for b in range(200):
            pick = rng.choice(gl, len(gl), replace=True); idx = np.concatenate([np.where(k & (gid == g_))[0] for g_ in pick]); bb.append(np.median(lo[idx]))
        rows.append((cen[i], float(np.median(lo[k])), float(np.std(bb)), int(k.sum()), float(np.median(np.log10(gb[k])))))
    rows = np.array(rows)
    pr = np.log10(nu_rar(10**rows[:, 0])) + rows[:, 4]; pm = np.log10(nu_muexp(10**rows[:, 0])) + rows[:, 4]
    chi_r = float(np.sum(((rows[:, 1] - pr)/rows[:, 2])**2)); chi_m = float(np.sum(((rows[:, 1] - pm)/rows[:, 2])**2))
    RES[foot] = (rows, pr, pm, chi_r, chi_m)
    if foot == "canonical":
        info(f"{'log y':>7} {'N':>5} {'<log g_obs>':>12} {'s.e.':>6} {'nu_RAR':>8} {'mu_exp':>8} {'pull RAR':>9} {'pull exp':>9}")
        for r_, a, b in zip(rows, pr, pm): info(f"{r_[0]:7.2f} {int(r_[3]):5d} {r_[1]:12.3f} {r_[2]:6.3f} {a:8.3f} {b:8.3f} {(r_[1]-a)/r_[2]:+9.1f} {(r_[1]-b)/r_[2]:+9.1f}")
rows, pr, pm, chi_r, chi_m = RES["canonical"]; dof = len(rows)
info(f"chi^2 (galaxy-level errors, {dof} bins): nu_RAR = {chi_r:.1f}, mu_exp = {chi_m:.1f}; difference {chi_m-chi_r:.1f}")
tr = (rows[:, 0] > -1.0) & (rows[:, 0] < 0.8)
worst_exp = float(np.max(np.abs((rows[tr, 1] - pm[tr])/rows[tr, 2])))
ck("S1 SPARC follows nu_RAR: with galaxy-level errors the binned relation matches the fitted kernel across four decades (it was fitted to these data, so this is calibration, not confirmation)",
   chi_r/dof < 3.0, f"chi^2/dof(nu_RAR) = {chi_r/dof:.2f}")
ck("S2 fixed-footing binned diagnostic: mu_exp has a larger diagonal residual statistic; the worst standardized bin residual is not a global model-rejection significance",
   chi_m - chi_r > 25 and worst_exp > 3.0, f"chi^2(mu_exp) - chi^2(nu_RAR) = {chi_m - chi_r:.1f} on {dof} bins; worst transition-bin pull against mu_exp = {worst_exp:.1f} sigma")
ra, pa, pma, cra, cma = RES["alt"]
ck("S3 the same diagonal-bin diagnostic favors nu_RAR at both fixed a0 footings; this does not profile a0 or correlated nuisance parameters",
   cma - cra > 25, f"alt footing: chi^2(mu_exp) - chi^2(nu_RAR) = {cma - cra:.1f}")

P(""); P("="*116); P("3.  the phantom maximum, for the kernel the data follow"); P("="*116)
info("For nu_RAR the phantom acceleration is g_ph = g_bar (nu - 1) = a_0 y e^{-sqrt y}/(1 - e^{-sqrt y}).  Its maximum:")
yy = np.logspace(-2, 2, 40001); gph = yy*(nu_rar(yy) - 1.0); ipk = int(np.argmax(gph)); ypk, gpk = yy[ipk], gph[ipk]
info(f"   max g_ph = {gpk:.4f} a_0  at  g_bar = {ypk:.3f} a_0   (mu_exp instead: 1/e = 0.368 a_0 at 0.632 a_0)")
info(f"   in m/s^2: {gpk*A0['canonical']:.3e} (canonical), {gpk*A0['alt']:.3e} (alt)")
# observed phantom, binned, galaxy-level error, near the predicted peak
ph = go - gb; a0c = A0["canonical"]; ly = np.log10(gb/a0c); edges = np.linspace(-2.6, 1.6, 22); cen = np.array([0.5*(edges[i]+edges[i+1]) for i in range(21)])
med, se = [], []
for i in range(21):
    k = (ly >= edges[i]) & (ly < edges[i+1])
    if k.sum() < 15: med.append(np.nan); se.append(np.nan); continue
    rng = np.random.default_rng(100+i); gl = np.unique(gid[k]); bb = [np.median(ph[np.concatenate([np.where(k & (gid == g_))[0] for g_ in rng.choice(gl, len(gl), replace=True)])]) for b in range(200)]
    med.append(float(np.median(ph[k]))); se.append(float(np.std(bb)))
med, se = np.array(med), np.array(se); ok = np.isfinite(med) & (se > 0)
win = ok & (cen > math.log10(ypk) - 0.5) & (cen < math.log10(ypk) + 0.5)
obs_pk = float(np.nanmax(med[win])); obs_pk_se = float(se[win][int(np.nanargmax(med[win]))])
ck("P1 the largest bin median in the selected peak window is within 2.5 bootstrap errors of the nu_RAR maximum; this does NOT test a ceiling on individual galaxies or data points",
   abs(obs_pk - gpk*a0c) < 2.5*obs_pk_se, f"observed max in the window {obs_pk/1e-11:.2f} +/- {obs_pk_se/1e-11:.2f} x 1e-11 m/s^2; predicted {gpk*a0c/1e-11:.2f} at g_bar = {ypk:.2f} a_0")
ck("P2 selected high-acceleration bin medians are lower than the peak-window median; this is a descriptive turnover, not a significance test. Newtonian recovery alone does not require phantom acceleration to vanish",
   (lambda hi: hi.sum() >= 2 and float(np.nanmax(med[hi])) < 0.8*obs_pk)(ok & (cen > 0.75) & (cen <= 1.45)), f"bins at log y in (0.75, 1.45]: max {float(np.nanmax(med[ok & (cen > 0.75) & (cen <= 1.45)]))/1e-11:.2f} vs peak {obs_pk/1e-11:.2f} (x1e-11); N bins {int((ok & (cen > 0.75) & (cen <= 1.45)).sum())}")

P(""); P("="*116); P("4.  mutation controls"); P("="*116)
rng = np.random.default_rng(7); sh = rng.permutation(lo)
rows_sh = []
for i in range(len(edges)-1):
    k = (np.log10(gb/a0c) >= edges[i]) & (np.log10(gb/a0c) < edges[i+1])
    if k.sum() >= 15: rows_sh.append((0.5*(edges[i]+edges[i+1]), float(np.median(sh[k])), float(np.median(np.log10(gb[k])))))
rows_sh = np.array(rows_sh); pr_sh = np.log10(nu_rar(10**rows_sh[:, 0])) + rows_sh[:, 2]
ck("M1 mutation: shuffling g_obs across points destroys the relation for both kernels, so S1/S2 are structure in the data and not in the binning",
   float(np.sum((rows_sh[:, 1] - pr_sh)**2)) > 50*float(np.sum((rows[:, 1] - pr)**2)), "shuffled residual power far exceeds the real one")
ck("M2 limiting check: the kernels agree asymptotically (deep MOND: g = sqrt(g_bar a_0); Newtonian: g = g_bar), so S2 probes their transition as well as fixed-input normalization",
   abs(math.log10(float(nu_rar(1e-4))) - math.log10(float(nu_muexp(1e-4)))) < 0.005 and abs(math.log10(float(nu_rar(1e3))) - math.log10(float(nu_muexp(1e3)))) < 0.001, "both limits agree to <0.005 dex")

P(""); P("="*116); P("VERDICT"); P("="*116)
P("  The repository has been running two kernels and calling them one.  The empirical nu_RAR = 1/(1-e^{-sqrt y}) and")
P("  the field-theory 'exact exponential' mu_exp = 1-e^{-x} share both limits and differ by up to ~0.08 dex in the")
P(f"  transition. At fixed inputs, the diagonal-bin statistic differs by {chi_m-chi_r:.0f} on {dof} bins, with")
P(f"  a largest standardized transition residual of {worst_exp:.1f} for mu_exp. These are conditional diagnostics,")
P("  not a calibrated rejection: cross-bin covariance, a0 fitting and galaxy nuisance parameters are absent.")
P("  The two_kernel_orbit_shape_2026 audit profiles a0 and resamples complete galaxies in paired draws.")
P("  A kernel substitution is a new action target; neither relativistic closure nor a PPN coefficient transfers automatically.")
P(f"  For nu_RAR's algebraic curve, the theoretical maximum g_ph is {gpk:.3f} a0 at g_bar={ypk:.2f} a0.")
P(f"  The selected observed peak-window median is {obs_pk/1e-11:.2f} +/- {obs_pk_se/1e-11:.2f} x 1e-11 m/s^2.")
P("  This median does not certify a bound on individual catalog estimates. The a0-Lambda relation remains an input.")
sys.exit(ck.done())
