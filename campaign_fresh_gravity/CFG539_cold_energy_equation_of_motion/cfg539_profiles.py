#!/usr/bin/env python3
"""CFG539 law-consistency statistic (FROZEN_CRITERIA.md): CFG526's statistic (cfg526_profiles.py, imported as a module, as CFG530 did) on the
TWO-SPECIES runs.  Declared changes, all forced by the two-species engine:
  (i)  NP = the run's mesh N; cache folder per N (_external_data/cfg539_work/profiles/N<N>/); rmin = the engine's RMIN_PHYS (CFG530's patch);
  (ii) M_grav = the particle mass (both species): the CFG539 engine has NO extra source term, so rho_grav = rho_particles exactly;
  (iii) the baryon masses come from the baryon particles: M_b,all = f_b (1 + delta_b), M_b,ret = f_ret f_b (1 + delta_b)
       (CFG526: f_b x all particles).  In `analyse` the one line `Mba = FB * Mp` reads the stored M_ba (asserted to occur once);
       for a single-species state (S0, EOM OFF) M_ba = f_b M_p, i.e. CFG526 exactly;
  (iv) f_ret, the census edge and the turnaround catchments are the engine's in_cover on the run's own total density at z = 0 (as CFG526 did
       through the engine's forces);
  (v)  the matched-S0 fields are CFG530's S0 caches at the same (L, N, NSEED 512, seed 359), copied into the CFG539 cache folder.
Peaks, r_ON, the 100 densest scored hosts, the profile radii, R = M_grav / M_law with M_law = M_b,all + (nu - 1) M_b,ret, are CFG526's.
  python3 cfg539_profiles.py compute NAME [NAME ...]     (NAME = a key of RUNS below)
  python3 cfg539_profiles.py check                       copy-identity check: CFG526's analyse vs the patched analyse on a CFG530 cache"""
import os, sys, json, math, types, time, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
P526 = os.path.join(CFG, "CFG526_small_scale_deficit_judged", "cfg526_profiles.py")
E539 = os.path.join(HERE, "cfg539_pm.py")
W539 = os.path.join(EXT, "cfg539_work"); PROF = os.path.join(W539, "profiles")
W530 = os.path.join(EXT, "cfg530_work")
REPL = [("rmin = 2 * L / 256 if L != 200 else 1.56", "rmin = mod.RMIN_PHYS"),
        ("Mba = FB * Mp", "Mba = (d['M_ba'][sel] * Mcell) if 'M_ba' in d.files else FB * Mp")]
src = open(P526).read()
for a, b in REPL:
    assert src.count(a) == 1, a
    src = src.replace(a, b)
C = types.ModuleType("cfg526p539"); C.__file__ = P526
exec(compile(src, P526, "exec"), C.__dict__)
import numpy as np
from scipy import ndimage

RMIN = {100: 0.78125, 200: 1.56}

def runs_table():
    """name -> (L, N, foot, eom, edge, mob, z0 npz path, json path)."""
    T = {}
    for L in (100, 200):
        for N in (128, 256):
            b = os.path.join(W530, "runs", f"S0_L{L}_N{N}",
                             f"cfg527_S0_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N{N}" + (f"_L{L}" if L != 200 else "") + "_drawSHELL")
            T[f"S0_L{L}_N{N}"] = (L, N, "canonical", "S0", True, 1.0, b + "_z0.npz", b + ".json")
            for foot, ft in (("canonical", "can"), ("alt", "alt")):
                T[f"S0{ft}_L{L}_N{N}"] = (L, N, foot, "S0", True, 1.0, b + "_z0.npz", b + ".json")   # S0 state judged with this footing's law
                for eom in ("A", "C"):
                    for edge, mob, sfx in ((True, 1.0, ""), (False, 1.0, "_NOEDGE"), (True, 0.5, "_mob0.5"), (True, 2.0, "_mob2")):
                        tag = f"cfg539_EOM{eom}{'' if edge else '_NOEDGE'}{f'_mob{mob:g}' if mob != 1.0 else ''}_FLAT_{foot}_N{N}_L{L}_ns512"
                        T[f"{eom}{ft}{sfx}_L{L}_N{N}"] = (L, N, foot, eom, edge, mob, os.path.join(W539, tag + "_z0.npz"),
                                                        os.path.join(W539, tag + ".json"))
            tag = f"cfg539_EOMOFF_FLAT_S0_N{N}_L{L}_ns512"
            T[f"OFF_L{L}_N{N}"] = (L, N, "canonical", "OFF", True, 1.0, os.path.join(W539, tag + "_z0.npz"), os.path.join(W539, tag + ".json"))
    return T
