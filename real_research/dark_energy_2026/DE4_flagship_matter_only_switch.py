#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE4 -- THE FLAGSHIP ON THE MATTER-ONLY SWITCH: on the lower branch of the switch's bistability -- the one the particle-mesh
construction runs (L377/L380, and the same-cell re-run L388+) -- does MOND stay on at the flagship radius at z = 2.5,
and what does the carrier do there?

WHY.  DE1/DE2 priced the vacuum-gated switch on its UPPER branch: the switch variable reads the dynamical density,
baryons + phantom (L352's "most favourable" placement; L363's region growth likewise).  The particle-mesh construction
switches on MATTER ONLY -- L377's own docstring: "x~_m the matter-only switch variable (the lower branch of L342's
bistability, stated)":  1.5 Omega_m(a) (rho_m/rho_bar_m - 1) [Omega_L(a)/Omega_L0]^p > x_c0.  So a galaxy keeps MOND at
radius r on that branch only if its local MATTER density there -- baryons, circumgalactic gas and whatever carrier it
retains -- exceeds
      rho_min(z) = rho_bar_m(z) [1 + x_c,eff(z) / (1.5 Omega_m(z))],   x_c,eff(z) = x_c0 E(z)^(2p).
The carrier is supposed to have LEFT galaxies by z ~ 2.5 (GP5/L356: an intact carrier moves the flagship +0.8 dex).
If it has left, the outskirts may fall below rho_min and MOND switches off there (Gauss: Newtonian beyond the edge,
the zero point then drops to -2 log10 nu(0.1)).  The cross-thread review (XR2 T4) flagged this branch point; this lane
computes it.

THE GALAXY (the record's own conventions).  Flagship radius r_F where g_bar = 0.1 a0 for point-mass baryons M_b (GP5/DE1).
Halo from L320's machinery (Moster+13 stellar-to-halo relation at M_* = M_b/(1 + mu), mu = 0.5((1+z)/2)^2, GP5's gas
fraction; Dutton & Maccio c200), used only to shape the dark and circumgalactic components:
  * baryonic disc: Hernquist with a = 3 kpc (M_b/1e11)^0.3 (L375);
  * circumgalactic gas: f_CGM x (f_b M_200 - M_b) in the halo's NFW shape (L375's convention, f_CGM = 1 its maximal share);
  * carrier: S x (1 - f_b) M_200 in the NFW shape; S = retained fraction (1 = intact; 0.06 = L380's fixed-cell clearing
    at 600-675 km/s; 0 = fully cleared).  Its gravity at r_F is Newtonian (kernel-invisible, L353), S x g_NFW with GP5's
    convention (the full M_200 NFW), so S = 1 reproduces GP5/L356's price.
Zero-point shift at r_F: 2 log10[(g_MOND or Newton + g_carrier) / (nu(0.1) 0.1 a0)] (GP5's definition; nu = L320's nu_RAR).

