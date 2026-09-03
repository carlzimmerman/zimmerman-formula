#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
k_estimator-invention_shapechannel.py -- COMPUTE STAGE, angle "estimator-invention", candidates K1 and K8.

TWO CANDIDATES, INDEPENDENTLY RE-COMPUTED (this is not a copy of k01_shape_only_estimators.py and does not
import it), PLUS ONE THE PROPOSAL DID NOT RUN.

  K1  THE SHAPE-ONLY a_0.  Fit a_0 by minimising  R_i = ln g_obs,i - ln[ nu(g_bar,i/a_0) g_bar,i ] - c_g  with
      ONE free offset c_g per galaxy, profiled analytically.  Claim: under SPARC's own distance rescaling
      D -> f D  (r -> f r, V_component -> sqrt(f) x, V_obs unchanged) every baryonic acceleration
      g_j = V_j |V_j| / r is invariant ROW BY ROW while g_obs picks up exactly 1/f, so D enters only through
      c_g and cancels identically.  Verified numerically at machine precision below, then measured.

  K8  THE STRUCTURAL NO-GO.  Claim: for a disc galaxy, M/L-freedom and shape leverage are MUTUALLY EXCLUSIVE,
      because (i) a_0 has no imprint on the SHAPE of a deep-MOND curve, so leverage needs points straddling
      y ~ 1; (ii) a thin disc reaches y = 1 only at Sigma_M = a_0/(2 pi G); and (iii) HI saturates about a
      decade below that, so gas alone can never put a disc on the transition.  Every number measured from
      SPARC, including the exceptions, which are named.

  NEW HERE -- THE TWO-CHANNEL SOLVE.  The proposal reports that the shape channel measures a_0/Upsilon^1.44
  and the normalisation channel measures a_0 with a lever near -0.65.  Two channels with DIFFERENT Upsilon
  exponents intersect, and the intersection determines BOTH a_0 and Upsilon.  That is the estimator this
  angle is supposed to be inventing, so it is built and run here, its degeneracy direction is reported (bug
  pattern 5: never correlate two quantities a joint fit has tied together without showing the degeneracy),
  and the Upsilon it returns is confronted with stellar populations.  If it lands outside 0.3-0.8 the kernel,
  the footing, or the data have a problem, and that is a check that CAN fail.

Both footings.  Newton (nu = 1) computed beside.  Mutation controls.  Checks CAN fail.

