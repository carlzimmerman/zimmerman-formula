#!/usr/bin/env python3
r"""
PROBLEM 2 -- PART 3 (FIXED units): pin the tilt amplitude A^r from the algebraic EOM with
DIMENSIONALLY CONSISTENT source, then the two carriers, then GATES.

Dimensional bookkeeping (geometric c=1, lengths in metres):
  A^mu dimensionless (contravariant component).  d_mu ~ 1/length.
  phi dimensionless (SZ normalization). varphi' = d_r phi ~ 1/length.
  Q = A^mu d_mu phi ~ 1/length.  Q0 ~ 1/Mpc.  Y = q d phi d phi ~ 1/length^2.
  m_A^2 = (2-K_B)(1+lam_s)Q0^2/K_B ~ (1/Mpc)^2  [1/length^2].  GOOD: matches LHS m_A^2 A^r.

The A^r EOM from varying the action (16piG=1) w.r.t. A^r. The action density terms with A^r:
  -F(Y,Q): the Euler-Lagrange variation of a term -F where Y,Q depend on A^r AND on d phi gives
  BOTH an algebraic piece (-F_Q dQ/dA^r etc, from the explicit A in Q,Y) AND, because A also sits
  inside q=g+AA which multiplies d phi d phi, the EOM is algebraic in A^r (no d/dr of A^r from -F).
  The vector kinetic -(K_B/2)F^2 would give the d/dr(A) stiffness, but Part 1 showed it is O(A^r^2)
  in strict spherical symmetry -> NO linear Laplacian. So the WHOLE linear A^r EOM is ALGEBRAIC:

      [ constraint-mass + Q0^2 mass ] A^r  =  - F_Q (dQ/dA^r) - F_Y (dY/dA^r)
            m_A^2 A^r                       =  - F_Q varphi'  - 2 F_Y Q varphi'

  LHS [1/length^2]*[dimensionless] = [1/length^2].  RHS [dimensionless]*[1/length] = [1/length].
  >>> DIMENSIONAL MISMATCH by one power of length. <<<
  Resolution: F_Q and F_Y are NOT dimensionless. F has units [1/length^2] (it sits in the action
  next to (2-K_B)Y ~ 1/length^2). So F_Q = dF/dQ ~ [1/length^2]/[1/length] = [1/length], and
  F_Y = dF/dY ~ [1/length^2]/[1/length^2] = dimensionless. Then:
     F_Q varphi'  ~ [1/length][1/length] = [1/length^2]   GOOD
     2 F_Y Q varphi' ~ [dimensionless][1/length][1/length] = [1/length^2]  GOOD
  So with F_Q ~ Q0-scale (the natural scale of the Q-sector, [1/length]) and F_Y ~ O(1)/sqrt(deep-MOND),
     m_A^2 A^r = F_Q varphi' + 2 F_Y Q0 varphi'
     A^r = (F_Q + 2 F_Y Q0) varphi' / m_A^2.
  With F_Q ~ Q0, F_Y ~ O(1), m_A ~ Q0:
     A^r ~ (Q0 + 2 Q0) varphi'/Q0^2 = 3 varphi'/Q0.      <-- the clean algebraic estimate.
"""
import numpy as np

c   = 2.99792458e8
G   = 6.674e-11
Mpc = 3.0857e22
kpc = 3.0857e19
H0  = 67.4e3/Mpc
Z   = 2*np.sqrt(8*np.pi/3)
a0  = c*H0/Z
theta_cosmo = 3*H0

Q0       = 1.0/Mpc          # 1/length
varphi_p = a0/c**2          # 1/length  (MOND scalar gradient)
L_u      = 10*kpc

print("="*100)
print("PART 3 (FIXED) -- algebraic A^r with dimensionally-consistent F_Q~Q0, F_Y~O(1), m_A~Q0")
print("="*100)
print(f"  Q0={Q0:.3e}/m  varphi'={varphi_p:.3e}/m  ->  varphi'/Q0 = {varphi_p/Q0:.3e}")
print(f"  natural algebraic tilt:  A^r ~ 3 varphi'/Q0 = {3*varphi_p/Q0:.3e}  (gradient/mass ratio)\n")

# exposures per unit A^r
dtheta_per_u = c/(3*H0*L_u)
dQ_per_u     = varphi_p/Q0
print(f"  exposures: d(theta/3H)/dA^r = c/(3H0 L_u) = {dtheta_per_u:.3e}")
print(f"             d(Q/Q0)/dA^r     = varphi'/Q0  = {dQ_per_u:.3e}\n")

