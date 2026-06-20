#!/usr/bin/env python3
"""
GAP-2 rep door -- the CRUX theorem, reproduced in-repo (the workflow agent's /tmp scripts were transient).

CLAIM (the SO(4,1) gate in representation language): the defining 5d representation of so(4,1) is
IRREDUCIBLE -- the common kernel of all 10 generators is exactly {0}. Hence there is NO SO(4,1)-invariant
timelike vector u^mu: the de Sitter VACUUM (SO(4,1)-invariant) can induce only true invariants (g_munu, the
volume form), never a preferred frame u^mu. This IS GAP-2: the frame must be selected by a STATE (the
condensate background / the static-patch observer), not by the symmetric vacuum -- and that costs a
postulated VEV (= the kinetic stiffness, relocated, never derived).

Both-ways + quarantine: this PROVES the wall (the gate is real, group-theoretic), and equally shows the
condensate's evasion is a break-by-a-state, not a derivation. a0/Z/kappa/I0 never asserted derived.
"""
import sympy as sp

# de Sitter dS_4 isometry group = SO(4,1), acting on 5d ambient R^{4,1}, metric eta=diag(-1,1,1,1,1).
eta = sp.diag(-1, 1, 1, 1, 1)
n = 5

# Generators M_{AB} (A<B) of so(4,1) in the defining rep:  (M_{AB})^C_D = eta_{AD} delta^C_B - eta_{BD} delta^C_A
def gen(A, B):
    M = sp.zeros(n, n)
    for C in range(n):
        for D in range(n):
            M[C, D] = eta[A, D]*sp.KroneckerDelta(C, B) - eta[B, D]*sp.KroneckerDelta(C, A)
    return M

gens = [gen(A, B) for A in range(n) for B in range(A+1, n)]
print(f"number of so(4,1) generators (A<B over 5 indices) = {len(gens)}  (expect 10 = 5*4/2)")
assert len(gens) == 10

# (1) verify each generator is in so(4,1):  M^T eta + eta M = 0
ok_alg = all(sp.simplify(M.T*eta + eta*M) == sp.zeros(n, n) for M in gens)
print(f"(1) algebra check  M^T eta + eta M = 0 for all 10 generators: {ok_alg}")
assert ok_alg

# (2) COMMON KERNEL: a vector v invariant under SO(4,1) must satisfy M v = 0 for every generator M.
#     Stack all 10 generators and compute the nullspace of the 50x5 system.
v = sp.Matrix(sp.symbols('v0:5'))
big = sp.Matrix.vstack(*[M*v for M in gens])          # 50 linear expressions in v0..v4
A = sp.Matrix([[sp.diff(expr, vi) for vi in v] for expr in big])   # 50 x 5 coefficient matrix
ns = A.nullspace()
print(f"(2) common kernel of all 10 generators (invariant vectors): dimension = {len(ns)}")
print(f"    => the ONLY SO(4,1)-invariant vector is v = 0 : {len(ns) == 0}")
assert len(ns) == 0, "found a nonzero invariant vector -- would CONTRADICT the gate"

# (3) the consequence, stated:
print()
print("THEOREM-OF-THE-WALL (GAP-2, sympy-verified):")
print("  The defining 5d rep of so(4,1) is irreducible (common kernel = {0}).")
print("  => NO SO(4,1)-invariant timelike vector u^mu exists.")
print("  => the SO(4,1) de Sitter VACUUM induces only true invariants (g_munu, vol form), never a frame u^mu.")
print("  => the preferred frame MUST be selected by a STATE (condensate background / static-patch observer),")
print("     not the vacuum -- evaded-not-closed; the kinetic stiffness K_B stays a postulated VEV (f^2~M^2),")
print("     the ghost-condensate postulate relocated one-for-one. GAP-2: rep-label, not a derivation.")
print()
print("ALL ASSERTIONS PASS.")
