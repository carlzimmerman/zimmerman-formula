#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG56 -- CFG40 REDONE WITH THE BULGE: the most massive star-forming disks (Ogle+2019) under B's law, with Simard+2011's bulge-to-total ratios.

WHY.  An independent referee reproduced CFG40 (mean +0.107, nine fastest +0.170, slope +0.194 with the exponential-disc model) and found its marginal fail depends on the baryon
structure model: with a point mass the nine fastest are +0.113 (which passes), with the spherical enclosed mass +0.201.  CFG40 put ALL the baryons in an exponential disc; massive spirals
have bulges, which move g_N toward the point-mass value.  Simard et al. 2011 (ApJS 196, 11; real_research/data/simard2011_ogle_bulge_disc.tsv, fetched with the owner's approval; every
galaxy matched one row and reproduces Ogle's R_d and inclination) give the r-band bulge-to-total ratio B/T (0.04-0.46, median 0.26) from the SAME fits Ogle used.

FROZEN BEFORE THE FIRST RUN.  CFG40's method, hypotheses, thresholds and error model exactly (read CFG40_README.md), with ONE change: the baryon structure.  Baryons: the stars M_* split into a
bulge (fraction B/T_r, a Hernquist sphere with scale a = R_e,bulge / 1.8153, the de Vaucouleurs-matched value; R_e from Simard) and an exponential disc (fraction 1 - B/T_r, R_d from Simard);
the gas M_gas in the disc.  g_N = g_disc(Freeman) + g_bulge(Hernquist enclosed mass) at the tabulated radius.  The law g = nu_mono(g_N/a0) g_N; the rule as CFG40.  B/T is a LIGHT fraction in r; the mass
fraction of a redder bulge in the W1 mass is larger, so a floor brackets it: B/T_mass = B/T_r + 0.10 (upper) and B/T_r - 0.10 (lower, clipped at 0) enter the model floor (half the range of the mean),
together with CFG40's M_* (+-0.2 dex) and gas (+-0.3 dex) terms.  Headline model: B/T_r.
  C1  CONTROL  the Simard rows match Ogle's R_d and inclination for all 23 (data file check), and with B/T = 0 the bulge+disc model reproduces CFG40's Freeman mean offset (+0.107 canonical) to 1e-6.
  H1  THE BARE LAW FITS THEM: |mean log(v_obs/v_law)| < 2 sigma, canonical.
  H2  [HEADLINE; MUTATE must fail] B fits: |mean| < 2 sigma AND |slope against log M_b| < 2 sigma AND the nine fastest (v > 340) |mean| < 2 sigma (canonical).
  R1-R3 (reported): CFG40's three earlier models on the same statistic; the alt footing; the offset against B/T and r/R_d.
  READING (declared): H2 PASS -> with the bulge the marginal CFG40 fail disappears and B holds through the top of the disk mass function.  H2 FAIL -> the fail survives the bulge.
MUTATE=1: the observed speeds multiplied by 0.5 -- H2 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG56_super_spirals_bulge.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib
import numpy as np
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG56_super_spirals_bulge", MUTATE)
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

SIM = {l.split("\t")[0]: l.rstrip("\n").split("\t") for l in open(os.path.join(C.REPO, "real_research", "data", "simard2011_ogle_bulge_disc.tsv")) if l.strip() and not l.startswith("#")}
for g in GALS:
    x = SIM[g["name"]]; g["BT"] = float(x[3]); g["Reb"] = float(x[8]); g["Rd_s"] = float(x[5]); g["i_s"] = float(x[7])
R.banner("C1  CONTROL: the table")
big = [g for g in GALS if g["name"] == "2MASX J15154614+0235564"][0]
ssfr = [g["lSFR"] - g["lMs"] for g in GALS]
check("C1 CONTROL: 23 galaxies; 2MASX J15154614+0235564 at 568 +- 16 km/s at 41 kpc; every sSFR > 1e-11 / yr",
      f"{len(GALS)} galaxies; the big one: {big['v'] / VF:.0f} +- {big['dv'] / VF:.0f} at {big['r']:.0f} kpc; min log sSFR {min(ssfr):.2f}",
      len(GALS) == 23 and big["v"] / VF == 568 and big["dv"] / VF == 16 and big["r"] == 41 and min(ssfr) > -11)


def gN_disc(Mb, Rd, r, model="freeman"):
    """Newtonian field at r [kpc] (m/s^2) of M_b [Msun] in an exponential disc of scale length Rd [kpc] (CFG40's three models)."""
    if model == "point":
        return G_ * Mb * MSUN / (r * KPC) ** 2
    if model == "sphere":
        return G_ * Mb * (1 - (1 + r / Rd) * math.exp(-r / Rd)) * MSUN / (r * KPC) ** 2
    y = r / (2 * Rd)
    v2 = 2 * G_ * Mb * MSUN / (Rd * KPC) * y * y * (i0(y) * k0(y) - i1(y) * k1(y))
    return v2 / (r * KPC)


def gN_bd(Ms, Mg, Rd, r, bt, Reb):
    """bulge (Hernquist, a = R_e/1.8153, mass bt Ms) + exponential disc ((1 - bt) Ms + Mg); the field in the plane (m/s^2)."""
    a = Reb / 1.8153
    gb = G_ * bt * Ms * MSUN * (1.0 / (r + a) ** 2) / KPC ** 2 if bt > 0 else 0.0
    return gb + gN_disc((1 - bt) * Ms + Mg, Rd, r, "freeman")


R.banner("C2  CONTROL: the Freeman field")
far = gN_disc(1e11, 5.0, 250.0) * (250.0 * KPC) ** 2 / (G_ * 1e11 * MSUN)
grid = np.linspace(0.5, 5, 451); vv = [gN_disc(1e11, 1.0, x) * x for x in grid]
check("C2 CONTROL: at r = 50 R_d the disc's g_N r^2 / (G M_b) = 1 within 1%; the v_N peak sits at r ~ 2.2 R_d",
      f"g_N r^2/(G M) = {far:.4f}; peak at {grid[int(np.argmax(vv))]:.2f} R_d", abs(far - 1) < 0.01 and abs(grid[int(np.argmax(vv))] - 2.2) < 0.1)


def pred(g, foot, model="bd", which="rule", colour=None, dMs=0.0, dMg=0.0, sig=0.0, dbt=0.0):
    a0 = A0SI[foot]
    Ms = 10 ** (g["lMs"] + dMs); Mg = 10 ** (g["lMg"] + dMg); Mb = Ms + Mg
    bt = min(max(g["BT"] + dbt, 0.0), 1.0)
    gn = gN_bd(Ms, Mg, g["Rd"], g["r"], bt, g["Reb"]) if model == "bd" else gN_disc(Mb, g["Rd"], g["r"], model)
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


R.banner("C1b  CONTROL: B/T = 0 reproduces CFG40")
import json as _json
_c40 = _json.load(open(os.path.join(HERE, "CFG40_super_spirals_results.json")))["numbers"]["RES"]["canonical|law"]["mean"]
_m0 = float(np.mean([math.log10(g["v"] / pred(g, "canonical", which="law", dbt=-1.0)[0]) for g in GALS]))
_match = all(abs(g["Rd_s"] - g["Rd"]) < 0.06 and abs(g["i_s"] - g["i"]) < 0.5 for g in GALS)
check("C1b CONTROL: every Simard row reproduces Ogle's R_d and inclination; with B/T = 0 the bulge+disc model reproduces CFG40's Freeman mean offset to 1e-6",
      f"R_d/i match for all 23: {_match}; mean with B/T = 0: {_m0:+.6f} against CFG40 {_c40:+.6f}" + (" [MUTATE: v x 0.5, so not compared]" if MUTATE else ""),
      _match and (MUTATE or abs(_m0 - _c40) < 1e-6))


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
    mods = [stat(foot, which, dbt=d, **kw)["mean"] for d in (-0.10, 0.0, +0.10)]
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
