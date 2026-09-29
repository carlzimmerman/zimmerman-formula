#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG53 -- THE MASSIVE PASSIVE DISKS BY SHAPE: does the outer rotation curve of a massive red disk rise, as B's derived cold-mass rule says
it must, or keep the law's shape?

WHY.  CFG41 scored Di Teodoro+2023's 15 massive HI disks (four S0 / S0a) by the AMPLITUDE of the flat part and could not separate the law
from the rule: the 0.2-dex stellar-mass systematic enters the rule steeply through the collapse mass (the rule's error on the four is
0.131 dex), and the sample's cut on HI width biases every amplitude high (B = 0.076 +- 0.030).  The rule's debris is an NFW component
of the collapse mass, and inside 30-97 kpc an NFW circular speed RISES, while the law's outer curve is flat or gently falling.  The SHAPE
of the outer curve (its logarithmic slope) is nearly blind to the stellar-mass normalisation under the law, fully blind to distance
under the law (x_N = G M_b / R^2 a0 does not move when D does), and a cut on the flat SPEED does not select on it directly.  The rule makes
debris for RED disks only (CFG36; CFG41 printed f_ex = 0 for every blue galaxy of this sample), so the red-minus-blue slope difference
cancels what the two colours share (tilted-ring fitting, warps, beam, the estimator, the width cut).

