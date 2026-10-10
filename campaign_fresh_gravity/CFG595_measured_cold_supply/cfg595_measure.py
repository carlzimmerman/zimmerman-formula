#!/usr/bin/env python3
"""CFG595 heavy stage (FROZEN_CRITERIA.md).  For a saved z = 0 state: deposit, call this lane's engine `forces` (diag = True) in the
state's own supply mode, capture the total potential (CFG526 / CFG555 method) and write a small cache (spectra, diagnostics) plus
the supply table.  For CFG530's saved ASSUMED states (and this lane's ASSUMED N256 states) it also writes the STATIC MEAS estimate:
forces in MEAS mode on the same frozen particle state (declared approximation, no re-evolution).
  nice -n 10 python3 cfg595_measure.py run JOB        (JOB = a folder of ../_external_data/cfg595_work/runs/)
  nice -n 10 python3 cfg595_measure.py saved530 JOB   (JOB = a folder of ../_external_data/cfg530_work/runs/, e.g. LRcan_L100_N512)
  nice -n 10 python3 cfg595_measure.py static JOB     (static MEAS on this lane's ASSUMED run JOB)
Caches: ../_external_data/cfg595_work/measure/.  Threads: CFG595_THREADS (default 8; 512^3 one at a time)."""
import os, sys, json, time, math, glob, importlib.util
NTH = int(os.environ.get("CFG595_THREADS", "8"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = str(NTH)
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W595 = os.path.join(EXT, "cfg595_work"); W530 = os.path.join(EXT, "cfg530_work")
OUT = os.path.join(W595, "measure"); os.makedirs(OUT, exist_ok=True)
ENGINE = os.path.join(HERE, "cfg595_pm.py")
RMIN_STUDY = {100.0: 2 * 100.0 / 256, 200.0: 1.56}

def load_engine(supply, foot, L, N, workdir):
    os.environ.update(CFG527_THREADS=str(NTH), CFG527_NSEED="512", CFG527_FRET_MODE="census", CFG527_NOCOMP="0", CFG527_DRAW="SHELL",
                      CFG527_L=f"{L:g}", CFG527_RMIN=repr(RMIN_STUDY[L]), CFG527_MUTATE="0", CFG595_SUPPLY=supply)
    sp = importlib.util.spec_from_file_location(f"cfg595_pm_{time.time_ns()}", ENGINE); mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    mod.WORK = workdir; mod.DTA_FILE = os.path.join(EXT, "cfg527_work", "cfg361_delta_ta_table.json")
    mod.RC = 0.0; mod.MIX = "NOFILT"; mod.FRETX = 1.0; mod.NTH = NTH
    return mod

def capture(mod, mesh, delta, foot, supply):
    """forces(diag) with the potential captured from the three acceleration transforms; returns (delta_grav, info, table)."""
    mod.SUPPLY = supply
    for k in ("mask", "catch", "fret"): mod._INC[k] = None
    mod._INC["calls"] = 0; mod._INC.pop("table", None); mod._INC.pop("meas_last", None)
    dta = mod.dta_table()
    rec = []; inv0 = mesh.inv
    def inv_rec(xk):
        rec.append(xk); del rec[:-3]
        return inv0(xk)
    mesh.inv = inv_rec
    _, info = mod.forces(mesh, delta, 1.0, "RES", "FLAT", foot, dta, diag=True)
    mesh.inv = inv0
    info.pop("_grids", None)
    num = sum(kv * x for kv, x in zip(mesh.kvec, rec)); del rec
    dgk = (-num / (1j * 1.5 * mod.Om)).astype(np.complex64); del num
    dgk[0, 0, 0] = 0
    dg = mesh.inv(dgk); del dgk
    tab = mod._INC.pop("table", None)
    if "meas_last" in mod._INC: info["meas_last"] = dict(mod._INC["meas_last"])
    return dg, info, tab

def scal(info):
    return {k: (float(v) if not isinstance(v, (bool, dict)) else v) for k, v in info.items() if isinstance(v, (int, float, bool, dict)) and k != "hosts"}

def process(name, pos_path, foot, L, N, modes, run_json=None):
    t0 = time.time()
    mod = load_engine(modes[0], foot, L, N, OUT)
    mesh = mod.Mesh(N)
    pos = np.load(pos_path)["pos"].astype(np.float64); delta = mesh.deposit(pos); del pos
    kb, pb, s8 = mod.measure_pk(mesh, delta, N ** 3)
    js = json.load(open(run_json))["snap"]["z0"] if run_json else None
    for sup in modes:
        out = os.path.join(OUT, f"cfg595_{name}_{sup}.json")
        dg, info, tab = capture(mod, mesh, delta, foot, sup)
        dsrc = (dg - delta).astype(np.float32)
        _, pg, s8g = mod.measure_pk(mesh, dg, N ** 3)
        if tab is not None:
            np.savez_compressed(os.path.join(OUT, f"cfg595_{name}_{sup}_z0_table.npz"), a=1.0, **tab)
        res = dict(name=name, supply=sup, foot=foot, L=L, N=N, state=os.path.relpath(pos_path, EXT), k=kb, P_part=pb, s8_part=s8,
                   P_grav=pg, s8_grav=s8g, src_absmax_rel=float(np.abs(dsrc).max() / (1.0 + float(delta.max()))),
                   mean_grav_minus_p=float(dsrc.astype(np.float64).mean()), info=scal(info),
                   json_z0=dict(P=js["P"], sigma8=js["sigma8"], e_sum=js.get("e_sum"), n_catch=js.get("n_catch"), q_max=js.get("q_max")) if js else None,
                   runtime_s=time.time() - t0)
        json.dump(res, open(out, "w"))
        print(f"done {name} {sup}: s8 part {s8:.5f} grav {s8g:.5f} t={time.time() - t0:.0f}s", flush=True)
        del dg, dsrc

if __name__ == "__main__":
    try: os.nice(10)
    except OSError: pass
    mode, job = sys.argv[1], sys.argv[2]
    if mode in ("run", "static"):
        d = os.path.join(W595, "runs", job); spec = json.load(open(os.path.join(d, "job.json")))["spec"]
        pz = glob.glob(os.path.join(d, "cfg595_*_z0.npz"))[0]; rj = pz.replace("_z0.npz", ".json")
        modes = [spec["supply"]] if mode == "run" else ["MEAS"]
        process(job if mode == "run" else job + "_static", pz, spec["foot"], spec["L"], spec["N"], modes, rj)
    elif mode == "saved530":
        d = os.path.join(W530, "runs", job); spec = json.load(open(os.path.join(d, "job.json")))["spec"]
        pz = glob.glob(os.path.join(d, "cfg527_*_z0.npz"))[0]; rj = pz.replace("_z0.npz", ".json")
        process("530_" + job, pz, spec["foot"], spec["L"], spec["N"], ["ASSUMED", "MEAS"], rj)
