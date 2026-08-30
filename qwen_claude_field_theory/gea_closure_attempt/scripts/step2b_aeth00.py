"""
Step 2b: Compute the aether contribution to the 00 weak-field equation.

The aether Lagrangian L_aeth = sqrt(-g) M^2 F(K) depends on g^{00} AND
d_i g^{00} (through nabla_i u^0).  The Euler-Lagrange equation wrt g^{00}
therefore produces second-derivative (nabla^2 Psi) terms.  This is what makes
the coefficient of nabla^2 Psi equal to mu(y) rather than the bare Einstein
value.

We work in the static weak-field limit:
   g_00 = -(1+2Psi),  g_ij = (1-2Phi) delta_ij,  g_0i = 0.
We express everything in terms of g00 and gii (and their derivatives),
compute L_aeth, and take the Euler-Lagrange equation wrt g00 (equivalently
g^{00}).  We keep F_K as a parameter 'fk' and use F = fk*K (dropping F(0)).

Conventions: signature (-,+,+,+), c=1.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
coords = [t, x, y, z]
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
M = sp.symbols('M', positive=True)
fk = sp.symbols('fk', real=True)   # F_K (treated as a parameter)

# Metric potentials as functions
P = sp.Function('P')(t, x, y, z)   # = Psi
Q = sp.Function('Q')(t, x, y, z)   # = Phi

# Use g00, gii as the independent variables.
g00 = -(1 + 2*P)
gii =  (1 - 2*Q)
ginv00 = 1/g00
ginvii = 1/gii
sqrtg = sp.sqrt(-g00*gii**3)

# aether (time aligned): u_mu = (-1,0,0,0)
# u^0 = g^{00} u_0 = -g^{00}
u0 = -ginv00

# nabla_i u^0 = d_i u^0 + Gamma^0_{i0} u^0
# Gamma^0_{i0} = 1/2 g^{00} d_i g_00  (static, no off-diag)
nab_i_u0 = {}
for i,xi in enumerate([x,y,z], start=1):
    d_i_u0 = u0.diff(xi)
    G0i0 = sp.Rational(1,2)*ginv00*g00.diff(xi)
    nab_i_u0[i] = sp.simplify(d_i_u0 + G0i0*u0)

# K = M^-2 K^{ij}_{00} nabla_i u^0 nabla_j u^0 ;  K^{ij}_{00} = c1 g^{ij} g_00
Kval = sp.Integer(0)
for i in range(1,4):
    for j in range(1,4):
        Kval += c1*ginvii*ginvii*g00*nab_i_u0[i]*nab_i_u0[j]
Kval = sp.simplify(Kval/M**2)
print("K =", Kval)

# aether Lagrangian density (quadratic part, F = fk*K)
L = sp.simplify(sqrtg*M**2*fk*Kval)
print("\nL_aeth =", L)

# Euler-Lagrange wrt g00 (treat g00 and its spatial derivatives as the field).
# E-L: dL/dg00 - d_i(dL/d(d_i g00)) = 0   (static, ignore t-derivatives)
# We need dL/dg00 and dL/d(d_i g00).  But L is expressed in terms of P (since
# g00 = -(1+2P)).  So d/dg00 = (dP/dg00) d/dP = (-1/2) d/dP.
# Equivalently, do the E-L wrt P:  dL/dP - d_i(dL/d(d_i P)) = 0, then convert.
# The 00 equation coefficient of nabla^2 P is what we want.

# Compute dL/dP (P appears without derivatives) and dL/d(d_i P).
dL_dP = sp.simplify(L.diff(P))
dL_dPd = {}
for i,xi in enumerate([x,y,z], start=1):
    dL_dPd[i] = sp.simplify(L.diff(xi))
# Now the E-L operator:  dL/dP - sum_i d_i(dL/d(d_i P))
EL = dL_dP
for i,xi in enumerate([x,y,z], start=1):
    EL -= dL_dPd[i].diff(xi)
EL = sp.simplify(EL)
print("\nE-L (aether, wrt P) =", EL)

# Extract the coefficient of nabla^2 P = P_xx + P_yy + P_zz.
# Build nabla^2 P and read the coefficient.
lapP = P.diff(x,2)+P.diff(y,2)+P.diff(z,2)
# EL should be of the form A * lapP + (terms with (dP)^2).
# Use a trick: set P to a quadratic function to isolate the lapP coefficient.
# Let P = (1/2) a x^2 (so P_xx = a, P_yy=P_zz=0, dP/dx = a x).
a = sp.symbols('a')
EL_sub = EL.subs({P: sp.Rational(1,2)*a*x**2, Q: 0})
# Now lapP = a.  Coefficient of a (linear in a) is the lapP coefficient.
# But there may be (dP)^2 ~ a^2 x^2 terms.  Keep only terms linear in a.
EL_lin_a = sp.simplify(sp.expand(EL_sub).as_coefficients_dict()[a])
print("\ncoefficient of lapP (aether part, at P=0) =", sp.simplify(EL_lin_a))

# Also get the full (dP)^2 terms: substitute P = a*x (linear, so lapP=0).
EL_sub2 = EL.subs({P: a*x, Q: 0})
EL_quad = sp.simplify(EL_sub2)
print("\nEL with P = a x (lapP=0, gives (dP)^2 terms) =", EL_quad)
