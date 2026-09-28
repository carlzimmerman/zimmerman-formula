#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG38 -- THE MASSIVE PASSIVE REGIME: do the SLUGGS globular-cluster dispersions of early-type galaxies want the extra mass of B's
derived cold-mass rule (CFG35/36), or the law alone?

WHY.  CFG36-37: with measured colour-split collapse masses (Mandelbaum+2016) the conservation rule is the law for every star-forming
spiral and for passive disks below log M_* ~ 11.2 (CFG37: 16 ATLAS3D HI discs follow the law, 0.3 sigma), and adds collapse debris only
above that on the red sequence.  h50 (hunt_2026/h50_gc_dispersions.py) measured globular-cluster dispersion profiles of 19 SLUGGS early
types out to 5-15 R_eff and found the law's zero-parameter prediction LOW by ~20% in the mean (h50's 50.2), worst in the most massive
(M87 +0.28 dex, NGC 5846 and NGC 4374 +0.21, NGC 1407 +0.16).  That is the regime the rule claims.

THE METHOD (declared before this script's first run).  h50's data, dispersion bins and isotropic Jeans machinery exec'd read-only (gamma =
3 tracer, Hernquist stars from SLUGGS's own stellar masses, the outer bins R > max(R_eff, 2 kpc)); CFG36's collapse masses (Mandelbaum's
RED relation -- every SLUGGS galaxy is an early type -- converted to M_200c) and CFG35's conservation form (edge x_e = 0.40):
g(r) = G [nu(g_N/a0) M_b(<r) + f_ex (1 - f_b) M_NFW(<r; M_coll)] / r^2.  SLUGGS's stellar masses stand in for Mandelbaum's Chabrier
masses (declared); hot gas is omitted, as in h50.  Per galaxy the offset is h50's: the mean over the outer bins of log(sigma_obs /
sigma_pred).  Sample: the mean over galaxies with the galaxy-to-galaxy error.

PRE-DECLARED
  C1  CONTROL  h50's committed per-galaxy law offsets (d_MOND, canonical) reproduced to the printed precision.
  H1  [HEADLINE; MUTATE must fail] THE RULE CLOSES WHAT THE LAW LEAVES: the rule's mean offset over the 19 lies within 2 sigma of zero
      (galaxy-to-galaxy error), both footings -- where the law's does not (h50: ~+0.08 dex, > 3 sigma).
  H2  THE MASS TREND GOES: the law's offsets rise with stellar mass; under the rule, the slope d(offset)/d log M_* is consistent with zero
      (< 2 sigma, bootstrap over galaxies), canonical.
  R1-R3 (reported): per-galaxy offsets, f_ex and collapse masses; the abundance-matched NFW of h50 (Moster) beside; the BLUE relation.
  READING (declared): H1 and H2 PASS -> in the massive passive regime the globular clusters want the rule's collapse debris: B's derived
  conservation rule with measured red collapse masses fits them, alongside the spirals and passive disks it leaves alone.  H1 FAIL ->
  the rule does not close the SLUGGS deficit.
MUTATE=1: every collapse mass divided by 100 (the rule reduces to the law) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG38_sluggs_massive_passive.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG38_sluggs_massive_passive", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every collapse mass / 100 -- H1 must FAIL ***")
MCF = 0.01 if MUTATE else 1.0
HUNT = os.path.join(C.REPO, "hunt_2026")
sys.path.insert(0, HUNT)

# h50's machinery and per-galaxy results, exec'd read-only
g50, _ = C.C4.exec_slices(os.path.join(HUNT, "h50_gc_dispersions.py"),
                          [(None, 'P(f"  (sig_obs and the three models are averaged over the bins outside max(1 R_e, 2 kpc)')], name="h50")
