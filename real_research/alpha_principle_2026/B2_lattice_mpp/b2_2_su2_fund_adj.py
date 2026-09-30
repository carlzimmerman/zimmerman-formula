#!/usr/bin/env python3
"""B2.2 -- SU(2) fundamental-adjoint lattice gauge theory: validation gates, the stage-1 structure map (susceptibility maxima of X_A along fixed-beta_F lines)
and the stage-2 refinement/triple-point analysis driven by a plan file written after stage 1 (declared in the pre-registration).
Action: S = beta_F sum (1 - x) + beta_A sum (1 - Tr_adj/3),  x = Tr U_p/2, Tr_adj = 4x^2 - 1.
Run:    python3 b2_2_su2_fund_adj.py [gates|stage1|full]      full (default) = gates + stage1 + stage2 (if b2_2_stage2_plan.json exists) + D-TP analysis
        exit 0 iff all declared internal gates pass; the physics RESULT is only reported.
MUTATE: python3 b2_2_su2_fund_adj.py MUTATE   update-side adjoint normalisation 1/2 instead of 1/3: gate G3 (reweighting consistency) must fail -> exit 1; exit 3 otherwise.
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np
import b2_lib as B

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "MUTATE" in sys.argv[1:]
MODE = [a for a in sys.argv[1:] if a != "MUTATE"]
MODE = MODE[0] if MODE else "full"
NW = int(os.environ.get("B2_WORKERS", "12"))
HITS = 6
FAILED = []
exe = B.build("su2z")   # Metropolis multi-hit + center-flip proposals (Amendment 5)


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def bessel_i(n, x):
    return sum((x / 2) ** (2 * k + n) / (math.factorial(k) * math.factorial(k + n)) for k in range(40))


def mean_se(x):
    t = B.tau_int(x)
    return float(np.mean(x)), float(np.std(x) / np.sqrt(len(x) / (2 * t)))


def gates():
    print("Declared validation gates (SU(2)):", flush=True)
    # G4 identity Tr_adj = 4 (Tr/2)^2 - 1 on random SU(2) elements, adjoint rep built from Pauli matrices
    rng = np.random.default_rng(1)
    sig = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]
    worst = 0.0
    for _ in range(200):
        q = rng.normal(size=4); q /= np.linalg.norm(q)
        U = q[0] * np.eye(2) + 1j * (q[1] * sig[0] + q[2] * sig[1] + q[3] * sig[2])
        R = np.array([[0.5 * np.trace(sig[a] @ U @ sig[b] @ U.conj().T).real for b in range(3)] for a in range(3)])
        worst = max(worst, abs(np.trace(R) - (4 * (0.5 * np.trace(U).real) ** 2 - 1)))
    if not MUT:
        chk("G4 Tr_adj = 4 (Tr U/2)^2 - 1 on 200 random SU(2) elements", worst < 1e-12, f"(worst {worst:.1e})")
    # G3 reweighting consistency: <X_A> at beta_A = 1.05 from the 1.00 runs vs direct, L=4, beta_F = 0.5 (two seeds pooled)
    def run(bF, bA, sd, mode, L=4, nsw=40000, nth=3000, hits=4, mut=MUT):
        a = [L, f"{bF:.4f}", f"{bA:.4f}", nsw, nth, sd, 0, hits, mode, int(mut)]
        return B.load(B.run_one(exe, a, "su2gate" + ("m" if mut else "")))
    d0 = np.vstack([run(0.5, 1.00, s, 0) for s in (11, 12)])
    d1 = np.vstack([run(0.5, 1.05, s, 0) for s in (13, 14)])
    Np = 6.0 * 4 ** 4
    x0 = d0[:, 1]
    w = np.exp((1.05 - 1.00) * Np * (x0 - x0.max()))
    rw = np.sum(w * x0) / np.sum(w)
    neff = 1.0 / np.sum((w / w.sum()) ** 2)
    se_rw = np.std(x0) / np.sqrt(neff / (2 * B.tau_int(x0)))
    m1, s1 = mean_se(d1[:, 1])
    ok3 = abs(rw - m1) < 4 * math.hypot(se_rw, s1)
    chk("G3 reweighting: <X_A>(1.05) from the 1.00 runs equals the direct 1.05 runs within 4 sigma (L=4, beta_F=0.5)", ok3, f"(rw {rw:.5f} +- {se_rw:.5f}; direct {m1:.5f} +- {s1:.5f}; ESS {neff:.0f})")
    if MUT:
        return ok3
    # G1 heat bath vs Metropolis at beta_A = 0, beta_F = 2.2, 4^4
    hb = np.vstack([run(2.2, 0.0, s, 1, nsw=30000, nth=2000) for s in (21, 22)])[:, 0]
    me = np.vstack([run(2.2, 0.0, s, 0, nsw=30000, nth=2000, hits=6) for s in (23, 24)])[:, 0]
    a, sa = mean_se(hb); b, sb = mean_se(me)
    chk("G1 Metropolis multi-hit equals the independent Creutz heat bath at beta_A = 0, beta_F = 2.2 (4^4) within 4 sigma", abs(a - b) < 4 * math.hypot(sa, sb), f"(HB {a:.5f} +- {sa:.5f}; Metropolis {b:.5f} +- {sb:.5f})")
    # G2 strong coupling: x = u + 4 u^5, u = I2(1)/I1(1) at beta_F = 1 (beta_A = 0), 6^4
    sc = run(1.0, 0.0, 31, 0, L=6, nsw=6000, nth=500)[:, 0]
    u = bessel_i(2, 1.0) / bessel_i(1, 1.0)
    pred = u + 4 * u ** 5
    m, se = mean_se(sc)
    chk("G2 strong-coupling series <x> = u + 4u^5 (u = I2(1)/I1(1)) at beta_F = 1 (6^4) within 0.003", abs(m - pred) < 0.003, f"(measured {m:.5f} +- {se:.5f}; series {pred:.5f})")
    return ok3


G3ok = gates()
if MUT:
    print("\nMUTATE CONTROL: update-side adjoint normalisation 1/2 instead of 1/3 -> G3", "FAILS as required (exit 1, the control fires)" if not G3ok else "did NOT fail: CONTROL BROKEN (exit 3)")
    sys.exit(1 if not G3ok else 3)
if MODE == "gates":
    sys.exit(0 if not FAILED else 1)

# --------------------------------------------------------------------------------------------------------------------------- stage 1
BF1 = [0.0, 0.2, 0.4, 0.54, 0.7, 0.9, 1.2]
BA1 = np.round(np.arange(1.4, 3.0001, 0.1), 4).tolist()
results = {"stage1": {}, "stage2": {}}
print("\nStage 1H hysteresis map, L=4 (Amendment 4): X_A from cold / hot starts; '*' = |diff| > 5 sigma and > 0.005 (first-order-like)", flush=True)
hm = B.hyst_map("su2z", 4, BF1, BA1, 4000, 1000, HITS, nw=NW)
for bF in BF1:
    fl = [bA for bA in BA1 if hm[(bF, bA)][6]]
    print(f"  beta_F={bF:4.2f}: flagged beta_A = {fl if fl else 'none'}", flush=True)
    results["stage1"][str(bF)] = {str(bA): hm[(bF, bA)] for bA in BA1}
json.dump(results, open(os.path.join(HERE, "2_su2_stage1H.json" if False else "b2_2_stage1H.json"), "w"), indent=1)
print("  full table (beta_A: X_A cold, X_A hot):", flush=True)
for bF in BF1:
    print(f"   beta_F={bF:4.2f}: " + " ".join(f"{bA:.2f}:{hm[(bF, bA)][0]:.3f}/{hm[(bF, bA)][2]:.3f}{'*' if hm[(bF, bA)][6] else ''}" for bA in BA1), flush=True)
if MODE == "stage1":
    sys.exit(0 if not FAILED else 1)

# --------------------------------------------------------------------------------------------------------------------------- stage 2
plan_path = os.path.join(HERE, "b2_2_stage2_plan.json")
if not os.path.exists(plan_path):
    print("\nno stage-2 plan file yet; stopping after stage 1", flush=True)
    sys.exit(0 if not FAILED else 1)
plan = json.load(open(plan_path))
print(f"\nStage 2 plan ({os.path.basename(plan_path)}): {plan.get('note', '')}", flush=True)
for item in plan["scans"]:
    r = B.scan_line("su2z", item["kind"], item["L"], item["fixed"], item["grid"], item["nsw"], item["nth"], item["seeds"], HITS, nw=NW, fine=item.get("fine", 0.005), tag_extra="s2")
    key = f"{item['kind']}_{item['L']}_{item['fixed']}"
    results["stage2"][key] = {k: v for k, v in r.items() if k != "curve"}
    mstr = "; ".join(f"x={m['x']:.4f}+-{m['err']:.4f} chi={m['chi']:.2f}{' EDGE' if m['edge'] else ''}" for m in r["maxima"])
    print(f"  {item['kind']}-scan L={item['L']} fixed={item['fixed']}: {mstr}   [tau_int max {r['tau_max']:.0f}, infl {r['infl']:.2f}]", flush=True)
json.dump(results, open(os.path.join(HERE, "b2_2_results.json"), "w"), indent=1)
print("\nresults written to b2_2_results.json (analysed by the D-TP section / b2_4)", flush=True)
sys.exit(0 if not FAILED else 1)
