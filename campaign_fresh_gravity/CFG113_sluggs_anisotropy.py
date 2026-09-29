#!/usr/bin/env python3
"""CFG113 -- DOES GC ORBITAL ANISOTROPY RESCUE THE LAW'S SLUGGS DEFICIT?  CFG111's JAM-calibrated SLUGGS test (published per-galaxy GC
density slopes gamma_i, isotropic orbits) with a constant orbital anisotropy beta for the GC tracer.

Criteria frozen and committed before any number: campaign_fresh_gravity/CFG113_FROZEN_CRITERIA.md (8ef01b411).
  bracket  constant beta in {-0.5, -0.25, 0, +0.25, +0.5} for every galaxy (spans the measured early-type GC-system anisotropies: NGC 5846
           red ~0.4 / blue ~0.15 outside ~3 R_e, Napolitano+2014; NGC 1407 metal-rich radial / metal-poor tangential, Wasserman+2018; M87 red
           tangential / blue ~isotropic, Li+2020); beta = 0 is the control (= CFG111); +0.75 / +0.9 reported beyond the bracket.
  machinery CFG111's per-galaxy pipeline (CFG55 exec'd read-only): published gamma_i, CFG55's JAM-calibrated masses (independent of the GC
           orbits), CFG55's 16; beta enters only h50's sigma_r2 / sigma_los (which already take a constant beta).  beta(r) is not tested.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  beta = 0 reproduces CFG111's committed per-galaxy offsets (law and rule, both footings) to 1e-9.
  C2  CONTROL  flat-v_c potential, power-law tracer: sigma_r2 / sigma_los reproduce sigma_los^2 / v_c^2 = (g - b(g-1)) / (g (g - 2b)) to 0.3%
               at R = 5 kpc for gamma in {2.5, 3.43}, beta in {-0.5, +0.5}.
  H1  [HEADLINE; MUTATE must fail] with the published gamma_i the law's JAM-calibrated SLUGGS deficit exceeds 2 sigma at EVERY beta in the
               bracket, both footings (the minimum over the bracket is tested).
  R1-R6 (reported): law and rule at every beta; per-galaxy null beta; the global null beta; gamma = 3 at beta = +-0.5; SLUGGS population
               masses at beta = +-0.5; the four centrals excluded at beta = +0.5.
  R7  (POST HOC, added after the first run; reported only) the law's mean at beta = 0.5 / 0.9 / 0.99 on an extended radial grid,
               bounding the solver's grid-edge bias near beta = 1.  Every other line of both logs is unchanged apart from timing.
MUTATE=1: on each footing every galaxy's observed outer dispersions x 10^(-D), D = the law's mean offset at (gamma_i, beta = +0.5) from the
  unmodified data -- the deficit removed, the scatter kept; H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG113_sluggs_anisotropy.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG113_sluggs_anisotropy", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: observed outer dispersions x 10^(-D) (the law's mean deficit at beta = +0.5 removed) -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")
BRACKET = (-0.5, -0.25, 0.0, 0.25, 0.5)
BEYOND = (0.75, 0.9)

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG55_sluggs_dynamical_masses.py")).read()
g55 = {"__file__": os.path.join(HERE, "CFG55_sluggs_dynamical_masses.py"), "__name__": "cfg55"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("\nRES = {}\n")], "CFG55", "exec"), g55)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
G16, law_mass_g, rule_mass, debris = g55["G16"], g55["law_mass_g"], g55["rule_mass"], g55["debris"]
sigma_r2, sigma_los, nu_h, GAMMA = g55["sigma_r2"], g55["sigma_los"], g55["nu_h"], g55["GAMMA"]
A0SI, G_, KPC, MSUN, FB, nfw_enclosed, SL = g55["A0SI"], g55["G_"], g55["KPC"], g55["MSUN"], g55["FB"], g55["nfw_enclosed"], g55["SL"]
NAMES = [g["name"] for g in G16]


def gamma_rel(lm):
    return min(max(-0.63 * lm + 9.81, 2.0), 4.0)


GLIT = {n: gamma_rel(float(SL["NGC" + str(int(n[3:]))]["logM*"])) for n in NAMES}
G3 = {n: float(GAMMA) for n in NAMES}
SHIFT = {f: {n: 0.0 for n in NAMES} for f in FOOTS}          # log10 factor on sigma_obs (MUTATE only)


def sigma_pred(g, foot, Ms, which, gam, beta):
    """CFG111's sigma_pred_g with a constant GC anisotropy beta in the Jeans solution and the projection."""
    r = g["r"]; a0 = A0SI[foot]; a_h = r["Re"] / 1.8153
    fx, Mh = debris(Ms, foot) if which == "rule" else (0.0, 1.0)

    def gf(rr):
        Mb = Ms * MSUN * rr ** 2 / (rr + a_h) ** 2; gN = G_ * Mb / (rr * KPC) ** 2
        out = gN * nu_h(gN / a0)
        if fx > 0:
            out = out + fx * (1 - FB) * G_ * np.asarray(nfw_enclosed(Mh, rr), float) * MSUN / (rr * KPC) ** 2
        return out
    return sigma_los(r["Rb"], sigma_r2(gf, gam, beta), gam, beta)


