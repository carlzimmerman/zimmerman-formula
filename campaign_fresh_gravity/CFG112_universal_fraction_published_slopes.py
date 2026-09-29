#!/usr/bin/env python3
"""CFG112 -- WITH PUBLISHED GC SLOPES, DOES ONE DEBRIS FRACTION FIT ALL TEN POPULATIONS AT 2 SIGMA?  CFG75: with CFG71's dynamical SLUGGS
masses (gamma = 3) the ten-population 2-sigma intersection is empty only through SLUGGS (2.6 sigma at phi = 1).  CFG111: with each galaxy's
published GC density slope the rule's JAM-calibrated SLUGGS offset at phi = 1 is 1.55 sigma.  Does the 2-sigma intersection open?

Criteria frozen and committed before any number: campaign_fresh_gravity/CFG112_FROZEN_CRITERIA.md (663f73877).
  machinery CFG71's harness exec'd read-only up to its scan (MUTATE forced 0): calib_mass_phi (the phi-scaled JAM calibration), debris_phi,
           CFG55's Jeans functions.  ONE change: U5d's prediction uses gamma_i per galaxy (CFG111's gamma_rel = clip(-0.63 log M* + 9.81, 2, 4))
           in sigma_r2 / sigma_los.  The other nine populations' o(phi), e(phi) are read from CFG71's committed scan (101-point grid on [0, 1]).
           Intersection at k sigma = CFG75's definition: the grid points where |o| <= k e for every population (edges = first / last point).
PRE-DECLARED (from the frozen file)
  C1  CONTROL  gamma_i = 3 for every galaxy: the patched U5d reproduces CFG71's committed U5d scan (o and e, 101 points, both footings) to 1e-9.
  C2  CONTROL  published gamma_i: U5d at phi = 0 / phi = 1 reproduces CFG111's committed law / rule means and errors (both footings) to 1e-6.
  C3  CONTROL  CFG75's committed 2-sigma intersection without SLUGGS ([0.23, 0.71] canonical, [0.21, 0.66] alt) reproduced from CFG71's JSON.
  H1  [HEADLINE; MUTATE must fail] with the published slopes the ten-population 2-sigma intersection is non-empty on both footings.
  R1-R4 (reported): U5d's 1 / 2 sigma intervals; the 1 / 3 sigma intersections; SLUGGS's own population masses (U5s); gamma_i +- 0.2.
MUTATE=1: gamma_i = 3 for every galaxy (the lane's one change undone) -- the 2-sigma intersection must be empty (CFG75), H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG112_universal_fraction_published_slopes.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG112_universal_fraction_published_slopes", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: gamma_i = 3 for every galaxy -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
F71 = os.path.join(HERE, "CFG71_universal_fraction_dynamical_sluggs.py")
src = open(F71).read()
g71 = {"__file__": F71, "__name__": "cfg71"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("\nGRID = np.round(")], "CFG71", "exec"), g71)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
assert g71["MCF"] == 1.0
G16, calib_mass_phi, debris_phi = g71["G16"], g71["calib_mass_phi"], g71["debris_phi"]
sr2, slos, GAMMA55, nu55, nfw55 = g71["sr2_55"], g71["slos55"], g71["GAMMA55"], g71["nu55"], g71["nfw55"]
A0SI55, FB55, G55, KPC55, MSUN55, SL = g71["A0SI55"], g71["FB55"], g71["G55"], g71["KPC55"], g71["MSUN55"], g71["g55"]["SL"]
NAMES = [g["name"] for g in G16]
GRID = np.round(np.linspace(0.0, 1.0, 101), 10)
U5 = "U5 SLUGGS (dynamical masses, 16)"
S71 = json.load(open(os.path.join(HERE, "CFG71_universal_fraction_dynamical_sluggs_results.json")))["numbers"]["scan"]
OTHERS = sorted({k.split("|")[0] for k in S71} - {U5})
assert len(OTHERS) == 9 and all(np.allclose(S71[n + "|canonical"]["phi"], GRID) for n in OTHERS)


def gamma_rel(lm):
    return min(max(-0.63 * lm + 9.81, 2.0), 4.0)


GLIT = {n: gamma_rel(float(SL["NGC" + str(int(n[3:]))]["logM*"])) for n in NAMES}
G3 = {n: float(GAMMA55) for n in NAMES}
GUSE = G3 if MUTATE else GLIT


def off_phi_g(g, foot, Ms, phi, gam):
    """CFG71's off_phi with the tracer slope gam in place of the global gamma = 3 (the lane's one change)."""
    r = g["r"]; a0 = A0SI55[foot]; a_h = r["Re"] / 1.8153
    fx, Mh = debris_phi(Ms, foot)

    def gf(rr):
        Mb = Ms * MSUN55 * rr ** 2 / (rr + a_h) ** 2; gN = G55 * Mb / (rr * KPC55) ** 2
        out = gN * nu55(gN / a0)
        if phi * fx > 0:
            out = out + phi * fx * (1 - FB55) * G55 * np.asarray(nfw55(Mh, rr), float) * MSUN55 / (rr * KPC55) ** 2
        return out
    s_ = slos(r["Rb"], sr2(gf, gam), gam)
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s_[r["out"]])))


_CAL = {}


def cal(g, foot, phi):
    k = (g["name"], foot, float(phi))
    if k not in _CAL:
        _CAL[k] = calib_mass_phi(g, foot, phi)
    return _CAL[k]


def scan(foot, gams, masses="dyn"):
    oo, ee, nx = [], [], []
    for ph in GRID:
        off = []
        for g in G16:
            m = cal(g, foot, ph) if masses == "dyn" else g["r"]["Mstar"]
            off.append(float("nan") if not np.isfinite(m) else off_phi_g(g, foot, m, ph, gams[g["name"]]))
        off = np.array(off); ok = np.isfinite(off); o = off[ok]
        oo.append(float(o.mean())); ee.append(float(o.std(ddof=1) / math.sqrt(len(o)))); nx.append(int((~ok).sum()))
    return dict(o=np.array(oo), e=np.array(ee), nexcl=nx)


def inside(o, e, k):
    return np.abs(np.asarray(o)) <= k * np.asarray(e)


def inter(u5, foot, k, drop_u5=False):
    good = np.ones(len(GRID), bool)
    for n in OTHERS:
        good &= inside(S71[n + "|" + foot]["o"], S71[n + "|" + foot]["e"], k)
    if not drop_u5:
        good &= inside(u5["o"], u5["e"], k)
    return (float(GRID[good][0]), float(GRID[good][-1]), int(good.sum())) if good.any() else None


def runs(mask):
    out, st = [], None
    for i, m in enumerate(mask):
        if m and st is None:
            st = i
        if not m and st is not None:
            out.append((float(GRID[st]), float(GRID[i - 1]))); st = None
    if st is not None:
        out.append((float(GRID[st]), float(GRID[-1])))
    return out


def fmt(iv):
    return "empty" if iv is None else f"[{iv[0]:.2f}, {iv[1]:.2f}] ({iv[2]} pts)"


# ================================================================== C1 / C2 / C3
R.banner("C1 / C2 / C3  CONTROLS")
dev, sc3 = 0.0, {}
for f in FOOTS:
    sc3[f] = scan(f, G3)
    ref = S71[U5 + "|" + f]
    dev = max(dev, float(np.max(np.abs(sc3[f]["o"] - np.array(ref["o"])))), float(np.max(np.abs(sc3[f]["e"] - np.array(ref["e"])))))
check("C1 CONTROL: with gamma = 3 for every galaxy the patched U5d reproduces CFG71's committed U5d scan (o, e; 101 points; both footings) to 1e-9",
      f"max |difference| {dev:.1e}", dev < 1e-9)
c111 = json.load(open(os.path.join(HERE, "CFG111_sluggs_literature_gamma_results.json")))["numbers"]["RES"]
SC = {f: scan(f, GUSE) for f in FOOTS}
d2, rows = 0.0, []
for f in FOOTS:
    for which, idx in (("law", 0), ("rule", -1)):
        mo, me = SC[f]["o"][idx], SC[f]["e"][idx]
        d2 = max(d2, abs(mo - c111[f][which]["mean"]), abs(me - c111[f][which]["err"]))
        rows.append(f"{f} {which} {mo:+.6f} +- {me:.6f} (CFG111 {c111[f][which]['mean']:+.6f} +- {c111[f][which]['err']:.6f})")
if MUTATE:
    check("C2 CONTROL: U5d at phi = 0 / 1 reproduces CFG111's committed law / rule (published gamma) to 1e-6  [MUTATE: gamma = 3, so not applicable; reported]",
          "; ".join(rows), True, load_bearing=False)
else:
    check("C2 CONTROL: with the published gamma_i, U5d at phi = 0 / 1 reproduces CFG111's committed law / rule means and errors (both footings) to 1e-6",
          f"max |difference| {d2:.1e}; " + "; ".join(rows), d2 < 1e-6)
want = {"canonical": (0.23, 0.71), "alt": (0.21, 0.66)}
got = {f: inter(None, f, 2, drop_u5=True) for f in FOOTS}
check("C3 CONTROL: CFG75's committed 2-sigma intersection without SLUGGS is reproduced from CFG71's JSON ([0.23, 0.71] canonical, [0.21, 0.66] alt)",
      "; ".join(f"{f} {fmt(got[f])}" for f in FOOTS),
      all(got[f] is not None and round(got[f][0], 2) == want[f][0] and round(got[f][1], 2) == want[f][1] for f in FOOTS))

# ================================================================== H1
R.banner("H1  THE TEN-POPULATION 2-SIGMA INTERSECTION WITH THE PUBLISHED SLOPES")
for f in FOOTS:
    P(f"    {f}: U5d o(phi) / e(phi) at phi = 0, 0.25, 0.5, 0.71, 0.75, 1: " +
      ", ".join(f"{SC[f]['o'][i]:+.4f}/{SC[f]['e'][i]:.4f} ({SC[f]['o'][i] / SC[f]['e'][i]:+.2f})" for i in (0, 25, 50, 71, 75, 100))
      + f"; galaxies excluded by the calibration: max {max(SC[f]['nexcl'])}")
I2 = {f: inter(SC[f], f, 2) for f in FOOTS}
h1 = all(I2[f] is not None for f in FOOTS)
check("H1 [HEADLINE] WITH THE PUBLISHED SLOPES THE TEN-POPULATION 2-SIGMA INTERSECTION IS NON-EMPTY, both footings"
      + ("  [MUTATE: gamma = 3]" if MUTATE else ""),
      "; ".join(f"{f}: {fmt(I2[f])}" for f in FOOTS) + "  [gamma = 3 (CFG75): empty, both footings]", h1)
bind = {}
for f in FOOTS:
    s5 = inside(SC[f]["o"], SC[f]["e"], 2)
    pairs = []
    for n in OTHERS:
        sn = inside(S71[n + "|" + f]["o"], S71[n + "|" + f]["e"], 2)
        if not (s5 & sn).any():
            pairs.append(n.split(" ")[0])
    bind[f] = pairs
P("    populations whose 2-sigma set is disjoint from SLUGGS's: " + "; ".join(f"{f}: {', '.join(v) if v else 'none'}" for f, v in bind.items()))

# ================================================================== reported rows
R.banner("REPORTED ROWS")
check("R1 (reported) U5d's 1-sigma and 2-sigma sets with the published slopes (grid runs)",
      "; ".join(f"{f}: 1s {runs(inside(SC[f]['o'], SC[f]['e'], 1)) or 'empty'}, 2s {runs(inside(SC[f]['o'], SC[f]['e'], 2)) or 'empty'}" for f in FOOTS),
      True, load_bearing=False)
I13 = {f: (inter(SC[f], f, 1), inter(SC[f], f, 3)) for f in FOOTS}
check("R2 (reported) the ten-population intersections at 1 sigma and 3 sigma with the published slopes",
      "; ".join(f"{f}: 1s {fmt(v[0])}, 3s {fmt(v[1])}" for f, v in I13.items()), True, load_bearing=False)
SS = {f: scan(f, GUSE, masses="own") for f in FOOTS}
I2s = {f: inter(SS[f], f, 2) for f in FOOTS}
check("R3 (reported) SLUGGS's own population masses for the 16 (U5s; debris phi-scaled in the prediction only), published slopes: 2-sigma set and intersection",
      "; ".join(f"{f}: U5s 2s {runs(inside(SS[f]['o'], SS[f]['e'], 2)) or 'empty'} (o(0) {SS[f]['o'][0] / SS[f]['e'][0]:+.2f}, o(1) {SS[f]['o'][-1] / SS[f]['e'][-1]:+.2f} sigma); ten-population {fmt(I2s[f])}" for f in FOOTS),
      True, load_bearing=False)
SH = {}
for d in (-0.2, +0.2):
    gs = {n: GUSE[n] + d for n in NAMES}
    SH[d] = {f: inter(scan(f, gs), f, 2) for f in FOOTS}
check("R4 (reported) the ten-population 2-sigma intersection with every gamma_i shifted by -0.2 / +0.2",
      "; ".join(f"{d:+.1f}: " + ", ".join(f"{f} {fmt(v[f])}" for f in FOOTS) for d, v in SH.items()), True, load_bearing=False)

reading = ("with the published slopes one debris fraction fits all ten populations at 2 sigma; the clause 'and not with dynamical SLUGGS masses' is superseded"
           if h1 else ("mixed: non-empty on one footing only" if any(I2[f] is not None for f in FOOTS) else
                       "with the published slopes the 2-sigma intersection stays empty; the clause stands"))
P(f"\n    READING (declared): {reading}")
R.num("gamma", GUSE)
R.num("U5d", {f: dict(phi=GRID.tolist(), o=SC[f]["o"].tolist(), e=SC[f]["e"].tolist(), nexcl=SC[f]["nexcl"]) for f in FOOTS})
R.num("U5s", {f: dict(o=SS[f]["o"].tolist(), e=SS[f]["e"].tolist()) for f in FOOTS})
R.num("I2", I2); R.num("I1_I3", I13); R.num("I2_own", I2s); R.num("R4", {str(d): v for d, v in SH.items()}); R.num("bind", bind); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
