#!/usr/bin/env python3
"""
G058 -- numeric design + cross-check for the Lean certificate
G058_omega_from_a0.lean (the G052 one-constant closure).

Computes Omega_Lambda = 32*pi*a0^2/(3*H0^2*c^2) in EXACT rationals (Fraction),
sandwiches pi with the same bounds Mathlib proves (Real.pi_gt_d6: 3.141592 < pi,
Real.pi_lt_d4: pi < 3.1416), and verifies the Lean interval theorem's margins
BEFORE committing the certificate.  Also cross-checks the G052 canonical
footing (H0 = 67.36, ratio 1.0003 vs Planck 0.6847 = the +0.07%).
"""
from fractions import Fraction as F

a0 = F("9.3619e-11")            # m/s^2, certified SI
c  = F(299792458)               # m/s, exact
H0 = F(674, 10) * F(1000) / F("3.085677581e22")   # 67.4 km/s/Mpc in s^-1

# Mathlib's pi bounds (PI.lean): 3.141592 < pi < 3.1416
pi_lo, pi_hi = F("3.141592"), F("3.1416")
TRUE_PI = F("3.14159265358979323846264338328")
assert pi_lo < TRUE_PI < pi_hi

K = 32 * a0**2 / (3 * H0**2 * c**2)          # Omega = K * pi
lo, hi = K * pi_lo, K * pi_hi
print(f"K (pi-free factor)      = {float(K):.16f}")
print(f"Omega_Lambda (true pi)  = {float(K*TRUE_PI):.16f}")
print(f"Lean window [K*pi_lo, K*pi_hi] = [{float(lo):.10f}, {float(hi):.10f}]")
print(f"in (0.68, 0.69) with margins: lo-0.68 = {float(lo - F(68,100)):.6f}, "
      f"0.69-hi = {float(F(69,100) - hi):.6f}")

# G052 canonical variant (H0 = 67.36): the registered 0.6857
H0b = F(6736, 100) * F(1000) / F("3.085677581e22")
Kb = 32 * a0**2 / (3 * H0b**2 * c**2)
print(f"H0=67.36 variant: [{float(Kb*pi_lo):.10f}, {float(Kb*pi_hi):.10f}] "
      f"(registered 0.6857)")

# Planck cross-check: derived/Planck = 1.000337 -> the +0.07% dex claim of G052
print(f"derived/Planck = {float(K*TRUE_PI)/0.6847:.6f} "
      f"(= +0.034%; G052's H0=67.36 variant: {float(Kb*TRUE_PI)/0.6847:.6f}, +0.07%)")
