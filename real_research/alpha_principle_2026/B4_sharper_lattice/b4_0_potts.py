#!/usr/bin/env python3
"""B4.0 -- gate G-P: the flat-histogram machinery (Wang-Landau table, refinement rounds, frozen-weight production, equal-weight criterion,
block jackknife, 1/V finite-size extrapolation) on the 2D q = 20 Potts model, whose first-order transition point is exactly known:
beta_c = ln(1 + sqrt(q)).  Gate: extrapolated beta_c within 3 sigma of the exact value, sigma < 0.005, >= 10 round trips at every L, double-peak (saddle) present.
Run:    python3 b4_0_potts.py            exit 0 iff the gate passes
MUTATE: python3 b4_0_potts.py MUTATE     the production acceptance drops the weight difference W(E')-W(E) (detailed balance violated): the gate must fail -> exit 1; exit 3 if it passes.
"""
import sys
sys.dont_write_bytecode = True
import math
import numpy as np
import b4_lib as B

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
Q = 20
BC = math.log(1 + math.sqrt(Q))
exe = B.build("potts", flags=())
Ls = (10, 12, 14, 16)
print(f"B4.0 Potts q={Q} gate (MUTATE={MUT}); exact beta_c = ln(1+sqrt(q)) = {BC:.6f}")
vals, errs, trips = [], [], []
for L in Ls:
    V = L * L
    m = B.Model(exe, f"potts{L}", dict(L=L, q=Q), "beta", BC, V, obounds=(None, 2.0 * V), nsig=2.5, quant=lambda lo, hi: (math.floor(lo) - 0.5, math.floor(lo) - 0.5 + min(int(hi) + 1 - math.floor(lo), 2 * V + 1 - math.floor(lo)), min(int(hi) + 1 - math.floor(lo), 2 * V + 1 - math.floor(lo))))
    r = B.run_point(m, delta=0.03, nb=300, nchain=4, nth=2000, nsw=100000, every=5, ref_nsw=60000, target_trav=40, max_batches=(2 if MUT else 30), mut=1 if MUT else 0, log=lambda s: None,
                    wl_flat_int=500)
    pool = r["pool"]
    e = B.jk_eq(pool, r["mid"], kind="weight")
    if e is None:
        print(f"  L={L}: equal-weight estimator failed"); vals.append(np.nan); errs.append(np.nan); trips.append(r["ntrav"]); continue
    print(f"  L={L:2d}: beta*(L) = {e['b']:.5f} +- {e['err']:.5f}   traversals {r['ntrav']}, flat {r['flat']:.2f}, saddle ln(P_peak/P_valley) {e['lnsaddle']:.2f}, blocks {e['nblk']} infl {e['infl']:.2f}")
    vals.append(e["b"]); errs.append(e["err"]); trips.append(r["ntrav"])
vals, errs = np.array(vals), np.array(errs)
FAILED = []
ok = np.all(np.isfinite(vals))
if ok:
    x = np.array([1.0 / (L * L) for L in Ls])
    w = 1 / np.maximum(errs, 1e-5) ** 2
    Amat = np.vstack([np.ones_like(x), x]).T
    cov = np.linalg.inv(Amat.T @ (Amat * w[:, None]))
    beta = cov @ (Amat.T @ (w * vals))
    chi2 = float(np.sum(w * (vals - Amat @ beta) ** 2))
    bc, sbc = beta[0], math.sqrt(cov[0, 0])
    print(f"  fit beta*(L) = beta_c + a/V:  beta_c = {bc:.5f} +- {sbc:.5f} (exact {BC:.5f}, deviation {(bc - BC) / sbc:+.2f} sigma), a = {beta[1]:.3f}, chi2 = {chi2:.2f} ({len(Ls) - 2} dof)")
    dev = abs(bc - BC)
    g1 = dev <= 3 * sbc and sbc < 0.005
else:
    g1 = False
    bc = sbc = float("nan")
if not g1:
    FAILED.append("G-P1")
g2 = all(t >= 20 for t in trips)  # >= 10 round trips = 20 traversals
print(f"  [{'PASS' if g1 else 'FAIL'}] G-P1 extrapolated beta_c within 3 sigma of the exact value, sigma < 0.005")
print(f"  [{'PASS' if g2 else 'FAIL'}] G-P2 >= 10 round trips (20 traversals) at every L: {trips}")
if not g2:
    FAILED.append("G-P2")
if MUT:
    fired = "G-P1" in FAILED
    print("\nMUTATE CONTROL: production acceptance without the weight difference ->", "gate FAILS as required (exit 1, the control fires)" if fired else "gate did NOT fail: CONTROL BROKEN (exit 3)")
    sys.exit(1 if fired else 3)
sys.exit(0 if not FAILED else 1)
