#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE11 -- THE LYMAN-ALPHA FOREST FOR THE CONVERGED MODEL: the MOND-sector switch, vacuum-gated, on the flux observable.

WHY.  The model the threads converged on (MOND-sector switch lap(Phi - v) = baryons + their phantom, p = 1,
x_c0 = 2.5, a transition width w <~ 0.25, MS3's cap, the triggered carrier) now has KiDS (DE10), cosmic shear (MS3/MS4)
and the flagship (MS2) scored on one model.  Its forest gate has only DE2's dominance bracket.  That bracket compares
against a matter-reading cell with no phantom in the switch variable, and the MOND-sector reading does contain a
phantom.  This lane runs the forest observable directly: the 1D flux power at fixed mean transmission.

METHOD.  L347's machinery is imported unchanged: L176's PM (128^3 mesh, 96^3 particles, Zel'dovich ICs at z = 49 from
CLASS, the same phases in every run of a box), FGPA flux with the pressure filter, redshift-space velocities, thermal
broadening, and Becker+2013 tau_eff.  Two boxes are run, 50 and 25 Mpc/h.  Only the switch in the force is replaced:
  x_MS = (3/2) Omega_m(a) [f_b delta + delta_ph]      the MOND-sector reading (MS2): baryons ~ f_b (1 + delta) and
                                                       their phantom, less the baryonic background f_b.
  delta_ph = div[f (nu - 1) grad phi_N] / (1.5 Omega_m/a), the phantom's own density (in rho_bar_m units).  It is
      LAGGED one step: the gate reads the phantom of the previous step.  At z = 49 the gate is off, so each region
      switches on only when its own baryons (and then its phantom) cross the threshold -- the history-selected branch.
  threshold x_c,eff(a) = x_c0 E(z)^(2p), p = 1, x_c0 = 2.5 (the vacuum gate); f = W(t), t = (x_MS/x_c,eff - 1)/(2w) + 1/2,
  W = Mathlib's smoothTransition, w = 0.25 and 0.02 (hard).
CONSERVATIVE BY CONSTRUCTION.  The kernel reads all matter's Newtonian field, as in L347, and every particle feels the
phantom.  The converged model's region kernel reads only the gated baryons, and its carrier feels Newtonian gravity
only, so both choices here over-state the phantom.  A pass therefore carries over; a fail would need the two-species
run.
CHECKS
  C1 CONTROL: this lane's run() in L347's mode (matter reading, constant x_c = 5, L347's tanh switch) reproduces L347's
     committed 50 Mpc/h P1D ratio at x_c = 5 (canonical), z = 3 and 2, to 1e-6.
  C2 CONTROL: the switch never on reproduces LCDM's P1D exactly (both boxes).
  A1 (reported) the gate's reach: the active mesh fraction and the phantom's largest density at z = 3 and 2.
  F1 [pre-declared hypothesis, load-bearing] the converged model PASSES L347's registered rule: worst
     |P1D/P1D_LCDM - 1| <= 0.10 for k_par in [0.2, 2] h/Mpc, z = 3 and 2, both footings, both boxes, both widths.
MUTATE=1 swaps in L358's failing cell (matter reading, constant x_c = 2.5, L347's switch).  F1 must then FAIL, as L358
recorded (worst 0.174), rc = 1.

SCOPE.  Single-fluid PM (conservative, above); no carrier clearing; the cap is not applied (it binds only above
v_loc = 325 km/s, not in the forest); FGPA with a fixed temperature-density relation; one phase per box.

Run from the repository root:  python3 real_research/dark_energy_2026/DE11_forest_converged_model.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G03 = os.path.join(REPO, "real_research", "g03_audit_2026")
sys.path.insert(0, G03)
import L347_switch_forest_flux_power as L7                             # noqa: E402  (L347's machinery, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE11_forest_converged_model"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE11", "mutate": MUTATE, "checks": {}, "numbers": {}}
FB = 0.02237 / (0.02237 + 0.1200)
P_GATE, X_C0 = 1.0, 2.5
EXPECT_PASS = True                                                    # F1, set before the run
INF = float("inf")


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


def Wsm(t):
    t = np.asarray(t, float)
    tt = np.clip(t, 1e-6, 1 - 1e-6)
    ell = np.clip(1 / tt - 1 / (1 - tt), -700, 700)
    return np.where(t >= 1, 1.0, np.where(t <= 0, 0.0, 1 / (1 + np.exp(ell))))


def run(cfg):
    """L347's run() with the switch replaced.  mode: 'lcdm' | 'l347' (matter reading, constant xc, tanh) |
    'mond' (the MOND-sector reading, vacuum-gated, lagged phantom, width w)."""
    name, L, mode, foot, xc, w = cfg
    bx = L7.Box(L); NG, NP = L7.NG, L7.NP
    rng = np.random.default_rng(7)
    kk = np.sqrt(bx.K2); kk[0, 0, 0] = bx.kf
    Pk = np.vectorize(lambda q: L7.P_lin(q, L7.ZI))(np.clip(kk, bx.kf, 40.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    delta0 = np.real(np.fft.ifftn(white * np.sqrt(Pk * NG ** 3 / L ** 3)))
    psi = [-gg for gg in bx.grad(bx.poisson(delta0))]
    q = (np.arange(NP) + 0.5) * L / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([bx.interp(pp, Q) for pp in psi], 1)
    ai = 1 / (1 + L7.ZI); fg = L7.Om_a(ai) ** 0.55
    x = (Q + disp) % L; p = ai ** 2 * L7.Hnorm(ai) * fg * disp
    npart = len(x); a0 = L7.A0[foot]
    state = {"dph": np.zeros((NG, NG, NG)), "f": np.zeros((NG, NG, NG))}

    def accel(x, a):
        rho = bx.deposit(x, np.full(npart, 1.0)) * NG ** 3 / npart
        delta = rho - 1.0
        phiN = bx.poisson(1.5 * L7.Om * delta / a)
        if mode == "lcdm" or (not np.isfinite(xc)):
            phi = phiN
        else:
            gphi = bx.grad(phiN)
            mag = np.sqrt(sum((gg / a ** 2) ** 2 for gg in gphi)) + 1e-30
            nu = L7.nu_mono(mag / a0)
            if mode == "l347":                                                 # L347's switch, verbatim
                xs = 1.5 * L7.Om_a(a) * delta
                f = np.ones_like(xs) if xc == 0 else 0.5 * (1 + np.tanh((xs - xc) / (0.1 * xc)))
            else:                                                              # the MOND-sector door, vacuum-gated
                z = 1 / a - 1
                xce = xc * (L7.Om * (1 + z) ** 3 + L7.OL) ** P_GATE
                xs = 1.5 * L7.Om_a(a) * (FB * delta + state["dph"])
                f = Wsm((xs / xce - 1) / (2 * w) + 0.5)
            src = bx.div([f * (nu - 1) * gg for gg in gphi])
            phi = phiN + bx.poisson(src)
            state["dph"] = src / (1.5 * L7.Om / a)                            # the phantom's density, rho_bar_m units
            state["f"] = f
        return -np.stack([bx.interp(gg, x) for gg in bx.grad(phi)], 1)

    a = ai; dlna = 0.02; zs = list(L7.ZOUT); out = {}
    acc = accel(x, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * L7.Hnorm(a))
        p += 0.5 * dt * acc; x = (x + dt * p / a ** 2) % L; a = a + da
        acc = accel(x, a); p += 0.5 * dt * acc
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                kpar, p1d, A = L7.flux_p1d(bx, x, p, a, z)
                out[str(z)] = {"kpar": kpar.tolist(), "p1d": p1d.tolist(), "A": A,
                               "active": float(np.mean(state["f"] > 0.5)), "f_mean": float(np.mean(state["f"])),
                               "dph_max": float(np.max(state["dph"]))}
                zs.remove(z)
    return name, out


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: L358's failing cell (matter reading, constant x_c = 2.5) replaces the converged model; F1 must FAIL ***")
    cfgs = []
    for L in (50.0, 25.0):
        t = f"L{int(L)}"
        cfgs += [(f"{t}_lcdm", L, "lcdm", "canonical", 0, 0),
                 (f"{t}_never", L, "mond", "canonical", INF, 0.25)]
        for foot in ("canonical", "alt"):
            for w in ((0.25,) if MUTATE else (0.25, 0.02)):
                if MUTATE:
                    cfgs.append((f"{t}_{foot}_w{w}", L, "l347", foot, 2.5, w))     # L358's x_c = 2.5 cell
                else:
                    cfgs.append((f"{t}_{foot}_w{w}", L, "mond", foot, X_C0, w))
    cfgs.append(("L50_l347_x5_canonical", 50.0, "l347", "canonical", 5.0, 0))       # C1: L347's committed cell
    with Pool(int(os.environ.get("DE11_POOL", "6"))) as pool:
        res = dict(pool.map(run, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done   [{time.time() - T0:.0f}s]")

    def ratio(a_, b_, z):
        return np.array(res[a_][z]["p1d"]) / np.array(res[b_][z]["p1d"])

    banner("C1 C2  CONTROLS")
    R47 = json.load(open(os.path.join(G03, "L347_switch_forest_flux_power_results.json")))["numbers"]["runs"]
    c1 = max(float(np.max(np.abs(ratio("L50_l347_x5_canonical", "L50_lcdm", z)
                                  - np.array(R47["L50_sw5_canon"][z]["p1d"]) / np.array(R47["L50_lcdm"][z]["p1d"]))))
             for z in ("3.0", "2.0"))
    check("C1 CONTROL: this lane's run() in L347's mode reproduces L347's committed 50 Mpc/h P1D ratio at x_c = 5 (z = 3, 2)",
          f"max |difference| = {c1:.1e}", c1 < 1e-6)
    c2 = max(float(np.max(np.abs(ratio(f"{t}_never", f"{t}_lcdm", z) - 1))) for t in ("L50", "L25") for z in ("3.0", "2.0"))
    check("C2 CONTROL: the switch never on reproduces LCDM's P1D exactly (both boxes)", f"max |ratio - 1| = {c2:.1e}", c2 < 1e-9)

    banner("A1  THE GATE'S REACH IN THE BOX")
    A1 = {}
    for k_, d in res.items():
        if "_w" in k_:
            A1[k_] = {z: {"active": d[z]["active"], "f_mean": d[z]["f_mean"], "dph_max": d[z]["dph_max"]} for z in ("3.0", "2.0")}
            P(f"    {k_:22s}: active mesh fraction z = 3 {d['3.0']['active']:.2e}, z = 2 {d['2.0']['active']:.2e};  "
              f"mean f {d['2.0']['f_mean']:.2e};  largest phantom density {d['2.0']['dph_max']:.1f} rho_bar_m (z = 2)")
    OUT["numbers"]["A1"] = A1
    check("A1 (reported) the active mesh fraction and the phantom's reach at z = 3 and 2", "see above", True, load_bearing=False)

    banner("F1  THE FOREST OBSERVABLE: worst |P1D/P1D_LCDM - 1| for k_par in [0.2, 2] h/Mpc, z = 3 and 2")
    worst, cells = 0.0, {}
    for k_ in res:
        if "_w" not in k_: continue
        t = k_.split("_")[0]
        for z in ("3.0", "2.0"):
            kp = np.array(res[k_][z]["kpar"]); r = ratio(k_, f"{t}_lcdm", z)
            m = (kp >= 0.2) & (kp <= 2.0)
            dv = float(np.max(np.abs(r[m] - 1)))
            cells[f"{k_}/z{z}"] = dv; worst = max(worst, dv)
            P(f"    {k_:22s} z = {z}: worst {dv:.4f}  (ratio range {r[m].min():.3f}-{r[m].max():.3f})")
    OUT["numbers"]["F1"] = {"worst": worst, "cells": cells}
    ok = worst <= 0.10
    check("F1 [pre-declared] the converged model passes the registered forest rule (worst <= 0.10, both boxes, footings, widths)",
          f"worst {worst:.4f}", ok == EXPECT_PASS,
          "conservative: all-matter kernel and a single fluid over-state the phantom (see the docstring)")
    OUT["numbers"]["runs"] = {k_: {z: {kk_: v for kk_, v in d.items() if kk_ in ("A", "active", "f_mean", "dph_max")}
                                   for z, d in r_.items()} for k_, r_ in res.items()}

    nlb = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    P(f"\n  {sum(ok_ for _, ok_, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
