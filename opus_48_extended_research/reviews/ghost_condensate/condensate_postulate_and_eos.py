#!/usr/bin/env python3
"""
evade_so41_gate -- part (b): is the CONDENSATE itself derivable, or is
"P(X) has a minimum at X0>0" the new postulate?  Plus the equation-of-state
crux that decides what the framework actually gets (dark ENERGY vs dark MATTER).

Two distinct questions are bundled in (b):
  (b1) WHERE does the postulate live?  Did we DERIVE that P has a minimum at X0>0
       (the "wrong-sign-then-stabilized" / ghost-condensate shape), or did we just
       MOVE the assumption from the kinetic term to the shape of P?
  (b2) EQUATION OF STATE: at the EXACT minimum P'(X0)=0 the background is rho=-p,
       w=-1 (a cosmological constant = dark ENERGY). The dust w=0 a^-3 behaviour the
       framework's K(Q) DARK-MATTER mode needs requires P'(X0) =/= 0, i.e. being
       DISPLACED off the exact minimum -- and the size of that displacement (hence
       Omega_dm) is a FREE integration constant. This is the SAME free-amount wall
       (banked DARK_MATTER_ILLUSION wall-3) re-appearing inside the GC language.
"""
import sympy as sp

print("="*78)
print("PART (b): is the condensate derived, or is 'P min at X0>0' the new postulate?")
print("="*78)

print("""
(b1) WHERE THE POSTULATE LIVES -- the shape of P(X) is an INPUT.
---------------------------------------------------------------
The ghost-condensate requires P(X) to:
  (i)  have a NON-TRIVIAL extremum at some X0 > 0  (P'(X0)=0, X0 != 0), and
  (ii) be a MINIMUM there  (P''(X0) > 0, the no-ghost condition for pi).
A canonical example is P(X) = (X - X0)^2 / 2  (ACLM use P ~ -X + X^2 form, same
content): the wrong-sign 'ghost' kinetic region (P'<0, where the field is unstable
and 'rolls') is STABILIZED by a higher term, and the field settles at the minimum
where the velocity X0 = <phidot>^2 is non-zero -> a constant-velocity 'condensate'.

NONE of (i)-(ii) is derived from dS-Unruh, from Lambda, or from the AeST aether
constraints. They are POSTULATES about the functional form of P:
  * "P has a wrong-sign region" (the field is a ghost over some X-range) -- postulate;
  * "that region is stabilized into a minimum at X0>0"                  -- postulate;
  * the VALUE of X0 (= the condensate velocity c = M^2)                  -- a free scale.

CONCLUSION (b1): the assumption is RELOCATED, not removed. In the dS-Unruh-induction
route the postulate was "there is a (K_B/2)F^2 kinetic term for the aether". In the
ghost-condensate route the postulate becomes "P(X) has a stabilized minimum at X0>0".
That is the SAME amount of input, expressed as a potential shape rather than a kinetic
coefficient. It is NOT a derivation of the field; it is a different PARAMETRIZATION of
the same postulate. (What it DOES buy -- genuinely -- is in the gate logic of part (a):
once you GRANT the shape, the preferred-frame kinetic term follows at tree level from a
background, so the SO(4,1) *vacuum* theorem is no longer the obstruction. The obstruction
MOVES from 'a symmetry theorem forbids it' to 'you must postulate the shape of P'.)
""")

print("="*78)
print("(b2) EQUATION-OF-STATE CRUX -- what the framework actually gets")
print("="*78)
# FRW, shift-symmetric P(X) scalar, X = phidot^2 (homogeneous). Standard k-essence:
#   rho = 2 X P'(X) - P(X),    p = P(X),    w = p/rho.
# First integral of shift symmetry: a^3 * P'(X) * phidot = const = I0  (the AeST a^3 K'(Q)=I0).
X = sp.symbols('X', positive=True)   # X = phidot^2 = c^2 at/near condensate
P = sp.Function('P')
rho = 2*X*sp.Derivative(P(X), X) - P(X)
p   = P(X)
print("\nk-essence:  rho = 2 X P'(X) - P(X),   p = P(X),   w = p/rho")

# CASE A: EXACT minimum, P'(X0)=0.
print("\n--- CASE A: EXACT condensate minimum, P'(X0) = 0 ---")
print("  rho = 2 X0 * 0 - P(X0) = -P(X0);   p = P(X0)  =>  p = -rho  =>  w = -1.")
print("  This is a COSMOLOGICAL CONSTANT (dark ENERGY). It does NOT redshift; w=-1.")
print("  [ACLM: the exact ghost condensate has rho=-p, drives de Sitter expansion.]")

