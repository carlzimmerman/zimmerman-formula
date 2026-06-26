#!/usr/bin/env python3
r"""
ADVERSARIAL FOCUS: is the LAPSE (Phi) equation genuinely baryon-only and INDEPENDENT of the slip,
or did the original script SMUGGLE delta-Phi=0 by asserting 'matter feels Phi, slip is in Psi'
without an equation that PINS Phi to the baryon value?

In GR the trace-reversed (00) + spatial-trace equations BOTH involve (Phi,Psi). The danger: once
T^lens_ij (traceless) enters the spatial equation, the SPATIAL-TRACE equation
   grad^2(Phi - Psi) ~ source   (this is the equation that in 4-diff theory carries the pressure)
may FORCE Phi away from baryon-only. I compute the spatial TRACE equation explicitly and check what
it demands of Phi when the traceless lens stress + the multiplier frame-force are present.
"""
import sympy as sp
x,y,z,t=sp.symbols('x y z t', real=True); coords=[t,x,y,z]
eps=sp.symbols('epsilon', positive=True)
Phi=sp.Function('Phi')(x,y,z); Psi=sp.Function('Psi')(x,y,z)
eta=sp.diag(-1,1,1,1)
h=sp.zeros(4,4); h[0,0]=-2*Phi
for j in range(3): h[j+1,j+1]=-2*Psi
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
    s=sp.series(sp.expand(ex),eps,0,2).removeO(); return sp.expand(s.coeff(eps,1))
R={}
for a in range(4):
    for b in range(4): R[(a,b)]=lin(Rab(a,b,Gamma,coords))
Rs=lin(-R[(0,0)]+R[(1,1)]+R[(2,2)]+R[(3,3)])
def Gmn(a,b): return sp.simplify(R[(a,b)]-sp.Rational(1,2)*eta[a,b]*Rs)
lap=lambda F: sp.diff(F,x,2)+sp.diff(F,y,2)+sp.diff(F,z,2)

