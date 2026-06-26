#!/usr/bin/env python3
"""
agentT4 — INDEPENDENT computation of the operator-ordering constant lambda in
Kanatchikov & Kholodnyi 2311.05525 eq. (23), the crux of the precanonical-QG
route to a0 ~ sqrt(Lambda).

Eq. (23), 2311.05525 (verbatim):
    lambda = -(1/16) gamma^{IJ} gamma^{KL} [ d/d(omega_mu^{IJ}) , omega_mu^{KL} ] = 3

Context (eqs 11-15, 22):
  - Spin connection term in the pSE (eq 14):
        (1/4) gamma^{IJ} d/d(omega_mu^{IJ})  ( omega_mu^{KL} gamma^{KL} ) acting by
        the COMMUTATOR Clifford product gamma^{IJ} (\vee) Psi := (1/2)[gamma^{IJ}, Psi].
  - lambda := Lambda / (8 pi G hbar kappa)^2   (eq 15) ; Lambda = lambda (8piGhbar kappa)^2 (eq 22)
  - a* := 8 pi G hbar kappa (eq 21);  a0 = 2 a-bar = sqrt(2 Lambda/lambda) (eq 32)

This script:
  (1) builds the Clifford algebra Cl(1,3) with a concrete real gamma rep,
      metric eta = diag(+1,-1,-1,-1) (the paper's signature, eq line ~86/90:
      gamma^I gamma^J + gamma^J gamma^I = 2 eta^{IJ}),
  (2) builds gamma^{IJ} = (1/2)[gamma^I, gamma^J] (the paper's normalization, 2511 eq 5/6
      gamma^{IJ}=1/2(gamma^I gamma^J - gamma^J gamma^I)),
  (3) computes the c-number from the ordering commutator
        [ d/d(omega_mu^{IJ}) , omega_mu^{KL} ] = delta^{IJ}_{KL} delta_mu^mu
      with the antisymmetric Kronecker delta^{IJ}_{KL} = delta^I_K delta^J_L - delta^I_L delta^J_K
      and the mu-sum,
  (4) contracts with gamma^{IJ} gamma^{KL} and traces, several index conventions,
      to see what numbers are forced and which are convention-dependent.

ALL NUMBERS MACHINE-COMPUTED. No value is hard-coded to a target.
"""
import sympy as sp
import itertools

# ---------------------------------------------------------------------------
# 1. Concrete gamma matrices for Cl(1,3), eta = diag(+1,-1,-1,-1).
#    Dirac representation (standard). Entries are exact (0, +/-1, +/-i).
# ---------------------------------------------------------------------------
I2 = sp.eye(2)
Z2 = sp.zeros(2)
i  = sp.I

sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -i], [i, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])

def block(A, B, C, D):
    return sp.Matrix(sp.BlockMatrix([[A, B], [C, D]]))

# Dirac basis: gamma^0 = diag(I,-I); gamma^k = [[0, sigma_k],[-sigma_k,0]]
g0 = block(I2, Z2, Z2, -I2)
g1 = block(Z2, sx, -sx, Z2)
g2 = block(Z2, sy, -sy, Z2)
g3 = block(Z2, sz, -sz, Z2)
gamma = [g0, g1, g2, g3]

eta = sp.diag(1, -1, -1, -1)

# sanity: Clifford relation g^I g^J + g^J g^I = 2 eta^{IJ} * 1_4
ok = True
for a in range(4):
    for b in range(4):
        lhs = gamma[a]*gamma[b] + gamma[b]*gamma[a]
        rhs = 2*eta[a, b]*sp.eye(4)
        if sp.simplify(lhs - rhs) != sp.zeros(4):
            ok = False
print("Clifford relation g^I g^J + g^J g^I = 2 eta^IJ holds:", ok)

# ---------------------------------------------------------------------------
# 2. gamma^{IJ} = (1/2)[gamma^I, gamma^J]   (paper normalization, 2511 eq 5/6).
#    Antisymmetric in (I,J): gamma^{IJ} = -gamma^{JI}, gamma^{II}=0.
# ---------------------------------------------------------------------------
def gIJ(a, b):
    return (gamma[a]*gamma[b] - gamma[b]*gamma[a]) / 2

