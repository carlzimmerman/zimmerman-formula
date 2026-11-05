#!/usr/bin/env python3
"""CQ6_past_first_caustic: 1D planar collapse of v3s's P(X) dust limit with AZ14's quartic regulator
F = lambda int |rho'|^4/rho^3 dx = 256 lambda int |psi'|^4 dx (psi = rho^(1/4)), Lagrangian sheets, exact planar
gravity with the background subtracted, implicit midpoint. Criteria: FROZEN_CRITERIA.md (8131404df6).
kappa = 1/2 FITTED; not theory closed. a0 does not enter (both footings identical, nothing pooled).
No particle; the cold sector stays retired. Adopts nothing.

usage: nice -n 10 python3 cq6.py all            (checks, MUTATE, ladder, K-dt, S1, analysis)
       python3 cq6.py smoke --N 256 --tend 8 --out DIR   (timing/smoke test, not a frozen run)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, time, signal, argparse
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import warnings
warnings.filterwarnings("ignore")
np.seterr(all="ignore")   # trial Newton states with Delta <= 0 are rejected by the line search

NOTE = "kappa = 1/2 FITTED; not theory closed. a0 does not enter; footings identical, not pooled."
L = 1.0
TC = 3.0                       # analytic first caustic (Zel'dovich, static background), tau units
TX = 2.0 * np.pi               # frozen crossing time t_x
T_END = TC + 10.0 * TX
W5_START = T_END - 5.0 * TX
A = 1.0 / (2.0 * np.pi * np.cosh(TC))
SAMPLE_DT = 0.05
FRACS = (0.25, 0.5, 0.75, 0.9)
PROFILE_X = np.array([0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5])
LAM = 1e-8
HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ["t", "K", "F", "W", "E", "P", "Rv", "rho_c", "w25", "w50", "w75", "w90", "min_D", "max_dlnrho"]

_STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: _STOP.__setitem__("flag", True))


def cells(x):
    xr = np.roll(x, -1)
    xr[-1] = xr[-1] + L
    return xr - x


def reg_from_D(D, lam, m):
    """F_d, G_c = dF/dDelta_c for cell widths D (periodic)."""
    psi = (m / D) ** 0.25
    psin = np.roll(psi, -1)
    s = 0.5 * (D + np.roll(D, -1))
    d = psin - psi
    F = 256.0 * lam * np.sum(d ** 4 / s ** 3)
    pdot = -psi / (4.0 * D)
    dc = -4.0 * d ** 3 * pdot / s ** 3 - 1.5 * d ** 4 / s ** 4          # d e_c / d Delta_c
    dn = 4.0 * d ** 3 * np.roll(pdot, -1) / s ** 3 - 1.5 * d ** 4 / s ** 4  # d e_c / d Delta_{c+1}
    G = 256.0 * lam * (dc + np.roll(dn, 1))
    return F, G, psi


def reg(x, lam, m):
    D = cells(x)
    F, G, psi = reg_from_D(D, lam, m)
    force = G - np.roll(G, 1)              # -dF/dx_i
    return F, G, force, D, psi


class Model:
    def __init__(self, N, lam):
        self.N, self.lam, self.m = N, lam, 1.0 / N
        self.q = -0.5 + (np.arange(N) + 0.5) / N
        self.rows = np.repeat(np.arange(N), 5)
        self.offs = np.tile(np.arange(-2, 3), N)
        self.cols = (self.rows + self.offs) % N
        self.diag = (self.offs == 0).astype(float)
        self.ncol = 8

    def acc(self, x):
        g = x - self.q
        g = g - g.mean()
        if self.lam == 0.0:
            return g
        _, _, f, _, _ = reg(x, self.lam, self.m)
        return f / self.m + g

    def jac_reg(self, x):
        N, h = self.N, 1e-30
        Jc = np.empty((self.ncol, N))
        for c in range(self.ncol):
            xp = x.astype(complex)
            xp[c::self.ncol] += 1j * h
            _, _, f, _, _ = reg(xp, self.lam, self.m)
            Jc[c] = f.imag / h / self.m
        return Jc[self.cols % self.ncol, self.rows]

    def step(self, x, v, dt):
        """One implicit-midpoint step; returns (x, v) or None on failure."""
        c = 0.25 * dt * dt
        base = x + 0.5 * dt * v
        y = base.copy()
        for it in range(25):
            R = y - base - c * self.acc(y)
            if not np.all(np.isfinite(R)):
                return None
            if self.lam == 0.0:
                data = (1.0 - c) * self.diag
            else:
                data = (1.0 - c) * self.diag - c * self.jac_reg(y)
            J = sp.csc_matrix((data, (self.rows, self.cols)), shape=(self.N, self.N))
            dx = -spla.spsolve(J, R)
            if not np.all(np.isfinite(dx)):
                return None
            if np.max(np.abs(dx)) <= 1e-12:
                y = y + dx
                break
            r0 = np.linalg.norm(R)
            alpha, ok = 1.0, False
            for ls in range(40):
                yt = y + alpha * dx
                if self.lam == 0.0 or np.all(cells(yt) > 0):
                    Rt = yt - base - c * self.acc(yt)
                    if np.all(np.isfinite(Rt)):
                        rt = np.linalg.norm(Rt)
                        if rt <= (1.0 - 1e-4 * alpha) * r0 or np.max(np.abs(Rt)) <= 1e-13:
                            ok = True
                            break
                alpha *= 0.5
            if not ok:
                return None
            y = yt
            if np.max(np.abs(alpha * dx)) <= 1e-12:
                break
        else:
            return None
        xn = 2.0 * y - x
        vn = 4.0 * (y - x) / dt - v          # v_{n+1} = 2 v_mid - v_n, v_mid = (x_{n+1} - x_n)/dt
        if self.lam > 0.0 and not np.all(cells(xn) > 0):
            return None
        return xn, vn

    def diag_row(self, t, x, v):
        m, lam = self.m, self.lam
        if lam > 0.0:
            F, G, _, D, psi = reg(x, lam, m)
            gwrap = G[-1]
            s = 0.5 * (D + np.roll(D, -1))
            dl = 4.0 * np.abs(np.roll(psi, -1) - psi) / (s * 0.5 * (psi + np.roll(psi, -1)))
            mdl = float(np.max(dl))
        else:
            F, gwrap, D, mdl = 0.0, 0.0, cells(x), float("nan")
        K = 0.5 * m * np.sum(v * v)
        ps = x - self.q
        ps = ps - ps.mean()
        W = -0.5 * m * np.sum(ps * ps)
        Wv = -m * np.sum(x * ps)
        Rv = (2 * K + 4 * F + L * gwrap) / Wv
        rho_c = m / D[self.N // 2 - 1]
        ws = [np.interp(f / 2, self.q, x) - np.interp(-f / 2, self.q, x) for f in FRACS]
        return [t, K, F, W, K + F + W, m * np.sum(v), Rv, rho_c] + ws + [float(np.min(D)), mdl]

    def profile(self, x):
        D = cells(x)
        X = x + 0.5 * D
        rho = self.m / D
        return 0.5 * (np.interp(PROFILE_X, X, rho) + np.interp(-PROFILE_X, X, rho))


def run(N, lam, dt, tend, tag, outdir):
    os.makedirs(outdir, exist_ok=True)
    resf = os.path.join(outdir, f"{tag}.json")
    if os.path.exists(resf):
        print(f"[{tag}] done already, skipping", flush=True)
        return json.load(open(resf))
    ck = os.path.join(outdir, f"{tag}_ckpt.npz")
    M = Model(N, lam)
    nsteps = int(round(tend / dt))
    every = int(round(SAMPLE_DT / dt))
    x = M.q - A * np.sin(2 * np.pi * M.q)
    v = np.zeros(N)
    n0, rows, prof, nprof, nsub, wall0 = 0, [], np.zeros(PROFILE_X.size), 0, 0, 0.0
    if os.path.exists(ck):
        z = np.load(ck)
        x, v, n0 = z["x"], z["v"], int(z["n"])
        rows, prof, nprof, nsub, wall0 = list(map(list, z["rows"])), z["prof"], int(z["nprof"]), int(z["nsub"]), float(z["wall"])
        print(f"[{tag}] resumed at step {n0}", flush=True)
    else:
        rows.append(M.diag_row(0.0, x, v))
    t_start = time.time()
    status, t_fail = "reached_t_end", None

    def save_ck(n):
        np.savez(ck, x=x, v=v, n=n, rows=np.array(rows), prof=prof, nprof=nprof, nsub=nsub,
                 wall=wall0 + time.time() - t_start)

    for n in range(n0, nsteps):
        t = (n + 1) * dt
        out = M.step(x, v, dt)
        if out is None and lam > 0.0:
            for j in range(1, 7):
                k, xs, vs, ok = 2 ** j, x, v, True
                for _ in range(k):
                    o = M.step(xs, vs, dt / k)
                    if o is None:
                        ok = False
                        break
                    xs, vs = o
                if ok:
                    out, nsub = (xs, vs), nsub + 1
                    break
        if out is None:
            status, t_fail = "BLOW-UP", t
            break
        xprev = x
        x, v = out
        Dmin = np.min(cells(x))
        if not np.all(np.isfinite(x)) or not np.all(np.isfinite(v)):
            status, t_fail = "BLOW-UP (non-finite)", t
            break
        if Dmin <= 0.0:
            # crossing (only reachable at lam = 0); interpolate the centre-cell width linearly in time
            d0 = cells(xprev)[N // 2 - 1]
            d1 = cells(x)[N // 2 - 1]
            t_fail = t - dt + dt * d0 / (d0 - d1) if d0 > 0 and d1 <= 0 else t
            status = "CROSSED"
            rows.append(M.diag_row(t, x, v))
            break
        if (n + 1) % every == 0:
            rows.append(M.diag_row(t, x, v))
            if t >= W5_START - 1e-9:
                prof = prof + M.profile(x)
                nprof += 1
        if (n + 1) % 10000 == 0:
            save_ck(n + 1)
            print(f"[{tag}] t={t:.3f} rho_c={rows[-1][7]:.3f} Rv={rows[-1][6]:.3f} "
                  f"dE={rows[-1][4]-rows[0][4]:.2e} wall={wall0+time.time()-t_start:.0f}s", flush=True)
        if _STOP["flag"]:
            save_ck(n + 1)
            print(f"[{tag}] SIGTERM: checkpoint at step {n+1}", flush=True)
            sys.exit(3)
    Z = np.array(rows)
    np.savez(os.path.join(outdir, f"{tag}_series.npz"), cols=np.array(COLS), data=Z)
    r = summarize(Z, prof, nprof, N, lam, dt, tend, status, t_fail, nsub, wall0 + time.time() - t_start)
    json.dump(r, open(resf, "w"), indent=1)
    if os.path.exists(ck):
        os.remove(ck)
    print(f"[{tag}] {status} t_fail={t_fail} wall={r['wall_s']:.0f}s", flush=True)
    return r


def summarize(Z, prof, nprof, N, lam, dt, tend, status, t_fail, nsub, wall):
    c = {k: i for i, k in enumerate(COLS)}
    t = Z[:, c["t"]]
    K = Z[:, c["K"]]
    E = Z[:, c["E"]]
    r = {"note": NOTE, "N": N, "lambda": lam, "dt": dt, "t_end": tend, "status": status, "t_fail": t_fail,
         "passed_caustic": status == "reached_t_end", "substep_events": nsub, "wall_s": wall,
         "energy_maxdev_over_Kmax": float(np.max(np.abs(E - E[0])) / max(np.max(K), 1e-300)),
         "K_max": float(np.max(K)), "E0": float(E[0]), "P_maxabs": float(np.max(np.abs(Z[:, c["P"]]))),
         "min_D_over_run": float(np.min(Z[:, c["min_D"]])), "max_dlnrho_over_run": float(np.nanmax(Z[:, c["max_dlnrho"]]))}
    first = t <= TC + TX
    i = int(np.argmax(np.where(first, Z[:, c["rho_c"]], -1)))
    r["first_bounce"] = {"rho_c_max": float(Z[i, c["rho_c"]]), "t": float(t[i]),
                         "rho_c_at_tc": float(np.interp(TC, t, Z[:, c["rho_c"]]))}
    coarse = np.arange(0, len(t), int(round(1.0 / SAMPLE_DT)))
    r["series_1tau"] = {k: [round(float(Z[j, c[k]]), 6) for j in coarse] for k in ("t", "rho_c", "Rv", "w50", "K", "F")}
    w = t >= W5_START - 1e-9
    if r["passed_caustic"] and np.any(w):
        Rv, wh = Z[w, c["Rv"]], Z[w, c["w50"]]
        r["W5"] = {"n_samples": int(w.sum()), "Rv_min": float(Rv.min()), "Rv_max": float(Rv.max()),
                   "Rv_mean": float(Rv.mean()), "w_half_mean": float(wh.mean()), "w_half_min": float(wh.min()),
                   "w_half_max": float(wh.max()),
                   "w_half_halfrange_over_mean": float((wh.max() - wh.min()) / (2 * wh.mean())),
                   "rho_c_mean": float(Z[w, c["rho_c"]].mean()), "rho_c_min": float(Z[w, c["rho_c"]].min()),
                   "rho_c_max": float(Z[w, c["rho_c"]].max()),
                   "w25_mean": float(Z[w, c["w25"]].mean()), "w75_mean": float(Z[w, c["w75"]].mean()),
                   "w90_mean": float(Z[w, c["w90"]].mean()),
                   "K_mean": float(Z[w, c["K"]].mean()), "F_mean": float(Z[w, c["F"]].mean()),
                   "profile_x": PROFILE_X.tolist(), "profile_rho_mean": (prof / max(nprof, 1)).tolist(),
                   "n_profile": nprof}
    return r


def checks():
    N, lam = 64, LAM
    m = 1.0 / N
    q = -0.5 + (np.arange(N) + 0.5) / N
    rng = np.random.default_rng(0)
    x = q - 0.8 * np.sin(2 * np.pi * q) / (2 * np.pi) + 1e-3 * rng.standard_normal(N)
    F, G, f, D, _ = reg(x, lam, m)
    h = 1e-30
    grad = np.empty(N)
    for j in range(N):
        xp = x.astype(complex)
        xp[j] += 1j * h
        grad[j] = reg(xp, lam, m)[0].imag / h
    kfd = float(np.max(np.abs(-grad - f)) / np.max(np.abs(f)))
    al = 0.7
    Fa = reg_from_D(al * D, lam, m)[0]
    khom1 = float(abs(Fa * al ** 4 - F) / F)
    khom2 = float(abs(np.sum(x * (-f)) + 4 * F + L * G[-1]) / F)
    out = {"note": NOTE, "K-FD_rel": kfd, "K-FD_pass": kfd <= 1e-8, "K-hom_scaling_rel": khom1,
           "K-hom_scaling_pass": khom1 <= 1e-12, "K-hom_virial_rel": khom2, "K-hom_virial_pass": khom2 <= 1e-10}
    print("[checks]", json.dumps(out), flush=True)
    return out


def rel(a, b):
    return abs(a - b) / abs(b)


EQ = ("rho_c_mean", "w25_mean", "w_half_mean", "w75_mean", "w90_mean", "Rv_mean")


def dmax(r1, r2):
    if "W5" not in r1 or "W5" not in r2:
        return float("inf"), {}
    d = {k: rel(r1["W5"][k], r2["W5"][k]) for k in EQ}
    return max(d.values()), d


def analyze(res, mut, chk):
    lad = [res["R256"], res["R512"], res["R1024"]]
    kzel = {f"N{r['N']}": {"t_cross": r["t_fail"], "rel": rel(r["t_fail"], TC) if r["t_fail"] else None,
                          "pass": bool(r["t_fail"] and rel(r["t_fail"], TC) <= 0.01)} for r in mut.values()}
    mutate_pass = all(r["status"] == "CROSSED" for r in mut.values())
    a = {f"N{r['N']}": r["passed_caustic"] for r in lad}
    b = {f"N{r['N']}": bool(r["energy_maxdev_over_Kmax"] <= 1e-3 and r["P_maxabs"] <= 1e-10) for r in lad}
    d_fine, dfd = dmax(res["R512"], res["R1024"])
    d_coarse, dcd = dmax(res["R256"], res["R512"])
    e_pass = d_fine <= 0.05
    kdt_d, kdtd = dmax(res["KDT512"], res["R512"])
    kdt = bool(res["KDT512"]["passed_caustic"] == res["R512"]["passed_caustic"]
               and res["KDT512"]["energy_maxdev_over_Kmax"] <= 1e-3 and res["KDT512"]["P_maxabs"] <= 1e-10
               and kdt_d <= 0.05)
    cv = {f"N{r['N']}": bool("W5" in r and 0.9 <= r["W5"]["Rv_min"] and r["W5"]["Rv_max"] <= 1.1) for r in lad[1:]}
    dd = {f"N{r['N']}": bool("W5" in r and r["W5"]["w_half_halfrange_over_mean"] <= 0.10) for r in lad[1:]}
    controls = all(v["pass"] for v in kzel.values()) and mutate_pass and chk["K-FD_pass"] \
        and chk["K-hom_scaling_pass"] and chk["K-hom_virial_pass"] and kdt
    shrink = d_coarse / d_fine if d_fine > 0 else float("inf")
    if not controls:
        label = "NOT EVALUABLE (control failed)"
    elif not all(a.values()):
        label = "ILL-POSED (blow-up or regulated crossing)"
    elif not e_pass and shrink < 1.5:
        label = "ILL-POSED (non-convergence)"
    elif not all(b.values()):
        label = "NOT EVALUABLE (energy line)"
    elif not e_pass:
        label = "NOT EVALUABLE (resolution-limited)"
    elif all(cv.values()) and all(dd.values()):
        label = "SETTLES"
    else:
        label = "OSCILLATES WITHOUT SETTLING"
    return {"note": NOTE, "label": label, "controls_pass": controls, "K-ZEL": kzel, "MUTATE_pass": mutate_pass,
            "K-dt": {"pass": kdt, "dmax": kdt_d, "d": kdtd}, "(a)": a, "(b)": b, "(c)": cv, "(d)": dd,
            "(e)": {"pass": e_pass, "d_fine": d_fine, "d_coarse": d_coarse, "shrink": shrink,
                    "d_fine_each": dfd, "d_coarse_each": dcd}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["all", "smoke"])
    ap.add_argument("--N", type=int, default=256)
    ap.add_argument("--tend", type=float, default=8.0)
    ap.add_argument("--lam", type=float, default=LAM)
    ap.add_argument("--dt", type=float, default=1e-3)
    ap.add_argument("--out", default=os.path.join(HERE, "runs"))
    g = ap.parse_args()
    if g.mode == "smoke":
        checks()
        r = run(g.N, g.lam, g.dt, g.tend, f"smoke_N{g.N}_lam{g.lam:g}_dt{g.dt:g}", g.out)
        Z = np.load(os.path.join(g.out, f"smoke_N{g.N}_lam{g.lam:g}_dt{g.dt:g}_series.npz"))["data"]
        for row in Z[-8:]:
            print("  t %.3f dE/Kmax %+.2e K %.2e F %.2e rho_c %.3f minD %.2e maxdlnrho %.1f" % (row[0], (row[4]-Z[0,4])/max(Z[:,1].max(),1e-300), row[1], row[2], row[7], row[12], row[13]))
        print(json.dumps({k: r[k] for k in ("status", "t_fail", "energy_maxdev_over_Kmax", "first_bounce",
                                             "min_D_over_run", "wall_s", "substep_events")}))
        print(json.dumps(r["series_1tau"]))
        return
    chk = checks()
    out = g.out
    mut = {f"M{N}": run(N, 0.0, 1e-3, T_END, f"M{N}", out) for N in (256, 512, 1024)}
    res = {}
    for tag, N, lam, dt in (("R256", 256, LAM, 1e-3), ("R512", 512, LAM, 1e-3), ("R1024", 1024, LAM, 1e-3),
                            ("KDT512", 512, LAM, 5e-4), ("S1_512", 512, 1e-9, 1e-3), ("S1_1024", 1024, 1e-9, 1e-3)):
        res[tag] = run(N, lam, dt, T_END, tag, out)
    ana = analyze(res, mut, chk)
    s1d, s1 = dmax(res["S1_512"], res["S1_1024"])
    ana["S1_numbers_only"] = {"d_512_1024": s1d, "d_each": s1}
    print("[label]", ana["label"], flush=True)
    strip = lambda r: {k: v for k, v in r.items() if k != "series_1tau"} | {"series_1tau": r.get("series_1tau")}
    json.dump({"note": NOTE, "criteria_commit": "8131404df6", "checks": chk, "analysis": ana,
               "runs": {k: strip(v) for k, v in res.items()}}, open(os.path.join(HERE, "cq6_results.json"), "w"), indent=1)
    json.dump({"note": NOTE, "criteria_commit": "8131404df6", "K-ZEL": ana["K-ZEL"], "MUTATE_pass": ana["MUTATE_pass"],
               "runs": mut}, open(os.path.join(HERE, "cq6_results_MUTATE.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
