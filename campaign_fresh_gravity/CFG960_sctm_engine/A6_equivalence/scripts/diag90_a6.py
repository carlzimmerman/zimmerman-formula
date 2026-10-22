"""DIAGNOSTIC ONLY (no output enters any record): replay force call 90 of SC1x at 1024^3 from the step-89 checkpoint with the
frozen engine, particles memory-mapped copy-on-write (read-only on disk), kicks/drifts disabled, stop after step 90.
Records the tracemalloc peak (live anonymous allocations; the mmapped particles are not counted) per stage, and the body sizes.
usage: python3 diag90.py ENGINE CKPT_DIR OUT.json"""
import os, sys, json, time, threading, tracemalloc, importlib.util, ctypes, re, subprocess
eng, ckdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.environ["CFG960_SWITCH"] = "SCT"
tracemalloc.start(1)
spec = importlib.util.spec_from_file_location("cfg960eng", eng); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
E = M.E; import numpy as np
REC = {}; INFO = {"bodies": [], "t0": time.time()}
_LP = ctypes.CDLL("/usr/lib/libproc.dylib")
class _RU(ctypes.Structure):
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in ("ut", "st", "piw", "iw", "pageins", "wired", "resident", "footprint")] + [("pad", ctypes.c_uint64 * 40)]
def fp():
    ru = _RU(); _LP.proc_pid_rusage(os.getpid(), 2, ctypes.byref(ru)); return ru.footprint / 1e9
def swap():
    o = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True).stdout
    return float(re.search(r"used = ([\d.]+)M", o).group(1))
SW0 = swap(); FPMAX = float(os.environ.get("DIAG_FPMAX", "36"))
def dump(reason):
    json.dump(dict(reason=reason, peak_MB={k: round(v / 1e6) for k, v in REC.items()}, info={k: v for k, v in INFO.items() if not k.startswith('_')}, t=time.time() - INFO["t0"]), open(out, "w"), indent=0)
def loop():
    n = 0
    while True:
        cur, pk = tracemalloc.get_traced_memory(); tracemalloc.reset_peak()
        k = E.STAGE[0]; REC[k] = max(REC.get(k, 0), pk); REC["fp:" + k] = max(REC.get("fp:" + k, 0), fp() * 1e9)
        n += 1
        if n % 50 == 0:
            dump("running")
            if fp() > FPMAX or swap() - SW0 > 1500:
                dump(f"SELF-ABORT fp {fp():.1f} swapgrow {swap() - SW0:.0f} stage {k}"); os._exit(9)
        time.sleep(0.01)
threading.Thread(target=loop, daemon=True).start()
def unit_check(prof, Mc, X, law, edges, dx, M_, mut=1.0):
    E.stage("unitcheck")
    rng = np.random.default_rng(7); nb = len(Mc); tot = prof.sum(1)
    sub = np.unique(np.concatenate([np.argsort(Mc)[-3000:], rng.choice(nb, min(nb, 7000), replace=False)]))
    BB0, dg0, re0 = M.body_points(prof[sub], Mc[sub], X[sub], law, edges, dx, M_, mut)
    sb = M.SH_BLOCK; M.SH_BLOCK = 50000
    SH, dg1, re1 = M.body_shells(prof[sub], Mc[sub], X[sub], law, edges, dx, M_, mut)
    M.check_shells(BB0, SH); assert re0.tobytes() == re1.tobytes() and json.dumps(dg0, default=str) == json.dumps(dg1, default=str)
    M.SH_BLOCK = sb
    mesh = E.Mesh(M_); Mm = M_
    i0, i1, wc = mesh.cic_idx(BB0["pos"]); ncorner = 0
    for cx in (0, 1):
        for cy in (0, 1):
            for cz in (0, 1):
                ix = i1[:, 0] if cx else i0[:, 0]; wx = wc[:, 0] if cx else 1 - wc[:, 0]
                iy = i1[:, 1] if cy else i0[:, 1]; wy = wc[:, 1] if cy else 1 - wc[:, 1]
                iz = i1[:, 2] if cz else i0[:, 2]; wz = wc[:, 2] if cz else 1 - wc[:, 2]
                I0 = (ix * Mm + iy) * Mm + iz; W0 = (wx * wy * wz).astype(np.float64) * BB0["w"]
                II, WW = [], []
                for a, b in SH["blocks"]:
                    pos, w, _ = M.shell_points(SH, a, b); j0, j1, vc = mesh.cic_idx(pos)
                    jx = j1[:, 0] if cx else j0[:, 0]; vx = vc[:, 0] if cx else 1 - vc[:, 0]
                    jy = j1[:, 1] if cy else j0[:, 1]; vy = vc[:, 1] if cy else 1 - vc[:, 1]
                    jz = j1[:, 2] if cz else j0[:, 2]; vz = vc[:, 2] if cz else 1 - vc[:, 2]
                    II.append((jx * Mm + jy) * Mm + jz); WW.append((vx * vy * vz).astype(np.float64) * w)
                assert np.concatenate(II).tobytes() == I0.tobytes() and np.concatenate(WW).tobytes() == W0.tobytes(), "deposit stream differs"
                ncorner += 1
    del i0, i1, wc, I0, W0, II, WW
    INFO["unit_check"] = dict(n_sub=int(len(sub)), n_points=int(len(BB0["w"])), n_nodes=int(len(BB0["cw"])), n_blocks=len(SH["blocks"]),
                              dg={k: v for k, v in dg0.items() if k != "re_dx"}, points_equal=True)
    del BB0, SH
    E.stage("bodies")
