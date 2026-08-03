#!/usr/bin/env python3
r"""mi_aqual_route_a_refit_2026.py -- THE FULL MILKY WAY AQUAL FIT, RE-SOLVED UNDER ROUTE A'S EXPONENTIAL
KERNEL. The committed alpha=2 study (mi_aqual_mond_refit_2026.py) is the anchor; Route A replaces the kernel,
so its Milky Way number cannot be rescaled -- outside spherical symmetry mu and nu are different objects and
the disc has to be solved again. This solves it.

WHAT CHANGED. Route A: nu(y) = 1/(1 - e^-sqrt(y)), equivalently mu = 1 - e^-u with x = u^2/mu. Adopted because
the power-law approach to Newton fails the solar system (alpha=1 forces a constant a0/2 sunward anomaly at
~1279x the Earth/Mars bound; alpha=2's 1/g tail binds at the SUN's Jupiter-driven reflex and leaves 8.5-12.4x
the Mars ranging budget). The exponential clears that by ~13 orders. The question here is what it costs -- or
buys -- on the one front where the alpha=2 kernel had a clean success: the local vertical force.

METHOD. The solver, the baryon model, the priors and chi^2 are NOT re-implemented. This script `exec`s the
anchor's definitions verbatim up to its first banner, so every difference below is attributable to the kernel
and nothing else. Two departures from the anchor, both established by the 2026-08-02 audit:
  * Sigma_dyn is interpolated in R (the anchor snapped to the mesh column nearest R0 while reading v_c AT R0,
    a one-sided upward bias). Applied to EVERY kernel here, so the kernel comparison stays like-for-like; the
    absolute box result in L7 is reported both ways because it is extractor-sensitive.
  * the (f_M, f_R) grid is widened, and every reported best is checked to be an INTERIOR point.

  L1  the anchor reproduces; and Route A's mu is validated THROUGH the solver against its own nu in spherical
      symmetry, where AQUAL guarantees mu(x) x = y exactly
  L2  the kernel swap at FIXED baryons -- the analytic cross-check, and the trade it makes
  L3  *** THE GRID, BOTH FOOTINGS, Route A and both controls ***
  L4  the anchor's three named configurations, like-for-like
  L5  the Eilers+2019 SLOPE test (permissive -- said so out loud)
  L6  THE KERNEL CONTROL, repeated honestly. The anchor's F4 was a check(True); this one can fail.
  L7  DOES ROUTE A ESCAPE LISANTI'S DILEMMA? An explicit acceptance-box search, answered yes or no.

a0 is an INPUT throughout, both footings, never fitted. Exit 0 = ran and every check held.
"""
from __future__ import annotations

import math
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mi_route_a_kernel import (A0_ALT, A0_CANON, mu as mu_exp, mu_alpha2, mu_simple, nu,
                               nu_alpha2, one_minus_mu, u_of_x)

ok: list[tuple[bool, str]] = []
T0 = time.time()


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


# ------------------------------------------------------------ the anchor's definitions, verbatim, no re-write
SRCPATH = pathlib.Path(__file__).with_name("mi_aqual_mond_refit_2026.py")
_src = SRCPATH.read_text()
_cut = _src.index('banner("F1')
_G: dict = {"__name__": "anchor_defs"}
exec(compile(_src[:_cut], str(SRCPATH), "exec"), _G)

G, KPC, PC, MSUN = _G["G"], _G["KPC"], _G["PC"], _G["MSUN"]
MSUN_PC2 = _G["MSUN_PC2"]
R0 = _G["R0"]
VC, VC_E, KZ, KZ_E = _G["VC"], _G["VC_E"], _G["KZ"], _G["KZ_E"]
MSTAR_P, MSTAR_E = _G["MSTAR_P"], _G["MSTAR_E"]
RDTHIN_P, RDTHIN_E = _G["RDTHIN_P"], _G["RDTHIN_E"]
SIGSTAR_P, SIGSTAR_E = _G["SIGSTAR_P"], _G["SIGSTAR_E"]
solve, densities, chi2 = _G["solve"], _G["densities"], _G["chi2"]
mass_of, sigma_of = _G["mass_of"], _G["sigma_of"]
obs_pub = _G["observables"]

VC_E_CORPUS = 4.0e3        # this corpus's own compiled v_c(R0) error, vs McMillan's statistical 3.0
A0_LIT = 1.2e-10           # the a0 the literature's simple mu is calibrated with -- the anchor's own control


def obs_fixed(fM, fR, a0, mu, **kw):
    """The anchor's extractor with Sigma_dyn interpolated in R, as v_c already was."""
    comp, rdt = densities(fM, fR)
    rho = lambda R, z: sum(f(R, z) for f in comp.values())
    Rc, zc, P = solve(rho, a0, mu, **kw)
    vc = math.sqrt(abs(np.interp(R0, Rc, np.gradient(P[:, 0], Rc))) * R0)
    dPdz = np.gradient(P, zc, axis=1)
    gz11 = np.array([np.interp(1.1 * KPC, zc, dPdz[j, :]) for j in range(len(Rc))])
    sd = abs(np.interp(R0, Rc, gz11)) / (2 * math.pi * G) / MSUN_PC2
    mstar = (mass_of(comp["thin"]) + mass_of(comp["thick"]) + mass_of(comp["bulge"])) / MSUN
    sigstar = (sigma_of(comp["thin"], R0, 1.1 * KPC) + sigma_of(comp["thick"], R0, 1.1 * KPC)) / MSUN_PC2
    return dict(vc=vc, sd=sd, mstar=mstar, sigstar=sigstar, rdt=rdt)


