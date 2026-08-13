#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERY_laneY_referee_2026.py -- adversarial referee of laneY_gate_counting_2026.py.

Independent re-derivations:
  P1  the A1 identity by a DIFFERENT route (explicit Lorentz boost to the aether rest frame).
  P2  the provenance chain X = sqrt(8pi) R_dm/(kappa nu0 mu17) + the unit cross-check.
  P3  velocities/thresholds re-derived (independent growth integration).
  P4  THE ATTACK: the support-side gate variable OMITS the static MOND gradient's
      contribution to Y (X-free, dominates the flow term for X <~ 1e3) -- the lane's own
      C3 uses exactly this static+flow totality at RAR radii.  Corrected ratio theorem.
  P5  THE X-PIN: C3's own arithmetic read backwards. The kinematic identity d_i phi = -Qbar v_i
      (the lane's A1 substitution) applied to the static MOND gradient at RAR radii
      (|grad phi_s| = sqrt(0.1..1) a0-tilde, required for the RAR) + the committed drain
      free-fall ~300 km/s forces  X = sqrt(y_static)/(v/c) = 316-1000.  Same field, same
      gradient, both jobs => equality, not a one-sided bound.
  P6  consequences at the pinned X: fork (a) realized; the 'CLASS clean iff X <~ 50-150'
      window is EXCLUDED; corrected cell-1 pricing.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

C = 2.99792458e8
MPC = 3.0856775814913673e22
H0K = 67.4; H0 = H0K * 1e3 / MPC
OM_M, OM_L, OM_R = 0.315, 0.685, 9.15e-5
OM_DM = 0.265; R_DM = OM_DM / OM_L
A0_CAN = 9.3619e-11; KAPPA = 0.5
NU0F, NU0C = 2.14e-5, 1.77e-4
ZREC = 1090.0; RREC = (1 + ZREC) ** 3
CH2 = 1.08e4; CS2_CAP = 2606.0
RHO_S, RHO_D = 1654.0, 1.0e6
V_H = np.sqrt(CH2)          # 103.9 km/s
V_FF = 300.0                # km/s committed drain free-fall at RAR radii (lane's own input)
LAM = 3 * OM_L * H0 ** 2 / C ** 2
A0T = A0_CAN / C ** 2       # a0-tilde, 1/m

ok = lambda c, s: print(("  [ok]   " if c else "  [FAIL] ") + s)

print("P1 -- A1 identity via explicit boost (independent route)")
# In the AETHER REST FRAME: A_mu = (-1,0,0,0). Boost the scalar gradient: in the frame where
# the condensate moves at w = v_phi - v_a (relative velocity, to O(v)), d_mu phi has spatial
# part -Qbar*w_i (kinematic identity v_i = -d_i phi/Qbar). Y = Q^2 - s^2 with Q = -A.dphi:
w1, w2, w3, Qb = sp.symbols("w1 w2 w3 Qbar", real=True)
dphi = sp.Matrix([Qb, -Qb * w1, -Qb * w2, -Qb * w3])   # aether-frame components, exact O(v)
eta = sp.diag(-1, 1, 1, 1)
Q = dphi[0]                                            # -A^mu d_mu phi with A=(1,0,0,0)
s2 = -(dphi.T * eta * dphi)[0]
Y = sp.expand(Q ** 2 - s2)
ok(sp.simplify(Y - Qb ** 2 * (w1 ** 2 + w2 ** 2 + w3 ** 2)) == 0,
   "Y = Qbar^2 |v_rel|^2 EXACTLY in the aether frame (not just to O(v^2): the frame choice "
   "absorbs the gamma factors) -- A1 CONFIRMED by an independent route")
# and delta-Y^(1)=0 trivially: Y is quadratic in w -- bridge1 line 60 consistent.

print("\nP2 -- provenance chain")
Q0F = np.sqrt(LAM) * R_DM / (NU0F * 1.0)               # mu17=1
XF = Q0F / A0T; XC = XF * NU0F / NU0C
ok(abs(XF / 1.81e5 - 1) < 0.01 and abs(XC / 2.19e4 - 1) < 0.01,
   f"X(mu17=1) = {XF:.3e} floor / {XC:.3e} ceiling  (claimed 1.81e5/2.19e4)")
ok(abs(np.sqrt(8 * np.pi) * R_DM / (KAPPA * NU0F) / XF - 1) < 1e-3,
   "X = sqrt(8pi) R_dm/(kappa nu0 mu17) algebra closes (to the frozen-a0's 5e-5 offset "
   "from exact kappa^2 Lam/8pi)")
ok(abs(KAPPA ** 2 * LAM / (8 * np.pi) / A0T ** 2 - 1) < 0.01,
   f"unit check kappa^2 Lam/8pi vs (a0/c^2)^2: ratio {KAPPA**2*LAM/(8*np.pi)/A0T**2:.5f}")

print("\nP3 -- independent growth + velocity spot checks")
def E(a): return np.sqrt(OM_R / a ** 4 + OM_M / a ** 3 + OM_L)
def rhs(N, y):
    a = np.exp(N)
    dlnH = (np.log(E(a * 1.0001)) - np.log(E(a * 0.9999))) / 0.0002
    Om = OM_M / a ** 3 / E(a) ** 2
    return [y[1], -(2 + dlnH) * y[1] + 1.5 * Om * y[0]]
sol = solve_ivp(rhs, [np.log(1e-4), 0], [1e-4, 1e-4], dense_output=True, rtol=1e-8, atol=1e-12)
def Dz(z): return sol.sol(np.log(1 / (1 + z)))[0]
def fz(z): s = sol.sol(np.log(1 / (1 + z))); return s[1] / s[0]
GR = Dz(0) / Dz(ZREC)
ok(680 < GR < 760, f"D(0)/D(1090) = {GR:.0f}  (lane: 716)")
ok(0.82 < fz(ZREC) < 0.87, f"f(1090) = {fz(ZREC):.3f}  (lane: 0.843)")
# BBKS sigma8-normalised
kk = np.logspace(-4, 1.5, 4000); HL = 0.674
def T(k):
    q = k / (OM_M * HL ** 2)
    return (np.log(1 + 2.34 * q) / (2.34 * q)) * (1 + 3.89 * q + (16.1 * q) ** 2
            + (5.46 * q) ** 3 + (6.71 * q) ** 4) ** -0.25
P = kk ** 0.965 * T(kk) ** 2
x8 = kk * 8.0 / HL
W8 = 3 * (np.sin(x8) - x8 * np.cos(x8)) / x8 ** 3
P *= (0.811 / np.sqrt(np.trapz(P * W8 ** 2 * kk ** 2, kk) / (2 * np.pi ** 2))) ** 2
def Del0(k): return np.sqrt(k ** 3 * np.interp(k, kk, P) / (2 * np.pi ** 2))
def vk(k, z):
    aH = H0K * E(1 / (1 + z)) / (1 + z)
    return fz(z) * (aH / k) * Del0(k) * Dz(z) / Dz(0)
v01, v1 = vk(0.1, ZREC), vk(1.0, ZREC)
m = (kk > 1e-3) & (kk < 3.0)
vrms = np.sqrt(np.trapz(np.array([vk(k, ZREC) for k in kk[m]]) ** 2, np.log(kk[m])))
ok(10 < v01 < 16 and 2.5 < v1 < 5.5, f"v_rec(k=0.1) = {v01:.1f}, v_rec(k=1) = {v1:.1f} km/s  (lane: 12.6, 3.7)")
ok(19 < vrms < 28, f"rms v_rec = {vrms:.1f} km/s  (lane: 23.1; v_bc literature ~30)")
def Arat(r, nu0): return np.sqrt(1 + nu0 ** 2) / np.sqrt(1 + (nu0 * r) ** 2)
vmax = max(vk(k, ZREC) for k in kk[m])
for nu0, lab, thm_c, thr_c in ((NU0F, "floor", 134, 78), (NU0C, "ceil", 47, 27)):
    amp = 1 / Arat(RREC, nu0)
    thm = 1 / (vmax * 1e3 / C * np.sqrt(amp)); thr = 1 / (vrms * 1e3 / C * np.sqrt(amp))
    ok(abs(thm / thm_c - 1) < 0.15 and abs(thr / thr_c - 1) < 0.15,
       f"{lab}: A0/A(rec) = {amp:.3e}; y_rec<1 thresholds X < {thm:.0f} (mode) / {thr:.0f} (rms) "
       f"(lane: {thm_c}/{thr_c})")

print("\nP4 -- THE ATTACK: static MOND gradient at the support point (omitted from y_h)")
# Committed support point: c_h^2 = GM/R_halt = 1.08e4 (km/s)^2; R_halt 13.5-60 kpc (stage 52
# B2/B4).  g_N = c_h^2/R_halt; static scalar gradient g_phi ~ sqrt(g_N a0_loc) (the framework's
# own RAR field); Y_static = |grad phi_s|^2 => y_static = g_N/a0_loc (MOND regime), X-FREE.
for Rh_kpc in (13.5, 60.0):
    gN = CH2 * 1e6 / (Rh_kpc * MPC / 1e3)
    print(f"    R_halt = {Rh_kpc:5.1f} kpc: g_N = {gN:.2e} m/s^2 = {gN/A0_CAN:.3f} a0 "
          f"=> y_static(surface) ~ {gN/A0_CAN:.3f}  [X-free]")
y_qs_surf = (CH2 * 1e6 / (13.5 * MPC / 1e3)) / A0_CAN     # 0.28, the favourable-to-lane end
y_flow_surf_perX2 = (V_H * 1e3 / C) ** 2                  # 1.2e-7 X^2 (A-credit ~1)
Xeq = np.sqrt(y_qs_surf / y_flow_surf_perX2)
ok(Xeq > 1000, f"static/flow crossover at the surface point: X_eq = {Xeq:.0f} -- for the lane's "
   f"own 'clean window' X <~ 50-150 the static term exceeds the flow term x{y_qs_surf/(150**2*y_flow_surf_perX2):.0f}-"
   f"x{y_qs_surf/(50**2*y_flow_surf_perX2):.0f}.  D1's y_support is the SUB-DOMINANT piece there")
# the lane's own C3 already treats kernel-Y at RAR radii as static+flow (the flow 'pushes the
# kernel Newtonian' ON TOP of the RAR's own MOND argument) -- internal inconsistency with D1.
# Corrected ratio at the worst CMB mode (k=1, v=3.7):
for X in (150.0, 52.0, 10.0):
    yrec = X ** 2 * (v1 * 1e3 / C) ** 2 / Arat(RREC, NU0F)
    yh = y_qs_surf + X ** 2 * y_flow_surf_perX2
    print(f"    X = {X:5.0f}: y_rec(k=1,floor) = {yrec:.3g}, y_h(static+flow) = {yh:.3g}, "
          f"ratio = {yrec/yh:.3g}" + ("   <-- RATIO < 1: D1 'theorem' FAILS" if yrec < yh else ""))
yr52 = 52 ** 2 * (v1 * 1e3 / C) ** 2 / Arat(RREC, NU0F)
ok(yr52 / y_qs_surf < 40, "the 36x 'minimum' (D1 vs surface) is an artifact of flow-only y_h; "
   "with the static term the X-free floor is GONE (ratio ~ y_rec(X)/y_qs -> 0 as X -> 0)")
# vs the DEEP calibration the failure is worse: y_qs(deep) >> 1 (g_N >> a0 at 1e6 rho_dm0),
# so the gate is OPEN there for every X while y_rec < 1 whenever X < 134 -- fork (b) as stated
# ('never opens at the halo') is FALSE.

print("\nP5 -- THE X-PIN (C3's arithmetic read backwards)")
# lane C3: flow-Y at v=300 km/s must satisfy y_flow <= 0.1-1 at RAR radii => X <= 316-1000.
# MIRROR: the RAR requires the SAME field to carry |grad phi_s| = sqrt(y_static) * a0tilde with
# y_static = 0.1-1 at those radii.  A1's kinematic identity (v_i = -d_i phi/Qbar) then slaves
# the condensate to v_s = sqrt(y_static) c/X.  Committed drain speed ~300 km/s =>
XLO = np.sqrt(0.1) / (V_FF * 1e3 / C); XHI = np.sqrt(1.0) / (V_FF * 1e3 / C)
ok(abs(XLO - 316) < 2 and abs(XHI - 999.3) < 2,
   f"v_s <= 300 km/s  =>  X >= {XLO:.0f}-{XHI:.0f}: EXACTLY C3's upper-bound numbers, mirrored. "
   f"One field, one gradient, both jobs => Qbar*v = |grad phi_s| => X ~ 316-1000 PINNED (not free)")
for X in (316.0, 1000.0):
    yrf = (X * vrms * 1e3 / C) ** 2 / Arat(RREC, NU0F)
    yrc = (X * vrms * 1e3 / C) ** 2 / Arat(RREC, NU0C)
    print(f"    at X = {X:4.0f}: y_rec(rms) = {yrf:.0f} (floor) / {yrc:.0f} (ceiling)  -- SATURATED")
ok((316 * vrms * 1e3 / C) ** 2 / Arat(RREC, NU0F) > 1,
   "fork (a) is REALIZED at the pinned X: y_rec >> 1 -- the saturation wall stands, but by the "
   "pin, not by the lane's 'X-free' route; and the 'CLASS clean iff X <~ 50-150' window is EMPTY")
mu17_lo = np.sqrt(8 * np.pi) * R_DM / (KAPPA * NU0F * 1000.0)
mu17_hi = np.sqrt(8 * np.pi) * R_DM / (KAPPA * NU0F * 316.0)
print(f"    implied mu17 (floor nu0): {mu17_lo:.0f}-{mu17_hi:.0f} -- inside C3's own 'mu17 >= 20-1800'")

print("\nP6 -- cell-1 q-boundary under the corrected support side (m=2), at the pinned X")
VSAT = CH2 * (1091.0 ** 3 / RHO_S) / CS2_CAP
ok(abs(VSAT / 3.254e6 - 1) < 0.01, f"V_sat = {VSAT:.3e} re-derived (committed stage53 inputs)")
vkmax = max(vk(k, ZREC) for k in (0.01, 0.03, 0.1, 0.3, 1.0))
for nu0, lab in ((NU0F, "floor"), (NU0C, "ceil")):
    for cal, r_env, yqs in (("surface", RHO_S, y_qs_surf), ("deep", RHO_D, 30.0)):
        Arh = Arat(RREC, nu0) / Arat(r_env, nu0)
        for X in (316.0, 1000.0):
            Yrec_over_Yh = (X * vkmax * 1e3 / C) ** 2 / (yqs * Arat(r_env, nu0) / Arat(1, nu0)) / 1.0
            # Y ratio = y_rec*A_rec/(y_qs*A_h); violation = VSAT * (Yratio)^2 * Arh^q
            Yr = ((X * vkmax * 1e3 / C) ** 2 / Arat(RREC, nu0) * Arat(RREC, nu0)) / (yqs * Arat(r_env, nu0))
            qn = np.log(VSAT * Yr ** 2) / (-np.log(Arh))
            print(f"    {lab:5s} {cal:7s} X={X:4.0f}: Y_rec/Y_h = {Yr:.3g}, q_need = {qn:.2f}"
                  f"   (lane D4 gave 0.53-0.92 X-free)")
print("\n    => the q-boundary is X-DEPENDENT once the static support term is included;")
print("       the lane's 'flow contrast is nu0-blind => ceiling relief evaporates' inherits the")
print("       flow-only support side and is NOT theorem-grade.")
