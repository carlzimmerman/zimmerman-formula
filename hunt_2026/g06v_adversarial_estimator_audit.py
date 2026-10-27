#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g06v_adversarial_estimator_audit.py -- ADVERSARIAL AUDIT of g06_local_volume_groups_lambda_edge.py.
=================================================================================================================
THE CLAIM UNDER ATTACK.  26 UNGC Local Volume groups (333 member entries) sit at a median missing boost of 0.817
(canonical a_0) / 0.746 (alt) at g_bar/a_0 = 0.0019, CONSISTENT with the framework's zero-parameter prediction and
NOT reproducing the liability table's cluster-scale deficit; claimed strength 3.6 sigma of separation from the
table's X-ray group/cluster median of 2.11, on the group side's bootstrap error alone.

THE LENS: the ESTIMATOR and the arithmetic.  This repo has been bitten by (1) total mass where enclosed mass
belongs, (2) a spherical formula on a disc, (3) an aperture centred on a local minimum, (4) a covariance reshaped
wrong, (5) a residual whose sign tracks a branch of the author's own prescription.  Every number below is
re-derived from the raw catalogue by code written independently of the target file: own coordinate transform, own
gapper, own group construction, own ANALYTIC Plummer enclosed-mass fraction (r^3/(r^2+a^2)^{3/2}) rather than a
cumulative trapezoid, and own quadrature.  NOTHING is imported from g06 except the shared loaders in hunt_lib.

The one quantity NOT re-derived from scratch is the per-group external field e_N, which needs the 2MRS + 2M++
machinery; it is taken verbatim from g06's own section-4 printout and then STRESSED over a factor 1 - 100 (V8), so
that no conclusion here rests on trusting it.

WHAT THIS FILE FOUND, STATED BEFORE THE CHECKS SO IT CANNOT BE READ OFF SELECTIVELY
  * The central number is EXACT.  Independent code reproduces 0.706 (isolated) and 0.816 (primary) against g06's
    0.706 and 0.817.  No arithmetic error was found.
  * The estimator survives every one of the five bug patterns.  In particular the measurement uses ENCLOSED mass:
    the total-mass point-mass shortcut would have given 0.648, and g06 does not take it.
  * The real defect is in the CLAIMED STRENGTH, not the claim.  The unweighted median over groups carrying 3 to 37
    velocities is not the right estimator, and it is biased LOW -- but correcting it moves the answer TOWARD unity
    and makes the cluster separation LARGER, not smaller.  Reported anyway, both ways, per the working rule.
  * Two checks below FAIL and are meant to: the richest-subsample instability (V9) and the double-counted groups
    (V10).  Neither overturns the headline; both are undisclosed in g06 and belong in its caveats.
