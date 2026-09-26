#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE2 -- THE JOINT WINDOW FOR THE VACUUM GATE: how steeply must dark energy's share switch MOND off into the past?

WHY.  In the assembled construction the vacuum's share of the expansion gates where the MOND response acts (L359):
MOND is on in a bound region where u = x~ [Omega_Lambda(z)/Omega_Lambda,0]^p >= x_c0, i.e. above the threshold
x_c,eff(z) = x_c0 E(z)^(2p) (and Omega_Lambda = 3 Lambda/K^2 is a local scalar of the khronon's foliation).  The exponent
p says how dark energy does this job, and it is chosen, not derived.  DE1 found the framework's own flagship caps it
(p_max ~ 1.97 at x_c0 = 2, canonical, z = 2.5), and that the cell the best-standing construction uses for cosmic shear
(p = 2, x_c0 = 2; L364/L367/L380) sits on the cap and fails it at M_b = 1e11 (canonical).  L367 scored cosmic shear at
two cells only (p = 1, x_c0 = 1.5 fails; p = 2, x_c0 = 2 passes).  But each gate reads the gate at ONE epoch:
   KiDS-1000 (lenses at z = 0.25):  x_c,eff(0.25) in S_K, the thresholds L352's compensated-profile fit (+ bias-like 2-halo)
                                    accepts at Delta chi^2 <= +4 against the unswitched model, both footings (L359 K1);
   cosmic shear (lens peak z = 0.5): x_c,eff(0.5) >= X_S(v_k): the region phantom is built on GP3's z = 0.5 mock at that
                                    threshold (L363/L364), and the carrier's nonlinear matter transfer T(k) (L367, committed,
                                    v_k = 600/650/700 km/s) must satisfy T <= T_max = -r_x s + sqrt(r_x^2 s^2 + 1.2 - s^2)
                                    on k = 0.1-1 h/Mpc, both footings (GP3's R <= 1.2);
   the flagship (z = 2.5):          x_c,eff(2.5) <= X_F, the largest threshold whose edge still encloses r(g_bar = 0.1 a0)
                                    for M_b = 1e10-1e11, both footings (DE1's numeric edge, L352's machinery);
   the forest (z = 2-3) and growth: certified by DOMINANCE over L359's weakest committed passing cell (p = 0.5,
                                    x_c0 = 1.5): a gate with p >= 0.5 and x_c0 >= 1.5 is at least as high at every z >= 0, so
                                    MOND is on in no more of the web; L358's table shows the forest deviation falls
                                    monotonically with the threshold, and growth likewise.
For the power-law gate the window follows in closed form: with e(z) = E(z)^2, a gate (p, x_c0) threads KiDS, shear and
the flagship iff  X_S/e(0.5)^p <= x_c0 <= min(X_K/e(0.25)^p, X_F/e(2.5)^p),  i.e. for an interval KiDS cap,
      ln(X_S/X_K)/ln(e(0.5)/e(0.25))  <=  p  <=  ln(X_F/X_S)/ln(e(2.5)/e(0.5))            (Lean: DE_vacuum_gate).
The time dependence is what opens it: with p = 0 the same threshold must sit below X_K and above X_S at once.

PRE-DECLARED HYPOTHESIS (written before any new computation, by interpolating L367's two committed margins linearly in
ln x): X_S ~ 4.0 at v_k = 600 km/s and ~ 3.4 at 650; a joint window exists at both kicks and contains the LINEAR gate
p = 1 (u = x~ Omega_Lambda/Omega_Lambda,0) with x_c0 ~ 2.3-2.7; L359's cell (p = 1, x_c0 = 2.5) is inside it.

