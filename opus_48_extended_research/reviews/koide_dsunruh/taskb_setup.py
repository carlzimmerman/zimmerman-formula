"""
TASK B SETUP — establish the per-STATE vs per-IRREP distinction sharply,
then test whether dS-Unruh can FORCE per-irrep. sympy/mpmath dps>=30.

Foundations (reproduce banked, then build the measure question on top):
  Brannen circulant: sqrt(m_k) = M(1 + r cos(phi + 2pi k/3)).
  Q = (sum m)/(sum sqrt m)^2 = 1/3 + r^2/6   (phase-free).
  Koide  Q=2/3 <=> r=sqrt2 <=> sqrt-mass vector at 45deg to (1,1,1)
                 <=> |doublet projection|^2 = |singlet projection|^2  (PER-IRREP equal).
  Overshoot Q=1 <=> r=2  <=> doublet:singlet = 2:1 in AMPLITUDE^2 (PER-STATE equal,
                 the 2 = doublet dimension).
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 40

M, r, phi = sp.symbols('M r phi', positive=True, real=True)
sm = [M*(1 + r*sp.cos(phi + 2*sp.pi*k/3)) for k in range(3)]
m  = [s**2 for s in sm]
Q  = sp.simplify(sum(m)/sum(sm)**2)
print("Q(r,phi) =", Q, "  (phase-free)")

# S3 decomposition: project sqrt-mass vector v=(sm0,sm1,sm2) onto
#   singlet (democratic) e0 = (1,1,1)/sqrt3
#   doublet (standard 2-dim rep) = orthogonal complement
v = sp.Matrix(sm)
e0 = sp.Matrix([1,1,1])/sp.sqrt(3)
p_singlet = (v.dot(e0))*e0           # projection onto singlet
p_doublet = v - p_singlet            # projection onto doublet (2-dim)
amp_singlet2 = sp.simplify(p_singlet.dot(p_singlet))   # |P_1 v|^2
amp_doublet2 = sp.simplify(p_doublet.dot(p_doublet))   # |P_2 v|^2
print("\n|singlet proj|^2 =", amp_singlet2)
print("|doublet proj|^2 =", amp_doublet2)
ratio_irrep = sp.simplify(amp_doublet2/amp_singlet2)
print("doublet/singlet (|proj|^2 ratio) =", ratio_irrep, " = r^2/2")

# PER-IRREP equal measure: |P_1 v|^2 = |P_2 v|^2  -> ratio = 1 -> r^2 = 2 -> r=sqrt2 -> Q=2/3
r_irrep = sp.solve(sp.Eq(ratio_irrep, 1), r)
print("\nPER-IRREP equal (|P_1|^2 = |P_2|^2): r =", r_irrep, " -> Q =", 
      sp.simplify(Q.subs(r, sp.sqrt(2))), " = KOIDE 2/3")

# PER-STATE equal measure: equal amplitude^2 PER STATE. singlet=1 state, doublet=2 states.
# 'Equal per state' = |P_2 v|^2 / 2  ==  |P_1 v|^2 / 1  -> ratio_irrep = 2 -> r^2=4 -> r=2 -> Q=1
r_state = sp.solve(sp.Eq(ratio_irrep, 2), r)
print("PER-STATE equal (|P_2|^2/2 = |P_1|^2/1): r =", r_state, " -> Q =",
      sp.simplify(Q.subs(r, 2)), " = OVERSHOOT 1")

print("\n=> CONFIRMED: Koide = per-IRREP equipartition; Overshoot = per-STATE equipartition.")
print("   The 'doublet dimension 2' is the ENTIRE difference (r^2: 2 vs 4).")
