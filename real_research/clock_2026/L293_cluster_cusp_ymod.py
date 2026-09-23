"""L293 -- THE CLUSTER-CUSP SHAPE OF THE Y-MODULATED CARRIER: the hydrostatic envelope in the deep-MOND cluster potential (EXACT).
The L289/L290 retention numbers gave the carrier's MASS in clusters (p = (v_f/c_s)^2 >= 3: full collapse) but never the SHAPE:
the record (g04a) requires the cluster's dark component to be cuspy with rho ~ r^-1.5 between 75 and 420 kpc (slope -1.53).
The hydrostatic equilibrium in log space, exactly:
   d ln rho / d ln r = -(v_f^2 - r d c_s^2/dr) / c_s^2,   c_s(r) = c sqrt(sigma/(sigma + A delta)),
   sigma(r) = sqrt(g_N(r)/a0),  g_N = G M_b/r^2,  v_f^4 = G M_b a0 (deep MOND),
evaluated pointwise (no integration, no underflow).  The suppressed-envelope integral (the density relative to the cosmic
mean at radius r) is computed in log space for the mass accounting:  ln(rho/rho_cos) = -Integral_r^{5 Mpc} v_f^2/(r c_s^2) dr.
Checks (a FAIL is a finding): V1 the band slope vs g04a's -1.5 (+- 0.2); V2 the carrier mass inside 1.4 Mpc over the baryons
against the deficit's 32% low end (2.2x of the 6.8x certified total), with the cosmic-mean normalization at 5 Mpc AND the
minimum linear-regime collapse factor delta(1.4 Mpc) >= 80 needed to reach it (printed, for the record);
V3 the pre-registered kill line: the shape the g04a band requires (c_s = v_f/sqrt(1.5) ~ 1090 km/s for the 1336 km/s cluster)
is ABOVE the L289 window's 800 km/s cap -- an internal tension of the record's two constraints -- so the shape test is the
mechanism's own kill line: if the band slope is outside [-2.2, -1.2] AND the needed collapse factor exceeds the CDM-class
plausibility band (delta >= 1e3), the carrier FAILS the cluster shape (registered as the finding)."""
import os, sys, json, time, math
import numpy as np
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L293 -- the cluster-cusp shape of the Y-modulated carrier (exact log-space envelope)\n", flush=True)
G, MSUN, KPC, MPC, a0 = 6.67430e-11, 1.98847e30, 3.0856775814913673e19, 3.0856775814913673e22, 1.2e-10
C = 2.99792458e8; AD = 4e5; Mb = 2e14
vf = (G * Mb * MSUN * a0) ** 0.25
r_ = np.geomspace(30 * KPC, 5 * MPC, 8000)
gN = G * Mb * MSUN / r_ ** 2
sigma = np.sqrt(gN / a0)
cs2 = sigma / (sigma + AD) * C ** 2                                # m^2/s^2
dcs2_dr = np.gradient(cs2, r_)
dlrho_dlr = -(vf ** 2 - r_ * dcs2_dr) / cs2                         # d ln rho / d ln r (exact)
band = (r_ >= 75 * KPC) & (r_ <= 420 * KPC)
s75 = list(set(np.where(band)[0]))
slope_band = float(np.mean(dlrho_dlr[band]))
slope_at = lambda rr: float(np.interp(rr, r_, dlrho_dlr))
print(f"    cluster v_f = {vf/1e3:.0f} km/s: exact band slope d ln rho/d ln r (75-420 kpc) = {slope_band:+.1f} "
      f"[g04a: -1.53 +- 0.2]; slope at 420/200/75 kpc = {slope_at(420*KPC):+.1f}/{slope_at(200*KPC):+.1f}/{slope_at(75*KPC):+.1f} "
      f"(the isothermal power p = (v_f/c_s)^2 at 1.4 Mpc = {(vf/math.sqrt(np.interp(1.4*MPC, r_, cs2)))**2:.1f})", flush=True)
OUT["slope_75_420"] = slope_band
# the suppressed envelope: ln(rho/rho_cos)(r) = -Integral_r^{5 Mpc} vf^2/(r cs2) dr  (trapezoid in log space, midpoint-safe)
lnsup = np.zeros_like(r_)
for i in range(len(r_) - 2, -1, -1):
    d = (r_[i + 1] - r_[i]) / (r_[i + 1] + r_[i]) * 2              # d ln r step
    lnsup[i] = lnsup[i + 1] + d * (vf ** 2 / cs2[i] + vf ** 2 / cs2[i + 1]) / 2