def offset(g, foot, Ms, which, gam, beta):
    r = g["r"]; s = sigma_pred(g, foot, Ms, which, gam, beta)
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s[r["out"]]))) + SHIFT[foot][g["name"]]


def sample(foot, masses, which, gams, beta, keep=lambda g: True):
    off = np.array([offset(g, foot, m, which, gams[g["name"]], beta) for g, m in zip(G16, masses) if np.isfinite(m) and keep(g)])
    return off, float(off.mean()), float(off.std(ddof=1) / math.sqrt(len(off)))


MASS = {f: dict(law=[law_mass_g(g, f) for g in G16], rule=[rule_mass(g, f) for g in G16], sl=[g["r"]["Mstar"] for g in G16]) for f in FOOTS}

# ================================================================== C1 / C2
R.banner("C1 / C2  CONTROLS")
c111 = json.load(open(os.path.join(HERE, "CFG111_sluggs_literature_gamma_results.json")))["numbers"]
dev = 0.0
for f in FOOTS:
    for w in ("law", "rule"):
        mine = sample(f, MASS[f][w], w, GLIT, 0.0)[0]
        dev = max(dev, float(np.max(np.abs(mine - np.array(c111["RES"][f][w]["per"])))))
assert all(abs(c111["gamma"][n] - GLIT[n]) < 1e-12 for n in NAMES)
check("C1 CONTROL: beta = 0 reproduces CFG111's committed per-galaxy offsets (law and rule, both footings) to 1e-9",
      f"max |d offset| {dev:.1e} (64 offsets)", dev < 1e-9)
VC = 2.0e5
worst, rows = 0.0, []
for gm in (2.5, 3.43):
    for b in (-0.5, 0.5):
        s = float(sigma_los(np.array([5.0]), sigma_r2(lambda rr: VC ** 2 / (rr * KPC), gm, b), gm, b)[0]) * 1e3
        want = (gm - b * (gm - 1)) / (gm * (gm - 2 * b))
        dv = abs((s / VC) ** 2 / want - 1); worst = max(worst, dv); rows.append(f"g {gm} b {b:+.1f}: {(s / VC) ** 2:.5f} vs {want:.5f}")
check("C2 CONTROL: flat-v_c potential, power-law tracer: h50's sigma_r2 / sigma_los reproduce the analytic sigma_los^2 / v_c^2 to 0.3% (R = 5 kpc)",
      f"worst {worst:.1e}; " + "; ".join(rows), worst < 3e-3)

if MUTATE:
    for f in FOOTS:
        D = sample(f, MASS[f]["law"], "law", GLIT, 0.5)[1]
        for n in NAMES:
            SHIFT[f][n] = -D
        P(f"    MUTATE {f}: D = {D:+.4f} dex removed from every galaxy's observed outer dispersions")

