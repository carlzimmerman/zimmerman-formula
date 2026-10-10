#!/usr/bin/env python3
"""CFG530 law-consistency statistic (FROZEN_CRITERIA.md): CFG526's cfg526_profiles.py imported as a module with the declared changes only:
NP = the run's mesh N; cache folder per N (profiles/N<N>/, matched S0 = S0_L<L> in that folder); each run's engine loaded with its own RMIN
and mix; and in `analyse` the line `rmin = 2 * L / 256 if L != 200 else 1.56` -> `rmin = mod.RMIN_PHYS` (asserted to occur once).
Also per run (reported): largest-catchment mass share and slab-spanning flag, from the engine's own catchment mask at z = 0.
  python3 cfg530_profiles.py compute [RUN_N ...]   heavy stage (engine forces on each saved z = 0 state), cached
  python3 cfg530_profiles.py identity              statistic identity check on CFG527's own 256^3 caches
  python3 cfg530_profiles.py                       stage 2 -> cfg530_profiles.json / .out"""
import os, sys, json, math, types
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
P526 = os.path.join(CFG, "CFG526_small_scale_deficit_judged", "cfg526_profiles.py")
E527 = os.path.join(CFG, "CFG527_law_respecting_engine", "cfg527_pm.py")
W530 = os.path.join(EXT, "cfg530_work"); PROF = os.path.join(W530, "profiles")
OLD = "rmin = 2 * L / 256 if L != 200 else 1.56"; NEW = "rmin = mod.RMIN_PHYS"
src = open(P526).read(); assert src.count(OLD) == 1
C = types.ModuleType("cfg526p"); C.__file__ = P526
exec(compile(src.replace(OLD, NEW), P526, "exec"), C.__dict__)
import numpy as np

sys.path.insert(0, HERE)
from run_530 import jobspec, result                      # the launcher's own job table

STUDY = [f"{r}_L{L}_N{N}" for L in (100, 200) for N in (128, 256, 512) for r in ("S0", "LRcan", "LRalt")] + \
        [f"{r}_L100_N{N}" for N in (128, 256) for r in ("BXcan", "BXalt")] + ["MUTA_L100_N256"]
S0_411 = os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512")      # reused (cfg530_s0reuse.json)

def spec_of(run):
    s = jobspec(run); short = run.rsplit("_N", 1)[0]
    if run == "S0_L200_N512":
        base = S0_411
    else:
        r = result(run); base = r[:-5] if r else None
    extra = {"DRAW": s["draw"]}
    return short, s, base, (int(s["L"]), E527, "CFG527", extra, s["switch"], s["foot"], base)

LAST = {}
_load0 = C.load_engine
def setup(N, table, rmin, mix):
    """point CFG526's module at mesh N, its per-N cache folder, and this N's run table."""
    C.NP = N; C.WORK = os.path.join(PROF, f"N{N}"); os.makedirs(C.WORK, exist_ok=True)
    C.RUNS = table; C._S0F.clear()
    def load_engine(name):
        mod = _load0(name)                                  # CFG526 loader (env, RC = 0, MIX = MIXA, NTH)
        mod.MIX = mix.get(name, "MIXA"); mod.RMIN_PHYS = rmin.get(name, mod.RMIN_PHYS)
        LAST["mod"] = mod
        return mod
    C.load_engine = load_engine

def tables(N):
    table, rmin, mix, names = {}, {}, {}, {}
    for run in STUDY:
        if not run.endswith(f"_N{N}"): continue
        short, s, base, tup = spec_of(run)
        if base is None: continue
        table[short] = tup; rmin[short] = s["rmin"]; mix[short] = s["mix"]; names[short] = run
    return table, rmin, mix, names

def percolation(short):
    mod = LAST.get("mod"); out = os.path.join(C.WORK, f"perc_{short}.json")
    if mod is None or mod._INC.get("catch") is None: return
    cm = mod._INC["catch"]; N = cm.shape[0]
    r, nc = mod.catch_labels(cm); mm = r >= 0
    pos = np.load(C.RUNS[short][6] + "_z0.npz")["pos"].astype(np.float64)
    mesh = mod.Mesh(N); rho = (1.0 + mesh.deposit(pos)).ravel(); del pos
    w = np.bincount(r[mm], weights=rho[mm], minlength=nc); big = int(np.argmax(w))
    idx = np.nonzero(r == big)[0]; ijk = np.unravel_index(idx, (N, N, N))
    span = [int(np.unique(c).size) for c in ijk]
    json.dump(dict(n_comp=int((w > 0).sum()), largest_mass_share=float(w[big] / w.sum()), largest_vol_frac=float(idx.size / N ** 3),
                   catch_vol_frac=float(mm.mean()), catch_mass_frac=float(rho[mm].sum() / rho.sum()),
                   largest_planes_per_axis=span, spanning=bool(max(span) == N)), open(out, "w"))

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "compute":
    try: os.nice(10)
    except OSError: pass
    want = sys.argv[2:] or STUDY
    for N in (128, 256, 512):
        table, rmin, mix, names = tables(N)
        setup(N, table, rmin, mix)
        order = sorted(table, key=lambda s: (0 if s.startswith("S0") else 1, s))
        for short in order:
            if names[short] not in want: continue
            LAST.clear()
            if not os.path.exists(os.path.join(C.WORK, f"cfg526_{short}.npz")) or not os.path.exists(os.path.join(C.WORK, f"perc_{short}.json")):
                if os.path.exists(os.path.join(C.WORK, f"cfg526_{short}.npz")):
                    os.remove(os.path.join(C.WORK, f"cfg526_{short}.npz"))      # recompute so the catchment mask is in hand
                C.compute(short)
                if table[short][4] != "S0": percolation(short)
    sys.exit(0)