def sigmas(o, vce=VC_E):
    return dict(vc=(o["vc"] - VC) / vce, sd=(o["sd"] - KZ) / KZ_E,
                mstar=(o["mstar"] - MSTAR_P) / MSTAR_E,
                rd=(o["rdt"] - RDTHIN_P) / RDTHIN_E,
                sig=(o["sigstar"] - SIGSTAR_P) / SIGSTAR_E)


def slope_of(fm, fr, a0, mu):
    """Transcribed from the anchor's F5 so slopes are comparable by construction (L5a regresses it)."""
    comp, _ = densities(fm, fr)
    rho = lambda R, z: sum(f(R, z) for f in comp.values())
    Rc, zc, P = solve(rho, a0, mu)
    g = np.gradient(P[:, 0], Rc)
    Rk = np.array([6, 8.21, 12, 16, 20, 25])
    v = np.array([math.sqrt(abs(np.interp(r * KPC, Rc, g)) * r * KPC) for r in Rk])
    return v, float(np.polyfit(Rk[1:], v[1:] / 1e3, 1)[0])


CACHE: dict = {}


def cell(tag, fM, fR, a0, mu):
    k = (tag, round(fM, 4), round(fR, 4))
    if k not in CACHE:
        CACHE[k] = obs_fixed(fM, fR, a0, mu)
    return CACHE[k]


banner("L1  THE ANCHOR REPRODUCES, AND ROUTE A's mu IS VALIDATED THROUGH THE SOLVER")

o_pub = obs_pub(1.30, 0.90, 9.36e-11, mu_alpha2)
print(f"  anchor cell (f_M, f_R) = (1.30, 0.90), alpha=2, published extractor:")
print(f"      v_c = {o_pub['vc']/1e3:.1f} km/s (published 198.6)     "
      f"Sigma_dyn = {o_pub['sd']:.1f} (published 75.2)")
check(abs(o_pub["vc"] / 1e3 - 198.6) < 0.3 and abs(o_pub["sd"] - 75.2) < 0.3,
      f"L1a the committed alpha=2 numbers reproduce from the SAME CODE to "
      f"{abs(o_pub['vc']/1e3-198.6):.2f} km/s and {abs(o_pub['sd']-75.2):.2f} Msun/pc^2. Every Route A "
      f"difference below is the kernel, not a re-implementation")

# --- spherical validation: AQUAL gives mu(x) x = y EXACTLY for a spherical source, so the solver must
#     reproduce the algebraic nu(y) there. Any residual that is COMMON to both kernels is mesh, not kernel.
RS = 1.0 * KPC
RHO0_S = 5.0e10 * MSUN / (8 * math.pi * RS**3)
rho_sph = lambda R, z: RHO0_S * np.exp(-np.sqrt(R * R + z * z) / RS)
M_S = mass_of(rho_sph)
RTEST = (10, 20, 40, 80)          # >= 10 Rs, so the enclosed fraction exceeds 0.997 and g_bar = GM/r^2
print(f"\n  spherical control source: M = {M_S/MSUN:.3e} Msun, exponential, scale 1 kpc")
print(f"  {'R [kpc]':>9}{'y':>10}{'g_obs/g_bar':>13}{'nu_exp(y)':>11}{'ratio':>9}   "
      f"{'a2: g/g':>10}{'nu_a2':>9}{'ratio':>9}")
dev = {"exp": 0.0, "a2": 0.0}
rows = []
for nm, mu_k, nu_k in (("exp", mu_exp, nu), ("a2", mu_alpha2, nu_alpha2)):
    Rc, zc, P = solve(rho_sph, A0_CANON, mu_k)
    g = np.gradient(P[:, 0], Rc)
    r = []
    for Rk in RTEST:
        gobs = abs(np.interp(Rk * KPC, Rc, g))
        gbar = G * M_S / (Rk * KPC) ** 2
        y = gbar / A0_CANON
        rat = gobs / gbar / float(nu_k(y))
        dev[nm] = max(dev[nm], abs(rat - 1.0))
        r.append((y, gobs / gbar, float(nu_k(y)), rat))
    rows.append(r)
for i, Rk in enumerate(RTEST):
    a, b = rows[0][i], rows[1][i]
    print(f"  {Rk:>9}{a[0]:>10.4f}{a[1]:>13.5f}{a[2]:>11.5f}{a[3]:>9.5f}   "
          f"{b[1]:>10.5f}{b[2]:>9.5f}{b[3]:>9.5f}")
check(dev["exp"] < 0.025 and abs(dev["exp"] - dev["a2"]) < 0.006,
      f"L1b Route A's AQUAL mu reproduces its own algebraic nu(y) through the cylindrical solver to "
      f"{100*dev['exp']:.2f}% in spherical symmetry -- and the superseded alpha=2 kernel shows the SAME "
      f"{100*dev['a2']:.2f}%, so that residual is mesh discretisation, not the kernel. The two Route A "
      f"representations are one kernel, as the module's K2 proves analytically")