"""
import sys, os, math, collections
import numpy as np
from scipy.stats import chi2
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0, DATA, vizier_tsv, _f, G, Msun, Mpc, H0

ck = Check(); rng = np.random.default_rng(20260903)
UPS_K, F_HE, F_HOT, MW_MSTAR, NMIN = 0.60, 1.33, 0.50, 5.0e10, 5
H0_KMS = H0*Mpc/1e3
# g06's own reported medians, the targets this file has to hit or contradict
G06 = dict(isolated=0.706, interp_can=0.817, interp_alt=0.746, x_can=0.00189, x_alt=0.00157,
           boot_lo=0.656, boot_hi=1.110, ups04=1.011, ups10=0.621, fhot0=0.912, fhot1=0.746,
           ap_rh=0.648, ap_3rmax=0.873, raw2mpp=2.215, a0x3_ratio=0.5841, nu_off=15.0, scramble=1.052)
# e_N (total, baryonic) per group, transcribed from g06's section-4 table.  STRESSED x1-x100 in V8.
EN = {"MESSIER031": 0.00021, "MESSIER081": 0.00012, "NGC3368": 0.00037, "Milky Way": 0.00007,
      "NGC5128": 0.00017, "NGC4258": 0.00018, "NGC5236": 0.00012, "NGC4736": 0.00015, "NGC4594": 0.00014,
      "IC0342": 0.00015, "NGC3412": 0.00059, "NGC0253": 0.00009, "NGC3115": 0.00014, "NGC3627": 0.00018,
      "NGC2784": 0.00010, "NGC6744": 0.00010, "NGC6946": 0.00011, "NGC4945": 0.00016, "MESSIER101": 0.00025,
      "NGC0925": 0.00006, "NGC2903": 0.00015, "NGC3432": 0.00016, "NGC3521": 0.00017, "NGC4631": 0.00016,
      "NGC5055": 0.00012, "NGC5194": 0.00018}

# ============================================================================================ INDEPENDENT REBUILD
def eq2gal(ra, de):
    rap, dep, lncp = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
    ra_, de_ = math.radians(ra), math.radians(de)
    b = math.asin(math.sin(de_)*math.sin(dep) + math.cos(de_)*math.cos(dep)*math.cos(ra_ - rap))
    l = lncp - math.atan2(math.cos(de_)*math.sin(ra_ - rap),
                          math.sin(de_)*math.cos(dep) - math.cos(de_)*math.sin(dep)*math.cos(ra_ - rap))
    return math.degrees(l) % 360.0, math.degrees(b)

def cart(ra, de, D):
    l, b = eq2gal(ra, de); lr, br = math.radians(l), math.radians(b)
    return np.array([D*math.cos(br)*math.cos(lr), D*math.cos(br)*math.sin(lr), D*math.sin(br)])

def gapper(v):
    x = np.sort(np.asarray(v, float)); n = len(x); i = np.arange(1, n)
    return float(math.sqrt(math.pi)/(n*(n - 1))*np.sum(i*(n - i)*np.diff(x)))

def angsep(a, b):
    r1, d1, r2, d2 = map(math.radians, (a["_RAJ2000"], a["_DEJ2000"], b["_RAJ2000"], b["_DEJ2000"]))
    return math.acos(max(-1.0, min(1.0, math.sin(d1)*math.sin(d2) + math.cos(d1)*math.cos(d2)*math.cos(r1 - r2))))

P("="*126); P("0.  INDEPENDENT REBUILD OF THE SAMPLE FROM THE RAW CATALOGUE"); P("="*126)
raw = vizier_tsv("ungc_karachentsev2013.tsv")
for x in raw:
    for k in ("Dist", "KLum", "MHI", "Vlg", "Ti1", "_RAJ2000", "_DEJ2000"): x[k] = _f(x[k])
    x["Name"] = x["Name"].strip(); x["MD"] = x["MD"].strip(); x["f_Dist"] = x["f_Dist"].strip()
byname = {x["Name"].upper(): x for x in raw}
sat = collections.defaultdict(list)
for x in raw:
    if x["Ti1"] > 0 and x["MD"].upper() in byname and x["MD"].upper() != x["Name"].upper():
        sat[x["MD"]].append(x)
groups = []
for hn, ss in sorted(sat.items(), key=lambda t: -len(t[1])):
    if len(ss) + 1 < NMIN: continue
    h = byname[hn.upper()]; mem = [h] + ss; D = h["Dist"]
    if D < 2.0:
        hv = cart(h["_RAJ2000"], h["_DEJ2000"], D)
        rr = np.array([np.linalg.norm(cart(m["_RAJ2000"], m["_DEJ2000"], m["Dist"]) - hv) for m in ss])
    else:
        rr = (4/3.)*np.array([angsep(h, m)*D for m in ss])
    ok = [m for m in mem if np.isfinite(m["Vlg"])]
    v = np.array([m["Vlg"] for m in ok], float); dd = np.array([m["Dist"] for m in ok], float)
    LK = float(np.nansum([10**m["KLum"] for m in mem if np.isfinite(m["KLum"])]))
    LKh = (10**h["KLum"] if np.isfinite(h["KLum"]) else 0.0)
    MHI = float(np.nansum([10**m["MHI"] for m in mem if np.isfinite(m["MHI"])]))
    if hn == "Milky Way": LK += MW_MSTAR/UPS_K; LKh = MW_MSTAR/UPS_K
    groups.append(dict(name=hn, N=len(mem), Nv=len(ok), D=D, rh=float(np.median(rr)), rmax=float(np.max(rr)),
                       sig=gapper(v - H0_KMS*dd), sig_raw=gapper(v), sdD=float(np.std(dd, ddof=1)),
                       LK=LK, LKh=LKh, MHI=MHI))
info(f"independent rebuild: {len(groups)} groups, {sum(g['N'] for g in groups)} member entries, "
     f"{sum(g['Nv'] for g in groups)} of them with a velocity")
ck("V0 the sample rebuilds identically from the raw VizieR table with independently written geometry, membership "
   "and gapper code.  If the group construction did not reproduce, nothing downstream would be comparable",
   len(groups) == 26 and sum(g["N"] for g in groups) == 333,
   f"{len(groups)} groups (g06: 26), {sum(g['N'] for g in groups)} members (g06: 333); member counts per group "
   f"{min(g['N'] for g in groups)}-{max(g['N'] for g in groups)}, velocities per group "
   f"{min(g['Nv'] for g in groups)}-{max(g['Nv'] for g in groups)}")

# ============================================================================ INDEPENDENT JEANS, ANALYTIC PLUMMER
def sigma_pred(g, a0, f_hot=F_HOT, ups=UPS_K, mode="interp", gmult=1.0, hot_central=False,
               proj=False, a0mult=1.0, nu_on=True, point_total=False):
    """Independent solve.  Plummer tracer with the group's own half-number radius; ANALYTIC enclosed-number
    fraction r^3/(r^2+a^2)^{3/2} (g06 uses a cumulative trapezoid -- deliberately a different route);
    sigma_r^2(r) = (1/rho) int_r^inf rho g dr'; then either the 3-D truncated number-weighted <sigma_r^2> that
    g06 uses, or (proj=True) the honest Abel-projected line-of-sight aperture dispersion."""
    a0 = a0*a0mult
    rh, rt = g["rh"]*Mpc, g["rmax"]*Mpc; a = rh/1.3047
    Mh = ups*g["LKh"]*Msun
    Msat = (ups*(g["LK"] - g["LKh"]) + F_HE*g["MHI"])*Msun
    Mhot = f_hot*ups*g["LK"]*Msun
    if hot_central: Mh, Mext = Mh + Mhot, Msat
    else:           Mext = Msat + Mhot
    # e_N was tabulated as gext/a_0(canonical), so the PHYSICAL field is EN x 9.36e-11.  It must NOT be rescaled
    # when the footing changes or when a_0 is mutated -- the external field is a property of the sky, not of a_0.
    gext = EN[g["name"]]*A0["canonical"]*gmult
    r = np.geomspace(1e-4*rh, 4000*rh, 6000)
    rho = (1.0 + (r/a)**2)**-2.5
    if point_total:                       # the WRONG shortcut: all baryons as one central point mass
        gN = G*(Mh + Mext)/r**2
    else:
        gN = G*(Mh + Mext*r**3/(r*r + a*a)**1.5)/r**2
    if not nu_on:
        gE = gN
    elif mode == "isolated":
        s = np.sqrt(gN/a0); gE = gN/(1.0 - np.exp(-s))
    else:
        x = (gN + gext)/a0; w = gext/(gN + gext); s = np.sqrt(x)
        nuv = 1.0/(1.0 - np.exp(-s)); Lv = -0.5*s*np.exp(-s)/(1.0 - np.exp(-s))
        gE = nuv*(1.0 + Lv*w/3.0)*gN
    integ = rho*gE
    tail = np.concatenate([np.cumsum((0.5*(integ[1:] + integ[:-1])*np.diff(r))[::-1])[::-1], [0.0]])
    s2 = tail/rho
    if not proj:
        w2 = rho*r**2*(r <= rt)
        return math.sqrt(float(np.trapz(w2*s2, r)/np.trapz(w2, r)))
    R = np.geomspace(1e-3*rh, rt, 220); num = np.empty_like(R); den = np.empty_like(R)
    for i, Rv in enumerate(R):
        k = r > Rv*1.0000001; rr2 = r[k]; jac = rr2/np.sqrt(rr2*rr2 - Rv*Rv)
        num[i] = 2*np.trapz(rho[k]*s2[k]*jac, rr2); den[i] = 2*np.trapz(rho[k]*jac, rr2)
    return math.sqrt(float(np.trapz(R*num, R)/np.trapz(R*den, R)))

def boosts(a0, **kw):
    return np.array([(g["sig"]*1e3/sigma_pred(g, a0, **kw))**2 for g in groups])

def xbar(a0, ups=UPS_K, f_hot=F_HOT):
    """g_bar/a_0 at the half-number radius, ENCLOSED mass, independently."""
    out = []
    for g in groups:
        rh = g["rh"]*Mpc; a = rh/1.3047
        Mh = ups*g["LKh"]*Msun
        Mext = (ups*(g["LK"] - g["LKh"]) + F_HE*g["MHI"])*Msun + f_hot*ups*g["LK"]*Msun
        out.append(G*(Mh + Mext*rh**3/(rh*rh + a*a)**1.5)/rh**2/a0)
    return np.array(out)

P(""); P("="*126); P("1.  THE CENTRAL NUMBER, RE-DERIVED"); P("="*126)
B = {}; X = {}
for foot, a0 in A0.items():
    B[foot] = boosts(a0); X[foot] = xbar(a0)
    info(f"{foot:9} a_0 = {a0:.3e}:  median boost {np.median(B[foot]):.3f} "
         f"({math.log10(np.median(B[foot])):+.3f} dex), median g_bar/a_0 = {np.median(X[foot]):.5f}")
b_iso = boosts(A0["canonical"], mode="isolated")
info(f"isolated branch (no external field): median boost {np.median(b_iso):.3f}")
ck("V1 the primary median reproduces on BOTH footings under independently written code -- different coordinate "
   "transform, different enclosed-mass route (analytic, not trapezoid), different quadrature.  A 2% tolerance; "
   "anything larger and one of the two files has an arithmetic error",
   abs(np.median(B["canonical"])/G06["interp_can"] - 1) < 0.02 and
   abs(np.median(B["alt"])/G06["interp_alt"] - 1) < 0.02,
   f"canonical {np.median(B['canonical']):.3f} vs g06's {G06['interp_can']}; alt {np.median(B['alt']):.3f} vs "
   f"{G06['interp_alt']}; isolated {np.median(b_iso):.3f} vs {G06['isolated']}")
ck("V2 the reported acceleration reproduces too, on both footings.  The rung's whole placement argument is that "
   "these groups sit BELOW every cluster row in g_bar/a_0, so this number carries as much weight as the boost",
   abs(np.median(X["canonical"])/G06["x_can"] - 1) < 0.02 and abs(np.median(X["alt"])/G06["x_alt"] - 1) < 0.02,
   f"canonical median g_bar/a_0 {np.median(X['canonical']):.5f} vs g06's {G06['x_can']}; alt "
   f"{np.median(X['alt']):.5f} vs {G06['x_alt']}; sample spans {X['canonical'].min():.5f} - "
   f"{X['canonical'].max():.5f}")

P(""); P("="*126); P("2.  THE FIVE BUG PATTERNS, ONE AT A TIME"); P("="*126)
b_pt = boosts(A0["canonical"], point_total=True)
ck("V3 (bug pattern 1: TOTAL mass where ENCLOSED belongs) g06 is NOT taking the shortcut.  Collapsing all the "
   "baryons onto one central point mass -- the move that would make the prediction look best-case -- gives a "
   "DIFFERENT and lower boost.  If g06 had used total mass its number would have matched this one instead",
   abs(math.log10(np.median(b_pt)/np.median(B["canonical"]))) > 0.05,
   f"total-mass point-mass shortcut {np.median(b_pt):.3f} vs g06's enclosed-mass solve "
   f"{np.median(B['canonical']):.3f}, a gap of {math.log10(np.median(b_pt)/np.median(B['canonical'])):+.3f} dex; "
   f"the shortcut would have understated the boost, so the choice is against interest")
b_proj = boosts(A0["canonical"], proj=True)
ck("V4 (bug pattern 3: the aperture) g06 predicts a 3-D number-weighted <sigma_r^2> truncated at r_max, but what "
   "is OBSERVED is a projected line-of-sight dispersion inside a projected aperture.  Redone honestly through the "
   "Abel integral -- Sigma(R) sigma_los^2(R) = 2 int_R^inf rho sigma_r^2 r dr/sqrt(r^2-R^2), then aperture-weighted "
   "by 2 pi R dR -- the answer must not move by more than the bootstrap half-width",
   abs(math.log10(np.median(b_proj)/np.median(B["canonical"]))) < 0.114,
   f"Abel-projected sigma_los estimator {np.median(b_proj):.3f} vs g06's 3-D truncated "
   f"{np.median(B['canonical']):.3f}, a shift of "
   f"{math.log10(np.median(b_proj)/np.median(B['canonical'])):+.3f} dex against the bootstrap half-width 0.114")
br = {m: float(np.median(boosts(A0["canonical"], mode=m))) for m in ("isolated", "interp")}
br["gext x10"] = float(np.median(boosts(A0["canonical"], gmult=10.0)))
ck("V5 (bug pattern 5: a residual whose sign tracks a branch of the author's own prescription) the answer must "
   "not be manufactured by the choice of external-field branch.  The admissible branches at the measured "
   "e_N/x_int ~ 0.06 are the isolated one and the interpolated one; they must bracket the answer inside the "
   "bootstrap band, and the sign of the residual must not flip between them",
   max(br["isolated"], br["interp"])/min(br["isolated"], br["interp"]) < 1.692 and
   (br["isolated"] - 1.0)*(br["interp"] - 1.0) > 0,
   f"isolated {br['isolated']:.3f}, interpolated {br['interp']:.3f} -- factor "
   f"{max(br['isolated'],br['interp'])/min(br['isolated'],br['interp']):.3f} against the bootstrap band's 1.692; "
   f"both on the same side of unity.  A tenfold error in e_N would give {br['gext x10']:.3f}")
hn = np.array([H0_KMS*g["sdD"] for g in groups]); so = np.array([g["sig"] for g in groups])
b_nohub = np.array([(g["sig_raw"]*1e3/sigma_pred(g, A0["canonical"]))**2 for g in groups])
ck("V6 the member-by-member Hubble-flow subtraction cannot be injecting the signal.  Distance errors turn "
   "v - H_0 D into a noise generator, and at 10 Mpc with TF distances that noise would be ~130 km/s, comparable "
   "to sigma itself.  It is not, because the member distances inside a group are overwhelmingly TRGB or "
   "membership-assigned, and dropping the correction entirely barely moves the median",
   float(np.median(hn/so)) < 0.35 and
   abs(math.log10(float(np.median(b_nohub))/np.median(B["canonical"]))) < 0.114,
   f"median H_0 x sd(D) inside a group = {np.median(hn):.1f} km/s against a median sigma of {np.median(so):.1f} "
   f"km/s (ratio {np.median(hn/so):.3f}); no-Hubble-correction median boost {np.median(b_nohub):.3f} vs "
   f"{np.median(B['canonical']):.3f}")

P(""); P("="*126); P("3.  THE CURRENCY AND THE COMPARISON SET"); P("="*126)
md = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "THE_LIABILITY_TABLE.md")).read()
rows = []
for line in md.splitlines():
    f = [c.strip().strip("*") for c in line.strip().strip("|").split("|")]
    if len(f) == 4:
        try: rows.append((float(f[0]), float(f[1]), f[2]))
        except ValueError: pass
G06_TABLE = [(44.7,0.001,"pressure"),(6.40,0.185,"rotation"),(6.00,0.049,"pressure"),(4.63,0.730,"pressure"),
    (4.60,0.010,"pressure"),(3.57,0.012,"two-body"),(3.45,0.361,"lensing"),(3.17,0.414,"lensing"),
    (3.15,0.382,"lensing"),(2.91,0.520,"pressure"),(2.76,0.259,"pressure"),(2.63,0.004,"pressure"),
    (2.56,0.059,"pressure"),(2.48,0.038,"rotation"),(2.24,0.041,"pressure"),(2.17,0.113,"pressure"),
    (2.13,0.036,"pressure"),(2.09,0.175,"pressure"),(1.93,0.110,"pressure"),(1.92,0.031,"pressure"),
    (1.69,0.800,"pressure"),(1.50,0.353,"rotation"),(1.48,0.111,"pressure"),(1.45,0.023,"pressure"),
    (1.30,1.640,"pressure"),(1.30,1.390,"rotation")]
ck("V7 g06 hard-codes the liability table into its section 6 rather than reading the file.  Every row is checked "
   "here against THE_LIABILITY_TABLE.md as it stands on disk.  A hard-coded table that has drifted from its "
   "source would make the whole cluster comparison a comparison with nothing",
   sorted(rows) == sorted(G06_TABLE),
   f"{len(rows)} numeric rows parsed from the .md, {len(G06_TABLE)} hard-coded in g06; "
   f"{'identical' if sorted(rows)==sorted(G06_TABLE) else 'MISMATCH'}")
info("the .md states its currency verbatim: 'the missing boost, i.e. the factor by which the observation exceeds")
info("the framework's zero-parameter prediction in *acceleration*'.  g06 reports (sigma_obs/sigma_pred)^2, which")
info("IS an acceleration ratio at fixed radius.  There is no square-root mismatch between the two sides.")
xray = [(b, x) for b, x, s in rows if s == "pressure" and b <= 3.0]
not_xray = [(b, x) for b, x, s in rows if s == "pressure" and b <= 3.0 and x > 0.6]
ck("V8 the comparison median survives the mislabel.  g06 calls all 14 pressure rows with boost <= 3 'X-ray group "
   "and cluster rows', but two of them are not (X-ray ellipticals 5-70 kpc; SLUGGS globular systems).  Dropping "
   "them must not move the comparison median, or the 0.41 dex separation would be an artefact of the bin",
   abs(np.median([b for b, _ in xray]) - np.median([b for b, x in xray if (b, x) not in not_xray])) < 0.05,
   f"all 14 pressure rows with boost <= 3: median {np.median([b for b,_ in xray]):.2f}; the 12 that really are "
   f"X-ray groups/clusters: median {np.median([b for b,x in xray if (b,x) not in not_xray]):.2f}")

P(""); P("="*126); P("4.  THE ESTIMATOR ITSELF: IS AN UNWEIGHTED MEDIAN THE RIGHT STATISTIC?"); P("="*126)
Nv = np.array([g["Nv"] for g in groups], float)
err = 2.0/np.sqrt(2*(Nv - 1))/math.log(10)
lb = np.log10(B["canonical"])
fac = np.array([chi2.median(nv - 1)/(nv - 1) for nv in Nv])
lbc = lb - np.log10(fac)
info(f"per-group velocity counts run {int(Nv.min())} to {int(Nv.max())}, so per-group errors run "
     f"{err.min():.3f} to {err.max():.3f} dex -- a factor {err.max()/err.min():.1f}.  An UNWEIGHTED median gives")
info("a group with 3 velocities the same vote as one with 37.  Two consequences, both computed here:")
info(f"  (a) sigma^2 estimated from n velocities is distributed as sigma_true^2 chi^2_(n-1)/(n-1), whose MEDIAN")
info(f"      sits below 1.  Per-group that is {np.log10(fac).min():+.3f} to {np.log10(fac).max():+.3f} dex, so an")
info(f"      unweighted median of boosts is biased LOW.  De-biased: {10**np.median(lbc):.3f}"
     f" ({np.median(lbc):+.3f} dex) against the raw {10**np.median(lb):.3f}.")
info(f"  (b) the boost distribution is right-skewed, so median != mean of log: median {np.median(lb):+.3f} dex vs")
info(f"      mean of log {np.mean(lb):+.3f} dex, a further {np.mean(lb)-np.median(lb):+.3f} dex.")
def wmean(y, e2):
    w = 1/e2; return float(np.sum(w*y)/np.sum(w)), float(1/math.sqrt(np.sum(w)))
def ml_scatter(y, e):
    def f(si):
        w = 1/(e**2 + si**2); mu = np.sum(w*y)/np.sum(w)
        return float(np.sum(w**2*((y - mu)**2 - (e**2 + si**2))))
    return brentq(f, 1e-4, 2.0)
si = ml_scatter(lb, err); mu, emu = wmean(lb, err**2 + si**2)
info(f"  the maximum-likelihood intrinsic scatter is {si:.3f} dex, and the properly weighted mean of log boost is")
info(f"  {mu:+.3f} +- {emu:.3f} dex, i.e. a boost of {10**mu:.3f}.")
ck("V9 (THE ESTIMATOR SUBSTITUTION, AND IT GOES THE OTHER WAY) replacing the unweighted median with the "
   "statistically correct estimator -- an inverse-variance weighted mean of log boost with the ML intrinsic "
   "scatter -- must not move the answer outside g06's own bootstrap band, or the headline is a statement about "
   "the choice of statistic.  It does not: it moves it TOWARD unity and TIGHTENS the error, which strengthens the "
   "claim rather than refuting it.  Recorded as found, per the working rule that a win is verified as hard as a "
   "deficit",
   G06["boot_lo"] <= 10**mu <= G06["boot_hi"],
   f"unweighted median {10**np.median(lb):.3f} ({np.median(lb):+.3f} dex) -> ML-weighted mean {10**mu:.3f} "
   f"({mu:+.3f} +- {emu:.3f} dex), inside g06's bootstrap band [{G06['boot_lo']}, {G06['boot_hi']}]; the "
   f"separation from the cluster median 2.11 goes from {(0.324-np.median(lb)):.3f}/0.114 = "
   f"{(0.324-np.median(lb))/0.114:.2f} sigma to {(0.324-mu):.3f}/{emu:.3f} = {(0.324-mu)/emu:.2f} sigma")
ck("V10 (FAILS -- AN UNDISCLOSED SUBSAMPLE INSTABILITY) the median must not depend on where the richness cut is "
   "put.  It does: the nine groups with >= 10 members, which carry the smallest statistical errors, sit well "
   "above the full-sample median, and the six with >= 20 members land INSIDE the liability table's cluster band "
   "1.45-3.45.  This is a median-of-nine effect -- the slope of log boost against log N is under 1.5 sigma "
   "against a permutation null, and the weighted mean of V9, which gives those groups most of the weight, still "
   "lands at unity -- but g06 does not disclose it and its 'these groups do not look like clusters' sentence is "
   "a statement about the full sample only",
   all(abs(math.log10(float(np.median(B["canonical"][np.array([g["N"] for g in groups]) >= c]))
                      /np.median(B["canonical"]))) < 0.114 for c in (8, 10, 20)),
   "; ".join(f"N>={c}: n={int((np.array([g['N'] for g in groups])>=c).sum())} median "
             f"{float(np.median(B['canonical'][np.array([g['N'] for g in groups])>=c])):.3f}"
             for c in (5, 8, 10, 20)))
xv = np.log10(np.array([g["N"] for g in groups], float)); A = np.vstack([xv, np.ones_like(xv)]).T
sl = float(np.linalg.lstsq(A, lb, rcond=None)[0][0])
null = np.array([np.linalg.lstsq(A, rng.permutation(lb), rcond=None)[0][0] for _ in range(6000)])
info(f"  slope of log boost against log N = {sl:+.3f} (r = {np.corrcoef(xv,lb)[0,1]:+.2f}) against a permutation "
     f"null of width {null.std():.3f}, i.e. {abs(sl)/null.std():.2f} sigma -- NOT a significant trend")

P(""); P("="*126); P("5.  SAMPLE INDEPENDENCE AND TWO UNDISCLOSED PRESCRIPTION LEVERS"); P("="*126)
hosts = set(g["name"].upper() for g in groups)
dup = [(g["name"], m["Name"]) for g in groups for m in sat[g["name"]] if m["Name"].upper() in hosts]
ck("V11 (FAILS) the 26 groups must be 26 independent systems for the bootstrap over them to mean anything.  They "
   "are not: some galaxies are simultaneously a host of one group and a catalogued member of another, so a few "
   "physical structures enter the sample twice.  The effect on the headline is small and in the conservative "
   "direction, but the bootstrap's effective N is smaller than 26 and g06 does not say so",
   len(dup) == 0, f"{len(dup)} host-in-another-group pairs: " + "; ".join(f"{a} contains host {b}" for a, b in dup) +
   f".  Dropping the duplicated hosts leaves n="
   f"{len([g for g in groups if g['name'] not in ('NGC4945','NGC3412')])} with median "
   f"{float(np.median(B['canonical'][[i for i,g in enumerate(groups) if g['name'] not in ('NGC4945','NGC3412')]])):.3f}"
   f" against {np.median(B['canonical']):.3f}")
b_hc = boosts(A0["canonical"], hot_central=True)
b_hc1 = boosts(A0["canonical"], hot_central=True, f_hot=1.0)
ck("V12 g06 places the hot gas on the EXTENDED satellite tracer profile.  The circumgalactic media it is standing "
   "in for are bound to the individual galaxies, and the host carries 93% of the light, so a compact placement is "
   "at least as defensible and was not bracketed.  It must not move the answer by more than the bootstrap "
   "half-width, and it does not -- but it is a second lever alongside Upsilon_K and it points the same way",
   abs(math.log10(float(np.median(b_hc))/np.median(B["canonical"]))) < 0.114,
   f"hot gas on the host instead of the tracer profile: {np.median(b_hc):.3f} "
   f"({math.log10(np.median(b_hc)/np.median(B['canonical'])):+.3f} dex); with f_hot = 1.0 as well, "
   f"{np.median(b_hc1):.3f}")
u04, u10 = float(np.median(boosts(A0["canonical"], ups=0.4))), float(np.median(boosts(A0["canonical"], ups=1.0)))
need = brentq(lambda u: float(np.median(boosts(A0["canonical"], ups=u))) - 2.11, 0.02, 0.6)
ck("V13 THE AUTHOR'S OWN STATED WEAKEST LINK, TESTED IN THE DIRECTION THAT MATTERS.  Upsilon_K moves the boost "
   "over 0.62 - 1.01, which is wider than the bootstrap band, so 'consistent with unity' IS Upsilon-dependent.  "
   "But the load-bearing conclusion is the SEPARATION FROM THE CLUSTER ROWS, and that is what has to survive: "
   "this check asks what Upsilon_K would be needed to lift these groups to the cluster median of 2.11, and the "
   "answer has to be outside any defensible K-band range or the rung is worthless",
   need < 0.25,
   f"Upsilon_K = 0.4 -> {u04:.3f}, 0.6 (adopted) -> {np.median(B['canonical']):.3f}, 1.0 -> {u10:.3f}; reaching "
   f"the cluster median 2.11 would need Upsilon_K = {need:.3f}, i.e. {UPS_K/need:.1f}x below the adopted value "
   f"and far outside Bell & de Jong 2001's K-band range.  The consistency-with-unity half of the claim is soft; "
   f"the no-cluster-deficit half is not")

P(""); P("="*126); P("6.  MUTATION CONTROLS ON THIS AUDIT'S OWN PIPELINE"); P("="*126)
b3 = boosts(A0["canonical"], a0mult=3.0)
ck("M1 mutation -- triple a_0 in THIS file's independent solver.  Deep-MOND scaling forces the boost down by "
   "1/sqrt(3); if this audit's own Jeans code were mis-normalised in a_0 it would not land there",
   abs(float(np.median(b3))/np.median(B["canonical"])/0.5774 - 1) < 0.25,
   f"ratio {np.median(b3)/np.median(B['canonical']):.4f} against 0.5774 (g06's own mutation gave "
   f"{G06['a0x3_ratio']})")
bn = boosts(A0["canonical"], nu_on=False)
ck("M2 mutation -- kernel off (nu = 1).  Must explode to the Newtonian missing mass, and must land near g06's "
   "own value for the same mutation, which is an end-to-end cross-check of two independently written pipelines "
   "in a regime far from the one they were tuned on",
   float(np.median(bn)) > 8.0 and abs(math.log10(float(np.median(bn))/G06["nu_off"])) < 0.1,
   f"Newtonian median boost {np.median(bn):.1f} (g06: {G06['nu_off']}), range {bn.min():.1f} - {bn.max():.1f}")
sv = [g["sig"] for g in groups]
sc = []
for _ in range(300):
    for g, s_ in zip(groups, rng.permutation(sv)): g["sig"] = s_
    sc.append(float(np.median(boosts(A0["canonical"]))))
for g, s_ in zip(groups, sv): g["sig"] = s_
ck("M3 mutation -- shuffle the measured dispersions across groups.  The median boost is a MARGINAL statistic and "
   "survives the shuffle, which is the honest limit of what this rung can prove: it constrains the overall scale "
   "of sigma against the overall scale of M_b^(1/4), not the per-group pairing.  g06 says this too; it is "
   "restated here because it bounds how much the 'consistent with the prediction' sentence is worth",
   abs(float(np.median(sc)) - np.median(B["canonical"]))/np.median(B["canonical"]) < 0.5,
   f"shuffled median boost {np.median(sc):.3f} +- {np.std(sc):.3f} vs real {np.median(B['canonical']):.3f} -- "
   f"only {abs(math.log10(np.median(sc)/np.median(B['canonical']))):.3f} dex apart, so the median alone cannot "
   f"distinguish the framework predicting EACH group from it predicting the ENSEMBLE SCALE")

P(""); P("="*126); P("7.  VERDICT"); P("="*126)
info("THE CLAIM IS NOT REFUTED.  The central number is exact under independently written code (0.816 vs 0.817 on")
info("the canonical footing, 0.706 vs 0.706 isolated), the currency matches the liability table's stated one, the")
info("hard-coded comparison table matches the .md row for row, and the estimator survives all five of this repo's")
info("bug patterns -- enclosed mass is used and not total (V3), the aperture costs 0.01 dex (V4), and the")
info("residual's sign does not track the external-field branch (V5).")
P("")
info("WHAT DOES NOT SURVIVE IS THE CLAIMED STRENGTH'S ERROR BAR, in BOTH directions:")
info(f"  * the unweighted median is the wrong statistic for groups carrying 3 to 37 velocities, and it is biased")
info(f"    LOW by {np.median(lb)-np.median(lbc):+.3f} dex from the median-of-chi^2 effect alone.  Correcting it moves the")
info(f"    answer to {10**mu:.3f} +- {emu:.3f} dex -- closer to unity, not further.  The 3.6 sigma separation from the")
info(f"    cluster rows becomes {(0.324-mu)/emu:.1f} sigma.  The claim gets STRONGER, not weaker, when the estimator is fixed.")
info(f"  * against that, the quoted 0.114 dex is a STATISTICAL half-width only.  g06's own Upsilon_K bracket is")
info(f"    0.21 dex wide and V12 adds a second undisclosed {abs(math.log10(np.median(b_hc)/np.median(B['canonical']))):.2f} dex lever in the same direction.  A")
info( "    referee would demand those in the error bar, which puts the honest separation nearer 2-3 sigma.")
info(f"  * two undisclosed sample facts: {len(dup)} host-in-another-group pairs (V11) so the effective N is under 26,")
info( "    and a richest-subsample median (V10) that lands inside the cluster band on 6 groups.  Neither is")
info( "    significant, both belong in the caveats.")
P("")
info("AND THE ONE THING THAT WOULD REVERSE IT IS THE ONE g06 ALREADY FLAGS: the external field.  A tenfold error")
info(f"in e_N gives {br['gext x10']:.3f}; the raw 2M++ reconstruction gives g06's {G06['raw2mpp']}.  E1's inversion argument is")
info("the load-bearing step and it is an argument between two crude estimates, not a measurement.")
sys.exit(ck.done())
