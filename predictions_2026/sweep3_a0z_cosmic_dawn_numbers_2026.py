#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sweep3_a0z_cosmic_dawn_numbers_2026.py
======================================
Predictions-audit inventory sweep 3/4 (a0(z) + cosmic dawn): RE-DERIVES every registered number in
this source group on BOTH a0 footings, so the inventory JSON/MD next to this file is not transcribed.

Source group covered: nbody_2026/stage17 (derived a0(z) law), stage19 (CLASS re-run), stage21
(MUSE/MSA-3D re-exam), stage23 (S8 null), stage24 (cosmic-dawn linear-growth theorem), stage25
(early-rotator BTFR + Sigma_dagger), stage26 (collapse timing), the Ly-alpha forest b-cutoff
(real_research/reviews/mi_forest_*), DESI w(z) dissolution, SN-Ia host step at a0.

What is recomputed HERE (closed-form, fast; the CLASS / CAMB / Monte-Carlo numbers are quoted from
the committed stage scripts, which were re-run for this sweep and whose exit codes are recorded):

  N1  a0 on both footings from the horizon formula (canonical rho_DE/cH_Lambda vs alt rho_total/cH0)
  N2  the derived a0(z) law  a0(z)/a0(0) = [sqrt(1+nu0^2)/sqrt(1+nu0^2 (1+z)^6)]^(1/2)  at the
      window floor/ceiling nu0 in [2.14e-5, 1.77e-4]; z_t = nu0^(-1/3) - 1; a0(z_*)/a0(0)
  N3  the RETIRED CPL-dressed law (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z)) at DESI DR2 (w0,wa)
      = (-0.75,-0.86) -- reproduced only to label the retired numbers (bump +6.1 % at z=0.5, 0.74 at z=3)
  N4  early-rotator BTFR: v(z)/v(0) = [a0(z)/a0(0)]^(1/4); first-detectable z against the committed
      0.06-dex floor (3.51 % in v); BOTH footings (ratio footing-independent, zero point moves by
      (a0_alt/a0_can)^(1/4))
  N5  Sigma_dagger = a0/(pi G) (a0-line own threshold) and Sigma_M = a0/(2 pi G) (the borrowed one, and
      the SN-Ia host-step surface-density scale) on BOTH footings
  N6  MUSE-DARK III raw slope tension for the derived law (= flat branch) and the drift-folded residual
  N7  MSA-3D genuine trend vs flat
  N8  DESI: the sector's non-dust remainder w(z) = -1/(1+nu^2) >= -1 always; |1+w| at z=2 (ceiling)
  N9  collapse-timing speedup from the a0-line r_ddot = -sqrt(gN^2 + a0(z) gN) at turnaround
      (stage 26 integral, re-run here in the same form) for M = 1e10 Msun at z = 6..25, canonical AND
      alt a0 (alt a0 is LARGER so y is smaller and the boost slightly larger -- the spread is printed)

