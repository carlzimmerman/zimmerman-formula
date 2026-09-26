#!/usr/bin/env python3
"""QF3 -- Q-closure SE-shrink (Z3-wave conductor lane; owns QF3_*).
Door (register 2026-09-26 09:10 ops note): QF2 recast the Q-closure door as an
SE-shrink requirement -- shrink s_Q on the L02 E[Q](tau0,q) tables before any
family search can be banked. This lane measures the SE scaling directly and
re-runs the VERBATIM bank gate on the shrunk tables. NOT a new family search:
only QF1's families F8-F10 and QF2's B1/B2 (loaded code, never transcribed).

Pre-registered (Z3-WAVE_BRIEF.md, fixed before any number):
 R1 SE-scaling: median over matched cells of s_Q(4x)/s_Q(L02) in [0.40, 0.60]
    (RE-REGISTERED with reason, see R1_reregistration_note; the original band
    [0.20, 0.32] was an arithmetic blunder in the brief: SEM = sigma/sqrt(n), so
    4x n gives 1/sqrt(4) = 1/2, not 1/4. The first run measured 0.5001 and was
    recorded FAIL verbatim in the .out before this correction).
 R2 engine consistency (fresh independent seeds): per-cell z of
    (E_Q_new - E_Q_L02)/sqrt(s_Q_new^2 + s_Q_L02^2); >= 90% of cells |z| <= 3
    AND max |z| <= 5; else exit 1 (numbers disagree).
 R3 bookkeeping: max |Q - X| < 1e-9 on every run; else exit 1.
 R4 bank gate VERBATIM (L02/QF1/QF2): family in-fit max <= 3 SE AND LOO holdout
    max <= 5 SE, central AND volume -> CLOSURE-BANKED-AT-4x, exit 0.
    Else classify honestly:
      NOISE-BOUND: stage-1 residual shrank >= 1.6x vs QF1's 13.68 SE -> project
        n_bank = 6e5 * (best/3)^2; if n_bank <= 4.8e6 run STAGE 2 (binding-q rows,
        both src, n = min(ceil(n_bank), 4.8e6), Pool(2)) and re-evaluate all gates
        on the best mixed table; if still > 3 SE -> honest FAIL with the floor.
      BIAS-FLOOR: residual did NOT shrink >= 1.6x -> grid-bias dominated; the
        door recasts AGAIN as a finer-tau0 rerun, not n-scaling. Honest exit 1.
House rules 1-10 (LOOP_CONDUCTOR.md) binding; leaf lane does NOT commit.
"""
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

from L02_q_functional import measure
from J02_moment_hierarchy import se
from QF1_q_closure import evaluate as qf1_evaluate
from QF2_q_noise_floor import run_table as qf2_run_table

HERE = os.path.dirname(os.path.abspath(__file__))
N_S1 = 600000            # 4x L02's 150000
N_S2_CAP = 4800000
SEED0 = 20260930         # fresh seeds, independent of L02's stream
GATE_IN, GATE_HOLD = 3.0, 5.0
QF1_OLD_BEST = 13.68     # register 2026-09-26 04:36 ops note (QF1 row)

RES = {"title": "QF3 Q-closure SE-shrink (n-scaling pilot, Z3-wave)",
       "pre_registration": "Z3-WAVE_BRIEF.md QF3-R1..R4 (fixed before any number)",
       "gates": {"R1_scaling_band": [0.40, 0.60], "R1_scaling_band_original": [0.20, 0.32], "R2_zfrac": 0.90, "R2_zmax": 5.0,
                 "R3_bookkeeping": 1e-9, "R4_infit": GATE_IN, "R4_holdout": GATE_HOLD}}


def run_cell(c):
    tau0, q, src, n, seed = c
    r = measure(tau0, q, src, n, seed, with_segs=False)
    Q, X = r["Q"], r["X"]
    return dict(tau0=tau0, q=q, src=src, n=n, seed=seed,
                E_Q=float(np.mean(Q)), s_Q=float(se(Q)),
                book_err=float(np.max(np.abs(Q - X))))


def build_cells(tbl, src, n, seed0):
    cells, meta = [], []
    sid = seed0
    for r in tbl:
        cells.append((r["tau0"], r["q"], src, n, sid))
        meta.append((r["tau0"], r["q"], src))
        sid += 1
    return cells, meta, sid


def table_rows(rows, n):
    return [dict(tau0=r["tau0"], q=r["q"], E_Q=r["E_Q"], s_Q=r["s_Q"], n=n) for r in rows]


def eval_gates(tbl, tag, store):
    fam = qf1_evaluate(tbl)
    bas = qf2_run_table(tbl, tag)
    infits = [v["infit_max_SE"] for v in fam.values()]
    holds = [v["holdout_max_SE"] for v in fam.values() if v["holdout_max_SE"] is not None]
    floor_b = []
    for q, rec in bas.items():
        for tg in ("B1_local_quad", "B2_spline"):
            r = rec.get(tg)
            if r:
                floor_b.append(max(r["infit_max_SE"], r["holdout_max_SE"]))
    out = dict(qf1_families=fam, qf2_floor=bas,
               worst_infit_SE=max(infits), worst_holdout_SE=max(holds) if holds else None,
               B_floor_max_SE=max(floor_b) if floor_b else None)
    store[tag] = out
    return out


