#!/usr/bin/env python3
"""SV3: successor to AC14 (planar AC2q fold vs v3s). Physics = AC10 (imported, unchanged in the interior).
Criteria: FROZEN_CRITERIA.md. Changes vs AC14, all declared there before any graded number:
  - integrator: implicit Radau IIA (order 5) with an analytic sparse Jacobian (rtol 1e-10, atol 1e-12, as AC14);
  - edge treatment E3: the excluded 5 % edge cells carry no stiffness (pressureless dust); the interior/edge
    interface uses a transmissive ghost (ghost pressure = adjacent interior cell's pressure). Variant E3b
    (linear-extrapolation ghost) is the K4 edge-sensitivity check;
  - per-run wall-time cap; per-rung checkpoints in parts/; SIGTERM checkpoints and exits.
Run from the repo root:
  nice -n 15 python3 action_search_2026_11_05/SV3_fold_implicit/sv3.py [--mutate] [--workers 3]
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, argparse, hashlib, time, signal
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
import scipy.sparse as sp
from scipy.integrate import solve_ivp
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "AC10_nonlinear_clock"))
import ac10  # noqa: E402  (physics, rows, constants: unchanged)

WB, X0, TMAX, JTHR, JREG, EDGE = ac10.WB, ac10.X0, ac10.TMAX, ac10.JTHR, ac10.JREG, ac10.EDGE
LADDER = (2000, 4000, 8000); EXTRA = 16000
RTOL, ATOL = 1e-10, 1e-12
CAP_RUN = 1500.0          # frozen per-run wall-time cap (s); a run hitting it -> row UNDECIDED (TIMEOUT)
SUBSET_K = 5              # frozen subset rule: every 5th stiffness-on AC2q row in ac10.physical_rows() order


class Timeout(Exception):
    pass


class Stop(Exception):
    pass


_STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: _STOP.__setitem__("flag", True))


def run(N, M1, Pi0, s2, gam, sheet=1.0, ghost="E3a", v_pert=None, jthr=JTHR, cap=CAP_RUN, want_traj=False):
    """AC10 label system with edge treatment E3 and Radau. ghost: 'E3a' transmissive, 'E3b' linear extrapolation,
    'VAC' vacuum (MUTATE-C only). v_pert = (A, k): initial v = 1 + A sin(k (q - q0)) (MUTATE-B only)."""
    q = np.linspace(X0[0], X0[1], N + 1); dq = q[1] - q[0]
    i0, i1 = int(EDGE * N), int((1 - EDGE) * N)              # interior cells [i0, i1)
    v0 = np.ones(N + 1)
    if v_pert is not None:
        v0 = 1.0 + v_pert[0] * np.sin(v_pert[1] * (q - X0[0]))
    y0 = np.concatenate([q, v0])
    qc = 0.5 * (q[1:] + q[:-1]); span = q[-1] - q[0]; e = EDGE * span
    T = 0.5 * (np.tanh((qc - q[0] - 0.5 * e) / (0.1 * e)) - np.tanh((qc - q[-1] + 0.5 * e) / (0.1 * e)))
    Pic = s2 + (Pi0 - s2) * T                              # AC10 A2-POST charge (gravity), unchanged
    mnode = np.zeros(N + 1); mnode[:-1] += Pic * dq / 2; mnode[1:] += Pic * dq / 2
    G = np.zeros(N)                                        # E3: stiffness only in interior cells with Pi > 0
    if gam > 0:
        G[i0:i1] = gam * np.maximum(Pic[i0:i1], 0.0) * dq  # P_c = G_c / dx_c  (= gam max(Pi,0) / J)
    press = bool(G.any())
    jn = np.arange(i0 + 1, i1)                              # nodes with two interior neighbour cells
    t_start = time.time()

    def pressure(x):
        dx = np.diff(x)
        P = np.zeros(N)
        P[i0:i1] = G[i0:i1] / dx[i0:i1]                     # interior J > 0 until the terminal fold event
        D = np.abs(x[2:] - x[:-2]) / 2                      # node spacing for nodes 1..N-1
        D = np.where(D > 1e-12 * dq, D, 1e-12 * dq)
        a = np.zeros(N + 1)
        a[jn] = -(P[jn] - P[jn - 1]) / D[jn - 1]
        if ghost == "E3b":                                  # linear-extrapolation ghosts at both interfaces
            gR = max(2 * P[i1 - 1] - P[i1 - 2], 0.0); gL = max(2 * P[i0] - P[i0 + 1], 0.0)
            a[i1] = -(gR - P[i1 - 1]) / D[i1 - 1]; a[i0] = -(P[i0] - gL) / D[i0 - 1]
        elif ghost == "VAC":                                # vacuum ghosts (P = 0 outside): MUTATE-C only
            a[i1] = -(0.0 - P[i1 - 1]) / D[i1 - 1]; a[i0] = -(P[i0] - 0.0) / D[i0 - 1]
        return a, dx, P, D

    def rhs(t, y):
        if _STOP["flag"]:
            raise Stop()
        if time.time() - t_start > cap:
            raise Timeout()
        x = y[:N + 1]; v = y[N + 1:]
        order = np.argsort(x, kind="stable")
        cs = np.cumsum(mnode[order]) - mnode[order] / 2
        left = np.empty(N + 1); left[order] = cs
        xmin, xmax = x.min(), x.max()
        cum = left - s2 * (x - xmin)
        Dtot = mnode.sum() - s2 * (xmax - xmin)
        a = M1 * (cum - Dtot / 2) - 0.5 * sheet * erf(x / (math.sqrt(2) * WB))
        if press:
            a = a + pressure(x)[0]
        return np.concatenate([v, a])

    rho = lambda x: np.exp(-x ** 2 / (2 * WB ** 2)) / (math.sqrt(2 * math.pi) * WB)
    I = sp.identity(N + 1, format="csr")

    def jac(t, y):
        """Analytic Jacobian: sheet + self-gravity (incl. the x_min/x_max columns) + pressure (banded).
        The sort-order jumps of the planar Gauss sum are delta functions and are omitted (Newton only)."""
        x = y[:N + 1]
        diag = -sheet * rho(x) - M1 * s2
        rows = [np.arange(N + 1)]; cols = [np.arange(N + 1)]; vals = [diag]
        if s2 != 0.0 and M1 != 0.0:
            imin, imax = int(np.argmin(x)), int(np.argmax(x))
            rows += [np.arange(N + 1), np.arange(N + 1)]; cols += [np.full(N + 1, imin), np.full(N + 1, imax)]
            vals += [np.full(N + 1, M1 * s2 * 0.5), np.full(N + 1, M1 * s2 * 0.5)]
        if press:
            _, dx, P, D = pressure(x)
            dPr = np.zeros(N); dPl = np.zeros(N)            # dP_c/dx_{c+1}, dP_c/dx_c
            dPr[i0:i1] = -G[i0:i1] / dx[i0:i1] ** 2; dPl[i0:i1] = -dPr[i0:i1]
            j = jn; Dj = D[j - 1]; dP = P[j] - P[j - 1]
            rows += [j, j, j]; cols += [j + 1, j, j - 1]
            vals += [-dPr[j] / Dj + dP / Dj ** 2 * 0.5,
                     -(dPl[j] - dPr[j - 1]) / Dj,
                     dPl[j - 1] / Dj - dP / Dj ** 2 * 0.5]
        A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N + 1, N + 1))
        return sp.bmat([[None, I], [A, None]], format="csc")

    def ev_fold(t, y):
        return (np.diff(y[:N + 1]) / dq)[i0:i1].min() - jthr
    ev_fold.terminal = True; ev_fold.direction = -1

    def ev_reg(t, y):
        return (np.diff(y[:N + 1]) / dq)[i0:i1].min() - JREG
    ev_reg.terminal = False; ev_reg.direction = -1
    te = np.linspace(0, TMAX, 241)
    t0 = time.time(); status_note = None
    try:
        sol = solve_ivp(rhs, (0, TMAX), y0, method="Radau", rtol=RTOL, atol=ATOL, jac=jac, t_eval=te,
                        events=[ev_fold, ev_reg], dense_output=want_traj)
    except Timeout:
        return dict(N=N, ghost=ghost, t_fold=None, J_min=None, v_max=None, status=-9, note="TIMEOUT",
                    seconds=time.time() - t0)
    Js = np.diff(sol.y[:N + 1], axis=0) / dq
    jmin = float(Js[i0:i1].min()) if Js.size else float("nan")
    vmax = float(np.abs(sol.y[N + 1:]).max()) if Js.size else float("nan")
    tf = float(sol.t_events[0][0]) if len(sol.t_events[0]) else None
    treg = float(sol.t_events[1][0]) if len(sol.t_events[1]) else None
    icell = None
    if tf is not None:
        jmin = min(jmin, jthr)
        yf = sol.y_events[0][0]; icell = int(np.argmin((np.diff(yf[:N + 1]) / dq)[i0:i1]) + i0)
        vmax = max(vmax, float(np.abs(yf[N + 1:]).max()))
    elif treg is not None:
        jmin = min(jmin, JREG)
    out = dict(N=N, ghost=ghost, t_fold=tf, t_below_Jreg=treg, fold_cell_frac=(icell / N if icell is not None else None),
                J_min=jmin, v_max=vmax, status=int(sol.status), nfev=int(sol.nfev), njev=int(sol.njev),
                nlu=int(sol.nlu), seconds=time.time() - t0, note=status_note)
    if want_traj:
        out.update(sol=sol, q=q, dq=dq, i0=i0, i1=i1)
    return out


def label(r):
    if r.get("note") == "TIMEOUT":
        return "UNDECIDED"
    if r["t_fold"] is not None:
        return "FOLD"
    return "REGULAR" if (r["status"] == 0 and r["t_below_Jreg"] is None and r["J_min"] >= JREG) else "UNDECIDED"


def judge(a, b):
    la, lb = label(a), label(b)
    if la != lb or la == "UNDECIDED":
        return False, None
    if la == "FOLD":
        rel = abs(b["t_fold"] - a["t_fold"]) / b["t_fold"]; return rel <= 1e-3, rel
    return True, None


def key(row):
    return hashlib.sha1(json.dumps({k: row[k] for k in sorted(row) if k not in ("tag", "_pdir")},
                                   sort_keys=True).encode()).hexdigest()[:16]


def rung(pdir, k, row, N, ghost="E3a"):
    fn = os.path.join(pdir, f"{k}_N{N}_{ghost}.json")
    if os.path.exists(fn):
        return json.load(open(fn))
    r = run(N, row["M1"], row["Pi0"], row["s2_use"], row["gam"], row.get("sheet", 1.0), ghost=ghost,
            v_pert=row.get("v_pert"))
    tmp = fn + ".tmp"; json.dump(r, open(tmp, "w"), default=float); os.replace(tmp, fn)
    return r


def stiff_on(row):
    return row["gam"] > 0 and row["Pi0"] > 0


def work(row):
    pdir = os.path.join(HERE, row.pop("_pdir")); k = key(row)
    fn = os.path.join(pdir, k + ".json")
    if os.path.exists(fn):
        return json.load(open(fn))
    try:
        rungs = [rung(pdir, k, row, N) for N in LADDER]
        labs = [label(r) for r in rungs]
        ok, rel = judge(rungs[1], rungs[2]); ok = ok and labs[0] == labs[1] == labs[2]
        extra = False
        if not ok and "UNDECIDED" not in labs:
            rungs.append(rung(pdir, k, row, EXTRA)); labs.append(label(rungs[-1])); extra = True
            ok, rel = judge(rungs[2], rungs[3])
        timeout = any(r.get("note") == "TIMEOUT" for r in rungs)
        lab = labs[-1] if ok else ("UNDECIDED" if ("UNDECIDED" in labs[-2:] or timeout) else "NOT CONVERGED")
        k4 = None
        if ok and stiff_on(row) and not row.get("no_k4"):   # K4 edge sensitivity at the deciding rung
            rb = rung(pdir, k, row, rungs[-1]["N"], ghost="E3b")
            lb = label(rb); la = labs[-1]
            relb = (abs(rb["t_fold"] - rungs[-1]["t_fold"]) / rungs[-1]["t_fold"]) if (la == lb == "FOLD") else None
            k4ok = (la == lb) and (relb is None or relb <= 1e-3)
            k4 = dict(N=rb["N"], label_E3b=lb, rel=relb, ok=k4ok)
            if not k4ok:
                lab = "UNDECIDED"                            # edge-sensitive
    except Stop:
        return None
    out = dict(row=row, rungs=rungs, labels=labs, label=lab, rel_change=rel, converged=ok, extra_rung=extra,
               timeout=timeout, K4=k4)
    tmp = fn + ".tmp"; json.dump(out, open(tmp, "w"), default=float); os.replace(tmp, fn)
    return out


def subset_rows():
    phys = ac10.physical_rows()
    on = [r for r in phys if r["model"] == "AC2q" and stiff_on(r)]
    pick = on[::SUBSET_K]
    tk = lambda r: (r["foot"], r["r_kpc"], r["w_kms"], r["M1"], r["Lstar_pc"], r["kind"])
    want = {tk(r) for r in pick}
    twins = [r for r in phys if r["model"] == "v3s" and tk(r) in want]
    return pick, twins


def stress_rows():
    rows = []
    for v in (0.2, 1.0):
        rows.append(dict(kind="stress_A1", model="v3s", M1=1.0, Pi0=v, s2_use=0.0, gam=0.0, tag=f"A1_{v}"))
    for v in (0.4, 2.0):
        rows.append(dict(kind="stress_A2", model="AC2q", M1=1.0, Pi0=v, s2_use=v, gam=0.0, tag=f"A2_{v}"))
    return rows


# MUTATE-B (power gate): acoustic standing wave, no sheet, no self-gravity, Mach 0.3, dust fold time 5.5
KB = 2 * math.pi * 2 / (X0[1] - X0[0]); AB = 1 / (5.5 * KB); C0B = AB / 0.3; PIB = 0.1; GAMB = C0B ** 2 / PIB


def mutate_rows():
    return [dict(kind="MUTATE_A_repulsive", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0, sheet=-1.0),
            dict(kind="MUTATE_B_acoustic_mach0.3", model="v3s", M1=0.0, Pi0=PIB, s2_use=0.0, gam=GAMB, sheet=0.0,
                 v_pert=[AB, KB], no_k4=True),
            dict(kind="MUTATE_B_dust_twin", model="v3s", M1=0.0, Pi0=PIB, s2_use=0.0, gam=0.0, sheet=0.0,
                 v_pert=[AB, KB])]


def all_rows():
    pick, twins = subset_rows()
    rows = stress_rows() + pick + twins
    rows.append(dict(kind="K1_zero_charge", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0))
    return sorted(rows, key=lambda r: -r["gam"] * max(r["Pi0"], 0.0))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mutate", action="store_true")
    ap.add_argument("--workers", type=int, default=3); ap.add_argument("--probe", action="store_true")
    ap.add_argument("--reverse", action="store_true")  # scheduling only: a second process takes rows from the other end
    a = ap.parse_args()
    if a.probe:                       # timing probe on a synthetic row NOT in the grid; prints cost only
        for N in (2000, 8000):
            o = run(N, 0.5, 0.03, 1e-4, 3e-5)
            print(N, {k: o[k] for k in ("status", "nfev", "njev", "nlu", "seconds")}, flush=True)
        return
    from multiprocessing import Pool
    pdir = "parts_MUTATE" if a.mutate else "parts"
    os.makedirs(os.path.join(HERE, pdir), exist_ok=True)
    rows = mutate_rows() if a.mutate else all_rows()
    if a.reverse:
        rows = rows[::-1]
    for r in rows:
        r["_pdir"] = pdir
    signal.signal(signal.SIGTERM, lambda *x: _STOP.__setitem__("flag", True))
    with Pool(min(a.workers, 3)) as pool:
        n = 0
        for o in pool.imap_unordered(work, rows):
            n += 1
            print(f"{n}/{len(rows)} done" + ("" if o else " (stopped, resumable)"), flush=True)
    print(f"all {len(rows)} rows done", flush=True)


if __name__ == "__main__":
    main()
