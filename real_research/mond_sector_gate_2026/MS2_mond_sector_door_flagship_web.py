#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
MS2 -- THE MOND-SECTOR DOOR'S OWN CELL: the flat-a0 flagship when the switch reads the baryons and their phantom only,
and how much of the unbound web the door can switch on.

WHY.  MS1: varied as an action term, a switch that reads the dark component (the matter-only reading the particle-mesh
runs use, or the leaf curvature DE1/DE2 read) hands the gate's variation to the carrier as an edge force 0.06-2300x its
own gravity; a switch that reads the MOND sector's own density, lap(Phi - v) = 4 pi G (rho_b + phantom) + const, keeps
the carrier exactly Newtonian.  The author's "all doors" decision gives every switch reading its own labelled cell.
This lane scores the MOND-sector door on the two things the switch variable decides by itself, before any
particle-mesh run: the flagship at z = 2.5 (DE4/DE6: on the matter-only reading it is CGM-conditional and the linear
cell p1_x2.5 loses it at 10% CGM), and the activation contrast of gas in the unbound web (XR4: on the matter reading
filaments with delta >~ 3.7-6.3 switch on at z <= 0.5, an order-one response nobody has computed).

THE DOOR.  x~_X = 1.5 Omega_m(z) [rho_X / rho_bar_m - f_b] >= x_c,eff(z) = x_c0 E(z)^(2p) (contrast, the baryonic
background f_b rho_bar_m that lap(Phi - v)'s leaf mean carries), or 1.5 Omega_m(z) rho_X / rho_bar_m >= x_c,eff
(absolute), with rho_X = rho_b + rho_ph: the disc, the circumgalactic gas and the on-branch phantom of the baryons --
NOT the carrier.  The matter door (DE4/DE6) reads rho_b + rho_carrier; the upper branch (DE1/DE4 MUTATE) reads
rho_b + rho_carrier + rho_ph.

THE GALAXY: DE4's, loaded unedited (L375's Hernquist baryons, the NFW-shaped CGM share f_CGM, L320's Moster halo for the
carrier's shape, the retained carrier fraction S; the flagship radius r_F where g_bar = 0.1 a0; GP5's zero-point shift
2 log10[(g_MOND or Newton + g_carrier)/(nu(0.1) 0.1 a0)]).  THE CELLS: DE6's eleven (L359's eight, DE2's two KiDS-capped
tops, the window's top-threshold corner).

CHECKS
  C1 CONTROL: with the matter door (the carrier in, the phantom out) DE4's committed F1 shifts at the linear cell are
     reproduced exactly (1e-12), 15 scenarios, both footings.
  C2 CONTROL: with the upper branch and no extra matter (point-mass baryons, S = 0, f_CGM = 0), DE1's committed z_max for
     the eight L359 cells is reproduced (0.02 in z) -- the door's phantom is DE1's.
  D1 THE DOOR IS CARRIER-BLIND: at every cell, reading, footing, CGM share and mass, the MOND-sector switch state at r_F
     and its z_max are identical for S = 0, 0.06, 0.3 and 1 (the carrier enters only the zero point, through its gravity).
  F1 THE FLAGSHIP ON THE DOOR at the linear cell (p = 1, x_c0 = 2.5), z = 2.5, M_b = 1e10 / 1e10.5 / 1e11, both
     footings, contrast reading: the switch is on at r_F for EVERY CGM share including none (f_CGM = 0, 0.1, 0.3, 1),
     so the zero point stays within 0.10 dex once the carrier is cleared (S = 0) -- the matter door needs f_CGM >= 0.3
     at this cell (DE4/DE6, reproduced in C1).
  Z1 (reported) z_max per cell, reading and CGM share on the door, beside DE6's matter door and DE1's upper branch.
  W1 THE UNBOUND WEB: where no region is on there is no phantom and the gas traces the matter, so the door's contrast is
     f_b times the matter door's: the gas switches on only at delta >= x / (1.5 Omega_m f_b) -- 1/f_b = 6.37 times the
     matter door's contrast at every cell and redshift.  Reported at z = 0, 0.25, 0.5 (XR4's filaments) and z = 2, 3 (the
     forest's IGM), with XR4's committed filament activation range mapped onto the door.
MUTATE=1 makes the door read the carrier as well (rho_X += the retained carrier): D1 must FAIL (the switch then depends on
S), rc = 1.

SCOPE.  Spherical, isolated galaxies at the flagship radius, the record's LambdaCDM-shaped CGM and carrier profiles; the
switch evaluated at r_F with the on-branch (DE1) phantom.  Where a region can be SEEDED (MS1/MS3: condensed baryons) is
not modelled here; the web statement is exact for gas tracing matter with no phantom.  KiDS, cosmic shear and the
particle-mesh gates on this door need their own runs (MS3 scores cosmic shear resolution-free).

Run from the repository root:  python3 real_research/mond_sector_gate_2026/MS2_mond_sector_door_flagship_web.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "MS2_mond_sector_door_flagship_web"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "MS2", "mutate": MUTATE, "checks": {}, "numbers": {}}
DEDIR = os.path.join(REPO, "real_research", "dark_energy_2026")


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the door reads the retained carrier as well; D1 must FAIL ***")

