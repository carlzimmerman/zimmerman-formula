#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG29 -- THE BINARY AUDIT OF THE ULTRA-FAINT FAILURE: can unresolved binary stars make the offset CFG28 left standing (+0.30-0.33
dex, 3.5-3.8 sigma), or is it beyond what binaries can do?

WHY.  CFG28 found the ultra-faint offset robust to our analysis, to tides and to measurement noise; binaries were the one escape.
Two published results bound what binaries can do, and both are used here as fixed inputs, not fitted:
  (a) single-epoch data: Monte Carlo populations of unresolved binaries are "unlikely to produce dispersions much in excess of
      ~4.5 km/s", even from a near-zero intrinsic dispersion (McConnachie & Cote 2010, ApJL);
  (b) multi-epoch data: with a 10-year baseline the residual binary bias reaches ~10-120% for systems whose true dispersion is below
      ~1 km/s, and is smaller for hotter systems (Ou et al. 2026, arXiv:2609.19407).
So binaries are strongest where the true dispersion is smallest.  Where the framework predicts a larger dispersion, and wherever
the measured dispersion exceeds the single-epoch ceiling, binaries cannot close a factor-2 gap.  The data (the committed LVD table;
the reference for each dispersion, ref_vlos, is carried) and FG001's estimator are CFG28's, exec'd read-only.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  CFG28's committed Kaplan-Meier medians (+0.325 / +0.304 dex) reproduced.
  H1  [HEADLINE; MUTATE must fail] where binaries are weak -- the ultra-faints whose framework-predicted dispersion is >= 1.5 km/s --
      the median offset (Kaplan-Meier with the upper limits) is > 0.2 dex and > 3 sigma with CFG28's systematic floor, both footings.
  H2  at least one ultra-faint beyond 80 kpc (negligible tides) has a measured dispersion above the single-epoch binary ceiling
      (4.5 km/s) by more than 2 sigma: a system binaries cannot explain even in principle.
  R1  (reported) the offset for predicted dispersion >= 2 km/s and < 1.5 km/s; per system, the binary floor the framework would
      need, sqrt(sigma_obs^2 - sigma_pred^2), against the caps (a) and (b); the dispersion references.
  READING: H1 PASS -> the offset persists where binaries are weakest, so binaries do not explain the failure; H1 FAIL -> the
  offset lives in the coldest systems, where binaries are strongest, and the failure is not established.
