#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L389 -- HARVEY+2015 SAME-CELL AT THE LINEAR VACUUM GATE (p = 1, x_c0 = 2.5): the merger step with the SAME switch as the
particle-mesh runs whose retention it uses.

WHY.  L381's Harvey verdict is withdrawn (correction 3151d88f2): its adapter never replaced L370/L371's switch
(SW_DEF = "p1_x1.5", active in the lensing-mass root and both phantom maps) while its retentions came from L377's p = 2,
x_c0 = 2 cell.  DE1/DE2 moved the construction to the linear gate p = 1, x_c0 = 2.5, and L388 re-ran the pooled
cosmology there.  This lane runs Harvey at that SAME cell on L388's pooled retention.

METHOD.  L371's script, loaded unedited except for its inputs (as L381), now INCLUDING the switch: right after L371 binds
L370's machinery, the cell is added to L370's SWITCH table and SW_DEF is set to it, which reaches all three active uses
(L370's lensing() and phantom_felt() take the cell explicitly; no default argument carries it).  L371's own checks and
output files are cut; its committed results are never touched.  The resolved cell, x_c,eff at the merger epoch z = 0.4
and the retention used are recorded per job.  Retention: L388's pooled medians in L371's bins and mapping (M(<1 Mpc/h)
6e13-1e14 -> lensing 1e14 Msun; 1.5e14-2.5e14 -> 3e14; >= 2.5e14 -> the 1e15 main cluster).  One process per job.
PRE-DECLARED (before the run): H: at some kick in L388's pooled window the phase-mixed shape S2 passes Harvey SAME-CELL --
the population-mean excess beta is <= +0.10 on all three estimators (100 kpc, 150 kpc, Lenstool-like fit).
PROVISIONAL, EITHER SIGN: retention is measured at z = 0 (L388) and applied at the z = 0.4 merger epoch (L371's inherited
practice); retention is not strictly monotone in time (L375: retained carrier is mostly undecayed infall), so the verdict
stands only until a same-epoch re-run.  Same cell, NOT yet the same model (XR1): the PM and merger phantom operators and
switch variables differ, and both stages are canonical-footing only.
CHECKS
  C1 CONTROL (gate-matched): the adapter with the switch LEFT at L371's p = 1, x_c0 = 1.5 and L381's inputs (L380's 600 km/s
     retention) reproduces L381's committed S1/S2/S3 and intact values exactly -- the switch assignment is the only change.
  C2 CONTROL: the switch took effect -- x_c,eff(0.4) of the jobs equals 2.5 E(0.4)^2 (the cell), not L371's 1.5 E(0.4)^2.
  R1 = H.  W (informational): S1, S2, S3 and the intact carrier at the new cell, every kick; carrier/baryons inside 150 kpc.
MUTATE=1: every retention is quartered (a hollowed carrier): R1 must FAIL (rc = 1).
L389_POOL sets the pool size (default 3; each job needs ~13 GB).

Run from the repository root after L388:  python3 real_research/dark_sector_2026/L389_harvey_same_cell_linear_gate.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
P71 = os.path.join(REPO, "real_research", "merger_infall_2026", "L371_harvey_slow_kick_carrier.py")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L389_harvey_same_cell_linear_gate"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L389", "cell": "p=1, x_c0=2.5", "mutate": MUTATE, "checks": {}, "numbers": {},
               "operators": {                                # SAME CELL, NOT YET THE SAME OPERATOR (cross-thread review, astra item 1)
                   "retention_source": "L388 PM (L377 phantom()): Newtonian field of ALL baryons on the periodic mesh; switch mask "
                                       "on the background-subtracted x~ = 1.5 Omega_m(a) delta_total at the cell; curl-free QUMOND of "
                                       "f (nu_mono - 1) g_N,b; carrier Newtonian; trigger on x~ + 1.5 Omega_m(a) delta_ph",
                   "merger_step": "L370 phantom_felt()/RealHalo.lensing(): each connected region's OWN baryons; switch mask on "
                                  "the absolute 1.5 rho/rho_crit(z) >= x_c,eff; same cell p = 1, x_c0 = 2.5, z = 0.4",
                   "status": "operator identity NOT established between the two steps; a resolved-halo comparison is pending"},
               "epoch": "retention measured at z = 0 (L388), applied at the z = 0.4 merger epoch (L371:85 practice): PROVISIONAL either sign",
               "footing": "canonical only (PM and merger stages)"}