CHECKS
  C1 CONTROL: GP5's flagship machinery (loaded unedited) reproduces L356's committed shifts (0.005 dex).
  C2 CONTROL: rho_min, on the gate's own background (L359's Omega_m = 0.3138; the halo machinery keeps L320's 0.3153),
     reproduces the cross-thread review's quoted value 4.36e-5 Msun/pc^3 at z = 2.5 (1%).
  C3 CONTROL: with the phantom-inclusive (upper-branch) density the switch is on at r_F for M_b <= 1e11 at the linear
     cell, as DE1/DE2 found (the on-branch deep-MOND phantom density at r_F exceeds rho_min).
  F1 THE FLAGSHIP ON THE MATTER-ONLY BRANCH at the linear cell (p = 1, x_c0 = 2.5), z = 2.5, M_b = 1e10 / 1e10.5 / 1e11,
     both footings: is there a carrier retention S in {0, 0.06, 0.1, 0.3, 1} that keeps |shift| <= 0.10 dex for all
     three masses, for each CGM share f_CGM in {0.1, 0.3, 1}?
     PRE-DECLARED HYPOTHESIS (written before the run, from the review's estimate and a hand estimate of an isothermal CGM):
     for f_CGM <= 0.3 there is NONE -- with the carrier intact the switch stays on but the carrier's own gravity moves
     the zero point beyond +0.10 dex (GP5's price), and with it cleared (S <= 0.1) MOND is off at r_F for M_b = 1e11
     (Newtonian, about -1.1 dex): the matter-only branch has a carrier pincer; a pass needs the maximal CGM (f_CGM ~ 1).
  B1 (reported) the bistable band: the cases (fully cleared or 6%-retained carrier, 10% or 30% CGM) in which the
     matter-only branch is off at r_F while the upper branch is on -- both states self-consistent there, so the galaxy's
     history decides; the matter-only edge r_m and rho_matter/rho_min at r_F are reported.
  Z1 (reported) the same at z = 2 and 3, and for the p = 2, x_c0 = 2 cell.
MUTATE=1 uses the phantom-inclusive switch density (the upper branch): with the carrier cleared the flagship must PASS
(inverted control, rc = 0), reproducing DE1/DE2's reading at the linear cell.

SCOPE.  Spherical, isolated galaxy; the CGM and carrier profiles borrow a LambdaCDM halo's shape (the record's L375
convention), not a framework-native formation history; the flagship uses point-mass baryons at r_F (GP5); the switch is
evaluated locally at r_F on a monotone density profile (on at r_F <=> the matter-only edge r_m >= r_F).

Run from the repository root:  python3 real_research/dark_energy_2026/DE4_flagship_matter_only_switch.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy.optimize import brentq
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE4_flagship_matter_only_switch"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE4", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the switch reads the phantom-inclusive density (upper branch); F1 must PASS (inverted control) ***")

# ---------------------------------------------------------------------------------- GP5's (and L320's) machinery, unedited
GP = os.path.join(REPO, "real_research", "generated_phantom_2026", "GP5_window_at_high_z.py")
NS = {"__name__": "gp5", "__file__": GP}
src = open(GP).read().split("# ============================================================================================ C1, C2")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), NS)
L20 = NS["L20"]
nu, halo_mass, g_nfw, c200, rho_crit = L20["nu"], L20["halo_mass"], L20["g_nfw"], L20["c200"], L20["rho_crit"]
A0, G, MSUN, KPC, Om, OL = L20["A0"], L20["G"], L20["MSUN"], L20["KPC"], L20["Om"], L20["OL"]
FB = 0.02237 / (0.02237 + 0.1200)                                         # L320's / L375's cosmic baryon fraction
flagship_gp5, survival = NS["flagship"], NS["survival"]
PC = KPC / 1e3
MSUN_PC3 = MSUN / PC ** 3                                                 # kg/m^3 per Msun/pc^3
OMG = 0.3138                                                              # the gate's background: L359's (L347's)
E2 = lambda z: OMG * (1 + z) ** 3 + 1 - OMG
Om_z = lambda z: OMG * (1 + z) ** 3 / E2(z)
rho_bar_m = lambda z: OMG * rho_crit(0.0) * (1 + z) ** 3                  # kg/m^3 (h = 0.6736, as L320/L359)
P(f"  GP5/L320 loaded: Om = {Om}, f_b = {FB:.4f}   [{time.time() - T0:.1f}s]")


def rho_min(z, p, xc0):
    return rho_bar_m(z) * (1 + xc0 * E2(z) ** p / (1.5 * Om_z(z)))


def halo(Mb, z):
    mu = 0.5 * ((1 + z) / 2) ** 2
    Mh = halo_mass(Mb / (1 + mu), z)
    c = c200(Mh, z); r200 = (3 * Mh * MSUN / (4 * math.pi * 200 * rho_crit(z))) ** (1 / 3); rs = r200 / c
    mfn = lambda x: math.log(1 + x) - x / (1 + x)
    rho_s = Mh * MSUN / (4 * math.pi * rs ** 3 * mfn(c))
    return dict(Mh=Mh, c=c, r200=r200, rs=rs, rho_s=rho_s, mu=mu)