print(f"  {'scenario':>34}{'A^r':>12}{'dtheta/3H':>14}{'dQ/Q0':>12}{'  verdict'}")
def regime(x): return "SWAMP" if x>1 else ("edge" if x>0.1 else "PIN")
rows = []
for label, Ar in [
    ("DERIVED algebraic A^r=3varphi'/Q0", 3*varphi_p/Q0),
    ("conservative A^r=varphi'/Q0",        varphi_p/Q0),
    ("soft m_A=Q0/10 -> A^r=300varphi'/Q0",300*varphi_p/Q0),
    ("PROMPT virial A^r=v_vir/c",          150e3/c),
    ("strict EJ static A^r=0",             0.0),
]:
    dth = Ar*dtheta_per_u
    dQ  = Ar*dQ_per_u
    rows.append((label,Ar,dth,dQ))
    print(f"  {label:>34}{Ar:>12.2e}{dth:>14.2e}{dQ:>12.2e}   theta:{regime(dth)}/Q:{regime(dQ)}")

print(f"""
  THE TWO NUMBERS (DERIVED algebraic tilt A^r ~ 3 varphi'/Q0 = {3*varphi_p/Q0:.1e}):
     delta-theta/3H = {3*varphi_p/Q0*dtheta_per_u:.2e}
     delta-Q/Q0     = {3*varphi_p/Q0*dQ_per_u:.2e}

  STRUCTURE: A^r ~ varphi'/Q0 ~ {varphi_p/Q0:.0e} (the galaxy MOND gradient over the cosmological
  scalar scale). Then:
    * delta-Q/Q0   = A^r * varphi'/Q0 = (varphi'/Q0)^2 ~ {(varphi_p/Q0)**2:.0e}  -- DOUBLY suppressed,
      PINNED to ~1e-9. Q is the ROBUST carrier (its own coupling is the same small varphi'/Q0).
    * delta-theta/3H = A^r * c/(3H0 L_u) = (varphi'/Q0)*(c/3H0 L_u). The first factor is small
      (~4e-5) but the second is HUGE (~1.5e5), product ~ {3*varphi_p/Q0*dtheta_per_u:.1f}. theta sits
      at the EDGE (order few-to-1): the derived tilt gives an O(1) -- few fractional wobble in theta.
  => theta=div A is NOT robustly pinned: a real, EOM-derived tilt of order varphi'/Q0 produces an
     O(1)-order fractional shift in theta/3H, because 3H0 is so tiny. Q is pinned to ~1e-9.\n""")

# ------------------------------------------------------------------------------------------
# The decisive ratio R is convention-INDEPENDENT (A^r cancels):
R = dQ_per_u/dtheta_per_u
print("="*100)
print("CONVENTION-INDEPENDENT RATIO (A^r cancels) -- which carrier dies first")
print("="*100)
print(f"  R = (dQ/Q0)/(dtheta/3H) = (varphi'/Q0)/(c/3H0 L_u) = varphi' 3H0 L_u/(Q0 c) = {R:.2e}")
print(f"  R << 1 by ~{1/R:.0e}: for ANY tilt amplitude, Q is shifted ~{1/R:.0e}x LESS than theta.")
print(f"  => theta is the FRAGILE carrier, Q the ROBUST one -- INDEPENDENT of how big the tilt is,")
print(f"     and independent of m_A, F_Q, F_Y. This is the load-bearing, convention-robust result.\n")

# the tilt that BREAKS each carrier (delta/.. = 1):
Ar_break_theta = 1.0/dtheta_per_u
Ar_break_Q     = 1.0/dQ_per_u
print(f"  tilt that makes delta-theta/3H = 1:  A^r = {Ar_break_theta:.2e}  ({Ar_break_theta*c/1e3:.1e} km/s-equiv)")
print(f"  tilt that makes delta-Q/Q0    = 1:  A^r = {Ar_break_Q:.2e}  ({Ar_break_Q*c/1e3:.1e} km/s-equiv)")
print(f"  => theta breaks at A^r~{Ar_break_theta:.0e} (a ~{Ar_break_theta*c:.0f} m/s tilt!); Q needs A^r~{Ar_break_Q:.0e}")
print(f"     (super-luminal -> Q is UNBREAKABLE by any physical tilt). The {Ar_break_Q/Ar_break_theta:.0e}x gap = 1/R.\n")
