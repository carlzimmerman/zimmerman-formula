#!/usr/bin/env python3
"""AN2 checks and S0. Run: python3 an2_checks.py S0|KD|KC|KZ|KE1|KE2|KR [--mutate]. kappa = 1/2 FITTED."""
import os, sys, json, time, math
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.special import elliprd
import an2
from an2 import G, AF, RX0, RB0, TU, Bg, Mesh, Sim, Tracker, tet_dets, fold_shape, solve_hold, solve_aqual_projection, MUTATE, TAG, HERE, peak_amp, deposit


def out(nm, d):
    fn = os.path.join(HERE, f"an2_checks{TAG}.jsonl")
    d = dict(check=nm, **d)
    with open(fn, "a") as f: f.write(json.dumps(d) + "\n")
    print(json.dumps(d), flush=True)


# ---------- S0 ellipsoid
def b_quad(ax):
    a1, a2, a3 = ax; pr = a1 * a2 * a3; o = []
    for i in range(3):
        w = (a1 * a2 * a3) ** (2 / 3)   # s = w x/(1-x), finite range
        def g(x):
            s = w * x / (1 - x)
            return w / (1 - x) ** 2 / ((ax[i]**2 + s) * math.sqrt((a1**2 + s) * (a2**2 + s) * (a3**2 + s)))
        o.append(pr * quad(g, 0, 1, epsabs=0, epsrel=1e-12, limit=400, points=[0.5])[0])
    return np.array(o)
def b_carlson(ax):
    a1, a2, a3 = ax; pr = a1 * a2 * a3; A = np.array([a1, a2, a3])**2
    return np.array([2 / 3 * pr * elliprd(A[(i + 1) % 3], A[(i + 2) % 3], A[i]) for i in range(3)])
def ellipsoid(d0, q, form="quad"):
    bg = Bg(); ai = 1 / 21.0; bf = b_quad if form == "quad" else b_carlson
    q = np.array(q, float); l = d0 * bf(q) / 2; Hi = bg.H(ai)
    y0 = np.concatenate([ai * q * (1 - l), Hi * ai * q * (1 - 2 * l)]); L = bg.OL * bg.H0**2; Pq = np.prod(q)
    def rhs(t, y):
        ax = y[:3]; a = float(bg.a(t)); dl = a**3 * Pq / np.prod(ax) - 1; b = bf(np.abs(ax)); rb = bg.rm0 / a**3
        return np.concatenate([y[3:], ax * (L - 4 * np.pi * G * rb * (1 / 3 + dl * b / 2))])
    ev = lambda t, y: y[:3].min() - 1e-4 * q[np.argmin(y[:3])]
    ev.terminal = True
    sol = solve_ivp(rhs, (bg.t(ai), 3 * bg.t(1.0)), y0, method="DOP853" if form == "quad" else "LSODA", rtol=1e-9, atol=1e-9 * q.min(), events=ev)
    t = sol.t_events[0][0] if len(sol.t_events[0]) else np.inf
    return float(t), float(1 / bg.a(t) - 1) if np.isfinite(t) and t < bg.t(1.0) * 3 else None


def S0():
    sh = json.load(open(os.path.join(HERE, "an2_shapes.json"))); rows = []
    for k, v in sh.items():
        for nm, R in (("0", [v["RG"]] * 3), ("A", v["A"]["R"]), ("B", v["B"]["R"])):
            t, z = ellipsoid(v["d0"], sorted(R))
            rows.append(dict(key=k, shape=nm, R=R, t_Gyr=t * TU, z_first_axis=z))
    out("S0", dict(rows=rows))


def KE1():
    sh = json.load(open(os.path.join(HERE, "an2_shapes.json")))
    v = sh["1e12"]; res = []
    for R in ([v["RG"]] * 3, v["A"]["R"], v["B"]["R"]):
        t1, _ = ellipsoid(v["d0"], sorted(R), "quad"); t2, _ = ellipsoid(v["d0"], sorted(R), "carlson")
        res.append(abs(t1 - t2) / t1)
    out("KE1", dict(err=res, line=1e-6, ok=max(res) <= 1e-6))


