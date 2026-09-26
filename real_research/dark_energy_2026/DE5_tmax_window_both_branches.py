#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE5 -- THE COSMIC-SHEAR BOUND ACROSS THE WHOLE VACUUM-GATE WINDOW, ON BOTH BRANCHES OF THE SWITCH: L363's T_max(k),
s^2 and r_x at every lens-epoch threshold DE2's window allows, for the upper (phantom-grown) regions DE2/DE3 used and,
separately labelled, for the lower (matter-only) regions the particle-mesh construction runs.

WHY.  A carrier passes cosmic shear at a gate cell iff its matter transfer obeys T(k) <= T_max(k; x) at every
k = 0.1-1 h/Mpc, where x = x_c,eff(0.5) is the cell's lens-epoch threshold (L364: R = T^2 + 2 r_x T s + s^2 <= 1.2).
DE2's window fixes which thresholds are available: x = x_c0 E^2(0.5)^p over the window's (p, x_c0) cells.  A carrier
that fails at one cell (e.g. the acceleration-triggered carrier at the linear cell, x = 4.36) can only be rescued by a
cell with a higher threshold, since T_max rises with x (DE2 M1).  The window's highest lens-epoch threshold follows in
closed form from DE2's committed caps: maximise x0 e_S^p subject to x0 e_K^p <= X_K, x0 e_F^p <= X_F, p >= 1/2 and
x0 >= 3/2 (dominance).  The two caps bind together at p* = ln(X_F/X_K)/ln(e_F/e_K), giving
      x_max(0.5) = X_K (e_S/e_K)^p*.
THE TWO BRANCHES (reported separately, never pooled).  L363's region builder starts from the cells whose MATTER contrast
passes the threshold plus the galaxies' own seed cells, then grows the regions with the phantom's density: its first
line is the lower (matter-only) branch -- the one L377/L380/L388 run -- and its converged mask is the upper branch
DE1/DE2/DE3 used.  The lower mask is built here with L363's own first line.

CHECKS
  C1 CONTROL: the upper-branch bound at x = 4.2 and 4.4 reproduces DE3's committed table exactly (1e-12).
  W1 x_max(0.5) from DE2's committed caps (closed form above) and the (p*, x0*) corner that attains it, inside the window.
  M1 on each branch T_max(k; x) is non-decreasing in x at every k and footing (the floor property).
  L1 THE BRANCHES DIFFER AS EXPECTED: at every threshold and footing the lower-branch regions give a smaller private
     phantom -- T_max(lower) >= T_max(upper) at every k, strictly somewhere.
  E1 (reported, the export) T_max, s^2, r_x per k, footing, threshold and branch, including x_max; and the largest
     T_max(k = 1) the window offers on each branch (what any carrier must stay below at k = 1).
MUTATE=1 builds the "lower" regions with L363's full growth (i.e. the upper branch): L1 must FAIL (rc = 1).

SCOPE.  L364's bound: one lens epoch (z = 0.5), P(k) not a projected xi_+-, r_x measured against the full matter field;
the regions are built on GP3's full-matter mock (the carrier's decay enters only through the scored transfer, L364's
approximation).  DE2's window is the upper branch's (KiDS was fitted with upper-branch edges); a lower-branch window
needs its own KiDS fit, not done here.

Run from the repository root:  python3 real_research/dark_energy_2026/DE5_tmax_window_both_branches.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from multiprocessing import get_context
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE5_tmax_window_both_branches"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE5", "mutate": MUTATE, "checks": {}, "numbers": {}}
G03 = os.path.join(REPO, "real_research", "g03_audit_2026")
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
if MUTATE: P("\n  *** MUTATE=1: the 'lower' regions are grown like the upper ones; L1 must FAIL ***")

# ---------------------------------------------------------------------------------- L363's machinery, loaded unedited
P63 = os.path.join(G03, "L363_region_kernel_lensing_power.py")
N63 = {"__name__": "l363", "__file__": P63}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P63).read().split("# ============================================================================================ C1 control")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), N63)
eS = N63["E2"]; Omz, RHO = N63["Omz"], N63["RHO"]
OM47 = 0.3138
E2g = lambda z: OM47 * (1 + z) ** 3 + 1 - OM47
eK, eF = E2g(0.25), E2g(2.5)
DE2 = json.load(open(os.path.join(HERE, "DE2_vacuum_gate_joint_window_results.json")))["numbers"]
DE3 = json.load(open(os.path.join(HERE, "DE3_tmax_at_linear_gate_results.json")))["numbers"]
XK = min(DE2["KiDS"]["X_K_exact"].values()); XF = min(v for k_, v in DE2["XF"].items() if float(k_.split("/")[1]) <= 11.0)
XS_floor = {vk: max(v for k_, v in DE2["XS"].items() if int(k_.split("/")[0]) == vk)
            for vk in sorted({int(k_.split("/")[0]) for k_ in DE2["XS"]})}           # both footings: the binding floor
