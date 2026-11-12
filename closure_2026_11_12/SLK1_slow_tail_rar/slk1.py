#!/usr/bin/env python3
"""SLK1 (SLOW-TAIL KERNEL ON THE RADIAL ACCELERATION RELATION).  Frozen criteria: FROZEN_CRITERIA.md (commit 08f20ab497).

The Codex slow-tail kernel mu = 1 - 1/sqrt(1+2x) against law S, law B and the published fitting function on the
published SPARC radial acceleration relation (Lelli et al. 2017, data behind Fig. 2), as published.  A test lane.

Run:   python3 -I slk1.py
       SLK1_MUTATE=newton python3 -I slk1.py        (must exit 1)
"""
import hashlib, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "sol61_push", "cold_production_2026_10_11", "empirical_2026_10_12", "RAR.mrt")
MUT = (os.environ.get("SLK1_MUTATE", "") or "").strip()
FOOT = {"canonical": 9.3603e-11, "alt": 1.132e-10}
EDGES = [-12.0, -11.5, -11.0, -10.5, -10.0, -9.5, -8.5]
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def g_K(gN, a0):
    y = np.maximum(np.asarray(gN, float) / a0, 1e-300); v = 1.0 + np.sqrt(2.0 * y)
    for _ in range(80):
        f = v ** 3 + 2.0 * v * v - 2.0 * y * v - 2.0 * y; v = v - f / (3.0 * v * v + 4.0 * v - 2.0 * y)
    return 0.5 * v * (v + 2.0) * a0
def g_S(gN, a0): return 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / gN))
def g_B(gN, a0): return np.sqrt(gN * gN + a0 * gN)
def g_R(gN, a0): return gN / (1.0 - np.exp(-np.sqrt(gN / a0)))
KERN = {"K": g_K, "S": g_S, "B": g_B, "R": g_R}

def stats(lgb, egb, lgo, ego, fun, a0, shift=0.0):
    gb = 10.0 ** (lgb + shift); lp = np.log10(fun(gb, a0)); r = lgo - lp
    slope = (np.log10(fun(gb * 1.01, a0)) - lp) / math.log10(1.01)
    chi2 = float(np.sum(r * r / (ego ** 2 + (slope * egb) ** 2)) / (len(r) - 1))
    med = [float(np.median(r[(lgb >= lo) & (lgb < hi)])) for lo, hi in zip(EDGES[:-1], EDGES[1:]) if np.sum((lgb >= lo) & (lgb < hi)) >= 20]
    return dict(rms=float(np.sqrt(np.mean(r * r))), median=float(np.median(r)), trend=float(max(med) - min(med)), chi2=chi2, bins=med)