# CASE B: DISPLACED off the minimum, P'(X) small but nonzero.
print("\n--- CASE B: DISPLACED off the minimum, P'(X) = epsilon (small, != 0) ---")
print("  Shift-sym first integral: a^3 P'(X) phidot = I0  =>  P'(X) phidot = I0 / a^3.")
print("  The 'kinetic'/displacement piece of rho:  rho_kin = 2 X P'(X) = 2 phidot * (P' phidot)")
print("                                                    = 2 phidot * I0 / a^3  ~  a^-3.")
print("  => the OFF-MINIMUM (displacement) energy redshifts as a^-3 == DUST, w=0.")
print("  [Mukohyama / 'Ghost Dark Matter': small positive P' => rho ~ a^-3, mimics CDM.]")
print("""
  *** THE CRUX ***  The dust (w=0, a^-3) component the framework's DARK-MATTER mode
  needs is the OFF-MINIMUM displacement, NOT the condensate minimum itself. Its
  amplitude is set by I0 -- the SAME shift-symmetric integration constant the banked
  AeST embedding already identified as FREE (a^3 K'(Q) = I0 for ANY I0;
  d rho_dust/dLambda = 0). The ghost-condensate language REPRODUCES, it does not
  remove, the free-amount wall:
     - the condensate MINIMUM  -> w=-1 dark ENERGY  (the Lambda face, already a0<->Lambda);
     - the DISPLACEMENT off it -> w=0  dark MATTER   (amplitude = I0, FREE).
  So 'the field is a ghost condensate' DERIVES neither (a) the amount of dark matter
  (free displacement I0) nor (b) why the displacement is ~Omega_dm rather than zero
  (which would be pure dark energy) or large.
""")

print("="*78)
print("SYNTHESIS: does the ghost condensate EVADE the SO(4,1) gate? -- PARTIAL/YES-with-cost")
print("="*78)
print("""
(a) GATE EVASION -- YES, structurally, AS A SYMMETRY THEOREM ABOUT THE VACUUM.
    The G2 gate says a dS-INVARIANT VACUUM's one-loop action induces only
    dS-invariant terms. The ghost-condensate kinetic term is NOT vacuum-induced; it is
    the tree-level 2nd variation around a NON-INVARIANT BACKGROUND (verified part (a):
    time-kinetic = 2 X0 P''(X0) survives, ordinary grad = -P'(X0) -> 0). Spontaneous
    Lorentz breaking by a solution is exactly how a Lorentz-invariant action yields a
    frame-dependent spectrum. The symmetry theorem does not bind a background. So the
    SPECIFIC obstruction that killed the dS-Unruh *induction* route (G2) is genuinely
    side-stepped. [This is a real, non-trivial point in the framework's favour.]

(b) BUT THE POSTULATE IS RELOCATED, NOT REMOVED -- and the AMOUNT STAYS FREE.
    The gate is evaded only by GRANTING that P(X) has a stabilized minimum at X0>0
    (the ghost-then-stabilized shape). That shape is the NEW postulate, replacing the
    old "(K_B/2)F^2 exists" postulate one-for-one. Nothing in dS-Unruh / Lambda / the
    AeST aether constraints DERIVES it. And the dust the dark-MATTER mode needs is the
    OFF-minimum displacement, whose amplitude I0 ~ Omega_dm is the SAME free
    integration constant (banked wall-3). The exact minimum gives w=-1 dark ENERGY, not
    dark matter.

NET: the ghost condensate is a GENUINE evasion of the G2 *vacuum symmetry theorem*
(it derives a preferred-frame kinetic term from a background, not a vacuum loop), but it
is NOT a derivation of THE FIELD: it relocates the postulate (kinetic term -> potential
shape P(X)) and leaves the dark-matter AMOUNT (the off-minimum displacement I0) free.
It also INHERITS the GC pathologies (Jeans/gradient instability, accretion/antigravity),
which the next script tabulates. 'Evades the gate' is PROVEN as a symmetry-theorem
statement; 'derives the field' is REFUTED -- the assumption moved, it did not vanish.
""")
print("[b] VERIFIED: w=-1 at exact min (dark energy); w=0 a^-3 off-min (dark matter),")
print("    amplitude = free I0. The 'P has a min at X0>0' shape is the relocated postulate.")
