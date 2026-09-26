#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR4_filament_gate_arithmetic.py -- open item 1 of the vacuum-gated construction (L357-L361): gas in active filaments at
z <~ 1 feeling its own deep-MOND field.  Cross-thread review, 2026-09-26.  Arithmetic only (< 1 s).

WHY.  The record states "nu ~ 50-70, force x8-12, infall 17-34 -> 5.5-10 Gyr" for active-filament gas (CLOSURE_MAP row
added in df81d0b72; THE_THEORY_AS_IT_STANDS_2026-09-22.md line 65) but no committed script computes it.  This file
(a) reproduces or refutes those numbers from stated assumptions, (b) gives the density above which filament gas is
ACTIVE under the gate the record now carries, so the size of the untested population is on the record.

MODEL.  Uniform cylinder of proper radius R and mean overdensity delta at redshift z; baryons trace the total
(share f_b = Omega_b/Omega_m); g_N,tot = 2 pi G rhobar_m(z) (1 + delta) R; g_Nb = f_b g_N,tot.  In an ACTIVE region the
gas feels nu(g_Nb/a0) g_Nb + (Newtonian carrier) (L361: in-region baryons move in phi + f P; e_N from embedded groups is
ignored, which OVERSTATES nu); LambdaCDM's gas feels g_N,tot.  Force ratio F = f_b nu + (1 - f_b) r_d, r_d = the carrier's
retained share (1 = kept, 0.075 = GP5/GP4 decayed).  Infall time t = sqrt(2 R/g) (a cylinder's is R-independent).
GATE (L359, DE1's density form): active iff 1.5 Omega_m(z) delta >= x_c0 E(z)^(2p)  ->  delta_th(z) = x_c0 E^(2p)/(1.5
Omega_m(z)).  The shear part of x~ is dropped, as in L359 (it can only LOWER the threshold), so delta_th is an upper bound.

CHECKS
  C1 CONTROL: kernel off (nu = 1) with the carrier kept gives a force ratio of exactly 1 (the construction = LambdaCDM).
  A1 THE RECORD'S NUMBERS: at z = 0, R = 1 Mpc, delta = 1-5, carrier kept: nu in ~[50, 70]-ish and force ratio in
     ~[8, 12], LambdaCDM infall 17-34 Gyr, construction 5.5-10 Gyr -- PASS if each quoted range is reproduced to 25%.
  R1 (reported) delta_th(z) for the DE2 window (p = 1, x_c0 = 2-2.97) and the p = 2, x_c0 = 2 cell, z = 0 ... 2.
  R2 (reported) force ratio and infall times for delta = 5, 10 at z = 0 and 0.5, carrier kept / decayed, both footings.
"""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: print(*a, flush=True)
G, MPC, GYR = 6.674e-11, 3.0857e22, 3.156e16
h = 0.674; H0 = 100 * h * 1e3 / MPC; OM_B = 0.02237 / h ** 2; OM_M = OM_B + 0.1200 / h ** 2; OM_L = 1 - OM_M
FB = OM_B / OM_M; RHOC = 3 * H0 ** 2 / (8 * math.pi * G)
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
OUT = {"lane": "XR4_filament_gate_arithmetic", "checks": {}, "numbers": {}}
CH = []


def check(name, ok, measured):
    ok = bool(ok); CH.append((name, ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


nu = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-30))))
E2 = lambda z: OM_M * (1 + z) ** 3 + OM_L
Omz = lambda z: OM_M * (1 + z) ** 3 / E2(z)


def filament(delta, z, a0, R_mpc=1.0, r_d=1.0, kernel=True):
    gtot = 2 * math.pi * G * RHOC * OM_M * (1 + z) ** 3 * (1 + delta) * R_mpc * MPC
    gb = FB * gtot
    n_ = nu(gb / a0) if kernel else 1.0
    F = (n_ * gb + (1 - FB) * r_d * gtot) / gtot
    t_l = math.sqrt(2 * R_mpc * MPC / gtot) / GYR
    return dict(nu=n_, ratio=F, t_lcdm=t_l, t_con=t_l / math.sqrt(F), gb_a0=gb / a0)


def delta_th(z, xc0, p):
    return xc0 * E2(z) ** p / (1.5 * Omz(z))


c1 = filament(5, 0.0, A0["canonical"], kernel=False)
check("C1 CONTROL: kernel off, carrier kept -> force ratio exactly 1", abs(c1["ratio"] - 1) < 1e-12, f"{c1['ratio']:.15f}")
rows = [filament(d, 0.0, A0["canonical"]) for d in (1.0, 3.0, 5.0)]
nus = [r["nu"] for r in rows]; rats = [r["ratio"] for r in rows]; tl = [r["t_lcdm"] for r in rows]; tc = [r["t_con"] for r in rows]
P(f"  z = 0, R = 1 Mpc, carrier kept, canonical: delta = 1/3/5 -> nu = {nus[0]:.0f}/{nus[1]:.0f}/{nus[2]:.0f}; "
  f"force ratio {rats[0]:.1f}/{rats[1]:.1f}/{rats[2]:.1f}; infall LCDM {tl[0]:.0f}/{tl[1]:.0f}/{tl[2]:.0f} Gyr -> "
  f"construction {tc[0]:.1f}/{tc[1]:.1f}/{tc[2]:.1f} Gyr")
within = lambda vals, lo, hi: all(0.75 * lo <= v <= 1.25 * hi for v in vals)
ok = (within(nus[1:], 50, 70) and within(rats[1:], 8, 12) and within(tl, 17, 34) and within(tc, 5.5, 10))
check("A1 THE RECORD'S NUMBERS (nu 50-70, force x8-12, infall 17-34 -> 5.5-10 Gyr) are reproduced to ~25% for delta ~ 1-5, "
      "R = 1 Mpc, z = 0, carrier kept", ok,
      f"nu {min(nus):.0f}-{max(nus):.0f}; ratio {min(rats):.1f}-{max(rats):.1f}; t_LCDM {min(tl):.0f}-{max(tl):.0f}; "
      f"t_con {min(tc):.1f}-{max(tc):.1f} Gyr")
P("\n  R1  activation threshold delta_th(z) (density-only x~; an upper bound since shear only lowers it)")
cells = [(1.0, 2.0), (1.0, 2.5), (1.0, 2.97), (2.0, 2.0)]
tab = {}
for p_, xc in cells:
    vals = [delta_th(z, xc, p_) for z in (0.0, 0.25, 0.5, 1.0, 2.0)]
    tab[f"p{p_}_xc{xc}"] = vals
    P(f"    p = {p_:g}, x_c0 = {xc:4.2f}:  z = 0/0.25/0.5/1/2 -> delta_th = " + " / ".join(f"{v:5.1f}" for v in vals))
OUT["numbers"]["delta_th"] = tab
P("\n  R2  force ratio and infall time in an ACTIVE filament (R = 1 Mpc)")
r2 = []
for foot, a0 in A0.items():
    for z in (0.0, 0.5):
        for d in (5.0, 10.0):
            for rd in (1.0, 0.075):
                f = filament(d, z, a0, r_d=rd); f.update(foot=foot, z=z, delta=d, r_d=rd); r2.append(f)
                P(f"    {foot:9s} z = {z:3.1f} delta = {d:4.1f} carrier {rd:5.3f}: nu = {f['nu']:5.1f}  force x{f['ratio']:5.2f}  "
                  f"infall {f['t_lcdm']:5.1f} -> {f['t_con']:4.1f} Gyr")
OUT["numbers"]["R2"] = r2
nf = sum(1 for _, ok_ in CH if not ok_)
OUT["n_checks"], OUT["n_fail"] = len(CH), nf
json.dump(OUT, open(os.path.join(HERE, "XR4_filament_gate_arithmetic_results.json"), "w"), indent=1)
P(f"\n  {len(CH) - nf}/{len(CH)} checks pass")
