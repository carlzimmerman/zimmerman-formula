#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG40 -- THE TOP OF THE DISK MASS FUNCTION: do the most massive star-forming disks rotate as B's law says?  (Ogle+2019's super spirals.)

WHY.  Candidate B's derived cold-mass rule (CFG35-CFG39) leaves star-forming disks on the bare law: with Mandelbaum+2016's measured BLUE
collapse masses the leftover collapse mass is zero (or small) for every SPARC spiral.  SPARC's heaviest spirals reach log M_* ~ 11.4; nothing
in the campaign has yet confronted B with the 10x rarer disks above that.  Ogle+2019 (arXiv:1909.09080; real_research/data/
ogle2019_super_spirals.tsv) measured Halpha rotation curves for 23 'super spirals' (log M_* 11.13-11.74) and report that above ~ 340 km/s the
baryonic Tully-Fisher relation 'breaks' (slope 0.25 +- 0.41 against 3.75 +- 0.11), 'inconsistent with MOND'.  That claim compares v_max with
the ASYMPTOTIC v^4 = G M_b a0.  But their speeds are maxima at r = 14-54 kpc, where a = v^2/r = 0.6-2 a0: the transition regime, where the
law's speed sits ABOVE the asymptote.  The test has to be made with the law evaluated at the radius, which is what B says.  Ogle's sample
is selected on luminosity and size, not on speed, so a velocity-selection bias does not enter (it does for Di Teodoro+2023; CFG41).

