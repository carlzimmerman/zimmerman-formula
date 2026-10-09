#!/usr/bin/env python3
"""CFG520 POST-HOC diagnostics of the failed calibration (not a verdict; written after CALIBRATION FAILED was seen, 2026-10-09).

PH1: where the halos of the calibrated centrals sit relative to the 512^3 completeness mass (150 m_p), per rule.
PH2: the primary form (alpha = 1) fitted to the upper bin [10.75, 11.00) alone: the B that matches it, and the resulting curve / m_lim,box.
PH3: the fallback scan's best alpha sits on the declared edge (0.30); alpha 0.05-0.25 evaluated with the same fit (outside the frozen range).
S0 catalogues only. Run: nice -n 10 python3 cfg520_posthoc.py
"""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg520_lib as LB  # noqa: E402
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
CAL = json.load(open(os.path.join(HERE, "cfg520_calib_results.json")))
T = np.array(CAL["target"]["T"]); wa = np.array(CAL["target"]["w_a"]); EDGES = np.array([10.5, 10.75, 11.0])
CAT = {k: np.load(os.path.join(EXT, "cfg506_work", f"cfg506_box_{k}.npz")) for k in ("S0512_359", "S0512_360")}
LOG, RES = [], {}


def say(s=""):
    print(s, flush=True); LOG.append(s)


def shams(B, al): return [LB.Sham(Z["Mta"], float(Z["MP"]), B, al) for Z in CAT.values()]


def fbox(B, al, edges=EDGES): return np.mean([s.parent_fraction_expect(edges) for s in shams(B, al)], axis=0)


fine = np.arange(10.5, 11.11, 0.1)
say("PH1: log M_min(m) of the abundance match vs the completeness mass log(150 m_p) = %.2f" % math.log10(150 * float(CAT["S0512_359"]["MP"])))
rules = {"CFG506 (B 17)": (17.0, 1.0), "primary best": (CAL["primary"]["B"], 1.0), "fallback best": (CAL["fallback"]["B"], CAL["fallback"]["alpha"])}
for nm, (B, al) in rules.items():
    s = shams(B, al)[0]
    say(f"  {nm:14s} B {B:7.2f} alpha {al:.2f}: m_lim,box {s.mlim_box:.2f}; log M_min at log M* 10.5 / 10.6 / 10.75 / 11.0 = "
        + " / ".join(f"{float(s.lMmin_of_m(m)):.2f}" for m in (10.5, 10.6, 10.75, 11.0))
        + "; parent fraction per 0.1 dex " + ", ".join(f"{a:.1f}: {v:.3f}" for a, v in zip(fine[:-1], s.parent_fraction_expect(fine))))
    RES[f"PH1|{nm}"] = dict(B=B, alpha=al, m_lim_box=s.mlim_box, fpar=s.parent_fraction_expect(fine).tolist())

say("\nPH2: alpha = 1, B fitted to the upper bin [10.75, 11.00) alone")
g = lambda lb: fbox(10 ** lb, 1.0)[1] - T[1]
lb = brentq(g, 0.5, 3.0, xtol=1e-4)
fb = fbox(10 ** lb, 1.0); s = shams(10 ** lb, 1.0)[0]
say(f"  B {10 ** lb:.2f}: f_box {np.round(fb, 4).tolist()} vs T {np.round(T, 4).tolist()}; m_lim,box {s.mlim_box:.2f}; per 0.1 dex "
    + ", ".join(f"{a:.1f}: {v:.3f}" for a, v in zip(fine[:-1], s.parent_fraction_expect(fine))))
RES["PH2"] = dict(B=10 ** lb, f_box=fb.tolist(), m_lim_box=s.mlim_box)

say("\nPH3: alpha below the declared range (same weighted fit over both bins)")
from scipy.optimize import minimize_scalar
RES["PH3"] = []
for al in (0.05, 0.10, 0.15, 0.20, 0.25):
    r = minimize_scalar(lambda x: float((wa * (fbox(10 ** x, al) - T) ** 2).sum()), bounds=(0.0, 4.5), method="bounded", options=dict(xatol=1e-3))
    fb = fbox(10 ** r.x, al)
    ok = bool(np.all(np.abs(fb - T) <= 0.05) and abs((wa * fb).sum() - (wa * T).sum()) <= 0.02)
    say(f"  alpha {al:.2f}: B {10 ** r.x:9.2f}; f_box {np.round(fb, 4).tolist()} -> would pass CAL-OK: {ok}")
    RES["PH3"].append(dict(alpha=al, B=10 ** r.x, f_box=fb.tolist(), cal_ok_would_pass=ok))
json.dump(RES, open(os.path.join(HERE, "cfg520_posthoc_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg520_posthoc.out"), "w").write("\n".join(LOG) + "\n")