# ---------------------------------------------------------------------------------- DE4's machinery, loaded unedited
P4 = os.path.join(DEDIR, "DE4_flagship_matter_only_switch.py")
D4 = {"__name__": "de4", "__file__": P4}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P4).read().split("# ============================================================================================ C1-C3 controls")[0]
         .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D4)
halo, rho_matter, rho_phantom_on, nu, g_nfw = D4["halo"], D4["rho_matter"], D4["rho_phantom_on"], D4["nu"], D4["g_nfw"]
A0, G, MSUN, KPC, MSUN_PC3, FB = D4["A0"], D4["G"], D4["MSUN"], D4["KPC"], D4["MSUN_PC3"], D4["FB"]
E2, Om_z, rho_bar_m = D4["E2"], D4["Om_z"], D4["rho_bar_m"]
DE4R = json.load(open(os.path.join(DEDIR, "DE4_flagship_matter_only_switch_results.json")))["numbers"]
DE1R = json.load(open(os.path.join(DEDIR, "DE1_vacuum_gate_flagship_results.json")))["numbers"]
D2 = json.load(open(os.path.join(DEDIR, "DE2_vacuum_gate_joint_window_results.json")))["numbers"]
DE6R = json.load(open(os.path.join(DEDIR, "DE6_flagship_window_matter_only_results.json")))["numbers"]
P(f"  DE4 machinery loaded; f_b = {FB:.4f}; DE6's committed z_max table loaded   [{time.time() - T0:.1f}s]")

MBS = (10.0, 10.5, 11.0); FEET = ("canonical", "alt")
L359_CELLS = [(0.5, 1.5), (0.5, 2.0), (0.5, 2.5), (1.0, 1.5), (1.0, 2.0), (1.0, 2.5), (2.0, 1.5), (2.0, 2.0)]
XK = min(D2["KiDS"]["X_K_exact"].values()); XF = min(v for k_, v in D2["XF"].items() if float(k_.split("/")[1]) <= 11.0)
_ps = math.log(XF / XK) / math.log(E2(2.5) / E2(0.25)); TOP = (round(_ps, 4), round(XK / E2(0.25) ** _ps, 4))
CELLS = L359_CELLS + [(0.5, 3.39), (1.0, 2.975), TOP]
SS = (0.0, 0.06, 0.3, 1.0); FC = (0.0, 0.1, 0.3, 1.0)


def threshold(z, p, xc0, reading, door):
    """density the switch variable must reach: matter/upper doors subtract rho_bar_m (DE6); the MOND-sector door
    subtracts the baryonic background f_b rho_bar_m (lap(Phi - v)'s leaf mean); absolute readings subtract nothing."""
    x = xc0 * E2(z) ** p / (1.5 * Om_z(z))
    if reading == "absolute":
        return rho_bar_m(z) * x
    return rho_bar_m(z) * ((FB if door == "mond" else 1.0) + x)


def rho_switch(Mb, foot, z, S, fcgm, door, rF, H):
    rm, disc, cgm, car = rho_matter(Mb, z, rF, S, fcgm, H)
    ph = rho_phantom_on(Mb, A0[foot], rF)
    if door == "matter":
        return rm
    if door == "upper":
        return rm + ph
    # the MOND-sector door: baryons (disc + CGM) and their phantom; the carrier only under MUTATE
    return disc + cgm + ph + (car if MUTATE else 0.0)


def switch_on(Mb, foot, z, p, xc0, S, fcgm, reading, door, bare=False):
    H = halo(Mb, z)
    rF = math.sqrt(G * Mb * MSUN / (0.1 * A0[foot]))
    if bare:                                                             # DE1's point-mass baryons, nothing else
        rho = rho_phantom_on(Mb, A0[foot], rF)
    else:
        rho = rho_switch(Mb, foot, z, S, fcgm, door, rF, H)
    return rho >= threshold(z, p, xc0, reading, door), rF, H


