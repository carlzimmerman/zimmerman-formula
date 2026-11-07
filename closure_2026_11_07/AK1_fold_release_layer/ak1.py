#!/usr/bin/env python3
"""AK1: does the certified planar fold machinery (FS2 scheme S) show the outside solver's critical layer and release
speed? Criteria: CRITERIA.md (8ed1798939, + addendum A1). Core ak1_core.c = FS2's core + nostop/snapshots (read-only).
Run from the repo root (checkpointed per row and rung; rerun resumes):
  nice -n 15 python3 closure_2026_11_07/AK1_fold_release_layer/ak1.py run [--workers 4]
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, hashlib, time, ctypes, subprocess, argparse, importlib.util
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FS2D = os.path.join(ROOT, "closure_2026_11_06", "FS2_fold_viscosity_free")
_s = importlib.util.spec_from_file_location("fs2", os.path.join(FS2D, "fs2.py"))
fs2 = importlib.util.module_from_spec(_s); sys.modules["fs2"] = fs2; _s.loader.exec_module(fs2)
fs1, ac10 = fs2.fs1, fs2.ac10
WB, X0, TMAX, JTHR, JREG, EDGE = ac10.WB, ac10.X0, ac10.TMAX, ac10.JTHR, ac10.JREG, ac10.EDGE
LEVELS, IREG = fs2.LEVELS, fs2.IREG
RUNGS = (4000, 8000)
DSNAP = (0.25, 0.5)
SRC = os.path.join(HERE, "ak1_core.c"); BUILD = os.path.join(HERE, "build")
key, twin = fs1.key, fs2.twin
SNAPF = ("t", "W", "WQ", "Vmax", "vpost", "vbulk", "emean", "fwhm", "peak", "ncoll", "xpeak")
CLAIM = {"canonical": dict(a0=1.2e-10, L=21.7), "alt": dict(a0=1.1e-10, L=22.9)}
CL = 2.99792458e8; PC = 3.0857e16; KPC = 3.0857e19


def lam_crit(foot, a0=None, L=None):
    a0 = a0 or CLAIM[foot]["a0"]; L = L or CLAIM[foot]["L"]
    return ((L * PC) ** 2 * CL ** 2 / a0) ** (1 / 3) / KPC


def v_claim(foot):
    c = CLAIM[foot]; return 2 * CL * (c["a0"] * c["L"] * PC / CL ** 2) ** (1 / 3) / 1e3


def _lib():
    os.makedirs(BUILD, exist_ok=True)
    h = hashlib.sha1(open(SRC, "rb").read()).hexdigest()[:12]
    so = os.path.join(BUILD, f"ak1_core_{h}.so")
    if not os.path.exists(so):
        tmp = so + f".{os.getpid()}.tmp"
        subprocess.check_call(["cc", "-O2", "-shared", "-fPIC", "-o", tmp, SRC, "-lm"]); os.replace(tmp, so)
    lib = ctypes.CDLL(so)
    D, I, L, P = ctypes.c_double, ctypes.c_int, ctypes.c_long, ctypes.POINTER(ctypes.c_double)
    lib.fs2_run.argtypes = ([I, D, D, D, D, D, D, D, D, D, D, D, I, D, D, D, D, L, D, P, I, I, P, I, P, P, P, P]
                            + [I, I, I, P, P, P, D, D, D, P])
    lib.fs2_run.restype = I
    return lib


_L = None


def run(N, M1, Pi0, s2, gam, sheet=1.0, cq=1.0, cl=0.5, cfl=0.4, fsheet=0.05, tmax=TMAX, edge_b=0, v0=1.0, A=0.0, kk=0.0):
    global _L
    if _L is None:
        _L = _lib()
    P = lambda a: a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    out = np.zeros(12); rec = np.zeros(1)
    lev = np.array(LEVELS, dtype=float); tl = np.zeros(len(LEVELS)); cl_ = np.zeros(len(LEVELS)); sl = np.zeros(len(LEVELS))
    ds = np.array(DSNAP); osn = np.zeros(11 * len(DSNAP)); oreg = np.zeros(11); ex = np.zeros(4)
    t0 = time.time()
    _L.fs2_run(int(N), M1, Pi0, s2, gam, sheet, cq, cl, cfl, fsheet, tmax, JTHR, int(edge_b), WB, X0[0], X0[1], EDGE,
               fs1.MAXSTEPS, fs1.WALL, P(out), -1, 0, P(rec), len(LEVELS), P(lev), P(tl), P(cl_), P(sl),
               1, IREG, len(DSNAP), P(ds), P(osn), P(oreg), float(v0), float(A), float(kk), P(ex))
    return dict(N=int(N), t_fold=(float(out[0]) if out[0] >= 0 else None), t_fold_all=(float(out[1]) if out[1] >= 0 else None),
                J_min=float(out[2]), status=int(out[5]), J_min_all=float(out[10]), nstep_end=int(out[4]),
                nstep_event=(int(ex[2]) if ex[2] >= 0 else None), t_lev=[float(x) if x >= 0 else None for x in tl],
                Pi_min=float(ex[0]) if ex[0] >= 0 else None, v_f=float(ex[1]), v_max_run=float(ex[3]),
                at_reg=dict(zip(SNAPF, map(float, oreg))),
                snaps=[dict(zip(SNAPF, map(float, osn[11 * k:11 * k + 11])), D=DSNAP[k]) for k in range(len(DSNAP))],
                seconds=time.time() - t0)


def lx2(r):
    return dict(r, gam=4 * r["gam"], Lstar_pc=2 * r["Lstar_pc"], _lx2=True, lx2=1)


def low_L(r):
    return r["Lstar_pc"] < 50


def main_rows():
    rows = ac10.physical_rows()
    return rows + [lx2(r) for r in rows if low_L(r)]


def clock1():
    return [r for r in ac10.physical_rows() if r["kind"] == "clock_only" and r["model"] == "AC2q"][0]


def mutate_rows():
    c = clock1(); vk = v_claim(c["foot"]) / c["w_kms"]
    rms = vk  # rms of A sin = A / sqrt 2
    return [dict(c, kind="MUTATE_V", v0=vk), dict(c, kind="MUTATE_V2", A=rms * math.sqrt(2), kk=20.0)]


def a2_rows():
    """Addendum A2 (post-result, disclosed): MUTATE-V's one row with t_max 60."""
    return [dict(mutate_rows()[0], kind="MUTATE_V_A2", tmax=60.0)]


