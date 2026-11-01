#!/usr/bin/env python3
"""PZ1_disc_during_collapse (FROZEN_CRITERIA.md): LC1's disc, started at each seed's run-measured turnaround instead of z_f, from X48's initial conditions to z = 0, gravity only. Preemptible: SIGTERM -> checkpoint, exit 75; --resume continues.
    python3 pz1_disc.py --seed 1 --work DIR [--resume] [--md-mult 2]
    python3 pz1_disc.py --checks     # K1, K2, K3, K5
kappa = 1/2 FITTED, unused; not theory closed."""
import sys; sys.dont_write_bytecode = True
import argparse, importlib.util, json, math, os, shutil, signal, subprocess, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); LC1 = os.path.join(REB, "LC1_live_contraction")
_s = importlib.util.spec_from_file_location("lc1_disc", os.path.join(LC1, "lc1_disc.py")); L = importlib.util.module_from_spec(_s); _s.loader.exec_module(L)
X, XA, disc_acc = L.X, L.XA, L.disc_acc; GYR, G = L.GYR, L.G; STOPS = (0.5, 0.25, 0.0); DROP = 0.002; SETUP = os.path.join(LC1, "lc1_setup.json")

def r_T(x, T):
    d = np.sqrt(((x[T] - x[T].mean(0)) ** 2).sum(1)); return float(d.mean()), float(np.median(d))

def turnaround_loop(st, m, eps, OLH2, eta, T, t_limit, poll=None):
    """Disc-free engine (X48's loop body) until R_T has fallen DROP below its maximum; every 10 steps a sample. Hands back the stored state at the maximum. st: x, v, acc, t, step, Rb, xb, vb, tb, sb, hist. poll() -> True asks to stop and checkpoint."""
    while st["t"] < t_limit:
        amax = float(np.sqrt((st["acc"] ** 2).sum(1)).max()); dt = min(eta * math.sqrt(eps / max(amax, 1e-30)) / GYR, t_limit - st["t"]); dts = dt * GYR
        st["v"] += 0.5 * dts * st["acc"]; st["x"] += dts * st["v"]; st["acc"] = X.accel(st["x"], m, eps, OLH2); st["v"] += 0.5 * dts * st["acc"]; st["t"] += dt; st["step"] += 1
        if st["step"] % 10 == 0:
            R, Rm = r_T(st["x"], T); st["hist"].append((st["t"], R, Rm))
            if R > st["Rb"]: st.update(Rb=R, xb=st["x"].copy(), vb=st["v"].copy(), tb=st["t"], sb=st["step"])
            elif R < st["Rb"] * (1 - DROP): return "found"
        if poll is not None and poll(st): return "stop"
    return "limit"

def t_to_z(C, t):
    zz = np.concatenate([np.linspace(0, 20, 401)]); tt = np.array([X.t_of_z(C, q) for q in zz]); return float(np.interp(-t, -tt, zz))

def lc1_axis(seed):
    """LC1's axis for the seed, by LC1's rule, from X48's snap_zf."""
    S = np.load(os.path.join(L.X48R, f"M1e12_s{seed}_ng64", "snap_zf.npz"), allow_pickle=False); meta = json.loads(str(S["meta"])); m = float(S["m"]); x0 = S["x"]; c0 = XA.centre(x0, m); r0_ = np.sqrt(((x0 - c0) ** 2).sum(1)); rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3; rv = XA.measure(x0, m, rho, meta["eps"])["rvir"]; sel = r0_ < 0.1 * rv; Lv = np.cross(x0[sel] - c0, S["v"][sel] - S["v"][sel].mean(0)).sum(0); return Lv / np.linalg.norm(Lv)

