#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG55 -- THE DYNAMICAL STELLAR-MASS TEST: is the SLUGGS globular-cluster deficit -- the one population where B's derived cold-mass rule
beats the bare law -- a stellar-mass artefact?

WHY.  CFG38: with SLUGGS's own stellar masses the law under-predicts the outer globular-cluster dispersions of 19 massive early types by
+0.080 +- 0.024 dex (3.3 sigma, canonical) and the rule's collapse debris closes the gap (+0.007 +- 0.017).  It is the only population
where the rule is preferred; the massive passive disks lean the other way (CFG41, CFG53: -1.25 sigma against the rule combined).  The
standing objection is the stellar mass.  CFG33 found that B's law, calibrated on ATLAS3D's JAM masses, needs a stellar M/L that grows with
dispersion, reaching x0.83-0.90 of Salpeter at sigma_e = 200-300 km/s -- heavier than a Chabrier population.  If SLUGGS's masses sit below
that, the deficit is an IMF artefact.  This lane replaces the population masses by DYNAMICAL ones: each model's stellar mass is fixed by
the galaxy's own inner stellar kinematics (the JAM mass inside the half-light sphere), and then the same model predicts the outer globular
clusters.  No IMF enters.

THE METHOD (declared before this script's first run).  CFG38's machinery exec'd read-only: h50's GC dispersion bins, isotropic Jeans with a
gamma = 3 tracer, Hernquist stars at a = R_e / 1.8153 with SLUGGS's R_e, the outer bins R > max(R_e, 2 kpc); CFG36's red collapse masses
and CFG35's conservation form at x_e = 0.40; nu_mono; hot gas omitted as in h50.  ATLAS3D (Cappellari+2013, XV): M_JAM = (M/L)_JAM L_r and
the 3D half-light radius r_1/2, both moved to SLUGGS's distance (M_JAM and r_1/2 scale as D).  The calibration is CFG33's (h9's)
convention: half the stars lie inside r_1/2, and the model's total mass there equals M_JAM / 2.  For the law that is
nu(g_N(r_1/2) / a0) M_* / 2 = M_JAM / 2 with g_N = G (M_* / 2) / r_1/2^2; for the rule, the collapse debris inside r_1/2,
f_ex (1 - f_b) M_NFW(< r_1/2; M_coll(M_*)), is added on the left.  Sample: the 16 of CFG38's 19 that are in ATLAS3D (NGC 1400, NGC 1407
and NGC 3115 lie outside its declination range); JAM quality >= 1 (all 16).  Statistic: CFG38's -- the mean over galaxies of the
per-galaxy mean of log(sigma_obs / sigma_pred) over the outer bins, with the galaxy-to-galaxy error.

PRE-DECLARED
  C1  CONTROL  CFG38's committed means reproduced by the exec'd machinery with SLUGGS's masses over the 19 (law +0.080, rule +0.007,
               canonical; to 1e-9 of the committed values).
  C2  CONTROL  CFG33's committed law calibration re-derived with this script's own code over ATLAS3D (quality >= 1): slope
               d log alpha_dyn / d log sigma_e = +0.204 and alpha_dyn at sigma = 100 / 200 / 300 km/s = x0.72 / x0.83 / x0.90 (to the
               printed precision).
  C3  CONTROL  the distance: h50's R_e equals SLUGGS's R_eff (arcsec) x the SLUGGS distance for all 16 (to 1e-6), and the calibration
               solver with the kernel switched off (nu = 1, no debris) returns M_* = M_JAM exactly (to 1e-10).
  H1  [HEADLINE; MUTATE must fail] CALIBRATED ON ITS OWN INNER KINEMATICS, THE LAW FITS THE OUTER GLOBULAR CLUSTERS: |mean offset| < 2 sigma
      over the 16, both footings.
  H2  THE RULE, CALIBRATED THE SAME WAY, STILL FITS: |mean offset| < 2 sigma over the 16, both footings.
  R1-R4 (reported): the same 16 with SLUGGS's masses (law, rule); per-galaxy table (log M_* from SLUGGS, JAM-law, JAM-rule; offsets;
      f_ex); the population alternatives on the same 16 (ATLAS3D's Salpeter M/L, and Salpeter - 0.25 dex); the calibration with the
      Hernquist enclosed fraction at r_1/2 in place of one half.
  READING (declared): H1 PASS -> the SLUGGS deficit is a stellar-mass artefact: calibrated on its own inner kinematics the law fits the
      outer globular clusters, and the derived rule loses its one supporting population (H2 then says whether the rule over-predicts).
      H1 FAIL -> the sign decides: a deficit that survives (> +2 sigma) means the massive early types want mass beyond the law independent
      of the IMF, and H2 says whether the rule supplies it; an over-prediction (< -2 sigma) means the inner kinematics carry more mass than
      the law can hold at the globular clusters.
MUTATE=1: every JAM mass halved (-0.30 dex) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG55_sluggs_dynamical_masses.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, json, contextlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG55_sluggs_dynamical_masses", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every JAM mass halved -- H1 must FAIL ***")
JF = 0.5 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
ARCSEC = 1 / 206264.806

