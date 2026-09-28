#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG37 -- THE PASSIVE-DISK TEST of B's derived cold-mass rule: do early-type galaxies with extended HI discs rotate as the law says,
or as the conservation rule with their (red) collapse masses says?

WHY.  CFG36: with measured colour-split collapse masses (Mandelbaum+2016) the conservation rule leaves every star-forming spiral on the
law, supplies about half of the X-ray ellipticals' missing mass, and predicts that PASSIVE galaxies with measured outer rotation
should rotate faster than the law -- SPARC's one S0 (UGC 2487) would be 0.14 dex too fast, and it is not.  One galaxy is not a test.
den Heijer+2015 (A&A 581, A98, Table 1; real_research/data/denheijer2015_etg_hi_tfr.tsv) measured the HI circular velocity at the
outermost point of the rotation curve (8-28 kpc, mean 15 kpc; 3.4-13.7 R_eff) for 16 ATLAS3D early types -- exactly the population.

THE METHOD (declared before this script's first run).  CFG36's machinery exec'd read-only (Mandelbaum's red relation converted to
M_200c; Dutton-Maccio NFW; the conservation form with the edge at x_e = 0.40).  Baryons: M_* = L_r x (M/L)_SFH (ATLAS3D's Salpeter
population M/L), plus 1.33 M_HI.  The collapse mass is looked up at the Chabrier-equivalent stellar mass (M_* x 10^-0.25, Mandelbaum's
convention).  At radius r: the law, v^2 = nu(G M_b / r^2 a0) G M_b / r (point mass: the stars are enclosed at 3-14 R_eff); the rule,
v^2 = [nu M_b + f_ex (1 - f_b) M_NFW(<r)] G / r.  The radius of each velocity is not tabulated: r = 15 kpc (the sample mean) is the
headline and 8 / 28 kpc bracket it.  Per galaxy the offset is log(v_obs / v_pred), with the velocity and inclination errors
(d log v = |cot i| di / ln 10).  Sample: the mean over the 16 with the galaxy-to-galaxy error, and a floor in quadrature: the IMF (Salpeter
vs Chabrier stellar masses) and the radius (8 vs 28 kpc), each as half the spread of the mean.

