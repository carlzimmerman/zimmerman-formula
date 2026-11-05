#!/usr/bin/env python3
"""CQ8_caustic_robust_solver: CQ6's discrete model (cq6.py, imported, not edited) with an adaptive implicit midpoint
(Verlet predictor, local error in units of the smallest cell). Criteria: FROZEN_CRITERIA.md (2b11436345).
kappa = 1/2 FITTED; not theory closed. a0 does not enter; footings identical, nothing pooled. No particle; the cold
sector stays retired. Adopts nothing.
usage: nice -n 10 python3 cq8.py all
"""
import os, sys, json, time, signal
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CQ6_past_first_caustic"))
import cq6
import warnings
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
NOTE = "kappa = 1/2 FITTED; not theory closed. a0 does not enter; footings identical, not pooled."
TC, T_END, W5 = cq6.TC, cq6.T_END, cq6.W5_START
WALL, DTMAX, DTFLOOR, SDT = 180.0, 1e-2, 1e-9, 0.05
OUT = os.path.join(HERE, "runs")
_STOP = {"f": False}
signal.signal(signal.SIGTERM, lambda *a: _STOP.__setitem__("f", True))


def implicit(M, x, v, dt, y0):
    c = 0.25 * dt * dt
    base = x + 0.5 * dt * v
    y = y0.copy()
    for it in range(30):
        R = y - base - c * M.acc(y)
        if not np.all(np.isfinite(R)):
            return None
        data = (1.0 - c) * M.diag if M.lam == 0.0 else (1.0 - c) * M.diag - c * M.jac_reg(y)
        J = sp.csc_matrix((data, (M.rows, M.cols)), shape=(M.N, M.N))
        dx = -spla.spsolve(J, R)
        if not np.all(np.isfinite(dx)):
            return None
        r0, alpha, ok = np.linalg.norm(R), 1.0, False
        for ls in range(30):
            yt = y + alpha * dx
            if M.lam == 0.0 or np.all(cq6.cells(yt) > 0):
                Rt = yt - base - c * M.acc(yt)
                if np.all(np.isfinite(Rt)) and (np.linalg.norm(Rt) <= (1 - 1e-4 * alpha) * r0 or np.max(np.abs(Rt)) <= 1e-13):
                    ok = True
                    break
            alpha *= 0.5
        if not ok:
            return None
        y = yt
        if np.max(np.abs(alpha * dx)) <= 1e-12:
            return 2.0 * y - x, 4.0 * (y - x) / dt - v
    return None


