#!/usr/bin/env python3
"""QF4 -- Q-closure finer-tau0 rerun (Z4-wave; owns QF4_*).
QF3b verdict (on disk): BIAS-FLOOR CONFIRMED -- replicate stable (9.15 vs 8.84 SE,
dev 3.5%), pooled 12.64 = 8.84*sqrt(2) (fixed-deviation signature) -> the residual vs
the L02 grid is tau0-grid/structure bias, n-scaling CLOSED, "door recast to a finer-
tau0 rerun". This lane executes that recast: measure E[Q] on an INTERSTITIAL tau0
grid, pool with the QF3+QF3b tables into a denser tau0 sampling, and evaluate the QF1
families on the denser grid. Pre-registered gates in Z4-WAVE_BRIEF.md (P0, G1, G2, G3),
fixed BEFORE any number; house rules 1-10 binding; leaf lane does NOT commit.
"""
import json, math, os, sys, time
from multiprocessing import Pool
import numpy as np
from L02_q_functional import measure
from J02_moment_hierarchy import se
from QF1_q_closure import evaluate as qf1_evaluate
from QF2_q_noise_floor import run_table as qf2_run_table

HERE = os.path.dirname(os.path.abspath(__file__))
N = 600000
SEED0 = 20260930 + 90000
TAUS_I = (0.4, 0.7, 1.5, 2.5)          # interstitial to L02 TAUS {0.3,0.5,1,2,3}
QS = (0.0, 3.0, 10.0)
GATE_IN, GATE_HOLD, GATE_STRUCT = 3.0, 5.0, 6.5
RES = {"title": "QF4 finer-tau0 rerun (QF3b recast door)",
       "pre_registration": "Z4-WAVE_BRIEF.md QF4 gates (fixed before any number)",
       "gates": {"G1_bank_in_SE": GATE_IN, "G1_bank_hold_SE": GATE_HOLD,
                 "G2_structural_SE": GATE_STRUCT}}
_T0 = time.time()

def run_cell(c):
    tau0, q, src, n, seed = c
    r = measure(tau0, q, src, n, seed, with_segs=False)
    return dict(tau0=tau0, q=q, src=src, n=n, seed=seed,
                E_Q=float(np.mean(r["Q"])), s_Q=float(se(r["Q"])),
                book_err=float(np.max(np.abs(r["Q"] - r["X"]))))

def finish(rc):
    RES["elapsed_s"] = round(time.time() - _T0, 1)
    RES["exit"] = rc
    with open(os.path.join(HERE, "QF4_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES.get(k) for k in
                      ("verdict", "dense_best_infit_SE", "dense_best_holdout_SE",
                       "P0_parity")}, indent=1))
    print("elapsed %ss; exit %s" % (RES["elapsed_s"], rc))
    sys.exit(rc)

