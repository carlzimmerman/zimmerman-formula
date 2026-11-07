#!/usr/bin/env python3
"""TC1 N1 / KA3: AC10's 12-row AC2q subset rerun with AC2q stiffness and with the QX19 blend stiffness.

Criteria: CRITERIA.md (4f3d3efa6b). AC10's physics is imported read-only from
action_search_2026_11_05/AC10_nonlinear_clock/ac10.py; run() below is AC10's run() verbatim except for
(i) a stiffness hook (AC2q max(Pi,0) or QX19 b f'(Pi/b), b = s^2/2) and (ii) recording interior Sigma/X = 2 Pi/s^2
on the saved samples before the first fold. Checkpointed per run under runs/ (rerun resumes; SIGTERM-safe).
  nice -n 10 python3 closure_2026_11_06/TC1_sigma_x_condition/tc1_runs.py [--workers 4]
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, glob, time, argparse, hashlib
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "action_search_2026_11_05", "AC10_nonlinear_clock"))
import ac10  # noqa: E402  (read-only import: constants, physical_rows)

LADDER = (2000, 4000)


def blend_fp():
    """f'(q) of AC21 iter_6, built exactly as qx19.py does (exact rationals, integrated from f'')."""
    q = sp.Symbol("q", nonnegative=True)
    form = json.load(open(glob.glob(os.path.join(REPO, "action_search_2026_11_05/AC21_smooth_3d/iter_6*/form.json"))[0]))
    pieces = [(sp.Rational(a), sp.Rational(b), sp.sympify(e, locals={"q": q})) for a, b, e in form["pieces"]]
    pieces = pieces + [(sp.Integer(1), sp.oo, sp.Integer(1))]
    out, c1 = [], sp.Integer(0)
    for a, b, e in pieces:
        F1 = sp.integrate(e, (q, a, q)) + c1
        t = sp.Symbol("t")                                # shifted variable t = q - a: avoids float cancellation
        poly = sp.Poly(sp.expand(F1.subs(q, t + a)), t)
        cf = [float(c) for c in poly.all_coeffs()]       # Horner in t (np.polyval)
        out.append((float(a), float(b) if b != sp.oo else math.inf, (lambda cf_, a_: (lambda x: np.polyval(cf_, x - a_)))(cf, float(a))))
        if b != sp.oo:
            c1 = F1.subs(q, b)
    def fp(x):
        x = np.asarray(x, float); y = np.zeros_like(x)
        for a, b, fn in out:
            m = (x > a) & (x <= b) if a > 0 else (x > 0) & (x <= b)
            if m.any():
                y[m] = fn(x[m])
        return y
    return fp


FP = blend_fp()


def stiff(Pi, model, b):
    if model == "AC2q":
        return np.maximum(Pi, 0.0)
    return b * FP(Pi / b)                    # QX19: F'(Pi) = b f'(Pi/b); f' = 0 for q <= 0, f' = q for q >= 1


