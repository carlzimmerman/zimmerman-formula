#!/usr/bin/env python3
"""
Lane 3 numbers, both footings, prove-by-moving-the-number.
(1) a0 = c*H_Lambda/Z = c^2 sqrt(Lambda/32pi), Z=sqrt(32pi/3), both footings.
(2) The Cassini Q2 ceiling and where each theory class sits.
No fitting, no claim beyond what is derivable/quoted. Exit 0.
"""
import math

c    = 2.99792458e8        # m/s
G    = 6.674e-11
# Planck 2018-ish
H0   = 2.20e-18            # s^-1 (~67.9 km/s/Mpc)
OmL  = 0.685
Lam  = 1.09e-52           # m^-2 (Lambda, from rho_DE)
Z    = math.sqrt(32*math.pi/3)

print(f"Z = sqrt(32pi/3) = {Z:.4f}")

# --- a0, canonical footing: rho_DE / cH_Lambda  ->  a0 = c^2 sqrt(Lambda/32pi) ---
# H_Lambda = c*sqrt(Lambda/3);  a0 = c*H_Lambda/Z = c^2 sqrt(Lambda/3)/sqrt(32pi/3)
#          = c^2 sqrt(Lambda/32pi)
a0_from_Lambda = c**2 * math.sqrt(Lam/(32*math.pi))
H_Lam = c*math.sqrt(Lam/3.0)
a0_canon = c*H_Lam/Z
print(f"\n[canonical footing  rho_DE / cH_Lambda]")
print(f"  H_Lambda = c sqrt(Lambda/3)      = {H_Lam:.3e} s^-1")
print(f"  a0 = c H_Lambda / Z              = {a0_canon:.3e} m/s^2")
print(f"  a0 = c^2 sqrt(Lambda/32pi)       = {a0_from_Lambda:.3e} m/s^2  (identity check)")
print(f"  TARGET canonical                 = 9.36e-11")

# --- a0, alt footing: rho_total / cH0 ---
a0_alt = c*H0/(2*math.pi)      # Milgrom's a0 ~ cH0/2pi heuristic (alt-footing family)
a0_alt2 = c*H0/Z               # same footing, framework Z instead of 2pi
print(f"\n[alt footing  rho_total / cH0]")
print(f"  a0 ~ c H0 / 2pi                  = {a0_alt:.3e} m/s^2")
print(f"  a0 = c H0 / Z                    = {a0_alt2:.3e} m/s^2")
print(f"  TARGET alt                       = 1.13e-10")

# Woodard's inserted nonlocal a0 (FREE input, not derived)
a0_woodard = 1.2e-10
print(f"\n[nonlocal Deffayet-Woodard] a0 INSERTED (free) = {a0_woodard:.3e}  "
      f"-> ratio to canonical = {a0_woodard/a0_canon:.2f}x  (NOT derived)")

# --- Cassini Q2 ceiling and class placement (quoted numbers, order-of-mag map) ---
print("\n--- Cassini solar quadrupole Q2 (s^-2) ---")
Q2_meas   = 3e-27      # (3 +/- 3)e-27  Cassini
Q2_sigma  = 3e-27
Q2_ceiling= Q2_meas + 2*Q2_sigma   # ~2sigma upper ~ 9e-27; context ceiling ~5.2e-27
print(f"  Cassini measured Q2   = ({Q2_meas:.0e} +/- {Q2_sigma:.0e})")
print(f"  ~2sigma upper bound   ~ {Q2_ceiling:.1e}   (working ceiling ~5.2e-27)")
print(f"  vector class (AeST)   ~ 2-3e-26  -> FAILS ceiling by ~{2.5e-26/5.2e-27:.1f}x  (+6-14 sigma)")
print(f"  exponential screening (nonlocal Deffayet-Woodard): Q2 UNCOMPUTED")
print(f"     -> structurally power-law-FREE; could sit << ceiling. THE decisive uncomputed number.")

# Sanity: identity a0=c^2 sqrt(Lambda/32pi) must equal c*H_Lambda/Z exactly
assert abs(a0_canon - a0_from_Lambda)/a0_canon < 1e-12, "a0 identity broken"
assert 8e-11 < a0_canon < 1.05e-10, "canonical a0 out of expected band"
print("\nAll identity/sanity checks passed.")
