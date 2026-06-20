#!/usr/bin/env python3
"""
adversarial_break_orthogonality.py  (2026-06-19)

ADVERSARIAL pass on 'one_field_both_roles': take the STRONG illusion claim seriously
and try as hard as possible to TIE a0 to the dust amount via ONE field, the way a
believer would. If any of these works, the orthogonality verdict is overturned and the
illusion thesis gets a real one-number win. If all fail, the orthogonality is robust.

We test FOUR believer moves, each the best version of 'one field, ONE origin':
  (A) A Y-Q CROSS TERM in F(Y,Q) ties the spatial (a0) and temporal (dust) sectors.
  (B) GHOST-CONDENSATE rigidity: the SAME K2 (mass) that sets the dust pressure also
      sets the MOND interpolation, so a0 and dust share K2.
  (C) dS-Unruh DERIVES K(Q) (not just K(Y)) so I0 is fixed by Lambda after all.
  (D) The Verlinde 'apparent DM = dS elastic back-reaction' revival: a0-driven response
      IS the dust (one mechanism). [Guardrail: banked mirage -- confirm still dead.]
"""
import sympy as sp
import numpy as np

print("="*78)
print("ADVERSARIAL: try to TIE a0 to the dust amount (break orthogonality)")
print("="*78)

# -----------------------------------------------------------------------------
# (A) Y-Q cross term
# -----------------------------------------------------------------------------
print("\n--- (A) Believer move: a Y*Q cross term in F(Y,Q) couples the sectors ---")
Y, Q, a, t = sp.symbols('Y Q a t', positive=True)
print("""
Suppose F(Y,Q) = K(Q) + J(Y) + g_c * Y * Q  (a cross coupling g_c).
On FRW, Y = q^00 (dphi)^2 with q^00 = g^00 + A^0 A^0 = -1 + 1 = 0  EXACTLY
  (A is unit-timelike and aligned with the FRW normal). So Y|_FRW = 0 identically.
=> ANY term with a positive power of Y vanishes on the homogeneous background:
   g_c * Y * Q |_FRW = 0.  The cross term cannot shift the background dust.
""")
qup00 = sp.symbols('qup00')
# demonstrate q^00 = 0 in rest frame
g00 = -1; A0up = 1
q00 = g00 + A0up*A0up
print(f"  q^00 = g^00 + A^0 A^0 = {g00} + {A0up*A0up} = {q00}   -> Y|_FRW = q^00 (phidot)^2 = 0")
print("""
  At the LINEAR perturbation level: delta Y = 2 q^0i_pert dphi0 dphi_i + ... is first
  order in the SPATIAL gradient of phi, which is itself a perturbation -> delta(Y*Q) is
  SECOND order in perturbations. The dust delta(rho) that builds the 3rd peak is FIRST
  order. So a Y*Q cross term contributes only at second (nonlinear) order -> cannot
  source the linear clustering, cannot tie I0 to a0.  (This is exactly why Skordis-
  Zlosnik say a0 'plays a role once NONLINEAR terms kick in' -- nonlinear, not the
  linear dust.)
VERDICT (A): cross term does NOT break orthogonality at the background or linear level.
""")

# -----------------------------------------------------------------------------
# (B) shared K2 (ghost condensate mass)
# -----------------------------------------------------------------------------
print("--- (B) Believer move: the SAME K2 sets BOTH the dust AND a0 ---")
print("""
Ghost condensate (Arkani-Hamed et al): K(Q) = -2Lambda + K2 (Q-Q0)^2 gives dust+CC.
The dust amplitude is 8piGtilde rho0 = Q0*I0 -- it does NOT contain K2 at leading order
(K2 sets the sound speed / mass mu^2 ~ K2, i.e. the CLUSTERING SCALE, not the amount).
a0 sits in the Y-sector coefficient [2 lam_s/(3(1+lam_s) a0)] -- a DIFFERENT coefficient
of a DIFFERENT (Y) term. There is no AeST relation K2 = f(a0): Verwayen-Skordis-Zlosnik
2024 treat mu (hence K2) as 'a free parameter in this work', pinned by rotation-curve
EXTENT, not by a0. And the data pull K2 OPPOSITE ways (galaxy-WL wants m^2/f_G<1 Mpc^-2,
clusters want >1) -- the signature of a FREE constant, not a0-locked.
VERDICT (B): K2 is free and even if shared would set the dust SCALE (mu), never the
dust AMOUNT (I0); does not tie a0 to how-much-dark-matter. Orthogonality holds.
""")

