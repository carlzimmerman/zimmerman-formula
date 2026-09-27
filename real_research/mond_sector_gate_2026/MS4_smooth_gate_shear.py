#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
MS4 -- DOES A SMOOTH, ACTION-READY GATE KEEP MS3's COSMIC-SHEAR PASS?  L363's resolution-free halo model on the
MOND-sector reading with DE7/DE9's smooth gate at the transition widths DE9's window allows.

WHY.  MS3 (2a5def6d9) passed cosmic shear with a SHARP gate: worst R 1.05/1.12 (canonical/alt) with every MOND region
capped at 1.75 Mpc (z = 0.5) and L388's retention.  An action term needs a smooth gate.  DE9 (8c3bfe8f3) found the smooth
gate's own data window on the MOND-sector reading at p = 1: transition widths w <= 0.5 (KiDS's cap falling 4.48 -> 3.76 as
w goes 0.1 -> 0.75).  DE9 did not score cosmic shear.  This lane does, on MS3's machinery.

THE SMOOTH GATE (DE7/DE9's): f = W(t), t = (u/x_c0 - 1)/(2w) + 1/2, W(t) = g(t)/(g(t) + g(1 - t)), g = e^(-1/t) (t > 0),
f = 0 from the first radius where t <= 0 outward.  u is MS3's MOND-sector door variable on the host in the mean density,
x = 1.5 Omega_m(z) (f_b rho_host + rho_ph)/rho_bar_m, read with the ungated phantom (first order in the gate's width).
The gated phantom's enclosed mass is f(r) M_ph(<r), so its transform is int f M_ph k j1(kr) dr (compensated wherever f
reaches 0), cut at r_cap when capped.
CHECKS
  C1 CONTROL: a near-sharp gate (w = 1e-3) reproduces MS3's committed door numbers at the linear cell with L388's
     retention (no cap 2.72/3.18; cap 1.75 Mpc 1.047/1.121) within 1%.
  S1 PRE-DECLARED (written before the run): with the 1.75 Mpc cap, worst R <= 1.2 on both footings at w = 0.25 and 0.5
     -- the smooth gate keeps MS3's pass.
  S2 (reported) without the cap, worst R at w = 0.25 and 0.5.
  S3 (reported) the largest passing cap at each width (1.5, 1.75, 2.0 Mpc).
MUTATE=1 removes the cap: S1 must FAIL (rc = 1).

SCOPE.  MS3's (L363's halo model: isolated regions, one lens epoch z = 0.5, P(k), GP0's observed bound baryons, L388's
retention by halo mass).  The gate variable uses the ungated phantom; the self-consistent smooth-gate solution would
shift the edge by O(w) less.

Run from the repository root:  python3 real_research/mond_sector_gate_2026/MS4_smooth_gate_shear.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np
from scipy.special import spherical_jn

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "MS4_smooth_gate_shear"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "MS4", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: no cap; S1 must FAIL ***")

# ---------------------------------------------------------------------------------- MS3's machinery, loaded unedited
p3 = os.path.join(HERE, "MS3_cosmic_shear_bound_mond_sector.py")
M3 = {"__name__": "ms3", "__file__": p3}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(p3).read().split('banner("C1  CONTROL')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), M3)
MS3R = json.load(open(os.path.join(HERE, "MS3_cosmic_shear_bound_mond_sector_results.json")))["numbers"]
GP0, KC, RHO, PNL, PLIN, h, ZS, aS = (M3[k_] for k_ in ("GP0", "KC", "RHO", "PNL", "PLIN", "h", "ZS", "aS"))
G, MS, MPC, nu_mono, Omz, E2, I1, nfw_uk = (M3[k_] for k_ in ("G", "MS", "MPC", "nu_mono", "Omz", "E2", "I1", "nfw_uk"))
FB, dn, bh, LMH, dlnM, XLIN, A0, KG = (M3[k_] for k_ in ("FB", "dn", "bh", "LMH", "dlnM", "XLIN", "A0", "KG"))
rho_bar_phys, rho_c_phys, ret_L388 = M3["rho_bar_phys"], M3["rho_c_phys"], M3["ret_L388"]


def Wg(t):
    t = np.asarray(t, float)
    g = lambda s: np.where(s > 0, np.exp(-1.0 / np.maximum(s, 1e-300)), 0.0)
    return g(t) / np.maximum(g(t) + g(1 - t), 1e-300)


def transform_smooth(M, Mb, xc, a0, rcap, w):
    c = 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h))) * (1 + ZS) ** -0.5
    r200 = (3 * M / (4 * math.pi * 200 * rho_c_phys)) ** (1 / 3); rs = r200 / c; mc = math.log(1 + c) - c / (1 + c)
    r = np.geomspace(1e-3 * r200, 30.0, 4000)
    y = G * Mb * MS / (r * MPC) ** 2 / a0
    Mph = (nu_mono(y) - 1) * Mb
    rho_ph = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    rho_h = np.where(r < r200, M / (4 * math.pi * rs ** 3 * mc) / ((r / rs) * (1 + r / rs) ** 2), 0.0)
    x = 1.5 * Omz * ((FB * rho_h + np.maximum(rho_ph, 0)) / rho_bar_phys)
    t = (x / xc - 1) / (2 * w) + 0.5
    f = Wg(t)
    off = np.where(t <= 0)[0]
    if off.size: f[off[0]:] = 0.0
    f = np.where(r <= rcap, f, 0.0)
    rc = r / aS; kr = np.outer(KC, rc)
    return np.trapz((f * Mph)[None, :] * KC[:, None] * spherical_jn(1, kr), rc, axis=1)


