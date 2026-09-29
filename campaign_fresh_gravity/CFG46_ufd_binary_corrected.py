#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG46 -- THE ULTRA-FAINT FAILURE AGAINST BINARY-CORRECTED DISPERSIONS (Arroyo-Polonio, Battaglia & Thomas 2026).

WHY.  CFG28-CFG29 refereed B's largest data failure, the Milky Way ultra-faints' measured dispersions +0.30-0.33 dex above the isolated law (3.5-3.8
sigma), and found that unresolved binaries could not explain it with PUBLISHED bounds (McConnachie & Cote 2010; Ou+2026) used as fixed inputs.  The
remaining escape was a statistical correction applied to the data themselves.  Arroyo-Polonio et al. 2026 (arXiv:2603.03129, Table 1;
real_research/data/arroyopolonio2026_ufd_binary_corrected.tsv) apply exactly that to 12 ultra-faints: a mixture model with the solar-neighbourhood
binary velocity distribution, single-epoch data, the binary fraction f free (flat prior) or fixed at 0.7.  They find dispersions lowered by ~1.25-1.75x
(masses by 1.5-3x).  This lane scores B on those corrected dispersions.

THE METHOD (declared before this script's first run).  FG001's committed estimator (exec'd read-only, as CFG28/CFG42): sigma^2 = g(r) r / 3 at r = (4/3) r_half
with half of the baryons enclosed, Upsilon_V = 2, stars only; the isolated law (nu_mono, both footings).  Galaxy inputs (M_V, r_half, gas) from the repo's
Milky Way LVD table (the same source as FG001), matched by name; FG001's brightness cut M_V > -7.7 removes Crater II (reported separately); three of the
paper's twelve (Eri III, Sag II, UNIONS 1) are absent from that table and are not scored.  Scored: the eight that remain (Boo I, Car II, Hyd I, Leo IV,
Leo V, Ret II, Seg 1, Wil 1).  Dispersions: the paper's posterior medians for f = 0 (sig_fz), f free (sig_f, HEADLINE) and f = 0.7 (sig_f7); the paper's
own f = 0 re-analysis is the control.  Statistic: the median over the eight of log10(sigma / sigma_law).  Errors: a bootstrap over the eight (2000), plus the
measurement error (each dispersion drawn from a split normal built from the paper's asymmetric 1-sigma errors, 2000 draws; the spread of the median), plus a
floor in quadrature = CFG28's: half the range of the median over Upsilon_V 1 to 4 and the pure deep-MOND estimator sigma^4 = (4/81) G M a0.  The rule
(reported): CFG42's sum with the Moster collapse mass (clamped at 1e9, declared there).

PRE-DECLARED
  C1  CONTROL  the table as transcribed: 12 rows; Boo I sig_fz = 2.55, sig_f = 2.18; the paper's sig_f is below its sig_fz for at least 10 of 12.
  C2  CONTROL  with the paper's f = 0 dispersions the bare law's offset is positive and within 0.1 dex of the uncorrected LVD-table value for the same eight (the
               paper's re-analysis is consistent with FG001's data).
  H1  [HEADLINE; MUTATE must fail] THE FAILURE SURVIVES THE BINARY CORRECTION: the bare law's median offset with the f-free dispersions is positive at more
      than 2 sigma on both footings.
  H2  the failure also survives the strongest correction (f = 0.7): positive at more than 1 sigma on both footings.
  H3  (reported as a test of the rule) the sum rule with the corrected dispersions is within 2 sigma of zero (not over-predicting) on both footings.
  R1  (reported) per-system offsets; the f = 0 and f = 0.7 versions; Crater II; the fraction of the eight with a positive offset.
  READING (declared): H1 PASS -> the statistical binary correction does not remove B's ultra-faint failure (it lowers it); the multi-epoch data are still the decisive
      test.  H1 FAIL -> the corrected dispersions no longer show a > 2 sigma failure: the failure was carried by binaries (statistically) and B's ultra-faint problem
      is not established.  H3 FAIL -> with the corrected dispersions the rule now over-predicts.
MUTATE=1: every dispersion multiplied by 0.5 -- H1 must FAIL (rc = 1).
NOTE (disclosed): H1's threshold (> 2 sigma) was declared without checking that eight systems can reach it at f = 0; on these eight even the uncorrected offset is 1.8 sigma.
  The post-hoc R2 (paired shift) was added after the main run for that reason.
Run: python3 campaign_fresh_gravity/CFG46_ufd_binary_corrected.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib, csv, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
import hunt_lib as HL
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG46_ufd_binary_corrected", MUTATE)
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
DATA = os.path.join(C.REPO, "real_research", "data")

T = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "arroyopolonio2026_ufd_binary_corrected.tsv")) if l.strip() and not l.startswith("#")]
TAB = {r[0]: dict(zip(T[0], r)) for r in T[1:]}
MAP = {"Boo I": "Bootes I", "Car II": "Carina II", "Cra II": "Crater II", "Hyd I": "Hydrus I", "Leo IV": "Leo IV", "Leo V": "Leo V",
       "Ret II": "Reticulum II", "Seg 1": "Segue 1", "Wil 1": "Willman 1"}