# ------------------------------------------------------------------ CFG38's machinery, read-only (its own MUTATE forced off)
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG38_sluggs_massive_passive.py")).read()
g38 = {"__file__": os.path.join(HERE, "CFG38_sluggs_massive_passive.py"), "__name__": "cfg38"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index('R.banner("H1 / H2  THE NINETEEN')], "CFG38", "exec"), g38)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
RES50, sigma_r2, sigma_los, GAMMA = g38["RES50"], g38["sigma_r2"], g38["sigma_los"], g38["GAMMA"]
G_, KPC, MSUN, nu_h = g38["G_"], g38["KPC"], g38["MSUN"], g38["nu_h"]
collapse, edge_phantom, FB, nfw_enclosed, A0SI = g38["collapse"], g38["edge_phantom"], g38["FB"], g38["nfw_enclosed"], g38["A0SI"]
offsets38 = g38["offsets"]


def rd(fn, key):
    L = [l.rstrip("\n").split("\t") for l in open(os.path.join(C.REPO, "real_research", "data", fn)) if l.strip() and not l.startswith("#")]
    H = [h.strip() for h in L[0]]
    return {(r[H.index(key)].strip()): dict(zip(H, [x.strip() for x in r])) for r in L[1:] if len(r) == len(H)}


A3 = rd("atlas3d_fj_table.tsv", "name")
SL = {("NGC" + v["NGC"].strip()) if v["NGC"].strip().isdigit() else v["NGC"]: v for v in rd("sluggs_forbes2017_galaxies.tsv", "NGC").values()
      if v.get("NGC", "").strip().isdigit()}


def fnum(s):
    try:
        return float(s)
    except Exception:
        return float("nan")


# ------------------------------------------------------------------ C1: CFG38 reproduced
R.banner("C1-C3  CONTROLS")
c38 = json.load(open(os.path.join(HERE, "CFG38_sluggs_massive_passive_results.json")))["numbers"]["RES"]["canonical"]
o_rule, _, _ = offsets38("canonical")
o_law = np.array([r["off_mond_canonical"] for r in RES50])
check("C1 CONTROL: CFG38's committed means reproduced with SLUGGS's masses over the 19 (law +0.080, rule +0.007, canonical)",
      f"law {o_law.mean():+.6f} (committed {c38['law_mean']:+.6f}); rule {o_rule.mean():+.6f} (committed {c38['rule_mean']:+.6f})",
      abs(o_law.mean() - c38["law_mean"]) < 1e-9 and abs(o_rule.mean() - c38["rule_mean"]) < 1e-9)

