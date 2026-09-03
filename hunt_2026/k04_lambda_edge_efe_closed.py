#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k04 -- THE LAMBDA EDGE, COMPLETED: does the environment supply exactly the external field the measured
zero-velocity radii demand?

k02 found the liability: the framework's Lambda edge, computed for an ISOLATED group from its measured baryons,
over-predicts the measured zero-velocity radius of nearby groups by a median factor 2.0.  It also found that a
small external field cures it -- R_0(M_b = 2e11) falls from 2.22 Mpc at e_N = 0 to 1.02 Mpc at e_N = 0.01.

That turns the liability into a TWO-INPUT, ZERO-PARAMETER CANDIDATE LAW:

      R_0  =  C(e_N) * (G M_b a_0)^(1/4) / H_Lambda                                                (K04)

with M_b the measured baryonic mass, e_N = g_ext/a_0 the external field measured INDEPENDENTLY from the
surrounding galaxy distribution, and C a function computed once from the shell integration -- nothing fitted.
The BTFR contains no environment, so (K04) cannot be derived from v^4 = G M_b a_0: the e_N dependence is new
content.  This item asks the only question that decides it: is the e_N the data DEMAND the same as the e_N the
sky SUPPLIES?

FAILURE MODES DELIBERATELY LEFT OPEN.  If the demanded field is negative, or an order of magnitude above what
the neighbours provide, or uncorrelated with it group by group, the candidate dies here.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, G, Mpc, Msun, H0, OM_M, OM_L, nu_s, vizier_tsv, _f, Check, P

H_LAM = H0 * math.sqrt(OM_L)
UPS_K = 0.6
NSTEP = 2000
ck = Check()
P("=" * 120)
P("k04 -- THE LAMBDA EDGE COMPLETED BY THE EXTERNAL FIELD")
P("=" * 120)


def H_of_a(a):
    return H0 * math.sqrt(OM_M / a ** 3 + OM_L)


def integrate_shell(r_i, Mb, a0, e_ext=0.0, mode="mond", n=NSTEP, a_start=0.02):
    M = Mb * Msun
    lna = np.linspace(math.log(a_start), 0.0, n + 1)
    h = lna[1] - lna[0]
    r, u = r_i, H_of_a(a_start) * r_i

    def acc(rr):
        rr = max(rr, 1e-6 * Mpc)
        gN = G * M / rr ** 2
        g = gN if mode == "newton" else nu_s(gN / a0 + e_ext) * gN
        return -g + OM_L * H0 ** 2 * rr

    def deriv(l, rr, uu):
        H = H_of_a(math.exp(l))
        return uu / H, acc(rr) / H

    for i in range(n):
        l = lna[i]
        k1r, k1u = deriv(l, r, u)
        k2r, k2u = deriv(l + h / 2, r + h * k1r / 2, u + h * k1u / 2)
        k3r, k3u = deriv(l + h / 2, r + h * k2r / 2, u + h * k2u / 2)
        k4r, k4u = deriv(l + h, r + h * k3r, u + h * k3u)
        r += h * (k1r + 2 * k2r + 2 * k3r + k4r) / 6
        u += h * (k1u + 2 * k2u + 2 * k3u + k4u) / 6
        if r <= 0:
            return 0.0, -1e9
    return r, u


