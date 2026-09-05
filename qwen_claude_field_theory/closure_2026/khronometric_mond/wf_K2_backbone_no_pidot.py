#!/usr/bin/env python3
"""
wf_K2_backbone_no_pidot.py  -- ADVERSARIAL test of Carl's ESCAPE claim.

Carl's premise (verbatim in the candidate):
  "the K^2 sector gives the khronon a genuine quadratic kinetic term A(y) pidot^2"
and the existing script wf_decisive_v2_correct.py asserts the K^2 backbone supplies a
CONSTANT A_KH>0 that can be ADDED to Flanagan's h_par so that  A_KH + h_par(y) > 0  for
all y, curing the y>1 longitudinal ghost.

This script tests that premise DIRECTLY by computing the extrinsic curvature K_ij of the
khronon foliation as a perturbation, in flat space (the leading slow-motion background),
and asking: does K_ij K^ij  or  K^2  contain a  d_i(pidot) d_j(pidot)  term at QUADRATIC
order?  If not, the K^2 backbone contributes ZERO to h^{ij} and CANNOT lift h_par.

Setup (leading slow-motion order = flat background; the Newtonian potential only enters
the MOND f-sector, not the extrinsic-curvature normalisation of the ghost):
    g = eta = diag(-1,1,1,1)
    khronon  T = t + eps*pi(t,x1,x2,x3)         (unitary-gauge fluctuation)
    n_a = -d_a T / sqrt(-g^{ab} d_a T d_b T)
    K_ab = h_a^c nabla_c n_b ,  h_a^c = delta_a^c + n_a n^c ,  nabla=partial (flat)
We expand to O(eps^2) and read off the coefficient of pidot-gradients.
"""
import sympy as sp

t, x1, x2, x3, eps = sp.symbols('t x1 x2 x3 eps', real=True)
X = [t, x1, x2, x3]
pi = sp.Function('pi')(t, x1, x2, x3)

# --- flat metric ---
eta = sp.diag(-1, 1, 1, 1)
etaInv = eta  # its own inverse

# --- khronon and its gradient ---
T = t + eps*pi
dT = sp.Matrix([sp.diff(T, xa) for xa in X])          # d_a T  (lower index)

# norm:  N2 = -g^{ab} dT_a dT_b
N2 = 0
for a in range(4):
    for b in range(4):
        N2 += -etaInv[a, b]*dT[a]*dT[b]
N2 = sp.expand(N2)
norm = sp.sqrt(N2)

# n_a = - dT_a / norm   (lower index).  Expand to O(eps^2).
n_low = sp.Matrix([sp.series(-dT[a]/norm, eps, 0, 3).removeO() for a in range(4)])
n_low = sp.Matrix([sp.expand(c) for c in n_low])

# n^a = g^{ab} n_b
n_up = sp.Matrix([sp.expand(sum(etaInv[a, b]*n_low[b] for b in range(4))) for a in range(4)])

# projector h_a^{ c} = delta_a^c + n_a n^c   (mixed)
def proj(a, c):
    return (1 if a == c else 0) + n_low[a]*n_up[c]

# nabla_c n_b = partial_c n_b (flat, Christoffel=0)
def dn(c, b):
    return sp.diff(n_low[b], X[c])

# K_ab = h_a^c h_b^d nabla_c n_d   (fully projected, symmetric spatial tensor)
def K(a, b):
    s = 0
    for c in range(4):
        for d in range(4):
            s += proj(a, c)*proj(b, d)*dn(c, d)
    return sp.expand(s)

print("="*74)
print("STEP 1 -- extrinsic curvature K_ab to LINEAR order in eps")
print("="*74)
Klin = {}
for a in range(4):
    for b in range(a, 4):
        expr = K(a, b)
        lin = sp.expand(expr).coeff(eps, 1)
        Klin[(a, b)] = sp.simplify(lin)
        lbl = ['t', '1', '2', '3']
        print(f"  K_({lbl[a]}{lbl[b]})^(1) =", Klin[(a, b)])

print()
print("  Reading: every LINEAR K_ab piece is a SPATIAL second derivative -d_i d_j pi.")
print("  The time-time and time-space components vanish at linear order, and NO pidot")
print("  (d_t pi) appears in the linear extrinsic curvature.  (pidot enters K only at")
print("  O(eps^2): the cross term d_i pi d_j pidot, which feeds the CUBIC action.)")
print()

print("="*74)
print("STEP 2 -- K_ij K^ij and K^2 to QUADRATIC order: any d(pidot) d(pidot)?")
print("="*74)
# Build spatial K_ij linear tensor (i,j in 1..3) and contract.
KK = 0          # K_ab K^ab  (full contraction with eta)
Ktr = 0         # K = g^{ab} K_ab  (trace)
# use linear K for the quadratic invariants (leading quadratic action)
Kfull_lin = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        aa, bb = (a, b) if a <= b else (b, a)
        Kfull_lin[a, b] = Klin[(aa, bb)]
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                KK += etaInv[a, c]*etaInv[b, d]*Kfull_lin[a, b]*Kfull_lin[c, d]
KK = sp.expand(KK)
Ktr = sp.expand(sum(etaInv[a, b]*Kfull_lin[a, b] for a in range(4) for b in range(4)))
K2 = sp.expand(Ktr**2)

# Does either contain a d_t pi (pidot) factor anywhere?
pidot = sp.diff(pi, t)
def contains_pidot(expr):
    # any derivative w.r.t. t of pi present as a factor?
    ders = expr.atoms(sp.Derivative)
    return any(d.variables.count(t) >= 1 for d in ders)

print("  K_ij K^ij  (quadratic) contains a time derivative of pi? ", contains_pidot(KK))
print("  K^2        (quadratic) contains a time derivative of pi? ", contains_pidot(K2))
print()
print("  K_ijK^ij =", KK)
print()
print("  K^2      =", K2)
print()
print("  Both are purely SPATIAL 4-derivative scalars  (d_i d_j pi)^2 and (nabla^2 pi)^2,")
print("  i.e. exactly Flanagan's Eq (38):  -(c^2/16piG) int [ beta pi_ij pi_ij")
print("  + (lambda+beta/3)(nabla^2 pi)^2 ].  There is NO  d_i(pidot) d_j(pidot)  term.")
print()
print("="*74)
print("VERDICT")
print("="*74)
print("  The K^2 UV backbone contributes ZERO to the h^{ij} tensor (the coefficient of")
print("  d_i(pidot) d_j(pidot) ) at quadratic order.  Its entire quadratic contribution")
print("  is spatial (4-derivative), matching Flanagan Eq (38).  Therefore it CANNOT add")
print("  a positive constant A_KH to h_par.  The longitudinal time-kinetic tensor is")
print("  h_par = (1-W'')/(4piG) = (1-y)e^-y / (4piG) from the MOND sector ALONE, and it")
print("  is NEGATIVE for y>1.  Carl's premise 'A(y) pidot^2 from the K^2 sector, A>=0")
print("  protected' is NOT realised: the K^2 sector makes no pidot^2 at leading order,")
print("  and the actual pidot-kinetic coefficient goes GHOST for a>a0.")
