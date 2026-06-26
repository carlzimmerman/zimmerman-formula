#!/usr/bin/env python3
"""
ROUTE 4 (c) -- TRIALITY / Spin(8) ACTION FIXED POINT on flavor space.

QUESTION: Is the 45deg sqrt-mass config a FIXED POINT of the Spin(8)-triality automorphism
(the framework's own symmetry home, per KOIDE_DIRAC_BRIDGE) acting on the 3-dim flavor
space -- defined WITHOUT 2/3? Triality is the order-3 outer automorphism of Spin(8)
permuting the three 8-dim reps (8v, 8s, 8c). On a 3-generation flavor space the relevant
order-3 element is the Z3 cyclic generator (the circulant phase shift). Its fixed-vector
structure is what we test.

The Koide circulant IS already built on the Z3 cyclic action:
    sqrt(m_k) = M (1 + r cos(2pi k/3 + delta)),  k=0,1,2.
The Z3 generator g: k -> k+1 acts on the sqrt-mass vector by CYCLIC PERMUTATION. Its
eigenvectors are the democratic (1,1,1) [eigenvalue 1] and the two circulant modes
(1,w,w^2),(1,w^2,w) [eigenvalues w,w^2], w=exp(2pi i/3). A REAL fixed vector of g is ONLY
the democratic axis (r=0). So the order-3 element has NO fixed vector at r=sqrt2: its only
real invariant is r=0. Triality alone CANNOT select 45deg.

What CAN single out a special r is a SELF-DUALITY / reflection-symmetric condition (a Z2,
not the Z3): the config invariant under the triality REFLECTION that exchanges the two
complex circulant modes. We test whether ANY natural Z2/Z3 invariance condition on the
flavor vector forces r=sqrt2 -- and trace each for a smuggled 2/3.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*80)
print("ROUTE 4(c) -- TRIALITY/Spin(8)/Z3 fixed point at r=sqrt2 ?")
print("="*80)

w = sp.exp(2*sp.pi*sp.I/3)
M, r, delta = sp.symbols('M r delta', positive=True)
ks = [0,1,2]
sqrt_m = [M*(1 + r*sp.cos(2*sp.pi*k/3 + delta)) for k in ks]

# ---------------------------------------------------------------------------
# [1] The Z3 cyclic generator: real fixed vectors are democratic only (r=0).
# ---------------------------------------------------------------------------
print("\n[1] Z3 cyclic generator g (triality order-3 element on 3 generations).")
P = sp.Matrix([[0,1,0],[0,0,1],[1,0,0]])   # cyclic permutation
eigs = P.eigenvects()
print("    cyclic permutation eigen-structure:")
for val, mult, vecs in eigs:
    print(f"      eigenvalue {val} (mult {mult}): {[list(vv) for vv in vecs]}")
print("    => the ONLY REAL eigenvector (eigenvalue 1) is democratic (1,1,1) -> r=0.")
print("       The Z3 element has NO real fixed vector at r=sqrt2. Triality(order-3) alone")
print("       fixes ONLY the symmetric point. (As 4a/4b found from the other side.)")

# ---------------------------------------------------------------------------
# [2] The Z2 'triality reflection' / self-duality. The triality group S3 also contains the
#     reflections (Z2) that fix the 8v and swap 8s<->8c. On the flavor circulant this is the
#     reflection that fixes the democratic + ONE standard axis and flips the other. The
#     SELF-DUAL config (equal weight in the two parts it relates) is the natural fixed locus.
#     Test: 'equal partition of trivial vs standard' = the Z2-self-dual point. Does it = r=sqrt2?
#     (This is the equipartition steelman -- but here as a SYMMETRY fixed-locus, not a thermal
#     argument. We must check if 2/3 is smuggled and if it is forced or a free choice.)
# ---------------------------------------------------------------------------
print("\n[2] Z2 self-duality: |trivial|^2 = |standard|^2 (equal partition) -- IS it forced?")
a,b,c = sp.symbols('a b c', real=True)
v = sp.Matrix([a,b,c])
n = sp.Matrix([1,1,1])
dem = (v.dot(n)/3)*n
std = v - dem
ratio = sp.simplify(std.dot(std)/dem.dot(dem))   # |std|^2/|dem|^2
print("    |std|^2/|dem|^2 (arbitrary v) =", ratio)
# For the circulant this equals r^2/2:
vc = sp.Matrix(sqrt_m)
demc = (vc.dot(n)/3)*n
stdc = vc - demc
ratio_c = sp.simplify(stdc.dot(stdc)/demc.dot(demc))
print("    for the Koide circulant: |std|^2/|dem|^2 =", sp.simplify(ratio_c), " = r^2/2")
sol = sp.solve(sp.Eq(ratio_c, 1), r)   # equal partition
print("    self-dual (ratio=1)  <=>  r^2/2=1  <=>  r =", [s for s in sol if s.is_positive or s==sp.sqrt(2)])
print("    => the Z2-self-dual / equal-partition locus IS r=sqrt(2).  BUT:")
print("       SMUGGLE-TRACE: 'equal partition |std|^2=|dem|^2' is the DEFINITION of cos^2=1/2")
print("       (theta=45deg), which is LOGICALLY IDENTICAL to Q=2/3 (Q=1/(3cos^2)). So")
print("       'demand the self-dual point' == 'demand 45deg' == 'demand 2/3'. It is the")
print("       SAME target re-expressed as a symmetry condition. It is NOT an independent")
print("       principle that DERIVES 45deg -- it RE-LABELS it (the 168th). Triality does NOT")
print("       force equal partition; it permits ANY r (the Z3 acts on the PHASE delta, not r).")

# Prove triality acts on delta (phase) not r (amplitude): the cyclic shift maps
#   delta -> delta + 2pi/3, leaving r and M invariant.
print("\n    PROOF triality moves phase not amplitude:")
shifted = [M*(1 + r*sp.cos(2*sp.pi*k/3 + (delta + 2*sp.pi/3))) for k in ks]
# this should be a cyclic permutation of the original sqrt_m
orig_set = sqrt_m
print("    g: delta -> delta+2pi/3 gives the cyclic permutation of the SAME (M,r) triple:")
diff = sp.simplify(sp.Matrix(shifted) - P*sp.Matrix(sqrt_m))
print("    [shifted - P.original] =", list(diff), " (zero => g only permutes; r,M untouched)")
print("    => r is a TRIALITY-INVARIANT modulus. The symmetry says NOTHING about its value.")
print("       r=sqrt2 is NOT a triality fixed point; it is a free modulus on the triality orbit.")

# ---------------------------------------------------------------------------
# [3] Is there a triality-INVARIANT POTENTIAL whose min is at equal partition? That just
#     re-imports 4a: V(r) S3-invariant -> extremum at r=0 or tuned. Confirm equal-partition
#     is NOT the extremum of |std|^2/|dem|^2 (it's a level set, monotone in r, no interior
#     extremum). So no triality-invariant dynamics PREFERS the self-dual point.
# ---------------------------------------------------------------------------
print("\n[3] Does triality-invariant dynamics PREFER equal partition? (is r=sqrt2 an extremum?)")
rr = sp.symbols('rr', positive=True)
partition_ratio = rr**2/2     # |std|^2/|dem|^2
dV = sp.diff(partition_ratio, rr)
print("    d/dr (|std|^2/|dem|^2) = d/dr(r^2/2) =", dV, " -> zero only at r=0 (no extremum at sqrt2).")
print("    The self-dual VALUE 1 is a generic level, not a stationary point. No dynamics")
print("    selects it without a tuned potential (= 4a smuggle).")

print("""
[VERDICT 4c] Spin(8)-triality does NOT non-circularly fix r=sqrt2:
  - The Z3 (order-3) triality element fixes ONLY the democratic axis (r=0); it acts on the
    circulant PHASE delta, leaving r a TRIALITY-INVARIANT FREE modulus.
  - The Z2 'self-dual / equal-partition' locus IS r=sqrt2, but 'equal partition |std|^2=
    |dem|^2' is LOGICALLY IDENTICAL to cos^2=1/2 = 45deg = Q=2/3 -> it RE-LABELS the target,
    does not derive it (smuggle confirmed by sympy: the condition == the answer).
  - No triality-invariant dynamics has an extremum at the self-dual point (r^2/2 is monotone).
  Triality gives the 1+2 decomposition (real, forced) but NOT the length ratio. NULL.
""")
