#!/usr/bin/env python3
r"""
CLEAN linearization to settle G_00 unambiguously. Use eps as a strict bookkeeping parameter:
metric = eta + eps*h, expand EVERYTHING to O(eps^1), take coeff(eps,1). No second-order leakage.
This replicates the ORIGINAL route1 method exactly (which is the right one) and prints the result.
"""
import sympy as sp
x,y,z,t=sp.symbols('x y z t', real=True); coords=[t,x,y,z]
eps=sp.symbols('epsilon', positive=True)
Phi=sp.Function('Phi')(x,y,z); Psi=sp.Function('Psi')(x,y,z)
lap=lambda F: sp.diff(F,x,2)+sp.diff(F,y,2)+sp.diff(F,z,2)

g=sp.diag(-(1+2*eps*Phi), 1-2*eps*Psi, 1-2*eps*Psi, 1-2*eps*Psi)
ginv=g.inv()
def christoffel(g, ginv, coords):
    n=len(coords); Gamma=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0
                for d in range(n): s+=ginv[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
                Gamma[a][b][cc]=sp.expand(s/2)
    return Gamma
Gamma=christoffel(g,ginv,coords)
def ricci(Gamma,coords):
    n=len(coords); R=sp.zeros(n,n)
    for b in range(n):
        for d in range(n):
            s=0
            for a in range(n):
                s+=sp.diff(Gamma[a][b][d],coords[a])-sp.diff(Gamma[a][b][a],coords[d])
                for e in range(n): s+=Gamma[a][a][e]*Gamma[e][b][d]-Gamma[a][d][e]*Gamma[e][b][a]
            R[b,d]=s
    return R
Ric=ricci(Gamma,coords)
Rs=sum(ginv[i,i]*Ric[i,i] for i in range(4))
# Einstein tensor, take strict O(eps) coefficient (the ORIGINAL method):
def lin(ex):
    return sp.expand(sp.series(ex,eps,0,2).removeO().coeff(eps,1))
G00=sp.simplify(lin(Ric[0,0]-sp.Rational(1,2)*g[0,0]*Rs))
Gxx=sp.simplify(lin(Ric[1,1]-sp.Rational(1,2)*g[1,1]*Rs))
Gxy=sp.simplify(lin(Ric[1,2]-sp.Rational(1,2)*g[1,2]*Rs))
print("CLEAN linearized Einstein (strict O(eps), original method):")
print("  G_00 =", G00)
print("  G_00 == 2 lap Psi ?", sp.simplify(G00-2*lap(Psi))==0)
print("  G_xy =", Gxy)
print("  G_xy == -d_x d_y (Phi-Psi) ?", sp.simplify(Gxy+sp.diff(Phi-Psi,x,y))==0)
print()
print("SETTLED: G_00 = 2 lap Psi (matches original route1 + textbook). The (00) eq sources PSI.")
print("The off-diagonal (ij) eq carries d_i d_j (Phi - Psi) = the SLIP, sourced by anisotropic stress.")
print()
# Now the clean delta-Phi logic:
print("CLEAN delta-Phi LOGIC on the correct equations:")
print("  (00):     2 lap Psi = 8piG rho_b                 -> Psi = baryon Newtonian potential.")
print("  (ij)off:  -d_i d_j(Phi-Psi) = 8piG sigma_ij(lens) -> sets Phi-Psi from anisotropic stress.")
print("""
  For a PURE SLIP delivering light-bending at g_obs while matter feels only g_N, you need:
     - Psi (light: lensing uses Phi+Psi) enhanced to the MOND value, AND
     - Phi (matter: geodesics use Phi) staying at the baryon value.
  Lensing potential = Phi+Psi; matter potential = Phi. With Psi = baryon (from 00!), to get the
  lensing enhancement you must enhance the SUM Phi+Psi, i.e. enhance PHI -- but that is the matter
  potential => fifth force. OR keep Phi=baryon and enhance Psi -- but Psi is PINNED to baryon by
  the (00) eq. CONTRADICTION within the metric sector for a metric-coupled density.
""")
print("="*88)
print(" THE CRUX, settled cleanly:")
print("="*88)
print("""
  The (00) Einstein eq pins Psi to the BARYON density (2 lap Psi = 8piG rho_b). The lensing slip
  needs the LENS potential Phi+Psi enhanced by ~the MOND factor while the MATTER potential Phi stays
  baryon. With Psi already pinned to baryon, the ONLY free metric function left to carry the lensing
  enhancement is Phi -- but enhancing Phi is exactly the fifth force on matter (delta-Phi != 0).

  So WITHIN the Einstein (metric) sector, sourced by a metric-coupled stress, you CANNOT simultaneously
  (a) lens at g_obs and (b) keep matter at g_N. This is the no-go's content, and it survives the
  preferred frame UNLESS the preferred frame ADDS independent constraints that DECOUPLE the three
  metric equations -- i.e. break the Einstein-tensor identities that tie (00),(0j),(ij) together.

  The non-dynamical multiplier lambda^j breaks ONE tie (the 0j/conservation one), which lets the
  source be non-conserved. But pinning Psi=baryon (00) while enhancing the lens (needs Phi or Psi up)
  with Phi=baryon (no fifth force) requires breaking the (00)<->(ij) tie TOO. One (0j) multiplier
  does not do that. You need a second, (ij)-sector constraint. Each added constraint is a free
  (hand-chosen) input. So delta-Phi=0 + the slip are bought by ~two hand-imposed constraints
  TOGETHER -- this is AeST-class phenomenology with extra Lagrange multipliers, NOT a derived slip
  and NOT a structurally-automatic delta-Phi=0.
""")