def ics(C, mass, seed, ng, rs=1.5, zi=40.0, eta=0.2, eps_frac=0.01):
    """X48's main, initial block, unchanged in content."""
    q, ps, meta = X.constrained_field(C, mass, seed, ng, rs); ai = 1 / (1 + zi); Di = float(np.interp(zi, C["ZG"], C["DG"])); Hi = X.Hz(C, zi); Om_i = C["Om"] * (1 + zi) ** 3 / (C["Om"] * (1 + zi) ** 3 + C["OL"]); f_i = Om_i ** 0.55
    x = ai * (q + Di * ps); v = Hi * x + ai * Hi * f_i * Di * ps; x -= x.mean(0); v -= v.mean(0); t = X.t_of_z(C, zi); meta.update(zi=zi, t_i=t, eta=eta, eps_frac=eps_frac, seed=seed)
    rf = (3 * meta["Mf"] / (4 * math.pi * 18 * math.pi ** 2 * C["rhom"] * (1 + meta["zf"]) ** 3)) ** (1 / 3); meta.update(eps=eps_frac * rf, rf_phys=rf, t_end=X.t_of_z(C, meta["zf"])); T = np.sqrt((q * q).sum(1)) <= meta["qM"]
    return x, v, t, meta, T

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int); ap.add_argument("--work"); ap.add_argument("--resume", action="store_true"); ap.add_argument("--md-mult", type=float, default=1.0); ap.add_argument("--ckpt-s", type=float, default=600.0); ap.add_argument("--checks", action="store_true")
    ap.add_argument("--ng", type=int, default=64); ap.add_argument("--axis-z", action="store_true", help="checks only: axis z, no X48 snapshot"); ap.add_argument("--kill-at", default="", help="checks only: phase:step,... raises SIGTERM"); ap.add_argument("--stop-step", type=int, default=0, help="checks only: stop this many steps after turnaround, checkpoint"); ap.add_argument("--wall-steps", type=int, default=0, help="timing only: stop after this many steps, checkpoint, exit 0"); a = ap.parse_args()
    D = json.load(open(SETUP)); C = X.cosmology(); OLH2 = C["OL"] * C["H0"] ** 2
    if a.checks: return checks(D, C, OLH2)
    os.makedirs(a.work, exist_ok=True); ck, done, taf = os.path.join(a.work, "ckpt.npz"), os.path.join(a.work, "done.json"), os.path.join(a.work, "turnaround.json")
    if a.resume and os.path.exists(done): print("complete: nothing to do", flush=True); return 0
    stop = dict(sig=None); signal.signal(signal.SIGTERM, lambda s, f: stop.update(sig=s)); signal.signal(signal.SIGINT, lambda s, f: stop.update(sig=s)); kills = [tuple(int(q) for q in k.split(":")) for k in a.kill_at.split(",") if k]; killflag = os.path.join(a.work, "killed.json"); killed = json.load(open(killflag)) if os.path.exists(killflag) else []
    x, v, t, meta, T = ics(C, 1e12, a.seed, a.ng); m = meta["mpart"]; eps, eta = meta["eps"], meta["eta"]; N = len(x); Msim = m * N; Md_f = D["Md"] * a.md_mult; dA, dB = D["Rd_kpc"] * 1e-3, 0.2 * D["Rd_kpc"] * 1e-3; tf = X.t_of_z(C, 0.0); ax = np.array([0.0, 0.0, 1.0]) if a.axis_z else lc1_axis(a.seed)
    phase, step = 0, 0; c = None; jumps = []; jmax = 0.0; tta = None; n_steps = 0; hist = []; Rb, xb, vb, tb, sb = 0.0, x.copy(), v.copy(), t, 0
    if a.resume and os.path.exists(ck):
        Z = np.load(ck, allow_pickle=False); x, v = Z["x"], Z["v"]; t, step, phase = float(Z["t"]), int(Z["step"]), int(Z["phase"]); hist = [tuple(q) for q in Z["hist"]]; n_steps = int(Z["n_steps"])
        if phase == 0: Rb, xb, vb, tb, sb = float(Z["Rb"]), Z["xb"], Z["vb"], float(Z["tb"]), int(Z["sb"])
        else: tta, c, jmax = float(Z["tta"]), Z["c"], float(Z["jmax"]); jumps = [tuple(q) for q in Z["jumps"]]
        print(f"resumed at step {step}, phase {phase}, t {t:.4f} Gyr", flush=True)
    else: print(json.dumps(dict(seed=a.seed, Md=Md_f, Rd_kpc=D["Rd_kpc"], axis=ax.tolist(), t_i=t, t_end=meta["t_end"], tf=tf, N=N, nT=int(T.sum()))), flush=True)
    clk = time.time()
    def save(path=ck):
        arrs = dict(x=x, v=v, t=np.array(t), step=np.array(step), phase=np.array(phase), hist=np.array(hist).reshape(-1, 3), n_steps=np.array(n_steps))
        if phase == 0: arrs.update(Rb=np.array(Rb), xb=xb, vb=vb, tb=np.array(tb), sb=np.array(sb))
        else: arrs.update(tta=np.array(tta), c=c, jmax=np.array(jmax), jumps=np.array(jumps).reshape(-1, 2))
        X.atomic_npz(path, **arrs)
    def killcheck():
        k = (phase, step)
        if k in kills and list(k) not in killed: killed.append(list(k)); json.dump(killed, open(killflag, "w")); os.kill(os.getpid(), signal.SIGTERM)
    if phase == 0:
        st = dict(x=x, v=v, t=t, step=step, Rb=Rb, xb=xb, vb=vb, tb=tb, sb=sb, hist=hist, acc=X.accel(x, m, eps, OLH2))
        if step == 0: R0, Rm0 = r_T(x, T); st["Rb"] = R0; st["hist"].append((t, R0, Rm0))
        def poll(s):
            nonlocal clk, x, v, t, step, Rb, xb, vb, tb, sb, n_steps
            n_steps += 1; x, v, t, step, Rb, xb, vb, tb, sb = s["x"], s["v"], s["t"], s["step"], s["Rb"], s["xb"], s["vb"], s["tb"], s["sb"]; killcheck()
            if s["step"] % 200 == 0: print(f"phase 0 step {s['step']} t {s['t']:.4f} Gyr R_T {s['Rb']:.4f}", flush=True)
            if a.wall_steps and n_steps >= a.wall_steps: return True
            if stop["sig"] is not None or time.time() - clk > a.ckpt_s:
                save(); clk = time.time()
                if stop["sig"] is not None: return True
            return False
        r = turnaround_loop(st, m, eps, OLH2, eta, T, meta["t_end"], poll); x, v, t, step, Rb, xb, vb, tb, sb = st["x"], st["v"], st["t"], st["step"], st["Rb"], st["xb"], st["vb"], st["tb"], st["sb"]
        if r == "stop":
            if stop["sig"] is not None: print(f"signal {stop['sig']}: checkpoint at step {step}, exit {X.YIELD_EXIT}", flush=True); return X.YIELD_EXIT
            save(); return 0
        if r == "limit": print("no turnaround before z_f: not complete", flush=True); save(); return 3
        hh = np.array(hist); x, v, t, step = xb.copy(), vb.copy(), tb, sb; phase = 1; tta = tb; c = XA.centre(x, m)
        X.atomic_json(taf, dict(t_ta=tta, z_ta=t_to_z(C, tta), step_ta=sb, R_max=Rb, t_ta_median=float(hh[np.argmax(hh[:, 2]), 0]), t_f=meta["t_end"], z_f=meta["zf"], t_i=meta["t_i"], n_T=int(T.sum()), hist=hh[::5].tolist()))
        print(f"turnaround: t {tta:.4f} Gyr, z {t_to_z(C, tta):.3f}, step {sb}, R_T {Rb:.4f} Mpc; t_f {meta['t_end']:.4f}", flush=True); save(); clk = time.time()
    def Md_of(t_): return Md_f * max(0.0, (t_ - tta) / (tf - tta))
    def total(x_, t_, c_):
        Md = Md_of(t_); A = X.accel(x_, m * (1 - Md / Msim), eps, OLH2); return (A + disc_acc(x_ - c_, Md, dA, dB, ax)) if Md > 0 else A
    acc = total(x, t, c); mo = dict(meta, steps=step, lc1=dict(Md=Md_f, Rd_kpc=D["Rd_kpc"], axis=ax.tolist(), md_mult=a.md_mult), pz1=dict(t_ta=tta)); stops = [(meta["zf"], "zf")] + [(z, f"z{z:.2f}") for z in STOPS]
    for zs, tag in stops:
        ts = X.t_of_z(C, zs); snap = os.path.join(a.work, f"snap_{tag}.npz")
        if t >= ts and os.path.exists(snap): continue
        while t < ts:
            amax = float(np.sqrt((acc * acc).sum(1)).max()); dt = min(eta * math.sqrt(eps / max(amax, 1e-30)) / GYR, ts - t); dts = dt * GYR
            v += 0.5 * dts * acc; x += dts * v; t += dt; step += 1; n_steps += 1
            if step % 10 == 0:
                cn = XA.centre(x, m); j = float(np.linalg.norm(cn - c)); jmax = max(jmax, j)
                if j > dA: jumps.append((t, j))
                c = cn
            acc = total(x, t, c); v += 0.5 * dts * acc; killcheck()
            if a.stop_step and step >= json.load(open(taf))["step_ta"] + a.stop_step: save(); print(f"stop-step {step}", flush=True); return 0
            if a.wall_steps and n_steps >= a.wall_steps: save(); print(f"wall-steps {n_steps}", flush=True); return 0
            if stop["sig"] is not None or time.time() - clk > a.ckpt_s:
                save(); clk = time.time()
                if stop["sig"] is not None: print(f"signal {stop['sig']}: checkpoint at step {step}, exit {X.YIELD_EXIT}", flush=True); return X.YIELD_EXIT
            if step % 200 == 0: print(f"phase 1 step {step} t {t:.4f}/{tf:.4f} Gyr dt {dt:.2e} jmax {jmax:.2e}", flush=True)
        X.atomic_npz(snap, x=x, v=v, m=np.array(m), meta=np.array(json.dumps(dict(mo, z_snap=zs, t_snap=t, step_snap=step, Md_now=Md_of(t), centre=c.tolist(), jmax=jmax)))); print(f"snapshot {tag} at step {step}, t {t:.4f} Gyr, M_d/M_d(0) {Md_of(t) / max(Md_f, 1e-300):.3f}", flush=True)
    X.atomic_json(done, dict(steps=step, t_end=t, N=N, t_ta=tta, jmax=jmax, jumps=jumps)); print(f"done: {step} steps", flush=True); return 0