CHECKS
  C1 CONTROL: L363's region kernel on GP3's mock reproduces L364's committed T_max at its two cells, both footings (1e-9).
  C2 CONTROL: L352's KiDS fit reproduces L359's committed Delta chi^2 at its eleven thresholds (0.05).
  C3 CONTROL: DE1's numeric edge reproduces DE1's committed p_max (x_c0 = 2, both footings) (1e-3).
  M1 the cosmic-shear margin max_k [T(k) - T_max(k; x)] falls monotonically with the threshold x on the scanned grid, at
     each kick and footing (so cosmic shear is a floor on x_c,eff(0.5)).
  S1 (reported) X_S(v_k, footing), the crossing interpolated in ln x between bracketing grid points.
  K1 (reported) the KiDS pass set on x in [1.4, 7.0] (step 0.02) and its upper edge X_K, located exactly by bisection on
     the exact fit (the fit is a step function of the threshold; a first run used nearest-grid lookup and admitted
     x_c,eff(0.25) = 3.8695, where the exact fit gives +4.59 on the alt footing -- W3 caught it).
  (the forest for CONSTANT thresholds is read from the committed L358/L347 tables: worst |P1D - 1| <= 0.10 needs
   x_c >~ 5.4; gated cells are certified by dominance as above)
  F1 (reported) X_F(M_b, footing) at z = 2.5 and its minimum over the flagship masses.
  W1 THE WINDOW: at v_k = 600 and 650 km/s (the committed transfers inside L380's window) the set of (p, x_c0) passing
     KiDS, cosmic shear, the flagship and the forest on both footings is non-empty (gated cells: p >= 0.5, x_c0 >= 1.5 by
     dominance; constant cells p = 0: the committed forest table).  The window's lower edge p = 0.5 is the dominance
     certification limit, not a measured edge; its upper edge is the flagship's.
  W2 (hypothesis) the linear gate p = 1 is inside the window at both kicks.
  W3 the window's KiDS membership, re-evaluated exactly (not from the table) at its corner cells, holds.
  W4 (reported) L359's eight cells against every gate; the window at 700 km/s; kicks 625/675 by linear interpolation of
     the committed transfers in v_k (indicative only).
MUTATE=1 removes the time dependence (only p = 0 gates are allowed): the window must close (W1 fails, rc = 1).

SCOPE.  The shear gate is L367's: one lens epoch (z = 0.5), P(k) not a projected xi_+-, r_x at its full-matter value
(L364's approximation), the carrier transfer from L366/L367's Newtonian single-box PM (L380's pooled transfer is not
saved; L377 found the phantom moves S8 by +0.6%).  KiDS is the switch-only fit of L352/L359 (the carrier's retained
halo, L360/L375, was scored at p = 2 only; x_c,eff(0.25) of the window cells lies within 0.2 of that cell's 3.38).  The
construction's cluster, clearing and Harvey gates (L380/L381) depend on the gate through the phantom felt by baryons
at z <~ 2 and were run at p = 2; a new cell needs L380's particle-mesh run repeated before the full construction can be
said to pass there.

Run from the repository root:  python3 real_research/dark_energy_2026/DE2_vacuum_gate_joint_window.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy.optimize import brentq
from multiprocessing import get_context
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE2_vacuum_gate_joint_window"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE2", "mutate": MUTATE, "checks": {}, "numbers": {}}
G03 = os.path.join(REPO, "real_research", "g03_audit_2026")
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
FEET = ("canonical", "alt")
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


def quiet_exec(src, ns):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, ns)
    return ns


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: only ungated (p = 0) thresholds are allowed; the window must close ***")

# ---------------------------------------------------------------------------------- machinery, loaded unedited
P63 = os.path.join(G03, "L363_region_kernel_lensing_power.py")
N63 = quiet_exec(open(P63).read().split("# ============================================================================================ C1 control")[0]
                 .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), {"__name__": "l363", "__file__": P63})
