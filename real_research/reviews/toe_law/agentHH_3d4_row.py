#!/usr/bin/env python3
"""Standalone [3d-4] hostile re-verification row (parallel insurance for step3d's serial
tail). Usage: agentHH_3d4_row.py {c3|wlo|canon|hostile|lin}"""
import sys
import mpmath as mp
from agentHH_pump_profile import (F_gevrey3, rho_c_pipeline2, fit_osc_model, CT)

tag = sys.argv[1]
cval = 2.0
ct = CT["fw"]
phF = mp.pi / 8
s3 = float(mp.sqrt(3))
grid10 = [float((mp.mpf('1.6') + mp.mpf('0.3') * j) ** 3) for j in range(10)]
wcut = mp.mpf('0.001')

if tag == "c3":
    F, cv, ctv = F_gevrey3(-2.0, ct, phF, 3.0, w_lo=mp.mpf('0.1'), npow=6), 3.0, float(ct)
elif tag == "wlo":
    F, cv, ctv = F_gevrey3(-2.0, ct, phF, cval, w_lo=mp.mpf('0.05'), npow=6), cval, float(ct)
elif tag == "canon":
    F, cv, ctv = F_gevrey3(-2.0, CT["canon"], phF, cval, w_lo=mp.mpf('0.1'), npow=6), cval, CT["canon"]
elif tag == "hostile":
    F, cv, ctv = F_gevrey3(-2.0, CT["hostile"], phF, cval, w_lo=mp.mpf('0.1'), npow=6), cval, CT["hostile"]
elif tag == "lin":
    # Born linearity: AF/2 on three points, to be ratioed against the [3d-1] values
    FG2 = F_gevrey3(-1.0, ct, phF, cval, w_lo=mp.mpf('0.1'), npow=6)
    nl = [5.832, 27.0, 64.0]
    r2 = rho_c_pipeline2(FG2, cval, nl, w_cut=wcut, dps=50, deg=28)
    for nu in nl:
        print(f"[3d4-lin] nu = {nu}: Drho(AF=-1) = {float((r2[nu]-nu).real):+.8e}")
    sys.exit(0)

rv = rho_c_pipeline2(F, cv, grid10, w_cut=wcut, dps=50, deg=28)
dv = [float((rv[nu] - nu).real) for nu in grid10]
for nu, d in zip(grid10, dv):
    print(f"[3d4-{tag}] nu = {nu:>7.3f}: Drho = {d:+.8e}")
ftv = fit_osc_model(grid10, dv, init=(-1.0 / 3, ctv, s3 * ctv, 1.0 / 3))
print(f"[3d4-{tag}] fit: s = {ftv['s']:.5f}  al = {ftv['al']:.5f} (target {ctv:.5f})  "
      f"be/al = {ftv['be']/ftv['al']:.5f} (target {s3:.5f})  q = {ftv['q']:+.4f}  "
      f"amp = {ftv['amp']:.4f}  phi = {ftv['phi']:+.4f}  rms_w = {ftv['rms_w']:.2e}")
