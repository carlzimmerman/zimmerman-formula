#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L381 -- THE HARVEY TEST ON THE POOLED WINDOW: do the full construction's group cores, at the kicks where L380 finds a pooled
window, keep enough collisionless carrier to hold the lensing peak on the galaxies when the gas is knocked loose?

WHY.  L371 (parallel lane, merger_infall_2026) applied Harvey+2015 (<beta> = -0.04 +/- 0.07, 72 substructures) to L366's
single-box NEWTONIAN retention at 650 km/s and found it fails: population-mean excess beta +0.104 (cusp kept, S1),
+0.135 (phase-mixed daughters, S2), +0.340 (recaptured, S3) on the Lenstool-like fit, against the <= +0.10 two-sigma
bound.  L377 then showed the full construction (the phantom felt by the baryons) raises cluster retention by 6-22%, and
L380 re-scored the pooled three-box construction with the corrected clearing gate.  This lane re-runs L371's test with the
retention L380 measures, pooled, at every kick in L380's pooled window.

METHOD.  L371's script, loaded unedited except for its inputs: the retention table EPS (lensing mass -> retention) is
replaced by L380's pooled medians in L371's own mass bins and mapping (M(<1 Mpc/h) 6e13-1e14 -> lensing 1e14 Msun;
1.5e14-2.5e14 -> 3e14; >= 2.5e14 -> the 1e15 main cluster), the daughters' kick VK by the window kick, L371's MUTATE flag is
held False, and L371's own checks and output files are cut (its committed results are never touched).  One process per
kick.  Shapes as L371: S1 (the cusp kept, optimistic), S2 (phase-mixed daughters, L321's retained(), Newtonian orbits),
S3 (recaptured, marginally bound, pessimistic).
PRE-DECLARED (before the run): H: at some kick in L380's pooled window, the phase-mixed shape S2 passes Harvey -- the
population-mean excess beta is <= +0.10 on all three estimators (100 kpc, 150 kpc, Lenstool-like fit).
CHECKS
  C1 CONTROL: the intact carrier reproduces L371's committed configuration-averaged excess beta (all three estimators, 1e-6).
  R1 = H.  W (informational): S1, S2, S3 at every window kick; the carrier-to-baryon ratio inside 150 kpc.
MUTATE=1: every retention is quartered (a hollowed carrier): R1 must FAIL (rc = 1).

Run from the repository root after L380:  python3 real_research/dark_sector_2026/L381_harvey_on_pooled_window.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
P71 = os.path.join(REPO, "real_research", "merger_infall_2026", "L371_harvey_slow_kick_carrier.py")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L381_harvey_on_pooled_window"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L381", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_PASS = True                                               # H, set before the run
BINMAP = {1e14: "6.0e+13-1.0e+14", 3e14: "1.5e+14-2.5e+14", 1e15: "2.5e+14-1.0e+17"}   # L371's mapping of L366's bins


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


def harvey(job):
    """L371's machinery with its retention table and kick replaced; returns the population means and core ratios."""
    tag, eps_med, vk = job
    src = open(P71).read()
    reps = [('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"),
            ('EPS = {"med": {1e14: 0.18, 3e14: 0.40, 1e15: 0.75}, "max": {1e14: 0.26, 3e14: 0.73, 1e15: 0.80}}',
             f'EPS = {{"med": {{1e14: {eps_med[1e14]!r}, 3e14: {eps_med[3e14]!r}, 1e15: {eps_med[1e15]!r}}}, "max": {{1e14: 1.0, 3e14: 1.0, 1e15: 1.0}}}}'),
            ("VK = 650.0", f"VK = {float(vk)!r}"),
            ('            "S1_max": ("S1", "max")}', "            }")]
    for a, b in reps:
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    MARK = "# ================================================================================================ checks"
    assert src.count(MARK) == 1
    src = src.split(MARK)[0]
    ns = {"__name__": "l371_in_l381", "__file__": P71}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, "L371(L381 inputs)", "exec"), ns)
    return tag, dict(MEAN=ns["MEAN"], CORE={f"{k[0]}|{k[1]:.0e}": float(v) for k, v in ns["CORE"].items()})


if __name__ == "__main__":
    P(__doc__)
    R80 = json.load(open(os.path.join(HERE, "L380_pooled_window_fixed_cell_clearing_results.json")))["numbers"]
    win = R80["windows"]["pooled"]
    kicks = win if win else list(R80["retention_by_mass"].keys())
    P(f"  L380's pooled window: {win or 'none'}; kicks scored here: {kicks}")
    jobs = []
    for t in kicks:
        rb = R80["retention_by_mass"][t]
        eps = {Ml: float(rb[b][0]) * (0.25 if MUTATE else 1.0) for Ml, b in BINMAP.items()}
        OUT["numbers"].setdefault("retention_used", {})[t] = {f"{k:.0e}": v for k, v in eps.items()}
        P(f"    {t}: retention used (lensing 1e14 / 3e14 / 1e15) = {eps[1e14]:.3f} / {eps[3e14]:.3f} / {eps[1e15]:.3f}")
        jobs.append((t, eps, float(t[1:])))
    if MUTATE:
        P("  MUTATE: every retention quartered (a hollowed carrier)")
    with Pool(min(len(jobs), int(os.environ.get("L381_POOL", "4")))) as pool:
        RES = dict(pool.map(harvey, jobs, chunksize=1))
    P(f"  {len(jobs)} kicks done   [{time.time() - T0:.0f}s]")

    banner("C1  CONTROL: L371's machinery reproduced")
    ref = json.load(open(os.path.join(REPO, "real_research", "merger_infall_2026", "L371_harvey_slow_kick_carrier_results.json")))["numbers"]["mean_beta"]["intact"]
    EST = ("100", "150", "fit")
    d1 = max(abs(RES[t]["MEAN"]["intact"][e] - ref[e]) for t in RES for e in EST)
    check("C1 the intact carrier reproduces L371's committed configuration-averaged excess beta (all estimators, every kick)",
          f"max |difference| {d1:.1e}", d1 < 1e-6)

    banner("HARVEY+2015 ON THE POOLED WINDOW (population-mean excess beta: 100 / 150 kpc / fit; bound <= +0.10)")
    PASS = {}
    for t in RES:
        M = RES[t]["MEAN"]
        for v in ("S1_med", "S2_med", "S3_med"):
            ok = all(M[v][e] <= -0.04 + 2 * 0.07 for e in EST)
            PASS[(t, v)] = ok
            P(f"    {t} {v}: " + "/".join(f"{M[v][e]:+.3f}" for e in EST) + f"  ({'/'.join(f'{(M[v][e] + 0.04) / 0.07:+.1f}' for e in EST)} sigma)"
              f"  -> {'pass' if ok else 'FAIL'};  carrier/baryons in 150 kpc: {RES[t]['CORE'][f'{v}|1e+14']:.2f} (1e14), {RES[t]['CORE'][f'{v}|3e+14']:.2f} (3e14)")
    OUT["numbers"].update(results=RES, passes={f"{k[0]}|{k[1]}": v for k, v in PASS.items()}, window=win)
    check("W (informational) S1, S2, S3 at every kick scored", "see table", True, "reported either way", load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    s2 = [t for t in RES if PASS[(t, "S2_med")]]
    check("R1 = H: at some kick in L380's pooled window the phase-mixed shape S2 passes Harvey on all three estimators",
          f"S2 passes at: {s2 or 'none'} (window {win or 'none'})", bool(win) and bool(s2) == EXPECT_PASS)

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o) if isinstance(o, (np.floating,)) else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
