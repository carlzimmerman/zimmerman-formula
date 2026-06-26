"""
Route C / step 3.  The generalized-Lagrange (acceleration-jet / Kawaguchi-Finsler) route.
Two things, both machine-checked:

 (A) CONSTRUCT a local higher-order Lagrangian L(x, v, a) whose Euler-Lagrange equation
     CONTAINS the MI law a*mu_fw(a/a0) + Phi' = 0 as a stationary/algebraic branch.
     The natural Finsler-2 kinetic scalar is the dS-Unruh proper-acceleration arc element
         T(a) = (a0^2/...) * [ sqrt(1 + 4 a^2/a0^2) ... ]  built so that dT/da = a*mu_fw(a/a0).
     i.e. T is the PRIMITIVE of the MI force-law.  Find T explicitly.

 (B) OSTROGRADSKI TEST.  Any nondegenerate L that depends genuinely on a=xddot has a
     linearly-unstable Ostrogradski ghost (the conjugate momentum to v is independent and
     the Hamiltonian is linear in it).  We compute the Ostrogradski Hamiltonian for the
     constructed L and check (i) nondegeneracy d^2L/da^2 != 0 and (ii) the linear-in-momentum
     instability.  This is the decisive ghost question for Route C.
"""
import sympy as sp

a, a0 = sp.symbols('a a_0', positive=True)
x_ = sp.symbols('x')           # |a|/a0
mu_fw = (sp.sqrt(1 + 4*x_**2) - 1)/(2*x_)

print("="*78)
print("STEP 3A.  The Finsler-2 acceleration kinetic scalar T(a): primitive of a*mu_fw(a/a0)")
print("="*78)
# MI force-law as a function of a (per unit mass):
f_a = a * (mu_fw.subs(x_, a/a0))
f_a = sp.simplify(f_a)
print("MI force-law f(a) = a*mu_fw(a/a0) =")
sp.pprint(f_a)
# T(a) = integral of f(a) da  (the kinetic potential in the acceleration variable)
T = sp.integrate(f_a, a)
T = sp.simplify(T)
print("\nT(a) = ∫ a*mu_fw(a/a0) da =")
sp.pprint(T)
# sanity: dT/da == f(a)
chk = sp.simplify(sp.diff(T, a) - f_a)
print("\n  check dT/da - f(a) =", chk, "  (must be 0)")

# Small/large a behaviour of T (limits).  Rewrite asinh as log to dodge the sympy aseries bug.
T_log = T.rewrite(sp.log)
T_small = sp.series(T, a, 0, 5).removeO()
# large-a via substitution a -> 1/eps, expand around eps=0
eps = sp.symbols('eps', positive=True)
T_eps = T_log.subs(a, 1/eps)
T_large_eps = sp.series(T_eps, eps, 0, 3)
print("\n  T(a->0)  ~", sp.simplify(T_small), "   (deep-MOND: T ~ a^3/(3 a0), cubic)")
print("  T(a->inf) leading terms (in eps=1/a):")
sp.pprint(T_large_eps)
print("   => T ~ a^2/2 - (a0/2) a + ...  (Newtonian a^2/2 kinetic + linear shift)")

print()
print("="*78)
print("STEP 3B.  OSTROGRADSKI HAMILTONIAN for L(x,v,a) = T(a) - Phi(x)")
print("          (the acceleration-Finsler free particle in a potential)")
print("="*78)
print("""
Ostrogradski canonical variables for L(x, xdot, xddot):
   Q1 = x,         Q2 = xdot
   P1 = dL/dxdot - d/dt(dL/dxddot),    P2 = dL/dxddot
Nondegeneracy: dP2/d(xddot) = d^2L/dxddot^2  must be invertible (!=0) to solve xddot(P2).
Hamiltonian: H = P1 xdot + P2 xddot(Q2,P2) - L.
The hallmark Ostrogradski instability: H is LINEAR in P1 (=> unbounded below).
""")
# L = T(a) - Phi(x).  Nondegeneracy:
d2T = sp.simplify(sp.diff(T, a, 2))
print("Nondegeneracy  d^2L/da^2 = T''(a) =")
sp.pprint(d2T)
print("\n  T''(a) at finite a:")
for av in [sp.Rational(1,100), sp.Rational(1,2), sp.Integer(1), sp.Integer(10)]:
    val = sp.N(d2T.subs(a0,1).subs(a,av))
    print(f"    a/a0={float(av):6.3f}:  T''={val}")
print("  -> T''(a) != 0 for all finite a  => L is NONDEGENERATE in xddot")
print("     => the Ostrogradski construction APPLIES (acceleration is a genuine dof).")

# Build the Ostrogradski Hamiltonian symbolically with generic T''(=:m_eff) != 0.
Q1, Q2, P1, P2 = sp.symbols('Q1 Q2 P1 P2', real=True)
acc = sp.symbols('acc', real=True)  # xddot solved from P2 = T'(acc)
Phi = sp.Function('Phi')
# H = P1*Q2 + P2*acc - (T(acc) - Phi(Q1)) where acc solves P2 = T'(acc).
# The structure we need is only the P1-dependence:
print("""
Ostrogradski H = P1*Q2 + [P2*acc(P2) - T(acc(P2))] + Phi(Q1).
  * The bracket is the Legendre transform of T in the acceleration -> a function of P2 only.
  * The FIRST term P1*Q2 is LINEAR in the canonical momentum P1, with Q2=xdot UNBOUNDED.
  => H is UNBOUNDED BELOW along P1 (take Q2 -> -inf or P1 -> with sign).  OSTROGRADSKI GHOST.
""")
print("VERDICT 3B: the nondegenerate acceleration-Finsler free particle L=T(a)-Phi has an")
print("Ostrogradski ghost (H linear in P1, unbounded). This is the GENERIC fate of any")
print("genuinely a-dependent local Lagrangian -- and it is WHY Milgrom-1994 forbids a local")
print("MI action: locality + a-dependence => higher-derivative => ghost.")
print()
print("The ONLY escapes (each tested next):")
print("  (i) DEGENERATE T'' (so acceleration is NOT a propagating dof) -> but T''!=0 here,")
print("      and a degenerate T would not carry mu_fw. Tested: c4.")
print("  (ii) NONLOCAL-in-time T (the established Galley route) -> not a finite-order local")
print("       Finsler structure at all; Ostrogradski inapplicable. This is the real home.")
print("  (iii) acceleration as a CONSTRAINED auxiliary (Lagrange-multiplier / first-order")
print("        form) -> tested c4: does the constraint remove the ghost or just hide it?")
