#!/usr/bin/env python3
"""
Constraint / DOF count for Metric-Bundle-MMG, and the consistency of ADDING the slip
constraint chi = (Phi-Psi)/c^2 = 0 on top of the MMG scalar machinery.

Phase space (ADM single metric), per point:
  gamma_ij (6) + pi^ij (6) + N (1) + pi_N (1) + N^i (3) + pi_i (3) = 20.

Baseline MMG constraint content (as given):
  FIRST CLASS  (spatial diff):  pi_i (3), H_i (3)                          -> F0 = 6
  SECOND CLASS (lapse/scalar):  pi_N (1), C_MB (1), D^2 q (1), D^2 p (1)   -> S0 = 4
  intended N_grav = 2.

DOF formula (per point):  N = (1/2) [ P - 2*F - S ],  F=#first-class, S=#second-class.

Question: add chi=0 (slip). Naive count with/without it. Is chi first- or second-class
against C_MB and pi_N? Does adding it change the count inconsistently (odd second-class rank)?

Everything below is EXACT sympy: the DOF arithmetic, the antisymmetric-rank theorem, and the
explicit emergent first-class null vector. No scaling estimates.
"""
import sympy as sp

def Ndof(P, F, S):
    """configuration-space DOF per point"""
    val = sp.Rational(P - 2*F - S, 2)
    return val

print("="*78)
print("STEP 0 -- DOF formula sanity check on pure GR")
print("="*78)
# GR: P=20, FC = pi_N,pi_i,H,H_i = 1+3+1+3 = 8, SC = 0
gr = Ndof(20, 8, 0)
print(f"  GR: P=20, F=8, S=0  ->  N = {gr}   (expect 2 graviton polarizations)")
assert gr == 2, "GR sanity FAILED"
print("  OK.")

print("\n"+"="*78)
print("STEP 1 -- Metric-Bundle-MMG WITHOUT the slip constraint")
print("="*78)
P = 20
F0 = 6          # pi_i(3) + H_i(3), first class (spatial diffeos)
S0 = 4          # pi_N, C_MB, D^2 q, D^2 p, mutually second class (rank 4)
print(f"  phase space P          = {P}")
print(f"  first-class  F0        = {F0}   (pi_i x3, H_i x3)")
print(f"  second-class S0        = {S0}   (pi_N, C_MB, D^2 q, D^2 p)")
N_noslip = Ndof(P, F0, S0)
print(f"  N_grav (no slip)       = (1/2)[{P} - 2*{F0} - {S0}] = {N_noslip}")
print("  -> matches the INTENDED 2 iff the 4 lapse/scalar constraints are mutually")
print("     second class with FULL rank 4 (their 4x4 Poisson matrix nonsingular).")
assert N_noslip == 2

print("\n"+"="*78)
print("STEP 2 -- Is the 4-set genuinely rank-4 second class? (needed for N=2)")
print("="*78)
print("  A set of 2m constraints is 'fully second class' iff its antisymmetric")
print("  Poisson matrix Delta_ab = {C_a, C_b} is NONsingular (rank 2m).")
print("  For the baseline to give exactly 2, Delta_(4x4) over {pi_N,C_MB,D^2q,D^2p}")
print("  must have rank 4.  Build a GENERIC full-rank 4x4 antisymmetric matrix A:")
a12,a13,a14,a23,a24,a34 = sp.symbols('a12 a13 a14 a23 a24 a34', real=True)
A = sp.Matrix([
    [ 0,    a12,  a13,  a14],
    [-a12,  0,    a23,  a24],
    [-a13, -a23,  0,    a34],
    [-a14, -a24, -a34,  0 ]])
detA = sp.expand(A.det())
print("  det A =", detA)
print("       = (a14*a23 - a13*a24 + a12*a34)^2   [ = Pfaffian(A)^2, a perfect square ]")
pf = a12*a34 - a13*a24 + a14*a23
assert sp.expand(detA - pf**2) == 0
print("  => generic A is nonsingular (rank 4) whenever the Pfaffian != 0. Baseline CAN give 2. OK.")

