#!/usr/bin/env python3
"""Keystone-only trim of step3d: [3d-0] free floor, [3d-1] forward run, [3d-2] contour
invariance, [3d-3] fits, + Born linearity. The [3d-4] hostile rows run as standalone
agentHH_3d4_row.py processes (same content, parallel)."""
import mpmath as mp
from agentHH_pump_profile import (F_gevrey3, rho_c_pipeline2, solve_branch2,
                                  build_node_cache2, mellin_from_cache, fit_osc_model, CT)

print("=" * 88)
print("[HH-3d] THE KEYSTONE — G class forward run = the Born-INVERSE profile pushed")
print("        through the exact pipeline: does the fingerprint transcribe?")
print("        (keystone trim: [3d-0..3] + linearity; [3d-4] rows run standalone)")
print("=" * 88)
cval = 2.0
third = mp.mpf(1) / 3
wcut = mp.mpf('0.001')
ct = CT["fw"]
phF = mp.pi / 8
FG = F_gevrey3(-2.0, ct, phF, cval, w_lo=mp.mpf('0.1'), npow=6)
grid = [float((mp.mpf('1.6') + mp.mpf('0.2') * j) ** 3) for j in range(16)]

resf = rho_c_pipeline2(lambda wv: mp.mpc(0), cval, [grid[0], grid[-1]],
                       w_cut=wcut, dps=50, deg=28)
fl0 = float(abs(resf[grid[0]] - grid[0]) / grid[0])
fl1 = float(abs(resf[grid[-1]] - grid[-1]) / grid[-1])
print(f"[3d-0] free floor at scan settings: nu = {grid[0]:.3f}: {fl0:.2e}; "
      f"nu = {grid[-1]:.3f}: {fl1:.2e}  -> {'PASS' if max(fl0, fl1) < 2e-12 else 'FAIL'}")
assert max(fl0, fl1) < 2e-12

res = rho_c_pipeline2(FG, cval, grid, w_cut=wcut, dps=50, deg=28)
dvals, preds = [], []
print(f"[3d-1] G profile: AF = -2, ct_F = ct_fw = {float(ct):.4f}, phF = pi/8, "
      f"qF = -4/3, w_lo = 0.1, npow = 6; transcription expectation (the OPERATOR map):")
print("        s = 1/3, al = ct, be/al = sqrt3; amp -> 2ct/3 = "
      f"{float(2 * ct / 3):.4f}, phi -> pi/8 - pi/3 + pi = "
      f"{float(mp.pi / 8 - mp.pi / 3 + mp.pi):.4f}, q -> 0 (naive-pred columns shown):")
for nu in grid:
    mp.mp.dps = 30
    d = float((res[nu] - nu).real)
    pred = float(-nu / 2 * FG(mp.mpf(nu) / cval))
    dvals.append(d)
    preds.append(pred)
    cosfac = float(mp.cos(mp.sqrt(3) * ct * mp.mpf(nu) ** third + phF))
    tag = f"ratio = {d/pred:9.5f}" if abs(cosfac) > 0.4 else "  (near node)"
    print(f"     nu = {nu:>7.3f}: Drho_c = {d:+.6e}  pred_naive = {pred:+.6e}  {tag}")

nuv = 64.0
old_dps = mp.mp.dps
mp.mp.dps = 50
try:
    br_alt = solve_branch2(FG, cval, mp.mpf('0.003'), mp.mpf(nuv * 2.2 / cval + 25),
                           s_a=9.0, T_rot=46.0, theta_rot=mp.pi / 4)
    A_, B_ = br_alt["A"], br_alt["B"]
    Wr = cval * (A_ * mp.conj(B_) - mp.conj(A_) * B_)
    cache_alt = build_node_cache2(br_alt, nuv, deg=32)
    Pp = mellin_from_cache(br_alt, cache_alt, nuv)
    bil = -2j * cval * (Pp * mp.conj(Pp)) / Wr
    altv = bil / (2 * mp.pi / cval ** 2)
finally:
    mp.mp.dps = old_dps
d64 = dvals[grid.index(64.0)]
shift = float(abs((altv - 64.0).real - d64))
print(f"[3d-2] contour-invariance at nu = 64: Drho shift = {shift:.2e} vs signal "
      f"{abs(d64):.2e} -> {'PASS' if shift < 0.01 * abs(d64) else 'FAIL'}")
assert shift < 0.01 * abs(d64)

import math
s3 = math.sqrt(3)
init = (-1.0 / 3, float(ct), s3 * float(ct), 1.0 / 3)
fitM = fit_osc_model(grid, dvals, init=init)
fitP = fit_osc_model(grid, preds, init=init)
print("[3d-3] free-(q, al, be, s) oscillatory VARPRO fits:")
for nm, ft in [("measured ", fitM), ("pred_naive", fitP)]:
    print(f"     {nm}: s = {ft['s']:.5f}  al = {ft['al']:.5f}  be = {ft['be']:.5f}  "
          f"be/al = {ft['be']/ft['al']:.5f}  q = {ft['q']:+.4f}  amp = {ft['amp']:.4f}  "
          f"phi = {ft['phi']:+.4f}  rms_w = {ft['rms_w']:.2e}")
print(f"     targets:   s = 1/3 = 0.33333  al = ct = {float(ct):.5f}  "
      f"be = sqrt3 ct = {s3*float(ct):.5f}  be/al = sqrt3 = {s3:.5f}")
dev_s = abs(fitM["s"] - 1.0 / 3)
dev_lock = abs(fitM["be"] / fitM["al"] - s3) / s3
dev_ct = abs(fitM["al"] - float(ct)) / float(ct)
gapMP = max(abs(fitM["s"] - fitP["s"]), abs(fitM["al"] - fitP["al"]) / fitP["al"],
            abs(fitM["be"] - fitP["be"]) / fitP["be"])
print(f"     |s - 1/3| = {dev_s:.4f}; lock dev = {dev_lock:.4f}; ct dev = {dev_ct:.4f}; "
      f"M-vs-P exponent gap = {gapMP:.4f}")
ok3 = dev_s < 0.02 and dev_lock < 0.03 and dev_ct < 0.03 and gapMP < 0.02
print(f"     gate (s to 0.02, lock to 3%, ct to 3%, M-vs-P to 0.02) -> "
      f"{'PASS' if ok3 else 'FAIL'}")
print(f"     operator-map check: amp = {fitM['amp']:.4f} vs 2ct/3 = {float(2*ct/3):.4f}; "
      f"phi = {fitM['phi']:+.4f} vs {float(mp.pi/8 - mp.pi/3 + mp.pi):+.4f}; "
      f"q = {fitM['q']:+.4f} vs ~0 (subleading-impurity drift expected)")

FG2 = F_gevrey3(-1.0, ct, phF, cval, w_lo=mp.mpf('0.1'), npow=6)
nl = [grid[1], grid[7], grid[12]]
r2 = rho_c_pipeline2(FG2, cval, nl, w_cut=wcut, dps=50, deg=28)
print("[3d-lin] Born linearity (AF -2 -> -1):", end="")
for nu in nl:
    rat = dvals[grid.index(nu)] / float((r2[nu] - nu).real)
    print(f"  nu={nu:.1f}: ratio = {rat:.6f}", end="")
print("   (2 = exact linearity)")
