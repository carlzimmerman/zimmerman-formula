"""Gate 8: Constraint preservation (MANDATORY).

Compute  dot S_A = { S_A, H_T }  and show that, because the 4x4 Dirac
matrix is invertible on the generic branch, preservation of the four scalar
constraints DETERMINES the four multipliers (lambda_N, mu_1, mu_2, mu_3)
rather than generating additional constraints.

Structure of the preservation equations.  With
    H_T = H_can + int d^3x [ lambda_N S_4 + mu_1 S_1 + mu_2 S_2 + mu_3 S_3
                             + (spatial-diffeo terms) ],
and  Phi_A = (S_4, S_1, S_2, S_3) = (pi_N, C_M, D^2 q, D^2 p),

    dot S_A = { S_A, H_can } + { S_A, sum_B lambda_B S_B }
            = r_A + sum_B Delta_AB lambda_B ,

where  r_A := { S_A, H_can }  is the inhomogeneous term and  Delta_AB =
{ S_A, S_B }  is the Dirac matrix (Gate 3).  The preservation condition
dot S_A = 0 is the linear system

    sum_B Delta_AB lambda_B = - r_A .                                    (*)

We verify, with a symbolic linear solve:
  (1) the coefficient matrix of (*) is exactly the Dirac matrix;
  (2) a unique solution lambda = Delta^{-1} (-r) exists iff det Delta != 0
      (Gate 6 generic branch);
  (3) the solution expresses each multiplier as a linear combination of the
      r_A's -> the multipliers ABSORB the inhomogeneity, generating NO new
      constraints;
  (4) explicit multiplier formulas (row-by-row elimination).
"""

import sympy as sp

print("=" * 70)
print("GATE 8: CONSTRAINT PRESERVATION")
print("=" * 70)

# --- Unknown multipliers and symbolic Dirac entries ---
lamN, mu1, mu2, mu3 = sp.symbols("lambda_N mu_1 mu_2 mu_3")
LN, K, b, c = sp.symbols("L_N K b c")
# Inhomogeneous terms r_A = { S_A, H_can }, A = (S_4, S_1, S_2, S_3)
r4, r1, r2, r3 = sp.symbols("r_4 r_1 r_2 r_3")

# Dirac matrix Delta_AB = { S_A, S_B }, rows/cols = (S_4, S_1, S_2, S_3)
Delta = sp.Matrix([
    [0,   LN,  0,  0],
    [-LN, 0,   b,  c],
    [0,  -b,   0,  K],
    [0,  -c,  -K,  0],
])
lam = sp.Matrix([lamN, mu1, mu2, mu3])
r   = sp.Matrix([r4, r1, r2, r3])

# ------------------------------------------------------------------
# (1) Build the preservation equations  dot S_A = r_A + (Delta lam)_A = 0
# ------------------------------------------------------------------
print("\n--- (1) preservation equations ---")
dotS = r + Delta * lam          # dot S_A = r_A + sum_B Delta_AB lam_B
eqs = [sp.Eq(dotS[i], 0) for i in range(4)]
for i, (S, eq) in enumerate(zip(("S_4","S_1","S_2","S_3"), eqs)):
    print(f"  dot {S:4s} = 0  :  {eq}")

# ------------------------------------------------------------------
# (2) Coefficient matrix of the multiplier system is Delta
# ------------------------------------------------------------------
print("\n--- (2) coefficient matrix === Dirac matrix ---")
# dotS_A = r_A + sum_B Delta_AB lam_B  =>  d(dotS_A)/d(lam_B) = Delta_AB.
coeff = sp.Matrix([[sp.diff(dotS[i], lam[j]) for j in range(4)] for i in range(4)])
print("  d(dotS)/d(lam) == Delta :", sp.simplify(coeff - Delta) == sp.zeros(4,4))

# ------------------------------------------------------------------
# (3) Unique solution exists iff det Delta != 0; solve it
# ------------------------------------------------------------------
print("\n--- (3) unique multiplier solution ---")
detD = sp.simplify(Delta.det())
print("  det Delta =", detD, "  (nonzero on generic branch, Gate 6)")
# Solve Delta lam = -r
sol = Delta.solve(-r)
sol = [sp.simplify(x) for x in sol]
names = ("lambda_N", "mu_1", "mu_2", "mu_3")
for nm, expr in zip(names, sol):
    print(f"  {nm:10s} = {expr}")

# ------------------------------------------------------------------
# (4) Row-by-row elimination (explicit structure)
# ------------------------------------------------------------------
print("\n--- (4) explicit elimination ---")
# Row S_4:  mu1 * LN = -r4   ->  mu1 = -r4 / LN
mu1_explicit = -r4 / LN
print(f"  [S_4 row]  mu_1  = -r_4 / L_N          (L_N elliptic, Gate 4)")
# Rows S_2, S_3:  2x2 system  [[0,K],[-K,0]] [mu2,mu3]^T = -[r2,r3] - [ -b mu1, -c mu1 ]
#   K mu3     = -r2 + b mu1
#  -K mu2     = -r3 + c mu1
mu3_explicit = (-r2 + b*mu1_explicit) / K
mu2_explicit = (r3 - c*mu1_explicit) / K   # from -K mu2 = -r3 + c mu1 -> mu2 = (r3 - c mu1)/K
print(f"  [S_2 row]  mu_3  = (-r_2 + b mu_1) / K  (K = C_q k^4, Gate 5)")
print(f"  [S_3 row]  mu_2  = ( r_3 - c mu_1) / K")
# Row S_1:  -lambda_N LN + b mu2 + c mu3 = -r1  ->  lambda_N = (r1 + b mu2 + c mu3)/LN
lamN_explicit = (r1 + b*mu2_explicit + c*mu3_explicit) / LN
print(f"  [S_1 row]  lambda_N = ( r_1 + b mu_2 + c mu_3) / L_N")

# Verify the explicit formulas equal the matrix solve
sol_explicit = sp.Matrix([lamN_explicit, mu1_explicit, mu2_explicit, mu3_explicit])
match = sp.simplify(sol_explicit - sp.Matrix(sol)) == sp.zeros(4,1)
print("\n  explicit formulas == matrix solve :", match)

# ------------------------------------------------------------------
# (5) No new constraints: the multipliers absorb ALL inhomogeneity
# ------------------------------------------------------------------
print("\n--- (5) no new constraints generated ---")
# Substitute the solved multipliers back into each dotS_A component-wise.
lam_subs = {lamN: sol[0], mu1: sol[1], mu2: sol[2], mu3: sol[3]}
dotS_sub = sp.Matrix([sp.simplify(dotS[i].subs(lam_subs)) for i in range(4)])
print("  dotS_A |_{lam=lam_sol} =", [x for x in dotS_sub],
      " -> all zero:", dotS_sub == sp.zeros(4,1))
# Because a solution exists for ARBITRARY r_A (the inhomogeneous terms are
# just numbers/functions of the fields, not constraints), preservation
# fixes the multipliers and imposes NO further condition on the fields.
print("  => for arbitrary r_A = {S_A, H_can}, a unique multiplier solution")
print("     exists.  Preservation determines (lambda_N, mu_1, mu_2, mu_3)")
print("     and generates NO tertiary constraint.  (Generic branch.)")

all_pass = (sp.simplify(coeff - Delta) == sp.zeros(4,4)
            and match
            and (dotS_sub == sp.zeros(4,1)))
print("\n" + "=" * 70)
print("GATE 8 RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 70)