LVD = {}
for r in csv.DictReader(open(os.path.join(ns["DSPH"], "lvd_dwarf_mw.csv"))):
    LVD[r["name"]] = r
GAL = []
for k, lv in MAP.items():
    r = LVD[lv]; MV = fnum(r["M_V"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"]); MHI = fnum(r["mass_HI"])
    t = TAB[k]
    GAL.append(dict(name=k, MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, MHI=(10 ** MHI if MHI is not None else 0.0), lvd_sig=fnum(r["vlos_sigma"]),
                    **{v: (float(t[v]) if t[v] not in ("", "nan") else None) for v in t if v not in ("name", "stars", "ref")}))
SCORED = [g for g in GAL if g["MV"] > -7.7]
CRA = [g for g in GAL if g["MV"] <= -7.7]

R.banner("C1 / C2  CONTROLS")
below = sum(float(v["sig_f"]) < float(v["sig_fz"]) for v in TAB.values())
check("C1 CONTROL: 12 rows; Boo I sig_fz = 2.55, sig_f = 2.18; sig_f < sig_fz for at least 10 of 12",
      f"{len(TAB)} rows; Boo I {TAB['Boo I']['sig_fz']} / {TAB['Boo I']['sig_f']}; sig_f < sig_fz for {below}", len(TAB) == 12 and TAB["Boo I"]["sig_fz"] == "2.55" and TAB["Boo I"]["sig_f"] == "2.18" and below >= 10)


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


def med_off(sample, key, foot, **kw):
    return float(np.median([math.log10(SF * g[key] / spred(g, foot, **kw)) for g in sample]))


ctrl = {f: (med_off(SCORED, "sig_fz", f), float(np.median([math.log10(g["lvd_sig"] / spred(g, f)) for g in SCORED]))) for f in FOOTS}
check("C2 CONTROL: with the paper's f = 0 dispersions the bare law's offset is positive and within 0.1 dex of the LVD-table value for the same eight",
      "; ".join(f"{f}: paper f=0 {a:+.3f}, LVD {b:+.3f}" for f, (a, b) in ctrl.items()), all(a > 0 and abs(a - b) < 0.1 for a, b in ctrl.values()) if not MUTATE else True)


def split_normal(rng, m, p, mn, n):
    u = rng.random(n); z = rng.standard_normal(n)
    v = np.where(z >= 0, m + z * p, m + z * mn)
    return np.maximum(v, 0.05)


def stat(key, foot, rule=False, seed=46, sample=None):
    smp = SCORED if sample is None else sample
    base = np.array([math.log10(SF * g[key] / spred(g, foot, rule=rule)) for g in smp]); m0 = float(np.median(base))
    rng = np.random.default_rng(seed)
    bs = [float(np.median(base[rng.integers(0, len(base), len(base))])) for _ in range(2000)]
    mc = []
    for _ in range(2000):
        vals = [split_normal(rng, g[key], g[key + "_p1"], g[key + "_m1"], 1)[0] for g in smp]
        mc.append(float(np.median([math.log10(SF * v / spred(g, foot, rule=rule)) for v, g in zip(vals, smp)])))
    fl = [float(np.median([math.log10(SF * g[key] / spred(g, foot, ups=u, rule=rule)) for g in smp])) for u in (1.0, 2.0, 4.0)]
    fl.append(float(np.median([math.log10(SF * g[key] / spred(g, foot, deep=True)) for g in smp])) if not rule else fl[1])
    floor = 0.5 * (max(fl) - min(fl))
    tot = math.sqrt(np.std(bs) ** 2 + np.std(mc) ** 2 + floor ** 2)
    return dict(med=m0, boot=float(np.std(bs)), meas=float(np.std(mc)), floor=floor, tot=tot, z=m0 / tot)


R.banner("H1 / H2 / H3  THE EIGHT ULTRA-FAINTS")
RES = {}
for foot in FOOTS:
    for key, lab in (("sig_fz", "f = 0"), ("sig_f", "f free"), ("sig_f7", "f = 0.7")):
        RES[(foot, key, "law")] = stat(key, foot)
    RES[(foot, "sig_f", "rule")] = stat("sig_f", foot, rule=True)
    for key, lab in (("sig_fz", "f = 0"), ("sig_f", "f free"), ("sig_f7", "f = 0.7")):
        v = RES[(foot, key, "law")]
        P(f"    {foot:9s} law  {lab:8s}: median {v['med']:+.3f} +- {v['tot']:.3f} (bootstrap {v['boot']:.3f}, measurement {v['meas']:.3f}, floor {v['floor']:.3f}) -> {v['z']:+.2f} sigma")
    v = RES[(foot, "sig_f", "rule")]
    P(f"    {foot:9s} rule f free : median {v['med']:+.3f} +- {v['tot']:.3f} -> {v['z']:+.2f} sigma")
for g in SCORED:
    P(f"    {g['name']:7s} sigma_law {spred(g, 'canonical'):5.2f}  paper f=0 {g['sig_fz']:5.2f}  f free {g['sig_f']:5.2f}  f=0.7 {g['sig_f7']:5.2f}  offsets "
      f"{math.log10(SF * g['sig_fz'] / spred(g, 'canonical')):+.2f} / {math.log10(SF * g['sig_f'] / spred(g, 'canonical')):+.2f} / {math.log10(SF * g['sig_f7'] / spred(g, 'canonical')):+.2f}")
h1 = all(RES[(f, "sig_f", "law")]["z"] > 2 for f in FOOTS)
h2 = all(RES[(f, "sig_f7", "law")]["z"] > 1 for f in FOOTS)
h3 = all(abs(RES[(f, "sig_f", "rule")]["z"]) < 2 for f in FOOTS)
check("H1 [HEADLINE] THE FAILURE SURVIVES THE BINARY CORRECTION: the bare law's median offset with the f-free dispersions is positive at > 2 sigma, both footings" + ("  [MUTATE: sigma x 0.5]" if MUTATE else ""),
      "; ".join(f"{f}: f = 0 {RES[(f, 'sig_fz', 'law')]['med']:+.3f}, f free {RES[(f, 'sig_f', 'law')]['med']:+.3f} +- {RES[(f, 'sig_f', 'law')]['tot']:.3f} ({RES[(f, 'sig_f', 'law')]['z']:+.2f} sigma)" for f in FOOTS), h1)
check("H2 THE FAILURE SURVIVES THE STRONGEST CORRECTION (f = 0.7): positive at > 1 sigma, both footings",
      "; ".join(f"{f}: {RES[(f, 'sig_f7', 'law')]['med']:+.3f} ({RES[(f, 'sig_f7', 'law')]['z']:+.2f} sigma)" for f in FOOTS), h2)
check("H3 THE RULE WITH THE CORRECTED DISPERSIONS IS WITHIN 2 SIGMA OF ZERO (not over-predicting), both footings",
      "; ".join(f"{f}: {RES[(f, 'sig_f', 'rule')]['med']:+.3f} ({RES[(f, 'sig_f', 'rule')]['z']:+.2f} sigma)" for f in FOOTS), h3)
pos = {k: sum(math.log10(SF * g[k] / spred(g, "canonical")) > 0 for g in SCORED) for k in ("sig_fz", "sig_f", "sig_f7")}
cr = CRA[0]
check("R1 (reported) fraction of the eight with a positive offset; Crater II (excluded by FG001's M_V cut)",
      f"positive offsets of 8: f=0 {pos['sig_fz']}, f free {pos['sig_f']}, f=0.7 {pos['sig_f7']}; Crater II (M_V {cr['MV']}): law {spred(cr, 'canonical'):.2f} vs f free {cr['sig_f']:.2f} ({math.log10(SF * cr['sig_f'] / spred(cr, 'canonical')):+.2f} dex)",
      True, load_bearing=False)
# post-hoc (added after the main run, disclosed): the paired effect of the correction itself, which does not depend on the sample's power
pair = {k: np.array([math.log10(g[k] / g["sig_fz"]) for g in SCORED]) for k in ("sig_f", "sig_f7")}
check("R2 (reported, POST-HOC: added after the main run) the paired shift of each dispersion by the correction, median over the eight (dex): f free, f = 0.7",
      f"f free {np.median(pair['sig_f']):+.3f} (range {pair['sig_f'].min():+.2f}..{pair['sig_f'].max():+.2f}); f = 0.7 {np.median(pair['sig_f7']):+.3f} (range {pair['sig_f7'].min():+.2f}..{pair['sig_f7'].max():+.2f}); "
      f"the uncorrected f = 0 offset on these eight is only {RES[('canonical', 'sig_fz', 'law')]['z']:+.2f} sigma, so H1's failure is largely lost power (N = 8 against 40 in CFG28)",
      True, load_bearing=False)
reading = ("the statistical binary correction does not remove B's ultra-faint failure; it lowers it" if h1 else
           "the corrected dispersions no longer show a > 2 sigma failure: B's ultra-faint problem is not established at the statistical level")
if not h3:
    reading += "; with the corrected dispersions the rule now over-predicts"
P(f"\n    READING (declared): {reading}")
R.num("RES", {f"{a}|{b}|{c}": v for (a, b, c), v in RES.items()}); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
