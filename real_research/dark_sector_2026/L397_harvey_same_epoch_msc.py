#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L397 -- HARVEY+2015 AT ITS OWN EPOCH, SAME CELL, SAME MODEL: the carrier retention of L396's same-model cell (the leak-free
MOND-sector switch with MS5's mean-curvature cap) measured at z = 0.4 -- the merger epoch -- fed through L389's same-cell adapter.

WHY.  L389's Harvey pass (the phase-mixed shape at 575 km/s, fit +0.096) is PROVISIONAL on two counts: it used retention
measured at z = 0 and applied at z = 0.4, and it used the matter-only switch branch's retention (L388).  L396 runs the
leak-free MOND-sector switch with MS5's action-term cap (the same cap as its shear score; L395's primary cell used the
withdrawn cap form and is not used here) at 575, 600 and 650 km/s and saves the z = 0.4 fields, giving retention by halo
mass AT the merger epoch.  This lane scores Harvey with that retention: same cell, same epoch, same model as L396's gates.

METHOD: L389's harvey_cell() imported unchanged (L371's machinery with the retention table, kick and switch cell replaced;
SW_DEF = p1_x2.5); retention: the pooled z = 0.4 medians of L396 in L371's bins and mapping (M(<1 Mpc/h) at z = 0.4:
6e13-1e14 -> lensing 1e14 Msun; 1.5e14-2.5e14 -> 3e14; >= 2.5e14 -> the 1e15 main cluster; a bin empty at z = 0.4 falls back to
the nearest populated lower bin, recorded in the output).  Kicks: every kick of L396's pooled window (575, 600, 650); if the
window is empty, all three are scored (reported) and R1 fails.
PRE-DECLARED (before the run): H: at some kick in the primary cell's pooled window the phase-mixed shape S2 passes Harvey at
the z = 0.4 retention (population-mean excess beta <= +0.10 on all three estimators).
CHECKS
  C1 CONTROL: L389's 575 km/s job (L388's z = 0 retention, same cell) through this lane reproduces L389's committed S1/S2/S3
     and intact values exactly.
  C2 CONTROL: the switch took effect (x_c,eff(0.4) = 2.5 E(0.4)^2 for every job).
  R1 = H.  W (informational): S1, S2, S3 and the intact carrier per kick; the z = 0 (provisional) values beside them.
MUTATE=1: every retention is quartered (a hollowed carrier): R1 must FAIL (rc = 1).
L397_POOL sets the pool size (default 3; ~13 GB a job).

