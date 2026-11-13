#!/usr/bin/env python3
"""FRZ3R reading T (AMENDMENT_A1, 5f39677e97; reported, never the frozen label): the turnaround-scope halo model realised on
its own terms. Reference haloes U_Rb, form-B haloes U_B (same uniform Poisson positions), smooth lognormal with target power
P_Rb,ta - one-halo(U_Rb), FRZ1's two-halo difference on the smooth component. Restartable by part; SIGTERM stops between parts.
Usage: nice -n 19 python3 frz3r_turn.py      kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import frz3r_core as C
import frz3r_run as R

STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda s, f: STOP.update(flag=True))
PARTS = R.PARTS

def turn_curves(z, foot):
    """FRZ1's turnaround-scope spectra of Rb and B on KT (whole mass grid)."""
    ns = C.frz1(); L = ns["L"]; ns["set_z"](z); layout = ns["layout"]; KKs = L["KK"]
    L["KK"] = C.KT[1:].copy(); L["PL"] = L["P_lin"](L["KK"]) * ns["S"]["D"] ** 2
    try:
        UB, _ = L["U_set"](lambda hb: layout(hb, foot, mode="B")); PB, _, _ = L["spectra_ta"](UB)
        UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    finally:
        L["KK"] = KKs; L["PL"] = L["P_lin"](KKs) * ns["S"]["D"] ** 2
    pad = lambda a: np.concatenate([[a[0]], a])
    return pad(PR), pad(PB)

def ttables(z):
    f = os.path.join(PARTS, f"turn_tables_z{z:.1f}.npz")
    if os.path.exists(f): return np.load(f, allow_pickle=True)["T"].item()
    T = R.tables(z); out = {}
    for ft in R.FOOTS:
        t = dict(T[ft]); U = t["U"]
        PR, PB = turn_curves(z, ft)
        t["ref"] = U["Rb"]; t["dU"] = U["B"] - U["Rb"]; t["PRta_KT"] = PR; t["PBta_KT"] = PB
        t["p1_Rb"] = np.sum(t["W"][:, None] * (U["Rb"] / t["RHO"]) ** 2, 0)
        t["Mta"] = U["Rb"][:, 0].copy()
        out[ft] = t
    np.savez(f, T=np.array(out, dtype=object)); return out

def build(grid, tab, seed):
    V = grid.L ** 3; RHO = tab["RHO"]
    wk = C.white(grid, seed)
    fs_exp = 1.0 - float(np.sum(tab["W"] * tab["Mta"])) / RHO
    S = np.maximum(tab["PRta_KT"] - tab["p1_Rb"], 1e-12)
    dsk, Gk, linfo = C.lognormal_smooth(grid, wk, S / fs_exp ** 2); del wk
    acc, Mh, nh = C.halo_parts(grid, tab, seed, ["ref", "dU"])
    fs = 1.0 - Mh / (RHO * V)
    T2m1 = grid.on_grid(np.sqrt(np.maximum(1.0 + tab["D2h_KT"] / S, 0.0))) - 1.0
    base = acc["ref"] + fs * dsk; dB = acc["dU"] + fs * dsk * T2m1; del acc
    out = {"R": base, "B": base + dB, "B2": base + 2.0 * dB, "B0": base + 0.0 * dB}
    for v in out.values(): v.flat[0] = 0.0
    return out, dict(fs=fs, fs_exp=fs_exp, n_halo=nh, **linfo)

def run_part(z, seed, ft, T, N=384):
    name = os.path.join(PARTS, f"turn_z{z:.1f}_s{seed}_{ft}_N{N}.json")
    if os.path.exists(name): return
    t0 = time.time(); tab = T[ft]
    ns = C.frz1(); ns["set_z"](z); D = ns["S"]["D"]; L = ns["L"]; tab["Plin_fn"] = (lambda k, D=D: L["P_lin"](k) * D * D)
    grid = C.Grid(N, R.LBOX); anchor = z in (2.2, 3.0, 4.4)
    FK, info = build(grid, tab, seed)
    res = dict(stage="turn", z=z, seed=seed, footing=ft, N=N, L=R.LBOX, info=info, dv=C.dv_cell(grid, z))
    kc, PR = C.pk3d(grid, FK["R"], nbins=40, kmin=0.3); res["P3D"] = dict(k=kc.tolist(), R=PR.tolist(), B=C.pk3d(grid, FK["B"], nbins=40, kmin=0.3)[1].tolist())
    res["expected_ratio_KT"] = dict(k=C.KT[1:].tolist(), R=(tab["PBta_KT"][1:] / tab["PRta_KT"][1:]).tolist())
    FL = {}
    def flux(tag, w, lam, gam=R.GAM, sF=1.0, mode="exp", broaden=True):
        rho = C.gas(grid, FK[w], lam); n = int(np.sum(rho < 1e-6)); res.setdefault("floored", {})[f"{tag}|{w}"] = n / rho.size
        rho = np.maximum(rho, 1e-6)
        kv, p, inf = C.flux_p1d(grid, rho, z, R.beta_of(gam) if mode != "thin" else 1.0, gam, R.Fbar(z, sF), broaden=broaden, mode=mode)
        FL.setdefault(tag, {})[w] = dict(p=p.tolist(), **inf); res["kv"] = kv.tolist()
    def gas1d(tag, w, lam):
        rho = np.maximum(C.gas(grid, FK[w], lam), 1e-6)
        kv, p = C.p1d(grid, z, rho / rho.mean(dtype=np.float64) - 1.0); res.setdefault("gas1d", {}).setdefault(tag, {})[w] = p.tolist()
    for w in ("R", "B"):
        flux("primary", w, R.LAM0); gas1d("gas_primary", w, R.LAM0)
    if anchor:
        for w in ("R", "B"): flux("M1_lin", w, R.LAM0, mode="lin")
        flux("M2_doubled", "B2", R.LAM0); flux("KA_a_zero", "B0", R.LAM0)
        if seed == 0:
            for w in ("R", "B"): flux("KA_c_thin", w, 0.0, mode="thin", broaden=False); gas1d("matter_los", w, 0.0)
        if seed in (0, 1):
            for w in ("R", "B"):
                flux("lam_x0.5", w, 0.5 * R.LAM0); flux("lam_x2", w, 2.0 * R.LAM0); flux("lam_rec", w, R.lam_rec(z))
    res["flux"] = FL; res["time_s"] = time.time() - t0; res["note"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
    tmp = name + ".tmp"; json.dump(res, open(tmp, "w")); os.replace(tmp, name)
    print(f"turn z {z:.1f} seed {seed} {ft}: {res['time_s']:.0f} s; fs {info['fs']:.4f} halos {info['n_halo']}", flush=True)

if __name__ == "__main__":
    ZB = [round(2.2 + 0.2 * i, 1) for i in range(12)]
    plan = [(z, s) for s in (0, 1) for z in (2.2, 3.0, 4.4)] + [(z, s) for s in (0, 1) for z in ZB if z not in (2.2, 3.0, 4.4)] \
         + [(z, s) for s in (2, 3) for z in (2.2, 3.0, 4.4)]
    cache = {}
    for z, s in plan:
        if z not in cache: cache = {z: ttables(z)}
        for ft in R.FOOTS:
            if STOP["flag"]: print("SIGTERM: stopped between parts; rerun to resume", flush=True); sys.exit(75)
            run_part(z, s, ft, cache[z])
    open(os.path.join(PARTS, "done_turn"), "w").write("done\n")