def main():
    t0 = time.time()
    l02 = json.load(open(os.path.join(HERE, "L02_results.json")))
    tbl0c, tbl0v = l02["table_central"], l02["table_volume"]
    # L02 rows carry no src field; annotate from the table they were loaded from
    for r in tbl0c:
        r["src"] = "central"
    for r in tbl0v:
        r["src"] = "volume"
    print(f"QF3 loaded L02 tables: central {len(tbl0c)} rows, volume {len(tbl0v)} rows; "
          f"stage-1 n = {N_S1} (4x L02 1.5e5), seeds fresh from {SEED0}", flush=True)

    # ---- stage 1 (checkpointed: QF3 died twice after a completed 25-min stage) ----
    cells, meta, sid = build_cells(tbl0c, "central", N_S1, SEED0)
    cells_v, meta_v, sid = build_cells(tbl0v, "volume", N_S1, sid)
    cells = cells + cells_v; meta = meta + meta_v
    ck_path = os.path.join(HERE, "QF3_stage1.json")
    res = None
    if os.path.exists(ck_path):
        try:
            ck = json.load(open(ck_path))
            if ck["n"] == N_S1 and ck["seed0"] == SEED0 and len(ck["res"]) == len(meta):
                res = ck["res"]
                print("stage-1 checkpoint loaded (%d cells, n=%d, seed0=%d)" % (len(res), N_S1, SEED0), flush=True)
        except Exception as e:
            print(f"checkpoint unreadable ({e}); re-running stage 1", flush=True)
    if res is None:
        with Pool(4) as ex:
            res = list(ex.map(run_cell, cells, chunksize=1))
        with open(ck_path, "w") as f:
            json.dump({"n": N_S1, "seed0": SEED0, "res": res}, f)
        print("stage-1 checkpoint written", flush=True)
    new = {(m[2], m[0], m[1]): r for m, r in zip(meta, res)}
    tbl1c = table_rows([new[("central", r["tau0"], r["q"])] for r in tbl0c], N_S1)
    tbl1v = table_rows([new[("volume", r["tau0"], r["q"])] for r in tbl0v], N_S1)

    # R3 bookkeeping
    bk = max(r["book_err"] for r in res)
    RES["R3_book_err_max"] = bk
    if bk >= RES["gates"]["R3_bookkeeping"]:
        RES["verdict"] = f"FAIL R3: bookkeeping |Q-X| = {bk:.2e} >= 1e-9"
        finish(1)

    # R1 scaling + R2 consistency
    ratios, zs = [], []
    for r0 in tbl0c + tbl0v:
        r1 = new[(r0["src"], r0["tau0"], r0["q"])]
        ratios.append(r1["s_Q"] / r0["s_Q"])
        zs.append((r1["E_Q"] - r0["E_Q"]) / math.sqrt(r1["s_Q"] ** 2 + r0["s_Q"] ** 2))
    med = float(np.median(ratios))
    zfrac = float(np.mean([abs(z) <= 3.0 for z in zs]))
    zmax = float(np.max(np.abs(zs)))
    RES.update(R1_median_ratio=med, R2_zfrac_le3=zfrac, R2_zmax=zmax)
    RES["R1_reregistration_note"] = (
        "Original band [0.20,0.32] (brief) expected s_Q ~ n^-1; WRONG: se() returns the "
        "standard error of the mean, sigma/sqrt(n), so 4x n -> ratio 1/2. First run "
        "measured 0.5001 and was recorded FAIL verbatim in QF3_q_se_shrink.out before "
        "this re-registration (W01 budget-change precedent: correction recorded with "
        "measured reason before gate-dependent verdicts). R2 (mean consistency, "
        "max|z|=1.95) was independent of the band and PASSED unchanged.")
    ok1 = 0.40 <= med <= 0.60
    ok2 = (zfrac >= 0.90) and (zmax <= RES["gates"]["R2_zmax"])
    RES["R1_pass"], RES["R2_pass"] = ok1, ok2
    print(f"R1 SE-scaling median ratio = {med:.4f} (band [0.20,0.32]) -> {'PASS' if ok1 else 'FAIL'}", flush=True)
    print(f"R2 consistency: frac|z|<=3 = {zfrac:.3f}, max|z| = {zmax:.2f} -> {'PASS' if ok2 else 'FAIL'}", flush=True)
    if not (ok1 and ok2):
        RES["verdict"] = "FAIL engine anomaly (R1/R2); no gate evaluation"
        finish(1)

    # R4 on stage-1 tables
    g1c = eval_gates(tbl1c, "central_4x", RES)
    g1v = eval_gates(tbl1v, "volume_4x", RES)
    best_in = min(g1c["worst_infit_SE"], g1v["worst_infit_SE"])
    best_ho = min(h for h in (g1c["worst_holdout_SE"], g1v["worst_holdout_SE"]) if h is not None)
    RES["stage1_best_infit_SE"] = best_in
    RES["stage1_best_holdout_SE"] = best_ho
    print(f"stage-1: best in-fit {best_in:.2f} SE, best holdout {best_ho:.2f} SE "
          f"(QF1 on L02 n0: 13.68 SE)", flush=True)

    banked = (max(g1c["worst_infit_SE"], g1v["worst_infit_SE"]) <= GATE_IN
              and max(h for h in (g1c["worst_holdout_SE"], g1v["worst_holdout_SE"]) if h is not None) <= GATE_HOLD)
    if banked:
        RES["verdict"] = "CLOSURE-BANKED-AT-4x: a loaded family meets the verbatim bank gate on the 4x tables"
        finish(0)

    # classify + conditional stage 2
    ratio_resid = best_in / QF1_OLD_BEST
    RES["residual_shrink_ratio"] = ratio_resid
    if ratio_resid > 0.625:
        RES["verdict"] = ("BIAS-FLOOR: stage-1 residual %.2f SE shrank only %.2fx (< 1.6x) -> "
                          "grid-bias dominated; n-scaling cannot bank the door; recast AGAIN as "
                          "a finer-tau0 rerun (NOT a family search)" % (best_in, 1.0 / ratio_resid))
        finish(1)
    n_bank = N_S1 * (best_in / GATE_IN) ** 2
    RES["n_bank_projected"] = n_bank
    if n_bank > N_S2_CAP:
        RES["verdict"] = ("NOISE-BOUND but out of stage-2 budget: projected n_bank = %.2e > cap %.2e; "
                          "floor after stage 1 = %.2f SE; honest FAIL" % (n_bank, N_S2_CAP, best_in))
        finish(1)
    n2 = int(min(n_bank * 1.2, N_S2_CAP))
    # binding q = argmax of infit over the two eval stores
    cands = [(v["qf1_families"][q]["infit_max_SE"], src, q)
             for src in ("central", "volume")
             for q, v in RES["central_4x" if src == "central" else "volume_4x"]["qf1_families"].items()]
    cands.sort(reverse=True)
    worst_in, worst_src, worst_q = cands[0]
    RES["stage2"] = {"trigger": f"binding q={worst_q} ({worst_src}) at {worst_in:.2f} SE",
                     "n_stage2": n2}
    print(f"stage 2: binding q={worst_q} ({worst_src}); rerun its tau0 rows at n = {n2}", flush=True)
    src_rows = tbl0c if worst_src == "central" else tbl0v
    qrows = [r for r in src_rows if r["q"] == worst_q]
    cells2, meta2, _ = build_cells(qrows, worst_src, n2, sid)
    with Pool(2) as ex:
        res2 = list(ex.map(run_cell, cells2, chunksize=1))
    RES["stage2"]["book_err_max"] = max(r["book_err"] for r in res2)
    new2 = {(m[0], m[1]): r for m, r in zip(meta2, res2)}
    base = tbl1c if worst_src == "central" else tbl1v
    mixed = [dict(tau0=new2[(r["tau0"], r["q"])]["tau0"], q=r["q"],
                  E_Q=new2[(r["tau0"], r["q"])]["E_Q"], s_Q=new2[(r["tau0"], r["q"])]["s_Q"],
                  n=n2) if r["q"] == worst_q else r for r in base]
    g2 = eval_gates(mixed, f"{worst_src}_stage2", RES)
    RES["stage2"]["worst_infit_SE"] = g2["worst_infit_SE"]
    RES["stage2"]["worst_holdout_SE"] = g2["worst_holdout_SE"]
    other = g1v if worst_src == "central" else g1c
    banked2 = (g2["worst_infit_SE"] <= GATE_IN
               and (g2["worst_holdout_SE"] is None or g2["worst_holdout_SE"] <= GATE_HOLD)
               and other["worst_infit_SE"] <= GATE_IN
               and (other["worst_holdout_SE"] is None or other["worst_holdout_SE"] <= GATE_HOLD))
    if banked2:
        RES["verdict"] = ("CLOSURE-BANKED (stage-2 mixed table): loaded family meets the verbatim "
                          "bank gate after the SE shrink")
        finish(0)
    RES["verdict"] = ("HONEST FAIL: bank gate still not met after stage 2 "
                      "(binding %.2f SE, other src %.2f SE); floor recorded, no re-tuning"
                      % (g2["worst_infit_SE"], other["worst_infit_SE"]))
    finish(1)


def finish(rc):
    RES["elapsed_s"] = round(time.time() - _T0, 1)
    RES["exit"] = rc
    with open(os.path.join(HERE, "QF3_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES[k] for k in ("verdict", "R1_median_ratio", "R2_zfrac_le3",
                                          "R2_zmax", "stage1_best_infit_SE",
                                          "stage1_best_holdout_SE") if k in RES}, indent=1))
    print(f"elapsed {RES['elapsed_s']}s; exit {rc}")
    sys.exit(rc)


_T0 = time.time()

if __name__ == "__main__":
    main()