EXPECT_PASS = True                                               # H, set before the run
CELL, CELL_PX = "p1_x2.5", (1.0, 2.5)
BINMAP = {1e14: "6.0e+13-1.0e+14", 3e14: "1.5e+14-2.5e+14", 1e15: "2.5e+14-1.0e+17"}   # L371's mapping of L366's bins
EST = ("100", "150", "fit")


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


def harvey_cell(job):
    """L371's machinery with its retention table, kick AND switch cell replaced (switch=None leaves L371's own cell)."""
    tag, eps_med, vk, switch = job
    src = open(P71).read()
    reps = [('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"),
            ('EPS = {"med": {1e14: 0.18, 3e14: 0.40, 1e15: 0.75}, "max": {1e14: 0.26, 3e14: 0.73, 1e15: 0.80}}',
             f'EPS = {{"med": {{1e14: {eps_med[1e14]!r}, 3e14: {eps_med[3e14]!r}, 1e15: {eps_med[1e15]!r}}}, "max": {{1e14: 1.0, 3e14: 1.0, 1e15: 1.0}}}}'),
            ("VK = 650.0", f"VK = {float(vk)!r}"),
            ('            "S1_max": ("S1", "max")}', "            }")]
    if switch is not None:
        name, (p_, x_) = switch
        a = '    "RealHalo", "cum_mass", "m_in", "RG", "GK", "A0K", "SW_DEF", "Grid", "phantom_felt"))'
        reps.append((a, a + f'\nL["SWITCH"][{name!r}] = ({p_!r}, {x_!r}); SW_DEF = {name!r}               # L389: the PM runs\' cell'))
    for a, b in reps:
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    MARK = "# ================================================================================================ checks"
    assert src.count(MARK) == 1
    src = src.split(MARK)[0]
    ns = {"__name__": "l371_in_l389", "__file__": P71}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, "L371(L389 inputs)", "exec"), ns)
    xce = float(ns["L"]["x_ceff"](0.4, ns["SW_DEF"]))
    return tag, dict(MEAN=ns["MEAN"], CORE={f"{k[0]}|{k[1]:.0e}": float(v) for k, v in ns["CORE"].items()},
                     SW_DEF=ns["SW_DEF"], x_ceff_z04=xce, Ez2_z04=float(ns["L"]["Ez2"](0.4)))