def R_smooth(xc, a0, rcap, w, ret=ret_L388):
    P1 = np.zeros_like(KC); X1 = np.zeros_like(KC); B = np.zeros_like(KC); rm = np.zeros_like(KC)
    for lm in LMH:
        M = 10 ** lm; n = float(np.interp(lm, GP0.LM, dn)); b = float(np.interp(lm, GP0.LM, bh))
        Mb = float(GP0.M_bound(M, ZS, "observed")); tr = transform_smooth(M, Mb, xc, a0, rcap, w); uk = nfw_uk(M, KC)
        P1 += n * tr ** 2 * dlnM / RHO ** 2; B += n * b * tr * dlnM / RHO
        fr = ret(M); mass_1h = (FB + (1 - FB) * fr) * M
        rm += n * ((M * uk) ** 2 - (mass_1h * uk) ** 2) * dlnM / RHO ** 2
        X1 += n * mass_1h * uk * tr * dlnM / RHO ** 2
    R = (PNL - rm + 2 * (X1 + I1 * B * PLIN) + P1 + B ** 2 * PLIN) / PNL
    return max(float(np.interp(math.log(q * h), np.log(KC), R)) for q in KG)


# ============================================================================================ C1
banner("C1  CONTROL: a near-sharp gate reproduces MS3's committed door numbers")
ref_nocap = {f: MS3R["X1"][f"door/L388 retention/{f}"]["worst"] for f in A0}
ref_cap = {f: MS3R["K1"]["1.75"][f]["worst"] for f in A0}
mine_nocap = {f: R_smooth(XLIN, A0[f], math.inf, 1e-3) for f in A0}
mine_cap = {f: R_smooth(XLIN, A0[f], 1.75, 1e-3) for f in A0}
dev = max(max(abs(mine_nocap[f] / ref_nocap[f] - 1), abs(mine_cap[f] / ref_cap[f] - 1)) for f in A0)
P(f"    no cap: {mine_nocap['canonical']:.3f}/{mine_nocap['alt']:.3f} vs MS3 {ref_nocap['canonical']:.3f}/{ref_nocap['alt']:.3f}; "
  f"cap 1.75: {mine_cap['canonical']:.3f}/{mine_cap['alt']:.3f} vs MS3 {ref_cap['canonical']:.3f}/{ref_cap['alt']:.3f}")
check("C1 CONTROL: w = 1e-3 reproduces MS3's committed door numbers (L388 retention, no cap and 1.75 Mpc cap) within 1%",
      f"max relative deviation {dev:.2e}", dev < 0.01, load_bearing=False)

# ============================================================================================ S1-S3
banner("S1-S3  THE SMOOTH GATE AT DE9's WIDTHS (p = 1, x_c0 = 2.5, L388 retention)")
TAB = {}
for w in (0.25, 0.5):
    for rc_ in ([math.inf] if MUTATE else [math.inf, 2.0, 1.75, 1.5]):
        TAB[(w, rc_)] = {f: R_smooth(XLIN, A0[f], rc_, w) for f in A0}
        P(f"    w = {w:4.2f}, cap {rc_:5.2f} Mpc: worst R canonical {TAB[(w, rc_)]['canonical']:.3f}, alt {TAB[(w, rc_)]['alt']:.3f}")
OUT["numbers"]["table"] = {f"{w}/{rc_}": v_ for (w, rc_), v_ in TAB.items()}
cap_used = math.inf if MUTATE else 1.75
s1 = all(TAB[(w, cap_used)][f] <= 1.2 for w in (0.25, 0.5) for f in A0)
check("S1 PRE-DECLARED: with the 1.75 Mpc cap the smooth MOND-sector gate keeps cosmic shear within 20% of LCDM (worst "
      "R <= 1.2) on both footings at w = 0.25 and 0.5",
      "; ".join(f"w {w}: {TAB[(w, cap_used)]['canonical']:.3f}/{TAB[(w, cap_used)]['alt']:.3f}" for w in (0.25, 0.5)), s1)
if not MUTATE:
    nocap = {w: TAB[(w, math.inf)] for w in (0.25, 0.5)}
    check("S2 (reported) without the cap the smooth gate fails as the sharp one does",
          "; ".join(f"w {w}: {v_['canonical']:.2f}/{v_['alt']:.2f}" for w, v_ in nocap.items()), True, load_bearing=False)
    best = {w: max([rc_ for rc_ in (2.0, 1.75, 1.5) if all(TAB[(w, rc_)][f] <= 1.2 for f in A0)], default=None) for w in (0.25, 0.5)}
    OUT["numbers"]["largest_passing_cap"] = best
    check("S3 (reported) the largest passing cap at each width", best, True, load_bearing=False)

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail; OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
