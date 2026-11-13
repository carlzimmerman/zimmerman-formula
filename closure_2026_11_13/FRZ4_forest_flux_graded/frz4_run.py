#!/usr/bin/env python3
"""FRZ4 (FROZEN_CRITERIA.md 199d710a9a): flux-level forest fields with the rare haloes realised bin by bin.
Built from SRF1's srf1_run.py (closure_2026_11_12/SRF1_settled_radius_flux_window, commit f9c71956d9): the painting loop and
the flux job are SRF1's, and FRZ3R's frz3r_core.py is imported read-only (gas, FGPA, saturation, mean flux, P1D, P3D). The
change (criteria section 3): every rare 0.1 dex bin in the forced set gets its own box with ONE forced halo, weight E_b;
numerator and denominator are both stratified; the base box leaves the forced bins out (an all-bin path from the same
Poisson draw is kept for known answer b).
One part per (stage, z, seed, footing); one JSON per box under tmp/<part>/ (restartable); SIGTERM stops between boxes
(exit 75); exit 76 when the peak resident memory passes 12 GB (the queue restarts the process, which resumes).
Usage: nice -n 19 python3 frz4_run.py <stage> <z> <seed> <footing>     stage: primary | bracket | clustered
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, signal, resource, shutil
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); sys.path.insert(1, os.path.join(REPO, "closure_2026_11_12", "FRZ3R_blind_flux_forest_regrade"))
import frz3r_core as C
import frz4_tables as TB
C.WORKERS = 1
NW = int(os.environ.get("FRZ4_THREADS", "2"))
MEM_LIMIT = float(os.environ.get("FRZ4_MEM_GB", "12")) * 1e9
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda s, f: STOP.update(flag=True))
PARTS = os.path.join(HERE, "parts"); TMP = os.path.join(HERE, "tmp"); os.makedirs(PARTS, exist_ok=True); os.makedirs(TMP, exist_ok=True)
LBOX, NGRID = 20.0, 384
GAM = 1.5
LAM0 = 0.079 * 0.6736                                   # 79 comoving kpc (Kulkarni+15, as FRZ3R / SRF1), Mpc/h comoving
def lam_rec(z): return 0.100 * (1 + z) * 0.6736         # 100 proper kpc
def tau_eff(z): return 0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132
def Fbar(z, s=1.0): return math.exp(-s * tau_eff(z))
def beta_of(g): return 2.0 - 0.7 * (g - 1.0)
fk_ = TB.fkey
CASES = [fk_(f) for f in TB.CASES]                      # f1.00 f2.00 f3.00 finf
E_THR, CUT, NMAX, NSUB, SUBCUM = 30.0, 0.005, 32, 10, 0.8
ANCH = (2.2, 3.0, 4.4)
BR_SPECS = [("lam_x0.5", 0.5 * LAM0, GAM, 1.0, "exp"), ("lam_x2", 2 * LAM0, GAM, 1.0, "exp"), ("lam_rec", None, GAM, 1.0, "exp"),
            ("gam_1.2", LAM0, 1.2, 1.0, "exp"), ("gam_1.6", LAM0, 1.6, 1.0, "exp"), ("tau_x0.9", LAM0, GAM, 0.9, "exp"),
            ("tau_x1.1", LAM0, GAM, 1.1, "exp"), ("M1_lin", LAM0, GAM, 1.0, "lin")]

class UGrid:
    """SRF1's UGrid: FRZ3R's Grid.on_grid evaluated on the unique |k| values and gathered (identical numbers, less work)."""
    def __init__(self, grid):
        cache = os.path.join(TMP, f"ugrid_N{grid.N}.npz")
        if os.path.exists(cache):
            z = np.load(cache); self.inv, self.ti, self.tw = z["inv"], z["ti"], z["tw"]; return
        kk = grid.k.ravel(); u, inv = np.unique(kk, return_inverse=True); self.inv = inv.astype(np.int32).reshape(grid.k.shape)
        KT = C.KT; lk = np.log(np.maximum(u, 1e-30)); lt = np.log(np.maximum(KT, 1e-30))
        i = np.clip(np.searchsorted(KT, u) - 1, 0, len(KT) - 2)
        w = np.where(i == 0, u / KT[1], (lk - lt[i]) / (lt[i + 1] - lt[i]))
        self.ti = i.astype(np.int32); self.tw = np.clip(w, 0, 1).astype(np.float32)
        np.savez(cache + ".tmp.npz", inv=self.inv, ti=self.ti, tw=self.tw); os.replace(cache + ".tmp.npz", cache)
    def vals(self, Ut):
        return ((1 - self.tw) * Ut[self.ti] + self.tw * Ut[self.ti + 1]).astype(np.float32)
    def on_grid(self, Ut, scale=None):
        v = self.vals(Ut)
        if scale is not None: v = v / scale
        return np.take(v, self.inv)

def masses(z):
    SN = TB.srh1(); SN["set_z"](z); L = SN["L"]; LM = L["LM"]
    sel = (LM >= 8.0 - 1e-9) & (LM <= 15.0 + 1e-9); idx = np.nonzero(sel)[0]
    return LM[idx], L["W_M"][idx].copy(), L["BIAS"][idx].copy()

def forced_set(t):
    """criteria section 3: forced rare bins and the bracket subset (section 4)."""
    V = LBOX ** 3; bins = t["bins"]; E = bins["Wsum"] * V; rare = (E < E_THR) & (E > 0)
    ik = int(np.searchsorted(C.KT, 3.0)); UR = t["UbR"][:, ik]
    s = {k: bins["Wsum"] * ((UR + t["Ub"][k][:, ik]) ** 2 - UR ** 2) for k in CASES}
    sh = {k: s[k] / abs(s[k].sum()) for k in CASES}
    p = bins["Wsum"] * UR ** 2; psh = p / p.sum()
    mx = np.max(np.abs(np.array([sh[k] for k in CASES])), 0)
    cand = np.nonzero(rare & ((mx >= CUT) | (psh >= CUT)))[0]
    order = sorted(cand.tolist(), key=lambda i: -max(mx[i], psh[i]))
    forced = sorted(order[:NMAX]); over = sorted(order[NMAX:])
    # bracket subset: forced bins by descending max share until the cumulative share of the forced set's total >= 0.8 at every f
    byshare = sorted(forced, key=lambda i: -mx[i]); sub = []
    for i in byshare:
        if len(sub) >= NSUB: break
        sub.append(i)
        if all(abs(sum(s[k][j] for j in sub)) >= SUBCUM * abs(sum(s[k][j] for j in forced)) for k in CASES): break
    info = dict(E=E.tolist(), rare=rare.tolist(), lM_lo=bins["lM_lo"].tolist(), share={k: sh[k].tolist() for k in CASES}, ref_share=psh.tolist(),
                forced=forced, over_cap=over, subset=sorted(sub),
                forced_share={k: float(sum(sh[k][j] for j in forced)) for k in CASES},
                nonforced_rare_share={k: float(sum(sh[k][j] for j in np.nonzero(rare)[0] if j not in forced)) for k in CASES},
                common_share={k: float(sh[k][~rare & (E > 0)].sum()) for k in CASES},
                forced_ref_share=float(sum(psh[j] for j in forced)))
    return forced, sorted(sub), info

def flux_job(grid, z, fk, lam, gam=GAM, sF=1.0, mode="exp", want3d=True):
    """SRF1's flux job: FRZ3R's gas, FGPA, saturation, mean-flux match, P1D (and P3D)."""
    g = C.gas(grid, fk, lam); fl = float(np.sum(g < 1e-6)) / g.size; g = np.maximum(g, 1e-6)
    kv, p, inf = C.flux_p1d(grid, g, z, beta_of(gam), gam, Fbar(z, sF), mode=mode); del g
    out = dict(p=p.tolist(), A=inf["A"], meanF=inf["meanF"], floored=fl)
    if want3d: out["P3D"] = C.pk3d(grid, fk, nbins=40, kmin=0.3)[1].tolist()
    return kv, out

def specs_for(stage, z):
    if stage == "bracket": return [(n, (lam_rec(z) if l is None else l), g, s, m) for n, l, g, s, m in BR_SPECS]
    return [("primary", LAM0, GAM, 1.0, "exp")]

def field_keys(stage, z, seed):
    """B fields per box (beyond R): cases; f0 at the anchors seed 0 (known answer a); doubled change at z 2.2 seed 0 (M2)."""
    keys = list(CASES)
    if stage == "primary" and seed == 0 and z in ANCH: keys.append("f0.00")
    dbl = list(CASES) if (stage == "primary" and seed == 0 and abs(z - 2.2) < 1e-9) else []
    return keys, dbl

def mem_check():
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > MEM_LIMIT:
        print(f"  peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.1f} GB: exit for restart", flush=True); sys.exit(76)

def run_jobs(grid, z, jobs, res):
    with ThreadPoolExecutor(max_workers=NW) as ex:
        futs = [(fn, sp, ex.submit(lambda b=bld, s=sp: flux_job(grid, z, b(), s[1], s[2], s[3], s[4], want3d=(s[0] == "primary")))) for fn, sp, bld in jobs]
        for fn, sp, fu in futs:
            kv, o = fu.result(); res["kv"] = kv.tolist(); res["flux"].setdefault(sp[0], {})[fn] = o

def run_part(stage, z, seed, ft):
    name = os.path.join(PARTS, f"{stage}_z{z:.1f}_s{seed}_{ft}.json")
    if os.path.exists(name): print(f"{os.path.basename(name)} exists", flush=True); return
    stem = os.path.join(TMP, f"{stage}_z{z:.1f}_s{seed}_{ft}"); os.makedirs(stem, exist_ok=True)
    t0 = time.time(); T = TB.tables(z); t = T[ft]; lM, W, b = masses(z)
    grid = C.Grid(NGRID, LBOX); ug = UGrid(grid); RHO = t["RHO"]; V = LBOX ** 3; norm = RHO * grid.dx ** 3
    forced, sub, finfo = forced_set(t)
    boxes = forced if stage == "primary" else sub
    specs = specs_for(stage, z); keys, dbl = field_keys(stage, z, seed)
    clustered = stage == "clustered"
    fs_exp = 1.0 - t["Mta_sum_painted"] / RHO
    S = np.maximum(t["PRta"] - t["p1_Rb"], 1e-12)
    def T2(key): return ug.on_grid(np.sqrt(np.maximum(1.0 + t["spec"][key]["D2h"] / S, 0.0))) - 1.0
    edges = np.arange(8.0 - 1e-9, lM[-1] + 0.1, 0.1); bid = np.digitize(lM, edges) - 1
    fset = set(forced)
    # ------------------------------------------------------------ base box
    bj = os.path.join(stem, "base.json")
    if not os.path.exists(bj):
        tb = time.time()
        wk = C.white(grid, seed); dsk, Gk, linfo = C.lognormal_smooth(grid, wk, S / fs_exp ** 2); del wk
        gf = None
        if clustered:
            gf = grid.irfft(Gk * np.exp(-0.5 * (grid.k * 0.5) ** 2)).ravel().astype(np.float64)
        del Gk
        # SRF1's paint loop (FRZ3R's random stream and order), two accumulations from the same draw
        rng = np.random.default_rng(7919 + seed)
        acc_all = np.zeros(grid.k.shape, np.complex64); acc_s = np.zeros(grid.k.shape, np.complex64)
        want_all = stage == "primary"
        dkeys = list(dict.fromkeys(keys + dbl))
        acc_d = {k: np.zeros(grid.k.shape, np.complex64) for k in dkeys}
        acc_P = np.zeros(grid.k.shape, np.complex64) if want_all else None
        Mh_all = 0.0; Mh_s = 0.0; nh = 0
        for ib in range(bid.max() + 1):
            m = bid == ib; Ne_i = W[m] * V; Ne = float(Ne_i.sum())
            if Ne <= 0: continue
            n = int(rng.poisson(Ne))
            if n == 0: continue
            wts = Ne_i / Ne
            if gf is None:
                pos = rng.random((n, 3)) * grid.L
            else:
                bb = float(np.sum(wts * b[m])); lw = bb * gf; lw -= lw.max(); pp = np.exp(lw); pp /= pp.sum()
                cells = rng.choice(grid.N ** 3, size=n, p=pp)
                pos = (np.stack(np.unravel_index(cells, (grid.N,) * 3), 1) + rng.random((n, 3))) * grid.dx
            nk = grid.rfft(C.cic(grid, pos)) / grid.wcic
            Uref = t["UbR"][ib]; aR = nk * ug.on_grid(Uref, norm)
            if want_all:
                acc_all += aR; Mh_all += n * Uref[0]
                acc_P += nk * ug.on_grid(t["Ub"]["finf"][ib], norm)
            if ib not in fset:
                acc_s += aR; Mh_s += n * Uref[0]
                for key in dkeys: acc_d[key] += nk * ug.on_grid(t["Ub"][key][ib], norm)
            nh += n; del nk, aR
        res = dict(box="base", flux={}, n_halo=nh, Mh_all=Mh_all, Mh_strat=Mh_s, fs_exp=fs_exp, info=linfo)
        Rs = acc_s + fs_exp * dsk; Rs.flat[0] = 0.0
        dfull = {}
        for key in dkeys:
            dfull[key] = acc_d[key] + fs_exp * dsk * T2(key)
        del acc_d, acc_s
        jobs = []
        for sp in specs:
            jobs.append(("R", sp, lambda: Rs))
            for key in keys: jobs.append(("B|" + key, sp, (lambda key=key: _z0(Rs + dfull[key]))))
            for key in dbl: jobs.append(("D2|" + key, sp, (lambda key=key: _z0(Rs + 2.0 * dfull[key]))))
        if want_all:
            fs_all = 1.0 - Mh_all / (RHO * V); res["fs_all"] = fs_all
            Rall = acc_all + fs_all * dsk; Rall.flat[0] = 0.0
            BPall = Rall + (acc_P + fs_all * dsk * T2("finf")); BPall.flat[0] = 0.0
            sp = specs[0]; jobs.append(("Rall", sp, lambda: Rall)); jobs.append(("BPall|finf", sp, lambda: BPall))
        del acc_all, acc_P
        run_jobs(grid, z, jobs, res)
        res["k3d"] = C.pk3d(grid, Rs, nbins=40, kmin=0.3)[0].tolist()
        np.save(os.path.join(stem, "Rs.npy"), Rs)
        if gf is not None: np.save(os.path.join(stem, "gf.npy"), gf.astype(np.float32))
        res["time_s"] = time.time() - tb
        json.dump(res, open(bj + ".tmp", "w")); os.replace(bj + ".tmp", bj)
        print(f"  {stage} z {z:.1f} s{seed} {ft} base: {res['time_s']:.0f} s; forced bins {len(forced)} (boxes {len(boxes)})", flush=True)
        del dfull, dsk
        if gf is not None: del gf
        import gc; gc.collect()
        mem_check()
    # ------------------------------------------------------------ forced boxes, one halo each
    Rs = None; gf = None
    for ib in boxes:
        if STOP["flag"]: print("SIGTERM: stopped between boxes; rerun to resume", flush=True); sys.exit(75)
        fj = os.path.join(stem, f"b{ib:03d}.json")
        if os.path.exists(fj): continue
        tb = time.time()
        if Rs is None: Rs = np.load(os.path.join(stem, "Rs.npy"))
        if clustered and gf is None: gf = np.load(os.path.join(stem, "gf.npy")).astype(np.float64)
        rng = np.random.default_rng([seed, int(round(z * 10)), int(ib), 104729])
        if not clustered:
            pos = rng.random((1, 3)) * grid.L
        else:
            bb = float(t["bins"]["bias"][ib]); lw = bb * gf; lw -= lw.max(); pp = np.exp(lw); pp /= pp.sum()
            cell = rng.choice(grid.N ** 3, size=1, p=pp); del lw, pp
            pos = (np.stack(np.unravel_index(cell, (grid.N,) * 3), 1) + rng.random((1, 3))) * grid.dx
        nk = grid.rfft(C.cic(grid, pos)) / grid.wcic
        Rb = Rs + nk * ug.on_grid(t["UbR"][ib], norm); Rb.flat[0] = 0.0
        dd = {key: nk * ug.on_grid(t["Ub"][key][ib], norm) for key in dict.fromkeys(keys + dbl)}; del nk
        res = dict(box=int(ib), lM=float(t["bins"]["lM_lo"][ib]), E=float(t["bins"]["Wsum"][ib] * V), pos=pos.tolist(), flux={})
        jobs = []
        for sp in specs:
            jobs.append(("R", sp, lambda: Rb))
            for key in keys: jobs.append(("B|" + key, sp, (lambda key=key: _z0(Rb + dd[key]))))
            for key in dbl: jobs.append(("D2|" + key, sp, (lambda key=key: _z0(Rb + 2.0 * dd[key]))))
        run_jobs(grid, z, jobs, res); del Rb, dd
        res["time_s"] = time.time() - tb
        json.dump(res, open(fj + ".tmp", "w")); os.replace(fj + ".tmp", fj)
        print(f"  {stage} z {z:.1f} s{seed} {ft} box {ib} (log M {res['lM']:.1f}, E {res['E']:.3g}): {res['time_s']:.0f} s", flush=True)
        mem_check()
    # ------------------------------------------------------------ merge
    out = dict(stage=stage, z=z, seed=seed, footing=ft, N=NGRID, L=LBOX, dv=C.dv_cell(grid, z), forced_info=finfo, boxes=boxes,
               note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
    base = json.load(open(bj)); out["base"] = base; out["kv"] = base["kv"]; out["k3d"] = base["k3d"]
    out["forced_boxes"] = {str(ib): json.load(open(os.path.join(stem, f"b{ib:03d}.json"))) for ib in boxes}
    out["time_s"] = base["time_s"] + sum(v["time_s"] for v in out["forced_boxes"].values())
    json.dump(out, open(name + ".tmp", "w")); os.replace(name + ".tmp", name)
    shutil.rmtree(stem)
    print(f"{stage} z {z:.1f} s{seed} {ft}: {out['time_s']:.0f} s in boxes ({len(boxes)} forced); wall {time.time() - t0:.0f} s this process", flush=True)

def _z0(fk):
    fk.flat[0] = 0.0; return fk

if __name__ == "__main__":
    st, z, seed, ft = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    assert st in ("primary", "bracket", "clustered") and ft in TB.FOOTS
    run_part(st, z, seed, ft)
