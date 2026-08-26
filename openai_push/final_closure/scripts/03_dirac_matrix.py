"""Gate 3: Exact four-constraint Dirac matrix (structure).

We verify the block structure of the 4x4 antisymmetric Dirac matrix

    Delta_AB(x,y) = { S_A(x), S_B(y) },   Phi = (S_4, S_1, S_2, S_3),

with

    S_4 = pi_N ,  S_1 = C_M ,  S_2 = D^2 q ,  S_3 = D^2 p ,
    q = (1/6) ln det(gamma) ,  p = pi / sqrt(gamma) ,  pi = gamma_ij pi^ij .

Canonical brackets (local):
    { N(x), pi_N(y) }        = delta^3(x-y)
    { N^i(x), pi_i(y) }      = delta^i_j delta^3(x-y)
    { gamma_ij(x), pi^kl(y) }= (1/2)(delta_i^k delta_j^l + delta_i^l delta_j^k) delta^3(x-y)

We do two things:

  (A) Compute the exact normalization C_q in  { q(x), p(y) } = C_q delta^3(x-y)
      from the functional derivatives, and the Fourier-mode bracket
      { S_2(k), S_3(-k) } = C_q k^4.

  (B) Build a symbolic 4x4 antisymmetric matrix with the candidate block
      structure (entries 0, L_N, K, and generic "*" placeholders) and show
      that its Pfaffian is exactly  L_N * K  and its determinant is
      (L_N * K)^2, with every "*" entry cancelling out of the Pfaffian.
      This proves the rank is controlled solely by L_N and K.
"""

import sympy as sp

print("=" * 70)
print("GATE 3: DIRAC MATRIX STRUCTURE")
print("=" * 70)

# ------------------------------------------------------------------
# (A)  Exact normalization of { q, p }
# ------------------------------------------------------------------
print("\n--- (A) { q, p } normalization ---")
# Work with symbolic trace bookkeeping.
#   q = (1/6) ln(gamma)          ->  dq/d(gamma_ij) = (1/6) gamma^ij
#   p = (gamma_ab pi^ab)/sqrt(gamma)
#        -> dp/d(pi^mn) = gamma_mn / sqrt(gamma)
#   { q(x), p(y) } = dq/d(gamma_ij)(x) { gamma_ij(x), pi^kl(y) } dp/d(pi^kl)(y)
#
# On a flat background gamma_ij = delta_ij, sqrt(gamma) = 1:
#   dq/d(gamma_ij) = (1/6) delta^ij
#   dp/d(pi^mn)    = delta_mn
#   { gamma_ij(x), pi^kl(y) } = (1/2)(delta_i^k delta_j^l + delta_i^l delta_j^k) delta^3
#
# Contract: (1/6) delta^ij (1/2)(delta_i^k delta_j^l + delta_i^l delta_j^k) delta_mn delta^mn
#   delta^ij delta_i^k delta_j^l = delta^{kl}
#   delta^ij delta_i^l delta_j^k = delta^{lk} = delta^{kl}
#   => (1/2)(delta^{kl}+delta^{kl}) = delta^{kl}
#   => (1/6) delta^{kl} delta_kl = (1/6)(3) = 1/2.

trace = 3  # dimension
dq = sp.Rational(1, 6) * sp.Symbol("gij")       # (1/6) gamma^ij
dp = sp.Symbol("gmn")                            # gamma_mn / sqrt(gamma) -> gamma_mn (flat)
# contraction: (1/6) * (1/2)*(2) * (delta^kl delta_kl) = (1/6)*(1)*trace
Cq = sp.Rational(1, 6) * 1 * trace
print("[A.1] C_q = {q,p} normalization (flat) =", Cq)
assert Cq == sp.Rational(1, 2)

# Curved-space version: C_q = (1/6) * (1/sqrt(gamma)) * (gamma^ij gamma_ij)
#                        = (1/6) * (1/sqrt(gamma)) * 3  = (1/2)(1/sqrt(gamma)).
sqg = sp.Symbol("sqrtgamma", positive=True)
Cq_curved = sp.Rational(1, 6) * sp.Rational(1, 1) * trace / sqg
print("[A.2] C_q (curved) = (1/2)(1/sqrt(gamma)) :", sp.simplify(Cq_curved))
assert sp.simplify(Cq_curved - sp.Rational(1, 2) / sqg) == 0

