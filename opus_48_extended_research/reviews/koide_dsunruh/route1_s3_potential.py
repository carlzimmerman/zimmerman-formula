import sympy as sp
mp_dps = 40

# ============================================================
# ROUTE 1 — most natural S3-invariant flavon potential.
# A 3-component flavon phi = (phi1,phi2,phi3) under S3 (perms of 3 objects).
# S3 irreps of the 3-dim rep: trivial (1) + doublet (2).
#   democratic / singlet:  s = (phi1+phi2+phi3)/sqrt3  along (1,1,1)
#   doublet:  the 2-dim orthogonal complement, amplitude d = sqrt(phi^2 - s^2)
# The Brannen amplitude r is EXACTLY the ratio (doublet)/(singlet) up to the
# M normalization: x_i = M(1 + r cos(...)) -> singlet part = M*sqrt3,
# doublet part = M*r*sqrt(3/2). So r = sqrt(2) * (d/s).  (verify below)
# A potential V(phi) S3-invariant + O(3) is built from the basic invariants:
#   I1 = sum phi_i           (singlet, NOT O(3) but IS S3 - the democratic direction)
#   I2 = sum phi_i^2         (= |phi|^2, the only quadratic O(3)+S3 invariant)
#   I3 = sum phi_i^3 , and  J = phi1 phi2 phi3   (cubic S3 invariants)
#   I4 = sum phi_i^4 , (sum phi_i^2)^2 , etc.
# We do NOT input 2/3 anywhere. We minimize and read off r at the minimum.
# ============================================================

p1,p2,p3 = sp.symbols('p1 p2 p3', real=True)
phi = sp.Matrix([p1,p2,p3])

# singlet (democratic) coordinate s and doublet magnitude d
s = (p1+p2+p3)/sp.sqrt(3)            # projection onto unit (1,1,1)
d2 = phi.dot(phi) - s**2             # squared doublet magnitude
# Relation to Brannen r: x_i = M(1+r cos(phi0+2pi k/3))
# check the r<->(d/s) map numerically-symbolically
r, M, ph0, kk = sp.symbols('r M ph0 kk', real=True)
xB = [M*(1+r*sp.cos(ph0 + 2*sp.pi*kk/3)) for kk in range(3)]
sB = (sum(xB))/sp.sqrt(3)
d2B = sum([xi**2 for xi in xB]) - sB**2
ratio2 = sp.simplify(d2B / sB**2)
print("doublet^2/singlet^2 for Brannen =", ratio2, " (expect r^2/2)")
print("  => r^2 = 2 * d^2/s^2 ; r=sqrt2 <=> d=s (doublet mag == singlet mag)")
print()

# So in invariant language: r=sqrt2 <=> |doublet| = |singlet|, a 50/50 split.
# r=sqrt2 <=> the VEV has EQUAL singlet and doublet magnitude.
# Q=2/3 NEVER mentioned. The target is the equal-split config. Now does a
# natural S3 potential FORCE equal split?

# ============================================================
# Build general renormalizable S3-invariant potential up to quartic.
# Basic S3 invariants (symmetric polynomials):
#   e1 = p1+p2+p3                (singlet)
#   q  = p1^2+p2^2+p3^2          (= |phi|^2)
#   c  = p1^3+p2^3+p3^3
#   t  = p1 p2 p3
# Renormalizable potential terms (mass^2 .. quartic) that are S3-singlets:
#   e1, e1^2, q, e1^3, e1*q, c, t, q^2, e1^4, e1^2 q, e1 c, e1 t, c*e1? etc.
# Most general S3+ (allow a linear/source to pick the democratic VEV) up to quartic:
e1 = p1+p2+p3
q  = p1**2+p2**2+p3**2
c  = p1**3+p2**3+p3**3
t  = p1*p2*p3
qq = q**2

# parametrize couplings
a1,b1,b2,g1,g2,g3,l1,l2,l3,l4 = sp.symbols('a1 b1 b2 g1 g2 g3 l1 l2 l3 l4', real=True)
V = (a1*e1
     + b1*e1**2 + b2*q
     + g1*e1**3 + g2*e1*q + g3*c
     + l1*e1**4 + l2*(e1**2)*q + l3*qq + l4*c*e1 )
# (t-terms p1p2p3 also S3-invariant; add to be complete)
g4,l5,l6 = sp.symbols('g4 l5 l6', real=True)
V = V + g4*t + l5*t*e1 + l6*sp.Symbol('p1p2p3sq')*0  # t*e1 quartic; q*? keep simple
print("Constructed general S3-invariant V up to quartic (couplings a1,b*,g*,l*).")
print("Number of independent invariant monomials used:", len(V.args))