# ------------------------------------------------------------------ C2: CFG33's law calibration re-derived with this script's own code
ET = []
for n, d in A3.items():
    e = dict(name=n, lsig=fnum(d["logsig_e"]), lmljam=fnum(d["logML_JAM"]), qual=fnum(d["qual"]), lr12=fnum(d["logr12"]), lL=fnum(d["logL"]),
             lmlsalp=fnum(d["logML_Salp"]), D=fnum(d["Dist_Mpc"]))
    if all(np.isfinite(e[k]) for k in ("D", "lsig", "lmlsalp", "lr12", "lL", "lmljam")):
        ET.append(e)


def law_mass(Mjam, r12_kpc, a0, kern_on=True):
    """CFG33's convention: nu(g_N(r12)/a0) M/2 = Mjam/2 with g_N = G (M/2)/r12^2 -- solved by bisection in log M (not CFG33's iteration)."""
    if not kern_on:
        return Mjam
    f = lambda lm: math.log10(10 ** lm * float(C.nu_mono(np.array([G_ * (10 ** lm / 2) * MSUN / (r12_kpc * KPC) ** 2 / a0]))[0])) - math.log10(Mjam)
    return 10 ** brentq(f, math.log10(Mjam) - 3, math.log10(Mjam) + 1, xtol=1e-13)


al = np.array([law_mass(10 ** (e["lmljam"] + e["lL"]), 10 ** e["lr12"] * ARCSEC * e["D"] * 1e3, A0SI["canonical"]) / 10 ** (e["lmlsalp"] + e["lL"])
               for e in ET])
q = np.array([e["qual"] >= 1 for e in ET]); ls_ = np.array([e["lsig"] for e in ET])
b_, a_ = np.polyfit(ls_[q] - 2.3, np.log10(al[q]), 1)
at = [10 ** (a_ + b_ * (math.log10(s) - 2.3)) for s in (100, 200, 300)]
check("C2 CONTROL: CFG33's law calibration re-derived with this script's own solver (slope +0.204; x0.72 / x0.83 / x0.90)",
      f"slope {b_:+.3f}; alpha_dyn at 100 / 200 / 300 km/s x{at[0]:.2f} / x{at[1]:.2f} / x{at[2]:.2f} (N = {int(q.sum())})",
      round(b_, 3) == 0.204 and [round(x, 2) for x in at] == [0.72, 0.83, 0.90])

# ------------------------------------------------------------------ the sample
G16 = []
for r in RES50:
    n = r["name"]
    if n not in A3:
        continue
    a, s = A3[n], SL[n]
    DS, DA = float(s["Dist"]), float(a["Dist_Mpc"])
    G16.append(dict(r=r, name=n, DS=DS, DA=DA, ReS=float(s["Reff"]) * ARCSEC * DS * 1e3, qual=fnum(a["qual"]), lsig=fnum(a["logsig_e"]),
                    Mjam=JF * 10 ** (fnum(a["logML_JAM"]) + fnum(a["logL"])) * DS / DA,
                    r12=10 ** fnum(a["logr12"]) * ARCSEC * DS * 1e3,
                    Msalp=10 ** (fnum(a["logML_Salp"]) + fnum(a["logL"])) * (DS / DA) ** 2))
dRe = max(abs(g["ReS"] - g["r"]["Re"]) for g in G16)
c3b = max(abs(law_mass(g["Mjam"], g["r12"], A0SI["canonical"], kern_on=False) / g["Mjam"] - 1) for g in G16)
check("C3 CONTROL: h50's R_e = SLUGGS's R_eff x SLUGGS's distance for all 16; the solver with the kernel off returns M_JAM exactly",
      f"{len(G16)} galaxies (qual >= 1: {sum(g['qual'] >= 1 for g in G16)}); max |R_e difference| {dRe:.1e} kpc; kernel-off max |M/M_JAM - 1| {c3b:.1e}",
      len(G16) == 16 and all(g["qual"] >= 1 for g in G16) and dRe < 1e-6 and c3b < 1e-10)


