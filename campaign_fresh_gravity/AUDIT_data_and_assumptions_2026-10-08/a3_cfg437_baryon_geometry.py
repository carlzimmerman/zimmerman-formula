#!/usr/bin/env python3
"""AUDIT A3 (read-only): CFG437 BX442.  CFG437 computes g_N = G (M* + M_gas)/R^2 at R = 8 kpc, i.e. ALL baryons as a point
mass inside 8 kpc, although the disc has r_1/2 ~ 5 kpc (R_d = 5/1.68 = 2.98 kpc, the script's own Rd).  This script
re-derives the implied a0 at the medians (Law+12: M* 6e10, M_gas 2e10, V_c 234 km/s, sigma_z 71) under
  (i)  point mass (CFG437 as committed),
  (ii) spherical enclosed mass of an exponential disc (fraction 1-(1+x)e^-x at x = R/R_d),
  (iii) razor-thin Freeman disc (V^2 = 4 pi G Sigma0 R_d y^2 [I0K0 - I1K1], y = R/2R_d),
and with the gas doubled (the z~2 molecular-gas scaling relations put f_gas ~ 0.4-0.5 at this M*, i.e. the
locally calibrated Schmidt-Kennicutt inversion is the LOW side) -- the inherited-assumption check asked for.
Readings A (V_c = V_rot) and B (asymmetric drift V^2 + 2 sigma^2 R/R_d, CFG437's choice) and B' (V^2 + sigma^2 R/R_d,
half the pressure term) are shown.  Predictions: flat 9.36e-11 / 1.13e-10; H(z) 3.08e-10 / 3.72e-10."""
import math, json, os
from scipy.special import i0, i1, k0, k1
HERE = os.path.dirname(os.path.abspath(__file__))
G, MS, KPC = 6.674e-11, 1.989e30, 3.0857e19
R, RD = 8.0, 5.0 / 1.68
def gN_of(Mb, geom):
    x = R / RD
    if geom == "point": return G * Mb * MS / (R * KPC) ** 2
    if geom == "sphere_enclosed": return G * Mb * MS * (1 - (1 + x) * math.exp(-x)) / (R * KPC) ** 2
    y = x / 2; S0 = Mb * MS / (2 * math.pi * (RD * KPC) ** 2)
    V2 = 4 * math.pi * G * S0 * RD * KPC * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y)); return V2 / (R * KPC)
def a0_implied(gobs, gN):
    r = gobs / gN
    if r <= 1: return float("nan")
    return gN / math.log(1 - 1 / r) ** 2
out, L = {}, []
L.append(f"x = R/R_d = {R/RD:.2f}; enclosed fraction (sphere) = {1-(1+R/RD)*math.exp(-R/RD):.3f}")
for Mg, gl in ((2e10, "M_gas 2e10 (SK inversion, as published)"), (4e10, "M_gas 4e10 (gas doubled)")):
    for geom in ("point", "sphere_enclosed", "freeman_thin"):
        gN = gN_of(6e10 + Mg, geom); row = {}
        for rd, v2 in (("A", 234e3 ** 2), ("B", 234e3 ** 2 + 2 * 71e3 ** 2 * R / RD), ("B'", 234e3 ** 2 + 71e3 ** 2 * R / RD)):
            row[rd] = a0_implied(v2 / (R * KPC), gN)
        out[f"{gl} | {geom}"] = dict(gN=gN, **row)
        L.append(f"  {gl:40s} {geom:16s} g_obs/g_N(A) {234e3**2/(R*KPC)/gN:5.2f}  a0: A {row['A']:.2e}  B {row['B']:.2e}  B' {row[chr(66)+chr(39)]:.2e}")
L.append("Reading: at R = 2.7 R_d the thin Freeman disc gives g_N within 2% of the point mass, so CFG437's point mass is a fair proxy; a spherical-enclosed estimate is 25% lower. The gas mass (SK inversion) moves reading A by ~x5 and reading B by ~x1.6: the locally calibrated inversion is the dominant inherited assumption; if it UNDER-estimates z~2 gas (as the molecular scaling relations suggest), the published-input implied a0 is biased HIGH (toward the H(z) rival, against flat).")
json.dump(out, open(os.path.join(HERE, "a3_cfg437_baryon_geometry.json"), "w"), indent=1)
print("\n".join(L)); open(os.path.join(HERE, "a3_cfg437_baryon_geometry.out"), "w").write("\n".join(L) + "\n")
