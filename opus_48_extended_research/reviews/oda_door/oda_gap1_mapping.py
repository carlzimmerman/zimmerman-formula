#!/usr/bin/env python3
"""
ODA GAP-1 ORIGIN TEST (2026-06-19)
==================================
Does Ichiro Oda, arXiv:2509.23648 ("Emergence of General Relativity from
Cosmological Constant Via Ghost Condensation"), DERIVE the framework's GAP-1
origin -- i.e. the FORM of the Q-sector kinetic term K(Q)=mu^2(Q-1)^2 (a
ghost-condensate P(X) with a stabilized minimum at X0>0) FROM the
cosmological constant Lambda?

Three head-on checks, sympy where the mapping is checkable:

  (1) FORM:  does Oda's <cbar c> condensate produce a P(X) = K(Q)=mu^2(Q-1)^2
             -shaped bosonic scalar kinetic function with a stabilized minimum
             at X0>0, or a different / EH-only structure?

  (2) TRANSMIT: does the chain reach the MOND / preferred-frame sector
             (J(Y), a0 = c^2 sqrt(Lambda/32pi), the aether u^mu), or stop at
             Einstein-Hilbert GR?

  (3) COEFFICIENT: does the condensate VEV fix the framework's coefficient
             kappa=1/2 / Z=sqrt(32pi/3) -- and if it APPEARS to, is that
             circular (Oda's O(1)'s free / inherited)?

QUARANTINE: kappa is PROVABLY UNFORCEABLE (banked KAPPA_FORCING_DOOR_CLOSED).
Any "Oda fixes the coefficient" claim is scrutinized HARD for circularity.
"""

import sympy as sp

print("="*78)
print("ODA arXiv:2509.23648  vs  ZIMMERMAN GAP-1  --  head-on mapping")
print("="*78)

# ---------------------------------------------------------------------------
# CHECK 1: THE FORM.
#   Framework Q-sector:  K(Q) = mu^2 (Q-1)^2  (ACLM bosonic ghost condensate)
#   Oda's object:        <cbar c> != 0  (FP anticommuting gauge-ghost bilinear)
# Are these the same KIND of object? Build both and compare structure.
# ---------------------------------------------------------------------------
print("\n--- CHECK 1: does Oda generate the FORM K(Q)=mu^2(Q-1)^2 ? ---")

Q, mu = sp.symbols('Q mu', real=True, positive=True)
KQ = mu**2 * (Q-1)**2                       # framework Q-sector (Verwayen-Skordis-Zlosnik Eq.7)
KQp  = sp.diff(KQ, Q)
KQpp = sp.diff(KQ, Q, 2)
Q0 = sp.solve(sp.Eq(KQp, 0), Q)[0]          # minimum location
print(f"  Framework K(Q)        = {KQ}")
print(f"  K'(Q)                 = {sp.simplify(KQp)}   -> minimum at Q0 = {Q0}")
print(f"  K''(Q0)               = {KQpp.subs(Q,Q0)}  ( = 2*mu^2 > 0  => stabilized minimum, NO ghost )")
print(f"  => This is a P(X)-type BOSONIC scalar with a non-trivial minimum at X0=Q0>0.")

# Oda's bilinear: the ACTION that contains the FP ghost is, from Eq.(2.10):
#   S_q = int sqrt(-g) [ Btilde R + lambda phi^4 - 6 i cbar box c ]
# The ghost kinetic term is STANDARD: -6 i cbar (box) c  (a quadratic, RIGHT-sign
# d'Alembertian kinetic term for an ANTICOMMUTING field c). There is NO function
# K(.) of a derivative-VEV-scalar; there is no wrong-sign-then-stabilized P(X).
# Symbolically the "condensate" is just a CONSTANT VEV of the bilinear:
oda_cbar_c_VEV = sp.symbols('cbarc_VEV')    # = <cbar c>, a NUMBER (Eq.3.1)
G = sp.symbols('G', positive=True)
oda_condensate_condition = sp.Eq(2*sp.I*oda_cbar_c_VEV, 1/(16*sp.pi*G))  # Eq.(3.1)
print(f"\n  Oda condensate (Eq.3.1): {oda_condensate_condition}")
print(f"  Oda ghost kinetic term (Eq.2.10): -6 i * cbar * (box) c   [STANDARD right-sign quadratic, anticommuting]")
print("  => <cbar c> is a CONSTANT bilinear VEV of FERMIONIC FP gauge ghosts.")
print("     There is NO function K(.) of a scalar, NO derivative VEV <(d phi)^2>=X0,")
print("     NO wrong-sign-then-stabilized minimum.  It is NOT a P(X).")

