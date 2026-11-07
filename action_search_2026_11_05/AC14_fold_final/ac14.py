#!/usr/bin/env python3
"""AC14: final label for AC2q's planar fold vs v3s. Physics = AC10 (imported, unchanged); declared device E1
(stiffness taper inside the excluded edge cells only); interior first-fold reading; all 240 + 240 rows.
Criteria: FROZEN_CRITERIA.md (ad9d747016). Checkpointed per row in parts/ (rerun resumes).
Run from the repo root:
  nice -n 10 python3 action_search_2026_11_05/AC14_fold_final/ac14.py [--mutate] [--workers 8] [--test]
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, argparse, hashlib, time
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "AC10_nonlinear_clock"))
import ac10  # noqa: E402  (physics, rows, constants: unchanged)

WB, X0, TMAX, JTHR, JREG, EDGE = ac10.WB, ac10.X0, ac10.TMAX, ac10.JTHR, ac10.JREG, ac10.EDGE
LADDER = (2000, 4000, 8000); EXTRA = 16000


def taper(q):
    qc = 0.5 * (q[1:] + q[:-1]); span = q[-1] - q[0]; e = EDGE * span
    return 0.5 * (np.tanh((qc - q[0] - 0.5 * e) / (0.1 * e)) - np.tanh((qc - q[-1] + 0.5 * e) / (0.1 * e)))


def run(N, M1, Pi0, s2, gam, sheet=1.0, jthr=JTHR, rtol=1e-10, atol=1e-12, want_traj=False, e2=False):
    """AC10's run with E1: gamma_cell = gam * T(q) (same tanh profile as AC10's edge charge taper)."""
    q = np.linspace(X0[0], X0[1], N + 1); dq = q[1] - q[0]
    i0, i1 = int(EDGE * N), int((1 - EDGE) * N)
    y0 = np.concatenate([q, np.ones(N + 1)])
    T = taper(q)
    Pic = s2 + (Pi0 - s2) * T
    mnode = np.zeros(N + 1); mnode[:-1] += Pic * dq / 2; mnode[1:] += Pic * dq / 2
    gcell = gam * T
    edge = np.ones(N, bool); edge[i0:i1] = False

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
            on = gcell * np.maximum(Pi, 0.0)
            if e2:                                         # E2-POST: edge cells only, pressure off smoothly below 10 J_thr
                z = np.clip((J - jthr) / (9 * jthr), 0.0, 1.0); wJ = z * z * (3 - 2 * z)
                on = np.where(edge, on * wJ, on)
            onp = np.concatenate([[0.0], on, [0.0]])
            dxn = np.concatenate([[dx[0]], 0.5 * (dx[:-1] + dx[1:]), [dx[-1]]])
            dxn = np.where(np.abs(dxn) > 1e-12 * dq, np.abs(dxn), 1e-12 * dq)
            a = a - (onp[1:] - onp[:-1]) / dxn
        return np.concatenate([v, a])

    def ev_fold(t, y):
        return (np.diff(y[:N + 1]) / dq)[i0:i1].min() - jthr
    ev_fold.terminal = True; ev_fold.direction = -1
    te = np.linspace(0, TMAX, 1201)
    sol = solve_ivp(rhs, (0, TMAX), y0, method="DOP853", rtol=rtol, atol=atol, t_eval=te, events=[ev_fold],
                    dense_output=want_traj)
    Js = np.diff(sol.y[:N + 1], axis=0) / dq
    jmin = float(Js[i0:i1].min()) if Js.size else float("nan")
    vmax = float(np.abs(sol.y[N + 1:]).max())
    tf = float(sol.t_events[0][0]) if len(sol.t_events[0]) else None
    icell = None
    if tf is not None:
        jmin = min(jmin, jthr)
        yf = sol.y_events[0][0]; icell = int(np.argmin((np.diff(yf[:N + 1]) / dq)[i0:i1]) + i0)
    out = dict(N=N, t_fold=tf, fold_cell_frac=(icell / N if icell is not None else None), J_min=jmin, v_max=vmax,
               status=int(sol.status), nfev=int(sol.nfev))
    if want_traj:
        out.update(sol=sol, q=q, dq=dq, i0=i0, i1=i1)
    return out


def label(r):
    if r["t_fold"] is not None:
        return "FOLD"
    # frozen: REGULAR only if interior J >= J_reg all the way to t_max (status 0); a solver stop is UNDECIDED
    return "REGULAR" if (r["J_min"] >= JREG and r["status"] == 0) else "UNDECIDED"


def judge(a, b):
    la, lb = label(a), label(b)
    if la != lb:
        return False, None
    if la == "FOLD":
        rel = abs(b["t_fold"] - a["t_fold"]) / b["t_fold"]; return rel <= 1e-3, rel
    return True, None


def ladder(M1, Pi0, s2, gam, sheet=1.0):
    rungs = [run(N, M1, Pi0, s2, gam, sheet) for N in LADDER]
    labs = [label(r) for r in rungs]
    ok, rel = judge(rungs[1], rungs[2]); ok = ok and labs[0] == labs[1] == labs[2]
    extra = False
    if not ok:
        rungs.append(run(EXTRA, M1, Pi0, s2, gam, sheet)); labs.append(label(rungs[-1])); extra = True
        ok, rel = judge(rungs[2], rungs[3])
    lab = labs[-1] if ok else "NOT CONVERGED"
    return dict(rungs=rungs, labels=labs, label=lab, rel_change=rel, converged=ok, extra_rung=extra)


def stress_rows():
    rows = []
    for v in (0.2, 1.0):
        rows.append(dict(kind="stress_A1", model="v3s", M1=1.0, Pi0=v, s2_use=0.0, gam=0.0, tag=f"A1_{v}"))
    for v in (0.4, 2.0):
        rows.append(dict(kind="stress_A2", model="AC2q", M1=1.0, Pi0=v, s2_use=v, gam=0.0, tag=f"A2_{v}"))
    return rows


def key(row):
    return hashlib.sha1(json.dumps({k: row[k] for k in sorted(row) if k not in ("tag", "_pdir")},
                                   sort_keys=True).encode()).hexdigest()[:16]


def work(row):
    pdir = os.path.join(HERE, row.pop("_pdir"))
    fn = os.path.join(pdir, key(row) + ".json")
    if os.path.exists(fn):
        return json.load(open(fn))
    t0 = time.time()
    lad = ladder(row["M1"], row["Pi0"], row["s2_use"], row["gam"], row.get("sheet", 1.0))
    out = dict(row=row, **lad, seconds=time.time() - t0)
    tmp = fn + ".tmp"
    json.dump(out, open(tmp, "w"), default=float); os.replace(tmp, fn)
    return out


def all_rows(mutate):
    if mutate:
        return [dict(kind="MUTATE_A_repulsive", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0, sheet=-1.0),
                dict(kind="MUTATE_B_mach0.3", model="AC2q", M1=1.0, Pi0=0.1, s2_use=0.1, gam=(1 / 0.3) ** 2 / 0.1)]
    rows = stress_rows() + ac10.physical_rows()
    rows.append(dict(kind="K1_zero_charge", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0))
    # slowest first (pressure on, strongest stiffness) so the tail is short
    return sorted(rows, key=lambda r: -r["gam"] * max(r["Pi0"], 0.0))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mutate", action="store_true")
    ap.add_argument("--workers", type=int, default=8); ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    if a.test:                                             # timing probe only, writes nothing
        r = [x for x in ac10.physical_rows() if x["model"] == "AC2q" and x["kind"] == "phantom"][0]
        t0 = time.time(); o = run(2000, r["M1"], r["Pi0"], r["s2_use"], r["gam"])
        print({k: v for k, v in o.items()}, f"{time.time() - t0:.1f}s"); return
    from multiprocessing import Pool
    pdir = "parts_MUTATE" if a.mutate else "parts"
    os.makedirs(os.path.join(HERE, pdir), exist_ok=True)
    rows = all_rows(a.mutate)
    for r in rows:
        r["_pdir"] = pdir
    with Pool(a.workers) as pool:
        n = 0
        for o in pool.imap_unordered(work, rows):
            n += 1
            if n % 20 == 0 or n == len(rows):
                print(f"{n}/{len(rows)} done", flush=True)
    print(f"all {len(rows)} rows done", flush=True)


if __name__ == "__main__":
    main()
