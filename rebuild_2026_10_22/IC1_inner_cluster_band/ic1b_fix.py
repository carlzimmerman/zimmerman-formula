#!/usr/bin/env python3
"""IC1_inner_cluster_band -- frozen criteria FROZEN_CRITERIA.md (4bf9ef4e51); amendment A1 (table resolution).

F-ISO: LN1 T7's non-singular isothermal core shape replaces X38's Burkert; q re-calibrated once on SPARC (OS1's rule);
all 15 X38 cluster cells graded, both footings.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ic1b_fix.py            -> ic1b_fix.out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ic1b_fix.py --mutate   -> singular isothermal (no core); K1 must fail
"""
import os, sys, json, math, time, resource
T0 = time.time()
MUTATE = "--mutate" in sys.argv; TAG = "_MUTATE" if MUTATE else ""
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.integrate import solve_ivp, quad
import ic1b_lib as L

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
if MUTATE: L.SHAPES["isothermal"] = lambda x: 8 * np.asarray(x, float) / 9
P(f"IC1_inner_cluster_band F-ISO {'MUTATE (singular isothermal, no core)' if MUTATE else 'normal run'}  (frozen 4bf9ef4e51)")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; not theory closed")
checks = []; RES = dict(frozen="4bf9ef4e51", mutate=MUTATE, footings={})

# K1 isothermal table vs independent quadrature
le = solve_ivp(lambda t, y: [y[1], math.exp(-y[0]) - 2 * y[1] / t], (1e-6, 200.0), [1e-12 / 6, 1e-6 / 3],
               dense_output=True, rtol=1e-12, atol=1e-15, method="LSODA")
Bq = lambda x: 4 * quad(lambda u: math.exp(-le.sol(3 * u)[0]) * u * u if u > 1e-6 / 3 else u * u, 0, x, epsabs=0, epsrel=1e-11, limit=500)[0]
Bi = L.SHAPES["isothermal"]
dq = max(abs(float(Bi(x)) / Bq(x) - 1) for x in (0.01, 0.3, 1, 3, 30))
dl = abs(float(Bi(1e4)) / (8e4 / 9) - 1); ds = abs(float(Bi(1e-3)) / (4e-9 / 3) - 1)
pp = L.prep(0, "canonical", "h0672"); Sg = L.SIG["canonical"] * 3.0
r0t, _ = L.solve_r0_shape(pp["Mfair"], pp["rta"], Sg, Bi); dm = abs(math.pi * Sg * r0t ** 2 * float(Bi(pp["rta"] / r0t)) / pp["Mfair"] - 1)
L.PREP.clear()
k1 = dq < 1e-6 and dl < 0.02 and ds < 1e-3 and dm < 1e-8
P(f"K1 isothermal table: quadrature max rel {dq:.1e}; large-x {dl:.1e}; small-x {ds:.1e}; solved r0 mass {dm:.1e}: {'PASS' if k1 else 'FAIL'}")
checks.append(("K1", k1))

def calibrate(foot, shape):
    cache = {}; bg = L.BGS["A_c2b_refit"]
    def rms(q):
        if q not in cache: cache[q] = L.sparc(foot, bg, q, shape)
        return cache[q]["rms"]
    coarse = [round(0.02 * i, 3) for i in range(61)]; qc = min(coarse, key=rms)
    fine = sorted({round(qc + 0.002 * j, 4) for j in range(-10, 11) if 0 <= qc + 0.002 * j <= 1.2})
    qf = min(fine, key=rms); return qf, cache[qf], rms(0.0), {q: cache[q]["rms"] for q in coarse}

