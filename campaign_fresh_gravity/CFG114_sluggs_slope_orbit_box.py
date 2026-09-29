#!/usr/bin/env python3
"""CFG114 -- DOES THE SLUGGS DEFICIT SURVIVE GC SLOPES AND ORBITS VARIED TOGETHER?  The 5 x 5 box of CFG111's slope shifts (every published
gamma_i + delta, delta = -0.4 .. +0.4) and CFG113's constant GC anisotropy bracket (beta = -0.5 .. +0.5), both footings.

Criteria frozen and committed before any number: campaign_fresh_gravity/CFG114_FROZEN_CRITERIA.md (c5b32b499).
  machinery CFG113's pipeline exec'd read-only up to its controls (itself CFG111's, CFG55 exec'd read-only): CFG55's JAM-calibrated masses
           (independent of the GC slopes and orbits), CFG55's 16; gamma and a constant beta enter only h50's sigma_r2 / sigma_los.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  the box's edges reproduce the committed lanes to 1e-9: (0, 0) = CFG111's law / rule means (both footings); (delta, 0) =
               CFG111's R2 (canonical); (0, beta) = CFG113's R1 bracket (both footings).
  H1  [HEADLINE; MUTATE must fail] the law's JAM-calibrated SLUGGS deficit exceeds 2 sigma in EVERY cell of the box, both footings.
  R1-R4 (reported): the law's box and its weakest cell; the rule's box and its cells with |z| >= 2; the number of cells (of 25) with the
               law > 2 sigma; at the law's weakest cell, SLUGGS population masses and the four centrals excluded.
MUTATE=1: every galaxy's observed outer dispersions x 10^(-D) per footing, D = the law's mean in its weakest cell (from the unmodified data)
  -- the deficit removed, the scatter kept; H1 must FAIL (rc = 1).  If the main run's H1 also fails the control is uninformative for H1.
Run: python3 campaign_fresh_gravity/CFG114_sluggs_slope_orbit_box.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG114_sluggs_slope_orbit_box", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: observed outer dispersions x 10^(-D) (the law's mean deficit in its weakest cell removed) -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")
DEL = (-0.4, -0.2, 0.0, 0.2, 0.4)
BET = (-0.5, -0.25, 0.0, 0.25, 0.5)

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
F113 = os.path.join(HERE, "CFG113_sluggs_anisotropy.py")
src = open(F113).read()
g113 = {"__file__": F113, "__name__": "cfg113"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================== C1 / C2")], "CFG113", "exec"), g113)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
sample, MASS, GLIT, SHIFT, NAMES = g113["sample"], g113["MASS"], g113["GLIT"], g113["SHIFT"], g113["NAMES"]
CENT = {"NGC4486", "NGC4365", "NGC4374", "NGC5846"}


def box(foot, which, masses=None, keep=lambda g: True):
    out = {}
    for d in DEL:
        gs = {n: GLIT[n] + d for n in NAMES}
        for b in BET:
            _, m, e = sample(foot, MASS[foot][which] if masses is None else masses, which, gs, b, keep)
            out[(d, b)] = (m, e)
    return out


def table(bx):
    rows = ["      delta \\ beta " + " ".join(f"{b:+7.2f}" for b in BET)]
    for d in DEL:
        rows.append(f"      {d:+.1f}          " + " ".join(f"{bx[(d, b)][0] / bx[(d, b)][1]:+7.2f}" for b in BET))
    return "\n".join(rows)


# ================================================================== C1
R.banner("C1  CONTROL: THE BOX'S EDGES REPRODUCE CFG111 AND CFG113")
LAW = {f: box(f, "law") for f in FOOTS}
RULE = {f: box(f, "rule") for f in FOOTS}
c111 = json.load(open(os.path.join(HERE, "CFG111_sluggs_literature_gamma_results.json")))["numbers"]
c113 = json.load(open(os.path.join(HERE, "CFG113_sluggs_anisotropy_results.json")))["numbers"]
dev = 0.0
for f in FOOTS:
    dev = max(dev, abs(LAW[f][(0.0, 0.0)][0] - c111["RES"][f]["law"]["mean"]), abs(RULE[f][(0.0, 0.0)][0] - c111["RES"][f]["rule"]["mean"]))
    for b in BET:
        dev = max(dev, abs(LAW[f][(0.0, b)][0] - c113["RES"][f][str(b)]["law"]["mean"]), abs(RULE[f][(0.0, b)][0] - c113["RES"][f][str(b)]["rule"]["mean"]))
for d in (-0.4, -0.2, 0.2, 0.4):
    lm, le, rm, re_ = c111["R2"][str(d)]
    dev = max(dev, abs(LAW["canonical"][(d, 0.0)][0] - lm), abs(LAW["canonical"][(d, 0.0)][1] - le),
              abs(RULE["canonical"][(d, 0.0)][0] - rm), abs(RULE["canonical"][(d, 0.0)][1] - re_))
check("C1 CONTROL: the box's edges reproduce CFG111 (centre, R2) and CFG113 (R1 bracket) to 1e-9",
      f"max |difference| {dev:.1e} (4 + 20 + 16 comparisons)", dev < 1e-9)

if MUTATE:
    for f in FOOTS:
        wc = min(LAW[f], key=lambda k: LAW[f][k][0] / LAW[f][k][1]); D = LAW[f][wc][0]
        for n in NAMES:
            SHIFT[f][n] = -D
        P(f"    MUTATE {f}: D = {D:+.4f} dex (the law's weakest cell delta {wc[0]:+.1f}, beta {wc[1]:+.2f}) removed from the observed dispersions")
    LAW = {f: box(f, "law") for f in FOOTS}
    RULE = {f: box(f, "rule") for f in FOOTS}

# ================================================================== H1
R.banner("H1  THE LAW'S DEFICIT OVER THE WHOLE BOX (published gamma_i + delta, constant beta)")
for f in FOOTS:
    P(f"    law, {f} (sigma = mean / error):\n" + table(LAW[f]))
wk = {f: min(LAW[f], key=lambda k: LAW[f][k][0] / LAW[f][k][1]) for f in FOOTS}
zmin = {f: LAW[f][wk[f]][0] / LAW[f][wk[f]][1] for f in FOOTS}
h1 = all(zmin[f] > 2 for f in FOOTS)
check("H1 [HEADLINE] THE LAW'S DEFICIT EXCEEDS 2 SIGMA IN EVERY CELL OF THE BOX, both footings" + ("  [MUTATE: deficit removed]" if MUTATE else ""),
      "; ".join(f"{f}: weakest cell delta {wk[f][0]:+.1f}, beta {wk[f][1]:+.2f}: {LAW[f][wk[f]][0]:+.4f} +- {LAW[f][wk[f]][1]:.4f} ({zmin[f]:+.2f} sigma)"
                for f in FOOTS) + "  [each range alone: CFG111 2.3-4.7 sigma; CFG113 >= 3.38 / 2.93 sigma]", h1)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
check("R1 (reported) the law's box: its weakest and strongest cells, both footings",
      "; ".join(f"{f}: min {zmin[f]:+.2f} at ({wk[f][0]:+.1f}, {wk[f][1]:+.2f}), max "
                f"{max(v[0] / v[1] for v in LAW[f].values()):+.2f}" for f in FOOTS), True, load_bearing=False)
for f in FOOTS:
    P(f"    rule, {f} (sigma):\n" + table(RULE[f]))
bad = {f: [k for k, v in RULE[f].items() if abs(v[0] / v[1]) >= 2] for f in FOOTS}
check("R2 (reported) the rule's box: the cells with |z| >= 2 (delta, beta)",
      "; ".join(f"{f}: {len(bad[f])} of 25: " + (", ".join(f'({d:+.1f}, {b:+.2f}) {RULE[f][(d, b)][0] / RULE[f][(d, b)][1]:+.2f}' for d, b in bad[f]) or "none")
                for f in FOOTS), True, load_bearing=False)
cnt = {f: sum(1 for v in LAW[f].values() if v[0] / v[1] > 2) for f in FOOTS}
check("R3 (reported) the number of cells (of 25) where the law's deficit exceeds 2 sigma",
      "; ".join(f"{f}: {cnt[f]}" for f in FOOTS), True, load_bearing=False)
d0, b0 = wk["canonical"]
gs0 = {n: GLIT[n] + d0 for n in NAMES}
sl = sample("canonical", MASS["canonical"]["sl"], "law", gs0, b0)
nc = sample("canonical", MASS["canonical"]["law"], "law", gs0, b0, keep=lambda g: g["name"] not in CENT)
check("R4 (reported) at the law's weakest cell (canonical): SLUGGS population masses; the four centrals excluded",
      f"cell ({d0:+.1f}, {b0:+.2f}): population masses {sl[1]:+.4f} ({sl[1] / sl[2]:+.2f} sigma); no centrals N = {len(nc[0])}: {nc[1]:+.4f} ({nc[1] / nc[2]:+.2f} sigma)",
      True, load_bearing=False)

reading = ("the law's SLUGGS deficit survives the mass-anisotropy degeneracy across both declared ranges together" if h1 else
           "at the favourable corner of the two ranges the law's deficit falls below 2 sigma: the SLUGGS failure is not robust to the joint degeneracy")
P(f"\n    READING (declared): {reading}")
ser = lambda bx: {f"{d:+.1f}|{b:+.2f}": [v[0], v[1]] for (d, b), v in bx.items()}
R.num("law", {f: ser(LAW[f]) for f in FOOTS}); R.num("rule", {f: ser(RULE[f]) for f in FOOTS})
R.num("weakest", {f: [wk[f][0], wk[f][1], zmin[f]] for f in FOOTS}); R.num("R3", cnt)
R.num("R4", dict(cell=[d0, b0], pop=sl[1:], nocent=nc[1:])); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
