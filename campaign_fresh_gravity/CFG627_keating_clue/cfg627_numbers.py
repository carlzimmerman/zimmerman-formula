#!/usr/bin/env python3
"""CFG627 -- back-of-envelope numbers for the Keating-clue README (read-and-think lane; < 1 s, 1 process).

N1  a0(z)/a0(0) at z = 2.148 (FRB 20240304B host) and z = 1.16 (CHIME): FLAT (Lambda constant; CFG549 own-ingredient
    prediction), versus the rival a0 ~ H(z).  Background E(z) uses Omega_m = 0.3153 (declared CMB input, as CFG549).
N2  Deep-MOND isothermal dispersion of a M* ~ 1e7 Msun host, sigma^4 = (4/81) G M a0 (standard-MOND point-mass
    estimator, INHERITED, used only to show the size), both footings, gas factors 1/3/10, FLAT vs a0 ~ H(z).
    Compared with a NIRSpec grating resolution floor (R ~ 1000 / 2700 -> sigma_instr ~ c/(2.355 R)).
N3  Mean cosmic DM at z = 2.148 for a standard baryon budget (Macquart form, INHERITED background; Omega_b h^2
    = 0.02237 Planck, f_d = 0.84 declared), to show the framework's background gives the same mean (it uses the same
    Omega_b, Omega_c/Omega_b = 5.364 and a constant rho_DE): only f_d (where baryons sit) can differ.
MUTATE (CFG627_MUTATE=1): set the rival exponent to 0 (a0 ~ H^0) -> N1 rival must collapse onto FLAT (ratio 1).
"""
import os, json
import numpy as np
from scipy.integrate import quad

MUT = os.environ.get("CFG627_MUTATE") == "1"
c = 2.99792458e8; G = 6.674e-11; Msun = 1.989e30; mp = 1.67262e-27; Mpc = 3.0857e22
Om, h, Obh2 = 0.3153, 0.6736, 0.02237
OL = 1 - Om
E = lambda z: np.sqrt(Om * (1 + z) ** 3 + OL)
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
p_rival = 0.0 if MUT else 1.0
out = {"mutate": MUT}

print("CFG627 numbers" + (" [MUTATE: rival exponent 0]" if MUT else ""))
for z in (1.16, 2.148, 2.5):
    flat, riv = 1.0, E(z) ** p_rival
    out[f"N1_z{z}"] = {"flat": flat, "rival_H": riv, "gap_dex": float(np.log10(riv / flat))}
    print(f"N1 z={z}: a0 ratio FLAT 1.000, a0~H(z) {riv:.3f}  (gap {np.log10(riv):.3f} dex)")

Mstar = 10 ** 6.89
for foot, a0 in A0.items():
    for gf in (1, 3, 10):
        M = Mstar * gf * Msun
        sf = ((4 / 81) * G * M * a0) ** 0.25 / 1e3
        sr = ((4 / 81) * G * M * a0 * E(2.148) ** p_rival) ** 0.25 / 1e3
        out[f"N2_{foot}_gas{gf}"] = {"sigma_flat_kms": sf, "sigma_rivalH_kms": sr}
        print(f"N2 {foot} Mbar={gf}xM*: sigma FLAT {sf:.1f} km/s, a0~H {sr:.1f} km/s (ratio {sr/sf:.3f})")
for R in (1000, 2700):
    s = c / (2.355 * R) / 1e3
    out[f"N2_instr_R{R}"] = s
    print(f"N2 NIRSpec R={R}: instrumental sigma ~ {s:.0f} km/s")

H0 = 100 * h * 1e3 / Mpc
Ob = Obh2 / h ** 2
fd, fe = 0.84, 7 / 8  # f_e: electrons per baryon mass for H + fully ionised He, Y = 0.25
K = 3 * c * H0 * Ob / (8 * np.pi * G * mp) * fe  # electrons m^-3 * m
for z in (1.0, 2.148):
    I = quad(lambda x: (1 + x) / E(x), 0, z)[0]
    dm = K * fd * I / (3.0857e16 * 1e6)  # pc cm^-3
    out[f"N3_DMcosmic_z{z}"] = dm
    print(f"N3 <DM_cosmic>(z={z}) = {dm:.0f} pc cm^-3 (f_d = {fd}); measured FRB 20240304B DM_cosmic+host/(1+z) ~ 2330")
json.dump(out, open("cfg627_numbers" + ("_MUTATE" if MUT else "") + ".json", "w"), indent=1)
if MUT:
    assert abs(out["N1_z2.148"]["rival_H"] - 1) < 1e-12, "MUTATE control failed"
    print("MUTATE control PASS: rival collapses onto FLAT")
