#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L378 -- THE FULL CONSTRUCTION, POOLED OVER THREE REALISATIONS: is the clearing-vs-clusters pinch real?

WHY.  L369: the Newtonian construction has no window over three 100 Mpc/h realisations -- the z = 2 dense-cell clearing
(G3) needs kicks above ~700 km/s, the X-COP cluster gate needs kicks below ~660.  L377: the full construction (the switched
phantom felt by the baryons and read by the trigger) raises cluster retention by 6-22% on one realisation and leaves G3
untouched; applying those shifts to L369's pooled gates ESTIMATES a near miss at 700 km/s (G3 0.31, X-COP 0.28, each
within 0.01 of its threshold).  An estimate is not a run.  This lane runs the full construction on all three realisations
at the kicks where the pinch sits.

SETUP: L377's run(), unchanged (full mode, canonical a_0, L359's p = 2 switch, nu_mono, phantom-inclusive trigger), seeds
(7, 11), (17, 21), (29, 33) as L369; v_k in {675, 700, 725, 750} km/s plus a LCDM run per realisation (15 runs).  Gates as
L369 computes them, per realisation and pooled (S_8 averaged, forest and shear from summed power, clearing from summed
dense-cell fractions, clusters as the median over all >= 1e14 Msun/h halos); KiDS is not re-scored (L375, resolved).
PRE-DECLARED (before the run): H: the POOLED full construction has a window (strict S_8, forest, clearing, two-sided X-COP,
p = 2 shear) at some kick in {675, 700, 725, 750} km/s.
CHECKS
  C1 CONTROL: the (7, 11) reruns at 675 and 700 reproduce L377's committed X-COP median, clearing and S_8 exactly.
  R1 = H.  W (informational): per-realisation and pooled tables; the pinch -- the lowest kick that clears (pooled G3 <= 0.30)
     against the highest kick that keeps clusters (pooled median >= the X-COP floor).
MUTATE=1: every kick is 0 (the decayed carrier stays): R1 must FAIL (rc = 1).  Run only if R1 passes in the main run (a
control that forces the window shut has nothing to discriminate when the main run already finds none -- as L369).
L378_POOL sets the pool size (default 8).

