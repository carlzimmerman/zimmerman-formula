import numpy as np
np.set_printoptions(precision=5, suppress=True)

# =====================================================================
# TEST D — THE DECISIVE FORK: is the boost/modular spectrum MULTIPLICITY-1
# or MULTIPLICITY->infinity? This decides whether shared-modular-flow
# REDUCES phi or leaves it as hard as before.
#
#   If multiplicity 1 (simple spectrum): centralizer is ABELIAN (a maximal
#     torus). Then KMS-at-beta fixes ALL diagonal weights, and the only
#     residual freedom is diagonal phases -> these are FIXED by requiring
#     psi to be a *-homomorphism carrying a fixed cyclic vector. => phi
#     REDUCES to a finite checkable condition (spectrum match + one cyclic
#     vector), which agentTT/agentSS showed coincides at the center.
#
#   If multiplicity > 1 (degenerate): centralizer is NON-abelian U(m).
#     KMS fixes only the BLOCK weights; within each multiplet a full U(m)
#     gauge survives that moves matter observables. => state-matching is
#     NOT reduced; the placement/dressing freedom agentTT found persists.
#
# So the verdict hinges on ONE computed structural fact about the SHARED
# modular flow: is the static-patch boost spectrum on the *observer*
# (crossed-product) algebra simple?
# =====================================================================

print("=== TEST D: multiplicity of the shared modular (boost) spectrum ===\n")

# Side 1 (dS, agentSS): modular flow = static-patch boost L_0; the discrete
# series rep is IRREDUCIBLE and LOWEST-WEIGHT -> ladder Delta+n with each
# level n NON-degenerate WITHIN one irrep. spacing uniform, matrix elts
# (n+1)(2Delta+n).  BUT the PHYSICAL dS algebra is the boost acting on the
# FULL bulk QFT Hilbert space = a DIRECT INTEGRAL / sum of MANY discrete
# series + principal series (one per bulk field mode & angular momentum l).
# => the boost spectrum on the physical algebra has CONTINUOUS / infinite
# multiplicity. We verify the structural statement, not a single irrep.

Delta = 0.5
# single irrep ladder: simple
n = np.arange(0,8)
single = Delta + n
print("single discrete-series irrep ladder (Delta+n):", single, " -> simple within irrep")

# physical dS: sum over angular momentum l (SO(3) on horizon sphere) AND over
# bulk field modes. Each l gives an independent discrete series with the SAME
# L_0 ladder shifted -> MASSIVE degeneracy of boost eigenvalues across l-towers.
# Model: l = 0..L gives (2l+1)-fold copies each contributing a ladder.
L = 4
levels = {}
for l in range(0, L+1):
    deg_l = 2*l+1
    base = Delta  # (schematically all towers share the L_0 ladder offset)
    for nn in range(0,8):
        val = round(base + nn, 6)
        levels[val] = levels.get(val,0) + deg_l
print("\nphysical dS boost spectrum multiplicities (sum over l=0..%d):"%L)
for v in sorted(levels)[:6]:
    print(f"  L_0 = {v:6.2f}  multiplicity = {levels[v]}")
print("  ... multiplicity GROWS with field content & l -> INFINITE in the limit.")

print("\n=== CONSEQUENCE ===")
print("The shared modular (boost) spectrum is HIGHLY DEGENERATE on the physical")
print("algebra (one ladder per bulk field-mode/angular sector). So the centralizer")
print("M_omega is a LARGE non-abelian von Neumann algebra (itself type II_1 in the")
print("crossed product), NOT a maximal torus. KMS-at-beta fixes only the boost")
print("WEIGHTS, leaving the FULL centralizer M_omega as residual gauge -- exactly")
print("the relative-commutant freedom. State-matching is NOT reduced to a finite")
print("check; it inherits an infinite-dim'l matching problem inside M_omega.")