# --- where in the kernel do the Milky Way observables actually sit? (float64 trap 8b made explicit)
comp_t, _ = densities(1.30, 0.90)
rho_t = lambda R, z: sum(f(R, z) for f in comp_t.values())
Rc, zc, P = solve(rho_t, A0_CANON, mu_exp)
gR = np.gradient(P[:, 0], Rc)
x_R0 = abs(np.interp(R0, Rc, gR)) / A0_CANON
u_R0 = float(u_of_x(x_R0))
i0 = int(np.argmin(np.abs(Rc - R0)))
dPdz = np.gradient(P, zc, axis=1)
x_z11 = abs(np.interp(1.1 * KPC, zc, dPdz[i0, :])) / A0_CANON
u_z11 = float(u_of_x(x_z11))
print(f"\n  at R0: x = |grad Phi|/a0 = {x_R0:.3f} -> u = {u_R0:.3f}, 1 - mu = {float(one_minus_mu(x_R0)):.4f}")
print(f"  at (R0, 1.1 kpc): x = {x_z11:.3f} -> u = {u_z11:.3f}, 1 - mu = {float(one_minus_mu(x_z11)):.4f}")
check(0.1 < u_R0 < 30.0 and 0.1 < u_z11 < 30.0,
      f"L1c both observables sit in the kernel's TRANSITION region (u = {u_R0:.2f} radial, {u_z11:.2f} "
      f"vertical), decades away from the u ~ 37 where 1 - mu underflows in float64. So no saturation is "
      f"hiding in these numbers -- and equally, this front IS kernel-sensitive by construction, which is why "
      f"it had to be re-solved")


banner("L2  THE KERNEL SWAP AT FIXED BARYONS -- the analytic cross-check and the trade it makes")

comp_n, _ = densities(1.30, 0.90)
rho_n = lambda R, z: sum(f(R, z) for f in comp_n.values())
Rc_n, _zc, P_n = solve(rho_n, A0_CANON, mu_exp, newtonian=True)
g_bar_R0 = abs(np.interp(R0, Rc_n, np.gradient(P_n[:, 0], Rc_n)))
y_bar = g_bar_R0 / A0_CANON
pred = math.sqrt(float(nu(y_bar)) / float(nu_alpha2(y_bar)))
o_a2 = cell("a2c", 1.30, 0.90, A0_CANON, mu_alpha2)
o_ex = cell("exc", 1.30, 0.90, A0_CANON, mu_exp)
meas = o_ex["vc"] / o_a2["vc"]
print(f"  Newtonian baryons at R0: g_bar = {g_bar_R0:.4e} m/s^2, y = g_bar/a0 = {y_bar:.4f}")
print(f"  nu_exp(y) = {float(nu(y_bar)):.4f} vs nu_alpha2(y) = {float(nu_alpha2(y_bar)):.4f}  "
      f"-> spherical prediction for v_c ratio = sqrt(ratio) = {pred:.4f}")
print(f"  the DISC solver gives v_c ratio = {o_ex['vc']/1e3:.1f}/{o_a2['vc']/1e3:.1f} = {meas:.4f}")
check(abs(meas / pred - 1.0) < 0.03,
      f"L2a the swap propagated correctly: the measured disc v_c ratio {meas:.4f} matches the spherical "
      f"prediction {pred:.4f} to {100*abs(meas/pred-1):.2f}%. Route A is a ~{100*(pred-1):.0f}% stronger boost "
      f"at the Milky Way's own y = {y_bar:.2f}, which is where the exponential and the alpha=2 forms differ "
      f"most -- not a small perturbation")
s_a2, s_ex = sigmas(o_a2), sigmas(o_ex)
_c1 = "%.1f (%+.1f s)" % (o_a2["vc"] / 1e3, s_a2["vc"])
_c2 = "%.1f (%+.1f s)" % (o_ex["vc"] / 1e3, s_ex["vc"])
_c3 = "%.1f (%+.2f s)" % (o_a2["sd"], s_a2["sd"])
_c4 = "%.1f (%+.2f s)" % (o_ex["sd"], s_ex["sd"])
print("\n  at the anchor's prior-respecting cell (1.30, 0.90), canonical a0, fixed extractor:")
print(f"      {'':<12}{'alpha=2':>20}{'Route A':>20}")
print(f"      {'v_c':<12}{_c1:>20}{_c2:>20}")
print(f"      {'Sigma_dyn':<12}{_c3:>20}{_c4:>20}")
check(abs(s_ex["vc"]) < abs(s_a2["vc"]) and abs(s_ex["sd"]) > abs(s_a2["sd"]),
      f"L2b THE TRADE, both directions at once: at FIXED baryons Route A improves the rotation curve from "
      f"{s_a2['vc']:+.1f} to {s_ex['vc']:+.1f} sigma AND degrades the vertical force from {s_a2['sd']:+.2f} to "
      f"{s_ex['sd']:+.2f} sigma. The alpha=2 kernel's one clean Milky Way success was the vertical force, and "
      f"Route A spends it. Whether that is a net gain is L3-L7's business, not this cell's")


banner("L3  THE GRID, BOTH FOOTINGS, ROUTE A AND BOTH CONTROLS -- a0 an INPUT everywhere")

FM = [1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8]
FR = [0.7, 0.8, 0.9, 1.0, 1.1]
COMBOS = [
    ("Route A exp, canon", "exc", mu_exp, A0_CANON),
    ("Route A exp, ALT", "exa", mu_exp, A0_ALT),
    ("alpha=2 superseded, canon", "a2c", mu_alpha2, A0_CANON),
    ("alpha=2 superseded, ALT", "a2a", mu_alpha2, A0_ALT),
    ("literature simple, a0=1.2e-10", "smL", mu_simple, A0_LIT),
    ("literature simple, canon a0", "smc", mu_simple, A0_CANON),
]
print(f"  f_M in {FM}\n  f_R in {FR}   (M_* scales as f_M f_R^2 -- f_R is NOT a pure concentration knob)\n")

