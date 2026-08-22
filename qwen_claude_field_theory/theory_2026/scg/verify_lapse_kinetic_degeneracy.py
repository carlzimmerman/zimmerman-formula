"""
Corroboration closure (2026-08-22): the 2-DOF degeneracy condition of the
quadratic SCG + auxiliary-scalar branch is EXACTLY the vanishing of the 2x2
kinetic form in (a_i, D_i phi).

Primary source (SECOND route, independent of arXiv:2604.14490):
  Zhi-Bang Yao & Xian Gao et al.,
  "Spatial covariant gravity with two degrees of freedom in the presence of an
   auxiliary scalar field: perturbation analysis", arXiv:2403.15355,
   Chin. Phys. C (2024) 10.1088/1674-1137/ad47a9.
  Fetched HTML gives, for the concrete d=2 Lagrangian, the degeneracy condition
      Eq. (89):   d2^2 - 4 c4 d1 = 0
  where (in the repo's notation) the quadratic lapse-acceleration sector is
      L2 ⊃ c4 (a_i a^i) + d2 (a_i D^i phi) + d1 (D_i phi D^i phi).

This script confirms Eq.(89) is det(M)=0 for the symmetric kinetic matrix
      M = [[ c4 ,  d2/2 ],
           [ d2/2,  d1  ]]
i.e. the scalar mode is removed by a KINETIC-MATRIX DEGENERACY (rank drop of the
(a_i, D_i phi) sector), NOT by an extra first-class gauge symmetry.  This matches
the Hamiltonian statement (arXiv:1910.13995 / 1806.02811 / 1409.6708): the
lapse-extrinsic-curvature (here lapse-scalar) sector must be degenerate, and the
resulting primary+secondary constraint pair is SECOND-CLASS because the lapse
enters nonlinearly.  The spatial-diffeo momentum constraint H_i stays first-class
by construction (spatial covariance).
"""
import sympy as sp

c4, d2, d1 = sp.symbols('c4 d2 d1', real=True)

# Symmetric kinetic form in the two co-vectors (a_i, D_i phi):
M = sp.Matrix([[c4, d2/sp.Integer(2)],
               [d2/sp.Integer(2), d1]])

det = sp.expand(M.det())                      # = c4*d1 - d2^2/4
eq89_lhs = d2**2 - 4*c4*d1                     # arXiv:2403.15355 Eq.(89) = 0

# det(M)=0  <=>  Eq.(89)=0 : show -4*det equals the Eq.(89) LHS identically.
identity = sp.simplify(eq89_lhs - (-4*det))
assert identity == 0, identity
print("det(M)               =", det)
print("Eq.(89) LHS          =", eq89_lhs)
print("Eq.(89) + 4*det(M)   =", sp.simplify(eq89_lhs + 4*det), " (== 0  =>  Eq.89 <=> det(M)=0)")

# Interpretation: at degeneracy the null direction of M is the combination of
# (a_i, D_i phi) that drops out of the kinetic sector -> no propagating scalar.
c4v, d1v = 1, sp.Rational(1, 4)               # pick c4=1, d1=1/4 -> d2=+-...
d2v = 2*sp.sqrt(c4v*d1v)                       # saturates Eq.(89): d2^2=4c4d1
Mv = M.subs({c4: c4v, d2: d2v, d1: d1v})
print("degenerate example M =", Mv.tolist(), " det =", sp.simplify(Mv.det()),
      " rank =", Mv.rank(), "(=1 => one null direction, scalar removed)")
assert sp.simplify(Mv.det()) == 0 and Mv.rank() == 1
print("PASS: Eq.(89) is exactly the kinetic-matrix degeneracy det(M)=0 (rank 2->1).")
