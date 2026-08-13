#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERC3_numbers.py -- independent recomputation of Lane C3 deliverables 2-4 (magnitude,
two-ended test, transport ceiling), built from scratch (own constants, own formula
derivations checked by hand), plus a quantitative rec-end drain estimate the lane
only made structurally (E4).

Derivations being re-checked (done by hand before coding):
  D2 ceiling: eps_J = [c^4/(16 pi G)] * 2(2-K_B) * (g/c^2)(g_phi/c^2) = (2-K_B) g g_phi/(8 pi G);
     |J| <= g_obs; P_req ~ rho g_obs R => ratio = (2-K_B) g_phi/(8 pi G rho R) and
     8 pi G rho R = 6 g_N for mean enclosed density  => ratio = (2-K_B) g_phi/(6 g_N).
  D3: ratio = 1 in deep MOND (g_phi ~ sqrt(gN a0)) => g_N* = (2-K_B)^2 a0/36.
  E2: g_lin = (4pi/3) G rho_m0 (1+z)^2 delta R_com  (physical peculiar field, exact for
     a tophat; delta_rec = sigma_0(R)/growth).
  F1: v = (2-K_B) g omega_Q/(8 pi G rho) [lane's normalization; my own shift-current
     derivation gives an extra factor 2 from rho = Q0 F_Q/(8 pi Gt) vs n = F_Q/(16 pi Gt) --
     flagged, immaterial inside the 4460x Q0 window]; rate = v/R vs 1/t_dyn.
  NEW: the SAME transport formula at the recombination end (rho = rho_dust(z_rec),
     g = g_lin, R = R_com/(1+z)) vs the Hubble rate H(z_rec) -- quantifying E4's
     'separation supplied by nonlinearity'.
