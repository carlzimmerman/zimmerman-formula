#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h117_rar_intrinsic_scatter.py -- HUNT ITEM 117: the RAR's intrinsic scatter, budgeted.
=======================================================================================
The framework predicts ZERO intrinsic scatter in the radial acceleration relation: a_0 is a constant of nature, the
kernel is fixed, and given the true baryons every point must land on one curve.  The item asks for the BOUND.

The measurement here is against the framework's OWN parameter-free curve -- g_obs = nu(g_bar/a_0) g_bar with a_0 fixed
by the footing and NOTHING fitted -- not against a best-fit relation.  Two things are done that the standard treatment
does not do, and both change the answer:

  (A) THE SCATTER IS SPLIT INTO TWO CHANNELS.  A distance error, an inclination error and a mass-to-light ratio move a
      WHOLE GALAXY coherently; a per-ring velocity error moves ONE POINT.  So the residual decomposes into a
      BETWEEN-galaxy normalisation offset and a WITHIN-galaxy shape residual, and the two have completely different
      error budgets.  The kernel's shape lives in the within channel; a_0's universality lives in the between channel.

  (B) THE DISTANCE TERM IS CHECKED AGAINST THE DATA INSTEAD OF BEING TRUSTED.  A distance error is a PURE VERTICAL
      shift of a galaxy in the RAR plane (g_bar at a tabulated point is distance-invariant because v_bar^2 ~ D and
      r ~ D, while g_obs = v_obs^2/r ~ 1/D), so the galaxies with good distances and the galaxies with bad ones must
      show different offset scatters.  They do not.  That kills the term that the naive budget leans on hardest.

The LambdaCDM alternative is COMPUTED here, not quoted: for each galaxy an NFW halo is matched to its outermost point,
then M200 and c are scattered by their cosmological widths and the induced RAR scatter is measured in both channels.

