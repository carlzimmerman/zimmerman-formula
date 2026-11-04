#!/usr/bin/env python3
"""V3X W2: C6's in-window Route N ladder (L* = 24 pc), closed with a lower-memory linear solver inside C6's Newton loop.

Criteria: FROZEN_CRITERIA.md (859c76bec3). Solver: v3x_solver.py (C6/D7d code imported read-only, no bytecode written).
Amendment A1 (disclosed in README): every Newton step here uses a diagonal shift mu = 1e-12 on the w rows of C6's
row-scaled Jacobian and 3 polish steps after the residual first drops below 1e-9 (both methods alike).
Run:  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 v3x_w2_ladder.py      (V3X_MUTATE=noscreen: screening removed)
Each solve runs in its own forked child under a 0.85e9-byte RSS watchdog (polled every 0.1 s). RSS and timing go to a side file / stderr.
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, time, resource, subprocess, warnings
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
warnings.filterwarnings("ignore")
import numpy as np
import multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import v3x_solver as V
C, S = V.C, V.S
MUT = os.environ.get("V3X_MUTATE", "")
if MUT not in ("", "noscreen"):
    sys.exit(f"unknown V3X_MUTATE={MUT}")
TAG = "_MUTATE" if MUT else ""
OUT, CHK, SIDE = [], {}, {}
RES = {"lane": "V3X_v3s_close_undecided", "part": "W2", "criteria": "859c76bec3", "mutate": MUT or None,
       "amendment_A1": "diagonal shift mu = 1e-12 on the w rows of the row-scaled Jacobian; 3 polish Newton steps"}
t0 = time.time()
MU, POLISH, MU_NOISE = 1e-12, 3, 1e-10
RSS_KILL = 0.85e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def T(s):
    print(f"  [{s}; {time.time() - t0:.0f}s]", file=sys.stderr, flush=True)


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


def J(*p): return json.load(open(os.path.join(ROOT, *p)))


GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16
R_SAT = 9.58 * AU
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
d7b = J("doors_push_2026_10_22", "D7b_cassini_Q2", "d7b_cassini_q2_results.json")
GE = {f: d7b["grid"][f]["none"]["E2"]["ge_total"] for f in FOOT}
V3W = J("rebuild_2026_10_22", "V3W_v3s_weak_spots", "w2_c6_rerun.json")
C6PJ = J("rebuild_2026_10_22", "C6P_cassini_high_precision", "c6p_cassini_hp.json")
RQS = [1.0, 10.0, 100.0]                       # x r_Saturn; graded = 100
GRADED = 2
def rM_of(a0): return math.sqrt(GM / a0)


def _solve(Lam, xe, a0, gres, method, permc, mu, conn):
    try:
        g = V.grid(Lam, gres)
        U, fin, it = V.solve_v(g, Lam, xe, method=method, permc=permc, mu=mu, polish=POLISH)
        q = [float(-S.q2_raw(g, U[0], rq * R_SAT / rM_of(a0)) * a0 / rM_of(a0)) for rq in RQS]
        conn.send(dict(ok=True, Q=q, residual=float(fin), iterations=int(it), N=int(g.N), Nr=int(g.Nr),
                       rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1.0 if sys.platform == "darwin" else 1e-3)))
    except Exception as ex:                    # reported, not hidden
        conn.send(dict(ok=False, error=f"{type(ex).__name__}: {ex}"))
    conn.close()


def run(Lam, xe, a0, gres, method="A", permc="COLAMD", mu=MU, label=""):
    """one solve in a forked child; the parent kills it if its RSS passes RSS_KILL."""
    ctx = mp.get_context("fork")
    a, b = ctx.Pipe(False)
    p = ctx.Process(target=_solve, args=(Lam, xe, a0, gres, method, permc, mu, b))
    t1 = time.time(); p.start(); b.close()
    peak, killed = 0.0, False
    while p.is_alive():
        if a.poll(0.1):
            break
        try:
            r = float(subprocess.run(["ps", "-o", "rss=", "-p", str(p.pid)], capture_output=True, text=True).stdout.strip() or 0) * 1024
        except ValueError:
            r = 0.0
        peak = max(peak, r)
        if r > RSS_KILL:
            p.kill(); killed = True; break
    out = a.recv() if (not killed and a.poll(5.0)) else dict(ok=False, error="killed at the RSS line" if killed else "no result")
    p.join()
    out["rss_bytes"] = max(peak, out.get("rss", 0.0)); out.pop("rss", None)
    out["killed"] = killed
    SIDE[label] = dict(rss_bytes=out["rss_bytes"], seconds=round(time.time() - t1, 1), killed=killed)
    T(f"{label}: {'ok' if out.get('ok') else out.get('error')} RSS {out['rss_bytes'] / 1e9:.2f} GB")
    return out


def p_obs(d12, d23, n):
    h = [1.0 / v for v in n]
    f = lambda p: (h[1] ** p - h[2] ** p) / (h[0] ** p - h[1] ** p) - d23 / d12
    lo, hi = 0.05, 12.0
    if f(lo) * f(hi) > 0:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)


def rich(q2, q3, n2, n3, p=2.0):
    return q3 + (q3 - q2) / ((n3 / n2) ** p - 1)


P("=" * 100)
P("V3X W2: C6's in-window ladder at L* = 24 pc, lower-memory Newton (block-tridiagonal out-of-core LU)"
  + ("  [MUTATE: screening removed]" if MUT else ""))
P("kappa = 1/2 FITTED; footings never pooled; adopts nothing; not theory closed.")
P(f"Amendment A1: shift mu = {MU:g} on the w rows, {POLISH} polish steps; C6's residual/scaling/line search/tolerance 1e-9 unchanged.")
P("=" * 100)
LADDER = [(40, 64), (50, 80), (60, 96), (70, 112)]
KA = [(30, 48), (40, 64)]
cells = {}; labels = {}
for f, A0 in FOOT.items():
    xe = GE[f] / A0; rM = rM_of(A0)
    Lam = 24 * PC / rM
    Lam_run = 0.0 if MUT else Lam
    F = float(C.routeF_Q2(GM, Lam * rM, xe, 0.0))
    cell = dict(Lam=Lam, x_e=xe, routeF=F)
    P(f"\n[{f}] a0 = {A0:.5g}, x_e = {xe:.6f}, Lambda = {Lam:.4f}{' (run at 0: AQUAL)' if MUT else ''}; Route F Q2 = {F:.6e} s^-2")
    sols = {}
    for gres in sorted(set(LADDER + ([] if MUT else KA))):
        o = run(Lam_run, xe, A0, gres, "A", label=f"{f}|A|{gres}")
        sols[gres] = o
        if o.get("ok"):
            P(f"  A {str(gres):10s} N {o['N']:7d}: Q2 @ 1, 10, 100 r_Sat = " + ", ".join(f"{v:.8e}" for v in o["Q"]) +
              f"; residual {o['residual']:.2e}, Newton steps {o['iterations']}")
        else:
            P(f"  A {str(gres):10s}: {o['error']}")
    cell["A"] = {str(k): {kk: vv for kk, vv in v.items() if kk not in ("rss_bytes", "killed")} for k, v in sols.items()}
    # ------------------------------------------------ K1: V3W's rungs
    if not MUT:
        v3 = V3W["C6prime"][f"{f}|L24pc"]["Q_by_rung_by_radius"]          # rungs (20,32), (30,48), (40,64)
        k1 = {}
        for gres, row in zip(KA, v3[1:]):
            o = sols[gres]
            k1[str(gres)] = [abs(a / b - 1) if o.get("ok") else None for a, b in zip(o.get("Q", [np.nan] * 3), row)]
        worst = {r: max(k1[str(gr)][j] for gr in KA) for j, r in enumerate(("1 r_Sat", "10 r_Sat", "100 r_Sat"))}
        cell["K1"] = dict(rel_by_rung=k1, worst_by_radius=worst)
        ok_k1 = all(v is not None and v <= 1e-6 for v in worst.values())
        check(f"W2-K1 [{f}]", ok_k1, "Method A vs V3W's committed Q2 at (30,48), (40,64), worst rel by radius: " +
              ", ".join(f"{k} {v:.2e}" for k, v in worst.items()) + " (line <= 1e-6 at all three radii, as frozen)")
        # ------------------------------------------------ K2: Method B cross-check where it fits
        k2 = {}
        for gres in [(30, 48), (40, 64), (50, 80)]:
            for permc in (["MMD_AT_PLUS_A", "COLAMD"] if gres == (30, 48) else ["COLAMD"]):
                ob = run(Lam, xe, A0, gres, "B", permc=permc, label=f"{f}|B-{permc}|{gres}")
                if ob.get("ok") and sols[gres].get("ok"):
                    d = abs(ob["Q"][GRADED] / sols[gres]["Q"][GRADED] - 1)
                    k2[f"{gres}|{permc}"] = dict(Q=ob["Q"], residual=ob["residual"], rel_vs_A_graded=d)
                    P(f"  B {permc:13s} {str(gres):10s}: Q2 @ 100 r_Sat {ob['Q'][GRADED]:.8e}; vs A {d:.2e}; residual {ob['residual']:.2e}")
                else:
                    k2[f"{gres}|{permc}"] = dict(not_run=ob.get("error"))
                    P(f"  B {permc:13s} {str(gres):10s}: not run to completion ({ob.get('error')})")
        cell["K2"] = k2
        ran = [v["rel_vs_A_graded"] for v in k2.values() if "rel_vs_A_graded" in v]
        ok_k2 = bool(ran) and max(ran) <= 1e-6
        check(f"W2-K2 [{f}]", ok_k2, f"A vs B at the graded radius where B completed ({len(ran)} solves): max rel {max(ran) if ran else float('nan'):.2e} (<= 1e-6)")
        # ------------------------------------------------ float64 noise: same rung at mu = 1e-10 (reported)
        noise = {}
        for gres in LADDER[1:]:
            on = run(Lam, xe, A0, gres, "A", mu=MU_NOISE, label=f"{f}|A-mu1e-10|{gres}")
            if on.get("ok") and sols[gres].get("ok"):
                noise[str(gres)] = abs(on["Q"][GRADED] / sols[gres]["Q"][GRADED] - 1)
        cell["mu_noise_rel_graded"] = noise
        P("  shift sensitivity (mu 1e-10 vs 1e-12) at 100 r_Sat: " + ", ".join(f"{k} {v:.1e}" for k, v in noise.items()))
    # ------------------------------------------------ the ladder and its grade
    ok_all = all(sols[g_].get("ok") for g_ in LADDER)
    if ok_all:
        q = np.array([sols[g_]["Q"][GRADED] for g_ in LADDER[1:]])       # 50, 60, 70
        n = [g_[0] for g_ in LADDER[1:]]
        conv = all(sols[g_]["residual"] < 1e-9 for g_ in LADDER)
        d12, d23 = abs(q[1] - q[0]), abs(q[2] - q[1])
        R2 = rich(q[1], q[2], n[1], n[2])
        po = p_obs(d12, d23, n)
        Rp = rich(q[1], q[2], n[1], n[2], po) if np.isfinite(po) else float("nan")
        mem = max(SIDE[f"{f}|A|{g_}"]["rss_bytes"] for g_ in LADDER) < 1e9 and not any(sols[g_]["killed"] for g_ in LADDER)
        lad = conv and d23 < d12 and abs(R2 / q[2] - 1) < 2e-2
        nf = abs(R2 / F - 1) < 5e-2 and (R2 > 0) == (F > 0)
        guard = np.isfinite(po) and 1.5 <= po <= 2.5
        q40 = sols[(40, 64)]["Q"][GRADED]
        cell.update(q_graded=dict(zip([str(g_) for g_ in LADDER], [q40] + q.tolist())), d12=d12, d23=d23,
                    d23_over_d12=d23 / d12, d23_over_d12_order2=((1 / n[1] ** 2 - 1 / n[2] ** 2) / (1 / n[0] ** 2 - 1 / n[1] ** 2)),
                    richardson2=R2, rich2_vs_finest=R2 / q[2] - 1, p_obs=po, richardson_pobs=Rp,
                    rich_pobs_vs_finest=(Rp / q[2] - 1) if np.isfinite(Rp) else None, N_over_F=R2 / F,
                    per_radius_N_over_F=[rich(sols[(60, 96)]["Q"][j], sols[(70, 112)]["Q"][j], 60, 70) / F for j in range(3)],
                    lines=dict(a_converged=conv, b_ladder=lad, c_routeF=nf, d_memory=mem, guard=guard))
        P(f"  ladder @ 100 r_Sat (40..70): " + ", ".join(f"{v:.8e}" for v in [q40] + q.tolist()))
        P(f"  d12 (50->60) {d12:.4e}, d23 (60->70) {d23:.4e}, ratio {d23 / d12:.4f} (order 2 expects {cell['d23_over_d12_order2']:.4f}); "
          f"p_obs {po:.3f}")
        P(f"  Richardson (order 2, 60/70) {R2:.6e}: vs finest {R2 / q[2] - 1:+.3e} (line 2e-2); at p_obs {Rp:.6e} ({(cell['rich_pobs_vs_finest'] if cell['rich_pobs_vs_finest'] is not None else float('nan')):+.3e}); "
          f"N/F {R2 / F:.5f} (line 5e-2); N/F at 1, 10, 100 r_Sat " + ", ".join(f"{v:.4f}" for v in cell["per_radius_N_over_F"]))
        P(f"  lines: (a) converged {conv}; (b) ladder {lad}; (c) Route F {nf}; (d) memory {mem}; guard p in [1.5, 2.5] {guard}")
        okc = conv and lad and nf and mem and guard
    else:
        okc = False; lad = nf = guard = conv = mem = False
        P("  ladder incomplete: " + "; ".join(f"{g_} {sols[g_].get('error')}" for g_ in LADDER if not sols[g_].get("ok")))
    cell["C6prime_ok"] = okc
    check(f"C6' [{f}]", okc, "in-window ladder (40,64)/(50,80)/(60,96)/(70,112): converged, shrinking steps, Richardson within 2e-2 of finest, "
          "N/F within 5e-2, RSS < 1 GB, p_obs in [1.5, 2.5]")
    # ------------------------------------------------ label (frozen rule)
    rep = V3W["reproduction"]
    rerun_ok = all(V3W["checks"][k]["ok"] for k in ("C1", "C3", "C4", "C5", "C7", "C8"))
    q2max = max(v["Q2_f"] for v in C6PJ["gate"][f]["G2a"].values())
    band_ok = q2max <= 9.0e-27 and C6PJ["labels"][f] == "PASS"
    if MUT:
        q2m = max(sols[(70, 112)]["Q"][GRADED], 0.0) if sols[(70, 112)].get("ok") else float("inf")
        band_ok = q2m <= 9.0e-27
        cell["mutate_Q2_graded"] = q2m
    k_ok = (not MUT) and CHK.get(f"W2-K1 [{f}]", False) and CHK.get(f"W2-K2 [{f}]", False)
    if okc and k_ok and rerun_ok and band_ok:
        lab = f"PASS: C6' in window (Richardson {cell['rich2_vs_finest']:+.2e} vs 2e-2, N/F {cell['N_over_F']:.4f}); C1, C3-C5, C7, C8 as V3W; C6P Q2 max {q2max:.2e} <= 9.0e-27"
    elif conv and lad and guard and mem and not nf and k_ok:
        lab = f"FAIL: in-window Q2 disagrees with Route F, N/F {cell['N_over_F']:.4f}"
    elif rerun_ok and not band_ok:
        lab = "FAIL: Q2 outside the Hees band"
    else:
        bad = [k for k in (f"W2-K1 [{f}]", f"W2-K2 [{f}]", f"C6' [{f}]") if not CHK.get(k, False)]
        lab = f"UNDECIDED: {bad} failed" + (f"; C6' lines (a)-(d) and guard {'all hold' if okc else 'do not all hold'}" if ok_all else "")
    labels[f] = lab
    cell["V3W_reproduction"] = rep
    cells[f] = cell
    P(f"W2 [{f}]: {lab}")
RES["cells"] = cells; RES["labels"] = labels
n_ok = sum(CHK.values())
P(f"\nW2 COMPLETE: {n_ok}/{len(CHK)} checks PASS")


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o


json.dump(clean(RES), open(os.path.join(HERE, f"v3x_w2_ladder{TAG}.json"), "w"), indent=1, sort_keys=True)
json.dump(clean(SIDE), open(os.path.join(HERE, f"v3x_w2_ladder{TAG}_rss.json"), "w"), indent=1, sort_keys=True)
open(os.path.join(HERE, f"v3x_w2_ladder{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n_ok == len(CHK) and all(v.startswith("PASS") for v in labels.values()) else 1)
