"""
Step 2c (jet method): Determine the aether contribution to the 00 weak-field eq.

Uses the jet (independent-derivative) method:
  - Replace P_i = dP/dx_i by independent symbols p_i,
    P_ii = d2P/dx_i^2 by independent symbols q_i.
  - Compute dL/dP and dL/dp_i as true partials.
  - The total x-derivative in the E-L operator is
        d/dx = partial_x + p_x partial_P + q_x partial_p_x
    (linear order in second derivatives: q terms enter only through
     d/dx(dL/dp_x) -> q_x).
  - Extract the coefficient of lapP = q_x + q_y + q_z.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
M = sp.symbols('M', positive=True)
fk = sp.symbols('fk', real=True)

# Jet variables
P = sp.symbols('P')            # field value
px, py, pz = sp.symbols('px py pz')   # first derivatives
qx, qy, qz = sp.symbols('qx qy qz')   # second derivatives

# metric (Q=Phi=0, flat spatial)
g00 = -(1 + 2*P)
ginv00 = 1/g00
sqrtg = sp.sqrt(-g00)          # sqrt(-g) with g_ii=1

u0 = -ginv00
# nabla_i u^0 = d_i u^0 + Gamma^0_{i0} u^0 ;  Gamma^0_{i0} = (1/2) g^{00} d_i g_00
nab = {
    'x': sp.simplify(u0.diff(P)*px + sp.Rational(1,2)*ginv00*g00.diff(P)*px*u0),
    'y': sp.simplify(u0.diff(P)*py + sp.Rational(1,2)*ginv00*g00.diff(P)*py*u0),
    'z': sp.simplify(u0.diff(P)*pz + sp.Rational(1,2)*ginv00*g00.diff(P)*pz*u0),
}
print("nab_i u^0 (jet):", nab)

# K = M^-2 c1 g^{ij} g_00 nab_i nab_j  (g^{ij} = delta^{ij})
Kval = sp.simplify(c1*ginv00*g00*(nab['x']**2 + nab['y']**2 + nab['z']**2)/M**2)
print("K (jet) =", Kval)

L = sp.simplify(sqrtg*M**2*fk*Kval)
print("L (jet) =", L)

# E-L: EL = dL/dP - d/dx(dL/dpx) - d/dy(dL/dpy) - d/dz(dL/dpz)
# total derivative operator (linear in q's):
# d/dx = px * d/dP + qx * d/dpx
dL_dP = sp.simplify(L.diff(P))
dL_dpx = sp.simplify(L.diff(px))
dL_dpy = sp.simplify(L.diff(py))
dL_dpz = sp.simplify(L.diff(pz))

ddpx_dx = sp.simplify(px*dL_dpx.diff(P) + qx*dL_dpx.diff(px))
ddpy_dy = sp.simplify(py*dL_dpy.diff(P) + qy*dL_dpy.diff(py))
ddpz_dz = sp.simplify(pz*dL_dpz.diff(P) + qz*dL_dpz.diff(pz))

EL = sp.simplify(dL_dP - ddpx_dx - ddpy_dy - ddpz_dz)
print("\nE-L (jet) =", EL)

# Coefficient of lapP = qx+qy+qz:
lap_coeff = sp.simplify(EL.coeff(qx))
print("\ncoefficient of lapP (aether part) =", lap_coeff)
# evaluate at P=0 (linear regime):
print("at P=0:", sp.simplify(lap_coeff.subs(P, 0)))
