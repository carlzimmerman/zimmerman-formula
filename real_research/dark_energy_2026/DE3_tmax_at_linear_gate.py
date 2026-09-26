#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE3 -- THE COSMIC-SHEAR BOUND AT THE LINEAR GATE: L363's region-kernel T_max(k), s^2 and r_x at the lens-epoch threshold
of DE2's linear-gate cell (p = 1, x_c0 = 2.5), exported as a table for a same-cell re-run of the construction.

WHY.  DE2 found a joint window for the vacuum gate that contains the linear gate p = 1; L359's cell (p = 1, x_c0 = 2.5)
passes KiDS, cosmic shear, the flagship and the forest.  DE2's results store the cosmic-shear MARGINS against L367's
committed transfers, not the bound itself.  A same-cell re-run of the particle-mesh construction (with its own nonlinear
transfer at that cell) needs the bound
      T_max(k) = -r_x s + sqrt(r_x^2 s^2 + 1.2 - s^2),   s^2 = P_ph/P_NL,   R = T^2 + 2 r_x T s + s^2 <= 1.2   (L364)
at the cell's lens-epoch threshold.  This lane computes it with L363's machinery (unedited), GP3's mock at z = 0.5 and
L364's seed, exactly as L364 and DE2 do.

THE CELL.  x_c,eff(0.5) = x_c0 [Omega_L0/Omega_L(0.5)]^p = 2.5 E^2(0.5), with E^2(0.5) = N63["E2"] = 1.745209 (GP3's mock
background, as L364/DE2 use; L359's L347 background gives 1.745275, 4e-5 relative): x = 4.36302.

CHECKS
  C1 CONTROL: L364's committed T_max at its two cells, both footings, reproduced exactly (1e-12).
  C2 CONTROL: DE2's committed cosmic-shear margins at the grid thresholds 4.2 and 4.4, against L367's transfers, both
     footings and all three kicks, reproduced (1e-12).
  T1 the cell's T_max(k) lies between the bracketing grid values (4.2, 4.4) at every k and footing (DE2 M1: monotone).
  S1 THE CELL'S VERDICT with L367's committed transfers: cosmic shear passes at v_k = 600, 650 and 700 km/s on both
     footings (max_k [T - T_max] < 0).
  E1 (reported, the export) T_max, s^2 and r_x per k and footing at the cell and at 4.2/4.4, in the results JSON.
MUTATE=1 evaluates the UNGATED threshold x = x_c0 = 2.5 at z = 0.5 (p = 0) in place of the cell: S1 must FAIL at 600 km/s
(rc = 1) -- the pass rests on the vacuum's growth between z = 0 and z = 0.5.

SCOPE.  The bound is L364's: one lens epoch (z = 0.5), P(k) not a projected xi_+-, r_x measured against the full matter
field.  The transfer used for S1 is L367's single-box Newtonian particle-mesh transfer; a same-cell re-run should use its
own transfer against this table.

Run from the repository root:  python3 real_research/dark_energy_2026/DE3_tmax_at_linear_gate.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from multiprocessing import get_context
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE3_tmax_at_linear_gate"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE3", "mutate": MUTATE, "checks": {}, "numbers": {}}
G03 = os.path.join(REPO, "real_research", "g03_audit_2026")
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
FEET = ("canonical", "alt")
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the ungated threshold x = x_c0 = 2.5 replaces the cell's; S1 must FAIL at 600 km/s ***")

