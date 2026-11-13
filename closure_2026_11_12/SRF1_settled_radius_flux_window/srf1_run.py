#!/usr/bin/env python3
"""SRF1 (FROZEN_CRITERIA.md fa73352ceb, AMENDMENT_A1 88144763e1): flux-level forest fields for the settled-radius family.
FRZ3R's frz3r_core.py is imported read-only (FRZ3R's folder); FRZ3R's reading T build with U_B replaced by U_S(f), plus the
stratified rare-halo estimator (base box + forced boxes). One part file per (stage, z, seed, footing); restartable; SIGTERM
stops between parts (exit 75). Flux fields run 4 at a time in threads with FFT workers 1 (4 threads in all).
Usage: nice -n 19 python3 srf1_run.py <stage> [z ...]   stage: primary | bracket | clustered | res
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); sys.path.insert(1, os.path.join(REPO, "closure_2026_11_12", "FRZ3R_blind_flux_forest_regrade"))
import frz3r_core as C
import srf1_tables as TB
C.WORKERS = 1
NW = int(os.environ.get("SRF1_THREADS", "3"))
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda s, f: STOP.update(flag=True))
PARTS = TB.PARTS; FOOTS = TB.FOOTS
LBOX = 20.0
GAM = 1.5
LAM0 = 0.079 * 0.6736                                   # 79 comoving kpc (Kulkarni+15, as FRZ3R), Mpc/h comoving
def lam_rec(z): return 0.100 * (1 + z) * 0.6736         # 100 proper kpc
def tau_eff(z): return 0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132
def Fbar(z, s=1.0): return math.exp(-s * tau_eff(z))
def beta_of(g): return 2.0 - 0.7 * (g - 1.0)
ANCH = (2.2, 3.0, 4.4)
FGRID = [0.70, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 2.00, 3.00, math.inf]      # A1 item 3
BRF = [1.00, 1.30, 2.00]
fk_ = TB.fkey
E_THR, SHARE_CUT, NG_MAX, MASS_CAP = 30.0, 0.03, 12, 0.05

class UGrid:
    """FRZ3R's Grid.on_grid evaluated on the unique |k| values and gathered (identical numbers, less work)."""
    def __init__(self, grid):
        kk = grid.k.ravel(); u, inv = np.unique(kk, return_inverse=True); self.inv = inv.astype(np.int32).reshape(grid.k.shape)
        KT = C.KT; lk = np.log(np.maximum(u, 1e-30)); lt = np.log(np.maximum(KT, 1e-30))
        i = np.clip(np.searchsorted(KT, u) - 1, 0, len(KT) - 2)
        w = np.where(i == 0, u / KT[1], (lk - lt[i]) / (lt[i + 1] - lt[i]))
        self.ti = i.astype(np.int32); self.tw = np.clip(w, 0, 1).astype(np.float32)
    def vals(self, Ut):
        return ((1 - self.tw) * Ut[self.ti] + self.tw * Ut[self.ti + 1]).astype(np.float32)
    def on_grid(self, Ut, scale=None):
        v = self.vals(Ut)
        if scale is not None: v = v / scale
        return np.take(v, self.inv)

_SN = {}
def masses(z):
    """per-grid-mass W, bias, painted subset exactly as FRZ3R's hm_tables / halo_parts use them."""
    SN = TB.srh1(); SN["set_z"](z); L = SN["L"]; LM = L["LM"]
    sel = (LM >= 8.0 - 1e-9) & (LM <= 15.0 + 1e-9); idx = np.nonzero(sel)[0]
    return LM[idx], L["W_M"][idx].copy(), L["BIAS"][idx].copy()