# -----------------------------------------------------------------------------
# (C) dS-Unruh derives K(Q)
# -----------------------------------------------------------------------------
print("--- (C) Believer move: dS-Unruh DERIVES K(Q), so Lambda fixes I0 ---")
print("""
dS-Unruh delivers: T_eff = (1/2pi) sqrt(a^2 + (cH_Lam)^2)  (Deser-Levin) -> the Y-sector
sqrt-law and the a0 SCALE. This is a STATIC response along a worldline (an INERTIA law).
The Q-sector dust is a COSMOLOGICAL energy density set by an INITIAL DATUM I0 (the
displacement of phi from Q0 at early times). dS-Unruh thermodynamics acts on the
worldline RESPONSE; it has no channel to set a cosmological initial condition.
Concretely: dK/dQ = I0/a^3 is the FIRST INTEGRAL of the shift-symmetric EOM; I0 is the
constant of integration. No bulk coupling (Lambda, a0, Z) is a constant of integration;
they are Lagrangian parameters. A thermodynamic identity on couplings cannot output an
integration constant -- a category separation, not a numerology miss.
Cross-check (already in one_field_both_roles.py): no dS combo of {Lambda,a0,Z,OmDE}
hits Omega_dust/Omega_DE=0.387 within ~19% w/o a tuned O(1).
VERDICT (C): dS-Unruh derives the Y-sector FORM + a0 scale, NOT the Q-sector K(Q)/I0.
""")

# -----------------------------------------------------------------------------
# (D) Verlinde elastic-backreaction revival
# -----------------------------------------------------------------------------
print("--- (D) Believer move: Verlinde-style 'apparent DM = dS back-reaction' (one mech) ---")
# Quantitative re-kill on clusters and RC shape (banked mirage; confirm dead).
# Verlinde 2016/17 apparent dark mass: M_D^2(r) = (a0 r^2 /(6 G)) * d(M_b r)/dr  (his Eq.)
# Two banked failures: (i) needs LOWERED M/L and predicts an unobserved radius-correlated
# RAR residual; (ii) fails clusters (under-predicts the cluster missing mass by ~2-3x and
# gives the wrong PROFILE). Also a0=cH0/6 (wrong footing, 1/6 != 1/Z=1/5.789).
a0 = 9.36e-11
G = 6.674e-11
Msun = 1.989e30
Mpc = 3.086e22
# Illustrative cluster: M_b ~ 1e14 Msun within r~1 Mpc; observed dynamical ~6x baryons.
Mb = 1e14*Msun
r = 1.0*Mpc
# Verlinde apparent dark mass (spherical, M_b roughly constant in r at the outskirt):
# M_D ~ sqrt(a0 * r^2 * M_b /(6 G))   (taking d(M_b r)/dr ~ M_b)
M_D = np.sqrt(a0 * r**2 * Mb /(6*G))
print(f"  Cluster toy: M_b={Mb/Msun:.2e} Msun, r=1 Mpc")
print(f"  Verlinde apparent dark mass M_D = {M_D/Msun:.2e} Msun  (ratio M_D/M_b={M_D/Mb:.2f})")
print(f"  Observed cluster missing factor ~5-6x baryons; Verlinde gives ~{M_D/Mb:.1f}x -> UNDER by ~{6/(M_D/Mb):.1f}x.")
print("""
  Plus the banked RC failures: Lelli-McGaugh-Schombert 2017 (SPARC): Verlinde EG needs
  IMPLAUSIBLY LOW M/L and predicts a radius-correlated RAR residual NOT seen; a0=cH0/6 is
  the wrong (cH0) footing and 1/6 != 1/Z. Dai-Stojkovic 2017 recover Newton (derivation
  contested). The cluster PROFILE is also wrong.
VERDICT (D): Verlinde elastic-back-reaction route stays a DEAD MIRAGE -- it neither fits
  clusters nor the RC shapes, and conflicts with the framework's own a0 footing.
  NOT revived. (Guardrail honored.)
""")

print("="*78)
print("ADVERSARIAL NET: orthogonality of a0 (Y-sector) and dust I0 (Q-sector) is ROBUST.")
print("All four believer moves to tie one field's two roles to ONE origin/number FAIL:")
print("  (A) Y*Q cross term -> 0 on FRW + 2nd order in perts (Skordis's 'nonlinear only')")
print("  (B) shared K2 -> sets dust SCALE not AMOUNT, and is free + data-squeezed")
print("  (C) dS-Unruh derives Y-form/a0, NOT the Q-sector integration constant I0")
print("  (D) Verlinde back-reaction -> still dead on clusters + RC shapes (mirage held)")
print("="*78)
print("""
=> ONE FIELD: YES (field content). ONE ORIGIN/NUMBER: NO (robust under adversarial push).
   The strong illusion claim survives only as 'dark matter is a MODE of the framework's
   own field' (no particle), NOT as 'a0 and the dark amount share a derived origin'.
""")
