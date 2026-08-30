"""
Step 1: Weak-field mapping K = kappa * y^2  (Assignment Sec 3).

CONVENTIONS (fixed throughout):
  - Metric signature: (-,+,+,+)
  - Units: c = 1  (matches the aether constraint u^mu u_mu + 1 = 0 in the action).
    c is restored in final physical formulas (MOND eq, cosmology).
  - Weak-field metric:
        ds^2 = -(1+2*Psi) dt^2 + (1-2*Phi) dx^2
    (g_00 = -(1+2 Psi), g_ii = (1-2 Phi) delta_ii, g_0i = 0)
  - Background aether aligned with time:  u_mu = (-1,0,0,0).

ORDER COUNTING:
  K is quadratic in nabla u.  nabla u is FIRST order in the potentials
  (nabla_i u^0 ~ partial_i Psi).  Therefore K is SECOND order.
  To get its coefficient we evaluate ALL metric factors (g, ginv, u^mu)
  on the Minkowski background (Psi=0, Phi=0) and multiply by the
  linear-order (nabla u)^2.  This is the standard weak-field procedure.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
_PsiF = sp.Function('Psi')
_PhiF = sp.Function('Phi')
Psi = _PsiF(t, x, y, z)
Phi = _PhiF(t, x, y, z)
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
M, a0 = sp.symbols('M a0', positive=True)
coords = [t, x, y, z]

# ---- metric (first order) ----
g00 = -(1 + 2*Psi)
gii =  (1 - 2*Phi)
g = sp.Matrix([
    [g00,  0,   0,   0  ],
    [  0,  gii,  0,   0  ],
    [  0,   0,  gii,  0  ],
    [  0,   0,   0,  gii ],
])
ginv = g.inv()

def christoffel(gm, ginv_m, mu, nu, rho):
    res = sp.Integer(0)
    for sigma in range(4):
        res += (ginv_m[mu, sigma] * (gm[rho, sigma].diff(coords[nu])
                                     + gm[nu, sigma].diff(coords[rho])
                                     - gm[nu, rho].diff(coords[sigma])))
    return sp.simplify(res/2)

# aether
u_cov = sp.Matrix([-1, 0, 0, 0])
u_con = ginv * u_cov
u0_con = sp.simplify(u_con[0])          # u^0 = 1/(1+2 Psi)

# nabla_i u^0 = d_i u^0 + Gamma^0_{i0} u^0   (linear order)
nab_i_u0 = {}
for i in range(1,4):
    d_i_u0 = u0_con.diff(coords[i])
    G0i0 = christoffel(g, ginv, 0, i, 0)
    nab_i_u0[i] = sp.simplify(d_i_u0 + G0i0*u0_con)

# ---- Extract the LINEAR coefficient of each derivative of Psi ----
# nab_i u^0 is linear in (partial_j Psi).  Use linear_coefficients to read the
# coefficient of partial_i Psi, then evaluate the (Psi,Phi)-dependent part at 0.
dPsi = {1: sp.Derivative(Psi, x), 2: sp.Derivative(Psi, y), 3: sp.Derivative(Psi, z)}
nab_coeff = {}
for i in (1,2,3):
    # coefficient of partial_i Psi in nab_i u^0 (treat the derivative as an atom)
    coeff_i = sp.simplify(nab_i_u0[i].coeff(dPsi[i]))
    # evaluate metric-dependent part at Minkowski
    coeff_i_mk = sp.simplify(coeff_i.subs({Psi:0, Phi:0}))
    nab_coeff[i] = coeff_i_mk
    print(f"coefficient of partial_i Psi in nab_i u^0 (i={i}) at Minkowski =", coeff_i_mk)

# So nab_i u^0 = -partial_i Psi  (to linear order).
# K^{ij}_{00} = c1 g^{ij} g_00 = -c1 delta^{ij} at Minkowski.
# K = M^-2 * Kij00_mk * (nab_i u^0)(nab_j u^0)
#   = M^-2 * (-c1 delta^{ij}) * (partial_i Psi)(partial_j Psi)
#   = -(c1/M^2) |grad Psi|^2
dPsi_x, dPsi_y, dPsi_z = sp.symbols('dPsi_x dPsi_y dPsi_z', real=True)
nab_lin = [nab_coeff[1]*dPsi_x, nab_coeff[2]*dPsi_y, nab_coeff[3]*dPsi_z]
Kij00_mk = -c1 * sp.eye(3)
K_val = sp.Integer(0)
for i in range(3):
    for j in range(3):
        K_val += Kij00_mk[i,j] * nab_lin[i] * nab_lin[j]
K_val = sp.simplify(K_val / M**2)
print("\nK (quadratic, Minkowski factors) =", K_val)

# match K = kappa y^2,  y^2 = |grad Psi|^2 / a0^2
g2 = dPsi_x**2 + dPsi_y**2 + dPsi_z**2
kappa = sp.simplify(K_val / (g2/a0**2))
print("\nkappa =", kappa)
