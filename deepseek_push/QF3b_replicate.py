#!/usr/bin/env python3
"""QF3b -- replicate diagnostic for QF3's borderline BIAS-FLOOR (Z3-wave; owns QF3b_*).
QF3 (this tick): stage-1 4x-n tables gave best in-fit 8.84 SE (QF1 families), shrink
1.55x vs QF1's 13.68 -- the pre-registered 1.6x threshold fired BIAS-FLOOR by a hair.
At 4x n the SEM halves, so a pure-bias residual must shrink exactly 2.0x; 1.55x is
consistent with the in-fit MAX-statistic (max over ~6 cells of bias + noise) being
noise-dominated. QF3b decides noise vs bias DIRECTLY with a pre-registered replicate.

Pre-registered here (fixed BEFORE any QF3b number; QF3's fired verdicts stand verbatim):
 - Replicate: full stage-1 rerun, same grid, n = 6e5, fresh seeds 20260930+50000+,
   Pool(4), checkpoint QF3b_stage1.json.
 - D1 (stability): |best_infit(QF3b) - 8.84|/8.84 <= 0.15 -> residual STABLE across
   replicates -> BIAS-FLOOR CONFIRMED (tau0-grid bias, not noise); door recast to a
   finer-tau0 rerun; exit 1.
 - D2 (pooled): regardless of D1, build the pooled table (E_Q = mean of the two
   independent replicates, s = sqrt(s1^2+s2^2)/2, effective n = 1.2e6) and evaluate
   the QF1 families: pooled best in-fit <= 6.5 SE (expected 8.84/sqrt(2) = 6.25 if
   noise-dominated) -> NOISE-BOUND restored with the pooled floor recorded and the
   exact n_bank projected for the pooled estimator; > 6.5 -> BIAS-FLOOR CONFIRMED.
 - Decision rule: BIAS-FLOOR confirmed iff D1 stable AND D2 > 6.5 (both point to a
   fixed bias); NOISE-BOUND iff D1 unstable OR D2 <= 6.5. Disagreement -> record both,
   verdict MIXED, exit 1 (no bank either way).
House rules 1-10 binding; leaf lane does NOT commit.
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
N_S1 = 600000
SEED0 = 20260930 + 50000
QF3_BEST = 8.84
QF3_THRESH = 0.15
POOLED_GATE = 6.5

RES = {"title": "QF3b replicate diagnostic (noise vs bias) for the Q-closure door",
       "pre_registration": "QF3b docstring (fixed before any number); QF3 verdicts stand verbatim",
       "gates": {"D1_stability_band": QF3_THRESH, "D1_reference": QF3_BEST,
                 "D2_pooled_gate": POOLED_GATE}}


def run_cell(c):
    tau0, q, src, n, seed = c
    r = measure(tau0, q, src, n, seed, with_segs=False)
    Q, X = r["Q"], r["X"]
    return dict(tau0=tau0, q=q, src=src, n=n, seed=seed,
                E_Q=float(np.mean(Q)), s_Q=float(se(Q)),
                book_err=float(np.max(np.abs(Q - X))))


def main():
    t0 = time.time()
    l02 = json.load(open(os.path.join(HERE, "L02_results.json")))
    tbl0c, tbl0v = l02["table_central"], l02["table_volume"]
    for r in tbl0c:
        r["src"] = "central"
    for r in tbl0v:
        r["src"] = "volume"
    ck_path = os.path.join(HERE, "QF3b_stage1.json")
    res = None
    if os.path.exists(ck_path):
        try:
            ck = json.load(open(ck_path))
            if ck["n"] == N_S1 and ck["seed0"] == SEED0 and len(ck["res"]) == 34:
                res = ck["res"]
                print("checkpoint loaded", flush=True)
        except Exception:
            pass
    if res is None:
        cells, sid = [], SEED0
        for r in tbl0c + tbl0v:
            cells.append((r["tau0"], r["q"], r["src"], N_S1, sid))
            sid += 1
        with Pool(4) as ex:
            res = list(ex.map(run_cell, cells, chunksize=1))
        with open(ck_path, "w") as f:
            json.dump({"n": N_S1, "seed0": SEED0, "res": res}, f)
        print("checkpoint written", flush=True)
    RES["book_err_max"] = max(r["book_err"] for r in res)
    if RES["book_err_max"] >= 1e-9:
        RES["verdict"] = "FAIL bookkeeping"
        finish(1)

    new = {(r["src"], r["tau0"], r["q"]): r for r in res}
    # replicate tables
    for tag, rows in (("central", tbl0c), ("volume", tbl0v)):
        tbl = [dict(tau0=new[("central" if tag == "central" else "volume", r["tau0"], r["q"])]["tau0"],
                    q=r["q"],
                    E_Q=new[(tag, r["tau0"], r["q"])]["E_Q"],
                    s_Q=new[(tag, r["tau0"], r["q"])]["s_Q"], n=N_S1) for r in rows]
        g = qf1_evaluate(tbl)
        RES[f"{tag}_replicate"] = {str(q): v for q, v in g.items()}
        # pooled table (QF3 checkpoint + this replicate)
        ck = json.load(open(os.path.join(HERE, "QF3_stage1.json")))["res"]
        old = {(r["src"], r["tau0"], r["q"]): r for r in ck}
        pooled = []
        for r in rows:
            a = old[(tag, r["tau0"], r["q"])]
            b = new[(tag, r["tau0"], r["q"])]
            pooled.append(dict(tau0=r["tau0"], q=r["q"],
                               E_Q=0.5 * (a["E_Q"] + b["E_Q"]),
                               s_Q=math.sqrt(a["s_Q"] ** 2 + b["s_Q"] ** 2) / 2.0,
                               n=2 * N_S1))
        gp = qf1_evaluate(pooled)
        gb = qf2_run_table(pooled, f"{tag}_pooled")
        RES[f"{tag}_pooled"] = {str(q): v for q, v in gp.items()}
        RES[f"{tag}_pooled_floor"] = {q: gb[q] for q in gb}

    def worst(d, key):
        vals = [v[key] for v in d.values() if v.get(key) is not None]
        return max(vals) if vals else None

    b_in = min(worst(RES["central_replicate"], "infit_max_SE"),
               worst(RES["volume_replicate"], "infit_max_SE"))
    p_in = min(worst(RES["central_pooled"], "infit_max_SE"),
               worst(RES["volume_pooled"], "infit_max_SE"))
    RES["replicate_best_infit_SE"] = b_in
    RES["pooled_best_infit_SE"] = p_in
    d1_dev = abs(b_in - QF3_BEST) / QF3_BEST
    d1 = d1_dev <= QF3_THRESH
    d2 = p_in <= POOLED_GATE
    RES.update(D1_stable=d1, D1_dev=d1_dev, D2_noise=d2)
    print(f"replicate best in-fit {b_in:.2f} SE (dev {d1_dev:.2f} from {QF3_BEST}); "
          f"pooled best in-fit {p_in:.2f} SE (gate {POOLED_GATE})", flush=True)
    if not d1 and d2:
        RES["verdict"] = ("NOISE-BOUND RESTORED: replicate in-fit moved %.0f%% (> %.0f%%) and the "
                          "pooled table (n_eff = 1.2e6) reads %.2f SE <= %.1f -- the QF3 1.55x "
                          "shrink was max-statistic noise, residuals scale ~ 1/sigma; project "
                          "n_bank for the pooled estimator and run stage 2 next tick"
                          % (100 * d1_dev, 100 * QF3_THRESH, p_in, POOLED_GATE))
        n_bank = 2 * N_S1 * (p_in / 3.0) ** 2
        RES["n_bank_pooled_projected"] = n_bank
        finish(0)
    if d1 and not d2:
        RES["verdict"] = ("BIAS-FLOOR CONFIRMED: replicate in-fit stable (dev %.0f%%) and pooled "
                          "%.2f SE > %.1f -- fixed tau0-grid bias; door recast to a finer-tau0 "
                          "rerun (n-scaling closed)" % (100 * d1_dev, p_in, POOLED_GATE))
        finish(1)
    if d1 and d2:
        RES["verdict"] = "MIXED: stable replicate but pooled <= gate; no bank either way; recorded"
        finish(1)
    RES["verdict"] = "MIXED: unstable replicate and pooled > gate; recorded"
    finish(1)


def finish(rc):
    RES["elapsed_s"] = round(time.time() - _T0, 1)
    RES["exit"] = rc
    with open(os.path.join(HERE, "QF3b_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES.get(k) for k in ("verdict", "replicate_best_infit_SE",
                                              "pooled_best_infit_SE", "D1_stable", "D2_noise")}, indent=1))
    print(f"elapsed {RES['elapsed_s']}s; exit {rc}")
    sys.exit(rc)


_T0 = time.time()

if __name__ == "__main__":
    main()