Exit 0 = every internal identity/ordering check held.  Writes sweep3_numbers.json alongside.
"""
import json
import os
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import quad

mp.mp.dps = 30
FAIL = []
NCHK = [0]
OUT = {}


def check(cond, label):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}")
    if not ok:
        FAIL.append(label)
    return ok


C = mp.mpf("2.99792458e8")
G = mp.mpf("6.67430e-11")
MPC = mp.mpf("3.0856775814913673e22")
PC = MPC / 10 ** 6
MSUN = mp.mpf("1.98892e30")
KAPPA = mp.mpf("0.5")
OM_L, OM_M = mp.mpf("0.685"), mp.mpf("0.315")
H0 = mp.mpf("67.4") * 1000 / MPC
NU0_FLOOR, NU0_CEIL = mp.mpf("2.14e-5"), mp.mpf("1.77e-4")
Z_STAR = mp.mpf("1089.9")
W0, WA = mp.mpf("-0.75"), mp.mpf("-0.86")

print("=" * 96)
print("N1  a0 on both footings")
print("=" * 96)
rho_crit = 3 * H0 ** 2 / (8 * mp.pi * G)
a0_can = KAPPA * C * mp.sqrt(G * OM_L * rho_crit)          # rho_DE footing
a0_alt = KAPPA * C * mp.sqrt(G * rho_crit)                 # rho_total footing (= cH0 sqrt(3/32pi))
OUT["a0_canonical"] = float(a0_can)
OUT["a0_alt"] = float(a0_alt)
print(f"  a0 canonical = {mp.nstr(a0_can, 5)}   a0 alt = {mp.nstr(a0_alt, 5)}   ratio = {mp.nstr(a0_alt / a0_can, 5)}")
check(abs(a0_can / mp.mpf("9.3619e-11") - 1) < 1e-3, "N1a canonical a0 reproduces the committed 9.3619e-11 to <0.1 %")
check(abs(a0_alt / mp.mpf("1.1279e-10") - 1) < 5e-3, "N1b alt a0 reproduces the committed 1.1279e-10 to <0.5 %")
check(abs(a0_alt / a0_can - 1 / mp.sqrt(OM_L)) < 1e-12, "N1c alt/canonical = 1/sqrt(Omega_Lambda) identically")

print("\n" + "=" * 96)
print("N2  derived a0(z) law (stage 17), footing-independent ratio")
print("=" * 96)


def a0r(z, nu0):
    z = mp.mpf(z)
    nu = nu0 * (1 + z) ** 3
    return mp.sqrt(mp.sqrt(1 + nu0 ** 2) / mp.sqrt(1 + nu ** 2))


def a0r_cpl(z):
    z = mp.mpf(z)
    return (1 + z) ** (mp.mpf("1.5") * (1 + W0 + WA)) * mp.e ** (-mp.mpf("1.5") * WA * z / (1 + z))


zt_lo = NU0_CEIL ** (mp.mpf(-1) / 3) - 1
zt_hi = NU0_FLOOR ** (mp.mpf(-1) / 3) - 1
OUT["z_t"] = [float(zt_lo), float(zt_hi)]
tab = {}
print(f"  z_t in [{mp.nstr(zt_lo, 3)}, {mp.nstr(zt_hi, 3)}]")
print("     z     derived floor   derived ceil   retired CPL")
for z in (0.405, 0.5, 1, 2, 3, 5, 10, 15, 20, 25, 30, 1089.9):
    f, c, p = a0r(z, NU0_FLOOR), a0r(z, NU0_CEIL), a0r_cpl(z)
    tab[str(z)] = [float(f), float(c), float(p)]
    print(f"  {z:>7}      {mp.nstr(f, 5):>8}       {mp.nstr(c, 5):>8}      {mp.nstr(p, 5):>8}")
OUT["a0z_table_floor_ceil_cpl"] = tab
check(16 < zt_lo < 18 and 34 < zt_hi < 36, "N2a z_t bracket reproduces stage 17's [16.8, 35.0]")
check(abs(a0r(3, NU0_CEIL) - 1) < 1e-4 and abs(a0r(5, NU0_CEIL) - 1) < 1e-3, "N2b constant to <0.1 % at z=3 and <1 % at z=5 (ceiling)")
check(abs(a0r(Z_STAR, NU0_FLOOR) - mp.mpf("0.006")) < 3e-4 and abs(a0r(Z_STAR, NU0_CEIL) - mp.mpf("0.00209")) < 3e-5,
      "N2c a0(z_*)/a0(0) = 0.0060 (floor) / 0.00209 (ceiling), stage 19 D1")
check(abs(a0r_cpl(0.5) - mp.mpf("1.061")) < 2e-3 and abs(a0r_cpl(3) - mp.mpf("0.740")) < 2e-3 and abs(a0r_cpl(10) - mp.mpf("0.36")) < 5e-3,
      "N3  RETIRED CPL law reproduces the retired numbers (+6.1 % z=0.5; 0.74 z=3; 0.36 z=10) -- labelled RETIRED")

print("\n" + "=" * 96)
print("N4  early-rotator BTFR deficit (stage 25), both footings")
print("=" * 96)
floor_v = 10 ** (mp.mpf("0.06") / 4) - 1
vdef = {}
for z in (5, 10, 15, 17, 20, 25, 30):
    vdef[str(z)] = [float(1 - a0r(z, NU0_FLOOR) ** mp.mpf("0.25")), float(1 - a0r(z, NU0_CEIL) ** mp.mpf("0.25"))]
    print(f"  z={z:>3}: deficit floor {100 * vdef[str(z)][0]:.4f} %   ceiling {100 * vdef[str(z)][1]:.3f} %")
OUT["btfr_v_deficit_floor_ceil"] = vdef
OUT["btfr_floor_in_v_percent"] = float(100 * floor_v)
z_det = next(z for z in range(5, 45) if 1 - a0r(z, NU0_CEIL) ** mp.mpf("0.25") > floor_v)
OUT["btfr_first_detectable_z_ceiling"] = z_det
zp_shift = (a0_alt / a0_can) ** mp.mpf("0.25")
OUT["btfr_zero_point_alt_over_can_in_v"] = float(zp_shift)
check(abs(100 * floor_v - mp.mpf("3.51")) < 0.02, "N4a 0.06 dex floor = 3.51 % in velocity")
check(z_det == 17, "N4b first-detectable redshift z ~ 17 (ceiling), stage 25 D2")
check(abs(vdef["10"][1] - 0.00337) < 5e-5 and abs(vdef["20"][1] - 0.0783) < 5e-4, "N4c 0.337 % at z=10, 7.83 % at z=20 (ceiling)")
check(abs(zp_shift - mp.mpf("1.0477")) < 1e-3, "N4d alt footing moves the absolute BTFR zero point by 1.0477x in v; the ratio curve is footing-independent")

print("\n" + "=" * 96)
print("N5  surface-density scales, both footings")
print("=" * 96)
unit = MSUN / PC ** 2
sd = {}
for name, a0 in (("canonical", a0_can), ("alt", a0_alt)):
    sd[name] = {"Sigma_dagger_a0_over_piG": float(a0 / (mp.pi * G) / unit),
                "Sigma_M_a0_over_2piG": float(a0 / (2 * mp.pi * G) / unit)}
    print(f"  {name:>9}: Sigma_dagger = {sd[name]['Sigma_dagger_a0_over_piG']:.1f}   Sigma_M = {sd[name]['Sigma_M_a0_over_2piG']:.1f}  Msun/pc^2")
OUT["surface_density"] = sd
check(abs(sd["canonical"]["Sigma_dagger_a0_over_piG"] - 213.7) < 0.5, "N5a Sigma_dagger canonical = 213.7 Msun/pc^2 (stage 25 C2)")
check(abs(sd["canonical"]["Sigma_M_a0_over_2piG"] - 106.9) < 0.3, "N5b Sigma_M canonical = 106.9 (= the SN-Ia host-step '107' scale)")
check(abs(sd["alt"]["Sigma_dagger_a0_over_piG"] - 258.3) < 0.5, "N5c Sigma_dagger alt = 258.3 Msun/pc^2 (never previously quoted); Sigma_M alt = 129.1")

print("\n" + "=" * 96)
print("N6/N7  MUSE-DARK III + MSA-3D against the derived (flat) law")
print("=" * 96)
A1, A1E, DRIFT = mp.mpf("1.59"), mp.mpf("0.105"), mp.mpf("0.80")
slope_der = (a0r(1.44, NU0_CEIL) - a0r(0.5, NU0_CEIL)) / mp.mpf("0.94")
t_flat = A1 / A1E
res50 = (A1 - DRIFT) / mp.sqrt(A1E ** 2 + (mp.mpf("0.5") * DRIFT) ** 2)
res30 = (A1 - DRIFT) / mp.sqrt(A1E ** 2 + (mp.mpf("0.3") * DRIFT) ** 2)
t_msa = mp.mpf("0.91") / mp.mpf("0.79")
OUT["muse"] = {"derived_slope_1e-10_per_z": float(slope_der), "raw_sigma_flat": float(t_flat),
               "drift_folded_sigma_50pct": float(res50), "drift_folded_sigma_30pct": float(res30)}
OUT["msa3d_sigma_from_flat"] = float(t_msa)
print(f"  derived slope {mp.nstr(slope_der, 3)}; raw {mp.nstr(t_flat, 3)} sigma; drift-folded {mp.nstr(res50, 3)}-{mp.nstr(res30, 3)} sigma; MSA-3D {mp.nstr(t_msa, 3)} sigma")
check(abs(slope_der) < 1e-3 and abs(t_flat - mp.mpf("15.14")) < 0.05, "N6a derived law is the flat branch: raw MUSE tension 15.1 sigma")
check(1.9 < res50 < 1.92 and 3.0 < res30 < 3.05, "N6b drift-folded residual 1.9-3.0 sigma (stage 21 A3)")
check(1.1 < t_msa < 1.2, "N7  MSA-3D genuine trend 1.15 sigma from flat")

print("\n" + "=" * 96)
print("N8  DESI: the sector cannot go phantom")
print("=" * 96)
w_z2 = -1 / (1 + (NU0_CEIL * 27) ** 2)
OUT["one_plus_w_z2_ceiling"] = float(1 + w_z2)
ws = [float(-1 / (1 + nu ** 2)) for nu in (mp.mpf("0.01"), 1, 100)]
print(f"  |1+w|(z=2, ceiling) = {mp.nstr(1 + w_z2, 3)};  w_nd across the transition: {ws}")
check(all(w >= -1 for w in ws) and abs(1 + w_z2 - mp.mpf("2.3e-5")) < 3e-6, "N8  w_nd >= -1 always; |1+w| = 2.3e-5 at z=2 -- DESI phantom past unreachable")

print("\n" + "=" * 96)
print("N9  collapse-timing speedup (stage 26 integral), canonical vs alt a0")
print("=" * 96)
Gf, MSUNf, MPCf = 6.67430e-11, 1.98892e30, 3.0856775814913673e22
H0f = 67.4e3 / MPCf


def r200(M, z):
    rho_c = 3 * (H0f * np.sqrt(0.315 * (1 + z) ** 3 + 0.685)) ** 2 / (8 * np.pi * Gf)
    return (3 * M * MSUNf / (800 * np.pi * rho_c)) ** (1 / 3)


def t_coll(Mkg, rta, a0z, mond):
    def g(r):
        gN = Gf * Mkg / r ** 2
        return np.sqrt(gN ** 2 + a0z * gN) if mond else gN

    def integrand(x):
        r = x * rta
        d = quad(g, r, rta, limit=200)[0]
        return 0.0 if d <= 0 else rta / np.sqrt(2 * d)

    return quad(integrand, 1e-4, 1 - 1e-9, limit=200)[0]


sp = {}
for z in (6, 10, 15, 25):
    rta = 2 * r200(1e10, z)
    row = {}
    for name, a0 in (("canonical", float(a0_can)), ("alt", float(a0_alt))):
        a0z = a0 * float(a0r(z, NU0_CEIL))
        row[name] = t_coll(1e10 * MSUNf, rta, a0z, False) / t_coll(1e10 * MSUNf, rta, a0z, True)
    sp[str(z)] = row
    print(f"  z={z:>2}: speedup canonical {row['canonical']:.3f}x   alt {row['alt']:.3f}x")
OUT["collapse_speedup_1e10_ceiling"] = sp
check(abs(sp["6"]["canonical"] - 2.027) < 0.01 and abs(sp["25"]["canonical"] - 1.144) < 0.01, "N9a canonical reproduces stage 26 C1: 2.027x (z=6) -> 1.144x (z=25)")
check(all(sp[z]["alt"] > sp[z]["canonical"] for z in sp) and sp["6"]["alt"] < 2.2, "N9b alt a0 (larger) gives a slightly larger speedup at every z; spread < 10 %")
check(sp["6"]["canonical"] > sp["10"]["canonical"] > sp["15"]["canonical"] > sp["25"]["canonical"], "N9c the speedup declines monotonically with z (the signed, distinctive shape)")

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "sweep3_numbers.json"), "w") as fh:
    json.dump(OUT, fh, indent=1)
print("\n" + "=" * 96)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    for f in FAIL:
        print("  FAILED:", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
