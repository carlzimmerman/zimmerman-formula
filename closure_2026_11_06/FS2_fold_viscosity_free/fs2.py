#!/usr/bin/env python3
"""FS2: viscosity-free fold reading for AC14's open door (AC2q planar fold vs v3s). Criteria: CRITERIA.md (1a686ed9a2).
Graded observable t_reg = first interior J <= J_reg (0.05). Physics = AC10 (unchanged); scheme S = FS1 (unchanged),
core fs2_core.c = FS1's core plus read-only level events. Rows, keys, ladder rungs and the stopping rule are FS1's.
Checkpointed per row and rung (rerun resumes; SIGTERM loses only the running rung). Run from the repo root:
  nice -n 15 python3 closure_2026_11_06/FS2_fold_viscosity_free/fs2.py ladder [--workers 4]
  ... fs2.py extra | checks
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, hashlib, time, ctypes, subprocess, argparse, importlib.util
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FS1D = os.path.join(os.path.dirname(HERE), "FS1_fold_shock_capturing")
_spec = importlib.util.spec_from_file_location("fs1", os.path.join(FS1D, "fs1.py"))   # FS1 driver by path (rows, keys)
fs1 = importlib.util.module_from_spec(_spec); sys.modules["fs1"] = fs1; _spec.loader.exec_module(fs1)
ac10 = fs1.ac10
WB, X0, TMAX, JTHR, JREG, EDGE = ac10.WB, ac10.X0, ac10.TMAX, ac10.JTHR, ac10.JREG, ac10.EDGE
LEVELS = (0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002)
IREG = LEVELS.index(JREG)
LADDER, EXTRA = fs1.LADDER, fs1.EXTRA
TOL_T, TOL_J, LINE = fs1.TOL_T, fs1.TOL_J, fs1.LINE
SRC = os.path.join(HERE, "fs2_core.c"); BUILD = os.path.join(HERE, "build")
key, main_rows, stress_rows, twin, stiff_ac2q = fs1.key, fs1.main_rows, fs1.stress_rows, fs1.twin, fs1.stiff_ac2q


def _lib():
    os.makedirs(BUILD, exist_ok=True)
    h = hashlib.sha1(open(SRC, "rb").read()).hexdigest()[:12]
    so = os.path.join(BUILD, f"fs2_core_{h}.so")
    if not os.path.exists(so):
        tmp = so + f".{os.getpid()}.tmp"
        subprocess.check_call(["cc", "-O2", "-shared", "-fPIC", "-o", tmp, SRC, "-lm"]); os.replace(tmp, so)
    lib = ctypes.CDLL(so)
    D, I, L, P = ctypes.c_double, ctypes.c_int, ctypes.c_long, ctypes.POINTER(ctypes.c_double)
    lib.fs2_run.argtypes = [I, D, D, D, D, D, D, D, D, D, D, D, I, D, D, D, D, L, D, P, I, I, P, I, P, P, P, P]
    lib.fs2_run.restype = I
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
    lev = np.array(LEVELS, dtype=float); tl = np.zeros(len(LEVELS)); cl_ = np.zeros(len(LEVELS)); sl = np.zeros(len(LEVELS))
    P = lambda a: a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    t0 = time.time()
    _L.fs2_run(int(N), M1, Pi0, s2, gam, sheet, cq, cl, cfl, fsheet, tmax, JTHR, int(edge_b), WB, X0[0], X0[1], EDGE,
               fs1.MAXSTEPS, fs1.WALL, P(out), rc, cap, P(rec), len(LEVELS), P(lev), P(tl), P(cl_), P(sl))
    st = int(out[5])
    r = dict(N=int(N), t_fold=(float(out[0]) if out[0] >= 0 else None), t_fold_all=(float(out[1]) if out[1] >= 0 else None),
             J_min=float(out[2]), v_max=float(out[3]), nstep=int(out[4]), status=st,
             fold_cell=(int(out[6]) if out[6] >= 0 else None), shock_at_fold=bool(out[7]),
             all_cell=(int(out[8]) if out[8] >= 0 else None), t_end=float(out[9]), J_min_all=float(out[10]),
             i0=int(EDGE * N), i1=int((1 - EDGE) * N), seconds=time.time() - t0,
             levels=list(LEVELS), t_lev=[float(x) if x >= 0 else None for x in tl],
             cell_lev=[int(x) if x >= 0 else None for x in cl_], shock_lev=[bool(x) for x in sl])
    r["edge_first"] = r["all_cell"] is not None and not (r["i0"] <= r["all_cell"] < r["i1"])
    if rec_node is not None:
        r["rec"] = rec[: 5 * int(out[11])].reshape(-1, 5)
    return r


def t_reg(r):
    return r["t_lev"][IREG]


def klass(r):
    """graded class at J_reg"""
    if r["status"] not in (0, 1):
        return "UNDECIDED"
    return "REACH" if t_reg(r) is not None else "REGULAR"


def change(a, b):
    ka, kb = klass(a), klass(b)
    if ka != kb or ka == "UNDECIDED":
        return None
    if ka == "REACH":
        return abs(t_reg(b) / t_reg(a) - 1)
    return abs(b["J_min"] / a["J_min"] - 1)


def judge(rungs):
    """CRITERIA ladder on t_reg: class equal on 2000/4000/8000 and last change within line; else 16000 vs 8000."""
    tol = lambda r: TOL_T if klass(r) == "REACH" else TOL_J
    ks = [klass(r) for r in rungs[:3]]
    e = change(rungs[1], rungs[2])
    if len(set(ks)) == 1 and ks[0] != "UNDECIDED" and e is not None and e <= tol(rungs[2]):
        return dict(converged=True, need_extra=False, label=ks[0], e=e, deciding=rungs[2]["N"])
    if len(rungs) < 4:
        return dict(converged=False, need_extra=True, label="NOT CONVERGED", e=e, deciding=None)
    e = change(rungs[2], rungs[3])
    ok = e is not None and e <= tol(rungs[3]) and klass(rungs[3]) == klass(rungs[2]) and all(k == ks[0] for k in ks)
    return dict(converged=ok, need_extra=False, label=klass(rungs[3]) if ok else "NOT CONVERGED", e=e, deciding=rungs[3]["N"])


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


def sample_ac2q():
    """K-visc / K-dt sample (CRITERIA): every 4th phantom AC2q, every 4th clock-only AC2q, every 8th soft AC2q."""
    rows = [r for r in ac10.physical_rows() if r["model"] == "AC2q"]
    ph = [r for r in rows if r["kind"] == "phantom"][::4]
    ck = [r for r in rows if r["kind"] == "clock_only"][::4]
    so = [r for r in rows if r["kind"] == "soft"][::8]
    return ph + ck + so


def sample_rows():
    s = sample_ac2q()
    return s + [twin(r) for r in s]


VARIANTS = (("visc2", dict(cq=2.0, cl=1.0)), ("visc05", dict(cq=0.5, cl=0.25)), ("dt", dict(cfl=0.2, fsheet=0.025)))


def pool_run(jobs, workers):
    from multiprocessing import Pool
    jobs = [j for j in jobs if not os.path.exists(rung_file(j[2], j[0], j[1]))]
    seen = set(); uj = []
    for j in jobs:
        f = rung_file(j[2], j[0], j[1])
        if f not in seen:
            seen.add(f); uj.append(j)
    jobs = uj
    jobs.sort(key=lambda j: -(j[1] ** 2) * (1 + 1e4 * math.sqrt(max(j[0]["gam"] * j[0]["Pi0"], 0))))
    print(f"{len(jobs)} rung jobs to run", flush=True)
    if not jobs:
        return
    with Pool(workers, maxtasksperchild=20) as pool:
        for i, o in enumerate(pool.imap_unordered(do_rung, jobs)):
            print(f"{i + 1}/{len(jobs)} {o['row']['kind']} {o['row']['model']} N{o['N']} {klass(o)} "
                  f"t_reg={t_reg(o)} t_fold={o['t_fold']} Jmin={o['J_min']:.4g} {o['seconds']:.0f}s", flush=True)


def grade_mod():
    spec = importlib.util.spec_from_file_location("fs2_grade", os.path.join(HERE, "grade.py"))
    g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["ladder", "extra", "checks"])
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    for d in ("parts", "parts_checks"):
        os.makedirs(os.path.join(HERE, d), exist_ok=True)
    if a.mode == "ladder":
        pool_run([(r, N, "parts") for r in main_rows() for N in LADDER], a.workers)
    elif a.mode == "extra":
        jobs = []
        for r in main_rows():
            rs = load_rungs("parts", r)
            if len(rs) >= 3 and judge(rs)["need_extra"]:
                jobs.append((r, EXTRA, "parts"))
        # FS1 rungs at 16000 (none in FS1; kept for KA completeness)
        pool_run(jobs, a.workers)
    else:
        pool_run(grade_mod().check_jobs(), a.workers)


if __name__ == "__main__":
    main()