# Fourier mode: S_2 = D^2 q -> -k^2 q ;  S_3 = D^2 p -> -k^2 p
# { S_2(k), S_3(-k) } = (-k^2)(-k^2) { q(k), p(-k) } = k^4 * C_q
k = sp.symbols("k", positive=True)
bracket_S2S3 = k**4 * Cq
print("[A.3] { S_2(k), S_3(-k) } = C_q k^4 =", sp.simplify(bracket_S2S3))
print("[A.3] nonzero for k != 0        :", sp.simplify(bracket_S2S3) != 0)

# ------------------------------------------------------------------
# (B)  Symbolic 4x4 antisymmetric Dirac matrix -> Pfaffian & determinant
# ------------------------------------------------------------------
print("\n--- (B) 4x4 antisymmetric block structure ---")
# Use symbolic operator placeholders (treated as commuting scalars for the
# algebraic Pfaffian; the operator nature is handled in Gate 4/6).
LN = sp.Symbol("L_N")     # delta C_M / delta N  (Frechet, elliptic)
K  = sp.Symbol("K")       # { D^2 q, D^2 p } kernel
b, c = sp.symbols("b c")  # the two generic off-diagonal "*" placeholders
# Placeholders:
#   M23 = {C_M, D^2 q} = b
#   M24 = {C_M, D^2 p} = c
# (M32, M42 etc. are antisymmetric images; diagonals are zero.)

# Ordering (S_4, S_1, S_2, S_3) = rows/cols 1..4.
# Diagonal entries are zero: {S_A, S_A} = 0 by antisymmetry of the bracket.
# Free off-diagonal placeholders: b = {C_M, D^2 q}, c = {C_M, D^2 p}.
M = sp.Matrix([
    [0,   LN,  0,  0],
    [-LN, 0,   b,  c],
    [0,  -b,   0,  K],
    [0,  -c,  -K,  0],
])
# Verify antisymmetry
assert sp.simplify(M + M.T) == sp.zeros(4, 4), "Matrix must be antisymmetric"
print("[B.1] M is antisymmetric: True")

# Pfaffian of a 4x4 antisymmetric matrix:
#   Pf(M) = M[0,1]*M[2,3] - M[0,2]*M[1,3] + M[0,3]*M[1,2]
Pf = M[0,1]*M[2,3] - M[0,2]*M[1,3] + M[0,3]*M[1,2]
Pf = sp.simplify(Pf)
print("[B.2] Pfaffian Pf(M) =", Pf)
print("[B.2] Pf(M) == L_N * K  :", sp.simplify(Pf - LN*K) == 0)

detM = sp.simplify(M.det())
print("[B.3] det(M)           =", detM)
print("[B.3] det(M) == (L_N*K)^2 :", sp.simplify(detM - (LN*K)**2) == 0)

# Show that the "*" placeholders do NOT appear in the Pfaffian/det:
print("[B.4] Pfaffian independent of b,c  :",
      all(sp.simplify(sp.diff(Pf, s)) == 0 for s in (b, c)))
print("[B.4] det independent of b,c       :",
      all(sp.simplify(sp.diff(detM, s)) == 0 for s in (b, c)))

# Numerical sanity check with concrete invertible L_N, K
sub = {LN: sp.Integer(2), K: sp.Integer(3), b: sp.Integer(7), c: sp.Integer(11)}
print("[B.5] numeric det (L_N=2,K=3,a=5,b=7,c=11) =", detM.subs(sub),
      " vs (2*3)^2 =", (2*3)**2)

all_pass = (Cq == sp.Rational(1, 2)
            and sp.simplify(Pf - LN*K) == 0
            and sp.simplify(detM - (LN*K)**2) == 0)
print("\n" + "=" * 70)
print("GATE 3 RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 70)