def groups_for(t, lM, W):
    """A1 items 1, 2: rare 0.5 dex groups kept by share of the ta-scope 1h difference at k 3; forced counts."""
    V = LBOX ** 3; bins = t["bins"]; E = bins["Wsum"] * V; lo = bins["lM_lo"]; rare = E < E_THR
    ik = int(np.searchsorted(C.KT, 3.0)); UR = t["UbR"][:, ik]; gidx = np.floor((lo + 1e-6 - 8.0) / 0.5).astype(int)
    shares = {}
    for key in ("f1.00", "f1.30", "f2.00"):
        dU = t["Ub"][key][:, ik]; d1 = bins["Wsum"] * ((UR + dU) ** 2 - UR ** 2); tot = d1.sum()
        shares[key] = {int(g): float(d1[rare & (gidx == g)].sum() / tot) for g in np.unique(gidx[rare])}
        shares[key]["common"] = float(d1[~rare].sum() / tot)
    keep = [g for g in sorted(k for k in shares["f1.00"] if k != "common") if max(abs(shares[k][g]) for k in shares) >= SHARE_CUT]
    out = []
    Mta_b = t["UbR"][:, 0]
    for g in keep:
        m = rare & (gidx == g) & (E > 0); Eg = float(E[m].sum())
        Mg = float(np.sum(E[m] * Mta_b[m]) / Eg)
        ng = int(min(NG_MAX, max(1, math.floor(MASS_CAP * t["RHO"] * V / Mg))))
        out.append(dict(g=int(g), lM=8.0 + 0.5 * g, bins=np.nonzero(m)[0].tolist(), E=E[m].tolist(), Eg=Eg, Mg=Mg, ng=ng, w=Eg / ng))
    dropped = {k: float(sum(v for gg, v in s.items() if gg != "common" and gg not in keep)) for k, s in shares.items()}
    return out, shares, dropped, rare

def paint(grid, ug, t, lM, W, b, seed, rare, keys_c, keys_rP, cluster_G=None, Rf=0.5):
    """FRZ3R's halo_parts loop (same random stream, same bins); ref painted on every halo; difference keys on common bins
    (keys_c) and, for the Poisson-only reading, on rare bins (keys_rP)."""
    rng = np.random.default_rng(7919 + seed)
    N, V = grid.N, grid.L ** 3; RHO = t["RHO"]; norm = RHO * grid.dx ** 3
    edges = np.arange(8.0 - 1e-9, lM[-1] + 0.1, 0.1); bid = np.digitize(lM, edges) - 1
    if cluster_G is not None:
        gf = grid.irfft(cluster_G * np.exp(-0.5 * (grid.k * Rf) ** 2)).ravel().astype(np.float64)
    acc_ref = np.zeros(grid.k.shape, np.complex64); acc_c = {k: np.zeros(grid.k.shape, np.complex64) for k in keys_c}
    acc_rP = {k: np.zeros(grid.k.shape, np.complex64) for k in keys_rP}; Mh = 0.0; ntot = 0
    for ib in range(bid.max() + 1):
        m = bid == ib; Ne_i = W[m] * V; Ne = float(Ne_i.sum())
        if Ne <= 0: continue
        n = int(rng.poisson(Ne))
        if n == 0: continue
        wts = Ne_i / Ne
        if cluster_G is None:
            pos = rng.random((n, 3)) * grid.L
        else:
            bb = float(np.sum(wts * b[m])); lw = bb * gf; lw -= lw.max(); p = np.exp(lw); p /= p.sum()
            cells = rng.choice(N ** 3, size=n, p=p)
            pos = (np.stack(np.unravel_index(cells, (N,) * 3), 1) + rng.random((n, 3))) * grid.dx
        nk = grid.rfft(C.cic(grid, pos)) / grid.wcic
        Uref = t["UbR"][ib]; acc_ref += nk * ug.on_grid(Uref, norm); Mh += n * Uref[0]
        ks = keys_c if not rare[ib] else []
        for key in ks: acc_c[key] += nk * ug.on_grid(t["Ub"][key][ib], norm)
        for key in keys_rP: acc_rP[key] += nk * ug.on_grid(t["Ub"][key][ib], norm)   # Poisson-only: every bin, in FRZ3R's order
        ntot += n; del nk
    return acc_ref, acc_c, acc_rP, Mh, ntot

