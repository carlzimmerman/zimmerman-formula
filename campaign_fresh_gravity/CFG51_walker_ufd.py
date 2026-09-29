#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG51 -- THE ULTRA-FAINT FAILURE WITH MULTI-EPOCH, BINARY-CLEANED DISPERSIONS (Walker+2023 Hectochelle/M2FS, reduced here).

WHY.  CFG28-CFG29 found B's ultra-faint failure robust to published binary bounds; CFG46 applied Arroyo-Polonio+2026's STATISTICAL binary correction to single-epoch
data (offset lowered 0.07-0.10 dex, test power lost on eight systems).  The decisive test is per-star MULTI-EPOCH data: stars whose velocity varies between epochs
are removed, and the dispersion is computed from the rest.  Walker et al. 2023 (ApJS 268, 19; VizieR J/ApJS/268/19; real_research/data/walker2023/, fetched with
the owner's approval) give per-epoch velocities for 16,369 stars in 38 systems, with up to 15 epochs per source.  CFG51/CFG51_walker_multiepoch/reduce_walker.py
reduces them (declared rules in its docstring) to dispersions: single-epoch, all-epoch mean, and binary-cleaned (stars with >= 2 epochs and chi^2 p < 0.01 removed).
Only TWO ultra-faints have enough multi-epoch coverage to be informative (n_multi >= 8 and >= half of the members): Bootes I (33 of 55 members multi-epoch, baseline
median 1900 d) and Tucana II (9 of 14, up to 15 epochs, baseline median 2500 d).  This lane scores B on those two.  It is a two-object test: no sample statistic.

CAVEATS DECLARED BEFORE THE RUN.  (i) The catalogue has no membership column; the reduction re-derives it (a velocity window of +-4 sigma_seed about the LVD systemic
velocity, logg < 4, Gaia PM and parallax), so it can remove large-excursion binaries BEFORE the cleaning step and bias sigma low; the count is in n_vreject (Bootes I 20).
(ii) Bootes I has two kinematic components in the literature (cold 2.4, hot 4.6 km/s, Koposov+2011) and the window keeps both; Arroyo-Polonio+2026's cold-only 2.18-2.55
is not comparable.  (iii) Tucana II is tidally disturbed in the literature (extended halo, velocity gradient); a gradient inflates a dispersion.  (iv) No wavelength
zero-point offset between epochs or instruments is modelled.

THE METHOD.  FG001's estimator (exec'd read-only): sigma^2 = g(r) r / 3 at r = (4/3) r_half, half of the baryons enclosed, Upsilon_V = 2, stars only, the isolated law
(nu_mono, both footings); M_V and r_half from the repo's LVD table.  Offset = log10(sigma_obs / sigma_law) for the single-epoch, all-epoch-mean and cleaned dispersions.
Per-system error: the reduction's asymmetric 1-sigma interval converted to dex, plus a floor in quadrature (half the range of the offset over Upsilon_V 1 to 4 and the
pure deep-MOND estimator).  The rule (CFG42's sum, Moster collapse mass clamped at 1e9) is reported.

PRE-DECLARED
  C1  CONTROL  the reduction is reproducible: the two informative systems' cleaned dispersions are 3.911 (Bootes I) and 4.064 km/s (Tucana II) and the repository's LVD
               literature values (4.0, 3.8) agree with the single-epoch ones to within 30%.
  H1  [HEADLINE; MUTATE must fail] the failure survives multi-epoch cleaning in both systems: the bare law's cleaned offset is positive at more than 2 sigma for
      Bootes I AND for Tucana II, on both footings.
  H2  the cleaning lowers but does not remove the offset: cleaned offset > 0 for both, and less than the single-epoch offset for both.
  R1  (reported) all three offsets per system; the rule; the paper-flag variant (Bootes I 3.95, Tucana II 3.45 km/s).
  READING (declared): H1 PASS -> in the two systems where multi-epoch cleaning is possible, the ultra-faint failure survives it at > 2 sigma each (two objects: not a
      population result).  H1 FAIL -> at least one system no longer shows a > 2 sigma failure.  Nothing here is a sample statistic.
MUTATE=1: every dispersion multiplied by 0.5 -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG51_walker_ufd.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
import hunt_lib as HL
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG51_walker_ufd", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every dispersion x 0.5 -- H1 must FAIL ***")
SF = 0.5 if MUTATE else 1.0
FOOTS = ("canonical", "alt")

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG36_colour_split_collapse.py")).read()
g36 = {"__file__": os.path.join(HERE, "CFG36_colour_split_collapse.py"), "__name__": "cfg36"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ H1")], "CFG36", "exec"), g36)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
edge_phantom, FB, nfw_enclosed = g36["edge_phantom"], g36["FB"], g36["nfw_enclosed"]
halo_mass = g36["g35"]["halo_mass"]
FGP = os.path.join(HERE, "CFG7_hierarchy_fg001.py")
ns = {"np": np, "math": math, "os": os, "csv": csv, "C": C, "HL": HL}
ns = C.C4.exec_slices(FGP, [("G, kpc, Msun, A0H = HL.G", "# ================================================================================================ K1 h43"),
                            ("MW_MB, M31_MB, UPS_V = 6.0e10", "REF43 = {")], ns=ns, name="fg001_slices")[0]
A0H, UPS_V, a_int, G, Msun, fnum = ns["A0H"], ns["UPS_V"], ns["a_int"], ns["G"], ns["Msun"], ns["fnum"]

W = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "CFG51_walker_multiepoch", "walker_reduced_dispersions.tsv")) if l.strip()]
WT = {r[0]: dict(zip(W[0], r)) for r in W[1:]}
LVD = {r["key"]: r for r in csv.DictReader(open(os.path.join(ns["DSPH"], "lvd_dwarf_mw.csv")))}
SYS = {"Bootes I": "Bootes_1", "Tucana II": "Tucana_2"}
GAL = []
for nm, wk in SYS.items():
    key = [k for k, r in LVD.items() if r["name"] == nm][0]; r = LVD[key]; t = WT[wk]
    MV = fnum(r["M_V"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); MHI = fnum(r["mass_HI"])
    f = lambda k: float(t[k])
    GAL.append(dict(name=nm, MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=(10 ** MHI if MHI is not None else 0.0), lit=fnum(r["vlos_sigma"]),
                    single=f("sigma_single"), single_p=f("plus_err_single"), single_m=f("minus_err_single"), allmean=f("sigma_allmean"),
                    clean=f("sigma_clean"), clean_p=f("plus_err_clean"), clean_m=f("minus_err_clean"), nmulti=int(t["n_multi"]), nmem=int(t["n_members"])))


def spred(g, foot, ups=None, deep=False, rule=False):
    a0 = A0H[foot]; ups = UPS_V if ups is None else ups
    Ms = ups * g["LV"]; Mb = Ms + 1.33 * g["MHI"]
    if deep:
        return (4.0 / 81.0 * G * Mb * Msun * a0) ** 0.25 / 1e3
    rh_pc = (4.0 / 3.0) * g["rh"]; rh = rh_pc * 3.0857e16
    gg = a_int(G * 0.5 * Mb * Msun / rh ** 2, 0.0, a0)
    if rule:
        Mh = float(halo_mass(UPS_V * g["LV"]))
        fex = max(0.0, 1.0 - edge_phantom(Mb, foot, 0.40) / ((1 - FB) * Mh))
        gg += G * fex * (1 - FB) * float(nfw_enclosed(Mh, rh_pc / 1000.0)) * Msun / rh ** 2
    return math.sqrt(gg * rh / 3.0) / 1e3


R.banner("C1  CONTROL")
bo, tu = GAL
check("C1 CONTROL: the reduction's cleaned dispersions are 3.911 (Bootes I) and 4.064 km/s (Tucana II); the LVD literature values agree with the single-epoch ones to 30%",
      f"Bootes I {bo['clean']:.3f} (single {bo['single']:.2f}, LVD {bo['lit']}); Tucana II {tu['clean']:.3f} (single {tu['single']:.2f}, LVD {tu['lit']})",
      abs(bo["clean"] - 3.911) < 5e-3 and abs(tu["clean"] - 4.064) < 5e-3 and abs(math.log(bo["single"] / bo["lit"])) < 0.3 and abs(math.log(tu["single"] / tu["lit"])) < 0.3)


def off(g, key, foot, **kw):
    return math.log10(SF * g[key] / spred(g, foot, **kw))


def err_dex(g, key, foot):
    p, m = (g["clean_p"], g["clean_m"]) if key == "clean" else (g["single_p"], g["single_m"])
    v = g[key]
    e = 0.5 * (math.log10(1 + p / v) + abs(math.log10(max(1 - m / v, 1e-3))))
    ofs = [off(g, key, foot, ups=u) for u in (1.0, 2.0, 4.0)] + [off(g, key, foot, deep=True)]
    fl = 0.5 * (max(ofs) - min(ofs))
    return math.sqrt(e ** 2 + fl ** 2), e, fl


R.banner("H1 / H2  THE TWO INFORMATIVE SYSTEMS")
RES = {}
for g in GAL:
    for foot in FOOTS:
        for key in ("single", "allmean", "clean"):
            o = off(g, key, foot)
            tot, e, fl = err_dex(g, "clean" if key == "clean" else "single", foot)
            RES[(g["name"], foot, key)] = dict(off=o, tot=tot, z=o / tot, e=e, fl=fl)
        RES[(g["name"], foot, "rule")] = dict(off=off(g, "clean", foot, rule=True))
    P(f"    {g['name']:10s} ({g['nmulti']} of {g['nmem']} multi-epoch) sigma_law {spred(g, 'canonical'):.2f} km/s; single {g['single']:.2f}, all-epoch mean {g['allmean']:.2f}, cleaned {g['clean']:.2f} (+{g['clean_p']:.2f} -{g['clean_m']:.2f})")
    for foot in FOOTS:
        P("       " + f"{foot:9s} offsets: " + ", ".join(f"{k} {RES[(g['name'], foot, k)]['off']:+.3f}" for k in ("single", "allmean", "clean"))
          + f"; cleaned {RES[(g['name'], foot, 'clean')]['off']:+.3f} +- {RES[(g['name'], foot, 'clean')]['tot']:.3f} ({RES[(g['name'], foot, 'clean')]['z']:+.2f} sigma); rule {RES[(g['name'], foot, 'rule')]['off']:+.3f}")
h1 = all(RES[(g["name"], f, "clean")]["z"] > 2 for g in GAL for f in FOOTS)
h2 = all(0 < RES[(g["name"], f, "clean")]["off"] < RES[(g["name"], f, "single")]["off"] for g in GAL for f in FOOTS)
check("H1 [HEADLINE] THE FAILURE SURVIVES MULTI-EPOCH CLEANING: the cleaned offset is positive at > 2 sigma for Bootes I AND Tucana II, both footings" + ("  [MUTATE: sigma x 0.5]" if MUTATE else ""),
      "; ".join(f"{g['name']} {f[:3]}: {RES[(g['name'], f, 'clean')]['off']:+.3f} +- {RES[(g['name'], f, 'clean')]['tot']:.3f} ({RES[(g['name'], f, 'clean')]['z']:+.2f})" for g in GAL for f in FOOTS), h1)
check("H2 THE CLEANING LOWERS BUT DOES NOT REMOVE THE OFFSET: 0 < cleaned < single-epoch, both systems and footings",
      "; ".join(f"{g['name']} {f[:3]}: single {RES[(g['name'], f, 'single')]['off']:+.3f} -> cleaned {RES[(g['name'], f, 'clean')]['off']:+.3f}" for g in GAL for f in FOOTS), h2)
check("R1 (reported) the paper-flag variant of the cleaning (Bootes I 3.95, Tucana II 3.45 km/s) and the rule",
      f"paper flag: Bootes I {math.log10(SF * 3.95 / spred(bo, 'canonical')):+.3f}, Tucana II {math.log10(SF * 3.45 / spred(tu, 'canonical')):+.3f}; rule (cleaned): "
      + ", ".join(f"{g['name']} {RES[(g['name'], 'canonical', 'rule')]['off']:+.3f}" for g in GAL), True, load_bearing=False)
reading = ("in the two systems where multi-epoch cleaning is possible the ultra-faint failure survives it at > 2 sigma each (two objects, not a population result)" if h1 else
           "at least one of the two systems no longer shows a > 2 sigma failure after multi-epoch cleaning")
P(f"\n    READING (declared): {reading}")
R.num("RES", {f"{a}|{b}|{c}": v for (a, b, c), v in RES.items()}); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