def wrap(name, stage):
    f = getattr(M, name)
    def g(*a, **kw):
        E.stage(stage); r = f(*a, **kw)
        if name == "body_shells":
            INFO['_ucargs'] = a
            INFO["bodies"].append(dict(n_bodies=int(len(a[1])), n_points=int(r[0]["n_points"]), n_shells=int(len(r[0]["sq"])), n_blocks=len(r[0]["blocks"]), n_nodes=int(len(r[0]["cw"])), dg={k: v for k, v in r[1].items() if k != "re_dx"},
                                       re_dx_q=[float(x) for x in np.percentile(r[1]["re_dx"], [50, 90, 99, 100])] if len(r[1]["re_dx"]) else []))
        if name == "refresh": INFO["refresh"] = r[0]
        if name == "merges": INFO["merges"] = r[0]
        E.stage(stage + "_done"); return r
    setattr(M, name, g)
for nm, st in (("body_shells", "bodies"), ("deposit_shells", "dep_shells"), ("merges", "merge"), ("pass_profiles", "profile"), ("pass_conversions", "convert"), ("refresh", "refresh_all"),
               ("partition_labels", "partition"), ("deposit_points", "dep_points"), ("deposit_converted", "xdep")):
    wrap(nm, st)
ii = E.interp1
def ii2(*a, **kw):
    if E.STAGE[0] != "accel": E.stage("accel")
    return ii(*a, **kw)
E.interp1 = ii2
def ck_load_mm(tag, P, PL, dom):
    meta = json.load(open(os.path.join(ckdir, "meta.json"))); o = {}
    for k, (dt, n) in meta["arrays"].items(): o[k] = np.memmap(os.path.join(ckdir, k + ".bin"), dtype=dt, mode="c", shape=(n,))
    P.x = [o[f"x{c}"] for c in range(3)]; P.mom = [o[f"m{c}"] for c in range(3)]; P.fd = o["fd"]
    lab = np.memmap(os.path.join(ckdir, "lab.bin"), dtype=np.int32, mode="r")
    for i0, i1 in P.chunks: PL.write(i0, i1, np.asarray(lab[i0:i1]))
    del lab
    dom.load(dict(np.load(os.path.join(ckdir, "dom.npz"))))
    INFO["dom_n_loaded"] = int(dom.n)
    return meta
M.ck_load = ck_load_mm
E.Particles.kick = lambda self, c, i0, i1, cc, accp: None
E.Particles.drift = lambda self, d: None
os.environ["CFG596_MAXSTEPS"] = "90"; E.MAXSTEPS = 90
try:
    M.run_sct("canonical", 1024); dump("run done")
    a = INFO.pop("_ucargs"); unit_check(*a); dump("done")
except Exception as ex:
    dump("exception " + repr(ex)); raise