print("\n  STRUCTURAL COMPARISON")
print("  " + "-"*60)
print(f"  {'property':<34}{'framework K(Q)':<16}{'Oda <cbar c>'}")
print("  " + "-"*60)
rows = [
 ("field statistics",        "bosonic scalar",  "fermionic (anticommuting)"),
 ("object type",             "P(X) function",   "constant bilinear VEV"),
 ("kinetic sign structure",  "wrong-then-stab", "standard right-sign"),
 ("minimum at X0>0",         "YES (Q0=1)",      "N/A (no P(X))"),
 ("Lorentz/diff breaking",   "spont. (frame)",  "Weyl gauge-fix (BRST)"),
 ("lives in",                "PHYSICAL spectrum","UNPHYSICAL (BRST quartet)"),
 ("propagating dof",         "1 scalar (dark)", "0 (confined, removed)"),
]
for a,b,c in rows:
    print(f"  {a:<34}{b:<16}{c}")
print("  " + "-"*60)
print("  VERDICT 1: Oda does NOT generate the FORM K(Q)=mu^2(Q-1)^2.")
print("             Different object class (boson P(X) vs fermion bilinear VEV).")
print("             'ghost condensate' is a FALSE COGNATE across the two.")

# ---------------------------------------------------------------------------
# CHECK 2: TRANSMIT. What is Oda's OUTPUT action, and does it contain ANY of
# the framework's MOND/preferred-frame ingredients?
#   Final Oda action (Eq.3.5):  S = int sqrt(-g) [ (1/16piG) R + lambda phi^4 ]
# ---------------------------------------------------------------------------
print("\n--- CHECK 2: does Oda TRANSMIT to the MOND / preferred-frame sector ? ---")
lam, phi = sp.symbols('lambda phi', positive=True)
R = sp.symbols('R', real=True)
oda_final = sp.Rational(1)/(16*sp.pi*G)*R + lam*phi**4   # Eq.(3.5) Lagrangian density (mod sqrt-g)
print(f"  Oda final Lagrangian (Eq.3.5):  L = {oda_final}")
print("  Degrees of freedom: exactly 2 (graviton). Oda's own text (p.6):")
print("    'f(R) gravity cannot be derived and only Einstein's general")
print("     relativity can be induced' -- the gauge R=0 is chosen so that")
print("     even an R^2/scalaron is EXCLUDED.")
needed = ["propagating dark scalar phi (Q/Y modes)",
          "J(Y) MOND interpolation function",
          "a0 = c^2 sqrt(Lambda/32pi) scale",
          "preferred frame / aether u^mu",
          "disformal / Lorentz-violating structure"]
print("\n  Framework MOND/preferred-frame ingredients PRESENT in Oda Eq.3.5?")
for n in needed:
    print(f"    [ NO ]  {n}")
print("  Oda STRUCTURALLY EXCLUDES the extra propagating scalar (R=0 kills f(R) scalaron).")
print("  VERDICT 2: NO transmission. Output is pure EH GR + a residual lambda*phi^4")
print("             cosmological term. No channel to MOND / a0 / preferred frame.")

# ---------------------------------------------------------------------------
# CHECK 2b: Is Lambda even CONSUMED? Trace Lambda through the chain.
#   S0 (Eq.2.1) = (Lambda/16piG) Vol     [Lambda present]
#   Sc (Eq.2.2) = lambda int sqrt-g phi^4 ; gauge phi=v with lambda v^4=Lambda/16piG
#   Final (Eq.3.5) = (1/16piG) R + lambda phi^4   [lambda phi^4 STILL THERE]
# The EH term's coefficient 1/16piG comes from <cbar c> (Eq.3.1), NOT from Lambda.
# ---------------------------------------------------------------------------
print("\n--- CHECK 2b: is Lambda CONSUMED/CONVERTED into the EH term ? ---")
v = sp.symbols('v', positive=True)
Lam = sp.symbols('Lambda', positive=True)
gauge_match = sp.Eq(lam*v**4, Lam/(16*sp.pi*G))     # Eq.(2.2) gauge phi=v reproduces (2.1)
print(f"  Weyl-rewrite gauge (Eq.2.2->2.1):  {gauge_match}")
print("  So lambda*phi^4 IS the Weyl-covariantized Lambda. It SURVIVES into Eq.3.5.")
# The EH coefficient:
eh_coeff_from_condensate = sp.Eq(sp.Symbol('EH_coeff'), 2*sp.I*oda_cbar_c_VEV)  # = 1/16piG, from Eq.3.1
print(f"  EH coefficient = 2i<cbar c> = 1/16piG   (Eq.3.1 condensate VEV)")
print("  => The R term is generated by the FP-GHOST VEV, NOT transmuted FROM Lambda.")
print("     Lambda persists intact as lambda*phi^4 alongside the new R term.")
print("  VERDICT 2b: 'EH from Lambda' headline is really 'EH from the FP-ghost")
print("              condensate, ALONGSIDE a still-present Lambda'. Lambda not consumed.")