def shift(Mb, foot, z, p, xc0, S, fcgm, reading, door, bare=False):
    on, rF, H = switch_on(Mb, foot, z, p, xc0, S, fcgm, reading, door, bare)
    a0 = A0[foot]; g_fw = float(nu(0.1)) * 0.1 * a0
    g = (g_fw if on else 0.1 * a0) + S * g_nfw(H["Mh"], z, rF)
    return 2 * math.log10(g / g_fw), on


def z_max(foot, p, xc0, S, fcgm, reading, door, bare=False):
    ok = lambda z: all(switch_on(10 ** l, foot, z, p, xc0, S, fcgm, reading, door, bare)[0] for l in MBS)
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
banner("C1-C2  CONTROLS: DE4's committed shifts on the matter door; DE1's committed z_max on the upper branch")
d1 = 0.0
for fc in (0.1, 0.3, 1.0):
    for S in (0.0, 0.06, 0.1, 0.3, 1.0):
        rows = DE4R["F1"][f"{fc}/{S}"]["rows"]
        mine = [shift(10 ** l, f, 2.5, 1.0, 2.5, S, fc, "contrast", "matter")[0] for l in MBS for f in FEET]
        d1 = max(d1, max(abs(a - b["shift"]) for a, b in zip(mine, rows)))
check("C1 CONTROL: the matter door reproduces DE4's committed F1 shifts exactly at the linear cell (15 scenarios, both "
      "footings)", f"max |diff| = {d1:.1e} dex", d1 < 1e-12, load_bearing=False)
d2 = 0.0
for (p, xc0) in L359_CELLS:
    for f in FEET:
        zm = z_max(f, p, xc0, 0.0, 0.0, "contrast", "upper", bare=True)
        d2 = max(d2, abs(zm - DE1R["F2"][f"{p}/{xc0}/{f}"]))
check("C2 CONTROL: with the upper-branch density and point-mass baryons only, DE1's committed z_max is reproduced for all "
      "eight L359 cells, both footings (0.02) -- the door's phantom is DE1's", f"max |dz| = {d2:.3f}", d2 < 0.02,
      load_bearing=False)
# a third control: DE6's committed matter-door z_max table, recomputed here
SC6 = [(0.0, 0.1), (0.0, 0.3), (0.0, 1.0), (0.06, 0.1), (0.06, 0.3), (0.06, 1.0)]
d3, n3 = 0.0, 0
for k_, v_ in DE6R["z_max"].items():
    reading, p, xc0, S, fc, f = k_.split("/")
    zm = z_max(f, float(p), float(xc0), float(S), float(fc), reading, "matter")
    fin = lambda q: q if math.isfinite(q) else 99.0
    d3 = max(d3, abs(fin(zm) - fin(v_))); n3 += 1
check("C3 CONTROL: DE6's committed matter-door z_max table is reproduced (every cell, scenario, reading, footing)",
      f"{n3} entries, max |dz| = {d3:.1e}", d3 < 1e-9, load_bearing=False)

# ============================================================================================ D1 the door is carrier-blind
banner("D1  THE DOOR IS CARRIER-BLIND: its switch state at r_F does not depend on the retained carrier S")
viol, tested = 0, 0
for reading in ("contrast", "absolute"):
    for (p, xc0) in CELLS:
        for fc in FC:
            for f in FEET:
                for l in MBS:
                    for z in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
                        st = [switch_on(10 ** l, f, z, p, xc0, S, fc, reading, "mond")[0] for S in SS]
                        tested += 1
                        viol += int(len(set(st)) > 1)
ZX = {}
for reading in ("contrast", "absolute"):
    for (p, xc0) in CELLS:
        for S in SS:
            for fc in FC:
                for f in FEET:
                    ZX[f"{reading}/{p}/{xc0}/{S}/{fc}/{f}"] = z_max(f, p, xc0, S, fc, reading, "mond")
zdiff = max(abs((ZX[f"{r}/{p}/{x}/{S}/{fc}/{f}"] if math.isfinite(ZX[f"{r}/{p}/{x}/{S}/{fc}/{f}"]) else 99.0)
                - (ZX[f"{r}/{p}/{x}/0.0/{fc}/{f}"] if math.isfinite(ZX[f"{r}/{p}/{x}/0.0/{fc}/{f}"]) else 99.0))
            for r in ("contrast", "absolute") for (p, x) in CELLS for S in SS for fc in FC for f in FEET)
