#!/usr/bin/env python3
"""B4.2 -- SU(3) fundamental-adjoint, flat-histogram (Wang-Landau table + refinement + frozen-weight production) line positions beta_A*(L, beta_F), equal-weight criterion.
Action S = beta_F sum (1 - Re Tr U/3) + beta_A sum (1 - Tr_adj/8), Tr_adj = |Tr U|^2 - 1 (the B2 / papers' normalisation).
Run:
  python3 b4_2_su3.py gates              gate G-C (flat-histogram code reweighted vs B2's independent canonical code, L=4, beta_F=0.4); exit 0 iff it passes
  python3 b4_2_su3.py point L bF         one line point: pilot -> Wang-Landau -> refinement -> production -> equal-weight/height beta_A* with jackknife; writes results/su3_L<L>_bF<bF>.json
  python3 b4_2_su3.py MUTATE             gate G-C with the production acceptance missing the weight difference: must fail -> exit 1; exit 3 otherwise
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import time
import numpy as np
import b4_lib as B

HERE = os.path.dirname(os.path.abspath(__file__))
B2SRC = os.path.join(HERE, "..", "B2_lattice_mpp", "src")
ARGS = [a for a in sys.argv[1:] if a != "MUTATE"]
MUT = "MUTATE" in sys.argv[1:]
MODE = "gates" if (MUT or not ARGS) else ARGS[0]
# first guess of the I-II / I-III line (B2's hysteresis midpoints, used only as the base point of the reweighting and the pilot; the answer does not depend on it)
GUESS = {0.0: 6.28, 0.4: 6.18, 0.6: 6.12, 0.8: 6.05, 1.0: 5.8, 1.2: 5.48, 1.6: 4.93, 2.0: 4.4, 2.4: 3.83}
PAR = {4: dict(nchain=4, nsw=40000, every=2, ref_nsw=15000, ref_rounds=12, nth=400, target=24, maxb=14),
       6: dict(nchain=4, nsw=40000, every=4, ref_nsw=20000, ref_rounds=12, nth=600, target=8, maxb=14)}
exe = B.build("su3m", flags=("-DZFLIP",))
FAILED = []


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def model_for(L, bF, bw=0.0, name=None):
    b0 = GUESS[round(bF, 4)] if round(bF, 4) in GUESS else float(np.interp(bF, sorted(GUESS), [GUESS[k] for k in sorted(GUESS)]))
    return B.Model(exe, name or f"su3L{L}f{bF:.3f}", dict(L=L, bF=f"{bF:.4f}"), "bA", b0, 6.0 * L ** 4, bw=bw, obounds=(None, 2.0 * 6.0 * L ** 4))


def reweighted_mean(pool, col, b, nblk=8):
    """<X>_b per plaquette from the pooled flat-histogram data, delete-one-block jackknife"""
    lw = pool.W + (b - pool.bA0) * pool.A
    x = (pool.A if col == 0 else pool.F) / pool.Np

    def est(m):
        w = np.exp(lw[m] - lw[m].max())
        return float(np.sum(w * x[m]) / np.sum(w))
    full = est(np.ones(len(x), bool))
    bid, nb = pool.blocks(nblk)
    jk = np.array([est(bid != j) for j in range(nb)])
    return full, float(np.sqrt((nb - 1) / nb * np.sum((jk - jk.mean()) ** 2)))


def gate_C(mut):
    print(f"Gate G-C (MUTATE={mut}): SU(3) L=4, beta_F=0.8, flat-histogram data reweighted vs B2's canonical Metropolis code", flush=True)
    exe_b2 = B.build("su3_b2z", srcname="su3", srcdir=B2SRC, flags=("-DZFLIP", "-I", B2SRC))
    L, bF = 4, 0.8
    m = model_for(L, bF, name="gateC")
    p = PAR[4]
    r = B.run_point(m, 0.25, nb="auto", nchain=p["nchain"], nth=p["nth"], nsw=p["nsw"], every=p["every"], ref_nsw=p["ref_nsw"], target_trav=20, max_batches=(2 if mut else p["maxb"]), mut=1 if mut else 0, log=lambda s: None, ref_rounds=p["ref_rounds"])
    pool = r["pool"]
    print(f"  flat-histogram production: {r['ntrav']} traversals, {len(pool.A)} samples, refinement rounds {r['refine_rounds']}, flat {r['flat']:.2f}", flush=True)
    allok = True
    for bA in (5.6, 6.5):
        for col, name in ((0, "X_A"), (1, "X_F")):
            mu, se = reweighted_mean(pool, col, bA)
            # canonical reference: B2's program (positional args: L bF bA nsw nth seed cold hits mode mut out every); its output columns are (X_F, X_A)
            ref = []
            for sd in (1, 2, 3):
                kv_out = os.path.join(B.CACHE, f"gateC_b2_{bA}_{sd}.bin")
                if not (os.path.exists(kv_out) and os.path.getsize(kv_out) > 0):
                    import subprocess
                    subprocess.run(["nice", "-n", "10", exe_b2, str(L), f"{bF:.4f}", f"{bA:.4f}", "40000", "3000", str(700 + sd), "1" if bA > 6.0 else "0", "4", "0", kv_out + ".tmp", "1"], check=True, capture_output=True)
                    os.replace(kv_out + ".tmp", kv_out)
                a = np.fromfile(kv_out, dtype=np.float64).reshape(-1, 2)
                ref.append(a[:, 1] if col == 0 else a[:, 0])
            ref = np.concatenate(ref)
            tau = B.tau_int(ref)
            mref, seref = float(ref.mean()), float(ref.std() / math.sqrt(len(ref) / (2 * tau)))
            ok = abs(mu - mref) < 4 * math.hypot(se, seref)
            allok &= ok
            print(f"    beta_A={bA}: <{name}> flat-histogram reweighted {mu:.5f} +- {se:.5f}; B2 canonical {mref:.5f} +- {seref:.5f}; diff {(mu - mref) / math.hypot(se, seref):+.1f} sigma", flush=True)
    return allok


if MODE == "gates":
    ok = gate_C(MUT)
    if MUT:
        print("\nMUTATE CONTROL: production acceptance without the weight difference -> G-C", "FAILS as required (exit 1, the control fires)" if not ok else "did NOT fail: CONTROL BROKEN (exit 3)")
        sys.exit(1 if not ok else 3)
    chk("G-C flat-histogram reweighted means equal the independent canonical code within 4 sigma (both observables, two beta_A)", ok)
    sys.exit(0 if not FAILED else 1)

if MODE == "wpoint":
    # windowed Wang-Landau estimator (Amendment 2): narrow overlapping windows, replicas from hot and cold starts, stitched ln g, equal-weight beta_A*
    L = int(ARGS[1]); bF = float(ARGS[2])
    m = model_for(L, bF)
    t0 = time.time()
    nrep = int(os.environ.get("B4_NREP", 6 if L <= 6 else 4))
    reps = tuple(((i % 2), 101 + 101 * i) for i in range(nrep))
    nw = int(os.environ.get("B4_WORKERS", "4"))
    r = B.window_point(m, 0.25, replicas=reps, nw=nw, wlmax=int(os.environ.get("B4_WLMAX", 400000)))
    out = dict(group="su3W", L=L, bF=bF, bA0=m.b0, seconds=time.time() - t0)
    if r is None:
        out["dropped"] = True; print("windowed estimator failed", flush=True)
    else:
        tfac = {6: 1.11, 4: 1.19, 2: 1.84, 3: 1.32}.get(nrep, 1.19)
        out.update(b=r["b"], err=tfac * r["spread"] / math.sqrt(nrep), spread=r["spread"], vals=r["vals"], lnsaddle=r["lnsaddle"], nbtot=r["nbtot"], nwin=r["nwin"], nrep=nrep, nsweeps=r["nsweeps"])
        print(f"su3W L={L} bF={bF}: beta_A*(windowed) = {out['b']:.5f} +- {out['err']:.5f} (replica spread {out['spread']:.5f}, n={nrep}); saddle {out['lnsaddle']:.1f}; {out['nwin']} windows of 16 bins; {out['seconds']:.0f} s", flush=True)
    json.dump(out, open(os.path.join(HERE, "results", f"su3W_L{L}_bF{bF:.4f}.json"), "w"), indent=1, default=float)

if MODE == "ppoint":
    # full-range flat-histogram PRODUCTION (the pre-registered primary estimator) started from the stitched windowed density of states (cached windowed runs) to skip the slow Wang-Landau stage
    L = int(ARGS[1]); bF = float(ARGS[2])
    p = PAR[L]
    m = model_for(L, bF)
    t0 = time.time()
    nrep = 6 if L <= 6 else 4
    reps = tuple(((i % 2), 101 + 101 * i) for i in range(nrep))
    NWK = int(os.environ.get("B4_WORKERS", "4"))
    wr = B.window_point(m, 0.25, replicas=reps, nw=NWK)
    init = dict(eps=0.21, lnG=wr["gmean"])
    r = B.run_point(m, 0.25, init=init, nb="auto", nchain=p["nchain"], nth=p["nth"], nsw=p["nsw"], every=p["every"], ref_nsw=p["ref_nsw"], target_trav=p["target"], max_batches=p["maxb"], log=lambda s: print(s, flush=True), ref_rounds=p["ref_rounds"], nw=NWK)
    pool = r["pool"]
    e = B.jk_eq(pool, r["mid"], kind="weight")
    h = B.jk_eq(pool, r["mid"], kind="height")
    out = dict(group="su3", L=L, bF=bF, bA0=m.b0, ntrav=r["ntrav"], nsamp=len(pool.A), refine_rounds=r["refine_rounds"], flat=r["flat"], seeded_from_windowed=True, seconds=time.time() - t0)
    flags = []
    if e is None:
        out["dropped"] = True; flags.append("estimator failed")
    else:
        nrt = r["ntrav"] / 2.0
        infl = 1.0
        if nrt < 2:
            out["dropped"] = True; flags.append("fewer than 2 round trips: dropped")
        elif nrt < 5:
            infl = math.sqrt(20.0 / nrt); flags.append(f"UNDERSAMPLED ({nrt:.1f} round trips): error inflated x{infl:.2f}")
        if r["flat"] < 0.2:
            flags.append(f"G-F: flatness {r['flat']:.2f} < 0.2")
        out.update(b=e["b"], err=e["err"] * infl, lnsaddle=e["lnsaddle"], XA_lo=e["XA_lo"] / pool.Np, XA_hi=e["XA_hi"] / pool.Np, cut=e["cut"], nblk=e["nblk"], infl_block=e["infl"], tau_indicator=B.phase_indicator_tau(pool, e["b"], e["cut"]))
        if h is not None:
            out.update(b_height=h["b"], err_height=h["err"] * infl)
    out["flags"] = flags
    json.dump(out, open(os.path.join(HERE, "results", f"su3_L{L}_bF{bF:.4f}.json"), "w"), indent=1, default=float)
    print(f"su3 L={L} bF={bF} PRODUCTION(seeded): beta_A*(weight) = " + (f"{out['b']:.5f} +- {out['err']:.5f}; traversals {r['ntrav']}; flat {r['flat']:.2f}; flags {flags}; {out['seconds']:.0f} s" if 'b' in out else f"FAILED {flags}"), flush=True)

if MODE == "point":
    L = int(ARGS[1]); bF = float(ARGS[2])
    p = PAR[L]
    m = model_for(L, bF)
    t0 = time.time()
    r = B.run_point(m, 0.25, nb="auto", nchain=p["nchain"], nth=p["nth"], nsw=p["nsw"], every=p["every"], ref_nsw=p["ref_nsw"], target_trav=p["target"], max_batches=p["maxb"], log=lambda s: print(s, flush=True), ref_rounds=p["ref_rounds"])
    pool = r["pool"]
    e = B.jk_eq(pool, r["mid"], kind="weight")
    h = B.jk_eq(pool, r["mid"], kind="height")
    out = dict(group="su3", L=L, bF=bF, bA0=m.b0, ntrav=r["ntrav"], nsamp=len(pool.A), refine_rounds=r["refine_rounds"], flat=r["flat"], wl=r["wl_log"], pilot={k: v for k, v in r["pilot"].items()}, seconds=time.time() - t0)
    flags = []
    if e is None:
        out["dropped"] = True; flags.append("estimator failed")
    else:
        nrt = r["ntrav"] / 2.0
        infl = 1.0
        if nrt < 2:
            out["dropped"] = True; flags.append("fewer than 2 round trips: dropped")
        elif nrt < 5:
            infl = math.sqrt(20.0 / nrt); flags.append(f"UNDERSAMPLED ({nrt:.1f} round trips): error inflated x{infl:.2f}")
        if r["flat"] < 0.2:
            flags.append(f"G-F: flatness {r['flat']:.2f} < 0.2")
        out.update(b=e["b"], err=e["err"] * infl, lnsaddle=e["lnsaddle"], XA_lo=e["XA_lo"] / pool.Np, XA_hi=e["XA_hi"] / pool.Np, F_lo=e.get("F_lo", float("nan")) / pool.Np, F_hi=e.get("F_hi", float("nan")) / pool.Np,
                   cut=e["cut"], nblk=e["nblk"], infl_block=e["infl"], tau_indicator=B.phase_indicator_tau(pool, e["b"], e["cut"]))
        if h is not None:
            out.update(b_height=h["b"], err_height=h["err"] * infl)
    out["flags"] = flags
    fn = os.path.join(HERE, "results", f"su3_L{L}_bF{bF:.4f}.json")
    json.dump(out, open(fn, "w"), indent=1, default=float)
    print(f"su3 L={L} bF={bF}: " + (f"beta_A*(weight) = {out['b']:.5f} +- {out['err']:.5f}; height {out.get('b_height', float('nan')):.5f} +- {out.get('err_height', float('nan')):.5f}; traversals {r['ntrav']}; flat {r['flat']:.2f}; saddle {out['lnsaddle']:.1f}; X_A phases {out['XA_lo']:.3f}/{out['XA_hi']:.3f}; X_F {out['F_lo']:.3f}/{out['F_hi']:.3f}; flags {flags}; {out['seconds']:.0f} s" if 'b' in out else f"FAILED {flags}"), flush=True)