def KE2(eta=0.05, N=96):
    eta = float(eta); N = int(N)
    sh = json.load(open(os.path.join(HERE, "an2_shapes.json")))["1e12"]; bg = Bg(); P = peak_amp("1e12"); L = 8 * P["qt"]
    R = np.array(sh["B"]["R"]); A = R / R.max() * L / 8; dq = L / N; i = (np.arange(N) + 0.5) * dq - L / 2
    X, Y, Z = np.meshgrid(i, i, i, indexing="ij"); mm = np.sqrt((X / A[0])**2 + (Y / A[1])**2 + (Z / A[2])**2)
    dl = P["d0"] * 0.5 * (1 - np.tanh((mm - 1) / 0.1)); m = Mesh(N, L); mean = dl.mean(); dk = m.fft(dl - mean)
    disp = np.stack([m.ifft(1j * m.gk[c] * dk * m.ik2) for c in range(3)]); ai = 1 / 21.0; mom = ai**2 * bg.H(ai) * disp
    fn = lambda p: np.sqrt((p[0] / A[0])**2 + (p[1] / A[1])**2 + (p[2] / A[2])**2) <= 0.8
    S = Sim(N, L, AF["canonical"], 1.0, eta, bg.t(ai), bg, disp, mom, dust=True, qmask_fn=fn)
    o = S.run(3 * bg.t(1.0), cap=1e9)
    tq = o.get("fold_q", {}).get("t_Gyr"); tode, zode = ellipsoid(P["d0"] - mean, sorted(A))
    err = abs(tq - tode * TU) / (tode * TU) if tq else None
    out("KE2" if (eta, N) == (0.05, 96) else "KE2_diag", dict(eta=eta, t_engine=tq, z_engine=o.get("fold_q", {}).get("z"), shape=o.get("fold_q", {}).get("shape"), eig=o.get("fold_q", {}).get("eig"), t_ode=tode * TU, z_ode=zode, err=err, line=0.03, ok=bool(err is not None and err <= 0.03), any=o.get("fold_any"), steps=o["nstep"], cpu=o["cpu_s"], rss=o["rss_gb"]))


def KZ(eta=0.05, N=64):
    eta = float(eta); N = int(N)
    bg = Bg(); ai = 1 / 21.0; res = {}
    for nm, dust, mu in (("KZ", True, 1.0), ("KZ2", False, 1.24e8 * 1e-3)):
        L = 145000.0; k = 2 * np.pi / L; dq = L / N; i = (np.arange(N) + 0.5) * dq
        q0 = np.meshgrid(i, i, i, indexing="ij")[0]
        Di, Dc = bg.D(ai), bg.D(0.5)
        Ak = Di / Dc; A = Ak / k
        s = np.zeros((3, N, N, N)); s[0] = -A * np.sin(k * q0)  # det J = 1 - D Ak cos(k q): q=0 crosses
        hh = 1e-5 * ai; f = (np.log(bg.D(ai + hh)) - np.log(bg.D(ai - hh))) / (np.log(ai + hh) - np.log(ai - hh))
        mom = ai**2 * bg.H(ai) * f * s
        S = Sim(N, L, AF["canonical"], mu, eta, bg.t(ai), bg, s, mom, dust=dust)
        S.tr.qmask[:] = True
        o = S.run(3 * bg.t(1.0), cap=1e9)
        t = o.get("fold_any", {}).get("t_Gyr"); tc = bg.t(0.5) * TU; err = abs(t - tc) / tc if t else None
        res[nm] = dict(t=t, t_exact=tc, err=err, steps=o["nstep"], shape=o.get("fold_any", {}).get("shape"), status=o["status"], ok=bool(err is not None and err <= 5e-3))
    out("KZ" if (eta, N) == (0.05, 64) else "KZ_diag", dict(eta=eta, N=N, res=res, line=5e-3, ok=all(v["ok"] for v in res.values())))