if __name__ == "__main__":
    P(__doc__)
    R88 = json.load(open(os.path.join(HERE, "L388_linear_gate_pooled_results.json")))["numbers"]
    assert json.load(open(os.path.join(HERE, "L388_linear_gate_pooled_results.json"))).get("cell") == "p=1, x_c0=2.5"
    win = R88["windows"]["pooled"]
    kicks = win if win else list(R88["retention_by_mass"].keys())
    P(f"  L388's pooled window (cell p = 1, x_c0 = 2.5): {win or 'none'}; kicks scored here: {kicks}")
    jobs = []
    for t in kicks:
        rb = R88["retention_by_mass"][t]
        eps = {Ml: float(rb[b][0]) * (0.25 if MUTATE else 1.0) for Ml, b in BINMAP.items()}
        OUT["numbers"].setdefault("retention_used", {})[t] = {f"{k:.0e}": v for k, v in eps.items()}
        P(f"    {t}: retention used (lensing 1e14 / 3e14 / 1e15) = {eps[1e14]:.3f} / {eps[3e14]:.3f} / {eps[1e15]:.3f}")
        jobs.append((t, eps, float(t[1:]), (CELL, CELL_PX)))
    if not MUTATE:                                               # C1: L381's own inputs and cell, through this adapter
        R80 = json.load(open(os.path.join(HERE, "L380_pooled_window_fixed_cell_clearing_results.json")))["numbers"]["retention_by_mass"]["v600"]
        jobs.append(("C1_L381_v600", {Ml: float(R80[b][0]) for Ml, b in BINMAP.items()}, 600.0, None))
    if MUTATE:
        P("  MUTATE: every retention quartered (a hollowed carrier)")
    with Pool(min(len(jobs), int(os.environ.get("L389_POOL", "3")))) as pool:
        RES = dict(pool.map(harvey_cell, jobs, chunksize=1))
    P(f"  {len(jobs)} jobs done   [{time.time() - T0:.0f}s]")

    banner("C1, C2  CONTROLS")
    if not MUTATE:
        R81 = json.load(open(os.path.join(HERE, "L381_harvey_on_pooled_window_results.json")))["numbers"]["results"]["v600"]["MEAN"]
        c1 = RES["C1_L381_v600"]["MEAN"]
        d1 = max(abs(c1[v][e] - R81[v][e]) for v in ("intact", "S1_med", "S2_med", "S3_med") for e in EST)
        check("C1 (gate-matched) the adapter with L371's own switch and L381's inputs reproduces L381's committed intact, S1, S2 "
              "and S3 values exactly -- the switch assignment is the only change", f"max |difference| {d1:.1e}", d1 < 1e-9)
    KT = [t for t in kicks]
    xs = {t: RES[t]["x_ceff_z04"] for t in KT}; ez = RES[KT[0]]["Ez2_z04"]
    ok2 = all(abs(x / (CELL_PX[1] * ez ** CELL_PX[0]) - 1) < 1e-12 and RES[t]["SW_DEF"] == CELL for t, x in xs.items())
    check("C2 the switch took effect: every job ran at x_c,eff(0.4) = 2.5 E(0.4)^2 (the cell), not L371's 1.5 E(0.4)^2",
          f"x_c,eff(0.4) = {sorted(set(round(x, 6) for x in xs.values()))} vs cell {CELL_PX[1] * ez:.6f}, L371 {1.5 * ez:.6f}; SW_DEF "
          f"{sorted(set(RES[t]['SW_DEF'] for t in KT))}", ok2)

    banner("HARVEY+2015 SAME-CELL (population-mean excess beta: 100 / 150 kpc / fit; bound <= +0.10)")
    PASS = {}
    for t in KT:
        M = RES[t]["MEAN"]
        P(f"    {t} intact (same cell): " + "/".join(f"{M['intact'][e]:+.3f}" for e in EST))
        for v in ("S1_med", "S2_med", "S3_med"):
            ok = all(M[v][e] <= -0.04 + 2 * 0.07 for e in EST)
            PASS[(t, v)] = ok
            P(f"    {t} {v}: " + "/".join(f"{M[v][e]:+.3f}" for e in EST) + f"  ({'/'.join(f'{(M[v][e] + 0.04) / 0.07:+.1f}' for e in EST)} sigma)"
              f"  -> {'pass' if ok else 'FAIL'};  carrier/baryons in 150 kpc: {RES[t]['CORE'][f'{v}|1e+14']:.2f} (1e14), {RES[t]['CORE'][f'{v}|3e+14']:.2f} (3e14)")
    OUT["numbers"].update(results=RES, passes={f"{k[0]}|{k[1]}": v for k, v in PASS.items()}, window=win)
    check("W (informational) S1, S2, S3 and the intact carrier at the new cell, every kick", "see table", True, "reported either way",
          load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    s2 = [t for t in KT if PASS[(t, "S2_med")]]
    check("R1 = H (PROVISIONAL: z = 0 retention at z = 0.4): at some kick in L388's pooled window the phase-mixed shape S2 passes "
          "Harvey same-cell (all three estimators)",
          f"S2 passes at: {s2 or 'none'} (window {win or 'none'})", bool(win) and bool(s2) == EXPECT_PASS)

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o) if isinstance(o, np.floating) else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