# ------------------------------------------------------------------ the models
def debris(Ms, foot):
    Mh = collapse(Ms, "red")
    return max(0.0, 1.0 - edge_phantom(Ms, foot, 0.40) / ((1 - FB) * Mh)), Mh


def rule_mass(g, foot, frac=0.5):
    """the rule's stellar mass: nu(g_N) Ms frac + f_ex (1 - f_b) M_NFW(<r12) = Mjam/2 (frac = the stellar fraction inside r12)."""
    a0 = A0SI[foot]

    def tot(lm):
        Ms = 10 ** lm; gN = G_ * frac * Ms * MSUN / (g["r12"] * KPC) ** 2
        fx, Mh = debris(Ms, foot)
        return frac * Ms * float(nu_h(gN / a0)) + fx * (1 - FB) * float(nfw_enclosed(Mh, g["r12"]))
    fr = lambda lm: math.log10(tot(lm)) - math.log10(g["Mjam"] / 2)
    if fr(8.0) * fr(13.5) > 0:      # the rule's debris alone exceeds the JAM mass: the rule cannot be calibrated (bug fix, disclosed)
        return float("nan")
    return 10 ** brentq(fr, 8.0, 13.5, xtol=1e-12)


def law_mass_g(g, foot, frac=0.5):
    a0 = A0SI[foot]
    f = lambda lm: math.log10(frac * 10 ** lm * float(nu_h(G_ * frac * 10 ** lm * MSUN / (g["r12"] * KPC) ** 2 / a0))) - math.log10(g["Mjam"] / 2)
    return 10 ** brentq(f, 8.0, 13.5, xtol=1e-12)


def sigma_pred(g, foot, Ms, which):
    r = g["r"]; a0 = A0SI[foot]; a_h = r["Re"] / 1.8153
    fx, Mh = debris(Ms, foot) if which == "rule" else (0.0, 1.0)

    def gf(rr):
        Mb = Ms * MSUN * rr ** 2 / (rr + a_h) ** 2; gN = G_ * Mb / (rr * KPC) ** 2
        out = gN * nu_h(gN / a0)
        if fx > 0:
            out = out + fx * (1 - FB) * G_ * np.asarray(nfw_enclosed(Mh, rr), float) * MSUN / (rr * KPC) ** 2
        return out
    return sigma_los(r["Rb"], sigma_r2(gf, GAMMA), GAMMA), fx


def offset(g, foot, Ms, which):
    s, fx = sigma_pred(g, foot, Ms, which); r = g["r"]
    return float(np.mean(np.log10(r["Sb"][r["out"]] / s[r["out"]]))), fx


def hernq_frac(g):
    a_h = g["r"]["Re"] / 1.8153
    return g["r12"] ** 2 / (g["r12"] + a_h) ** 2


def sample(foot, masses, which, keep=lambda g: True):
    off = np.array([offset(g, foot, m, which)[0] for g, m in zip(G16, masses) if np.isfinite(m) and keep(g)])
    return off, float(off.mean()), float(off.std(ddof=1) / math.sqrt(len(off)))


RES = {}
for f in FOOTS:
    ML = [law_mass_g(g, f) for g in G16]; MR = [rule_mass(g, f) for g in G16]; MS = [g["r"]["Mstar"] for g in G16]
    RES[f] = dict(ML=ML, MR=MR, law=sample(f, ML, "law"), rule=sample(f, MR, "rule"), law_sl=sample(f, MS, "law"), rule_sl=sample(f, MS, "rule"))

