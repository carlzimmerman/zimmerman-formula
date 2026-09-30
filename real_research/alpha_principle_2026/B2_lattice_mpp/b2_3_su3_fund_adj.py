#!/usr/bin/env python3
"""B2.3 -- SU(3) fundamental-adjoint lattice gauge theory: validation gates, the stage-1 structure map (susceptibility maxima of X_A along fixed-beta_F lines)
and the stage-2 refinement/triple-point data driven by a plan file written after stage 1 (declared in the pre-registration).
Action: S = beta_F sum (1 - ReTr U_p/3) + beta_A sum (1 - Tr_adj U_p/8),  Tr_adj = |Tr U|^2 - 1.
Run:    python3 b2_3_su3_fund_adj.py [gates|stage1|full]      exit 0 iff all declared internal gates pass; the physics RESULT is only reported.
MUTATE: python3 b2_3_su3_fund_adj.py MUTATE   update-side adjoint normalisation 1/9 instead of 1/8: gate G3 (reweighting consistency) must fail -> exit 1; exit 3 otherwise.
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
HITS = 4
FAILED = []
exe = B.build("su3z")   # Metropolis multi-hit + Z3 center-flip proposals (Amendment 5)


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def mean_se(x):
    t = B.tau_int(x)
    return float(np.mean(x)), float(np.std(x) / np.sqrt(len(x) / (2 * t)))


def run(bF, bA, sd, L, nsw, nth, hits=HITS, mut=MUT, cold=0):
    a = [L, f"{bF:.4f}", f"{bA:.4f}", nsw, nth, sd, cold, hits, int(mut)]
    return B.load(B.run_one(exe, a, "su3gate" + ("m" if mut else "")))


def gates():
    print("Declared validation gates (SU(3)):", flush=True)
    # G4 identities: Tr_adj = |Tr|^2 - 1 for random SU(3) elements (adjoint rep from Gell-Mann matrices) and unitarity of the generated group elements
    rng = np.random.default_rng(2)
    lam = np.zeros((8, 3, 3), complex)
    lam[0][0, 1] = lam[0][1, 0] = 1; lam[1][0, 1] = -1j; lam[1][1, 0] = 1j; lam[2][0, 0] = 1; lam[2][1, 1] = -1
    lam[3][0, 2] = lam[3][2, 0] = 1; lam[4][0, 2] = -1j; lam[4][2, 0] = 1j; lam[5][1, 2] = lam[5][2, 1] = 1; lam[6][1, 2] = -1j; lam[6][2, 1] = 1j
    lam[7] = np.diag([1, 1, -2]) / math.sqrt(3)
    worst = 0.0
    for _ in range(100):
        A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)); Q, R_ = np.linalg.qr(A); Q = Q / np.linalg.det(Q) ** (1 / 3)
        Rm = np.array([[0.5 * np.trace(lam[a] @ Q @ lam[b] @ Q.conj().T).real for b in range(8)] for a in range(8)])
        worst = max(worst, abs(np.trace(Rm) - (abs(np.trace(Q)) ** 2 - 1)))
    if not MUT:
        chk("G4 Tr_adj = |Tr U|^2 - 1 on 100 random SU(3) elements (adjoint built from Gell-Mann matrices)", worst < 1e-10, f"(worst {worst:.1e})")
    # G3 reweighting consistency in beta_A (L=4, beta_F = 0.8, from 4.0 to 4.4, two seeds pooled)
    b0, b1 = 4.0, 4.05
    d0 = np.vstack([run(0.8, b0, s, 4, 60000, 4000) for s in (11, 12)])
    d1 = np.vstack([run(0.8, b1, s, 4, 60000, 4000) for s in (13, 14)])
    Np = 6.0 * 4 ** 4
    x0 = d0[:, 1]
    w = np.exp((b1 - b0) * Np * (x0 - x0.max()))
    rw = np.sum(w * x0) / np.sum(w)
    neff = 1.0 / np.sum((w / w.sum()) ** 2)
    se_rw = np.std(x0) / np.sqrt(neff / (2 * B.tau_int(x0)))
    m1, s1 = mean_se(d1[:, 1])
    ok3 = (abs(rw - m1) < 4 * math.hypot(se_rw, s1)) and neff >= 1000   # a gate with too few effective samples has no power and FAILS
    chk("G3 reweighting: <X_A>(4.05) from the 4.0 runs equals the direct 4.05 runs within 4 sigma, with ESS >= 1000 (L=4, beta_F=0.8)", ok3, f"(rw {rw:.5f} +- {se_rw:.5f}; direct {m1:.5f} +- {s1:.5f}; ESS {neff:.0f}; naive shift {m1 - x0.mean():.5f})")
    if MUT:
        return ok3
    # G1 plaquette at beta_F = 6.0 (beta_A = 0), 8^4: 0.5937 (widely quoted; RECALLED, used as a coarse sanity gate only)
    p = run(6.0, 0.0, 21, 8, 1500, 500, cold=1)[:, 0]
    m, se = mean_se(p)
    chk("G1 SU(3) plaquette at beta = 6.0 (8^4) within 0.004 of the recalled 0.5937", abs(m - 0.5937) < 0.004, f"(measured {m:.5f} +- {se:.5f})")
    # G2 strong coupling <X_F> = beta_F/18 to 10% at beta_F = 0.5, beta_A = 0 (4^4)
    q = run(0.5, 0.0, 22, 4, 20000, 1000)[:, 0]
    m, se = mean_se(q)
    chk("G2 strong coupling <X_F> = beta_F/18 to 10% at beta_F = 0.5 (4^4)", abs(m - 0.5 / 18) < 0.1 * 0.5 / 18, f"(measured {m:.5f} +- {se:.5f}; leading order {0.5 / 18:.5f})")
    return ok3


G3ok = gates()
if MUT:
    print("\nMUTATE CONTROL: update-side adjoint normalisation 1/9 instead of 1/8 -> G3", "FAILS as required (exit 1, the control fires)" if not G3ok else "did NOT fail: CONTROL BROKEN (exit 3)")
    sys.exit(1 if not G3ok else 3)
if MODE == "gates":
    sys.exit(0 if not FAILED else 1)

BF1 = [0.0, 0.4, 0.8, 1.2, 1.6, 2.4]
BA1 = np.round(np.arange(3.5, 8.0001, 0.25), 4).tolist()
results = {"stage1": {}, "stage2": {}}
print("\nStage 1H hysteresis map, L=%s (Amendment 4): X_A from cold / hot starts; '*' = |diff| > 5 sigma and > 0.005 (first-order-like)" % os.environ.get("B2_HYST_L", "4"), flush=True)
HL = int(os.environ.get("B2_HYST_L", "4"))
hm = B.hyst_map("su3z", HL, BF1, BA1, 4000, 1000, HITS, nw=NW)
for bF in BF1:
    fl = [bA for bA in BA1 if hm[(bF, bA)][6]]
    print(f"  beta_F={bF:4.2f}: flagged beta_A = {fl if fl else 'none'}", flush=True)
    results["stage1"][str(bF)] = {str(bA): hm[(bF, bA)] for bA in BA1}
json.dump(results, open(os.path.join(HERE, "3_su3_stage1H.json" if False else ("b2_3_stage1H.json" if HL == 4 else f"b2_3_stage1H_L{HL}.json")), "w"), indent=1)
print("  full table (beta_A: X_A cold, X_A hot):", flush=True)
for bF in BF1:
    print(f"   beta_F={bF:4.2f}: " + " ".join(f"{bA:.2f}:{hm[(bF, bA)][0]:.3f}/{hm[(bF, bA)][2]:.3f}{'*' if hm[(bF, bA)][6] else ''}" for bA in BA1), flush=True)
if MODE == "stage1":
    sys.exit(0 if not FAILED else 1)

plan_path = os.path.join(HERE, "b2_3_stage2_plan.json")
if not os.path.exists(plan_path):
    print("\nno stage-2 plan file yet; stopping after stage 1", flush=True)
    sys.exit(0 if not FAILED else 1)
plan = json.load(open(plan_path))
print(f"\nStage 2 plan ({os.path.basename(plan_path)}): {plan.get('note', '')}", flush=True)
for item in plan["scans"]:
    r = B.scan_line("su3z", item["kind"], item["L"], item["fixed"], item["grid"], item["nsw"], item["nth"], item["seeds"], HITS, nw=NW, fine=item.get("fine", 0.01), tag_extra="s2")
    key = f"{item['kind']}_{item['L']}_{item['fixed']}" + item.get("suffix", "")
    results["stage2"][key] = {k: v for k, v in r.items() if k != "curve"}
    mstr = "; ".join(f"x={m['x']:.4f}+-{m['err']:.4f} chi={m['chi']:.2f}{' EDGE' if m['edge'] else ''}" for m in r["maxima"])
    print(f"  {item['kind']}-scan L={item['L']} fixed={item['fixed']}: {mstr}   [tau_int max {r['tau_max']:.0f}, infl {r['infl']:.2f}]", flush=True)
json.dump(results, open(os.path.join(HERE, "b2_3_results.json"), "w"), indent=1)
print("\nresults written to b2_3_results.json", flush=True)
sys.exit(0 if not FAILED else 1)