def rho_nfw_shape(H, r):
    x = r / H["rs"]
    return H["rho_s"] / (x * (1 + x) ** 2) if r < H["r200"] else 0.0


def rho_matter(Mb, z, r, S, fcgm, H):
    a = 3.0 * (Mb / 1e11) ** 0.3 * KPC
    disc = Mb * MSUN * a / (2 * math.pi * r * (r + a) ** 3)                # Hernquist
    Mcgm = max(FB * H["Mh"] - Mb, 0.0) * fcgm
    cgm = rho_nfw_shape(H, r) * Mcgm / H["Mh"]
    car = rho_nfw_shape(H, r) * S * (1 - FB)
    return disc + cgm + car, disc, cgm, car


def rho_phantom_on(Mb, a0, r):
    """upper-branch (on) deep-MOND phantom density of point-mass baryons at r, from L320's nu (analytic derivative)."""
    h = 1e-6
    M = lambda rr: Mb * MSUN * nu(G * Mb * MSUN / (rr ** 2 * a0))
    dM = (M(r * (1 + h)) - M(r * (1 - h))) / (2 * r * h)
    return dM / (4 * math.pi * r ** 2)


def evaluate(Mb, foot, z, p, xc0, S, fcgm, upper=False):
    a0 = A0[foot]; H = halo(Mb, z)
    rF = math.sqrt(G * Mb * MSUN / (0.1 * a0))
    rm, disc, cgm, car = rho_matter(Mb, z, rF, S, fcgm, H)
    rho_sw = rm + (rho_phantom_on(Mb, a0, rF) if upper else 0.0)
    rmin = rho_min(z, p, xc0)
    on = rho_sw >= rmin
    g_fw = float(nu(0.1)) * 0.1 * a0
    g_c = S * g_nfw(H["Mh"], z, rF)
    g = (g_fw if on else 0.1 * a0) + g_c
    # the matter-only edge r_m (largest r with rho_matter >= rho_min), for B1
    f_edge = lambda r: math.log(max(rho_matter(Mb, z, r, S, fcgm, H)[0], 1e-300) / rmin)
    rs_ = np.geomspace(0.3 * KPC, 0.99 * H["r200"], 400)
    vals = np.array([f_edge(r) for r in rs_])
    idx = np.where(vals >= 0)[0]
    r_m = float(rs_[idx.max()]) if len(idx) else 0.0
    return dict(rF_kpc=rF / KPC, rho_min=rmin / MSUN_PC3, rho_matter=rm / MSUN_PC3, disc=disc / MSUN_PC3,
                cgm=cgm / MSUN_PC3, carrier=car / MSUN_PC3, rho_switch=rho_sw / MSUN_PC3, on=bool(on),
                shift=2 * math.log10(g / g_fw), r_m_kpc=r_m / KPC, Mh=H["Mh"], c=H["c"])


# ============================================================================================ C1-C3 controls
banner("C1-C3  CONTROLS: GP5 reproduces L356; rho_min; the upper branch is on at r_F (DE1/DE2)")
L356 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L356_construction_highz_price_results.json")))["numbers"]["H3"]
mine = flagship_gp5(0.8, 2.5, r_override=survival(2.5, 0.8))
d1 = max(abs(m[4] - r_["dzp_dex"]) for m, r_ in zip(mine, L356))
check("C1 CONTROL: GP5's flagship machinery reproduces L356's committed shifts (0.005 dex)", f"max |diff| = {d1:.1e} dex", d1 < 5e-3)
rmin25 = rho_min(2.5, 1.0, 2.5) / MSUN_PC3
check("C2 CONTROL: rho_min at the linear cell, z = 2.5, matches the cross-thread review's quoted 4.36e-5 Msun/pc^3 (1%)",
      f"rho_min(2.5) = {rmin25:.4e} Msun/pc^3", abs(rmin25 / 4.36e-5 - 1) < 0.01)