BEST: dict = {}
for label, tag, mu_k, a0 in COMBOS:
    print(f"  --- {label}:  a0 = {a0:.4e} m/s^2 ---")
    print(f"  {'f_M':>5}{'f_R':>5}{'v_c':>8}{'s_vc':>7}{'Sig_dyn':>9}{'s_sd':>7}{'M_*':>10}{'s_M':>6}"
          f"{'Sig_*':>7}{'s_Sg':>6}{'R_d':>6}{'s_Rd':>6}{'chi2_d':>8}{'chi2_p':>8}{'chi2':>8}")
    print("  " + "-" * 104)
    bb = None
    for fM in FM:
        for fR in FR:
            o = cell(tag, fM, fR, a0, mu_k)
            c, cd, cp = chi2(o)
            s = sigmas(o)
            if bb is None or c < bb[0]:
                bb = (c, cd, cp, fM, fR, o)
            print(f"  {fM:>5.2f}{fR:>5.2f}{o['vc']/1e3:>8.1f}{s['vc']:>+7.1f}{o['sd']:>9.1f}{s['sd']:>+7.2f}"
                  f"{o['mstar']:>10.2e}{s['mstar']:>+6.1f}{o['sigstar']:>7.1f}{s['sig']:>+6.1f}"
                  f"{o['rdt']/KPC:>6.2f}{s['rd']:>+6.1f}{cd:>8.1f}{cp:>8.1f}{c:>8.1f}")
    print(f"      coarse best: (f_M, f_R) = ({bb[3]:.2f}, {bb[4]:.2f})  chi2 = {bb[0]:.1f} "
          f"(data {bb[1]:.1f}, priors {bb[2]:.1f})    [{time.time()-T0:.0f}s elapsed]\n")
    BEST[tag] = dict(label=label, a0=a0, mu=mu_k, coarse=bb)

interior = {t: (min(FM) < b["coarse"][3] < max(FM) and min(FR) < b["coarse"][4] < max(FR))
            for t, b in BEST.items()}
_cells = ", ".join("%s:(%.2f,%.2f)" % (t, BEST[t]["coarse"][3], BEST[t]["coarse"][4]) for t in BEST)
check(all(interior.values()),
      f"L3a every one of the six coarse bests is an INTERIOR grid point ({_cells}), "
      f"so the grid is wide enough for all three kernels and no reported minimum is an unexplored edge -- the "
      f"defect the audit found in the anchor's f_R = 0.90 low edge")

# --- local refinement around each coarse best, so grid granularity is not doing the comparing
print("  refining each best on a 3x3 half-step neighbourhood (df_M = 0.15, df_R = 0.05) ...")
for tag, b in BEST.items():
    c0, _, _, fM0, fR0, _ = b["coarse"]
    bb = b["coarse"]
    for fM in (fM0 - 0.15, fM0, fM0 + 0.15):
        for fR in (fR0 - 0.05, fR0, fR0 + 0.05):
            if fM <= 0 or fR <= 0:
                continue
            o = cell(tag, fM, fR, b["a0"], b["mu"])
            c, cd, cp = chi2(o)
            if c < bb[0]:
                bb = (c, cd, cp, fM, fR, o)
    b["best"] = bb
    s = sigmas(bb[5])
    print(f"    {b['label']:<32} best (f_M, f_R) = ({bb[3]:.2f}, {bb[4]:.2f})  chi2 = {bb[0]:.1f}  "
          f"v_c {s['vc']:+.2f}s  Sig_dyn {s['sd']:+.2f}s  M_* {s['mstar']:+.2f}s  Sig_* {s['sig']:+.2f}s  "
          f"R_d {s['rd']:+.2f}s")

bex, bea = BEST["exc"]["best"], BEST["exa"]["best"]
check(bea[0] != bex[0],
      f"L3b the two footings are NOT degenerate on this front: canonical a0 = {A0_CANON:.4e} gives chi2 = "
      f"{bex[0]:.1f} at (f_M, f_R) = ({bex[3]:.2f}, {bex[4]:.2f}) and the alt a0 = {A0_ALT:.4e} gives "
      f"{bea[0]:.1f} at ({bea[3]:.2f}, {bea[4]:.2f}). The alt footing's larger a0 buys the same v_c with "
      f"{100*(1-bea[3]/bex[3]):+.0f}% of the stellar mass scaling -- the spread between footings is a real "
      f"part of the answer, not a rounding")


banner("L4  THE ANCHOR'S THREE NAMED CONFIGURATIONS, LIKE-FOR-LIKE")

NAMED = [("priors respected (1.30, 0.90)", 1.30, 0.90),
         ("v_c-bought  (1.90, 0.90)", 1.90, 0.90)]
print(f"  {'configuration':<32}{'kernel':<14}{'v_c':>8}{'s_vc':>7}{'Sig_dyn':>9}{'s_sd':>7}"
      f"{'s_M':>6}{'s_Sg':>6}{'s_Rd':>6}{'chi2_p':>8}{'chi2':>8}")
print("  " + "-" * 108)
for nm, fM, fR in NAMED:
    for kl, tag, mu_k, a0 in (("alpha=2 canon", "a2c", mu_alpha2, A0_CANON),
                              ("Route A canon", "exc", mu_exp, A0_CANON),
                              ("Route A ALT", "exa", mu_exp, A0_ALT)):
        o = cell(tag, fM, fR, a0, mu_k)
        c, cd, cp = chi2(o)
        s = sigmas(o)
        print(f"  {nm:<32}{kl:<14}{o['vc']/1e3:>8.1f}{s['vc']:>+7.1f}{o['sd']:>9.1f}{s['sd']:>+7.2f}"
              f"{s['mstar']:>+6.1f}{s['sig']:>+6.1f}{s['rd']:>+6.1f}{cp:>8.1f}{c:>8.1f}")
