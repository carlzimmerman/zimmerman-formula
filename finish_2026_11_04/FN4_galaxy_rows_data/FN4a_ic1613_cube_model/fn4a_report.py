#!/usr/bin/env python3
"""FN4a report: the frozen label from stage 0 and M_free, every check, and the post-result reading of the fits.
Reads fn4a_s0.json and cache/fit_*.json; writes fn4a.out / fn4a.json. Run: python3 -I fn4a_report.py
kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.join(HERE, "cache")
J = lambda n: json.load(open(os.path.join(CA, f"fit_{n}.json")))
s0 = json.load(open(os.path.join(HERE, "fn4a_s0.json"))); fr = J("free"); k = len(fr["V"]); LINE = float(chi2.ppf(0.95, k)); LO, HI = 24.5, 45.8
OUT = []; R = {}
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def reading(free, scans):
    """the frozen label rule applied to fits: per scan, the inclinations where chi2 - chi2_free <= LINE."""
    ok_in = any(LO <= r["inc"] <= HI and r["chi2"] - free["chi2"] <= LINE for s in scans for r in s["rows"])
    ok_lo = any(r["inc"] < LO and r["chi2"] - free["chi2"] <= LINE for s in scans for r in s["rows"])
    if free["chi2_red"] > 1.5: return "NOT EVALUABLE (M_free chi2_red > 1.5)"
    if ok_in: return "LAW FITS THE CUBE"
    if ok_lo: return "LAW FITS ONLY BELOW 24.5"
    return "GENUINE OVER-PREDICTION"


P("FN4a IC 1613 in its LITTLE THINGS cube. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework.")
S0a, S0b = s0["S0a"]["passed"], s0["S0b"]["passed"]; free_ok = fr["chi2_red"] <= 1.5
label = "NOT EVALUABLE" if not (S0a and S0b and free_ok) else None
P(f"S0a HI mass: {s0['S0a']['MHI_D07']:.3e} Msun at 0.7 Mpc against Oh+15 {s0['S0a']['Oh15_MHI']:.3e} (ratio {s0['S0a']['ratio']:.3f}; line 10 %) -> {'PASS' if S0a else 'FAIL'}")
P(f"S0b V(R_max): corrected {s0['S0b']['V_c_corrected']:.2f}, uncorrected {s0['S0b']['V_rot_uncorrected']:.2f}, against Oh+15 16.9 (line 2 km/s on the corrected value, A2) -> {'PASS' if S0b else 'FAIL'}")
P(f"M_free: chi2 {fr['chi2']:.1f} on {fr['ndat']:,} voxels, chi2_red {fr['chi2_red']:.3f} (line 1.5) -> {'PASS' if free_ok else 'FAIL'}; i {fr['inc']:.1f}, PA {fr['pa']:.1f}")
R["frozen_label"] = label or "see readings"; R["checks"] = dict(S0a=S0a, S0b=S0b, M_free_chi2_red=fr["chi2_red"], line_chi2_095=LINE, k=k)
scans = {}
for f in ("canonical", "alt"):
    sc = [J(f"law_{f}")] + ([J(f"nc_{f}")] if os.path.exists(os.path.join(CA, f"fit_nc_{f}.json")) else [])
    scans[f] = sc
    for s in sc:
        P(f"[{f}] {s['stage']}: delta chi2 by i: " + ", ".join(f"{r['inc']:g} {r['chi2'] - fr['chi2']:+.0f}" for r in s["rows"]) + f"; best i {s['best_inc']:g}")
    R[f"reading_{f}"] = reading(fr, sc); P(f"[{f}] the frozen rule read on these fits (POST-RESULT): {R[f'reading_{f}']}; without the M_free line: "
                                          + reading(dict(fr, chi2_red=1.0), sc))
nw = J("newton"); ka3 = min(r["chi2"] for r in nw["rows"]) - fr["chi2"] > LINE
R["KA3"] = dict(best_delta=min(r["chi2"] for r in nw["rows"]) - fr["chi2"], passed=ka3)
P(f"KA3 Newton: best delta chi2 {R['KA3']['best_delta']:+.0f} at i {nw['best_inc']:g} (must exceed {LINE:.1f}) -> {'PASS' if ka3 else 'FAIL'}")
for ka, want in (("ka1", "LAW FITS THE CUBE"), ("ka2", "GENUINE OVER-PREDICTION")):
    if not os.path.exists(os.path.join(CA, f"fit_{ka}.json")): P(f"{ka.upper()} not run"); continue
    d = J(ka); rd = reading(d["free"], [d["law"]]); ok = rd == want
    if ka == "ka1": ok = ok and abs(d["law"]["best_inc"] - 35.0) <= 5.0
    R[ka.upper()] = dict(reading=rd, want=want, free_chi2_red=d["free"]["chi2_red"], free_inc=d["free"]["inc"], law_best_inc=d["law"]["best_inc"],
                         delta_by_inc={r["inc"]: r["chi2"] - d["free"]["chi2"] for r in d["law"]["rows"]}, passed=ok)
    P(f"{ka.upper()}: mock M_free chi2_red {d['free']['chi2_red']:.3f}, i {d['free']['inc']:.1f}; M_law best i {d['law']['best_inc']:g}; reading {rd} (want {want}) -> {'PASS' if ok else 'FAIL'}")
mu = J("mutate"); mb = mu["chi2_red"] > 1.5; R["MUTATE"] = dict(chi2_red=mu["chi2_red"], bites=mb)
P(f"MUTATE (channels shuffled): M_free chi2_red {mu['chi2_red']:.3f} -> {'BITES (NOT EVALUABLE)' if mb else 'DID NOT BITE'}")
P(f"\nLABEL (frozen): {R['frozen_label']}" + (" (stage-0 check failed: " + ", ".join(n for n, v in (("S0a", S0a), ("S0b", S0b)) if not v) + ("; M_free chi2_red > 1.5" if not free_ok else "") + ")" if label else ""))
json.dump(R, open(os.path.join(HERE, "fn4a.json"), "w"), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, "fn4a.out"), "w").write("\n".join(OUT) + "\n")