"""
import numpy as np

FAIL = []
def check(cond, label):
    print(f"  [{'ok' if cond else 'FAIL'}] {label}")
    if not cond:
        FAIL.append(label)

G, C = 6.6743e-11, 2.99792458e8
MSUN, KPC = 1.989e30, 3.0857e19
MPC = 1e3 * KPC
H0 = 67.4e3 / MPC
rho_crit = 3 * H0**2 / (8 * np.pi * G)
rho_dm0, rho_m0 = 0.265 * rho_crit, 0.315 * rho_crit
A0C, A0A = 9.3619e-11, 1.1279e-10
NU_LO, NU_HI = 2.14e-5, 1.77e-4
M = 2.51e12 * MSUN

def a0_local(a0, over, nu0):
    Ar = np.sqrt(1 + nu0**2) / np.sqrt(1 + (nu0 * over)**2)   # committed stage53 law (A ratio)
    return a0 * np.sqrt(Ar)                                    # a0 ~ sqrt(A)

def gline(gn, a0): return np.sqrt(gn * gn + gn * a0)
def gms08(gn, a0):
    y = gn / a0
    return gn / (1 - np.exp(-np.sqrt(y)))

# ---- D1 ----
rho_h = 1654 * rho_dm0
R = (3 * M / (4 * np.pi * rho_h))**(1 / 3)
gN = G * M / R**2
check(abs(R / KPC - 221.4) < 1.5 and abs(gN - 7.14e-12) / 7.14e-12 < 0.01,
      f"D1  R = {R/KPC:.1f} kpc, g_N = {gN:.3e} = {gN/A0C:.4f} a0_can  [lane: 221.4 / 7.14e-12]")

# ---- D2 table, min/max ----
def ratio(over, a0f, kern, kb, nu0=None):
    rho = over * rho_dm0
    R_ = (3 * M / (4 * np.pi * rho))**(1 / 3)
    gn = G * M / R_**2
    a0 = a0_local(a0f, over, nu0) if nu0 else a0f
    gphi = kern(gn, a0) - gn
    return (2 - kb) * gphi / (6 * gn)

surf = [ratio(1654, a, k, kb) for a in (A0C, A0A) for k in (gline, gms08) for kb in (0.10, 0.25)]
i1e4 = [ratio(1e4, a, k, kb, NU_HI) for a in (A0C, A0A) for k in (gline, gms08) for kb in (0.10, 0.25)]
dflr = [ratio(1e6, a, k, kb, NU_LO) for a in (A0C, A0A) for k in (gline, gms08) for kb in (0.10, 0.25)]
dcei = [ratio(1e6, a, k, kb, NU_HI) for a in (A0C, A0A) for k in (gline, gms08) for kb in (0.10, 0.25)]
print(f"      surface: {min(surf):.4f}-{max(surf):.4f}   1e4: {min(i1e4):.4f}-{max(i1e4):.4f}   "
      f"1e6 floor: {min(dflr):.4f}-{max(dflr):.4f}   1e6 ceil: {min(dcei):.6f}-{max(dcei):.6f}")
check(abs(min(surf) - 0.804) < 0.01 and abs(max(surf) - 1.107) < 0.01,
      "D2a surface ceiling 0.80-1.11 REPRODUCED (O(1), not a kill there)")
check(abs(1 / max(dflr) - 133) < 5 and 1 / min(dcei) > 7e3,
      f"D2b deep shortfall {1/max(dflr):.0f}x (floor) to {1/min(dcei):.0f}x (ceiling) "
      f"[lane: 133x-1e4x] -- REPRODUCED")
mono = [ratio(o, A0C, gline, 0.10, NU_HI) for o in (1654, 1e4, 1e5, 1e6)]
check(all(mono[i] > mono[i + 1] for i in range(3)),
      f"D2c ratio FALLS inward monotonically: {['%.4f' % m for m in mono]} (1654->1e6) -- "
      f"inner shells never supported, lane's onion argument holds")

# ---- D3 ----
halts = {}
for lab, a0 in (("can", A0C), ("alt", A0A)):
    for kb in (0.10, 0.25):
        gs = (2 - kb)**2 * a0 / 36
        halts[(lab, kb)] = np.sqrt(G * M / gs) / KPC
vals = sorted(halts.values())
print(f"      R_halt values: {[f'{v:.0f}' for v in vals]} kpc")
check(abs(vals[0] - 176) < 2 and abs(vals[-1] - 210) < 2,
      f"D3  R_halt spans {vals[0]:.0f}-{vals[-1]:.0f} kpc: the REPORT'S '176-226 kpc' upper "
      f"edge is WRONG (should be 210; its own table prints 193/210/176/191) -- minor, "
      f"conclusion (~200-kpc fringe core, KiDS-charged class) unchanged")
check((2 - 0.10)**2 / 36 < 8.2 / 60,
      "D3a g_* ~ 0.085-0.100 a0, ~80x below the brief's g_* <= 8.2 a0 bound [brief-anchored, "
      "NOT verifiable in-repo -- provenance correctly marked 'unowned' by the lane]")

# ---- E2 / E3 ----
z = 1090.0
g_at = lambda Rc_m, sig: (4 * np.pi / 3) * G * rho_m0 * (1 + z)**2 * (sig / 850.0) * Rc_m
gl = [g_at(11.87 * MPC, 0.80), g_at(30 * MPC, 0.35), g_at(100 * MPC, 0.06)]
print(f"      g_lin(rec): {[f'{g:.2e}' for g in gl]}  = {[f'{g/A0C:.2f}' for g in gl]} a0")
check(abs(gl[0] / 3.08e-10 - 1) < 0.02 and gl[0] / gN > 40,
      f"E2/E3 g_lin(rec, 8 h^-1 Mpc) = {gl[0]:.2e} = {gl[0]/gN:.0f}x halo-surface g_N -- "
      f"two-ended INVERSION in g REPRODUCED (recorded against interest by the lane: honest)")

# ---- F1 ----
rho_tb = rho_h * 0.315 / 0.265
t_dyn = 1 / np.sqrt(G * rho_tb)
gobs = gline(gN, A0C)
drain = lambda omQ: (2 - 0.10) * gobs * omQ / (8 * np.pi * G * rho_h * C) * C / R
r_h, r_m = drain(H0) * t_dyn, drain(C / MPC) * t_dyn
print(f"      t_dyn = {t_dyn/3.156e16:.2f} Gyr; drain/binding: Hubble {r_h:.2f}x, mu-pin {r_m:.0f}x")
check(abs(r_h - 0.15) < 0.02 and abs(r_m - 671) < 15,
      "F1  drain ceiling 0.15x-671x REPRODUCED.  NOTE: my own shift-current normalization "
      "(n = F_Q/16piGt, rho = Q0 F_Q/8piGt) gives 2x the lane's v_eff -- an O(2) convention "
      "ambiguity, immaterial inside the 4460x unpinned-Q0 window, but the pre-stated kill "
      "threshold '0.3x at mu-pinned Q0' inherits it (mu-pinned value is >>0.3x either way)")

# ---- NEW: the rec-end transport drain, quantified (E4 made only structurally) ----
rho_dust_rec = rho_dm0 * (1 + z)**3
R_phys_rec = 11.87 * MPC / (1 + z)
H_rec = H0 * np.sqrt(0.315 * (1 + z)**3 + 9.2e-5 * (1 + z)**4 + 0.685)
v_rec = (2 - 0.10) * gl[0] * (C / MPC) / (8 * np.pi * G * rho_dust_rec * C)   # mu-pinned ceiling
rate_rec = v_rec * C / R_phys_rec
halo_rate = drain(C / MPC)
sep = (halo_rate * t_dyn) / (rate_rec / H_rec)
print(f"      rec end (mu-pinned ceiling): drain rate = {rate_rec:.2e}/s vs H(rec) = {H_rec:.2e}/s "
      f"=> {rate_rec/H_rec:.1e} of Hubble; halo end {r_m:.0f}x binding => separation ~ {sep:.1e}")
check(rate_rec / H_rec < 1e-3 and sep > 1e5,
      f"E4+ QUANTIFIED: at the SAME mu-pinned Q0 the rec-end fractional drain is "
      f"{rate_rec/H_rec:.1e} of the Hubble rate while the halo end is {r_m:.0f}x binding -- "
      f"{sep:.0e} separation.  The lane's '3-5 orders' is CONSERVATIVE (understated); the "
      f"structural pass of the binding-epoch wall is REAL on this arithmetic")

print()
if FAIL:
    print("FAILED:", *FAIL, sep="\n  - ")
    raise SystemExit(1)
print("VERC3_numbers: ALL CHECKS PASSED")