RUNS = runs_table()

def load_engine(name):
    L, N, foot, eom, edge, mob, _, _ = RUNS[name]
    env = {"CFG539_L": f"{L:g}", "CFG539_RMIN": str(RMIN[L]), "CFG539_THREADS": "4", "CFG539_NSEED": "512",
           "CFG539_EOM": eom if eom in ("A", "C") else "OFF", "CFG539_EDGE": "1" if edge else "0", "CFG539_MOB": str(mob)}
    for k in list(os.environ):
        if k.startswith("CFG539_"): del os.environ[k]
    os.environ.update(env)
    spec = importlib.util.spec_from_file_location(f"e539_{name}", E539); mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def setup(N):
    C.NP = N; C.WORK = os.path.join(PROF, f"N{N}"); os.makedirs(C.WORK, exist_ok=True); C._S0F.clear()
    for L in (100, 200):                                   # matched-S0 fields: CFG530's caches (same L, N, NSEED, seed)
        dst = os.path.join(C.WORK, f"cfg526_S0_L{L}_rhop.npy"); srcf = os.path.join(W530, "profiles", f"N{N}", f"cfg526_S0_L{L}_rhop.npy")
        if not os.path.exists(dst) and os.path.exists(srcf):
            shutil.copyfile(srcf, dst)
    C.RUNS = {n: (v[0], E539, "CFG539", {}, "S0" if v[3] in ("S0", "OFF") else "RES", v[2], v[6][:-8]) for n, v in RUNS.items() if v[1] == N}
    C.load_engine = load_engine

def ball(M, R):
    return C.ball(M, R)

