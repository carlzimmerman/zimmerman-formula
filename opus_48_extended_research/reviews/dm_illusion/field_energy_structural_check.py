#!/usr/bin/env python3
r"""
field_energy_structural_check.py  (topic: dark_sector_is_field_energy)
======================================================================
The ONE fresh structural calc the task demands: is the AeST K(Q) a^-3
"dark-matter-mimic" component genuinely the SCALAR FIELD's own energy
density (kinetic energy of the shift-symmetric scalar phi redshifting as
dust), NOT a particle? And: is the amount (I0 ~ Omega_dm) pinned by sqrt(Lambda)?

We do NOT re-derive; we VERIFY the structural facts already banked, sympy-clean,
so the "field not particle" claim in part (a) is checked on its own terms, and the
honest line (part b: the CMB still needs that energy) and the Verlinde re-exam
(part c) are stated against the actual stress-energy structure.

Quarantine held: a0/Z/kappa NOT asserted derived. Both-ways.

Primary source (verified verbatim in prior session vs ar5iv):
  Skordis & Zlosnik 2021, PRL 127 161302 = arXiv:2007.00082.
"""
import sympy as sp

print("="*78)
print("(1) IS THE a^-3 COMPONENT THE SCALAR FIELD'S OWN ENERGY DENSITY? (structural)")
print("="*78)
# AeST scalar sector (shift-symmetric in phi, i.e. depends on Q = u^mu d_mu phi and
# Y=|grad phi|^2). On FLRW the field is homogeneous phi=phi(t), so Q = phidot/N (the
# field's TIME-derivative = its canonical "velocity"), Y=0. The scalar Lagrangian is
#   L_phi = (1/8 pi Gtilde) [ K(Q) ]   with K = -2 Lambda + K2 (Q-Q0)^2 + ...
# This is a k-essence / shift-symmetric scalar: NO mass term in phi itself (only in Q),
# NO particle excitations counted -- the "density" is the field's stress-energy T^0_0.

t = sp.symbols('t', positive=True)
a = sp.Function('a', positive=True)(t)
Q = sp.Function('Q')(t)          # Q = phidot/N  (the scalar's velocity invariant)
I0, Q0, K2, Lam = sp.symbols('I0 Q0 K2 Lambda', real=True)

# Shift symmetry phi -> phi + const => a conserved Noether current for phi.
# Its EOM on FLRW integrates ONCE to:   a^3 * K'(Q) = I0   (the shift charge).
# => K'(Q) = I0 / a^3.  This is the banked PRL result.
Kp = I0/a**3                      # = dK/dQ, the conserved shift current density
print("  shift-symmetric scalar  => conserved current:  a^3 K'(Q) = I0")
print("  => K'(Q) = I0 / a^3   (the integration constant I0 = the shift charge)")

# The scalar's ENERGY DENSITY (its T^0_0). For a k-essence L=L(Q) with Q=phidot/N,
# the canonical energy density is  rho_phi = Q * dL/dQ - L = Q*K'(Q) - K   (up to the
# -2Lambda piece which is the dark-ENERGY part). The DUST piece is the Q*K'(Q) term:
rho_dust = Q*Kp                    # = Q * I0 / a^3
print("\n  scalar energy density (dust piece):  rho_dust = Q * K'(Q) = Q * I0 / a^3")
# Near the K-minimum Q -> Q0 (slow drift), so:
rho_dust_today = Q0*I0/a**3
print(f"  near Q->Q0:  rho_dust = Q0 * I0 / a^3   => 8 pi Gtilde rho_dust0 = Q0*I0")
# CHECK the redshift law: d/dt of (rho_dust * a^3) with rho ~ a^-3 => pressureless (w=0).
rho = sp.Function('rho')(t)
cons = sp.diff(rho*a**3, t)        # continuity for w=0 dust:  rho a^3 = const
sol = sp.dsolve(sp.Eq(sp.diff(rho,t) + 3*sp.diff(a,t)/a*rho, 0), rho)
print(f"\n  continuity (w=0):  d/dt(rho) + 3 (adot/a) rho = 0  =>  {sol.rhs}  (~ a^-3) CONFIRMED")
print("""
  STRUCTURAL VERDICT (a): the a^-3 component IS the shift-symmetric SCALAR FIELD's
  OWN energy density T^0_0 = Q*K'(Q) (the field's kinetic/velocity energy in Q),
  carried by a CLASSICAL FIELD configuration -- NOT a gas of particles. There is:
    - NO mass term for phi (shift symmetry forbids it) => NO particle rest mass,
    - NO thermal momentum distribution => NO free-streaming, NO Tremaine-Gunn floor,
    - w=0, c_s^2 ~ 0 sub-horizon => it CLUSTERS like cold dust by construction.
  So 'no WIMP -- it is the gravitational scalar's field energy' is STRUCTURALLY TRUE
  in the embedding. The CDM-mimic is field energy density, not a particle species.
""")