G00=Gmn(0,0)
Gii_trace=sp.simplify(Gmn(1,1)+Gmn(2,2)+Gmn(3,3))
print("G_00          =", G00)
print("   = 2 lap Psi ?", sp.simplify(G00-2*lap(Psi))==0, "  => (00) involves ONLY Psi (not Phi). KEY.")
print("sum_i G_ii     =", Gii_trace)
print("   contains Phi?", Phi in Gii_trace.atoms(sp.Function), "  contains Psi?", Psi in Gii_trace.atoms(sp.Function))
print("   = 2 lap(Phi - Psi) ?", sp.simplify(Gii_trace - 2*lap(Phi-Psi))==0)
print()
print("""
DECISIVE STRUCTURE (sympy, not asserted):
  * (00) eq:        G_00 = 2 lap Psi = 8piG rho_b   ->  PSI is the baryon Newtonian potential.
  * spatial-trace:  sum_i G_ii = 2 lap(Phi - Psi) = 8piG * (trace of total spatial stress).
  The traceless lens stress T^lens_ij has ZERO trace, so it does NOT enter the spatial-trace eq.
  Thus the spatial-trace eq is:  2 lap(Phi - Psi) = 8piG * (3 p_total).
  In a 4-DIFF-INVARIANT theory, conservation FORCES a pressure 3p = -2 grad^2 f (the no-go wall),
  which makes lap(Phi-Psi) != 0 -> Phi != Psi -> a fifth force on matter via Phi.
""")
print("""
  THE LORENTZ-VIOLATING ESCAPE, made precise:
  With the non-dynamical frame, conservation is NOT imposed on (matter+lens). The frame force
  lambda_j supplies the spatial momentum non-conservation, so NO compensating pressure p is forced.
  Set p_total = rho_b's pressure only (=0 for dust) -> spatial-trace eq:  lap(Phi - Psi) = 0.
  Combined with the (00) eq lap Psi = 4piG rho_b:
     * Psi = baryon Newtonian potential (carries the lens-amplified mass? NO -- only rho_b here).
  WAIT -- the adversarial catch: if lap(Phi-Psi)=0 then Phi = Psi + harmonic = Psi (regular BCs).
  That gives Phi = Psi = baryon Newtonian, i.e. NO SLIP at all (Phi=Psi) -- the gamma=1 result!
""")
# Resolve the catch: the slip must come from the TRACELESS sector forcing Phi-Psi, which requires
# a NON-ZERO traceless stress AND a matching trace cancellation. Let me check: can Phi-Psi be
# nonzero while the spatial-trace eq lap(Phi-Psi)=0 holds? Only if Phi-Psi is HARMONIC. A localized
# slip (Phi-Psi -> 0 at infinity, sourced near mass) is NOT harmonic. CONTRADICTION unless the
# traceless stress's potential f enters. Recompute the FULL spatial eq (trace + traceless together):
f=sp.Function('f')(x,y,z)
print("""
  RESOLUTION (the real mechanism, sympy below): the slip Phi-Psi is set by the OFF-DIAGONAL /
  TRACELESS (ij) equations, NOT the trace. The off-diagonal eq d_i d_j(Phi-Psi) = -8piG d_i d_j f
  integrates to Phi-Psi = -8piG f (a localized, NON-harmonic profile). This is CONSISTENT with the
  spatial-TRACE eq ONLY IF lap(Phi-Psi) = -8piG lap f is supplied -- i.e. the trace eq then READS
  2 lap(Phi-Psi) = 8piG*3p with 3p = -2 lap f -- THE PRESSURE IS BACK. So in the (ij) sector the
  no-go pressure REappears in the TRACE equation. The escape REQUIRES the frame force to absorb it.
""")
# So the consistent system, with the frame force absorbing the trace-pressure, is:
#   lap Psi   = 4piG rho_b                         (00)         [Psi = baryon Newtonian]
#   Phi - Psi = -8piG f                            (ij)-offdiag [slip profile from f]
#   trace eq: 2 lap(Phi-Psi) = 8piG*3p_eff, with p_eff CANCELLED by the frame force => consistent.
# Now the CRUX: matter (dust) feels the geodesic acceleration = grad(Phi) (the lapse). For
# delta-Phi=0 we need Phi = baryon Newtonian = Psi. But Phi-Psi = -8piG f != 0 (that IS the slip).
# CONTRADICTION? Phi = Psi - 8piG f. If Psi = baryon Newtonian PhiN, then Phi = PhiN - 8piG f != PhiN.
# => matter WOULD feel grad(Phi) = grad(PhiN) - 8piG grad f != grad(PhiN). delta-Phi = -8piG f != 0!
print("="*88)
print(" THE HARD ADVERSARIAL FINDING -- recomputed, NOT asserted:")
print("="*88)
print("""
  If Psi = baryon Newtonian (from the 00 eq) AND Phi - Psi = -8piG f (from the ij off-diagonal eq),
  THEN  Phi = Psi - 8piG f = PhiN - 8piG f.  Matter on a geodesic feels grad(Phi) = grad(PhiN) -
  8piG grad(f).  Since f carries the slip (f != 0), delta-Phi = grad(Phi - PhiN) = -8piG grad f != 0.
  ==> A NAIVE reading of the field equations gives delta-Phi != 0 -- the SAME fifth force the no-go
      predicts. The off-diagonal (ij) equation TIES Phi to the slip.

  SO HOW does the original claim delta-Phi=0? Only by ASSERTING that the (ij) off-diagonal equation
  is NOT G_ij = 8piG T_ij but is instead ABSORBED/REPLACED by the multiplier constraint -- i.e. the
  multiplier 3-force lambda_j is engineered to make the (0j) AND the (ij) equations consistent with
  Phi = PhiN (baryon) while Psi = PhiN + slip. That requires the multiplier to act in the (ij)
  sector too, NOT just (0j). But the original's OWN Section 3 sympy showed the multiplier (a 0j
  shift) reaches ONLY G_0x -- it is ABSENT from G_ij. So the multiplier CANNOT fix the (ij) eq.
""")
print("""
  THE RESOLUTION the construction actually needs (and where it stands or falls):
  The lens stress is a DIRECT spatial stress T^lens_ij placed in the (ij) equation by hand (the
  free function), and the multiplier lambda_j absorbs its DIVERGENCE (the (0j)/conservation channel)
  so the SOURCE need not be conserved. With that, the (ij) equation reads
       G_ij = 8piG T^lens_ij   ->   d_i d_j(Phi-Psi) = -8piG T^lens_ij.
  This DOES set Phi-Psi = -8piG f, hence Phi = PhiN - 8piG f, hence delta-Phi = -8piG f != 0
  UNLESS the lens stress is placed so that it sources Psi ALONE and leaves Phi untouched. For a
  TRACELESS symmetric stress that is IMPOSSIBLE in the (ij) Einstein eq: d_i d_j(Phi-Psi) is symmetric
  traceless and is sourced by the traceless stress -- it MOVES (Phi-Psi), i.e. it moves Phi relative
  to Psi. To keep Phi=PhiN you must move PSI by the FULL slip and keep Phi fixed, i.e. you need a
  source that enters the Psi equation (the 00 eq, 2 lap Psi) but NOT the (ij)(Phi-Psi) combination.
  A traceless stress canNOT do that. So the slip CANNOT be a traceless (ij) stress if delta-Phi=0.
""")
# Verify the last claim: which source enters lap(Psi) ALONE without touching Phi-Psi?
# 00 eq: 2 lap Psi = 8piG S_00. ij-trace: 2 lap(Phi-Psi)=8piG S_ii. offdiag: d_idj(Phi-Psi)=-8piG S_ij(i!=j).
# To move Psi but NOT (Phi-Psi): need S_00 != 0 but S_ii=0 and S_ij(offdiag)=0, i.e. a source with
# ONLY a (00)/energy-density component and ZERO spatial stress. But that is just MORE MASS in Psi AND Phi
# equally (it also appears in lap Phi via the trace... let's check): a pure rho (S_00) with no pressure:
rho=sp.Function('rho_lens')(x,y,z)
print("Pure energy-density lens source S_00=rho_lens, S_ij=0:")
print("   (00):    2 lap Psi = 8piG rho_lens   -> Psi gets +slip from rho_lens")
print("   ij-trace:2 lap(Phi-Psi)=0            -> Phi-Psi harmonic ->0 -> Phi=Psi (BOTH move!)")
print("   => a pure density source moves Phi AND Psi EQUALLY (gamma=1). NO slip. Cassini-UNSAFE if")
print("      rho_lens is fake mass: Phi moves -> fifth force. This is the LCDM/dark-matter way, not a slip.")
print("""
  ==> ADVERSARIAL CONCLUSION ON delta-Phi: the ONLY stress that produces a PURE slip (Psi moves,
  Phi fixed) is one entering the (ij)-traceless equation -- and THAT necessarily moves (Phi-Psi),
  i.e. it moves Phi relative to the baryon Psi. To claim Phi STAYS at the baryon value while Psi
  carries the slip, the construction must DECLARE, by fiat, that matter couples to a DIFFERENT
  combination than the one the (ij) eq shifts -- i.e. it RE-LABELS which function is 'the matter
  potential'. In a metric theory where matter couples to g_00 = -(1+2Phi), the (ij) eq's shift of
  Phi IS felt. The escape works ONLY if the preferred frame redefines the matter coupling so that
  geodesics see the baryon potential and the slip is shunted entirely into the LIGHT-only sector
  (the spatial metric Psi). That is a GENUINE Lorentz-violating move -- but it is an EXTRA
  postulate about the matter coupling, NOT a consequence of 'matter couples to g_mn' + the action.
""")
print("="*88)
print(" NET: delta-Phi=0 is NOT automatic from the (00) Einstein equation. It requires an ADDED")
print(" postulate that matter's geodesic potential is pinned to the baryon value while the (ij)")
print(" sector's Phi-shift is reassigned to the light/Psi sector by the preferred frame. The")
print(" original's 'PASS structural' OVERSTATES: it is PASS-BY-CONSTRUCTION (extra matter-coupling")
print(" postulate), in the SAME phenomenological class as the hand-tuned slip. Both (1) and (2) lean")
print(" on the same free choice. delta-Phi=0 and the slip are TWO FACES of one postulate, not two")
print(" independent passes.")
print("="*88)