THE METHOD (declared before this script's first run).  CFG41's machinery exec'd read-only: the data, the colour convention (RC3 T <= 0 red),
CFG36's collapse masses, the conservation form at x_e = 0.40, nu_mono, point-mass baryons with sphere / Freeman brackets at R_d = 8 kpc.
Outer curve: the points with R >= R_max / 2 (every galaxy has >= 4).  Slope: weighted least squares of ln V on ln R, weights (V / dV)^2,
formal error x sqrt(2) (adjacent tilted rings share the beam).  Predicted slopes: the SAME estimator with the SAME weights applied to the
law's and the rule's speeds at the same radii.  Per galaxy r_i = s_obs - s_law (the observed slope relative to the law) and
p_i = s_rule - s_law (the rule's predicted excess).  Groups: red (T <= 0) and blue (the rest); inverse-variance means with the
observational errors, each group's error scaled by sqrt(chi2 / dof) when that exceeds 1.  D_obs = <r>_red - <r>_blue and
D_rule = <p>_red - <p>_blue (same weights); the law predicts D = 0.  Systematics, each applied COHERENTLY to every galaxy, as half the
spread of the quantity tested: the baryon model (point / sphere / Freeman), M_* +-0.2 dex, M_gas +-0.1 dex, distance +-dD (the paper's;
moves R and M_b together).  sigma = the statistical error and the systematics in quadrature.

PRE-DECLARED
  C1  CONTROL  the data as CFG41 read them: 15 galaxies, 216 points; red (T <= 0) = NGC 1167, NGC 5790, UGC 12591, UGC 12811.
  C2  CONTROL  CFG41's committed four-S0 amplitude numbers reproduced by the exec'd machinery (rule -0.105, law +0.004; to 1e-9), and this
               script's radius-resolved speed equal to CFG41's at CFG41's radius for every galaxy, both predictions, three models (to 1e-9).
  C3  CONTROL  the slope estimator: a flat curve gives 0 and a power law R^0.1 gives 0.1 at every galaxy's radii (to 1e-12).
  H1  THE LAW FITS THE BLUE SHAPES: |<r>_blue| < 2 sigma, canonical.
  H2  [HEADLINE; MUTATE must fail] THE RED DISKS' SHAPE REJECTS THE RULE'S DEBRIS: (D_obs - D_rule) / sigma < -2 on both footings.
  H3  THE TEST HAS POWER: D_rule / sigma >= 2, canonical (the rule's and the law's predicted shapes differ by 2 sigma).
  R1-R5 (reported): per-galaxy table; the absolute red test (<r>_red against <p>_red and against 0); the WISE colours (W2-W3 < 2.0 red);
      the two flagged galaxies (NGC 5635, UGC 12591) removed; amplitude and shape together for the four (Stouffer of CFG41's rule z and
      this script's absolute red rule z).
  READING (declared): H3 FAIL -> the shape cannot decide either.  H3 PASS and H2 PASS -> massive passive disks do not rise as the rule's
      debris requires: the derived rule is rejected on its own population by a test blind to the stellar-mass normalisation.  H3 PASS and
      H2 FAIL -> the shape does not reject the rule; if D_obs also sits > 2 sigma above 0, the shape favours the rule over the law.
MUTATE=1: every galaxy's observed speeds multiplied by v_rule / v_law (canonical, nominal) at each radius -- the data made to carry the
rule's shape (the factor is 1 wherever f_ex = 0) -- H2 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG53_passive_disk_shapes.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, json, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG53_passive_disk_shapes", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: observed speeds x v_rule / v_law (canonical, nominal) -- H2 must FAIL ***")
FOOTS = ("canonical", "alt")

# ------------------------------------------------------------------ CFG41's machinery, read-only (its own MUTATE forced off)
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG41_massive_spirals_hi.py")).read()
g41 = {"__file__": os.path.join(HERE, "CFG41_massive_spirals_hi.py"), "__name__": "cfg41"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("\nRES = {}\n")], "CFG41", "exec"), g41)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
GALS, PTS, TAB = g41["GALS"], g41["PTS"], g41["TAB"]
gN, colour_of, pred41, stat41 = g41["gN"], g41["colour_of"], g41["pred"], g41["stat"]
collapse, edge_phantom, nfw_enclosed, FB = g41["collapse"], g41["edge_phantom"], g41["nfw_enclosed"], g41["FB"]
G_, KPC, MSUN, A0SI = g41["G_"], g41["KPC"], g41["MSUN"], g41["A0SI"]
RED = lambda g, wise=False: colour_of(g, wise) == "red"


def vpred(g, foot, Rk, model="point", which="rule", wise=False, dMs=0.0, dMg=0.0, sD=0):
    """CFG41's pred() at an arbitrary radius Rk (kpc as tabulated); sD = +-1 moves the distance by the paper's dD (R and M_b together)."""
    t = TAB[g["name"]]; fD = 1.0 + sD * float(t["dD"]) / float(t["D_Mpc"])
    a0 = A0SI[foot]; r = Rk * fD
    Ms = 10 ** (g["lMs"] + dMs) * fD ** 2; Mb = Ms + 10 ** (g["lMg"] + dMg) * fD ** 2
    gn = gN(Mb, r, model)
    gl = float(C.nu_mono(np.array([gn / a0]))[0]) * gn
    fex = 0.0
    if which == "rule":
        Mh = collapse(Ms, colour_of(g, wise)); fex = max(0.0, 1.0 - edge_phantom(Mb, foot, 0.40) / ((1 - FB) * Mh))
        gl += fex * (1 - FB) * float(nfw_enclosed(Mh, r)) * G_ * MSUN / (r * KPC) ** 2
    return math.sqrt(gl * r * KPC) / 1e3, fex


def outer(g):
    pts = sorted(PTS[g["name"]]); rmax = pts[-1][0]
    o = [p for p in pts if p[0] >= rmax / 2]
    return np.array(o if len(o) >= 3 else pts[-3:])


def wls(x, y, w):
    xb, yb = np.sum(w * x) / np.sum(w), np.sum(w * y) / np.sum(w)
    sxx = np.sum(w * (x - xb) ** 2)
    return float(np.sum(w * (x - xb) * (y - yb)) / sxx), float(math.sqrt(1.0 / sxx))


# ------------------------------------------------------------------ C1-C3
R.banner("C1-C3  CONTROLS")
reds = [g["name"] for g in GALS if RED(g)]
check("C1 CONTROL: the data as CFG41 read them: 15 galaxies, 216 points; red (T <= 0) = NGC 1167, NGC 5790, UGC 12591, UGC 12811",
      f"{len(GALS)} galaxies, {sum(len(v) for v in PTS.values())} points; red {reds}",
      len(GALS) == 15 and sum(len(v) for v in PTS.values()) == 216 and sorted(reds) == ["NGC1167", "NGC5790", "UGC12591", "UGC12811"])
c41 = json.load(open(os.path.join(HERE, "CFG41_massive_spirals_hi_results.json")))["numbers"]["RES"]
S0 = lambda g: g["T"] is not None and g["T"] <= 0
rep = {w: stat41("canonical", w, sel=S0)["corr"] for w in ("rule", "law")}
dev = max(abs(pred41(g, f, model=m, which=w)[0] - vpred(g, f, g["Rm"], model=m, which=w)[0])
          for g in GALS for f in FOOTS for w in ("law", "rule") for m in ("point", "sphere", "freeman"))
check("C2 CONTROL: CFG41's four-S0 numbers reproduced (rule -0.105, law +0.004) and the radius-resolved speed equals CFG41's at its radius",
      f"rule {rep['rule']:+.6f} (committed {c41['canonical|rule|s0']['corr']:+.6f}), law {rep['law']:+.6f} "
      f"(committed {c41['canonical|law|s0']['corr']:+.6f}); max speed difference {dev:.1e} km/s",
      abs(rep["rule"] - c41["canonical|rule|s0"]["corr"]) < 1e-9 and abs(rep["law"] - c41["canonical|law|s0"]["corr"]) < 1e-9 and dev < 1e-9)
c3 = max(max(abs(wls(np.log(o[:, 0]), np.zeros(len(o)), (o[:, 1] / o[:, 2]) ** 2)[0]),
             abs(wls(np.log(o[:, 0]), 0.1 * np.log(o[:, 0]), (o[:, 1] / o[:, 2]) ** 2)[0] - 0.1)) for o in map(outer, GALS))
check("C3 CONTROL: the slope estimator returns 0 for a flat curve and 0.1 for R^0.1 at every galaxy's radii", f"max error {c3:.1e}", c3 < 1e-12)

# ------------------------------------------------------------------ the slopes
MUTF = {}
if MUTATE:
    for g in GALS:
        o = outer(g)
        MUTF[g["name"]] = np.array([vpred(g, "canonical", r, which="rule")[0] / vpred(g, "canonical", r, which="law")[0] for r in o[:, 0]])


def slopes(foot, wise=False, **var):
    """per galaxy: observed slope and error, the law's and the rule's slope by the same estimator, the rule's f_ex at the outermost point."""
    out = {}
    for g in GALS:
        o = outer(g); Rr, V, dV = o[:, 0], o[:, 1].copy(), o[:, 2]
        if MUTATE:
            V = V * MUTF[g["name"]]
        w = (o[:, 1] / dV) ** 2; x = np.log(Rr)
        so, eo = wls(x, np.log(V), w)
        sl = wls(x, np.log([vpred(g, foot, r, which="law", wise=wise, **var)[0] for r in Rr]), w)[0]
        rr = [vpred(g, foot, r, which="rule", wise=wise, **var) for r in Rr]
        sr = wls(x, np.log([q[0] for q in rr]), w)[0]
        out[g["name"]] = dict(s=so, e=eo * math.sqrt(2), law=sl, rule=sr, fex=rr[-1][1], n=len(o), R0=float(Rr[0]), R1=float(Rr[-1]),
                              red=RED(g, wise))
    return out


def gmean(vals, errs, pvals):
    w = 1.0 / np.asarray(errs) ** 2; v = np.asarray(vals)
    m = float(np.sum(w * v) / np.sum(w)); e = float(1.0 / math.sqrt(np.sum(w)))
    dof = len(v) - 1; chi2 = float(np.sum(w * (v - m) ** 2))
    b = max(1.0, math.sqrt(chi2 / dof)) if dof > 0 else 1.0
    return m, e * b, float(np.sum(w * np.asarray(pvals)) / np.sum(w)), chi2, dof


def groups(S, keep=lambda n: True):
    res = {}
    for col in ("red", "blue"):
        names = [n for n, v in S.items() if (v["red"] == (col == "red")) and keep(n)]
        r = [S[n]["s"] - S[n]["law"] for n in names]; e = [S[n]["e"] for n in names]; p = [S[n]["rule"] - S[n]["law"] for n in names]
        m, em, pm, chi2, dof = gmean(r, e, p)
        res[col] = dict(names=names, r=m, e=em, p=pm, chi2=chi2, dof=dof)
    res["Dobs"] = res["red"]["r"] - res["blue"]["r"]; res["Drule"] = res["red"]["p"] - res["blue"]["p"]
    res["estat"] = math.sqrt(res["red"]["e"] ** 2 + res["blue"]["e"] ** 2)
    return res


VARS = {"model": [dict(model=m) for m in ("point", "sphere", "freeman")], "M_*": [dict(dMs=+0.2), dict(dMs=-0.2)],
        "M_gas": [dict(dMg=+0.1), dict(dMg=-0.1)], "distance": [dict(sD=+1), dict(sD=-1)]}


def analyse(foot, wise=False, keep=lambda n: True):
    S = slopes(foot, wise); G = groups(S, keep)
    q = {"Dobs-Drule": lambda G_: G_["Dobs"] - G_["Drule"], "Dobs": lambda G_: G_["Dobs"], "Drule": lambda G_: G_["Drule"],
         "blue": lambda G_: G_["blue"]["r"], "red-rule": lambda G_: G_["red"]["r"] - G_["red"]["p"], "red": lambda G_: G_["red"]["r"]}
    sysv = {k: {} for k in q}
    for fam, vs in VARS.items():
        Gv = [groups(slopes(foot, wise, **v), keep) for v in vs]
        for k, fn in q.items():
            vals = [fn(x) for x in Gv]; sysv[k][fam] = 0.5 * (max(vals) - min(vals))
    sy = {k: math.sqrt(sum(x ** 2 for x in v.values())) for k, v in sysv.items()}
    sig = math.sqrt(G["estat"] ** 2 + sy["Dobs-Drule"] ** 2)
    sigL = math.sqrt(G["estat"] ** 2 + sy["Dobs"] ** 2)
    sigB = math.sqrt(G["blue"]["e"] ** 2 + sy["blue"] ** 2)
    sigRr = math.sqrt(G["red"]["e"] ** 2 + sy["red-rule"] ** 2); sigRl = math.sqrt(G["red"]["e"] ** 2 + sy["red"] ** 2)
    return dict(S=S, G=G, sys=sysv, sy=sy, sig=sig, z2=(G["Dobs"] - G["Drule"]) / sig, zlaw=G["Dobs"] / sigL, z3=G["Drule"] / sig,
                z1=G["blue"]["r"] / sigB, zred_rule=(G["red"]["r"] - G["red"]["p"]) / sigRr, zred_law=G["red"]["r"] / sigRl)


A = {f: analyse(f) for f in FOOTS}
R.banner("PER GALAXY (canonical): outer slope d ln V / d ln R, observed vs the law and the rule (same estimator, same radii)")
S = A["canonical"]["S"]
for g in GALS:
    s = S[g["name"]]
    P(f"    {g['name']:9s} {'red ' if s['red'] else 'blue'} {s['n']:2d} pts {s['R0']:5.1f}-{s['R1']:5.1f} kpc: obs {s['s']:+.3f} +- {s['e']:.3f}; "
      f"law {s['law']:+.3f}; rule {s['rule']:+.3f} (f_ex {s['fex']:.2f}); obs - law {s['s'] - s['law']:+.3f}")
for f in FOOTS:
    a = A[f]; G = a["G"]
    P(f"\n    {f}: red <r> {G['red']['r']:+.4f} +- {G['red']['e']:.4f} (chi2 {G['red']['chi2']:.1f}/{G['red']['dof']}), rule predicts "
      f"{G['red']['p']:+.4f}; blue <r> {G['blue']['r']:+.4f} +- {G['blue']['e']:.4f} (chi2 {G['blue']['chi2']:.1f}/{G['blue']['dof']}), "
      f"rule predicts {G['blue']['p']:+.4f}")
    P(f"    {f}: D_obs {G['Dobs']:+.4f}, D_rule {G['Drule']:+.4f}; stat {G['estat']:.4f}; syst (D_obs - D_rule) " +
      ", ".join(f"{k} {v:.4f}" for k, v in a["sys"]["Dobs-Drule"].items()) + f" -> sigma {a['sig']:.4f}")
    P(f"    {f}: (D_obs - D_rule)/sigma {a['z2']:+.2f}; D_obs/sigma_law {a['zlaw']:+.2f}; D_rule/sigma {a['z3']:+.2f}; blue <r>/sigma {a['z1']:+.2f}")

# ------------------------------------------------------------------ H1-H3
R.banner("H1-H3")
c = A["canonical"]
check("H1 THE LAW FITS THE BLUE SHAPES: |<r>_blue| < 2 sigma, canonical",
      f"<r>_blue {c['G']['blue']['r']:+.4f} -> {c['z1']:+.2f} sigma", abs(c["z1"]) < 2)
check("H2 [HEADLINE] THE RED DISKS' SHAPE REJECTS THE RULE'S DEBRIS: (D_obs - D_rule)/sigma < -2 on both footings"
      + ("  [MUTATE: speeds x v_rule/v_law]" if MUTATE else ""),
      "; ".join(f"{f}: D_obs {A[f]['G']['Dobs']:+.4f} vs D_rule {A[f]['G']['Drule']:+.4f} -> {A[f]['z2']:+.2f} sigma" for f in FOOTS),
      all(A[f]["z2"] < -2 for f in FOOTS))
check("H3 THE TEST HAS POWER: D_rule / sigma >= 2, canonical", f"D_rule {c['G']['Drule']:+.4f}, sigma {c['sig']:.4f} -> {c['z3']:+.2f}",
      c["z3"] >= 2)

# ------------------------------------------------------------------ R rows
R.banner("R2-R5 (reported)")
for f in FOOTS:
    a = A[f]
    check(f"R2 (reported, {f}) the absolute red test: <r>_red against the rule's <p>_red and against the law's 0",
          f"<r>_red {a['G']['red']['r']:+.4f} vs rule {a['G']['red']['p']:+.4f}: {a['zred_rule']:+.2f} sigma; vs law 0: {a['zred_law']:+.2f} sigma",
          True, load_bearing=False)
Aw = analyse("canonical", wise=True)
check("R3 (reported) the WISE colours (W2-W3 < 2.0 red), canonical",
      f"red = {Aw['G']['red']['names']}; D_obs {Aw['G']['Dobs']:+.4f}, D_rule {Aw['G']['Drule']:+.4f}: (D_obs - D_rule)/sigma {Aw['z2']:+.2f}; "
      f"power {Aw['z3']:+.2f}", True, load_bearing=False)
Af = analyse("canonical", keep=lambda n: n not in ("NGC5635", "UGC12591"))
check("R4 (reported) the two flagged galaxies (NGC 5635, UGC 12591) removed, canonical",
      f"D_obs {Af['G']['Dobs']:+.4f}, D_rule {Af['G']['Drule']:+.4f}: (D_obs - D_rule)/sigma {Af['z2']:+.2f}; power {Af['z3']:+.2f}",
      True, load_bearing=False)
zamp = c41["canonical|rule|s0"]["z"]
check("R5 (reported) amplitude (CFG41) and shape together for the four red disks, against the rule (Stouffer)",
      f"CFG41 amplitude z {zamp:+.2f}; shape (absolute red vs rule) z {c['zred_rule']:+.2f}; combined {(zamp + c['zred_rule']) / math.sqrt(2):+.2f}",
      True, load_bearing=False)

h2, h3 = all(A[f]["z2"] < -2 for f in FOOTS), c["z3"] >= 2
if not h3:
    reading = "the shape cannot decide either: the rule's predicted red-blue slope difference is under 2 sigma"
elif h2:
    reading = ("massive passive disks do not rise as the rule's debris requires: the derived rule is rejected on its own population by a "
               "test blind to the stellar-mass normalisation")
else:
    reading = ("the shape does not reject the rule" + ("; D_obs sits > 2 sigma above 0, so the shape favours the rule over the law"
                                                         if c["zlaw"] > 2 else ""))
P(f"\n    READING (declared): {reading}")
R.num("slopes", {f: A[f]["S"] for f in FOOTS})
R.num("groups", {f: {k: v for k, v in A[f]["G"].items()} for f in FOOTS})
R.num("sys", {f: A[f]["sys"] for f in FOOTS})
R.num("z", {f: {k: A[f][k] for k in ("sig", "z1", "z2", "z3", "zlaw", "zred_rule", "zred_law")} for f in FOOTS})
R.num("R3_wise", {k: Aw[k] for k in ("z2", "z3")}); R.num("R4_noflag", {k: Af[k] for k in ("z2", "z3")})
R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
