#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
k02_rar_slope_law.py -- SECOND-LAW HUNT: THE RAR SLOPE LAW, a parameter-free prediction of a measured curve.
=============================================================================================================
THE CANDIDATE, as an equation between measured quantities:

        d ln g_obs                       sqrt(y) exp(-sqrt(y))                   g_bar               c
        ----------  =  Phi(y)  =  1 -  --------------------------- ,      y = ---------- ,   a_0 = --- sqrt(G rho_DE)
        d ln g_bar                       2 ( 1 - exp(-sqrt(y)) )                  a_0                2

The left side is the LOCAL LOGARITHMIC SLOPE of the radial acceleration relation.  The right side has NO free
parameter: the kernel is Route A and a_0 is fixed by the cosmological constant.  Phi runs monotonically from
1/2 (deep) to 1 (Newtonian), and the whole curve -- where it turns, how fast, and its two asymptotes -- is
predicted by Lambda alone.

WHY IT IS NOT A RESTATEMENT (the criterion that killed several apparent wins this session).
Take the deep-MOND law v^4 = G M_b a_0 and try to derive this.  It gives g_obs^2 = a_0 g_bar exactly, hence
ln g_obs = (1/2) ln g_bar + (1/2) ln a_0, hence d ln g_obs / d ln g_bar = 1/2 IDENTICALLY, with a_0 appearing
only in the INTERCEPT and not at all in the slope.  The derivation closes to a CONSTANT, and a constant
carries no a_0.  Every g_bar-dependence of Phi is therefore content the BTFR does not have, and the whole
measurement below is a test of the part of the theory that v^4 = G M_b a_0 does not contain.  The BTFR is
the Phi = 1/2 null hypothesis in the table below, and it is fitted with its own free intercept, so it is
not disadvantaged by the comparison.

WHY IT IS WORTH MEASURING THIS WAY: the slope is measured WITHIN each galaxy, between consecutive radii, so
  * distance cancels EXACTLY (r -> f r and V_component -> sqrt(f) x leave every g_bar invariant and multiply
    every g_obs by the same 1/f, so both log-differences are untouched);
  * the sin i that deprojects V_obs cancels EXACTLY (a constant factor on g_obs);
  * a coherent per-galaxy Upsilon error cancels EXACTLY from the slope VALUE for a star-dominated galaxy
    (it shifts ln g_bar by a constant), and survives only by moving the point into a different g_bar bin --
    the residual lever is measured below rather than assumed.

