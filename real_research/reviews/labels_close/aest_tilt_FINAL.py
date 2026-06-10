#!/usr/bin/env python3
r"""
PROBLEM 2 (AeST aether tilt) -- FINAL consolidated result.
==========================================================
Question (relay-upgraded): does a virial-magnitude radial aether tilt A^r swamp ANY background-
tracking scalar in a galaxy, or only theta=div A? Compute the tilt's effect on BOTH carriers:
  theta = div A           (the rising-a0 carrier; sees a DERIVATIVE of A^r)
  Q     = A^mu d_mu phi   (the declining V(Q) fallback's carrier; sees A^r ALGEBRAICALLY x dphi')

DERIVED (sympy, Parts 1&4):
  * In STRICT spherical symmetry the vector kinetic -(K_B/2)F^2 gives the radial tilt NO linear
    Laplacian (it enters at O(A^r^2)); the tilt is an ALGEBRAIC mode with mass m_A^2 from the
    unit-norm multiplier + the Q0^2 mass m_A^2=(2-K_B)(1+lam_s)Q0^2/K_B.
  * A^r=0 is NOT a solution: dL/dA^r|_{A^r=0} = -(F_Q + 2 F_Y A^t Q0) varphi' != 0, sourced by the
    galaxy scalar gradient varphi' (vanishes only when varphi'=0 -> recovers Eling-Jacobson vacuum).
    => A^r = (F_Q + 2 F_Y A^t Q0) varphi'/m_A^2  ~  varphi'/Q0  (small but NONZERO).
"""
import numpy as np
c=2.99792458e8; G=6.674e-11; Mpc=3.0857e22; kpc=3.0857e19; H0=67.4e3/Mpc
Z=2*np.sqrt(8*np.pi/3); a0=c*H0/Z
Q0=1.0/Mpc; varphi_p=a0/c**2; L_u=10*kpc
dtheta_per_u=c/(3*H0*L_u); dQ_per_u=varphi_p/Q0
R=dQ_per_u/dtheta_per_u

print("#"*100)
print("# FINAL -- AeST radial-tilt effect on BOTH carriers (theta=divA and Q=A.dphi)")
print("#"*100)
print(f"""
SCALES: a0={a0:.2e} m/s^2  3H0={3*H0:.2e}/s  Q0~mu~1/Mpc={Q0:.2e}/m  varphi'(MOND)~a0/c^2={varphi_p:.2e}/m

THE TWO EXPOSURES (fractional shift of each carrier per unit tilt A^r):
   d(theta/3H)/dA^r = c/(3H0 L_u)  = {dtheta_per_u:.2e}   <- HUGE (3H0 absurdly small)
   d(Q/Q0)/dA^r     = varphi'/Q0   = {dQ_per_u:.2e}   <- tiny (galaxy grad << cosmo scale)

CONVENTION-INDEPENDENT RATIO (tilt amplitude, m_A, F_Q, F_Y all cancel):
   R = (dQ/Q0)/(dtheta/3H) = varphi' 3H0 L_u/(Q0 c) = {R:.2e}
   => theta is ~{1/R:.0e}x MORE fragile than Q to ANY radial tilt. This is the load-bearing result.

DERIVED tilt A^r ~ varphi'/Q0 = {varphi_p/Q0:.1e} (galaxy MOND gradient / cosmological scalar scale):""")
Ar=varphi_p/Q0
print(f"   delta-theta/3H = {Ar*dtheta_per_u:.2e}    (theta: O(1)-few, NOT robustly pinned)")
print(f"   delta-Q/Q0     = {Ar*dQ_per_u:.2e}    (Q: PINNED to ~1e-9)")
print(f"""
PROMPT'S VIRIAL SCENARIO  A^r = v_vir/c = {150e3/c:.1e}:
   delta-theta/3H = {150e3/c*dtheta_per_u:.2e}    (theta SWAMPED by ~70x)
   delta-Q/Q0     = {150e3/c*dQ_per_u:.2e}    (Q PINNED to ~2e-8)

CROSSOVER tilts: theta breaks (shift=1) at A^r={1/dtheta_per_u:.1e} (~{c/dtheta_per_u:.0f} m/s drift);
                 Q breaks at A^r={1/dQ_per_u:.1e} (super-luminal -> Q UNBREAKABLE by physical tilt).

BOTH-WAYS PINCER on the aether mass m_A (the only knob that could pin theta):
   To pin theta you need m_A > 1/(132 kpc) -- a screening length SHORTER than a galaxy, which
   SCREENS OUT galaxy MOND (SZ require mu^-1 >~ 1 Mpc). So no m_A pins theta AND keeps MOND.
   Honest edge: at mu^-1~0.1-0.3 Mpc (marginal-MOND) theta is borderline (dtheta/3H~0.05-0.5);
   the theta verdict is 'order-unity uncertain', not 'swamped by many orders'.

GATE A (stability): m_A^2=(2-K_B)(1+lam_s)Q0^2/K_B > 0 for 0<K_B<2, lam_s>-1 (the GW170817+CMB
   window). So A^r=0 is a STABLE attractor (massive mode relaxes back); ghost-freedom of the spin-1
   tilt mode FORCES the tilt small -- but 'small' (~varphi'/Q0) is not small ENOUGH for theta given
   its 10^5 exposure. Stability pins the AMPLITUDE, not theta's fractional shift.

GATE B (boundary): turnaround radius (GM/H0^2)^{1/3} ~ 1-10 Mpc >> galaxy ~10-30 kpc, so the galaxy
   is DEEP INSIDE the static (Killing-aligned) region; theta=3H boundary value comes from the FRW
   exterior by matching. Correct asymptotics: theta -> 3H at the galaxy from OUTSIDE, perturbed
   INSIDE by the sourced tilt (the O(1) wobble above). Galaxy is on the STATIC side, not the
   transition shell.

VERDICT:
   * theta = div A : SWAMPED (more precisely: order-unity-shifted; NOT robustly pinned). A real,
     EOM-sourced, stable tilt of order varphi'/Q0 gives delta-theta/3H = O(1)-O(10) because 3H0 is
     so tiny. theta is NOT a reliable a0 carrier inside galaxies. [Moot for RISING -- dead at CMB.]
   * Q = A.dphi   : PINNED to ~1e-9 (virial: ~2e-8). The declining-branch covariant V(Q) fallback,
     which needs Q pinned to its cosmological Q0, is SAFE: Q is the ROBUST carrier, protected by
     Q0(cosmo) >> varphi'(galaxy) -- exactly because Q lives in the cosmological/time sector.

   => LABEL: SWAMPED-theta-only. The tilt swamps theta=div A but NOT Q. The declining V(Q) carrier
      survives; the rising theta=div A carrier does not (and was already dead at the CMB).
""")
print("#"*100)