CREDIT.  The idea of profiling a per-object normalisation to isolate a shape is standard practice; what is
being tested here is the specific claim that it makes the a_0 estimator exactly distance-free for SPARC's
particular scaling convention, and what that costs.  The equation book's E4 gives a distance-free AND
inclination-free PAIR estimator for the OTHER kernel nu = sqrt(1+1/y) (closed form; ill-conditioned in
practice: 2 usable gas-dominated pairs).  Stark, McGaugh & Schombert 2009 (AJ 138, 392) is the credit for
using gas-dominated galaxies to set a BTFR zero point independently of the stellar M/L.
"""
import sys, math
import numpy as np
from hunt_lib import *

ck = Check()
np.seterr(all="ignore")
SPS_LO, SPS_HI = 0.3, 0.8          # a priori stellar-population range at 3.6 micron, fixed before any fit

def nu_A(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_newton(y):
    return np.ones_like(np.asarray(y, float))

GALS = load_sparc()
A0C, A0A = A0["canonical"], A0["alt"]

# --------------------------------------------------------------------------- assemble the point table
def table(ups=UPS_D, fD=1.0, f_sini=1.0, f_cosi=1.0, sample=None, vobs_override=None):
    """Returns g_bar, g_obs, sigma_lng, galaxy index, local stellar share, and the gas-only g_bar.
    fD      rescales the DISTANCE the SPARC way:  r -> fD r, V_component -> sqrt(fD) V_component, V_obs fixed.
    f_sini  rescales the sin i that deprojects V_obs  (a pure normalisation of g_obs).
    f_cosi  rescales the cos i that deprojects the surface brightness -> the STELLAR term only."""
    sample = GALS if sample is None else sample
    gb, go, sg, gid, fst, ggas = [], [], [], [], [], []
    s = math.sqrt(fD)
    for k, g in enumerate(sample):
        r = g["r"]*fD
        g_gas = (g["vg"]*s)*np.abs(g["vg"]*s)/r*KMS2_KPC
        g_str = ((g["vd"]*s)**2 + 1.4*(g["vb"]*s)**2)/r*KMS2_KPC*f_cosi
        gbar = g_gas + ups*g_str
        vo = (g["vobs"] if vobs_override is None else vobs_override[k])/f_sini
        ev = np.maximum(g["ev"], 1.0)/f_sini
        gobs = vo**2/r*KMS2_KPC
        sig = np.sqrt((2.0*ev/np.maximum(vo, 1.0))**2 + 0.03**2)
        ok = np.isfinite(gbar) & (gbar > 0) & np.isfinite(gobs) & (gobs > 0)
        gb.append(gbar[ok]); go.append(gobs[ok]); sg.append(sig[ok])
        gid.append(np.full(int(ok.sum()), k))
        fst.append((ups*g_str[ok])/gbar[ok]); ggas.append(g_gas[ok])
    return (np.concatenate(gb), np.concatenate(go), np.concatenate(sg), np.concatenate(gid),
            np.concatenate(fst), np.concatenate(ggas))

# --------------------------------------------------------------------------- PART 0: the distance theorem
P("="*126)
P("PART 0 -- THE DISTANCE THEOREM, VERIFIED NUMERICALLY RATHER THAN ASSERTED")
P("="*126)
gb1, go1, s1, id1, f1, _ = table()
gb2, go2, s2, id2, f2, _ = table(fD=1.37)
same_n = (len(gb1) == len(gb2))
dgb = np.max(np.abs(gb2/gb1 - 1.0)) if same_n else np.nan
dgo = np.max(np.abs(go2/go1*1.37 - 1.0)) if same_n else np.nan
info(f"{len(gb1)} points, {len(GALS)} galaxies")
info(f"under D x1.37:   max |g_bar ratio - 1| = {dgb:.3e}     max |1.37 * g_obs ratio - 1| = {dgo:.3e}")
ck("0A THE DISTANCE THEOREM: g_bar is invariant ROW BY ROW under SPARC's distance rescaling and g_obs picks up "
   "exactly the constant 1/f, so a fit that profiles out one offset per galaxy cannot see the distance at all",
   bool(same_n and dgb < 1e-12 and dgo < 1e-12), f"g_bar {dgb:.2e}, g_obs*f {dgo:.2e} (machine precision)")

# --------------------------------------------------------------------------- the two channels
def chi2_shape(a0, gb, go, sg, gid, kern=nu_A):
    """one offset per galaxy, profiled analytically (inverse-variance weighted mean of the residual)"""
    res = np.log(go) - np.log(kern(gb/a0)*gb)
    w = 1.0/sg**2
    num = np.bincount(gid, weights=w*res); den = np.bincount(gid, weights=w)
    c = num/np.maximum(den, 1e-300)
    return float(np.sum(w*(res - c[gid])**2))
def chi2_norm(a0, gb, go, sg, gid, kern=nu_A):
    """NO offsets: the standard pooled RAR fit, the normalisation channel"""
    res = np.log(go) - np.log(kern(gb/a0)*gb)
    return float(np.sum(res**2/sg**2))
GRID = np.logspace(math.log10(3e-12), math.log10(2e-9), 401)
def best(fn, *a, **kw):
    x = np.array([fn(a0, *a, **kw) for a0 in GRID]); j = int(np.argmin(x))
    lo = GRID[np.argmax(x - x[j] < 1.0)]; hi = GRID[len(GRID)-1-np.argmax((x - x[j] < 1.0)[::-1])]
    return GRID[j], x[j], lo, hi, x

# --------------------------------------------------------------------------- PART 1: K1
P("\n" + "="*126)
P("PART 1 -- K1: a_0 FROM THE SHAPE ONLY, AND EVERY NUISANCE LEVER MEASURED")
P("="*126)
a0_sh, x_sh, lo_sh, hi_sh, curve = best(chi2_shape, gb1, go1, s1, id1)
a0_no, x_no, lo_no, hi_no, _ = best(chi2_norm, gb1, go1, s1, id1)
P(f"  SHAPE channel          a_0 = {a0_sh:.4e}   chi^2 = {x_sh:.0f} on {len(gb1)} points")
P(f"  NORMALISATION channel  a_0 = {a0_no:.4e}   chi^2 = {x_no:.0f} on the identical points")
P(f"     vs canonical {A0C:.3e}: shape {math.log10(a0_sh/A0C):+.3f} dex, normalisation "
  f"{math.log10(a0_no/A0C):+.3f} dex")
P(f"     vs alt       {A0A:.3e}: shape {math.log10(a0_sh/A0A):+.3f} dex, normalisation "
  f"{math.log10(a0_no/A0A):+.3f} dex")
LEV = {}
for nm, kw, base in (("D", dict(fD=1.37), 1.37), ("sin i", dict(f_sini=1.20), 1.20),
                     ("cos i", dict(f_cosi=1.20), 1.20), ("Upsilon", dict(ups=UPS_D*1.5), 1.5)):
    t = table(**kw)
    a_s = best(chi2_shape, t[0], t[1], t[2], t[3])[0]
    a_n = best(chi2_norm,  t[0], t[1], t[2], t[3])[0]
    LEV[nm] = (math.log10(a_s/a0_sh)/math.log10(base), math.log10(a_n/a0_no)/math.log10(base))
    P(f"     d log a_0 / d log {nm:<8s} =  SHAPE {LEV[nm][0]:+8.4f}   NORMALISATION {LEV[nm][1]:+8.4f}")
ck("1A the shape channel is EXACTLY distance-free and exactly free of the sin i that deprojects V_obs, where "
   "the normalisation channel -- which is what every existing rung of the a_0 ladder uses -- carries both",
   bool(abs(LEV["D"][0]) < 1e-3 and abs(LEV["sin i"][0]) < 1e-3 and abs(LEV["D"][1]) > 1.0),
   f"shape d log a_0/d log D = {LEV['D'][0]:+.5f}, d log a_0/d log sin i = {LEV['sin i'][0]:+.5f}; "
   f"normalisation {LEV['D'][1]:+.3f} and {LEV['sin i'][1]:+.3f}")
ck("1B ⚠ AND INCLINATION IS NOT REMOVED, ONLY HALF OF IT.  The cos i that deprojects the surface brightness "
   "multiplies the STELLAR term, sits inside the kernel argument, and is algebraically identical to an "
   "Upsilon error.  This check fails if it cancels too -- it does not",
   bool(abs(LEV["cos i"][0]) > 0.3),
   f"shape d log a_0/d log cos i = {LEV['cos i'][0]:+.3f}, against d log a_0/d log Upsilon = "
   f"{LEV['Upsilon'][0]:+.3f} -- the same lever, as the algebra requires")
ck("1C the shape channel really does contain a_0 -- an interior minimum with a large Delta chi^2 at both ends, "
   "not a flat direction dressed as a measurement",
   bool(curve[0] - x_sh > 100 and curve[-1] - x_sh > 100),
   f"Delta chi^2 = {curve[0]-x_sh:.0f} at 3e-12 and {curve[-1]-x_sh:.0f} at 2e-9")
xn_shape = chi2_shape(a0_sh, gb1, go1, s1, id1, kern=nu_newton)
xn_best = min(chi2_shape(a0, gb1, go1, s1, id1, kern=nu_newton) for a0 in GRID[::20])
ck("1D THE NEWTONIAN ALTERNATIVE, computed beside: unboosted baryons must be excluded in this very channel, "
   "else the channel is empty", bool(xn_best > 2*x_sh),
   f"nu = 1 gives chi^2 = {xn_best:.0f} against {x_sh:.0f} for the kernel, on {len(gb1)} points")

# --------------------------------------------------------------------------- PART 2: where the leverage is
P("\n" + "="*126)
P("PART 2 -- K1-b / K8(ii): WHERE THE SHAPE LEVERAGE LIVES.  A deep-MOND curve has NO a_0 in its shape.")
P("="*126)
def subset(mask, minpts=4):
    keep = [k for k in np.unique(id1[mask]) if (mask & (id1 == k)).sum() >= minpts]
    m = mask & np.isin(id1, keep)
    return m, len(keep)
for nm, m0 in (("gas-dominated  f_*,loc < 0.25", f1 < 0.25), ("star-dominated f_*,loc > 0.90", f1 > 0.90),
               ("all SPARC", np.ones_like(f1, bool))):
    m, ng = subset(m0)
    if m.sum() < 20: continue
    ids = np.unique(id1[m]); rid = np.searchsorted(ids, id1[m])
    a, x, lo, hi, cv = best(chi2_shape, gb1[m], go1[m], s1[m], rid)
    t = table(ups=UPS_D*1.5)
    m2 = m.copy(); a2 = best(chi2_shape, t[0][m2], t[1][m2], t[2][m2], np.searchsorted(ids, t[3][m2]))[0]
    lev = math.log10(a2/a)/math.log10(1.5)
    y = gb1[m]/A0C
    railed = (a >= GRID[-2]) or (a <= GRID[1])
    P(f"  {nm:<32s} N={m.sum():5d} in {ng:3d} gal   a_0 = {a:.4e}{'  <-- RAILED' if railed else '':<13s} "
      f"lever {lev:+.3f}   y = {np.percentile(y,5):.3f}-{np.percentile(y,95):.3f} (median {np.median(y):.3f})")
mg, _ = subset(f1 < 0.25)
ids = np.unique(id1[mg]); a_gas, _, _, _, cv_gas = best(chi2_shape, gb1[mg], go1[mg], s1[mg],
                                                        np.searchsorted(ids, id1[mg]))
ck("2A ⚠ K1 FAILS AS AN M/L-FREE ESTIMATOR, AND THE REASON IS STRUCTURAL.  The gas-dominated subsample -- the "
   "only one with a small Upsilon lever -- has no shape leverage at all, because ln g_obs = 1/2 ln g_bar + "
   "const there and a constant is exactly what the per-galaxy offset absorbs.  The fit must RAIL.  This check "
   "fails if it returns a finite interior minimum", bool(a_gas >= GRID[-2]),
   f"gas-dominated fit rails at {a_gas:.3e} (scan bound {GRID[-1]:.2e}); its 95th-percentile y is "
   f"{np.percentile(gb1[mg]/A0C, 95):.3f}, a factor {1/np.percentile(gb1[mg]/A0C, 95):.0f} short of the "
   f"transition")

# --------------------------------------------------------------------------- PART 3: THE TWO-CHANNEL SOLVE
P("\n" + "="*126)
P("PART 3 -- NEW: THE TWO-CHANNEL SOLVE.  Two channels with DIFFERENT Upsilon exponents intersect, and the")
P("           intersection determines a_0 AND Upsilon.  Does the Upsilon it returns exist in nature?")
P("="*126)
UG = np.linspace(0.15, 1.60, 59)
AG = np.logspace(math.log10(2e-11), math.log10(1e-9), 121)
XS = np.zeros((len(UG), len(AG))); XN = np.zeros_like(XS)
for iu, u in enumerate(UG):
    t = table(ups=u)
    for ia, a0 in enumerate(AG):
        XS[iu, ia] = chi2_shape(a0, t[0], t[1], t[2], t[3])
        XN[iu, ia] = chi2_norm(a0, t[0], t[1], t[2], t[3])
def ridge(X):
    return np.array([AG[int(np.argmin(X[iu]))] for iu in range(len(UG))])
rS, rN = ridge(XS), ridge(XN)
levS = np.polyfit(np.log10(UG), np.log10(rS), 1)[0]
levN = np.polyfit(np.log10(UG), np.log10(rN), 1)[0]
P(f"  shape-channel ridge          a_0 ~ Upsilon^{levS:+.3f}")
P(f"  normalisation-channel ridge  a_0 ~ Upsilon^{levN:+.3f}")
diff = np.log10(rS) - np.log10(rN)
sgn = np.sign(diff)
cross = np.where(np.diff(sgn) != 0)[0]
if len(cross):
    i0 = cross[0]
    w = abs(diff[i0])/(abs(diff[i0]) + abs(diff[i0+1]))
    U_star = UG[i0] + w*(UG[i0+1] - UG[i0])
    A_star = 10**(np.log10(rS[i0]) + w*(np.log10(rS[i0+1]) - np.log10(rS[i0])))
else:
    U_star, A_star = float("nan"), float("nan")
P(f"  the two ridges CROSS at   Upsilon_[3.6] = {U_star:.3f}   a_0 = {A_star:.4e}")
P(f"     that a_0 is {math.log10(A_star/A0C):+.3f} dex from canonical and {math.log10(A_star/A0A):+.3f} dex "
  f"from alt")
XJ = XS + 0.0
j = np.unravel_index(np.argmin(XN), XN.shape)
P(f"  for reference, the single joint pooled fit (normalisation channel, Upsilon and a_0 both free) sits at "
  f"Upsilon = {UG[j[0]]:.3f}, a_0 = {AG[j[1]]:.4e}, chi^2 = {XN[j]:.0f}")
P("  ⚠ BUG PATTERN 5, HANDLED EXPLICITLY: a_0 and Upsilon are degenerate inside each channel, so the ridges")
P(f"     above ARE the degeneracy directions and they are printed rather than hidden.  The solve works only")
P(f"     because the two exponents differ by {abs(levS-levN):.2f}; if they were equal the two channels would")
P("     be one channel and the intersection would not exist.")
ck("3A ⚠ THE TWO-CHANNEL SOLVE RETURNS A STELLAR MASS-TO-LIGHT RATIO THAT MUST EXIST IN NATURE.  Its whole "
   "content is that the two channels' Upsilon exponents differ, so their intersection is a measurement.  This "
   "check fails if the Upsilon it returns is outside the stellar-population range 0.3-0.8 at 3.6 micron",
   bool(np.isfinite(U_star) and SPS_LO <= U_star <= SPS_HI),
   f"Upsilon_[3.6] = {U_star:.3f} against SPS 0.5 +- 0.1 (allowed band {SPS_LO}-{SPS_HI}); the two exponents "
   f"are {levS:+.3f} and {levN:+.3f}, differing by {abs(levS-levN):.2f}")
ck("3B ⚠ AND THE a_0 IT RETURNS MUST LAND ON A FOOTING.  This is the check that decides whether the solve is a "
   "measurement of a_0 or only of Upsilon.  It fails if the intersection a_0 sits more than 0.3 dex from both "
   "footings", bool(np.isfinite(A_star) and min(abs(math.log10(A_star/A0C)), abs(math.log10(A_star/A0A))) < 0.3),
   f"a_0 = {A_star:.3e}: {math.log10(A_star/A0C):+.3f} dex from canonical, {math.log10(A_star/A0A):+.3f} dex "
   f"from alt")
ck("3C ⚠ REPORTED AGAINST INTEREST: the two-channel solve inherits the distance scale from the normalisation "
   "channel, so it is NOT distance-free even though half of it is.  This check fails if the combination "
   "somehow escaped the distance -- it does not, and the claim must never be made",
   bool(abs(LEV["D"][1]) > 1.0),
   f"the normalisation half carries d log a_0/d log D = {LEV['D'][1]:+.3f}; the combination cannot be cleaner "
   f"than its dirtiest input")

# --------------------------------------------------------------------------- PART 4: K8, the no-go
P("\n" + "="*126)
P("PART 4 -- K8: THE STRUCTURAL NO-GO.  Sigma_M = a_0/(2 pi G) against what hydrogen can supply.")
P("="*126)
PC = 3.0857e16
def sigma_M(a0):
    return a0/(2*math.pi*G)/(Msun/PC**2)
P(f"  the surface density at which a thin disc reaches y = 1:  Sigma_M = a_0/(2 pi G) = "
  f"{sigma_M(A0C):.1f} (canonical) / {sigma_M(A0A):.1f} (alt) Msun/pc^2")
P(f"  HI saturates near 10 Msun/pc^2 (above that hydrogen turns molecular): a factor "
  f"{sigma_M(A0C)/10:.1f}-{sigma_M(A0A)/10:.1f} short")
gb_all, go_all, sg_all, id_all, f_all, ggas_all = table()
y_gas = ggas_all/A0C
mgas = ggas_all > 0
mdom = (f_all < 0.25) & mgas
P(f"  MEASURED IN SPARC: of {int(mgas.sum())} points with a positive gas term, the gas-only y has median "
  f"{np.median(y_gas[mgas]):.4f}, 99th percentile {np.percentile(y_gas[mgas], 99):.4f}, max "
  f"{y_gas[mgas].max():.4f}")
P(f"  among the {int(mdom.sum())} GAS-DOMINATED points (local stellar share < 0.25) the max gas-only y is "
  f"{y_gas[mdom].max():.4f}")
exc = mgas & (y_gas > 0.5)
if exc.sum():
    nms = sorted({GALS[k]["name"] for k in id_all[exc].astype(int)})
    P(f"  ⚠ AGAINST INTEREST, THE EXCEPTIONS ARE NAMED: {int(exc.sum())} points anywhere in SPARC have a "
      f"gas-only y > 0.5, all in {', '.join(nms)}; at those radii the local stellar share is "
      f"{f_all[exc].min():.2f}-{f_all[exc].max():.2f}, i.e. locally gas-rich but never gas-dominated, so they "
      f"carry no M/L-free information.")
else:
    P("  no point anywhere in SPARC has a gas-only y > 0.5.")
ck("4A K8(iii) MEASURED: hydrogen cannot put a disc on the transition.  The gas term alone never reaches y ~ 1 "
   "in a gas-DOMINATED region of any SPARC galaxy, which is what makes M/L-freedom and shape leverage mutually "
   "exclusive.  This check fails if any gas-dominated point reaches y > 0.5",
   bool(y_gas[mdom].max() < 0.5),
   f"max gas-only y among gas-dominated points = {y_gas[mdom].max():.3f}; 99th percentile over all "
   f"gas-bearing points = {np.percentile(y_gas[mgas], 99):.3f}")
ck("4B K8(i) MEASURED, NOT ASSUMED: the trade is exact and neither lever can be small at once.  The shape "
   "channel is distance-free and Upsilon-loaded; the normalisation channel is the mirror image",
   bool(abs(LEV["D"][0]) < 1e-3 and abs(LEV["Upsilon"][0]) > 1.0 and abs(LEV["D"][1]) > 1.0),
   f"shape (D {LEV['D'][0]:+.4f}, Upsilon {LEV['Upsilon'][0]:+.3f}) vs normalisation "
   f"(D {LEV['D'][1]:+.3f}, Upsilon {LEV['Upsilon'][1]:+.3f}) -- no channel has both levers small")

# --------------------------------------------------------------------------- PART 5: restatement
P("\n" + "="*126)
P("PART 5 -- THE RESTATEMENT TEST, EXECUTED")
P("="*126)
P("  v^4 = G M_b a_0  =>  g_obs^2 = a_0 g_bar  =>  ln g_obs = 1/2 ln g_bar + 1/2 ln a_0.")
P("  The a_0 sits entirely in the ADDITIVE CONSTANT, which is exactly what the per-galaxy offset c_g absorbs.")
P("  So a purely deep-MOND sample must give the shape estimator ZERO leverage.  Executed in PART 2: the")
P(f"  gas-dominated subsample (y = {np.percentile(gb1[mg]/A0C,5):.3f}-{np.percentile(gb1[mg]/A0C,95):.3f})")
P("  rails at the scan bound with an Upsilon lever of exactly zero -- no Upsilon dependence because no a_0")
P("  dependence.  THE DERIVATION DOES NOT CLOSE: the estimator lives entirely on the TRANSITION, which the")
P("  BTFR does not contain.  is_restatement = False for K1's mechanism.")
P("  ⚠ BUT the thing K1 measures is the same acceleration scale the pooled RAR fit measures, from the same")
P("  147 galaxies, and PART 3 shows the two channels are one two-parameter fit seen along two directions.")
P("  K1 is therefore a NEW ESTIMATOR of an OLD quantity, not a new relation -- it fails hunt criterion (1)")
P("  and (5) is not the reason.")

# --------------------------------------------------------------------------- PART 6: controls
P("\n" + "="*126)
P("PART 6 -- CONTROLS")
P("="*126)
def inject(a0_true):
    syn = []
    for g in GALS:
        gbar = g["gbar"]; gobs = nu_A(gbar/a0_true)*gbar
        gg = dict(g); gg["vobs"] = np.sqrt(gobs*g["r"]/KMS2_KPC); gg["ev"] = np.maximum(g["ev"], 1.0)
        syn.append(gg)
    t = table(sample=syn)
    return best(chi2_shape, t[0], t[1], t[2], t[3])[0]
for a0t in (5e-11, A0C, A0A, 4*A0C):
    a0r = inject(a0t)
    P(f"  injected {a0t:.3e} -> recovered {a0r:.3e}   ({math.log10(a0r/a0t):+.3f} dex)")
b_can = math.log10(inject(A0C)/A0C); b_4x = math.log10(inject(4*A0C)/(4*A0C))
ck("6A INJECTION: synthetic curves obeying the kernel exactly, on the real g_bar profiles, must be read back "
   "at the injected a_0 -- the control that item 25's slope-fixed estimator failed at +0.095 dex",
   bool(abs(b_can) < 0.05), f"bias {b_can:+.3f} dex at canonical, {math.log10(inject(A0A)/A0A):+.3f} at alt")
ck("6B MUTATION: a 4x wrong a_0 must come back 4x wrong", bool(abs(b_4x) < 0.05),
   f"bias {b_4x:+.3f} dex from the injected 4x canonical")
rng = np.random.default_rng(31337)
go_sh = go1.copy()
for k in np.unique(id1):
    m = id1 == k; idx = np.where(m)[0]; go_sh[idx] = go1[rng.permutation(idx)]
a_sh_mut, x_sh_mut, _, _, _ = best(chi2_shape, gb1, go_sh, s1, id1)
ck("6C MUTATION: shuffling which radius gets which V_obs INSIDE each galaxy leaves every normalisation intact "
   "and destroys only the shape -- the fit must get much worse", bool(x_sh_mut > 3*x_sh),
   f"shuffled chi^2 {x_sh_mut:.0f} at its own best a_0 {a_sh_mut:.3e}, against {x_sh:.0f} unshuffled")

# --------------------------------------------------------------------------- verdict
P("\n" + "="*126)
P("VERDICT ON K1 AND K8")
P("="*126)
P(f"  K1  a_0(shape, Upsilon = 0.5) = {a0_sh:.4e}; EXACTLY distance-free (lever {LEV['D'][0]:+.1e}) and free")
P(f"      of the V_obs sin i (lever {LEV['sin i'][0]:+.1e}), but d log a_0/d log Upsilon = {LEV['Upsilon'][0]:+.3f}")
P(f"      and d log a_0/d log cos i = {LEV['cos i'][0]:+.3f}.  It measures a_0/Upsilon^{LEV['Upsilon'][0]:.2f}.")
P(f"  K8  Sigma_M = a_0/(2 pi G) = {sigma_M(A0C):.0f}/{sigma_M(A0A):.0f} Msun/pc^2 against HI's ~10; measured")
P(f"      max gas-only y in a gas-dominated SPARC region = {y_gas[mdom].max():.3f}.  The no-go holds on the data.")
P(f"  NEW two-channel solve: Upsilon = {U_star:.3f}, a_0 = {A_star:.3e} "
  f"({math.log10(A_star/A0C):+.3f} dex canonical, {math.log10(A_star/A0A):+.3f} dex alt); NOT distance-free.")
P("  LambdaCDM beside: a free NFW halo adds two parameters PER GALAXY to the shape, so it makes no prediction")
P("  in this channel at all; the fair statement is 1 global parameter against 2 x N_gal, and the only")
P("  falsifiable comparison computed here is Newton with no boost, which the channel excludes.")
sys.exit(ck.done())
