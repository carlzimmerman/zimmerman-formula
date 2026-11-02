#!/usr/bin/env python3
"""DR8 part B: LC1's disc grown in an isolated Eddington halo, same kernel, gravity only, no accretion, no Lambda term, no expansion. Preemptible: SIGTERM -> checkpoint, exit 75; --resume continues.
    python3 dr8_live.py --kind core --seed 1 --work DIR --T 7.7 [--md-mult 1 | 0] [--resume] [--stops 3.85,7.7] [--centre com|shrink]
kappa = 1/2 FITTED, unused; not theory closed."""
import argparse, importlib.util, json, math, os, signal, sys, time
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(REB, "ZK1_fast_force_kernel")); sys.path.insert(0, os.path.join(REB, "LC1_live_contraction"))
import dr8_ic as IC, lc1_disc as L
X, XA = L.X, L.XA; GYR = L.GYR; ETA = 0.2; EPS = 0.7e-3; AX = np.array([0.0, 0.0, 1.0])
def centre_com(x, r, c):
    for _ in range(5): sel = ((x - c) ** 2).sum(1) < r * r; c = x[sel].mean(0)
    return c
def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--kind"); ap.add_argument("--seed", type=int); ap.add_argument("--work"); ap.add_argument("--T", type=float, default=7.7); ap.add_argument("--Tgrow", type=float, default=7.7); ap.add_argument("--md-mult", type=float, default=1.0); ap.add_argument("--N", type=int, default=60000); ap.add_argument("--resume", action="store_true"); ap.add_argument("--ckpt-s", type=float, default=600.0); ap.add_argument("--stops", default=""); ap.add_argument("--centre", default="shrink"); ap.add_argument("--max-steps", type=int, default=0); ap.add_argument("--term-at", type=int, default=0); ap.add_argument("--zero-through", action="store_true"); ap.add_argument("--rdec", type=float, default=0.1); ap.add_argument("--log-jumps", action="store_true"); a = ap.parse_args(argv)
    os.makedirs(a.work, exist_ok=True); ck, done = os.path.join(a.work, "ckpt.npz"), os.path.join(a.work, "done.json")
    if a.resume and os.path.exists(done): print("complete", flush=True); return 0
    stop = dict(sig=None); signal.signal(signal.SIGTERM, lambda s, f: stop.update(sig=s)); signal.signal(signal.SIGINT, lambda s, f: stop.update(sig=s))
    S = IC.setup(); icf = os.path.join(a.work, "ic.npz")
    if os.path.exists(icf): Z = np.load(icf, allow_pickle=False); x0, v0, m, Msim = Z["x"], Z["v"], float(Z["m"]), float(Z["Msim"])
    else: x0, v0, m, Msim, Mod = IC.build(a.kind, S, a.N, a.seed, a.rdec); X.atomic_npz(icf, x=x0, v=v0, m=np.array(m), Msim=np.array(Msim))
    Mdf = S["Md"] * a.md_mult; dA, dB = S["Rd"], 0.2 * S["Rd"]; rc0 = S["r0"]; rcut = rc0 if a.kind == "core" else 5 * S["R2"] / S["c_nfw"]
    cen = (lambda x_, c_: centre_com(x_, rcut, c_)) if a.centre == "com" else (lambda x_, c_: XA.centre(x_, m))
    if a.resume and os.path.exists(ck): Z = np.load(ck, allow_pickle=False); x, v, t, step, c = Z["x"], Z["v"], float(Z["t"]), int(Z["step"]), Z["c"]; jumps = Z["jumps"].tolist(); print(f"resumed at step {step}, t {t:.4f}", flush=True)
    else: x, v, t, step = x0.copy(), v0.copy(), 0.0, 0; c = cen(x, np.median(x, axis=0)); jumps = []
    clk = time.time()
    def total(x_, t_, c_):
        Md = Mdf * min(t_ / a.Tgrow, 1.0); A = X.accel(x_, m * (1 - Md / Msim), EPS, 0.0)
        return (A + L.disc_acc(x_ - c_, Md, dA, dB, AX)) if (Md > 0 or a.zero_through) else A
    acc = total(x, t, c); stops = sorted(set([float(s) for s in a.stops.split(",") if s] + [a.T])); mo = dict(kind=a.kind, seed=a.seed, N=len(x), eps=EPS, Msim=Msim, Mdf=Mdf, Rd=S["Rd"], Tgrow=a.Tgrow, centre=a.centre, rdec=a.rdec)
    for ts in stops:
        snap = os.path.join(a.work, f"snap_t{ts:.2f}.npz")
        if t >= ts and os.path.exists(snap): continue
        while t < ts:
            amax = float(np.sqrt((acc * acc).sum(1)).max()); dt = min(ETA * math.sqrt(EPS / max(amax, 1e-30)) / GYR, ts - t); dts = dt * GYR
            v += 0.5 * dts * acc; x += dts * v; t += dt; step += 1
            if step % 10 == 0:
                c1 = cen(x, c); jumps.append(float(np.linalg.norm(c1 - c))); c = c1
            acc = total(x, t, c); v += 0.5 * dts * acc
            if a.term_at and step == a.term_at: stop["sig"] = 15
            if stop["sig"] is not None or time.time() - clk > a.ckpt_s:
                X.atomic_npz(ck, x=x, v=v, t=np.array(t), step=np.array(step), c=c, jumps=np.array(jumps)); clk = time.time()
                if stop["sig"] is not None: print(f"signal: checkpoint at step {step}, exit {X.YIELD_EXIT}", flush=True); return X.YIELD_EXIT
            if step % 100 == 0: print(f"step {step} t {t:.4f}/{a.T} dt {dt:.2e} wall {time.time():.0f}", flush=True)
            if a.max_steps and step >= a.max_steps:
                X.atomic_npz(os.path.join(a.work, "end.npz"), x=x, v=v, t=np.array(t), step=np.array(step), jumps=np.array(jumps), c=c); return 0
        Md = Mdf * min(t / a.Tgrow, 1.0); X.atomic_npz(snap, x=x, v=v, m=np.array(m), c=c, meta=np.array(json.dumps(dict(mo, t_snap=t, step=step, Md_now=Md, jump_rms=float(np.sqrt(np.mean(np.square(jumps)))) if jumps else 0.0, jump_max=max(jumps) if jumps else 0.0)))); print(f"snapshot t {t:.3f} step {step}", flush=True)
    X.atomic_json(done, dict(steps=step, t_end=t, N=len(x))); print(f"done {step} steps", flush=True); return 0
if __name__ == "__main__": sys.exit(main())