# Independent antisymmetric pairs IJ with I<J : 6 of them in 4D.
pairs = [(a, b) for a in range(4) for b in range(4) if a < b]
print("number of independent gamma^{IJ} (I<J):", len(pairs))

# ---------------------------------------------------------------------------
# 3. The ordering commutator c-number.
#    [ d/d(omega_mu^{IJ}) , omega_nu^{KL} ] = delta_mu^nu * Delta^{IJ}_{KL},
#    where Delta^{IJ}_{KL} is the identity on the antisymmetric (I,J)<->(K,L) pair.
#    With omega_mu^{IJ} taken antisymmetric in (IJ), the canonical pairing is
#      d/d(omega_mu^{IJ}) omega_mu^{KL} = delta_mu^mu (delta^I_K delta^J_L - delta^I_L delta^J_K).
#    The c-number that the WEYL (symmetric) ordering leaves over is exactly the
#    (1/2) of the full commutator -> but eq (14)'s factor 1/4 and the (\vee)=1/2[,]
#    already carry those halves. We compute the bare contraction first, then track
#    every factor explicitly in step 5.
# ---------------------------------------------------------------------------

# Delta^{IJ}_{KL} on antisym pairs: 1 if {IJ}=={KL} as ordered antisym pair, with sign.
def delta_anti(a, b, c, d):
    # delta^a_c delta^b_d - delta^a_d delta^b_c
    return (1 if (a == c and b == d) else 0) - (1 if (a == d and b == c) else 0)

# ---------------------------------------------------------------------------
# 4. The Clifford contraction  S := sum_{IJ,KL} gamma^{IJ} gamma^{KL} Delta^{IJ}_{KL}
#    Two natural index conventions for the (IJ),(KL) sums:
#      (A) FREE sum over all I,J,K,L in 0..3 (each runs independently, 4^4 terms).
#          Then gamma^{IJ} Delta^{IJ}_{KL} gamma^{KL} = sum gamma^{IJ} gamma_{IJ}-style.
#      (B) ORDERED sum over independent antisym pairs I<J, K<L (6x6 terms),
#          which avoids double counting the (IJ) vs (JI) copies.
#    The paper writes summed (repeated) indices IJ,KL with NO I<J restriction, i.e.
#    convention (A) (Einstein summation over all four indices). We compute BOTH.
# ---------------------------------------------------------------------------

# Convention (A): full Einstein sum over I,J,K,L = 0..3
S_A = sp.zeros(4)
for (a, b, c, d) in itertools.product(range(4), repeat=4):
    coeff = delta_anti(a, b, c, d)
    if coeff != 0:
        S_A += coeff * (gIJ(a, b) * gIJ(c, d))
# This is sum_{IJKL} gamma^{IJ} gamma^{KL} (delta^I_K delta^J_L - delta^I_L delta^J_K)
trS_A = sp.simplify(sp.trace(S_A))
# Is S_A proportional to identity?
S_A_simpl = sp.simplify(S_A)
print("\n--- Convention (A): full Einstein sum over I,J,K,L=0..3 ---")
print("S_A proportional to 1_4 ?", S_A_simpl == sp.simplify(S_A_simpl[0,0])*sp.eye(4))
print("S_A[0,0] =", sp.simplify(S_A_simpl[0,0]))
print("Tr S_A =", trS_A, "   Tr S_A / 4 =", sp.nsimplify(trS_A/4))

# Convention (B): ordered independent pairs I<J, K<L
S_B = sp.zeros(4)
for (a, b) in pairs:
    for (c, d) in pairs:
        coeff = delta_anti(a, b, c, d)
        if coeff != 0:
            S_B += coeff * (gIJ(a, b) * gIJ(c, d))