# ---------------------------------------------------------------------------------- L363's machinery, loaded unedited
P63 = os.path.join(G03, "L363_region_kernel_lensing_power.py")
N63 = {"__name__": "l363", "__file__": P63}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P63).read().split("# ============================================================================================ C1 control")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), N63)
eS = N63["E2"]
OM47 = 0.3138
XCELL = 2.5 * (1.0 if MUTATE else eS)
XCELL_L359 = 2.5 * (OM47 * 1.5 ** 3 + 1 - OM47)
L364 = json.load(open(os.path.join(G03, "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]
L367 = json.load(open(os.path.join(DS, "L367_triggered_carrier_cosmic_shear_results.json")))["numbers"]["transfer"]
TRANS = {int(k_[1:]): {float(q): v_ for q, v_ in d_["T"].items()} for k_, d_ in L367.items()}
DE2 = json.load(open(os.path.join(HERE, "DE2_vacuum_gate_joint_window_results.json")))["numbers"]
P(f"  L363 loaded (mock E^2(0.5) = {eS:.6f}); the cell's threshold x = {XCELL:.5f}"
  + (f" (L359's background would give {XCELL_L359:.5f})" if not MUTATE else " (UNGATED, p = 0)"))

MK = N63["build_mock"](100.0, 256, 20260926)                          # L364's mock and seed
P(f"  GP3 mock built (100 Mpc, 256^3, seed 20260926)   [{time.time() - T0:.0f}s]")


def bound_at(args):
    xc, foot = args
    src = MK["rhoB"]
    mask, _ = N63["build_regions"](MK, src, xc, A0[foot])
    rp, _, _, _ = N63["region_phantom"](MK, mask, src * mask, A0[foot])
    pk = N63["spectra"](MK, {"m": MK["rho_m"] / N63["RHO"] - 1, "ph": rp / N63["RHO"]})
    kh, Pmm = pk("m", "m"); _, Pxx = pk("m", "ph"); _, Ppp = pk("ph", "ph")
    rx = Pxx / np.sqrt(np.maximum(Pmm * Ppp, 1e-300)); s2 = Ppp / N63["PNL_of"](kh)
    S2 = {q: float(np.interp(q, kh, s2)) for q in KG}; RX = {q: float(np.interp(q, kh, rx)) for q in KG}
    TM = {q: (-RX[q] * math.sqrt(S2[q]) + math.sqrt(max(RX[q] ** 2 * S2[q] + 1.2 - S2[q], 0.0))) for q in KG}
    return (xc, foot, TM, S2, RX)


C1_CELLS = {"p=1, x_c0=1.5": 1.5 * eS, "p=2, x_c0=2.0": 2.0 * eS ** 2}
XS = [XCELL, 4.2, 4.4] + list(C1_CELLS.values())
with get_context("fork").Pool(3) as pool:
    res = pool.map(bound_at, [(x, f) for x in XS for f in FEET], chunksize=1)
TAB = {(round(x, 7), f): dict(T_max=t, s2=s, rx=r) for x, f, t, s, r in res}
P(f"  bound computed at {len(res)} (threshold, footing) points   [{time.time() - T0:.0f}s]")

# ============================================================================================ C1, C2 controls
banner("C1-C2  CONTROLS: L364's committed T_max; DE2's committed margins at 4.2 and 4.4")
d1 = max(abs(TAB[(round(x, 7), f)]["T_max"][q] - L364[f"{c}/{f}"][str(q)]) for c, x in C1_CELLS.items() for f in FEET for q in KG)
check("C1 CONTROL: L364's committed T_max reproduced exactly at its two cells, both footings", f"max |diff| = {d1:.1e}", d1 < 1e-12)
d2 = 0.0
for vk, T in TRANS.items():
    for f in FEET:
        for x in (4.2, 4.4):
            m = max(T[q] - TAB[(round(x, 7), f)]["T_max"][q] for q in KG)
            d2 = max(d2, abs(m - DE2["margin"][f"{vk}/{f}"][str(x)]))
check("C2 CONTROL: DE2's committed cosmic-shear margins at x = 4.2 and 4.4 reproduced (all kicks, both footings)",
      f"max |diff| = {d2:.1e}", d2 < 1e-12)

# ============================================================================================ T1, S1
banner("T1-S1  THE CELL: its bound between the grid neighbours, and cosmic shear with L367's committed transfers")
between = all(min(TAB[(4.2, f)]["T_max"][q], TAB[(4.4, f)]["T_max"][q]) - 1e-12 <= TAB[(round(XCELL, 7), f)]["T_max"][q]
              <= max(TAB[(4.2, f)]["T_max"][q], TAB[(4.4, f)]["T_max"][q]) + 1e-12 for f in FEET for q in KG)
if MUTATE:
    P("  [n/a ] T1 not applicable under MUTATE: the ungated threshold 2.5 lies outside [4.2, 4.4] by construction")
    OUT["checks"]["T1"] = {"ok": None, "measured": "not applicable under MUTATE", "load_bearing": False}
else:
    check("T1 the cell's T_max(k) lies between the bracketing grid values at every k and footing (monotone in the threshold)",
          f"{between}", between, "the table is consistent with DE2's monotone floor")
MARG = {}
for vk, T in sorted(TRANS.items()):
    for f in FEET:
        MARG[(vk, f)] = max(T[q] - TAB[(round(XCELL, 7), f)]["T_max"][q] for q in KG)
    P(f"    v_k = {vk}: margin max_k [T - T_max] canonical {MARG[(vk, 'canonical')]:+.4f}, alt {MARG[(vk, 'alt')]:+.4f}")
okS = all(m < 0 for m in MARG.values())
check("S1 THE CELL'S VERDICT: cosmic shear passes at v_k = 600, 650 and 700 km/s on both footings with L367's transfers",
      "; ".join(f"{vk}/{f}: {m:+.4f}" for (vk, f), m in MARG.items()), okS,
      "the linear gate's lens-epoch threshold leaves room for the carrier's matter power at every committed kick")

# ============================================================================================ E1 export
banner("E1  THE EXPORT: T_max, s^2 = P_ph/P_NL and r_x per k and footing")
for x in (XCELL, 4.2, 4.4):
    for f in FEET:
        t = TAB[(round(x, 7), f)]
        P(f"    x = {x:.5f} {f:9s}: T_max " + ", ".join(f"{q}: {t['T_max'][q]:.4f}" for q in KG))
        P(f"                      s^2   " + ", ".join(f"{q}: {t['s2'][q]:.4g}" for q in KG))
        P(f"                      r_x   " + ", ".join(f"{q}: {t['rx'][q]:.4f}" for q in KG))
OUT["numbers"]["cell"] = dict(p=0.0 if MUTATE else 1.0, x_c0=2.5, E2_mock=eS, x_lens=XCELL, x_lens_L359_background=XCELL_L359)
OUT["numbers"]["table"] = {f"{x:.7f}/{f}": {k_: {str(q): v_[q] for q in KG} for k_, v_ in TAB[(round(x, 7), f)].items()}
                           for x in (XCELL, 4.2, 4.4) + tuple(C1_CELLS.values()) for f in FEET}
OUT["numbers"]["margins_L367"] = {f"{vk}/{f}": m for (vk, f), m in MARG.items()}
check("E1 (reported) the table is written for the cell and its grid neighbours, both footings", "see results JSON", True,
      load_bearing=False)

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail
OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
