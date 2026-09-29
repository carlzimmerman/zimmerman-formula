#!/usr/bin/env python3
"""CFG111 -- DOES THE SLUGGS DEFICIT SURVIVE PUBLISHED PER-GALAXY GC DENSITY SLOPES?  CFG55's JAM-calibrated SLUGGS test with each
galaxy's GC density slope gamma_i from Alabi et al. 2017's literature relation instead of the fixed gamma = 3 (CFG76: the law's offset
is zero at gamma ~ 1.83, the rule's at ~ 2.45).

Criteria frozen and committed before any number: campaign_fresh_gravity/CFG111_FROZEN_CRITERIA.md (d36b680bb).
  slopes   gamma_i = clip(-0.63 log10 M*_SLUGGS,i + 9.81, 2, 4) (Alabi+2017, MNRAS 468, 3949, from a literature compilation of GC density
           profiles); reproduces its Table 1 to 0.01 (C2).  A literature calibration, not a fit to the dispersions.
  machinery CFG55's pipeline exec'd read-only (h50's GC bins and isotropic Jeans solution, CFG55's JAM calibration, the rule's debris);
           only gamma in sigma_r2 / sigma_los changes, per galaxy.  The calibrated masses do not depend on gamma.  CFG55's 16 galaxies.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  with gamma_i = 3 for every galaxy the per-galaxy machinery reproduces CFG55's committed offsets (law and rule, canonical)
               per galaxy to 1e-9, and the means +0.0970 / +0.0456.
  C2  CONTROL  the relation reproduces Alabi+2017's Table 1 values (quoted in the frozen file) to 0.01 for all 18 galaxies.
  H1  [HEADLINE; MUTATE must fail] with the literature slopes the law's JAM-calibrated SLUGGS deficit survives: mean > 2 sigma, both footings.
  H2  with the same slopes the rule fits: |mean| < 2 sigma, both footings.
  R1-R4 (reported): SLUGGS population masses; gamma_i +-0.2 / +-0.4; the per-galaxy gamma that nulls the law's offset; the four
               group/cluster centrals excluded.
MUTATE=1: gamma_i = 1.83 for every galaxy (CFG76's zero point for the law) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG111_sluggs_literature_gamma.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG111_sluggs_literature_gamma", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: gamma_i = 1.83 for every galaxy -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG55_sluggs_dynamical_masses.py")).read()
g55 = {"__file__": os.path.join(HERE, "CFG55_sluggs_dynamical_masses.py"), "__name__": "cfg55"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("\nRES = {}\n")], "CFG55", "exec"), g55)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
G16, law_mass_g, rule_mass, debris = g55["G16"], g55["law_mass_g"], g55["rule_mass"], g55["debris"]
sigma_r2, sigma_los, nu_h, offset55, GAMMA = g55["sigma_r2"], g55["sigma_los"], g55["nu_h"], g55["offset"], g55["GAMMA"]
A0SI, G_, KPC, MSUN, FB, nfw_enclosed, SL = g55["A0SI"], g55["G_"], g55["KPC"], g55["MSUN"], g55["FB"], g55["nfw_enclosed"], g55["SL"]
NAMES = [g["name"] for g in G16]


def gamma_rel(lm):
    return min(max(-0.63 * lm + 9.81, 2.0), 4.0)


def logM(name):
    key = "NGC" + str(int(name[3:]))
    return float(SL[key]["logM*"])


GLIT = {n: gamma_rel(logM(n)) for n in NAMES}
GUSE = {n: (1.83 if MUTATE else GLIT[n]) for n in NAMES}


def sigma_pred_g(g, foot, Ms, which, gam):
    r = g["r"]; a0 = A0SI[foot]; a_h = r["Re"] / 1.8153
    fx, Mh = debris(Ms, foot) if which == "rule" else (0.0, 1.0)

    def gf(rr):
        Mb = Ms * MSUN * rr ** 2 / (rr + a_h) ** 2; gN = G_ * Mb / (rr * KPC) ** 2
        out = gN * nu_h(gN / a0)
        if fx > 0:
            out = out + fx * (1 - FB) * G_ * np.asarray(nfw_enclosed(Mh, rr), float) * MSUN / (rr * KPC) ** 2
        return out
    return sigma_los(r["Rb"], sigma_r2(gf, gam), gam), fx


def offset_g(g, foot, Ms, which, gam):
    s, fx = sigma_pred_g(g, foot, Ms, which, gam); r = g["r"]
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s[r["out"]])))


def sample_g(foot, masses, which, gams, keep=lambda g: True):
    off = np.array([offset_g(g, foot, m, which, gams[g["name"]]) for g, m in zip(G16, masses) if np.isfinite(m) and keep(g)])
    return off, float(off.mean()), float(off.std(ddof=1) / math.sqrt(len(off)))


MASS = {f: dict(law=[law_mass_g(g, f) for g in G16], rule=[rule_mass(g, f) for g in G16], sl=[g["r"]["Mstar"] for g in G16]) for f in FOOTS}

# ================================================================== C1 / C2
R.banner("C1 / C2  CONTROLS")
c55 = json.load(open(os.path.join(HERE, "CFG55_sluggs_dynamical_masses_results.json")))["numbers"]["RES"]["canonical"]
G3 = {n: float(GAMMA) for n in NAMES}
dev = 0.0
for which in ("law", "rule"):
    ms = MASS["canonical"][which]
    mine = np.array([offset_g(g, "canonical", m, which, G3[g["name"]]) for g, m in zip(G16, ms)])
    theirs = np.array([offset55(g, "canonical", m, which)[0] for g, m in zip(G16, ms)])
    dev = max(dev, float(np.max(np.abs(mine - theirs))))
m3l = sample_g("canonical", MASS["canonical"]["law"], "law", G3)[1]; m3r = sample_g("canonical", MASS["canonical"]["rule"], "rule", G3)[1]
check("C1 CONTROL: with gamma = 3 for every galaxy the per-galaxy machinery reproduces CFG55's offsets per galaxy (law, rule; canonical) to 1e-9 and the committed means",
      f"max |d offset| {dev:.1e}; means law {m3l:+.6f} (committed {c55['law']['mean']:+.6f}), rule {m3r:+.6f} (committed {c55['rule']['mean']:+.6f}); global GAMMA = {GAMMA}",
      dev < 1e-9 and abs(m3l - c55["law"]["mean"]) < 1e-9 and abs(m3r - c55["rule"]["mean"]) < 1e-9)
QUOTED = {720: 2.71, 821: 2.88, 1023: 2.89, 2768: 2.75, 3377: 3.20, 3607: 2.63, 4278: 2.91, 4365: 2.56, 4374: 2.56, 4459: 2.89, 4473: 2.91,
          4486: 2.49, 4494: 2.87, 4526: 2.72, 4649: 2.50, 4697: 2.79, 5846: 2.59, 7457: 3.43}
d2 = max(abs(round(gamma_rel(float(SL["NGC" + str(n)]["logM*"])), 2) - v) for n, v in QUOTED.items())
check("C2 CONTROL: the relation reproduces Alabi+2017's Table 1 values (quoted in the frozen file) to 0.01 for all 18 galaxies",
      f"max |difference| {d2:.3f}; gamma_i for the 16: " + ", ".join(f"{n[3:]} {GLIT[n]:.2f}" for n in NAMES), d2 < 0.005 + 1e-9)

# ================================================================== H1 / H2
R.banner("H1 / H2  THE JAM-CALIBRATED SLUGGS TEST WITH PER-GALAXY LITERATURE SLOPES")
RES = {}
for f in FOOTS:
    RES[f] = dict(law=sample_g(f, MASS[f]["law"], "law", GUSE), rule=sample_g(f, MASS[f]["rule"], "rule", GUSE))
for i, n in enumerate(NAMES):
    P(f"    {n}  gamma {GUSE[n]:.2f}: law {RES['canonical']['law'][0][i]:+.3f}  rule {RES['canonical']['rule'][0][i]:+.3f}")
zl = {f: RES[f]["law"][1] / RES[f]["law"][2] for f in FOOTS}
zr = {f: RES[f]["rule"][1] / RES[f]["rule"][2] for f in FOOTS}
check("H1 [HEADLINE] WITH THE LITERATURE SLOPES THE LAW'S JAM-CALIBRATED SLUGGS DEFICIT SURVIVES: mean > 2 sigma, both footings"
      + ("  [MUTATE: gamma = 1.83]" if MUTATE else ""),
      "; ".join(f"{f}: {RES[f]['law'][1]:+.4f} +- {RES[f]['law'][2]:.4f} ({zl[f]:+.2f} sigma)" for f in FOOTS)
      + f"  [gamma = 3 (CFG55): +0.0970, 3.99 sigma]", all(zl[f] > 2 for f in FOOTS))
check("H2 WITH THE SAME SLOPES THE RULE FITS: |mean| < 2 sigma, both footings",
      "; ".join(f"{f}: {RES[f]['rule'][1]:+.4f} +- {RES[f]['rule'][2]:.4f} ({zr[f]:+.2f} sigma)" for f in FOOTS)
      + f"  [gamma = 3 (CFG55): +0.0456, 2.58 sigma]", all(abs(zr[f]) < 2 for f in FOOTS))

# ================================================================== reported rows (canonical)
R.banner("REPORTED ROWS (canonical)")
sl_l = sample_g("canonical", MASS["canonical"]["sl"], "law", GUSE); sl_r = sample_g("canonical", MASS["canonical"]["sl"], "rule", GUSE)
check("R1 (reported) SLUGGS population masses with the same slopes",
      f"law {sl_l[1]:+.4f} +- {sl_l[2]:.4f} ({sl_l[1] / sl_l[2]:+.2f} sigma); rule {sl_r[1]:+.4f} +- {sl_r[2]:.4f} ({sl_r[1] / sl_r[2]:+.2f} sigma)",
      True, load_bearing=False)
sh = {}
for d in (-0.4, -0.2, +0.2, +0.4):
    gs = {n: GUSE[n] + d for n in NAMES}
    sh[d] = (sample_g("canonical", MASS["canonical"]["law"], "law", gs), sample_g("canonical", MASS["canonical"]["rule"], "rule", gs))
check("R2 (reported) every gamma_i shifted by -0.4 / -0.2 / +0.2 / +0.4",
      "; ".join(f"{d:+.1f}: law {v[0][1]:+.4f} ({v[0][1] / v[0][2]:+.2f}), rule {v[1][1]:+.4f} ({v[1][1] / v[1][2]:+.2f})" for d, v in sh.items()),
      True, load_bearing=False)
nul = []
for g, m in zip(G16, MASS["canonical"]["law"]):
    fz = lambda gm, g=g, m=m: offset_g(g, "canonical", m, "law", gm)
    try:
        gz = brentq(fz, 1.0, 4.5, xtol=1e-4); nul.append((g["name"], gz))
    except ValueError:
        nul.append((g["name"], float("nan")))
check("R3 (reported) per galaxy: the gamma that would null the law's offset, beside its literature gamma_i",
      "; ".join(f"{n[3:]} {gz:.2f} (lit {GLIT[n]:.2f})" for n, gz in nul), True, load_bearing=False)
CENT = {"NGC4486", "NGC4365", "NGC4374", "NGC5846"}
nc_l = sample_g("canonical", MASS["canonical"]["law"], "law", GUSE, keep=lambda g: g["name"] not in CENT)
nc_r = sample_g("canonical", MASS["canonical"]["rule"], "rule", GUSE, keep=lambda g: g["name"] not in CENT)
check("R4 (reported) the four group/cluster centrals (M87, NGC 4365, NGC 4374, NGC 5846) excluded",
      f"N = {len(nc_l[0])}: law {nc_l[1]:+.4f} ({nc_l[1] / nc_l[2]:+.2f} sigma); rule {nc_r[1]:+.4f} ({nc_r[1] / nc_r[2]:+.2f} sigma)", True, load_bearing=False)

h1 = all(zl[f] > 2 for f in FOOTS)
reading = ("the gamma caveat does not rescue the law: with the published slopes (2.5-3.4) the deficit remains" if h1 else
           "with the published slopes the law's deficit falls below 2 sigma: the SLUGGS failure was an artefact of gamma = 3")
reading += ("; the rule fits" if all(abs(zr[f]) < 2 for f in FOOTS) else "; the rule does not fit")
P(f"\n    READING (declared): {reading}")
R.num("gamma", GUSE); R.num("RES", {f: {w: dict(mean=v[1], err=v[2], per=v[0].tolist()) for w, v in RES[f].items()} for f in FOOTS})
R.num("R1", dict(law=sl_l[1:], rule=sl_r[1:])); R.num("R2", {str(d): [v[0][1], v[0][2], v[1][1], v[1][2]] for d, v in sh.items()})
R.num("R3", dict(nul)); R.num("R4", dict(law=nc_l[1:], rule=nc_r[1:])); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
