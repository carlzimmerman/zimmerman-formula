#!/usr/bin/env python3
"""FRZ3R driver: one part file per (stage, z, seed, footing). Restartable: existing parts are skipped; SIGTERM exits 75
after the current part (no partial part is written). Usage: nice -n 19 python3 frz3r_run.py <stage> [z ...]
stage: anchor | other | res (N 256) | clustered.  kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import frz3r_core as C

STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda s, f: STOP.update(flag=True))
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOTS = ("canonical", "alt")
LBOX = 20.0
GAM, BETA = 1.5, 2.0 - 0.7 * 0.5            # gamma 1.5 -> beta 1.65
LAM0 = 0.079 * 0.6736                        # 79 comoving kpc (Kulkarni+15) in Mpc/h, held in comoving units
def lam_rec(z): return 0.100 * (1 + z) * 0.6736   # record stage16: 100 proper kpc
def tau_eff(z): return 0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132
def Fbar(z, s=1.0): return math.exp(-s * tau_eff(z))
def beta_of(g): return 2.0 - 0.7 * (g - 1.0)

def tables(z):
    f = os.path.join(PARTS, f"tables_z{z:.1f}.npz")
    if os.path.exists(f):
        d = np.load(f, allow_pickle=True); return d["T"].item()
    T = {}
    for ft in FOOTS:
        t = C.hm_tables(z, ft)
        PSR, D2, D1 = C.frz1_curves_on_KT(z, ft)
        t = C.prepare(t, PSR); t["D2h_KT"] = D2; t["D1h_KT"] = D1
        t.pop("Plin_fn")
        T[ft] = t
    np.savez(f, T=np.array(T, dtype=object)); return T

def run_part(stage, z, seed, ft, N, T):
    name = os.path.join(PARTS, f"{stage}_z{z:.1f}_s{seed}_{ft}_N{N}.json")
    if os.path.exists(name): return
    t0 = time.time(); tab = T[ft]
    ns = C.frz1(); ns["set_z"](z); D = ns["S"]["D"]; L = ns["L"]
    tab["Plin_fn"] = (lambda k, D=D: L["P_lin"](k) * D * D)
    grid = C.Grid(N, LBOX)
    clustered = stage == "clustered"
    anchor = stage == "anchor"
    which = ("R", "BM", "BP", "BM2", "BM0") if anchor else ("R", "BM")
    FK, Gk, info = C.build_fields(grid, tab, seed, clustered=clustered, which=which)
    res = dict(stage=stage, z=z, seed=seed, footing=ft, N=N, L=LBOX, info=info, dv=C.dv_cell(grid, z))
    # matter level: 3D power of the unsmoothed fields
    kc, PR = C.pk3d(grid, FK["R"], nbins=40, kmin=0.3)
    res["P3D"] = dict(k=kc.tolist(), R=PR.tolist())
    for w in FK:
        if w != "R": res["P3D"][w] = C.pk3d(grid, FK[w], nbins=40, kmin=0.3)[1].tolist()
    FL = {}
    def floor(rho, tag):
        n = int(np.sum(rho < 1e-6)); res.setdefault("floored", {})[tag] = n / rho.size
        return np.maximum(rho, 1e-6)
    def flux(tag, w, lam, gam=GAM, sF=1.0, vlos=None, mode="exp", broaden=True):
        rho = floor(C.gas(grid, FK[w], lam), f"{tag}|{w}")
        kv, p, inf = C.flux_p1d(grid, rho, z, beta_of(gam) if mode != "thin" else 1.0, gam, Fbar(z, sF), broaden=broaden, vlos=vlos, mode=mode)
        FL.setdefault(tag, {})[w] = dict(p=p.tolist(), **inf); res["kv"] = kv.tolist()
        return rho
    # gas-skewer 1D power (unsmoothed matter along LOS for known answer c; smoothed gas reported)
    def gas1d(tag, w, lam):
        rho = np.maximum(C.gas(grid, FK[w], lam), 1e-6)          # same floor as the flux step
        kv, p = C.p1d(grid, z, rho / rho.mean(dtype=np.float64) - 1.0); res.setdefault("gas1d", {}).setdefault(tag, {})[w] = p.tolist()
    flist = ["R", "BM"] + (["BP"] if anchor else [])
    for w in flist:
        flux("primary", w, LAM0)
        gas1d("gas_primary", w, LAM0)
    if anchor:
        for w in ("R", "BM"):
            flux("M1_lin", w, LAM0, mode="lin")
            flux("lam_x0.5", w, 0.5 * LAM0); flux("lam_x2", w, 2.0 * LAM0); flux("lam_rec", w, lam_rec(z))
            flux("gam_1.2", w, LAM0, gam=1.2); flux("gam_1.6", w, LAM0, gam=1.6)
            flux("Fbar_tau_x0.9", w, LAM0, sF=0.9); flux("Fbar_tau_x1.1", w, LAM0, sF=1.1)
        flux("M2_doubled", "BM2", LAM0); flux("KA_a_zero", "BM0", LAM0)
        if seed == 0:
            for w in ("R", "BM"):
                flux("KA_c_thin", w, 0.0, mode="thin", broaden=False); gas1d("matter_los", w, 0.0)
        if seed in (0, 1):
            v = C.los_velocity(grid, Gk, z, None)
            for w in ("R", "BM"): flux("vel", w, LAM0, vlos=v)
    res["flux"] = FL; res["time_s"] = time.time() - t0
    res["note"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
    tmp = name + ".tmp"; json.dump(res, open(tmp, "w")); os.replace(tmp, name)
    print(f"{stage} z {z:.1f} seed {seed} {ft} N {N}: {res['time_s']:.0f} s; fs {info['fs']:.4f} halos {info['n_halo']}", flush=True)

if __name__ == "__main__":
    stage = sys.argv[1]; zs = [float(x) for x in sys.argv[2:]]
    seeds = {"anchor": (0, 1, 2, 3), "other": (0, 1), "res": (0, 1), "clustered": (0, 1)}[stage]
    N = 256 if stage == "res" else 384
    for z in zs:
        T = tables(z)
        for seed in seeds:
            for ft in FOOTS:
                if STOP["flag"]: print("SIGTERM: stopped between parts; rerun to resume", flush=True); sys.exit(75)
                run_part(stage, z, seed, ft, N, T)
    open(os.path.join(PARTS, f"done_{stage}_" + "_".join(f"{z:.1f}" for z in zs)), "w").write("done\n")