R.banner("PER GALAXY (canonical): log M_* from SLUGGS, calibrated on JAM under the law and under the rule; outer offsets")
c = RES["canonical"]
ir = 0
for i, g in enumerate(G16):
    if not np.isfinite(c["MR"][i]):
        P(f"    {g['name']:8s} the rule cannot be calibrated (its debris alone exceeds the JAM mass): excluded from the rule's mean")
        continue
    fx = debris(c["MR"][i], "canonical")[0]
    P(f"    {g['name']:8s} sigma_e {10 ** g['lsig']:4.0f}: log M_* SLUGGS {math.log10(g['r']['Mstar']):.2f}, JAM-law {math.log10(c['ML'][i]):.2f}, "
      f"JAM-rule {math.log10(c['MR'][i]):.2f} (f_ex {fx:.2f}); offsets law {c['law'][0][i]:+.3f}, rule {c['rule'][0][ir]:+.3f} "
      f"(SLUGGS masses: law {c['law_sl'][0][i]:+.3f}, rule {c['rule_sl'][0][i]:+.3f})")
    ir += 1
dm = np.log10(np.array(c["ML"]) / np.array([g["r"]["Mstar"] for g in G16]))
P(f"\n    JAM-law minus SLUGGS masses: median {np.median(dm):+.3f} dex, mean {dm.mean():+.3f} +- {dm.std(ddof=1) / math.sqrt(len(dm)):.3f}")
for f in FOOTS:
    v = RES[f]
    P(f"    {f:9s}: JAM-calibrated law {v['law'][1]:+.4f} +- {v['law'][2]:.4f} ({v['law'][1] / v['law'][2]:+.2f} sigma); rule {v['rule'][1]:+.4f} +- "
      f"{v['rule'][2]:.4f} ({v['rule'][1] / v['rule'][2]:+.2f} sigma) | SLUGGS masses, same 16: law {v['law_sl'][1]:+.4f} ({v['law_sl'][1] / v['law_sl'][2]:+.2f}), "
      f"rule {v['rule_sl'][1]:+.4f} ({v['rule_sl'][1] / v['rule_sl'][2]:+.2f})")

R.banner("H1 / H2")
z = {f: RES[f]["law"][1] / RES[f]["law"][2] for f in FOOTS}; zr = {f: RES[f]["rule"][1] / RES[f]["rule"][2] for f in FOOTS}
check("H1 [HEADLINE] CALIBRATED ON ITS OWN INNER KINEMATICS, THE LAW FITS THE OUTER GLOBULAR CLUSTERS: |mean| < 2 sigma over the 16, both footings"
      + ("  [MUTATE: JAM masses halved]" if MUTATE else ""),
      "; ".join(f"{f}: {RES[f]['law'][1]:+.4f} +- {RES[f]['law'][2]:.4f} ({z[f]:+.2f} sigma)" for f in FOOTS), all(abs(x) < 2 for x in z.values()))
check("H2 THE RULE, CALIBRATED THE SAME WAY, STILL FITS: |mean| < 2 sigma over the 16, both footings",
      "; ".join(f"{f}: {RES[f]['rule'][1]:+.4f} +- {RES[f]['rule'][2]:.4f} ({zr[f]:+.2f} sigma)" for f in FOOTS), all(abs(x) < 2 for x in zr.values()))

R.banner("R1-R4 (reported)")
for f in FOOTS:
    v = RES[f]
    check(f"R1 (reported, {f}) the same 16 with SLUGGS's masses", f"law {v['law_sl'][1]:+.4f} +- {v['law_sl'][2]:.4f} "
          f"({v['law_sl'][1] / v['law_sl'][2]:+.2f} sigma); rule {v['rule_sl'][1]:+.4f} +- {v['rule_sl'][2]:.4f} ({v['rule_sl'][1] / v['rule_sl'][2]:+.2f} sigma)",
          True, load_bearing=False)
pop = {}
for lab, fac in (("Salpeter", 1.0), ("Salpeter - 0.25 dex", 10 ** -0.25)):
    ms = [g["Msalp"] * fac for g in G16]
    pop[lab] = {w: sample("canonical", ms, w)[1:] for w in ("law", "rule")}