def run(N, M1, Pi0, s2, gam, model, sheet=1.0, jthr=ac10.JTHR, rtol=1e-10, atol=1e-12):
    X0, EDGE, WB, TMAX = ac10.X0, ac10.EDGE, ac10.WB, ac10.TMAX
    q = np.linspace(X0[0], X0[1], N + 1); dq = q[1] - q[0]
    i0, i1 = int(EDGE * N), int((1 - EDGE) * N)
    y0 = np.concatenate([q, np.ones(N + 1)])
    bg_out = s2
    b = s2 / 2.0                                         # b = X, X = s^2/2
    qc = 0.5 * (q[1:] + q[:-1]); span = q[-1] - q[0]; e = EDGE * span
    T = 0.5 * (np.tanh((qc - q[0] - 0.5 * e) / (0.1 * e)) - np.tanh((qc - q[-1] + 0.5 * e) / (0.1 * e)))
    Pic = s2 + (Pi0 - s2) * T
    mnode = np.zeros(N + 1); mnode[:-1] += Pic * dq / 2; mnode[1:] += Pic * dq / 2
    bgs = float(stiff(np.array([bg_out]), model, b)[0]) if bg_out > 0 else 0.0

    def rhs(t, y):
        x = y[:N + 1]; v = y[N + 1:]
        dx = np.diff(x); J = dx / dq
        order = np.argsort(x, kind="stable")
        cs = np.cumsum(mnode[order]) - mnode[order] / 2
        left = np.empty(N + 1); left[order] = cs
        xmin, xmax = x.min(), x.max()
        cum = left - s2 * (x - xmin)
        Dtot = mnode.sum() - s2 * (xmax - xmin)
        a = M1 * (cum - Dtot / 2) - 0.5 * sheet * erf(x / (math.sqrt(2) * WB))
        if gam > 0:
            with np.errstate(divide="ignore", invalid="ignore"):
                Pi = np.where(J > 0, Pic / J, 0.0)
            on = stiff(Pi, model, b)
            onp = np.concatenate([[bgs], on, [bgs]])
            dxn = np.concatenate([[dx[0]], 0.5 * (dx[:-1] + dx[1:]), [dx[-1]]])
            dxn = np.where(np.abs(dxn) > 1e-12 * dq, np.abs(dxn), 1e-12 * dq)
            a = a - gam * (onp[1:] - onp[:-1]) / dxn
        return np.concatenate([v, a])

    def ev_fold(t, y):
        return (np.diff(y[:N + 1]) / dq)[i0:i1].min() - jthr
    ev_fold.terminal = True; ev_fold.direction = -1

    def ev_all(t, y):
        return (np.diff(y[:N + 1]) / dq).min() - jthr
    ev_all.terminal = False; ev_all.direction = -1
    te = np.linspace(0, TMAX, 1201)
    sol = solve_ivp(rhs, (0, TMAX), y0, method="DOP853", rtol=rtol, atol=atol, t_eval=te, events=[ev_fold, ev_all])
    Js = np.diff(sol.y[:N + 1], axis=0) / dq
    tf = float(sol.t_events[0][0]) if len(sol.t_events[0]) else None
    tfa = float(sol.t_events[1][0]) if len(sol.t_events[1]) else None
    tcut = tfa if tfa is not None else (tf if tf is not None else sol.t[-1])
    m = sol.t < tcut                                     # samples strictly before the first fold
    Jin = Js[i0:i1, m]; Jall = Js[:, m]
    with np.errstate(divide="ignore", invalid="ignore"):
        rin = 2 * Pic[i0:i1, None] / (Jin * s2); rall = 2 * Pic[:, None] / (Jall * s2)   # Sigma/X = 2 Pi/s^2
    ok_in = Jin > 0; ok_all = Jall > 0
    def layer_frac(r, ok, bb):                           # fraction of cell-samples with 0 < Sigma < bb X
        return float(np.mean((r[ok] > 0) & (r[ok] < bb))) if ok.any() else float("nan")
    return dict(N=N, model=model, t_fold=tf, t_fold_all=tfa, n_samples=int(m.sum()),
                J_min=float(Js[i0:i1].min()), J_max_in_prefold=float(Jin.max()) if Jin.size else None,
                v_max=float(np.abs(sol.y[N + 1:]).max()), status=int(sol.status), nfev=int(sol.nfev),
                sx_in_min=float(rin[ok_in].min()), sx_in_max=float(rin[ok_in].max()),
                sx_all_min=float(rall[ok_all].min()), sx_all_max=float(rall[ok_all].max()),
                layer_in=layer_frac(rin, ok_in, 1.0), layer_all=layer_frac(rall, ok_all, 1.0),
                layer_in_b4=layer_frac(rin, ok_in, 4.0), layer_all_b4=layer_frac(rall, ok_all, 4.0))


def subset_rows():
    return [r for r in ac10.physical_rows() if r["model"] == "AC2q" and r["r_kpc"] in (11.0, 156.0)
            and r["w_kms"] == 68.75 and r["Lstar_pc"] < 50 and r["M1"] == min(
                x["M1"] for x in ac10.physical_rows() if x["foot"] == r["foot"] and x["r_kpc"] == r["r_kpc"])]


def jobs():
    out = []
    for r in subset_rows():
        for model in ("AC2q", "QX19"):
            for N in LADDER:
                out.append(dict(row=r, model=model, N=N))
    return out


def jkey(j):
    return hashlib.sha1(json.dumps(j, sort_keys=True, default=float).encode()).hexdigest()[:16]


def work(j):
    fn = os.path.join(HERE, "runs", jkey(j) + ".json")
    if os.path.exists(fn):
        return fn
    t0 = time.time(); r = j["row"]
    res = run(j["N"], r["M1"], r["Pi0"], r["s2_use"], r["gam"], j["model"])
    out = dict(job=j, **res, seconds=time.time() - t0)
    tmp = fn + ".tmp"; json.dump(out, open(tmp, "w"), default=float); os.replace(tmp, fn)
    return fn


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=4); a = ap.parse_args()
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    js = jobs()
    print(f"{len(subset_rows())} rows, {len(js)} runs", flush=True)
    from multiprocessing import Pool
    js.sort(key=lambda j: j["N"])
    with Pool(a.workers) as p:
        for fn in p.imap_unordered(work, js):
            print("done", os.path.basename(fn), flush=True)


if __name__ == "__main__":
    main()
