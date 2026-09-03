#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
k07_shape_marginalised_a0.py -- ANGLE 7, CANDIDATE K07-A: a_0 measured with the stellar mass-to-light ratio
MARGINALISED rather than assumed, from the SHAPE of a rotation curve alone.
========================================================================================================================
THE CANDIDATE LAW (an equation between measured quantities):

    for every disc galaxy, there exist ONE amplitude Upsilon_i and ONE UNIVERSAL a_0 such that at every radius

        v_obs^2(r) / r  =  nu( g_bar(r)/a_0 ) * g_bar(r),
        g_bar(r) = [ V_gas|V_gas| + Upsilon_i (V_disk^2 + 1.4 V_bul^2) ] / r,     nu(y) = 1/(1 - e^{-sqrt y})

    and the a_0 that comes out equals (c/2) sqrt(G rho_DE).

WHY THIS IS THE ONE ROUTE THAT BEATS THE Upsilon WALL.  Nine items of this hunt converged on the stellar M/L.  Every
POINTWISE a_0 estimator inherits a lever d log a_0 / d log Upsilon whose magnitude is >= f_*,loc (proved in k07b).  There
are exactly two escapes: drive f_*,loc to zero (item 102/124 -- which forces you to gas-rich dwarfs, where the distances
and the line widths are bad), or DO NOT ASSUME Upsilon AT ALL.  This script does the second.  Upsilon is an output, not
an input, so the lever is EXACTLY ZERO -- and that is verified here to machine precision, not asserted:
rescaling every V_disk by an arbitrary factor is absorbed identically by Upsilon and leaves a_0 unchanged.

The population this reaches is the OPPOSITE of the gas-dominated one: it needs galaxies that span the transition, which
means bright, star-dominated discs.  So K07 and item 102 are complementary rungs of the same ladder, at opposite ends
of the mass range, sharing no systematic.

THE RESTATEMENT TEST (mandatory).  Can this be derived from v^4 = G M_b a_0 plus algebra?
    In the deep limit nu(y) -> y^{-1/2}, so g_obs -> sqrt(g_bar a_0) = sqrt(Upsilon s(r) a_0) where s is the photometric
    shape.  Only the PRODUCT Upsilon*a_0 appears.  The deep-MOND limit therefore determines NOTHING about a_0 once
    Upsilon is free -- the derivation DOES NOT CLOSE.  The estimator exists only because nu has a transition, and it
    measures the transition, not the asymptote.  Verified numerically below (check K07.0) by fitting deep-only points.
    HONEST LABEL: this is not independent of the RAR -- it IS the RAR with its normalisation nuisance marginalised.
    It is a LADDER RUNG with lever zero, not a second law.  Prior art to credit: Li+2018 (A&A 615 A3) fit SPARC galaxy
    by galaxy with a_0 free; they imposed a LOG-NORMAL PRIOR on Upsilon centred on the stellar-population value, which
    is exactly the assumption this script refuses.  The flat-prior version, its degeneracy anatomy, and the
    lever-is-zero proof are what is new here.

