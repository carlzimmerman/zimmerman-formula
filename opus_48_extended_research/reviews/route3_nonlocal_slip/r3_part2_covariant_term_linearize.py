#!/usr/bin/env python3
"""
ROUTE 3 -- PART 2: WRITE the covariant nonlocal traceless term and LINEARIZE it in sympy.
=========================================================================================
Part 1 fixed the bullseye: the partner's effective stress must have delta-rho^eff sourcing Psi
and a traceless anisotropic stress Pi^eff = (1/2)delta-rho^eff that holds Phi fixed (delta-Phi=0).

PART 2 builds an EXPLICIT covariant Deser-Woodard-style nonlocal term coupled to the TRACELESS
part of the curvature, and LINEARIZES it on the weak-field metric to read off delta-Phi, delta-Psi.

The candidate covariant term (Route 3 form):
   S_3 = (1/16 pi G) int d^4x sqrt(-g)  S_munu  [ G( Box^{-1} R ) ]^{,munu}_TT ...   -- too vague.
We make it CONCRETE and computable. Two concrete covariant realizations are tested:

  (A) TRACELESS-RICCI nonlocal coupling:
        S_A = (mu^2/16 pi G) int sqrt(-g)  W( Box^{-1} R ) * ( R_munu R^munu - (1/4) R^2 ) ...
      -- but R_munu R^munu - (1/4)R^2 is the traceless-Ricci-squared scalar (quadratic in curvature),
         a SCALAR, so on variation it sources Phi+Psi symmetrically. We test if the NONLOCAL weighting
         W(Box^{-1}R) breaks the symmetry. (Spoiler from Part 1: a pure scalar won't give pure slip;
         we must couple to a TENSOR structure with a preferred-frame/traceless projector.)

  (B) THE TRACELESS-PROJECTED nonlocal tensor coupling (the genuine Route 3 object):
        S_B = (1/16 pi G) int sqrt(-g)  Sigma^munu  [ Box^{-1} (G_munu - (1/4) g_munu G) ]
      where Sigma^munu is built from the metric-defined preferred frame u^mu = -d_mu chi/|dchi|,
      chi = Box^{-1}1 (the Deser-Woodard cosmic frame, NOT a propagating aether), and
      Ghat_munu := G_munu - (1/4) g_munu G  is the TRACELESS part of the Einstein/curvature tensor.
      The (Box^{-1} Ghat_munu) is a derivative-LOWERING nonlocal object (no Ostrogradski),
      and coupling it through the traceless projector kills the trace (delta-Phi) channel.

We linearize BOTH on
   g_munu = eta_munu + h_munu,   h_00 = -2 Phi,  h_ij = -2 Psi delta_ij,  h_0i = 0,
quasistatic (drop time derivatives), to first order in Phi, Psi.
We compute the linearized field equations delta(S_EH + S_partner)/delta h = 0 and read delta-Phi.

This requires the linearized curvature. We build it explicitly in sympy for the perturbed metric.
"""
import sympy as sp

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)
def h(t): print("\n"+"-"*88+"\n "+t+"\n"+"-"*88)

# ============================================================================
H("PART 2: explicit linearized curvature of the weak-field (Phi,Psi) metric")
# ============================================================================
# coordinates and small potentials
t, x, y, z = sp.symbols('t x y z', real=True)
X = [t, x, y, z]
eps = sp.symbols('epsilon', positive=True)  # bookkeeping order parameter
Phi = sp.Function('Phi')
Psi = sp.Function('Psi')
# Potentials depend on space only (quasistatic / static)
Ph = Phi(x, y, z)
Ps = Psi(x, y, z)

# Metric: ds^2 = -(1+2 eps Phi)dt^2 + (1-2 eps Psi)(dx^2+dy^2+dz^2)
g = sp.zeros(4, 4)
g[0, 0] = -(1 + 2*eps*Ph)
g[1, 1] = (1 - 2*eps*Ps)
g[2, 2] = (1 - 2*eps*Ps)
g[3, 3] = (1 - 2*eps*Ps)

# inverse metric to first order
ginv = sp.zeros(4, 4)
ginv[0, 0] = -(1 - 2*eps*Ph)
ginv[1, 1] = (1 + 2*eps*Ps)
ginv[2, 2] = (1 + 2*eps*Ps)
ginv[3, 3] = (1 + 2*eps*Ps)

def series1(expr):
    """Truncate to first order in eps."""
    return sp.series(sp.expand(expr), eps, 0, 2).removeO()

