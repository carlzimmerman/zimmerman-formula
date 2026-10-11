#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG468 zero-field runs -- the compute half of arm 2 (FROZEN_CRITERIA.md, b0d7274a0).  It only PRODUCES work arrays; the frozen
rule is applied by cfg468_kernel_family.py.  Everything is CFG325/CFG358's protocol with the kernel swapped:
  engine   cfg468_engine.py, byte-identical to cfg358_engine.py (= CFG321's engine; sha256 checked below), not edited
  kernels  cfg468_kernels.make_engine_kernel(name): one physical unit y*_ref for every kernel
  data     class D: seeds 321 / 322, rms yhat 1e-4, L = 16, T = 80; pairs delta = 0, 1e-3, 1e-5
  grids    NS = 127, 255, 511, 1023; eps = 1e-3, 1e-4
Work arrays: ../_external_data/cfg468_work/ (MUTATE kernel: cfg468_work_MUTATE/), relative to the repository root, outside git.
Finished arrays are never recomputed (resume).
Run from the repository root (the lane used: nice -n 15, 6 processes):
  CFG468_KERNELS=nu_simple,nu_standard,S1,S2,MUTATE_kink nice -n 15 python3 campaign_fresh_gravity/CFG468_kernel_family/cfg468_zero_field_runs.py
Options: CFG468_NS (comma list), CFG468_EPSS, CFG468_NPROC (<= 6), CFG468_SMOKE=1 (T = 4, separate _SMOKE directory).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, hashlib, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")
import numpy as np
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
ENGINE_SHA256 = "bde2fbb6abb12fad4e8392917b792374016fd8127da2a02dcaa8338ff8952174"
_h = hashlib.sha256(open(os.path.join(HERE, "cfg468_engine.py"), "rb").read()).hexdigest()
if _h != ENGINE_SHA256:
    sys.exit(f"ABORT: cfg468_engine.py sha256 {_h} != CFG321's engine {ENGINE_SHA256}")
sys.path.insert(0, HERE)
import cfg468_engine as EN
import cfg468_kernels as KN

j340 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json")))
if abs(float(j340["numbers"]["P1"]["alpha_c_max"]) - KN.ALPHA_C) > 0:
    sys.exit("ABORT: L340 alpha_c_max differs from the kernels' ALPHA_C")

SMOKE = os.environ.get("CFG468_SMOKE", "0") == "1"
KERNELS = [k for k in os.environ.get("CFG468_KERNELS", "nu_simple,nu_standard,S1,S2,MUTATE_kink").split(",") if k]
NS = tuple(int(x) for x in os.environ.get("CFG468_NS", "127,255,511,1023").split(","))
EPSS = tuple(float(x) for x in os.environ.get("CFG468_EPSS", "1e-3,1e-4").split(","))
DELTAS = (0.0, 1e-3, 1e-5)
NPROC = min(6, int(os.environ.get("CFG468_NPROC", "6")))
L1D, YRMS0, T1D = 16.0, 1e-4, (4.0 if SMOKE else 80.0)


def ext_dir(kern):
    d = "cfg468_work" + ("_MUTATE" if kern == "MUTATE_kink" else "") + ("_SMOKE" if SMOKE else "")
    return os.path.join(os.path.dirname(REPO), "_external_data", d)


def fname(s):
    return os.path.join(ext_dir(s["kern"]), f"cfg468_main_{s['kern']}_n{s['n']}_eps{s['eps']:.0e}_delta{s['delta']:.0e}.npz")


def task(spec):
    warnings.filterwarnings("ignore", message=".*encountered in matmul.*")
    t0 = time.time()
    fn = fname(spec)
    if os.path.exists(fn):
        return dict(spec=spec, skipped=True, wall=0.0, status="exists")
    n, eps, delta = spec["n"], spec["eps"], spec["delta"]
    gr = EN.Grid(1, n, L1D)
    K = KN.make_engine_kernel(spec["kern"])
    psi0, u0, G0, g0 = EN.initial_data(gr, K, eps, 321, YRMS0, delta=delta, seed2=322)
    o = EN.evolve(gr, K, eps, psi0, u0, G0, g0, T1D)
    meta = {"status": o["status"], "n_indef": int(o["n_indef"]), "n_refac": int(o["n_refac"]), "max_res": float(o["max_res"]),
            "dt": float(o["dt"]), "m": int(o["m"]), "wall": time.time() - t0, "kernel": spec["kern"], "engine_sha256": _h}
    os.makedirs(ext_dir(spec["kern"]), exist_ok=True)
    tmp = fn[:-4] + ".partial.npz"
    np.savez_compressed(tmp, snap_t=o["snaps_t"], snap_w=o["snaps_w"], meta=json.dumps(meta),
                        **{"rec_" + k_: np.array(v_) for k_, v_ in o["rec"].items()})
    os.replace(tmp, fn)
    return dict(spec=spec, skipped=False, **meta)


if __name__ == "__main__":
    specs = [{"kern": k, "n": n, "eps": e, "delta": d} for k in KERNELS for e in EPSS for n in NS for d in DELTAS]
    PRIO = {"S1": 0, "MUTATE_kink": 1, "nu_simple": 2, "nu_standard": 3, "S2": 4, "nu_mono_generic": 5}   # decisive kernels first
    specs.sort(key=lambda s: (PRIO.get(s["kern"], 9), -(s["n"] / math.sqrt(s["eps"]))))
    print(f"CFG468 zero-field runs: {len(specs)} specs; kernels {KERNELS}; N {NS}; eps {EPSS}; {NPROC} processes; "
          f"T = {T1D}{' (SMOKE)' if SMOKE else ''}; engine sha256 verified", flush=True)
    T0 = time.time()
    with get_context("fork").Pool(NPROC) as pool:
        for r in pool.imap_unordered(task, specs):
            s = r["spec"]
            if r["skipped"]:
                print(f"  exists: {s['kern']} n={s['n']} eps={s['eps']:.0e} delta={s['delta']:.0e}", flush=True)
            else:
                print(f"  done: {s['kern']:12s} n={s['n']:4d} eps={s['eps']:.0e} delta={s['delta']:.0e}  status={r['status']}  "
                      f"indef={r['n_indef']}  refac={r['n_refac']}  max_res={r['max_res']:.1e}  wall={r['wall']:.0f} s  "
                      f"(elapsed {time.time() - T0:.0f} s)", flush=True)
    print(f"all done; wall {time.time() - T0:.0f} s", flush=True)
