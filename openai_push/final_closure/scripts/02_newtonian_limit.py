"""Gate 2: Newtonian limit.

Verify that the MOND lapse constraint

    C_M = D_i[ c^2 mu(y) D^i ln N ] - 4 pi G rho_m ,
    y   = (c^2/a0) |D ln N| ,
    mu  = 1 - e^{-y} ,

reduces, for  N = 1 + Psi/c^2 + O(Psi^2/c^4) , to the MOND modified
Poisson equation

    D_i[ (1 - e^{-|D Psi|/a0}) D^i Psi ] = 4 pi G rho_b

with no missing sign or factor.  The key point is that the explicit c^2
in the flux cancels the 1/c^2 from D_i ln N at leading order, while y
itself stays O(1)  (y -> |D Psi|/a0), so the exponential is kept exact.

Method: substitute  c = 1/sqrt(eps)  (so eps = 1/c^2 -> 0) and expand the
flux divergence in eps to O(eps^0), keeping exp(-y) exact.  Then compare
the O(eps^0) operator with the target MOND operator on a concrete radial
potential (so the absolute-value branch is unambiguous).
"""

import sympy as sp

X, Y = sp.symbols("X Y", real=True)
a0, Gc = sp.symbols("a0 G", positive=True)
eps = sp.symbols("eps", positive=True)   # eps = 1/c^2

print("=" * 70)
print("GATE 2: NEWTONIAN LIMIT")
print("=" * 70)

# ------------------------------------------------------------------
# Build the flux divergence as a function of eps, then expand to O(eps^0)
# ------------------------------------------------------------------
def flux_divergence(Psi, vars_):
    """Return D_i[ (1/eps) mu(y) D^i ln N ]  with c^2 = 1/eps."""
    c2 = 1 / eps
    N = 1 + Psi * eps                # N = 1 + Psi/c^2 = 1 + eps*Psi
    lnN = sp.log(N)
    grad = [sp.diff(lnN, v) for v in vars_]
    gradsq = sum(g**2 for g in grad)
    y = c2 / a0 * sp.sqrt(gradsq)    # y = (c^2/a0)|DlnN|
    mu = 1 - sp.exp(-y)
    flux = [c2 * mu * g for g in grad]
    return sum(sp.diff(f, v) for f, v in zip(flux, vars_))

def target_monD(Psi, vars_):
    """Return D_i[ mu(|D Psi|/a0) D^i Psi ]."""
    gP = [sp.diff(Psi, v) for v in vars_]
    yP = sp.sqrt(sum(g**2 for g in gP)) / a0
    muP = 1 - sp.exp(-yP)
    return sum(sp.diff(muP * g, v) for g, v in zip(gP, vars_))

# Use a concrete radial potential so |.| is unambiguous:
#   Psi = A r^2 ,  r^2 = X^2 + Y^2.  Then |D Psi| = 2 A r > 0 (away from 0).
A = sp.symbols("A", positive=True)
Psi = A * (X**2 + Y**2)

divN = flux_divergence(Psi, (X, Y))
divN_series = sp.series(divN, eps, 0, 1).removeO()   # O(eps^0)
target = target_monD(Psi, (X, Y))

print("\n[P.1] test potential Psi = A (X^2+Y^2)")
print("[P.2] flux divergence, O(eps^0)  =", sp.simplify(divN_series))
print("[P.3] target MOND operator       =", sp.simplify(target))

diff_check = sp.simplify(divN_series - target)
print("[P.4] (divN_O0 - target) == 0    :", diff_check == 0)
if diff_check != 0:
    print("[P.4] residual (unsimplified)   =", diff_check)

# ------------------------------------------------------------------
# Also verify the intermediate O(1) pieces explicitly (the c^2 cancellation):
#   dlnN = eps Psi' + O(eps^2)         ->  c^2 dlnN = Psi' + O(eps)
#   y    = |DPsi|/a0 + O(eps)          ->  mu(y) = mu(|DPsi|/a0) + O(eps)
# ------------------------------------------------------------------
print("\n--- intermediate O(1) pieces (c^2 cancellation) ---")
N = 1 + Psi * eps
lnN = sp.log(N)
dlnN_X = sp.diff(lnN, X)
dlnN_X_series = sp.series(dlnN_X, eps, 0, 2).removeO()
print("[P.5] D_X ln N = eps*Psi_X + O(eps^2) :", sp.simplify(dlnN_X_series))
c2_dlnN = sp.series((1/eps) * dlnN_X, eps, 0, 1).removeO()
print("[P.6] c^2 D_X ln N  (O(eps^0))        :", sp.simplify(c2_dlnN),
      " == D_X Psi :", sp.simplify(c2_dlnN - sp.diff(Psi, X)) == 0)

y_expr = (1/eps) / a0 * sp.sqrt(sum(sp.diff(lnN, v)**2 for v in (X, Y)))
y_series = sp.series(y_expr, eps, 0, 1).removeO()
y_target = sp.sqrt(sum(sp.diff(Psi, v)**2 for v in (X, Y))) / a0
print("[P.7] y (O(eps^0))                      :", sp.simplify(y_series))
print("[P.7] |D Psi|/a0                        :", sp.simplify(y_target))
print("[P.7] y == |DPsi|/a0 at O(eps^0)        :",
      sp.simplify(y_series - y_target) == 0)

all_pass = (diff_check == 0)
print("\n" + "=" * 70)
print("GATE 2 RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 70)