P(f"  L363 loaded (mock E^2(0.5) = {eS:.6f}); DE2's caps: X_K = {XK:.4f} (z = 0.25), X_F = {XF:.2f} (z = 2.5)")

# ============================================================================================ W1 the window's top threshold
banner("W1  THE WINDOW'S HIGHEST LENS-EPOCH THRESHOLD (closed form from DE2's committed caps)")
pstar = math.log(XF / XK) / math.log(eF / eK)
x0star = XK / eK ** pstar
xmax = XK * (eS / eK) ** pstar
# brute-force confirmation on a fine grid with DE2's own constraints
best = (0.0, None)
for p in np.arange(0.5, 3.0001, 0.001):
    x0 = min(XK / eK ** p, XF / eF ** p)
    if x0 >= 1.5 and x0 * eS ** p > best[0]:
        best = (x0 * eS ** p, (float(p), float(x0)))
P(f"    p* = {pstar:.4f}, x0* = {x0star:.4f}: x_max(0.5) = {xmax:.4f}; brute force {best[0]:.4f} at (p, x0) = "
  f"({best[1][0]:.3f}, {best[1][1]:.4f})")
OUT["numbers"]["window_top"] = dict(pstar=pstar, x0star=x0star, xmax=xmax, brute=best[0])
check("W1 the window's highest lens-epoch threshold x_max(0.5) from DE2's caps: closed form = brute force (1e-3), attained "
      "inside the window (x0* >= 1.5, p* >= 0.5)", f"x_max = {xmax:.4f} at p* = {pstar:.3f}, x0* = {x0star:.3f}",
      abs(best[0] / xmax - 1) < 1e-3 and x0star >= 1.5 and pstar >= 0.5)

# ---------------------------------------------------------------------------------- the bound on both branches
MK = N63["build_mock"](100.0, 256, 20260926)                          # L364's mock and seed
P(f"  GP3 mock built (100 Mpc, 256^3, seed 20260926)   [{time.time() - T0:.0f}s]")


def lower_mask(xc):
    """L363 build_regions' own first line: cells whose matter contrast passes the threshold, plus the seed cells."""
    seed = MK["rhoB"] > 0
    return (1.5 * Omz * (MK["rho_m"] / RHO - 1) >= xc) | seed


def bound_at(args):
    xc, foot, branch = args
    src = MK["rhoB"]
    if branch == "upper" or (branch == "lower" and MUTATE):
        mask, _ = N63["build_regions"](MK, src, xc, A0[foot])
    else:
        mask = lower_mask(xc)
    rp, _, _, _ = N63["region_phantom"](MK, mask, src * mask, A0[foot])
    pk = N63["spectra"](MK, {"m": MK["rho_m"] / RHO - 1, "ph": rp / RHO})
    kh, Pmm = pk("m", "m"); _, Pxx = pk("m", "ph"); _, Ppp = pk("ph", "ph")
    rx = Pxx / np.sqrt(np.maximum(Pmm * Ppp, 1e-300)); s2 = Ppp / N63["PNL_of"](kh)
    S2 = {q: float(np.interp(q, kh, s2)) for q in KG}; RX = {q: float(np.interp(q, kh, rx)) for q in KG}
    TM = {q: (-RX[q] * math.sqrt(S2[q]) + math.sqrt(max(RX[q] ** 2 * S2[q] + 1.2 - S2[q], 0.0))) for q in KG}
    return (xc, foot, branch, TM, S2, RX, float(mask.mean()))


XLIN = 2.5 * eS                                                         # the linear cell's exact threshold (DE3)
XS = sorted(set([2.5, 3.0, 3.5, 4.0, 4.2, XLIN, 4.4, 5.0, 5.5, 6.0, 6.5, xmax]))
jobs = [(x, f, b) for x in XS for f in FEET for b in ("upper", "lower")]
with get_context("fork").Pool(3) as pool:
    res = pool.map(bound_at, jobs, chunksize=1)
