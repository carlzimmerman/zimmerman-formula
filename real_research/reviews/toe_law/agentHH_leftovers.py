#!/usr/bin/env python3
"""Leftover scan rows (trims of step3c/3c2/3c4 — the parts not already banked in logs):
[3c-X] filter bank, [3c-E] index-1 control, [3c2-b] band contour-invariance at nu = 50,
[3c4-b] w0 = 6 band tail (the a(w0)-scaling of the index-1/2 constant)."""
import mpmath as mp
import numpy as np
from agentHH_pump_profile import (F_bank, F_expw, F_logGauss, rho_c_pipeline2,
                                  solve_branch2, build_node_cache2, mellin_from_cache,
                                  fit_tail_laws, NUS_SCAN)

cval = 2.0
nus = NUS_SCAN + [50.0, 70.0, 97.0]

# ---- X: three-channel filter bank ----
banks = [(1.5, 0.3), (4.5, 0.18), (13.5, 0.108)]
FX = F_bank(banks, sig=0.5)
resX = rho_c_pipeline2(FX, cval, nus, dps=46)
print(f"[3c-X] filter bank {banks}, sig = 0.5 (log-spaced channels x3):")
for nu in nus:
    mp.mp.dps = 30
    d = (resX[nu] - nu).real
    pred = -nu / 2 * FX(mp.mpf(nu) / cval)
    print(f"     nu = {nu:>5}: Drho_c = {mp.nstr(d, 8):>15}  pred_naive = "
          f"{mp.nstr(pred, 8):>15}  ratio = {mp.nstr(d / pred, 6)}")
print("     => channel-wise transcription + the band-edge index-1/2 shed of each channel")
print("        (Born additivity, [3a-lin]); no nu^{1/3} oscillation, no lock. A bank can")
print("        only reach (C1) by TUNING its weights into the fingerprint itself.")

# ---- E: index-1 positive control ----
Fe = F_expw(0.3)
nuse = [4.0, 6.0, 9.0, 13.5, 20.0, 28.0]
rese = rho_c_pipeline2(Fe, cval, nuse, dps=46)
de = []
print("[3c-E] index-1 control F = 0.3 e^{-w} x turn-on (true exponential, decay 1/c):")
for nu in nuse:
    mp.mp.dps = 30
    d = (rese[nu] - nu).real
    de.append(d)
    pred = -nu / 2 * Fe(mp.mpf(nu) / cval)
    print(f"     nu = {nu:>5}: Drho_c = {mp.nstr(d, 8):>15}  pred_naive = "
          f"{mp.nstr(pred, 8):>15}  ratio = {mp.nstr(d / pred, 6)}")
laws = fit_tail_laws(nuse, de)
print(f"     pure-power resid {laws['power']['max_resid']:.3f}; +exp: "
      f"s=1/3: a = {laws['s=1/3']['a']:+.4f} resid {laws['s=1/3']['max_resid']:.3f} | "
      f"s=1/2: a = {laws['s=1/2']['a']:+.4f} resid {laws['s=1/2']['max_resid']:.3f} | "
      f"s=1: a = {laws['s=1']['a']:+.4f} resid {laws['s=1']['max_resid']:.2e}")
print(f"     => s = 1 wins, a vs transcription-pred 1/c = {1/cval:.4f} (+operator-map")
print("        subleading): the methodology DETECTS a true exponential and reads its index.")

# ---- [3c2-b] band contour-invariance at nu = 50 ----
FB1 = F_logGauss(0.3, 3.0, 0.5)
res1 = rho_c_pipeline2(FB1, cval, [50.0], dps=46)
d50 = float((res1[50.0] - 50.0).real)
old_dps = mp.mp.dps
mp.mp.dps = 46
try:
    br_alt = solve_branch2(FB1, cval, mp.mpf('0.003'), mp.mpf(50 * 2.2 / cval + 25),
                           s_a=9.0, T_rot=46.0, theta_rot=mp.pi / 4)
    A_, B_ = br_alt["A"], br_alt["B"]
    Wr = cval * (A_ * mp.conj(B_) - mp.conj(A_) * B_)
    cache_alt = build_node_cache2(br_alt, 50.0, deg=32)
    Pp = mellin_from_cache(br_alt, cache_alt, 50.0)
    bil = -2j * cval * (Pp * mp.conj(Pp)) / Wr
    altv = bil / (2 * mp.pi / cval ** 2)
finally:
    mp.mp.dps = old_dps
shift = abs(float((altv - 50.0).real) - d50)
print(f"[3c2-b] band contour-invariance at nu = 50: shift = {shift:.2e} vs signal "
      f"{abs(d50):.2e} -> {'PASS' if shift < 0.01 * abs(d50) else 'FAIL'}")
assert shift < 0.01 * abs(d50)
print("     => the index-1/2 beyond-band tail is contour-independent: a real response")
print("        feature (and first-order: [3c2-a] ratio 2.0026/2.0002; kernel ratio")
print("        0.9974/0.9998, [3c4-a]).")

# ---- [3c4-b] w0 = 6 band: the a(w0) scaling ----
FB6 = F_logGauss(0.3, 6.0, 0.5)
nus6 = [36.0, 50.0, 64.0, 80.0, 97.0]
res6 = rho_c_pipeline2(FB6, cval, nus6, dps=48)
dv6 = [float((res6[nu] - nu).real) for nu in nus6]
print("[3c4-b] w0 = 6 band beyond-band tail:")
for nu, d in zip(nus6, dv6):
    print(f"     nu = {nu:>5}: Drho_c = {d:+.6e}")
nus_f = np.array(nus6)
y = np.log(np.abs(np.array(dv6)))
A12 = np.column_stack([np.ones_like(nus_f), np.log(nus_f), -np.sqrt(nus_f)])
c12, *_ = np.linalg.lstsq(A12, y, rcond=None)
r12 = np.abs(y - A12 @ c12).max()
print(f"     index-1/2 fit: a(w0=6) = {c12[2]:+.4f} (w0=3 gave ~2.0), q = {c12[1]:+.3f}, "
      f"max ln-resid = {r12:.4f}")
print(f"     scaling diagnosis: a = sqrt(2 c w0)-like? pred {2.0 * float(np.sqrt(2.0)):.3f}; "
      f"w0-independent (a = sqrt(2c))? pred 2.0")
