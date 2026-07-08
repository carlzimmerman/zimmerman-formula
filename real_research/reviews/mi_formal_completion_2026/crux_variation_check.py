#!/usr/bin/env python3
r"""
CRUX CROSS-CHECK (corrected): the kinetic QUADRATIC FORM for the u-perturbation.

Q = u^mu u^a grad_a(u^b grad_b u_mu), u = ubar + eps V (CONSTANT amplitude V, plane wave e^{i k.x}
so grad -> i k). We want the O(eps^2) piece of Q that is the KINETIC quadratic form  V^mu M_{mu nu}(k) V^nu.
Because everything is O(eps^2) and carries exactly two factors of the SINGLE perturbation V, we can
take V CONSTANT (amplitude) and each grad -> i k_a. Then Q is a pure polynomial in (ubar, V, k), and
its eps^2 part IS the quadratic form. We extract the symmetric matrix M_{mu nu}(k), then ask:
   is M_{mu nu} V^nu = 0 for ALL V on the constraint surface (ubar.V = 0)?
If yes -> no propagating u kinetic term (transverse spin-1 + spin-0 both non-dynamical) -> u passive.
If no  -> a transverse u-mode propagates -> u promoted to a dynamical dof -> crux FAILS.

This is the HONEST test. We do it in full 4-D.
"""
import sympy as sp

# 4-D Minkowski eta = diag(-1,1,1,1). Plane wave: u^mu = ubar^mu + eps V^mu e^{i k.x}, grad_a -> i k_a.
eta = sp.diag(-1,1,1,1)
ub = sp.Matrix(sp.symbols('ub0 ub1 ub2 ub3', real=True))
V  = sp.Matrix(sp.symbols('V0 V1 V2 V3', real=True))
k  = sp.Matrix(sp.symbols('k0 k1 k2 k3', real=True))
eps = sp.symbols('eps')
I = sp.I

# u^mu (upper), u_mu (lower):
Uup = ub + eps*V           # amplitude form (the e^{i k.x} carried implicitly; grad->i k)
Udn = eta*Uup              # lower index

def raise_dot(a,b):  # a^mu b_mu with both given as upper-index columns
    return (a.T*eta*b)[0,0]

# grad_a of (upper-index component field f^mu) with f = fbar + eps Vf e^{ikx}: grad_a f = eps (i k_a) Vf.
# We build Box_u acting on a LOWER scalar component u_mu = Udn[mu].
# (u^b grad_b) f  where f is a scalar field carried by the perturbation:
#   for the BACKGROUND part of u^b: contributes ubar^b (i k_b) (eps V_f)
#   for the eps part of u^b:        contributes eps V^b (i k_b)(...) -> O(eps^2) already if f is O(eps)
# We need Q to O(eps^2). Track eps carefully by symbolic expansion.

# Represent each scalar's spacetime dependence by (i k_a) per gradient acting on the eps-part ONLY
# (the background is constant). Implement grad on an expression that is a polynomial in eps with
# vector coefficients: grad_a picks the eps-part and multiplies i k_a. Since only the eps*V pieces
# depend on x, grad_a(Uup[mu]) = eps V[mu]*(i k_a);  grad_a(background)=0.

def grad(expr_vec_component, a):
    # expr is linear in eps (has an eps-part = the plane-wave); grad = i k_a * (eps-part)
    epart = sp.expand(expr_vec_component).coeff(eps,1)
    return I*k[a]*eps*epart

# u^b grad_b (scalar f):
def Du(f):
    return sum(Uup[b]*grad(f,b) for b in range(4))
# but Du(f) is now O(eps): (ubar^b + eps V^b)(i k_b eps f_pert) = i k_b ubar^b eps f_pert + O(eps^2)
# Box_u f = u^a grad_a( Du(f) ). Du(f) is O(eps); grad of it picks its eps^1 coeff * i k_a:
def Boxu(f):
    df = Du(f)
    return sum(Uup[a]*grad(df,a) for a in range(4))

# Q = sum_mu Uup[mu] * Boxu( Udn[mu] )
Q = 0
for mu in range(4):
    Q += Uup[mu]*Boxu(Udn[mu])
Q = sp.expand(Q)
Q2 = sp.expand(Q.coeff(eps,2))    # the O(eps^2) quadratic form (kinetic + lower-deriv all mixed;
                                  # but by construction Boxu already carried the 2 gradients -> this
                                  # IS the 2-derivative quadratic form V M(k) V)
Q2 = sp.simplify(Q2)
print("O(eps^2) two-derivative quadratic form  V^mu M_{mu nu}(k) V^nu :")
print("  Q2 =", Q2)

# Build the symmetric matrix M_{mu nu} from Q2 = sum_{mu<=nu} coeff * V_mu V_nu.
M = sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        if mu==nu:
            M[mu,nu] = Q2.coeff(V[mu],2)
        else:
            # coefficient of V_mu V_nu (split evenly for symmetry)
            c = sp.expand(Q2).coeff(V[mu],1).coeff(V[nu],1)
            M[mu,nu] = c/2
M = sp.simplify(M)
print("\nSymbol matrix M_{mu nu}(k) (symmetric):")
sp.pprint(M)

# --- Does M annihilate transverse perturbations (ubar.V = 0)?  Compute M V for general V, then
#     restrict to ubar.V=0 and ubar.ubar=-1, and see if M V lies purely along ubar (longitudinal),
#     i.e. the PHYSICAL (transverse) projection of the kinetic term vanishes.
MV = sp.simplify(M*V)
print("\nM.V (general) =")
sp.pprint(MV)

# Transverse projector P = eta + ubar ubar^T (raising) restricted; work with the scalar test:
# physical kinetic content on transverse modes = V_perp^T M V_perp. Parametrize V transverse:
# choose ubar timelike rest frame ubar=(1,0,0,0) (ubar.ubar=-1). Then transverse V = (0, V1,V2,V3).
subs_rest = {ub[0]:1, ub[1]:0, ub[2]:0, ub[3]:0}
M_rest = sp.simplify(M.subs(subs_rest))
print("\nM in the ubar rest frame ubar=(1,0,0,0):")
sp.pprint(M_rest)
# transverse block = rows/cols 1..3 (spatial); longitudinal = 0-0 component.
Vt = sp.Matrix([0, V[1], V[2], V[3]])
transverse_kinetic = sp.simplify((Vt.T*M_rest*Vt)[0,0])
print("\nTRANSVERSE kinetic form  V_perp^T M V_perp (rest frame) =", transverse_kinetic)
long_kinetic = sp.simplify((sp.Matrix([V[0],0,0,0]).T*M_rest*sp.Matrix([V[0],0,0,0]))[0,0])
print("LONGITUDINAL kinetic form (V0 only)                    =", long_kinetic)

print("""
VERDICT LOGIC:
  * If TRANSVERSE kinetic form == 0  -> the spin-1 (and spin-0 transverse) u-modes have NO kinetic
    term -> they do NOT propagate. The only nonzero kinetic structure is LONGITUDINAL (along ubar),
    which the unit-norm constraint u.u=-1 (=> ubar.V=0 => V0=0 in rest frame) FREEZES.
    => u carries NO physical propagating kinetic term. u stays PASSIVE. CRUX = WIN.
  * If TRANSVERSE kinetic form != 0 -> a transverse u-mode propagates -> u is promoted to a
    dynamical dof. CRUX = FAIL.
""")
print("DONE. exit 0.")