Run from the repository root:  python3 real_research/dark_sector_2026/L378_full_construction_pooled.py
"""
import os, sys, json, math, time, tempfile, shutil
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import L377_full_construction_pm as L77                        # noqa: E402  (L377's full-construction run, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L378_full_construction_pooled"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L378", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_WINDOW = True                                             # H, set before the run
L6, L7, L2 = L77.L6, L77.L7, L77.L2
LBOX, NG, NP, RHO_M, KG = L77.LBOX, L77.NG, L77.NP, L77.RHO_M, L77.KG
SEEDS = ((7, 11), (17, 21), (29, 33))
VK = (675.0, 700.0, 725.0, 750.0)
TAGS = tuple(f"v{int(v)}" for v in VK)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


if __name__ == "__main__":
    P(__doc__)
    TMP = tempfile.mkdtemp(prefix="L378_")
    cfgs = []
    for sp, sk in SEEDS:
        cfgs.append((f"s{sp}_lcdm", sp, sk, float("inf"), 0.0, 0.0, TMP, "none", L77.A0["canonical"]))
        cfgs += [(f"s{sp}_{t}", sp, sk, L77.XC_TRIG, 0.0 if MUTATE else v, 10.0, TMP, "full", L77.A0["canonical"])
                 for t, v in zip(TAGS, VK)]
    if MUTATE:
        P("  MUTATE: v_k = 0 in every decaying run")
    P(f"  {len(cfgs)} runs, pool {int(os.environ.get('L378_POOL', '8'))}")
    with Pool(int(os.environ.get("L378_POOL", "8"))) as pool:
        res = dict(pool.map(L77.run, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")

    TM = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]
    est = L6.eps_bounds(); lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())
    s = L2.Sim(LBOX, NG, NP)
    ld = lambda nm, z, f: np.load(os.path.join(TMP, f"{nm}_z{z}_{f}.npy")).astype(float)
    M = {}
    for sp, _ in SEEDS:
        L = f"s{sp}_lcdm"; rho_l, rc_l = ld(L, 0.0, "rho"), ld(L, 0.0, "rhoc")
        pk = L6.peaks(s, rho_l)
        Mh = np.array([L6.sphere_sum(s, rho_l, p_, 1.0) * RHO_M for p_ in pk]); sel = Mh >= 1e14
        Mc_l = np.array([L6.sphere_sum(s, rc_l, p_, 1.0) for p_ in pk])
        M[sp] = {}
        for t in TAGS:
            r_ = res[f"s{sp}_{t}"]
            eps = np.array([L6.sphere_sum(s, ld(f"s{sp}_{t}", 0.0, "rhoc"), p_, 1.0) for p_ in pk]) / Mc_l
            M[sp][t] = dict(s8=r_["0.0"]["sigma8"] / res[L]["0.0"]["sigma8"],
                            p1d={z: (np.array(r_[z]["p1d"]), np.array(res[L][z]["p1d"]), np.array(res[L][z]["kpar"])) for z in ("3.0", "2.0")},
                            cid=(r_["2.0"]["carrier_in_dense"], res[L]["2.0"]["carrier_in_dense"]),
                            pk=({q: r_["0.5"]["pk"][q] for q in KG}, {q: res[L]["0.5"]["pk"][q] for q in KG}), eps_sel=eps[sel])
    shutil.rmtree(TMP, ignore_errors=True)

    def gates(rows):                                             # L369's gate arithmetic
        s8 = float(np.mean([r["s8"] for r in rows])); fdev = 0.0
        for z in ("3.0", "2.0"):
            px = sum(r["p1d"][z][0] for r in rows); pl = sum(r["p1d"][z][1] for r in rows); kp = rows[0]["p1d"][z][2]
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(px[m] / pl[m] - 1))))
        g3 = sum(r["cid"][0] for r in rows) / max(sum(r["cid"][1] for r in rows), 1e-30)
        eps = np.concatenate([r["eps_sel"] for r in rows]); med = float(np.median(eps)) if len(eps) else float("nan")
        T = {q: math.sqrt(sum(r["pk"][0][q] for r in rows) / sum(r["pk"][1][q] for r in rows)) for q in KG}
        sh = all(T[q] <= TM[f"p=2, x_c0=2.0/{f_}"][str(q)] for q in KG for f_ in ("canonical", "alt"))
        return dict(S8=s8, forest=fdev, G3=g3, eps_cl=med, n_cl=int(len(eps)), shear=bool(sh),
                    full=bool(s8 >= 0.922 and fdev <= 0.10 and g3 <= 0.30 and lo <= med <= hi and sh))

    banner("C1  CONTROL: the (7, 11) reruns reproduce L377")
    R77 = json.load(open(os.path.join(HERE, "L377_full_construction_pm_results.json")))["numbers"]["table"]
    dev = []
    if not MUTATE:
        for t in ("v675", "v700"):
            g1 = gates([M[7][t]]); r7 = R77[f"full_can_{t}"]
            dev += [abs(g1["eps_cl"] / r7["eps_cl"] - 1), abs(g1["G3"] / r7["G3"] - 1), abs(g1["S8"] / r7["S8"] - 1)]
    else:
        dev = [abs(res["s7_lcdm"]["0.0"]["sigma8"] / json.load(open(os.path.join(HERE, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["runs"]["lcdm"]["0.0"]["sigma8"] - 1)]
    check("C1 the (7, 11) reruns reproduce L377's committed X-COP median, clearing and S_8 at 675 and 700 km/s" if not MUTATE else
          "C1 the (7, 11) LCDM run reproduces L366's sigma_8", f"max relative deviation {max(dev):.1e} over {len(dev)} numbers", max(dev) < 1e-9)

    banner("THE GATE TABLE: full construction, per realisation and pooled")
    P(f"    X-COP two-sided {lo:.3f}-{hi:.3f}; clearing <= 0.30; forest <= 0.10; S8 >= 0.922")
    TAB = {}
    for key, rows_of in [(str(sp), lambda t, sp=sp: [M[sp][t]]) for sp, _ in SEEDS] + [("pooled", lambda t: [M[sp][t] for sp, _ in SEEDS])]:
        TAB[key] = {}
        for t in TAGS:
            g = gates(rows_of(t)); TAB[key][t] = g
            P(f"    {key:>6s} {t}: S8 {g['S8']:.3f} | forest {g['forest']:.3f} | cleared {g['G3']:.2f}{'' if g['G3'] <= 0.3 else ' X'} | "
              f"X-COP eps {g['eps_cl']:.3f}{'' if lo <= g['eps_cl'] <= hi else (' UNDER' if g['eps_cl'] < lo else ' OVER')} (n={g['n_cl']}) | "
              f"shear {'ok' if g['shear'] else 'X'}  =>  {'ALL PASS' if g['full'] else 'no'}")
    WIN = {k_: [t for t in TAGS if TAB[k_][t]["full"]] for k_ in TAB}
    Pp = TAB["pooled"]
    v_clear = next((t for t in TAGS if Pp[t]["G3"] <= 0.30), None)
    v_keep = [t for t in TAGS if Pp[t]["eps_cl"] >= lo]
    P(f"\n    windows: " + "; ".join(f"{k_}: {v or 'none'}" for k_, v in WIN.items()))
    P(f"    the pinch (pooled): lowest kick that clears = {v_clear or '> 750'}; kicks keeping clusters above the floor = {v_keep or 'none (all below 675)'}")
    OUT["numbers"].update(table=TAB, windows=WIN, pinch=dict(v_clear=v_clear, v_keep=v_keep), eps_bounds=dict(lo=lo, hi=hi))
    check("W (informational) per-realisation and pooled gate tables; the pinch", "see tables", True, "reported either way", load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    check("R1 = H: the POOLED full construction has a window at some kick in 675-750 km/s", f"pooled window: {WIN['pooled'] or 'none'}",
          bool(WIN["pooled"]) == EXPECT_WINDOW)

    banner("VERDICT")
    P(f"""  Full construction pooled over three realisations: window {WIN['pooled'] or 'none'}; lowest clearing kick {v_clear or '> 750'},
  cluster-keeping kicks {v_keep or 'none'}.  LIMITS: three 100 Mpc/h boxes on a 0.39 Mpc/h mesh, the clearing gate is the
  mesh proxy G3 (its resolved targets pass, L375/L376), the switch on the matter-only branch, the trigger posited.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