def summarise(short, N):
    res, h = C.analyse(short)
    ok, why = C.kcheck(short, res)
    out = {"N": N, "L": res["L"], "foot": res["foot"], "n_hosts": res["n_hosts"], "n_scored": res["n_scored"], "K_ok": ok, "K_why": why}
    if h is not None:
        out.update(core_R=res["core"]["R"], core_n=res["core"]["n"], core_D_law=res["core"]["D_law"], core_D_eng=res["core"]["D_eng"],
                   per=[{"R_cells": p["R_cells"], "r_eff": p["r_eff"], "n": p["n"], "R": p["R"]} for p in res["per"]],
                   lM_range=res["lM_range"], re_cells_med=res["re_cells_med"])
    pf = os.path.join(C.WORK, f"perc_{short}.json")
    if os.path.exists(pf): out["perc"] = json.load(open(pf))
    return out, h

def pairs(hA, hB, ix):
    out = []
    for jA, jB in ix:
        mA = hA["scored"][:, jA] & (hA["lM"] >= 12.7) & (hA["lM"] <= 14.3)
        mB = hB["scored"][:, jB] & (hB["lM"] >= 12.7) & (hB["lM"] <= 14.3)
        o = {"r_phys": float(hA["reff"][jA]), "nA": int(mA.sum()), "nB": int(mB.sum())}
        if mA.sum() >= 10 and mB.sum() >= 10:
            a = float(np.median(np.log10(hA["R"][mA, jA]))); b = float(np.median(np.log10(hB["R"][mB, jB])))
            o.update(logR_coarse=a, logR_fine=b, d=b - a)
        else:
            o["skip"] = True
        out.append(o)
    return out

def identity():
    """the patched statistic on CFG527's own caches must reproduce cfg527_profiles.json core R to 1e-12."""
    ref = json.load(open(os.path.join(CFG, "CFG527_law_respecting_engine", "cfg527_profiles.json")))["runs"]
    W527 = os.path.join(EXT, "cfg527_work")
    tab, rmin, mix = {}, {}, {}
    def t(L, foot): return os.path.join(W527, f"cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_{foot}_N256" + (f"_L{L}" if L != 200 else "") + "_drawSHELL")
    for L in (100, 200):
        tab[f"S0_L{L}"] = (L, E527, "CFG527", {}, "S0", "canonical", None)
        for tag, foot in (("LRcan", "canonical"), ("LRalt", "alt")):
            tab[f"{tag}_L{L}"] = (L, E527, "CFG527", {"DRAW": "SHELL"}, "RES", foot, t(L, foot)); mix[f"{tag}_L{L}"] = "NOFILT"
            rmin[f"{tag}_L{L}"] = 1.56 if L == 200 else 2 * L / 256
    setup(256, tab, rmin, mix); C.WORK = os.path.join(W527, "profiles")
    out = {}
    for n in ("LRcan_L100", "LRalt_L100", "LRcan_L200", "LRalt_L200"):
        res, _ = C.analyse(n); a, b = res["core"]["R"][0], ref[n]["core"]["R"][0]
        out[n] = {"core_R_cfg530": a, "core_R_cfg527": b, "abs_diff": abs(a - b)}
        print(n, out[n], flush=True)
    out["pass"] = all(v["abs_diff"] <= 1e-12 for v in out.values() if isinstance(v, dict))
    json.dump(out, open(os.path.join(HERE, "cfg530_identity.json"), "w"), indent=1)
    print("statistic identity:", "PASS" if out["pass"] else "FAIL")

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "identity":
    identity(); sys.exit(0)

if __name__ == "__main__":
    A, H = {}, {}
    for N in (128, 256, 512):
        table, rmin, mix, names = tables(N)
        setup(N, table, rmin, mix)
        for short in sorted(table):
            if table[short][4] == "S0" or not os.path.exists(os.path.join(C.WORK, f"cfg526_{short}.npz")): continue
            if not os.path.exists(os.path.join(C.WORK, f"cfg526_S0_L{table[short][0]}.npz")): continue
            A[names[short]], H[names[short]] = summarise(short, N)
            a = A[names[short]]
            print(f"{names[short]:16s} scored {a['n_scored']:3d}  core R {a.get('core_R', [float('nan')])[0]:.3f}  K {'ok' if a['K_ok'] else 'FAIL'}  "
                  f"perc {a.get('perc', {}).get('largest_mass_share', float('nan')):.2f} span {a.get('perc', {}).get('spanning')}", flush=True)
    PH = {}
    for tag in ("LRcan", "LRalt", "BXcan", "BXalt"):
        for L in (100, 200):
            for lo, hi in ((128, 256), (256, 512)):
                a, b = f"{tag}_L{L}_N{lo}", f"{tag}_L{L}_N{hi}"
                if H.get(a) is not None and H.get(b) is not None:
                    PH[f"{a}->{b}"] = pairs(H[a], H[b], ((0, 2), (2, 4), (4, 6)))   # coarse R = 1, 2, 4 cells = fine R = 2, 4, 8 cells
    json.dump({"runs": A, "phys_pairs": PH}, open(os.path.join(HERE, "cfg530_profiles.json"), "w"), indent=1)
