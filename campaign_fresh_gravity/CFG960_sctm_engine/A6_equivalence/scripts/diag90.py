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
    json.dump(dict(reason=reason, peak_MB={k: round(v / 1e6) for k, v in REC.items()}, info=INFO, t=time.time() - INFO["t0"]), open(out, "w"), indent=0)
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
def wrap(name, stage):
    f = getattr(M, name)
    def g(*a, **kw):
        E.stage(stage); r = f(*a, **kw)
        if name == "body_points":
            INFO["bodies"].append(dict(n_bodies=int(len(a[1])), n_points=int(len(r[0]["w"])), n_nodes=int(len(r[0]["cw"])), dg={k: v for k, v in r[1].items() if k != "re_dx"},
                                       re_dx_q=[float(x) for x in np.percentile(r[1]["re_dx"], [50, 90, 99, 100])] if len(r[1]["re_dx"]) else []))
        if name == "refresh": INFO["refresh"] = r[0]
        if name == "merges": INFO["merges"] = r[0]
        E.stage(stage + "_done"); return r
    setattr(M, name, g)
for nm, st in (("body_points", "bodies"), ("merges", "merge"), ("pass_profiles", "profile"), ("pass_conversions", "convert"), ("refresh", "refresh_all"),
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
    M.run_sct("canonical", 1024); dump("done")
except Exception as ex:
    dump("exception " + repr(ex)); raise
