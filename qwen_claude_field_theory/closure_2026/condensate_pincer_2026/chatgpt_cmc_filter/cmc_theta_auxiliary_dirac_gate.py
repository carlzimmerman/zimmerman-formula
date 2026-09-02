#!/usr/bin/env python3
"""
cmc_theta_auxiliary_dirac_gate.py

Reduced canonical check for making the branch-selective filter variable Theta
an honest NONDYNAMICAL auxiliary, not a dark matter field.

Use ADM trace momentum pi and impose the auxiliary constraint

    C_Theta = Theta + pi/(M_P^2 sqrt(gamma)) = 0.

With the standard Einstein-Hilbert ADM convention,
    pi = -M_P^2 sqrt(gamma) K,
so
    Theta = K.

Therefore:
  static time-symmetric galaxy branch: pi=K=0 -> Theta=0,
  FLRW: K=3H -> Theta=3H.

Add the nondynamical filter auxiliary chi with

    C_chi = [k^2 + a^2 xi^2 Theta^2/(9 c^2)] chi - k^2 n = 0.

Primary auxiliary momenta:
    p_Theta = 0,
    p_chi   = 0.

Question:
Does the (Theta,chi) extension itself add a propagating canonical mode?

The 4x4 auxiliary Dirac matrix is computed exactly.
"""

import sympy as sp

Theta, pTheta, chi, pchi = sp.symbols("Theta pTheta chi pchi", real=True)
q, pq = sp.symbols("q pq", real=True)
n, pn = sp.symbols("n pn", real=True)

alpha, k2, b = sp.symbols("alpha k2 b", positive=True, real=True)

coords = [Theta, chi, q, n]
moms   = [pTheta, pchi, pq, pn]

# alpha stands for 1/(M_P^2 sqrt(gamma)) in the reduced scalar model.
CTheta = Theta + alpha*pq
Cchi = (k2 + b*Theta**2)*chi - k2*n

constraints = [pTheta, CTheta, pchi, Cchi]

def PB(F,G):
    return sp.expand(sum(
        sp.diff(F,qi)*sp.diff(G,pi)-sp.diff(F,pi)*sp.diff(G,qi)
        for qi,pi in zip(coords,moms)
    ))

D = sp.Matrix([[PB(F,G) for G in constraints] for F in constraints])
detD = sp.factor(D.det())

print("AUXILIARY CONSTRAINTS")
print("---------------------")
print("p_Theta = 0")
print("C_Theta = Theta + alpha*pi = 0")
print("p_chi = 0")
print("C_chi = (k^2+b Theta^2) chi - k^2 n = 0")
print()

print("AUXILIARY DIRAC MATRIX")
print("----------------------")
sp.pprint(D)
print()
print("det =", detD)

target = (k2 + b*Theta**2)**2
assert sp.simplify(detD-target) == 0

print()
print("STATIC BRANCH Theta=0")
print("---------------------")
static_det = sp.simplify(detD.subs(Theta,0))
print("det =", static_det)
assert static_det == k2**2
print("For k!=0, full auxiliary rank remains 4.")

print()
print("FLRW BRANCH Theta=3H")
print("--------------------")
H = sp.symbols("H", positive=True, real=True)
flrw_det = sp.factor(detD.subs(Theta,3*H))
print("det =", flrw_det)
assert sp.simplify(flrw_det - (k2+9*b*H**2)**2) == 0

print()
print("DOF COUNT OF AUXILIARY EXTENSION")
print("--------------------------------")
print("Two auxiliary canonical pairs = 4 phase-space dimensions.")
print("Four second-class constraints remove all 4.")
print("=> zero local propagating auxiliary DOF in this reduced canonical block.")

print()
print("PHYSICAL IDENTIFICATION")
print("-----------------------")
print("With alpha=1/(M_P^2 sqrt(gamma)) and pi=-M_P^2 sqrt(gamma) K:")
print("C_Theta=0 => Theta=K.")
print("Static K=0 => filter mass vanishes exactly.")
print("FLRW K=3H => filter mass = xi H/c.")

print()
print("VERDICT")
print("-------")
print("PASS (reduced auxiliary gate): Theta and chi can both be introduced as")
print("second-class nondynamical auxiliaries; no dark/dustlike propagating mode")
print("is required to obtain the branch-selective Hubble filter.")
print()
print("OPEN:")
print("The COMPLETE gravity+MOND+Theta+chi constraint matrix must still be")
print("computed. Cross-brackets may alter the gravitational scalar chain.")