check("R3 (reported, canonical) population masses on the same 16: ATLAS3D's Salpeter M/L, and Salpeter - 0.25 dex (Chabrier-like)",
      "; ".join(f"{k}: law {v['law'][0]:+.4f} ({v['law'][0] / v['law'][1]:+.2f} sigma), rule {v['rule'][0]:+.4f} ({v['rule'][0] / v['rule'][1]:+.2f} sigma)"
                for k, v in pop.items()), True, load_bearing=False)
MLh = [law_mass_g(g, "canonical", hernq_frac(g)) for g in G16]; MRh = [rule_mass(g, "canonical", hernq_frac(g)) for g in G16]
lh, rh = sample("canonical", MLh, "law"), sample("canonical", MRh, "rule")
check("R4 (reported, canonical) calibration with the Hernquist enclosed fraction at r_1/2 in place of one half",
      f"stellar fraction inside r_1/2 {min(hernq_frac(g) for g in G16):.2f}-{max(hernq_frac(g) for g in G16):.2f}; law {lh[1]:+.4f} "
      f"({lh[1] / lh[2]:+.2f} sigma), rule {rh[1]:+.4f} ({rh[1] / rh[2]:+.2f} sigma)", True, load_bearing=False)

inr = lambda g: np.isfinite(RES["canonical"]["MR"][G16.index(g)]) and math.log10(RES["canonical"]["MR"][G16.index(g)]) >= 10.28
out_r = [g["name"] for g in G16 if not inr(g)]
pr = {f: (sample(f, RES[f]["ML"], "law", keep=inr)[1:], sample(f, RES[f]["MR"], "rule", keep=inr)[1:]) for f in FOOTS}
check("R5 (reported; POST HOC, disclosed) without the galaxies whose calibrated rule mass lies below Mandelbaum's red range (log M_* < 10.28: "
      "clamped collapse masses, CFG36's standing caution)",
      f"removed {out_r}; " + "; ".join(f"{f}: law {v[0][0]:+.4f} ({v[0][0] / v[0][1]:+.2f} sigma), rule {v[1][0]:+.4f} ({v[1][0] / v[1][1]:+.2f} sigma)"
                                      for f, v in pr.items()), True, load_bearing=False)
R.num("R5_posthoc_inrange", dict(removed=out_r, **{f: dict(law=v[0], rule=v[1]) for f, v in pr.items()}))

h1 = all(abs(x) < 2 for x in z.values())
if h1:
    reading = ("the SLUGGS deficit is a stellar-mass artefact: calibrated on its own inner kinematics the law fits the outer globular "
               "clusters, and the derived rule loses its one supporting population"
               + ("; the rule, calibrated the same way, also fits" if all(abs(x) < 2 for x in zr.values()) else "; the rule, calibrated the same way, no longer fits"))
elif all(x > 2 for x in z.values()):
    reading = ("the deficit survives dynamical stellar masses: the massive early types want mass beyond the law independent of the IMF"
               + ("; the rule supplies it" if all(abs(x) < 2 for x in zr.values()) else "; the rule does not close it"))
else:
    reading = "mixed: the footings disagree or the law over-predicts; see the table"
P(f"\n    READING (declared): {reading}")
R.num("RES", {f: dict(law=dict(mean=v["law"][1], err=v["law"][2], per=v["law"][0].tolist()), rule=dict(mean=v["rule"][1], err=v["rule"][2], per=v["rule"][0].tolist()),
                      law_sluggs=dict(mean=v["law_sl"][1], err=v["law_sl"][2]), rule_sluggs=dict(mean=v["rule_sl"][1], err=v["rule_sl"][2]),
                      logM_law=[math.log10(x) for x in v["ML"]], logM_rule=[math.log10(x) for x in v["MR"]]) for f, v in RES.items()})
R.num("names", [g["name"] for g in G16]); R.num("dlogM_law_minus_sluggs", dm.tolist())
R.num("R3_population", pop); R.num("R4_hernquist", dict(law=lh[1:], rule=rh[1:])); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
