#!/usr/bin/env python3
"""Trim of step3a1: completes [e] (p = 2, 8/3 + exact anchors) and runs [f] — the Born
kernel applied to the G profile (the kernel-side lock answer). [a]-[d] and the first
three C(p) rows are banked in the original step3a1 log."""
import mpmath as mp
import numpy as np
from agentHH_pump_profile import (born_drho, rho_c_bessel_closed, rho_c_coulomb_closed,
                                  F_gevrey3, fit_osc_model, CT)

cval = 2.0
print("[e-cont] the read coefficient C(p), remaining rows:")
for p in [mp.mpf(2), mp.mpf(8) / 3]:
    row = []
    for nu in [20.0, 50.0]:
        Fp = lambda s, pv=p: s ** (-pv)
        b = born_drho(nu, cval, Fp, S_max=1200, dps=50)
        Cv = -float(b) / (nu * (nu / cval) ** (-float(p)))
        row.append(f"nu={nu:.0f}: C = {Cv:+.5f}")
    print(f"     p = {mp.nstr(p, 4):>6}: " + "   ".join(row))
mp.mp.dps = 100
exC2 = -(rho_c_bessel_closed(200.0, mp.mpf('0.01'), mp.mpf(2)) - 200).real \
    / (200 * mp.mpf('0.01') * (mp.mpf(100)) ** -2)
exC1 = -(rho_c_coulomb_closed(200.0, mp.mpf('0.01'), mp.mpf(2)) - 200).real \
    / (200 * mp.mpf('0.01') * (mp.mpf(100)) ** -1)
print(f"     exact anchors at nu = 200, coupling 0.01: C(2) = {mp.nstr(exC2, 6)}, "
      f"C(1) = {mp.nstr(exC1, 6)}")

print("[f] Born kernel applied to the G profile (independent of the pipeline):")
ct = CT["fw"]
FG = F_gevrey3(-2.0, ct, mp.pi / 8, cval, w_lo=mp.mpf('0.1'), npow=6)
grid = [float((mp.mpf('1.6') + mp.mpf('0.2') * j) ** 3) for j in range(16)]
dB = []
for nu in grid:
    b = born_drho(nu, cval, FG, S_max=80, dps=50)
    dB.append(float(b))
    print(f"     nu = {nu:>7.3f}: Born Drho_c = {float(b):+.6e}")
s3 = float(mp.sqrt(3))
ftB = fit_osc_model(grid, dB, init=(-1.0 / 3, float(ct), s3 * float(ct), 1.0 / 3))
print(f"     Born-side fit: s = {ftB['s']:.5f}  al = {ftB['al']:.5f}  "
      f"be = {ftB['be']:.5f}  be/al = {ftB['be']/ftB['al']:.5f}  q = {ftB['q']:+.4f}  "
      f"amp = {ftB['amp']:.4f}  phi = {ftB['phi']:+.4f}  rms_w = {ftB['rms_w']:.2e}")
print(f"     targets:       s = 0.33333  al = {float(ct):.5f}  be = {s3*float(ct):.5f}  "
      f"be/al = {s3:.5f}; operator map: amp -> {float(2*ct/3):.4f}, "
      f"phi -> {float(mp.pi/8 - mp.pi/3 + mp.pi):+.4f}")
print("     => to be read against [3d]'s pipeline fit: agreement = the transcription")
print("        confirmed by two fully independent computations.")