MUTATE=1: every dispersion and limit is halved (CFG28's control) -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG29_ufd_binary_audit.py   (MUTATE=1 for the control; ~10 s)
"""
import os, sys, math, json, io, contextlib, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG29_ufd_binary_audit", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every dispersion and limit halved -- H1 must FAIL ***")

# CFG28's machinery (FG001's loader and estimator, the upper-limit loader, Kaplan-Meier, bootstrap), exec'd read-only, unmutated
C28P = os.path.join(HERE, "CFG28_ufd_referee.py")
s28 = open(C28P).read()
cut = s28.index("# ================================================================================================ C1")
g = {"__file__": C28P, "__name__": "cfg28_prefix"}
_env = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s28[:cut], C28P, "exec"), g)
if _env is None:
    os.environ.pop("MUTATE")
else:
    os.environ["MUTATE"] = _env
UFD, UL, spred, km_median, boot, A0H = g["UFD"], g["UL"], g["spred"], g["km_median"], g["boot"], g["A0H"]
C28 = json.load(open(os.path.join(HERE, "CFG28_ufd_referee_results.json")))["numbers"]["RES"]
MUT = 0.5 if MUTATE else 1.0
REF = {r["name"]: r["ref_vlos"] for r in csv.DictReader(open(os.path.join(g["ns"]["DSPH"], "lvd_dwarf_mw.csv")))}
CAP_SE = 4.5                                                                                   # McConnachie & Cote 2010

# ================================================================================================ C1
R.banner("C1  CONTROL: CFG28's Kaplan-Meier medians")
dev = 0.0
for foot, a0 in A0H.items():
    x = np.array([math.log10(d["sig"] / spred(d, a0)) for d in UFD]); xu = np.array([math.log10(d["sig_ul"] / spred(d, a0)) for d in UL])
    dev = max(dev, abs(km_median(x, xu) - C28[foot]["km"][0]))
check("C1 CONTROL: CFG28's committed Kaplan-Meier medians reproduced", f"max |d| {dev:.1e}", dev <= 1e-12)

# ================================================================================================ H1 / R1
R.banner("H1  WHERE BINARIES ARE WEAKEST: the ultra-faints the framework predicts at >= 1.5 km/s")
OUT = {}
for foot, a0 in A0H.items():
    sp = np.array([spred(d, a0) for d in UFD]); spu = np.array([spred(d, a0) for d in UL])
    so = MUT * np.array([d["sig"] for d in UFD]); su = MUT * np.array([d["sig_ul"] for d in UL])
    x, xu = np.log10(so / sp), np.log10(su / spu)
    floor = C28[foot]["floor"]
    rows = {}
    for lab, cut_, cutu in (("pred >= 1.5", sp >= 1.5, spu >= 1.5), ("pred >= 2.0", sp >= 2.0, spu >= 2.0), ("pred < 1.5", sp < 1.5, spu < 1.5)):
        m = km_median(x[cut_], xu[cutu]); e = boot(km_median, x[cut_], xu[cutu])
        rows[lab] = dict(med=m, err=e, z=m / math.sqrt(e ** 2 + floor ** 2), n=int(cut_.sum()), nu=int(cutu.sum()))
    OUT[foot] = dict(rows=rows, floor=floor)
    P(f"    {foot:9s}: " + "; ".join(f"{k}: {v['med']:+.3f} +- {v['err']:.3f} ({v['n']} + {v['nu']} limits) -> {v['z']:.1f} sigma" for k, v in rows.items()))
h1 = all(OUT[f]["rows"]["pred >= 1.5"]["med"] > 0.2 and OUT[f]["rows"]["pred >= 1.5"]["z"] > 3.0 for f in OUT)
check("H1 [HEADLINE] where binaries are weakest (framework-predicted dispersion >= 1.5 km/s) the median offset is > 0.2 dex and > 3 sigma "
      "with CFG28's floor, both footings" + ("  [MUTATE: dispersions halved]" if MUTATE else ""),
      "; ".join(f"{f}: {v['rows']['pred >= 1.5']['med']:+.3f} dex, {v['rows']['pred >= 1.5']['z']:.1f} sigma" for f, v in OUT.items()), h1)

# ================================================================================================ H2 the single-epoch ceiling
R.banner("H2  BEYOND THE SINGLE-EPOCH BINARY CEILING (4.5 km/s, McConnachie & Cote 2010), FAR FROM THE MILKY WAY")
a0c = A0H["canonical"]
beyond = []
for d in UFD:
    s_ = MUT * d["sig"]; e_ = MUT * d["esig"]
    zc = (s_ - CAP_SE) / e_
    sp_ = spred(d, a0c)
    need = math.sqrt(max(s_ ** 2 - sp_ ** 2, 0.0))
    d["_row"] = dict(name=d["name"], sig=s_, err=e_, D=d["D"], pred=sp_, need=need, z_cap=zc, ref=REF.get(d["name"], ""))
    if d["D"] > 80 and zc > 2:
        beyond.append(d["_row"])
for r_ in sorted((d["_row"] for d in UFD), key=lambda r: -r["need"]):
    P(f"    {r_['name']:18s} D {r_['D']:6.1f} kpc  sigma {r_['sig']:5.2f} +- {r_['err']:4.2f}  predicted {r_['pred']:4.2f}  binary floor needed "
      f"{r_['need']:4.2f} km/s  (above 4.5 km/s by {r_['z_cap']:+.1f} sigma)  [{r_['ref']}]")
h2 = len(beyond) >= 1
check("H2 at least one ultra-faint beyond 80 kpc has a dispersion above the single-epoch binary ceiling (4.5 km/s) by > 2 sigma",
      ("; ".join(f"{b['name']} ({b['sig']:.1f} +- {b['err']:.1f} km/s at {b['D']:.0f} kpc, {b['z_cap']:.1f} sigma above)" for b in beyond) or "none"), h2)
needs = np.array([d["_row"]["need"] for d in UFD])
P(f"\n    binary floor the framework needs (canonical): median {np.median(needs):.2f} km/s; {int((needs > 2.0).sum())} of {len(needs)} systems need "
  f"more than 2.0 km/s (about the most a 10-yr multi-epoch baseline leaves for a true dispersion near 1 km/s, Ou et al. 2026)")
reading = ("binaries do not explain the failure: the offset persists where binaries are weakest" if h1 else
           "the offset lives in the coldest systems, where binaries are strongest: the failure is not established")
P(f"    READING (declared): {reading}")
check("R1 (reported) the per-system binary floors and the references", f"median floor {np.median(needs):.2f} km/s; beyond the ceiling: "
      f"{len(beyond)}", True, load_bearing=False)
R.num("H1", OUT); R.num("beyond_ceiling", beyond); R.num("per_system", [d["_row"] for d in UFD]); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