trS_B = sp.simplify(sp.trace(S_B))
S_B_simpl = sp.simplify(S_B)
print("\n--- Convention (B): ordered pairs I<J, K<L (6x6) ---")
print("S_B proportional to 1_4 ?", S_B_simpl == sp.simplify(S_B_simpl[0,0])*sp.eye(4))
print("S_B[0,0] =", sp.simplify(S_B_simpl[0,0]))
print("Tr S_B =", trS_B, "   Tr S_B / 4 =", sp.nsimplify(trS_B/4))

# ---------------------------------------------------------------------------
# 5. Assemble lambda under the paper's prefactor -1/16, with the mu-sum.
#    Eq (23): lambda = -(1/16) gamma^{IJ} gamma^{KL} [d/d omega_mu^{IJ}, omega_mu^{KL}]
#    The [.,.] gives Delta^{IJ}_{KL} * (sum over mu of delta_mu^mu).
#    In 4D spacetime mu = 0..3 -> sum_mu delta_mu^mu = 4.
#    The whole thing is a c-number = (operator) acting as multiple of identity;
#    the scalar lambda is read off as the coefficient of 1_4 (i.e. (1/4)Tr).
# ---------------------------------------------------------------------------
mu_sum = 4   # sum_{mu=0}^{3} delta_mu^mu  (number of spacetime dims)

print("\n=============== lambda assembled (coefficient of 1_4) ===============")
for tag, trS in [("A full-Einstein", trS_A), ("B ordered-pairs", trS_B)]:
    # gamma^{IJ}gamma^{KL}Delta = S (a matrix ~ c*1_4); scalar c = Tr/4
    c_scalar = sp.nsimplify(trS/4)
    # with mu-sum and the -1/16 prefactor
    lam_with_mu   = sp.nsimplify(sp.Rational(-1,16) * c_scalar * mu_sum)
    lam_no_mu     = sp.nsimplify(sp.Rational(-1,16) * c_scalar)
    print(f"[{tag}] scalar(gIJgKL Delta)=Tr/4 = {c_scalar}")
    print(f"        lambda = -1/16 * scalar * (mu-sum=4) = {lam_with_mu}")
    print(f"        lambda = -1/16 * scalar (NO mu-sum)  = {lam_no_mu}")

# ---------------------------------------------------------------------------
# 6. Cross-check the key Clifford identity that drives the number:
#    sum_{IJ} gamma^{IJ} gamma_{IJ}  (with metric raising/lowering) and
#    sum_{IJ} gamma^{IJ} gamma^{IJ} (no metric, flat sum) -- these differ and are
#    the heart of the convention dependence.
# ---------------------------------------------------------------------------
print("\n--- Clifford scalar identities (diagnostic) ---")
# (a) full Einstein sum gamma^{IJ} gamma^{IJ} (no metric on the contraction)
T1 = sp.zeros(4)
for a in range(4):
    for b in range(4):
        T1 += gIJ(a, b)*gIJ(a, b)
print("sum_{I,J=0..3} gamma^{IJ}gamma^{IJ}  = (Tr/4)*1 with Tr/4 =", sp.nsimplify(sp.trace(sp.simplify(T1))/4))
# (b) metric-contracted gamma^{IJ} gamma_{IJ} = eta_{IK}eta_{JL} gamma^{IJ}gamma^{KL}
T2 = sp.zeros(4)
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                T2 += eta[a,c]*eta[b,d]*gIJ(a,b)*gIJ(c,d)
print("gamma^{IJ}gamma_{IJ} (metric)        = (Tr/4)*1 with Tr/4 =", sp.nsimplify(sp.trace(sp.simplify(T2))/4))
# (c) ordered-pairs gamma^{IJ}gamma_{IJ} (I<J, metric)
T3 = sp.zeros(4)
for (a,b) in pairs:
    T3 += eta[a,a]*eta[b,b]*gIJ(a,b)*gIJ(a,b)
print("sum_{I<J} gamma^{IJ}gamma_{IJ}        = (Tr/4)*1 with Tr/4 =", sp.nsimplify(sp.trace(sp.simplify(T3))/4))
print("sum_{I<J} gamma^{IJ}gamma^{IJ} (flat) = (Tr/4)*1 with Tr/4 =", sp.nsimplify(sp.trace(sp.simplify(S_B))/4))
