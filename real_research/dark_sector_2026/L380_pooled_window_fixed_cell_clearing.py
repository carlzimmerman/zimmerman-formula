#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L380 -- THE POOLED FULL CONSTRUCTION RE-SCORED WITH THE CORRECTED CLEARING GATE: is there a window?

WHY.  L369/L378 found no pooled window because the z = 2 clearing gate G3 needed kicks >= 725 km/s.  L379 showed G3 is
selection-biased: it is computed over each run's OWN dense cells, and clearing removes cells from that set (the model keeps
~1% of LCDM's dense cells), so G3 measures the minority that kept carrier.  On fixed cells -- the carrier the run keeps in
LCDM's dense cells, relative to LCDM's, the same fixed-position methodology as L366's cluster retention -- dense regions at
z = 2 are cleared to 5-10% at 675-700 km/s in every environment.  L379 is a correction, not a window.  This lane re-scores
the pooled full construction with the corrected clearing gate, every other gate unchanged.

SETUP: L377's full construction (canonical a_0, p = 2 switch, nu_mono phantom felt by the baryons and read by the trigger)
with L379's z = 2 field output (its transformed run, imported unchanged); L369's three realisations; v_k in {600, 625, 650,
675} km/s plus a LCDM run each (15 runs).  Gates pooled exactly as L378 (S_8 averaged; forest and shear from summed power;
X-COP two-sided median over all >= 1e14 Msun/h halos), with clearing replaced by the FIXED-CELL measure: summed over boxes,
the carrier kept in LCDM's dense cells (1 + delta > 50 at z = 2) / LCDM's carrier there, threshold 0.30 (the record's).
The record's own-dense-set G3 is reported beside it.  KiDS is not re-scored (L375, resolved: passes); RC100 and the RAR are
L376's (resolved: pass).
PRE-DECLARED (before the run): H: the pooled full construction has a window -- strict S_8, forest, fixed-cell clearing,
two-sided X-COP and the p = 2 cosmic-shear cell all pass -- at some kick in {600, 625, 650, 675} km/s.
CHECKS
  C1 CONTROL: the (7, 11) run at 675 km/s reproduces L378's committed X-COP median, own-dense-set clearing and S_8 exactly.
  R1 = H.  W (informational): per-realisation and pooled tables on both clearing measures; the per-halo retention and mass
     of every peak (for the Harvey test, L371's machinery) and the pooled retention in L371's mass bins.
MUTATE=1: every kick is 0 (the decayed carrier stays; one run per realisation, used for every kick): R1 must FAIL (rc = 1).
L380_POOL sets the pool size (default 8).

Run from the repository root:  python3 real_research/dark_sector_2026/L380_pooled_window_fixed_cell_clearing.py
"""
import os, sys, json, math, time, tempfile, shutil
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import L379_clearing_by_environment as L79                     # noqa: E402  (L377's run with the z = 2 fields, as L379)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L380_pooled_window_fixed_cell_clearing"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L380", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_WINDOW = True                                             # H, set before the run
L77 = L79.L77
L6, L7, L2 = L77.L6, L77.L7, L77.L2
LBOX, NG, NP, RHO_M, KG = L77.LBOX, L77.NG, L77.NP, L77.RHO_M, L77.KG
SEEDS = ((7, 11), (17, 21), (29, 33))
VK = (600.0, 625.0, 650.0, 675.0)
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
    TMP = tempfile.mkdtemp(prefix="L380_")
    cfgs, SRC = [], {}
    for sp, sk in SEEDS:
        cfgs.append((f"s{sp}_lcdm", sp, sk, float("inf"), 0.0, 0.0, TMP, "none", L77.A0["canonical"]))
        if MUTATE:
            cfgs.append((f"s{sp}_v0", sp, sk, L77.XC_TRIG, 0.0, 10.0, TMP, "full", L77.A0["canonical"]))
            SRC.update({(sp, t): f"s{sp}_v0" for t in TAGS})
        else:
            cfgs += [(f"s{sp}_{t}", sp, sk, L77.XC_TRIG, v, 10.0, TMP, "full", L77.A0["canonical"]) for t, v in zip(TAGS, VK)]
            SRC.update({(sp, t): f"s{sp}_{t}" for t in TAGS})
    if MUTATE:
        P("  MUTATE: v_k = 0 in every decaying run (one run per realisation, used for every kick)")
    P(f"  {len(cfgs)} runs, pool {int(os.environ.get('L380_POOL', '8'))}")
    with Pool(int(os.environ.get("L380_POOL", "8"))) as pool:
        res = dict(pool.map(L79.run_z2, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")

    TM = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]
    est = L6.eps_bounds(); lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())
    s = L2.Sim(LBOX, NG, NP)
    ld = lambda nm, z, f: np.load(os.path.join(TMP, f"{nm}_z{z}_{f}.npy")).astype(float)
    M = {}; HALOS = {}
    for sp, _ in SEEDS:
        L = f"s{sp}_lcdm"; rho_l, rc_l = ld(L, 0.0, "rho"), ld(L, 0.0, "rhoc")
        pk = L6.peaks(s, rho_l)
        Mh = np.array([L6.sphere_sum(s, rho_l, p_, 1.0) * RHO_M for p_ in pk]); sel = Mh >= 1e14
        Mc_l = np.array([L6.sphere_sum(s, rc_l, p_, 1.0) for p_ in pk])
        r2l, c2l = ld(L, 2, "rho"), ld(L, 2, "rhoc"); fixed = r2l > 50.0            # LCDM's dense cells at z = 2
        cl_fix = float(c2l[fixed].sum())
        M[sp] = {}; HALOS[str(sp)] = dict(M_lt_1Mpc_h=Mh.tolist(), eps={})
        for t in TAGS:
            nm = SRC[(sp, t)]; r_ = res[nm]
            eps = np.array([L6.sphere_sum(s, ld(nm, 0.0, "rhoc"), p_, 1.0) for p_ in pk]) / Mc_l
            HALOS[str(sp)]["eps"][t] = eps.tolist()
            M[sp][t] = dict(s8=r_["0.0"]["sigma8"] / res[L]["0.0"]["sigma8"],
                            p1d={z: (np.array(r_[z]["p1d"]), np.array(res[L][z]["p1d"]), np.array(res[L][z]["kpar"])) for z in ("3.0", "2.0")},
                            cid=(r_["2.0"]["carrier_in_dense"], res[L]["2.0"]["carrier_in_dense"]),
                            fix=(float(ld(nm, 2, "rhoc")[fixed].sum()), cl_fix),
                            pk=({q: r_["0.5"]["pk"][q] for q in KG}, {q: res[L]["0.5"]["pk"][q] for q in KG}), eps_sel=eps[sel])
    shutil.rmtree(TMP, ignore_errors=True)

    def gates(rows):                                             # L378's gate arithmetic, clearing on fixed cells
        s8 = float(np.mean([r["s8"] for r in rows])); fdev = 0.0
        for z in ("3.0", "2.0"):
            px = sum(r["p1d"][z][0] for r in rows); pl = sum(r["p1d"][z][1] for r in rows); kp = rows[0]["p1d"][z][2]
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(px[m] / pl[m] - 1))))
        g3a = sum(r["cid"][0] for r in rows) / max(sum(r["cid"][1] for r in rows), 1e-30)
        g3b = sum(r["fix"][0] for r in rows) / max(sum(r["fix"][1] for r in rows), 1e-30)
        eps = np.concatenate([r["eps_sel"] for r in rows]); med = float(np.median(eps)) if len(eps) else float("nan")
        T = {q: math.sqrt(sum(r["pk"][0][q] for r in rows) / sum(r["pk"][1][q] for r in rows)) for q in KG}
        sh = all(T[q] <= TM[f"p=2, x_c0=2.0/{f_}"][str(q)] for q in KG for f_ in ("canonical", "alt"))
        return dict(S8=s8, forest=fdev, G3_own=g3a, clear_fixed=g3b, eps_cl=med, n_cl=int(len(eps)), shear=bool(sh),
                    full=bool(s8 >= 0.922 and fdev <= 0.10 and g3b <= 0.30 and lo <= med <= hi and sh),
                    full_with_record_G3=bool(s8 >= 0.922 and fdev <= 0.10 and g3a <= 0.30 and lo <= med <= hi and sh))

    banner("C1  CONTROL: the (7, 11) run at 675 km/s reproduces L378")
    if not MUTATE:
        R78 = json.load(open(os.path.join(HERE, "L378_full_construction_pooled_results.json")))["numbers"]["table"]["7"]["v675"]
        g1 = gates([M[7]["v675"]])
        dev = max(abs(g1["eps_cl"] / R78["eps_cl"] - 1), abs(g1["G3_own"] / R78["G3"] - 1), abs(g1["S8"] / R78["S8"] - 1))
        check("C1 the (7, 11) run at 675 km/s reproduces L378's committed X-COP median, own-dense-set clearing and S_8",
              f"max relative deviation {dev:.1e} over 3 numbers", dev < 1e-9)
    else:
        dev = abs(res["s7_lcdm"]["0.0"]["sigma8"] / json.load(open(os.path.join(HERE, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["runs"]["lcdm"]["0.0"]["sigma8"] - 1)
        check("C1 the (7, 11) LCDM run reproduces L366's sigma_8", f"relative deviation {dev:.1e}", dev < 1e-9)

    banner("THE GATE TABLE with the corrected (fixed-cell) clearing, per realisation and pooled")
    P(f"    X-COP two-sided {lo:.3f}-{hi:.3f}; clearing <= 0.30; forest <= 0.10; S8 >= 0.922")
    TAB = {}
    for key, rows_of in [(str(sp), lambda t, sp=sp: [M[sp][t]]) for sp, _ in SEEDS] + [("pooled", lambda t: [M[sp][t] for sp, _ in SEEDS])]:
        TAB[key] = {}
        for t in TAGS:
            g = gates(rows_of(t)); TAB[key][t] = g
            P(f"    {key:>6s} {t}: S8 {g['S8']:.3f} | forest {g['forest']:.3f} | clearing fixed {g['clear_fixed']:.3f}"
              f"{'' if g['clear_fixed'] <= 0.3 else ' X'} (record's G3 {g['G3_own']:.2f}) | X-COP eps {g['eps_cl']:.3f}"
              f"{'' if lo <= g['eps_cl'] <= hi else (' UNDER' if g['eps_cl'] < lo else ' OVER')} (n={g['n_cl']}) | shear {'ok' if g['shear'] else 'X'}"
              f"  =>  {'ALL PASS' if g['full'] else 'no'}{' (also with the record G3)' if g['full_with_record_G3'] else ''}")
    WIN = {k_: [t for t in TAGS if TAB[k_][t]["full"]] for k_ in TAB}
    P("\n    windows (corrected clearing): " + "; ".join(f"{k_}: {v or 'none'}" for k_, v in WIN.items()))
    MBINS = ((6e13, 1e14), (1e14, 1.5e14), (1.5e14, 2.5e14), (2.5e14, 1e17))           # L371's bins of M(<1 Mpc/h)
    RB = {}
    for t in TAGS:
        mh = np.concatenate([np.array(HALOS[str(sp)]["M_lt_1Mpc_h"]) for sp, _ in SEEDS])
        ee = np.concatenate([np.array(HALOS[str(sp)]["eps"][t]) for sp, _ in SEEDS])
        RB[t] = {f"{b0:.1e}-{b1:.1e}": (float(np.median(ee[(mh >= b0) & (mh < b1)])) if ((mh >= b0) & (mh < b1)).any() else None,
                                       int(((mh >= b0) & (mh < b1)).sum())) for b0, b1 in MBINS}
        P(f"    pooled retention by M(<1 Mpc/h) (L371's bins), {t}: " + ", ".join(f"{k_}: {v[0]:.2f} (n={v[1]})" if v[0] is not None else f"{k_}: - (n=0)" for k_, v in RB[t].items()))
    OUT["numbers"].update(table=TAB, windows=WIN, eps_bounds=dict(lo=lo, hi=hi), halos=HALOS, retention_by_mass=RB)
    check("W (informational) per-realisation and pooled gate tables on both clearing measures", "see tables", True,
          "reported either way", load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    check("R1 = H: the pooled full construction has a window on the corrected gate set at some kick in 600-675 km/s",
          f"pooled window: {WIN['pooled'] or 'none'}", bool(WIN["pooled"]) == EXPECT_WINDOW)

    banner("VERDICT")
    P(f"""  Pooled full construction, corrected (fixed-cell) clearing: window {WIN['pooled'] or 'none'}; per realisation
  """ + "; ".join(f"({sp}) {WIN[str(sp)] or 'none'}" for sp, _ in SEEDS) + """.
  LIMITS: three 100 Mpc/h boxes on a 0.39 Mpc/h mesh; the trigger posited (no action); the switch on the matter-only branch;
  KiDS, RC100 and the RAR from the resolved shell model (L375, L376), not from these boxes.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