def checks(D, C, OLH2):
    OUT = []; good = True
    def P(s): print(s, flush=True); OUT.append(s)
    P("PZ1 checks; kappa = 1/2 FITTED, unused; not theory closed")
    # K1: M_d 0 through the disc's force call, from the initial conditions, against X48's unmodified main (compiled kernel)
    w = os.path.join(HERE, "cache_k1"); shutil.rmtree(w, ignore_errors=True); os.makedirs(w); av = sys.argv; sys.argv = ["x48_fast", "--mass", "1e12", "--seed", "1", "--ng", "64", "--work", w, "--max-steps", "60"]; rc = X.main(); sys.argv = av; Z = np.load(os.path.join(w, "ckpt.npz"), allow_pickle=False); assert rc == 3 and int(Z["step"]) == 60
    x, v, t, meta, T = ics(C, 1e12, 1, 64); m, eps, eta = meta["mpart"], meta["eps"], meta["eta"]; ax = np.array([0.0, 0.0, 1.0]); tA = lambda x_: X.accel(x_, m * (1 - 0.0), eps, OLH2) + disc_acc(x_, 0.0, 3.565e-3, 7.13e-4, ax); acc = tA(x)
    for _ in range(60):
        amax = float(np.sqrt((acc * acc).sum(1)).max()); dt = min(eta * math.sqrt(eps / max(amax, 1e-30)) / GYR, 1e9); dts = dt * GYR; v += 0.5 * dts * acc; x += dts * v; acc = tA(x); v += 0.5 * dts * acc; t += dt
    d = max(float(np.abs(x - Z["x"]).max() / np.abs(Z["x"]).max()), float(np.abs(v - Z["v"]).max() / np.abs(Z["v"]).max())); ok = d <= 1e-12; good &= ok; P(f"K1 M_d 0 through the disc call, 60 steps from the initial conditions, against x48_fast main: {d:.1e}: {'PASS' if ok else 'FAIL'}"); shutil.rmtree(w, ignore_errors=True)
    # K2
    rng = np.random.default_rng(1); dx = rng.normal(size=(1000, 3)) * 0.01; u = rng.normal(size=3); u /= np.linalg.norm(u); h = 1e-6; Md, A, B_ = 6e10, 3e-3, 6e-4; num = np.stack([-(L.disc_pot(dx + h * np.eye(3)[k], Md, A, B_, u) - L.disc_pot(dx - h * np.eye(3)[k], Md, A, B_, u)) / (2 * h) for k in range(3)], axis=1); an = disc_acc(dx, Md, A, B_, u); e = float(np.max(np.linalg.norm(an - num, axis=1) / np.linalg.norm(an, axis=1))); ok = e <= 1e-6; good &= ok; P(f"K2 disc force against the potential's gradient: {e:.1e}: {'PASS' if ok else 'FAIL'}")
    # K3: uniform sphere, Lambda off, against the shell ODE
    from scipy.integrate import solve_ivp
    NS = 4000; rng = np.random.default_rng(3); u = rng.normal(size=(NS, 3)); u /= np.linalg.norm(u, axis=1)[:, None]; r = rng.random(NS) ** (1 / 3); xs = u * r[:, None]; xs -= xs.mean(0); M = 1e12; ms = M / NS; H = 0.8 * math.sqrt(2 * G * M); vs = H * xs; R_ = np.sqrt((xs * xs).sum(1)); e3 = 0.005; Ts = np.ones(NS, bool)
    st = dict(x=xs.copy(), v=vs.copy(), acc=X.accel(xs, ms, e3, 0.0), t=0.0, step=0, Rb=r_T(xs, Ts)[0], xb=xs.copy(), vb=vs.copy(), tb=0.0, sb=0, hist=[])
    res = turnaround_loop(st, ms, e3, 0.0, 0.2 * 0.5, Ts, 300.0); sol = solve_ivp(lambda _t, y: [y[1], -G * M / y[0] ** 2], (0, 1), [1.0, H], events=lambda _t, y: y[1], rtol=1e-10, atol=1e-12); t_an = float(sol.t_events[0][0]) / GYR
    e = abs(st["tb"] - t_an) / t_an; rb = r_T(st["xb"], Ts)[0]; ok = res == "found" and e <= 0.02 and abs(rb - st["Rb"]) <= 1e-12 * rb; good &= ok; P(f"K3 turnaround finder: t_ta {st['tb']:.4f} against the shell ODE {t_an:.4f} Gyr, {e:.2%}; state handed back has R_T of the maximum, |d| {abs(rb - st['Rb']):.1e}: {'PASS' if ok else 'FAIL'}")
    # K5: preemption across both phases, small real run (ng 24)
    w0, w1 = os.path.join(HERE, "cache_k5a"), os.path.join(HERE, "cache_k5b")
    for q in (w0, w1): shutil.rmtree(q, ignore_errors=True)
    base = [sys.executable, os.path.abspath(__file__), "--seed", "1", "--ng", "24", "--axis-z", "--resume"]; env = dict(os.environ); a1 = subprocess.run(base + ["--work", w0, "--stop-step", "100"], env=env, capture_output=True, text=True); ta = json.load(open(os.path.join(w0, "turnaround.json"))) if os.path.exists(os.path.join(w0, "turnaround.json")) else None
    if ta is None or int(np.load(os.path.join(w0, "ckpt.npz"))["phase"]) != 1: P(f"K5 setup: run a did not reach the disc phase at all: {a1.stdout[-300:]} {a1.stderr[-300:]}: FAIL"); good = False
    else:
        s0 = ta["step_ta"]; kl = f"0:{max(s0 // 2 // 10 * 10 + 3, 13)},1:{s0 + 53}"; rc = []
        for _ in range(4):
            p = subprocess.run(base + ["--work", w1, "--stop-step", "100", "--kill-at", kl], env=env, capture_output=True, text=True); rc.append(p.returncode)
            if p.returncode != 75: break
        Za, Zb = np.load(os.path.join(w0, "ckpt.npz")), np.load(os.path.join(w1, "ckpt.npz")); d = max(float(np.abs(Za["x"] - Zb["x"]).max() / np.abs(Za["x"]).max()), float(np.abs(Za["v"] - Zb["v"]).max() / np.abs(Za["v"]).max())); ok = d <= 1e-12 and rc == [75, 75, 0]; good &= ok; P(f"K5 SIGTERM at {kl} (turnaround at step {s0}), exits {rc}, against the uninterrupted run 100 steps after turnaround: {d:.1e}: {'PASS' if ok else 'FAIL'}")
    for q in (w0, w1): shutil.rmtree(q, ignore_errors=True)
    open(os.path.join(HERE, "pz1_checks.out"), "w").write("\n".join(OUT) + "\n"); return 0 if good else 1

if __name__ == "__main__":
    sys.exit(main())