print("\n"+"="*78)
print("STEP 3 -- ADD the slip: chi=0 becomes a 5th lapse/scalar constraint")
print("="*78)
print("  The slip chi = ln N + q = (Phi-Psi)/c^2 (committed identity, mmg_slip_reconciliation.py).")
print("  It is built from N and gamma, i.e. it lives in the SAME lapse/scalar block as")
print("  {pi_N, C_MB, D^2 q, D^2 p}. So the second-class candidate set becomes 5 constraints:")
print("     {pi_N, C_MB, D^2 q, D^2 p, chi}.")
print("  Its Poisson matrix is a 5x5 ANTISYMMETRIC matrix Delta5 = [[A, b],[-b^T, 0]],")
print("  where b_i = {C_i, chi} for i in the 4-set.")
b1,b2,b3,b4 = sp.symbols('b1 b2 b3 b4', real=True)   # {pi_N,chi},{C_MB,chi},{D^2q,chi},{D^2p,chi}
b = sp.Matrix([b1,b2,b3,b4])
Delta5 = sp.Matrix.vstack(
    sp.Matrix.hstack(A, b),
    sp.Matrix.hstack(-b.T, sp.Matrix([[0]])))
print("\n  Delta5 =")
sp.pprint(Delta5)
det5 = sp.expand(Delta5.det())
print("\n  det(Delta5) =", det5)
print("  THEOREM (odd antisymmetric): every antisymmetric matrix of ODD size is singular.")
assert det5 == 0, "odd antisymmetric determinant should vanish identically"
print("  -> det(Delta5) == 0 IDENTICALLY (verified). So the 5 constraints canNOT all be")
print("     mutually second class: the Dirac matrix is degenerate.")

print("\n"+"="*78)
print("STEP 4 -- Rank and null space of Delta5 when A is full-rank (baseline healthy)")
print("="*78)
print("  Pick a concrete full-rank A (Pfaffian=1) and generic b to read off rank/nullity:")
subs_full = {a12:1, a13:0, a14:0, a23:0, a24:0, a34:1,   # Pfaffian = a12*a34 = 1  (nonsingular)
             b1:sp.Rational(2), b2:sp.Rational(-3), b3:sp.Rational(5), b4:sp.Rational(7)}
A_num = A.subs(subs_full)
D5_num = Delta5.subs(subs_full)
print("  rank(A_4x4)   =", A_num.rank(), "  (full rank 4 -> baseline S0=4, N=2 as designed)")
print("  rank(Delta5)  =", D5_num.rank(), "  (even, <=4: an odd antisym matrix has EVEN rank)")
print("  nullity       =", 5 - D5_num.rank())
ns = D5_num.nullspace()
print("  null space dimension =", len(ns))
v = ns[0]
v = v / v[4] if v[4] != 0 else v      # normalize so chi-component = 1 if possible
print("  null vector (normalized on chi-slot) v =", sp.simplify(v.T))
print("  -> chi-component of the null (first-class) direction =", sp.simplify(v[4]))
assert v[4] != 0
print("  NONZERO. The emergent first-class combination NECESSARILY contains chi.")

print("\n"+"="*78)
print("STEP 5 -- General proof: the null vector is v = (-A^{-1} b, 1), chi-slot ALWAYS 1")
print("="*78)
print("  Solve Delta5 v = 0 with v=(x,c):  A x + b c = 0  and  -b^T x = 0.")
print("  From the first block: x = -A^{-1} b c.")
Ainv = A.inv()
x_gen = sp.simplify(-Ainv*b)     # times c
print("  x/c = -A^{-1} b =")
sp.pprint(sp.simplify(x_gen))
print("  Check the second block -b^T x = +c * b^T A^{-1} b must vanish:")
quad = sp.simplify((b.T*Ainv*b)[0])
print("    b^T A^{-1} b =", quad)
print("  LEMMA: A^{-1} of an antisymmetric A is antisymmetric => b^T A^{-1} b is an")
print("         antisymmetric quadratic form => identically 0.  (verified:", quad==0, ")")
assert quad == 0
print("  => v = c*(-A^{-1} b, 1) solves Delta5 v = 0 for ANY b, with chi-slot = 1 (nonzero).")
print("  CONCLUSION: whenever A (the 4-set) is nonsingular, bordering it with chi ALWAYS")
print("  produces exactly ONE first-class combination, and chi appears in it with unit weight.")
print("  chi is therefore NEVER purely second class against {pi_N, C_MB, D^2q, D^2p};")
print("  it is second class against 3 independent directions and FIRST class along one.")

