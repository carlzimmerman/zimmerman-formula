#!/usr/bin/env python3
"""Check Argon's numbers from its NO-GO reply on alpha, 2026-11-02. Convention: a0 = c^2/(2 L), as Argon's variants 1 and 2 use."""
import math
L1 = 1.0
rows = {"V1 L1": 1.0, "V2 c/sqrt(4 pi G rho)": 1 / math.sqrt(4 * math.pi), "V3 dS radius": math.sqrt(3 / (8 * math.pi)), "V4 active": math.sqrt(3 / (4 * math.pi))}
argon = {"V1 L1": .5, "V2 c/sqrt(4 pi G rho)": math.sqrt(math.pi), "V3 dS radius": .1727, "V4 active": .2443}
for k, L in rows.items():
    kap = 1 / (2 * L)
    print(f"{k}: L/L1 {L:.4f}; kappa = 1/(2L) {kap:.4f}; alpha = kappa^2/pi {kap**2/math.pi:.4f}; Argon kappa {argon[k]:.4f}; Argon = L/2? {abs(argon[k]-L/2) < 1e-3}")
a2 = math.exp(-4 * math.asinh(.5))
print("form a mu(1)", 1 - 1 / 4, "boost", 1 / math.sqrt(.75) - 1, "; form b mu(1)", 1 - a2, "boost", 1 / math.sqrt(1 - a2) - 1, "; golden^-4", ((math.sqrt(5) - 1) / 2) ** 4)
GM, s = 1.327e20, 2 * 9.36e-11
print("g = s at r =", math.sqrt(GM / s) / 1.496e11, "AU; Argon's sqrt(2) form", math.sqrt(2 * GM / s) / 1.496e11, "AU; quoted 7000")
print("Q2 from ratio:", 5.48 * 5.2e-27, 3.92 * 5.2e-27)
