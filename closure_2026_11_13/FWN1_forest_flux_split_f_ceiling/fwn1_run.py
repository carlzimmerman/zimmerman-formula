#!/usr/bin/env python3
"""FWN1 (FROZEN_CRITERIA.md fab8a8ee0e, sections 2 and 10): COPY of FRZ6's frz6_run.py (closure_2026_11_13/
FRZ6_forest_flux_candidate_graded) with this lane's field plan: stages inf (pass 1: R, Sinf, twin fields), fin (pass 2:
S5.00, S10.00, twin fields, base R for identity; S3.00 control at seeds 0, 1), oz (other z bins, seed 0), bracketF and
clusteredF (the new S subset). T1 doubles the change in EVERY box (D2| fields in base and forced boxes). The forced set,
base box, random streams, flux job and estimator are FRZ6's (= FRZ4's) unchanged, so R reproduces FRZ6 (known answer i).
Usage: nice -n 19 python3 -I -B fwn1_run.py <stage> <z> <seed> <footing>
FRZ6's docstring follows.
FRZ6 (FROZEN_CRITERIA.md, section 2): COPY of FRZ4's frz4_run.py (closure_2026_11_13/FRZ4_forest_flux_graded) with fields added:
the crossing-speed split cases S1.25 / S2.00 / S3.00 (tables from frz6_tables.py), the base-box twins T1 (doubled change) and
T2 (saturation removed), the measured-range lambda_P specs, and the S bracket subset. The forced set, the base box, the forced
boxes, the random streams and the estimator are FRZ4's, so every FRZ4 part is reproduced (known answer i).
Stages: sprim (R + S fields in forced boxes; base box carries every field; with --whole also U and C in forced boxes),
full (z 2.2 seeds >= 2: R + U + C + S everywhere), bracketS, clusteredS (S subset), mrU (FRZ4's subset, measured-range specs).
Usage: nice -n 19 python3 -I -B frz6_run.py <stage> <z> <seed> <footing> [--whole]
FRZ4's docstring follows.
FRZ4 (FROZEN_CRITERIA.md 199d710a9a): flux-level forest fields with the rare haloes realised bin by bin.
Built from SRF1's srf1_run.py (closure_2026_11_12/SRF1_settled_radius_flux_window, commit f9c71956d9): the painting loop and
the flux job are SRF1's, and FRZ3R's frz3r_core.py is imported read-only (gas, FGPA, saturation, mean flux, P1D, P3D). The
change (criteria section 3): every rare 0.1 dex bin in the forced set gets its own box with ONE forced halo, weight E_b;
numerator and denominator are both stratified; the base box leaves the forced bins out (an all-bin path from the same
Poisson draw is kept for known answer b).
One part per (stage, z, seed, footing); one JSON per box under tmp/<part>/ (restartable); SIGTERM stops between boxes
(exit 75); exit 76 when the peak resident memory passes 12 GB (the queue restarts the process, which resumes).
FRZ4 usage was: frz4_run.py <stage> <z> <seed> <footing>     stage: primary | bracket | clustered
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
import fwn1_tables as TB
C.WORKERS = 1
NW = int(os.environ.get("FWN1_THREADS", "3"))
MEM_LIMIT = float(os.environ.get("FWN1_MEM_GB", "16")) * 1e9
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
CASES = [fk_(f) for f in TB.CASES]                      # f1.00 f2.00 f3.00 finf (U and C; FRZ4's forced-set rule)
SCASES = ["S5.00", "S10.00", "Sinf"]                      # FWN1 cases (criteria section 1)
CTRL = "S3.00"                                            # control j1 (z 2.2 seeds 0, 1)
def ckpc(x): return x * 1e-3 * 0.6736                     # comoving kpc -> Mpc/h, as LAM0
MR_SPECS = {"lam_mr_lo": ckpc(91.4), "lam_mr_mid": ckpc(113.8), "lam_mr_hi": ckpc(138.6)}   # Rorai+17 Table S2, z 3 (PROVISIONAL)
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
    # FRZ6: the S cases' shares (reported) and the S bracket subset (criteria section 7: FRZ4's rule with the S cases)
    sS = {k: bins["Wsum"] * ((UR + t["Ub"][k][:, ik]) ** 2 - UR ** 2) for k in SCASES}
    shS = {k: sS[k] / abs(sS[k].sum()) if abs(sS[k].sum()) > 0 else sS[k] * 0 for k in SCASES}
    mxS = np.max(np.abs(np.array([shS[k] for k in SCASES])), 0)
    subS = []
    for i in sorted(forced, key=lambda i: -mxS[i]):
        if len(subS) >= NSUB: break
        subS.append(i)
        if all(abs(sum(sS[k][j] for j in subS)) >= SUBCUM * abs(sum(sS[k][j] for j in forced)) for k in SCASES): break
    info_S = dict(share_S={k: shS[k].tolist() for k in SCASES}, subset_S=sorted(subS),
                  forced_share_S={k: float(sum(shS[k][j] for j in forced)) for k in SCASES},
                  nonforced_rare_share_S={k: float(sum(shS[k][j] for j in np.nonzero(rare)[0] if j not in forced)) for k in SCASES},
                  common_share_S={k: float(shS[k][~rare & (E > 0)].sum()) for k in SCASES},
                  frac_above=t["bins"]["frac_above"].tolist(), n_above=int(t["n_above"]), n_grid=int(t["n_grid"]), vstar=float(t["vstar"]))
    info = dict(E=E.tolist(), rare=rare.tolist(), lM_lo=bins["lM_lo"].tolist(), share={k: sh[k].tolist() for k in CASES}, ref_share=psh.tolist(),
                forced=forced, over_cap=over, subset=sorted(sub), **info_S,
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


PRIMARY = ("primary", LAM0, GAM, 1.0, "exp")
M1SPEC = ("M1_lin", LAM0, GAM, 1.0, "lin")
def spec_list(names, z):
    d = {n: (n, (lam_rec(z) if l is None else l), g, s, m) for n, l, g, s, m in BR_SPECS}   # FRZ4's specs_for: lam_rec(z) for None
    for n, l in MR_SPECS.items(): d[n] = (n, l, GAM, 1.0, "exp")
    return [d[n] for n in names]

def plan(stage, z, seed, whole):
    """FWN1 field plan (criteria section 10): per spec, the fields of the base box and of each forced box.
    Field = (name, key, mult); key None = R."""
    z22 = abs(z - 2.2) < 1e-9
    f0 = ["f0.00"] if (stage in ("inf", "oz") and seed == 0 and z in ANCH) else []
    def flds(keys, dbl=(), R=True):
        return ([("R", None, 0.0)] if R else []) + [("B|" + k, k, 1.0) for k in keys] + [("D2|" + k, k, 2.0) for k in dbl]
    if stage == "inf":
        assert z22
        base = [(PRIMARY, flds(["Sinf"] + f0, ["Sinf"])), (M1SPEC, flds(["Sinf"]))]
        return dict(base=base, box=[(PRIMARY, flds(["Sinf"] + f0, ["Sinf"]))], which="forced", clustered=False)
    if stage == "fin":
        assert z22
        ks = ["S5.00", "S10.00"] + ([CTRL] if seed in (0, 1) else [])
        base = [(PRIMARY, flds(ks, ["S5.00", "S10.00"])), (M1SPEC, flds(["S5.00", "S10.00"]))]
        return dict(base=base, box=[(PRIMARY, flds(ks, ["S5.00", "S10.00"], R=False))], which="forced", clustered=False)
    if stage == "oz":
        assert not z22
        return dict(base=[(PRIMARY, flds(SCASES + f0))], box=[(PRIMARY, flds(SCASES + f0))], which="forced", clustered=False)
    if stage == "bracketF":
        sp = spec_list([n for n, *_ in BR_SPECS] + ["lam_mr_lo", "lam_mr_hi"], z)
        return dict(base=[(s_, flds(SCASES)) for s_ in sp], box=[(s_, flds(SCASES)) for s_ in sp], which="subset_S", clustered=False)
    if stage == "clusteredF":
        return dict(base=[(PRIMARY, flds(SCASES))], box=[(PRIMARY, flds(SCASES))], which="subset_S", clustered=True)
    raise ValueError(stage)

def mem_check():
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > MEM_LIMIT:
        print(f"  peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.1f} GB: exit for restart", flush=True); sys.exit(76)

# ------------------------------------------------------------ physical-footprint guard (added 2026-11-13 ~21:40 EST on the
# lead's operational instruction after the 21:17 swap event; no criterion changes): after EVERY flux job the process's current
# physical footprint (macOS proc_pid_rusage, ri_phys_footprint) is read; above FWN1_FOOT_GB (14 GB) the process exits 76 at once
# (os._exit; the box's JSON is written only when the box is complete, so nothing partial is kept) and the runner restarts it.
# A box that has forced two such exits is then run with one flux thread, so a restart cannot loop. Numbers are unchanged: each
# flux job is deterministic and independent of the thread count.
import ctypes
FOOT_LIMIT = float(os.environ.get("FWN1_FOOT_GB", "14")) * 1e9
class _RU(ctypes.Structure):
    _fields_ = [("ri_uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in (
        "ri_user_time", "ri_system_time", "ri_pkg_idle_wkups", "ri_interrupt_wkups", "ri_pageins", "ri_wired_size",
        "ri_resident_size", "ri_phys_footprint", "ri_proc_start_abstime", "ri_proc_exit_abstime")]
try:
    _libproc = ctypes.CDLL("/usr/lib/libproc.dylib")
except OSError:
    _libproc = None
def footprint():
    if _libproc is None: return 0.0
    ru = _RU()
    if _libproc.proc_pid_rusage(os.getpid(), 0, ctypes.byref(ru)) != 0: return 0.0
    return float(ru.ri_phys_footprint)
def _restart_file(stem, label): return os.path.join(stem, f"footprint_exits_{label}.txt")
def run_jobs(grid, z, jobs, res, stem=None, label=None):
    nw = NW
    if stem is not None and os.path.exists(_restart_file(stem, label)) and int(open(_restart_file(stem, label)).read() or 0) >= 2: nw = 1
    with ThreadPoolExecutor(max_workers=nw) as ex:
        futs = [(fn, sp, ex.submit(lambda b=bld, s=sp: flux_job(grid, z, b(), s[1], s[2], s[3], s[4], want3d=(s[0] == "primary")))) for fn, sp, bld in jobs]
        for fn, sp, fu in futs:
            kv, o = fu.result(); res["kv"] = kv.tolist(); res["flux"].setdefault(sp[0], {})[fn] = o
            fp = footprint()
            if fp > FOOT_LIMIT:
                if stem is not None:
                    rf = _restart_file(stem, label); n = int(open(rf).read() or 0) if os.path.exists(rf) else 0
                    open(rf, "w").write(str(n + 1))
                print(f"  physical footprint {fp / 1e9:.1f} GB in {label} ({nw} threads): exit for restart", flush=True)
                sys.stdout.flush(); os._exit(76)

def make_jobs(pl, Rx, dd):
    jobs = []
    for sp, fl in pl:
        for name, key, mult in fl:
            if key is None: jobs.append((name, sp, lambda: Rx))
            else: jobs.append((name, sp, (lambda key=key, mult=mult: _z0(Rx + mult * dd[key]))))
    return jobs

def run_part(stage, z, seed, ft, whole=False):
    tag = f"{stage}_z{z:.1f}_s{seed}_{ft}" + ("_whole" if whole else "")
    name = os.path.join(PARTS, tag + ".json")
    if os.path.exists(name): print(f"{os.path.basename(name)} exists", flush=True); return
    stem = os.path.join(TMP, tag); os.makedirs(stem, exist_ok=True)
    t0 = time.time(); T = TB.tables(z); t = T[ft]; lM, W, b = masses(z)
    grid = C.Grid(NGRID, LBOX); ug = UGrid(grid); RHO = t["RHO"]; V = LBOX ** 3; norm = RHO * grid.dx ** 3
    forced, sub, finfo = forced_set(t)
    PL = plan(stage, z, seed, whole)
    boxes = {"forced": forced, "subset": sub, "subset_S": finfo["subset_S"]}[PL["which"]]
    clustered = PL["clustered"]
    bkeys = list(dict.fromkeys(k for _, fl in PL["base"] for _, k, _ in fl if k is not None))
    xkeys = list(dict.fromkeys(k for _, fl in PL["box"] for _, k, _ in fl if k is not None))
    fs_exp = 1.0 - t["Mta_sum_painted"] / RHO
    S = np.maximum(t["PRta"] - t["p1_Rb"], 1e-12)
    def T2(key): return ug.on_grid(np.sqrt(np.maximum(1.0 + t["spec"][key]["D2h"] / S, 0.0))) - 1.0
    edges = np.arange(8.0 - 1e-9, lM[-1] + 0.1, 0.1); bid = np.digitize(lM, edges) - 1
    fset = set(forced)
    # ------------------------------------------------------------ base box (FRZ4's paint loop and random stream)
    bj = os.path.join(stem, "base.json")
    if not os.path.exists(bj):
        tb = time.time()
        wk = C.white(grid, seed); dsk, Gk, linfo = C.lognormal_smooth(grid, wk, S / fs_exp ** 2); del wk
        gf = None
        if clustered:
            gf = grid.irfft(Gk * np.exp(-0.5 * (grid.k * 0.5) ** 2)).ravel().astype(np.float64)
        del Gk
        rng = np.random.default_rng(7919 + seed)
        acc_s = np.zeros(grid.k.shape, np.complex64)
        acc_d = {k: np.zeros(grid.k.shape, np.complex64) for k in bkeys}
        Mh_s = 0.0; nh = 0
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
            if ib not in fset:
                nk = grid.rfft(C.cic(grid, pos)) / grid.wcic
                Uref = t["UbR"][ib]; acc_s += nk * ug.on_grid(Uref, norm); Mh_s += n * Uref[0]
                for key in bkeys: acc_d[key] += nk * ug.on_grid(t["Ub"][key][ib], norm)
                del nk
            nh += n
        res = dict(box="base", flux={}, n_halo=nh, Mh_strat=Mh_s, fs_exp=fs_exp, info=linfo)
        Rs = acc_s + fs_exp * dsk; Rs.flat[0] = 0.0
        dfull = {key: acc_d[key] + fs_exp * dsk * T2(key) for key in bkeys}
        del acc_d, acc_s
        run_jobs(grid, z, make_jobs(PL["base"], Rs, dfull), res, stem, "base")
        res["k3d"] = C.pk3d(grid, Rs, nbins=40, kmin=0.3)[0].tolist()
        np.save(os.path.join(stem, "Rs.npy"), Rs)
        if gf is not None: np.save(os.path.join(stem, "gf.npy"), gf.astype(np.float32))
        res["time_s"] = time.time() - tb
        json.dump(res, open(bj + ".tmp", "w")); os.replace(bj + ".tmp", bj)
        print(f"  {tag} base: {res['time_s']:.0f} s; forced bins {len(forced)} (boxes {len(boxes)})", flush=True)
        del dfull, dsk
        if gf is not None: del gf
        import gc; gc.collect()
        mem_check()
    # ------------------------------------------------------------ forced boxes, one halo each (FRZ4's stream)
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
        dd = {key: nk * ug.on_grid(t["Ub"][key][ib], norm) for key in xkeys}; del nk
        res = dict(box=int(ib), lM=float(t["bins"]["lM_lo"][ib]), E=float(t["bins"]["Wsum"][ib] * V), pos=pos.tolist(), flux={})
        run_jobs(grid, z, make_jobs(PL["box"], Rb, dd), res, stem, f"b{ib:03d}"); del Rb, dd
        res["time_s"] = time.time() - tb
        json.dump(res, open(fj + ".tmp", "w")); os.replace(fj + ".tmp", fj)
        print(f"  {tag} box {ib} (log M {res['lM']:.1f}, E {res['E']:.3g}): {res['time_s']:.0f} s", flush=True)
        mem_check()
    # ------------------------------------------------------------ merge
    out = dict(stage=stage, z=z, seed=seed, footing=ft, whole=whole, N=NGRID, L=LBOX, dv=C.dv_cell(grid, z), forced_info=finfo, boxes=boxes,
               note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
    base = json.load(open(bj)); out["base"] = base; out["kv"] = base["kv"]; out["k3d"] = base["k3d"]
    out["forced_boxes"] = {str(ib): json.load(open(os.path.join(stem, f"b{ib:03d}.json"))) for ib in boxes}
    out["time_s"] = base["time_s"] + sum(v["time_s"] for v in out["forced_boxes"].values())
    json.dump(out, open(name + ".tmp", "w")); os.replace(name + ".tmp", name)
    shutil.rmtree(stem)
    print(f"{tag}: {out['time_s']:.0f} s in boxes ({len(boxes)}); wall {time.time() - t0:.0f} s this process", flush=True)

def _z0(fk):
    fk.flat[0] = 0.0; return fk

if __name__ == "__main__":
    st, z, seed, ft = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    assert st in ("inf", "fin", "oz", "bracketF", "clusteredF") and ft in TB.FOOTS
    run_part(st, z, seed, ft, whole="--whole" in sys.argv[5:])