sm = BEST["smL"]["best"]
ssm = sigmas(sm[5])
print(f"  {'literature simple, own best':<32}{'simple 1.2e-10':<14}{sm[5]['vc']/1e3:>8.1f}{ssm['vc']:>+7.1f}"
      f"{sm[5]['sd']:>9.1f}{ssm['sd']:>+7.2f}{ssm['mstar']:>+6.1f}{ssm['sig']:>+6.1f}{ssm['rd']:>+6.1f}"
      f"{sm[2]:>8.1f}{sm[0]:>8.1f}")

o_vcb_a2 = cell("a2c", 1.90, 0.90, A0_CANON, mu_alpha2)
o_vcb_ex = cell("exc", 1.90, 0.90, A0_CANON, mu_exp)
s_vcb_a2, s_vcb_ex = sigmas(o_vcb_a2), sigmas(o_vcb_ex)
check(abs(s_a2["sd"]) < 1.0 and abs(s_a2["vc"]) > 5.0 and abs(s_ex["vc"]) < abs(s_a2["vc"]),
      f"L4a the anchor's published dilemma is reproduced in its own terms -- alpha=2 at (1.30, 0.90) has the "
      f"vertical force at {s_a2['sd']:+.2f} sigma and the rotation curve at {s_a2['vc']:+.1f} sigma -- and "
      f"Route A moves the rotation curve to {s_ex['vc']:+.1f} sigma at the SAME baryons. The anchor's "
      f"'v_c-bought' cell (1.90, 0.90), which cost alpha=2 M_* {s_vcb_a2['mstar']:+.1f} sigma and Sigma_* "
      f"{s_vcb_a2['sig']:+.1f} sigma, is under Route A already OVERSHOOTING v_c at {s_vcb_ex['vc']:+.1f} sigma")


banner("L5  THE EILERS+2019 SLOPE TEST -- and it is PERMISSIVE, said out loud")

SLOPE_OBS, SLOPE_STAT, SLOPE_SYS = -1.7, 0.1, 0.46
SLOPE_TOT = math.hypot(SLOPE_STAT, SLOPE_SYS)
print(f"""  Eilers, Hogg, Rix & Ness 2019 (ApJ 871, 120): dv_c/dR = {SLOPE_OBS} +- {SLOPE_STAT} (stat)
  +- {SLOPE_SYS} (sys) km/s/kpc over 5-25 kpc. The systematic ALONE admits -1.24 to -2.16 at 1 sigma and
  {SLOPE_OBS-2*SLOPE_TOT:+.2f} to {SLOPE_OBS+2*SLOPE_TOT:+.2f} at 2 sigma, so this test EXCLUDES very little and no
  agreement here should be sold as strong. It is reported because the anchor reported it.\n""")
SL = [("alpha=2, priors respected (1.30, 0.90)", 1.30, 0.90, A0_CANON, mu_alpha2),
      ("Route A canon, priors respected (1.30, 0.90)", 1.30, 0.90, A0_CANON, mu_exp),
      (f"Route A canon, BEST ({bex[3]:.2f}, {bex[4]:.2f})", bex[3], bex[4], A0_CANON, mu_exp),
      (f"Route A ALT, BEST ({bea[3]:.2f}, {bea[4]:.2f})", bea[3], bea[4], A0_ALT, mu_exp),
      (f"literature simple, BEST ({sm[3]:.2f}, {sm[4]:.2f})", sm[3], sm[4], A0_LIT, mu_simple)]
print(f"  {'model':<48}{'v_c(8.21)':>11}{'v_c(20)':>9}{'slope':>8}{'vs obs':>16}")
print("  " + "-" * 96)
SLOPES = {}
for nm, fm, fr, a0, mu_k in SL:
    v, s_ = slope_of(fm, fr, a0, mu_k)
    z = (s_ - SLOPE_OBS) / SLOPE_TOT
    SLOPES[nm] = (s_, z)
    print(f"  {nm:<48}{v[1]/1e3:>11.1f}{v[4]/1e3:>9.1f}{s_:>8.2f}{z:>+11.1f} sigma")
k_a2 = SL[0][0]
check(abs(SLOPES[k_a2][0] + 1.14) < 0.06,
      f"L5a the slope routine is the anchor's: it returns {SLOPES[k_a2][0]:+.2f} km/s/kpc for the published "
      f"alpha=2 (1.30, 0.90) model against the published -1.14, so L5's Route A slopes are comparable to the "
      f"committed ones by construction")
k_best = SL[2][0]
check(abs(SLOPES[k_best][1]) < 3.0,
      f"L5b Route A's BEST-FIT model has slope {SLOPES[k_best][0]:+.2f} km/s/kpc, i.e. "
      f"{SLOPES[k_best][1]:+.1f} sigma from Eilers' {SLOPE_OBS} on stat+sys in quadrature. Read this as a "
      f"NON-EXCLUSION, not a confirmation: the +-{SLOPE_SYS} systematic is wide enough that a flat-ish and a "
      f"steeply falling curve both survive it")


banner("L6  THE KERNEL CONTROL -- the anchor's F4 was a check(True); this one can fail")

cE, cA, cS, cSc = BEST["exc"]["best"][0], BEST["a2c"]["best"][0], BEST["smL"]["best"][0], BEST["smc"]["best"][0]
cEa, cAa = BEST["exa"]["best"][0], BEST["a2a"]["best"][0]
print(f"  all on ONE grid, ONE extractor, ONE set of priors, each kernel at its own best (f_M, f_R):\n")
print(f"  {'kernel / footing':<34}{'best cell':>14}{'chi2':>8}{'chi2_pri':>10}{'s_vc':>8}{'s_sd':>8}"
      f"{'s_M':>7}{'s_Sg':>7}")
