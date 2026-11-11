#!/usr/bin/env python3
"""WV1 S3 production run: one spherical Schrodinger-Poisson collapse (wv1_sp_lib), with the frozen S3 diagnostics
evaluated on the full grid at each output (z = 2, 1, 0.5 and nine times spaced evenly over the last 1 Gyr).

    python3 wv1_s3.py --mass 10.7 --fac 1 --footing canonical [--law] [--dxfac 0.5 --zend 2]
writes runs/<tag>.json (metrics) and runs/<tag>.npz (compact float32 profiles). Preemptible: checkpoints every 10 min
and on SIGTERM to $WV1_CKPT (default: the system temp dir), resumes from it. One thread, under 3 GB.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, time, signal, argparse, tempfile, pickle
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wv1_sp_lib as S
L = S.L

ap = argparse.ArgumentParser()
ap.add_argument("--mass", type=float, required=True)
ap.add_argument("--fac", type=int, required=True)
ap.add_argument("--footing", required=True)
ap.add_argument("--law", action="store_true")
ap.add_argument("--dxfac", type=float, default=1.0)
ap.add_argument("--zend", type=float, default=0.0)
ap.add_argument("--mutate_static_all", action="store_true")   # not used by runs (M3 is applied in grading)
args = ap.parse_args()

KD1 = json.load(open(os.path.join(HERE, "..", "..", "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")))
S2 = json.load(open(os.path.join(HERE, "wv1_s1s2.json")))["S2"]
fo = args.footing
nu_max_fo = S2[fo]["nu_max_kpc_kms"]
nu = nu_max_fo if args.fac == 1 else S2["canonical"]["nu_max_kpc_kms"] * args.fac
V_EST = {10.7: 750.0, 9.4: 250.0}[args.mass]
X0 = {10.7: 4000.0, 9.4: 2500.0}[args.mass]
s = KD1["footings"][fo]["setting"]
cos0 = L.Cosmo(s["h"], s["omega_d"], s["omega_b"])
kJ0 = (16 * math.pi * L.G * cos0.nbar0 / nu ** 2) ** 0.25          # comoving Jeans wavenumber today (1/kpc)
x_max = max(X0, 3 * 2 * math.pi / kJ0)
dx = args.dxfac * math.pi * nu / (6 * V_EST)
tag = f"{fo}_M{args.mass}_f{args.fac}_{'law' if args.law else 'off'}" + ("" if args.dxfac == 1 and args.zend == 0 else f"_dx{args.dxfac}_z{args.zend:g}")
os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
OUTJ, OUTN = os.path.join(HERE, "runs", tag + ".json"), os.path.join(HERE, "runs", tag + ".npz")
CK = os.path.join(os.environ.get("WV1_CKPT", tempfile.gettempdir()), "wv1_ckpt")
os.makedirs(CK, exist_ok=True)
CKF = os.path.join(CK, tag + ".pkl")

run = S.Run(nu, args.mass, fo, KD1, x_max=x_max, dx=dx, law_bracket=args.law)
cos = run.cos
t0 = cos.t_of_a(1.0)
tz = lambda zz: cos.t_of_a(1.0 / (1.0 + zz))
outs = [("z2", tz(2.0))]
if args.zend == 0:
    outs += [("z1", tz(1.0)), ("z0.5", tz(0.5))]
    outs += [(f"g{i}", t0 - (1.0 / L.TU) * (1 - i / 8)) for i in range(9)]
outs.sort(key=lambda q: q[1])
t_end = outs[-1][1]
a0 = run.a0
K = 4 * math.pi * L.G
RB = np.logspace(math.log10(0.3), math.log10(run.xmax * 1.0), 401)      # physical-radius bin edges at z=0 scale (kpc)

state = {"t": run.t, "steps": 0, "hist": [], "res": {}, "sum_rho": None, "n_sum": 0, "wall": 0.0, "next_out": 0}
if os.path.exists(CKF):
    ck = pickle.load(open(CKF, "rb"))
    run.u = ck["u"]; run.t = ck["t"]; run.steps = ck["steps"]; state = ck["state"]
    print(f"[{tag}] resumed at t = {run.t:.5f} (step {run.steps})", flush=True)

STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__("flag", True))


def save_ckpt():
    state["t"] = run.t; state["steps"] = run.steps
    pickle.dump({"u": run.u, "t": run.t, "steps": run.steps, "state": state}, open(CKF + ".tmp", "wb"))
    os.replace(CKF + ".tmp", CKF)


def binned(r, w, val):
    """mass-weighted mean of val in RB bins (r physical); returns (centres, mean, mass)."""
    idx = np.digitize(r, RB) - 1
    ok = (idx >= 0) & (idx < len(RB) - 1)
    m = np.bincount(idx[ok], weights=w[ok], minlength=len(RB) - 1)
    mv = np.bincount(idx[ok], weights=(w * val)[ok], minlength=len(RB) - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.sqrt(RB[1:] * RB[:-1]), np.where(m > 0, mv / m, np.nan), m


def diagnostics(label):
    D = run.diag()
    r, rho, v, gin, A, au = D["r"], D["rho"], D["v"], D["gin"], D["A"], D["au"]
    a = D["a"]
    x, dxg = run.x, run.dx
    w = rho * r ** 2 * a * dxg                            # shell mass / 4 pi (physical)
    out = {"label": label, "z": D["z"], "t_Gyr": D["t"] * L.TU, "a": a}
    # fold-free: local maxima of the comoving density with FWHM < 4 cells
    dens = au ** 2 / x ** 2
    im = np.where((dens[1:-1] > dens[:-2]) & (dens[1:-1] >= dens[2:]))[0] + 1
    narrow = 0
    for i in im:
        h = 0.5 * dens[i]; wl = 0; wr = 0
        while wl < 4 and i - wl - 1 >= 0 and dens[i - wl - 1] >= h: wl += 1
        while wr < 4 and i + wr + 1 < len(dens) and dens[i + wr + 1] >= h: wr += 1
        if wl + wr + 1 < 4: narrow += 1
    out["n_maxima"] = int(len(im)); out["n_narrow_maxima"] = int(narrow)
    out["max_density_over_bar"] = float(dens.max() / run.rbar)
    out["central_over_bar"] = float(np.mean(dens[:3]) / run.rbar)
    Wk = S.dst1(run.u - run.bg)
    pw = np.abs(Wk) ** 2
    out["nyquist_top10pc_power_frac"] = float(pw[int(0.9 * len(pw)):].sum() / max(pw.sum(), 1e-300))
    # turnaround radius from mass-weighted radial velocity in bins
    rc_, vb, mb = binned(r, w, v)
    neg = np.where((vb < 0) & (mb > 0))[0]
    if len(neg):
        j = neg[-1]
        out["r_ta"] = float(RB[j + 1])
    else:
        out["r_ta"] = 0.0
    # static frame test (S3(b)): |v| <= 0.1 v_c and |A - dPhi/dr| <= 0.1 |dPhi/dr|, from index 1 (x = 2 dx)
    vc = np.sqrt(np.maximum(r * gin, 0.0))
    with np.errstate(invalid="ignore"):
        mask = (gin > 0) & (np.abs(v) <= 0.1 * vc) & (np.abs(A - gin) <= 0.1 * np.abs(gin))
    bad = np.where(~mask[1:])[0]
    i_fail = (bad[0] + 1) if len(bad) else len(mask)
    out["R_s"] = float(r[i_fail - 1]) if i_fail >= 2 else 0.0
    out["static_cells_frac_inside_rta"] = float(mask[r < max(out["r_ta"], r[1])].mean()) if out["r_ta"] > 0 else float("nan")
    # S3(c): phantom charge of V1's frame from A (unscreened local law), against Psi's density
    x_ = np.abs(A) / a0
    P = np.sign(A) * (a0 / K) * x_ / (1 + x_)
    DP = np.gradient(r ** 2 * P, r) / r ** 2
    badc = DP > rho
    Pm = (a0 / K) * (gin / a0) / (1 + gin / a0) * np.sign(gin)                 # M4: A -> dPhi/dr
    DPm = np.gradient(r ** 2 * Pm, r) / r ** 2
    badm = DPm > rho
    cm = np.cumsum(w); cb = np.cumsum(w * badc); cbm = np.cumsum(w * badm)
    rq = np.sqrt(RB[1:] * RB[:-1])
    prof = {"rq": rq, "M_cum": np.interp(rq, r, cm), "Mbad_cum": np.interp(rq, r, cb), "Mbad_M4_cum": np.interp(rq, r, cbm)}
    # median |A|/a0 and |A|/gin inside r_ta (fringe report)
    inn = (r < out["r_ta"]) & (r > r[1]) if out["r_ta"] > 0 else (r < r[1])
    if inn.any():
        out["median_absA_over_a0_inside_rta"] = float(np.median(np.abs(A[inn]) / a0))
        out["median_absA_over_g_inside_rta"] = float(np.median(np.abs(A[inn]) / np.maximum(gin[inn], 1e-300)))
    # compact profiles (bins)
    _, rho_b_, _ = binned(r, w, np.ones_like(r))
    shell_vol = (4 * math.pi / 3) * (RB[1:] ** 3 - RB[:-1] ** 3)
    prof.update({"rho_bin": mb * 4 * math.pi / shell_vol, "v_bin": vb, "static_frac_bin": binned(r, np.ones_like(r), mask.astype(float))[1],
                 "badc_frac_bin": binned(r, w, badc.astype(float))[1]})
    return out, prof, rho


T_START = time.time()
last_ck = time.time()
V, d = run.V(run.t)
PROF = {}
if os.path.exists(CKF + ".prof.npz"):
    PROF = dict(np.load(CKF + ".prof.npz"))
while state["next_out"] < len(outs):
    lab, tn = outs[state["next_out"]]
    while run.t < tn - 1e-12:
        dt = min(run.choose_dt(d, 2e-3), tn - run.t)
        V, d = run.step(dt, V)
        if run.steps % 50 == 0:
            rc = float(np.mean(np.abs(run.u[:3]) ** 2 / run.x[:3] ** 2) / run.rbar)
            state["hist"].append((run.t * L.TU, rc))
        if time.time() - last_ck > 600 or STOP["flag"]:
            state["wall"] += time.time() - T_START; T_START = time.time()
            save_ckpt(); np.savez(CKF + ".prof.npz", **PROF); last_ck = time.time()
            if STOP["flag"]:
                print(f"[{tag}] SIGTERM: checkpointed at t = {run.t:.5f}", flush=True); sys.exit(3)
    o, prof, rho = diagnostics(lab)
    state["res"][lab] = o
    for kk_, vv in prof.items():
        PROF[f"{lab}__{kk_}"] = np.asarray(vv, dtype=np.float32)
    if lab.startswith("g"):
        state["sum_rho"] = rho if state["sum_rho"] is None else state["sum_rho"] + rho
        state["n_sum"] += 1
    print(f"[{tag}] {lab} z {o['z']:.3f}: r_ta {o['r_ta']:.1f} kpc, R_s {o['R_s']:.3f} kpc, max dens {o['max_density_over_bar']:.3g} x mean, "
          f"narrow maxima {o['n_narrow_maxima']}/{o['n_maxima']}, step {run.steps}", flush=True)
    state["next_out"] += 1
    save_ckpt(); np.savez(CKF + ".prof.npz", **PROF)

state["wall"] += time.time() - T_START
res = {"tag": tag, "footing": fo, "logMb": args.mass, "fac": args.fac, "nu_kpc_kms": nu, "law_bracket": args.law,
       "dxfac": args.dxfac, "zend": args.zend, "N": run.N, "dx_kpc": run.dx, "x_max_kpc": run.xmax, "steps": run.steps,
       "wall_s": round(state["wall"], 1), "outputs": state["res"]}
h = np.array(state["hist"]) if state["hist"] else np.zeros((0, 2))
if len(h):
    i = int(np.argmax(h[:, 1]))
    res["central_peak_over_bar"] = float(h[i, 1]); res["central_peak_t_Gyr"] = float(h[i, 0])
    res["central_end_over_bar"] = float(h[-1, 1])
if args.zend == 0:
    mean_rho = state["sum_rho"] / state["n_sum"]
    D = run.diag()
    rc0 = float(np.mean(mean_rho[:3]))
    below = np.where(mean_rho <= 0.5 * rc0)[0]
    res["r_c_lastGyr"] = float(D["r"][below[0]]) if len(below) else float("nan")
    res["central_density_lastGyr_Msun_kpc3"] = rc0
    rta0 = state["res"]["g8"]["r_ta"]
    res["r_ta_z0"] = rta0
    res["r_c_over_r_ta"] = res["r_c_lastGyr"] / rta0 if rta0 > 0 else float("nan")
    res["R_s_lastGyr_min"] = min(state["res"][f"g{i}"]["R_s"] for i in range(9))
    fr, frm = [], []
    for i in range(9):
        lab = f"g{i}"
        rq = PROF[f"{lab}__rq"]; M_ = np.interp(rta0, rq, PROF[f"{lab}__M_cum"]); Mb_ = np.interp(rta0, rq, PROF[f"{lab}__Mbad_cum"])
        Mbm = np.interp(rta0, rq, PROF[f"{lab}__Mbad_M4_cum"])
        fr.append(float(Mb_ / M_) if M_ > 0 else float("nan")); frm.append(float(Mbm / M_) if M_ > 0 else float("nan"))
    res["S3c_bad_mass_frac_lastGyr"] = fr; res["S3c_bad_mass_frac_max"] = max(fr)
    res["M4_bad_mass_frac_max"] = max(frm)
    res["narrow_maxima_total"] = sum(o["n_narrow_maxima"] for o in state["res"].values())
if len(h):
    PROF["hist_t_Gyr"] = h[:, 0].astype(np.float64); PROF["hist_central_over_bar"] = h[:, 1].astype(np.float64)
json.dump(res, open(OUTJ, "w"), indent=1, default=float)
np.savez_compressed(OUTN, **PROF)
for f_ in (CKF, CKF + ".prof.npz"):
    if os.path.exists(f_):
        os.remove(f_)
print(f"[{tag}] done: {run.steps} steps, {res['wall_s']} s" + (f"; R_s(last Gyr, min) {res['R_s_lastGyr_min']:.3f} kpc, r_ta {res['r_ta_z0']:.1f}, "
      f"r_c {res['r_c_lastGyr']:.3f}, S3(c) bad fraction max {res['S3c_bad_mass_frac_max']:.3f}" if args.zend == 0 else ""), flush=True)