# ---------------------------------------------------------------------------
# CHECK 3: COEFFICIENT. Does Oda fix the framework's kappa=1/2 / Z=sqrt(32pi/3)?
# Oda fixes 1/16piG = the EH/Planck normalization via the POSTULATED VEV.
# Map: framework a0 = kappa c^2 sqrt(Lambda)/sqrt(8pi); at kappa=1/2, Z=sqrt(32pi/3).
# Does Oda's chain touch kappa, Z, or a0? Test the dimensional content.
# ---------------------------------------------------------------------------
print("\n--- CHECK 3: does Oda FIX the coefficient kappa=1/2 / Z=sqrt(32pi/3) ? ---")
kappa, c = sp.symbols('kappa c', positive=True)
# framework relations (banked):
a0_expr = kappa * c**2 * sp.sqrt(Lam) / sp.sqrt(8*sp.pi)
Z_expr  = 2*sp.sqrt(6)*sp.sqrt(sp.pi)/(3*kappa)
print(f"  Framework:  a0   = {a0_expr}")
print(f"              Z    = {Z_expr}")
print(f"              at kappa=1/2:  Z = {sp.simplify(Z_expr.subs(kappa, sp.Rational(1,2)))}  (= sqrt(32pi/3))")
chk = sp.simplify(Z_expr.subs(kappa, sp.Rational(1,2)) - sp.sqrt(sp.Rational(32,3)*sp.pi))
print(f"              check  Z(1/2) - sqrt(32pi/3) = {chk}  (0 => identity holds)")

# What Oda's VEV pins:
print("\n  What Oda's condensate VEV (Eq.3.1) pins:")
print("    2i<cbar c> = 1/16piG   ->  fixes NEWTON's CONSTANT G_N (EH normalization).")
print("  Is G_N in {kappa, Z, a0}?  ")
print("    a0 = kappa c^2 sqrt(Lambda/32pi)  -- depends on Lambda & kappa, NOT on G alone.")
print("    (Note rho_DE = Lambda c^2/(8 pi G) DOES carry G, but a0 = kappa c sqrt(G rho_DE)")
print("     = kappa c^2 sqrt(Lambda/8pi) -- the G CANCELS. a0 is G-INDEPENDENT.)")
# show the G-cancellation explicitly:
rho_DE = Lam*c**2/(8*sp.pi*G)
a0_via_rho = kappa*c*sp.sqrt(G*rho_DE)
print(f"\n    a0 via density route = kappa c sqrt(G rho_DE) = {sp.simplify(a0_via_rho)}")
print(f"    -> G has CANCELLED. So pinning G (Oda's only output) does NOT touch a0.")

# Is the value 1/16piG forced, or postulated/dimensional?
print("\n  Is even G_N genuinely DERIVED by Oda?  NO:")
print("    - <cbar c> at coincident points is ILL-DEFINED (Eq.3.2 limit, conceded).")
print("    - regularization 'beyond the scope of this article'.")
print("    - 1/16piG ASSUMED by DIMENSIONAL matching ('no other scales owing to")
print("      scale invariance' -> Planck scale). It is a postulated O(1)xPlanck VEV.")
print("  => Oda's free O(1) (the magnitude of <cbar c>) is fit to GIVE 1/16piG.")
print("     This is structurally IDENTICAL to the banked CKN circularity: the O(1)")
print("     is CHOSEN to land the target, not derived. Even if one tried to read a")
print("     'kappa' out of it, the choice that lands it IS the input (circular).")
print("\n  VERDICT 3: Oda does NOT fix kappa=1/2 / Z / a0.")
print("    - Only G_N is pinned, and only by a postulated, admittedly ill-defined VEV.")
print("    - a0 is G-INDEPENDENT, so pinning G is a0-IRRELEVANT.")
print("    - Any 'kappa from Oda' reading would be CIRCULAR (free O(1) chosen to land")
print("      the target), consistent with banked KAPPA_FORCING_DOOR_CLOSED.")

# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("SUMMARY  (Oda vs GAP-1)")
print("="*78)
print("  (1) FORM K(Q)=mu^2(Q-1)^2 from Lambda?      NO  (fermion bilinear, not boson P(X))")
print("  (2) TRANSMIT to MOND / a0 / pref-frame?     NO  (pure EH GR; scalar EXCLUDED)")
print("  (3) FIX kappa=1/2 / Z / a0?                 NO  (pins G only; a0 is G-indep;")
print("                                                   any kappa-read is CIRCULAR)")
print("  => GAP-1 stays POSTULATED-not-DERIVED. Door returns NOT-FORCED.")
print("     Joins Door D (Mersini-Houghton) and the dead dS-Unruh SO(4,1) route.")
print("     Oda is at most a distant MECHANISM ANALOGY ('a condensate VEV can make a")
print("     kinetic/EH term from a Lambda-only start'), undercut by the boson/fermion")
print("     mismatch and the GR-only / scalar-EXCLUDING output.")
print("="*78)
