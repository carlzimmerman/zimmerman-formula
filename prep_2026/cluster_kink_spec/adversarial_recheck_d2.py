#!/usr/bin/env python3
"""
ADVERSARIAL RECHECK, Door 2 (cluster y_c kink spec) -- independent machinery.

Re-derives, with scipy quad/brentq (NOT the cumsum/interp grids of
kink_target_spec.py):
  (a) r_kink for the M500 = 5e14 Msun fiducial (both footings), by hand;
  (b) the BCG-only analytic r_kink (shows the gas is a ~1 kpc correction);
  (c) the universal kink amplitude (n=1, n=2) and the RAR slope break at y_c
      via independent maximization / analytic derivative;
  (d) Gemini's mock r_kink analytically (closed form, no grid at all);
  (e) an independent coarse Abel projection of the Sigma(R) deficit for the
      5e14 fiducial at 4 spot radii (checks the bipolar lobes + exterior zero);
  (f) the Tian+2020 confrontation: y_max of the banked CLASH RAR data vs y_c,
      and the signal vs the banked 0.059 dex scatter / 0.1-0.3 dex systematics.

All asserts compare against the numbers CLAIMED in kink_target_spec.py /
run_output.txt.  Exit 0 <=> the claims survive independent re-derivation.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
H0 = 70.0e3 / (KPC * 1e3)
RHO_C = 3 * H0**2 / (8 * np.pi * G)
Z_FW = np.sqrt(32 * np.pi / 3)
Y_C = Z_FW / 2
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10

nu = lambda y: np.sqrt(1 + 1 / y)

# ---------------- (a) r_kink for M500 = 5e14, independent quad/brentq --------
M500 = 5e14 * MSUN
r500 = (3 * M500 / (4 * np.pi * 500 * RHO_C)) ** (1 / 3)
M_bcg = 5.0e11 * (5e14 / 1e14) ** 0.4 * MSUN          # Kravtsov+18 scaling
a_H = (20.0 / 1.8153) * KPC                            # Re = 20 kpc
f_gas, beta, rc = 0.12, 0.65, 0.12 * r500

shape = lambda r: (1 + (r / rc) ** 2) ** (-1.5 * beta)
Mshape = lambda r: 4 * np.pi * quad(lambda x: shape(x) * x**2, 0, r,
                                    limit=200)[0]
gas_norm = f_gas * M500 / Mshape(r500)
M_gas = lambda r: gas_norm * Mshape(r)
M_bar = lambda r: M_bcg * (r / (r + a_H)) ** 2 + M_gas(r)
g_bar = lambda r: G * M_bar(r) / r**2

rk_can = brentq(lambda r: g_bar(r) - Y_C * A0_CAN, 0.5 * KPC, 200 * KPC) / KPC
rk_alt = brentq(lambda r: g_bar(r) - Y_C * A0_ALT, 0.5 * KPC, 200 * KPC) / KPC
fb = (M_bcg * ((rk_can * KPC) / (rk_can * KPC + a_H)) ** 2) / M_bar(rk_can * KPC)
print(f"(a) M500=5e14 fiducial:  r500 = {r500/KPC:.0f} kpc")
print(f"    r_kink canon = {rk_can:.2f} kpc  (claimed 11.2)")
print(f"    r_kink alt   = {rk_alt:.2f} kpc  (claimed  9.2)")
print(f"    BCG share of M_bar at r_kink = {fb:.2%}  (claimed 99.49%)")
assert abs(rk_can - 11.2) < 0.15 and abs(rk_alt - 9.2) < 0.15
assert fb > 0.99

# ---------------- (b) BCG-only closed form -----------------------------------
rk_bcg = (np.sqrt(G * M_bcg / (Y_C * A0_CAN)) - a_H) / KPC
print(f"(b) BCG-only analytic r_kink = sqrt(G M_bcg/(y_c a0)) - a = "
      f"{rk_bcg:.2f} kpc  -> gas moves it only {rk_can - rk_bcg:+.2f} kpc")
assert abs(rk_bcg - rk_can) < 1.0        # gas is a sub-kpc correction

# ---------------- (c) amplitude + slope break, independent ------------------
def dev_dex(y, n):
    t = (Y_C / y) ** n
    return np.log10(nu(y) / (1 + (nu(y) - 1) * t))
r1 = minimize_scalar(lambda y: -dev_dex(y, 1), bounds=(Y_C, 50), method="bounded")
r2 = minimize_scalar(lambda y: -dev_dex(y, 2), bounds=(Y_C, 50), method="bounded")
print(f"(c) peak deviation n=1: {-r1.fun:.4f} dex at y={r1.x:.2f} "
      f"(claimed 0.0170 @ 6.13); n=2: {-r2.fun:.4f} dex at y={r2.x:.2f} "
      f"(claimed 0.0260 @ 5.24)")
assert abs(-r1.fun - 0.0170) < 5e-4 and abs(r1.x - 6.13) < 0.05
assert abs(-r2.fun - 0.0260) < 5e-4 and abs(r2.x - 5.24) < 0.05
# slope below y_c (analytic): 1 - 1/(2(y+1)); above: numeric derivative
s_below = 1 - 1 / (2 * (Y_C + 1))
h = 1e-6
def slope_thr(y, n):
    f = lambda yy: np.log10(yy * (1 + (nu(yy) - 1) * (Y_C / yy) ** n))
    return (f(y + h) - f(y - h)) / (np.log10(y + h) - np.log10(y - h))
def slope_uncut(y):
    f = lambda yy: np.log10(yy * nu(yy))
    return (f(y + h) - f(y - h)) / (np.log10(y + h) - np.log10(y - h))
yA = Y_C * (1 + 1e-3)
d1 = slope_thr(yA, 1) - slope_uncut(yA)
d2 = slope_thr(yA, 2) - slope_uncut(yA)
print(f"    slope below y_c (analytic) = {s_below:.4f} (claimed 0.8715); "
      f"break n=1 = {d1:+.4f} (claimed -0.1376), n=2 = {d2:+.4f} (claimed -0.2749)")
assert abs(s_below - 0.8715) < 5e-4
assert abs(d1 + 0.1376) < 3e-3 and abs(d2 + 0.2749) < 3e-3

# ---------------- (d) Gemini mock, closed form -------------------------------
rk_gem = (np.sqrt(G * 1e14 * MSUN / (Y_C * 1.2e-10)) - 50 * KPC) / KPC
print(f"(d) Gemini mock analytic r_kink = {rk_gem:.1f} kpc (claimed 150.3; "
      f"his a0=1.2e-10 is NEITHER footing, and his nu is the standard-MOND")
print(f"    simple nu = 1/2+sqrt(1/4+1/y), not the framework nu = sqrt(1+1/y))")
assert abs(rk_gem - 150.3) < 1.0

# ---------------- (e) independent coarse Sigma(R) projection, 5e14 ----------
def g_obs_un(r):
    gb = g_bar(r); return gb * nu(gb / A0_CAN)
def g_obs_th(r):
    gb = g_bar(r); y = gb / A0_CAN
    return gb * (1 + (nu(y) - 1) * min(1.0, Y_C / y))
def rho_eff(r, gfun):
    hh = 1e-4 * r
    Mp = gfun(r + hh) * (r + hh) ** 2 / G
    Mm = gfun(r - hh) * (r - hh) ** 2 / G
    return (Mp - Mm) / (2 * hh) / (4 * np.pi * r**2)
def Sigma(R, gfun):
    # 2 int_R^rmax rho(r) r dr / sqrt(r^2 - R^2), u = sqrt(r^2-R^2)
    umax = np.sqrt((3000 * KPC) ** 2 - R**2)
    return 2 * quad(lambda u: rho_eff(np.sqrt(u**2 + R**2), gfun), 0, umax,
                    limit=400)[0]
print("(e) independent Sigma(R) deficit, 5e14 fiducial (claimed +2.83% peak, "
      "-2.07% lobe at 9.5 kpc, ~0 at 2*r_kink):")
spots = {1.0: None, 5.0: None, 9.5: None, 2 * rk_can: None}
for Rk in spots:
    R = Rk * KPC
    su, st = Sigma(R, g_obs_un), Sigma(R, g_obs_th)
    spots[Rk] = (su - st) / su
    print(f"      R = {Rk:6.1f} kpc : deficit = {spots[Rk]*100:+.2f}%")
assert 0.02 < spots[1.0] < 0.04                 # interior deficit lobe ~ +3%
assert -0.03 < spots[9.5] < -0.01               # excess lobe just inside kink
assert abs(spots[2 * rk_can]) < 0.002           # exterior: exact agreement
print(f"    p_req sanity: 11 bins at ~2% rms -> sqrt(sum f^2) ~ "
      f"{np.sqrt(11)*0.019*100:.1f}% (claimed 6.25%); p_req(3sig) ~ 2%/bin -- consistent")

# ---------------- (f) Tian+2020 confrontation --------------------------------
y_tian_max = 2.1e-10 / A0_CAN                   # banked lane2: max g_bar 2.1e-10
print(f"(f) Tian+2020 CLASH RAR: max g_bar = 2.1e-10 -> y_max = {y_tian_max:.2f}"
      f" < y_c = {Y_C:.2f}: existing cluster-RAR data NEVER REACHES the throttle")
print(f"    regime; innermost Tian radius 14 kpc >~ r_kink (8-23 kpc).")
print(f"    Signal 0.017-0.026 dex vs Tian scatter 0.059 dex ({0.059/0.026:.1f}-"
      f"{0.059/0.017:.1f}x below) and 0.1-0.3 dex systematics "
      f"({0.1/0.026:.1f}-{0.3/0.017:.0f}x below).")
assert y_tian_max < Y_C
print("\nALL D2 ADVERSARIAL RECHECKS PASS")
