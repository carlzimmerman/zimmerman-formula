#!/usr/bin/env python3
"""LC1_live_contraction (FROZEN_CRITERIA.md): a Miyamoto-Nagai disc grown in a live zoom from z_f to z = 0, gravity only, with ZN1's engine. Preemptible: SIGTERM -> checkpoint, exit 75; --resume continues.
    python3 lc1_disc.py --seed 1 --work DIR [--resume] [--md-mult 2]
    python3 lc1_disc.py --checks     # K1, K2, K3
kappa = 1/2 FITTED; not theory closed."""
import argparse, importlib.util, json, math, os, signal, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REB, "ZK1_fast_force_kernel")); import x48_fast; X = x48_fast.X
_s = importlib.util.spec_from_file_location("x48_analyze", os.path.join(REB, "X48_native_cf_zoom", "x48_analyze.py")); XA = importlib.util.module_from_spec(_s); _s.loader.exec_module(XA)
GYR = 1 / X.KMS_MPC_TO_GYR; G = X.G; STOPS = (0.5, 0.25, 0.0); X48R = os.path.join(REB, "X48_native_cf_zoom", "runs"); SETUP = os.path.join(HERE, "lc1_setup.json")
def disc_acc(dx, Md, a, b, ax):
    z = dx @ ax; Rv = dx - z[:, None] * ax; R2 = (Rv * Rv).sum(1); s = np.sqrt(z * z + b * b); D2 = R2 + (a + s) ** 2; fac = G * Md / D2 ** 1.5
    return -(fac[:, None] * Rv + (fac * z * (a + s) / s)[:, None] * ax)
def disc_pot(dx, Md, a, b, ax):
    z = dx @ ax; R2 = (dx * dx).sum(1) - z * z; return -G * Md / np.sqrt(R2 + (a + np.sqrt(z * z + b * b)) ** 2)
