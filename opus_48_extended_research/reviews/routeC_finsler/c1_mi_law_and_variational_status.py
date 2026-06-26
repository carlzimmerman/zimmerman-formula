"""
Route C / step 1. Establish the MI law precisely and ask the FIRST honest question:
is the dS-Unruh MI EOM  m a mu_fw(|a|/a0) = F  derivable from a LOCAL point-particle
Lagrangian L(x, xdot)?  This is the Milgrom-1994 no-go territory.  A Finsler structure
is, by definition, a LOCAL Lagrangian L(x, xdot) homogeneous degree-1 in xdot.  So if the
MI law is NOT a local-L Euler-Lagrange equation, no ordinary Finsler structure can produce
it, and we must go to a generalized (acceleration-dependent / Lagrange / nonlocal) geometry.

Everything machine-checked in sympy.
"""
import sympy as sp

print("="*78)
print("STEP 1.  The dS-Unruh MI law and its interpolation function")
print("="*78)

x = sp.symbols('x', positive=True)  # x = |a|/a0
# Framework interpolation (modified-inertia reading):
mu_fw = (sp.sqrt(1 + 4*x**2) - 1)/(2*x)
print("mu_fw(x) =", mu_fw)

# Newtonian limit x->inf : mu_fw -> 1
lim_inf = sp.limit(mu_fw, x, sp.oo)
print("  mu_fw(inf) =", lim_inf, "  (Newtonian: m a = F)")
# deep-MOND limit x->0 : mu_fw -> x
lim0 = sp.series(mu_fw, x, 0, 2).removeO()
print("  mu_fw(x->0) ~", lim0, "  (deep-MOND: m a^2/a0 = F)")

# Check the algebraic content: the MI law  a*mu_fw(a/a0) = g_N  inverts to the
# dS-Unruh g_obs = sqrt(g_N^2 + g_N a0).  Verify.
gN, a0, a = sp.symbols('g_N a_0 a', positive=True)
# MI law (per unit mass): a * mu_fw(a/a0) = gN
mi_lhs = a * ((sp.sqrt(1 + 4*(a/a0)**2) - 1)/(2*(a/a0)))
mi_lhs = sp.simplify(mi_lhs)
print("\n  a*mu_fw(a/a0) =", mi_lhs, "  (set = g_N)")
# Solve for a in terms of gN
sol = sp.solve(sp.Eq(mi_lhs, gN), a)
print("  solve a:", sol)
gobs_target = sp.sqrt(gN**2 + gN*a0)
for s in sol:
    diff = sp.simplify(s - gobs_target)
    print("   candidate a =", sp.simplify(s), " ; a - sqrt(gN^2+gN a0) =", diff)

print("\n  => the MI law a*mu_fw(a/a0)=g_N is EXACTLY equivalent to")
print("     a = g_obs = sqrt(g_N^2 + g_N a0).  CONFIRMED." )

print()
print("="*78)
print("STEP 2.  Is m a mu_fw(|a|/a0) = F an Euler-Lagrange eq of a LOCAL L(x,xdot)?")
print("="*78)
print("""
For a NON-relativistic point particle a local Lagrangian L(x, v) gives EL:
   d/dt(dL/dv) - dL/dx = 0  ->  M(v) a + (...) = -dPhi/dx
The inertial coefficient multiplying the acceleration is the Hessian
   M_ij(v) = d^2 L / dv_i dv_j   (the 'mass matrix'), a function of VELOCITY only.
The dS-Unruh MI needs the inertial coefficient to be a function of the ACCELERATION
magnitude |a| (through mu_fw(|a|/a0)).  A velocity-Hessian can NEVER depend on a.
Therefore NO local L(x,v) reproduces it.  This is the kinematic core of Milgrom-1994.
""")

# Demonstrate concretely: try the most general isotropic local L(v) = f(v^2/2) (1 dof radial).
v = sp.symbols('v', real=True)
f = sp.Function('f')
L = f(v**2/2)
# EL inertial coefficient = d^2L/dv^2
M = sp.diff(L, v, 2)
print("For L = f(v^2/2):  d^2L/dv^2 =", sp.simplify(M))
print("  -> depends on v only (f' + v^2 f''), NEVER on the acceleration a.")
print("  CONFIRMED: no velocity-Lagrangian Hessian can carry mu_fw(|a|/a0).")

print()
print("="*78)
print("STEP 3.  Milgrom-1994 no-go, stated precisely for the Finsler question")
print("="*78)
print("""
Milgrom 1994 (astro-ph/9303012): a Galilei-invariant, LOCAL action for a particle whose
EOM is m a mu(a/a0)=F does NOT exist; the MI theory must be either NONLOCAL in time or
break Galilei invariance.  Reason: Galilei invariance forbids the action from depending on
the (frame-dependent) velocity in a way that yields an a-dependent inertia at the two-
derivative level; building a-dependence requires HIGHER derivatives, which by Galilean
boost can only enter through invariant combinations that are TOTAL TIME DERIVATIVES at the
needed order unless the action is nonlocal.

CONSEQUENCE FOR FINSLER (the honest framing of Route C):
  * An ORDINARY Finsler structure F(x, xdot), homogeneous degree 1 in xdot, is a LOCAL
    velocity-Lagrangian.  By Step 2 it CANNOT carry a(|a|/a0)-dependent inertia.  So
    ordinary Finsler is FORECLOSED for the MI law by the same no-go.
  * The only Finsler-type geometries that could carry acceleration-dependence are the
    GENERALIZED ones whose 'line element' depends on xddot (xdot, xddot):  these are the
    Finsler-of-higher-order / 'Lagrange' / Kawaguchi (areal/k-jet) geometries.  Those are
    HIGHER-DERIVATIVE Lagrangians -> Ostrogradski ghost risk, the next thing to test.
""")
print("STEP-1/2/3 done.  Next: build the higher-order (acceleration) Finsler structure.")
