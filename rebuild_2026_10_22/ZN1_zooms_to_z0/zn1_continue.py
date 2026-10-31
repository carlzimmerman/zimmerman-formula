#!/usr/bin/env python3
"""ZN1_zooms_to_z0: continue an X48 zoom from its z_f snapshot to z = 0 with X48's own accel, step rule, softening and background. X48's files are read only.
Snapshots at z = 0.5, 0.25, 0 where later than z_f. Preemptible: SIGTERM -> checkpoint, exit 75; --resume continues.
    python3 zn1_continue.py --src X48_RUN_DIR --work DIR [--resume]
    python3 zn1_continue.py --k1 X48_RUN_DIR   # K1: from X48's last checkpoint, reproduce X48's own snap_zf.npz
kappa = 1/2 FITTED; not theory closed."""
import argparse, importlib.util, json, math, os, signal, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
_sp = importlib.util.spec_from_file_location("x48_zoom", os.path.join(REB, "X48_native_cf_zoom", "x48_zoom.py")); X = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(X)
GYR = 1 / X.KMS_MPC_TO_GYR; YIELD = X.YIELD_EXIT; STOPS = (0.5, 0.25, 0.0)

def setup(C, meta):
    rf = (3 * meta["Mf"] / (4 * math.pi * 18 * math.pi ** 2 * C["rhom"] * (1 + meta["zf"]) ** 3)) ** (1 / 3)
    return rf, meta["eps_frac"] * rf, C["OL"] * C["H0"] ** 2

def advance(x, v, acc, t, step, t_stop, eta, eps, m, OLH2, on_step=None):
    """X48's loop body, unchanged."""
    while t < t_stop:
        amax = float(np.sqrt((acc * acc).sum(1)).max())
        dt = min(eta * math.sqrt(eps / max(amax, 1e-30)) / GYR, t_stop - t); dts = dt * GYR
        v += 0.5 * dts * acc; x += dts * v; acc = X.accel(x, m, eps, OLH2); v += 0.5 * dts * acc
        t += dt; step += 1
        if on_step is not None and on_step(x, v, t, step, dt): return x, v, acc, t, step, True
    return x, v, acc, t, step, False

def k1(src):
    C = X.cosmology(); Z = np.load(os.path.join(src, "ckpt.npz"), allow_pickle=False); S = np.load(os.path.join(src, "snap_zf.npz"), allow_pickle=False)
    x, v = Z["x"].copy(), Z["v"].copy(); t, step = float(Z["t"]), int(Z["step"]); meta = json.loads(str(Z["meta"])); ms = json.loads(str(S["meta"])); m = float(S["m"])
    rf, eps, OLH2 = setup(C, meta); assert abs(eps / ms["eps"] - 1) < 1e-15 and abs(rf / ms["rf_phys"] - 1) < 1e-15, "softening differs"
    n0 = step; x, v, acc, t, step, _ = advance(x, v, X.accel(x, m, eps, OLH2), t, step, ms["t_end"], meta["eta"], eps, m, OLH2)
    dx = float(np.abs(x - S["x"]).max() / np.abs(S["x"]).max()); dv = float(np.abs(v - S["v"]).max() / np.abs(S["v"]).max()); ok = dx <= 1e-12 and dv <= 1e-12 and step == ms["steps"]
    s = f"K1 {os.path.basename(src)}: from X48's checkpoint at step {n0} to step {step} (X48 {ms['steps']}): max |d| x {dx:.1e}, v {dv:.1e}: {'PASS' if ok else 'FAIL'}"; print(s, flush=True)
    open(os.path.join(HERE, "zn1_k1.out"), "a").write(s + "\n"); return 0 if ok else 1

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--src"); ap.add_argument("--work"); ap.add_argument("--resume", action="store_true"); ap.add_argument("--ckpt-s", type=float, default=600.0); ap.add_argument("--k1"); a = ap.parse_args()
    if a.k1: return k1(a.k1)
    os.makedirs(a.work, exist_ok=True); ck, done = os.path.join(a.work, "ckpt.npz"), os.path.join(a.work, "done.json")
    if a.resume and os.path.exists(done): print("complete: nothing to do", flush=True); return 0
    stop = dict(sig=None)
    def on_sig(s, f): stop["sig"] = s
    signal.signal(signal.SIGTERM, on_sig); signal.signal(signal.SIGINT, on_sig)
    C = X.cosmology(); S = np.load(os.path.join(a.src, "snap_zf.npz"), allow_pickle=False); meta = json.loads(str(S["meta"])); m = float(S["m"])
    if a.resume and os.path.exists(ck):
        Z = np.load(ck, allow_pickle=False); x, v = Z["x"], Z["v"]; t, step = float(Z["t"]), int(Z["step"]); print(f"resumed at step {step}, t {t:.4f} Gyr", flush=True)
    else:
        x, v = S["x"].copy(), S["v"].copy(); t, step = float(meta["t_end"]), int(meta["steps"]); print(json.dumps(dict(M=meta["M"], seed=meta["seed"], zf=meta["zf"], t_start=t, step_start=step, N=len(x))), flush=True)
    rf, eps, OLH2 = setup(C, meta); assert abs(eps / meta["eps"] - 1) < 1e-15, "softening differs from X48's"
    t0 = X.t_of_z(C, 0.0); acc = X.accel(x, m, eps, OLH2); clk = dict(last=time.time())
    def on_step(x_, v_, t_, step_, dt_):
        if stop["sig"] is not None or time.time() - clk["last"] > a.ckpt_s:
            X.atomic_npz(ck, x=x_, v=v_, t=np.array(t_), step=np.array(step_), meta=np.array(json.dumps(meta))); clk["last"] = time.time()
            if stop["sig"] is not None: return True
        if step_ % 200 == 0: print(f"step {step_} t {t_:.4f}/{t0:.4f} Gyr dt {dt_:.2e}", flush=True)
        return False
    for zs in STOPS:
        if zs >= meta["zf"]: continue
        ts = X.t_of_z(C, zs); snap = os.path.join(a.work, f"snap_z{zs:.2f}.npz")
        if t >= ts and os.path.exists(snap): continue
        x, v, acc, t, step, halted = advance(x, v, acc, t, step, ts, meta["eta"], eps, m, OLH2, on_step)
        if halted: print(f"signal {stop['sig']}: checkpoint at step {step}, exit {YIELD}", flush=True); return YIELD
        X.atomic_npz(snap, x=x, v=v, m=np.array(m), meta=np.array(json.dumps(dict(meta, z_snap=zs, t_snap=t, step_snap=step)))); print(f"snapshot z {zs:.2f} at step {step}, t {t:.4f} Gyr", flush=True)
    X.atomic_json(done, dict(steps=step, t_end=t, N=len(x))); print(f"done: {step} steps", flush=True); return 0

if __name__ == "__main__":
    sys.exit(main())