def compute(name):
    L, N, foot, eom, edge, mob, npz, js_path = RUNS[name]
    setup(N)
    out = os.path.join(C.WORK, f"cfg526_{name}.npz")
    if os.path.exists(out):
        print("cached", name); return
    t0 = time.time()
    mod = load_engine(name)
    z = np.load(npz)
    if "pos_b" in z.files:
        pb = z["pos_b"].astype(np.float64); pc = z["pos_c"].astype(np.float64) if "pos_c" in z.files else pb
    else:
        pb = z["pos"].astype(np.float64); pc = pb
    js = json.load(open(js_path))["snap"]["z0"]
    mesh = mod.Mesh(N); dta = mod.dta_table()
    dtot, db, dc = mod.deposit2(mesh, pb, pc); del pb, pc
    K = {"shared": {}}
    _, _, info = mod.forces2(mesh, dtot, db, dc, 1.0, "FLAT", foot, dta, diag=True)    # z = 0 law diagnostics (S0 too: this footing's law)
    if eom in ("A", "C", "OFF"):                           # state reproduction (K1): the z = 0 diagnostics recomputed from the saved positions
        for k_ in ("d_sum", "unfilled_frac", "cold_frac_in_edge", "mass_frac_in_catch"):
            if k_ in js: K["shared"][k_] = [float(info[k_]), float(js[k_])]
    kb, pkb, s8 = mod.measure_pk(mesh, dtot, N ** 3)
    K["pk_z0_check"] = float(np.max(np.abs(np.array(pkb) / np.array(js["P"]) - 1)))
    K["s0_maxdiff_rel"] = 0.0; K["mean_grav_minus_p"] = 0.0          # rho_grav = rho_particles identically (no extra source)
    D = js.get("Delta_ta")
    if D is None:
        D = math.exp(np.interp(0.0, np.log1p(dta["z"]), np.log(dta["D"])))
    catch, fret = mod.in_cover(mesh, dtot, D, 1.0, 1.0, "FLAT", foot, want_fret=True)
    FB = mod.FB
    rho_p = (1.0 + dtot).astype(np.float32); del dtot
    rba = (FB * (1.0 + db)).astype(np.float32); rbret = (fret * rba).astype(np.float32); del db, dc
    kk = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
    kJ = lambda T: math.sqrt(1.5 * mod.Om) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    fc, fh, fs = mod.MIXES["MIXA"]
    Wk = (fc / (1.0 + kk / kJ(1e4) ** 2) + fh / (1.0 + kk / kJ(1e6) ** 2) + fs).astype(np.float32); del kk
    rin = mesh.inv(mesh.fwd(rbret) * Wk); del Wk
    dx = L / N
    mx = ndimage.maximum_filter(rho_p, size=3, mode="wrap"); pk = np.argwhere(rho_p == mx); del mx
    pk = pk[np.argsort(rho_p[pk[:, 0], pk[:, 1], pk[:, 2]])[::-1][:C.NCAND]]
    ii = (pk[:, 0], pk[:, 1], pk[:, 2])
    Rg = np.geomspace(dx, 8.0, 14)
    rpk = mesh.fwd(rho_p)
    ok = np.ones(len(pk), bool); ron = np.zeros(len(pk))
    for R in Rg:
        b, nb = ball(N, R / dx)
        mean = mesh.inv(rpk * mesh.fwd(b))[ii] / nb
        ok &= mean >= D; ron[ok] = R
    prof = {}; nball = []
    fk = {"p": rpk, "bret": mesh.fwd(rbret), "in": mesh.fwd(rin), "ba": mesh.fwd(rba)}
    for R in C.RPROF:
        b, nb = ball(N, R); nball.append(nb); bk = mesh.fwd(b)
        for f, xk in fk.items():
            prof.setdefault(f, []).append(mesh.inv(xk * bk)[ii])
    prof = {f: np.array(v).T for f, v in prof.items()}
    prof["g"] = prof["p"]
    np.savez_compressed(out, pk=pk, ron=ron, rho_at=rho_p[ii], fret_at=fret[ii], nball=np.array(nball), dx=dx, L=L, Om=mod.Om, FB=FB,
                        Delta_ta=D, foot=foot, sw=("S0" if eom in ("S0", "OFF") else "RES"), **{f"M_{f}": v for f, v in prof.items()},
                        K=json.dumps(K), info=json.dumps({k: v for k, v in info.items() if isinstance(v, (int, float))}), s8=s8)
    print(f"done {name} {time.time() - t0:.0f}s K={json.dumps(K)}", flush=True)

def analyse(name):
    L, N = RUNS[name][0], RUNS[name][1]
    setup(N)
    return C.analyse(name)

def identity_check():
    """the patched analyse must equal CFG526's on a CFG530 cache (which has no M_ba key): CFG530 LRcan_L200 N256."""
    import types as _t
    s0 = open(P526).read().replace(REPL[0][0], REPL[0][1])
    C0 = _t.ModuleType("c0"); C0.__file__ = P526; exec(compile(s0, P526, "exec"), C0.__dict__)
    out = {}
    for MOD in (C0, C):
        MOD.NP = 256; MOD.WORK = os.path.join(W530, "profiles", "N256"); MOD._S0F.clear()
        MOD.RUNS = {"LRcan_L200": (200, os.path.join(CFG, "CFG527_law_respecting_engine", "cfg527_pm.py"), "CFG527", {"DRAW": "SHELL"},
                                   "RES", "canonical", "unused")}
        l0 = MOD.load_engine
        def le(name, l0=l0, MOD=MOD):
            m = l0(name); m.MIX = "NOFILT"; m.RMIN_PHYS = 1.56; return m
        MOD.load_engine = le
        r, h = MOD.analyse("LRcan_L200"); out[MOD.__name__] = r["core"]["R"][0]
    return out

if __name__ == "__main__":
    try: os.nice(10)
    except OSError: pass
    if len(sys.argv) > 1 and sys.argv[1] == "compute":
        for n in sys.argv[2:]:
            compute(n)
    elif len(sys.argv) > 1 and sys.argv[1] == "check":
        o = identity_check(); print(o); v = list(o.values()); print("IDENTITY", "PASS" if abs(v[0] - v[1]) <= 1e-12 else "FAIL")