def forced(grid, ug, t, gr, seed, z, keys):
    rng = np.random.default_rng([seed, int(round(z * 10)), gr["g"], 104729])
    norm = t["RHO"] * grid.dx ** 3; p = np.array(gr["E"]) / gr["Eg"]
    pick = rng.choice(len(gr["bins"]), size=gr["ng"], p=p); counts = np.bincount(pick, minlength=len(gr["bins"]))
    acc_ref = np.zeros(grid.k.shape, np.complex64); acc = {k: np.zeros(grid.k.shape, np.complex64) for k in keys}; Mh = 0.0
    for j, ib in enumerate(gr["bins"]):
        n = int(counts[j])
        if n == 0: continue
        pos = rng.random((n, 3)) * grid.L
        nk = grid.rfft(C.cic(grid, pos)) / grid.wcic
        acc_ref += nk * ug.on_grid(t["UbR"][ib], norm); Mh += n * t["UbR"][ib][0]
        for key in keys: acc[key] += nk * ug.on_grid(t["Ub"][key][ib], norm)
    return acc_ref, acc, Mh, counts.tolist()

def flux_job(grid, z, fk, lam, gam=GAM, sF=1.0, mode="exp", want3d=True):
    g = C.gas(grid, fk, lam); fl = float(np.sum(g < 1e-6)) / g.size; g = np.maximum(g, 1e-6)
    kv, p, inf = C.flux_p1d(grid, g, z, beta_of(gam), gam, Fbar(z, sF), mode=mode); del g
    out = dict(p=p.tolist(), A=inf["A"], meanF=inf["meanF"], floored=fl)
    if want3d: out["P3D"] = C.pk3d(grid, fk, nbins=40, kmin=0.3)[1].tolist()
    return kv, out

