#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG180 mock null worlds (frozen in CFG180_FROZEN_CRITERIA.md section 6-C).
  python3 CFG180_null_mocks.py <s>       s = 1.00 or 1.42; SEED env (default 180; re-run 181); N env (default 200 per family)
Per-mock streams come from SeedSequence(SEED).spawn, so the result does not depend on the worker schedule.
Shared (not independent): the CFG165 pipeline via CFG180_lib.M.  New: the mock generator (CFG180_lib.mock_sample) and this driver.
"""
import os
import sys
import json
import math
import time
from multiprocessing import Pool

import numpy as np

import CFG180_lib as L
M = L.M

S_ARG = float(sys.argv[1]) if len(sys.argv) > 1 else 1.42
SEED = int(os.environ.get("SEED", "180"))
N = int(os.environ.get("N", "200"))
MU_K = float(os.environ.get("MU_K", "0.7"))          # frozen 0.7; other values are POST-HOC labelled extras
FAMS = {"F1": (1.0, 0.0), "F2": (2.0, 0.0), "F3": (1.0, 0.15), "F4": (1.0, "draw")}
NGRID_MOCK = 200          # coarser bracketing grid for speed (brentq refines); declared

Su0 = L.get_kurvs("inc_star_deg")
Sk0 = L.get_kross()
AS = L.get_anchor()
sp = L.sp_scaled(S_ARG)
ANCH = M.anchor_pool(sp, 0.0, "canonical", AS)["flat"][0]
ro = L.robs(float(np.median(Su0.z)), float(np.median(Sk0.z)), float(np.median(Su0.logM)), float(np.median(Sk0.logM)))
IN_REAL = ro["inrep"](2.0)
REL_IN = (ro["inrep"](2.0)[0] / ro["Rin"], ro["inrep"](2.0)[1] / ro["Rin"])
REL_LIT = (0.8, 1.2)


def one(args):
    truth, fam, i, ss = args
    rng = np.random.default_rng(ss)
    Rtrue, D = FAMS[fam]
    Dv = float(rng.normal(0.0, 0.17)) if D == "draw" else D
    Sk, fk = L.mock_sample(Sk0, sp, truth, MU_K, 0.0, rng, ANCH, ret_floor=True)
    Su, fu = L.mock_sample(Su0, sp, truth, MU_K * Rtrue, Dv, rng, ANCH, ret_floor=True)
    r = L.solve_pair(Sk, Su, AS, S_ARG, spK=sp, spU=sp, ngrid=NGRID_MOCK)
    out = dict(floorK=fk, floorU=fu, D=Dv)
    for law in L.LAWS:
        rl = r[law]["R"]
        out[law] = None if rl is None else dict(R=rl["R"], lo=rl["lo"], hi=rl["hi"], qlo=rl["qlo"], qhi=rl["qhi"])
    return (truth, fam, out)


def labels(out, truth, Rtrue, rel):
    br = (rel[0] * Rtrue, rel[1] * Rtrue)
    dis = {}
    for law in L.LAWS:
        rl = out[law]
        dis[law] = False if rl is None else L.disfav_overlap(rl, br)
    tl = "flat" if truth == "flat" else "H"
    ol = "H" if truth == "flat" else "flat"
    if dis[ol] and not dis[tl]:
        return "CORRECT-ONLY"
    if dis[tl] and not dis[ol]:
        return "WRONG-ONLY"
    if dis[tl] and dis[ol]:
        return "BOTH"
    return "NEITHER"


def main():
    t0 = time.time()
    print("=" * 100)
    print(f"CFG180 mock nulls: s={S_ARG}  N={N} per family  seed={SEED}  repo=<repo>  (mu_true KROSS {MU_K}; anchor offset {ANCH:.4f})")
    print("=" * 100, flush=True)
    jobs = []
    ss = np.random.SeedSequence(SEED)
    keys = [(t, f) for t in ("flat", "H") for f in FAMS]
    kids = ss.spawn(len(keys))
    for (t, f), kid in zip(keys, kids):
        for i, c in enumerate(kid.spawn(N)):
            jobs.append((t, f, i, c))
    with Pool(12) as pool:
        res = pool.map(one, jobs, chunksize=8)
    summ = {}
    for (t, f) in keys:
        rows = [o for tt, ff, o in res if tt == t and ff == f]
        Rtrue = FAMS[f][0]
        rec = {}
        for law in L.LAWS:
            v = np.array([o[law]["R"] for o in rows if o[law] is not None])
            rec[law] = dict(n=int(len(v)), none=int(len(rows) - len(v)),
                            q=[float(x) for x in np.percentile(v, [16, 50, 84])] if len(v) > 4 else None)
        lab_in = [labels(o, t, Rtrue, REL_IN) for o in rows]
        lab_lit = [labels(o, t, Rtrue, REL_LIT) for o in rows]
        def frac(labs):
            return {k: labs.count(k) / len(labs) for k in ("CORRECT-ONLY", "WRONG-ONLY", "BOTH", "NEITHER")}
        pat = []
        for o in rows:
            ok = True
            for law in L.LAWS:
                rl = o[law]
                if rl is None or rl["R"] < 2.5 or not L.disfav_overlap(rl, IN_REAL):
                    ok = False
            pat.append(ok)
        rec.update(lab_in=frac(lab_in), lab_lit=frac(lab_lit), pattern=float(np.mean(pat)),
                   floorU=float(np.mean([o["floorU"] for o in rows])), floorK=float(np.mean([o["floorK"] for o in rows])))
        summ[f"{t}|{f}"] = rec
        def q(x):
            return "n/a" if x is None else f"{x[1]:.2f} [{x[0]:.2f}, {x[2]:.2f}]"
        print(f"truth {L.NAMES[t]:5s} {f} (R_true {Rtrue}, D {FAMS[f][1]}): R_flat {q(rec['flat']['q'])} (no-be {rec['flat']['none']}/{N}); R_rival {q(rec['H']['q'])} (no-be {rec['H']['none']}/{N})")
        print(f"      label (in-repo width): {{{', '.join(f'{k} {v:.2f}' for k, v in rec['lab_in'].items())}}}   (+-20% width): {{{', '.join(f'{k} {v:.2f}' for k, v in rec['lab_lit'].items())}}}   observed-pattern {rec['pattern']:.2f}   floored discs U/K {rec['floorU']:.2f}/{rec['floorK']:.1f}", flush=True)
    # meaning lines
    print("\n-- frozen meaning tests")
    for t in ("flat", "H"):
        r = summ[f"{t}|F1"]["lab_in"]
        print(f"  power at s={S_ARG} truth {L.NAMES[t]}: F1 P(CORRECT-ONLY)={r['CORRECT-ONLY']:.2f}, P(WRONG-ONLY)={r['WRONG-ONLY']:.2f}  -> {'HAS POWER' if r['CORRECT-ONLY'] >= 0.5 and r['WRONG-ONLY'] <= 0.05 else 'NO POWER'}")
    for t in ("flat", "H"):
        for f in ("F3", "F4"):
            p = summ[f"{t}|{f}"]["pattern"]
            print(f"  observed pattern reproducible by a null: truth {L.NAMES[t]} {f}: P(pattern)={p:.2f} {'(>= 0.2: reproducible)' if p >= 0.2 else ''}")
    fn = f"CFG180_null_mocks_s{S_ARG:.2f}_seed{SEED}" + ("" if MU_K == 0.7 else f"_muK{MU_K}") + "_results.json"
    with open(os.path.join(L.HERE, fn), "w") as f:
        json.dump(summ, f, indent=1)
    print(f"\nruntime {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