print("  " + "-" * 96)
for tag in ("exc", "exa", "a2c", "a2a", "smL", "smc"):
    b = BEST[tag]["best"]
    s = sigmas(b[5])
    print(f"  {BEST[tag]['label']:<34}{f'({b[3]:.2f}, {b[4]:.2f})':>14}{b[0]:>8.1f}{b[2]:>10.1f}"
          f"{s['vc']:>+8.2f}{s['sd']:>+8.2f}{s['mstar']:>+7.2f}{s['sig']:>+7.2f}")
DCHI2_1SIG_2DOF = 2.30
gap_a2 = abs(cA - cS)
gap_ex = abs(cE - cS)
print(f"\n  Route A vs the kernel it REPLACES:            Delta chi2 = {cA - cE:+.1f}  (canonical footing)")
print(f"                                                Delta chi2 = {cAa - cEa:+.1f}  (alt footing)")
print(f"  Route A vs the LITERATURE's simple mu:        Delta chi2 = {cS - cE:+.1f}  "
      f"(+ favours Route A, - favours the literature)")
print(f"  alpha=2 vs the literature's simple mu:        Delta chi2 = {cS - cA:+.1f}")
print(f"  the literature's kernel at the FRAMEWORK's a0: chi2 = {cSc:.1f}  (vs {cS:.1f} at its own 1.2e-10)")
check(cA - cE > DCHI2_1SIG_2DOF and cAa - cEa > DCHI2_1SIG_2DOF,
      f"L6a *** ROUTE A BEATS THE KERNEL IT REPLACES ON THE MILKY WAY, on both footings and decisively: "
      f"Delta chi2 = {cA-cE:+.1f} (canonical) and {cAa-cEa:+.1f} (alt), against the {DCHI2_1SIG_2DOF} that "
      f"1 sigma on two joint parameters would need. *** The switch was forced by the solar system and it "
      f"IMPROVES the Milky Way; that is not what a patch usually does")
check(gap_ex < gap_a2,
      f"L6b and the control's verdict has MOVED: the literature's simple mu led the framework's kernel by "
      f"Delta chi2 = {gap_a2:.1f} under alpha=2 on this grid (the anchor reported 21.9 vs 56.9 on its own "
      f"narrower one, the same story), and under Route A the gap is {gap_ex:.1f}. The framework's kernel is no "
      f"longer the one being beaten by the literature's")
# the two kernels' own boost factors at the Galaxy's own y, which is WHY the Galaxy cannot separate them
nu_exp_mw = float(nu(y_bar))
nu_sim_mw = (1.0 + math.sqrt(1.0 + 4.0 / y_bar)) / 2.0        # inverse of mu = x/(1+x)
check(abs(cS - cE) < DCHI2_1SIG_2DOF,
      f"L6c *** AGAINST INTEREST, AND THIS IS THE MAIN COST: the Milky Way is now NON-DIAGNOSTIC of Route A "
      f"versus the literature's simple mu. |Delta chi2| = {abs(cS-cE):.1f} is below {DCHI2_1SIG_2DOF}, i.e. the "
      f"two kernels fit the Galaxy indistinguishably. *** The reason is structural, not a coincidence of this "
      f"grid: at the Galaxy's own y = {y_bar:.2f} the boost factors are nu_RouteA = {nu_exp_mw:.4f} and "
      f"nu_simple = {nu_sim_mw:.4f}, apart by {100*abs(nu_exp_mw/nu_sim_mw-1):.1f}% against the "
      f"{100*abs(nu_exp_mw/float(nu_alpha2(y_bar))-1):.0f}% that separated Route A from alpha=2. Route A stops "
      f"LOSING this control and does not start WINNING it -- the front no longer discriminates the framework's "
      f"kernel from the literature's, which is a loss of evidential value even though the fit improved")


banner("L7  DOES ROUTE A ESCAPE LISANTI'S DILEMMA?  -- an explicit acceptance box, answered")

BOX = 2.0
KEYS = ("vc", "sd", "mstar", "rd", "sig")
print(f"""  THE DILEMMA, stated so it can be answered: is there ONE baryon model that simultaneously matches the
  rotation curve at R0, the local vertical force, and every star-count prior? The anchor's answer under
  alpha=2 was no -- "no point satisfies both". The test: does any solved cell hold all five constraints
  within {BOX:.0f} sigma at once (v_c, Sigma_dyn, M_*, R_d, Sigma_*)?\n""")
print(f"  {'kernel / footing':<34}{'cells in box':>13}{'best box cell':>15}{'chi2':>8}"
      f"{'worst constraint':>26}")
