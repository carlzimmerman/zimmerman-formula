#!/usr/bin/env python3
"""CFG221 POST HOC (written after the frozen operating-characteristics tables were read; reported only): does the bootstrap size B = 500 of the frozen operating-characteristics runs
(B = 10,000 is used on real discs) change the picture?  The leave-one-out requirement re-draws the calibration and the resamples in every fit, so with margins of 0.02 to 0.07 dex the
Monte Carlo noise of the CI edges (about 0.01 dex at B = 500) can flip a cell.  Same rule, mocks (REAL, true offset 0), K = 100, seed 221, with B = 500 (the frozen value, repeated on a fresh
stream) and B = 2000, sigma scale 1 (frozen) and 0.5, N in {20, 36, 50}, both truths.
Run:  python3 campaign_fresh_gravity/CFG221_z35_decision_rule/cfg221_bootstrap_size.py        (a few minutes on 16 cores)
"""
import os, sys, json, time
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg221_decision_rule as M


def cell(task):
    s, truth, N, B, i = task
    M.SIGMA = np.array([0.30, 0.30, 0.40]) * s
    rng = np.random.default_rng(np.random.SeedSequence([221, 7000 + i]))
    cnt = {"LO": 0, "HI": 0, "NONE": 0}
    for _ in range(M.K_MOCK):
        v, _, _ = M.rule(M.gen_mock(M.BASE, N, truth, 0.0, M.SCEN["REAL"], rng), "FLAT", "H(z)", B, rng, sigma=M.SIGMA)
        cnt[v] += 1
    return task, cnt


if __name__ == "__main__":
    import multiprocessing as mp
    out = []

    def P(s=""):
        print(s, flush=True); out.append(s)

    P(__doc__.split("Run:")[0].strip())
    t0 = time.time()
    tasks, i = [], 0
    for s in (1.0, 0.5):
        for truth in ("FLAT", "H(z)"):
            for N in (20, 36, 50):
                for B in (500, 2000):
                    tasks.append((s, truth, N, B, i)); i += 1
    with mp.get_context("spawn").Pool(processes=min(15, mp.cpu_count())) as pool:
        res = pool.map(cell, tasks, chunksize=1)
    R = {(t[0], t[1], t[2], t[3]): c for t, c in res}
    P("\nP(correct separation), REAL, true offset c = 0, K = 100 mocks:")
    P(f"  {'sigma scale':11s} {'truth':6s} " + "  ".join(f"N = {N}: B=500  B=2000" for N in (20, 36, 50)))
    for s in (1.0, 0.5):
        for truth in ("FLAT", "H(z)"):
            good = "LO" if truth == "FLAT" else "HI"
            P(f"  {s:11.2f} {truth:6s} " + "   ".join(f"      {R[(s, truth, N, 500)][good] / M.K_MOCK:5.2f}   {R[(s, truth, N, 2000)][good] / M.K_MOCK:5.2f}" for N in (20, 36, 50)))
    P(f"\n{time.time() - t0:.0f} s")
    open(os.path.join(HERE, "cfg221_bootstrap_size.out"), "w").write("\n".join(out) + "\n")
    json.dump({"|".join(map(str, k)): v for k, v in R.items()}, open(os.path.join(HERE, "cfg221_bootstrap_size_results.json"), "w"), indent=1)
