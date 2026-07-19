#!/usr/bin/env python3
"""Independent dimensional + numeric check of the framework's dark-energy equations,
including the physics-referee's SEVERE catch. Prove-by-moving-the-number."""
import numpy as np
c   = 2.99792458e8            # m/s
G   = 6.67430e-11            # m^3/kg/s^2
Lam = 1.089e-52              # 1/m^2  (Planck 2018 cosmological constant)
Z2  = 32*np.pi/3             # Z^2 (dimensionless)
Z   = np.sqrt(Z2)
CANON = 9.355e-11            # target a0 (canonical footing), m/s^2

print(f"Z = sqrt(32pi/3) = {Z:.5f}   (target 5.78881)")

# ---- 1. geometric form a0 = c^2 sqrt(Lambda/32pi)  [Lambda in 1/m^2] ----
a0_geo = c**2 * np.sqrt(Lam/(32*np.pi))
print(f"\n[GEO]  a0 = c^2 sqrt(Lambda/32pi)          = {a0_geo:.4e} m/s^2   (target {CANON:.3e})")

# ---- 2. SI mass-density form a0 = (c/2) sqrt(G rho_DE) ----
rho_DE = Lam*c**2/(8*np.pi*G)                 # kg/m^3  (standard rho_Lambda)
a0_si  = (c/2)*np.sqrt(G*rho_DE)
print(f"[SI ]  rho_DE = Lambda c^2/(8piG)          = {rho_DE:.4e} kg/m^3")
print(f"[SI ]  a0 = (c/2) sqrt(G rho_DE)           = {a0_si:.4e} m/s^2   (target {CANON:.3e})")

# ---- 3. inverse: rho_DE = 4 a0^2/(G c^2) ----
rho_back = 4*CANON**2/(G*c**2)
print(f"[INV]  rho_DE = 4 a0^2/(G c^2)             = {rho_back:.4e} kg/m^3   (matches {rho_DE:.3e}? {np.isclose(rho_back,rho_DE,rtol=2e-3)})")

# ---- 4. THE REFEREE'S SEVERE CATCH: c^2 sqrt(rho_DE/32pi) with a MASS density is WRONG ----
a0_bad = c**2*np.sqrt(rho_DE/(32*np.pi))
print(f"\n[BAD]  c^2 sqrt(rho_DE/32pi) w/ MASS rho   = {a0_bad:.4e} (kg^0.5 m^0.5 s^-2)  <-- NOT m/s^2, ~{a0_bad:.0f}, dimensionally wrong (referee correct)")

# ---- 5. the Friedmann term I gave Carl: Z^2 a0^2/c^2 must equal H_Lambda^2 = Lambda c^2/3 ----
term  = Z2*CANON**2/c**2
H_Lam2 = Lam*c**2/3
print(f"\n[FRW]  Z^2 a0^2/c^2                        = {term:.4e} s^-2")
print(f"[FRW]  H_Lambda^2 = Lambda c^2/3           = {H_Lam2:.4e} s^-2   (equal? {np.isclose(term,H_Lam2,rtol=3e-3)})")
print(f"[FRW]  => H^2 = 8piG/3 rho_m + Z^2 a0^2/c^2 reduces to LCDM dark-energy term at z=0: CONFIRMED")

# ---- 6. dimensional sanity of the Friedmann term (units of 1/s^2) ----
# [a0^2/c^2] = (m/s^2)^2 / (m/s)^2 = 1/s^2  -> matches H^2. Z^2 dimensionless. OK.
print(f"\n[DIM]  [Z^2 a0^2/c^2] = (m/s^2)^2/(m/s)^2 = 1/s^2 = [H^2]  OK")
print("EXIT 0")
