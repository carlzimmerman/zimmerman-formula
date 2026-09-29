#!/usr/bin/env python3
"""YM1 -- POST-HOC descriptive table (not pre-registered, asserts nothing): Yang-Mills instanton actions S_i = 2 pi / alpha_i (= 8 pi^2 / g_i^2)
of the three SM gauge couplings at the Planck / reduced-Planck scale (lane Y1's validated running, read-only), next to Z^2 = 32 pi/3 and 32 pi^2.
Run: python3 ym1_instanton_peek.py
"""
import sys, os, math
sys.dont_write_bytecode = True
H = os.path.dirname(os.path.abspath(__file__))
for s in ("Y1_running_precision", "B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(H, "..", s))
import y1_lib as L
tr = L.run_central(mu_max=1e21)
Z2 = 32 * math.pi / 3
REL = {"Y": 0.0023, "2": 0.00021, "3": 0.0012}
print(f"Z^2 = 32pi/3 = {Z2:.4f};  32 pi^2 = {32 * math.pi ** 2:.3f};  4 Z^2 = {4 * Z2:.3f}")
for name, mu in (("M_P", 1.22089e19), ("M_red", 2.435e18)):
    aY, a2, a3 = tr.A(mu)
    print(f"\nscale {name} = {mu:.5e} GeV   (1/alpha_i = A(mu); Y1 relative errors 0.23% / 0.021% / 0.12%)")
    for lab, v in (("Y", aY), ("2", a2), ("3", a3), ("1_GUT(=0.6 Y)", 0.6 * aY)):
        key = lab if lab in REL else "Y"
        print(f"  {lab:14s} 1/alpha = {v:9.4f}   S=2pi/alpha = {2 * math.pi * v:8.3f}   (1/alpha)/Z^2 = {v / Z2:.4f}   S/32pi^2 = {2 * math.pi * v / (32 * math.pi ** 2):.4f}   1sigma = {REL[key] * v:.3f}")
print("\nReading: none of the S_i equals 32 pi^2 or a simple multiple within its error; 1/alpha_1(GUT) sits 1.1% (~5 sigma at M_P) from Z^2.  No claim is made; the zero-knob grammar")
print("1/alpha_i = c * pi^r Z^p kappa^q (lanes A1/A2) already contains these forms and found 0 hits.  alpha stays an INPUT; kappa = 1/2 FITTED.")
