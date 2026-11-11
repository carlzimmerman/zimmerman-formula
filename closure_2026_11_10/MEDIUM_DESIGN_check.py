#!/usr/bin/env python3
"""MEDIUM_DESIGN_2026-11-10.md, section 3: SI arithmetic for a cold medium that exchanges momentum with baryons.
A hand check, not a lane: no criteria, no label. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

If the medium is to be heated to the baryons' virial dispersion where the baryonic acceleration exceeds a0 and to stay
collisionless outside, a baryon column of a0 / (pi G) must be one optical depth (mean enclosed acceleration of a column
Sigma is pi G Sigma). That fixes an opacity kappa = pi G / a0 per unit baryon mass. This script prints what that opacity
does at recombination and through a cluster's gas.

    python3 MEDIUM_DESIGN_check.py > MEDIUM_DESIGN_check.out
"""
import math

G = 6.67430e-11; c = 2.99792458e8; Mpc = 3.0856775814913673e22; pc = Mpc / 1e6
Msun = 1.98847e30; mp = 1.67262192e-27
h = 0.674; H0 = 100e3 * h / Mpc; rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)
Ob, Om, Orad = 0.0493, 0.3147, 9.15e-5          # the record's pinned fit (CO2 / KL1) to the digits needed here

print("MEDIUM_DESIGN check (SI). A hand check, not a lane. kappa = 1/2 FITTED; not theory closed.")
for name, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    Sig = a0 / (math.pi * G); kap = 1 / Sig
    print(f"[{name}] a0 = {a0:.4e} m/s^2")
    print(f"  column a0/(pi G) = {Sig:.4f} kg/m^2 = {Sig * pc ** 2 / Msun:.1f} Msun/pc^2 = {Sig * 0.1:.4f} g/cm^2")
    print(f"  opacity pi G / a0 = {kap:.3f} m^2/kg = {kap * 10:.1f} cm^2/g = {kap * mp * 1e4:.2e} cm^2 per proton"
          f" = {kap * 10 / 0.4:.0f} x the Thomson opacity of ionised hydrogen (0.4 cm^2/g)")
    for z in (1100.0, 3400.0):
        rho_b = Ob * rho_crit * (1 + z) ** 3
        lam = 1 / (rho_b * kap)
        Hz = H0 * math.sqrt(Om * (1 + z) ** 3 + Orad * (1 + z) ** 4 + (1 - Om - Orad))
        RH = c / Hz
        print(f"  z {z:.0f}: baryon density {rho_b:.2e} kg/m^3; mean free path {lam / pc:.1f} pc;"
              f" Hubble radius {RH / Mpc * 1e3:.0f} kpc ({RH / lam:.1e} mean free paths)")
        for v in (1e3, 3e4):
            print(f"         drag rate at a relative speed of {v / 1e3:.0f} km/s: {v / lam / Hz:.2f} of the expansion rate")
    for ne, L in ((1e-2, 500.0), (3e-3, 1000.0), (1e-3, 1000.0)):
        col = ne * 1e6 * 1.17 * mp * L * 1e3 * pc
        print(f"  gas column n_e {ne:g} cm^-3 over {L:.0f} kpc: {col * 0.1:.4f} g/cm^2 -> optical depth {col * kap:.2f}")
    print(f"  stellar disc column 50 Msun/pc^2 -> optical depth {50 * Msun / pc ** 2 * kap:.2f}")