RES50, sigma_r2, sigma_los, GAMMA = g50["res"], g50["sigma_r2"], g50["sigma_los"], g50["GAMMA"]
G_, KPC, MSUN, nu_h = g50["G"], g50["kpc"], g50["Msun"], g50["nu"]
# CFG36's collapse masses and CFG35's edge phantom, exec'd read-only with MUTATE off
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG36_colour_split_collapse.py")).read()
g36 = {"__file__": os.path.join(HERE, "CFG36_colour_split_collapse.py"), "__name__": "cfg36"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ H1")], "CFG36", "exec"), g36)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
collapse, edge_phantom, FB, nfw_enclosed = g36["collapse"], g36["edge_phantom"], g36["FB"], g36["nfw_enclosed"]
A0SI = C.A0_SI

# ================================================================================================ C1
R.banner("C1  CONTROL: h50's committed per-galaxy law offsets")
o50 = open(os.path.join(HUNT, "h50_gc_dispersions.out")).read()
com = {m.group(1): float(m.group(2)) for m in re.finditer(r"^(NGC\d+|IC\d+)\s+\d+\s+.*?\|\s+([+-][0-9.]+)\s+[+-][0-9.]+\s+[+-][0-9.]+\s*$", o50, re.M)}
dev = max(abs(round(r["off_mond_canonical"], 2) - com[r["name"]]) for r in RES50)
check("C1 CONTROL: h50's committed per-galaxy law offsets (canonical) reproduced to the printed precision",
      f"{len(RES50)} galaxies; max |d| {dev:.3f} (e.g. NGC4486 {[r['off_mond_canonical'] for r in RES50 if r['name'] == 'NGC4486'][0]:+.3f})", dev <= 0.005 + 1e-9)


def rule_sigma(r, foot, colour="red"):
    a0 = A0SI[foot]; Ms = r["Mstar"]; a_h = r["Re"] / 1.8153
    Mh = MCF * collapse(Ms, colour)
    fex = max(0.0, 1.0 - edge_phantom(Ms, foot, 0.40) / ((1 - FB) * Mh))

    def g(rr):
        Mb = Ms * MSUN * rr ** 2 / (rr + a_h) ** 2; gN = G_ * Mb / (rr * KPC) ** 2
        return gN * nu_h(gN / a0) + fex * (1 - FB) * G_ * np.asarray(nfw_enclosed(Mh, rr), float) * MSUN / (rr * KPC) ** 2
    return sigma_los(r["Rb"], sigma_r2(g, GAMMA), GAMMA), fex, Mh


def offsets(foot, colour="red"):
    out, fx, mh = [], [], []
    for r in RES50:
        s, f_, m_ = rule_sigma(r, foot, colour)
        out.append(float(np.mean(np.log10(r["Sb"][r["out"]] / s[r["out"]])))); fx.append(f_); mh.append(m_)
    return np.array(out), fx, mh


R.banner("H1 / H2  THE NINETEEN SLUGGS EARLY TYPES")
RES = {}
lms = np.log10([r["Mstar"] for r in RES50])
for foot in ("canonical", "alt"):
    off, fx, mh = offsets(foot)
    law = np.array([r["off_mond_" + foot] for r in RES50])
    RES[foot] = dict(rule=off.tolist(), law=law.tolist(), fex=fx, Mh=mh, rule_mean=float(off.mean()), rule_err=float(off.std(ddof=1) / math.sqrt(len(off))),
                     law_mean=float(law.mean()), law_err=float(law.std(ddof=1) / math.sqrt(len(law))))
    v = RES[foot]
    P(f"    {foot:9s}: law {v['law_mean']:+.3f} +- {v['law_err']:.3f} ({v['law_mean'] / v['law_err']:+.1f} sigma); rule {v['rule_mean']:+.3f} +- {v['rule_err']:.3f} "
      f"({v['rule_mean'] / v['rule_err']:+.1f} sigma); the rule adds mass in {sum(x > 0 for x in fx)} of {len(fx)}")
for r, o, l_, x, m in zip(RES50, RES["canonical"]["rule"], RES["canonical"]["law"], RES["canonical"]["fex"], RES["canonical"]["Mh"]):
    P(f"      {r['name']:8s} log M* {math.log10(r['Mstar']):5.2f}: law {l_:+.2f} -> rule {o:+.2f}  (f_ex {x:.2f}, M200c {m:.1e})")
check("H1 [HEADLINE] THE RULE CLOSES WHAT THE LAW LEAVES: the rule's mean offset within 2 sigma of zero, both footings"
      + ("  [MUTATE: collapse masses / 100]" if MUTATE else ""),
      "; ".join(f"{f}: rule {v['rule_mean']:+.3f} ({v['rule_mean'] / v['rule_err']:+.1f} sigma), law {v['law_mean']:+.3f} ({v['law_mean'] / v['law_err']:+.1f} sigma)"
                for f, v in RES.items()), all(abs(v["rule_mean"] / v["rule_err"]) < 2 for v in RES.values()))
rng = np.random.default_rng(38)
ro = np.array(RES["canonical"]["rule"]); lo = np.array(RES["canonical"]["law"])
sl = lambda y, idx: np.polyfit(lms[idx], y[idx], 1)[0]
bs = [sl(ro, i) for i in (rng.integers(0, len(ro), len(ro)) for _ in range(2000))]
bl = [sl(lo, i) for i in (rng.integers(0, len(lo), len(lo)) for _ in range(2000))]
s_r, s_l = sl(ro, np.arange(len(ro))), sl(lo, np.arange(len(lo)))
check("H2 THE MASS TREND GOES: under the rule d(offset)/d log M_* is consistent with zero (< 2 sigma, bootstrap), canonical",
      f"rule slope {s_r:+.3f} +- {np.std(bs):.3f} ({s_r / np.std(bs):+.1f} sigma); law slope {s_l:+.3f} +- {np.std(bl):.3f} ({s_l / np.std(bl):+.1f} sigma)",
      abs(s_r / np.std(bs)) < 2)
nfw = np.array([r["off_nfw"] for r in RES50]); blue = offsets("canonical", "blue")[0]
check("R1 (reported) h50's abundance-matched NFW (Moster, colour-blind) and the rule with the BLUE relation, canonical",
      f"NFW {nfw.mean():+.3f} +- {nfw.std(ddof=1) / math.sqrt(len(nfw)):.3f}; blue-relation rule {blue.mean():+.3f} +- {blue.std(ddof=1) / math.sqrt(len(blue)):.3f}",
      True, load_bearing=False)
def lcdm_red(r):
    """POST-HOC (added after the main run, for fairness): LambdaCDM on the SAME measured red collapse masses -- stars + the full cold halo,
    no phantom."""
    Ms = r["Mstar"]; a_h = r["Re"] / 1.8153; Mh = MCF * collapse(Ms, "red")
    g = lambda rr: G_ * (Ms * MSUN * rr ** 2 / (rr + a_h) ** 2 + (1 - FB) * np.asarray(nfw_enclosed(Mh, rr), float) * MSUN) / (rr * KPC) ** 2
    s = sigma_los(r["Rb"], sigma_r2(g, GAMMA), GAMMA)
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s[r["out"]])))