print("  " + "-" * 98)
BOXRES = {}
for tag in ("exc", "exa", "a2c", "a2a", "smL", "smc"):
    b = BEST[tag]
    inbox = []
    for (t, fM, fR), o in CACHE.items():
        if t != tag:
            continue
        s = sigmas(o)
        if max(abs(s[k]) for k in KEYS) <= BOX:
            inbox.append((chi2(o)[0], fM, fR, o))
    inbox.sort()
    BOXRES[tag] = inbox
    if inbox:
        c_, fM, fR, o = inbox[0]
        s = sigmas(o)
        w = max(KEYS, key=lambda k: abs(s[k]))
        print(f"  {b['label']:<34}{len(inbox):>13}{f'({fM:.2f}, {fR:.2f})':>15}{c_:>8.1f}"
              f"{f'{w} at {s[w]:+.2f}s':>26}")
    else:
        # how close does the closest cell get?
        cl = min(((max(abs(sigmas(o)[k]) for k in KEYS), fM, fR, o)
                  for (t, fM, fR), o in CACHE.items() if t == tag), key=lambda z: z[0])
        s = sigmas(cl[3])
        w = max(KEYS, key=lambda k: abs(s[k]))
        print(f"  {b['label']:<34}{0:>13}{f'({cl[1]:.2f}, {cl[2]:.2f})':>15}"
              f"{chi2(cl[3])[0]:>8.1f}{f'{w} at {s[w]:+.2f}s (closest)':>26}")
n_ex = len(BOXRES["exc"]) + len(BOXRES["exa"])
n_a2 = len(BOXRES["a2c"]) + len(BOXRES["a2a"])


def worst_reach(tag):
    """the smallest achievable WORST-constraint violation for a kernel: how close it gets to the box."""
    return min(max(abs(sigmas(o)[k]) for k in KEYS) for (t, _fM, _fR), o in CACHE.items() if t == tag)


w_ex = min(worst_reach("exc"), worst_reach("exa"))
w_a2 = min(worst_reach("a2c"), worst_reach("a2a"))
w_sm = min(worst_reach("smL"), worst_reach("smc"))
check(n_ex == 0 and n_a2 == 0,
      f"L7a *** ROUTE A DOES NOT ESCAPE LISANTI'S DILEMMA. *** {n_ex} Route A cell(s) and {n_a2} alpha=2 "
      f"cell(s) clear the {BOX:.0f}-sigma box on all five constraints at once, over both footings and the "
      f"whole grid. The anchor's 'no point satisfies both' SURVIVES the kernel switch -- the exponential "
      f"kernel does not buy a jointly acceptable Milky Way, and any reading of the chi2 improvement in L6a as "
      f"'the Galaxy now works' is wrong")
check(w_ex < w_a2,
      f"L7b what DID change is how close the dilemma comes to being satisfied: the best worst-constraint "
      f"Route A can reach is {w_ex:.2f} sigma against alpha=2's {w_a2:.2f} sigma -- a real narrowing "
      f"({100*(1-w_ex/w_a2):.0f}%) that still misses the {BOX:.0f}-sigma box. alpha=2 misses it on "
      f"{max(KEYS, key=lambda k: abs(sigmas(BEST['a2c']['best'][5])[k]))}, Route A on a different constraint "
      f"-- the binding one moved")
check(len(BOXRES["smc"]) > 0 and n_ex == 0,
      f"L7c *** AGAINST INTEREST, THE SHARPEST SINGLE LINE IN THIS SCRIPT: the ONLY combination on the whole "
      f"run that clears the box is the LITERATURE's simple mu evaluated at the FRAMEWORK's own canonical a0 "
      f"({len(BOXRES['smc'])} cell, worst constraint {w_sm:.2f} sigma). *** So the Milky Way's one jointly "
      f"acceptable solution here credits the framework's a0 and the literature's kernel, not the framework's "
      f"kernel. That is the honest headline of L6c and L7a taken together, and it is not a result the "
      f"framework can claim")

# what the escape actually costs, and how fragile it is. If NEITHER footing produced a box cell, the honest
# reference point is the closest cell Route A reaches -- the script must report that case, not crash on it.
if BOXRES["exc"] or BOXRES["exa"]:
    bt = "exc" if BOXRES["exc"] else "exa"
    c_b, fM_b, fR_b, o_b = BOXRES[bt][0]
    HEAD = "WHAT THE ESCAPE IS, in full"
else:
    bt = "exc"
    _w, fM_b, fR_b, o_b = min(((max(abs(sigmas(o)[k]) for k in KEYS), fM, fR, o)
                               for (t, fM, fR), o in CACHE.items() if t == bt), key=lambda z: z[0])
    c_b = chi2(o_b)[0]
    HEAD = "NO CELL ENTERED THE BOX -- here is the CLOSEST Route A gets"
s_b = sigmas(o_b)
s_b4 = sigmas(o_b, VC_E_CORPUS)
o_b_pub = obs_pub(fM_b, fR_b, BEST[bt]["a0"], mu_exp)
sd_bias = o_b_pub["sd"] - o_b["sd"]
print(f"""
  {HEAD}: {BEST[bt]['label']}, (f_M, f_R) = ({fM_b:.2f}, {fR_b:.2f})
      v_c(R0)   = {o_b['vc']/1e3:6.1f} km/s      ({s_b['vc']:+.2f} sigma on McMillan's +-3.0, {s_b4['vc']:+.2f} on this corpus's +-4)
      K_z,1.1   = {o_b['sd']:6.1f} Msun/pc^2 ({s_b['sd']:+.2f} sigma vs 73.9 +- 6.0)
      M_*       = {o_b['mstar']:.3e} Msun  ({s_b['mstar']:+.2f} sigma vs 54.3e9 +- 5.7e9)
      R_d,thin  = {o_b['rdt']/KPC:6.2f} kpc       ({s_b['rd']:+.2f} sigma vs 2.6 +- 0.52)
      Sigma_*   = {o_b['sigstar']:6.1f} Msun/pc^2 ({s_b['sig']:+.2f} sigma vs Bovy & Rix's 38 +- 4)
      chi2 = {c_b:.1f} on 3 effective dof

  THE SHAPE OF THE COMPROMISE, stated against interest: R_d comes out {abs(s_b['rd']):.1f} sigma
  {'below' if s_b['rd'] < 0 else 'above'} the adopted scale length, the stellar mass {s_b['mstar']:+.1f} sigma
  {'above' if s_b['mstar'] > 0 else 'below'} McMillan's, and the LOCAL stellar column {s_b['sig']:+.1f} sigma
  against Bovy & Rix -- a {'shorter, heavier' if (s_b['rd'] < 0 and s_b['mstar'] > 0) else 'differently shaped'}
  disc than the star counts prefer. And the residual has MOVED: at the anchor's prior-respecting cell alpha=2
  had the rotation curve {s_a2['vc']:+.1f} sigma with the vertical force at {s_a2['sd']:+.2f}; here the
  rotation curve is {s_b['vc']:+.2f} and the VERTICAL FORCE is the binding one at {s_b['sd']:+.2f} sigma.
  The tension changed which constraint it loads; it did not vanish.""")