def run(N, lam, tol, tag, tend=T_END):
    os.makedirs(OUT, exist_ok=True)
    f = os.path.join(OUT, f"{tag}.json")
    if os.path.exists(f):
        return json.load(open(f))
    M = cq6.Model(N, lam)
    x = M.q - cq6.A * np.sin(2 * np.pi * M.q); v = np.zeros(N)
    a = M.acc(x); t, dt, nxt, n, nrej = 0.0, 1e-3, SDT, 0, 0
    rows = [M.diag_row(0.0, x, v) + [float(np.max(np.abs(a))), dt]]
    t0, status, tfail = time.time(), "REACHED", None
    while t < tend - 1e-12:
        if time.time() - t0 > WALL:
            status = "WALL"; break
        if _STOP["f"]:
            status = "SIGTERM"; break
        h = min(dt, nxt - t)
        if h < DTFLOOR and nxt - t > DTFLOOR:
            status, tfail = "BLOW-UP", t; break
        xp = x + h * v + 0.5 * h * h * a
        o = implicit(M, x, v, h, 0.5 * (x + xp))
        if o is None:
            dt = 0.5 * h; nrej += 1; continue
        xn, vn = o
        err = np.max(np.abs(xn - xp)) / np.min(cq6.cells(x))
        if err > tol:
            dt = h * max(0.2, 0.9 * (tol / err) ** (1 / 3)); nrej += 1; continue
        crossed = np.min(cq6.cells(xn)) <= 0.0
        if crossed and lam > 0:
            dt = 0.5 * h; nrej += 1; continue
        if crossed:
            d0, d1 = cq6.cells(x)[N // 2 - 1], cq6.cells(xn)[N // 2 - 1]
            tfail = t + h * d0 / (d0 - d1) if d0 > 0 and d1 <= 0 else t + h
            status = "CROSSED"; x, v = xn, vn; break
        x, v, t, n = xn, vn, t + h, n + 1
        a = M.acc(x)
        dt = min(DTMAX, h * min(2.0, 0.9 * (tol / max(err, 1e-300)) ** (1 / 3))) if h == dt or err > 0 else dt
        if abs(t - nxt) < 1e-12:
            t = nxt; rows.append(M.diag_row(t, x, v) + [float(np.max(np.abs(a))), h]); nxt = round(nxt + SDT, 10)
    Z = np.array(rows)
    cols = cq6.COLS + ["max_acc", "dt"]
    np.savez(os.path.join(OUT, f"{tag}_series.npz"), cols=np.array(cols), data=Z)
    c = {k: i for i, k in enumerate(cols)}
    K, E = Z[:, c["K"]], Z[:, c["E"]]
    r = {"note": NOTE, "tag": tag, "N": N, "lambda": lam, "tol": tol, "status": status, "t_fail": tfail,
         "t_last": float(Z[-1, 0]), "steps": n, "rejects": nrej, "wall_s": round(time.time() - t0, 1),
         "dE_over_Kmax": float(np.max(np.abs(E - E[0])) / max(K.max(), 1e-300)),
         "rho_c_at_tc": float(np.interp(TC, Z[:, 0], Z[:, c["rho_c"]])) if Z[-1, 0] >= TC else None,
         "samples": {k: [float(z) for z in Z[:, c[k]]] for k in ("t", "rho_c", "Rv", "max_acc", "dt", "E", "K")}}
    w = Z[:, 0] >= W5 - 1e-9
    if status == "REACHED" and w.any():
        r["W5"] = {k: float(Z[w, c[k]].mean()) for k in ("rho_c", "w25", "w50", "w75", "w90", "Rv")}
        r["W5"]["Rv_min"], r["W5"]["Rv_max"] = float(Z[w, c["Rv"]].min()), float(Z[w, c["Rv"]].max())
    if status != "SIGTERM":
        json.dump(r, open(f, "w"))
    print(f"[{tag}] {status} t_fail={tfail} t_last={r['t_last']:.2f} steps={n} rej={nrej} dE={r['dE_over_Kmax']:.1e} "
          f"rho_c(tc)={r['rho_c_at_tc']} wall={r['wall_s']}s", flush=True)
    if status == "SIGTERM":
        sys.exit(3)
    return r


def at(r, k, tt):
    s = r["samples"]; i = int(round(tt / SDT))
    return s[k][i] if i < len(s["t"]) and abs(s["t"][i] - tt) < 1e-6 else None


def rel(a, b):
    return abs(a - b) / abs(b)


def main():
    LAMS, NS = (1e-8, 1e-7, 1e-6), (256, 512, 1024)
    mut = {N: run(N, 0.0, 1e-4, f"M{N}", tend=3.5) for N in NS}
    kz = {N: (r["t_fail"], bool(r["status"] == "CROSSED" and rel(r["t_fail"], TC) <= 0.01)) for N, r in mut.items()}
    kc = cq6.run(256, 1e-8, 1e-3, 3.4, "KCQ6_R256", OUT)
    kcq6a = bool(kc["status"] == "BLOW-UP" and abs(kc["t_fail"] - 3.216) <= 1e-3)
    R = {(l, N): run(N, l, 1e-4, f"L{l:g}_N{N}") for l in LAMS for N in NS}
    lad = {tol: (R[(1e-8, 512)] if tol == 1e-4 else run(512, 1e-8, tol, f"L1e-08_N512_tol{tol:g}")) for tol in (1e-3, 1e-4, 1e-5)}
    ref = {256: 5.561, 512: 5.596, 1024: 5.600}
    kcq6b = {N: (R[(1e-8, N)]["rho_c_at_tc"], bool(R[(1e-8, N)]["rho_c_at_tc"] and rel(R[(1e-8, N)]["rho_c_at_tc"], ref[N]) <= 0.01)) for N in NS}

    def ladder(p, q):
        tl = min(p["t_last"], q["t_last"]); worst = {"rho_c": 0, "Rv": 0, "max_acc": 0}
        for i in range(1, int(round(tl / SDT)) + 1):
            for k in worst:
                worst[k] = max(worst[k], rel(at(p, k, i * SDT), at(q, k, i * SDT)))
        ok = worst["rho_c"] <= 0.02 and worst["Rv"] <= 0.02 and worst["max_acc"] <= 0.10
        if p["status"] == "BLOW-UP" and q["status"] == "BLOW-UP":
            ok = ok and rel(p["t_fail"], q["t_fail"]) <= 0.02
        return {"t_common": tl, "worst": worst, "pass": bool(ok)}
    kdt = ladder(lad[1e-4], lad[1e-5]); kdt_coarse = ladder(lad[1e-3], lad[1e-4])
    controls = all(v[1] for v in kz.values()) and kcq6a and all(v[1] for v in kcq6b.values()) and kdt["pass"]
    per = {}
    for l in LAMS:
        rs = [R[(l, N)] for N in NS]
        ts = round(min(r["t_last"] for r in rs) / SDT) * SDT
        A = [at(r, "max_acc", ts) for r in rs]
        bu = all(r["status"] == "BLOW-UP" for r in rs) and rs[0]["t_fail"] > rs[1]["t_fail"] > rs[2]["t_fail"]
        gr = ts >= 3.3 - 1e-9 and A[1] / A[0] >= 1.5 and A[2] / A[1] >= 1.5
        d = {"t_star": ts, "A_at_t_star": A, "ratios": [A[1] / A[0], A[2] / A[1]],
             "status": [r["status"] for r in rs], "t_last": [r["t_last"] for r in rs], "t_fail": [r["t_fail"] for r in rs],
             "dE": [r["dE_over_Kmax"] for r in rs], "blowup_order": bool(bu), "acc_growth": bool(gr)}
        hi = rs[1:]
        if kdt["pass"] and (bu or gr):
            lab = "ILL-POSED"
        elif all(r["status"] == "REACHED" and r["dE_over_Kmax"] <= 1e-3 and "W5" in r for r in hi):
            conv = max(rel(hi[0]["W5"][k], hi[1]["W5"][k]) for k in ("rho_c", "w25", "w50", "w75", "w90", "Rv")) <= 0.05
            vir = all(0.9 <= r["W5"]["Rv_min"] and r["W5"]["Rv_max"] <= 1.1 for r in hi)
            lab = ("SETTLES" if vir else "OSCILLATES WITHOUT SETTLING") if conv else "NOT EVALUABLE"
        else:
            lab = "NOT EVALUABLE"
        d["label"] = lab; per[f"{l:g}"] = d
    labs = [per[f"{l:g}"]["label"] for l in LAMS]
    if not controls:
        label = "NOT EVALUABLE (control failed)"
    elif len(set(labs)) == 1:
        label = labs[0]
    else:
        label = "MIXED: " + "; ".join(f"{lb} at {l:g}" for l, lb in zip(LAMS, labs))
    out = {"note": NOTE, "criteria_commit": "2b11436345", "label": label, "controls_pass": controls,
           "K-ZEL": {str(k): v for k, v in kz.items()}, "MUTATE_pass": all(r["status"] == "CROSSED" for r in mut.values()),
           "K-CQ6a": {"t_fail": kc["t_fail"], "status": kc["status"], "pass": kcq6a},
           "K-CQ6b": {str(k): v for k, v in kcq6b.items()}, "K-dt": kdt, "K-dt_tol1e-3_vs_1e-4_reported": kdt_coarse,
           "ladder_runs": {f"{t:g}": {k: lad[t][k] for k in ("status", "t_fail", "t_last", "steps", "dE_over_Kmax")} for t in lad},
           "per_lambda": per,
           "runs": {r["tag"]: {k: v for k, v in r.items() if k != "samples"} for r in list(R.values()) + list(mut.values())}}
    json.dump(out, open(os.path.join(HERE, "cq8_results.json"), "w"), indent=1)
    print("[label]", label, flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "smoke":
        run(int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), "smoke", tend=float(sys.argv[5]))
    else:
        main()
