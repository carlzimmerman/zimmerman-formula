#!/usr/bin/env python3
"""FS1: shock-capturing label for AC14's open door (AC2q planar fold vs v3s). Criteria: CRITERIA.md (f716e2f98f).
Physics = AC10 (imported unchanged); scheme S (conservative Lagrangian pressure + limited shock viscosity + SSP-RK3)
in fs1_core.c, compiled here. Checkpointed per row and rung (rerun resumes; SIGTERM loses only the running rung).
Run from the repo root:
  nice -n 15 python3 closure_2026_11_06/FS1_fold_shock_capturing/fs1.py ladder [--workers 4]
  ... fs1.py extra | checks
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, hashlib, time, ctypes, subprocess, argparse
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "action_search_2026_11_05", "AC10_nonlinear_clock"))
import ac10  # noqa: E402  (physics, rows, constants: unchanged)

WB, X0, TMAX, JTHR, JREG, EDGE = ac10.WB, ac10.X0, ac10.TMAX, ac10.JTHR, ac10.JREG, ac10.EDGE
LADDER = (2000, 4000, 8000); EXTRA = 16000
TOL_T = 2.5e-3; TOL_J = 0.1; LINE = 1e-2
MAXSTEPS = 200_000_000; WALL = 4 * 3600.0
SRC = os.path.join(HERE, "fs1_core.c"); BUILD = os.path.join(HERE, "build")
DEFAULT = dict(cq=1.0, cl=0.5, cfl=0.4, fsheet=0.05, edge_b=0, sheet=1.0)


def _lib():
    os.makedirs(BUILD, exist_ok=True)
    h = hashlib.sha1(open(SRC, "rb").read()).hexdigest()[:12]
    so = os.path.join(BUILD, f"fs1_core_{h}.so")
    if not os.path.exists(so):
        tmp = so + f".{os.getpid()}.tmp"
        subprocess.check_call(["cc", "-O2", "-shared", "-fPIC", "-o", tmp, SRC, "-lm"]); os.replace(tmp, so)
    lib = ctypes.CDLL(so)
    D, I, L, P = ctypes.c_double, ctypes.c_int, ctypes.c_long, ctypes.POINTER(ctypes.c_double)
    lib.fs1_run.argtypes = [I, D, D, D, D, D, D, D, D, D, D, D, I, D, D, D, D, L, D, P, I, I, P]
    lib.fs1_run.restype = I
    return lib


_L = None


def run(N, M1, Pi0, s2, gam, sheet=1.0, cq=1.0, cl=0.5, cfl=0.4, fsheet=0.05, tmax=TMAX, edge_b=0,
        rec_node=None, rec_cap=400000):
    global _L
    if _L is None:
        _L = _lib()
    out = np.zeros(12)
    rc = -1 if rec_node is None else int(rec_node)
    cap = rec_cap if rec_node is not None else 0
    rec = np.zeros(max(cap, 1) * 5)
    t0 = time.time()
    _L.fs1_run(int(N), M1, Pi0, s2, gam, sheet, cq, cl, cfl, fsheet, tmax, JTHR, int(edge_b), WB, X0[0], X0[1], EDGE,
               MAXSTEPS, WALL, out.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), rc, cap,
               rec.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
    st = int(out[5])
    r = dict(N=int(N), t_fold=(float(out[0]) if out[0] >= 0 else None), t_fold_all=(float(out[1]) if out[1] >= 0 else None),
             J_min=float(out[2]), v_max=float(out[3]), nstep=int(out[4]), status=st,
             fold_cell=(int(out[6]) if out[6] >= 0 else None), shock_at_fold=bool(out[7]),
             all_cell=(int(out[8]) if out[8] >= 0 else None), t_end=float(out[9]), J_min_all=float(out[10]),
             i0=int(EDGE * N), i1=int((1 - EDGE) * N), seconds=time.time() - t0)
    r["edge_first"] = r["all_cell"] is not None and not (r["i0"] <= r["all_cell"] < r["i1"])
    if rec_node is not None:
        r["rec"] = rec[: 5 * int(out[11])].reshape(-1, 5)
    return r


def klass(r):
    if r["status"] == 1:
        return "FOLD"
    if r["status"] == 0:
        return "HELD"
    return "UNDECIDED"


def sub(r):
    k = klass(r)
    if k == "HELD":
        return "REGULAR" if r["J_min"] >= JREG else "SHOCK-HELD"
    return k


def change(a, b):
    """relative change from rung a to rung b, None if classes differ or undecided"""
    ka, kb = klass(a), klass(b)
    if ka != kb or ka == "UNDECIDED":
        return None
    if ka == "FOLD":
        return abs(b["t_fold"] / a["t_fold"] - 1)
    return abs(b["J_min"] / a["J_min"] - 1)


def judge(rungs):
    """CRITERIA ladder: classes equal on 2000/4000/8000 and last change within line; else 16000 vs 8000."""
    tol = lambda r: TOL_T if klass(r) == "FOLD" else TOL_J
    ks = [klass(r) for r in rungs[:3]]
    e = change(rungs[1], rungs[2])
    if len(set(ks)) == 1 and ks[0] != "UNDECIDED" and e is not None and e <= tol(rungs[2]):
        return dict(converged=True, need_extra=False, label=ks[0], e=e, deciding=rungs[2]["N"])
    if len(rungs) < 4:
        return dict(converged=False, need_extra=True, label="NOT CONVERGED", e=e, deciding=None)
    e = change(rungs[2], rungs[3])
    ok = e is not None and e <= tol(rungs[3]) and klass(rungs[3]) == klass(rungs[2])
    return dict(converged=ok, need_extra=False, label=klass(rungs[3]) if ok else "NOT CONVERGED", e=e, deciding=rungs[3]["N"])


def key(row):
    return hashlib.sha1(json.dumps({k: row[k] for k in sorted(row) if not k.startswith("_") and k != "tag"},
                                   sort_keys=True, default=float).encode()).hexdigest()[:16]


def rung_file(pdir, row, N):
    return os.path.join(HERE, pdir, f"{key(row)}_{N}.json")


def do_rung(job):
    row, N, pdir = job
    fn = rung_file(pdir, row, N)
    if os.path.exists(fn):
        return json.load(open(fn))
    kw = {k: row[k] for k in ("sheet", "cq", "cl", "cfl", "fsheet", "edge_b") if k in row}
    r = run(N, row["M1"], row["Pi0"], row["s2_use"], row["gam"], **kw)
    out = dict(row=row, **r)
    tmp = fn + f".{os.getpid()}.tmp"
    json.dump(out, open(tmp, "w"), default=float); os.replace(tmp, fn)
    return out


def load_rungs(pdir, row):
    rs = []
    for N in LADDER + (EXTRA,):
        fn = rung_file(pdir, row, N)
        if os.path.exists(fn):
            rs.append(json.load(open(fn)))
    return rs


def stress_rows():
    rows = []
    for v in (0.2, 1.0):
        rows.append(dict(kind="stress_A1", model="v3s", M1=1.0, Pi0=v, s2_use=0.0, gam=0.0, tag=f"A1_{v}"))
    for v in (0.4, 2.0):
        rows.append(dict(kind="stress_A2", model="AC2q", M1=1.0, Pi0=v, s2_use=v, gam=0.0, tag=f"A2_{v}"))
    return rows


def main_rows():
    rows = ac10.physical_rows()
    rows += [dict(kind="K1_zero_charge", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0),
             dict(kind="MUTATE_A_repulsive", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0, sheet=-1.0),
             dict(kind="MUTATE_B_mach0.3", model="AC2q", M1=1.0, Pi0=0.1, s2_use=0.1, gam=(1 / 0.3) ** 2 / 0.1),
             dict(kind="MUTATE_P1_zero_charge", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0, sheet=1.03)]
    clock1 = [r for r in ac10.physical_rows() if r["kind"] == "clock_only" and r["model"] == "AC2q"][0]
    rows.append(dict(clock1, kind="MUTATE_P3_clock", sheet=1.03, _src=key(clock1)))
    return rows


def stiff_ac2q():
    return [r for r in ac10.physical_rows() if r["model"] == "AC2q" and r["gam"] > 0 and r["Pi0"] > 0]


def twin(row):
    tk = lambda rw: (rw["foot"], rw["r_kpc"], rw["w_kms"], rw["M1"], rw["Lstar_pc"], rw["kind"])
    return [r for r in ac10.physical_rows() if r["model"] == "v3s" and tk(r) == tk(row)][0]


def pool_run(jobs, workers):
    from multiprocessing import Pool
    jobs = [j for j in jobs if not os.path.exists(rung_file(j[2], j[0], j[1]))]
    # cost order: stiff and fine first so the tail is short
    jobs.sort(key=lambda j: -(j[1] ** 2) * (1 + 1e4 * math.sqrt(max(j[0]["gam"] * j[0]["Pi0"], 0))))
    print(f"{len(jobs)} rung jobs to run", flush=True)
    if not jobs:
        return
    with Pool(workers, maxtasksperchild=20) as pool:
        for i, o in enumerate(pool.imap_unordered(do_rung, jobs)):
            print(f"{i + 1}/{len(jobs)} {o['row']['kind']} {o['row']['model']} N{o['N']} {klass(o)} "
                  f"t={o['t_fold']} Jmin={o['J_min']:.4g} {o['seconds']:.0f}s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["ladder", "extra", "checks"])
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    for d in ("parts", "parts_checks"):
        os.makedirs(os.path.join(HERE, d), exist_ok=True)
    if a.mode == "ladder":
        jobs = [(r, N, "parts") for r in main_rows() for N in LADDER]
        pool_run(jobs, a.workers)
    elif a.mode == "extra":
        jobs = []
        for r in main_rows():
            rs = load_rungs("parts", r)
            if len(rs) >= 3 and judge(rs)["need_extra"]:
                jobs.append((r, EXTRA, "parts"))
        pool_run(jobs, a.workers)
    else:  # checks: K-visc, K-dt on the sample at the deciding rung; K4 on DIFF pairs; MUTATE-P2
        import importlib.util                              # load THIS lane's grade.py by path (AC10's dir is on sys.path)
        spec = importlib.util.spec_from_file_location("fs1_grade", os.path.join(HERE, "grade.py"))
        grade = importlib.util.module_from_spec(spec); spec.loader.exec_module(grade)
        jobs = grade.check_jobs()
        pool_run(jobs, a.workers)


if __name__ == "__main__":
    main()