def main():
    l02 = json.load(open(os.path.join(HERE, "L02_results.json")))
    ck3 = json.load(open(os.path.join(HERE, "QF3_stage1.json")))["res"]
    ck3b = json.load(open(os.path.join(HERE, "QF3b_stage1.json")))["res"]
    old = {(r["src"], r["tau0"], r["q"]): r for r in ck3}
    rep = {(r["src"], r["tau0"], r["q"]): r for r in ck3b}

    # ---- P0 parity: 2 fresh original-grid cells vs QF3 stage-1
    par = [(0.5, 0.0, "central", N, SEED0),
           (2.0, 3.0, "volume", N, SEED0 + 1)]
    with Pool(2) as ex:
        prow = ex.map(run_cell, par)
    pmax = 0.0
    for r in prow:
        o = old[(r["src"], r["tau0"], r["q"])]
        z = abs(r["E_Q"] - o["E_Q"]) / math.sqrt(r["s_Q"] ** 2 + o["s_Q"] ** 2)
        pmax = max(pmax, z)
        print("P0 %s tau0=%s q=%s: %.6f vs %.6f  z=%.2f" %
              (r["src"], r["tau0"], r["q"], r["E_Q"], o["E_Q"], z), flush=True)
    RES["P0_parity"] = {"max_z": pmax, "pass": bool(pmax < 3.0)}
    if pmax >= 3.0:
        RES["verdict"] = "FAIL P0 machinery parity (z=%.2f >= 3)" % pmax
        finish(1)

    # ---- interstitial cells
    cells, sid = [], SEED0 + 100
    for t in TAUS_I:
        for q in QS:
            for s in ("central", "volume"):
                cells.append((t, q, s, N, sid)); sid += 1
    with Pool(6) as ex:
        res = ex.map(run_cell, cells, chunksize=1)
    RES["book_err_max"] = max(r["book_err"] for r in res)
    if RES["book_err_max"] >= 1e-9:
        RES["verdict"] = "FAIL bookkeeping"
        finish(1)
    with open(os.path.join(HERE, "QF4_stage1.json"), "w") as f:
        json.dump({"n": N, "seed0": SEED0 + 100, "res": res}, f)
    print("interstitial cells: %d measured, checkpoint written" % len(res), flush=True)

    # ---- denser table per src: pooled originals (n_eff 1.2e6) + fresh interstitial
    inter = {(r["src"], r["tau0"], r["q"]): r for r in res}
    best_in, best_ho = None, None
    for tag, tbl0 in (("central", l02["table_central"]), ("volume", l02["table_volume"])):
        denser = []
        for r in tbl0:
            a, b = old[(tag, r["tau0"], r["q"])], rep[(tag, r["tau0"], r["q"])]
            denser.append(dict(tau0=r["tau0"], q=r["q"],
                               E_Q=0.5 * (a["E_Q"] + b["E_Q"]),
                               s_Q=math.sqrt(a["s_Q"] ** 2 + b["s_Q"] ** 2) / 2.0,
                               n=2 * N))
        for t in TAUS_I:            # fix-forward: interstitial rows keyed by TAUS_I
            for q in QS:            # (run-1 KeyError crash preserved verbatim in .err)
                m = inter[(tag, t, q)]
                denser.append(dict(tau0=m["tau0"], q=m["q"], E_Q=m["E_Q"],
                                   s_Q=m["s_Q"], n=N))
        g = qf1_evaluate(denser)
        RES[tag + "_dense"] = {str(q): v for q, v in g.items()}
        gb = qf2_run_table(denser, tag + "_dense_floor")
        RES[tag + "_dense_floor"] = {q: v for q, v in gb.items()}
        ins = [v["infit_max_SE"] for v in g.values() if v["infit_max_SE"] is not None]
        hos = [v["holdout_max_SE"] for v in g.values() if v["holdout_max_SE"] is not None]
        bi = max(ins) if ins else float("inf")
        bh = max(hos) if hos else float("inf")
        RES[tag + "_best"] = {"infit_max_SE": bi, "holdout_max_SE": bh}
        best_in = bi if best_in is None else max(best_in, bi)
        best_ho = bh if best_ho is None else max(best_ho, bh)
        print("%s denser grid: best in-fit %.2f SE, holdout %.2f SE" % (tag, bi, bh),
              flush=True)
    RES["dense_best_infit_SE"], RES["dense_best_holdout_SE"] = best_in, best_ho
    if best_in <= GATE_IN and best_ho <= GATE_HOLD:
        RES["verdict"] = ("CLOSED FORM BANKED on the denser tau0 grid: best in-fit "
                          "%.2f <= %.1f SE and holdout %.2f <= %.1f SE (QF1 gate verbatim)"
                          % (best_in, GATE_IN, best_ho, GATE_HOLD))
        finish(0)
    if best_in > GATE_STRUCT:
        RES["verdict"] = ("STRUCTURAL: denser-tau0 best in-fit %.2f > %.1f SE -- tau0-grid "
                          "discretization is NOT the cause; Q-closure door CLOSED honest-FAIL "
                          "at the current engine" % (best_in, GATE_STRUCT))
        finish(1)
    RES["verdict"] = ("DISCRETIZATION-CONFIRMED (partial): denser-tau0 best in-fit %.2f SE "
                      "(QF3 8.84); not banked (%.2f > %.1f in / %.2f vs %.1f hold); door OPEN"
                      % (best_in, best_in, GATE_IN, best_ho, GATE_HOLD))
    finish(1)

if __name__ == "__main__":
    main()