classes = {}
for foot in L.FEET:
    o1 = L.OS1J["footings"][foot]; o1c = o1["clusters"]["cells"]; o1ok = o1["clusters"]["ok"]; R = {}
    if not MUTATE:
        qb, sb, _, _ = calibrate(foot, "burkert"); cb, _, _ = L.grade(foot, qb)
        dpr = max(abs(cb[h][k]["pred"] - o1c[h][k]["pred"]) for h in L.HK for k in o1c[h])
        k0 = qb == o1["q_f"] and abs(sb["rms"] - o1["sparc_A"]["rms"]) < 1e-9 and dpr < 1e-9
        P(f"\n=== [{foot}] K0 Burkert path: q_f {qb:.3f} (OS1 {o1['q_f']:.3f}), SPARC {sb['rms']:.4f}, cluster |dpred| {dpr:.1e}: {'PASS' if k0 else 'FAIL'}"
          f"   [{time.time() - T0:.0f} s]")
        checks.append((f"K0[{foot}]", k0))
    else:
        P(f"\n=== [{foot}] MUTATE")
    qi, si, r0_, curve = calibrate(foot, "isothermal"); lok = L.line(si)
    sB = L.sparc(foot, L.BGS["B_cfg886_bg"], qi, "isothermal")
    P(f"   F-ISO calibration: q_iso = {qi:.3f} (Burkert q_f {o1['q_f']:.3f}); SPARC A rms {si['rms']:.4f} @ U {si['U_median']:.2f} "
      f"(q=0: {r0_:.4f}; Burkert at q_f {o1['sparc_A']['rms']:.4f}); line {'PASS' if lok else 'FAIL'}; bg B {sB['rms']:.4f} @ U {sB['U_median']:.2f}"
      f"   [{time.time() - T0:.0f} s]")
    cells, ok, nsat = L.grade(foot, qi, "isothermal")
    for k in cells["h0672"]:
        a, b = cells["h0672"][k], cells["h0686"][k]
        P(f"     {k:10s} meas {a['meas']:+.3f}+-{a['s']:.3f} pred {a['pred']:+.3f} Z {a['Z']:+.2f} / h0686 {b['Z']:+.2f}  (OS1 {o1c['h0672'][k]['Z']:+.2f})"
          + ("" if ok[k] else "  FAIL"))
    newfail = [k for k in ok if o1ok[k] and not ok[k]]
    zin = max(abs(cells[h]["G-IN-Mall"]["Z"]) for h in L.HK); zin1 = max(abs(o1c[h]["G-IN-Mall"]["Z"]) for h in L.HK)
    if lok and all(ok.values()): cls = "PASS"
    elif lok and not newfail and 2 < zin < zin1: cls = "IMPROVES"
    else: cls = "FAILS"
    P(f"   G-IN-Mall max|Z| {zin1:.2f} -> {zin:.2f}; OS1-passing cells now failing: {newfail or 'none'}; saturated halos {nsat}")
    near = {}
    for dq_ in (-0.05, 0.05):
        _, okv, _ = L.grade(foot, round(qi + dq_, 4), "isothermal"); near[f"{qi + dq_:.3f}"] = [k for k in okv if not okv[k]]
    P(f"   (reported) fails at q_iso -/+ 0.05: {near}")
    P(f"   CLASS [{foot}]: {cls}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    classes[foot] = cls
    RES["footings"][foot] = dict(q_iso=qi, sparc_A=dict(rms=si["rms"], U=si["U_median"], line=lok), sparc_B=dict(rms=sB["rms"], U=sB["U_median"]),
                                 rms_curve=curve, cells=cells, ok=ok, new_fail=newfail, zin=zin, zin_os1=zin1, nsat=nsat, near=near, cls=cls)
RES["verdict"] = classes["canonical"] if classes["canonical"] == classes["alt"] else f"UNDECIDED (footings disagree: {classes})"
P(f"\n=== VERDICT{' (MUTATE, reported only)' if MUTATE else ''}: {RES['verdict']}")
checks.append(("K2", rss() < 2.0))
n = sum(v for _, v in checks); P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks)
                                + f"; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
RES["checks"] = {k: bool(v) for k, v in checks}
open(os.path.join(L.HERE, f"ic1b_fix{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(L.HERE, f"ic1b_fix_results{TAG}.json"), "w"), indent=1, default=float)
if MUTATE: sys.exit(1 if not RES["checks"]["K1"] else 0)
sys.exit(0 if n == len(checks) else 1)
