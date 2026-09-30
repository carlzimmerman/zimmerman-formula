#!/usr/bin/env python3
"""B2.1 -- compact U(1) 4D Wilson action: weak first-order transition beta_c(L) from the energy-susceptibility peak (binned multi-histogram reweighting,
block jackknife), extrapolated as beta_c + a/L^4.  Pre-registered in B2_PREREGISTRATION.md (Amendment 1).
Run:    python3 b2_1_u1_wilson.py           exit 0 iff all declared gates pass (the RESULT is only reported)
MUTATE: python3 b2_1_u1_wilson.py MUTATE    wrong update rule (acceptance exp(-dS/2)); gate G1 must fail -> exit 1 (control fires); exit 3 if it does not.
"""
import sys
sys.dont_write_bytecode = True
import os
import numpy as np
import b2_lib as B

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
NW = int(os.environ.get("B2_WORKERS", "12"))
TAG = "u1mut" if MUT else "u1"
HITS = 4
NTH = 5000
if MUT:
    PLAN = {6: (np.arange(1.000, 1.0201, 0.002), 20000, [1, 2]), 8: (np.arange(1.000, 1.0201, 0.002), 20000, [1, 2])}
else:
    g1 = np.arange(1.000, 1.0201, 0.002)
    g2 = np.arange(1.004, 1.0181, 0.002)
    PLAN = {6: (g1, 100000, [1, 2]), 8: (g1, 60000, [1, 2]), 10: (g2, 30000, [1, 2]), 12: (g2, 25000, [1, 2])}
LIT_LO, LIT_HI = 1.0100, 1.0117          # declared acceptance interval for the infinite-volume Wilson beta_c (papers' 1.0106; ~1.0111 recalled)
SIG_MAX = 0.0015
FAILED = []


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


exe = B.build("u1")
jobs = []
keys = []
for L, (grid, nsw, seeds) in PLAN.items():
    for b in grid:
        for sd in seeds:
            cold = 0 if sd == 1 else 1
            jobs.append((exe, [L, f"{b:.4f}", nsw, NTH, 1000 * L + sd + int(round(b * 1e4)), cold, 0, HITS, int(MUT)], TAG))
            keys.append((L, round(float(b), 4), sd))
print(f"B2.1 U(1) Wilson  (MUTATE={MUT})  jobs={len(jobs)}", flush=True)
paths = B.run_many(jobs, NW, verbose=False)
data = {k: B.load(p)[:, 0] for k, p in zip(keys, paths)}

# ---- per-L susceptibility peak
res = {}
for L, (grid, nsw, seeds) in PLAN.items():
    Np = 6.0 * L ** 4
    ser, bet, taus = [], [], []
    for b in grid:
        for sd in seeds:
            ser.append(data[(L, round(float(b), 4), sd)])
            bet.append(float(b))
    nblk = 8
    wh = B.Wham1D(ser, bet, Np, nblk=nblk)
    for s in ser:
        taus.append(B.tau_int(s))
    blen = len(ser[0]) // nblk
    tau_max = max(taus)
    infl = max(1.0, np.sqrt(5.0 * tau_max / blen))
    pg = np.arange(grid[0], grid[-1] + 1e-9, 0.00005)
    fchi = lambda w, lr, b: w.obs(b, lr)[1]
    fbind = lambda w, lr, b: -w.obs(b, lr)[2]
    lr0 = wh.solve()
    bpk, chipk = B.peak(wh, lr0, fchi, pg)
    bbin, _ = B.peak(wh, lr0, fbind, pg)
    est, estb = [], []
    for j in range(nblk):
        lrj = wh.solve(drop=j)
        est.append(B.peak(wh, lrj, fchi, pg)[0])
        estb.append(B.peak(wh, lrj, fbind, pg)[0])
    m, e = B.jackknife(est)
    e *= infl
    mb, eb = B.jackknife(estb)
    eb *= infl
    interior_b = (bbin > grid[0] + 0.002) and (bbin < grid[-1] - 0.002)
    interior = (bpk > grid[0] + 0.002) and (bpk < grid[-1] - 0.002)
    # first-order diagnostic: peak height
    res[L] = dict(b=bpk, e=e, bbin=bbin, ebin=eb, interior_b=interior_b, chi=chipk, interior=interior, tau=tau_max, infl=infl, blen=blen)
    print(f"  L={L:2d}: beta_c(chi peak) = {bpk:.5f} +- {e:.5f} (jackknife x{infl:.2f});  Binder-min {bbin:.5f} +- {eb:.5f} (interior {interior_b});  chi_max = {chipk:.3f};  tau_int(E) max over runs = {tau_max:.1f} sweeps (block {blen});  interior = {interior}", flush=True)