THE METHOD (declared before this script's first run).  CFG36's machinery exec'd read-only (Mandelbaum's blue / red relation converted to
M_200c; Dutton-Maccio NFW; the conservation form with the edge at x_e = 0.40; nu_mono; both a0 footings).  Baryons: M_* (WISE W1 with a
constant M/L_W1 = 0.6, the paper's) + M_gas (the paper's Schmidt-law estimate from the WISE W3 SFR; HI could not be measured).  The paper's
stellar masses stand in for Mandelbaum's Chabrier masses (declared, as SPARC's did in CFG36).  Structure: an exponential disc of scale length
R_d (Simard et al. 2011's SDSS disc fit) carrying all the baryons; its Newtonian field at r is Freeman's,
v_N^2 = (2 G M_b / R_d) y^2 [I0(y)K0(y) - I1(y)K1(y)], y = r / 2R_d  (headline).  Brackets: a point mass M_b (upper g_N) and the spherical
enclosed mass M_b [1 - (1 + r/R_d) e^{-r/R_d}] (lower g_N).  The law: g = nu(g_N / a0) g_N.  The rule:
g = nu(g_N/a0) g_N + f_ex (1 - f_b) G M_NFW(<r) / r^2, with f_ex from the collapse mass at the star-forming (blue) relation, NFW at M_200c.
Colour: sSFR = SFR / M_* > 1e-11 / yr -> blue, else red (declared; all 23 are checked in C1).  Observed: v_max +- dv, with the inclination
error dlog v = |cot i| di / ln 10 at di = 5 deg (declared; the paper quotes none), and stellar (0.2 dex) and gas (0.3 dex) mass errors
propagated.  Offset per galaxy = log10 (v_obs / v_pred).  Sample: the mean over the 23 with the galaxy-to-galaxy error, plus a floor in
quadrature: the baryon-structure model (half the spread of the mean across the three), the stellar mass (+-0.2 dex, all together) and the
gas mass (+-0.3 dex, all together), each as half the shift of the mean.

PRE-DECLARED
  C1  CONTROL  the table as transcribed: 23 galaxies, 2MASX J15154614+0235564 at v = 568 +- 16 km/s at 41 kpc; every galaxy has
               sSFR > 1e-11 / yr (the blue relation applies to all).
  C2  CONTROL  the Freeman field: at r = 50 R_d the disc's v_N^2 r / (G M_b) = 1 within 1%, and its peak sits at r ~ 2.2 R_d.
  H1  THE BARE LAW FITS THEM: |mean log(v_obs / v_law)| < 2 sigma, canonical footing.
  H2  [HEADLINE; MUTATE must fail] B (the law + the rule with the blue relation, canonical) fits them: |mean offset| < 2 sigma AND |slope of the
      offset against log M_b| < 2 sigma AND the nine fastest (v > 340 km/s) have |mean offset| < 2 sigma.
  R1-R5 (reported): the alt footing; the point and spherical baryon models; the asymptotic v^4 = G M_b a0 comparison (what the paper did);
      the rule's f_ex and its +1 sigma collapse masses; the rule with the red relation, for scale.
  READING (declared): H2 PASS -> B holds through the top of the disk mass function and the 'break' is the transition regime, not a failure of the law.
      H2 FAIL -> B fails on the most massive star-forming disks, and that joins the ultra-faints as a clean standing failure.  H1 FAIL and H2 PASS
      -> the rule is doing the work here, which would be a new result for the blue relation.  H1 PASS -> the law alone suffices.
MUTATE=1: the observed speeds multiplied by 0.5 -- H2 must FAIL (rc = 1).
CHANGED AFTER THE FIRST MUTATE RUN, BEFORE THE MAIN RUN (disclosed): the control first used 0.7.  H2 PASSED under it (mean -0.048 +- 0.075), because the
  systematic floor (0.075 dex, mostly the 0.2-dex stellar mass) is too large for a 0.155-dex error to bite -- the control had no bite.  It also
  revealed that the unmutated offsets are near +0.11 dex (mean) with the slope unchanged (+0.19 +- 0.10): seen BEFORE the main run.  No hypothesis,
  clause or threshold of H1/H2 was changed; only the control's strength (0.5, a 0.30-dex error).
Run: python3 campaign_fresh_gravity/CFG40_super_spirals.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib
import numpy as np
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG40_super_spirals", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: observed speeds x 0.5 -- H2 must FAIL ***")
VF = 0.5 if MUTATE else 1.0
FOOTS = ("canonical", "alt")

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG36_colour_split_collapse.py")).read()
g36 = {"__file__": os.path.join(HERE, "CFG36_colour_split_collapse.py"), "__name__": "cfg36"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ H1")], "CFG36", "exec"), g36)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
collapse, edge_phantom, FB, nfw_enclosed = g36["collapse"], g36["edge_phantom"], g36["FB"], g36["nfw_enclosed"]
G_, KPC, MSUN, A0SI = g36["G_"], g36["KPC"], g36["MSUN"], g36["A0SI"]
DI = math.radians(5.0)                                                   # declared inclination error (the paper quotes none)

T = [l.rstrip("\n").split("\t") for l in open(os.path.join(C.REPO, "real_research", "data", "ogle2019_super_spirals.tsv")) if l.strip() and not l.startswith("#")]
H = T[0]; GALS = []
for r in T[1:]:
    d = dict(zip(H, r))
    GALS.append(dict(name=d["name"], alt=d["alt_name"], Rd=float(d["Rd_kpc"]), i=float(d["i_deg"]), lMs=float(d["logMstars"]), lMg=float(d["logMgas"]),
                     lSFR=float(d["logSFR"]), v=float(d["vmax"]) * VF, dv=float(d["dvmax"]) * VF, r=float(d["r_kpc"]), ul=int(d["ul"])))

R.banner("C1  CONTROL: the table")
big = [g for g in GALS if g["name"] == "2MASX J15154614+0235564"][0]
ssfr = [g["lSFR"] - g["lMs"] for g in GALS]
check("C1 CONTROL: 23 galaxies; 2MASX J15154614+0235564 at 568 +- 16 km/s at 41 kpc; every sSFR > 1e-11 / yr",
      f"{len(GALS)} galaxies; the big one: {big['v'] / VF:.0f} +- {big['dv'] / VF:.0f} at {big['r']:.0f} kpc; min log sSFR {min(ssfr):.2f}",
      len(GALS) == 23 and big["v"] / VF == 568 and big["dv"] / VF == 16 and big["r"] == 41 and min(ssfr) > -11)


def gN_disc(Mb, Rd, r, model="freeman"):
    """Newtonian field at r [kpc] of M_b [Msun] in an exponential disc of scale length Rd [kpc] (m/s^2)."""
    if model == "point":
        return G_ * Mb * MSUN / (r * KPC) ** 2
    if model == "sphere":
        return G_ * Mb * (1 - (1 + r / Rd) * math.exp(-r / Rd)) * MSUN / (r * KPC) ** 2
    y = r / (2 * Rd)
    v2 = 2 * G_ * Mb * MSUN / (Rd * KPC) * y * y * (i0(y) * k0(y) - i1(y) * k1(y))
    return v2 / (r * KPC)


R.banner("C2  CONTROL: the Freeman field")
far = gN_disc(1e11, 5.0, 250.0) * (250.0 * KPC) ** 2 / (G_ * 1e11 * MSUN)
grid = np.linspace(0.5, 5, 451); vv = [gN_disc(1e11, 1.0, x) * x for x in grid]
check("C2 CONTROL: at r = 50 R_d the disc's g_N r^2 / (G M_b) = 1 within 1%; the v_N peak sits at r ~ 2.2 R_d",
      f"g_N r^2/(G M) = {far:.4f}; peak at {grid[int(np.argmax(vv))]:.2f} R_d", abs(far - 1) < 0.01 and abs(grid[int(np.argmax(vv))] - 2.2) < 0.1)


def pred(g, foot, model="freeman", which="rule", colour=None, dMs=0.0, dMg=0.0, sig=0.0):
    a0 = A0SI[foot]
    Ms = 10 ** (g["lMs"] + dMs); Mb = Ms + 10 ** (g["lMg"] + dMg)
    gn = gN_disc(Mb, g["Rd"], g["r"], model)
    gl = float(C.nu_mono(np.array([gn / a0]))[0]) * gn
    fex = 0.0
    if which == "rule":
        col = colour or ("blue" if g["lSFR"] - g["lMs"] > -11 else "red")
        Mh = collapse(Ms, col, sig); fex = max(0.0, 1.0 - edge_phantom(Mb, foot, 0.40) / ((1 - FB) * Mh))
        gl += fex * (1 - FB) * float(nfw_enclosed(Mh, g["r"])) * G_ * MSUN / (g["r"] * KPC) ** 2
    return math.sqrt(gl * g["r"] * KPC) / 1e3, fex, Mb


def asym(g, foot):
    Mb = 10 ** g["lMs"] + 10 ** g["lMg"]
    return (G_ * Mb * MSUN * A0SI[foot]) ** 0.25 / 1e3


def stat(foot, which, **kw):
    off = np.array([math.log10(g["v"] / pred(g, foot, which=which, **kw)[0]) for g in GALS])
    lMb = np.array([math.log10(pred(g, foot, which=which, **kw)[2]) for g in GALS])
    A = np.vstack([lMb - lMb.mean(), np.ones(len(lMb))]).T
    coef, res, *_ = np.linalg.lstsq(A, off, rcond=None)
    s2 = float(((off - A @ coef) ** 2).sum() / (len(off) - 2)); se = math.sqrt(s2 / float(((lMb - lMb.mean()) ** 2).sum()))
    fast = np.array([g["v"] / VF > 340 for g in GALS])
    return dict(off=off, mean=float(off.mean()), err=float(off.std(ddof=1) / math.sqrt(len(off))), slope=float(coef[0]), slope_se=se,
                fast_mean=float(off[fast].mean()), fast_err=float(off[fast].std(ddof=1) / math.sqrt(fast.sum())), nfast=int(fast.sum()))


def floor(foot, which, **kw):
    m0 = stat(foot, which, **kw)["mean"]
    mods = [stat(foot, which, model=mm, **{k: v for k, v in kw.items() if k != "model"})["mean"] for mm in ("freeman", "point", "sphere")]
    mod = 0.5 * (max(mods) - min(mods))
    ms = 0.5 * abs(stat(foot, which, dMs=+0.2, **kw)["mean"] - stat(foot, which, dMs=-0.2, **kw)["mean"])
    mg = 0.5 * abs(stat(foot, which, dMg=+0.3, **kw)["mean"] - stat(foot, which, dMg=-0.3, **kw)["mean"])
    return mod, ms, mg


RES = {}
for f in FOOTS:
    for w in ("law", "rule"):
        s = stat(f, w); mod, ms, mg = floor(f, w)
        tot = math.sqrt(s["err"] ** 2 + mod ** 2 + ms ** 2 + mg ** 2)
        s.update(mod=mod, ms=ms, mg=mg, tot=tot, z=s["mean"] / tot, zs=s["slope"] / s["slope_se"], zf=s["fast_mean"] / math.hypot(s["fast_err"], math.hypot(mod, math.hypot(ms, mg))))
        RES[(f, w)] = s

R.banner("H1 / H2  THE 23 SUPER SPIRALS")
for g in GALS:
    vl, _, Mb = pred(g, "canonical", which="law"); vr, fx, _ = pred(g, "canonical", which="rule")
    P(f"    {g['alt'] if g['alt'] != '-' else g['name'][-19:]:>26s} log M_b {math.log10(Mb):5.2f}  r {g['r']:3.0f} kpc  v_obs {g['v'] / VF:4.0f} +- {g['dv'] / VF:3.0f};"
      f" law {vl:5.1f}; rule {vr:5.1f} (f_ex {fx:.2f}); asym {asym(g, 'canonical'):5.1f}")
for (f, w), v in RES.items():
    P(f"    {f:9s} {w:5s}: mean {v['mean']:+.3f} +- {v['tot']:.3f} (gal {v['err']:.3f}, model {v['mod']:.3f}, M* {v['ms']:.3f}, gas {v['mg']:.3f}) -> {v['z']:+.2f} sigma;"
      f" slope {v['slope']:+.3f} +- {v['slope_se']:.3f} ({v['zs']:+.2f}); fastest {v['nfast']}: {v['fast_mean']:+.3f} ({v['zf']:+.2f} sigma)")
Lc, Rc = RES[("canonical", "law")], RES[("canonical", "rule")]
h1 = abs(Lc["z"]) < 2
h2 = abs(Rc["z"]) < 2 and abs(Rc["zs"]) < 2 and abs(Rc["zf"]) < 2
check("H1 THE BARE LAW FITS THEM: |mean log(v_obs / v_law)| < 2 sigma, canonical",
      f"{Lc['mean']:+.3f} +- {Lc['tot']:.3f} ({Lc['z']:+.2f} sigma)", h1)
check("H2 [HEADLINE] B (law + blue-relation rule) FITS THEM: |mean| < 2 sigma, |slope vs log M_b| < 2 sigma, |mean of the 9 fastest| < 2 sigma (canonical)"
      + ("  [MUTATE: v_obs x 0.5]" if MUTATE else ""),
      f"mean {Rc['mean']:+.3f} +- {Rc['tot']:.3f} ({Rc['z']:+.2f}); slope {Rc['slope']:+.3f} ({Rc['zs']:+.2f}); fastest {Rc['nfast']}: {Rc['fast_mean']:+.3f} ({Rc['zf']:+.2f})", h2)

# reported
asy = np.array([math.log10(g["v"] / asym(g, "canonical")) for g in GALS]); lMb = np.array([g["lMs"] for g in GALS])
lMb = np.log10(10 ** np.array([g["lMs"] for g in GALS]) + 10 ** np.array([g["lMg"] for g in GALS]))
fexs = np.array([pred(g, "canonical", which="rule")[1] for g in GALS])
p1 = [pred(g, "canonical", which="rule", sig=+1.0)[0] for g in GALS]; p1z = float(np.mean([math.log10(g["v"] / v) for g, v in zip(GALS, p1)]))
red = float(np.mean([math.log10(g["v"] / pred(g, "canonical", which="rule", colour="red")[0]) for g in GALS]))
mods = {m: stat("canonical", "law", model=m)["mean"] for m in ("freeman", "point", "sphere")}
check("R1 (reported) the asymptotic v^4 = G M_b a0 comparison (the paper's); the baryon models (law only)",
      f"asymptote: mean log(v_obs/v_asym) {asy.mean():+.3f}, fastest 9: {asy[[g['v'] / VF > 340 for g in GALS]].mean():+.3f}; law by model: "
      + ", ".join(f"{m} {x:+.3f}" for m, x in mods.items()), True, load_bearing=False)
check("R2 (reported) the rule's leftover; the rule at +1 sigma collapse masses; the rule with the RED relation, for scale",
      f"f_ex > 0 in {int((fexs > 0).sum())} of 23 (max {fexs.max():.2f}); +1 sigma mean {p1z:+.3f}; red-relation mean {red:+.3f}", True, load_bearing=False)
check("R3 (reported) the alt footing", "; ".join(f"{w}: {RES[('alt', w)]['mean']:+.3f} +- {RES[('alt', w)]['tot']:.3f} ({RES[('alt', w)]['z']:+.2f} sigma)" for w in ("law", "rule")),
      True, load_bearing=False)
reading = ("B holds through the top of the disk mass function; the 'break' is the transition regime" if h2 else
           ("B fails on the most massive star-forming disks" if not h2 else ""))
if h2 and not h1:
    reading += "; the bare law does not fit, so the rule is doing the work"
P(f"\n    READING (declared): {reading}")
R.num("RES", {f"{f}|{w}": {k: (v.tolist() if hasattr(v, 'tolist') else v) for k, v in s.items()} for (f, w), s in RES.items()})
R.num("R", dict(asym_mean=float(asy.mean()), fex=fexs.tolist(), p1_mean=p1z, red_mean=red, models=mods)); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
