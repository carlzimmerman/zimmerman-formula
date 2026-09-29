#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG41 -- THE MASSIVE PASSIVE DISKS, at last: Di Teodoro+2023's 15 extremely massive spirals with extended HI rotation curves, under B's law and
B's derived cold-mass rule.

WHY.  CFG37 found that the rule bites only above log M_* ~ 11.2 on the red sequence, and that no passive disk with extended kinematics above
that mass was in the repository ('none is in the repository').  Di Teodoro et al. 2023 (MNRAS 518, 6340; arXiv:2207.02906) measured HI rotation
curves out to 30-97 kpc for 15 galaxies with log M_* 11.0-11.7 (WISE), including four S0 / S0a (NGC 1167, NGC 5790, UGC 12591, UGC 12811) --
exactly the population.  CFG40 (Ogle+2019, star-forming super spirals) found the law slightly slow at the top of the disk mass function; this
sample is the HI cross-check.  The curves are not tabulated; they were read from the paper's vector atlas figures (data file with provenance).

A SELECTION BIAS THAT CUTS ONE WAY.  The sample was selected on speed: SDSS M_* > 1e11 and ALFALFA inclination-corrected HI width > 300 km/s.  A cut on
the observed speed picks upward fluctuations at fixed mass, so the raw mean of log(v_obs / v_law) is biased HIGH.  CFG41_selbias_mc.py (a
Monte-Carlo, all choices declared in its docstring) gives +0.067 to +0.085 dex where the mock reproduces the real sample's mean v_flat (~290
km/s) and mass (log M_* ~ 11.25), and +0.003 to +0.154 dex across its whole grid.  The correction used here is B = 0.076 +- 0.030 dex
(matched-grid centre; the error covers the matched rows' spread and the mass-function variants).  It is subtracted from every offset; its error
enters the floor.

THE METHOD (declared before this script's first run).  CFG36's machinery exec'd read-only (Mandelbaum's blue / red relation as M_200c; Dutton-Maccio
NFW; the conservation form at x_e = 0.40; nu_mono; both footings).  Baryons: M_* (WISE W1, Upsilon = 0.6, the paper's; stands in for Mandelbaum's
Chabrier masses) + M_gas (1.36 M_HI, the paper's).  Velocity: the paper's tabulated v_flat with its error.  Radius: the mean galactocentric radius of the
points the Lelli+2016 flat-part algorithm includes (recomputed here from the recovered points; the control checks it).  Structure: point mass
(headline; the flat parts lie at 15-97 kpc, well outside the discs) with brackets -- an exponential disc (Freeman) and the spherical enclosed mass, both at
R_d = 8 kpc (the paper gives no R_d).  Colour: CFG36's convention on RC3 type T (T <= 0 red; T >= 1 or no T blue).  Offset = log10(v_flat / v_pred) - B.
Sample: mean over the 15 with the galaxy-to-galaxy error (std / sqrt N), plus a floor in quadrature: the baryon-structure model (half the spread of the
mean), the stellar mass (+-0.2 dex), the gas mass (+-0.1 dex, the paper's), the radius (mean flat radius +-25%) and B's error (0.030).

PRE-DECLARED
  C1  CONTROL  the data: 15 galaxies, 216 points; the table's v_flat for NGC 5440 is 303 +- 25.
  C2  CONTROL  the Lelli+2016 algorithm applied to the recovered points reproduces the paper's tabulated v_flat within 3 km/s for >= 12 of 15
               galaxies (the recovered points are faithful to the paper's own analysis).
  H1  THE BARE LAW FITS THEM after the selection correction: |mean(log v_obs/v_law - B)| < 2 sigma, canonical.
  H2  [HEADLINE; MUTATE must fail] B (law + rule, canonical) FITS THEM: (a) |mean(log v_obs/v_B - B)| < 2 sigma over the 15, AND (b) over the four S0 / S0a
      (T <= 0) the rule does not over-predict: mean(log v_obs/v_B - B) > -2 sigma_S0 with sigma_S0 = the four's own std / 2 with the floor in quadrature.
  H3  THE RULE BITES: f_ex > 0 in at least 2 of the 4 S0 / S0a (otherwise the passive-disk test of the rule is empty, as CFG37's H2 was).
  R1-R6 (reported): uncorrected offsets; the alt footing; the WISE colour assignment (W2-W3 < 2.0 red); the two galaxies the paper flags as
      uncertain (NGC 5635, UGC 12591) excluded; per-galaxy table; the brackets.
  READING (declared): H1, H2, H3 PASS -> the derived rule fits the first massive passive disks (log M_* 11.3-11.7) while the law fits the rest, on the HI tracer.
      H2b FAIL -> the rule over-predicts massive passive disks (the CFG36/UGC 2487 worry, now on four).  H3 FAIL -> the four do not test the rule.
      H1 FAIL -> the law fails on these massive disks even after the selection correction.
MUTATE=1: the observed speeds multiplied by 0.5 -- H2 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG41_massive_spirals_hi.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib
import numpy as np
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG41_massive_spirals_hi", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: observed speeds x 0.5 -- H2 must FAIL ***")
VF = 0.5 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
BIAS, DBIAS = 0.076, 0.030

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG36_colour_split_collapse.py")).read()
g36 = {"__file__": os.path.join(HERE, "CFG36_colour_split_collapse.py"), "__name__": "cfg36"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ H1")], "CFG36", "exec"), g36)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
collapse, edge_phantom, FB, nfw_enclosed = g36["collapse"], g36["edge_phantom"], g36["FB"], g36["nfw_enclosed"]
G_, KPC, MSUN, A0SI = g36["G_"], g36["KPC"], g36["MSUN"], g36["A0SI"]
DATA = os.path.join(C.REPO, "real_research", "data")


def rd(fn):
    L = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, fn)) if l.strip() and not l.startswith("#")]
    return [dict(zip(L[0], r)) for r in L[1:]]


TAB = {d["name"]: d for d in rd("diteodoro2023_massive_spirals.tsv")}
MOR = {d["name"]: d for d in rd("diteodoro2023_morphology.tsv")}
PTS = {}
for d in rd("diteodoro2023_hi_rotation_curves.tsv"):
    PTS.setdefault(d["name"], []).append((float(d["R_kpc"]), float(d["V_kms"]), float(d["dV_kms"])))


def lelli(pts):
    """Lelli, McGaugh & Schombert 2016 eqs 1-2: mean of the two outermost points, then include inner points while within 5% of the running mean."""
    pts = sorted(pts); V = [p[1] for p in pts]; Rr = [p[0] for p in pts]
    inc = [len(V) - 1, len(V) - 2]; m = (V[-1] + V[-2]) / 2
    k = len(V) - 3
    while k >= 0 and abs(V[k] - m) / m <= 0.05:
        inc.append(k); m = float(np.mean([V[i] for i in inc])); k -= 1
    return m, float(np.mean([Rr[i] for i in inc])), len(inc)


GALS = []
for n, t in TAB.items():
    m, rm, ni = lelli(PTS[n])
    T = MOR[n]["T"]; w = MOR[n]["W2W3"]
    GALS.append(dict(name=n, lMs=float(t["logMs_W1"]), lMg=float(t["logMgas"]), v=float(t["vflat"]) * VF, dv=float(t["dvflat"]) * VF,
                     Rm=rm, Nin=ni, alg=m, T=(None if T == "nan" else int(T)), w=(None if w == "nan" else float(w)), flag=int(t["flag_uncertain"])))

R.banner("C1 / C2  CONTROLS: the data and the recovered curves")
check("C1 CONTROL: 15 galaxies, 216 recovered points; NGC 5440's tabulated v_flat = 303 +- 25",
      f"{len(GALS)} galaxies; {sum(len(p) for p in PTS.values())} points; NGC5440 {TAB['NGC5440']['vflat']} +- {TAB['NGC5440']['dvflat']}",
      len(GALS) == 15 and sum(len(p) for p in PTS.values()) == 216 and TAB["NGC5440"]["vflat"] == "303" and TAB["NGC5440"]["dvflat"] == "25")
agree = [abs(g["alg"] - g["v"] / VF) for g in GALS]
check("C2 CONTROL: the Lelli+2016 algorithm on the recovered points reproduces the paper's v_flat within 3 km/s for >= 12 of 15",
      f"{sum(a <= 3.0 for a in agree)} of 15; worst {max(agree):.0f} km/s ({GALS[int(np.argmax(agree))]['name']})", sum(a <= 3.0 for a in agree) >= 12)


def gN(Mb, r, model, Rd=8.0):
    if model == "point":
        return G_ * Mb * MSUN / (r * KPC) ** 2
    if model == "sphere":
        return G_ * Mb * (1 - (1 + r / Rd) * math.exp(-r / Rd)) * MSUN / (r * KPC) ** 2
    y = r / (2 * Rd)
    return 2 * G_ * Mb * MSUN / (Rd * KPC) * y * y * (i0(y) * k0(y) - i1(y) * k1(y)) / (r * KPC)


def colour_of(g, wise=False):
    if wise:
        return "red" if (g["w"] is not None and g["w"] < 2.0) else "blue"
    return "red" if (g["T"] is not None and g["T"] <= 0) else "blue"


def pred(g, foot, model="point", which="rule", wise=False, dMs=0.0, dMg=0.0, rfac=1.0):
    a0 = A0SI[foot]; r = g["Rm"] * rfac
    Ms = 10 ** (g["lMs"] + dMs); Mb = Ms + 10 ** (g["lMg"] + dMg)
    gn = gN(Mb, r, model)
    gl = float(C.nu_mono(np.array([gn / a0]))[0]) * gn
    fex = 0.0
    if which == "rule":
        Mh = collapse(Ms, colour_of(g, wise)); fex = max(0.0, 1.0 - edge_phantom(Mb, foot, 0.40) / ((1 - FB) * Mh))
        gl += fex * (1 - FB) * float(nfw_enclosed(Mh, r)) * G_ * MSUN / (r * KPC) ** 2
    return math.sqrt(gl * r * KPC) / 1e3, fex


def offs(foot, which, sel=None, **kw):
    G = [g for g in GALS if (sel is None or sel(g))]
    return np.array([math.log10(g["v"] / pred(g, foot, which=which, **kw)[0]) for g in G])


def stat(foot, which, sel=None, **kw):
    off = offs(foot, which, sel, **kw)
    raw = float(off.mean()); err = float(off.std(ddof=1) / math.sqrt(len(off)))
    mods = [offs(foot, which, sel, **{**kw, "model": m}).mean() for m in ("point", "sphere", "freeman")]
    mod = 0.5 * (max(mods) - min(mods))
    ms = 0.5 * abs(offs(foot, which, sel, **{**kw, "dMs": +0.2}).mean() - offs(foot, which, sel, **{**kw, "dMs": -0.2}).mean())
    mg = 0.5 * abs(offs(foot, which, sel, **{**kw, "dMg": +0.1}).mean() - offs(foot, which, sel, **{**kw, "dMg": -0.1}).mean())
    rr = 0.5 * abs(offs(foot, which, sel, **{**kw, "rfac": 1.25}).mean() - offs(foot, which, sel, **{**kw, "rfac": 0.75}).mean())
    tot = math.sqrt(err ** 2 + mod ** 2 + ms ** 2 + mg ** 2 + rr ** 2 + DBIAS ** 2)
    return dict(n=len(off), raw=raw, corr=raw - BIAS, err=err, mod=mod, ms=ms, mg=mg, rr=rr, tot=tot, z=(raw - BIAS) / tot, per=off.tolist())


S0 = lambda g: g["T"] is not None and g["T"] <= 0
RES = {}
for f in FOOTS:
    for w in ("law", "rule"):
        RES[(f, w, "all")] = stat(f, w); RES[(f, w, "s0")] = stat(f, w, sel=S0)

R.banner("H1 / H2 / H3  THE FIFTEEN MASSIVE DISKS")
for g in GALS:
    vl, _ = pred(g, "canonical", which="law"); vr, fx = pred(g, "canonical", which="rule")
    P(f"    {g['name']:9s} T {str(g['T']):>4s} {colour_of(g):4s} log M_b {math.log10(10 ** g['lMs'] + 10 ** g['lMg']):5.2f}  R_flat {g['Rm']:5.1f} kpc ({g['Nin']:2d} pts)  v_flat {g['v'] / VF:4.0f} +- {g['dv'] / VF:3.0f};"
      f" law {vl:5.1f}; rule {vr:5.1f} (f_ex {fx:.2f}){'  [flagged uncertain by the paper]' if g['flag'] else ''}")
for k, v in RES.items():
    P(f"    {k[0]:9s} {k[1]:5s} {k[2]:3s} (N={v['n']:2d}): raw {v['raw']:+.3f}, corrected {v['corr']:+.3f} +- {v['tot']:.3f} "
      f"(gal {v['err']:.3f}, model {v['mod']:.3f}, M* {v['ms']:.3f}, gas {v['mg']:.3f}, radius {v['rr']:.3f}, bias {DBIAS:.3f}) -> {v['z']:+.2f} sigma")
La, Ra, Rs = RES[("canonical", "law", "all")], RES[("canonical", "rule", "all")], RES[("canonical", "rule", "s0")]
fx_s0 = [pred(g, "canonical", which="rule")[1] for g in GALS if S0(g)]
h1 = abs(La["z"]) < 2
h2a = abs(Ra["z"]) < 2
s0err = math.sqrt(np.std(np.array(Rs["per"]), ddof=1) ** 2 / Rs["n"] + Rs["mod"] ** 2 + Rs["ms"] ** 2 + Rs["mg"] ** 2 + Rs["rr"] ** 2 + DBIAS ** 2)
h2b = Rs["corr"] > -2 * s0err
h3 = sum(x > 0 for x in fx_s0) >= 2
check("H1 THE BARE LAW FITS THEM after the selection correction: |mean - B| < 2 sigma (canonical)",
      f"raw {La['raw']:+.3f}, corrected {La['corr']:+.3f} +- {La['tot']:.3f} ({La['z']:+.2f} sigma)", h1)
check("H2 [HEADLINE] B FITS THEM: (a) |mean - B| < 2 sigma over the 15; (b) the rule does not over-predict the four S0/S0a" + ("  [MUTATE: v x 0.5]" if MUTATE else ""),
      f"(a) {Ra['corr']:+.3f} +- {Ra['tot']:.3f} ({Ra['z']:+.2f}); (b) four S0/S0a: corrected {Rs['corr']:+.3f} +- {s0err:.3f} (> {-2 * s0err:+.3f}?) -> {Rs['corr'] / s0err:+.2f} sigma", h2a and h2b)
check("H3 THE RULE BITES: f_ex > 0 in at least 2 of the four S0/S0a", "f_ex: " + ", ".join(f"{x:.2f}" for x in fx_s0), h3)

# reported
raw_only = {w: RES[("canonical", w, "all")]["raw"] for w in ("law", "rule")}
wise = {w: stat("canonical", w, wise=True) for w in ("law", "rule")}
nof = lambda g: not g["flag"]
excl = {w: stat("canonical", w, sel=nof) for w in ("law", "rule")}
check("R1 (reported) uncorrected offsets; the alt footing", f"raw: law {raw_only['law']:+.3f}, rule {raw_only['rule']:+.3f}; alt corrected: "
      + ", ".join(f"{w} {RES[('alt', w, 'all')]['corr']:+.3f} ({RES[('alt', w, 'all')]['z']:+.2f} sigma)" for w in ("law", "rule")), True, load_bearing=False)
check("R2 (reported) the WISE colour assignment; the two galaxies the paper flags as uncertain excluded",
      "WISE colours: " + ", ".join(f"{w} {v['corr']:+.3f} ({v['z']:+.2f})" for w, v in wise.items()) + "; excluding NGC5635 / UGC12591: "
      + ", ".join(f"{w} {v['corr']:+.3f} ({v['z']:+.2f}, N={v['n']})" for w, v in excl.items()), True, load_bearing=False)
lawS0 = RES[("canonical", "law", "s0")]
check("R3 (reported) the four S0/S0a under the law and under the rule",
      f"law {lawS0['corr']:+.3f} (raw {lawS0['raw']:+.3f}); rule {Rs['corr']:+.3f} (raw {Rs['raw']:+.3f}); per galaxy (rule, raw): "
      + ", ".join(f"{g['name']} {o:+.3f}" for g, o in zip([g for g in GALS if S0(g)], Rs["per"])), True, load_bearing=False)
reading = ("the derived rule fits the first massive passive disks and the law fits the rest, on the HI tracer" if (h1 and h2a and h2b and h3) else
           ("the rule over-predicts the massive passive disks" if not h2b else ("the four S0/S0a do not test the rule" if not h3 else
            ("the law fails on these massive disks even after the selection correction" if not h1 else "B fails the mean test"))))
P(f"\n    READING (declared): {reading}")
R.num("RES", {f"{a}|{b}|{c}": v for (a, b, c), v in RES.items()}); R.num("bias", dict(B=BIAS, dB=DBIAS)); R.num("fex_s0", fx_s0); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
