#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE6 -- DE1 ON THE MATTER-ONLY BRANCH, CELL BY CELL: across the vacuum-gate window, how far back in time does each gate
cell keep MOND on at the flagship radius when the switch reads matter only (the lower branch the particle-mesh
construction runs), and how does that compare with DE1's upper branch?  Reported per labelled cell, never pooled.

WHY.  DE1 found the flagship caps the gate exponent on the upper branch (the switch reads baryons + phantom): p <= 1.97 at
x_c0 = 2, with z_max = 4.2-5.0 for the p = 1 cells and 2.46-2.70 for p = 2.  DE4 found that on the lower branch -- the
switch reads matter only, L377's "x~_m" -- the linear cell (p = 1, x_c0 = 2.5) keeps the flagship at z = 2.5 only when the
carrier is essentially gone AND circumgalactic gas holds the gate open (>~ 30% of L375's maximal share).  The user asked
for every switch variable to be explored as its own branch.  This lane runs DE1's questions on the lower branch for every
window cell, for two readings of the switch variable:
  * CONTRAST (L377's, the Hamiltonian-constraint form of L346/Lean I26):  1.5 Omega_m(z) (rho/rho_bar - 1) >= x_c,eff(z);
  * ABSOLUTE (L342's static form):                                          1.5 Omega_m(z) rho/rho_bar     >= x_c,eff(z),
with x_c,eff(z) = x_c0 E(z)^(2p) and rho the local matter density (baryons + CGM + retained carrier).

THE GALAXY: DE4's, loaded unedited (L375's Hernquist baryons and NFW-shaped CGM share f_CGM, L320's Moster halo for the
carrier's shape, retained fraction S; the flagship radius r_F where g_bar = 0.1 a0 for point-mass baryons, GP5's shift).

THE CELLS: L359's eight (the p = 2, x_c0 = 2 cell kept as a reference though DE1 excludes it), and three window corners from
DE2: (0.5, 3.39) and (1.0, 2.975) (the KiDS-capped top of x_c0 at p = 1/2 and 1), and the window's top-threshold corner
(p*, x0*) where the KiDS and flagship caps bind together (DE5 W1's closed form).

CHECKS
  C1 CONTROL: at the linear cell, contrast reading, DE4's committed F1 shifts are reproduced exactly (1e-12).
  C2 CONTROL: with the upper-branch density and no extra matter (point-mass baryons, S = 0, f_CGM = 0), DE1's committed
     z_max for the eight L359 cells is reproduced (0.02 in z).
  H1 PRE-DECLARED HYPOTHESIS (written before the run, from DE4): on the lower branch, contrast reading, with the carrier
     fully cleared (S = 0): (a) at f_CGM = 0.3 the p <= 1 window cells keep the flagship at z = 2.5 for M_b = 1e10-1e11 on
     both footings while the p = 2 cells lose it; (b) at f_CGM = 0.1 every window cell loses it at M_b = 1e11.
  V1 (reported) the absolute reading moves the lower-branch threshold density by the factor x/(1 + x) with
     x = x_c,eff/(1.5 Omega_m); its effect on z_max per cell.
  Z1 (reported) z_max per cell, branch reading and scenario (S in {0, 0.06}, f_CGM in {0.1, 0.3, 1}), both footings.
  L1 THE BRANCHES DIFFER: per cell, scenario, reading and footing, z_max(lower) <= z_max(upper, same matter), strictly
     lower somewhere (the discriminating check for the control).
MUTATE=1 reads the upper-branch (phantom-inclusive) density for the "lower" switch: L1 must FAIL (the two coincide), rc = 1.
(Note added after the first run: H1(b) was falsified -- at f_CGM = 0.1 the p = 0.5 cells and (1, 1.5) keep the flagship;
H1 is left load-bearing and its failure recorded, and L1 is the check the control flips.)

SCOPE.  Spherical, isolated galaxies at the flagship radius; LambdaCDM-shaped CGM and carrier profiles (L375's convention);
the switch evaluated at r_F on a monotone profile; the formation history that selects the branch is not modelled.

Run from the repository root:  python3 real_research/dark_energy_2026/DE6_flagship_window_matter_only.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy.optimize import brentq
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE6_flagship_window_matter_only"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE6", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the switch reads the upper-branch (phantom-inclusive) density; H1 must fail ***")

# ---------------------------------------------------------------------------------- DE4's machinery, loaded unedited
P4 = os.path.join(HERE, "DE4_flagship_matter_only_switch.py")
D4 = {"__name__": "de4", "__file__": P4}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P4).read().split("# ============================================================================================ C1-C3 controls")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D4)
halo, rho_matter, rho_phantom_on, nu, g_nfw = D4["halo"], D4["rho_matter"], D4["rho_phantom_on"], D4["nu"], D4["g_nfw"]
A0, G, MSUN, KPC, MSUN_PC3 = D4["A0"], D4["G"], D4["MSUN"], D4["KPC"], D4["MSUN_PC3"]
E2, Om_z, rho_bar_m = D4["E2"], D4["Om_z"], D4["rho_bar_m"]
DE4R = json.load(open(os.path.join(HERE, "DE4_flagship_matter_only_switch_results.json")))["numbers"]
DE1R = json.load(open(os.path.join(HERE, "DE1_vacuum_gate_flagship_results.json")))["numbers"]
D2 = json.load(open(os.path.join(HERE, "DE2_vacuum_gate_joint_window_results.json")))["numbers"]
P(f"  DE4 machinery loaded   [{time.time() - T0:.1f}s]")

MBS = (10.0, 10.5, 11.0); FEET = ("canonical", "alt")
L359_CELLS = [(0.5, 1.5), (0.5, 2.0), (0.5, 2.5), (1.0, 1.5), (1.0, 2.0), (1.0, 2.5), (2.0, 1.5), (2.0, 2.0)]
# the top-threshold corner (DE5 W1's closed form from DE2's committed caps: both caps bind at p*)
XK = min(D2["KiDS"]["X_K_exact"].values()); XF = min(v for k_, v in D2["XF"].items() if float(k_.split("/")[1]) <= 11.0)
_ps = math.log(XF / XK) / math.log(E2(2.5) / E2(0.25)); TOP = (round(_ps, 4), round(XK / E2(0.25) ** _ps, 4))
CELLS = L359_CELLS + [(0.5, 3.39), (1.0, 2.975), TOP]


def threshold(z, p, xc0, reading):
    x = xc0 * E2(z) ** p / (1.5 * Om_z(z))
    return rho_bar_m(z) * ((1 + x) if reading == "contrast" else x)


def switch_on(Mb, foot, z, p, xc0, S, fcgm, reading, upper=False, bare=False):
    a0 = A0[foot]; H = halo(Mb, z)
    rF = math.sqrt(G * Mb * MSUN / (0.1 * a0))
    rm = 0.0 if bare else rho_matter(Mb, z, rF, S, fcgm, H)[0]
    rho = rm + (rho_phantom_on(Mb, a0, rF) if upper else 0.0)
    return rho >= threshold(z, p, xc0, reading), rF, H


def shift(Mb, foot, z, p, xc0, S, fcgm, reading, upper=False, bare=False):
    on, rF, H = switch_on(Mb, foot, z, p, xc0, S, fcgm, reading, upper, bare)
    a0 = A0[foot]; g_fw = float(nu(0.1)) * 0.1 * a0
    g = (g_fw if on else 0.1 * a0) + S * g_nfw(H["Mh"], z, rF)
    return 2 * math.log10(g / g_fw), on


def z_max(foot, p, xc0, S, fcgm, reading, upper=False, bare=False):
    """highest z at which the switch stays on at r_F for all three flagship masses (bisection; 0 if off at z = 0)."""
    ok = lambda z: all(switch_on(10 ** l, foot, z, p, xc0, S, fcgm, reading, upper, bare)[0] for l in MBS)
    if not ok(0.0):
        return 0.0
    if ok(12.0):
        return float("inf")
    lo, hi = 0.0, 12.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    return lo


# ============================================================================================ C1, C2 controls
banner("C1-C2  CONTROLS: DE4's committed shifts at the linear cell; DE1's committed z_max on the upper branch")
d1 = 0.0
for fc in (0.1, 0.3, 1.0):
    for S in (0.0, 0.06, 0.1, 0.3, 1.0):
        rows = DE4R["F1"][f"{fc}/{S}"]["rows"]
        mine = [shift(10 ** l, f, 2.5, 1.0, 2.5, S, fc, "contrast")[0] for l in MBS for f in FEET]
        d1 = max(d1, max(abs(a - b["shift"]) for a, b in zip(mine, rows)))
check("C1 CONTROL: DE4's committed F1 shifts reproduced exactly at the linear cell (contrast reading, 15 scenarios)",
      f"max |diff| = {d1:.1e} dex", d1 < 1e-12)
d2 = 0.0
for (p, xc0) in L359_CELLS:
    for f in FEET:
        zm = z_max(f, p, xc0, 0.0, 0.0, "contrast", upper=True, bare=True)
        d2 = max(d2, abs(zm - DE1R["F2"][f"{p}/{xc0}/{f}"]))
check("C2 CONTROL: with the upper-branch density and point-mass baryons only, DE1's committed z_max is reproduced for all "
      "eight L359 cells, both footings (0.02)", f"max |dz| = {d2:.3f}", d2 < 0.02,
      "the same threshold variable as DE1 (4 pi G (rho - rho_bar)/H^2 = 1.5 Omega_m (rho/rho_bar - 1)); DE4's analytic "
      "phantom density at r_F against L352's numeric edge")

# ============================================================================================ Z1 the table
banner("Z1  z_max PER CELL ON THE " + ("UPPER (MUTATE)" if MUTATE else "LOWER (MATTER-ONLY)") + " BRANCH, BOTH READINGS")
SC = [(0.0, 0.1), (0.0, 0.3), (0.0, 1.0), (0.06, 0.1), (0.06, 0.3), (0.06, 1.0)]
Z1 = {}
for reading in ("contrast", "absolute"):
    for (p, xc0) in CELLS:
        for (S, fc) in SC:
            for f in FEET:
                Z1[f"{reading}/{p}/{xc0}/{S}/{fc}/{f}"] = z_max(f, p, xc0, S, fc, reading, upper=MUTATE)
        P(f"    {reading:8s} cell (p = {p:5.3f}, x_c0 = {xc0:5.3f}): z_max canonical/alt for (S, f_CGM) = " + "; ".join(
            f"({S}, {fc}): {Z1[f'{reading}/{p}/{xc0}/{S}/{fc}/canonical']:.2f}/{Z1[f'{reading}/{p}/{xc0}/{S}/{fc}/alt']:.2f}"
            for (S, fc) in SC))
OUT["numbers"]["z_max"] = Z1
# the upper branch with the SAME matter (baryons + CGM + carrier + the phantom), for the branch comparison L1
ZU = {}
for reading in ("contrast", "absolute"):
    for (p, xc0) in CELLS:
        for (S, fc) in SC:
            for f in FEET:
                ZU[f"{reading}/{p}/{xc0}/{S}/{fc}/{f}"] = z_max(f, p, xc0, S, fc, reading, upper=True)
OUT["numbers"]["z_max_upper_same_matter"] = ZU
fin = lambda v: v if math.isfinite(v) else 99.0
le = all(fin(Z1[k_]) <= fin(ZU[k_]) + 1e-9 for k_ in Z1)
gap = max(fin(ZU[k_]) - fin(Z1[k_]) for k_ in Z1)
check("L1 THE BRANCHES DIFFER: for every cell, scenario, reading and footing the matter-only branch keeps MOND at the "
      "flagship radius to no higher redshift than the upper branch with the same matter, and to a strictly lower one "
      "somewhere", f"all <=: {le}; largest z_max gap (upper - lower) = {gap:.2f}", le and gap > 0.05,
      "the phantom's own density is what lets the upper branch hold the gate open; the lower branch has only matter")

# ============================================================================================ H1 the hypothesis
banner("H1  THE PRE-DECLARED HYPOTHESIS AT z = 2.5 (contrast reading, carrier fully cleared)")
at25 = {}
for (p, xc0) in CELLS:
    for fc in (0.1, 0.3):
        rows = [shift(10 ** l, f, 2.5, p, xc0, 0.0, fc, "contrast", upper=MUTATE) for l in MBS for f in FEET]
        at25[(p, xc0, fc)] = dict(pass_=all(abs(s_) <= 0.10 for s_, _ in rows), on=[o for _, o in rows])
        P(f"    cell (p = {p:5.3f}, x_c0 = {xc0:5.3f}), f_CGM = {fc}: on at r_F " + " ".join("on" if o else "OFF" for o in
          at25[(p, xc0, fc)]["on"]) + f" -> flagship {'PASS' if at25[(p, xc0, fc)]['pass_'] else 'fail'}")
OUT["numbers"]["z25"] = {f"{p}/{xc0}/{fc}": dict(passes=v["pass_"], on=v["on"]) for (p, xc0, fc), v in at25.items()}
ha = all(at25[(p, x, 0.3)]["pass_"] for (p, x) in CELLS if p <= 1.0) and all(not at25[(p, x, 0.3)]["pass_"]
                                                                               for (p, x) in CELLS if p >= 2.0)
hb = all(not at25[(p, x, 0.1)]["pass_"] for (p, x) in CELLS)
check("H1 (pre-declared) lower branch, contrast reading, S = 0 at z = 2.5: (a) at f_CGM = 0.3 every p <= 1 cell keeps the "
      "flagship and every p = 2 cell loses it; (b) at f_CGM = 0.1 every window cell loses it",
      f"(a) {ha}; (b) {hb}", ha and hb,
      "on the lower branch the gate needs matter at the flagship radius; the steeper the gate, the more it needs")

# ============================================================================================ V1 readings
banner("V1  (reported) ABSOLUTE vs CONTRAST: the threshold-density factor x/(1 + x) and its effect")
for (p, xc0) in [(1.0, 2.5), (2.0, 2.0)]:
    for z in (0.25, 2.5):
        x = xc0 * E2(z) ** p / (1.5 * Om_z(z))
        P(f"    cell (p = {p}, x_c0 = {xc0}), z = {z}: x = {x:.2f}; absolute/contrast threshold = {x/(1+x):.4f}")
dz = [Z1[f"absolute/{p}/{xc0}/{S}/{fc}/{f}"] - Z1[f"contrast/{p}/{xc0}/{S}/{fc}/{f}"] for (p, xc0) in CELLS for (S, fc) in SC
      for f in FEET if math.isfinite(Z1[f"absolute/{p}/{xc0}/{S}/{fc}/{f}"]) and math.isfinite(Z1[f"contrast/{p}/{xc0}/{S}/{fc}/{f}"])]
check("V1 (reported) the absolute reading shifts z_max by a small amount against the contrast reading at the flagship radius "
      "(the local matter contrast there is >> 1)", f"z_max(absolute) - z_max(contrast): min {min(dz):+.3f}, max {max(dz):+.3f}",
      True, load_bearing=False)

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail
OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