print("="*78)
print("(2) IS THE AMOUNT (I0 -> Omega_dust) PINNED BY sqrt(Lambda)? -> NO (banked, re-shown)")
print("="*78)
# Lambda enters K ONLY as the additive constant -2 Lambda. It does NOT appear in K'(Q):
K_full = -2*Lam + K2*(Q - Q0)**2
Kp_full = sp.diff(K_full, Q)
print(f"  K(Q) = -2 Lambda + K2 (Q-Q0)^2 + ...   =>  K'(Q) = {Kp_full}")
print(f"  d/dLambda [ K'(Q) ] = {sp.diff(Kp_full, Lam)}   <-- Lambda DROPS OUT of the current")
print("""  => a^3 K'(Q)=I0 holds for ANY I0 regardless of Lambda: d(rho_dust)/dLambda = 0.
     I0 is an INTEGRATION CONSTANT (an initial datum), orthogonal to the bulk coupling
     Lambda. a0 = c^2 sqrt(Lambda/32pi) lives in the Y-sector (Y^3/2), absent from FRW
     (Y=0) => a0 provably absent from linear perturbations (Bridge-1). So sqrt(Lambda)
     CANNOT set the field-energy AMOUNT. Omega_dust ~ Omega_dm ~ 0.26 is a TUNED
     why-now coincidence, NOT a derivation. [field DERIVED as energy; AMOUNT free]
""")

print("="*78)
print("(3) THE HONEST LINE (b): the CMB 3rd peak REQUIRES this energy density")
print("="*78)
# Banked CAMB 1.6.6 monotone (reproduced prior session): P3/P2 vs Omega_c h^2.
import numpy as np
omh2 = np.array([0.000, 0.060, 0.120, 0.180])
P3P2 = np.array([0.527, 0.793, 0.980, 1.118])
print("  P3/P2 vs the a^-3 clustering field density (real CAMB 1.6.6, banked):")
for x,y in zip(omh2,P3P2):
    tag = " <- baryon/MI-only: 3rd peak CRUSHED" if x==0 else (" <- Planck (observed ~0.98)" if abs(x-0.12)<1e-9 else "")
    print(f"    Omega_field h^2={x:.3f}  ->  P3/P2={y:.3f}{tag}")
print("""  => Planck observes P3/P2~0.98 -> REQUIRES Omega_field h^2 ~ 0.12 of a COLD,
     a^-3-clustering energy density. 'Literally nothing there' is FORBIDDEN by data.
     The defensible 'dark matter is an illusion' = NO PARTICLE (it is the gravitational
     scalar's field energy), NOT 'the missing-mass data is illusory'. Honest line held.
""")

print("="*78)
print("(4) THE VERLINDE RE-EXAM (c): does 'field energy' revive elastic back-reaction?")
print("="*78)
print("""  Verlinde's 'apparent DM = de Sitter ELASTIC back-reaction to baryons' makes the
  dark sector a DEFORMATION SOURCED BY the baryons (rho_D ~ f(rho_baryon), the
  'spacetime's memory of displaced dS entropy'). The AeST field energy is the OPPOSITE
  structure on three counts:
    (i) INDEPENDENT amplitude. rho_dust = Q0*I0/a^3 has its OWN free integration
        constant I0; it is NOT a functional of the baryon distribution. Verlinde's
        rho_D IS a functional of M_baryon (g_D = sqrt(a0 g_B /6) form). Different objects.
    (ii) CLUSTERS. Verlinde under-predicts cluster mass (residual ~2-3x, Bullet offset);
         AeST's INDEPENDENT a^-3 dust supplies whatever Omega the data want (~0.25), and
         can sit OFFSET from the gas (it is its own field, free to not track baryons) --
         which is exactly why AeST passes the CMB+clusters where Verlinde fails.
    (iii) MECHANISM. The framework's OWN dS back-reaction calc (routeD_backreaction_crux.py)
          shows the dS vacuum is KMS-PASSIVE: integrating it out gives inertia RISING with a
          = ANTI-MOND, and the self-consistent T_eff(a) walks the wrong way. So treating the
          dark sector as the framework's field energy does NOT revive Verlinde -- it REPLACES
          the (dead) elastic-response mechanism with an INDEPENDENT cold scalar condensate.
  => Verlinde stays DEAD (fails clusters/RC + KMS-passive); the field-energy reading is a
     DIFFERENT, working structure (independent amplitude, can offset baryons, fits CMB).
     Banked guardrail HONORED: the elastic back-reaction mirage is NOT revived.
""")
print("DONE. Quarantine held; both-ways; no manufactured derivation.")