Run from the repository root after L396:  python3 real_research/dark_sector_2026/L397_harvey_same_epoch_msc.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from L389_harvey_same_cell_linear_gate import harvey_cell, BINMAP, CELL, CELL_PX, EST   # noqa: E402  (L389's adapter, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L397_harvey_same_epoch_msc"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L397", "cell": "p=1, x_c0=2.5", "switch": "msck (MOND-sector + MS5's mean-curvature cap), L396's same-model cell",
               "epoch": "retention measured at z = 0.4, the merger epoch", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT = True                                                    # H, set before the run


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
    R96 = json.load(open(os.path.join(HERE, "L396_msc_cell_575_results.json")))["numbers"]
    RB4 = R96["retention_by_mass_z04"]
    win = list(R96["windows"]["msck"])
    kicks = win if win else ["v575", "v600", "v650"]
    P(f"  primary cell's pooled window: {win or 'none'}; kicks scored here: {kicks}")
    jobs = []
    for t in kicks:
        rb = RB4[f"msck/{t}"]
        order = list(rb.keys())                                   # L371's bins, ascending in mass
        eps, fb = {}, {}
        for Ml, b in BINMAP.items():                              # an empty bin at z = 0.4 falls back to the nearest populated lower bin
            j = order.index(b)
            while j >= 0 and rb[order[j]][0] is None:
                j -= 1
            if j < 0:
                raise SystemExit(f"no populated bin at or below {b} for {t}")
            if order[j] != b:
                fb[f"{Ml:.0e}"] = order[j]
            eps[Ml] = float(rb[order[j]][0]) * (0.25 if MUTATE else 1.0)
        if fb:
            P(f"    {t}: empty z = 0.4 bin(s) -- fell back to the nearest populated lower bin: {fb}")
            OUT["numbers"].setdefault("bin_fallbacks", {})[t] = fb
        OUT["numbers"].setdefault("retention_used_z04", {})[t] = {f"{k:.0e}": v for k, v in eps.items()}
        P(f"    {t}: z = 0.4 retention used (lensing 1e14 / 3e14 / 1e15) = {eps[1e14]:.3f} / {eps[3e14]:.3f} / {eps[1e15]:.3f}")
        jobs.append((t, eps, float(t[1:]), (CELL, CELL_PX)))
    if not MUTATE:                                               # C1: L389's own 575 km/s job
        R88 = json.load(open(os.path.join(HERE, "L388_linear_gate_pooled_results.json")))["numbers"]["retention_by_mass"]["v575"]
        jobs.append(("C1_L389_v575", {Ml: float(R88[b][0]) for Ml, b in BINMAP.items()}, 575.0, (CELL, CELL_PX)))
    else:
        P("  MUTATE: every retention quartered (a hollowed carrier)")
    with Pool(min(len(jobs), int(os.environ.get("L397_POOL", "3")))) as pool:
        RES = dict(pool.map(harvey_cell, jobs, chunksize=1))
    P(f"  {len(jobs)} jobs done   [{time.time() - T0:.0f}s]")

    banner("C1, C2  CONTROLS")
    if not MUTATE:
        R89 = json.load(open(os.path.join(HERE, "L389_harvey_same_cell_linear_gate_results.json")))["numbers"]["results"]["v575"]["MEAN"]
        c1 = RES["C1_L389_v575"]["MEAN"]
        d1 = max(abs(c1[v][e] - R89[v][e]) for v in ("intact", "S1_med", "S2_med", "S3_med") for e in EST)
        check("C1 L389's 575 km/s job through this lane reproduces L389's committed intact, S1, S2 and S3 values exactly", f"max |difference| {d1:.1e}", d1 < 1e-9)
    ez = RES[kicks[0]]["Ez2_z04"]
    ok2 = all(abs(RES[t]["x_ceff_z04"] / (CELL_PX[1] * ez ** CELL_PX[0]) - 1) < 1e-12 and RES[t]["SW_DEF"] == CELL for t in kicks)
    check("C2 the switch took effect: every job ran at x_c,eff(0.4) = 2.5 E(0.4)^2", f"{sorted(set(round(RES[t]['x_ceff_z04'], 6) for t in kicks))}", ok2)

    banner("HARVEY+2015, SAME CELL, OWN EPOCH (z = 0.4 retention; population-mean excess beta 100 / 150 kpc / fit; bound <= +0.10)")
    R89all = json.load(open(os.path.join(HERE, "L389_harvey_same_cell_linear_gate_results.json")))["numbers"]["results"]
    PASS = {}
    for t in kicks:
        M = RES[t]["MEAN"]
        for v in ("S1_med", "S2_med", "S3_med"):
            ok = all(M[v][e] <= -0.04 + 2 * 0.07 for e in EST)
            PASS[(t, v)] = ok
            prov = R89all.get(t, {}).get("MEAN", {}).get(v)
            P(f"    {t} {v}: " + "/".join(f"{M[v][e]:+.3f}" for e in EST) + f"  ({'/'.join(f'{(M[v][e] + 0.04) / 0.07:+.1f}' for e in EST)} sigma) -> "
              f"{'pass' if ok else 'FAIL'}" + (f"   (L389, z = 0 matter-branch retention: fit {prov['fit']:+.3f})" if prov else ""))
    OUT["numbers"].update(results=RES, passes={f"{k[0]}|{k[1]}": v for k, v in PASS.items()}, window=win)
    check("W (informational) S1, S2, S3 per kick at the z = 0.4 retention, the provisional z = 0 values beside them", "see table", True,
          "reported either way", load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    s2 = [t for t in kicks if PASS[(t, "S2_med")]]
    check("R1 = H: at some kick in the primary cell's pooled window the phase-mixed shape S2 passes Harvey at the z = 0.4 retention",
          f"S2 passes at: {s2 or 'none'} (window {win or 'none'})", bool(win) and bool(s2) == EXPECT)

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o) if isinstance(o, np.floating) else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
