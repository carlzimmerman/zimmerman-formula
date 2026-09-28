#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG28 -- ADVERSARIAL REFEREE OF THE LARGEST STANDING FAILURE: the Milky Way's ultra-faint dwarfs at 7.5-8.0 sigma (FG001's G7;
CFG18).  Is the offset real, or is it made by our own analysis, or by inflated velocity dispersions?

WHY.  Under ownership (FG001) an accreted satellite obeys the isolated law of its infall baryons; the ultra-faints were quenched
by reionisation and hold no gas, so the law predicts their dispersions from their stars alone.  The measured dispersions sit
+0.355/+0.334 dex above that (7.97/7.52 sigma; canonical/alt).  Both sides are refereed.
  OUR ANALYSIS.  FG001 (i) drops every ultra-faint whose dispersion is only an upper limit -- 9 of the 40 with a dispersion
  measurement, likely the slowest systems, so the selection pushes the median up; (ii) quotes a statistical error only,
  1.2533 rms/sqrt(n), with no coherent systematic floor.
  THE DATA.  A dispersion can be inflated by unresolved binaries (roughly a constant few km/s added in quadrature), by Milky Way
  tides (strongest for the closest systems), and by small noisy samples.
Data: the committed LVD Milky Way table (real_research/data/dsph/lvd_dwarf_mw.csv; Pace 2024).  FG001's loader, estimator and
constants are exec'd read-only (the isolated law of the stars, Upsilon_V = 2, r = (4/3) r_half, sigma^2 = g(r) r / 3).

