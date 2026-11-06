#!/usr/bin/env python3
"""AC10: nonlinear planar evolution of AC2q (and its v3s twin): cold khronon stream crossing a baryon sheet.

Criteria: FROZEN_CRITERIA.md (552db86f89). Reduction checked in s1_reduction.py (S1).
Dimensionless units: crossing-scale speed w = 1, K Sigma_b = 1 (tau_f = w/(K Sigma_b) = 1), K = 1, charges as K Pi tau_f^2.
Label force a = (M-1)/2 [D(<x) - D(>x)] - (1/2) erf(x/(sqrt2 w_b)) - gamma_hat d_x max(Pi, 0),
D = excess column, cell excess (Pi_0 - s^2 J) dq (AC2q) or Pi_0 dq (v3s, s = 0).
Run from the repo root (checkpointed per row under parts/; rerun resumes):
  nice -n 10 python3 action_search_2026_11_05/AC10_nonlinear_clock/ac10.py [--mutate] [--workers 8]
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, argparse, hashlib, time
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
X14 = os.path.join(ROOT, "rebuild_2026_10_22/X14_caustic_completion/x14_caustic_completion_results.json")
CL = 2.99792458e8; PC = 3.0857e16
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTAR = {"canonical": (21.7, 90.0), "alt": (22.9, 90.0)}
WB = 1e-3; X0 = (-3.0, -0.05); TMAX = 6.0; JTHR = 1e-3; JREG = 0.05; EDGE = 0.05
LADDER = (2000, 4000, 8000)


def run(N, M1, Pi0, s2, gam, sheet=1.0, jthr=JTHR, rtol=1e-10, atol=1e-12, want_traj=False):
    """Integrate N cells (N+1 labels). Returns fold time (or None), min interior J, max |v|, crossing data."""
    q = np.linspace(X0[0], X0[1], N + 1); dq = q[1] - q[0]
    i0, i1 = int(EDGE * N), int((1 - EDGE) * N)              # interior cells [i0, i1)
    y0 = np.concatenate([q, np.ones(N + 1)])
    bg_out = s2                                            # charge outside the stream (background clock; 0 for v3s)

    # A2-POST: the excess charge (Pi0 - s2) tapers smoothly to the background inside the excluded edge cells only
    # (removes the grid-scale stiffness force at a charge jump; interior cells keep Pi0 exactly)
    qc = 0.5 * (q[1:] + q[:-1]); span = q[-1] - q[0]; e = EDGE * span
    T = 0.5 * (np.tanh((qc - q[0] - 0.5 * e) / (0.1 * e)) - np.tanh((qc - q[-1] + 0.5 * e) / (0.1 * e)))
    Pic = s2 + (Pi0 - s2) * T                              # cell charge densities at t = 0
    mnode = np.zeros(N + 1); mnode[:-1] += Pic * dq / 2; mnode[1:] += Pic * dq / 2   # label (sheet-model) charges

    def rhs(t, y):
        x = y[:N + 1]; v = y[N + 1:]
        dx = np.diff(x); J = dx / dq
        # multistream-safe planar Gauss: excess column to the left in x (sorted), background s^2 subtracted over the
        # stream's extent; identical to the index-ordered cell sum before any crossing
        order = np.argsort(x, kind="stable")
        cs = np.cumsum(mnode[order]) - mnode[order] / 2
        left = np.empty(N + 1); left[order] = cs
        xmin, xmax = x.min(), x.max()
        cum = left - s2 * (x - xmin)
        Dtot = mnode.sum() - s2 * (xmax - xmin)
        a = M1 * (cum - Dtot / 2) - 0.5 * sheet * erf(x / (math.sqrt(2) * WB))
        if gam > 0:
            with np.errstate(divide="ignore", invalid="ignore"):
                Pi = np.where(J > 0, Pic / J, 0.0)         # pressure only in single-stream (unfolded) cells
            on = np.maximum(Pi, 0.0)
            onp = np.concatenate([[max(bg_out, 0.0)], on, [max(bg_out, 0.0)]])
            dxn = np.concatenate([[dx[0]], 0.5 * (dx[:-1] + dx[1:]), [dx[-1]]])
            dxn = np.where(np.abs(dxn) > 1e-12 * dq, np.abs(dxn), 1e-12 * dq)
            a = a - gam * (onp[1:] - onp[:-1]) / dxn
        return np.concatenate([v, a])

    def ev_fold(t, y):
        dx = np.diff(y[:N + 1]) / dq
        return dx[i0:i1].min() - jthr
    ev_fold.terminal = True; ev_fold.direction = -1

    def ev_all(t, y):                                      # A2-POST reading: first fold over all cells (non-terminal)
        return (np.diff(y[:N + 1]) / dq).min() - jthr
    ev_all.terminal = False; ev_all.direction = -1
    te = np.linspace(0, TMAX, 1201)
    sol = solve_ivp(rhs, (0, TMAX), y0, method="DOP853", rtol=rtol, atol=atol, t_eval=te, events=[ev_fold, ev_all],
                    dense_output=want_traj)
    Js = np.diff(sol.y[:N + 1], axis=0) / dq
    jmin = float(Js[i0:i1].min()) if Js.size else float("nan")
    vmax = float(np.abs(sol.y[N + 1:]).max())
    tf = float(sol.t_events[0][0]) if len(sol.t_events[0]) else None
    if tf is not None:
        jmin = min(jmin, jthr)
    tfa = float(sol.t_events[1][0]) if len(sol.t_events[1]) else None
    out = dict(N=N, t_fold=tf, t_fold_all=tfa, J_min=jmin, v_max=vmax, status=int(sol.status), nfev=int(sol.nfev))
    if want_traj:
        out["sol"] = sol; out["q"] = q; out["dq"] = dq; out["i0"] = i0
    return out


def label(r):
    if r["t_fold"] is not None:
        return "FOLD"
    return "REGULAR" if r["J_min"] >= JREG else "UNDECIDED"


def ladder(M1, Pi0, s2, gam, sheet=1.0):
    rungs = [run(N, M1, Pi0, s2, gam, sheet) for N in LADDER]
    labs = [label(r) for r in rungs]
    conv = len(set(labs)) == 1
    if labs[-1] == "FOLD" and conv:
        rel = abs(rungs[-1]["t_fold"] - rungs[-2]["t_fold"]) / rungs[-1]["t_fold"]
        conv = rel <= 1e-3
    else:
        rel = None
    fa = [r["t_fold_all"] for r in rungs]                 # A2-POST reading
    if all(v is not None for v in fa):
        rel_a = abs(fa[-1] - fa[-2]) / fa[-1]; lab_a = "FOLD" if rel_a <= 1e-3 else "NOT CONVERGED"
    elif all(v is None for v in fa):
        rel_a = None; lab_a = labs[-1] if conv else "NOT CONVERGED"
    else:
        rel_a = None; lab_a = "NOT CONVERGED"
    return dict(rungs=rungs, labels=labs, label=labs[-1] if conv else "NOT CONVERGED", rel_change=rel, converged=conv,
                label_all=lab_a, rel_change_all=rel_a)


def physical_rows():
    d = json.load(open(X14))["F5"]["numbers"]
    rows = []
    for foot, A0 in FOOT.items():
        Ks2 = 32 * math.pi * A0 ** 2 / CL ** 2             # K s^2 = 8 pi G rho_DE, rho_DE = a0^2/(kappa^2 c^2 G), s^2 = 2 rho_DE
        for r in d[foot]:
            for w in (68.75, 74.8):
                tau = w * 1e3 / (2 * r["g_m_s2"]); ell = w * 1e3 * tau
                for m1 in r["M_theta_minus_1_bracket"]:
                    for L in LSTAR[foot]:
                        gh = (L * PC) ** 2 / (2 * ell ** 2)
                        base = dict(foot=foot, r_kpc=r["r_kpc"], w_kms=w, M1=m1, Lstar_pc=L, tau_f_s=tau,
                                    Pi_ph=r["K_rho_ph_s-2"] * tau ** 2, s2=Ks2 * tau ** 2, gam=gh)
                        for kind in ("phantom", "clock_only", "soft"):
                            ph = {"phantom": base["Pi_ph"], "clock_only": 0.0, "soft": -base["Pi_ph"]}[kind]
                            rows.append(dict(base, kind=kind, model="AC2q", Pi0=ph + base["s2"], s2_use=base["s2"]))
                            rows.append(dict(base, kind=kind, model="v3s", Pi0=ph, s2_use=0.0))
    return rows


def stress_rows():
    rows = []
    for v in (0.4, 0.6):
        rows.append(dict(kind="stress_A1", model="v3s", M1=1.0, Pi0=v, s2_use=0.0, gam=0.0, tag=f"A1_{v}"))
    for v in (0.8, 1.2):
        rows.append(dict(kind="stress_A2", model="AC2q", M1=1.0, Pi0=v, s2_use=v, gam=0.0, tag=f"A2_{v}"))
    return rows


def key(row):
    return hashlib.sha1(json.dumps({k: row[k] for k in sorted(row) if k not in ("tag",)}, sort_keys=True).encode()).hexdigest()[:16]


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


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mutate", action="store_true"); ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--only", default=""); ap.add_argument("--subset", action="store_true")
    a = ap.parse_args()
    from multiprocessing import Pool
    pdir = "parts_MUTATE" if a.mutate else "parts"
    os.makedirs(os.path.join(HERE, pdir), exist_ok=True)
    if a.mutate:
        rows = [dict(kind="MUTATE_A_repulsive", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0, sheet=-1.0),
                dict(kind="MUTATE_B_mach0.3", model="AC2q", M1=1.0, Pi0=0.1, s2_use=0.1, gam=(1 / 0.3) ** 2 / 0.1)]
    else:
        rows = stress_rows() + physical_rows()
        if a.subset:                                       # declared information subset (README): 11 and 156 kpc,
            rows = [r for r in rows if r["kind"].startswith("stress") or (   # w 68.75, low M-1 bracket, Lstar minimum
                r["r_kpc"] in (11.0, 156.0) and r["w_kms"] == 68.75 and r["Lstar_pc"] < 50
                and r["M1"] == min(x["M1"] for x in physical_rows() if x["foot"] == r["foot"] and x["r_kpc"] == r["r_kpc"]))]
        rows.append(dict(kind="K1_zero_charge", model="v3s", M1=1.0, Pi0=0.0, s2_use=0.0, gam=0.0))
    for r in rows:
        r["_pdir"] = pdir
    with Pool(a.workers) as pool:
        res = []
        for i, o in enumerate(pool.imap_unordered(work, rows)):
            res.append(o)
            if i % 20 == 0:
                print(f"{i + 1}/{len(rows)} done", flush=True)
    print(f"all {len(res)} rows done", flush=True)


if __name__ == "__main__":
    main()