print("\n"+"="*78)
print("STEP 6 -- Recount the DOF with the slip added (two exhaustive branches)")
print("="*78)
print("  The 5-set splits as: 4 second-class (rank of Delta5) + 1 first-class (nullity).")
print("  Spatial-diff first class unchanged: F0 = 6.")
F_with = 6 + 1     # 6 spatial + 1 emergent first-class combination
S_with = 4         # rank(Delta5)=4 second class
N_with = Ndof(P, F_with, S_with)
print(f"  BRANCH A (emergent constraint is a genuine gauge generator, closes under evolution):")
print(f"     F = {F_with} (6 spatial + 1 emergent), S = {S_with}")
print(f"     N_grav = (1/2)[{P} - 2*{F_with} - {S_with}] = {N_with}")
print(f"     -> N_grav = {N_with} < intended 2.  A tensor polarization is traded for a SPURIOUS")
print(f"        gauge symmetry.  OVERCONSTRAINED.  (This is the 'drives N_grav below 2' failure.)")
assert N_with == 1

print("\n  BRANCH B (emergent first-class chi_FC does NOT commute with H_total):")
print("     Dirac consistency  d/dt chi_FC = {chi_FC, H_total} ~ 0  is not automatic.")
print("     - if it yields a NEW independent (secondary) constraint chi', add it: the pair")
print("       (chi_FC, chi') is generically second class -> S=6, F=6 ->")
N_branchB = Ndof(P, 6, 6)
print(f"         N_grav = (1/2)[{P} - 12 - 6] = {N_branchB}  (even further below 2), or")
print("     - if {chi_FC, H_total} reduces to a NONZERO phase-space function with no new")
print("       constraint, the Lagrange multiplier is fixed inconsistently => 0 = (nonzero):")
print("       the constraint algebra is INCONSISTENT (no solution). Hard kill.")
print("  In NEITHER branch does the count return to 2.")

print("\n"+"="*78)
print("STEP 7 -- The only escape, and why it is barred here (honesty check)")
print("="*78)
print("  Escape would require chi to be DEPENDENT on {pi_N,C_MB,D^2q,D^2p} on the constraint")
print("  surface (then adding it is redundant, count stays 2, but slip=0 is not a NEW input).")
print("  But committed DC-013 / mmg_slip_reconciliation.py show the single-metric structure")
print("  LOCKS a nonzero slip: on the constraint surface D^2 q=0 forces lap(Psi)=0 (Newtonian)")
print("  while the MOND lapse gives Phi=sqrt(GM a0)ln r => Phi != Psi => chi != 0 there.")
print("  Hence chi=0 is INDEPENDENT of (indeed INCOMPATIBLE with) the existing 4 constraints,")
print("  so the redundant/vacuous escape is barred. We are forced into Steps 3-6. KILL.")

print("\n"+"="*78)
print("SUMMARY")
print("="*78)
print(f"  WITHOUT slip:  P=20, F=6, S=4  ->  N_grav = {N_noslip}   (consistent, rank-4 even 2nd class)")
print(f"  WITH slip:     5th 2nd-class candidate -> Delta5 (5x5 antisym) is SINGULAR (det=0)")
print(f"                 => rank 4 + nullity 1 => 1 emergent FIRST-class combo (chi-weight=1)")
print(f"                 => F=7, S=4 -> N_grav = {N_with}  (Branch A), or new secondary/")
print(f"                    inconsistency (Branch B).  NEVER returns to 2.")
print(f"  chi vs (pi_N, C_MB): second class against 3 directions, FIRST class along one")
print(f"                       combination -> mixed, and the first-class piece is the killer.")
print(f"  VERDICT: the slip constraint CANNOT be added to Metric-Bundle-MMG without")
print(f"           overconstraining (N_grav 2 -> 1) or making the 2nd-class system")
print(f"           odd-rank/inconsistent. DEAD as a way to legislate Phi=Psi.")
