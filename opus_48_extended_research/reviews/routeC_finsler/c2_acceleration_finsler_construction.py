"""
Route C / step 2.  Build the ACCELERATION-dependent (higher-order Finsler / Lagrange)
free-particle action whose Euler-Lagrange equation IS the dS-Unruh MI trajectory.

Construction principle (this is the natural Finsler-of-2nd-order line element):
A higher-order Finsler / Kawaguchi structure has a "metric arc length"
    S = m c \int F(x, xdot, xddot) d\tau
homogeneous degree 1 in (xdot, xddot) jointly under reparametrization.  We seek the F
whose stationary curves reproduce  a*mu_fw(a/a0) = g_N  in the nonrelativistic, weak-field
limit.

We work in the nonrelativistic 1-D radial reduction first (the cleanest place to see the
structure and to test ghosts), then ask if it lifts.

KEY OBJECT: define the "dS-Unruh proper acceleration" scalar
    A = sqrt(a^2 + a_L^2),   a_L = c H_Lambda   (Deser-Levin effective temperature scalar)
The MI law a mu_fw(a/a0) = g_N with a0 = a_L * Z-relation... but for the EOM what matters is
the kinetic functional whose variation gives the LHS.  We REVERSE-ENGINEER it:

The MI EOM (1-D, free particle in potential Phi, per unit mass) is
    a * mu_fw(|a|/a0)  +  dPhi/dx = 0.
Question: is the LHS  a*mu_fw(|a|/a0)  the variational derivative of SOME local functional
of (x, xdot, xddot)?  i.e. does there exist L(xddot) (acceleration-only kinetic term) with
EL =  d^2/dt^2 (dL/d xddot)  ... that equals  a*mu_fw?  We test this directly.
"""
import sympy as sp

t = sp.symbols('t')
x = sp.Function('x')(t)
a0 = sp.symbols('a_0', positive=True)

xd  = sp.diff(x, t)        # velocity
xdd = sp.diff(x, t, 2)     # acceleration a
print("="*78)
print("STEP 2a.  Is a*mu_fw(|a|/a0) the EL derivative of a pure-acceleration L(xddot)?")
print("="*78)
print("""
For a higher-derivative Lagrangian L(x, xdot, xddot) the Euler-Lagrange equation is
   dL/dx - d/dt(dL/dxdot) + d^2/dt^2(dL/dxddot) = 0.
A pure-acceleration kinetic term L_kin = G(xddot) contributes  d^2/dt^2 (G'(xddot)) to EL.
For the MI inertial term to be  a*mu_fw(|a|/a0)  (NOT its second time derivative) we would
instead want L_kin to contribute the inertial term ALGEBRAICALLY.  That is impossible from
G(xddot): d^2/dt^2 (G'(a)) is a 4th-derivative object, never the algebraic a*mu_fw(a).
So a pure-acceleration kinetic term gives the WRONG derivative order. CONFIRMED below.
""")
a = sp.symbols('a', real=True)
G = sp.Function('G')
# contribution to EL from L=G(xddot):
contrib = sp.diff(G(xdd).diff(xdd), t, 2)
print("EL contribution of L=G(xddot):  d^2/dt^2(G'(a)) =")
sp.pprint(contrib)
print("\n  -> contains x'''' (4th derivative). The MI term a*mu_fw(a) is 2nd-derivative,")
print("     ALGEBRAIC in a.  A pure-acceleration Finsler kinetic term does NOT produce it.")

print()
print("="*78)
print("STEP 2b.  The CORRECT Finsler structure: velocity-Lagrangian that PRODUCES a*mu(a)")
print("          requires the inertial coefficient to be the EL *itself*, i.e. we need")
print("          d/dt(dL/dxdot) - dL/dx = a*mu_fw(a/a0).  Solve for L.")
print("="*78)
print("""
We need a (possibly higher-order) L with  EL[L] = a*mu_fw(|a|/a0).  Write the MI momentum:
the MI law in Milgrom's MI form (2208.07073) defines a kinetic momentum p such that
   dp/dt = a*mu_fw(a/a0)   would require p = \int mu_fw(a/a0) a dt  -- but that integral is
NONLOCAL in time (the integrand depends on the full a-history), which is EXACTLY Milgrom-94.

The cleanest LOCAL attempt: define the MI "kinetic energy density" K(a) by asking
   a*mu_fw(a/a0) = dK/da / (something)...
Try the ANSATZ that the EOM is the gradient of a function of a:  is there H(a) with
   dH/da = mu_fw(a/a0) * a   AND  the EOM = d/dt(dH/da-momentum)?  Test the integrability.
""")
# The MI 'force law' f(a) = a*mu_fw(a/a0).  Can it be written as the t-derivative of a
# local momentum p(a, v)?  p would have to satisfy dp/dt = f(a).  With p=p(v) (Finsler),
# dp/dt = p'(v) a.  So we'd need p'(v) a = a mu_fw(a/a0) => p'(v) = mu_fw(a/a0): LHS depends
# on v, RHS on a => impossible unless mu_fw is constant.  This is Step-2 again, sharper:
print("If p = p(v) (Finsler momentum), dp/dt = p'(v)*a.")
print("MI law needs dp/dt = a*mu_fw(a/a0) => p'(v) = mu_fw(a/a0):")
print("   LHS depends on v, RHS on a  => NO local Finsler momentum exists.")
print("   (Constant mu would be Newtonian.)  This is the Milgrom no-go, re-derived.")
print()
print("CONCLUSION 2: the MI inertial term is genuinely NONLOCAL-in-time (p = history")
print("integral of mu_fw(a)*a) OR requires acceleration as an INDEPENDENT jet coordinate.")
print("The latter is the generalized-Lagrange (Miron) route -> next file c3.")