def kvisc_rows():
    return [dict(r, cq=2.0, cl=1.0, _chk="visc2") for r in fs2.sample_ac2q() if r["kind"] in ("phantom", "clock_only") and low_L(r)]


def rung_file(row, N):
    return os.path.join(HERE, "parts", f"{key(row)}_{N}.json")


def do_rung(job):
    row, N = job
    fn = rung_file(row, N)
    if os.path.exists(fn):
        return json.load(open(fn))
    kw = {k: row[k] for k in ("sheet", "cq", "cl", "cfl", "fsheet", "edge_b", "v0", "A", "kk", "tmax") if k in row}
    r = run(N, row["M1"], row["Pi0"], row["s2_use"], row["gam"], **kw)
    out = dict(row=row, **r)
    tmp = fn + f".{os.getpid()}.tmp"
    json.dump(out, open(tmp, "w"), default=float); os.replace(tmp, fn)
    return out


def load(row, N):
    fn = rung_file(row, N)
    return json.load(open(fn)) if os.path.exists(fn) else None


def all_jobs():
    jobs = [(r, N) for r in main_rows() for N in RUNGS]
    jobs += [(r, N) for r in mutate_rows() for N in RUNGS]
    jobs += [(r, 8000) for r in kvisc_rows()]
    return jobs


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=["run", "a2"]); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
    from multiprocessing import Pool
    src = all_jobs() if a.mode == "run" else [(r, N) for r in a2_rows() for N in RUNGS]
    jobs = [j for j in src if not os.path.exists(rung_file(*j))]
    jobs.sort(key=lambda j: -(j[1] ** 2) * (1 + 1e4 * math.sqrt(max(j[0]["gam"] * j[0]["Pi0"], 0))))
    print(f"{len(jobs)} rung jobs", flush=True)
    with Pool(a.workers, maxtasksperchild=20) as pool:
        for i, o in enumerate(pool.imap_unordered(do_rung, jobs)):
            s = o["snaps"][-1]
            print(f"{i + 1}/{len(jobs)} {o['row']['kind']} {o['row']['model']} N{o['N']} t_reg={o['t_lev'][IREG]} "
                  f"W={s['W']:.4g} vpost={s['vpost']:.4g} Vmax={s['Vmax']:.4g} fwhm={s['fwhm']:.3g} {o['seconds']:.0f}s", flush=True)


if __name__ == "__main__":
    main()