CREDIT, AND AN HONEST DOWNGRADE OF THE NOVELTY CLAIM (checked against the literature while writing this).
  * The kernel nu = 1/(1 - exp(-sqrt(y))) is McGaugh, Lelli & Schombert 2016 (PRL 117, 201101), who fitted it
    to the RAR with g_dagger FREE and Upsilon fixed -- i.e. through the normalisation, not the slope.
  * ⚠ The local logarithmic slope of the RAR is NOT a new observable.  Desmond 2023 (MNRAS 521, 1817, "On the
    functional form of the radial acceleration relation") uses exactly this quantity, evaluates it at
    g_bar,min and g_bar,max, ranks candidate functional forms by it, and concludes that "the SPARC data are
    insufficient to determine robustly the limiting behaviour of the RAR".  The dead heat between Route A and
    the simple mu found below is the same conclusion, reached independently.
  * Inside this repository, prep_2026/kernel_fingerprint/fingerprint.py proposed the local slope at fixed
    discrepancy as an a_0-independent kernel fingerprint in 2026-07 and never confronted it with data (no .out
    exists).  Item 22 tested the FORWARD direction with a_0 assumed (r = 0.62); item 91 tried the second
    derivative and found it unmeasurable.
  WHAT IS ACTUALLY NEW, then, is narrower than the item hoped, and is stated narrowly: (i) the slope measured
  as a WITHIN-GALAXY log-difference, which makes it exactly distance-free and exactly free of the sin i that
  deprojects V_obs -- neither of which is true of a slope read off the pooled RAR; (ii) the comparison run
  with a_0 FIXED by the cosmological constant and nothing fitted at all.

Both footings.  Rival kernels computed beside.  Mutation controls.  Checks CAN fail.
"""
import sys, math
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(2026090302)
np.seterr(all="ignore")

# ------------------------------------------------------------------------- the kernels and their slope laws
def Phi_routeA(y):
    u = np.sqrt(np.maximum(np.asarray(y, float), 1e-300)); e = np.exp(-u)
    return 1.0 - u*e/(2.0*(1.0 - e))
def Phi_sqrt(y):
    """nu = sqrt(1+1/y): the equation book's kernel (Milgrom 1999 vacuum function).  Phi = 1 - 1/(2(y+1))."""
    y = np.asarray(y, float); return 1.0 - 1.0/(2.0*(y + 1.0))
def Phi_simple(y):
    """the 'simple' mu = x/(1+x): nu = (1 + sqrt(1+4/y))/2."""
    y = np.maximum(np.asarray(y, float), 1e-300); s = np.sqrt(1.0 + 4.0/y)
    # d ln nu/d ln y = (2/y)/(s (1+s))
    return 1.0 - (2.0/y)/(s*(1.0 + s))
def Phi_deep(y):
    """the BTFR / deep-MOND null: the slope is 1/2 everywhere, a_0 lives only in the intercept."""
    return np.full(np.shape(y), 0.5)
def Phi_newton(y):
    return np.full(np.shape(y), 1.0)
KERNELS = [("Route A (operative)", Phi_routeA), ("sqrt(1+1/y) (equation book)", Phi_sqrt),
           ("simple mu = x/(1+x)", Phi_simple), ("deep MOND == the BTFR", Phi_deep),
           ("Newton, no boost", Phi_newton)]

# ------------------------------------------------------------------------- the measured slope profile
gals = load_sparc()
DB_MIN = 0.02          # a priori: consecutive radii must differ by >2% in ln g_bar, else the ratio is 0/0
def pairs(sample, ups=UPS_D, sD=1.0, s_sin=1.0, gobs_override=None):
    dO, dB, GM, WT, GID = [], [], [], [], []
    for k, g in enumerate(sample):
        s = math.sqrt(sD); r = g["r"]*sD
        gg = (g["vg"]*s)*np.abs(g["vg"]*s)/r*KMS2_KPC
        gd = (g["vd"]*s)**2/r*KMS2_KPC; gbl = (g["vb"]*s)**2/r*KMS2_KPC
        gb = gg + ups*(gd + 1.4*gbl)
        vo = g["vobs"]/s_sin; ev = np.maximum(g["ev"], 1.0)/s_sin
        go = vo**2/r*KMS2_KPC
        if gobs_override is not None: go = gobs_override[k]
        sg = np.sqrt((2.0*ev/np.maximum(vo, 1.0))**2 + 0.03**2)
        ok = np.isfinite(gb) & (gb > 0) & np.isfinite(go) & (go > 0)
        gb, go, sg = gb[ok], go[ok], sg[ok]
        for i in range(len(gb) - 1):
            db = math.log(gb[i+1]) - math.log(gb[i])
            if abs(db) < DB_MIN: continue
            dO.append(math.log(go[i+1]) - math.log(go[i])); dB.append(db)
            GM.append(math.sqrt(gb[i]*gb[i+1])); WT.append(1.0/(sg[i]**2 + sg[i+1]**2)); GID.append(k)
    return (np.array(dO), np.array(dB), np.array(GM), np.array(WT), np.array(GID))

EDGES = np.logspace(-12.2, -9.0, 12)     # a priori binning, fixed before looking at any result
def slope_profile(dO, dB, GM, WT, GID):
    """Regression through the origin of dO on dB inside each g_bar bin: the mean local RAR slope there.
    ⚠ BUG FIXED IN THE MAKING: the bin-error bootstrap MUST use its own fixed-seed generator.  The first
    version drew from the module-level rng, so calling this function twice (which the lever test does) gave
    different error bars and hence different weights, and the 'measured' distance lever came out at -0.13
    when the algebra says it is identically zero.  That was bootstrap noise divided by log10(1.37), not a
    dependence.  With the seed fixed the levers below come out at the numerical floor, as they must."""
    brng = np.random.default_rng(777)
    out = []
    for i in range(len(EDGES) - 1):
        m = (GM >= EDGES[i]) & (GM < EDGES[i+1])
        if m.sum() < 25: out.append((np.nan,)*5); continue
        num = float(np.sum(WT[m]*dO[m]*dB[m])); den = float(np.sum(WT[m]*dB[m]**2))
        s = num/den
        gl = np.unique(GID[m]); bs = []
        idxs = {p: np.where(m & (GID == p))[0] for p in gl}
        for _ in range(300):
            pick = brng.choice(gl, len(gl), replace=True)
            sel = np.concatenate([idxs[p] for p in pick])
            d2 = float(np.sum(WT[sel]*dB[sel]**2))
            if d2 > 0: bs.append(float(np.sum(WT[sel]*dO[sel]*dB[sel]))/d2)
        out.append((math.sqrt(EDGES[i]*EDGES[i+1]), s, float(np.std(bs)) if bs else np.nan, int(m.sum()), len(gl)))
    return out

P("="*126)
P("THE MEASURED SLOPE PROFILE OF THE RADIAL ACCELERATION RELATION, WITHIN GALAXIES")
P("="*126)
pr = pairs(gals)
info(f"{len(pr[0])} consecutive-radius pairs from {len(gals)} SPARC galaxies (|d ln g_bar| > {DB_MIN})")
PROF = slope_profile(*pr)
P("")
P(f"  {'g_bar (m/s^2)':>14s} {'measured slope':>16s} {'+-':>7s} {'N pairs':>8s} {'N gal':>6s} | " +
  "  ".join(f"{n.split(' (')[0][:16]:>16s}" for n, _ in KERNELS[:4]))
for row in PROF:
    if not np.isfinite(row[0]): continue
    gm, s, e, n, ng = row
    preds = "  ".join(f"{np.mean(f(gm/A0['canonical'])):16.3f}" for _, f in KERNELS[:4])
    P(f"  {gm:14.3e} {s:16.3f} {e:7.3f} {n:8d} {ng:6d} | {preds}")

# ------------------------------------------------------------------------- the parameter-free comparison
P(""); P("="*126)
P("ZERO-PARAMETER COMPARISON: each kernel's slope law with a_0 FIXED by Lambda, no fitting anywhere")
P("="*126)
good = [r for r in PROF if np.isfinite(r[0]) and np.isfinite(r[2]) and r[2] > 0]
gm = np.array([r[0] for r in good]); sm = np.array([r[1] for r in good]); se = np.array([r[2] for r in good])
info(f"{len(good)} usable bins spanning g_bar = {gm.min():.2e} to {gm.max():.2e} "
     f"(y = {gm.min()/A0['canonical']:.3f} to {gm.max()/A0['canonical']:.2f} on the canonical footing)")
CHI = {}
P(f"  {'kernel':30s} {'footing':10s} {'chi^2':>9s} {'dof':>5s} {'chi^2/dof':>10s}   free parameters")
for name, f in KERNELS:
    for foot, a0 in A0.items():
        pred = f(gm/a0)
        if name.startswith("deep") or name.startswith("Newton"):
            c = float(np.sum(((sm - pred)/se)**2)); dof = len(gm)
        else:
            c = float(np.sum(((sm - pred)/se)**2)); dof = len(gm)
        CHI[(name, foot)] = c
        P(f"  {name:30s} {foot:10s} {c:9.1f} {dof:5d} {c/dof:10.2f}   0 (a_0 from Lambda)")
        if name.startswith("Newton"): break        # Newton has no a_0
best = min(CHI, key=CHI.get)
ck("A the parameter-free prediction is not refuted, and it beats the restatement: with a_0 fixed by the "
   "cosmological constant and nothing fitted, the Route A slope law fits the measured RAR slope profile "
   "better than the deep-MOND slope of 1/2 -- which is the BTFR's own prediction for this observable, and is "
   "what a restatement of v^4 = G M_b a_0 would give",
   min(CHI[("Route A (operative)", f)] for f in A0) < CHI[("deep MOND == the BTFR", "canonical")],
   f"Route A chi^2 = {CHI[('Route A (operative)','canonical')]:.1f} (canonical) / "
   f"{CHI[('Route A (operative)','alt')]:.1f} (alt) vs deep-MOND 1/2 {CHI[('deep MOND == the BTFR','canonical')]:.1f} "
   f"on {len(gm)} bins")
ck("B the observable discriminates between kernels at all -- if every kernel gave the same chi^2 the "
   "measurement would be empty",
   max(CHI.values()) > 3*max(min(CHI.values()), 1.0),
   f"best {best[0]} ({best[1]}) chi^2 = {CHI[best]:.1f}; worst {max(CHI, key=CHI.get)[0]} "
   f"chi^2 = {max(CHI.values()):.1f}")

# --- the FAIR kernel comparison: let each kernel fit its own a_0, so only the SHAPE is being judged ---
P("")
P("  THE FAIR KERNEL COMPARISON -- each kernel allowed its OWN best a_0, so only the SHAPE of Phi(y) is judged:")
FREE = {}
for name, f in KERNELS[:3]:
    xs = np.logspace(-11.6, -9.3, 400)
    c = np.array([np.sum(((sm - f(gm/a))/se)**2) for a in xs])
    i = int(np.argmin(c)); FREE[name] = (float(xs[i]), float(c[i]))
    P(f"    {name:30s} best a_0 = {xs[i]:.3e}   chi^2 = {c[i]:7.1f} on {len(gm)} bins, 1 parameter")
bestfree = min(FREE, key=lambda k: FREE[k][1])
cA = FREE["Route A (operative)"][1]; cS = FREE["sqrt(1+1/y) (equation book)"][1]
cM = FREE["simple mu = x/(1+x)"][1]
ck("B2 ⚠ HALF A WIN, STATED AS HALF A WIN.  With each kernel given its own free a_0 -- so that only the SHAPE "
   "of Phi(y) is judged -- the operative Route A kernel is preferred over the equation book's sqrt(1+1/y) by "
   "Delta chi^2 ~ 9, but it is a DEAD HEAT with the 'simple' mu = x/(1+x) (Delta chi^2 < 1).  So the observable "
   "separates one rival and not the other, and Route A must not be quoted as 'the kernel the data pick'.  "
   "What it does do is what prep_2026/kernel_fingerprint/fingerprint.py proposed on paper in 2026-07 and never "
   "confronted with data, and what items 90 and 91 tried through the second derivative and could not measure",
   (cS - cA) > 5.0 and abs(cM - cA) < 5.0,
   "  ".join(f"{k.split(' (')[0]}: chi^2 {v[1]:.1f} at a_0 {v[0]:.2e}" for k, v in FREE.items()))

# ------------------------------------------------------------------------- a_0 from the slope profile alone
P(""); P("="*126)
P("a_0 MEASURED FROM THE SLOPE PROFILE ALONE -- distance-free and sin-i-free by construction")
P("="*126)
def a0_from_slopes(gm, sm, se, f=Phi_routeA):
    xs = np.logspace(-11.6, -9.3, 400)
    c = np.array([np.sum(((sm - f(gm/a))/se)**2) for a in xs])
    i = int(np.argmin(c)); lo = hi = xs[i]
    for j in range(i, -1, -1):
        if c[j] - c[i] > 1.0: lo = xs[j]; break
    for j in range(i, len(xs)):
        if c[j] - c[i] > 1.0: hi = xs[j]; break
    return xs[i], lo, hi, c[i]
a_s, a_lo, a_hi, c_s = a0_from_slopes(gm, sm, se)
info(f"a_0 (slope profile, Upsilon = 0.5) = {a_s:.4e}   68% [{a_lo:.3e}, {a_hi:.3e}]   "
     f"(+{math.log10(a_hi/a_s):.3f}/-{math.log10(a_s/a_lo):.3f} dex)   chi^2/dof = {c_s/max(len(gm)-1,1):.2f}")
for foot, a0 in A0.items():
    info(f"   vs {foot:10s} {a0:.3e}: {math.log10(a_s/a0):+.3f} dex")
# levers, measured
lev = {}
for lab, kw in (("D x1.37", dict(sD=1.37)), ("sin i x0.90", dict(s_sin=0.90))):
    pr2 = pairs(gals, **kw); PR2 = slope_profile(*pr2)
    g2 = [r for r in PR2 if np.isfinite(r[0]) and np.isfinite(r[2]) and r[2] > 0]
    a2 = a0_from_slopes(np.array([r[0] for r in g2]), np.array([r[1] for r in g2]), np.array([r[2] for r in g2]))[0]
    lev[lab] = math.log10(a2/a_s)
for u in (0.25, 1.00):
    pr2 = pairs(gals, ups=u); PR2 = slope_profile(*pr2)
    g2 = [r for r in PR2 if np.isfinite(r[0]) and np.isfinite(r[2]) and r[2] > 0]
    lev[f"Upsilon = {u}"] = a0_from_slopes(np.array([r[0] for r in g2]), np.array([r[1] for r in g2]),
                                           np.array([r[2] for r in g2]))[0]
lev_ups = math.log10(lev["Upsilon = 1.0"]/lev["Upsilon = 0.25"])/math.log10(4.0)
info(f"   LEVERS, measured not assumed:  d log a_0/d log D = {lev['D x1.37']/math.log10(1.37):+.4f}   "
     f"d log a_0/d log sin i = {lev['sin i x0.90']/math.log10(0.90):+.4f}   "
     f"d log a_0/d log Upsilon = {lev_ups:+.3f}")
U_rec = {f: UPS_D*10**(math.log10(a_s/a0)/lev_ups) for f, a0 in A0.items()}
info(f"   the shape channel measures a_0/Upsilon^{lev_ups:.2f}, so at Upsilon = 0.5 it sits HIGH.  The Upsilon "
     f"that reconciles it: {U_rec['canonical']:.3f} (canonical), {U_rec['alt']:.3f} (alt)")
info(f"   item 76 read the SAME quantity out of the NORMALISATION channel and got 0.656 (canonical) / "
     f"0.504 (alt).  The two channels are independent in their systematics and must agree.")
ck("C ⚠ AGAINST INTEREST AND THEN CROSS-CHECKED: at Upsilon = 0.5 the shape channel returns a_0 HIGH by "
   "+0.16 to +0.24 dex.  That is not a discrepancy but the Upsilon lever: the shape channel measures "
   "a_0/Upsilon^1.4, and the Upsilon that reconciles it must land inside the stellar-population range "
   "0.3-0.8 AND agree with what the normalisation channel independently required (item 76: 0.656 / 0.504).  "
   "If it did not, the two channels would be inconsistent and one of them would be wrong",
   all(0.3 < v < 0.8 for v in U_rec.values()) and abs(U_rec['canonical'] - 0.656) < 0.15,
   f"a_0 = {a_s:.3e} [+{math.log10(a_hi/a_s):.3f}/-{math.log10(a_s/a_lo):.3f} dex] at Upsilon = 0.5; "
   f"reconciling Upsilon {U_rec['canonical']:.3f} / {U_rec['alt']:.3f} against item 76's 0.656 / 0.504")
ck("D the levers are what the algebra says: distance and the V_obs deprojection cancel to the numerical floor "
   "because a within-galaxy log-difference cannot see a constant factor, and Upsilon survives because it moves "
   "the point into a different g_bar bin",
   abs(lev['D x1.37']) < 0.01 and abs(lev['sin i x0.90']) < 0.01,
   f"|d log a_0/d log D| = {abs(lev['D x1.37']/math.log10(1.37)):.5f}, "
   f"|d log a_0/d log sin i| = {abs(lev['sin i x0.90']/math.log10(0.90)):.5f}, Upsilon {lev_ups:+.3f}")

# ------------------------------------------------------------------------- controls
P(""); P("="*126); P("CONTROLS"); P("="*126)
# injection: synthetic curves obeying the kernel EXACTLY, through the identical pipeline
for a_true in (9.36e-11, 1.13e-10, 3.744e-10):
    rr = np.random.default_rng(int(a_true*1e13)); over = []
    for g in gals:
        gg = g["vg"]*np.abs(g["vg"])/g["r"]*KMS2_KPC
        gb = gg + UPS_D*(g["vd"]**2 + 1.4*g["vb"]**2)/g["r"]*KMS2_KPC
        gb = np.maximum(gb, 1e-16)
        over.append(nu(gb/a_true)*gb*np.exp(rr.normal(0, np.minimum(2*np.maximum(g["ev"],1.0)/np.maximum(g["vobs"],1.0), 0.15))))
    prI = pairs(gals, gobs_override=over); PI = slope_profile(*prI)
    gI = [r for r in PI if np.isfinite(r[0]) and np.isfinite(r[2]) and r[2] > 0]
    aI = a0_from_slopes(np.array([r[0] for r in gI]), np.array([r[1] for r in gI]), np.array([r[2] for r in gI]))[0]
    info(f"   injected a_0 = {a_true:.3e}  ->  recovered {aI:.3e}  ({math.log10(aI/a_true):+.3f} dex)")
    if abs(a_true - 9.36e-11) < 1e-13: bias_c = math.log10(aI/a_true)
    if abs(a_true - 3.744e-10) < 1e-13: bias_4 = math.log10(aI/a_true)
ck("M1 INJECTION: synthetic curves that obey the kernel exactly, run through the identical binning, "
   "differencing and weighting, are read back at the injected a_0 within 0.06 dex -- the finite-difference and "
   "binning biases are quantified, not assumed away (item 25's estimator failed exactly this control)",
   abs(bias_c) < 0.06, f"bias at canonical {bias_c:+.3f} dex")
ck("M2 MUTATION: a 4x wrong a_0 must be recovered as 4x wrong",
   abs(bias_4) < 0.15, f"injected 4x canonical, recovered {bias_4:+.3f} dex from it")
dO, dB, GM, WT, GID = pr
sh = rng.permutation(len(dO))
num = float(np.sum(WT*dO[sh]*dB)); den = float(np.sum(WT*dB**2))
info(f"   a GLOBAL shuffle of dO does NOT give zero -- it gives {num/den:+.3f} against the measured "
     f"{float(np.sum(WT*dO*dB))/den:+.3f} -- because both differences are predominantly NEGATIVE (both "
     f"accelerations fall outward), so a shuffle keeps their signs aligned.  That is a property of the "
     f"variables, not evidence.  The mutation that IS a clean null for a LAW about the g_bar dependence is to "
     f"destroy that dependence and check the profile goes FLAT:")
info("   nor is a dO shuffle a clean null for a REGRESSION SLOPE, because <dO> is not zero and each bin has "
     "its own dB distribution, so the shuffled statistic inherits a spurious bin dependence.  The null that IS "
     "clean for the claim 'the slope depends on g_bar' is to permute the BIN LABEL, leaving every (dO, dB) pair "
     "intact and only destroying which g_bar it belongs to.  The profile must then be FLAT at the global slope:")
shg = rng.permutation(len(GM))
PSH = slope_profile(dO, dB, GM[shg], WT, GID)
gsh = [r for r in PSH if np.isfinite(r[0]) and np.isfinite(r[2]) and r[2] > 0]
s_sh = np.array([r[1] for r in gsh]); e_sh = np.array([r[2] for r in gsh])
rise_real = (sm[-1] - sm[0])/math.sqrt(se[0]**2 + se[-1]**2)
rise_sh = (s_sh[-1] - s_sh[0])/math.sqrt(e_sh[0]**2 + e_sh[-1]**2)
glob = float(np.sum(WT*dO*dB))/float(np.sum(WT*dB**2))
info(f"   bin-label-permuted profile: " + " ".join(f"{v:.3f}" for v in s_sh) + f"   (global slope {glob:.3f})")
ck("M3 MUTATION, corrected twice: permuting the bin label -- destroying the g_bar dependence and nothing else "
   "-- must flatten the profile, because the RISE is the entire content of the law (the constant part is the "
   "BTFR restatement and is not what is being tested)",
   abs(rise_sh) < 0.35*abs(rise_real),
   f"real profile rises {sm[0]:.3f} -> {sm[-1]:.3f} ({rise_real:.1f} sigma); bin-permuted "
   f"{s_sh[0]:.3f} -> {s_sh[-1]:.3f} ({rise_sh:.1f} sigma), flat about the global {glob:.3f}")

P(""); P("="*126); P("THE ALTERNATIVE, COMPUTED BESIDE"); P("="*126)
P("  Newton with no dark matter is excluded by this observable at chi^2 = "
  f"{CHI[('Newton, no boost','canonical')]:.0f} on {len(gm)} bins.")
P("  LambdaCDM with a free halo is NOT excluded and cannot be: two halo parameters per galaxy can reproduce any")
P("  slope profile, and the published simulation work (Navarro+2017, Ludlow+2017, Keller-Wadsley 2017) shows")
P("  hydrodynamic LambdaCDM does reproduce an RAR of roughly this shape.  What LambdaCDM does not do is PREDICT")
P("  the curve above from a laboratory-measurable constant with nothing fitted.  That asymmetry -- one theory")
P("  makes the prediction, the other accommodates the measurement -- is the honest statement, and it is the")
P("  same asymmetry item 119 recorded.  It is not a discriminating test and must not be quoted as one.")
P("")
P("  THE RESTATEMENT TEST, EXPLICITLY:  v^4 = G M_b a_0  =>  g_obs^2 = a_0 g_bar  =>  d ln g_obs/d ln g_bar = 1/2")
P("  identically, with a_0 only in the intercept.  The derivation CLOSES, to a constant -- so the constant part")
P(f"  of the measurement is a restatement and the g_bar-DEPENDENCE is not.  Measured: the slope rises from")
if len(gm) >= 2:
    P(f"  {sm[0]:.3f} +- {se[0]:.3f} at g_bar = {gm[0]:.2e} to {sm[-1]:.3f} +- {se[-1]:.3f} at {gm[-1]:.2e}, a rise of "
      f"{(sm[-1]-sm[0])/math.sqrt(se[0]**2+se[-1]**2):.1f} sigma against the BTFR's flat 1/2.")
sys.exit(ck.done())
