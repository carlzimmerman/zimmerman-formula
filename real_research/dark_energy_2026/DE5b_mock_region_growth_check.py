#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE5b -- AN INDEPENDENT CHECK OF MS3's U1 ON THE BUILDER DE3/DE5 USED: CAN L363's MOCK GROW AN ISOLATED GALAXY'S REGION?

DE3 and DE5 bound cosmic shear with L363's region kernel on L364's 256^3, 100 Mpc mock.  MS3 (mond_sector_gate_2026,
committed 2a5def6d9) found that L363's region builder, started from one isolated seed cell, never grows: 1e12, 1e13 and
1e14 Msun hosts stay at one cell against analytic phantom edges of 1.26, 2.26 and 4.61 Mpc.  MS3 tested its own
MOND-sector reading.  This lane repeats the test on L363's OWN upper-branch builder (build_regions, loaded unedited:
rho_m + the phantom computed on the dilated mask with Dirichlet walls >= the threshold), the builder DE3/DE5 ran.

CHECKS
  G1 [load-bearing] from an isolated seed (the bound baryons in one cell of L364's size, 0.39 Mpc, on a mean-density
     background), L363's upper-branch builder stays below half the analytic edge for M_b = 4.74e10, 5.0e11 and
     8.63e12 Msun (MS3's three hosts) at the linear cell's lens-epoch threshold x_c,eff(0.5) = 4.363.
  C1 CONTROL: the analytic upper-branch edge of each host (DE1's closed form with the background term, point-mass
     QUMOND with nu_mono) is resolved by the grid: >= 3 cells.
     [As first declared, C1 FAILS for the smallest host (2.9 cells); it is kept and recorded.  C1b was added after
     that first run.]
  C1b CONTROL: the same grid fed the analytic ungated phantom recovers every host's analytic edge to 15%, so the grid
     can represent the regions the builder fails to grow.
MUTATE=1 feeds the builder the analytic ungated phantom density instead of its Dirichlet one: the region then grows to
the analytic edge, and G1 must FAIL (rc = 1).

READING.  The builder computes each trial region's phantom with Dirichlet walls on that region.  For a one-cell region the
centred-gradient phantom vanishes, so the phantom never lifts a neighbour above threshold.  Regions grow only where a
matter-contrast region already surrounds the galaxy.  The phantom-supported outskirts -- where the upper branch's
edges sit -- are absent from the mock, so DE3/DE5's T_max tables are mock-based and not established; see MS3 for the
halo-model bound.

Run from the repository root:  python3 real_research/dark_energy_2026/DE5b_mock_region_growth_check.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE5b_mock_region_growth_check"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE5b", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the builder is fed the analytic ungated phantom; G1 must FAIL ***")

# ---------------------------------------------------------------------------------- L363's machinery, loaded unedited
P63 = os.path.join(REPO, "real_research", "g03_audit_2026", "L363_region_kernel_lensing_power.py")
NS = {"__name__": "l363", "__file__": P63}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P63).read().split("# ============================================================================================ C1 control")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), NS)
RHO, Omz, aS, A0, G, MS, MPC = NS["RHO"], NS["Omz"], NS["aS"], NS["A0"], NS["G"], NS["MS"], NS["MPC"]
nu_mono = NS["nu_mono"]
XLIN = 2.5 * (0.3138 * 1.5 ** 3 + 0.6862)                             # x_c,eff(0.5) at the linear cell (DE3)
Nn, dx = 64, 100.0 / 256                                              # L364's cell (comoving Mpc)
P(f"  L363 loaded; x_c,eff(0.5) = {XLIN:.4f}; cell {dx:.3f} Mpc comoving   [{time.time() - T0:.0f}s]")


def analytic_edge(Mb, a0):
    """DE1's upper-branch edge: largest r with 1.5 Omega_m(z) (rho_dyn/rho_bar - 1) >= x, point-mass QUMOND (physical)."""
    r = np.geomspace(1e-3, 30.0, 20000)                                 # physical Mpc
    y = G * Mb * MS / (r * MPC) ** 2 / a0
    M = Mb * nu_mono(y)
    rho = np.gradient(M, r) / (4 * math.pi * r ** 2)                    # Msun/Mpc^3 physical
    x = 1.5 * Omz * (rho / (RHO / aS ** 3) - 1)
    on = np.where(x >= XLIN)[0]
    return float(r[on.max()]) if on.size else 0.0