def make_setup():
    import contextlib, io
    src = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); T = open(src).read(); NE = {"__file__": src, "__name__": "em1_ro"}; a0 = sys.argv; sys.argv = [src]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(T[:T.index("# ---------------- halo profiles")], src, "exec"), NE)
    sys.argv = a0; R1 = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))["rows"]["A_c2b_refit"]["R1"]
    Om, h, wb = 0.2976016, 0.6856427, 0.0223081; Ob = wb / h ** 2; fc = (Om - Ob) / Om; lMd = 10 + (math.log10(fc * 1e12) - R1["a"]) / R1["b"]; G_ = NE["GALS"]; lm = np.array([q["lMb"] for q in G_]); rd = np.array([q["meta"]["Rdisk"] for q in G_]); s = np.abs(lm - lMd) <= 0.2
    D = dict(lgMd=lMd, Md=10 ** lMd, Rd_kpc=float(np.median(rd[s])), n=int(s.sum()), fc=fc, a=R1["a"], b=R1["b"]); json.dump(D, open(SETUP, "w"), indent=1); return D
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int); ap.add_argument("--work"); ap.add_argument("--resume", action="store_true"); ap.add_argument("--md-mult", type=float, default=1.0); ap.add_argument("--ckpt-s", type=float, default=600.0); ap.add_argument("--checks", action="store_true"); a = ap.parse_args()
    D = json.load(open(SETUP)) if os.path.exists(SETUP) else make_setup(); C = X.cosmology(); OLH2 = C["OL"] * C["H0"] ** 2
    if a.checks: return checks(D, C, OLH2)
    os.makedirs(a.work, exist_ok=True); ck, done = os.path.join(a.work, "ckpt.npz"), os.path.join(a.work, "done.json")
    if a.resume and os.path.exists(done): print("complete: nothing to do", flush=True); return 0
    stop = dict(sig=None); signal.signal(signal.SIGTERM, lambda s, f: stop.update(sig=s)); signal.signal(signal.SIGINT, lambda s, f: stop.update(sig=s))
    S = np.load(os.path.join(X48R, f"M1e12_s{a.seed}_ng64", "snap_zf.npz"), allow_pickle=False); meta = json.loads(str(S["meta"])); m = float(S["m"]); eps = meta["eps"]; N = len(S["x"]); Msim = m * N; Md_f = D["Md"] * a.md_mult; dA, dB = D["Rd_kpc"] * 1e-3, 0.2 * D["Rd_kpc"] * 1e-3; t0 = float(meta["t_end"]); tf = X.t_of_z(C, 0.0)
    x0 = S["x"]; c0 = XA.centre(x0, m); r0_ = np.sqrt(((x0 - c0) ** 2).sum(1)); rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3; rv = XA.measure(x0, m, rho, eps)["rvir"]; sel = r0_ < 0.1 * rv; L = np.cross(x0[sel] - c0, S["v"][sel] - S["v"][sel].mean(0)).sum(0); ax = L / np.linalg.norm(L)
    if a.resume and os.path.exists(ck):
        Z = np.load(ck, allow_pickle=False); x, v = Z["x"], Z["v"]; t, step = float(Z["t"]), int(Z["step"]); print(f"resumed at step {step}, t {t:.4f} Gyr", flush=True)
    else:
        x, v = S["x"].copy(), S["v"].copy(); t, step = t0, int(meta["steps"]); print(json.dumps(dict(seed=a.seed, Md=Md_f, Rd_kpc=D["Rd_kpc"], axis=ax.tolist(), rvir_zf=rv, t0=t0, tf=tf, N=N)), flush=True)
    c = XA.centre(x, m); clk = time.time()
    def total(x_, t_, c_):
        Md = Md_f * max(0.0, (t_ - t0) / (tf - t0)); A = X.accel(x_, m * (1 - Md / Msim), eps, OLH2); return (A + disc_acc(x_ - c_, Md, dA, dB, ax)) if Md > 0 else A
    acc = total(x, t, c); mo = dict(meta, lc1=dict(Md=Md_f, Rd_kpc=D["Rd_kpc"], axis=ax.tolist(), md_mult=a.md_mult))
    for zs in STOPS:
        ts = X.t_of_z(C, zs); snap = os.path.join(a.work, f"snap_z{zs:.2f}.npz")
        if t >= ts and os.path.exists(snap): continue
        while t < ts:
            amax = float(np.sqrt((acc * acc).sum(1)).max()); dt = min(meta["eta"] * math.sqrt(eps / max(amax, 1e-30)) / GYR, ts - t); dts = dt * GYR
            v += 0.5 * dts * acc; x += dts * v; t += dt; step += 1
            if step % 10 == 0: c = XA.centre(x, m)
            acc = total(x, t, c); v += 0.5 * dts * acc
            if stop["sig"] is not None or time.time() - clk > a.ckpt_s:
                X.atomic_npz(ck, x=x, v=v, t=np.array(t), step=np.array(step), meta=np.array(json.dumps(mo))); clk = time.time()
                if stop["sig"] is not None: print(f"signal {stop['sig']}: checkpoint at step {step}, exit {X.YIELD_EXIT}", flush=True); return X.YIELD_EXIT
            if step % 200 == 0: print(f"step {step} t {t:.4f}/{tf:.4f} Gyr dt {dt:.2e}", flush=True)
        X.atomic_npz(snap, x=x, v=v, m=np.array(m), meta=np.array(json.dumps(dict(mo, z_snap=zs, t_snap=t, step_snap=step, Md_now=Md_f * (t - t0) / (tf - t0), centre=c.tolist())))); print(f"snapshot z {zs:.2f} at step {step}, t {t:.4f} Gyr", flush=True)
    X.atomic_json(done, dict(steps=step, t_end=t, N=N)); print(f"done: {step} steps", flush=True); return 0
