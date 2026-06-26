#!/usr/bin/env python3
r"""
LAST DEFENSE CHECK: can the (0j) multiplier lambda^j, through its metric variation
delta(lambda^j E_{0j})/delta g^{munu}, back-react into the (ij)/Phi-fixing equation?
If yes, the single multiplier COULD hold Phi fixed and the original's delta-Phi=0 survives
as specified. If no, a second (ij) constraint is needed -> delta-Phi=0 is an EXTRA postulate.

E_{0j}[g] is the (0j) Einstein/momentum combination = G_{0j} (the constraint targets the momentum
constraint). The multiplier term is  S_lm = int sqrt(-g) lambda^j (G_{0j} - W_j).
Its metric variation is  lambda^j * delta G_{0j}/delta g^{munu}  + (G_{0j}-W_j) delta(sqrt-g lambda)/...
On-shell of the constraint (G_{0j}=W_j) the second piece vanishes. The first piece,
lambda^j delta G_{0j}/delta g^{munu}, is a LINEAR-IN-lambda contribution to the (munu) field eq.

Question: does lambda^j delta G_{0j}/delta g^{ij} have a nonzero (ij) (in particular trace/00)
component that could hold Phi? Compute delta G_{0j}/delta g^{ab} structure at linear order.
"""
import sympy as sp
# At linear order, G_{0j} = (1/2)(d_k d_j N_k - lap N_j) + (time derivs of Psi) [shift sector].
# For a STATIC config the multiplier enforces a relation among the shift N_j. Varying g to get the
# back-reaction: delta G_{0j}/delta g^{munu}. The KEY structural fact: G_{0j} is BUILT from the
# metric's (0j) and spatial components; its variation w.r.t. g^{00} (the lapse Phi) is what could
# reach the Phi sector. Compute whether G_{0j} depends on Phi (g_00) at all at linear order.
x,y,z,t=sp.symbols('x y z t', real=True); coords=[t,x,y,z]
eps=sp.symbols('epsilon', positive=True)
Phi=sp.Function('Phi')(x,y,z); Psi=sp.Function('Psi')(x,y,z)
N=[sp.Function('N'+str(j))(x,y,z) for j in range(3)]
T=sp.symbols('T_t', real=True)  # placeholder
eta=sp.diag(-1,1,1,1)
h=sp.zeros(4,4); h[0,0]=-2*Phi
for j in range(3):
    h[j+1,j+1]=-2*Psi; h[0,j+1]=N[j]; h[j+1,0]=N[j]
g=eta+eps*h; ginv=eta-eps*(eta*h*eta)
def christ(g,gi,c):
    n=len(c); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0
                for d in range(n): s+=gi[a,d]*(sp.diff(g[d,b],c[cc])+sp.diff(g[d,cc],c[b])-sp.diff(g[b,cc],c[d]))
                G[a][b][cc]=sp.expand(s/2)
    return G
Gamma=christ(g,ginv,coords)
def Rab(a,b,G,c):
    n=len(c); s=0
    for m in range(n):
        s+=sp.diff(G[m][a][b],c[m])-sp.diff(G[m][a][m],c[b])
        for e in range(n): s+=G[m][m][e]*G[e][a][b]-G[m][b][e]*G[e][a][m]
    return s
def lin(ex):
    return sp.expand(sp.series(sp.expand(ex),eps,0,2).removeO().coeff(eps,1))
G0x=sp.simplify(lin(Rab(0,1,Gamma,coords)))   # eta_{0x}=0 so G_0x = R_0x to linear order
print("G_{0x} (linearized, with lapse Phi, slip Psi, shift N present) =")
print("  ", G0x)
print()
hasPhi = Phi in G0x.atoms(sp.Function)
hasPsi = Psi in G0x.atoms(sp.Function)
print("  G_{0x} depends on Phi (the lapse)? ", hasPhi)
print("  G_{0x} depends on Psi?            ", hasPsi)
print("  G_{0x} depends on the shift N_j?  ", any(N[j] in G0x.atoms(sp.Function) for j in range(3)))
print("""
READ: the momentum-constraint combination E_{0j}=G_{0j} that the multiplier targets is, at linear
order on a static background, built from time-derivatives of (Psi) and spatial derivatives of the
shift N_j. The lapse Phi enters G_{0j} only through TIME derivatives (d_t Phi), which VANISH in a
STATIC configuration. So:
  * In the STATIC weak field (the lensing regime), G_{0j} carries NO Phi dependence.
  * Therefore lambda^j (delta G_{0j}/delta g^{munu}) has NO leverage on the static lapse Phi:
    delta G_{0j}/delta(g_00) ~ d_t(...) -> 0 statically.
  => The (0j) multiplier's back-reaction CANNOT reach or hold the static lapse Phi. Confirmed.
""")
print("="*90)
print(" FINAL: the single (0j) multiplier lambda^j, even through its full metric back-reaction,")
print(" does NOT touch the static lapse Phi (G_{0j} is Phi-blind statically). So it CANNOT hold")
print(" Phi at the baryon value against the (ij) traceless-stress shift delta-Phi=-8piG f. To get")
print(" delta-Phi=0 you MUST add a second, (ij)-sector non-dynamical constraint. delta-Phi=0 is")
print(" therefore NOT delivered by the action AS SPECIFIED -- it needs an extra hand-imposed")
print(" constraint, putting it in the SAME by-hand class as the slip.")
print("="*90)