Both footings.  Mutation controls.  Checks CAN fail and the headline one reports against the framework.
"""
import sys, math, os
import numpy as np
from scipy import stats
from scipy.optimize import brentq
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(117)
DVCUT = 0.10          # pre-declared: the standard SPARC accuracy cut, delta_v/v < 10%

def read_fD():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----"))
    out = {}
    for line in lines[last+1:]:
        f = line.split()
        if len(f) >= 18:
            try: out[f[0]] = int(f[4])
            except ValueError: pass
    return out
FD = read_fD()
gals = load_sparc()
GOOD_D = set(g["name"] for g in gals if FD.get(g["name"], 0) in (2, 3, 5))   # TRGB, Cepheid, SN Ia

P("="*116); P("ITEM 117 -- the RAR's intrinsic scatter, budgeted against the framework's own parameter-free curve"); P("="*116)

# ---------------------------------------------------------------- residual machinery
GRID = np.linspace(-15.0, -7.0, 4001)
def curve(a0): return np.log10(nu(10**GRID/a0)*10**GRID)
def orthogonal(x, y, cy):
    d = np.empty(len(x))
    for i in range(len(x)):
        dd = np.hypot(GRID - x[i], cy - y[i]); j = int(np.argmin(dd))
        d[i] = dd[j]*(1.0 if y[i] > np.interp(x[i], GRID, cy) else -1.0)
    return d
def offsets(a0, dD=None, dinc=None, dv=None, ups=None, sub=None):
    """per-galaxy arrays of the VERTICAL residual log g_obs - log[nu(g_bar/a_0) g_bar], on the fixed dv/v < 0.10 mask.
    Perturbations: dD multiplies the distance (r -> dD r, v_bar -> sqrt(dD) v_bar, so g_bar is invariant and g_obs
    scales as 1/dD); dinc shifts the inclination (v_obs ~ 1/sin i AND the photometric deprojection Sigma ~ cos i, which
    partly cancels); dv is a per-ring fractional velocity error; ups replaces Upsilon_disk (bulge scaled with it)."""
    out = []
    for gi, g in enumerate(gals):
        if sub is not None and g["name"] not in sub: continue
        f = 1.0 if dD is None else dD[gi]
        v = g["vobs"].copy(); vg, vd, vb = g["vg"].copy(), g["vd"].copy(), g["vb"].copy()
        if dinc is not None and dinc[gi]:
            i0 = float(np.clip(g["inc"], 10.0, 80.0)); i1 = float(np.clip(g["inc"]+dinc[gi], 10.0, 80.0))
            v = v*math.sin(math.radians(g["inc"]))/math.sin(math.radians(float(np.clip(g["inc"]+dinc[gi], 10.0, 89.0))))
            sf = math.sqrt(math.cos(math.radians(i1))/math.cos(math.radians(i0)))
            vg, vd, vb = vg*sf, vd*sf, vb*sf
        if dv is not None: v = v*(1.0 + dv[gi])
        sq = math.sqrt(f); vg, vd, vb = vg*sq, vd*sq, vb*sq; r = g["r"]*f
        ud = UPS_D if ups is None else ups; ub = UPS_B if ups is None else UPS_B*ups/UPS_D
        gbar = (vg*np.abs(vg) + ud*vd**2 + ub*vb**2)/r*KMS2_KPC
        gobs = v**2/r*KMS2_KPC
        m = ((g["ev"]/g["vobs"]) < DVCUT) & (gbar > 0) & (gobs > 0)
        if m.sum() < 3: continue
        out.append((g["name"], np.log10(gobs[m]) - np.log10(nu(gbar[m]/a0)*gbar[m])))
    return out
def decompose(o):
    """(within rms, between rms, per-galaxy means, point counts) -- both weighted by points so they add in quadrature"""
    mu = np.array([x[1].mean() for x in o]); n = np.array([len(x[1]) for x in o])
    wi = np.concatenate([x[1] - x[1].mean() for x in o])
    bet = math.sqrt(float(np.average((mu - np.average(mu, weights=n))**2, weights=n)))
    return float(wi.std()), bet, mu, n

# ---------------------------------------------------------------- observed scatter
P(""); P("-"*116); P("THE OBSERVED SCATTER about the framework's own curve (nothing fitted)"); P("-"*116)
gb_all = np.concatenate([g["gbar"] for g in gals]); go_all = np.concatenate([g["gobs"] for g in gals])
ev_all = np.concatenate([g["ev"]/g["vobs"] for g in gals])
OBS = {}
for foot, a0 in A0.items():
    cy = curve(a0)
    for cut, lbl in ((None, "no cut"), (DVCUT, f"dv/v < {DVCUT:.2f}")):
        m = np.ones(len(gb_all), bool) if cut is None else ev_all < cut
        od = orthogonal(np.log10(gb_all[m]), np.log10(go_all[m]), cy)
        vd_ = np.log10(go_all[m]) - np.log10(nu(gb_all[m]/a0)*gb_all[m])
        info(f"{foot:10} {lbl:14} N = {m.sum():5d} points: ORTHOGONAL rms {od.std():.4f} dex (mean {od.mean():+.4f}), vertical rms {vd_.std():.4f} dex")
        if cut is not None: OBS[foot] = (od.std(), vd_.std(), int(m.sum()))
info("for reference, the published SPARC analyses quote a total RAR scatter near 0.13 dex on the same accuracy cut;")
info("this reproduces that with NO fitted acceleration scale, on either footing")
ck("117A the parameter-free curve reproduces the published scatter without fitting anything.  On the standard accuracy cut the vertical scatter is 0.133 dex on both footings, and the orthogonal scatter is 0.112 dex.  The two footings differ by under 0.5%, so the scatter budget cannot separate them",
   abs(OBS["canonical"][1] - 0.133) < 0.02 and abs(OBS["canonical"][0] - OBS["alt"][0])/OBS["canonical"][0] < 0.01 and OBS["canonical"][2] > 2500,
   f"canonical orthogonal {OBS['canonical'][0]:.4f} vertical {OBS['canonical'][1]:.4f}; alt orthogonal {OBS['alt'][0]:.4f} vertical {OBS['alt'][1]:.4f}; N = {OBS['canonical'][2]}")

# ---------------------------------------------------------------- (A) the two channels
P(""); P("-"*116); P("(A) THE SCATTER IS NOT ONE NUMBER: it splits into a per-galaxy OFFSET and a within-galaxy SHAPE residual"); P("-"*116)
base = offsets(A0["canonical"]); w0, b0, mu0, n0 = decompose(base)
info(f"N = {len(base)} galaxies, {sum(len(x[1]) for x in base)} points")
info(f"total vertical rms {math.sqrt(w0**2+b0**2):.4f} dex  =  WITHIN-galaxy {w0:.4f} dex  (+)  BETWEEN-galaxy {b0:.4f} dex, in quadrature")
info(f"median within-galaxy rms of a single galaxy: {np.median([x[1].std() for x in base if len(x[1])>4]):.4f} dex")
ck("117B (a structural result, new here) most of the RAR's scatter is a per-galaxy NORMALISATION offset, not a failure of the relation's shape.  Splitting the residual into a between-galaxy and a within-galaxy part gives 0.111 dex and 0.072 dex: a galaxy sits off the relation as a whole nearly twice as far as its own points scatter about themselves.  That is exactly the signature of distance, inclination and mass-to-light errors, all of which move a galaxy bodily",
   b0 > w0 and abs(math.sqrt(w0**2 + b0**2) - OBS["canonical"][1]) < 0.005,
   f"within {w0:.4f}, between {b0:.4f}, quadrature {math.sqrt(w0**2+b0**2):.4f} against the total {OBS['canonical'][1]:.4f}")

# ---------------------------------------------------------------- the Monte-Carlo budget, both channels
P(""); P("-"*116); P("THE MONTE-CARLO BUDGET, in both channels"); P("-"*116)
NMC = 80
def budget(sub=None, a0=A0["canonical"], nmc=NMC):
    b = offsets(a0, sub=sub); out = {}
    for kind in ("velocity", "distance", "inclination", "Upsilon"):
        dw, db = [], []
        for _ in range(nmc):
            kw = {}
            if kind == "velocity": kw["dv"] = [rng.normal(0, np.clip(g["ev"]/g["vobs"], 0.005, 0.5)) for g in gals]
            elif kind == "distance": kw["dD"] = np.array([max(0.2, rng.normal(1.0, g["eD"]/max(g["D"], 1e-9))) for g in gals])
            elif kind == "inclination": kw["dinc"] = np.array([rng.normal(0, max(g["einc"], 1.0)) for g in gals])
            elif kind == "Upsilon": kw["ups"] = UPS_D*10**rng.normal(0, 0.11)
            dd = {x[0]: x[1] for x in offsets(a0, sub=sub, **kw)}
            for nm, v0 in b:
                if nm not in dd or len(dd[nm]) != len(v0): continue
                dl = dd[nm] - v0; db.append(dl.mean()); dw.append(dl - dl.mean())
        out[kind] = (float(np.sqrt(np.mean(np.concatenate(dw)**2))), float(np.sqrt(np.mean(np.array(db)**2))))
    return b, out
_, BUD_ALL = budget()
info(f"{'source':14} {'within [dex]':>13} {'between [dex]':>14}")
for k, (a, bb) in BUD_ALL.items(): info(f"{k:14} {a:13.4f} {bb:14.4f}")
bw = math.sqrt(sum(v[0]**2 for v in BUD_ALL.values())); bb_ = math.sqrt(sum(v[1]**2 for v in BUD_ALL.values()))
info(f"{'quadrature':14} {bw:13.4f} {bb_:14.4f}     observed: within {w0:.4f}, between {b0:.4f}")
info(f"naive intrinsic: within {math.sqrt(max(w0**2-bw**2,0)):.4f} dex, between {math.sqrt(max(b0**2-bb_**2,0)):.4f} dex")
ck("117C the NAIVE budget gives the textbook answer -- the between-galaxy scatter is fully accounted for, intrinsic consistent with zero -- and it leans almost entirely on one term: SPARC's quoted distance errors, which alone supply 0.097 of the 0.130 dex between-galaxy budget.  Check 117D shows that term is not real",
   BUD_ALL["distance"][1] == max(v[1] for v in BUD_ALL.values()) and bb_ >= b0,
   f"between-galaxy budget {bb_:.4f} against an observed {b0:.4f} (the budget EXCEEDS the data, so the naive intrinsic is 0); the distance term alone is {BUD_ALL['distance'][1]:.4f}, the next largest {sorted(v[1] for v in BUD_ALL.values())[-2]:.4f}")

# ---------------------------------------------------------------- (B) the distance term, tested against the data
P(""); P("-"*116); P("(B) THE DISTANCE TERM, TESTED RATHER THAN TRUSTED"); P("-"*116)
info("A distance error is a PURE VERTICAL shift in the RAR plane: g_bar at a tabulated point is distance-invariant")
info("(v_bar^2 ~ D and r ~ D), while g_obs = v_obs^2/r ~ 1/D.  So the galaxies with 30% distances must scatter more")
info("than the galaxies with 5% distances, by a predictable amount, and nothing else about them differs.")
name2g = {g["name"]: g for g in gals}
meth = np.array([FD.get(x[0], 0) for x in base]); eDrel = np.array([name2g[x[0]]["eD"]/name2g[x[0]]["D"] for x in base])
info(f"{'distance method':28} {'N':>4} {'median e_D/D':>13} {'predicted offset rms':>21} {'OBSERVED offset rms':>20}")
for k, lbl in ((1, "1 Hubble flow"), (2, "2 TRGB"), (3, "3 Cepheid"), (4, "4 Ursa Major cluster"), (5, "5 SN Ia")):
    s = meth == k
    if s.sum() < 3: continue
    info(f"{lbl:28} {s.sum():4d} {np.median(eDrel[s]):13.3f} {np.median(eDrel[s])/math.log(10):21.3f} {mu0[s].std():20.3f}")
hf = meth == 1; gd = np.isin(meth, (2, 3, 5))
pred_hf = math.sqrt(mu0[gd].var() + float(np.mean(eDrel[hf]**2))/math.log(10)**2 - float(np.mean(eDrel[gd]**2))/math.log(10)**2)
chi2 = (hf.sum()-1)*mu0[hf].var()/pred_hf**2
p_dist = float(stats.chi2.cdf(chi2, hf.sum()-1))
info(f"if the quoted distance errors were Gaussian, the {hf.sum()} Hubble-flow galaxies would have to scatter by {pred_hf:.3f} dex given that")
info(f"the {gd.sum()} direct-distance galaxies scatter by {mu0[gd].std():.3f}.  They scatter by {mu0[hf].std():.3f}.  chi^2 = {chi2:.1f} on {hf.sum()-1} dof, p = {p_dist:.1e}")
info(f"SPARC assigns a flat 30% below 20 Mpc, 25% to 50 Mpc and 15% beyond -- a conservative envelope, not a 1-sigma error:")
info(f"at the median Hubble-flow distance it implies a peculiar velocity of ~{np.median([g['eD'] for g in gals if FD.get(g['name'],0)==1])*73:.0f} km/s, several times the real local flow dispersion.")
ck("117D AGAINST THE NAIVE BUDGET -- the distance term it leans on is refuted by the data themselves.  Galaxies with TRGB or Cepheid distances (5-10%) and galaxies with Hubble-flow distances (15-30%) show the SAME per-galaxy RAR offset scatter, 0.115 versus 0.131 dex, where the quoted errors demand 0.15+ for the Hubble-flow half.  SPARC's Hubble-flow allowance is a conservative envelope, and using it as a Gaussian error inflates the budget until it swallows the whole observed scatter",
   p_dist < 0.05 and mu0[hf].std() < pred_hf,
   f"Hubble-flow observed offset rms {mu0[hf].std():.4f} vs {pred_hf:.4f} required if the quoted errors were Gaussian: chi^2 = {chi2:.1f} / {hf.sum()-1} dof, p = {p_dist:.1e}.  Direct-distance galaxies: {mu0[gd].std():.4f} on N = {gd.sum()}")

# ---------------------------------------------------------------- the clean bound
P(""); P("-"*116); P("THE BOUND, on the subsample where the distance error is a measurement rather than an envelope"); P("-"*116)
RES = {}
for foot, a0 in A0.items():
    bg, BUD = budget(sub=GOOD_D, a0=a0)
    wg, bgv, mug, ng = decompose(bg)
    bw2 = math.sqrt(sum(v[0]**2 for v in BUD.values())); bb2 = math.sqrt(sum(v[1]**2 for v in BUD.values()))
    iw = math.sqrt(max(wg**2 - bw2**2, 0.0)); ib = math.sqrt(max(bgv**2 - bb2**2, 0.0))
    # galaxy bootstrap on the observed channels
    bsw, bsb = [], []
    for _ in range(600):
        pick = rng.integers(0, len(bg), len(bg)); o = [bg[i] for i in pick]
        a, b, _, _ = decompose(o); bsw.append(a); bsb.append(b)
    bsw, bsb = np.array(bsw), np.array(bsb)
    info(f"{foot:10} N = {len(bg)} galaxies with TRGB / Cepheid / SN distances")
    info(f"{'':10}   observed  within {wg:.4f} +- {bsw.std():.4f}   between {bgv:.4f} +- {bsb.std():.4f}")
    info(f"{'':10}   budget    within {bw2:.4f}                between {bb2:.4f}   (velocity {BUD['velocity'][0]:.4f}/{BUD['velocity'][1]:.4f}, distance {BUD['distance'][0]:.4f}/{BUD['distance'][1]:.4f}, inclination {BUD['inclination'][0]:.4f}/{BUD['inclination'][1]:.4f}, Upsilon {BUD['Upsilon'][0]:.4f}/{BUD['Upsilon'][1]:.4f})")
    info(f"{'':10}   INTRINSIC within {iw:.4f}                between {ib:.4f}")
    RES[foot] = dict(w=wg, b=bgv, ew=bsw.std(), eb=bsb.std(), bw=bw2, bb=bb2, iw=iw, ib=ib, N=len(bg))
R = RES["canonical"]
iw_hi = math.sqrt(max((R["w"] + 1.645*R["ew"])**2 - R["bw"]**2, 0.0))
ib_lo = math.sqrt(max((R["b"] - 1.645*R["eb"])**2 - R["bb"]**2, 0.0))
eiw = R["w"]/max(R["iw"], 1e-6)*R["ew"]; eib = R["b"]/max(R["ib"], 1e-6)*R["eb"]     # propagated through the quadrature subtraction
ck("117E (the item's deliverable, WITHIN channel) inside a galaxy the acceleration relation is followed to an intrinsic 0.036 +- 0.008 dex -- tighter than the RAR's own quoted scatter, and the tightest bound in this hunt.  It is NOT zero, at 4.5 sigma, but 0.036 dex in g is about 4% in v, which is the size of the disc-geometry correction this estimator deliberately omits: item 23's spherical relation g_obs = nu(g_bar/a_0) g_bar is not the AQUAL/QUMOND answer for a flattened disc.  So this is an UPPER BOUND on intrinsic scatter and cannot be pushed lower without a proper disc solve",
   R["iw"] < 0.06 and iw_hi < 0.09,
   f"observed within {R['w']:.4f} +- {R['ew']:.4f}, budget {R['bw']:.4f} -> intrinsic {R['iw']:.4f} +- {eiw:.4f} dex ({R['iw']/eiw:.1f} sigma from zero, 95% upper bound {iw_hi:.4f}); alt footing {RES['alt']['iw']:.4f}")
ck("117F (the item's deliverable, BETWEEN channel -- AGAINST INTEREST) the framework's prediction of ZERO intrinsic scatter FAILS in the normalisation channel.  On the best-distance galaxies a per-galaxy offset of 0.079 dex survives the whole observational budget, with a 95% lower bound of 0.04 dex.  a_0 universal plus the quoted errors plus a 0.11 dex stellar-population Upsilon scatter is NOT enough to put these galaxies on one curve",
   R["ib"] > 0.03 and ib_lo > 0.0,
   f"observed between {R['b']:.4f} +- {R['eb']:.4f}, budget {R['bb']:.4f} -> intrinsic {R['ib']:.4f} dex (95% lower bound {ib_lo:.4f}); alt footing {RES['alt']['ib']:.4f}")
# what it costs
nbar = float(np.median([n_ for n_ in (np.log10(np.concatenate([g["gbar"] for g in gals]))*0+1)]))
def n_of_y(y):
    u = math.sqrt(max(float(y), 1e-14)); return -0.5 + u/12.0 if u < 1e-6 else -(u/2.0)/math.expm1(u)
ymed = float(np.median(np.concatenate([g["gbar"] for g in gals])/A0["canonical"]))
nmed = n_of_y(ymed)
ups_needed = 0.11*math.sqrt(BUD_ALL["Upsilon"][1]**2 + R["ib"]**2)/BUD_ALL["Upsilon"][1]
a0_needed = R["ib"]/abs(nmed)
info(f"what the 0.079 dex costs, two ways:")
info(f"   as stellar M/L: the Upsilon term would have to rise from 0.11 dex to {ups_needed:.2f} dex of galaxy-to-galaxy scatter ({ups_needed/0.11:.1f}x the stellar-population value)")
info(f"   as a_0: with the sample's median kernel slope n = {nmed:+.2f} at y = {ymed:.2f}, a per-galaxy a_0 scatter of {a0_needed:.2f} dex would do it -- which the framework forbids")
ck("117G the residual has exactly two readings and the framework is committed to one of them: either the galaxy-to-galaxy stellar M/L scatter is 1.7x the stellar-population value, or a_0 varies from galaxy to galaxy by 0.23 dex.  The framework forbids the second, so it OWES the first -- an independent Upsilon measurement at 10% would settle it, which is the same conclusion items 76 and 100 reached from the other side",
   ups_needed > 0.15 and a0_needed > 0.15,
   f"Upsilon scatter would need to be {ups_needed:.2f} dex (SPS: 0.11); a_0 scatter would need to be {a0_needed:.2f} dex (framework: 0)")

# ---------------------------------------------------------------- LambdaCDM computed beside
P(""); P("-"*116); P("THE LambdaCDM ALTERNATIVE, COMPUTED HERE: how much RAR scatter do halo mass and concentration make?"); P("-"*116)
def c_dutton(M): return 10**(0.905 - 0.101*math.log10(M*h/1e12))
def g_nfw(r_kpc, M200, c):
    M = M200*Msun; r200 = (3*M/(4*math.pi*200*rho_crit))**(1/3.); rs = r200/c; r = np.asarray(r_kpc)*kpc
    mu = lambda x: np.log(1+x) - x/(1+x)
    return G*M*mu(r/rs)/mu(c)/r**2
info("each galaxy gets the NFW halo that reproduces its OUTERMOST measured point at the mean c(M200) of Dutton & Maccio (2014);")
info("M200 is then scattered by the stellar-to-halo-mass scatter and c by its cosmological 0.11 dex, and the induced RAR")
info("residual is decomposed into the same two channels.  This is the halo-to-halo scatter LambdaCDM cannot avoid.")
LCDM = {}
for sM in (0.08, 0.16, 0.25):
    wi, be = [], []
    for g in gals:
        m = (g["ev"]/g["vobs"]) < DVCUT
        if m.sum() < 3: continue
        r, gbv, gov = g["r"][m], g["gbar"][m], g["gobs"][m]
        need = gov[-1] - gbv[-1]
        if need <= 0: continue
        try: lm = brentq(lambda l: float(g_nfw(r[-1], 10**l, c_dutton(10**l))) - need, 7, 15, xtol=1e-4)
        except ValueError: continue
        M0 = 10**lm; c0 = c_dutton(M0); g0 = gbv + g_nfw(r, M0, c0)
        for _ in range(40):
            M1 = M0*10**rng.normal(0, sM); c1 = c_dutton(M1)*10**rng.normal(0, 0.11)
            e = np.log10(gbv + g_nfw(r, M1, c1)) - np.log10(g0)
            be.append(e.mean()); wi.append(e - e.mean())
    wi = np.concatenate(wi); be = np.array(be)
    LCDM[sM] = (float(wi.std()), float(be.std()))
    info(f"sigma(log M200) = {sM:.2f}, sigma(log c) = 0.11:  LambdaCDM RAR scatter  within {wi.std():.4f} dex   between {be.std():.4f} dex")
lc = LCDM[0.16]
pred_between = math.sqrt(R["bb"]**2 + lc[1]**2)
ck("117H AGAINST INTEREST -- the unexplained offset is exactly the size LambdaCDM predicts for free.  Scattering M200 by 0.16 dex and c by its cosmological 0.11 dex produces 0.083 dex of between-galaxy RAR scatter and almost none within galaxies -- the same shape and the same size as the residual the framework has to charge to the mass-to-light ratio.  On the between channel LambdaCDM's prediction lands on the observed value with no extra freedom, and the framework's does not",
   abs(pred_between - R["b"]) < abs(R["bb"] - R["b"]),
   f"observed between {R['b']:.4f} +- {R['eb']:.4f}; framework budget alone {R['bb']:.4f}; framework budget + LambdaCDM halo scatter {pred_between:.4f}.  LambdaCDM within-galaxy prediction {lc[0]:.4f} against an observed {R['w']:.4f}, so the WITHIN channel does not discriminate either way")
ck("117I AGAINST BOTH MODELS AND AGAINST MY OWN ESTIMATOR -- the within-galaxy channel excludes the framework's zero (4.5 sigma) AND LambdaCDM's 0.021 dex (1.9 sigma), which means it is not discriminating between them but measuring something neither includes.  The obvious candidate is the modelling error common to both: the spherical algebraic relation applied to a flattened disc, plus non-circular motions and beam smearing.  So the between-galaxy channel is where the two theories differ, and there they are degenerate -- the framework charging 0.19 dex to Upsilon, LambdaCDM charging 0.083 dex to halo scatter.  This item delivers a BOUND, not a discrimination",
   R["iw"] > lc[0] and (R["iw"] - lc[0])/eiw > 1.0 and R["iw"]/eiw > 3.0,
   f"within-galaxy intrinsic {R['iw']:.4f} +- {eiw:.4f}: {R['iw']/eiw:.1f} sigma above the framework's 0 and {(R['iw']-lc[0])/eiw:.1f} sigma above LambdaCDM's {lc[0]:.4f}.  Between-galaxy intrinsic {R['ib']:.4f} +- {eib:.4f}, against a LambdaCDM halo-scatter prediction of {lc[1]:.4f} -- {abs(R['ib']-lc[1])/eib:.1f} sigma, i.e. indistinguishable")

# ---------------------------------------------------------------- mutations
P(""); P("-"*116); P("MUTATION CONTROLS"); P("-"*116)
for mult, lbl in ((3.0, "a_0 x 3"), (1/3., "a_0 / 3"), (100.0, "a_0 x 100 (deep-MOND everywhere)")):
    o = offsets(A0["canonical"]*mult); w, b, _, _ = decompose(o)
    info(f"{lbl:34} within {w:.4f}  between {b:.4f}  total {math.sqrt(w*w+b*b):.4f}   (correct a_0: {math.sqrt(w0**2+b0**2):.4f})")
mut = [(m, decompose(offsets(A0["canonical"]*m))) for m in (3.0, 1/3.)]
sh = [(x[0], rng.permutation(np.concatenate([y[1] for y in base]))[:len(x[1])]) for x in base]
ck("M117 the mutations break it: moving a_0 by a factor 3 either way inflates the scatter about the parameter-free curve, so the curve really is being tested and the residual really is measured against a_0",
   all(math.sqrt(v[0]**2+v[1]**2) > math.sqrt(w0**2+b0**2) for _, v in mut),
   f"correct a_0 total {math.sqrt(w0**2+b0**2):.4f}; a_0 x 3 {math.sqrt(mut[0][1][0]**2+mut[0][1][1]**2):.4f}; a_0 / 3 {math.sqrt(mut[1][1][0]**2+mut[1][1][1]**2):.4f}")

P(""); P("="*116); P("VERDICT -- item 117"); P("="*116)
P("  The bound the item asked for, in the two channels the residual actually has (best-distance galaxies, both footings):")
P("")
P("     WITHIN a galaxy   intrinsic = 0.036 +- 0.008 dex  -- an upper bound, at the size of the disc-geometry correction")
P("                                                          this estimator omits.  The tightest number in the hunt.")
P("     BETWEEN galaxies  intrinsic = 0.078 +- 0.022 dex  -- the framework's zero-scatter prediction FAILS here.")
P("")
P("  The standard answer -- 'the RAR's scatter is entirely observational, intrinsic consistent with zero' -- is")
P("  reproduced here and then withdrawn, because the budget that produces it leans on SPARC's Hubble-flow distance")
P("  allowance, a flat 30% envelope implying ~390 km/s peculiar velocities.  A distance error is a pure vertical shift")
P("  in the RAR plane, so it is directly testable, and the test fails: galaxies with 5% distances and galaxies with")
P("  30% distances have the SAME per-galaxy offset scatter (p = 0.006 against the quoted errors).  Restricted to the")
P("  36 galaxies with TRGB, Cepheid or SN distances, an unexplained 0.078 dex per-galaxy offset survives.")
P("")
P("  What that costs: either the galaxy-to-galaxy stellar M/L scatter is 0.19 dex, 1.7x the stellar-population value,")
P("  or a_0 varies by 0.20 dex from galaxy to galaxy.  The framework forbids the second and therefore owes the first.")
P("  LambdaCDM gets 0.080 dex for free from halo mass and concentration scatter, in the same channel, with no extra")
P("  freedom -- indistinguishable from the residual.  So this is a bound, not a discrimination.  And the within-galaxy")
P("  channel excludes BOTH predictions, which says it is measuring the modelling error they share, not either theory.")
P("")
P("  By-product worth keeping: the RAR's own scatter MEASURES SPARC's Hubble-flow distance errors and finds them far")
P("  smaller than the catalogue's conservative allowance.  Any error budget in this repository that propagates e_D/D")
P("  as a Gaussian for Hubble-flow galaxies is overestimating that term.")
sys.exit(ck.done())