TAB = {(round(x, 7), f, b): dict(T_max=t, s2=s, rx=r, active=m) for x, f, b, t, s, r, m in res}
P(f"  bound computed at {len(res)} (threshold, footing, branch) points   [{time.time() - T0:.0f}s]")

# ============================================================================================ C1, M1, L1
banner("C1-L1  CONTROL, MONOTONICITY, AND THE TWO BRANCHES")
d1 = max(abs(TAB[(round(x, 7), f, "upper")]["T_max"][q] - DE3["table"][f"{x:.7f}/{f}"]["T_max"][str(q)])
         for x in (4.2, 4.4, XLIN) for f in FEET for q in KG)
check("C1 CONTROL: the upper-branch bound reproduces DE3's committed table at x = 4.2, 4.3630219, 4.4 (both footings)",
      f"max |diff| = {d1:.1e}", d1 < 1e-12)
mono = {b: all(TAB[(round(XS[i + 1], 7), f, b)]["T_max"][q] >= TAB[(round(XS[i], 7), f, b)]["T_max"][q] - 1e-9
               for i in range(len(XS) - 1) for f in FEET for q in KG) for b in ("upper", "lower")}
check("M1 on each branch T_max(k; x) is non-decreasing in the threshold at every k and footing",
      f"upper: {mono['upper']}; lower: {mono['lower']}", mono["upper"] and mono["lower"])
geq = all(TAB[(round(x, 7), f, "lower")]["T_max"][q] >= TAB[(round(x, 7), f, "upper")]["T_max"][q] - 1e-12
          for x in XS for f in FEET for q in KG)
strict = max(TAB[(round(x, 7), f, "lower")]["T_max"][q] - TAB[(round(x, 7), f, "upper")]["T_max"][q]
             for x in XS for f in FEET for q in KG)
check("L1 THE BRANCHES: the lower (matter-only) regions give a smaller private phantom than the upper (grown) regions, so "
      "T_max(lower) >= T_max(upper) at every threshold, k and footing, strictly somewhere",
      f"all >=: {geq}; largest gain in T_max {strict:+.4f}", geq and strict > 1e-4,
      "the grown regions extend each galaxy's MOND zone into its outskirts; the matter-only ones stop where the matter "
      "contrast falls below the gate")

# ============================================================================================ E1 export
banner("E1  THE EXPORT: T_max(k) per threshold, footing and branch; the window's best T_max(k = 1)")
for b in ("upper", "lower"):
    for f in FEET:
        P(f"    {b:5s} {f:9s}: T_max(k = 0.5 / 0.7 / 1.0) at x = " + "; ".join(
            f"{x:.3f}: {TAB[(round(x, 7), f, b)]['T_max'][0.5]:.3f}/{TAB[(round(x, 7), f, b)]['T_max'][0.7]:.3f}/"
            f"{TAB[(round(x, 7), f, b)]['T_max'][1.0]:.3f}" for x in XS))
    P(f"    {b:5s} active volume fraction at x = " + ", ".join(f"{x:.2f}: {TAB[(round(x, 7), 'canonical', b)]['active']:.3f}" for x in XS))
top = {b: {f: TAB[(round(xmax, 7), f, b)]["T_max"] for f in FEET} for b in ("upper", "lower")}
for b in ("upper", "lower"):
    P(f"    the window's best bound at k = 1 ({b} branch, x_max = {xmax:.3f}): canonical {top[b]['canonical'][1.0]:.4f}, "
      f"alt {top[b]['alt'][1.0]:.4f}")
OUT["numbers"]["table"] = {f"{b}/{x:.7f}/{f}": {k_: ({str(q): v_[q] for q in KG} if isinstance(v_, dict) else v_)
                                                  for k_, v_ in TAB[(round(x, 7), f, b)].items()}
                           for x in XS for f in FEET for b in ("upper", "lower")}
OUT["numbers"]["window_best_k1"] = {b: {f: top[b][f][1.0] for f in FEET} for b in ("upper", "lower")}
OUT["numbers"]["shear_floor_DE2"] = XS_floor
check("E1 (reported) the table covers DE2's shear floors to the window's top threshold on both branches", "see results JSON",
      True, load_bearing=False)

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail
OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