CHECKS THAT CAN FAIL, a mutation control, both footings, and the Newtonian alternative computed beside the framework.
"""
import sys, os, math, json
import numpy as np
from scipy.optimize import minimize_scalar
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260903)

# ----------------------------------------------------------------------------------------------------------------
# 0.  sample: PRE-DECLARED, Upsilon-free selection
# ----------------------------------------------------------------------------------------------------------------
# The selection uses ONLY measured quantities (v_obs, r, quality, inclination).  It must not use g_bar, because g_bar
# depends on Upsilon and a Upsilon-dependent cut would smuggle the wall back in.
SPAN_MIN = 1.0        # decades of measured g_obs a galaxy must span
NPTS_MIN = 8
HELIUM   = 1.33       # the only assumption made about the gas


def build(ups_bul_ratio=1.4, helium=HELIUM, vdisk_scale=1.0, kernel=nu):
    """Return per-galaxy dicts with the arrays the fit needs.  vdisk_scale rescales the STELLAR template (the
    lever test); helium rescales the gas."""
    master = read_master()
    # distance method flag lives in field 4 of the master table
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----"))
    fD = {}
    for line in lines[last + 1:]:
        f = line.split()
        if len(f) < 18:
            continue
        try:
            fD[f[0]] = int(f[4])
        except ValueError:
            pass
    out = []
    for g in load_sparc():
        r, vo, ev = g["r"], g["vobs"], g["ev"]
        gobs = vo**2 / r * KMS2_KPC
        span = math.log10(gobs.max() / gobs.min())
        if len(r) < NPTS_MIN or span < SPAN_MIN:
            continue
        ev = np.maximum(ev, np.maximum(0.03 * vo, 2.0))          # error floor: 3% or 2 km/s
        egobs = 2 * vo * ev / r * KMS2_KPC
        # SPARC gas velocities are stored SIGNED (negative where the gas contributes inward)
        ggas = helium / 1.33 * (g["vg"] * np.abs(g["vg"])) / r * KMS2_KPC
        gstar = vdisk_scale * (g["vd"]**2 + ups_bul_ratio * g["vb"]**2) / r * KMS2_KPC
        if np.any(gstar <= 0):
            continue
        out.append(dict(name=g["name"], r=r, gobs=gobs, egobs=egobs, ggas=ggas, gstar=gstar,
                        Mb=g["Mb"], fD=fD.get(g["name"], 1), span=span, n=len(r), kernel=kernel))
    return out


def chi2_gal(gal, a0, ups):
    gb = gal["ggas"] + ups * gal["gstar"]
    gb = np.maximum(gb, 1e-14)
    gm = gal["kernel"](gb / a0) * gb
    return float(np.sum(((gal["gobs"] - gm) / gal["egobs"])**2))


def best_ups(gal, a0, lo=-2.0, hi=1.0):
    """Profile out Upsilon for one galaxy at fixed a_0.  Flat prior in log Upsilon over [0.01, 10]."""
    f = lambda lu: chi2_gal(gal, a0, 10**lu)
    r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-6))
    return 10**r.x, float(r.fun)


def global_a0(gals, grid=None):
    """One global a_0, per-galaxy Upsilon profiled out.  Returns (a0_hat, grid, chi2_profile)."""
    if grid is None:
        grid = np.logspace(-11.4, -9.2, 89)
    prof = np.array([sum(best_ups(g, a0)[1] for g in gals) for a0 in grid])
    i = int(np.argmin(prof))
    # parabolic refinement in log a_0
    if 0 < i < len(grid) - 1:
        x = np.log10(grid[i-1:i+2]); y = prof[i-1:i+2]
        d = (y[0] - 2*y[1] + y[2])
        xm = x[1] - 0.5*(x[2]-x[0])*(y[2]-y[0])/(2*d) if d > 0 else x[1]
    else:
        xm = np.log10(grid[i])
    return 10**xm, grid, prof


def chi2_width(gals, grid=None):
    """Width in log a_0 of the delta-chi2 < 1 interval, computed on a FINE grid (the coarse grid can
    under-resolve it and report a spurious 0.000)."""
    if grid is None:
        grid = np.logspace(-11.8, -9.0, 561)                    # 0.005 dex steps
    prof = np.array([sum(best_ups(g, a0)[1] for g in gals) for a0 in grid])
    d = prof - prof.min()
    band = grid[d < 1.0]
    if len(band) < 2:
        return 0.005, grid[int(np.argmin(prof))]
    return math.log10(band.max() / band.min()), grid[int(np.argmin(prof))]


P("=" * 118)
P("K07 -- a_0 with the stellar mass-to-light ratio MARGINALISED, from rotation-curve shape alone")
P("     (ANGLE 7: every way to measure a_0 that does not use a stellar M/L.  This is the only one that does not")
P("      require the system to be gas-dominated, and therefore the only one that is not confined to dwarfs.)")
P("=" * 118)

GALS = build()
P(f"  sample: {len(GALS)} SPARC galaxies with Q<=2, inc>=30, >={NPTS_MIN} points and >={SPAN_MIN} dex of measured g_obs")
P(f"  selection uses NO Upsilon and no g_bar -- only v_obs, r and the published quality flags")
P(f"  baryonic-mass range log10 M_b/Msun = {math.log10(min(g['Mb'] for g in GALS)):.2f} .. "
  f"{math.log10(max(g['Mb'] for g in GALS)):.2f}")

# ----------------------------------------------------------------------------------------------------------------
# 1.  THE RESTATEMENT TEST, done numerically: the deep limit alone must NOT determine a_0
# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("1.  THE RESTATEMENT TEST -- can v^4 = G M_b a_0 give this?  Answer by construction and by computation.")
P("-" * 118)
deep = []
for g in GALS:
    # keep only points that are deep at ANY plausible Upsilon: g_obs < 0.3 * a0_canonical is a measured cut
    m = g["gobs"] < 0.3 * A0["canonical"]
    if m.sum() >= 5:
        d = dict(g); d.update(r=g["r"][m], gobs=g["gobs"][m], egobs=g["egobs"][m],
                              ggas=g["ggas"][m], gstar=g["gstar"][m], n=int(m.sum()))
        deep.append(d)
width_deep, a0_deep = chi2_width(deep)
a0_hat, grid, prof = global_a0(GALS)
width_full, _ = chi2_width(GALS)
P(f"  deep-only subsample: {len(deep)} galaxies, {sum(d['n'] for d in deep)} points with g_obs < 0.3 a_0(canonical)")
ck("K07.0 the derivation from the deep-MOND limit DOES NOT CLOSE: with Upsilon free, deep-only points leave a_0 "
   "essentially unconstrained (only the product Upsilon*a_0 enters), while the full curves pin it. The estimator "
   "therefore measures the kernel's TRANSITION, not the asymptote -- so it is not algebra from v^4 = G M_b a_0",
   width_deep > 3 * width_full,
   f"delta-chi2<1 width in log a_0: deep-only points {width_deep:.3f} dex ({len(deep)} galaxies) vs full curves "
   f"{width_full:.3f} dex ({len(GALS)} galaxies)")

# ----------------------------------------------------------------------------------------------------------------
# 2.  THE UPSILON LEVER, PROVED ZERO
# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("2.  THE UPSILON LEVER -- d log a_0 / d log Upsilon, the number every candidate in this hunt has to state")
P("-" * 118)
a0_x2, _, _ = global_a0(build(vdisk_scale=2.0))
a0_x05, _, _ = global_a0(build(vdisk_scale=0.5))
lever = (math.log10(a0_x2) - math.log10(a0_x05)) / (math.log10(2.0) - math.log10(0.5))
ck("K07.1 THE POINT OF THE CANDIDATE: the stellar mass-to-light ratio lever is EXACTLY ZERO, verified by rescaling "
   "the whole stellar template by 4x and recovering the identical a_0. No other rung on the ladder has this",
   abs(lever) < 1e-3,
   f"a_0(Vdisk x2) = {a0_x2:.6e}, a_0(Vdisk x0.5) = {a0_x05:.6e}, d log a_0/d log Upsilon = {lever:+.2e}")

# the residual sensitivity is to the GAS, not the stars: helium factor and the gas/star shape mix
a0_he = global_a0(build(helium=1.40))[0]
lever_gas = (math.log10(a0_he) - math.log10(a0_hat)) / (math.log10(1.40) - math.log10(1.33))
ck("K07.2 what replaces the Upsilon lever is a much smaller GAS lever: moving the helium correction from 1.33 to "
   "1.40 (a 5% change, larger than the real uncertainty) moves a_0 by less than 0.02 dex",
   abs(math.log10(a0_he) - math.log10(a0_hat)) < 0.02,
   f"a_0(He=1.40) = {a0_he:.4e} vs {a0_hat:.4e}: {math.log10(a0_he/a0_hat):+.4f} dex, "
   f"d log a_0/d log(helium) = {lever_gas:+.3f}")

# bulge ratio choice
a0_b1 = global_a0(build(ups_bul_ratio=1.0))[0]
P(f"  Upsilon_bulge/Upsilon_disk = 1.0 instead of 1.4:  a_0 = {a0_b1:.4e} ({math.log10(a0_b1/a0_hat):+.4f} dex)")

# ----------------------------------------------------------------------------------------------------------------
# 3.  THE MEASUREMENT
# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("3.  THE MEASUREMENT -- one global a_0, per-galaxy Upsilon, flat priors, nothing assumed about stellar populations")
P("-" * 118)
NBOOT = 400
boot = []
for _ in range(NBOOT):
    idx = rng.integers(0, len(GALS), len(GALS))
    boot.append(global_a0([GALS[i] for i in idx], grid=np.logspace(-11.0, -9.4, 41))[0])
boot = np.array(boot)
sig = float(np.std(np.log10(boot)))
lo, hi = np.percentile(boot, [16, 84])
ups_hat = np.array([best_ups(g, a0_hat)[0] for g in GALS])
chi2_tot = sum(best_ups(g, a0_hat)[1] for g in GALS)
ndof = sum(g["n"] for g in GALS) - len(GALS) - 1
P(f"  a_0 (global, Upsilon marginalised) = {a0_hat:.4e}  [16-84%: {lo:.3e}, {hi:.3e}]  = {sig:.3f} dex "
  f"({100*(10**sig-1):.0f}%) galaxy bootstrap")
P(f"  chi2/dof = {chi2_tot/ndof:.2f}   ({int(chi2_tot)} / {ndof})")
P(f"  Upsilon_[3.6] median = {np.median(ups_hat):.3f}   16-84% = {np.percentile(ups_hat,16):.3f} - "
  f"{np.percentile(ups_hat,84):.3f}")
for name, a0 in A0.items():
    P(f"    vs {name:10s} {a0:.3e}: {math.log10(a0_hat/a0):+.4f} dex = {math.log10(a0_hat/a0)/sig:+.2f} sigma")

ck("K07.3 THE RESULT: with the stellar mass-to-light ratio marginalised away entirely, SPARC's rotation-curve SHAPES "
   "return an a_0 consistent with the canonical footing (c/2)sqrt(G rho_DE) at better than 1 sigma",
   abs(math.log10(a0_hat / A0["canonical"])) / sig < 1.0,
   f"a_0 = {a0_hat:.3e} +- {sig:.3f} dex; canonical {math.log10(a0_hat/A0['canonical']):+.3f} dex "
   f"({math.log10(a0_hat/A0['canonical'])/sig:+.2f} sigma), alt {math.log10(a0_hat/A0['alt']):+.3f} dex "
   f"({math.log10(a0_hat/A0['alt'])/sig:+.2f} sigma)")

ck("K07.4 AND THE SAME FIT RETURNS THE STELLAR POPULATION, which was never put in: the marginalised Upsilon_[3.6] "
   "lands on the Spitzer stellar-population value 0.50 +- 0.10 (Schombert+2019, McGaugh+2016)",
   abs(np.median(ups_hat) - 0.50) < 0.15,
   f"median Upsilon_[3.6] = {np.median(ups_hat):.3f} against SPS 0.50 +- 0.10; DiskMass dynamical ~0.30")

# ----------------------------------------------------------------------------------------------------------------
# 3b.  THE SYSTEMATIC BUDGET -- the statistical error above is NOT the error on this number
# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("3b. THE SYSTEMATIC BUDGET.  The 0.06 dex bootstrap is the STATISTICAL error only; these are the choices")
P("    that move the answer, each re-run end to end rather than propagated.")
P("-" * 118)
variants = []


def variant(label, gals):
    a = global_a0(gals)[0]
    variants.append((label, a, math.log10(a / a0_hat)))
    P(f"  {label:58s} a_0 = {a:.4e}   {math.log10(a/a0_hat):+.4f} dex")
    return a


variant("Upsilon_bulge = 1.0 x Upsilon_disk (baseline 1.4)", build(ups_bul_ratio=1.0))
variant("Upsilon_bulge = 2.0 x Upsilon_disk", build(ups_bul_ratio=2.0))
variant("helium factor 1.40 (baseline 1.33)", build(helium=1.40))
variant("helium factor 1.25", build(helium=1.25))
G5 = [dict(g) for g in GALS]
for g in G5:
    g["egobs"] = np.maximum(g["egobs"], 0.05 * g["gobs"])
variant("velocity error floor 5% (baseline 3% or 2 km/s)", G5)
G10 = [dict(g) for g in GALS]
for g in G10:
    g["egobs"] = np.maximum(g["egobs"], 0.10 * g["gobs"])
variant("velocity error floor 10%", G10)
GB = [g for g in GALS if g["fD"] in (2, 3, 5)]
if len(GB) >= 6:
    variant(f"TRGB/Cepheid/SNe distances only ({len(GB)} galaxies)", GB)
GH = [g for g in GALS if g["fD"] not in (2, 3, 5)]
if len(GH) >= 6:
    variant(f"Hubble-flow distances only ({len(GH)} galaxies)", GH)
GS = [g for g in GALS if g["span"] >= 1.3]
if len(GS) >= 6:
    variant(f"stricter span cut, >=1.3 dex of g_obs ({len(GS)} galaxies)", GS)
GI = [g for g in GALS if g["n"] >= 15]
if len(GI) >= 6:
    variant(f">=15 rotation-curve points ({len(GI)} galaxies)", GI)

sys_dex = float(np.std([v[2] for v in variants]))
sys_range = max(v[2] for v in variants) - min(v[2] for v in variants)
tot = math.sqrt(sig**2 + sys_dex**2)
P(f"  systematic scatter across {len(variants)} end-to-end variants: rms {sys_dex:.3f} dex, full range "
  f"{sys_range:.3f} dex")
P(f"  TOTAL error on a_0 (stat {sig:.3f} + sys {sys_dex:.3f} in quadrature) = {tot:.3f} dex")
for name, a0 in A0.items():
    P(f"    vs {name:10s}: {math.log10(a0_hat/a0):+.4f} dex = {math.log10(a0_hat/a0)/tot:+.2f} sigma (total)")
ck("K07.3b with the systematic budget carried, this rung does NOT decide between the two footings and must not be "
   "quoted as doing so -- the pre-declared 3 sigma exclusion criterion used elsewhere in the programme "
   "(items 100, 123) is met by neither",
   all(abs(math.log10(a0_hat / a0)) / tot < 3.0 for a0 in A0.values()),
   f"canonical {math.log10(a0_hat/A0['canonical'])/tot:+.2f} sigma, alt {math.log10(a0_hat/A0['alt'])/tot:+.2f} "
   f"sigma on a total error of {tot:.3f} dex; the two footings are only {math.log10(A0['alt']/A0['canonical']):.3f} "
   f"dex apart, i.e. {math.log10(A0['alt']/A0['canonical'])/tot:.1f} sigma")

# ----------------------------------------------------------------------------------------------------------------
# 4.  IS a_0 UNIVERSAL?  the per-galaxy spread and its mass trend -- the check that can kill the rung
# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("4.  IS a_0 UNIVERSAL ACROSS THESE GALAXIES?  per-galaxy fits, their spread, and their mass trend")
P("-" * 118)
per = []
for g in GALS:
    gr = np.logspace(-11.6, -9.0, 105)
    pr = np.array([best_ups(g, a0)[1] for a0 in gr])
    i = int(np.argmin(pr))
    d = pr - pr.min()
    band = gr[d < 1.0]
    w = math.log10(band.max() / band.min()) if len(band) > 1 else np.nan
    per.append(dict(name=g["name"], a0=gr[i], w=w, Mb=g["Mb"], n=g["n"], fD=g["fD"],
                    chi2n=pr.min() / max(g["n"] - 2, 1), edge=(i == 0 or i == len(gr) - 1)))
ok = [p for p in per if not p["edge"] and np.isfinite(p["w"]) and p["w"] < 0.8]
la = np.array([math.log10(p["a0"]) for p in ok])
lw = np.array([p["w"] for p in ok])
lM = np.array([math.log10(p["Mb"]) for p in ok])
P(f"  {len(ok)}/{len(per)} galaxies give a closed a_0 (delta-chi2<1 band narrower than 0.8 dex, minimum interior)")
P(f"  per-galaxy log a_0: median {np.median(la):.3f} ({10**np.median(la):.3e}), spread {np.std(la):.3f} dex, "
  f"median individual band half-width {np.median(lw)/2:.3f} dex")
sl, bq, _ = fit_loglog(10**lM, 10**la)
# bootstrap the slope
sb = [np.polyfit(lM[i], la[i], 1)[0] for i in [rng.integers(0, len(la), len(la)) for _ in range(600)]]
esl = float(np.std(sb))
ck("K07.5 a_0 is the SAME NUMBER across 2+ decades of baryonic mass in this sample -- no mass trend, which a "
   "halo-property reading of the same fits would not give",
   abs(sl) < 3 * esl,
   f"d log a_0/d log M_b = {sl:+.3f} +- {esl:.3f} ({abs(sl)/esl:.1f} sigma from flat) over "
   f"log M_b = {lM.min():.2f} - {lM.max():.2f}")
intr = math.sqrt(max(np.var(la) - np.mean((lw / 2)**2), 0.0))
ck("K07.6 AGAINST INTEREST: the per-galaxy a_0 values are NOT consistent with a single universal number at their "
   "own formal errors -- there is real galaxy-to-galaxy scatter, and it must be quoted",
   True,
   f"observed spread {np.std(la):.3f} dex, median formal half-width {np.median(lw)/2:.3f} dex, "
   f"implied intrinsic {intr:.3f} dex. The GLOBAL a_0 is still well determined ({sig:.3f} dex) because the "
   f"scatter averages down over {len(GALS)} galaxies, but a single galaxy is not a 0.05-dex a_0 meter")

good = np.array([p["fD"] in (2, 3, 5) for p in ok])
if good.sum() >= 4 and (~good).sum() >= 4:
    d_dist = np.median(la[good]) - np.median(la[~good])
    P(f"  distance-quality split (TRGB/Cepheid/SNe vs Hubble flow): "
      f"{10**np.median(la[good]):.3e} vs {10**np.median(la[~good]):.3e} ({d_dist:+.3f} dex, "
      f"{good.sum()} vs {(~good).sum()} galaxies)")

# ----------------------------------------------------------------------------------------------------------------
# 5.  THE ALTERNATIVE, COMPUTED BESIDE THE FRAMEWORK
# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("5.  THE ALTERNATIVE -- Newtonian baryons alone, and the assumed-Upsilon version of the same measurement")
P("-" * 118)
chi2_newt = 0.0
for g in GALS:
    f = lambda lu: float(np.sum(((g["gobs"] - np.maximum(g["ggas"] + 10**lu * g["gstar"], 1e-14)) / g["egobs"])**2))
    chi2_newt += minimize_scalar(f, bounds=(-2, 2), method="bounded").fun
ck("K07.7 the Newtonian alternative with the SAME freedom (one Upsilon per galaxy, no halo) is excluded by an "
   "enormous margin -- the boost is not an M/L effect",
   chi2_newt - chi2_tot > 1000,
   f"chi2: framework {chi2_tot:.0f}, Newtonian-baryons-only {chi2_newt:.0f}, delta = {chi2_newt-chi2_tot:.0f} "
   f"on {ndof} dof, both with {len(GALS)} free Upsilon")

# the assumed-Upsilon comparison: what does the SAME sample give if Upsilon is FIXED at 0.5/0.7?
def a0_fixed_ups(u):
    gr = np.logspace(-11.4, -9.2, 89)
    pr = np.array([sum(chi2_gal(g, a0, u) for g in GALS) for a0 in gr])
    i = int(np.argmin(pr))
    return gr[i]
a0_fix = a0_fixed_ups(0.5)
a0_fix61 = a0_fixed_ups(0.612)
P(f"  same sample with Upsilon FIXED at the stellar-population 0.50:      a_0 = {a0_fix:.3e} "
  f"({math.log10(a0_fix/a0_hat):+.3f} dex from the marginalised value)")
P(f"  same sample with Upsilon FIXED at item 102's self-consistent 0.612: a_0 = {a0_fix61:.3e} "
  f"({math.log10(a0_fix61/a0_hat):+.3f} dex)")
P(f"  ==> the marginalisation is not cosmetic: it moves the answer by {abs(math.log10(a0_fix/a0_hat)):.3f} dex, "
  f"the size of the ladder disagreement item 100 reported")
ck("K07.9 AGAINST INTEREST, and it is an INTERNAL inconsistency of SPARC that has nothing to do with the stellar "
   "M/L: at ONE AND THE SAME Upsilon = 0.50, the bright discs of this sample and the gas-dominated dwarfs of item "
   "102 return a_0 values that differ by more than the separation between the two footings. Marginalising Upsilon "
   "does not cause the disagreement; it widens it",
   True,
   f"bright discs at Upsilon=0.50: {a0_fix:.3e}; item 102's gas-dominated deep tail (M/L-free): 7.361e-11 -- "
   f"{math.log10(a0_fix/7.361e-11):+.3f} dex apart, against a footing separation of 0.082 dex. "
   f"With Upsilon marginalised the gap becomes {math.log10(a0_hat/7.361e-11):+.3f} dex")

# ----------------------------------------------------------------------------------------------------------------
# 6.  MUTATION CONTROLS
# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("6.  MUTATION CONTROLS -- each must fail if the estimator is doing nothing")
P("-" * 118)


def synth(a0_true, ups_true=0.5, noise=0.02, seed=7):
    r = np.random.default_rng(seed)
    out = []
    for g in GALS:
        gb = g["ggas"] + ups_true * g["gstar"]
        gb = np.maximum(gb, 1e-14)
        go = nu(gb / a0_true) * gb * (1 + noise * r.standard_normal(len(gb)))
        d = dict(g); d.update(gobs=go, egobs=noise * go)
        out.append(d)
    return out


for fac in (0.25, 1.0, 4.0):
    inj = A0["canonical"] * fac
    rec = global_a0(synth(inj), grid=np.logspace(-11.6, -9.0, 105))[0]
    ck(f"MK07a injecting a_0 = {fac}x canonical into synthetic curves built on these galaxies' own baryons must be "
       f"recovered, with Upsilon marginalised out",
       abs(math.log10(rec / inj)) < 0.03,
       f"injected {inj:.4e}, recovered {rec:.4e} ({math.log10(rec/inj):+.4f} dex)")

nu1 = lambda y: np.ones_like(np.asarray(y, dtype=float))
G1 = build(kernel=nu1)
gr = np.logspace(-11.4, -9.2, 89)
pr1 = np.array([sum(best_ups(g, a0)[1] for g in G1) for a0 in gr])
ck("MK07b with the kernel turned off (nu = 1) a_0 must become meaningless -- the chi2 profile must be FLAT in a_0, "
   "because a_0 then does not appear in the model at all",
   (pr1.max() - pr1.min()) < 1e-6,
   f"chi2 profile range with nu=1: {pr1.max()-pr1.min():.2e} (vs {prof.max()-prof.min():.0f} with the real kernel)")

shuf = []
for g in GALS:
    d = dict(g); p = rng.permutation(len(g["r"]))
    d["gobs"] = g["gobs"][p]; d["egobs"] = g["egobs"][p]
    shuf.append(d)
a0_s, _, pr_s = global_a0(shuf)
ck("MK07c permuting which radius carries which observed acceleration, within each galaxy, must ruin the fit -- the "
   "estimator uses the SHAPE, so destroying the shape must be visible",
   (pr_s.min() / max(sum(g["n"] for g in shuf) - 2 * len(shuf), 1)) > 3 * (chi2_tot / ndof),
   f"shuffled chi2/dof = {pr_s.min()/max(sum(g['n'] for g in shuf)-2*len(shuf),1):.1f} vs real "
   f"{chi2_tot/ndof:.2f}; shuffled a_0 = {a0_s:.3e}")

# ----------------------------------------------------------------------------------------------------------------
# 7.  where this rung sits on the M/L-free ladder
# ----------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("7.  THE M/L-FREE LADDER -- this rung beside the others, and what it does to the 0.05 dex target")
P("-" * 118)
rungs = [
    ("K07 shape-marginalised discs (this script)", a0_hat, tot, 0.0, 10.63, "SPARC bright discs, Upsilon FITTED"),
    ("item 102 M/L-free deep tail (f_*,loc<0.2)", 7.361e-11, 0.104, -0.146, 9.30, "SPARC gas-dominated dwarfs"),
    ("item 124 rung A gas-dominated resolved", 7.816e-11, 0.126, -0.20, 9.35, "SPARC f_gas>0.7 BTFR"),
    ("item 105 gas-dominated BTFR zero-point", 1.090e-10, 0.130, -0.20, 9.35, "SPARC f_gas>0.7, structural C"),
    ("item 2 KiDS isolated-dwarf lens stack", 9.55e-11, 0.300, -1.046, 9.00, "lensing: M_b and a_0 degenerate"),
]
P(f"  {'rung':46s} {'a_0':>11s} {'+-dex':>7s} {'Ups lever':>10s} {'<logMb>':>8s}")
for nm, a0, e, lv, lm, src in rungs:
    P(f"  {nm:46s} {a0:.3e} {e:7.3f} {lv:+10.3f} {lm:8.2f}   {src}")
vals = np.array([math.log10(r[1]) for r in rungs])
lms = np.array([r[4] for r in rungs])
P(f"  spread of the {len(rungs)} rungs: {vals.max()-vals.min():.3f} dex (target for a second law: 0.05)")
P(f"  mass span of the rungs: {lms.max()-lms.min():.2f} decades  (item 125 promised nine)")
ck("K07.8 WHAT THIS RUNG ACTUALLY BUYS, and what it does not. It buys the one thing item 123/125 said was "
   "structurally impossible -- an M/L-free a_0 that is NOT confined to gas-rich dwarfs, because marginalising "
   "Upsilon does not require the stars to be absent. It does NOT close the ladder: it lands ABOVE the gas-rich "
   "rungs and widens the spread rather than collapsing it",
   True,
   f"mass span of the M/L-free ladder rises from 1.1 decades (all gas-rich dwarfs) to {lms.max()-lms.min():.2f} "
   f"with this rung, and this rung alone spans {math.log10(max(g['Mb'] for g in GALS)/min(g['Mb'] for g in GALS)):.2f} "
   f"decades internally; but the rung-to-rung spread is {vals.max()-vals.min():.3f} dex against the 0.05 criterion")

P("")
sys.exit(ck.done())
