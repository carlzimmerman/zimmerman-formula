"""
Step 2: Derive the weak-field (00) field equation of GEA from the quadratic action.

Goal: verify the Living-Reviews GEA result
    mu(y) = F_K + (1 - F_K)/(1 - C/2),   C = c1 - c4,
and fix the overall Newtonian normalization (measured G_N).

Method: build the quadratic (in the potentials) action
    S_2 = (1/16 pi G) int sqrt(-g) [ R^{(2)} + M^2 F_K(0) K^{(2)} ]
with the time-aligned aether u_mu = (-1,0,0,0), then vary wrt the metric
perturbations (Psi, Phi) and read the 00 (Poisson) component.

Conventions: signature (-,+,+,+), c=1.
  g_00 = -(1+2 Psi), g_ij = (1-2 Phi) delta_ij, g_0i = 0.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
coords = [t, x, y, z]
Psi = sp.Function('Psi')(t, x, y, z)
Phi = sp.Function('Phi')(t, x, y, z)
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
M = sp.symbols('M', positive=True)
FK0 = sp.symbols('FK0', real=True)      # F_K(0)
G = sp.symbols('G', positive=True)

eta = sp.diag(-1, 1, 1, 1)

# metric and inverse (keep only up to 2nd order in Psi,Phi)
g00 = -(1 + 2*Psi)
gii =  (1 - 2*Phi)
g = sp.Matrix([
    [g00, 0, 0, 0],
    [0, gii, 0, 0],
    [0, 0, gii, 0],
    [0, 0, 0, gii],
])
ginv = g.inv()

# Truncate: keep terms up to 2nd order in (Psi, Phi) and their derivatives.
# We do this by expanding in a bookkeeping parameter eps.
eps = sp.symbols('eps')
g_eps = g.subs({Psi: eps*Psi, Phi: eps*Phi})
ginv_eps = g_eps.inv()

def trunc2(expr):
    # expand in eps, keep up to eps^2, set eps->1
    e = sp.expand(expr.series(eps, 0, 3).removeO())
    return sp.simplify(e.subs(eps, 1))

g2 = trunc2(g_eps)
ginv2 = trunc2(ginv_eps)

def christoffel(gm, ginv_m, mu, nu, rho):
    res = sp.Integer(0)
    for s in range(4):
        res += ginv_m[mu, s]*(gm[rho, s].diff(coords[nu])
                              + gm[nu, s].diff(coords[rho])
                              - gm[nu, rho].diff(coords[s]))
    return sp.simplify(res/2)

# Riemann, Ricci, R
def riemann(gm, ginv_m, a, b, c_, d):
    # R^a_{b c d} = d_c Gamma^a_{b d} - d_d Gamma^a_{b c} + Gamma^a_{c e}Gamma^e_{b d} - Gamma^a_{d e}Gamma^e_{b c}
    res = sp.Integer(0)
    for e in range(4):
        G1 = christoffel(gm, ginv_m, a, b, d)
        G2 = christoffel(gm, ginv_m, a, b, c_)
        res += G1.diff(coords[c_]) - G2.diff(coords[d])
        for f in range(4):
            res += christoffel(gm, ginv_m, a, c_, f)*christoffel(gm, ginv_m, f, b, d)
            res -= christoffel(gm, ginv_m, a, d, f)*christoffel(gm, ginv_m, f, b, c_)
    return sp.simplify(res)

Ricci = sp.zeros(4,4)
for b in range(4):
    for d in range(4):
        for a in range(4):
            Ricci[b,d] += riemann(g2, ginv2, a, b, a, d)
Ricci = sp.Matrix(Ricci)
R = sp.simplify(sum(Ricci[i,i] for i in range(4)))
print("R (quadratic) =", sp.simplify(R))

# Einstein tensor
E = Ricci - sp.Matrix.eye(4)*R/2
G00 = sp.simplify(E[0,0])
print("\nG_00 (quadratic) =", G00)

# ---- aether K to quadratic order ----
# u^mu = g^{mu nu} u_nu, u_nu = (-1,0,0,0)
u_cov = sp.Matrix([-1,0,0,0])
u_con = sp.simplify((ginv2 * u_cov))
print("\nu^mu =", u_con.T)

# nabla_i u^0 to linear order
nab_i_u0 = {}
for i in range(1,4):
    d_i = u_con[0].diff(coords[i])
    G0i0 = christoffel(g2, ginv2, 0, i, 0)
    nab_i_u0[i] = sp.simplify(d_i + G0i0*u_con[0])
print("nabla_i u^0 =", nab_i_u0)

# K = M^-2 K^{ij}_{00} nabla_i u^0 nabla_j u^0 ;  K^{ij}_{00} = c1 g^{ij} g_00
Kval = sp.Integer(0)
for i in range(1,4):
    for j in range(1,4):
        Kval += c1*ginv2[i,j]*g2[0,0]*nab_i_u0[i]*nab_i_u0[j]
Kval = sp.simplify(trunc2(Kval)/M**2)
print("\nK (quadratic) =", Kval)

# ---- aether stress-energy 00 component ----
# T^{aeth}_{mu nu} = M^2 [ F_K (K_{mu nu} - 1/2 g_{mu nu} K) + 1/2 g_{mu nu} F ]
# For the 00 component at quadratic order, F ~ F_K(0) K (drop F(0) constant).
# We need K_{00}.  K_{mu nu} = variation tensor.  For the time-aligned aether,
# the aether "field" entering is nabla_i u^0.  The aether stress 00 piece is
# proportional to F_K(0) * (quadratic in nabla u) with the c1 tensor structure.
# We compute it by varying the aether action term directly wrt g^{00}.
# Simpler: the aether Lagrangian density (quadratic) is M^2 F_K(0) K.
# Its contribution to the 00 equation is (1/2) d/dh_00 [sqrt(-g) M^2 F_K(0) K] type.
# Instead, compute T^{aeth}_{00} = -(2/sqrt(-g)) dS_aeth/dg^{00} via the known
# linearized aether stress tensor.  For the K-invariant form, to quadratic order
# the 00 component is:
#   T^{aeth}_{00} = M^2 F_K(0) [ c1 (nabla_0 u . nabla_0 u) + c1 g_00 |nabla u|^2
#                               + c2 (...) + c3 (...) - c4 (...) + 1/2 g_00 (F - F_K K) ]
# For the time-aligned aether the only nonzero aether gradient is nabla_i u^0,
# so nabla_0 u = 0.  Thus the "c1 (nabla_0 u)^2" type term vanishes and we are
# left with the metric-structure pieces.  We compute T^{aeth}_{00} by direct
# functional differentiation of sqrt(-g) M^2 F_K(0) K with respect to g^{00}.

# Treat g^{00} as an independent variable: perturb g00 -> g00 + delta, recompute K.
delta = sp.symbols('delta')
ginv2_p = ginv2.copy()
ginv2_p[0,0] = ginv2[0,0] - delta*ginv2[0,0]**2   # d g^{00}/d g_00 = -g^{00} g^{00}
# K depends on g^{ij} and g_00 and u^0.  For a g_00 perturbation only:
#   g^{ij} unchanged, g_00 -> g_00+delta, u^0 = g^{00}(-1) -> changes.
K_p = sp.Integer(0)
for i in range(1,4):
    for j in range(1,4):
        K_p += c1*ginv2_p[i,j]*(g2[0,0]+delta)*nab_i_u0[i]*nab_i_u0[j]
# u^0 change: u^0 = -g^{00}; with g^{00} -> g^{00}(1-delta g^{00})?  Actually
# g^{00} = -1/(1+2Psi); perturbing g_00 by delta changes g^{00}.  But nabla_i u^0
# already encodes u^0.  To quadratic order the dominant 00 aether stress is:
K_p = sp.simplify(K_p)
# dK/dg_00 at delta=0:
dK_dg00 = sp.simplify(K_p.diff(delta).subs(delta,0))
print("\ndK/dg_00 =", dK_dg00)

# T^{aeth}_{00} = -(2/sqrt(-g)) d(S_aeth)/dg^{00};  dS/dg^{00} = (M^2 F_K0) d(sqrt(-g) K)/dg^{00}
# d sqrt(-g)/dg^{00} = -1/2 sqrt(-g) g_00 ;  dK/dg^{00} = (dK/dg_00)(dg_00/dg^{00}) = dK_dg00 * (-1/g_00^2)
sqrtg = sp.simplify(sp.sqrt(-g2.det()))
dK_dginv00 = sp.simplify(dK_dg00 * (-1/g2[0,0]**2))
T_aeth_00 = sp.simplify(-2/sqrtg * (M**2*FK0)*( sp.simplify((-sp.sqrt(-g2.det())*g2[0,0]/2) + sqrtg*dK_dginv00) ))
# Note: d(sqrt(-g) K)/dg^{00} = (d sqrt(-g)/dg^{00}) K + sqrt(-g) dK/dg^{00}
T_aeth_00 = sp.simplify(-2/sqrtg*(M**2*FK0)*( (-sp.sqrt(-g2.det())*g2[0,0]/2)*Kval + sqrtg*dK_dginv00 ))
print("\nT_aeth_00 =", T_aeth_00)
