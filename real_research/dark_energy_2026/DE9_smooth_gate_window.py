#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE9 -- THE SMOOTH GATE'S OWN EMPIRICAL WINDOW, AND ITS TRADE-OFF WITH WELL-POSEDNESS.

DE2 pinned the vacuum gate with a HARD step at u = x_c0 (u = x~ [Omega_L(z)/Omega_L0]^p).  An action needs a smooth gate
(DE7): f = W(t), t = (u/x_c0 - 1)/(2w) + 1/2, W = Mathlib's smoothTransition, active between u_lo = x_c0 (1 - w) and
u_hi = x_c0 (1 + w).  The lead track's gate has w = 1: it starts turning on at u = 0.  This lane asks which (p, x_c0, w)
the data allow for the smooth gate, on two readings of the switch, and sets that against DE7's finding that a narrower
transition needs a stronger repair.

THE READINGS (each its own labelled cell, the author's "all doors"):
  curvature (DE1/DE2's upper branch, V0's default): x = 4 pi G (rho_dyn - rho_bar_m)/H^2, rho_dyn = baryons + phantom;
  MOND-sector (MS1/MS2: lap(Phi - v), leak-free when varied): x = 4 pi G (rho_b + rho_ph - f_b rho_bar_m)/H^2, the
    baryonic background subtracted (MS2's door).  Isolated lenses carry no carrier here, so the two readings differ only
    by the background: x_MS = x_curv + (3/2) Omega_m(z) (1 - f_b).
THE CONSTRAINTS:
  KiDS, z = 0.25 (a CAP) and the flagship, z = 2.5, 1e11 Msun (a CAP): recomputed here with the smooth gate itself
    (DE8's operator, loaded unedited, with the MOND-sector reading added; sigma = 1, 1/m = 0.1 Mpc; switch only, as
    DE2's KiDS cap was);
  the forest, z = 2-3 (a FLOOR): DE2's dominance, x_c0 >= 1.5 at p >= 0.5, applied at the transition's LOWER end
    u_lo = x_c0 (1 - w) (sufficient if the forest deviation is monotone in the gate's activity, as across hard
    thresholds, L358 F1).  The MOND-sector reading is less active in the web (1/f_b = 6.4x the overdensity, MS2), so
    the same floor is sufficient for it a fortiori.
  cosmic shear is NOT used: DE2's floor is mock-based and not established (DE5b, MS3); on the halo model the region
    kernel needs a region cap (MS3), which a gate threshold alone does not supply.

CHECKS
  C1 CONTROL: the curvature reading's smooth KiDS scan at w = 0.02 with Dirichlet screening (1/m = 1 kpc, sigma = 0)
     reproduces DE2's hard cap 3.867 to 3%.
  C2 CONTROL: the same for the flagship: DE2's hard caps X_F (364.5 canonical, 482.5 alt, 1e11) to 3%.
  K1 [load-bearing] each reading's smooth KiDS cap lies between the hard caps of its transition's two ends:
     X_K,r/(1 + w) <= cap(w) <= X_K,r/(1 - w) (3% grid tolerance), X_K,r the reading's near-hard cap (w = 0.02).
  F1 [load-bearing] the same for the flagship cap at z = 2.5, both footings.
  E1 [reported] where each smooth cap sits between u_lo and u_hi, and the widest w for which an x_c0 range survives
     [1.5/(1 - w), min(KiDS cap/E(0.25)^2p, flagship cap/E(2.5)^2p)] per reading and p.
  T1 [reported] the trade-off with DE7's well-posedness reach z_wp(w) (committed results).
  W1 [load-bearing] the transition width matters: on both readings the smooth KiDS cap at w = 0.75 is at least 10%
     below the one at w = 0.1, and so is the flagship cap (canonical).
MUTATE=1 replaces the smooth gate by the hard gate at its midpoint u = x_c0 (no width): W1 must FAIL, rc = 1.
[History: the first MUTATE put the hard gate at u_lo; that sits exactly on K1's bracket edge, so K1 could not fail and
the control passed (6/6, rc = 0).  W1 and the midpoint mutation replaced it; K1 and F1 are kept as consistency checks.]

SCOPE.  Isolated lenses, spherical; the edge-layer term f' P included; the upper-branch reading reads the ungated
phantom (on-branch convention).  Cosmic shear and the carrier are not in this window (see above); the forest is
bracketed, not recomputed.

Run from the repository root:  python3 real_research/dark_energy_2026/DE9_smooth_gate_window.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE9_smooth_gate_window"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE9", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the direct scans use the hard gate at the midpoint u = x_c0; W1 must FAIL ***")

# ---------------------------------------------------------------------------------- DE8's machinery, loaded unedited
P8 = os.path.join(HERE, "DE8_kids_sigma_axis_both_branches.py")
D8 = {"__name__": "de8", "__file__": P8}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P8).read().split("# ============================================================================================ C1 C2 C3 controls")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D8)
solve_region, fit_cell, Wg, rr, rf, nu_vec, G, MS, A0, KPC_, Om, rho_crit0, Hz, N = [D8[k] for k in (
    "solve_region", "fit_cell", "Wg", "rr", "rf", "nu_vec", "G", "MS", "A0", "KPC_", "Om", "rho_crit0", "Hz", "N")]
BASE = D8["BASE"]
D2 = json.load(open(os.path.join(HERE, "DE2_vacuum_gate_joint_window_results.json")))["numbers"]
D7 = json.load(open(os.path.join(HERE, "DE7_gate_action_term_mond_normalised_results.json")))["numbers"]
E2G = lambda z: 0.3138 * (1 + z) ** 3 + 0.6862                        # L359's gate background (DE1-DE8)
X_K = min(D2["KiDS"]["X_K_exact"].values())
X_F = {f_: D2["XF"][f"{f_}/11.0"] for f_ in ("canonical", "alt")}
XF_bind = min(X_F.values())
X_FOREST = 1.5
P(f"  DE8 machinery loaded; DE2's hard caps: X_K = {X_K:.4f}, X_F(1e11) = {X_F}; forest floor x_c0 >= {X_FOREST}   [{time.time() - T0:.0f}s]")

# ============================================================================================ the direct scans
H_L = Hz(0.25)


FB = D8["FB"]


def gate_reading(Mb, a0, z, xc_eff, w, reading="curvature"):
    """the smooth gate at redshift z on a reading (curvature: rho_dyn - rho_bar_m; mond: rho_b + rho_ph - f_b rho_bar_m;
    the point-mass lens's density is its phantom); MUTATE: the hard gate at the midpoint."""
    Mdyn = Mb * nu_vec(G * Mb / rr ** 2 / a0)
    rho = np.gradient(Mdyn, rr) / (4 * math.pi * rr ** 2)
    sub = 1.0 if reading == "curvature" else FB
    x = 4 * math.pi * G * (rho - sub * Om * rho_crit0 * (1 + z) ** 3) / Hz(z) ** 2
    if MUTATE:                                                          # the hard step at the midpoint, no width
        on = x >= xc_eff
        it = int(np.where(on)[0].max()) if on.any() else -1
        return np.where(np.arange(N) <= it, 1.0, 0.0)
    t = (x / xc_eff - 1) / (2 * w) + 0.5
    f = Wg(t)
    off = np.where(t <= 0)[0]
    if off.size: f[off[0]:] = 0.0
    return f


def flagship_shift(xc_eff, w, foot, m_inv, sigma, reading="curvature", Mb=1e11 * MS, z=2.5):
    a0 = A0[foot]
    rF = math.sqrt(G * Mb / (0.1 * a0))
    f = gate_reading(Mb, a0, z, xc_eff, w, reading)
    extra = solve_region(Mb, a0, f, m_inv, sigma)                      # r^2 (f P)'/G on interior faces
    gF = G * (Mb + float(np.interp(math.log(rF), np.log(rf), extra))) / rF ** 2
    gfull = float(nu_vec(np.array([0.1]))[0]) * 0.1 * a0
    return 2 * math.log10(max(gF, 1e-300) / gfull)


def cap_flagship(w, foot, m_inv, sigma, reading="curvature", tol=-0.05):
    lo, hi = 20.0, 5000.0
    if flagship_shift(lo, w, foot, m_inv, sigma, reading) < tol: return lo
    for _ in range(50):
        mid = math.sqrt(lo * hi)
        if flagship_shift(mid, w, foot, m_inv, sigma, reading) >= tol: lo = mid
        else: hi = mid
    return lo


# DE8's fit reads its gate through the name gate_f in its own namespace; one reading is added there (the MOND-sector
# door, labelled "mond"), every other branch falls through to DE8's own function unchanged.
_gate_f8 = D8["gate_f"]


def _gate_f_plus(branch, Mb, a0, xc_eff, w, rho_car):
    if branch != "mond":
        return _gate_f8(branch, Mb, a0, xc_eff, w, rho_car)
    Mdyn = Mb * nu_vec(G * Mb / rr ** 2 / a0)
    rho = np.gradient(Mdyn, rr) / (4 * math.pi * rr ** 2)          # MS1's reading: baryons + phantom, never the carrier
    #   (rho_car is deliberately NOT added: the MOND-sector door is carrier-blind; every DE9 KiDS cell has no carrier
    #   anyway -- cc = None, so rho_car was zero; the '+ rho_car' of the first commit changed no number)
    x = 4 * math.pi * G * (rho - FB * D8["rho_bar"]) / D8["H_L"] ** 2
    if w is None:
        on = x >= xc_eff
        it = int(np.where(on)[0].max()) if on.any() else -1
        return np.where(np.arange(N) <= it, 1.0, 0.0)
    t = (x / xc_eff - 1) / (2 * w) + 0.5
    f = Wg(t)
    off = np.where(t <= 0)[0]
    if off.size: f[off[0]:] = 0.0
    return f


D8["gate_f"] = _gate_f_plus
BR = {"curvature": "upper", "mond": "mond"}


def kids_ok(x, w, m_inv, sigma, reading="curvature"):
    br = BR[reading]
    if MUTATE:
        d = {f_: fit_cell(f_, br, x, None, m_inv, sigma, None) - BASE[f_] for f_ in ("canonical", "alt")}
    else:
        d = {f_: fit_cell(f_, br, x, w, m_inv, sigma, None) - BASE[f_] for f_ in ("canonical", "alt")}
    return all(v <= 4.0 for v in d.values()), d


def cap_kids(w, m_inv, sigma, reading="curvature", xs=np.arange(1.5, 9.01, 0.1)):
    last = None
    for x in xs:
        ok, _ = kids_ok(float(x), w, m_inv, sigma, reading)
        if ok: last = float(x)
        elif last is not None: break
    if last is None: return None
    lo, hi = last, last + 0.1
    for _ in range(8):
        mid = 0.5 * (lo + hi)
        if kids_ok(mid, w, m_inv, sigma, reading)[0]: lo = mid
        else: hi = mid
    return lo


banner("C1 C2  CONTROLS: the near-hard smooth gate reproduces DE2's hard caps")
ck = cap_kids(0.02, 1 * KPC_, 0.0)
c1 = abs(ck / X_K - 1) if ck else float("inf")
check("C1 CONTROL: KiDS cap at w = 0.02, 1/m = 1 kpc, sigma = 0 reproduces DE2's hard cap", f"{ck} vs {X_K:.3f} ({c1:.1%})",
      c1 <= 0.03)
cf = {f_: cap_flagship(0.02, f_, 1 * KPC_, 0.0) for f_ in ("canonical", "alt")}
c2 = max(abs(cf[f_] / X_F[f_] - 1) for f_ in cf)
check("C2 CONTROL: flagship cap at w = 0.02, 1/m = 1 kpc reproduces DE2's hard caps (1e11)",
      f"canonical {cf['canonical']:.1f} vs {X_F['canonical']:.1f}, alt {cf['alt']:.1f} vs {X_F['alt']:.1f} ({c2:.1%})", c2 <= 0.03)
P(f"  controls done   [{time.time() - T0:.0f}s]")

# ============================================================================================ K1 F1 the smooth caps
banner("K1 F1  EACH READING'S SMOOTH CAPS (sigma = 1, 1/m = 0.1 Mpc; V0's choices), per transition width w")
WS = [0.1, 0.25, 0.5, 0.75]
READ = ("curvature", "mond")
KH = {r: cap_kids(0.02, 100 * KPC_, 1.0, r) for r in READ}                   # each reading's near-hard reference
FH = {r: {f_: cap_flagship(0.02, f_, 100 * KPC_, 1.0, r) for f_ in ("canonical", "alt")} for r in READ}
P(f"    near-hard references (w = 0.02): KiDS {KH}; flagship {FH}   [{time.time() - T0:.0f}s]")
KC, FC = {r: {} for r in READ}, {r: {} for r in READ}
for r in READ:
    for w in WS:
        KC[r][w] = cap_kids(w, 100 * KPC_, 1.0, r)
        FC[r][w] = {f_: cap_flagship(w, f_, 100 * KPC_, 1.0, r) for f_ in ("canonical", "alt")}
        P(f"    {r:9s} w = {w:4.2f}: KiDS cap x_c,eff(0.25) = {KC[r][w]}  (bracket {KH[r] / (1 + w):.3f}-{KH[r] / (1 - w):.3f});  "
          f"flagship cap x_c,eff(2.5) = {FC[r][w]['canonical']:.1f}/{FC[r][w]['alt']:.1f}   [{time.time() - T0:.0f}s]")
OUT["numbers"]["KiDS_cap"] = {r: {str(w): v for w, v in KC[r].items()} for r in READ}
OUT["numbers"]["flagship_cap"] = {r: {str(w): v for w, v in FC[r].items()} for r in READ}
OUT["numbers"]["near_hard"] = {"KiDS": KH, "flagship": FH}
k1 = all(KC[r][w] is not None and KH[r] is not None and KH[r] / (1 + w) * 0.97 <= KC[r][w] <= KH[r] / (1 - w) * 1.03
         for r in READ for w in WS)
check("K1 each reading's smooth KiDS cap lies between the hard caps of its transition's two ends, for every w (3%)",
      {r: {w: KC[r][w] for w in WS} for r in READ}, k1,
      "KiDS responds to the smooth gate between its two hard ends, so the bracket holds for it")
f1 = all(FH[r][f_] / (1 + w) * 0.97 <= FC[r][w][f_] <= FH[r][f_] / (1 - w) * 1.03 for r in READ for w in WS for f_ in ("canonical", "alt"))
check("F1 the same for the flagship cap at z = 2.5, both footings",
      {r: {w: {f_: round(v, 1) for f_, v in FC[r][w].items()} for w in WS} for r in READ}, f1)

wk = {r: KC[r][0.75] / KC[r][0.1] for r in READ if KC[r][0.1] and KC[r][0.75]}
wf = {r: FC[r][0.75]["canonical"] / FC[r][0.1]["canonical"] for r in READ}
check("W1 the transition width matters: cap(w = 0.75)/cap(w = 0.1) <= 0.9 for KiDS and the flagship, both readings",
      f"KiDS {({r: round(v, 3) for r, v in wk.items()})}; flagship {({r: round(v, 3) for r, v in wf.items()})}",
      len(wk) == 2 and all(v <= 0.9 for v in wk.values()) and all(v <= 0.9 for v in wf.values()),
      "a broad transition is active below x_c0, so it must sit at a lower threshold to keep the same data")

# ============================================================================================ E1 effective thresholds
banner("E1  WHERE THE SMOOTH CAPS SIT, AND THE WINDOW IN (p, x_c0, w) PER READING")
EFF = {r: {} for r in READ}
for r in READ:
    for w in WS:
        ek = (KH[r] / KC[r][w]) if KC[r][w] else None                     # the hard u (in x_c0) with the same cap
        ef = FH[r]["canonical"] / FC[r][w]["canonical"]
        EFF[r][w] = {"KiDS_u_eff": ek, "flagship_u_eff": ef}
        P(f"    {r:9s} w = {w:4.2f}: the smooth KiDS cap acts like a hard gate at u = {ek:.3f} x_c0, the flagship's at "
          f"u = {ef:.3f} x_c0 (u_lo = {1 - w:.2f}, u_hi = {1 + w:.2f})")
EK, EF = E2G(0.25), E2G(2.5)
WIN = {}
for r in READ:
    for p in (0.5, 1.0, 1.5, 1.9):
        rows = {}
        for w in WS:
            if KC[r][w] is None: rows[w] = None; continue
            hi = min(KC[r][w] / EK ** p, min(FC[r][w].values()) / EF ** p)
            lo = X_FOREST / (1 - w)
            rows[w] = (round(lo, 3), round(hi, 3)) if hi >= lo else None
        WIN[f"{r}/{p}"] = rows
        P(f"    {r:9s} p = {p}: x_c0 window per w " + ", ".join(f"{w}: {v}" for w, v in rows.items()))
OUT["numbers"]["effective"] = {r: {str(w): v for w, v in EFF[r].items()} for r in READ}
OUT["numbers"]["window"] = {k: {str(w): v for w, v in rows.items()} for k, rows in WIN.items()}
check("E1 (reported) the effective thresholds and the (p, x_c0, w) window per reading (KiDS + flagship caps direct, the "
      "forest floor at u_lo; shear not used)", {k: [w for w, v in rows.items() if v] for k, rows in WIN.items()}, True,
      load_bearing=False)

# ============================================================================================ T1 the trade-off
banner("T1  THE TRADE-OFF: the widest transition the data allow vs DE7's well-posedness reach (committed)")
ZW = {w: D7["z_wp"].get(f"1.0/2.5/{w}/0.0073/canonical/1e+11") for w in (1.0, 0.5, 0.25)}
P(f"    DE7, baseline cell (p = 1, x_c0 = 2.5, 1e11, canonical, c2 = 7.3e-3): repaired window stays open to z_wp = "
  + ", ".join(f"w = {w}: {v[0]} (fails at {v[1]})" for w, v in ZW.items()))
P(f"    this lane, p = 1: widths with a surviving x_c0 range -- curvature {[w for w, v in WIN['curvature/1.0'].items() if v]}, "
  f"MOND-sector {[w for w, v in WIN['mond/1.0'].items() if v]}")
P("    DE7's N3: the Lambda-scaled repair keeps KiDS lenses within 10% only for eta <= ~3e-8 (1e11), i.e. edges to z ~ 0.5")
P("    at w = 1 and fewer at narrower w; the MOND-sector reading's own stability is the matter-sector budget (not computed).")
OUT["numbers"]["tradeoff"] = {"z_wp": ZW, "window_p1": {r: [w for w, v in WIN[f"{r}/1.0"].items() if v] for r in READ}}
check("T1 (reported) the pincer in numbers", OUT["numbers"]["tradeoff"], True, load_bearing=False)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
