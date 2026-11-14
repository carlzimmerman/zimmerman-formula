#!/usr/bin/env python3
"""BJ1 build B driver (FROZEN_CRITERIA.md 9e7ce0dfe6, section 2, G-F at flux level): a copy of XJ1's second-pass driver
xj1b2_run.py (closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface) with the fields R, B1, B2, B3 (the
charge-budget junction at the first, second and third caustic, tables from bj1_lib.tables) and, at the anchors, the twin
TWB = R + 2 (B1 - R); parts in parts_b/. Box, realisation, gas, flux, guards, seeds and brackets are FWN1R's / XJ1's,
unchanged. The graded fields may be narrowed by BJ1B_CASES (comma list, default B1,B2,B3; B1 is always built, for the
twin) to the cases that pass G-RC, as the criteria say. XJ1's docstring follows.
XJ1 build B, second pass (AMENDMENT_A3 and AMENDMENT_A5): a copy of xj1b_run.py with the case list changed. FWN1R driver:
one JSON part per (stage, z, seed, footing); both footings of a (z, seed) are built together (shared counts, positions,
white noise). Restartable: finished parts are skipped. SIGTERM, or peak RSS above 16 GB, stops between parts with exit 75.
  nice -n 19 python3 -I -B bj1b_run.py prim <seed> [<seed> ...]   (all 12 bins)
  nice -n 19 python3 -I -B bj1b_run.py br                          (brackets: anchors, seeds 0, 1)
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, signal, resource, subprocess
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bj1_lib as BL
X = BL.X                                                   # FWN1R's library, read-only (through XJ1's)

STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda s, f: STOP.update(flag=True))
PARTS = os.environ.get("BJ1B_PARTS") or os.path.join(HERE, "parts_b"); os.makedirs(PARTS, exist_ok=True)
RSS_MAX = 16 * 1024 ** 3
GRADED = [c for c in os.environ.get("BJ1B_CASES", "B1,B2,B3").split(",") if c]
assert set(GRADED) <= {"B1", "B2", "B3"} and GRADED
FIELDS = ["B1"] + [c for c in GRADED if c != "B1"]
CASES = dict([("R", ("R", 0, "main"))] + [(c, ("B", int(c[1]), "main")) for c in FIELDS])
BRK = {"lam_x0.5": dict(lam=0.5 * X.LAM0), "lam_x2": dict(lam=2.0 * X.LAM0), "gam_1.2": dict(gam=1.2), "gam_1.6": dict(gam=1.6),
       "tau_x0.9": dict(stau=0.9), "tau_x1.1": dict(stau=1.1), "lam_91.4": dict(lam=X.lam_kpc(91.4)), "lam_138.6": dict(lam=X.lam_kpc(138.6))}

def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss       # bytes on macOS (counts reusable pages; inflated)
def footprint_gb():
    """physical footprint (what macOS memory pressure counts), from the system's footprint tool."""
    try:
        o = subprocess.run(["footprint", "-p", str(os.getpid())], capture_output=True, text=True, timeout=30).stdout
        for ln in o.splitlines():
            if "phys_footprint:" in ln:
                v, u = ln.split(":")[1].split()[:2]; return float(v) * {"KB": 1e-6, "MB": 1e-3, "GB": 1.0}.get(u, 1.0)
    except Exception: pass
    return 0.0
def pname(stage, z, s, ft, tag=None): return os.path.join(PARTS, f"{stage}_z{z:.1f}_s{s}" + (f"_{tag}" if tag else "") + f"_{ft}.json")

def names_for(stage, z, s):
    if stage == "br": return ["R"] + FIELDS
    return ["R"] + FIELDS