P52 = os.path.join(G03, "L352_switch_gauss_compensation.py")
L52 = quiet_exec(open(P52).read().split("real_mode = ")[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"),
                 {"__name__": "l352", "__file__": P52})
A0 = L52["A0"]; fit_model = L52["fit_model"]
G, MS, MPCm = L52["G"], L52["MS"], L52["MPCm"]; KPCm = MPCm / 1e3
H0, Om, rho_crit0, Hz, nu_mono_vec, rr = L52["H0"], L52["Om"], L52["rho_crit0"], L52["Hz"], L52["nu_vec"], L52["rr"]
OM47 = 0.3138                                                          # L359's gate background (L347)
E2 = lambda z: OM47 * (1 + z) ** 3 + (1 - OM47)
eK, eS, eF = E2(0.25), N63["E2"], E2(2.5)                              # N63["E2"] = E(0.5)^2 of GP3's mock (L363)
P(f"  loaded L363 (mock epoch E^2 = {eS:.6f}) and L352 (KiDS fit, edge machinery)   [{time.time() - T0:.0f}s]")
L364 = json.load(open(os.path.join(G03, "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]
L367 = json.load(open(os.path.join(DS, "L367_triggered_carrier_cosmic_shear_results.json")))["numbers"]["transfer"]
TRANS = {int(k_[1:]): {float(q): v_ for q, v_ in d_["T"].items()} for k_, d_ in L367.items()}
L359 = json.load(open(os.path.join(G03, "L359_vacuum_gated_switch_results.json")))["numbers"]
DE1 = json.load(open(os.path.join(HERE, "DE1_vacuum_gate_flagship_results.json")))["numbers"]
P(f"  committed inputs: L364 T_max (2 cells x 2 footings), L367 transfers at v_k = {sorted(TRANS)}, L359 K1/F1/W1, DE1 P1")

# ---------------------------------------------------------------------------------- cosmic shear: T_max(k; x) on GP3's mock
MK = N63["build_mock"](100.0, 256, 20260926)                          # L364's mock and seed
P(f"  GP3 mock built (100 Mpc, 256^3, seed 20260926)   [{time.time() - T0:.0f}s]")


def tmax_of(args):
    xc, foot = args
    src = MK["rhoB"]
    mask, _ = N63["build_regions"](MK, src, xc, A0[foot])
    rp, _, _, _ = N63["region_phantom"](MK, mask, src * mask, A0[foot])
    pk = N63["spectra"](MK, {"m": MK["rho_m"] / N63["RHO"] - 1, "ph": rp / N63["RHO"]})
    kh, Pmm = pk("m", "m"); _, Pxx = pk("m", "ph"); _, Ppp = pk("ph", "ph")
    rx = Pxx / np.sqrt(np.maximum(Pmm * Ppp, 1e-300)); s2 = Ppp / N63["PNL_of"](kh)
    S2 = {q: float(np.interp(q, kh, s2)) for q in KG}; RX = {q: float(np.interp(q, kh, rx)) for q in KG}
    return (xc, foot, {q: (-RX[q] * math.sqrt(S2[q]) + math.sqrt(max(RX[q] ** 2 * S2[q] + 1.2 - S2[q], 0.0))) for q in KG},
            S2, RX)


XS_GRID = [2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 5.0, 5.5, 6.1, 7.0]
C1_CELLS = {"p=1, x_c0=1.5": 1.5 * eS, "p=2, x_c0=2.0": 2.0 * eS ** 2}
jobs = [(x, f) for x in XS_GRID for f in FEET] + [(x, f) for x in C1_CELLS.values() for f in FEET]
ctx = get_context("fork")
with ctx.Pool(3) as pool:
    res = pool.map(tmax_of, jobs, chunksize=1)
TM = {(round(x, 7), f): t for x, f, t, _, _ in res}
PH = {(round(x, 7), f): dict(s2=s, rx=r) for x, f, _, s, r in res}
P(f"  cosmic-shear bound T_max computed at {len(jobs)} (threshold, footing) points   [{time.time() - T0:.0f}s]")

# ============================================================================================ C1-C3 controls
banner("C1-C3  CONTROLS: L364's T_max; L359's KiDS; DE1's p_max")
dev1 = max(abs(TM[(round(x, 7), f)][q] - L364[f"{c}/{f}"][str(q)]) for c, x in C1_CELLS.items() for f in FEET for q in KG)
check("C1 CONTROL: L363's region kernel on GP3's mock reproduces L364's committed T_max at its two cells, both footings",
      f"max |diff| = {dev1:.1e}", dev1 < 1e-9)

BASE = {f: fit_model(A0[f], 0.0, "none", True)[0] for f in FEET}
dev2 = 0.0
for cell, v in L359["K1"].items():
    for f in FEET:
        d = fit_model(A0[f], round(v["x_eff"], 4), "compensated", True)[0] - BASE[f]
        dev2 = max(dev2, abs(d - v["dchi2"][f]))
check("C2 CONTROL: L352's KiDS fit reproduces L359's committed Delta chi^2 at its eleven thresholds (0.05)",
      f"max |diff| = {dev2:.2e}", dev2 < 0.05)


def r_flag(Mb, a0):
    return math.sqrt(G * Mb * MS / (0.1 * a0))


def r_edge_numeric(Mb, a0, z, xc):                                    # DE1's edge (L352's model_M2 edge, interpolated)
    M = Mb * MS * nu_mono_vec(G * Mb * MS / rr ** 2 / a0)
    rho_dyn = np.gradient(M, rr) / (4 * math.pi * rr ** 2)
    xx = 4 * math.pi * G * (rho_dyn - Om * rho_crit0 * (1 + z) ** 3) / Hz(z) ** 2
    on = xx >= xc
    if not on.any():
        return 1e-30
    it = int(np.where(on)[0].max())
    if it + 1 >= len(rr):
        return float(rr[-1])
    xa, xb = xx[it], xx[it + 1]
    t = (math.log(xa) - math.log(xc)) / (math.log(xa) - math.log(max(xb, 1e-300))) if xb > 0 else 0.0
    return float(math.exp(math.log(rr[it]) + t * (math.log(rr[it + 1]) - math.log(rr[it]))))


dev3 = 0.0
for f in FEET:
    m_ = lambda p, a0=A0[f]: math.log(r_edge_numeric(1e11, a0, 2.5, 2.0 * E2(2.5) ** p) / r_flag(1e11, a0))
    dev3 = max(dev3, abs(brentq(m_, 0.0, 6.0, xtol=1e-6) - DE1["P1"][f"2.0/{f}"]["pmax_numeric"]))
check("C3 CONTROL: DE1's numeric edge reproduces DE1's committed p_max at x_c0 = 2, both footings (1e-3)",
      f"max |diff| = {dev3:.1e}", dev3 < 1e-3)

# ============================================================================================ M1, S1 the cosmic-shear floor
banner("M1-S1  THE COSMIC-SHEAR FLOOR ON THE GATE AT z = 0.5: margin max_k [T - T_max(x)] against the threshold x")
MARG = {}
for vk, T in TRANS.items():
    for f in FEET:
        MARG[(vk, f)] = [max(T[q] - TM[(round(x, 7), f)][q] for q in KG) for x in XS_GRID]
        P(f"    v_k = {vk} {f:9s}: margin at x = " + ", ".join(f"{x:.2f}:{m:+.3f}" for x, m in zip(XS_GRID, MARG[(vk, f)])))
mono = all(all(b <= a + 1e-6 for a, b in zip(m[:-1], m[1:])) for m in MARG.values())
tmono = all(all(TM[(round(XS_GRID[i + 1], 7), f)][q] >= TM[(round(XS_GRID[i], 7), f)][q] - 1e-6 for i in range(len(XS_GRID) - 1))
            for f in FEET for q in KG)
check("M1 the cosmic-shear margin falls monotonically with the threshold (and T_max(k; x) rises with x at every k): cosmic "
      "shear is a FLOOR on x_c,eff(0.5)", f"margin monotone: {mono}; T_max monotone at every k: {tmono}", mono and tmono,
      "a higher threshold makes smaller regions, a smaller private phantom, and more room for the carrier's matter power")


def crossing(xs, ms):
    """smallest x at which the (monotone) margin is <= 0, interpolated linearly in ln x."""
    if ms[0] <= 0:
        return xs[0]
    for i in range(len(xs) - 1):
        if ms[i] > 0 >= ms[i + 1]:
            t = ms[i] / (ms[i] - ms[i + 1])
            return math.exp(math.log(xs[i]) + t * (math.log(xs[i + 1]) - math.log(xs[i])))
    return float("inf")


XS = {(vk, f): crossing(XS_GRID, MARG[(vk, f)]) for vk in TRANS for f in FEET}
XSb = {vk: max(XS[(vk, f)] for f in FEET) for vk in TRANS}
for vk in sorted(TRANS):
    P(f"    X_S(v_k = {vk}) = {XS[(vk, 'canonical')]:.3f} (canonical), {XS[(vk, 'alt')]:.3f} (alt) -> both footings: {XSb[vk]:.3f}")
OUT["numbers"]["XS"] = {f"{vk}/{f}": XS[(vk, f)] for vk in TRANS for f in FEET}
OUT["numbers"]["margin"] = {f"{vk}/{f}": dict(zip(XS_GRID, m)) for (vk, f), m in MARG.items()}
check("S1 (reported) the cosmic-shear floor X_S(v_k) on the gate at the lens epoch, both footings",
      "; ".join(f"{vk}: {XSb[vk]:.2f}" for vk in sorted(TRANS)), all(math.isfinite(v) for v in XSb.values()), load_bearing=False)

# ============================================================================================ K1 the KiDS pass set
banner("K1  THE KiDS PASS SET ON x_c,eff(0.25) (L352's compensated fit + bias-like 2-halo, Delta chi^2 <= +4, both footings)")
XK_GRID = np.round(np.arange(1.40, 7.0001, 0.02), 4)


def kids_fit(args):
    x, f = args
    return fit_model(A0[f], float(x), "compensated", True)[0] - BASE[f]


with ctx.Pool(3) as pool:
    _dk = pool.map(kids_fit, [(x, f) for f in FEET for x in XK_GRID], chunksize=4)
DK = {f: np.array(_dk[i * len(XK_GRID):(i + 1) * len(XK_GRID)]) for i, f in enumerate(FEET)}
okK = (DK["canonical"] <= 4.0) & (DK["alt"] <= 4.0)
XK = float(XK_GRID[np.where(okK)[0].max()]) if okK.any() else float("nan")
gaps = [float(x) for x, o in zip(XK_GRID, okK) if (not o) and x < XK]
P("    Delta chi^2 (canonical/alt) at x = " + ", ".join(f"{x:.2f}:{DK['canonical'][i]:+.1f}/{DK['alt'][i]:+.1f}"
                                                        for i, x in enumerate(XK_GRID) if i % 10 == 0))
P(f"    pass set: all of [{XK_GRID[0]:.2f}, {XK:.2f}] except {gaps if gaps else 'nothing'}; first failure above: "
  f"{XK_GRID[np.where(okK)[0].max() + 1] if okK.any() and np.where(okK)[0].max() + 1 < len(XK_GRID) else 'none'}; "
  f"Delta chi^2 at x = 5 / 7: {DK['canonical'][np.argmin(abs(XK_GRID - 5))]:+.0f}/{DK['alt'][np.argmin(abs(XK_GRID - 5))]:+.0f}, "
  f"{DK['canonical'][-1]:+.0f}/{DK['alt'][-1]:+.0f}")
OUT["numbers"]["KiDS"] = dict(x=XK_GRID.tolist(), dchi2={f: DK[f].tolist() for f in FEET}, X_K=XK, gaps=gaps)


# the exact KiDS cap: the fit is a step function of the threshold (edges snap to L352's radial grid), so the cap is
# located by bisection on the EXACT fit between the last passing and the first failing grid point, per footing.
# (A first run looked thresholds up at the NEAREST grid point; that admitted x_c,eff(0.25) = 3.8695, where the exact
# fit gives +4.59 on the alt footing -- W3 caught it.)
XK_exact = {}
if okK.any() and np.where(okK)[0].max() + 1 < len(XK_GRID):
    i_last = int(np.where(okK)[0].max())
    for f in FEET:
        lo_, hi_ = float(XK_GRID[i_last]), float(XK_GRID[i_last + 1])
        if fit_model(A0[f], hi_, "compensated", True)[0] - BASE[f] <= 4.0:
            XK_exact[f] = hi_
            continue
        for _ in range(14):
            mid = 0.5 * (lo_ + hi_)
            if fit_model(A0[f], round(mid, 6), "compensated", True)[0] - BASE[f] <= 4.0:
                lo_ = mid
            else:
                hi_ = mid
        XK_exact[f] = lo_
XKe = min(XK_exact.values()) if XK_exact else XK
P(f"    exact KiDS cap (bisection on the exact fit): " + ", ".join(f"{f} {v:.4f}" for f, v in XK_exact.items())
  + f" -> both footings: x_c,eff(0.25) <= {XKe:.4f}")
OUT["numbers"]["KiDS"]["X_K_exact"] = XK_exact
gaps_ok = not gaps                                                     # the scanned pass set has no holes below the cap


def kids_ok(x):
    return (XK_GRID[0] <= x <= XKe) and gaps_ok


# ============================================================================================ F1 the flagship cap
banner("F1  THE FLAGSHIP CAP ON THE GATE AT z = 2.5 (the edge encloses r(g_bar = 0.1 a0))")
XF = {}
for f in FEET:
    for lMb in (10.0, 10.5, 11.0, 11.5):
        Mb = 10 ** lMb
        g_ = lambda x, Mb=Mb, a0=A0[f]: math.log(r_edge_numeric(Mb, a0, 2.5, x) / r_flag(Mb, a0))
        XF[(f, lMb)] = brentq(g_, 1.0, 1e6, xtol=1e-6)
        P(f"    {f:9s} M_b = 1e{lMb:.1f}: X_F = {XF[(f, lMb)]:.1f}" + ("   (informational, above the flagship masses)" if lMb > 11 else ""))
XFb = min(XF[(f, l)] for f in FEET for l in (10.0, 10.5, 11.0))
OUT["numbers"]["XF"] = {f"{f}/{l}": v for (f, l), v in XF.items()}
P(f"    binding cap (both footings, M_b <= 1e11): X_F = {XFb:.1f}")

# ---------------------------------------------------------------------------------- the forest for UNGATED thresholds (committed)
L358w = json.load(open(os.path.join(G03, "L358_forest_kids_pincer_observable_results.json")))["numbers"]["worst"]
L347n = json.load(open(os.path.join(G03, "L347_switch_forest_flux_power_results.json")))["numbers"]
f7 = max(max(1 - lo, hi - 1) for k_, (lo, hi) in L347n["F2"].items() if "sw7" in k_)
FT = sorted([(float(k_), v) for k_, v in L358w.items()] + [(5.0, L347n["verdict"]["worst_dev_xc5"]), (7.0, f7)])
XF0 = next(x0_ + (0.10 - d0) * (x1_ - x0_) / (d1 - d0) for (x0_, d0), (x1_, d1) in zip(FT[:-1], FT[1:]) if d0 > 0.10 >= d1)
P(f"\n  the forest for constant thresholds (L358 + L347, committed worst |P1D - 1|): " + ", ".join(f"{x:.1f}: {d:.3f}" for x, d in FT)
  + f"  -> passes (<= 0.10) above x_c = {XF0:.2f}")
OUT["numbers"]["forest_ungated"] = dict(table=FT, X_forest_const=XF0)

# ============================================================================================ W1-W4 the window
banner("W1-W4  THE JOINT WINDOW IN (p, x_c0): KiDS (z = 0.25) + cosmic shear (z = 0.5) + flagship (z = 2.5) + dominance")
PG = np.round(np.arange(0.0, 3.0001, 0.01), 4); XG = np.round(np.arange(1.0, 8.0001, 0.005), 4)


def window(vk_floor):
    cells = []
    for p in PG:
        if MUTATE and p != 0.0:
            continue
        for x0 in XG:
            if p == 0.0:                                                       # constant threshold: the committed table
                if x0 < XF0:
                    continue
            elif not ((p >= 0.5 - 1e-9) and (x0 >= 1.5 - 1e-9)):              # gated: forest + growth by dominance
                continue
            if x0 * eS ** p < vk_floor:                                        # cosmic shear
                continue
            if x0 * eF ** p > XFb:                                             # flagship
                continue
            if not kids_ok(x0 * eK ** p):                                      # KiDS
                continue
            cells.append((float(p), float(x0)))
    return cells


WIN = {vk: window(XSb[vk]) for vk in sorted(TRANS)}
for vk, cells in WIN.items():
    if cells:
        ps = [c[0] for c in cells]; xs = [c[1] for c in cells]
        P(f"    v_k = {vk}: {len(cells)} grid cells; p in [{min(ps):.2f}, {max(ps):.2f}], x_c0 in [{min(xs):.3f}, {max(xs):.3f}]")
        for pp in (0.5, 1.0, 1.5, 2.0):
            sub = [c[1] for c in cells if abs(c[0] - pp) < 1e-9]
            P(f"        p = {pp:.1f}: x_c0 in " + (f"[{min(sub):.3f}, {max(sub):.3f}]" if sub else "(none)"))
    else:
        P(f"    v_k = {vk}: NO window")
OUT["numbers"]["window"] = {str(vk): dict(n=len(c), p=[min(q[0] for q in c), max(q[0] for q in c)] if c else None,
                                          x0=[min(q[1] for q in c), max(q[1] for q in c)] if c else None) for vk, c in WIN.items()}
okW1 = bool(WIN[600]) and bool(WIN[650])
check("W1 THE WINDOW: at v_k = 600 and 650 km/s a vacuum gate (p >= 0.5, x_c0 >= 1.5) passes KiDS-1000, cosmic shear and "
      "the flagship on both footings (forest and growth by dominance over L359's committed cells)",
      "; ".join(f"{vk}: {len(WIN[vk])} cells" for vk in (600, 650)), okW1,
      "the vacuum's growth into the past is what threads the four epochs: MUTATE (p = 0) must close it")

lin = {vk: [c for c in WIN[vk] if abs(c[0] - 1.0) < 1e-9] for vk in (600, 650)}
check("W2 (hypothesis, pre-declared) the LINEAR gate p = 1 (u = x~ Omega_Lambda/Omega_Lambda,0) is inside the window at "
      "both kicks", "; ".join(f"{vk}: x_c0 in [{min(c[1] for c in lin[vk]):.3f}, {max(c[1] for c in lin[vk]):.3f}]"
                             if lin[vk] else f"{vk}: none" for vk in (600, 650)),
      all(lin[vk] for vk in (600, 650)), load_bearing=False)

corner_ok, corners = True, []
for vk in (600, 650):
    if not WIN[vk]:
        continue
    pmin = min(c[0] for c in WIN[vk]); pmax = max(c[0] for c in WIN[vk])
    for pp in (pmin, pmax, 1.0):
        sub = [c for c in WIN[vk] if abs(c[0] - pp) < 1e-9]
        for c in (sub[0], sub[-1]) if sub else ():
            xe = c[1] * eK ** c[0]
            dd = {f: fit_model(A0[f], round(xe, 4), "compensated", True)[0] - BASE[f] for f in FEET}
            corners.append(dict(vk=vk, p=c[0], x0=c[1], x_eff_025=xe, dchi2=dd))
            corner_ok &= all(v <= 4.0 for v in dd.values())
OUT["numbers"]["corners"] = corners
check("W3 the window's KiDS membership holds when re-evaluated exactly at its corner cells (not from the 0.02 table)",
      f"{sum(all(v <= 4 for v in c['dchi2'].values()) for c in corners)}/{len(corners)} corners pass exactly",
      corner_ok and len(corners) > 0 or MUTATE)

banner("W4  (reported) THE RECORD'S CELLS AGAINST EVERY GATE; OTHER KICKS")
rows = []
for c in L359["W1"]:
    p, x0 = c["p"], c["x_c0"]
    xe = (x0 * eK ** p, x0 * eS ** p, x0 * eF ** p)
    g = dict(kids=kids_ok(xe[0]), flagship=xe[2] <= XFb, **{f"shear{vk}": xe[1] >= XSb[vk] for vk in sorted(TRANS)})
    rows.append(dict(p=p, x0=x0, x_eff=xe, gates=g))
    P(f"    L359 cell p = {p:.1f}, x_c0 = {x0:.1f}: x_c,eff(0.25/0.5/2.5) = {xe[0]:.2f}/{xe[1]:.2f}/{xe[2]:.1f} -> "
      + ", ".join(f"{k_} {'ok' if v else 'FAIL'}" for k_, v in g.items()))
OUT["numbers"]["L359_cells"] = rows
for vk in (625, 675):
    T = {q: 0.5 * (TRANS[vk - 25][q] + TRANS[vk + 25][q]) for q in KG}
    xs_ = max(crossing(XS_GRID, [max(T[q] - TM[(round(x, 7), f)][q] for q in KG) for x in XS_GRID]) for f in FEET)
    w = window(xs_)
    P(f"    v_k = {vk} (transfer interpolated between committed kicks, indicative): X_S = {xs_:.2f}; window "
      + (f"p in [{min(c[0] for c in w):.2f}, {max(c[0] for c in w):.2f}], {len(w)} cells" if w else "NONE"))
    OUT["numbers"][f"interp_{vk}"] = dict(XS=xs_, n=len(w))

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  Each gate reads the vacuum gate at one epoch.  Cosmic shear needs x_c,eff(0.5) >= {XSb[600]:.2f} (600 km/s) / {XSb[650]:.2f}
  (650); KiDS accepts x_c,eff(0.25) up to {XKe:.3f}; the flagship caps x_c,eff(2.5) at {XFb:.0f}.  The power-law gate threads
  them iff  ln(X_S/X_K)/ln(e(0.5)/e(0.25)) <= p <= ln(X_F/X_S)/ln(e(2.5)/e(0.5)).""")
if okW1:
    P(f"""  A window exists at both kicks.  At 650 km/s: p in [{min(c[0] for c in WIN[650]):.2f}, {max(c[0] for c in WIN[650]):.2f}]; the linear gate
  p = 1 needs x_c0 in [{min(c[1] for c in lin[650]):.3f}, {max(c[1] for c in lin[650]):.3f}] (600 km/s: [{min(c[1] for c in lin[600]):.3f}, {max(c[1] for c in lin[600]):.3f}]) if present.""" if lin[650] and lin[600] else
      f"  A window exists at both kicks; the linear gate is {'inside' if lin[650] else 'NOT inside'} it at 650 km/s.")
else:
    P("  No gate threads the four epochs at the window kicks: the vacuum gate, as a power law, is closed by these gates.")

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail
OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