PRE-DECLARED
  C1  CONTROL  the table as transcribed: 16 galaxies; NGC 3941 at i = 57 deg, v_circ = 148 km/s (the paper's worked example).
  H1  THE LAW FITS THE PASSIVE DISKS: |mean log(v_obs / v_law)| < 2 sigma, both footings.
  H2  [HEADLINE; MUTATE must fail] THE CONSERVATION RULE WITH RED COLLAPSE MASSES OVER-PREDICTS THEM: mean log(v_obs / v_rule) < 0 at
      more than 2 sigma, both footings.
  R1-R3 (reported): per-galaxy offsets, f_ex and collapse masses; the dynamical (JAM) M/L instead of the population one; the rule with the
      BLUE relation, for scale.
  READING (declared): H1 PASS and H2 PASS -> passive disks follow the law and reject the rule's extra mass: B's derived conservation rule,
      with the measured red collapse masses, is falsified on the population CFG36 named, and B's cold sector still has no rule for massive
      passive systems that spares their disks.  H2 FAIL -> the passive disks do not reject the rule's extra mass.  H1 FAIL -> the passive
      disks do not follow the law either.
MUTATE=1: every collapse mass divided by 100 -- H2 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG37_passive_disks.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG37_passive_disks", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every collapse mass / 100 -- H2 must FAIL ***")
MCF = 0.01 if MUTATE else 1.0
FOOTS = ("canonical", "alt")

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG36_colour_split_collapse.py")).read()
g36 = {"__file__": os.path.join(HERE, "CFG36_colour_split_collapse.py"), "__name__": "cfg36"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ H1")], "CFG36", "exec"), g36)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
collapse, edge_phantom, FB, nfw_enclosed = g36["collapse"], g36["edge_phantom"], g36["FB"], g36["nfw_enclosed"]
G_, KPC, MSUN, A0SI = g36["G_"], g36["KPC"], g36["MSUN"], g36["A0SI"]

T = [l.rstrip("\n").split("\t") for l in open(os.path.join(C.REPO, "real_research", "data", "denheijer2015_etg_hi_tfr.tsv")) if l.strip() and not l.startswith("#")]
H = T[0]; GALS = []
for r in T[1:]:
    d = dict(zip(H, r))
    di = [abs(float(x)) for x in d["di_deg"].split(",")]
    GALS.append(dict(name=d["name"], i=float(d["i_deg"]), di=max(di), v=float(d["vcirc"]), dv=float(d["dv"]), MHI=10 ** float(d["logMHI"]),
                     Lr=10 ** float(d["logLr"]), ml_sfh=10 ** float(d["logML_SFH"]), ml_jam=10 ** float(d["logML_JAM"])))
R.banner("C1  CONTROL: the table")
n3941 = [g for g in GALS if g["name"] == "NGC3941"][0]
check("C1 CONTROL: 16 galaxies; NGC 3941 at i = 57 deg, v_circ = 148 km/s (the paper's worked example)",
      f"{len(GALS)} galaxies; NGC 3941 i = {n3941['i']:.0f}, v = {n3941['v']:.0f}", len(GALS) == 16 and n3941["i"] == 57 and n3941["v"] == 148)


def pred(g, foot, r_kpc=15.0, imf="salp", colour="red", ml="sfh"):
    a0 = A0SI[foot]
    Ms = g["Lr"] * (g["ml_sfh"] if ml == "sfh" else g["ml_jam"]) * (1.0 if imf == "salp" else 10 ** -0.25)
    Mb = Ms + 1.33 * g["MHI"]
    gb = G_ * Mb * MSUN / (r_kpc * KPC) ** 2
    Mlaw = float(C.nu_mono(np.array([gb / a0]))[0]) * Mb
    Mh = MCF * collapse(g["Lr"] * g["ml_sfh"] * 10 ** -0.25, colour)
    fex = max(0.0, 1.0 - edge_phantom(Mb, foot, 0.40) / ((1 - FB) * Mh))
    Mrule = Mlaw + fex * (1 - FB) * float(nfw_enclosed(Mh, r_kpc))
    v = lambda M: math.sqrt(G_ * M * MSUN / (r_kpc * KPC)) / 1e3
    return v(Mlaw), v(Mrule), fex, Mh


def stat(foot, which, **kw):
    off = np.array([math.log10(g["v"] / pred(g, foot, **kw)[0 if which == "law" else 1]) for g in GALS])
    return off, float(off.mean()), float(off.std(ddof=1) / math.sqrt(len(off)))


RES = {}
for f in FOOTS:
    for which in ("law", "rule"):
        off, m, e = stat(f, which)
        imf = abs(stat(f, which, imf="chab")[1] - m)
        rad = 0.5 * abs(stat(f, which, r_kpc=28.0)[1] - stat(f, which, r_kpc=8.0)[1])
        tot = math.sqrt(e ** 2 + imf ** 2 + rad ** 2)
        RES[(f, which)] = dict(mean=m, err=e, imf=imf, rad=rad, tot=tot, z=m / tot, per=off.tolist())
R.banner("H1 / H2  THE SIXTEEN PASSIVE DISKS")
for g in GALS:
    vl, vr, fx, mh = pred(g, "canonical")
    P(f"    {g['name']:8s} v_obs {g['v']:4.0f} +- {g['dv']:3.0f}; law {vl:5.1f}; rule {vr:5.1f} (f_ex {fx:.2f}, M200c {mh:.1e})")
for (f, w), v in RES.items():
    P(f"    {f:9s} {w:5s}: mean log(v_obs/v_pred) {v['mean']:+.3f} +- {v['tot']:.3f} (galaxies {v['err']:.3f}, IMF {v['imf']:.3f}, radius {v['rad']:.3f}) -> {v['z']:+.2f} sigma")
check("H1 THE LAW FITS THE PASSIVE DISKS: |mean log(v_obs/v_law)| < 2 sigma, both footings",
      "; ".join(f"{f}: {RES[(f, 'law')]['mean']:+.3f} ({RES[(f, 'law')]['z']:+.2f} sigma)" for f in FOOTS), all(abs(RES[(f, "law")]["z"]) < 2 for f in FOOTS))
check("H2 [HEADLINE] THE CONSERVATION RULE WITH RED COLLAPSE MASSES OVER-PREDICTS THEM: mean log(v_obs/v_rule) < 0 at > 2 sigma, both footings"
      + ("  [MUTATE: collapse masses / 100]" if MUTATE else ""),
      "; ".join(f"{f}: {RES[(f, 'rule')]['mean']:+.3f} ({RES[(f, 'rule')]['z']:+.2f} sigma)" for f in FOOTS), all(RES[(f, "rule")]["z"] < -2 for f in FOOTS))
jam = {w: stat("canonical", w, ml="jam")[1] for w in ("law", "rule")}
blue = stat("canonical", "rule", colour="blue")[1]
check("R1 (reported) the dynamical (JAM) M/L for the stars; the rule with the BLUE relation (canonical, r = 15 kpc)",
      f"JAM: law {jam['law']:+.3f}, rule {jam['rule']:+.3f}; blue-relation rule {blue:+.3f}", True, load_bearing=False)
h1 = all(abs(RES[(f, "law")]["z"]) < 2 for f in FOOTS); h2 = all(RES[(f, "rule")]["z"] < -2 for f in FOOTS)
reading = ("passive disks follow the law and reject the rule's extra mass: the derived conservation rule with measured red collapse masses is "
           "falsified on this population" if (h1 and h2) else ("the passive disks do not reject the rule's extra mass" if not h2 else
                                                                 "the passive disks do not follow the law either"))
P(f"\n    READING (declared): {reading}")
R.num("RES", {f"{f}|{w}": v for (f, w), v in RES.items()}); R.num("R1", dict(jam=jam, blue=blue)); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
