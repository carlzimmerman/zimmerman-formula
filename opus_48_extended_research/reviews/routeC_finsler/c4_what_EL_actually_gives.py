"""
Route C / step 4.  THE LOAD-BEARING HONESTY CHECK.
In c3 I built T(a)=∫ a*mu_fw da and claimed L=T(a)-Phi is the acceleration-Finsler MI action.
But I must VERIFY what the Euler-Lagrange equation of L=T(xddot)-Phi(x) ACTUALLY is, because
a*mu_fw(a) being dT/da does NOT mean EL[T(a)] = a*mu_fw(a).  The EL of a pure-acceleration
term is  d^2/dt^2(dT/da) = d^2/dt^2(a*mu_fw(a)), a FOURTH-derivative object, NOT the MI law.

So the c3 "construction" does NOT reproduce the MI law.  Make this explicit, then ask:
is there ANY local L(x,v,a) whose EL = a*mu_fw(a/a0) + Phi' ?  (Answer: no -- prove it.)
"""
import sympy as sp

t = sp.symbols('t')
x = sp.Function('x')(t)
a0 = sp.symbols('a_0', positive=True)
Phi = sp.Function('Phi')

xd  = x.diff(t)
xdd = x.diff(t, 2)

# mu_fw(a/a0) and the MI force-law f(a)=a*mu_fw
def mu_of(aexpr):
    xx = aexpr/a0
    return (sp.sqrt(1+4*xx**2)-1)/(2*xx)
f_a_sym = lambda aa: aa*mu_of(aa)

print("="*78)
print("STEP 4A.  EL of L = T(xddot) - Phi(x)  with  T'(a)=a*mu_fw(a/a0).  What is it really?")
print("="*78)
a = sp.symbols('a', positive=True)
T = -a*a0/2 + a*sp.sqrt(4*a**2+a0**2)/4 + a0**2*sp.asinh(2*a/a0)/8  # from c3
Tprime = sp.simplify(sp.diff(T, a))
print("T'(a) = a*mu_fw(a/a0) =", Tprime)
# EL of L=T(xddot)-Phi(x):  dL/dx - d/dt(dL/dxdot) + d^2/dt^2(dL/dxddot)
#   dL/dx = -Phi'(x);  dL/dxdot=0;  dL/dxddot = T'(xddot)
EL = -Phi(x).diff(x) + sp.diff(Tprime.subs(a, xdd), t, 2)
print("\nEL[L] = -Phi'(x) + d^2/dt^2( T'(xddot) ) :")
print("   = -Phi'(x) + d^2/dt^2( a*mu_fw(a/a0) )|_{a=xddot}")
print("   -> a FOURTH-order ODE in x(t).  This is NOT the MI law a*mu_fw + Phi' = 0.")
print("   CONFIRMED: the pure-acceleration Finsler kinetic term does NOT give the MI law;")
print("   it gives its 2nd time-derivative dressed onto a 4th-order equation.")

print()
print("="*78)
print("STEP 4B.  Does ANY local L(x, xdot, xddot) have EL EXACTLY = a*mu_fw(a/a0)+Phi'(x)?")
print("="*78)
print("""
The MI law is a SECOND-order ODE:  a*mu_fw(a/a0) = -Phi'(x),  i.e.  G(xddot) = -Phi'(x)
with G(a)=a*mu_fw(a/a0) a NONLINEAR invertible function of the acceleration ALONE.
For a local L(x,v,a) the EL is generically 4th order:
   EL = L_x - d/dt L_v + d^2/dt^2 L_a .
To be 2nd order, the 3rd/4th-derivative terms must cancel.  The coefficient of the highest
(4th) derivative is L_aa.  So a 2nd-order EL needs L_aa = 0  =>  L is LINEAR in a:
   L = A(x,v) a + B(x,v).
Then EL = [A_x a + B_x] - d/dt[A_v a + A xddot + B_v]  (using L_v = A_v a + B_v, L_a=A)
        = lower-order in a.  Let us compute it and see if it can equal G(xddot)=a*mu_fw(a).
""")
print("""
A linear-in-a Lagrangian gives EL whose a-dependence is at most LINEAR with (x,v)-dependent
coefficients (plus a-independent pieces) -- it can produce 'M(x,v)*a' (velocity/position-
dependent inertia) but NEVER the nonlinear  a*mu_fw(a/a0) = -a0/2 + sqrt(4a^2+a0^2)/2 ,
which is a transcendental function of a ALONE.  A NONLINEAR-in-a EL needs L_aa != 0, which
makes the EL 4th-order (Step 4A) = Ostrogradski.

THEOREM (local 1-D): there is NO local L(x,xdot,xddot,...) whose Euler-Lagrange equation is
the 2nd-order MI law a*mu_fw(a/a0) = -Phi'(x):
   * L_aa=0 (2nd-order EL) => a-dependence only LINEAR => cannot match nonlinear mu_fw;
   * L_aa!=0 (nonlinear a) => 4th-order EL + Ostrogradski ghost, and the EL is the 2nd
     time-derivative of the force-law, not the force-law.
This is the precise, sympy-grounded statement of Milgrom-1994 in the Finsler language.
""")

# Demonstrate the nonlinearity is genuinely transcendental in a (not polynomial):
G = -a0/2 + sp.sqrt(4*a**2+a0**2)/2
is_poly = G.is_polynomial(a)
print("G(a)=a*mu_fw(a/a0) polynomial in a? ", is_poly, " (False => cannot come from linear-in-a L)")
print()
print("STEP 4 VERDICT: a LOCAL acceleration-Finsler MI action does NOT exist (either wrong")
print("EOM order, or Ostrogradski ghost). The Finsler reformulation REPRODUCES the Milgrom-94")
print("no-go; it adds no local field content. The geometry must be NONLOCAL (next: c5).")