# ================================================================== H1
R.banner("H1  THE LAW'S DEFICIT ACROSS THE DECLARED ANISOTROPY BRACKET (published gamma_i)")
RES = {f: {} for f in FOOTS}
for f in FOOTS:
    for b in BRACKET + BEYOND:
        RES[f][b] = dict(law=sample(f, MASS[f]["law"], "law", GLIT, b), rule=sample(f, MASS[f]["rule"], "rule", GLIT, b))
for f in FOOTS:
    P(f"    {f}: " + "; ".join(f"beta {b:+.2f} law {RES[f][b]['law'][1]:+.4f} ({RES[f][b]['law'][1] / RES[f][b]['law'][2]:+.2f})" for b in BRACKET))
zmin = {f: min(RES[f][b]["law"][1] / RES[f][b]["law"][2] for b in BRACKET) for f in FOOTS}
bmin = {f: min(BRACKET, key=lambda b: RES[f][b]["law"][1] / RES[f][b]["law"][2]) for f in FOOTS}
h1 = all(zmin[f] > 2 for f in FOOTS)
check("H1 [HEADLINE] WITH THE PUBLISHED SLOPES THE LAW'S DEFICIT EXCEEDS 2 SIGMA AT EVERY BETA IN THE BRACKET, both footings"
      + ("  [MUTATE: deficit removed]" if MUTATE else ""),
      "; ".join(f"{f}: minimum {zmin[f]:+.2f} sigma at beta {bmin[f]:+.2f} ({RES[f][bmin[f]]['law'][1]:+.4f} +- {RES[f][bmin[f]]['law'][2]:.4f})" for f in FOOTS)
      + "  [beta = 0 (CFG111): +3.60 / +3.22 sigma]", h1)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
check("R1 (reported) the law and the rule at every beta (canonical | alt; sigma = mean / error)",
      "; ".join(f"beta {b:+.2f}: law {RES['canonical'][b]['law'][1]:+.4f} ({RES['canonical'][b]['law'][1] / RES['canonical'][b]['law'][2]:+.2f}) | "
                f"{RES['alt'][b]['law'][1] / RES['alt'][b]['law'][2]:+.2f}, rule {RES['canonical'][b]['rule'][1]:+.4f} "
                f"({RES['canonical'][b]['rule'][1] / RES['canonical'][b]['rule'][2]:+.2f}) | {RES['alt'][b]['rule'][1] / RES['alt'][b]['rule'][2]:+.2f}"
                for b in BRACKET + BEYOND), True, load_bearing=False)
nul = []
for g, m in zip(G16, MASS["canonical"]["law"]):
    fz = lambda b, g=g, m=m: offset(g, "canonical", m, "law", GLIT[g["name"]], b)
    try:
        nul.append((g["name"], brentq(fz, -1.0, 0.99, xtol=1e-4)))
    except ValueError:
        nul.append((g["name"], float("nan")))
check("R2 (reported) per galaxy (canonical): the constant beta in [-1, 0.99] that nulls the law's offset (nan = none), beside gamma_i",
      "; ".join(f"{n[3:]} {b:+.2f} (gamma {GLIT[n]:.2f}, offset at 0 {RES['canonical'][0.0]['law'][0][i]:+.3f})" for i, (n, b) in enumerate(nul))
      + "  [NGC 5846 measured: red ~0.4, blue ~0.15 outside ~3 R_e]", True, load_bearing=False)
gnul = {}
for f in FOOTS:
    fz = lambda b, f=f: sample(f, MASS[f]["law"], "law", GLIT, b)[1]
    try:
        gnul[f] = brentq(fz, -1.0, 0.99, xtol=1e-4)
    except ValueError:
        gnul[f] = float("nan")
check("R3 (reported) the one constant beta in [-1, 0.99] that nulls the law's mean offset (nan = none)",
      "; ".join(f"{f}: {gnul[f]:+.3f} (mean at beta 0.99: {sample(f, MASS[f]['law'], 'law', GLIT, 0.99)[1]:+.4f})" for f in FOOTS), True, load_bearing=False)