def run(stage, z, s, box, TT, btag=None):
    if all(os.path.exists(pname(stage, z, s, ft, btag)) for ft in X.FOOTS): return
    t0 = time.time(); iz = X.ZB.index(z); names = names_for(stage, z, s)
    FK, info = X.realise(box, TT, iz, s, names)
    for ft in X.FOOTS:
        fk = FK[ft]; T = TT[ft]
        res = dict(lane="BJ1B", stage=stage, z=z, seed=s, footing=ft, N=box.N, L=box.L, info=dict(n_halo=info["n_halo"], **info[ft]),
                   vstar=T["vstar"], n_above=T["n_above"], n_grid=T["n"], layout_info=T["info"], flux={}, floored={}, P3D={})
        if stage == "prim":
            kc = None
            for nm in names:
                kc, p = X.pk3d(box, fk[nm]); res["P3D"][nm] = p.tolist()
            res["P3D"]["k"] = kc.tolist()
            res["expected"] = {nm: [float(np.interp(math.log(k), np.log(X.KT[1:]), (T["P"][nm] / T["P"]["R"])[1:])) for k in (1.0, 3.0, 5.0)] for nm in names}
            jobs = [(nm, nm, {}) for nm in names]
            if z in X.ANCH:
                fk["TWB"] = fk["R"] + np.complex64(2.0) * (fk["B1"] - fk["R"]); jobs.append(("TWB", "TWB", {}))
            tags = [("primary", j) for j in jobs]
        else:
            tags = [(btag, (nm, nm, BRK[btag])) for nm in names]; res["bracket"] = btag
        for tag, (lab, nm, o) in tags:
            rho, fl = X.gas(box, fk[nm], o.get("lam", X.LAM0))
            kv, p, inf = X.flux_p1d(box, rho, z, gam=o.get("gam", 1.5), stau=o.get("stau", 1.0)); del rho
            res["flux"].setdefault(tag, {})[lab] = dict(p=p.tolist(), **inf); res["floored"][f"{tag}|{lab}"] = fl; res["kv"] = kv.tolist()
            fp = footprint_gb(); res["footprint_max_gb"] = max(res.get("footprint_max_gb", 0.0), fp)
            if fp > 16.0: print(f"physical footprint {fp:.1f} GB above 16 GB: exiting for a restart (part not written)", flush=True); sys.exit(75)
        res["time_s"] = time.time() - t0; res["rss_gb"] = rss() / 1024 ** 3
        res["note"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
        f = pname(stage, z, s, ft, btag); json.dump(res, open(f + ".tmp", "w")); os.replace(f + ".tmp", f)
        FK[ft] = None; fk = None
    del FK
    print(f"{stage} z {z:.1f} seed {s}" + (f" {btag}" if btag else "") + f": {time.time() - t0:.0f} s; halos {info['n_halo']}; fs {info['canonical']['fs']:.4f}; peak RSS {rss() / 1024 ** 3:.2f} GB", flush=True)

if __name__ == "__main__":
    stage = sys.argv[1]
    plan = [(z, int(s)) for z in X.ZB for s in sys.argv[2:]] if stage == "prim" else [(z, s, b) for z in X.ANCH for s in (0, 1) for b in BRK]
    if os.environ.get("BJ1B_TESTZ"): plan = [p_ for p_ in plan if p_[0] == float(os.environ["BJ1B_TESTZ"])]
    box = X.Box(int(os.environ.get("BJ1B_N", "384")), 20.0); cache = {}
    for item in plan:
        z, s = item[0], item[1]; btag = item[2] if len(item) > 2 else None
        if STOP["flag"]: print("SIGTERM: stopped between parts; rerun to resume", flush=True); sys.exit(75)
        if rss() > RSS_MAX: print("peak RSS above 16 GB: exiting for a restart", flush=True); sys.exit(75)
        if all(os.path.exists(pname(stage, z, s, ft, btag)) for ft in X.FOOTS): continue
        # FWN1R's operational checks before every part (unchanged): stop below 8 GB disk or above 14 GB swap; wait unless
        # >= 10 GB disk and >= 24 GB free + inactive memory. Up to two runners; a part is claimed by an exclusive claim file.
        st = os.statvfs(PARTS); free_gb = st.f_bavail * st.f_frsize / 1024 ** 3
        sw = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout
        sw_mb = float(sw.split("used = ")[1].split("M")[0])
        vm = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout.splitlines()
        pg = int(vm[0].split("page size of ")[1].split()[0]); pv = {l.split(":")[0]: int(l.split(":")[1].strip().rstrip(".")) for l in vm[1:] if ":" in l and l.split(":")[1].strip().rstrip(".").isdigit()}
        mem_gb = (pv.get("Pages free", 0) + pv.get("Pages inactive", 0)) * pg / 1024 ** 3
        if free_gb < 8 or sw_mb > 14336: print(f"STOP: free disk {free_gb:.1f} GB, swap used {sw_mb:.0f} MB", flush=True); sys.exit(2)
        if free_gb < 10 or mem_gb < 24: print(f"WAIT: free disk {free_gb:.1f} GB, free + inactive memory {mem_gb:.1f} GB", flush=True); sys.exit(3)
        cl = os.path.join(PARTS, f"{stage}_z{z:.1f}_s{s}" + (f"_{btag}" if btag else "") + ".claim")
        try:
            fd = os.open(cl, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, str(os.getpid()).encode()); os.close(fd)
        except FileExistsError:
            try:
                pid = int(open(cl).read().strip()); os.kill(pid, 0); continue        # claimed by a live runner
            except (ProcessLookupError, ValueError):                               # stale claim: take it over
                open(cl + ".tmp", "w").write(str(os.getpid())); os.replace(cl + ".tmp", cl)
        if z not in cache: cache = {z: BL.tables(z, CASES)}
        try: run(stage, z, s, box, cache[z], btag)
        finally: os.remove(cl)
        print("one part per process (memory bound): exiting for a restart", flush=True); sys.exit(75)
    print(f"stage {stage} {sys.argv[2:]} done", flush=True)
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
