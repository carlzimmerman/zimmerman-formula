#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG243_controls -- the frozen controls K1-K5 (reproduce committed numbers before any gate), plus the controls this phase adds for the
tools it substitutes for memory (K6 the CLASS velocity-divergence normalisation, K7 the CLASS growth against CFG7's committed growth).
A failed control stops the lane (the run_all script checks the exit code).

FROZEN (section 5): K1 CLASS sigma_8 = 0.8116 (CFG4_cosmology.out); K2 CFG251's A1 ratio (0.4)^3 = 0.064; K3 CFG131's x* = 20.2 and
f = 1.70 at x = 30 from the Omega ratios; K4 CFG118's M_ta = 23.6 M_b scaling (consistency, not a reproduction: no shell run here);
K5 CFG4's thresholds 11.81 / 8.89 / 7.09 / 5.72 (and delta_lin 1.276 -> 1.076).
"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import CFG243_common as C

R = C.Run("CFG243_controls")
P = R.P
P(__doc__.strip())

R.banner("K1/K7: CLASS reproduces CFG4's sigma_8 and the committed growth")
c = C.class_cosmo([0, 2.5, 10, 100, 1100])
k0, D2_0 = C.delta2(c, 0, "d_m")
s8 = C.sigma_R(k0, D2_0, 8.0 / c.h())
k0t, D2_0t = C.delta2(c, 0, "d_tot")
s8t = C.sigma_R(k0t, D2_0t, 8.0 / c.h())
P(f"  CLASS: Omega_m = {c.Omega_m():.5f} (CFG4 uses {C.OMEGA_M}); sigma_8 (d_m) = {s8:.5f}, (d_tot) = {s8t:.5f}; CFG4_cosmology.out: 0.8116")
R.check("K1 CLASS sigma_8 reproduces CFG4_cosmology.out's 0.8116 (|diff| <= 5e-4)", abs(s8t - 0.8116) <= 5e-4 and abs(s8 - 0.8116) <= 1e-3,
        f"{s8t:.5f} / {s8:.5f}")
R.check("K1b CLASS total matter Omega_m = 0.3157 (CFG4's committed value; |diff| <= 5e-4)", abs(c.Omega_m() - 0.3157) <= 5e-4, f"{c.Omega_m():.5f}")
C7 = C.load_c7()
L = C7.LCDM
ks, D2z = C.delta2(c, 10, "d_m")
ratio_class = C.sigma_R(ks, D2z, 8.0 / c.h()) / s8
ratio_c7 = float(L.D(1 / 11.0) / L.D(1.0))
P(f"  sigma_8(z=10)/sigma_8(0): CLASS {ratio_class:.5f} vs CFG7_common's D(1/11)/D(1) = {ratio_c7:.5f}")
R.check("K7 CLASS growth (z = 10 to 0 on 8/h Mpc) agrees with CFG7_common's committed D(a) to 2%", abs(ratio_class / ratio_c7 - 1) <= 0.02,
        f"{ratio_class:.5f} vs {ratio_c7:.5f}")

R.banner("K2/K3: CFG251's A1 ratio and CFG131's vacuum-ledger numbers")
R.check("K2 CFG251 A1: (r_e/r_ta)^3 = 0.4^3 = 0.064", abs(0.4 ** 3 - 0.064) < 1e-12, f"{0.4 ** 3}")
oc_ob, ol_ob = 5.36, 13.9                       # CFG131's own inputs (README line 5)
xstar = math.sqrt((oc_ob + ol_ob + 1.0) ** 2 - 1.0)
f30 = (math.sqrt(1 + 900.0) - 1 - oc_ob) / ol_ob
x629 = math.sqrt((oc_ob + 1.0) ** 2 - 1.0)
P(f"  x* = {xstar:.2f} (CFG131: 20.2); f(x=30) = {f30:.3f} (CFG131: 1.70); no-conversion limit x = {x629:.2f} (CFG131: 6.29)")
R.check("K3 CFG131: x* = 20.2, f(30) = 1.70, no-conversion limit 6.29", abs(xstar - 20.2) < 0.06 and abs(f30 - 1.70) < 0.01 and abs(x629 - 6.29) < 0.01,
        f"{xstar:.2f}, {f30:.3f}, {x629:.2f}")

R.banner("K4/K5: CFG118's turnaround mass and CFG4's thresholds")
rta118 = 236.0
Mta = 4 * math.pi / 3 * rta118 ** 3 * (C.OMEGA_M * C.RHOC0_KPC) * float(L.one_plus_delta_ta(1.0))
P(f"  top-hat mass inside CFG118's r_ta(1e9) = 236 kpc at the committed contrast {float(L.one_plus_delta_ta(1.0)):.2f}: {Mta / 1e9:.1f} M_b (CFG118: 23.6)")
R.check("K4 CFG118's M_ta = 23.6 M_b is consistent with its r_ta = 236 kpc and the committed contrast (to 15%; no shell run here)",
        abs(Mta / 1e9 / 23.6 - 1) <= 0.15, f"{Mta / 1e9:.1f}")
vals = [(z, float(L.one_plus_delta_ta(1 / (1 + z))), float(L.delta_lin_ta(1 / (1 + z)))) for z in (0, 0.25, 0.64, 2.5)]
cfg4 = {0: 11.81, 0.25: 8.89, 0.64: 7.09, 2.5: 5.72}
P("  committed LCDM (CFG7_common) turnaround contrast / delta_lin vs CFG4_README: " + "; ".join(f"z={z}: {a:.2f}/{d:.3f} (CFG4 {cfg4[z]})" for z, a, d in vals))
R.check("K5 CFG4's contrasts 11.81 / 8.89 / 7.09 / 5.72 reproduced to 0.6% by the committed LCDM", all(abs(a / cfg4[z] - 1) <= 0.006 for z, a, d in vals),
        ", ".join(f"{a:.2f}" for z, a, d in vals))
R.check("K5b CFG4's delta_lin 1.276 (z=0) and 1.076 (z=2.5) reproduced to 0.5% (the frozen thresholds)",
        abs(vals[0][2] / 1.276 - 1) <= 0.005 and abs(vals[3][2] / 1.076 - 1) <= 0.005, f"{vals[0][2]:.4f}, {vals[3][2]:.4f}")

R.banner("K6: CLASS velocity-divergence normalisation (Newtonian gauge): theta_tot / (calH delta_tot) = -f at z = 10, k = 1/Mpc")
cn = C.class_cosmo([10, 1100], newtonian=True)
tr = cn.get_transfer(10)
k = tr["k (h/Mpc)"] * cn.h()
i = int(np.argmin(abs(k - 1.0)))
calH = cn.Hubble(10.0) / (1 + 10.0)   # a H, with H in 1/Mpc; a = 1/11: a H = H/11
calH = cn.Hubble(10.0) * (1.0 / 11.0)
ratio = tr["t_tot"][i] / (calH * tr["d_tot"][i])
f10 = float(L.f(1 / 11.0))
P(f"  k = {k[i]:.3f}/Mpc: theta_tot/(calH delta_tot) = {ratio:.4f}; -f(z=10) from CFG7_common = {-f10:.4f}")
R.check("K6 theta_tot/(calH delta_tot) = -f (3%): the transfer normalisation of t_tot is the physical divergence per unit delta", abs(ratio + f10) <= 0.03 * f10,
        f"{ratio:.4f} vs {-f10:.4f}")

R.finish()
