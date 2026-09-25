#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L358 -- DOES THE FOREST-KiDS PINCER ON L342's SWITCH SURVIVE ON THE FOREST OBSERVABLE?

WHY.  L352 Z7 closed the bound-region switch with a pincer: with the realizable (Gauss-compensated) profile, KiDS-1000
accepts only x_c ~ 2-3 (Delta chi^2 <= +4 with a 2-halo term, both footings), while "every tested x_c <= 7 FAILS" the
forest.  That forest side is L346's MATTER power.  L347 then showed that on the OBSERVABLE -- the 1D flux power at fixed
mean transmission -- the switch is borderline at x_c = 5 (10.8%) and passes at x_c = 7 (7.2%).  The pincer therefore
needs the observable at the thresholds KiDS accepts.  This lane measures it.

METHOD: L347's machinery imported unchanged (L176's PM; the constraint-derived switch x = (3/2) Omega_m delta_mesh,
Lean I26; nu_mono; FGPA flux with pressure filter, redshift-space velocities, thermal broadening, Becker+2013 tau_eff;
two boxes 50 and 25 Mpc/h; same phases in every run of a box).  Thresholds x_c in {2, 2.5, 3, 4}, both footings.
PRE-DECLARED
  * the forest-observable acceptance of a threshold: worst |P1D_switch/P1D_LCDM - 1| <= 0.10 over k_par in [0.2, 2] h/Mpc,
    z = 3 and 2, both footings, both boxes (L347's rule);
  * THE PINCER HOLDS ON THE OBSERVABLE iff every KiDS-accepted threshold (x_c = 2, 2.5, 3) FAILS that rule;
    it OPENS if any of them passes.  x_c = 4 is reported alongside (KiDS: +8.3/+9.0, just outside its +4 cut).
CHECKS
  C1 CONTROL: re-running L347's x_c = 5 canonical 50 Mpc/h cell reproduces L347's committed P1D ratios exactly.
  F1 the worst P1D deviation for each threshold (the forest-observable curve vs x_c).
  F2 THE PINCER VERDICT (direction fixed after an exploratory run of this same script, not committed; nothing else
     changed): see RESULT.
  F3 RESOLUTION DEPENDENCE (recorded): the verdict is carried by the finer (25 Mpc/h) box at z = 2; the coarse box alone
     would pass the KiDS-accepted x_c = 3.
RESULT.  The worst flux-power deviation falls smoothly with the threshold: x_c = 2 / 2.5 / 3 / 4 give 0.185 / 0.174 /
0.160 / 0.131 (L347: 5 -> 0.108, 7 -> 0.072).  Every KiDS-accepted threshold fails the 10% rule, so L352's pincer HOLDS
on the observable -- but only through the 25 Mpc/h box at z = 2 (canonical 0.143-0.173); the 50 Mpc/h box gives
0.086-0.114 there and alone would pass x_c = 3.  The finer box resolves the switched-on filaments better, so it is taken
as the closer of the two, but the pincer is resolution-conditional, not converged.
MUTATE=1: the switch never turns on -- every deviation vanishes and F2 must flip (rc = 1).

Run from the repository root:  python3 real_research/g03_audit_2026/L358_forest_kids_pincer_observable.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import L347_switch_forest_flux_power as L7            # noqa: E402  (L347's machinery, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L358_forest_kids_pincer_observable"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L358", "mutate": MUTATE, "checks": {}, "numbers": {}}


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


INF = float("inf")
XCS = [2.0, 2.5, 3.0, 4.0]
KIDS_OK = [2.0, 2.5, 3.0]                              # L352 Z4/Z7: Delta chi^2 <= +4 with a 2-halo term, both footings
EXPECT_PINCER = True                                   # fixed from the exploratory run (see RESULT)

if __name__ == "__main__":
    P(__doc__)
    cfgs = []
    for L in (50.0, 25.0):
        t = f"L{int(L)}"
        cfgs.append((f"{t}_lcdm", L, "lcdm", "canonical", 0))
        for xc in XCS:
            for foot in ("canonical", "alt"):
                cfgs.append((f"{t}_x{xc}_{foot}", L, "switch", foot, INF if MUTATE else xc))
    cfgs.append(("L50_x5.0_canonical_ctrl", 50.0, "switch", "canonical", 5.0))
    with Pool(10) as pool:
        res = dict(pool.map(L7.run, cfgs))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")
    OUT["numbers"]["runs"] = res

    def p1d_ratio(name, t, z):
        kp = np.array(res[f"{t}_lcdm"][z]["kpar"]); r = np.array(res[name][z]["p1d"]) / np.array(res[f"{t}_lcdm"][z]["p1d"])
        m = (kp >= 0.2) & (kp <= 2.0)
        return kp[m], r[m]

    banner("CONTROL")
    ref = json.load(open(os.path.join(HERE, "L347_switch_forest_flux_power_results.json")))
    rr = ref["numbers"]["runs"]
    d = 0.0
    for z in ("3.0", "2.0"):
        mine = np.array(res["L50_x5.0_canonical_ctrl"][z]["p1d"]) / np.array(res["L50_lcdm"][z]["p1d"])
        theirs = np.array(rr["L50_sw5_canon"][z]["p1d"]) / np.array(rr["L50_lcdm"][z]["p1d"])
        d = max(d, float(np.max(np.abs(mine - theirs))))
    check("C1 re-running L347's x_c = 5 canonical 50 Mpc/h cell reproduces L347's committed P1D ratios", f"max |difference| = {d:.1e}",
          d < 1e-9, "same code, same phases: the machinery is reproducible")

    banner("F1  THE FOREST-OBSERVABLE CURVE: worst |P1D ratio - 1| over k_par 0.2-2 h/Mpc, z = 3 and 2")
    worst = {}
    for xc in XCS:
        cells = {}
        for t in ("L50", "L25"):
            for foot in ("canonical", "alt"):
                for z in ("3.0", "2.0"):
                    _, r = p1d_ratio(f"{t}_x{xc}_{foot}", t, z)
                    cells[(t, foot, z)] = float(np.max(np.abs(r - 1)))
        worst[xc] = max(cells.values())
        wc = max(v for (t, f, z), v in cells.items() if f == "canonical")
        P(f"    x_c = {xc:3.1f}: worst {worst[xc]:.3f} (canonical {wc:.3f});  by cell: " +
          ", ".join(f"{t}/{f[:5]}/z{z[0]} {v:.3f}" for (t, f, z), v in sorted(cells.items())) +
          f"   -> {'PASS' if worst[xc] <= 0.10 else 'FAIL'} the 10% rule")
    P("    (L347, committed: x_c = 5 worst 0.108, x_c = 7 worst 0.072)")
    OUT["numbers"]["worst"] = {str(k): v for k, v in worst.items()}
    check("F1 (informational) the forest-observable deviation falls as the threshold rises (less of the forest switched on)",
          ", ".join(f"x_c {k}: {v:.3f}" for k, v in worst.items()),
          all(worst[XCS[i]] >= worst[XCS[i + 1]] - 0.01 for i in range(len(XCS) - 1)), "reported either way", load_bearing=False)

    banner("F2  THE PINCER ON THE OBSERVABLE")
    kids_fail = [xc for xc in KIDS_OK if worst[xc] > 0.10]
    holds = len(kids_fail) == len(KIDS_OK)
    OUT["numbers"]["pincer"] = dict(kids_ok=KIDS_OK, failing=kids_fail, holds=holds)
    check(f"F2 THE PINCER {'HOLDS' if EXPECT_PINCER else 'OPENS'} ON THE OBSERVABLE: "
              + ("every KiDS-accepted threshold (x_c = 2, 2.5, 3) fails the forest's 10% flux-power rule" if EXPECT_PINCER
                 else "at least one KiDS-accepted threshold passes the forest's 10% flux-power rule"),
              f"worst deviations: " + ", ".join(f"x_c {k}: {worst[k]:.3f}" for k in KIDS_OK), holds == EXPECT_PINCER,
              "L352 Z7's closure, re-checked on the forest observable rather than matter power")

    coarse3 = max(float(np.max(np.abs(p1d_ratio(f"L50_x3.0_{f}", "L50", z)[1] - 1))) for f in ("canonical", "alt") for z in ("3.0", "2.0"))
    fine3 = max(float(np.max(np.abs(p1d_ratio(f"L25_x3.0_{f}", "L25", z)[1] - 1))) for f in ("canonical", "alt") for z in ("3.0", "2.0"))
    OUT["numbers"]["resolution_x3"] = dict(coarse=coarse3, fine=fine3)
    check("F3 (informational) resolution dependence at the KiDS-accepted x_c = 3: the coarse box alone would pass, the fine box fails",
          f"worst deviation at x_c = 3: 50 Mpc/h {coarse3:.3f}, 25 Mpc/h {fine3:.3f}", coarse3 <= 0.10 < fine3,
          "the pincer is carried by the finer box -- resolution-conditional, not converged", load_bearing=False)

    banner("VERDICT")
    P(f"""  Forest observable (1D flux power, fixed mean transmission) vs threshold: {', '.join(f'x_c {k}: {v:.3f}' for k, v in worst.items())}
  (L347: x_c 5: 0.108, x_c 7: 0.072).  KiDS (L352, realizable profile + 2-halo) accepts x_c = 2-3.
  The KiDS-accepted thresholds failing the forest's 10% rule: {kids_fail} -> the pincer {'HOLDS' if holds else 'OPENS'} on the observable,
  carried by the 25 Mpc/h box (x_c = 3: {fine3:.3f}; the 50 Mpc/h box gives {coarse3:.3f}) -- resolution-conditional.
  LIMITS: FGPA on a 0.2-0.4 Mpc/h grid, one realisation per box; KiDS side is L352's (linear 2-halo term).""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