c3 = [evaluate(10 ** l, f, 2.5, 1.0, 2.5, 0.0, 0.1, upper=True) for l in (10.0, 10.5, 11.0) for f in ("canonical", "alt")]
check("C3 CONTROL: on the upper (phantom-inclusive) branch the switch is on at r_F for M_b = 1e10-1e11, both footings, at "
      "the linear cell (DE1/DE2's reading)", f"rho_switch/rho_min at r_F: " + ", ".join(f"{r['rho_switch']/r['rho_min']:.1f}" for r in c3),
      all(r["on"] for r in c3))

# ============================================================================================ F1
banner("F1  THE FLAGSHIP ON THE " + ("UPPER (MUTATE)" if MUTATE else "MATTER-ONLY") + " BRANCH: linear cell (p = 1, x_c0 = 2.5), z = 2.5")
SS = (0.0, 0.06, 0.1, 0.3, 1.0); FC = (0.1, 0.3, 1.0); MBS = (10.0, 10.5, 11.0)
F1 = {}
for fc in FC:
    for S in SS:
        rows = [evaluate(10 ** l, f, 2.5, 1.0, 2.5, S, fc, upper=MUTATE) for l in MBS for f in ("canonical", "alt")]
        worst = max(rows, key=lambda r: abs(r["shift"]))
        F1[f"{fc}/{S}"] = dict(rows=rows, worst=worst["shift"], all_on=all(r["on"] for r in rows),
                               passes=all(abs(r["shift"]) <= 0.10 for r in rows))
        P(f"    f_CGM = {fc:3.1f}, S = {S:4.2f}: switch on at r_F: "
          + " ".join(("on" if r["on"] else "OFF") for r in rows)
          + f"  | worst shift {worst['shift']:+.3f} dex -> {'PASS' if F1[f'{fc}/{S}']['passes'] else 'fail'}")
r11 = evaluate(1e11, "canonical", 2.5, 1.0, 2.5, 0.06, 0.3, upper=MUTATE)
P(f"    detail, M_b = 1e11 canonical, S = 0.06, f_CGM = 0.3: r_F = {r11['rF_kpc']:.1f} kpc; rho_min = {r11['rho_min']:.3e}; "
  f"disc {r11['disc']:.2e} + CGM {r11['cgm']:.2e} + carrier {r11['carrier']:.2e} = {r11['rho_matter']:.2e} Msun/pc^3 "
  f"(M_200 = {r11['Mh']:.2e}, c = {r11['c']:.1f})")
OUT["numbers"]["F1"] = F1
passing = {fc: [S for S in SS if F1[f"{fc}/{S}"]["passes"]] for fc in FC}
okF = all(passing[fc] for fc in FC)
check("F1 THE FLAGSHIP: on this branch, for every CGM share there is a carrier retention S that keeps the deep-MOND zero "
      "point within 0.10 dex at z = 2.5 for M_b = 1e10-1e11, both footings",
      "passing S by f_CGM: " + "; ".join(f"{fc}: {passing[fc] if passing[fc] else 'none'}" for fc in FC), okF,
      "on the matter-only branch the carrier is squeezed from both sides: kept, its gravity moves the zero point; "
      "cleared, the outskirts fall below the gate and MOND switches off")
hyp = (not passing[0.1]) and (not passing[0.3])
P(f"    pre-declared hypothesis (no retention passes for f_CGM <= 0.3; a pass needs the maximal CGM): "
  f"{'CONFIRMED' if hyp and not MUTATE else ('n/a (MUTATE)' if MUTATE else 'NOT confirmed')}"
  + (f"; maximal CGM passes at S = {passing[1.0]}" if passing[1.0] else "; the maximal CGM does not rescue it either"))