OUT["numbers"]["z_max_door"] = ZX
check("D1 THE DOOR IS CARRIER-BLIND: at every cell, reading, footing, CGM share, mass and z = 0.5-4 the MOND-sector "
      "switch state at r_F, and its z_max, are the same for S = 0, 0.06, 0.3 and 1",
      f"{viol} state changes with S in {tested} (cell, reading, footing, f_CGM, mass, z) cases; max |z_max(S) - z_max(0)| "
      f"= {zdiff:.3g}", viol == 0 and zdiff < 1e-12,
      "the carrier enters the flagship only through its gravity (the zero point), never through the switch")

# ============================================================================================ F1 the flagship on the door
banner("F1  THE FLAGSHIP ON THE MOND-SECTOR DOOR: linear cell (p = 1, x_c0 = 2.5), z = 2.5, carrier cleared (S = 0)")
F1 = {}
for fc in FC:
    rows = []
    for l in MBS:
        for f in FEET:
            sh_c, on_c = shift(10 ** l, f, 2.5, 1.0, 2.5, 0.0, fc, "contrast", "mond")
            sh_m, on_m = shift(10 ** l, f, 2.5, 1.0, 2.5, 0.0, fc, "contrast", "matter")
            rows.append(dict(lMb=l, foot=f, door_on=on_c, door_shift=sh_c, matter_on=on_m, matter_shift=sh_m))
    F1[str(fc)] = rows
    P(f"    f_CGM = {fc:3.1f}: door on at r_F " + " ".join("on" if r["door_on"] else "OFF" for r in rows)
      + f" -> max |shift| {max(abs(r['door_shift']) for r in rows):.3f} dex;   matter door "
      + " ".join("on" if r["matter_on"] else "OFF" for r in rows)
      + f" -> max |shift| {max(abs(r['matter_shift']) for r in rows):.3f} dex")
# the retained carrier's gravity alone sets the zero point on the door: the largest S that still passes (M_b 1e10-1e11)
Smax = {}
for fc in FC:
    lo, hi = 0.0, 1.0
    passes = lambda S: all(abs(shift(10 ** l, f, 2.5, 1.0, 2.5, S, fc, "contrast", "mond")[0]) <= 0.10 for l in MBS for f in FEET)
    if passes(1.0):
        Smax[str(fc)] = 1.0
    else:
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if passes(mid) else (lo, mid)
        Smax[str(fc)] = lo
P("    the largest retained carrier fraction at r_F that keeps |shift| <= 0.10 dex on the door, by f_CGM: "
  + ", ".join(f"{k_}: {v_:.3f}" for k_, v_ in Smax.items()))
OUT["numbers"]["F1"] = F1; OUT["numbers"]["F1_Smax"] = Smax
ok_f1 = all(all(r["door_on"] and abs(r["door_shift"]) <= 0.10 for r in rows) for rows in F1.values())
mat_fail = [fc for fc, rows in F1.items() if not all(r["matter_on"] for r in rows)]
check("F1 THE FLAGSHIP ON THE DOOR: at the linear cell, z = 2.5, with the carrier cleared, the MOND-sector switch is on at "
      "r_F for M_b = 1e10-1e11 on both footings for EVERY CGM share including none, so the zero point stays within 0.10 dex",
      f"door: all on and |shift| <= 0.10 for f_CGM in {list(F1)}: {ok_f1}; the matter door loses r_F at f_CGM = {mat_fail}",
      ok_f1, "the phantom holds the region open once the carrier has gone: the flagship needs only the clearing, not the "
      "circumgalactic gas the matter door leans on")

# ============================================================================================ Z1 the table
banner("Z1  z_max PER CELL ON THE DOOR (carrier cleared), beside the matter door (DE6) and the upper branch")
Z1 = {}
for (p, xc0) in CELLS:
    for reading in ("contrast", "absolute"):
        for fc in FC:
            for f in FEET:
                Z1[f"{reading}/{p}/{xc0}/{fc}/{f}"] = dict(
                    door=ZX[f"{reading}/{p}/{xc0}/0.0/{fc}/{f}"],
                    matter=z_max(f, p, xc0, 0.0, fc, reading, "matter"),
                    upper=z_max(f, p, xc0, 0.0, fc, reading, "upper"))
    P(f"    cell (p = {p:5.3f}, x_c0 = {xc0:5.3f}) contrast, canonical/alt, f_CGM = 0 / 0.1 / 0.3: door "
      + " / ".join(f"{Z1[f'contrast/{p}/{xc0}/{fc}/canonical']['door']:.2f}|{Z1[f'contrast/{p}/{xc0}/{fc}/alt']['door']:.2f}" for fc in (0.0, 0.1, 0.3))
      + "; matter " + " / ".join(f"{Z1[f'contrast/{p}/{xc0}/{fc}/canonical']['matter']:.2f}|{Z1[f'contrast/{p}/{xc0}/{fc}/alt']['matter']:.2f}" for fc in (0.0, 0.1, 0.3)))