r4 = {b: (sample("canonical", MASS["canonical"]["law"], "law", G3, b), sample("canonical", MASS["canonical"]["rule"], "rule", G3, b)) for b in (-0.5, 0.0, 0.5)}
check("R4 (reported) gamma = 3 for every galaxy (CFG55's baseline), canonical: the law and the rule at beta = -0.5 / 0 / +0.5",
      "; ".join(f"beta {b:+.1f}: law {v[0][1]:+.4f} ({v[0][1] / v[0][2]:+.2f}), rule {v[1][1]:+.4f} ({v[1][1] / v[1][2]:+.2f})" for b, v in r4.items()),
      True, load_bearing=False)
r5 = {b: (sample("canonical", MASS["canonical"]["sl"], "law", GLIT, b), sample("canonical", MASS["canonical"]["sl"], "rule", GLIT, b)) for b in (-0.5, 0.5)}
check("R5 (reported) SLUGGS's population masses, published gamma_i, canonical: the law and the rule at beta = -0.5 / +0.5",
      "; ".join(f"beta {b:+.1f}: law {v[0][1]:+.4f} ({v[0][1] / v[0][2]:+.2f}), rule {v[1][1]:+.4f} ({v[1][1] / v[1][2]:+.2f})" for b, v in r5.items()),
      True, load_bearing=False)
CENT = {"NGC4486", "NGC4365", "NGC4374", "NGC5846"}
nc = (sample("canonical", MASS["canonical"]["law"], "law", GLIT, 0.5, keep=lambda g: g["name"] not in CENT),
      sample("canonical", MASS["canonical"]["rule"], "rule", GLIT, 0.5, keep=lambda g: g["name"] not in CENT))
check("R6 (reported) the four group/cluster centrals excluded, beta = +0.5, canonical",
      f"N = {len(nc[0][0])}: law {nc[0][1]:+.4f} ({nc[0][1] / nc[0][2]:+.2f} sigma); rule {nc[1][1]:+.4f} ({nc[1][1] / nc[1][2]:+.2f} sigma)",
      True, load_bearing=False)

HG = sigma_r2.__globals__                                    # h50's namespace (read-only use; restored below)
RG0, LRG0 = HG["RG"], HG["LRG"]
try:
    HG["RG"] = np.geomspace(0.02, 3e6, 1600); HG["LRG"] = np.log(HG["RG"])
    r7 = {f: {b: sample(f, MASS[f]["law"], "law", GLIT, b)[1] for b in (0.5, 0.9, 0.99)} for f in FOOTS}
finally:
    HG["RG"], HG["LRG"] = RG0, LRG0
check("R7 (post hoc, reported only; added after the first run) the law's mean offset at beta = 0.5 / 0.9 / 0.99 on an extended radial grid "
      "(to 3e6 kpc, 1600 points), bounding the solver's grid-edge bias near beta = 1",
      "; ".join(f"{f}: " + ", ".join(f"beta {b}: {v:+.4f} (standard grid {RES[f][b]['law'][1] if b in RES[f] else sample(f, MASS[f]['law'], 'law', GLIT, b)[1]:+.4f})"
                                      for b, v in r7[f].items()) for f in FOOTS), True, load_bearing=False)
reading = ("orbital anisotropy inside the measured range does not rescue the law" if h1 else
           "radially biased GC orbits inside the measured range bring the law's deficit below 2 sigma: the SLUGGS failure is degenerate with the GC orbits")
P(f"\n    READING (declared): {reading}")
R.num("RES", {f: {str(b): {w: dict(mean=v[1], err=v[2], per=v[0].tolist()) for w, v in d.items()} for b, d in RES[f].items()} for f in FOOTS})
R.num("zmin", zmin); R.num("R2", dict(nul)); R.num("R3", gnul)
R.num("R4", {str(b): [v[0][1], v[0][2], v[1][1], v[1][2]] for b, v in r4.items()})
R.num("R5", {str(b): [v[0][1], v[0][2], v[1][1], v[1][2]] for b, v in r5.items()})
R.num("R6", dict(law=nc[0][1:], rule=nc[1][1:])); R.num("R7", {f: {str(b): v for b, v in d.items()} for f, d in r7.items()}); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