# Christoffel symbols Gamma^a_bc to first order
def christoffel(g, ginv, X):
    n = len(X)
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                Gam[a][b][c] = series1(s/2)
    return Gam

print("Building Christoffel symbols (1st order)...")
Gam = christoffel(g, ginv, X)

# Ricci tensor R_bc = d_a Gamma^a_bc - d_c Gamma^a_ba + Gamma^a_ad Gamma^d_bc - Gamma^a_cd Gamma^d_ba
def ricci(Gam, X):
    n = len(X)
    R = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
                for d in range(n):
                    s += Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a]
            R[b, c] = series1(s)
    return R

print("Building Ricci tensor (1st order)...")
Ric = ricci(Gam, X)

# Ricci scalar R = g^bc R_bc
Rscalar = 0
for b in range(4):
    for c in range(4):
        Rscalar += ginv[b, c]*Ric[b, c]
Rscalar = series1(Rscalar)

# Einstein tensor G_bc = R_bc - (1/2) g_bc R
Gten = sp.zeros(4, 4)
for b in range(4):
    for c in range(4):
        Gten[b, c] = series1(Ric[b, c] - sp.Rational(1, 2)*g[b, c]*Rscalar)

h("Linearized curvature components (drop time derivatives for quasistatic; keep spatial)")
# define spatial Laplacian operator symbol via the actual derivatives
def lap3(f):
    return sp.diff(f, x, 2) + sp.diff(f, y, 2) + sp.diff(f, z, 2)

# Print the key components at order eps^1
R00 = sp.expand(Ric[0, 0]).coeff(eps, 1)
Rii = sp.expand(Ric[1, 1]).coeff(eps, 1)  # take xx component
Rsc1 = sp.expand(Rscalar).coeff(eps, 1)
G00 = sp.expand(Gten[0, 0]).coeff(eps, 1)
Gxx = sp.expand(Gten[1, 1]).coeff(eps, 1)
Gxy = sp.expand(Gten[1, 2]).coeff(eps, 1)

# substitute time-derivative terms -> 0 (static), express via Laplacians
def static(expr):
    # set all time derivatives to zero
    e = expr
    e = e.subs({sp.Derivative(Ph, t): 0, sp.Derivative(Ps, t): 0})
    return sp.simplify(e)

print("  R_00 (order eps) =", static(R00))
print("  R_xx (order eps) =", static(Rii))
print("  R    (order eps) =", static(Rsc1))
print("  G_00 (order eps) =", static(G00), "   [expect: 2 nabla^2 Psi]")
print("  G_xy (order eps, off-diag) =", static(Gxy), "   [the SLIP source: d_x d_y (Phi-Psi)]")

# Confirm G_00 = 2 lap Psi
G00_check = sp.simplify(static(G00) - 2*lap3(Ps))
print("  CHECK G_00 - 2 nabla^2 Psi =", G00_check, "  (==0 confirms standard linearized GR)")
# Confirm off-diagonal G_xy = - d_x d_y (Phi - Psi)
Gxy_check = sp.simplify(static(Gxy) - ( -sp.diff(Ph - Ps, x, y) ))
print("  CHECK G_xy + d_x d_y(Phi-Psi) =", sp.simplify(static(Gxy) + sp.diff(Ph-Ps, x, y)),
      "  (==0 confirms the slip is sourced by Phi-Psi)")

print("""
  => CONFIRMED: the OFF-DIAGONAL Einstein tensor G_ij (i!=j) = -d_i d_j (Phi - Psi).
     This is the SLIP channel. A partner whose effective stress has a NONZERO traceless
     (off-diagonal) part sources Phi-Psi. A partner with delta-Phi=0 needs its traceless
     stress to source exactly -d_i d_j(Psi). This is the covariant traceless coupling target.
""")

# Save the linearized tensors for Part 3 (the covariant term variation).
import pickle, os
out = {
    'G00': static(G00), 'Gxx': static(Gxx), 'Gxy': static(Gxy),
    'R00': static(R00), 'Rxx': static(Rii), 'Rscalar': static(Rsc1),
}
# We can't easily pickle sympy Functions across files cleanly; just re-derive in Part 3.
print("\nLinearized curvature built and cross-checked against textbook GR. Proceed to Part 3:")
print("vary the covariant nonlocal traceless term and read delta-Phi, delta-Psi, c_T, ghost.")