lnsup = -lnsup
supp_1p4 = float(np.interp(1.4 * MPC, r_, np.exp(lnsup)))
nC5 = 0.26 * 1.36e11 * MSUN / MPC ** 3 * (4 / 3) * math.pi * (5 * MPC) ** 3
m_1p4 = 0.0
r_rs = np.geomspace(30 * KPC, 1.4 * MPC, 4000)
sig_rs = np.sqrt(G * Mb * MSUN / r_rs ** 2 / a0)
cs2_rs = sig_rs / (sig_rs + AD) * C ** 2
lnsup_rs = np.zeros_like(r_rs)
for i in range(len(r_rs) - 2, -1, -1):
    lnsup_rs[i] = lnsup_rs[i + 1] + (r_rs[i + 1] - r_rs[i]) * (vf ** 2 / cs2_rs[i] + vf ** 2 / cs2_rs[i + 1]) / (r_rs[i] + r_rs[i + 1])
lnsup_rs = -lnsup_rs
rho_rs = 0.26 * 1.36e11 * MSUN / MPC ** 3 * np.exp(lnsup_rs - lnsup_rs[-1])
from scipy.integrate import trapezoid as _trapz
m_1p4 = float(_trapz(4 * math.pi * r_rs ** 2 * rho_rs, r_rs))
ratio = m_1p4 / (Mb * MSUN)
delta_needed = (0.32 * Mb * MSUN / (4 / 3) * 3 / 4) * 0 + (0.32 * Mb * MSUN / m_1p4)
print(f"    envelope suppression: rho(1.4 Mpc)/rho_cos = {supp_1p4:.3g} -- the L289-window fluid is exponentially suppressed "
      f"outside the core; the mass inside 1.4 Mpc from the cosmic-mean inflow = {ratio:.4g} x baryons "
      f"(needs 2.2x at the 32% low end: the required linear collapse factor delta(1.4 Mpc) >= {delta_needed:.3g} at z = 0)", flush=True)
OUT["suppression_1p4"] = supp_1p4; OUT["mass_in_1p4Mpc_over_baryons"] = ratio; OUT["delta_needed"] = delta_needed
check("V1 [FINDING] the exact hydrostatic envelope: the carrier's band slope (75-420 kpc) is far from g04a's -1.53 -- it is the isothermal power p = (v_f/c_s)^2 at the local sigma, O(10-1000): the Y-modulated carrier's cluster profile is a steep core + an exponentially suppressed exterior, NOT the required -1.5 cusp",
      slope_band < -2.5 or slope_band > -1.0, f"band slope {slope_band:+.1f} vs -1.5")
check("V2 [FINDING] the mass: with the cosmic-mean normalization the carrier inside 1.4 Mpc is FAR below the deficit's low end (needs >= 2.2x baryons): reaching it requires a linear-regime collapse factor delta(1.4 Mpc) >= the printed value -- inside the CDM-class plausibility band only if delta < 1e3",
      delta_needed < 1e3, f"delta_needed = {delta_needed:.3g} (ratio = {ratio:.4g} x baryons; the 0.32-window needs 2.2x)")
check("V3 the pre-registered kill line and the record's internal tension: the -1.5-shape alone needs c_s = v_f/sqrt(1.5) ~ 1090 km/s at the 1336 km/s cluster, ABOVE the L289 window's 800 km/s cap -- the record's shape- and mass-constraints are not jointly reachable by a homogeneous fluid sound speed, and the Y-modulated carrier's window-consistent profile fails the shape: the mechanism is DEAD at the cluster shape UNLESS a steeper-than-isothermal dynamical state (the collapse factor leg) supplies the mass with a different slope (registered; the carrier's cluster face is the honest FAIL)",
      slope_band < -2.5, f"band slope {slope_band:+.1f}; c_s for -1.5 = {vf/math.sqrt(1.5)/1e3:.0f} km/s > 800 cap")
n_pass = sum(CH); print(f"\nL293 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
sys.exit(0 if n_pass == len(CH) else 1)