OUT["numbers"]["Z1"] = Z1
cells_25 = [c for c in CELLS if all(Z1[f"contrast/{c[0]}/{c[1]}/0.0/{f}"]["door"] >= 2.5 for f in FEET)]
check("Z1 (reported) the cells whose door keeps the flagship radius on to z >= 2.5 with no CGM at all (both footings)",
      f"{cells_25}", True, load_bearing=False)

# ============================================================================================ W1 the unbound web
banner("W1  THE UNBOUND WEB: activation contrast of gas tracing matter, no phantom (door vs matter door)")
W1 = {}
for (p, xc0) in CELLS:
    for z in (0.0, 0.25, 0.5, 2.0, 3.0):
        x = xc0 * E2(z) ** p / (1.5 * Om_z(z))
        W1[f"{p}/{xc0}/{z}"] = dict(matter=x, door=x / FB)
lin = {z: W1[f"1.0/2.5/{z}"] for z in (0.0, 0.25, 0.5, 2.0, 3.0)}
P("    linear cell (p = 1, x_c0 = 2.5), delta needed to switch on, matter door -> MOND-sector door: "
  + "; ".join(f"z = {z}: {v_['matter']:.1f} -> {v_['door']:.1f}" for z, v_ in lin.items()))
# XR4's committed filament activation range (the DE2 gate at z = 0-0.5, density-only x~): delta >= 3.7-6.3
xr4 = json.load(open(os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26", "XR4_filament_gate_arithmetic_results.json")))
xr4d = xr4["numbers"]["delta_th"]
for cellk, vals in xr4d.items():
    P(f"    XR4's committed activation contrasts ({cellk}, its five epochs): " + ", ".join(f"{v_:.2f}" for v_ in vals)
      + "  ->  on the door: " + ", ".join(f"{v_ / FB:.1f}" for v_ in vals))
OUT["numbers"]["W1_XR4_mapped"] = {k_: [v_ / FB for v_ in vals] for k_, vals in xr4d.items()}
ratio = [v_["door"] / v_["matter"] for v_ in W1.values()]
OUT["numbers"]["W1"] = W1
check("W1 THE UNBOUND WEB: with no phantom and gas tracing matter, the door's activation contrast is exactly 1/f_b = "
      f"{1 / FB:.2f} times the matter door's at every cell and redshift -- XR4's delta >~ 3.7-6.3 filaments at z <= 0.5 "
      f"need delta >~ {3.7 / FB:.0f}-{6.3 / FB:.0f} on the door",
      f"ratio min {min(ratio):.4f}, max {max(ratio):.4f}; linear cell z = 0 / 0.5 / 3: delta >= {lin[0.0]['door']:.1f} / "
      f"{lin[0.5]['door']:.1f} / {lin[3.0]['door']:.1f}", abs(min(ratio) * FB - 1) < 1e-12 and abs(max(ratio) * FB - 1) < 1e-12,
      "only condensed baryons (discs, group gas) can seed a region; the phantom then grows it (MS3); ordinary filament "
      "gas and the forest's IGM stay Newtonian unless a seeded region reaches them")

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  The MOND-sector door (the switch reads lap(Phi - v): baryons and their phantom, never the carrier) is carrier-blind by
  construction (D1), so the flagship's switch no longer leans on circumgalactic gas: at the linear cell it is on at the
  flagship radius at z = 2.5 for every CGM share including none (F1), where the matter door needs >~ 30% of L375's maximal
  CGM (DE4/DE6).  The zero point then depends only on how completely the carrier has left r_F (largest passing S at r_F
  by f_CGM: {', '.join(f'{k_}: {v_:.3f}' for k_, v_ in Smax.items())}).  In the unbound web the door needs 1/f_b = {1 / FB:.2f}
  times the matter door's contrast to switch on (W1), so XR4's active-filament population and the forest's IGM stay
  Newtonian unless a region seeded by condensed baryons grows into them.  Not scored here: KiDS and the particle-mesh
  gates on this door; cosmic shear is MS3's (resolution-free: it needs the regions capped near 1.75 Mpc at z = 0.5).""")

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail; OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