def main():
    tag = "slk1" + ("_MUTATE_" + MUT if MUT else "")
    P("SLK1 (SLOW-TAIL KERNEL ON THE RADIAL ACCELERATION RELATION)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    rows = []
    for l in open(DATA):
        p = l.split()
        if len(p) == 4:
            try: rows.append([float(x) for x in p])
            except ValueError: pass
    A = np.array(rows); lgb, egb, lgo, ego = A.T
    P("\n[data] %s  sha256 %s  points %d" % (os.path.relpath(DATA, REPO), hashlib.sha256(open(DATA, "rb").read()).hexdigest()[:16], len(A)))
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    P("\n[instrument checks]")
    r1 = stats(lgb, egb, lgo, ego, g_R, 1.20e-10)["rms"]
    ck("R1", "published fitting function at a0 = 1.20e-10: rms 0.13 +- 0.01 dex", "%.4f" % r1, abs(r1 - 0.13) <= 0.01)
    y = np.logspace(-6, 8, 400); x = g_K(y, 1.0); e1 = float(np.max(np.abs(x * (1.0 - 1.0 / np.sqrt(1.0 + 2.0 * x)) / y - 1.0)))
    xs = g_S(y, 1.0); e2 = float(np.max(np.abs(xs * xs / (1.0 + xs) / y - 1.0)))
    ck("R2", "kernel inversions: K to 1e-10, S to 1e-12", "%.1e ; %.1e" % (e1, e2), e1 < 1e-10 and e2 < 1e-12)

    foot = {k: (1.0e-30 if MUT == "newton" else v) for k, v in FOOT.items()}
    RES = dict(lane="SLK1", criteria_commit="08f20ab497", mutate=MUT, n=len(A), checks=CK, fixed={}, shift={}, a0free={})
    P("\n[fixed footings, as published]   kernel: rms, median, trend, reduced chi2, binned medians")
    for nm, a0 in foot.items():
        for k in ("K", "S", "B", "R"):
            st = stats(lgb, egb, lgo, ego, KERN[k], a0); RES["fixed"]["%s_%s" % (k, nm)] = st
            P("  %-9s %s  rms %.4f  median %+.4f  trend %.4f  chi2 %.2f   bins %s" % (nm, k, st["rms"], st["median"], st["trend"], st["chi2"], " ".join("%+.3f" % b for b in st["bins"])))
    words = {}
    for nm in foot:
        K, S = RES["fixed"]["K_" + nm], RES["fixed"]["S_" + nm]
        if K["rms"] <= S["rms"] + 0.010 and K["trend"] <= S["trend"] + 0.03 and abs(K["median"]) <= abs(S["median"]) + 0.03: w = "RAR COMPARABLE"
        elif K["rms"] >= S["rms"] + 0.020 or K["trend"] >= S["trend"] + 0.06: w = "RAR WORSE"
        else: w = "RAR MARGINAL"
        words[nm] = w
        P("  %-9s K against S: rms %+.4f, trend %+.4f, |median| %+.4f  -> %s" % (nm, K["rms"] - S["rms"], K["trend"] - S["trend"], abs(K["median"]) - abs(S["median"]), w))
    verdict = "%s / %s" % (words["canonical"], words["alt"]); RES["verdict"] = verdict
    if MUT:
        ref = json.load(open(os.path.join(HERE, "slk1_results.json")))["fixed"]
        up = all(RES["fixed"]["K_" + k]["rms"] > ref["K_" + k]["rms"] for k in FOOT)
        P("\n[MUTATE %s] rms of K: canonical %.3f (ref %.3f), alt %.3f (ref %.3f) -> %s" % (MUT, RES["fixed"]["K_canonical"]["rms"], ref["K_canonical"]["rms"],
          RES["fixed"]["K_alt"]["rms"], ref["K_alt"]["rms"], "rose on both footings, as required; exit 1" if up else "DID NOT RISE"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if up else 2)

    P("\n[reported: one global shift of log g_bar free within +-0.15 dex, minimising the rms]")
    grid = np.arange(-0.15, 0.1501, 0.005)
    for nm, a0 in foot.items():
        for k in ("K", "S", "B", "R"):
            rr = [stats(lgb, egb, lgo, ego, KERN[k], a0, s)["rms"] for s in grid]; s = float(grid[int(np.argmin(rr))]); st = stats(lgb, egb, lgo, ego, KERN[k], a0, s)
            st["shift"] = s; RES["shift"]["%s_%s" % (k, nm)] = st
            P("  %-9s %s  shift %+.3f dex%s  rms %.4f  median %+.4f  trend %.4f  chi2 %.2f" % (nm, k, s, " (at the limit)" if abs(abs(s) - 0.15) < 1e-6 else "", st["rms"], st["median"], st["trend"], st["chi2"]))
    P("\n[reported: a0 free, minimising the rms]")
    ag = np.logspace(math.log10(3e-11), math.log10(3e-10), 201)
    for k in ("K", "S", "B", "R"):
        rr = [stats(lgb, egb, lgo, ego, KERN[k], a)["rms"] for a in ag]; ab = float(ag[int(np.argmin(rr))]); st = stats(lgb, egb, lgo, ego, KERN[k], ab); st["a0"] = ab
        RES["a0free"][k] = st
        P("  %s  a0 = %.3e m/s^2  rms %.4f  median %+.4f  trend %.4f  chi2 %.2f" % (k, ab, st["rms"], st["median"], st["trend"], st["chi2"]))
    allok = all(v["ok"] for v in CK.values())
    P("\n[summary]")
    P("  instrument checks: %s" % ("all pass" if allok else "FAILED -> NOT EVALUABLE"))
    P("  LANE WORD (K against S, canonical / alt): %s" % (verdict if allok else "NOT EVALUABLE"))
    P("  kappa = 1/2 FITTED. A test lane; adopts nothing. No outcome favours the framework.")
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