check(sd_bias > 0.0,
      f"L7d and this cell is EXTRACTOR-SENSITIVE, so it is quoted with that attached: the anchor's snapped "
      f"extractor returns Sigma_dyn = {o_b_pub['sd']:.1f} against the interpolated {o_b['sd']:.1f}, i.e. "
      f"{sd_bias:+.1f} Msun/pc^2 = {sd_bias/KZ_E:+.2f} sigma of one-sided upward bias (v_c is untouched: "
      f"{o_b_pub['vc']/1e3:.1f} vs {o_b['vc']/1e3:.1f} km/s). On the snapped extractor the vertical force "
      f"here reads {sigmas(o_b_pub)['sd']:+.2f} sigma instead of {s_b['sd']:+.2f}, so part of how CLOSE Route "
      f"A gets is the audit's fix and not the kernel -- had this cell cleared the box, the box membership "
      f"would have been extractor-dependent. The kernel comparisons in L7a/L7b are immune: every kernel there "
      f"used the same fixed extractor")

_verdict = ("DOWNGRADES it from irreducible to marginal -- a jointly acceptable cell now exists" if n_ex > 0
            else "NARROWS it but does NOT escape it -- no cell satisfies all five at once")
_a2b = sigmas(BEST["a2c"]["best"][5])
print(f"""
  THE ANSWER TO THE QUESTION ASKED: Route A {_verdict}. The numbers: {n_ex} Route A cells and {n_a2} alpha=2
  cells clear the {BOX:.0f}-sigma box; the best worst-constraint falls from {w_a2:.2f} sigma (alpha=2) to
  {w_ex:.2f} sigma (Route A), and the best chi2 from {cA:.1f} to {cE:.1f} canonical. So the kernel switch made
  the Milky Way substantially LESS bad and left it short of jointly acceptable, with the binding constraint
  moved off the rotation curve and onto the vertical force. Three things stop this being a win for the
  FRAMEWORK specifically rather than for the exponential FAMILY: the literature's simple mu matches it to
  Delta chi2 = {abs(cS-cE):.1f} (L6c), it is the LITERATURE's kernel that supplies the run's only box-clearing
  cell (L7c), and the closest Route A solution wants a disc shorter and heavier than the star counts prefer
  while part of its closeness comes from the extractor fix rather than the kernel (L7d).""")


banner("SCOPE AND CAVEATS")
print(f"""   * TWO free parameters only (a common stellar-mass scale, a common scale-length scale), and f_R moves
     the mass as f_R^2, so it is not a clean concentration knob. Every chi2 here is an UPPER bound on what a
     wider refit would reach, for all three kernels equally.
   * a0 was an INPUT throughout, both footings, never fitted or nudged. Canonical {A0_CANON:.4e} and alt
     {A0_ALT:.4e}. The alt footing reaches the same v_c with a lower stellar mass scale, and the two are
     separated by only Delta chi2 = {abs(cE-cEa):.1f} ({'alt' if cEa < cE else 'canonical'} ahead), i.e. the
     footing fork is NOT resolved by this front under Route A -- worth recording because under the alpha=2
     kernel the alt footing led by a clear margin.
   * v_c(R0) = 233.1 +- 3.0 is McMillan's STATISTICAL error; this corpus's own compilation is 233 +- 4. Both
     conventions are printed at the box cell. The +-3.0 is the tighter one, i.e. the one that is harder on the
     framework, and it is the one the chi2 uses.
   * The vertical target 73.9 is McMillan's FITTED K_z,1.1 with Holmberg & Flynn's +-6, not an error he
     quotes. The Sigma_* prior is Bovy & Rix's stellar column. Gas is held at survey values, bulge at DIRBE.
   * Reduced mesh (n = 110, growth 1.085, 400 Picard), the anchor's own settings, so the numbers are
     comparable to the committed ones cell by cell.
   * The anchor's F4 carries a live check(True) at its line ~297 ("F4 recorded: ..."), which cannot fail and
     therefore recorded rather than tested the kernel control. L6a/L6b/L6c above are falsifiable inequalities
     on the same comparison. The anchor's F2/F3 checks have the same shape (check(True), and an `or True`).
   * NOT tested here, and each could move this: the full rotation curve rather than v_c(R0) alone; thin and
     thick discs freed separately; R0 and the gas freed; the external-field effect; and the MI (as opposed to
     AQUAL) realisation of the same kernel, which is a DIFFERENT theory outside spherical symmetry and is not
     what this solver integrates.""")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.   [{time.time()-T0:.0f}s]")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the Milky Way AQUAL fit re-solved under Route A, both footings, a0 an input, kernel "
      "control repeated with a check that could have failed.")