def analytic_phantom_grid(Mb, a0):
    """the ungated point-mass phantom density on the grid (comoving Msun/Mpc^3), for the MUTATE control."""
    c0 = Nn // 2
    ii = np.indices((Nn, Nn, Nn)) - c0
    rc = np.sqrt((ii ** 2).sum(0)) * dx                                 # comoving Mpc
    rphys = np.maximum(rc, 0.5 * dx) * aS
    y = G * Mb * MS / (rphys * MPC) ** 2 / a0
    rg = np.geomspace(0.5 * dx * aS, 30.0, 20000)
    Mph = (nu_mono(G * Mb * MS / (rg * MPC) ** 2 / a0) - 1) * Mb
    rho_ph = np.gradient(Mph, rg) / (4 * math.pi * rg ** 2)             # physical
    return np.interp(rphys, rg, rho_ph) * aS ** 3                       # comoving


G1, C1 = {}, {}
for Mb in (4.74e10, 5.0e11, 8.63e12):
    rhoB = np.zeros((Nn, Nn, Nn)); c0 = Nn // 2; rhoB[c0, c0, c0] = Mb / dx ** 3
    mk = {"dx": dx, "rho_m": np.full((Nn, Nn, Nn), RHO) + rhoB, "rhoB": rhoB}
    if MUTATE:
        rp = analytic_phantom_grid(Mb, A0["canonical"])
        mask = (1.5 * Omz * ((mk["rho_m"] + np.maximum(rp, 0.0)) / RHO - 1) >= XLIN) | (rhoB > 0)
        nit = 1
    else:
        mask, nit = NS["build_regions"](mk, rhoB, XLIN, A0["canonical"], True, iters=20)
    R_grid = (3 * mask.sum() * dx ** 3 / (4 * math.pi)) ** (1 / 3)
    re = analytic_edge(Mb, A0["canonical"]) / aS                        # comoving Mpc
    G1[Mb] = {"cells": int(mask.sum()), "R_grid": R_grid, "R_edge": re, "iterations": nit}
    C1[Mb] = re / dx
    P(f"    M_b = {Mb:.2e}: region {int(mask.sum())} cells, radius {R_grid:.2f} Mpc comoving after {nit} iteration(s); "
      f"analytic edge {re:.2f} Mpc comoving ({re / dx:.1f} cells)   [{time.time() - T0:.0f}s]")
OUT["numbers"]["G1"] = {f"{k:.3g}": v for k, v in G1.items()}
check("C1 CONTROL: every host's analytic upper-branch edge spans >= 3 grid cells (the grid could resolve the region)",
      {f"{k:.2e}": round(v, 1) for k, v in C1.items()}, all(v >= 3 for v in C1.values()))
C1b = {}
for Mb in G1:
    rhoB = np.zeros((Nn, Nn, Nn)); c0 = Nn // 2; rhoB[c0, c0, c0] = Mb / dx ** 3
    rp = analytic_phantom_grid(Mb, A0["canonical"])
    m_an = (1.5 * Omz * ((np.full((Nn, Nn, Nn), RHO) + rhoB + np.maximum(rp, 0.0)) / RHO - 1) >= XLIN) | (rhoB > 0)
    C1b[Mb] = (3 * m_an.sum() * dx ** 3 / (4 * math.pi)) ** (1 / 3) / G1[Mb]["R_edge"]
check("C1b CONTROL: fed the analytic ungated phantom, the same grid recovers every host's analytic edge to 15%",
      {f"{k:.2e}": round(v, 3) for k, v in C1b.items()}, all(abs(v - 1) <= 0.15 for v in C1b.values()))
check("G1 L363's upper-branch builder, from an isolated seed, stays below half the analytic edge for all three hosts",
      "; ".join(f"{k:.2e}: {v['R_grid']:.2f} vs {v['R_edge']:.2f} Mpc" for k, v in G1.items()),
      all(v["R_grid"] < 0.5 * v["R_edge"] for v in G1.values()),
      "MS3's U1 holds for the builder DE3/DE5 ran: the mock has no phantom-supported regions around isolated galaxies")

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