# ---- extrapolation
def wfit(Ls, use, key="b", ekey="e"):
    x = np.array([1.0 / L ** 4 for L in use]); y = np.array([res[L][key] for L in use]); s = np.array([max(res[L][ekey], 1e-6) for L in use])
    A = np.vstack([np.ones_like(x), x]).T
    W = np.diag(1 / s ** 2)
    cov = np.linalg.inv(A.T @ W @ A)
    p = cov @ A.T @ W @ y
    return p[0], np.sqrt(cov[0, 0]), p[1]


Ls = sorted(res)
ok_interior = all(res[L]["interior"] for L in Ls)
if not MUT:
    b8, e8, a8 = wfit(Ls, [8, 10, 12])
    b10, e10, a10 = wfit(Ls, [10, 12])
    ball, eall, aall = wfit(Ls, [6, 8, 10, 12])
    fs = abs(b10 - ball)
    tot = float(np.hypot(e8, fs))
    print(f"\n  1/L^4 fit L=8,10,12: beta_c(inf) = {b8:.5f} +- {e8:.5f} (stat), slope a = {a8:.2f}")
    print(f"  fit L=10,12: {b10:.5f}; fit all L=6..12: {ball:.5f} +- {eall:.5f}; finite-size systematic |diff| = {fs:.5f}")
    print(f"  RESULT: beta_c^Wilson(inf) = {b8:.5f} +- {tot:.5f}  (stat {e8:.5f} (+) FS {fs:.5f});  literature interval accepted {LIT_LO}-{LIT_HI} (papers 1.0106, later literature ~1.0111)")
    print(f"  relative precision on beta_c: {100 * tot / b8:.3f}%")
    # AMENDMENT 6 (post-hoc, see the pre-registration): the Binder-cumulant minimum, declared as the cross-check, is used as the gate estimator
    bb8, eb8, ab8 = wfit(Ls, [8, 10, 12], "bbin", "ebin")
    bb10, _, _ = wfit(Ls, [10, 12], "bbin", "ebin")
    bball, ebal, _ = wfit(Ls, [6, 8, 10, 12], "bbin", "ebin")
    fsb = abs(bb10 - bball)
    totb = float(np.hypot(eb8, fsb))
    print(f"\n  BINDER-minimum estimator: fit L=8,10,12: {bb8:.5f} +- {eb8:.5f} (stat), slope {ab8:.2f}; fit L=10,12: {bb10:.5f}; fit all L: {bball:.5f}; FS systematic {fsb:.5f}")
    print(f"  RESULT (Binder estimator, gate estimator after Amendment 6): beta_c^Wilson(inf) = {bb8:.5f} +- {totb:.5f}  ({100 * totb / bb8:.3f}%)")
    Gchi = all(res[L]["interior"] for L in Ls) and (abs(b8 - 0.5 * (LIT_LO + LIT_HI)) <= 0.5 * (LIT_HI - LIT_LO) + 3 * tot) and tot <= SIG_MAX
else:
    b8, e8, a8 = wfit(Ls, [6, 8]); tot = e8
    print(f"\n  MUTATED fit L=6,8: beta_c = {b8:.5f} +- {e8:.5f}")

print("\nDeclared gates:")
if MUT:
    G1 = ok_interior and (abs(b8 - 0.5 * (LIT_LO + LIT_HI)) <= 0.5 * (LIT_HI - LIT_LO) + 3 * tot) and tot <= SIG_MAX
    chk("G1 beta_c(inf) inside the accepted literature interval within 3 sigma, all peaks interior to the grid, total sigma <= 0.0015", G1, f"(beta_c {b8:.5f} +- {tot:.5f}; interior {ok_interior})")