OUT["numbers"]["F1_hypothesis_confirmed"] = hyp

# ============================================================================================ B1, Z1
banner("B1-Z1  (reported) the bistable band at r_F, other redshifts and the p = 2, x_c0 = 2 cell")
B1 = []
for (S, fc) in ((0.0, 0.1), (0.0, 0.3), (0.06, 0.3)):
    for l in MBS:
        for f in ("canonical", "alt"):
            lo = evaluate(10 ** l, f, 2.5, 1.0, 2.5, S, fc, upper=False)
            up = evaluate(10 ** l, f, 2.5, 1.0, 2.5, S, fc, upper=True)
            B1.append(dict(S=S, fcgm=fc, lMb=l, foot=f, lower_on=lo["on"], upper_on=up["on"], r_m_kpc=lo["r_m_kpc"],
                           rF_kpc=lo["rF_kpc"], rho_matter_over_min=lo["rho_matter"] / lo["rho_min"]))
            P(f"    S = {S:4.2f}, f_CGM = {fc:3.1f}, M_b = 1e{l:.1f} {f:9s}: matter-only edge r_m = {lo['r_m_kpc']:6.1f} kpc vs r_F = "
              f"{lo['rF_kpc']:5.1f}; rho_matter/rho_min at r_F = {lo['rho_matter']/lo['rho_min']:.2f}; lower branch "
              f"{'on' if lo['on'] else 'OFF'}, upper {'on' if up['on'] else 'OFF'}"
              + ("  <- bistable at r_F: history decides" if (up["on"] and not lo["on"]) else ""))
OUT["numbers"]["B1"] = B1
nb = sum(1 for b in B1 if b["upper_on"] and not b["lower_on"])
check("B1 (reported) the number of (retention, CGM, mass, footing) cases in which r_F lies in the switch's bistable band "
      "(lower branch off, upper branch on) -- the cases where formation history, not the static equations, decides",
      f"{nb}/{len(B1)} cases: " + ", ".join(f"S={b['S']}/f={b['fcgm']}/1e{b['lMb']:.1f}/{b['foot'][:3]}" for b in B1
                                            if b["upper_on"] and not b["lower_on"]),
      True, load_bearing=False)
Z1 = {}
for (p, xc0) in ((1.0, 2.5), (2.0, 2.0)):
    for z in (2.0, 2.5, 3.0):
        for S in (0.06, 1.0):
            rows = [evaluate(10 ** l, f, z, p, xc0, S, 0.3, upper=MUTATE) for l in MBS for f in ("canonical", "alt")]
            Z1[f"{p}/{xc0}/{z}/{S}"] = [dict(on=r["on"], shift=r["shift"]) for r in rows]
            P(f"    cell (p = {p}, x_c0 = {xc0}), z = {z}, S = {S:4.2f}, f_CGM = 0.3: on at r_F "
              + " ".join(("on" if r["on"] else "OFF") for r in rows) + f"; worst shift {max((r['shift'] for r in rows), key=abs):+.3f}")
OUT["numbers"]["Z1"] = Z1

# ============================================================================================ verdict
banner("VERDICT")
if MUTATE:
    P("  MUTATE: the upper (phantom-inclusive) branch -- DE1/DE2's reading -- keeps MOND on at r_F; the flagship passes once")
    P("  the carrier is cleared.")
else:
    P(f"""  On the matter-only switch the particle-mesh construction runs, the flagship at z = 2.5 needs the carrier gone (its
  gravity costs up to {F1['0.3/1.0']['worst']:+.2f} dex when intact) AND enough circumgalactic matter at r_F to keep the gate open
  (rho_min = {rmin25:.2e} Msun/pc^3 at the linear cell). Passing retentions by CGM share: {passing}.
  The upper branch (DE1/DE2's) keeps MOND on there; the two branches differ exactly at the flagship radius, so which
  one a galaxy occupies -- a question of formation history, not of the static equations -- decides the flagship.""")

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail
OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
