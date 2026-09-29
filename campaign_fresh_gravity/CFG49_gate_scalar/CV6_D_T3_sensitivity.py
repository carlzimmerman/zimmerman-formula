#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CV6-D -- SENSITIVITY: the kernel-response cross term T3 (XR15's name) that DE12/DE13 neglect.

The gate energy is -B(y) W(chi), and B depends on the baryons' Newtonian field through y = g_N/a0.  Its mixed second variation couples the gas displacement to dchi:
    E2 contains  -B_y (dy/deps) W'(chi0) eps dchi,   B_y = a0^2 h(y)/(4 pi G)  (dB/dy for B = a0^2 q(y^2)/8piG, q' = nu - 1),  dy/drho = 4 pi G/(k a0) (k along g_N),
  so  kappa_3(k) = a0 h_MOND(y) W'(chi0) / (k h),  eps = h drho.
With chi slaved (m2 -> inf) and the gas eliminated, the worst sign gives base = a - 2 kappa_3 - B W'' + mu k^2, so the local stiffness needed is
    mu_req(r, k) = (B W'' + 2 kappa_3 - a)_+ / k^2 ,   largest at the layer's smallest wavenumber k_min = 2 pi/L (kappa_3 ~ 1/k while mu k^2 ~ k^2, so the requirement falls with k).
PRE-DECLARED  T3 [reported sensitivity, load-bearing for the claim 'T3 does not change the verdict']:  max over the 24 layers of
    R_T3 = max_r mu_req(k_min; with kappa_3) / max_r mu_req(k_min; without)  <= 1.10.
CONTROL (MUTATE=x30 multiplies kappa_3 by 30): R_T3 must exceed 1.10 (the check has teeth).
SCOPE: a frozen-background WKB estimate (the exact treatment is nonlocal in delta rho); T4 (B_rho rho W, the gas's own MOND self-gravity, Jeans) is not included, as in DE12/DE13.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv6_common as c

MUT = os.environ.get("MUTATE", "")
FAC = 30.0 if MUT == "x30" else 1.0
P = lambda *a: print(*a, flush=True)
P(__doc__.split("PRE-DECLARED")[0].strip())
if MUT: P("\n  *** MUTATE=x30: kappa_3 x 30 ***")
Rs = {}
for (z, Mb, f) in c.GAL:
    trf = c.layer_fine(z, Mb, f); co = c.layer_coeffs(trf)
    a0 = c.A0[f]; y = trf["y"]; hM = c.h_of(y)
    L = co["r"].max() - co["r"].min(); kmin = 2 * math.pi / L
    k3 = FAC * a0 * hM * co["W1"] / (kmin * co["h"])
    req0 = np.maximum(co["BW2"] - co["a"], 0.0) / kmin ** 2
    req1 = np.maximum(co["BW2"] + 2 * k3 - co["a"], 0.0) / kmin ** 2
    Rs[(z, Mb, f)] = req1.max() / req0.max()
    P(f"    z = {z:4.2f} M_b = {Mb:.0e} {f:9s}: L = {L / c.KPC:7.1f} kpc; max 2 kappa_3 / max B W'' = {2 * np.max(k3) / np.max(co['BW2']):.2e}; R_T3 = {Rs[(z, Mb, f)]:.4f}")
mx = max(Rs.values())
ok = mx <= 1.10
P(f"  [{'PASS' if ok else 'FAIL'}] T3 max over 24 layers of R_T3 = {mx:.4f} (threshold 1.10)")
if MUT == "x30": P("  (mutation: the check must FAIL)")
P(f"\n  load-bearing failures: {0 if ok else 1}")
sys.exit(0 if ok else 1)