lr_ = np.array([lcdm_red(r) for r in RES50])
check("R2 (reported; POST-HOC, added after the main run) LambdaCDM on the same measured red collapse masses (stars + full halo, no phantom)",
      f"{lr_.mean():+.3f} +- {lr_.std(ddof=1) / math.sqrt(len(lr_)):.3f} ({lr_.mean() / (lr_.std(ddof=1) / math.sqrt(len(lr_))):+.1f} sigma); low-mass half "
      f"(log M* < 11.2) {lr_[lms < 11.2].mean():+.3f}, high-mass half {lr_[lms >= 11.2].mean():+.3f}", True, load_bearing=False)
R.num("R2_lcdm_red", lr_.tolist())
h1 = all(abs(v["rule_mean"] / v["rule_err"]) < 2 for v in RES.values()); h2 = abs(s_r / np.std(bs)) < 2
reading = ("in the massive passive regime the globular clusters want the rule's collapse debris: the derived conservation rule with measured red "
           "collapse masses fits them" if (h1 and h2) else ("the rule does not close the SLUGGS deficit" if not h1 else
                                                           "the rule closes the mean but leaves a mass trend"))
P(f"\n    READING (declared): {reading}")
R.num("RES", RES); R.num("H2", dict(rule_slope=float(s_r), rule_err=float(np.std(bs)), law_slope=float(s_l), law_err=float(np.std(bl))))
R.num("R1", dict(nfw_mean=float(nfw.mean()), blue_mean=float(blue.mean()))); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