def KD(N=64):
    N = int(N); L = 1000.0; dq = L / N; k = 2 * np.pi / L; i = (np.arange(N)) * dq
    X, Y, Z = np.meshgrid(i, i, i, indexing="ij"); a, b, c_, e = 0.2 / k, 0.15 / k, 0.1 / k, 0.25 / k
    d = np.stack([a * np.sin(k * Y) + e * np.sin(k * X), b * np.sin(k * Z), c_ * np.sin(k * X)])
    dets = tet_dets(d, dq); errs = []; errs_c = []
    def Jdet(x, y, z):
        return (1 + e * k * np.cos(k * x)) * (1) * 1 - a * k * np.cos(k * y) * (0 - b * k * np.cos(k * z) * c_ * k * np.cos(k * x))
    def Jcol(j, x, y, z):  # analytic column j of J at a point
        if j == 0: return [1 + e * k * np.cos(k * x), 0 * x, c_ * k * np.cos(k * x)]
        if j == 1: return [a * k * np.cos(k * y), 1 + 0 * x, 0 * x]
        return [0 * x, b * k * np.cos(k * z), 1 + 0 * x]
    for pm, sg, dt in zip(an2.PERMS, an2.PSIGN, dets):
        w = np.zeros(3); w[pm[0]] += 3 / 4; w[pm[1]] += 2 / 4; w[pm[2]] += 1 / 4
        errs_c.append(float(np.abs(dt - Jdet(X + w[0] * dq, Y + w[1] * dq, Z + w[2] * dq)).max()))   # frozen form, first run
        cols = []; base = np.zeros(3)
        for ax in pm:   # A1: each column at its own tet edge midpoint
            mid = base.copy(); mid[ax] += 0.5; cols.append(Jcol(ax, X + mid[0] * dq, Y + mid[1] * dq, Z + mid[2] * dq)); base[ax] += 1
        A, B, C = cols
        det = A[0] * (B[1] * C[2] - B[2] * C[1]) - B[0] * (A[1] * C[2] - A[2] * C[1]) + C[0] * (A[1] * B[2] - A[2] * B[1])
        errs.append(float(np.abs(dt - sg * det).max()))
    a_err = max(errs); a_err_centroid = max(errs_c)
    i2 = (np.arange(N) + 0.5) * dq - L / 2; X, Y, Z = np.meshgrid(i2, i2, i2, indexing="ij"); r2 = X**2 + Y**2 + Z**2; w = 60.0
    mask = np.ones((N, N, N), bool)
    def trk(): return Tracker(N, dq, mask, mutate=MUTATE)
    # compressed held core: det 1e-9 at centre, no crossing
    f = 1e-3 + (1 - 1e-3) * (1 - np.exp(-(r2 / (150.0 * 150.0)) ** 2)); comp = np.stack([X * (f - 1), Y * (f - 1), Z * (f - 1)])
    T = trk(); s0 = T.scan(comp * 0); T.prev["any"] = s0["any"][0]; T.prev["q"] = s0["q"][0]
    seq = [T.scan(comp * x) for x in (0.5, 0.9, 1.0, 1.0)]
    fired = []
    for j, sc in enumerate(seq): fired += T.update(float(j), float(j + 1), sc)
    mind = seq[-1]["any"][0]; held_ok = (not fired) and T.cand["any"] is None and mind > 0
    # synthetic sheet fold on the right step, at the right plane
    ks = k; sheet = np.stack([-np.sin(ks * X) / ks, 0 * X, 0 * X])
    T = trk(); sc = T.scan(sheet * 0.5); T.prev["any"] = sc["any"][0]; T.prev["q"] = sc["q"][0]; steps = [0.8, 0.95, 1.02, 1.1, 1.2]; firedat = None
    for j, x in enumerate(steps):
        nw = T.update(float(j), float(j + 1), T.scan(sheet * x))
        if nw and firedat is None: firedat = j; break
    fo = T.fold["any"]; ii = np.unravel_index(fo["idx"], (N, N, N)) if fo else None
    site_ok = fo is not None and abs(X[ii] + 0.5 * dq) <= 1.5 * dq
    # exact det of the first-order sheet at grid scale reaches 0 between x=0.95 and 1.02 in 64 cells: true crossing step index 2, confirmed at 3
    step_ok = firedat == 3
    # transient: inverts then reverses
    T = trk(); sc = T.scan(sheet * 0.5); T.prev["any"] = sc["any"][0]; T.prev["q"] = sc["q"][0]
    r = []
    for j, x in enumerate((0.9, 1.05, 0.9, 0.9)): r += T.update(float(j), float(j + 1), T.scan(sheet * x))
    tr_ok = (not r) and T.transient >= 1
    # shape reads
    fil = np.stack([-0.99 * np.sin(k * X) / k, -0.99 * np.sin(k * Y) / k, 0 * X]); pt = np.stack([-0.99 * np.sin(k * X) / k, -0.99 * np.sin(k * Y) / k, -0.99 * np.sin(k * Z) / k]); sh = sheet * 0.99
    idx = np.ravel_multi_index((N // 2, N // 2, N // 2), (N, N, N))
    names = [fold_shape(z, idx, N, dq)[0] for z in (sh, fil, pt)]
    sh_ok = names == ["sheet", "filament", "point"]
    ok = bool(a_err <= 2e-3 and held_ok and site_ok and step_ok and tr_ok and sh_ok)
    out("KD", dict(N=N, analytic_err=a_err, frozen_form_err_centroid=a_err_centroid, line=2e-3, held_mindet=mind, held_ok=bool(held_ok), site_ok=bool(site_ok), firedat=firedat, step_ok=bool(step_ok), transient_ok=bool(tr_ok), shapes=names, ok=ok))


def KC():
    H_B = 0.6856426703851345; acc = 1e10 * H_B / 3.0856775814913673e22; GC = 4.30091e-13
    A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
    NC, LC, MC = 128, 0.32, 1e11; m = Mesh(NC, LC); b = 2 * m.dx
    ii = np.arange(NC) * m.dx - LC / 2; X, Y, Z = np.meshgrid(ii, ii, ii, indexing="ij"); rr = np.sqrt(X**2 + Y**2 + Z**2)
    rho = (1 + rr**2 / b**2) ** -2.5; rho *= MC / (rho.sum() * m.dx**3)
    Sb = 4 * math.pi * GC * (rho - rho.mean()); Sbk = m.fft(Sb); del rho, Sb
    rhat = [np.where(rr > 0, c / np.maximum(rr, 1e-30), 0) for c in (X, Y, Z)]; del X, Y, Z
    edges = np.geomspace(3 * m.dx, LC / 8, 11); shell = np.digitize(rr, edges)
    sm = lambda f: np.array([f[shell == i].mean() for i in range(1, 11)])
    rad = lambda Gv: Gv[0] * rhat[0] + Gv[1] * rhat[1] + Gv[2] * rhat[2]
    res = {}; sg = -1.0 if MUTATE else 1.0
    for foot in A0:
        a0c = A0[foot] / acc
        Gv, GN, inf1 = solve_aqual_projection(m, Sbk, a0c)
        gNm = np.sqrt(GN[0]**2 + GN[1]**2 + GN[2]**2); y = np.maximum(gNm, 1e-300) / a0c
        law = 0.5 * (1 + np.sqrt(1 + 4 / y)) * rad(GN); del gNm, y, GN
        gs, ls = sm(rad(Gv)), sm(law); del law
        c1 = float(np.max(np.abs(gs / ls - 1)))
        gm = np.sqrt(Gv[0]**2 + Gv[1]**2 + Gv[2]**2); om = 1 - gm / (a0c + gm)
        Stk = m.div_k([om * Gv[c] for c in range(3)]); Stk[0, 0, 0] = 0; del om
        phik = -(Sbk + Stk) * m.ik2
        xi, inf2 = solve_hold(m, Stk, 0.0, a0c)
        xk = m.fft(xi); Gt = [m.grad_c(phik, c) for c in range(3)]; Gx = [m.grad_c(xk, c) for c in range(3)]
        c2a = float(np.max(np.abs(sm(rad(Gt)) / ls - 1)))
        net = np.sqrt(sum((Gt[c] - sg * Gx[c])**2 for c in range(3))); tot = np.sqrt(sum(Gt[c]**2 for c in range(3)))
        c2b = float(np.max(sm(net) / sm(tot)))
        res[foot] = dict(c1=c1, c2_baryon=c2a, c2_field_net=c2b, hold_iters=inf2["iters"], hold_res=inf2["res"], ok=bool(max(c1, c2a, c2b) <= 0.01))
    out("KC", dict(res=res, line=0.01, ok=all(v["ok"] for v in res.values())))


def KR():
    key, mu, foot, sh = "1e15", 56.6, "canonical", "A"; N, eta = 32, 0.05
    a = an2.build_row(key, mu, foot, sh, N, eta, 8); oa = a.run(a.t0, cap=1e9); ta = oa["fold_q"]["t_Gyr"]
    ck = os.path.join(HERE, "ckpt_KR.npz")
    b = an2.build_row(key, mu, foot, sh, N, eta, 8); r1 = b.run(b.t0, ckpt=ck, kill_at=oa["nstep"] // 2, cap=1e9); an2.STOP["flag"] = False
    c = an2.build_row(key, mu, foot, sh, N, eta, 8); oc = c.run(c.t0, ckpt=ck, cap=1e9); tc = oc["fold_q"]["t_Gyr"]
    if os.path.exists(ck): os.remove(ck)
    rel = abs(ta - tc) / ta
    out("KR", dict(first=r1["status"], ta=ta, tb=tc, rel=rel, line=1e-10, steps=oa["nstep"], ok=bool(r1["status"] == "PREEMPTED" and rel <= 1e-10)))


if __name__ == "__main__":
    globals()[sys.argv[1]](*[x for x in sys.argv[2:] if not x.startswith("--")])