def checks(D, C, OLH2):
    OUT = []; good = True
    def P(s): print(s, flush=True); OUT.append(s)
    P(f"LC1 setup: lg M_d {D['lgMd']:.3f} (EM1 a {D['a']}, b {D['b']}, f_c {D['fc']:.5f}), R_d {D['Rd_kpc']:.2f} kpc (median of {D['n']} SPARC galaxies)")
    S = np.load(os.path.join(X48R, "M1e13_s1_ng48", "snap_zf.npz"), allow_pickle=False); meta = json.loads(str(S["meta"])); m = float(S["m"]); eps = meta["eps"]; ax = np.array([0.0, 0.0, 1.0])
    def run(with_zero_disc):
        x, v = S["x"].copy(), S["v"].copy(); acc = X.accel(x, m, eps, OLH2)
        for _ in range(20):
            amax = float(np.sqrt((acc * acc).sum(1)).max()); dt = meta["eta"] * math.sqrt(eps / max(amax, 1e-30)) / GYR; dts = dt * GYR; v += 0.5 * dts * acc; x += dts * v; acc = X.accel(x, m, eps, OLH2)
            if with_zero_disc: acc = acc + disc_acc(x, 0.0, 3e-3, 6e-4, ax)
            v += 0.5 * dts * acc
        return x, v
    x0, v0 = run(False); x1, v1 = run(True); d = max(float(np.abs(x1 - x0).max() / np.abs(x0).max()), float(np.abs(v1 - v0).max() / np.abs(v0).max())); ok = d <= 1e-12; good &= ok; P(f"K1 M_d 0 against the engine, 20 steps: {d:.1e}: {'PASS' if ok else 'FAIL'}")
    rng = np.random.default_rng(1); dx = rng.normal(size=(1000, 3)) * 0.01; u = rng.normal(size=3); u /= np.linalg.norm(u); h = 1e-6; Md, A, B_ = 6e10, 3e-3, 6e-4; num = np.stack([-(disc_pot(dx + h * np.eye(3)[k], Md, A, B_, u) - disc_pot(dx - h * np.eye(3)[k], Md, A, B_, u)) / (2 * h) for k in range(3)], axis=1); an = disc_acc(dx, Md, A, B_, u); e = float(np.max(np.linalg.norm(an - num, axis=1) / np.linalg.norm(an, axis=1))); ok = e <= 1e-6; good &= ok; P(f"K2 analytic disc force against the potential's gradient, 1000 points: {e:.1e}: {'PASS' if ok else 'FAIL'}")
    import re as _re
    TX = open(os.path.join(REB, "X39_baryonic_contraction", "x39_contraction.py")).read(); ns = dict(np=np, SGN=1.0); exec(TX[TX.index("def contract(r, Mb, M0, F, gnedin=None):"):TX.index('P("\\n=== checks")')], ns); from scipy.optimize import brentq
    rr = np.geomspace(1e-4, 2.0, 20000); mu = lambda y: np.log1p(y) - y / (1 + y); M0 = 1e12 * mu(rr / 0.03) / mu(1 / 0.03); Mdf = 6e10; Md_ = Mdf * (1 - 3e-3 / np.sqrt(rr ** 2 + 9e-6)); F = Mdf / 1e12; Mf, _, _ = ns["contract"](rr, Md_, M0, F); own = []
    for ri, m0 in zip(rr[8000:18000:2500], M0[8000:18000:2500]):
        f = lambda lr: math.exp(lr) * (Mdf * (1 - 3e-3 / math.sqrt(math.exp(2 * lr) + 9e-6)) + m0) - ri * m0 * (1 + F); rf = math.exp(brentq(f, math.log(ri * 1e-3), math.log(ri * 2))); own.append((rf, m0))
    e = max(abs(float(np.interp(math.log(rf), np.log(rr), Mf)) / m0 - 1) for rf, m0 in own); ok = e <= 1e-5; good &= ok; P(f"K3 CN1's contract against a separate root solve, test profile: {e:.1e}: {'PASS' if ok else 'FAIL'}")
    open(os.path.join(HERE, "lc1_checks.out"), "w").write("\n".join(OUT) + "\n"); return 0 if good else 1
if __name__ == "__main__":
    sys.exit(main())