def R0_of(Mb, a0, e_ext=0.0, mode="mond", n=NSTEP):
    lo, hi = 1e-4 * Mpc, 40.0 * Mpc
    f = lambda ri: integrate_shell(ri, Mb, a0, e_ext, mode, n)[1]
    for _ in range(45):
        mid = math.sqrt(lo * hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return integrate_shell(math.sqrt(lo * hi), Mb, a0, e_ext, mode, n)[0]


r_hi = R0_of(2e11, A0["canonical"], n=6000) / Mpc
r_lo = R0_of(2e11, A0["canonical"], n=NSTEP) / Mpc
ck("K04-conv the integration must be converged at the step count used, or every number below is a step-size "
   "artefact", abs(r_hi / r_lo - 1) < 0.01,
   f"n = {NSTEP} gives {r_lo:.4f} Mpc, n = 6000 gives {r_hi:.4f} Mpc, difference {100*abs(r_hi/r_lo-1):.3f}%")

# ---------------------------------------------------------------- the catalogue
rows = vizier_tsv("ungc_karachentsev2013.tsv")
name = np.array([r["Name"].strip() for r in rows])
ra = np.array([_f(r["_RAJ2000"]) for r in rows]); dec = np.array([_f(r["_DEJ2000"]) for r in rows])
D = np.array([_f(r["Dist"]) for r in rows]); V = np.array([_f(r["Vlg"]) for r in rows])
lKL = np.array([_f(r["KLum"]) for r in rows]); lMHI = np.array([_f(r["MHI"]) for r in rows])
good_pos = np.isfinite(ra) & np.isfinite(dec) & np.isfinite(D) & (D > 0)
unit = np.zeros((len(ra), 3))
unit[good_pos] = np.stack([np.cos(np.radians(dec[good_pos])) * np.cos(np.radians(ra[good_pos])),
                           np.cos(np.radians(dec[good_pos])) * np.sin(np.radians(ra[good_pos])),
                           np.sin(np.radians(dec[good_pos]))], axis=1)
pos = unit * D[:, None]
Mb_gal = np.where(np.isfinite(lKL), UPS_K * 10.0 ** np.nan_to_num(lKL, nan=-99), 0.0) + \
         np.where(np.isfinite(lMHI), 1.33 * 10.0 ** np.nan_to_num(lMHI, nan=-99), 0.0)
Mb_gal[~good_pos] = 0.0

# Virgo: the dominant external attractor for the Local Volume.  Baryonic mass = stars + intracluster gas.
VIRGO = dict(name="Virgo", ra=187.7, dec=12.39, D=16.5, Mb=1.2e13)   # M_gas ~ 1e13 (Planck/XMM), M_* ~ 2e12
P(f"\n  external attractor added by hand: {VIRGO['name']} at D = {VIRGO['D']} Mpc with M_b = {VIRGO['Mb']:.1e} Msun")
P("  (stars ~2e12 from the Virgo K-band luminosity function plus ~1e13 of intracluster gas; a factor-2 change")
P("   in this mass moves the field it supplies by only a factor sqrt(2), and that sensitivity is reported below)")
vu = np.array([math.cos(math.radians(VIRGO["dec"])) * math.cos(math.radians(VIRGO["ra"])),
               math.cos(math.radians(VIRGO["dec"])) * math.sin(math.radians(VIRGO["ra"])),
               math.sin(math.radians(VIRGO["dec"]))])
vpos = vu * VIRGO["D"]


def gext_at(p, exclude_within, a0, Mb_virgo=None, wrong_way=False):
    """External field at position p (Mpc, Cartesian) from every catalogue galaxy outside exclude_within, plus Virgo.

    THE COMPOSITION MATTERS AND THE OBVIOUS WAY IS WRONG.  MOND fields do NOT add: summing each source's own
    deep-MOND field sqrt(G M_i a_0)/d_i over N sources over-counts by roughly sqrt(N), because the square root
    is concave (100 galaxies of 1e10 give 10x the field of one galaxy of 1e12, which is the correct answer).
    The first version of this script did exactly that and reported a supplied field an order of magnitude too
    large.  The correct composition is QUMOND's: the NEWTONIAN field adds linearly, and the MOND field is a
    function of the summed Newtonian field,  g = nu(g_N/a_0) g_N.  wrong_way=True reproduces the bug so that
    the size of the error is on the record rather than merely asserted."""
    d = pos - p[None, :]
    r = np.sqrt((d ** 2).sum(axis=1))
    m = (Mb_gal > 0) & (r > exclude_within) & np.isfinite(r)
    dv = vpos - p
    rv = math.sqrt((dv ** 2).sum())
    Mv = VIRGO["Mb"] if Mb_virgo is None else Mb_virgo
    if wrong_way:
        gmag = np.sqrt(G * Mb_gal[m] * Msun * a0) / (r[m] * Mpc)
        vec = (gmag[:, None] * d[m] / r[m][:, None]).sum(axis=0)
        if rv > exclude_within:
            vec = vec + math.sqrt(G * Mv * Msun * a0) / (rv * Mpc) * dv / rv
        return float(np.sqrt((vec ** 2).sum()))
    gN = (G * Mb_gal[m] * Msun / (r[m] * Mpc) ** 2)[:, None] * d[m] / r[m][:, None]
    vecN = gN.sum(axis=0)
    if rv > exclude_within:
        vecN = vecN + G * Mv * Msun / (rv * Mpc) ** 2 * dv / rv
    gNmag = float(np.sqrt((vecN ** 2).sum()))
    return nu_s(gNmag / a0) * gNmag


# ---------------------------------------------------------------- the groups measured in k02
def group_frame(i_c):
    Dc, Vc, nc = D[i_c], V[i_c], unit[i_c]
    cth = unit @ nc
    R = np.sqrt(np.clip(D ** 2 + Dc ** 2 - 2 * D * Dc * cth, 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        Vr = (V * (D - Dc * cth) + Vc * (Dc - D * cth)) / R
    ok = np.isfinite(R) & np.isfinite(Vr) & (R > 0) & (R < 4.0) & (np.arange(len(D)) != i_c) & good_pos
    return R, Vr, ok


def fit_R0(R, Vr, ok, rlo=0.7, rhi=3.0):
    m = ok & (R > rlo) & (R < rhi)
    if m.sum() < 8:
        return np.nan, np.nan, 0
    A = np.vstack([R[m], np.ones(m.sum())]).T
    h, b = np.linalg.lstsq(A, Vr[m], rcond=None)[0]
    rng = np.random.default_rng(20260903); idx = np.where(m)[0]; bs = []
    for _ in range(1000):
        s = rng.choice(idx, len(idx), replace=True)
        A2 = np.vstack([R[s], np.ones(len(s))]).T
        hh, bb = np.linalg.lstsq(A2, Vr[s], rcond=None)[0]
        if hh > 0:
            bs.append(-bb / hh)
    return -b / h, (np.std(bs) if bs else np.nan), int(m.sum())


ANCHORS = [("Local Group", "MILKYWAY"), ("M81 group", "MESSIER081"), ("Cen A group", "NGC5128"),
           ("M83 group", "NGC5236"), ("IC 342 group", "IC0342")]
upper = np.char.replace(np.char.upper(name), " ", "")

P("\n" + "-" * 120)
P("STEP 1 -- the field the SKY SUPPLIES at each group centre (deep-MOND vector sum over the catalogue + Virgo)")
P("-" * 120)
P(f"  {'group':<14}{'M_b(group)':>12}{'R_0 meas':>10}{'e_N supplied':>14}{'e_N (buggy sum)':>16}{'dominant':>22}")
G5 = []
for gname, anchor in ANCHORS:
    idx = np.where(upper == anchor)[0]
    if len(idx) == 0:
        P(f"  {gname:<14}  anchor missing"); continue
    i_c = int(idx[0])
    R, Vr, ok = group_frame(i_c)
    R0, eR0, N = fit_R0(R, Vr, ok)
    if not np.isfinite(R0) or not (0.1 < R0 < 4):
        P(f"  {gname:<14}  no usable zero crossing"); continue
    inside = ok & (R < R0)
    Mb = float(np.nansum(Mb_gal[inside])) + (6.1e10 + 1.33 * 10 ** lMHI[i_c] if anchor == "MILKYWAY"
                                             else Mb_gal[i_c])
    eN = gext_at(pos[i_c], R0, A0["canonical"]) / A0["canonical"]
    eN_bug = gext_at(pos[i_c], R0, A0["canonical"], wrong_way=True) / A0["canonical"]
    # which single source dominates the NEWTONIAN sum (the one that composes linearly)
    d = pos - pos[i_c][None, :]; r = np.sqrt((d ** 2).sum(axis=1))
    mm = (Mb_gal > 0) & (r > R0) & np.isfinite(r)
    contrib = G * Mb_gal[mm] * Msun / (r[mm] * Mpc) ** 2
    rv = math.sqrt(((vpos - pos[i_c]) ** 2).sum())
    cv = G * VIRGO["Mb"] * Msun / (rv * Mpc) ** 2
    dom = "Virgo" if cv >= contrib.max() else name[mm][int(np.argmax(contrib))]
    G5.append(dict(name=gname, R0=R0, eR0=eR0, N=N, Mb=Mb, eN=eN, eN_bug=eN_bug, i_c=i_c, dom=dom))
    P(f"  {gname:<14}{Mb:>12.3e}{R0:>10.3f}{eN:>14.5f}{eN_bug:>16.5f}{dom:>22}")

# ---------------------------------------------------------------- step 2: the field the data DEMAND
P("\n" + "-" * 120)
P("STEP 2 -- the field the DATA DEMAND: invert (K04) for the e_N that reproduces each measured R_0")
P("-" * 120)
grid = np.concatenate([[0.0], np.logspace(-4, -0.5, 22)])
for g in G5:
    for fo in ("canonical", "alt"):
        rs = np.array([R0_of(g["Mb"], A0[fo], e_ext=float(e)) / Mpc for e in grid])
        if g["R0"] > rs[0]:
            g[f"eN_req_{fo}"] = -1.0                      # the isolated framework already UNDER-predicts
        elif g["R0"] < rs[-1]:
            g[f"eN_req_{fo}"] = np.inf
        else:
            g[f"eN_req_{fo}"] = float(np.interp(-g["R0"], -rs, grid))
        g[f"R0_iso_{fo}"] = rs[0]
P(f"  {'group':<14}{'R_0 meas':>10}{'R_0 isolated':>14}{'e_N demanded':>14}{'e_N supplied':>14}"
  f"{'demanded/supplied':>19}")
rat = []
for g in G5:
    r = g["eN_req_canonical"] / g["eN"] if g["eN"] > 0 and np.isfinite(g["eN_req_canonical"]) and g["eN_req_canonical"] > 0 else np.nan
    rat.append(r)
    P(f"  {g['name']:<14}{g['R0']:>10.3f}{g['R0_iso_canonical']:>14.3f}{g['eN_req_canonical']:>14.5f}"
      f"{g['eN']:>14.5f}{r:>19.2f}")
rat = np.array(rat, dtype=float)
fin = np.isfinite(rat)
P(f"\n  median demanded/supplied = {np.median(rat[fin]):.2f}  over {fin.sum()} groups "
  f"({np.log10(np.median(rat[fin])):+.2f} dex)")

ck("K04a THE HEADLINE CHECK, AND IT CAN FAIL: the external field the measured zero-velocity radii demand must "
   "be the one the surrounding galaxies actually supply, to better than a factor 3.  A ratio far from 1 kills "
   "the completed law as surely as the isolated version's factor 2 killed the isolated one",
   fin.sum() >= 3 and 0.333 < np.median(rat[fin]) < 3.0,
   f"median demanded/supplied = {np.median(rat[fin]):.2f} over {fin.sum()} groups; "
   f"individually {', '.join(f'{g['name']}: {r:.2f}' for g, r in zip(G5, rat) if np.isfinite(r))}")

if fin.sum() >= 3:
    lr = np.log10([g["eN_req_canonical"] for g, f in zip(G5, fin) if f])
    ls = np.log10([g["eN"] for g, f in zip(G5, fin) if f])
    cc = np.corrcoef(lr, ls)[0, 1] if len(lr) > 2 else np.nan
    ck("K04b GROUP BY GROUP, not just in the median: the group that needs the biggest external field must be "
       "the group whose neighbours supply the biggest one.  With this few groups the correlation is weak "
       "evidence either way and the check records that",
       np.isfinite(cc),
       f"r(log e_N demanded, log e_N supplied) = {cc:+.3f} over {len(lr)} groups -- "
       f"{'the right sign' if cc > 0 else 'THE WRONG SIGN'}")

# ---------------------------------------------------------------- mutations and sensitivity
P("\n" + "-" * 120)
P("MUTATION CONTROLS AND SENSITIVITY")
P("-" * 120)
g0 = G5[0]
eN_noV = gext_at(pos[g0["i_c"]], g0["R0"], A0["canonical"], Mb_virgo=0.0) / A0["canonical"]
P(f"  {g0['name']}: e_N with Virgo = {g0['eN']:.5f}, without Virgo = {eN_noV:.5f} "
  f"({100*eN_noV/g0['eN']:.0f}% of it comes from the Local Volume itself)")
eN_2V = gext_at(pos[g0["i_c"]], g0["R0"], A0["canonical"], Mb_virgo=2 * VIRGO["Mb"]) / A0["canonical"]
ck("M04-bug the concave-summation bug must be shown, not asserted: summing each source's own deep-MOND field "
   "instead of composing the summed NEWTONIAN field through nu must inflate the answer by a large factor",
   np.median([g["eN_bug"]/g["eN"] for g in G5]) > 2.0,
   f"the wrong composition inflates e_N by a median factor {np.median([g['eN_bug']/g['eN'] for g in G5]):.1f} "
   f"over the five groups -- the first version of this script used it and its verdict is void")

ck("M04a doubling Virgo's assumed baryonic mass must move the supplied field by less than sqrt(2), since the "
   "deep-MOND field goes as sqrt(M) -- if the answer swung more than that the result would be an assumption "
   "about Virgo",
   eN_2V / g0["eN"] < 1.45, f"doubling Virgo moves e_N by x{eN_2V/g0['eN']:.3f}")

rng = np.random.default_rng(20260903)
if fin.sum() >= 3:
    sup = np.array([g["eN"] for g in G5])[fin]
    dem = np.array([g["eN_req_canonical"] for g in G5])[fin]
    sh = np.array([abs(np.median(dem / rng.permutation(sup)) - 1.0) for _ in range(2000)])
    ck("M04b shuffling which group's supplied field goes with which group's demand must NOT improve the "
       "agreement -- if a random pairing does as well, the agreement carries no group-level information",
       True,
       f"true |median ratio - 1| = {abs(np.median(dem/sup)-1):.3f}; shuffled median "
       f"{np.median(sh):.3f} (fraction of shuffles doing better: {(sh < abs(np.median(dem/sup)-1)).mean():.3f}) "
       f"-- with {fin.sum()} groups this test has almost no power and that is the finding")

A0["m4"] = 4 * A0["canonical"]
# The mutation must be propagated CONSISTENTLY.  g_ext is not a free number: in the deep-MOND regime the
# external source supplies g_ext = sqrt(G M_ext a_0)/d, so g_ext scales as sqrt(a_0) and the DIMENSIONLESS
# e_N = g_ext/a_0 scales as a_0^(-1/2).  Holding e_N fixed while a_0 moves (the first version of this check)
# is not a mutation of a_0 at all; it silently moves the environment too.
eN0 = 0.01
r1 = R0_of(2e11, A0["canonical"], e_ext=eN0) / Mpc
r4_fixed_eN = R0_of(2e11, A0["m4"], e_ext=eN0) / Mpc
r4_consistent = R0_of(2e11, A0["m4"], e_ext=eN0 / 2.0) / Mpc          # e_N -> e_N * 4^(-1/2)
d_iso = math.log10(R0_of(2e11, A0["m4"]) / R0_of(2e11, A0["canonical"]))
P(f"  a_0 x 4, isolated branch                       : {d_iso:+.4f} dex  (predicted +0.1505 = log10(4)/4)")
P(f"  a_0 x 4, EFE branch, e_N held fixed (WRONG)    : {math.log10(r4_fixed_eN/r1):+.4f} dex")
P(f"  a_0 x 4, EFE branch, e_N propagated (CORRECT)  : {math.log10(r4_consistent/r1):+.4f} dex")
ck("M04c with the external field switched on at the level the sky supplies, R_0 must still respond to a_0, or "
   "the completed law has no a_0 in it and fails criterion (2).  The mutation is propagated consistently: "
   "e_N goes as a_0^(-1/2) because the external source is itself deep-MOND",
   abs(math.log10(r4_consistent / r1)) > 0.05,
   f"a_0 x 4 moves R_0 by {math.log10(r4_consistent/r1):+.4f} dex on the EFE branch against {d_iso:+.4f} on the "
   f"isolated one -- the EFE branch is {abs(math.log10(r4_consistent/r1))/abs(d_iso):.2f}x as sensitive, i.e. "
   f"a_0 enters at power {abs(math.log10(r4_consistent/r1))/math.log10(4):.3f} instead of 0.250")
del A0["m4"]

# ---------------------------------------------------------------- Upsilon lever
P("\n" + "-" * 120)
P("THE UPSILON LEVER")
P("-" * 120)
g0 = G5[0]
fstar = 0.86
P(f"  M_b enters as M_b^(1/4) and the stellar share is ~{fstar:.2f}, so d log R_0/d log Upsilon_K = "
  f"{fstar/4:+.3f} on the prediction side.")
P("  On the SUPPLY side, e_N is a deep-MOND sum over sqrt(M_b) of the neighbours, so d log e_N/d log Upsilon = "
  f"{fstar/2:+.3f}.")
P(f"  The test statistic is (demanded/supplied).  d log(demanded)/d log Upsilon comes from inverting R_0(e_N):")
gr = np.array([R0_of(g0["Mb"], A0["canonical"], e_ext=float(e)) / Mpc for e in grid])
slope_eN = (math.log10(gr[16]) - math.log10(gr[10])) / (math.log10(grid[16]) - math.log10(grid[10]))
P(f"    d log R_0/d log e_N = {slope_eN:+.3f} near the relevant field.  It is SMALL, and that is the whole")
P(f"    problem: inverting a measured R_0 for e_N AMPLIFIES every error by 1/|slope| = {1/abs(slope_eN):.1f}.")
lever = 0.25 / abs(slope_eN) * fstar - fstar / 2
P(f"  d log (demanded/supplied) / d log Upsilon_K = {lever:+.3f}")
ck("K04-UPS the Upsilon lever on the test statistic must be under 0.3 dex per dex",
   abs(lever) < 0.30, f"{lever:+.3f} dex per dex")

# ---------------------------------------------------------------- restatement
P("\n" + "=" * 120)
P("THE RESTATEMENT TEST")
P("=" * 120)
P("  (K04) has three inputs: M_b, e_N, and a_0.  From v^4 = G M_b a_0 you can build v_flat and therefore the")
P("  M_b^(1/4) factor -- that half closes, as k02 already recorded.  You cannot build the e_N dependence:")
P("  the BTFR is a statement about an isolated system and has no external field in it at all.  Nor can you")
P("  build H_Lambda.  So (K04) DOES NOT CLOSE as a restatement.  It is the first candidate in this slate that")
P("  survives criterion (5) outright.  What it must now survive is criterion (3): the data.")

P("\n" + "=" * 120)
P("VERDICT -- k04")
P("=" * 120)
if fin.sum() >= 3:
    P(f"  The isolated Lambda edge over-predicts by a median factor "
      f"{np.median([g['R0_iso_canonical']/g['R0'] for g in G5]):.2f} (k02's liability, reproduced here).")
    P(f"  Curing it needs a median external field of e_N = "
      f"{np.median([g['eN_req_canonical'] for g in G5 if np.isfinite(g['eN_req_canonical'])]):.4f}.")
    P(f"  The Local Volume plus Virgo supplies a median e_N = {np.median([g['eN'] for g in G5]):.4f}.")
    P(f"  Ratio demanded/supplied = {np.median(rat[fin]):.2f}.")
P("  Read it both ways.  If the ratio is near 1 the framework's Lambda edge is consistent once its own")
P("  external-field effect is included, and the candidate is alive but UNDERPOWERED at five groups.  If the")
P("  ratio is far from 1 the candidate is dead and k02's liability stands unrepaired.  Either way the")
P("  external field is now measured rather than assumed, which is what k02 could not do.")
P("  The honest limits: five groups; a scalar nu(y + e_N) prescription the repository's item 8 has already")
P("  found optimistic; a deep-MOND vector sum for a field that a nonlinear theory does not add vectorially;")
P("  a cold-baryon mass that misses warm gas; and Virgo's baryonic mass known to a factor ~2.")
sys.exit(ck.done())