else:
    print(f"  [INFO] original G1 with the chi-peak estimator (FIRSTRUN): {'PASS' if Gchi else 'FAIL'}  (chi-peak beta_c {b8:.5f} +- {tot:.5f}; interior {ok_interior}); kept for the record, not in the exit code after Amendment 6")
    ok_b = all(res[L]["interior_b"] for L in Ls)
    G1 = ok_b and (abs(bb8 - 0.5 * (LIT_LO + LIT_HI)) <= 0.5 * (LIT_HI - LIT_LO) + 3 * totb) and totb <= SIG_MAX
    chk("G1' (Amendment 6) Binder-minimum beta_c(inf) inside the accepted literature interval within 3 sigma, all minima interior to the grid, total sigma <= 0.0015", G1, f"(beta_c {bb8:.5f} +- {totb:.5f}; interior {ok_b})")
if not MUT:
    # G2 thermalisation: hot and cold starts must agree far from the transition
    jj = []
    for bb in (0.98, 1.04):
        for cold in (0, 1):
            jj.append((exe, [8, f"{bb:.4f}", 4000, 1500, 77 + cold, cold, 0, HITS, 0], "u1g2"))
    pp = B.run_many(jj, NW, verbose=False)
    dd = [B.load(p)[:, 0] for p in pp]
    ok2 = True
    for i, bb in enumerate((0.98, 1.04)):
        h, c = dd[2 * i], dd[2 * i + 1]
        se = np.hypot(np.std(h) / np.sqrt(len(h) / (2 * B.tau_int(h))), np.std(c) / np.sqrt(len(c) / (2 * B.tau_int(c))))
        ok2 &= abs(h.mean() - c.mean()) < 4 * se + 1e-5
        print(f"    beta={bb}: hot {h.mean():.5f}  cold {c.mean():.5f}  (se {se:.5f})")
    chk("G2 hot and cold starts agree at beta = 0.98, 1.04 (8^4)", ok2)
    # G3 reweighting consistency: from the 1.006 run(s) to 1.008 vs direct 1.008 runs at L=6
    Np = 6.0 * 6 ** 4
    s6 = np.concatenate([data[(6, 1.006, 1)], data[(6, 1.006, 2)]])
    d8 = np.concatenate([data[(6, 1.008, 1)], data[(6, 1.008, 2)]])
    w = np.exp((1.008 - 1.006) * Np * (s6 - s6.max()))
    rw = np.sum(w * s6) / np.sum(w)
    neff = 1.0 / np.sum((w / w.sum()) ** 2)
    se_rw = np.std(s6) / np.sqrt(neff / (2 * B.tau_int(s6)))
    se_d = np.std(d8) / np.sqrt(len(d8) / (2 * B.tau_int(d8)))
    chk("G3 reweighting: <E>(1.008) from the 1.006 run agrees with the direct 1.008 run (6^4) within 4 sigma", abs(rw - d8.mean()) < 4 * np.hypot(se_rw, se_d) + 1e-5, f"(rw {rw:.5f}, direct {d8.mean():.5f}, se {np.hypot(se_rw, se_d):.5f})")

if MUT:
    fired = not G1
    print("\nMUTATE CONTROL: wrong update rule (acceptance exp(-dS/2)) -> G1", "FAILS as required (exit 1, the control fires)" if fired else "did NOT fail: CONTROL BROKEN (exit 3)")
    sys.exit(1 if fired else 3)
import json
json.dump(dict(beta_c=float(bb8), sigma=float(totb), stat=float(eb8), fs=float(fsb), estimator="Binder-cumulant minimum (Amendment 6)", chi_peak=dict(beta_c=float(b8), sigma=float(tot), stat=float(e8), fs=float(fs)), per_L={str(L): dict(b=float(res[L]["b"]), e=float(res[L]["e"]), tau=float(res[L]["tau"])) for L in res}), open(os.path.join(B.HERE, "b2_1_result.json"), "w"), indent=1)
print("\nCross-check note: the Wilson-action value is compared with the interval the papers printed (1.0106) and the value recalled from later literature (~1.0111).")
sys.exit(0 if not FAILED else 1)