PRE-DECLARED (before this script's first run)
  C1  CONTROL  FG001's committed ultra-faint isolated median (+0.355/+0.334 dex) and its gate value (7.97/7.52 sigma) reproduced.
  T1  [censoring] the median offset with the upper-limit systems included as left-censored values (Kaplan-Meier on the reflected
      offset), 2000-resample bootstrap error.  Reported beside it: the limits taken as detections at their limits.
  T2  [tides] the ultra-faints beyond 80 kpc of the Galactic centre (weaker tides) against those inside (Kaplan-Meier medians,
      bootstrap errors); the Spearman correlation of the resolved offsets with distance.
  T3  [binaries] two one-parameter population models by maximum likelihood, each with an intrinsic log scatter, the upper limits
      entering as censored terms: a shared additive floor, sigma_obs^2 = sigma_pred^2 + s^2 (what unresolved binaries or any
      constant contamination would do), against a shared factor, sigma_obs = f sigma_pred (what a real mass discrepancy would do).
  T4  [precision] the resolved systems whose dispersion error is <= 25%: median and FG001's error.
  T5  [systematics] a coherent floor: Upsilon_V from 1 to 4 and the pure deep-MOND estimator sigma^4 = (4/81) G M a0 in place of
      FG001's; floor = half the range of the median over these variants; z recomputed with the floor in quadrature.
  H1  [HEADLINE; MUTATE must fail] the failure is robust to OUR analysis: with the upper limits included (T1) and the systematic
      floor (T5), the median offset is > 0.2 dex and > 3 sigma on both footings.
  H2  the offset survives the data tests available here: the far subsample (T2) and the precise subsample (T4) each show a positive
      offset at > 2 sigma, on both footings.
  R1  (reported) T3: the fitted floor s (km/s), the factor f, the scatter and Delta ln L.
  READING: H1 FAIL -> the 8 sigma was made by our analysis.  H1 PASS + H2 FAIL -> it rests on the closest or least precise systems:
  inflation is plausible and the failure is not established.  H1 PASS + H2 PASS -> it is robust to our analysis and to the data
  tests available here; the decisive remaining test is multi-epoch, binary-corrected dispersions.
MUTATE=1: every ultra-faint dispersion (and limit) is halved, as if half the speed were inflation -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG28_ufd_referee.py   (MUTATE=1 for the control; ~20 s)
"""
import os, sys, math, json, csv
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
import hunt_lib as HL
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG28_ufd_referee", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every ultra-faint dispersion and limit halved -- H1 must FAIL ***")

FGP = os.path.join(HERE, "CFG7_hierarchy_fg001.py")
ns = {"np": np, "math": math, "os": os, "csv": csv, "C": C, "HL": HL}
ns = C.C4.exec_slices(FGP, [("G, kpc, Msun, A0H = HL.G", "# ================================================================================================ K1 h43"),
                            ("MW_MB, M31_MB, UPS_V = 6.0e10", "REF43 = {")], ns=ns, name="fg001_slices")[0]
A0H, UPS_V, resid, sigma_pred, fnum, G_, Msun = ns["A0H"], ns["UPS_V"], ns["resid"], ns["sigma_pred"], ns["fnum"], ns["G"], ns["Msun"]
UFD = ns["ufd"]
FG = json.load(open(os.path.join(HERE, "CFG7_hierarchy_fg001_results.json")))["numbers"]
MUT = 0.5 if MUTATE else 1.0

# the upper-limit ultra-faints FG001's loader drops (same columns, same cut M_V > -7.7)
UL = []
for r in csv.DictReader(open(os.path.join(ns["DSPH"], "lvd_dwarf_mw.csv"))):
    ul = fnum(r["vlos_sigma_ul"]); MV = fnum(r["M_V"])
    rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
    Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
    if ul is None or MV is None or rh is None or Dh is None or MV <= -7.7:
        continue
    MHI = fnum(r["mass_HI"])
    UL.append(dict(name=r["name"], MV=MV, LV=10 ** (0.4 * (4.83 - MV)), rh=rh, D=Dh, sig_ul=ul, MHI=(10 ** MHI if MHI is not None else 0.0),
                   host_mb=ns["MW_MB"]))


def spred(d, a0, ups=None, deep=False):
    Mb = (UPS_V if ups is None else ups) * d["LV"] + 1.33 * d["MHI"]
    if deep:
        return (4.0 / 81.0 * G_ * Mb * Msun * a0) ** 0.25 / 1e3
    return sigma_pred(Mb, (4.0 / 3.0) * d["rh"], d.get("D"), d["host_mb"], a0, efe=False)


def offsets(a0, ups=None, deep=False):
    x = np.array([math.log10(MUT * d["sig"] / spred(d, a0, ups, deep)) for d in UFD])
    xu = np.array([math.log10(MUT * d["sig_ul"] / spred(d, a0, ups, deep)) for d in UL])
    return x, xu


ELOG = np.array([0.4343 * d["esig"] / d["sig"] for d in UFD])
DR = np.array([d["D"] for d in UFD]); DU = np.array([d["D"] for d in UL])


def km_median(x, xu):
    """median of left-censored data (x detected, xu upper limits) by Kaplan-Meier on y = -x (right-censored)."""
    y = np.concatenate([-x, -xu]); ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]
    S, n = 1.0, len(y)
    i = 0
    while i < len(y):
        t = y[i]; j = i
        d_ = 0; c_ = 0
        while j < len(y) and y[j] == t:
            d_ += int(ev[j]); c_ += int(not ev[j]); j += 1
        if d_:
            S *= 1.0 - d_ / n
            if S <= 0.5:
                return -t
        n -= d_ + c_
        i = j
    return -y[-1]


def boot(fn, x, xu, nb=2000, seed=28):
    rng = np.random.default_rng(seed); v = []
    for _ in range(nb):
        a = x[rng.integers(0, len(x), len(x))]; b = xu[rng.integers(0, len(xu), len(xu))] if len(xu) else xu
        v.append(fn(a, b))
    return float(np.std(v))


# ================================================================================================ C1
R.banner("C1  CONTROL: FG001's committed ultra-faint median and gate value")
dev = 0.0
for foot, a0 in A0H.items():
    med = float(np.median(resid(UFD, a0, efe=False)))
    dev = max(dev, abs(med - FG["SAT"][f"{foot}|ufd"]["med_iso"]))
    s_ = FG["SAT"][f"{foot}|ufd"]
    zc = abs(s_["med_iso"]) / (1.2533 * s_["rms_iso"] / math.sqrt(s_["n"]))
    dev = max(dev, abs(zc - FG["GATES"]["G7 MW ultra-faints"][foot]["fg001"]))
P(f"    resolved ultra-faints: {len(UFD)}; upper limits dropped by FG001: {len(UL)} (" + ", ".join(f"{d['name']} <= {d['sig_ul']}" for d in UL) + ")")
check("C1 CONTROL: FG001's committed ultra-faint isolated median and gate value reproduced", f"max |d| {dev:.1e}", dev <= 1e-9)

# ================================================================================================ T1-T5
RES = {}
for foot, a0 in A0H.items():
    x, xu = offsets(a0)
    # T1 censoring
    m_fg = float(np.median(x)); e_fg = 1.2533 * float(np.sqrt(np.mean((x - np.mean(x)) ** 2))) / math.sqrt(len(x))
    m_km = km_median(x, xu); e_km = boot(km_median, x, xu)
    m_lim = float(np.median(np.concatenate([x, xu])))
    # T5 systematic floor (on the censored median)
    var = [km_median(*offsets(a0, ups=u)) for u in (1.0, 2.0, 4.0)] + [km_median(*offsets(a0, deep=True))]
    floor = 0.5 * (max(var) - min(var))
    z_km = m_km / math.sqrt(e_km ** 2 + floor ** 2)
    # T2 tides
    far, farU = x[DR > 80], xu[DU > 80]; near, nearU = x[DR <= 80], xu[DU <= 80]
    m_far = km_median(far, farU); e_far = boot(km_median, far, farU)
    m_near = km_median(near, nearU); e_near = boot(km_median, near, nearU)
    rho, prho = spearmanr(DR, x)
    # T4 precision
    good = (ELOG / 0.4343) <= 0.25
    xg = x[good]; m_g = float(np.median(xg)); e_g = 1.2533 * float(np.std(xg)) / math.sqrt(len(xg))
    RES[foot] = dict(fg=(m_fg, e_fg), km=(m_km, e_km), lim=m_lim, floor=floor, var=var, z_km=z_km, far=(m_far, e_far, len(far), len(farU)),
                     near=(m_near, e_near, len(near), len(nearU)), rho=(float(rho), float(prho)), prec=(m_g, e_g, int(good.sum())))

R.banner("T1 / T5  CENSORING AND THE SYSTEMATIC FLOOR")
for foot, v in RES.items():
    P(f"    {foot:9s}: FG001 (limits dropped) {v['fg'][0]:+.3f} +- {v['fg'][1]:.3f}; limits as detections {v['lim']:+.3f}; Kaplan-Meier with the "
      f"limits {v['km'][0]:+.3f} +- {v['km'][1]:.3f} (bootstrap); floor {v['floor']:.3f} dex (Upsilon_V 1/2/4, deep-MOND estimator: "
      + "/".join(f"{q:+.3f}" for q in v["var"]) + f") -> {v['z_km']:.1f} sigma")
h1 = all(v["km"][0] > 0.2 and v["z_km"] > 3.0 for v in RES.values())
check("H1 [HEADLINE] robust to our analysis: with the upper limits (Kaplan-Meier) and the systematic floor, the median offset is > 0.2 dex "
      "and > 3 sigma on both footings" + ("  [MUTATE: dispersions halved]" if MUTATE else ""),
      "; ".join(f"{f}: {v['km'][0]:+.3f} dex, {v['z_km']:.1f} sigma" for f, v in RES.items()), h1)

R.banner("T2 / T4  TIDES AND PRECISION")
for foot, v in RES.items():
    P(f"    {foot:9s}: beyond 80 kpc {v['far'][0]:+.3f} +- {v['far'][1]:.3f} ({v['far'][2]} resolved + {v['far'][3]} limits); inside {v['near'][0]:+.3f} "
      f"+- {v['near'][1]:.3f} ({v['near'][2]} + {v['near'][3]}); Spearman(offset, distance) rho = {v['rho'][0]:+.2f} (p = {v['rho'][1]:.2f}); "
      f"error <= 25%: {v['prec'][0]:+.3f} +- {v['prec'][1]:.3f} (N = {v['prec'][2]})")
h2 = all(v["far"][0] > 0 and v["far"][0] / v["far"][1] > 2 and v["prec"][0] > 0 and v["prec"][0] / v["prec"][1] > 2 for v in RES.values())
check("H2 the offset survives the data tests: the far (> 80 kpc) and the precise (error <= 25%) subsamples each show a positive offset "
      "at > 2 sigma, both footings",
      "; ".join(f"{f}: far {v['far'][0] / v['far'][1]:.1f} sigma, precise {v['prec'][0] / v['prec'][1]:.1f} sigma" for f, v in RES.items()), h2)

# ================================================================================================ T3 floor vs factor
R.banner("T3  A CONSTANT FLOOR (BINARIES) OR A FACTOR (MISSING MASS)?")
T3 = {}
for foot, a0 in A0H.items():
    sp = np.array([spred(d, a0) for d in UFD]); spu = np.array([spred(d, a0) for d in UL])
    so = MUT * np.array([d["sig"] for d in UFD]); su = MUT * np.array([d["sig_ul"] for d in UL])

    def nll(p, model):
        par, tau = math.exp(p[0]), math.exp(p[1])
        m = np.sqrt(sp ** 2 + par ** 2) if model == "floor" else par * sp
        mu = np.sqrt(spu ** 2 + par ** 2) if model == "floor" else par * spu
        s_ = np.sqrt(ELOG ** 2 + tau ** 2)
        ll = np.sum(norm.logpdf(np.log10(so), np.log10(m), s_))
        ll += np.sum(norm.logcdf((np.log10(su) - np.log10(mu)) / np.sqrt(tau ** 2 + 0.05 ** 2)))
        return -ll
    out = {}
    for model, p0 in (("floor", [math.log(3.0), math.log(0.15)]), ("factor", [math.log(2.0), math.log(0.15)])):
        best = min((minimize(nll, [p0[0] + dp, p0[1] + dq], args=(model,), method="Nelder-Mead",
                             options=dict(xatol=1e-7, fatol=1e-9, maxiter=4000)) for dp in (-0.5, 0, 0.5) for dq in (-0.5, 0, 0.5)),
                   key=lambda r: r.fun)
        out[model] = dict(par=math.exp(best.x[0]), tau=math.exp(best.x[1]), lnL=-best.fun)
    out["dlnL_floor_minus_factor"] = out["floor"]["lnL"] - out["factor"]["lnL"]
    T3[foot] = out
    P(f"    {foot:9s}: floor s = {out['floor']['par']:.2f} km/s (scatter {out['floor']['tau']:.3f} dex, ln L {out['floor']['lnL']:.2f}); factor f = "
      f"{out['factor']['par']:.2f} (scatter {out['factor']['tau']:.3f} dex, ln L {out['factor']['lnL']:.2f}); Delta ln L (floor - factor) "
      f"{out['dlnL_floor_minus_factor']:+.2f}; predicted dispersions {sp.min():.2f}-{sp.max():.2f} km/s")
check("R1 (reported) T3: the floor and factor fits, and which the population prefers",
      "; ".join(f"{f}: s {v['floor']['par']:.2f} km/s, f {v['factor']['par']:.2f}, dlnL {v['dlnL_floor_minus_factor']:+.2f}" for f, v in T3.items()),
      True, load_bearing=False)
reading = ("the 8 sigma was made by our analysis" if not h1 else
           "it rests on the closest or least precise systems: inflation plausible, failure not established" if not h2 else
           "robust to our analysis and to the data tests available here; the decisive remaining test is multi-epoch, binary-corrected dispersions")
P(f"\n    READING (declared): {reading}")
R.num("RES", RES); R.num("T3", T3); R.num("reading", reading)
R.num("upper_limits", [dict(name=d["name"], sig_ul=d["sig_ul"], D=d["D"]) for d in UL])
nf = R.write()
sys.exit(1 if nf else 0)
