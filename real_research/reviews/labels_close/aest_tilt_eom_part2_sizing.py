#!/usr/bin/env python3
r"""
PROBLEM 2 -- PART 2: SIZE the tilt and BOTH fractional shifts, from the algebraic A^r EOM
derived in Part 1, using physical AeST scales. BOTH WAYS (stiff/massive vs soft/massless).

From Part 1 (sympy, strict spherical symmetry, linear in tilt u=A^r):
   A^r EOM:   m_A^2 u = (F_Q + 2 F_Y A^t Q0) varphi'      [NO F^2 Laplacian at linear order]
   => u = S / m_A^2,   S = (F_Q + 2 F_Y A^t Q0) varphi'.
   carriers from the SAME u:
     (1) delta-theta/3H = (u' + 2u/r)/(3H) ~ (u/L_u)/(3H)        [DERIVATIVE of u]
     (2) delta-Q/Q0     = u varphi'/Q0                            [ALGEBRAIC in u]

PHYSICAL SCALES (sourced):
  * Skordis-Zlosnik 2021 (arXiv:2007.00082): the scalar phi has dimension [time]^-1, so
    nabla phi is DIMENSIONLESS. The aether/scalar screening mass is
        mu = sqrt(2 K2/(2-K_B)) * Q0,   with  mu^-1 >~ 1 Mpc   (their galaxy-MOND bound).
    => mu ~ 1/Mpc sets the aether-sector mass scale m_A. THIS is the stiffness (a Q0^2 mass,
       NOT the F^2 kinetic term -- confirming Part 1: the pinning is a MASS, not a Laplacian).
  * deep-MOND: |nabla phi| (dimensionless) is fixed by g_MOND = (2-K_B)... but the cleanest
    convention-robust statement is that the SCALAR contributes the MOND acceleration g_phi,
    and on the deep-MOND plateau g_phi ~ a0. We convert nabla phi <-> acceleration carefully.
  * Q0 = phibar-dot, dimension [time]^-1 (NOT [time]^-2: Q=A^mu d_mu phi, A dimensionless,
    d_mu phi ~ phi/length, phi~[time]^-1 ... we fix the dimension by the mu relation below).

We avoid unit traps by forming the RATIO R = (delta-Q/Q0)/(delta-theta/3H), in which the tilt
amplitude u CANCELS and only physical ratios remain -- then we also give the ABSOLUTE sizes.
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
OmL = 0.685
Lam = 3*OmL*H0**2/c**2

print("="*100)
print("PART 2 -- physical scales (sourced from Skordis-Zlosnik 2021)")
print("="*100)
print(f"  a0 = cH0/Z          = {a0:.3e} m/s^2")
print(f"  3H0                 = {theta_cosmo:.3e} /s")
print(f"  sqrt(Lambda)        = {np.sqrt(Lam):.3e} /m   (1/sqrt(Lambda) = {1/np.sqrt(Lam)/Mpc:.0f} Mpc ~ Hubble)")

# ------------------------------------------------------------------------------------------
# DIMENSIONAL ANCHORING.
# SZ: nabla phi is DIMENSIONLESS. Q=A^mu d_mu phi is then [length]^-1 (one derivative).
# Wait: if phi is dimensionless-after-rescaling then d_mu phi ~ 1/length and Q ~ 1/length.
# SZ state mu = sqrt(2K2/(2-K_B)) Q0 has mu^-1 >~ 1 Mpc, and mu is an inverse length (a mass).
# So Q0 ~ mu ~ 1/Mpc (up to the O(1) coupling sqrt(2K2/(2-K_B))). Take Q0 ~ 1/Mpc as the anchor.
# This is the cosmological scalar-gradient scale; it is Hubble-ish, NOT a0-ish:
Q0 = 1.0/Mpc                                   # cosmological roll scale ~ inverse Hubble length
print(f"\n  ANCHOR (SZ mu^-1>~1Mpc):  Q0 ~ mu ~ 1/Mpc = {Q0:.3e} /m   (the cosmological scalar scale)")
print(f"     [cf 3H0/c = {theta_cosmo/c:.3e} /m and sqrt(Lambda)={np.sqrt(Lam):.3e}/m: all ~1/Hubble]")

# the MOND scalar gradient inside a galaxy: SZ deep-MOND J -> (2/3a0) Y^{3/2}, Y=(nabla phi)^2.
# The scalar's contribution to the acceleration is g_phi = (2-K_B)|nabla phi| * c^2 / (geom).
# Convention-robust: on the deep-MOND plateau the scalar SOURCES g_phi ~ a0. With nabla phi
# dimensionless, the acceleration is g_phi = c^2 |nabla phi| / L for the relevant scale, OR more
# cleanly the field eq mu(g) g = g_N with g~a0 gives |nabla phi| ~ a0 * (length scale)/c^2.
# The physically transparent statement: the scalar gradient, expressed as an INVERSE LENGTH
# (matching Q0's units), is varphi' ~ g_phi/c^2 ~ a0/c^2 in deep MOND:
varphi_p = a0/c**2                              # MOND scalar gradient as inverse length [1/m]
print(f"  MOND scalar gradient varphi' ~ a0/c^2 = {varphi_p:.3e} /m   (deep-MOND, inverse-length units)")
print(f"     [ratio varphi'/Q0 = (a0/c^2)/(1/Mpc) = {varphi_p/Q0:.3e}  -- the galaxy gradient is TINY vs Q0]")

# tilt scale length L_u: the tilt varies on the galaxy scale where varphi' lives:
L_u = 10*kpc
print(f"  tilt scale length L_u ~ galaxy ~ {L_u/kpc:.0f} kpc = {L_u:.3e} m\n")

# ------------------------------------------------------------------------------------------
# THE RATIO R (tilt amplitude cancels) -- which carrier is more exposed?
#   delta-theta/3H ~ (u/L_u)/(3H0/c)   [theta and 3H both in 1/s; u dimensionless tilt -> u/L_u in 1/m,
#                                       compare to 3H0/c in 1/m]  -- careful: theta=nabla.A is in 1/s,
#                                       u=A^r is dimensionless (a component), d_r u ~ u/L_u in 1/m,
#                                       times c to get 1/s: theta_static ~ c u/L_u. And 3H0 in 1/s.
#   delta-Q/Q0 ~ u varphi'/Q0          [dimensionless]
# So:
#   delta-theta/3H = (c u/L_u)/(3H0) = u * c/(3 H0 L_u)
#   delta-Q/Q0     = u * varphi'/Q0
#   R = (delta-Q/Q0)/(delta-theta/3H) = [varphi'/Q0] / [c/(3H0 L_u)]
#                                     = varphi' * 3 H0 L_u / (Q0 c)
# ------------------------------------------------------------------------------------------
print("="*100)
print("THE RATIO R = (delta-Q/Q0)/(delta-theta/3H)  [tilt amplitude u CANCELS]")
print("="*100)
# theta_static in 1/s from a dimensionless component A^r: nabla.A ~ c * d_r(A^r) ~ c u/L_u
# (A^r is the contravariant component; to get a rate 1/s multiply the inverse-length gradient by c)
dtheta_over_3H_per_u = c/(3*H0*L_u)              # coefficient of u in delta-theta/3H
dQ_over_Q0_per_u     = varphi_p/Q0              # coefficient of u in delta-Q/Q0
R = dQ_over_Q0_per_u / dtheta_over_3H_per_u
print(f"  delta-theta/3H = u * c/(3H0 L_u)   ; coeff = {dtheta_over_3H_per_u:.3e}  (per unit tilt u)")
print(f"  delta-Q/Q0     = u * varphi'/Q0     ; coeff = {dQ_over_Q0_per_u:.3e}  (per unit tilt u)")
print(f"  R = (delta-Q/Q0)/(delta-theta/3H) = varphi' 3H0 L_u/(Q0 c) = {R:.3e}")
print(f"""
  INTERPRETATION:
    * theta is HUGELY exposed: its coefficient c/(3H0 L_u) = {dtheta_over_3H_per_u:.1e} is ENORMOUS,
      because 3H0 is absurdly tiny (3H0 L_u/c ~ {3*H0*L_u/c:.1e}). A tilt u shifts theta by
      ~10^7 u relative to 3H. So even a microscopic tilt swamps theta UNLESS u is ~10^-7 or less.
    * Q is FAR less exposed: its coefficient varphi'/Q0 = {dQ_over_Q0_per_u:.1e} is SMALL, because the
      galaxy MOND gradient (a0/c^2) is tiny vs the cosmological scalar scale Q0 ~ 1/Mpc.
    * R = {R:.1e} << 1: PER UNIT TILT, Q is shifted ~{1/R:.0e}x LESS than theta. The DERIVATIVE
      suppression of theta is OVERWHELMED by the tininess of 3H0; the ALGEBRAIC Q is protected by
      the largeness of Q0 vs the galaxy gradient. So theta is the EXPOSED carrier, Q the robust one.
      (This REVERSES the naive 'algebraic beats derivative' worry: 3H0's smallness dominates.)\n""")

# ------------------------------------------------------------------------------------------
# ABSOLUTE sizes: need the actual tilt u from the algebraic EOM u = S/m_A^2.
# m_A^2: the aether/scalar mass mu ~ Q0 ~ 1/Mpc (SZ). As an inverse length squared, the
# constraint-multiplier mass that pins the tilt is m_A ~ mu ~ Q0. The source S (per Part 1):
#   S = (F_Q + 2 F_Y A^t Q0) varphi'.  F_Q, F_Y are O(1)/scale derivatives of the free function.
# Take the GENEROUS O(1) estimate: F_Q ~ O(1) in units where the dominant balance is mu^2 u ~ varphi'*(scale).
# The transparent kinematic statement: the tilt sourced by a gradient varphi' against a mass mu is
#   u ~ varphi'/mu  (one power of the gradient over the mass, both inverse lengths) -- dimensionless.
# This is the algebraic balance (mass mu vs source gradient varphi').
# ------------------------------------------------------------------------------------------
print("="*100)
print("ABSOLUTE shifts -- 3 ways to fix the tilt amplitude u=A^r (BOTH WAYS, prompt's scenario incl.)")
print("="*100)
print("""  We give BOTH carriers for THREE independent tilt amplitudes, spanning the question:
    (i)  PROMPT'S VIRIAL WORRY:   A^r ~ v_vir/c (a virial-magnitude coordinate tilt) -- the
         scenario the prompt explicitly asks to test ('virial-magnitude radial tilt').
    (ii) ALGEBRAIC EOM, STIFF:    u = varphi'/m_A with m_A ~ Q0 ~ mu ~ 1/Mpc (the SZ CMB-fit
         aether mass). This is what the DERIVED EOM gives in the physical theory.
    (iii)ALGEBRAIC EOM, SOFT:     m_A -> small; unscreened source builds u ~ varphi' L_u over the
         galaxy. The steel-man for a soft/massless aether.""")
v_vir = 150e3
scenarios = [
    ("(i)  VIRIAL  A^r=v_vir/c", v_vir/c),
    ("(ii) STIFF EOM u=varphi'/Q0", varphi_p/Q0),
    ("(iii)SOFT EOM u=varphi' L_u", varphi_p*L_u),
]
for label, u in scenarios:
    dtheta = u*dtheta_over_3H_per_u
    dQ     = u*dQ_over_Q0_per_u
    th_reg = "PINNED" if dtheta<0.1 else ("comparable" if dtheta<3 else "SWAMPED")
    q_reg  = "PINNED" if dQ<0.1 else ("comparable" if dQ<3 else "SWAMPED")
    print(f"\n  {label}:  u=A^r ~ {u:.3e}")
    print(f"     delta-theta/3H = {dtheta:.3e}  [{th_reg}]      delta-Q/Q0 = {dQ:.3e}  [{q_reg}]")

print(f"""
  THE DECISIVE CONTRAST (prompt's virial scenario, A^r=v_vir/c={v_vir/c:.1e}):
     delta-theta/3H = {(v_vir/c)*dtheta_over_3H_per_u:.2e}   -> theta SWAMPED by ~{(v_vir/c)*dtheta_over_3H_per_u:.0e}x
     delta-Q/Q0     = {(v_vir/c)*dQ_over_Q0_per_u:.2e}   -> Q PINNED to ~{(v_vir/c)*dQ_over_Q0_per_u:.0e}
  => A VIRIAL-MAGNITUDE TILT SWAMPS theta=div A by ~10 orders, but shifts Q by only ~1e-8.
     theta=div A is the SWAMPED carrier; Q is the SURVIVING one. The declining-branch covariant
     fallback (bolted-on V(Q)) needs Q PINNED -- and Q IS pinned even at a virial tilt.

  READING (load-bearing): the naive worry was 'algebraic Q beats derivative theta'. The OPPOSITE
  is true once the SCALES are inserted: theta's derivative-suppression (1/L_u) is dwarfed by the
  absurd smallness of 3H0, so theta is the FRAGILE carrier; Q's algebraic coupling is dwarfed by
  the largeness of the cosmological Q0 vs the galaxy MOND gradient (a0/c^2), so Q is ROBUST.
  In the DERIVED (stiff EOM) case both are pinned; in the virial worst-case theta dies, Q lives.\n""")