def run_part(stage, z, seed, ft, N=384, box=None):
    """box None: the whole part in one process. box 'base': base box only (saves the reference halo field and the smooth field
    to temporary npy files); box '<g>': forced group g only (loads them). 'merge' joins the sub-parts into the part file.
    One box per process keeps memory bounded (macOS does not return freed memory between boxes)."""
    name = os.path.join(PARTS, f"{stage}_z{z:.1f}_s{seed}_{ft}_N{N}.json")
    if os.path.exists(name): return
    stem = name[:-5]
    if box == "merge":
        res = json.load(open(stem + "__base.json"))
        for gr in res["groups"]:
            sub = json.load(open(stem + f"__g{gr['g']}.json"))
            for sp, bxs in sub["flux"].items(): res["flux"].setdefault(sp, {}).update(bxs)
            res.setdefault("forced", {})[str(gr["g"])] = sub["forced"]; res["time_s"] += sub["time_s"]
        tmp = name + ".tmp"; json.dump(res, open(tmp, "w")); os.replace(tmp, name)
        for f in [stem + "__base.json", stem + "__acc_ref.npy", stem + "__dsk.npy"] + [stem + f"__g{gr['g']}.json" for gr in res["groups"]]:
            if os.path.exists(f): os.remove(f)
        print(f"{stage} z {z:.1f} seed {seed} {ft} N {N}: {res['time_s']:.0f} s; groups {[(g['lM'], g['ng']) for g in res['groups']]}; fs {res['fs']:.4f} halos {res['n_halo']}", flush=True)
        return
    if box not in (None, "base"):
        sub = stem + f"__g{box}.json"
        if os.path.exists(sub): return
    elif box == "base" and os.path.exists(stem + "__base.json"): return
    t0 = time.time(); T = TB.tables(z); t = T[ft]; lM, W, b = masses(z)
    grid = C.Grid(N, LBOX); ug = UGrid(grid); RHO = t["RHO"]; V = LBOX ** 3
    groups, shares, dropped, rare = groups_for(t, lM, W)
    anchor = z in ANCH
    if stage == "primary":
        fl = [fk_(f) for f in FGRID] + (["f0.00", "MU2"] if (anchor and seed == 0) else [])
        flP = ["f1.00", "finf"]
        specs = [("primary", LAM0, GAM, 1.0, "exp")]
    else:
        fl = [fk_(f) for f in BRF]; flP = []
        if stage == "bracket":
            specs = [("primary", LAM0, GAM, 1.0, "exp"), ("lam_x0.5", 0.5 * LAM0, GAM, 1.0, "exp"), ("lam_x2", 2 * LAM0, GAM, 1.0, "exp"),
                     ("lam_rec", lam_rec(z), GAM, 1.0, "exp"), ("gam_1.2", LAM0, 1.2, 1.0, "exp"), ("gam_1.6", LAM0, 1.6, 1.0, "exp"),
                     ("tau_x0.9", LAM0, GAM, 0.9, "exp"), ("tau_x1.1", LAM0, GAM, 1.1, "exp"), ("M1_lin", LAM0, GAM, 1.0, "lin")]
        else:
            specs = [("primary", LAM0, GAM, 1.0, "exp")]
    # ---- base box (FRZ3R reading T reference)
    fs_exp = 1.0 - t["Mta_sum_painted"] / RHO
    if box not in (None, "base"):
        meta = json.load(open(stem + "__base.json")); acc_ref = np.load(stem + "__acc_ref.npy"); dsk = np.load(stem + "__dsk.npy")
        Mh = meta["Mh"]; res = dict(flux={}); gr = [g for g in groups if str(g["g"]) == str(box)][0]
        def run_jobs(jobs):
            with ThreadPoolExecutor(max_workers=NW) as ex:
                futs = [(bx, fn, sp, ex.submit(lambda b=bld, s=sp: flux_job(grid, z, b(), s[1], s[2], s[3], s[4], want3d=(s[0] == "primary")))) for bx, fn, sp, bld in jobs]
                for bx, fn, sp, fu in futs:
                    kv, o = fu.result(); res["flux"].setdefault(sp[0], {}).setdefault(bx, {})[fn] = o
        aref, acc, Mf, counts = forced(grid, ug, t, gr, seed, z, fl)
        fsg = 1.0 - (Mh + Mf) / (RHO * V); Rg = acc_ref + aref + fsg * dsk; Rg.flat[0] = 0.0; del aref, acc_ref
        res["forced"] = dict(counts=counts, fs=fsg, Mforced=Mf)
        jobs = []
        for sp in specs:
            jobs.append((f"g{gr['g']}", "R", sp, lambda: Rg))
            for key in fl: jobs.append((f"g{gr['g']}", "B|" + key, sp, (lambda key=key: Rg + acc[key])))
        run_jobs(jobs); res["time_s"] = time.time() - t0
        tmp = stem + f"__g{box}.json.tmp"; json.dump(res, open(tmp, "w")); os.replace(tmp, stem + f"__g{box}.json")
        print(f"  {stage} z {z:.1f} seed {seed} {ft} group {box}: {res['time_s']:.0f} s", flush=True); return
    S = np.maximum(t["PRta"] - t["p1_Rb"], 1e-12)
    wk = C.white(grid, seed); dsk, Gk, linfo = C.lognormal_smooth(grid, wk, S / fs_exp ** 2); del wk
    acc_ref, acc_c, acc_rP, Mh, nh = paint(grid, ug, t, lM, W, b, seed, rare, list(dict.fromkeys(fl + flP)), flP,
                                           cluster_G=Gk if stage == "clustered" else None)
    del Gk
    fs = 1.0 - Mh / (RHO * V)
    base = acc_ref + fs * dsk; base.flat[0] = 0.0
    def T2(key): return ug.on_grid(np.sqrt(np.maximum(1.0 + t["spec"][key]["D2h"] / S, 0.0))) - 1.0
    res = dict(stage=stage, z=z, seed=seed, footing=ft, N=N, L=LBOX, dv=C.dv_cell(grid, z), fs=fs, fs_exp=fs_exp, n_halo=nh, info=linfo,
               groups=[{k: v for k, v in g.items()} for g in groups], shares=shares, dropped_share=dropped, flux={}, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
    def mk_base(key, poisson=False):
        if poisson: fk = base + (acc_rP[key] + fs * dsk * T2(key))      # FRZ3R's order: base + (acc_dU + fs dsk T2m1)
        else: fk = base + acc_c[key] + fs * dsk * T2(key)
        fk.flat[0] = 0.0; return fk
    jobs = []                                            # (box, field, spec, builder)
    for sp in specs:
        jobs.append(("base", "R", sp, lambda: base))
        for key in fl: jobs.append(("base", "B|" + key, sp, (lambda key=key: mk_base(key))))
        if sp[0] == "primary":
            for key in flP: jobs.append(("base", "BP|" + key, sp, (lambda key=key: mk_base(key, True))))
    def run_jobs(jobs):
        with ThreadPoolExecutor(max_workers=NW) as ex:
            futs = [(bx, fn, sp, ex.submit(lambda b=bld, s=sp: flux_job(grid, z, b(), s[1], s[2], s[3], s[4], want3d=(s[0] == "primary")))) for bx, fn, sp, bld in jobs]
            for bx, fn, sp, fu in futs:
                kv, o = fu.result(); res["kv"] = kv.tolist(); res["flux"].setdefault(sp[0], {}).setdefault(bx, {})[fn] = o
    run_jobs(jobs)
    kc = C.pk3d(grid, base, nbins=40, kmin=0.3)[0]; res["k3d"] = kc.tolist()
    del acc_c, acc_rP
    if box == "base":
        res["Mh"] = Mh; res["time_s"] = time.time() - t0
        np.save(stem + "__acc_ref.npy", acc_ref); np.save(stem + "__dsk.npy", dsk)
        tmp = stem + "__base.json.tmp"; json.dump(res, open(tmp, "w")); os.replace(tmp, stem + "__base.json")
        print(f"  {stage} z {z:.1f} seed {seed} {ft} base: {res['time_s']:.0f} s; groups {[g['g'] for g in groups]}", flush=True); return
    # ---- forced boxes
    for gr in groups:
        if STOP["flag"]: break
        aref, acc, Mf, counts = forced(grid, ug, t, gr, seed, z, fl)
        fsg = 1.0 - (Mh + Mf) / (RHO * V); Rg = acc_ref + aref + fsg * dsk; Rg.flat[0] = 0.0; del aref
        gres = dict(counts=counts, fs=fsg, Mforced=Mf); res.setdefault("forced", {})[str(gr["g"])] = gres
        jobs = []
        for sp in specs:
            jobs.append((f"g{gr['g']}", "R", sp, lambda: Rg))
            for key in fl: jobs.append((f"g{gr['g']}", "B|" + key, sp, (lambda key=key: Rg + acc[key])))
        run_jobs(jobs); del acc, Rg
    if STOP["flag"]: print("SIGTERM inside part: part not written", flush=True); sys.exit(75)
    res["time_s"] = time.time() - t0
    tmp = name + ".tmp"; json.dump(res, open(tmp, "w")); os.replace(tmp, name)
    print(f"{stage} z {z:.1f} seed {seed} {ft} N {N}: {res['time_s']:.0f} s; groups {[ (g['lM'], g['ng']) for g in groups]}; fs {fs:.4f} halos {nh}", flush=True)

if __name__ == "__main__":
    if sys.argv[1] == "one":                     # one part per process (macOS malloc keeps freed memory across parts)
        st, z, seed, ft = sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]; bx = sys.argv[6] if len(sys.argv) > 6 else None
        run_part(st, z, seed, ft, N=256 if st == "res" else 384, box=bx); sys.exit(0)
    if sys.argv[1] == "groups":                  # print the forced group ids of a base sub-part
        st, z, seed, ft = sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]; N = 256 if st == "res" else 384
        nm = os.path.join(PARTS, f"{st}_z{z:.1f}_s{seed}_{ft}_N{N}")
        if os.path.exists(nm + ".json"): print(""); sys.exit(0)
        print(" ".join(str(g["g"]) for g in json.load(open(nm + "__base.json"))["groups"])); sys.exit(0)
    stage = sys.argv[1]; zs = [float(x) for x in sys.argv[2:]]
    for z in zs:
        if stage == "primary": seeds = (0, 1) if z in ANCH else (0,)
        else: seeds = (0,)
        for seed in seeds:
            for ft in FOOTS:
                if STOP["flag"]: print("SIGTERM: stopped between parts; rerun to resume", flush=True); sys.exit(75)
                run_part(stage, z, seed, ft, N=256 if stage == "res" else 384)
    open(os.path.join(PARTS, f"done_{stage}_" + "_".join(f"{z:.1f}" for z in zs)), "w").write("done\n")
